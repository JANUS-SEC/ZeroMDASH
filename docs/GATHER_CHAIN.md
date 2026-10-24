# Gather mode：跨 workspace 攻击链聚合方案

本文设计一个新的 `--scan-mode gather`。它不重新扫描目标，也不等同于现有
`target_repos` 多仓库模式；它消费多个已经完成的 ZeroMDASH workspace，在一个
共同业务场景下重新建立跨目标数据流、信任边界和攻击能力传递关系，再产出只属于
该场景的跨目标攻击链报告。

建议的逻辑流程是：

```text
gather_analyze_attack_surface
  -> gather_plan_chains
  -> [gather_chain_subtask]*
  -> gather_prepare_report_groups
  -> summary
  -> polish_report
```

LangGraph 的实际实现需要一个纯路由节点完成动态 fan-out：

```text
START
  -> gather_analyze_attack_surface
  -> gather_plan_chains
  -> dispatch_gather_chains
       -> no candidate ------------------------+
       -> N x gather_chain_subtask              |
              -> gather_chain_investigate_subtask
              -> gather_chain_critic_subtask
                    -> revise -> gather_chain_investigate_subtask
                    -> close  -> gather_finalize_chain_subtask
       -> gather_prepare_report_groups <--------+
  -> summary
  -> polish_report
  -> END
```

其中 `dispatch_gather_chains` 和 `gather_finalize_chain_subtask` 是实现所需的内部
节点，不改变用户看到的逻辑阶段。前者只做 `Send` 路由，后者只做闭包、引用和
资格校验。

## 1. 设计结论

### 1.1 gather 必须是独立 graph

现有 `build_graph()` 假定一次运行只有一个顶层 workspace、一个 `repo_path`、一个
attack-surface report 和一个 Domain Registry。当前 `ChainSubtaskInputState` 同样只
携带一个 `repo_path`、`attack_surface` 和 `domain_registry`。如果只在现有节点里增加
若干路径列表，会同时产生四类问题：

- 不同 workspace 的 `PRIM-*`、`ENT-*`、`INV-*` 和 `CHAIN-*` ID 会碰撞；
- agent 无法判断一条证据、一个版本约束或一段代码属于哪个 target；
- 当前 agent sandbox 只显式开放当前 task workspace，未定义多个源 workspace 的
  只读访问语义；
- 当前 `summary` 会把 source workspace 的 standalone finding 当成本次扫描结果，
  造成重复报告，而 gather 应只报告新的跨目标闭包。

因此新增 `build_gather_graph()` 和 `run_gather()`，使用独立的 `GatherState`。共享
现有 agent invocation、qualification、report formatting 等基础设施，但不让
`ZeroMDASHState` 同时承担单目标扫描和联邦聚合两种语义。

### 1.2 gather 是二阶段分析，不修改源 workspace

源 workspace 是已完成扫描的证据源，必须保持只读。gather 运行创建自己的输出
workspace，并在启动时把结构化产物复制成带哈希的输入快照。V1 同时把源码复制到
gather workspace 的隔离 snapshot（排除 `.git`、`.zeromdash` 等元数据），agent
只读取该副本，避免只支持 writable `--add-dir` 的 runtime 修改源 workspace。V1
不跟随源码树中的符号链接；依赖外部 symlink target 的源码必须作为显式 target/repo
输入，否则 preflight 应把它记录为 coverage limitation。

```text
source workspace A --+
source workspace B --+--> gather input snapshot --> gather graph --> gather workspace
source workspace C --+
```

这样可以保证：

- gather 的日志、候选、chain result 和 summary 不污染任何源扫描；
- 一次 gather 运行消费的是固定证据快照，源日志后续变化不会静默改变当前结果；
- 报告中的每个结论都能追溯到 target、workspace、artifact、JSON pointer 和代码位置。

### 1.3 Agent-Native 的边界

Agent 负责需要语义判断的工作：

- 从共同业务场景推断目标间的真实交互拓扑；
- 识别协议、对象、身份、权限和生命周期状态在目标间如何传递；
- 判断名字不同但语义相同的 capability 是否能绑定；
- 发现单目标扫描没有显式表达的 emergent impact；
- 对每个跨目标 edge 做正反论证，并决定证据是否足够。

Python 只负责不能交给自然语言推理的硬约束：

- YAML/JSON schema、路径和 workspace 完整性检查；
- 输入快照、SHA-256、稳定排序和 ID namespace；
- active result 选择、陈旧 artifact 排除和 reducer merge；
- source reference、target transition、primitive/chain ID 的引用完整性；
- 资格门槛、CVSS 格式、输出文件和报告结构校验。

确定性代码可以提供候选或冲突 advisory，但不得用字符串完全匹配作为语义真值，
也不得在 agent 判断前硬裁掉 capability near-match 或 emergent-impact 路径。

## 2. CLI 契约

新增：

```text
--scan-mode full|diff|gather
--gather-workspace-to-chain MULTI_TARGET_CONFIG.yaml
```

推荐命令：

```bash
zeromdash \
  --scan-mode gather \
  --gather-workspace-to-chain ./multi-target-config.yaml \
  --agent-config ./zeromdash.gather.yaml \
  --workspace-root ./.zeromdash
```

可直接运行的示例在 `demo/gather-multi-target-config.example.yaml`（manifest）和
`demo/gather-agent-config.example.yaml`（gather 节点配置）；示例中的相对路径都相
对于 manifest 所在目录解析，因此从仓库根目录执行时用
`--gather-workspace-to-chain demo/gather-multi-target-config.example.yaml` 即可。

`--agent-config` 在 gather 模式下配置本次 gather graph 的 runtime、model、focus、
并发和 chain budget。manifest 中每个 target 的 `agent_config` 则描述源扫描所使用的
配置和 threat context；两者职责不同，不能隐式选择“第一个 target 的 runtime”作为
gather runtime。

如果 CLI 未传 `--agent-config`，可以读取 manifest 可选的
`gather_agent_config`；两者都没有时使用 gather 节点默认 backend。CLI 显式参数优先。

### 2.1 参数校验矩阵

| 条件 | 行为 |
| --- | --- |
| `scan_mode=gather` 且缺少 `--gather-workspace-to-chain` | 启动前失败 |
| `scan_mode=full/diff` 且提供该参数 | 启动前失败 |
| gather 与 `--target`、`--diff-file`、`--diff-git` 同用 | 启动前失败 |
| gather 与 `--preset-attack-surface` 同用 | 启动前失败 |
| gather 与 `--disable-spec`、`--disable-target-history`、`--disable-new-feature` 同用 | 启动前失败；这些 track 已经在源 workspace 完成 |
| gather 与 `--disable-chain` 同用 | 启动前失败；与模式目的矛盾 |
| manifest 少于两个 target | 启动前失败 |
| target name 重复或 namespace 后碰撞 | 启动前失败 |
| workspace 不存在、不是目录或缺少 `workspace.json` | 启动前失败 |
| 缺少 attack-surface 内容或没有任何可用 chain evidence | 启动前失败并列出 target |
| `agent_config` 不存在或 YAML 无法解析 | 启动前失败 |

V1 不把 gather 混入现有 `--start-from-subtask`、`--start-from-chain` 和
`--start-from-summary`。后续需要恢复能力时，增加明确的
`--start-from-gather-chain <gather-workspace>`，不要让单目标 restore loader 猜测
workspace 类型。

### 2.2 CLI 分派

`main()` 应在现有 full/diff 参数交叉校验和 backend health check 之前识别 gather：

```python
if scan_mode == "gather":
    manifest = load_gather_manifest(gather_workspace_to_chain)
    gather_agent_configs = resolve_gather_agent_config(...)
    enabled_nodes = GATHER_GRAPH_NODES
    selected_backends = resolve_startup_backends_for(enabled_nodes, ...)
    final = run_gather(manifest=manifest, ...)
else:
    final = run(...)
```

不能继续沿用“从 `DEFAULT_BACKENDS` 减去 disabled nodes”的方式计算健康检查集合，
否则 gather 启动时会无意义地检查 `search_spec`、`plan_by_*` 等不会运行的节点。

## 3. multi-target-config.yaml

建议 V1 schema：

```yaml
schema_version: "1.0"

# 可选；缺省使用配置文件名。用于 gather workspace 名称和报告标题。
name: payment-control-plane

# 必填；描述这些 target 如何共同工作，而不是泛化的安全审计方法论。
scenario: >
  External tenants submit deployment requests to api-gateway. The gateway
  authenticates the caller and forwards a normalized workload specification to
  scheduler. Scheduler selects a worker and sends an execution request to
  runtime-agent. The runtime agent mounts tenant-provided artifacts and reports
  status back through scheduler to api-gateway.

# 可选；CLI --agent-config 的 fallback。它配置 gather 节点本身。
gather_agent_config: ./zeromdash.gather.yaml

targets:
  - name: api-gateway
    agent_config: ./configs/api-gateway.yaml
    workspace: ./.zeromdash/workspace_for_api-gateway
    role: northbound API, authentication and request normalization

  - name: scheduler
    agent_config: ./configs/scheduler.yaml
    workspace: ./.zeromdash/workspace_for_scheduler
    role: placement, policy propagation and worker selection

  - name: runtime-agent
    agent_config: ./configs/runtime-agent.yaml
    workspace: ./.zeromdash/workspace_for_runtime-agent
    role: privileged workload materialization and execution
```

约束：

- `schema_version`、`scenario` 和 `targets` 必填；`scenario` trim 后不能为空；
- `targets` 至少两个；每项的 `name`、`agent_config`、`workspace` 必填；
- 所有相对路径都相对于 multi-target config 所在目录解析，不相对于当前 shell；
- `name` 经 `slugify()` 后必须唯一，建议原始值也限制为
  `[A-Za-z0-9_.-]+`，避免同形 namespace；
- `role` 可选，只描述该 target 在共同场景中的职责；
- target 的 `agent_config` 只提取 `common_focus`、target/repository 描述和与证据
  解释有关的 focus。不得继承其 runtime、model、provider、env 或 fallback，更不能把
  其中的 secret 写入 snapshot、prompt 或 `final_state.json`；
- manifest 自身和解析后的 canonical form 都写入 gather workspace；后续报告引用
  canonical form。

建议给 manifest 增加 JSON Schema：

```text
zeromdash/presets/contracts/gather-targets.schema.json
```

## 4. gather workspace

输出仍使用 `Workspace` 的基本能力，但增加显式的 `inputs/` 和 gather 专属日志目录：

```text
workspace_for_gather_<name>/
  workspace.json
  gather_manifest.yaml
  inputs/
    manifest.normalized.json
    gather_inputs.lock.json
    <target_id>/
      workspace.json
      source_context.json
      attack_surface/
        ...                         # main/attack_surface/ 的快照
      primitive_res/
        ...                         # active、合法的 primitive envelope
      subtask_res/
        ...                         # active terminal result envelope
      chain_res/
        ...                         # confirmed chain_finding envelope
  main/
    attack_surface/
      gather_attack_surface.md
      cross_target_registry.json
  log/
    state/
      gather_evidence_pool.json
      gather_chain_plan.json
    review_log/
      gather_*.log
    gather_chain_res/
      <gchain-id>.json
    gather_chain_candidates/
      <gchain-id>.json
    gather_report_groups.json
    agent_commands.jsonl
  sub_workspace/
    node_gather_analyze_attack_surface/
    node_gather_plan_chains/
    node_gather_chain_investigate_subtask/subtask_<gchain-id>/
    node_gather_chain_critic_subtask/subtask_<gchain-id>/
  summary.en.md
  summary.zh_CN.md
  summary.md
  gate_result.json
  final_state.json
```

不要把 gather 结果写进现有的 `log/chain_res`。目录名分开可以防止单目标 restore
loader 把跨目标 finding 当成普通 `ChainFinding`。

### 4.1 输入快照与漂移检测

CLI preflight 在建图前完成以下步骤：

1. canonicalize manifest、workspace 和 agent-config 路径；
2. 读取 `workspace.json` 和可选 `final_state.json`；
3. 选择 active subtask results，沿用现有 canonical `subtask_res` 覆盖 legacy
   `review_res` 的规则；
4. 沿用 `declared_package_ids()` / `primitive_has_package_source()` 语义，避免把旧
   package 遗留的 `primitive_res` 重新带回；
5. `chain_res` 只接受 `outcome_type=chain_finding`，拒绝 candidate、inconclusive
   和格式不完整的文件；
6. 复制被选中的 JSON 和 `main/attack_surface/` 内容，记录每个文件的 SHA-256；
7. 记录源码根、git HEAD、dirty status 摘要和源 workspace schema/version；
8. 输出 `gather_inputs.lock.json`，之后所有结构化读取只来自 snapshot。

对于支持当前 schema 的 workspace，active chain result 应优先由当前
`final_state.chain_findings` / `report_groups` 反向确认；旧 workspace 没有这两项时，
可以读取合法的 `chain_res` envelope，但必须标记 `legacy_activity_unverified=true`，
并要求 gather battle 重新核对其 constituent evidence。不能仅因目录中存在 JSON 就
把历史重跑遗留结果视为当前有效结果。

agent 需要回查源代码时，通过 `source_context.json` 定位 gather workspace 内的源码
snapshot。运行结束前仍重新检查原始源码的 git HEAD 和 dirty status 摘要（非 git
目录使用 tree hash）；发生漂移时，不得静默确认 chain，应将相关 candidate 标为
`source_drift` 并使 gate fail closed。

### 4.2 多 workspace sandbox

当前 agent adapter 只从当前 `sub_workspace` 推导一个 task workspace，并对部分
runtime 使用 `--add-dir <workspace_base>`。gather 需要在 invocation contract 中增加：

```python
additional_read_roots: list[str]
```

它只来自 manifest 中已经 canonicalize 且通过 preflight 的源码根。各 runtime 应映射
到真正的只读授权；如果某 runtime 只能把额外目录授权为可写，则默认不直接挂载源
workspace，而是使用只读 snapshot/worktree。不能仅靠 prompt 中的“请勿修改”代替
权限隔离。

## 5. State 与核心数据契约

建议新增 `zeromdash/gather_state.py`，避免继续扩大单目标 `ZeroMDASHState`。

### 5.1 GatherTarget

```python
class GatherTarget(TypedDict, total=False):
    target_id: str
    name: str
    role: str
    workspace_path: str
    agent_config_path: str
    source_roots: list[str]
    source_scan_mode: str
    source_revision: dict[str, Any]
    source_common_focus: str
    snapshot_root: str
    artifact_hashes: dict[str, str]
```

`target_id` 是稳定 namespace。所有源 ID 都转换为：

```text
<target_id>::<local-id>
```

如果一个源 workspace 本身包含 `target_repos`，则 repo 级引用使用：

```text
<target_id>::<repo-id>::<local-id>
```

原始 ID 必须保留在 `source_ref.local_id`，不能只保留改写后的字符串。

### 5.2 SourceRef

每条进入 gather 的事实都必须带统一 provenance：

```json
{
  "target_id": "scheduler",
  "workspace_id": "workspace_for_scheduler",
  "artifact_kind": "primitive_res",
  "artifact_path": "inputs/scheduler/primitive_res/prim-004.json",
  "artifact_sha256": "...",
  "json_pointer": "/capabilities_gained/0",
  "local_id": "PRIM-004",
  "repo_id": "scheduler-core",
  "revision": "<git sha>",
  "code_locations": ["pkg/queue/dispatch.go:418"]
}
```

任何无法落到 `SourceRef` 的“可能”“常见设计”只能成为 hypothesis 或 deployment
assumption，不能成为已确认 edge。

### 5.3 GatherEvidenceUnit

源 artifact 不能原样扔给 planner。preflight normalizer 将其转成统一 evidence unit：

```json
{
  "unit_id": "scheduler::PRIM-004",
  "unit_kind": "primitive",
  "target_id": "scheduler",
  "component": "placement-cache",
  "entry_conditions": {},
  "required_capabilities": [],
  "attacker_controls": [],
  "capabilities_gained": [],
  "handoff_objects": [],
  "required_entity_states": [],
  "resulting_entity_states": [],
  "terminal_impact": {},
  "constraints": {
    "versions": [],
    "config": [],
    "identity": [],
    "deployment": []
  },
  "source_refs": []
}
```

`unit_kind` 有三种：

- `primitive`：来自有效的 `primitive_res` 或 active `subtask_res.primitive`；
- `standalone_finding`：来自通过 qualification gate 且具有 capability view 的
  `subtask_res.finding`；
- `local_chain`：来自已确认 `chain_res.finding`，作为不可拆掉证据约束的
  macro-primitive。它保留 constituent primitive IDs、bindings 和 closure facts。

`local_chain` 可以参与跨目标组合，但不能与其 constituent primitives 在同一候选中
重复计分，也不能因为源 chain 已确认，就自动证明跨 target handoff 成立。

相同 unit 的去重优先级固定为：active `subtask_res` envelope 中的 primitive 高于同名
`primitive_res`，canonical `subtask_res` 高于 legacy `review_res`，同一 source hash
只保留一次。发生内容冲突时不做 last-write-wins，而是记录 `input_conflict` 并阻止相关
unit 进入 confirmed pool。

`observation`、`rejected`、`inconclusive` 和未通过 qualification 的 finding 不进入
evidence pool。它们可放入 `context_only` 供 agent 了解负证据，但不能被 binding 引用
为 provider。

### 5.4 CrossTargetRegistry

`gather_analyze_attack_surface` 的 JSON 输出至少包含：

```json
{
  "schema_version": "1.0",
  "scenario": "...",
  "targets": [],
  "interfaces": [],
  "data_flows": [
    {
      "flow_id": "FLOW-001",
      "producer_target_id": "api-gateway",
      "consumer_target_id": "scheduler",
      "data_object": "normalized workload specification",
      "transport": "RPC",
      "producer_representation": "...",
      "consumer_representation": "...",
      "trust_transition": "authenticated tenant -> scheduler service identity",
      "security_controls": [],
      "identity_mapping": [],
      "lifecycle": [],
      "source_refs": [],
      "confidence": 0.0,
      "status": "confirmed"
    }
  ],
  "cross_target_invariants": [],
  "deployment_assumptions": [],
  "unresolved_gaps": []
}
```

`status` 至少区分 `confirmed`、`scenario_asserted`、`hypothesized` 和 `contradicted`。
只有 `confirmed` 可以直接支撑最终 chain edge；`scenario_asserted` 必须在 chain battle
中补齐部署或代码证据。

### 5.5 GatherChainCandidate

```json
{
  "schema_version": "1.0",
  "chain_id": "GCHAIN-<stable-hash>",
  "target_sequence": ["api-gateway", "scheduler", "runtime-agent"],
  "ordered_unit_ids": [
    "api-gateway::PRIM-002",
    "scheduler::CHAIN-003",
    "runtime-agent::PRIM-011"
  ],
  "attacker_entry": {},
  "bindings": [
    {
      "provider_unit_id": "api-gateway::PRIM-002",
      "consumer_unit_id": "scheduler::CHAIN-003",
      "flow_id": "FLOW-001",
      "provided_capability": {},
      "required_capability": {},
      "handoff_object": {},
      "compatibility_reason": "...",
      "source_refs": []
    }
  ],
  "global_constraints": {},
  "expected_terminal_impact": {},
  "emergent_impact_hypothesis": {},
  "rank_score": 0.0,
  "agent_reasoning": "...",
  "deterministic_advisories": []
}
```

`chain_id` 应由 normalized candidate 内容计算稳定 hash，而不是按 agent 返回顺序编号。
至少将 `target_sequence`、`ordered_unit_ids`、binding endpoints 和 flow IDs 纳入 hash。

### 5.6 GatherState

顶层状态只保留汇总流程需要的数据：

```python
class GatherState(TypedDict, total=False):
    scan_mode: str
    scenario_name: str
    scenario: str
    manifest_path: str
    manifest_hash: str
    task_id: str
    workspace_root: str
    role_lang: str
    gather_targets: list[GatherTarget]
    source_read_roots: list[str]
    input_lock_path: str
    agent_configs: dict[str, dict[str, Any]]
    common_focus: str
    top_K: dict[str, int]
    gather_config: dict[str, Any]
    gather_attack_surface: str
    cross_target_registry_path: str
    cross_target_registry: dict[str, Any]
    gather_evidence_pool: list[GatherEvidenceUnit]
    gather_evidence_pool_path: str
    gather_chain_plan: list[GatherChainCandidate]
    gather_chain_plan_path: str
    gather_chain_candidates: Annotated[list[dict[str, Any]], operator.add]
    gather_chain_findings: Annotated[list[dict[str, Any]], operator.add]
    gather_report_groups: list[dict[str, Any]]
    gather_report_groups_path: str
    summary: str
    summary_en: str
    summary_zh_CN: str
    gate_result: dict[str, Any]
    errors: Annotated[list[str], operator.add]
```

另建 `GatherChainSubtaskInputState`、`GatherChainSubtaskState` 和
`GatherChainSubtaskOutputState`，以 nested graph 隔离每条候选的 iteration、
investigation、review 和 history。

## 6. 节点设计

### 6.1 gather_analyze_attack_surface

输入：

- manifest 中的共同 `scenario`；
- 每个 target 的 role、sanitized source config context；
- 每个 snapshot 下的完整 `attack_surface/`；
- 每个 target 的 source revision 和 repo registry；
- 可选的 source observation 作为负证据背景。

输出：

- `main/attack_surface/gather_attack_surface.md`：面向人的跨目标数据流和信任边界；
- `main/attack_surface/cross_target_registry.json`：供后续节点消费的结构化拓扑。

该节点不是把多个 `attack_surface.md` 拼接起来，而是回答：

1. 哪个 target 生产什么对象、凭据、标识、状态或 capability；
2. 哪个 target 消费它，期间经过何种序列化、传输、鉴权和权限映射；
3. producer 与 consumer 对同一字段或状态有哪些不一致假设；
4. 跨 target 后哪些校验丢失、哪些状态变成 authoritative、哪些缓存或 fallback
   会改变语义；
5. 哪些场景连接有双侧证据，哪些仅由 scenario 声明，哪些仍未知。

Agent-Native 分工建议：

- 每个 target 一个 bounded reader subagent，提取 ingress、egress、对象和 trust
  boundary；
- 一个 interaction mapper 按 scenario 建立有向数据流；
- 一个 boundary critic 专门查找身份、格式、生命周期和 fallback 语义不一致；
- parent agent 汇总、消歧并生成两个最终 artifact。

不要机械地产生全部 target 的 `N x (N-1)` 配对。先由 scenario 和 target role 产生
候选交互，再对有证据的有向 pair 深挖；`gather.max_pair_passes` 只作为成本上限。

### 6.2 gather_plan_chains

该节点启动时由确定性 helper 生成 `gather_evidence_pool.json`，然后让 agent 基于：

- normalized evidence units；
- cross-target registry；
- scenario；
- deterministic compatibility/conflict advisories；
- `top_K.chain` 和 gather budget；

生成值得进入 battle 的候选。

建议 native subagents 分别做：

- forward composition：从攻击者入口沿 capability/data-flow 向后扩展；
- backward composition：从高价值 terminal impact 反推必要能力；
- seam composition：从 `FLOW-*`、identity mapping、representation mismatch 和
  lifecycle transition 出发找组合；
- constraint review：检查版本、配置、部署、身份、时序和对象一致性；
- adversarial pruning：专门证明候选为什么不成立，抑制故事化拼接。

parent agent 最后统一 reconcile。deterministic prefilter 只能是 advisory：即使字段名
不一致，只要双侧代码和语义支持，agent 可以修复 binding；但不能发明不存在的 source
unit、flow 或未确认的 exploit step。

V1 默认只分发满足以下条件的候选：

- `target_sequence` 至少包含两个不同 target；
- 至少一条 binding 跨 target；
- 所有 `ordered_unit_ids` 存在于 evidence pool；
- 所有跨 target binding 引用存在的 `FLOW-*`，或明确标为 battle 必须验证的
  `scenario_asserted` flow；
- 候选没有重复使用同一 local chain 及其 constituent primitive；
- 候选数量不超过 `top_K.chain`。

无候选不是错误。节点写出空 `chains`、明确的 `reason/notes`，然后路由到
`gather_prepare_report_groups`，最终 summary 说明未形成已验证的跨目标攻击链。

### 6.3 gather_chain_subtask

每条 candidate 进入独立 nested graph：

```text
START
  -> gather_chain_investigate_subtask
  -> gather_chain_critic_subtask
       -> revise: gather_chain_investigate_subtask
       -> close/max rounds: gather_finalize_chain_subtask
  -> END
```

investigator 必须逐 edge 给出：

- producer 侧生成、控制或污染对象的代码/事实证据；
- 实际传输、共享存储或控制面交互证据；
- consumer 侧解析、信任、状态转换和 sink 证据；
- 身份、权限、版本、配置、部署和时序约束；
- attacker 从初始能力到最终 C/I/A impact 的完整因果链；
- 对 source workspace 原结论的复核，而不是只引用其标题。

critic 使用与现有 chain 相同的 `closure_verdict + fact_verdicts` 思路，但 fact ID
必须覆盖所有：

- source unit；
- local binding；
- cross-target binding；
- scenario/deployment assumption；
- terminal impact；
- 反证和影响边界。

建议 verdict 为 `confirmed | rejected | unknown`。任何必要事实为 `unknown` 时，chain
不得确认；critic 可以要求下一轮 investigator 补证。第一轮无 finding 同样不能直接
结束，至少要完成一次反向路径/替代接口检查。

### 6.4 gather_finalize_chain_subtask

finalizer 先跑确定性硬门槛，再允许 native-subagent finalizer 处理“结构检查失败但
语义证据完整”的有限情况。硬门槛至少包括：

- 所有 unit、flow、target 和 source ref 存在；
- chain 顺序、binding endpoints 和 agent investigation 一致；
- 至少两个 target，且至少一个 confirmed cross-target edge；
- 每个必要 fact 有显式 verdict，不能把 legacy/unknown 静默当 confirmed；
- 全局版本、配置、部署、身份和时序约束可同时满足；
- 不依赖 evidence pool 外的未确认 primitive；
- 终点是直接 C/I/A impact，而不是“可进一步利用”；
- `source_drift=false`；
- CVSS v4.0 只在整条 gather chain 闭合后计算。

native finalizer 只能解释 contract 表达差异，例如同义 capability 的字段映射；它
不能覆盖缺失 source ref、未知必要事实、单目标候选、没有真实跨目标 edge、互斥全局
约束或 source drift 等硬失败。

成功写入 `log/gather_chain_res/<gchain-id>.json`；失败或不确定写入
`log/gather_chain_candidates/<gchain-id>.json`。失败候选不能进入报告 finding。

### 6.5 gather_prepare_report_groups

这个节点只消费 `gather_chain_findings`，不把源 workspace 的 standalone finding
单独再报一遍。源 finding/primitive/local chain 只作为 provenance 和链中步骤出现。

先按稳定 key 做确定性分组：

```text
terminal security property
+ final impact target
+ final root-cause anchor
+ normalized target sequence
```

然后可调用 native-subagent `gather_report_group_adjudicator` 识别语义重复：相同根因
经不同中间 target 或相同攻击路径的证据变体可合并，但不能把不同 trust boundary、
不同最终 impact 或互斥部署条件的 chain 合并。

### 6.6 summary 与 polish_report

graph 中仍使用节点名 `summary`，但 `build_gather_graph()` 应把它绑定到
`gather_summary()`，不要让现有单目标 `summary()` 通过大量 `if scan_mode` 承担两套
输入契约。

gather summary 只消费 `gather_report_groups` 和 cross-target registry，报告至少包含：

- 共同业务场景和 target 角色；
- 被确认和未确认的 target 间数据流；
- 每条漏洞的跨目标攻击路径；
- 每个 edge 的双侧代码/日志证据与 source workspace provenance；
- 必要部署、版本、配置、身份和时序条件；
- 数据流图和攻击时序图；
- 最终 impact、影响 target、CVSS v4.0 和范围边界；
- 未闭合候选与证据缺口摘要，但不把它们编号为 `VULN-*`。

`polish_report` 可以复用现有节点，只需让报告结构诊断器接受 gather 报告增加的
“Target topology / 目标拓扑”和“Cross-target bindings / 跨目标绑定”章节。

`gate_result.json` 增加：

```json
{
  "scan_mode": "gather",
  "scenario": "payment-control-plane",
  "source_workspaces": [],
  "decision": "block",
  "blocking_findings": [],
  "warning_findings": [],
  "unclosed_candidates": [],
  "input_lock_hash": "..."
}
```

## 7. Agent 配置

gather coordinator config 建议复用现有 YAML 结构并新增 `gather` 段：

```yaml
common_focus: >
  Attacker Profile: untrusted tenant controls northbound workload requests.
  Impact Boundaries: cross-service authorization bypass, tenant isolation loss,
  or privileged code execution on runtime workers.
  Technical Lifecycle Focus: request normalization, identity propagation,
  placement, artifact materialization, execution and status callbacks.
  Exclusions: availability-only overload without a violated isolation contract.

max_concurrency: 8

top_K:
  chain: 16

gather:
  max_pair_passes: 12
  max_chain_length: 6
  max_candidates_before_top_k: 200
  max_battle_rounds: 3
  require_cross_target: true

node:
  gather_analyze_attack_surface:
    runtime: claude_code
    config: bedrock
    focus: ""

  gather_plan_chains:
    runtime: codex
    config: ark
    focus: ""

  gather_chain_investigate_subtask:
    runtime: codex
    config: ark
    focus: ""

  gather_chain_critic_subtask:
    runtime: codex
    config: ark
    focus: ""

  gather_chain_finalizer_subtask:
    runtime: codex
    config: ark
    focus: ""

  gather_report_group_adjudicator:
    runtime: codex
    config: ark
    focus: ""

  summary:
    runtime: claude_code
    config: bedrock

  polish_report:
    runtime: claude_code
    config: bedrock
```

以下节点应加入 `NATIVE_SUBAGENT_REQUIRED_NODES`：

```text
gather_analyze_attack_surface
gather_plan_chains
gather_chain_investigate_subtask
gather_chain_critic_subtask
gather_chain_finalizer_subtask
gather_report_group_adjudicator
summary
```

`dispatch_gather_chains`、evidence normalization 和 deterministic final gate 不调用
agent，因此不进入 backend config。

## 8. 建议模块边界

新增：

```text
zeromdash/gather.py
zeromdash/gather_graph.py
zeromdash/gather_state.py
zeromdash/nodes/gather_analyze_attack_surface.py
zeromdash/nodes/gather_plan_chains.py
zeromdash/nodes/dispatch_gather_chains.py
zeromdash/nodes/gather_chain_investigate_subtask.py
zeromdash/nodes/gather_chain_critic_subtask.py
zeromdash/nodes/gather_finalize_chain_subtask.py
zeromdash/nodes/gather_prepare_report_groups.py
zeromdash/nodes/gather_summary.py
zeromdash/nodes/core/gather_evidence.py
zeromdash/nodes/core/gather_qualification.py
zeromdash/presets/contracts/gather-targets.schema.json
zeromdash/presets/contracts/cross-target-registry.schema.json
zeromdash/presets/contracts/gather-chain-plan.schema.json
zeromdash/presets/contracts/gather-chain-investigation.schema.json
zeromdash/presets/contracts/gather-chain-review.schema.json
zeromdash/presets/contracts/gather-chain-finalizer.schema.json
zeromdash/presets/roles/gather_*.md
zeromdash/presets/roles/zh_CN/gather_*.md
```

修改：

- `zeromdash/cli.py`：增加 mode/option、manifest 分派和 gather-only 参数校验；
- `zeromdash/workspace.py`：增加 gather workspace materialization，或引入
  `GatherWorkspace` 子类；
- `zeromdash/agents.py` 与 `nodes/core/invocation.py`：增加明确的 read roots；
- `zeromdash/presets.py`：注册 gather contracts 和 native-subagent 节点；
- `zeromdash/nodes/core/constants.py`：默认 backend、节点集合和 aliases；
- `zeromdash/nodes/__init__.py`：导出 gather nodes；
- `zeromdash/prompts.py`：新增 gather prompt；
- `README.md` / `ARCH.md`：CLI 和总架构入口，细节链接到本文。

共享现有实现时优先抽取纯函数，而不是让 gather 伪装成单目标 state：

- active subtask artifact 选择；
- primitive/finding qualification；
- stable JSON write、artifact-first retry；
- CVSS v4.0 校验；
- report group 的机械校验和 Markdown diagnostics。

## 9. 失败语义与可观测性

所有 agent node 继续使用 artifact-first validation。`rc=0` 只表示 backend 进程正常
退出，不代表 gather artifact 合法；最终以 attempt log 的 `validation_status` 为准。

建议每个 attempt header 增加：

```json
{
  "scan_mode": "gather",
  "scenario": "payment-control-plane",
  "manifest_hash": "...",
  "input_lock_hash": "...",
  "target_ids": ["api-gateway", "scheduler", "runtime-agent"],
  "chain_id": "GCHAIN-...",
  "validation_status": "valid"
}
```

失败分三层记录：

- `input_error`：manifest、路径、workspace 或 source schema 不合法，graph 不启动；
- `agent_error`：runtime、timeout 或结构化输出失败，按现有 retry/fallback 处理；
- `qualification_failure`：agent 能完成分析，但 cross-target closure 不成立，保留为
  candidate，不升级为 vulnerability。

`final_state.json` 不嵌入所有源 artifact 全文，只记录 canonical paths、hash、计数和
最终 state，避免文件过大。完整证据在 `inputs/` 和 gather result 目录中。

## 10. 测试方案

### 10.1 CLI 与 manifest

- `--help` 展示 `full|diff|gather` 和新参数；
- gather 缺参数、非 gather 带参数、与 diff/target/restore 组合时正确失败；
- 相对路径按 manifest 目录解析；
- duplicate name、slug collision、少于两个 target、空 scenario 被拒绝；
- target agent config 的 `env` 不进入 snapshot、prompt 或 final state；
- backend health check 只覆盖 gather graph 实际节点。

### 10.2 输入 normalization

- canonical `subtask_res` 覆盖 legacy `review_res`；
- package rer跑后旧 `primitive_res` 不复活；
- rejected/inconclusive 不进入 evidence pool；
- standalone finding 只有 qualification passed 且有 capability view 才可作为 unit；
- confirmed `chain_res` 转换为 local-chain unit，并保留 constituent provenance；
- 不同 workspace 的相同 local ID namespace 后不碰撞；
- snapshot hash 和 source drift 检测稳定。

### 10.3 graph

- graph 从 `gather_analyze_attack_surface` 开始，不执行 fetch/search/plan_by_*；
- plan 为空时只执行一次 `gather_prepare_report_groups -> summary -> polish_report`；
- 多 candidate 通过 `Send` 并发，nested state 不串扰；
- critic revise 有上限，最终都经过 gather finalizer；
- reducers 只合并 gather candidate/finding/error。

### 10.4 qualification

- 单 target 候选必拒绝；
- 无跨 target binding 必拒绝；
- 不存在的 unit、flow 或 source ref 必拒绝；
- scenario-only edge 未补证时必拒绝；
- local chain 与其 constituent primitive 重复使用必拒绝；
- 互斥版本、配置、身份或部署条件必拒绝；
- 任一必要 fact 为 unknown 必拒绝；
- source drift 必拒绝；
- 完整跨目标闭包只产生一个带稳定 ID 的 gather finding。

### 10.5 report

- source standalone findings 不被重复编号；
- 每个 gather vulnerability 至少包含两个 target 和一条跨 target edge；
- 中英文报告 group ID 和数量一致；
- 每条漏洞都有跨目标数据流图、攻击时序图、代码证据、约束和 CVSS；
- Mermaid 做真实 parser/render 校验，而不是只统计 fence 数；
- 无闭合链时仍生成结构完整的 no-finding 报告。

测试运行使用仓库约定的 Python：

```bash
python3.14 -m unittest tests.test_cli tests.test_nodes_gather tests.test_gather_graph
python3.14 -m unittest discover -s tests
```

## 11. 分阶段落地

### Phase 1：入口、manifest 与快照

1. 扩展 `--scan-mode` 和新增 `--gather-workspace-to-chain`；
2. 实现 manifest schema、path resolution 和参数互斥；
3. 创建独立 gather workspace；
4. 实现 active artifact 选择、namespace、snapshot 和 input lock；
5. 完成单测，不接 agent。

完成标准：给定多个真实 workspace，可以稳定生成相同的
`gather_inputs.lock.json` 和 `gather_evidence_pool.json`，源 workspace 零修改。

### Phase 2：跨目标 surface 与计划

1. 实现 `gather_analyze_attack_surface` role/prompt/schema；
2. 实现 `cross_target_registry.json` 的 hard validator；
3. 实现 `gather_plan_chains` 和 advisory-only compatibility helper；
4. 实现 `dispatch_gather_chains`；
5. 加入 native-subagent runtime gate。

完成标准：agent 能从真实场景生成带双侧 provenance 的 `FLOW-*`，并只分发至少跨
两个 target 的候选。

### Phase 3：battle 与 qualification

1. 实现 gather investigate/critic nested graph；
2. 实现逐 fact verdict、feedback 和 bounded rounds；
3. 实现 gather finalizer 与 source drift 检查；
4. 输出 confirmed result 和 failed candidate 到分离目录。

完成标准：只有所有跨 target edge 和约束闭合的 candidate 能进入
`gather_chain_res`，其余都有机器可读 rejection reason。

### Phase 4：报告、恢复与文档

1. 实现 `gather_prepare_report_groups` 和 `gather_summary`；
2. 扩展 report diagnostics、gate result 和双语模板；
3. 更新 README/ARCH/demo config；
4. 做真实 Mermaid render 和端到端 fixture 测试；
5. 再设计 `--start-from-gather-chain`，以 input-lock hash 作为恢复前置条件。

## 12. 验收标准

V1 可以按以下条件验收：

- 一条命令能够从 manifest 中的多个已完成 workspace 创建独立 gather workspace；
- 任一源 workspace 在运行前后内容 hash 不变；
- 所有输入 artifact 和最终 finding 都有 target-scoped ID 与 `SourceRef`；
- `gather_analyze_attack_surface` 产出可校验的跨目标拓扑，而不是文件拼接；
- `gather_plan_chains` 使用 native subagents 做 forward/backward/seam/constraint 分析；
- chain battle 至少验证一条真实跨目标 edge，不能把 scenario 当作证据；
- deterministic gate 无法被 agent 文本绕过；
- summary 不重复报告源 workspace 的 standalone finding；
- 空结果、部分失败和证据不足都有可读报告与机器可读状态；
- 所有新增测试和现有全量测试通过。

这套边界使 gather 成为“多个既有审计结果之上的跨系统证明层”：源 workspace 提供
已经审过的局部事实，gather agent 负责发现语义组合，critic 和 finalizer 则确保最终
报告的每条跨目标攻击链都有完整、可追溯且同时可满足的证据闭包。

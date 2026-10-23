# P0: 跨漏洞原语聚合与攻击链分析方案

本文档给出 `TODO.md` 中 P0 的实现方案，重点说明两件事：

- 对现有 ZeroMDASH 流程需要做哪些变更。
- 如何搜索并判定一个有效的 `CHAIN`，避免把“看起来能串起来”的未闭合组合误报为漏洞。

核心原则：`chain_finding` 只能来自已确认原语的端到端闭包。单个 subtask 里发现的机制如果没有独立 C/I/A 影响，应被保存为 `confirmed_primitive`，但不能直接进入最终漏洞报告。chain 阶段只消费这些已经确认的原语和具备 capability view 的 standalone finding，不能在聚合阶段临时发明新的前置漏洞。

## 1. 当前流程的问题

现有主流程大致是：

```text
gather/search/analyze
  -> plan_by_*
  -> dispatch_subtasks
  -> [investigate_subtask <-> critic_subtask -> finalize_subtask]*
  -> summary
```

当前资格门槛只认“自身已经违反安全契约并产生直接 C/I/A 影响”的结果。`critic_subtask` / qualification gate 会要求：

- `security_contract_violation=true`
- `standalone_security_impact=true`
- `required_external_primitives=[]`
- 存在直接 C/I/A 影响
- CVSS v4.0 Base vector 有效且非零

这对 standalone vulnerability 是正确的，但会丢掉一类重要结果：代码机制、可达性、攻击者可控对象和获得的能力都已经被确认，只是它本身还不能构成完整漏洞。例如“可控对象进入某缓存状态”“获得跨租户对象引用”“绕过一段前置检查但还需要后续 sink”。这些结果现在通常会被归到 observation 或 insufficient evidence，后续无法聚合成攻击链。

P0 要解决的是：把“未闭合但已确认的攻击能力”作为一等产物保存下来，然后在所有 subtask 完成后做有界聚合，寻找能端到端闭合为直接 C/I/A 影响的攻击链。

## 2. 目标流程

目标流程改为两级 subtask graph：

```text
gather/search/analyze
  -> plan_by_*
  -> dispatch_subtasks
  -> [investigate_subtask <-> critic_subtask -> finalize_subtask]*
  -> materialize_chain_pool
  -> plan_chains
  -> dispatch_chains
  -> [chain_investigate_subtask <-> chain_critic_subtask -> finalize_chain_subtask]*
  -> prepare_report_groups
  -> summary
```

第一层 subtask 只负责确认局部事实，终态分为：

- `standalone_finding`：自身已经闭合为漏洞，按现有 hard gate 计算 CVSS。
- `confirmed_primitive`：机制、可达性、攻击者控制和能力获得已经确认，但自身不能闭合为漏洞，不计算 CVSS。
- `observation`：有安全相关事实，但不足以作为原语参与 chain。
- `rejected`：明确不是问题。
- `inconclusive`：证据不足或 critic 轮次耗尽。

第二层 chain subtask 只负责验证候选组合是否能闭合。它不能把 `observation`、`rejected`、`inconclusive` 当成前置原语，也不能把 chain 过程中猜出来的新机制直接升级为 confirmed primitive。

最终 `summary` 消费的是 `report_groups`，而不是直接消费原始四个 finding bucket。`report_groups` 由确定性去重节点生成，输入包括 standalone findings、chain findings 和 patch-gap 特例。

## 3. 需要新增和修改的模块

建议新增模块：

```text
zeromdash/nodes/materialize_chain_pool.py
zeromdash/nodes/plan_chains.py
zeromdash/nodes/dispatch_chains.py
zeromdash/nodes/chain_investigate_subtask.py
zeromdash/nodes/chain_critic_subtask.py
zeromdash/nodes/finalize_chain_subtask.py
zeromdash/nodes/prepare_report_groups.py
zeromdash/nodes/core/primitive_qualification.py
zeromdash/nodes/core/chain_compatibility.py
zeromdash/nodes/core/chain_qualification.py
zeromdash/nodes/core/report_dedup.py
```

主要修改点：

- `zeromdash/state.py`
  - 增加 `Primitive`、`ChainCandidate`、`ChainFinding`、`ReportGroup` TypedDict。
  - 顶层 state 增加 `confirmed_primitives`、`chain_candidates`、`chain_findings`、`report_groups`。
  - 增加 `ChainSubtaskInputState`、`ChainSubtaskState`、`ChainSubtaskOutputState`。

- `zeromdash/graph.py`
  - `subtask` 不再直接连到 `summary`。
  - 所有初步 subtask 完成后进入 `materialize_chain_pool`。
  - `plan_chains` 生成有界候选，再由 `dispatch_chains` fan out 到 chain nested graph。
  - chain 全部结束后进入 `prepare_report_groups`，再进入 `summary`。
  - restore graph 要增加从 subtask、chain、summary 三个阶段恢复的入口。

- `zeromdash/nodes/core/qualification.py`
  - 保留现有 standalone vulnerability hard gate。
  - 新增 primitive gate。primitive gate 不要求 direct C/I/A，不要求 CVSS，也不要求 `standalone_security_impact=true`。
  - qualification 输出必须区分 `outcome_type` 和 `disposition`，避免把 primitive 伪装成 vulnerability disposition。

- `zeromdash/nodes/finalize_subtask.py`
  - 根据 critic 的终态输出，分别持久化 standalone finding、confirmed primitive、observation 或 reject。
  - `confirmed_primitive` 需要写入 `log/primitive_res/*.json`，并回传到 parent state。

- `zeromdash/nodes/summary.py`
  - 改为消费 `report_groups`。
  - `gate_result` 基于 report group 和最终漏洞，而不是原始 finding bucket。
  - 保留双语报告、代码证据、数据流图、攻击时序图、版本边界、CVSS v4.0 的现有要求。

- `zeromdash/nodes/core/constants.py`
  - 增加 chain 节点默认 backend。
  - 原生子 agent 要求增加 `chain_investigate_subtask` 和 `chain_critic_subtask`。

- `zeromdash/cli.py`
  - `top_K` 增加 `chain`。
  - 增加 `--disable-chain`。
  - 增加 `--start-from-chain <workspace>`。
  - 增加 selected chain 重跑入口，语义与 selected subtask 类似，但产物写入独立目录，不覆盖 canonical chain 结果。

## 4. 数据契约

### 4.1 初步 subtask 终态 envelope

`finalize_subtask` 应统一输出一个 envelope，再根据 `outcome_type` 路由：

```json
{
  "schema_version": "2.0",
  "outcome_type": "standalone_finding",
  "subtask_id": "vuln_similar_003",
  "finding": {},
  "primitive": null,
  "review": {},
  "history": []
}
```

`outcome_type` 可取：

```text
standalone_finding
confirmed_primitive
observation
rejected
inconclusive
```

不要复用 `disposition` 表达 primitive。`disposition` 仍用于漏洞/非漏洞 taxonomy；`outcome_type` 用于 workflow 路由。

### 4.2 Primitive

`confirmed_primitive` 的最小结构：

```json
{
  "schema_version": "2.0",
  "primitive_id": "prim_...",
  "source_subtask_ids": ["vuln_similar_003"],
  "repo_id": "main",
  "revision": "commit-or-scope-id",
  "component": "auth/session",
  "root_cause_anchor": {
    "symbol": "SessionStore::lookup",
    "locations": ["src/session.cc:120"]
  },
  "entry_conditions": {
    "attacker_position": "remote unauthenticated",
    "required_config": [],
    "required_versions": [],
    "notes": []
  },
  "required_capabilities": [],
  "attacker_controls": [
    {
      "object_type": "http_parameter",
      "object_id": "sid",
      "constraints": ["attacker-chosen string"]
    }
  ],
  "capabilities_gained": [
    {
      "kind": "object_reference",
      "object_type": "session",
      "scope": "same-service",
      "principal": "victim",
      "address_space": "server-process",
      "properties": ["cross-user session handle"]
    }
  ],
  "handoff_objects": [],
  "reliability": {
    "level": "medium",
    "reason": "requires existing victim session id collision window"
  },
  "evidence": {
    "code_locations": [],
    "call_paths": [],
    "counterevidence": []
  },
  "missing_next_capabilities": [],
  "confirmation": {
    "critic_verdict": "confirm",
    "confidence": 0.75
  }
}
```

约束：

- `primitive_id` 由 orchestrator 计算，不接受模型直接生成的最终 ID。
- 一个 primitive 表示一个主要机制。一个机制可以产生多个 `capabilities_gained`。
- 如果同一 subtask 发现多个互相独立的机制，应拆成多个 primitive 或生成后续 subtask，不应塞进一个 primitive。
- `custom` capability 只能用于报告和人工审阅，不能自动匹配成 chain edge。

### 4.3 Standalone Finding 的 capability view

standalone finding 仍然按现有漏洞路径处理，但如果它也要进入 chain pool，必须提供 `capability_view`：

```json
{
  "capabilities_gained": [],
  "handoff_objects": [],
  "evidence": {}
}
```

没有 `capability_view` 的 standalone finding 只能进入最终报告，不能作为 chain 中的能力提供者。这样可以避免把“已经有漏洞影响”误当成任意后续能力。

### 4.4 Chain Candidate

`plan_chains` 输出候选，不输出漏洞：

```json
{
  "chain_id": "chain_...",
  "ordered_primitive_ids": ["prim_a", "prim_b"],
  "attacker_entry": {
    "capabilities": []
  },
  "bindings": [
    {
      "consumer_primitive_id": "prim_b",
      "required_capability": {},
      "provider": {
        "type": "primitive",
        "primitive_id": "prim_a",
        "capability": {}
      },
      "compatibility_reason": "same object_type and address_space; victim principal preserved"
    }
  ],
  "expected_terminal_impact": {
    "confidentiality": "high",
    "integrity": "none",
    "availability": "none"
  },
  "rank_score": 0.82,
  "pruning_context": {}
}
```

candidate 是“值得投入 chain battle 验证的假设”。它不是 finding。

### 4.5 Chain Finding

`chain_finding` 的必要条件：

- `ordered_primitive_ids` 中每个 primitive 都来自 confirmed pool。
- 每个 requirement 都能由 attacker entry 或更早 primitive 的 gained capability 满足。
- 所有版本、配置、principal、tenant、address space、trust boundary 约束能同时成立。
- 不依赖未确认的外部 primitive。
- 最后一跳或组合后的终态产生直接 C/I/A 影响。
- CVSS v4.0 Base vector 与最终直接影响一致。

## 5. Capability 模型

chain 搜索需要一个受控 capability vocabulary。建议第一版只支持以下 `kind` 自动匹配：

```text
controlled_request
authenticated_session
credential_access
object_reference
address_disclosure
relative_file_read
arbitrary_file_read
relative_file_write
arbitrary_file_write
relative_memory_read
arbitrary_memory_read
relative_memory_write
arbitrary_memory_write
command_execution
code_execution
identity_impersonation
privilege_gain
sandbox_escape
security_boundary_bypass
denial_trigger
```

每个 capability 至少包含：

- `kind`
- `object_type`
- `scope`
- `principal`
- `tenant`
- `address_space`
- `properties`
- `constraints`

自动兼容只允许发生在同一 vocabulary 内。`kind=custom`、自然语言描述、或字段缺失的 capability 不能自动闭合，只能进入 unresolved check。

## 6. 有效 CHAIN 的判定原理

### 6.1 形式化定义

把每个 primitive 看成一个带证据的状态转换：

```text
P = (R, G, C, E)
```

含义：

- `R`：执行该 primitive 需要满足的 capability requirements。
- `G`：执行后攻击者获得的 capabilities。
- `C`：版本、配置、身份、租户、地址空间、repo/component、trust boundary 等约束。
- `E`：代码证据、调用路径和反证。

攻击者初始能力为：

```text
A0 = threat model 中允许的初始能力
```

一个候选 chain 是有序 primitive 序列：

```text
Chain = [P1, P2, ..., Pn]
```

执行到第 `i` 步前，攻击者已知能力集合为：

```text
Ai = A0 ∪ G(P1) ∪ ... ∪ G(Pi-1)
```

`Pi` 可执行当且仅当 `R(Pi)` 中每个 requirement 都能在 `Ai` 中找到一个兼容 provider。provider 可以来自 `A0`，也可以来自任意更早 primitive，不要求只来自紧邻上一跳。

这点很重要：真实攻击链经常需要累计能力，例如第一步获得 victim object reference，第二步获得 address disclosure，第三步同时需要这两个能力。实现上可以保存为有序列表，但验证必须基于“累积能力闭包”，不能只做相邻节点字符串拼接。

### 6.2 Requirement 与 Capability 的兼容

一个 requirement `r` 被 capability `g` 满足，需要同时通过以下检查：

- `kind` 兼容：相同 kind，或在显式定义的偏序里 `g` 强于 `r`。例如 `arbitrary_file_read` 可以满足 `relative_file_read`，反过来不行。
- `object_type` 兼容：对象类型一致，或存在显式父子类型关系。
- `principal` 兼容：能力作用的身份能覆盖 requirement 需要的身份，不能把 attacker 自身权限当成 victim/admin 权限。
- `tenant` 兼容：跨租户必须有明确证据，不能把 same-tenant 能力升级成 cross-tenant。
- `address_space` 兼容：同进程、同主机、远端服务、客户端浏览器等地址空间必须一致；跨地址空间需要 `handoff_object`。
- `scope` 兼容：repo/component/trust boundary 的跨越必须由证据说明。
- `constraints` 可满足：长度、格式、时序、配置、认证状态等约束不能冲突。

任何未知字段都不能被当作通过。未知字段可以让 candidate 进入 chain battle 请求补证，但 deterministic closure gate 不能据此产出 `chain_finding`。

### 6.3 全局约束可满足性

除了每条 binding 的局部兼容，整条 chain 还必须满足全局一致性：

- 所有 primitive 的 affected version 区间交集非空。
- required config 不互相排斥。
- 同一个对象在多步之间的 identity 保持一致，除非存在明确转换证据。
- principal/tenant 没有被无证据提升。
- 跨 repo、跨 component、跨 trust boundary 时存在明确 handoff object，例如 token、file、network request、message queue event、shared database row。
- chain 中不能重复使用同一个 root cause 形成无意义循环。

全局约束检查失败的组合必须被裁剪，并保存裁剪原因。

### 6.4 终态影响

有效 chain 的最后必须产生直接 C/I/A 影响。下面这些情况不能成为 `chain_finding`：

- 只是获得了“可能继续利用”的能力，但没有最终 sink。
- 最终影响依赖一个未确认的外部漏洞。
- 只证明了 hardening opportunity 或 defense-in-depth 缺口。
- CVSS vector 的 VC/VI/VA/SC/SI/SA 与声明的 direct impact 不一致。

CVSS 只在 `chain_finding` 阶段计算，评分对象是完整攻击链的最终影响，不是单个 primitive 的局部严重性。

## 7. 搜索有效 CHAIN 的算法

### 7.1 输入池构建

`materialize_chain_pool` 在所有初步 subtask 完成后运行：

```text
qualified standalone findings
  + confirmed primitives
  -> normalize
  -> dedupe
  -> chain_pool.json
```

standalone finding 进入 pool 时分两种身份：

- reportable vulnerability：保留独立报告资格。
- capability provider：只有存在 `capability_view` 时才参与 chain 搜索。

dedupe 使用 orchestrator 生成的 stable key：

```text
schema_version
+ repo_id
+ revision/scope
+ component
+ root_cause_anchor symbol
+ normalized root_cause locations
+ normalized capability signature
```

不要把 subtask id 或模型生成的 title 放进稳定 ID 的核心字段。它们可作为 metadata，但不能决定同一机制是否重复。

### 7.2 建索引

为每个 primitive 建两个索引：

- `requires_index`: requirement kind -> consumers
- `gains_index`: capability kind -> providers

搜索后继时只查与新增 capability kind 兼容的 consumers，避免对所有 primitive 做笛卡尔积。

### 7.3 状态扩展

搜索状态包含：

```text
ordered_primitive_ids
available_capabilities
bindings
global_constraints
terminal_impact_estimate
rank_score
```

初始状态来自 `A0`，即 threat model 允许的攻击者入口能力。每加入一个 primitive：

1. 检查该 primitive 尚未在路径中出现。
2. 检查它的每个 requirement 是否能由 `available_capabilities` 绑定。
3. 合并版本/配置/对象/身份/租户/地址空间约束。
4. 将它的 `capabilities_gained` 加入 `available_capabilities`。
5. 如果出现 terminal direct impact，生成 chain candidate。
6. 如果没有 terminal impact，但仍有可兼容后继，继续扩展。

这实际上是在做 capability closure search，而不是自然语言相似度搜索。

### 7.4 排序和裁剪

建议默认配置：

```yaml
top_K:
  chain: 16
chain:
  enabled: true
  max_length: 4
  max_successors_per_capability: 4
  beam_width: 64
  max_candidates_before_top_k: 200
  max_battle_rounds: 2
```

rank score 可由以下因素组成：

- requirement/gain 的 kind 精确匹配优先。
- object/principal/tenant/address_space 字段越完整越优先。
- 跨 trust boundary 且 handoff object 明确的组合优先。
- 最终 sink 和 direct impact 越明确越优先。
- primitive critic confidence 越高越优先。
- 缺少 unresolved checks 越少越优先。
- chain 越短越优先，但不能压过更高置信度的真实链。

裁剪时必须保存原因：

```text
version_conflict
config_conflict
object_scope_mismatch
principal_mismatch
tenant_mismatch
address_space_mismatch
missing_handoff_object
cycle
successor_cap
max_length
beam_width
top_k
duplicate_path
unresolved_custom_capability
```

这些原因写入 `log/review_log/chain_pruning.jsonl`，用于解释为什么某些 primitive 没有进入 battle。

### 7.5 Chain Battle

`plan_chains` 只做静态筛选。进入 `chain_investigate_subtask <-> chain_critic_subtask` 的 candidate 还必须重新验证代码证据。

`chain_investigate_subtask` 必须输出：

- 完整攻击者入口。
- ordered primitive ids。
- 每个 primitive 的证据引用。
- 每个 requirement 的 provider binding。
- 每一步 capability transition。
- 跨 repo/component/trust boundary 的 handoff object。
- 全局版本和配置约束。
- 最终 C/I/A 影响。
- 反证和仍未满足的事实。

`chain_critic_subtask` 必须逐项检查：

- 所有 primitive 是否来自 confirmed pool。
- 每个 binding 的 kind/object/principal/tenant/address_space/scope 是否兼容。
- 版本和配置是否能同时成立。
- handoff object 是否有证据。
- 是否仍依赖未确认外部原语。
- 最终影响是否直接产生 C/I/A。
- CVSS v4.0 vector 是否与最终影响一致。

critic 可以要求 revise，但 revise 只能补证、修正 binding 或降级 candidate。它不能新增一个未确认 primitive 并让当前 chain 直接闭合。

### 7.6 Deterministic Closure Gate

`finalize_chain_subtask` 需要在模型 critic 之后再做一次确定性 gate：

```text
all_primitives_confirmed
AND all_requirements_bound_to_prior_capabilities
AND all_bindings_compatible
AND global_constraints_satisfiable
AND no_unconfirmed_external_primitive
AND attacker_entry_valid
AND final_direct_cia_impact
AND cvss4_valid_and_matches_impact
```

只有全部为 true 才输出 `chain_finding`。否则输出 `chain_candidate`，并标注失败原因。失败 candidate 可以保留给人工审阅或后续 subtask，但不能进入漏洞计数。

## 8. 去重与报告规则

新增 `prepare_report_groups`，在 summary 前做确定性分组：

- 同一个 root cause、同一个 sink、同一个 security property 的 finding 合并为一个 report group。
- chain 如果只是把某个 standalone finding 作为最终 sink 的可选攻击路径，应吸收该 standalone finding，避免重复计数。
- standalone finding 如果有独立直接影响，同时又作为另一个 chain 的中间 capability provider，可以保留独立报告；chain 报告中引用它的 capability view。
- 同一 root cause 的不同入口路径可以合并到一个 `VULN-XXX`，保留多条 attack paths。
- 如果同一 group 中有多个有效 CVSS path，主分数取最高已证实 score，同时保留每条 path 的 vector。
- patch gap 特例继续保留独立格式，不参与 primitive chain 自动闭合，除非 patch audit 也输出了符合 v2 schema 的 capability view。

`summary` 只负责写报告，不负责决定漏洞是否成立，也不负责 chain 去重。

## 9. 持久化和恢复

建议新增产物：

```text
log/subtask_res/<subtask_id>.json
log/primitive_res/<primitive_id>.json
log/state/chain_pool.json
log/state/chain_plan.json
log/review_log/chain_pruning.jsonl
log/chain_res/<chain_id>.json
log/chain_candidates/<chain_id>.json
log/report_groups.json
log/selected_chain_runs/<run_id>/
```

写 JSON 使用 temp file + atomic replace，避免并发 fan-out 时读到半截文件。

恢复语义：

- `--start-from-subtask <workspace>`：复用 gather/plan，重跑或补跑初步 subtask，然后继续 chain 和 summary。
- `--start-from-chain <workspace>`：读取 `subtask_res` 和 `primitive_res`，重新生成或复用 chain plan，再跑 chain 和 summary。
- `--start-from-summary <workspace>`：读取 standalone findings、chain findings 和 report groups，只重跑 summary。
- `--select-chain-to-run <chain_id>`：只重跑指定 chain，结果写入 selected run 目录，不覆盖 canonical `chain_res`。

旧版 `review_res` 作为兼容输入继续参与恢复；同名文件以 `subtask_res` 为准。只有 v2 schema 且通过 primitive/capability validator 的记录才能进入 chain pool。

## 10. 实施顺序

建议分 5 个 PR 落地：

1. Schema v2 和 primitive gate
   - 增加 `outcome_type`。
   - 让初步 subtask 可以产出 `confirmed_primitive`。
   - 写入 `log/primitive_res`。
   - 此阶段 summary 行为基本不变。

2. Chain pool 和 deterministic planner
   - 实现 capability vocabulary。
   - 实现 primitive stable id、dedupe、compatibility check、bounded search。
   - 输出 `chain_pool.json`、`chain_plan.json`、`chain_pruning.jsonl`。

3. Chain battle 和 closure gate
   - 增加 chain nested graph。
   - 实现 chain investigator/critic prompt 和 harness contract。
   - `finalize_chain_subtask` 只允许闭合 chain 输出 `chain_finding`。

4. Report grouping 和 summary 改造
   - 增加 `prepare_report_groups`。
   - summary/gate_result 改为消费 report groups。
   - 处理 standalone 与 chain 的吸收、合并和 CVSS path 保留。

5. CLI、恢复、测试和文档
   - 增加 chain 配置、恢复入口、selected chain run。
   - 补齐单元测试和端到端小样例。

## 11. 验收测试

至少覆盖以下场景：

- 一个 confirmed primitive 没有 direct C/I/A，不计算 CVSS，但写入 `primitive_res`。
- 一个依赖外部未确认原语的结果不能进入 summary 漏洞计数。
- 两个 primitive 的 capability/requirement 完全兼容时生成 chain candidate。
- 版本冲突、配置冲突、tenant 不一致、principal 不一致、address space 不一致时被裁剪，并记录原因。
- 跨 repo/component/trust boundary 没有 handoff object 时不能闭合。
- chain battle 发现证据不足时只输出 candidate，不输出 finding。
- 只有闭合 chain 才计算 CVSS，且 CVSS impact metrics 必须与 final direct impact 一致。
- standalone finding 被 chain 作为最终 sink 吸收时不重复计数。
- standalone finding 作为中间 capability provider 且自身有独立影响时，既能保留独立报告，也能被 chain 引用。
- `--start-from-chain` 不重跑初步 subtask。
- `--select-chain-to-run` 不覆盖 canonical chain 产物。
- 没有 primitive 或没有 candidate 时，summary 仍能正常输出。

## 12. P0 范围边界

P0 建议只做当前 workspace 内的 chain 聚合：

- 支持 full mode 的多 repo，因为现有 workspace 已有聚合 repo 视图。
- 不把 multi-repo diff attribution 放进 P0；当前 diff 多 repo 语义需要单独设计。
- 不接入跨 workspace 历史漏洞 KB。历史 KB 属于 TODO 里的后续 P1。
- 不让 LLM 自由发明 capability vocabulary。第一版 vocabulary 应小而明确，后续根据误报/漏报扩展。

这样做的好处是边界清楚：第一层确认原语，第二层搜索和验证组合，summary 只报告已经闭合的结果。第 13 节进一步将语义裁决交给 Agent；代码层只保留机械完整性 gate、成本控制和可审计 advisory。

## 13. Agent-Native Chain 与 Domain Registry 修订

本节是当前设计，取代上文 7.2–7.6 中将 deterministic matching/closure 作为语义裁决者的部分。上文的数据模型、持久化、恢复、成本控制和报告规则仍然适用。

### 13.1 Goal

ZeroMDASH uses two analysis levels:

```text
initial subtasks
  investigate_subtask <-> critic_subtask
    -> standalone findings (CVSS v4.0)
    -> confirmed primitives (no standalone CVSS)

chain aggregation
  plan_chains
    -> chain_investigate_subtask <-> chain_critic_subtask
    -> chain findings (CVSS v4.0 for the closed end-to-end chain)

reporting
  standalone findings + chain findings
    -> deterministic grouping/deduplication
    -> bilingual summary + evidence-grounded diagrams
```

The semantic decisions in chain composition belong to agents. Python code may
normalize artifacts, produce advisory candidates, enforce budgets, validate
references and schemas, and calculate CVSS. It must not make a final security
decision merely because two model-generated strings match or differ.

### 13.2 Domain Model and Invariant Registry

`analyze_attack_surface` produces two synchronized artifacts:

- `main/attack_surface/attack_surface.md`: the human-readable analysis;
- `main/attack_surface/domain_invariant_registry.json`: structured domain
  vocabulary and evidence references for downstream agents.

The registry is domain-adaptive. The common schema contains:

- `entities`: protected resources, principals, state objects and backing
  objects discovered in the target domain;
- `representations`: aliases, caches, shadow state, serialized forms and other
  representations of an entity;
- `invariants`: properties such as containment, provenance, ownership,
  freshness, synchronization, lifecycle validity and representation
  consistency;
- `transitions`: attacker-relevant state or capability transitions;
- `seams`: producer/consumer, mutator/protector, authoritative/derived-state,
  logical/physical-backing and setup/runtime boundaries worth testing.

IDs are stable references, not automatic truth. A registry entry gives agents
a shared vocabulary and an evidence index; investigators and critics still
verify every claim against source. Domain-specific views such as a Protected
Resource and Mapping Registry are derived from these generic objects instead
of being hard-coded into the workflow.

### 13.3 Initial Analysis

All initial planners receive the registry and should attach relevant
`domain_refs` to subtask hints. Initial investigator and critic agents use the
same registry when verifying object identity, lifecycle, representation and
invariant claims.

An initial result is one of:

- `standalone_finding`: the local issue itself closes direct C/I/A impact and
  passes the existing CVSS v4.0 qualification gate;
- `confirmed_primitive`: mechanism, reachability, attacker control and gained
  capability are confirmed, but the item does not independently close impact;
- observation, rejected or inconclusive.

Primitives retain registry references plus required/resulting entity states.
These references improve later composition, but do not make a binding valid by
themselves.

### 13.4 Agent-Native Chain Planning

`plan_chains` must run on a native-subagent-capable harness. Its parent agent
coordinates bounded specialist subagents, for example:

1. forward composer: start from attacker capabilities and search forward;
2. backward composer: start from possible terminal impact and search backward;
3. seam composer: inspect registry seams and cross-component handoff objects;
4. constraint auditor: test version, configuration, principal, tenant, object,
   lifecycle and address-space coexistence.

The deterministic prefilter remains useful, but only as advisory input. It may
emit candidate paths, mismatch reasons and pruning scores. An agent may recover
a candidate rejected by exact matching when it supplies an explicit semantic
repair with registry references and source evidence. Likewise, an agent may
reject a deterministic match whose objects or deployment conditions differ.

`plan_chains` may only reference confirmed primitive IDs. It cannot invent an
unverified exploit step. A missing step is retained as an unmet fact or a
residual hypothesis for later initial-subtask planning.

### 13.5 Chain Battle

`chain_investigate_subtask` verifies one candidate and delegates bounded native
subagents per binding, seam, global constraint or emergent-impact claim. It
outputs explicit `binding_claims`, `capability_transitions`,
`emergent_transitions`, registry references, evidence and unmet facts.

`chain_critic_subtask` uses independent adversarial subagents to falsify:

- provider/consumer object identity;
- capability strength and permission compatibility;
- cross-repository or cross-address-space handoff;
- version/configuration/lifecycle coexistence;
- the final impact and claimed violated invariant.

It returns one `edge_verdicts` item for each binding and one
`transition_verdicts` item for each emergent transition, then an overall
verdict. A failed edge or transition cannot be silently removed by the parent
agent.

### 13.6 Emergent Impact

A valid chain does not require any individual primitive to carry terminal
impact. Two or more confirmed state transitions may jointly create a new
security violation. The chain investigator proposes this emergent transition,
the chain critic confirms it with evidence, and only the closed chain receives
CVSS v4.0.

The final mechanical validator checks only hard integrity properties:

- all referenced primitive and registry IDs exist;
- primitive IDs are unique and ordered;
- every claimed edge has a critic verdict;
- no unmet fact or unconfirmed external primitive remains;
- evidence and required output fields are present;
- the final direct impact and CVSS v4.0 vector are structurally consistent.

It does not rerun exact capability matching as a final semantic veto.

### 13.7 Reporting

`summary` consumes standalone findings and closed chain findings. Existing
bilingual report requirements remain unchanged: code evidence, threat model,
trigger conditions, affected versions, CVSS v4.0, and one evidence-grounded
data-flow plus attack-sequence diagram per canonical `VULN-XXX`.

Deterministic report grouping prevents a standalone finding from being counted
again merely because it participates in a chain. Confirmed primitives and
unclosed chain candidates remain auditable artifacts, not reported
vulnerabilities.

### 13.8 Compatibility and Cost Controls

- Existing workspaces without a domain registry remain restorable; downstream
  agents receive an explicit unavailable/legacy marker.
- Existing deterministic prefilter and pruning logs remain available as
  advisory evidence.
- `top_K.chain`, maximum chain length, beam width, successor cap and battle
  rounds bound cost, but cannot silently turn an advisory mismatch into a
  security conclusion.
- `plan_chains`, `chain_investigate_subtask` and `chain_critic_subtask` require
  a native-subagent-capable harness.

## 14. Multi-Repo Hybrid Analysis 与 Chain Context Completeness

本节解决 multi-repo 目标在进入 Chain 之前的上下文稀释问题。当前实现只在
`fetch_target_repo` 后将多个仓库映射到同一个 `main/repo/<repo_id>` 聚合视图；
后续 gather、attack-surface、planner 和 initial subtask 仍共享一套大上下文。这样虽然
允许跨仓读取源码，但大仓库容易淹没小仓库，单仓 primitive 的召回率、跨仓接口契约
覆盖率和裁剪可解释性都不足。

本节是 multi-repo + Chain 的下一阶段设计；在 `hybrid` layout 落地后，它取代
第 12 节“仅依赖现有聚合 repo 视图”的 multi-repo 分析方式。`aggregate` layout 和
single-repo 兼容路径仍保留。

### 14.1 Chain 与仓库数量正交

Chain 不应被限制为只有 multi-repo 才能启用。Chain 组合的是 confirmed
primitives，而不是 repositories；同一仓库的不同子系统也可能形成有效攻击链。

建议把两个维度分开配置：

```yaml
analysis:
  layout: aggregate | hybrid | auto

chain:
  enabled: true | false
  scope: intra_repo | cross_repo | both
```

语义如下：

| Target | Analysis layout | Chain behavior |
|---|---|---|
| single repo | `aggregate` | 可启用 intra-repo Chain，保持当前初步分析流程 |
| multi repo + Chain disabled | `aggregate` | 保持现有聚合分析行为，直接报告 standalone findings |
| multi repo + Chain enabled | `hybrid` | 强制 repo-local lanes + integration lane，再进入全局 Chain |
| multi repo + 显式 `hybrid` | `hybrid` | 即使 Chain 关闭，也可用 local/integration lanes 提升 standalone finding 召回 |

`auto` 在 single-repo 下解析为 `aggregate`；在 multi-repo + Chain 下解析为
`hybrid`。不能根据仓库数量关闭已经显式启用的 Chain。

### 14.2 Fetch 一次，按仓派发分析

不为每个 repo 重复执行完整的 `fetch_target_repo` 节点。顶层 fetch 负责一次性完成：

```text
fetch_target_repo
  -> main/repos/<repo_id>          # canonical source checkout
  -> main/repo/<repo_id>           # aggregate source view
  -> main/repos/_manifest.json     # repo identity / role / revision / paths
```

materialization barrier 确认全部 required repositories 已获取后，通过 LangGraph
`Send("repo_analysis", child_state)` 为每个 repo 派发同一个 compiled nested graph。
每个 child state 的 `repo_path` 指向 `main/repos/<repo_id>`，而不是完整聚合目录。

每条 repo-local lane 保持正确的数据依赖顺序：

```text
repo-local search_*
  -> repo-local search_new_feature
  -> repo-local analyze_attack_surface
  -> repo-local plan_by_*
  -> repo-local investigate_subtask <-> critic_subtask
  -> repo_analysis_package
```

`plan_by_*` 必须位于 `analyze_attack_surface` 之后，因为 planner 需要读取 local
attack surface 和 Domain Registry。`fetch_target_repo` 则保持顶层统一调度，避免重复
clone、manifest 漂移和多个 lane 互相覆盖工作目录。

### 14.3 Repo-Local Lane

repo-local lane 的目标是保证每个仓库都能形成独立、足够密度的上下文，而不是假设
漏洞一定局限于该仓库。建议产物布局：

```text
main/repo_analysis/<repo_id>/
  spec/
  fuzz/
  writeup/
  patch/
  feature/
  attack_surface/attack_surface.md
  attack_surface/domain_invariant_registry.json
  coverage_ledger.json

log/repo_analysis/<repo_id>/
  review_log/
  subtask_res/
  primitive_res/
  repo_analysis_package.json
```

所有 local subtask 和 primitive 使用 repository-qualified stable ID，例如：

```text
qemu::vuln-001
linux-kvm::prim_abcd...
libslirp::entity:packet-state
```

local investigator 只需在本仓库内闭合代码机制。若它确认了一个面向外部组件的能力或
前置条件，应保存为 `confirmed_primitive`，并用 `required_capabilities`、
`capabilities_gained`、handoff object 和 namespaced registry refs 描述接口，而不是
因为尚未看到另一仓库实现就丢弃。

每条 lane 最终输出 `repo_analysis_package.json`：

```json
{
  "repo_id": "repo-a",
  "revision": "...",
  "status": "complete|partial|failed",
  "context_paths": {},
  "registry_path": "...",
  "subtask_ids": [],
  "standalone_finding_ids": [],
  "primitive_ids": [],
  "coverage_ledger_path": "...",
  "errors": []
}
```

### 14.4 Shared Discovery 与 Evidence Routing

并非所有 gather 节点都应简单复制 N 次：

- `search_target_history`、`search_fuzz_driver`、`search_new_feature`：按 repo 执行；
- `search_spec`：repo-local lane 负责实现相关规范，另保留一次 target-global 规范搜索；
- `search_similar_software`：target-global 执行一次，避免每个 repo 重复发散；
- `search_similar_history`：基于全局 similar software 结果收集一次，再按 repo、component、
  interface 和 evidence relevance 路由给 local lanes；
- 所有共享搜索结果保留 source provenance，禁止把“没有路由到某 repo”解释为该 repo
  不受影响。

共享 discovery cache 只减少重复 token 和网络请求，不替代 repo-local source
grounding。

### 14.5 Integration Lane

仅有 repo-local lanes 仍会漏掉“单看两边都合理、组合后违反接口契约”的 primitive。
因此所有 repo packages 完成后，必须增加 integration lane：

```text
repo_analysis_packages + target-global context
  -> build_integration_context
  -> analyze_integration_surface
  -> plan_integration_subtasks
  -> investigate_subtask <-> critic_subtask
  -> integration findings + confirmed primitives
```

`build_integration_context` 负责汇总但不做安全裁决：

- repository roles、revisions、build/link/runtime relations；
- local Domain Registries 的 namespaced federation；
- producer/consumer、mutator/protector、setup/runtime、primary/fallback、
  logical/physical-backing 等 seam hypotheses；
- 跨仓配置、协议、ABI、共享对象、序列化格式和生命周期 handoff；
- local coverage ledgers 中尚未被调查的 integration-facing entries。

不能按名称相似度直接合并两个 registry entity。跨仓 object-equivalence、alias 或
handoff 关系必须作为带双方源码证据的 hypothesis，由 integration
investigate/critic 验证。

Integration Registry 建议独立保存：

```text
main/integration/attack_surface.md
main/integration/domain_invariant_registry.json
main/integration/deployment_manifest.json
main/integration/interface_catalog.json
```

### 14.6 Federated Registry 与 Deployment Manifest

全局 Chain 不直接把 local Registry JSON 拼接后交给 Agent，而是消费 federated
registry：

```text
repo-local facts:       <repo_id>::<local_id>
integration relations: integration::<relation_id>
```

federated registry 保留 local source ownership，并把跨仓关系标记为
`hypothesis|confirmed|rejected`。只有经过 initial critic 确认的 relation 才能成为
primitive 事实；未确认 relation 只能帮助规划，不得让 Chain 自动闭合。

`deployment_manifest.json` 描述候选代码是否可能同时运行：

```json
{
  "repositories": [
    {"repo_id": "repo-a", "revision": "...", "required": true}
  ],
  "build_relations": [],
  "runtime_relations": [],
  "feature_constraints": [],
  "known_unknowns": []
}
```

Manifest 可以由 Agent 从源码、构建文件、依赖元数据和用户输入推导，但必须区分事实、
推断与未知项。Chain critic 负责基于源码证据审查共存性；代码层只检查引用和字段
完整性。

### 14.7 Global Primitive Pool 与 Candidate Context Pack

global primitive pool 的输入为：

```text
all repo-local standalone capability providers
+ all repo-local confirmed primitives
+ integration standalone capability providers
+ integration confirmed primitives
```

`materialize_chain_pool` 必须保留 `repo_id`、来源 lane、registry refs、revision 和
evidence provenance。`plan_chains` 使用 compact primitive cards、federated registry
seam index 和 deterministic advisory 做全局组合。

在派发 chain battle 前增加 `prepare_chain_context`，为每个 candidate 生成精确上下文包：

```text
log/chain_context/<chain_id>.json
  - complete primitive records
  - referenced local/integration Registry neighborhoods
  - relevant attack-surface excerpts
  - repository-qualified code evidence
  - deployment constraints and known unknowns
  - deterministic advisories and counterevidence
```

context pack 用于保证关键证据不会被大 pool 挤出 prompt，不是 Agent 的读取边界；
chain investigator/critic 仍可按需读取完整 workspace。

### 14.8 Chain Gap Feedback Loop

Chain battle 发现缺失 primitive 时，不能只把 `unmet_facts` 留档后结束。增加有界回路：

```text
chain battle
  -> collect_chain_gaps
  -> chain_gap_planner
  -> repo-local or integration initial subtasks
  -> investigate_subtask <-> critic_subtask
  -> update primitive pool
  -> plan_chains again
```

规则：

- `chain_gap_planner` 是 Agent-Native planner，只把 gap 转成可证伪的 initial subtask；
- Chain Agent 仍不能直接创建 confirmed primitive；新机制必须经过普通 initial critic；
- gap 使用稳定 ID，按 required capability、affected registry objects、repo scope 和 evidence
  去重；
- 默认最多 1–2 个 gap rounds，并限制每轮 gap 数和新增 subtasks 数；
- 只有产生新的 confirmed primitive 或 standalone capability provider 时才重新
  `plan_chains`；
- 连续一轮没有新增 primitive、重复 gap、缺少目标源码或预算耗尽时终止；
- 历史 candidate、失败原因和 gap-to-subtask-to-primitive lineage 必须持久化。

该回路是减少复杂链漏报的关键：它允许 Chain 反向指出“还缺什么能力”，但不会绕过
initial investigate/critic 的证据门槛。

### 14.9 Coverage Barrier 与预算公平性

每条 repo lane 和 integration lane 都生成 `coverage_ledger.json`。至少记录：

```json
{
  "registry_item_id": "repo-a::seam:x",
  "risk": "high",
  "status": "covered|not_dispatched|uncovered|unknown",
  "subtask_ids": [],
  "reason": "..."
}
```

`audit_context_coverage` barrier 在进入 global pool 前执行机械审计：

- 每个 repo 是否至少完成一条有效 analysis lane；
- high-risk invariant/seam/transition 是否被 subtask 覆盖，或有明确裁剪原因；
- integration-facing entries 是否进入 integration lane；
- 是否有 repo 因全局 top-K 或上下文竞争而零派发；
- 失败/partial lane 是否被正确传播到 summary。

Coverage ledger 不是“无漏洞证明”。`uncovered` 和 coverage 不完整必须解释为未知，不能
解释为安全。

预算采用“每仓保底 + 全局竞争”，而不是只使用一个 global top-K：

```yaml
multi_repo_analysis:
  min_subtasks_per_repo:
    spec: 3
    vuln: 8
    patch: 5
    feature: 5
  integration_caps:
    spec: 10
    vuln: 20
    patch: 10
    feature: 15
  global_caps:
    spec: 40
    vuln: 80
    patch: 50
    feature: 50
```

先满足每个 required repo 的最低证据密度，再让剩余预算按风险和可达性全局竞争。

### 14.10 Failure、Restore 与 Reporting 语义

每个 repo package 和 integration package 都有 `complete|partial|failed` 状态。默认：

- required repo fetch 失败：停止 workflow；
- required repo analysis 失败：允许保存 partial artifacts，但不得声称完整扫描；
- optional repo 失败：继续运行，并把缺失依赖加入 deployment known-unknowns；
- Chain 可以在 partial pool 上生成 candidate，但 summary 必须标记 coverage limitation；
- 只有完整证据闭合的 chain 才能成为 finding，不能用“其他 lane 可能存在证据”填补缺口。

恢复入口必须保留 repo scope 和 round lineage：

- `--start-from-subtask`：复用 repo/integration packages，只补跑未完成或选中的 initial
  subtasks；
- `--start-from-chain`：读取 federated registry、deployment manifest、global pool 和
  coverage ledger；
- selected subtask ID 必须接受 `<repo_id>::<subtask_id>` 和
  `integration::<subtask_id>`；
- gap-round 产物与 canonical initial results 分目录保存，但进入下一轮 pool 时统一去重。

最终 summary 聚合：

```text
repo-local standalone findings
+ integration standalone findings
+ closed chain findings
+ coverage / partial-analysis limitations
```

报告去重仍按最终根因与攻击路径进行，不能因为同一 primitive 出现在 local package、
integration package 和 chain context pack 中而重复计数。

### 14.11 推荐 Graph 形态

```text
START
  -> fetch_target_repo (once)
  -> materialize_repo_manifest
  -> global discovery
  -> [N x repo_analysis nested graph]
       repo search_*
       -> repo search_new_feature
       -> repo analyze_attack_surface
       -> repo plan_by_*
       -> [repo initial subtask battles]
       -> repo package + coverage ledger
  -> build_integration_context
  -> integration attack surface / registry / deployment manifest
  -> integration planners
  -> [integration initial subtask battles]
  -> audit_context_coverage
  -> materialize global primitive pool
  -> plan_chains
  -> prepare_chain_context
  -> [chain battles]
  -> collect_chain_gaps
       -> if bounded new gaps: gap initial subtasks -> update pool -> plan_chains
       -> otherwise: prepare_report_groups
  -> summary
  -> polish_report
  -> END
```

实现上优先使用一个可复用的 `build_repo_analysis_graph()` nested graph 和
`Send("repo_analysis", ...)`，不要为每个 repo 静态复制一整组 LangGraph node。这样可
保持主图稳定、状态隔离、并发控制和 restore 语义清晰。

### 14.12 验收标准

至少覆盖：

- single-repo + Chain 仍能运行，不因仓库数量被关闭；
- multi-repo + Chain 自动选择 hybrid layout；
- multi-repo + Chain disabled 保持当前 aggregate 行为；
- fetch 只执行一次，每个 repo lane 使用正确 canonical repo path 和 revision；
- 小仓库不会因全局 top-K 被零派发；
- local registries 使用 namespace，不因同名 entity 被自动合并；
- integration-only contract flaw 可以产出 integration primitive；
- global pool 同时包含 local 和 integration primitives，且 provenance 不丢失；
- candidate context pack 只装配相关 Registry 邻域和证据，但不限制 Agent 读取 workspace；
- chain gap 可生成新的 initial subtask，新 primitive 经 critic 确认后触发下一轮 planning；
- 重复 gap、无新增 primitive 或达到 round/budget 上限时可靠终止；
- required repo lane 失败时 summary 明确标记 partial coverage；
- restore/selected-run 能使用 repository-qualified IDs，且不覆盖 canonical artifacts。

# ZeroMDASH 架构说明

ZeroMDASH 是一个基于 LangGraph 编排的多 Agent 安全分析 workflow。它通过
Codex CLI、Claude Code、TraeX (`traecli` / `traex`)、Kimi Code、OpenCode、
DeepSeek Harness (`dsh`) 等外部 agent runtime，以及进程内的 DeepAgent
adapter，对目标项目进行源码获取、规范/历史漏洞/相似软件信息收集、攻击面分析、
子任务规划、子 agent 调查与 critic 复核，最后产出总结报告。

本文档分为三部分：

1. 项目代码架构
2. Agent workflow
3. 使用姿势：CLI + agent-config

---

## 1. 项目代码架构

### 1.1 顶层结构

```text
ZeroMDASH/
  zeromdash/              # 主分析 workflow
  zeromdash_repro/        # 复现/验证 workflow
  tests/                  # 单元测试
  pyproject.toml          # Python package metadata 和 CLI entrypoints
```

`pyproject.toml` 中注册了两个命令：

```toml
[project.scripts]
zeromdash = "zeromdash.cli:main"
zeromdash-repro = "zeromdash_repro.cli:main"
```

---

### 1.2 `zeromdash/` 主包

```text
zeromdash/
  __init__.py
  cli.py
  graph.py
  gather.py
  gather_graph.py
  gather_state.py
  nodes/
    __init__.py
    core/
    fetch_target_repo.py
    prepare_scan_scope.py
    search_*.py
    plan_by_*.py
    analyze_attack_surface.py
    dispatch_subtasks.py
    investigate_subtask.py
    critic_subtask.py
    finalize_subtask.py
    materialize_chain_pool.py
    plan_chains.py
    dispatch_chains.py
    chain_investigate_subtask.py
    chain_critic_subtask.py
    finalize_chain_subtask.py
    prepare_report_groups.py
    gather_analyze_attack_surface.py
    gather_plan_chains.py
    dispatch_gather_chains.py
    gather_chain_investigate_subtask.py
    gather_chain_critic_subtask.py
    gather_finalize_chain_subtask.py
    gather_prepare_report_groups.py
    gather_summary.py
    summary.py
    polish_report.py
  state.py
  agents.py
  workspace.py
  prompts.py
  presets.py
  skills.py
  presets/
    AGENTS.md
    CLAUDE.md
    .claude/
    .codex/
    .kimi-code/
    roles/
    contracts/
    skills/
```

#### `cli.py`

CLI 入口，负责：

- 解析 `zeromdash` 命令行参数。
- 加载 `.env`。
- 解析 `--agent-config` YAML 文件，包括顶层 `max_concurrency`（默认 8）、
  `top_K`（含 `chain` bucket）、`chain` 聚合控制段（`enabled` /
  `max_length` / `max_successors_per_capability` / `beam_width` /
  `max_candidates_before_top_k` / `max_battle_rounds` /
  `attacker_entry_capabilities`）、`gather` 跨 workspace 控制段和 per-node
  runtime/config/provider/env/fallbacks。
- 解析 `--scan-mode gather --gather-workspace-to-chain <manifest>`，并将其分派到
  独立的 `gather_graph.run_gather(...)`。
- 对每个 node 的 runtime/config/provider/env 以及显式 fallbacks 做启动前 health check。
- 如果某个 node health check 失败，则 pause 等待人工输入临时 runtime/config/provider/model。
- 调用 `zeromdash.graph.run(...)` 启动 workflow。

关键设计：

- 只执行 agent-config 中显式声明的 fallback chain；不会隐式猜测备用 runtime。
- 每个 node 使用明确配置的 primary runtime，并在该 runtime 的既有重试耗尽后才切到 fallback。
- health check 失败需要 human 介入，而不是静默切换到其他 agent。

---

#### `graph.py`

LangGraph 拓扑定义，负责：

- 构建主 workflow graph。
- `gather_graph.py` 构建跨 workspace 的独立 gather graph 和 gather-chain nested graph。
- 构建 subtask 嵌套 graph。
- 构建 `--start-from-subtask` 使用的恢复图、`--select-subtask-to-run`
  使用的隔离恢复图、`--start-from-chain` 使用的 chain 恢复图、
  `--select-chain-to-run` 使用的隔离 chain 恢复图、
  `--start-from-summary` 使用的 `summary -> polish_report`
  恢复图，以及 `--start-from-polish-report` 使用的单节点报告润色图。
- 初始化 `ZeroMDASHState`。
- 创建 workspace。
- 注入 Langfuse metadata。
- 调用 `graph.invoke(...)`，并把 `max_concurrency` 传入 LangGraph config
  以限制 `Send(...)` fan-out 的同时执行数量。

主图大致结构：

```text
START
  -> fetch_target_repo
  -> prepare_scan_scope
  -> search_spec
  -> search_fuzz_driver
  -> search_similar_software -> N x search_similar_history
  -> search_target_history
  -> search_new_feature
  -> analyze_attack_surface
  -> plan_by_spec
  -> plan_by_vuln_similar
  -> plan_by_vuln_patch
  -> plan_by_new_feature
  -> dispatch_subtasks
  -> N x subtask nested graph
  -> materialize_chain_pool
  -> plan_chains
  -> dispatch_chains
  -> N x chain_subtask nested graph
  -> prepare_report_groups
  -> summary
  -> polish_report
  -> END
```

`scan_mode=gather` 不进入上面的 fetch/search/planner 主图，而使用独立拓扑：

```text
START
  -> gather_analyze_attack_surface
  -> gather_plan_chains
  -> dispatch_gather_chains
  -> N x gather_chain_subtask nested graph
       gather_chain_investigate_subtask
         <-> gather_chain_critic_subtask
         -> gather_finalize_chain_subtask
  -> gather_prepare_report_groups
  -> summary
  -> polish_report
  -> END
```

`gather.py` 在 graph 启动前校验 multi-target manifest，为源 artifact 和源码建立
隔离 snapshot，以 `<target_id>::<local_id>` 命名空间化 primitive、standalone
finding 和 local chain，并写出 `inputs/gather_inputs.lock.json` 与
`log/state/gather_evidence_pool.json`。源 workspace 不作为输出目录使用。

gather graph 的语义推理由 native subagents 完成，Python 只负责 artifact 选择、
引用完整性、跨 target 条件、source drift、constraint/CVSS 和报告格式等硬门槛。
详细数据契约与边界见 [`GATHER_CHAIN.md`](./GATHER_CHAIN.md)。

---

#### `nodes/`

Workflow 业务逻辑包。每个 LangGraph node 使用独立模块；`nodes/__init__.py`
保留历史 `zeromdash.nodes` facade，兼容现有 import 和 monkeypatch 入口。
共享的 runtime 配置、agent 调用与 retry、qualification、planner/dispatch、
repository materialize、报告校验逻辑位于 `nodes/core/`。

主要职责：

- 根据 state 拼 prompt。
- 准备 sub workspace。
- 根据 node agent-config 选择 runtime/config/provider/env。
- 调用 agent。
- 解析 agent 输出。
- 写入 workspace 中间产物。
- 更新 LangGraph state。

主要节点分组：

```text
fetch:
  fetch_target_repo
  prepare_scan_scope

gather:
  search_spec
  search_fuzz_driver
  search_similar_software
  search_similar_history
  search_target_history
  search_new_feature

fuse:
  analyze_attack_surface

planning:
  plan_by_spec
  plan_by_vuln_similar
  plan_by_vuln_patch
  plan_by_new_feature

dispatch:
  dispatch_subtasks
  dispatch_all

subtask loop:
  investigate_subtask
  critic_subtask
  route_after_critic
  finalize_subtask

chain planning:
  materialize_chain_pool
  plan_chains
  dispatch_chains
  dispatch_all_chains

chain subtask loop:
  chain_investigate_subtask
  chain_critic_subtask
  route_after_chain_critic
  finalize_chain_subtask

report:
  prepare_report_groups

final:
  summary
```

---

#### `state.py`

LangGraph state schema。

核心类型：

- `ZeroMDASHState`：主图 state。
- `Subtask`：planner 产出的子任务。
- `Finding`：subtask 最终产出的 finding。
- `Primitive`：已确认但不能独立闭合为漏洞的攻击原语，记录稳定 id、
  repo/component、前置条件（`entry_conditions` / `required_capabilities`）、
  攻击者控制对象、获得的 capability、交接对象、可靠性、证据、来源 subtask
  和仍缺少的下一跳能力。
- `ChainCandidate`：`plan_chains` 产出的有序原语组合，包含 bindings、
  全局约束、期望终端影响、rank 和裁剪上下文。
- `ChainFinding`：端到端闭合并通过 chain 资格门槛的 finding，基于完整
  攻击链计算 CVSS v4.0。
- `ReportGroup`：`prepare_report_groups` 产出的报告归组，按最终根因和
  攻击路径去重 standalone finding 与 chain finding。
- `SubtaskInputState`：嵌套 subtask graph 输入；除 subtask 外还透传 `common_focus` / `scan_scope` / `scope_path` / `attack_surface` / `spec_doc` / `similar_writeups`，让 investigator 在完整仓库上下文和 diff 归因范围下做 top-down 调查。
- `SubtaskState`：subtask graph 内部状态。
- `SubtaskOutputState`：subtask graph 输出。
- `ChainSubtaskInputState` / `ChainSubtaskState` / `ChainSubtaskOutputState`：
  嵌套 chain graph 的输入/内部/输出状态；输入透传 `chain_candidate`、
  `chain_pool` 和 `max_chain_iterations`。

并发聚合字段使用 `operator.add` reducer，例如：

```python
similar_writeups
similar_patches
spec_findings
vuln_candidates
patch_findings
feature_findings
confirmed_primitives
chain_candidates
chain_findings
errors
```

这样多个并发 `Send(...)` 返回的 list 会自动聚合。

---

#### `agents.py`

Agent runtime adapter。

当前支持：

- `claude_code`
- `codex`
- `traex`
- `kimi`
- `opencode`
- `dsh`
- `deepagent`

其中 `claude_code`、`codex`、`traex`、`kimi`、`opencode`、`dsh` 是外部
CLI runtime；`deepagent` 是进程内 Python adapter，会导入
`deepagents.create_deep_agent` 并调用其 LangGraph app。

所有 agent adapter 暴露统一接口：

```python
run(prompt, cwd=None, timeout=None, extra_args=None, env=None) -> AgentResult
```

其中：

- 一般 runtime 的 `cwd` 指向本次调用的 sub workspace。
- `traex` 使用 `traecli exec -C <sub_workspace> -`，通过 stdin 接收 prompt，
  通过 `--output-last-message` 返回最终消息；object-shaped 结构化节点会同时
  使用 `--output-schema <sub_workspace>/output.schema.json`。TraeX 0.201.1
  不接受顶层 array schema，因此 planner 的 `Subtask[]` 继续由 ZeroMDASH
  orchestrator 的现有 validator 校验。
- `traex` 将 sub workspace 作为项目根以加载 `AGENTS.md`，并通过
  `--add-dir <workspace_base>` 给完整任务 workspace 增加可写权限。
  Adapter 同时设置 `project_root_markers=[]`，防止 TraeX 沿父目录继续继承
  task workspace 或宿主仓库中的其他 `AGENTS.md`。
- `dsh` adapter 把该参数当作**逻辑 cwd**；其进程物理 cwd 指向 task
  workspace base，使 DSH 的单根 `workspace-write` sandbox 能覆盖完整任务。
- `extra_args` 来自 agent-config 的 `config`。
- `env` 来自 agent-config 的 `provider` 和 `env`。

`AgentEnv` 支持：

```python
dict[str, str | None]
```

含义：

- `KEY: "value"`：设置/覆盖环境变量。
- `KEY: None`：从 agent 子进程环境中删除该变量。

---

#### `workspace.py`

管理每次任务的文件系统 workspace。

典型布局：

```text
<workspace-root>/workspace_for_<target>/
  main/
    repo/              # 目标源码
    scope/             # scope.json / changes.diff / changed files/symbols
    spec/              # 规范/标准资料
    attack_surface/    # attack_surface.md + domain_invariant_registry.json
    writeup/           # 目标项目历史漏洞 writeup
    patch/             # 目标项目历史 patch
      _patch_commits.json # patch-manifest v1.0; single/multi repo 统一格式
  similar/
    <similar-software>/
      repo/
      writeup/
      patch/
  log/
    review_log/
    state/
      plan_by_*.json   # planner 结构化计划与审计状态
      dispatch_plan.json
      chain_pool.json
      chain_plan.json  # 有界 chain 候选与裁剪原因
    subtask_res/
    primitive_res/     # confirmed primitive 结构化产物
    chain_res/         # 端到端闭合的 chain finding
    selected_chain_runs/  # --select-chain-to-run 的隔离产物
    agent_commands.jsonl
  sub_workspace/
    node_<node>/
    node_<node>/subtask_<id>/
  workspace.json
```

每个 node/subtask 分支会有一个稳定的 sub workspace。没有 `subtask_id` 的普通节点使用：

```text
sub_workspace/node_<node>/
```

带 `subtask_id` 的 fan-out 分支使用：

```text
sub_workspace/node_<node>/subtask_<id>/
```

同一个 node/subtask 分支中的重试或多轮 investigate/critic 会复用对应目录。物化 preset 时按当前 runtime 过滤 backend-specific 文件：

- `CLAUDE.md`
- `AGENTS.md`
- `.claude/settings.json`
- `.codex/config.toml`
- `.kimi-code/AGENTS.md`
- `.kimi-code/local.toml`
- `skills/`
- `output.schema.json`（仅需要结构化 JSON 输出的 node）

其中根目录 `AGENTS.md` 由 Codex 与 TraeX 共用；`.codex/config.toml` 只会
materialize 给 Codex。TraeX 的 workspace 权限、headless 默认审批策略、
ephemeral session、最终消息文件和 structured-output schema 均由 adapter 的
CLI 参数控制，不需要额外的项目级 `.trae/` 配置文件。`exec` 模式无法交互审批，
因此 adapter 不启用 Auto-Review，也不使用危险的 full-access bypass。

`roles/` 与 `contracts/` 是 presets 内部目录，不会原样复制到 sub workspace；它们会被注入到 runtime 指令文件的 `{role_block}` / `{contract_block}` 占位符，或按 node 拷贝成单个 `output.schema.json`。

---

#### `prompts.py`

各 node 的 prompt 模板。

节点函数在 `nodes/<node_name>.py` 中将 state、workspace path、focus、subtask、critic feedback 等信息填充进这些模板。

---

#### `presets.py` / `presets/`

负责把运行时 preset materialize 到 sub workspace。

`presets/` 目录包含：

- Agent 全局指令：`CLAUDE.md`、`AGENTS.md`
- Claude/Codex/Kimi runtime 配置；TraeX 复用 `AGENTS.md`
- 各 node role card
- structured output contract schema
- critic expert skills

---

#### `skills.py`

critic 阶段使用的 expert skill discovery。

`critic_subtask` 会在运行时发现 bundled skills 和 sub workspace 自定义 skills，并生成 `skills_catalog.md` 供 critic 选择专家视角。

---

## 2. Agent workflow

### 2.1 主 workflow 总览

```text
zeromdash CLI
  -> parse args / agent-config
  -> startup health check per node
  -> graph.run
    -> Workspace.create
    -> build_graph
    -> graph.invoke
```

主图分为六个阶段：

1. Fetch：获取目标源码。
2. Gather：收集规范、fuzz driver、相似软件、历史漏洞。
3. Fuse：融合资料，分析攻击面。
4. Planning：生成漏洞分析子任务。
5. Subtask Loop：每个子任务独立调查、critic 复核、终态分类（standalone
   finding / confirmed primitive / observation / rejected / inconclusive）。
6. Chain 聚合：把 standalone finding 和 confirmed primitive 汇入 chain 池；
   确定性有界搜索只提供 advisory，`plan_chains` 使用原生 subagent 组合候选，
   再用第二级 chain investigate/critic battle 验证端到端闭环，最后归组去重后进入 summary。

这个 workflow 的核心不是固定规则扫描，而是**领域自适应的漏洞挖掘工程**：

- 先用 gather 阶段发散理解目标领域：规范、测试入口、相似实现、历史漏洞。
- 再用 threat model 和 attack surface 把发散信息收敛到可达入口、信任边界、权限边界和高风险状态机。
- planner 不直接“报洞”，而是把规格差异、历史漏洞模式、补丁遗漏模式转成可验证 subtask。
- investigator 对每个 subtask 做 top-down 调查：先读 attack surface 报告 + spec + 历史漏洞，定出入口 / 信任边界 / sink 类别，再 code-grounded 验证；critic 负责反证、降噪、要求证据，避免把猜测当漏洞。
- 最终 summary 面向 triage：明确攻击面、利用前提、影响、证据路径、置信度和下一步复现策略。

因此 wrapper agent 生成 CLI + agent-config 时，最重要的输入不是“给每个 node 都写很长 focus”，而是：

1. 确认目标仓库和 fetch 方式。
2. 写清威胁模型。
3. 指明少数必须关注的领域资源，例如 fuzz dashboard、核心规范、稳定分支或历史安全公告。
4. 让发散阶段保持发散；规划/复核阶段依赖上游产物和 subtask 证据，调查阶段则显式接收 attack surface 报告 + spec + 历史漏洞 + 威胁模型做 top-down 调查。

---

### 2.2 Fetch 阶段

```text
START -> fetch_target_repo -> prepare_scan_scope
```

`fetch_target_repo` 负责把目标源码 materialize 到：

```text
main/repo/
```

当 `target` 是本地目录时，runtime 不再依赖 agent 执行复制；编排器会确定性地把完整源码复制到
`main/repo/`，跳过原目录中的 `.git` / `.zeromdash` 等本地元数据，并且不修改原目录。
URL / 项目名等非本地目录目标仍由 `fetch_target_repo` agent 解析和拉取。

如果源码获取失败，或目录为空，会直接停止整个 workflow，避免后续节点分析空源码树。

`prepare_scan_scope` 是确定性节点，不调用模型：

- `scan_mode=full`：完整仓库进入扫描范围，保持原有全仓扫描行为。
- `scan_mode=diff`：仓库本身已经包含 patch 后代码；节点只解析
  `--diff-file`，或对远程 git target 解析 `--diff-git before..after`，写出
  `main/scope/`，并校验 diff 中非删除路径存在于 patched repo。
- `--diff-git` 会要求 fetch 阶段保留 `.git`，scope 阶段补取/解析两个 ref，
  detached checkout 到 `after` commit，再生成 two-dot diff。支持 commit、tag
  和 branch。
- diff 是归因、优先级和卡点范围，不是代码阅读边界。planner / investigator /
  critic 仍可读取完整仓库来分析调用链、类型、配置、生命周期和 sibling paths。

---

### 2.3 Gather 阶段

源码获取成功后，主图 fan-out 到多个信息收集节点：

```text
prepare_scan_scope
  -> search_spec
  -> search_fuzz_driver
  -> search_similar_software
  -> search_target_history
```

其中 `search_similar_software` 会进一步动态 fan-out：

```text
search_similar_software
  -> search_similar_history(similar_software=A)
  -> search_similar_history(similar_software=B)
  -> search_similar_history(similar_software=C)
```

这些分支的结果通过 state reducer 聚合到：

```text
similar_writeups
similar_patches
```

这些 gather 节点全部完成后，`search_new_feature` 才运行。它读取 spec、fuzz、
target history、similar history 和源码，产出 `main/feature/` 下的新近变化或弱覆盖
feature surface：

```text
{search_spec, search_fuzz_driver, search_similar_history, search_target_history}
  -> search_new_feature
```

---

### 2.4 Attack surface barrier

`analyze_attack_surface` 依赖 gather 阶段结果和 `search_new_feature` 的 feature
surface 产物。

Graph 使用 multi-source edge 作为 barrier：

```text
{search_spec, search_fuzz_driver, search_similar_history, search_target_history}
  -> search_new_feature
  -> analyze_attack_surface
```

这样可以避免 `analyze_attack_surface` 被多个 predecessor 重复触发。

---

### 2.5 Planning 阶段

攻击面分析完成后，进入四个 planner：

```text
analyze_attack_surface
  -> plan_by_spec
  -> plan_by_vuln_similar
  -> plan_by_vuln_patch
  -> plan_by_new_feature
```

四个 planner 分别产出：

```text
spec_subtasks
vuln_subtasks
patch_subtasks
feature_subtasks
```

每个 subtask 大致包含：

```json
{
  "id": "...",
  "bucket": "spec | vuln | patch_miss | feature",
  "objective": "...",
  "hints": {}
}
```

---

### 2.6 Subtask dispatch

planner 全部完成后，进入统一 dispatch barrier：

```text
{plan_by_spec, plan_by_vuln_similar, plan_by_vuln_patch, plan_by_new_feature}
  -> dispatch_subtasks
```

diff 模式不设置默认数字上限。`analyze_attack_surface` 先生成
`## Diff Risk Surface Registry`；每个 `RS-XXX` 表示一条独立的
changed-code anchor -> untrusted input -> state machine -> sink 数据流及其安全
不变量。四个 planner 围绕这些 canonical risk surface 挂载 spec / CVE /
patch / feature 证据，而不是按证据条目数量拆 subtask。

diff 模式下每个 planner 会写三类产物：

```text
plan_by_*.candidates.json    # 模型原始候选，保留召回审计
plan_by_*.json               # 按 risk_surface_id 做桶内聚合后的可执行计划
plan_by_*.convergence.json   # 过滤/聚合映射和原因
```

`dispatch_all` 再按同一 `risk_surface_id` 做跨 bucket 聚合，把其他
objective 和证据引用写入代表任务的 `hints.merged_subtasks`，然后将独立风险面
转成：

```python
Send("subtask", child_state)
```

`max_concurrency` 只限制已派发任务的同时执行数量。`top_K` 是用户显式配置的
成本上限；未配置时不截断，配置后可能牺牲覆盖率。diff mode 不隐式设置
`top_K`。full mode 保持原有全仓 planning / dispatch 语义。

实际选择写入 `log/state/dispatch_plan.json`，包含每个 bucket 的候选数、
diff 归因数、独立风险面数、最终任务、合并去向以及未选原因。无法建立
diff anchor -> sink 因果链的 adjacent / pre-existing 候选只保留在
`*.candidates.json`，不单独派发。

diff 模式下 Send 顺序按 spec / vuln / patch / feature 做 round-robin，避免某个
大 bucket 把 `max_concurrency` 槽位和执行队列长期占满。full 模式保持原有顺序。

如果没有任何 subtask，全新扫描仍直接进入 `summary`，保证 workflow 总是有最终输出；但恢复场景里只要 state 已有 finding 或 primitive，即使本批没有新 subtask，也会继续进入 `materialize_chain_pool` 做 chain 聚合。

---

### 2.7 Subtask nested graph

每个 subtask 都会进入一个独立的嵌套图：

```text
START
  -> investigate_subtask
  -> critic_subtask
  -> route_after_critic
      -> investigate_subtask   # verdict == revise 且未达到 max_iterations
                                # 或第一轮 no-finding 试图 confirm/reject
      -> finalize_subtask      # verdict == confirm/reject 或达到 max_iterations
  -> END
```

使用 nested graph 的原因是隔离每个 subtask 的 scratch state：

```text
subtask
iteration
investigation
review
review_history
```

父图通过 `_dispatch` 把上游上下文透传进 `SubtaskInputState`，让 investigator 做 top-down 调查而非纯 code-by-code：

```text
common_focus        # 顶层威胁模型
scan_scope          # full/diff 模式、changed files/hunks、卡点策略
scope_path          # main/scope/scope.json
attack_surface      # analyze_attack_surface 产出的报告路径
spec_doc            # search_spec 产出的规范路径
similar_writeups    # 相似软件历史漏洞 writeup 目录
feature_docs        # main/feature 中的新/弱覆盖 feature surface 产物
```

父图只接收最终输出：

```text
spec_findings
vuln_candidates
patch_findings
feature_findings
confirmed_primitives
errors
```

这样多个 subtask 并发时不会互相污染中间状态。

---

### 2.8 Critic feedback loop

`investigate_subtask` 负责对子任务做代码调查。

`critic_subtask` 负责严格复核调查结果，并输出：

```json
{
  "verdict": "confirm | reject | revise",
  "severity": "...",
  "confidence": 0.0,
  "feedback": {
    "gaps": [],
    "requested_evidence": []
  },
  "selected_skills": []
}
```

如果 verdict 是 `revise`，下一轮 `investigate_subtask` 会收到上一轮 critic feedback。
如果第一轮 investigation 就输出 `no-finding`，runtime 会阻止 `confirm/reject`
直接终止，并强制一轮 `revise`，要求 investigator 发散枚举同一漏洞模式的所有可能路径。

每轮 investigation 的格式重试不计入 `iteration`。orchestrator 在每次 attempt
前删除 sub-workspace 中旧的 `finding.json` / `investigation.json` /
`output.json`，先校验 stdout；只有 stdout 不满足非空 title/detail、
`evidence.code_locations` 和 `evidence.call_path` 契约时，才尝试读取本轮新生成
且通过同一契约的 JSON artifact。三次格式尝试及显式 runtime fallback 都失败时，
CLI 会请求临时 runtime/config/provider/model，健康检查通过后重试当前调用，
不增加 investigation iteration。有效的 critic revise/reject 仍走正常业务流程。
没有启用人工恢复协调器的程序调用，仍结束该 subtask 并返回 errors。

`nodes/core/recovery.py` 用运行作用域内的 ContextVar 共享协调器，由 LangChain
传播到并发 worker；锁和回调不进入可序列化的 graph state。worker 把恢复请求
放入队列，由 CLI 主线程串行完成输入和健康检查。每个节点的临时配置带 revision，
等待中的旧 revision 失败复用已更新的配置；更新仅作用于调用副本，不并发修改
原始 state 或 YAML。嵌套调用由最外层重试循环负责恢复，防止在尚有自动尝试或
fallback 时提前询问。

EOF/取消会唤醒所有等待恢复的任务并阻止新 agent 调用，已有产物保留；正在执行的
进程允许完成。恢复记录写入 `runtime_recovery.jsonl`，临时配置写入成功结束时的
`final_state.json`。人工重试的 attempt 日志带 `recovery-N`，不覆盖耗尽的日志。

DSH adapter 额外处理 subprocess timeout：若该 invocation 在超时前生成了相对
启动快照发生变化、非空且可解析为 JSON object 的 `finding.json`，adapter 会结束
等待并把该文件交回上述 artifact fallback；完整 schema 仍由 orchestrator 的同一
validator 校验。陈旧、空、损坏或不满足契约的文件不会掩盖 timeout。

终止条件：

```text
verdict in {confirm, reject}
或 iteration >= max_iterations
例外：第一轮 no-finding 总是先强制 revise 一轮，第二轮后再受终止条件约束
```

`min_critic_skills` 会作为 prompt 中的最低 skill 选择要求传给 critic。运行时会过滤不存在的 skill，并在 `review.feedback.gaps` 中记录选择数量不足的问题，同时设置 `skill_selection_ok=false`。当前路由逻辑只按 `verdict`、`iteration` 和第一轮 no-finding 规则决定是否 finalize；skill 数量不足本身不会强制改写 verdict。

---

### 2.9 Chain 聚合阶段

所有第一级 subtask 完成后，主图进入 chain 聚合阶段：

```text
subtask (全部完成)
  -> materialize_chain_pool
  -> plan_chains
  -> dispatch_chains
  -> N x chain_subtask nested graph
  -> prepare_report_groups
```

`materialize_chain_pool` 是确定性节点，汇集三路 confirmed primitive：

- state 中本批次的 `confirmed_primitives`。
- `log/primitive_res/*.json`。
- `log/subtask_res/*.json` 中内嵌的 `primitive`（用于恢复路径）。

此外，每个通过资格门槛的 standalone finding 也会转换成一个 capability
provider primitive 进入同一个池：它保留独立报告资格，同时作为已证实
capability 供后续链条消费。池内 primitive 按稳定 id 去重。

`plan_chains` 是 native-subagent-required 的 Agent-Native 规划节点。代码层先生成
有界 deterministic advisory，但它不做最终语义裁决：

- 用 `required_capabilities` -> `capabilities_gained` 的结构化兼容关系
  （kind / object_type / scope / principal / tenant / address_space 等字段）
  匹配后继；只有消费已有 capability 的 primitive 才能作为后继，避免任意
  拼接；匹配/不匹配均作为 advisory 输入。
- 有界搜索：`max_length`（默认 4）、`max_successors_per_capability`
  （默认 4）、`beam_width`（默认 64）、`max_candidates_before_top_k`
  （默认 200），最后按 rank 截断到 `top_K.chain`（默认 16）。
- planner 通过 forward/backward/seam/constraint 原生子 agent 读取完整 primitive
  pool、Domain Model and Invariant Registry 及 advisory，修复语义近似、对象身份、
  handoff 和 emergent-impact 候选。
- 所有裁剪都记录原因（`missing_required_capability` / `max_length` /
  `cycle` / `successor_cap` / `beam_width` / `top_k` 等），与候选一起写入
  `log/state/chain_plan.json`。

`dispatch_chains` 把候选转成：

```python
Send("chain_subtask", child_state)
```

并透传 `chain_candidate`、`chain_pool` 和 `max_chain_iterations`（来自
`chain.max_battle_rounds`，默认 2）。

chain 嵌套图与第一级 subtask graph 同构：

```text
START
  -> chain_investigate_subtask
  -> chain_critic_subtask
  -> route_after_chain_critic
      -> chain_investigate_subtask   # verdict == revise 且未达轮数上限
      -> finalize_chain_subtask      # confirm/reject 或达到上限
  -> END
```

`chain_investigate_subtask` 必须给出完整攻击者入口、按顺序排列的
primitive、每一步 capability 转换、跨组件交接对象和最终安全影响；
`chain_critic_subtask` 逐边核查前置条件是否由上一跳满足、版本/配置是否
能同时成立、对象和地址空间是否一致，以及是否仍依赖未证实的外部原语。
两者都是 native-subagent-required 节点，使用独立的
`chain-investigation.schema.json` / `chain-review.schema.json` 契约和
role card（`presets/roles/chain_*.md`）。

`finalize_chain_subtask` 执行机械完整性硬门槛：校验 primitive/registry ID、顺序、
逐边 critic verdict、未满足事实、证据和 CVSS，但不重新用字符串 matcher 推翻
Agent 已核验的 binding。只有端到端闭环、所有必要
primitive 均已确认且产生最终直接 C/I/A 影响的组合，才写入
`log/chain_res/<chain_id>.json` 成为 `ChainFinding`，并基于完整攻击链
计算 CVSS v4.0；终态影响可以由多个单独无 terminal impact 的 primitive 组合后
首次产生。未闭合组合只保留为 retained candidate / confirmed
primitive，不会伪装成漏洞。

`prepare_report_groups` 在 summary 之前做确定性归组：standalone finding
和 chain finding 按最终根因和攻击路径去重，chain finding 吸收其组成
primitive 对应的 standalone 报告资格，避免同一问题既单独报告又作为
chain 组成部分重复计数。

---

### 2.10 Finalize 和 Summary

`finalize_subtask` 将最终结果落盘到：

```text
log/subtask_res/<subtask-id>.json
```

canonical result 保留最终 finding 和完整迭代历史：

```json
{
  "finding": {},
  "history": []
}
```

如果 verdict 是 `reject`，只落盘，不返回 finding。

`finalize_subtask` 同时给每个结果做终态分类（`outcome_type`）：

```text
standalone_finding   # 通过资格硬门槛，自身闭合为漏洞，计算 CVSS v4.0
confirmed_primitive  # 机制/可达性/能力已确认，但自身不能闭合为漏洞
observation          # 有安全相关事实，不足以作为原语参与 chain
rejected             # 明确不是问题
inconclusive         # 证据不足或 critic 轮次耗尽
```

`confirmed_primitive` 不单独计算 CVSS，也不会因为
`standalone_security_impact=false` 或仍需其他原语而被丢弃：
`build_confirmed_primitive` 会生成稳定 id、前置条件、攻击者控制对象、
capability、交接对象、可靠性、证据、来源 subtask 和缺失的下一跳能力，
落盘到 `log/primitive_res/<primitive-id>.json`，并内嵌在对应
`subtask_res` 记录中随 `confirmed_primitives` 写回父图。

如果是 confirm 或达到 max iteration，则按 bucket 写回父图：

```text
bucket == spec       -> spec_findings
bucket == vuln       -> vuln_candidates
bucket == patch_miss -> patch_findings
bucket == feature    -> feature_findings
```

diff 模式下 finding 额外保留：

```text
scope_relation      # introduced/enabled/regressed/pre_existing/unrelated/unknown
diff_evidence       # changed/context locations + change-to-sink causal path
scope_verdict
gate_decision       # block/warn/ignore
```

最后 `summary` 消费 `prepare_report_groups` 产出的 `ReportGroup`：
standalone finding 与 chain finding 已按最终根因和攻击路径归组去重，
组内再按根因、sink/state、触发条件和代码路径聚合，然后用同一组
`VULN-XXX` id/顺序输出中英文报告：

```text
summary.en.md
summary.zh_CN.md
summary.md          # summary.en.md 的兼容副本
gate_result.json    # 机器可读 MR 卡点结果
```

`gate_result.json` 的 `block` 条件由 orchestrator 校准：finding 必须被 critic
confirm，severity 为 high/critical，scope verdict 为
introduced/enabled/regressed，并且存在完整的 change-to-sink path 和因果解释。
pre-existing/unrelated finding 即使真实也不阻塞当前变化。

---

### 2.11 提前终止与恢复图

主图支持两个提前终止点：

```text
--till-node analyze:
fetch/gather -> analyze_attack_surface -> END

--till-node plan:
fetch/gather -> search_new_feature -> analyze_attack_surface -> enabled planners -> finish_plan -> END
```

`--till-node analyze` 会校验 `main/attack_surface/attack_surface.md` 非空且
`domain_invariant_registry.json` 结构合法。`--till-node plan` 会校验所有 enabled planner 都写出合法的 `log/state/plan_by_*.json`。

`--start-from-subtask <workspace>` 不走完整主图，而是从已有 workspace 重建 state，再进入裁剪图：

```text
START
  -> dispatch_subtasks
  -> N x subtask nested graph
  -> materialize_chain_pool
  -> plan_chains
  -> dispatch_chains
  -> N x chain_subtask nested graph
  -> prepare_report_groups
  -> summary
  -> polish_report
  -> END
```

恢复时会读取 `workspace.json`、可选的 `final_state.json`、`main/repo/`、`main/attack_surface/attack_surface.md`、`log/state/plan_by_spec.json`、`plan_by_vuln.json`、`plan_by_patch.json`，以及存在时的 `plan_by_feature.json`。禁用的 track 不要求对应 planner 文件；旧 workspace 没有 feature plan 时仍可恢复。进入 dispatch barrier 后会重新做 diff 归因和跨 bucket 聚合并生成 `dispatch_plan.json`。旧 workspace 没有 `RS-XXX` registry 时使用保守的路径和语义兼容推断，宁可多派发也不做激进误合并。subtask 全部完成后继续走 chain 聚合阶段；恢复场景里如果 state 已有 finding/primitive，即使本批没有新 subtask 也会进入 chain pool。

`--select-subtask-to-run` 是上述恢复入口的隔离执行模式。它先按 planner
JSON 校验并筛选指定 ID，清空本次临时 state 的
`completed_subtask_ids`，然后进入独立恢复图：

```text
START
  -> dispatch_subtasks
  -> selected N x subtask nested graph
  -> collect_selected_subtask_statuses
  -> END
```

该图没有 summary 边，也不写 canonical `log/subtask_res/`。默认产物位于：

```text
log/selected_temp_<UTC timestamp>/
  attempts/
  investigations/
  critic_reviews/
  results/
  agent_commands.jsonl
  selected_subtask_statuses.json
  final_state.json
```

显式 `--select-subtask-to-run-log-dir` 必须指向一个不存在的目录。
`results/<subtask-id>.json` 仍保留 `finding + history`，便于和 canonical
结果逐轮比较；是否采纳该结果由后续人工或显式提升流程决定。

`--start-from-chain <workspace>` 从已有 workspace 重建 state 后直接进入
chain 聚合阶段：

```text
START
  -> materialize_chain_pool
  -> plan_chains
  -> dispatch_chains
  -> N x chain_subtask nested graph
  -> prepare_report_groups
  -> summary
  -> polish_report
  -> END
```

chain 池来自 `log/primitive_res/*.json`、`log/subtask_res/*.json` 中内嵌的
primitive，以及 subtask_res 里通过资格门槛的 standalone finding 转换出的
capability provider；随后重新生成 `log/state/chain_plan.json` 并继续
chain battle、归组和 summary。

`--select-chain-to-run` 是上述入口的隔离执行模式：只重跑指定 chain id
（`chain_plan.json` 中的稳定 `chain_<hash>`），进入独立恢复图：

```text
START
  -> materialize_chain_pool
  -> plan_chains
  -> dispatch_chains
  -> selected N x chain_subtask nested graph
  -> collect_selected_chain_statuses
  -> END
```

该图没有 summary 边，也不写 canonical `log/chain_res/`。默认产物位于
`log/selected_chain_runs/<timestamp>/`；显式
`--select-chain-to-run-log-dir` 必须指向一个不存在的目录。

`--start-from-summary <workspace>` 只构建单节点 graph：

```text
START -> summary -> END
```

它要求 `workspace.json`、非空 `main/repo/`、非空 `main/attack_surface/attack_surface.md` 和 `log/subtask_res/*.json`。当前实现会重新加载 `subtask_res` 中序列化的 finding，并按 `kind` 分到 `spec_findings` / `vuln_candidates` / `patch_findings` / `feature_findings`；这是报告重生成路径，不会重新运行 critic。

---

## 3. Agent runtime/config 设计

### 3.1 Runtime

`agent-config` 中每个 node 可以指定 runtime：

```yaml
runtime: claude_code
runtime: codex
runtime: kimi
runtime: opencode
runtime: dsh
runtime: deepagent
```

其中 `investigate_subtask`、`critic_subtask`、`plan_chains`、
`chain_investigate_subtask`、`chain_critic_subtask`、`summary` 是 native-subagent-required
节点，只允许使用当前 adapter 已验证能创建原生子 agent 的 harness：

```text
codex / codex_cli
traex / trae-cli
claude_code
```

限制同时覆盖 primary 和全部显式 fallback；只要其中一个 runtime 不具备该
能力，配置解析或执行前解析 runtime chain 时就 fail closed。Codex 调用会显式
加入 `--enable multi_agent`，TraeX 调用会加入
`--config features.multi_agent_v2.enabled=true`，Claude Code 则只在这六个节点
生成的 local settings 中允许 `Agent` tool。Kimi、OpenCode、DeepAgent 当前 adapter 没有经过
验证的原生子 agent 契约；DSH 的 bundled headless-minimal overlay 明确禁用了
subagent tools，所以它们只能用于其他节点。

术语上，`subtask` 是 ZeroMDASH 自己通过 LangGraph `Send("subtask", ...)`
派发的调查/复核工作单元；`subagent` 只指 Codex、TraeX 或 Claude Code harness
内部真正创建的原生子代理。

规范 runtime 名称：

```text
claude_code
codex
kimi
opencode
dsh
deepagent
```

常用 alias：

```text
claude       -> claude_code
codex_cli    -> codex
openai_codex -> codex
kimi_code    -> kimi
kimi_cli     -> kimi
open_code    -> opencode
deepseek_harness     -> dsh
deepseek_harness_cli -> dsh
deep_agent   -> deepagent
```

所以模板里可以写：

```yaml
runtime: claude_code   # 或 claude
runtime: codex         # 或 codex_cli
runtime: kimi          # 或 kimi_code
runtime: dsh           # 或 deepseek_harness
```

`deepagent` 不启动外部 CLI。它要求设置 `ZEROMDASH_DEEPAGENT_MODEL`，并在当前 Python 进程中调用 `deepagents` 库。

---

### 3.2 Config

`config` 在 YAML 中推荐写短名。

#### Claude Code

```yaml
runtime: claude_code
config: bedrock
```

会在解析后变成：

```text
$HOME/.claude/settings.bedrock.json
```

并传给 Claude Code：

```bash
--settings $HOME/.claude/settings.bedrock.json
```

也就是说，`runtime=claude_code` 时，`config` 是 Claude Code settings 的短名或路径：

```yaml
# 推荐短名
runtime: claude_code
config: bedrock      # -> ~/.claude/settings.bedrock.json

# 也可以显式路径
runtime: claude_code
config: $HOME/.claude/settings.bedrock.json
```

如果 `config` 看起来已经是路径，则保持路径语义，只做 `$HOME` / `~` 展开：

```yaml
config: $HOME/.claude/settings.bedrock.json
config: ~/.claude/settings.bedrock.json
config: /abs/path/settings.bedrock.json
```

#### Codex

```yaml
runtime: codex
config: volc_ark
```

会保持为：

```text
volc_ark
```

并传给 Codex：

```bash
--profile volc_ark
```

也就是说，`runtime=codex` 时，`config` 是 Codex profile 名称，不会被转换成文件路径：

```yaml
runtime: codex
config: ark          # -> codex --profile ark
```

如果 `config` 为空或省略，则不传 `--settings` / `--profile`，由对应 runtime 使用自己的默认配置。

#### Explicit fallbacks

每个 node 可以声明显式 fallback chain。fallback 项支持与 primary 相同的
`runtime` / `config` / `provider` / `model` / `env` 字段：

```yaml
node:
  plan_by_vuln_similar:
    runtime: codex
    fallbacks:
      - runtime: claude_code
        config: ark-proxy
        provider: ark
      - runtime: codex
        config: foundry
        model: gpt-5.5
        provider: foundry
```

fallback 只在当前 runtime 的既有 retry 次数耗尽后触发；不会因为一次失败就立刻切换。
启动 health check 会检查 primary 和所有 fallback，避免主流程失败后才发现备用配置不可用。

#### Kimi Code

```yaml
runtime: kimi
```

Kimi Code 通常从 `~/.kimi-code/config.toml` 读取 provider/model 配置；ZeroMDASH 不会把 `config` 转换成 Kimi 专用 CLI 参数。Kimi 子进程会在 sub workspace 中读取 `.kimi-code/AGENTS.md` 和 `.kimi-code/local.toml`，后者把整个 ZeroMDASH workspace 加入 Kimi 的 additional workspace directories。

---

#### DeepSeek Harness

```yaml
runtime: dsh
provider: deepseek-official
model: deepseek-v4-pro
```

`dsh` 使用 `dsh --profile headless`，默认运行 ZeroMDASH-safe
minimal-plus-search 模式，只向模型暴露受限工具：

```text
bash
str_replace_editor
glob
grep
```

该模式在 bundled `.dsh/headless-minimal.patch.yml` 中实现。它保持
`workspace-write`，加入 bounded `glob`/`grep` 以减少裸 shell 搜索轮次，
关闭交互式 approval、DSH writable filesystem 工具、web、session-title LLM、
DSH 内部 subagent/workflow/Ralph/goal 等嵌套编排能力，并把 session
transcript 重定向到 invocation-local `.dsh/sessions/`。

DSH headless 只接受 argv task，不能把大型 ZeroMDASH prompt 直接放到命令行。
adapter 会把完整 task 写入 `.dsh/prompt.md`，bundled patch 在 DSH 启动时读取
该文件并作为原始 user message 提交。进程物理 cwd 是 task workspace base，
保证 DSH 单根 `workspace-write` sandbox 覆盖完整工作区；模型看到的逻辑 cwd
仍是 invocation sub-workspace。

invocation-local 格式：

```text
sub_workspace/node_<node>[/subtask_<id>]/
  .dsh/
    AGENTS.md                  # 渲染后的 node role / contract / 路径规则
    headless-minimal.patch.yml # bundled minimal composition
    invocation.json           # 物理/逻辑 cwd 与各文件路径
    prompt.md                 # 完整原始任务，避免 argv E2BIG
    settings.yaml             # per-run provider/model/reasoning
    sessions/                 # 该 invocation 的 DSH transcript
  output.schema.json          # 仅结构化输出 node
  skills/
```

`config` 在 DSH runtime 下表示一个额外的、受信任的 `--patch` 路径，应用在
bundled minimal patch 之后。`provider` / `model` 不转换为 `--model`，而是写入
invocation-local `settings.yaml`。

---

### 3.3 Provider

`provider` 表示当前 runtime config 背后的模型/服务提供方。

当前模板只使用这些 provider 标签：

```yaml
provider: bedrock
provider: bailian
provider: ark
```

选择 provider 的原则：**读取你引用的全局配置文件 / profile，看它实际连接哪家 API**。

- `runtime=claude_code` 时，查看 `~/.claude/settings.<config>.json` 或显式 settings 路径。
- `runtime=codex` 时，查看 Codex profile 对应的全局配置。
- 如果 settings/profile 使用 AWS Bedrock，就写 `provider: bedrock`。
- 如果使用阿里百炼，就写 `provider: bailian`。
- 如果使用火山 Ark，就写 `provider: ark`。

当前 provider-specific 环境处理主要实现了 Claude Code + Bedrock；`bailian` / `ark` 目前主要是语义标签，具体 API 行为由所选 settings/profile 决定。

当配置：

```yaml
runtime: claude_code
provider: bedrock
```

会自动设置/清理环境变量：

```text
CLAUDE_CODE_USE_BEDROCK=1
ZEROMDASH_CLAUDE_MODEL=None
ZEROMDASH_CLAUDE_SETTINGS_PATH=<resolved config path>
ANTHROPIC_AUTH_TOKEN=None
ANTHROPIC_BASE_URL=None
ANTHROPIC_MODEL=None
ANTHROPIC_SMALL_FAST_MODEL=None
ANTHROPIC_DEFAULT_HAIKU_MODEL=None
ANTHROPIC_DEFAULT_SONNET_MODEL=None
ANTHROPIC_DEFAULT_OPUS_MODEL=None
CLAUDE_CODE_SUBAGENT_MODEL=None
AWS_BEARER_TOKEN_BEDROCK=<继承父进程中的值，如果存在>
```

如果 `provider` 不是 `bedrock`，Claude Code 会清理：

```text
CLAUDE_CODE_USE_BEDROCK=None
AWS_BEARER_TOKEN_BEDROCK=None
```

以避免 shell 中残留的 Bedrock 环境污染非 Bedrock 调用。

---

### 3.4 Focus

agent-config 支持两层 focus：

1. 顶层 `common_focus`：全局 focus，会注入所有 focus-aware node（含 `investigate_subtask` 与 `critic_subtask`——两者虽 stage-specific focus 通常留空，但会收到 `common_focus` 威胁模型，用于判断攻击者位置 / 信任边界 / 影响）。
2. 每个 node 的 `focus`：stage-specific focus，只注入对应 node。

顶层 `common_focus` 推荐写任务级威胁模型：攻击者位置、入口、信任边界、权限、目标组件、影响类型和版本/分支约束。

```yaml
common_focus: >
  Attacker controls untrusted guest inputs and KVM userspace ioctls, crosses
  the guest/host and EL1/EL2 boundary, and targets VM isolation bugs that may
  cause host memory corruption, information leak, or VM escape.
```

也可以写成 mapping 形式，便于以后扩展：

```yaml
common_focus:
  focus: >
    Attacker controls untrusted guest inputs and targets host isolation.
```

每个 node 可以继续配置局部 focus：

```yaml
node:
  search_spec:
    focus: authoritative upstream specs, RFCs, protocol standards
```

多行也可以：

```yaml
node:
  search_spec:
    focus: >
      authoritative upstream specs, RFCs,
      protocol standards, and security requirements
```

focus 会作为 stage-specific focus 注入 prompt。

当前优先级：

```text
CLI/state 的 common_focus > agent-config 顶层 common_focus > 空
CLI/state 的 <node>_focus > agent-config 中该 node 的 focus > 空
```

CLI focus 参数仍然保留用于兼容老脚本，但已经从 `zeromdash --help` 中隐藏；新用法应把 focus 写进 agent-config。

---

### 3.5 Env

`env` 是可选 mapping：

```yaml
node:
  search_spec:
    env:
      CUSTOM_ENV: hello
      API_BASE_URL: https://example.com
      REMOVE_ME: null
```

含义：

```text
CUSTOM_ENV=hello       # 设置/覆盖
API_BASE_URL=...       # 设置/覆盖
REMOVE_ME=None         # 从 agent 子进程环境中删除
```

`env` 中的字符串值支持 `$HOME` / `$VAR` 展开。

---

## 4. 使用姿势

### 4.1 安装/运行

开发环境常用：

```bash
pip install -e .
```

或使用项目已有 Python 环境直接运行 CLI entrypoint。

---

### 4.2 准备 agent-config

仓库里的 `demo/zeromdash.oss.demo.yaml` 是单仓库 **demo / template**，用于展示一个完整 agent-config 应该覆盖哪些 node、每个字段怎么写，以及哪些 focus 应该由具体任务填充。`demo/zeromdash.oss.multi-repo-demo.yaml` 展示主仓库加插件/功能仓库组成一个目标时的 `target_repos` 写法。它们都不是某个目标的最佳配置，不应该不加修改地用于真实任务。

建议使用方式：

```bash
cp demo/zeromdash.oss.demo.yaml zeromdash.oss.<target>.yaml

# 多仓库目标
cp demo/zeromdash.oss.multi-repo-demo.yaml zeromdash.oss.<target>.yaml
```

然后按目标领域修改：

- `fetch_target_repo.focus`：通常写明确仓库地址、分支、tag 或 mirror，例如 `git://git.kernel.org/pub/scm/virt/kvm/kvm.git`。
- `search_spec.focus`：通常留空，除非有必须命中的规范集合；该阶段需要发散。
- `search_fuzz_driver.focus`：通常留空；内核类目标可提示去 `https://syzkaller.appspot.com/` 查相关 dashboard / program。
- `search_similar_software.focus`：通常留空；该阶段也需要发散。
- `search_similar_history.focus` / `search_target_history.focus`：重点写 threat model，例如攻击者位置、入口、信任边界、权限、影响类型、目标组件、版本/分支约束。
- `search_new_feature.focus`：强调需要补齐的 feature surface 覆盖缺口，例如近期新增 parser、工具模式、外部 backend bridge、状态机或 feature flag。
- `analyze_attack_surface.focus`：强调目标 threat model 下的入口、信任边界、权限边界、共享状态和并发边界。
- `plan_by_*`：通常留空，让 planner 依赖 gather + attack surface 产物。
- `investigate_subtask` / `critic_subtask`：stage-specific `focus` 通常留空，让 subtask objective 和 critic contract 主导；但顶层 `common_focus`（威胁模型）会注入两者。investigate 阶段还会自动收到 attack surface 报告、spec、目标 / 相似软件历史漏洞路径，做 top-down 调查而非纯 code-by-code。
- `plan_chains`：通常留空；它读取完整 primitive pool、Domain Registry 和 deterministic advisory，并通过 harness 原生 subagent 做 forward/backward/seam/constraint 组合。
- `chain_investigate_subtask` / `chain_critic_subtask`：同样通常留空；chain candidate 已携带有序 primitive、bindings 和期望终端影响，chain critic 按契约逐边核查闭环。两者也是 native-subagent-required 节点，runtime 限制与 `investigate_subtask` / `critic_subtask` 相同。
- `summary.focus`：强调最终攻击面模型、confirmed/rejected hypotheses、影响、证据路径和下一步验证策略。

本地私有配置可以命名为：

```text
zeromdash.oss.local.yaml
```

`.gitignore` 默认忽略 `zeromdash.oss.*.yaml`，但保留 `demo/` 下的两个 demo YAML。多仓库目标当前只支持 full scan；在 per-repository diff schema 落地前不能使用 `--scan-mode diff`。

---

### 4.3 Wrapper agent 如何生成 CLI + agent-config

后续如果实现 wrapper agent，它应该输出两类东西：

1. 一个可运行 CLI 命令。
2. 一个 task-specific agent-config YAML。

推荐生成流程：

#### Step 1：识别目标和仓库

从用户输入中抽取：

```text
target_name: kvm-arm64
repo_url: git://git.kernel.org/pub/scm/virt/kvm/kvm.git
branch_or_tag: <optional>
workspace_root: ./.zeromdash
```

写入：

```yaml
node:
  fetch_target_repo:
    focus: git://git.kernel.org/pub/scm/virt/kvm/kvm.git
```

#### Step 2：选择 runtime/config/provider

根据用户环境或全局配置文件选择：

```yaml
node:
  search_spec:
    runtime: claude_code
    config: bedrock
    provider: bedrock
```

或：

```yaml
node:
  plan_by_spec:
    runtime: codex
    config: ark
    provider: ark
```

注意：provider 不是凭空猜测，应读取对应 settings/profile 判断 API 服务商。

#### Step 3：生成 threat model focus

wrapper agent 应该优先问清或推断 threat model，然后填入 history / attack-surface / summary 相关 focus：

```yaml
common_focus: >
  Attacker controls untrusted guest code and KVM userspace ioctls, crosses
  the guest/host and EL1/EL2 boundary, and targets guest-to-host impact,
  host kernel memory corruption, isolation bypass, information leak, and
  incomplete stable backports.

node:
  search_target_history:
    focus: >
      Prioritize KVM/arm64 stage-2 MMU, VGIC, vCPU state, sysreg emulation,
      timer emulation, and pKVM/nVHE shared state security fixes.
```

#### Step 4：不要过度填 focus

发散型和 subtask 驱动型 node 通常留空：

```yaml
node:
  search_spec:
    runtime: claude_code
    config: bedrock
    provider: bedrock
    focus: ""

  plan_by_spec:
    runtime: claude_code
    config: bedrock
    provider: bedrock
    focus: ""
```

#### Step 5：输出 CLI

最终给用户一个命令：

```bash
zeromdash \
  --target kvm-arm64 \
  --workspace-root ./.zeromdash \
  --agent-config zeromdash.oss.kvm-arm64.yaml \
  --max-iterations 1 \
  --min-critic-skills 1
```

如果使用 Claude Code + Bedrock，需要确保：

```bash
export AWS_BEARER_TOKEN_BEDROCK=...
```

---

### 4.4 运行 ZeroMDASH

```bash
zeromdash \
  --target <target-repo-or-software> \
  --workspace-root ./.zeromdash \
  --agent-config zeromdash.oss.local.yaml
```

常用成本控制参数：

```bash
zeromdash \
  --target <target> \
  --agent-config zeromdash.oss.local.yaml \
  --max-iterations 1 \
  --min-critic-skills 1
```

`--disable-spec` 跳过整条 spec 链路（`search_spec` + `plan_by_spec`）；`plan_by_spec` 不跑则 `spec_subtasks` 为空，spec bucket 的 subtask 也不会 dispatch。适合不需要做规范合规检查、只想跑历史漏洞类比 / 补丁遗漏两条链路时砍成本：

```bash
zeromdash \
  --target <target> \
  --agent-config zeromdash.oss.local.yaml \
  --disable-spec
```

---

### 4.5 Health check 和人工介入

启动时 ZeroMDASH 会对每个 node 的 primary runtime/config/provider/env 以及显式
fallbacks 做 health check。

如果某个配置失败，会 pause：

```text
ZeroMDASH paused: health check failed for node 'search_spec'.
Please provide a temporary runtime/config/provider/model for this node.
runtime [claude_code]:
config [bedrock]:
provider [bedrock]:
model []:
```

输入临时配置后，会重新 health check。通过后 workflow 继续。

---

### 4.6 输出位置

默认输出在：

```text
.zeromdash/workspace_for_<target>/
```

关键文件：

```text
summary.en.md
summary.zh_CN.md
summary.md
final_state.json
main/repo/
main/scope/
main/spec/
main/attack_surface/
main/writeup/
main/patch/
gate_result.json
similar/
log/review_log/
log/subtask_res/
log/primitive_res/
log/chain_res/
log/agent_commands.jsonl
sub_workspace/
```

`summary.en.md` 和 `summary.zh_CN.md` 是同一 canonical 漏洞聚合的中英文报告；
`summary.md` 是英文报告的兼容副本。

`final_state.json` 是最终 LangGraph state，包含 task id、workspace、errors、聚合 findings 等机器可读信息；CLI 不再把这份 state 直接 dump 到 stdout。

`log/agent_commands.jsonl` 可用于审计每次 agent 启动命令、cwd、returncode 和 resume id。

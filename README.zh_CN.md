# ZeroMDASH

ZeroMDASH 是 Microsoft MDASH 的开源重实现：一套基于 LangGraph 的多 Agent
漏洞分析流水线，驱动 Claude Code、Codex CLI、TraeX（`traecli` / `traex`）、
Kimi Code、OpenCode、DeepSeek Harness（`dsh`）、DeepAgent 等外部编码 Agent
运行时完成安全审计。

更深入的架构与原理说明见 [ARCH.md](docs/ARCH.md)。

## 快速开始

```bash
pip install -e ".[all]"
zeromdash --target https://github.com/curl/curl
```

分析结果落在 `.zeromdash/workspace_for_<target>/`：

- `main/repo/` — 目标源码树
- `main/scope/` — full/diff 扫描范围，含复制的 diff、变更文件与 hunk
- `main/attack_surface/` — 数据流攻击面报告
- `main/spec/` — 相关 RFC / 标准规范
- `main/feature/` — 新增或弱覆盖的特性面
- `main/writeup/` + `main/patch/` — 历史 CVE 与补丁
- `similar/<sw>/` — 同类软件及其漏洞资料
- `log/review_res/` — 每个子任务的 finding（JSON）
- `log/review_log/plan_by_*.candidates.json` — diff 模式下 planner 的原始候选集
- `log/review_log/plan_by_*.json` — 各 bucket 的可执行计划
- `log/review_log/plan_by_*.convergence.json` — diff 收敛映射
- `log/review_log/dispatch_plan.json` — 实际派发选择与未选原因
- `log/agent_commands.jsonl` — 已启动的 agent 命令与 resume 元数据
- `log/selected_temp_<UTC 时间戳>/` — 选中子任务重跑的隔离输出
- `sub_workspace/` — 各节点 agent 的工作目录，含渲染后的 preset
- `final_state.json` — 机器可读的最终 LangGraph 状态
- `summary.en.md` — 英文安全报告
- `summary.zh_CN.md` — 简体中文安全报告
- `summary.md` — `summary.en.md` 的兼容副本
- `gate_result.json` — 机器可读的 MR 卡点决策

## CLI 参数

```
--target TEXT              目标软件（路径、git URL 或包名）
--scan-mode full|diff|gather
                           全仓扫描、diff 高亮扫描或跨 workspace gather（默认：full）
--gather-workspace-to-chain YAML
                           gather 模式必需的多目标 workspace manifest
--diff-file PATCH          已应用到目标仓库的 unified git diff
--diff-git BEFORE..AFTER   在拉取的远程 git 仓库中基于两个 ref 生成 diff
--workspace-root PATH      输出目录（默认：./.zeromdash）
--task-id TEXT             自定义任务 id
--max-iterations INT       每个子任务的最大 critic 反馈轮数（默认：3）
--min-critic-skills INT    要求 critic 至少应用的专家技能数（默认：2）
--role-lang TEXT           角色卡语言，如 en 或 zh_CN（默认：en）
--agent-config YAML_FILE   配置节点运行时与工作流上限
--preset-attack-surface MD 在分析前预置攻击面报告
--disable-spec             跳过 spec 链路（search_spec + plan_by_spec，无 spec 子任务）
--disable-target-history   跳过目标历史漏洞与补丁遗漏规划
--disable-new-feature      跳过新特性覆盖缺口分析
--till-node analyze|plan   在 analyze_attack_surface 或全部 planner JSON 落盘后停止
--start-from-subtask DIR   恢复已有 workspace，从子任务派发阶段开始
--select-subtask-to-run IDS
                           只重跑选中的 planner 子任务 ID，不生成 summary
--select-subtask-to-run-log-dir DIR
                           选中重跑的隔离输出目录
--start-from-summary DIR   恢复已有 workspace，只运行 summary
--fail-on-gate             diff 模式 finding 触发卡点时以非零码退出
```

示例：

```bash
# 本地源码树
zeromdash --target ./my-project --workspace-root /tmp/audit

# MR/代码 diff 卡点：仓库已打好补丁；diff 只用于高亮与归因
zeromdash \
  --target ./patched-repo \
  --scan-mode diff \
  --diff-file /tmp/change.patch \
  --fail-on-gate

# 远程 git 区间：拉取 ref、检出 AFTER，并高亮 BEFORE..AFTER
zeromdash \
  --target https://example.com/team/repo.git \
  --scan-mode diff \
  --diff-git release-1.0..main \
  --fail-on-gate

# 使用中文角色卡
zeromdash --target curl --role-lang zh_CN

# 跳过 spec 链路（成本控制）
zeromdash --target curl --disable-spec

# 私有软件跳过目标历史漏洞检索
zeromdash --target ./private-project --disable-target-history

# 在攻击面分析后停止
zeromdash --target curl --till-node analyze

# 在 planner JSON 落盘后停止
zeromdash --target curl --till-node plan

# 恢复一个已有 planner JSON 的 workspace
zeromdash --start-from-subtask .zeromdash/workspace_for_curl

# 只重跑选中子任务；canonical 结果保持不变
zeromdash \
  --start-from-subtask .zeromdash/workspace_for_curl \
  --select-subtask-to-run vuln-013,patch-008,spec012

# 使用显式隔离输出目录
zeromdash \
  --start-from-subtask .zeromdash/workspace_for_curl \
  --select-subtask-to-run vuln-013 \
  --select-subtask-to-run-log-dir selected_runs/vuln-013-review

# 从 log/review_res/*.json 重新生成中英文报告
zeromdash --start-from-summary .zeromdash/workspace_for_curl

# 把已完成的源 workspace 串成跨目标攻击链
zeromdash \
  --scan-mode gather \
  --gather-workspace-to-chain demo/gather-multi-target-config.example.yaml \
  --agent-config demo/gather-agent-config.example.yaml
```

当 `--target` 是本地目录时，ZeroMDASH 会在分析前把完整源码树确定性地复制到
`main/repo/`。原目录不会被修改，本地 `.git` / `.zeromdash` 元数据不会被复制。

## Gather 模式

`gather` 是独立的第二级 graph，把多个已经跑完的单目标 workspace 串成跨目标攻击
链。它不 fetch、也不重新扫描目标源码，而是：

- 把每个源 workspace 的 attack surface、primitive、subtask 与本地 chain 产物复制
  到 `inputs/<target-id>/` 下，形成不可变证据快照；
- 给所有 source id 按 target 加命名空间，避免跨 workspace 的 ID 碰撞；
- 合成 scenario 级的 cross-target registry，再由 Agent 原生 planner 规划，只对
  跨越至少两个 target 的候选跑 investigate/critic battle；
- 源 workspace 里已确认的 finding 只作为证据引用，不会在 gather 报告里被重复
  报成新漏洞。

gather graph：

```text
gather_analyze_attack_surface
  -> gather_plan_chains
  -> dispatch_gather_chains
  -> N x gather_chain_subtask（investigate -> critic -> finalize）
  -> gather_prepare_report_groups
  -> summary
  -> polish_report
```

完整架构与证据契约见 [docs/GATHER_CHAIN.md](docs/GATHER_CHAIN.md)。

### 前置条件

manifest 里每个 target 必须指向一次已完成的扫描：

- `workspace.json` 存在；
- `main/attack_surface/` 下至少有一个非空文件；
- `log/primitive_res/`、`log/subtask_res/`、`log/review_res/`、`log/chain_res/`
  中至少有一个非空 `*.json`（chain evidence）；
- `agent_config` 指向的文件存在且 YAML 可解析。

`targets` 至少两项，`name` 不能重复，slugify 之后也不能碰撞。

### manifest

```yaml
schema_version: "1.0"
name: example-service-stack        # 可选；默认取文件名，用于 workspace 名和报告标题
scenario: >                        # 必填；描述这些 target 如何共同工作，而非通用审计方法论
  External tenants submit deployment requests to api-gateway ...

# 可选；CLI 未传 --agent-config 时的 fallback，配置 gather 节点本身
gather_agent_config: ./gather-agent-config.example.yaml

targets:
  - name: public-api               # 必填；slug 后唯一
    agent_config: ./zeromdash.oss.demo.yaml   # 必填；源扫描使用的配置
    workspace: ./.zeromdash/workspace_for_public-api  # 必填；已完成的源 workspace
    role: tenant authentication and job normalization  # 可选；该 target 在场景中的职责
```

可直接运行的示例是 `demo/gather-multi-target-config.example.yaml`，对应的 gather
节点配置是 `demo/gather-agent-config.example.yaml`。manifest 内的所有相对路径都
相对于 manifest 所在目录解析，与当前 shell 目录无关，因此从仓库根目录执行时给
manifest 加 `demo/` 前缀即可，示例内部的引用不需要改。

`gather_agent_config` / `--agent-config` 配置本次 gather graph 的 runtime、model、
focus、并发和 chain budget：

```yaml
top_K:
  chain: 16

gather:
  max_pair_passes: 12              # 定向 target 对深挖的最大次数
  max_chain_length: 6              # 单条链允许的最大 evidence unit 数
  max_candidates_before_top_k: 200 # top_K.chain 之前的原始候选上限
  max_battle_rounds: 3             # 每条链的 investigate/critic 最大轮数
  require_cross_target: true       # gather 模式下不能设为 false
```

manifest 中每个 target 的 `agent_config` 只提供 `common_focus`、仓库描述和与证据
解释相关的 focus；其 runtime、model、provider、env、fallback 不会被继承，其中的
secret 也不会写入快照、prompt 或 `final_state.json`。gather 模式的 agent-config
不允许定义 `target_repos`。

### 参数校验

| 条件 | 行为 |
| --- | --- |
| `--scan-mode gather` 但缺少 `--gather-workspace-to-chain` | 启动前失败 |
| 非 gather 模式却提供 `--gather-workspace-to-chain` | 启动前失败 |
| gather 与 `--target`、`--diff-file`、`--diff-git` 同用 | 启动前失败 |
| gather 与 `--preset-attack-surface`、`--till-node` 同用 | 启动前失败 |
| gather 与 `--start-from-*` 恢复模式同用 | 启动前失败 |
| gather 与 `--disable-spec` / `--disable-target-history` / `--disable-new-feature` / `--disable-chain` 同用 | 启动前失败；这些 track 已在源 workspace 完成 |
| manifest `schema_version` 不是 `1.0`、`scenario` 为空、`targets` 少于两项 | 启动前失败 |
| target `name` 重复或 slugify 后碰撞 | 启动前失败 |
| workspace 不存在、缺 `workspace.json`、无 attack surface 或无 chain evidence | 启动前失败并列出 target |
| `agent_config` / `gather_agent_config` 不存在或 YAML 无法解析 | 启动前失败 |

`--fail-on-gate` 在 gather 模式下同样生效，读取 gather workspace 的
`gate_result.json`。

### gather workspace 布局

gather 模式写入独立的 `.zeromdash/workspace_for_gather-<scenario-name>/`，不使用
`main/repo/` 作为输入源：

```text
workspace_for_gather-<scenario-name>/
├── workspace.json
├── gather_manifest.yaml
├── inputs/
│   ├── manifest.normalized.json
│   ├── gather_inputs.lock.json
│   └── <target-id>/
│       ├── workspace.json       # 清洗后的源 workspace 元数据
│       ├── source_context.json  # 清洗后的 focus / 仓库上下文，不含 env secret
│       ├── attack_surface/      # 源 main/attack_surface 快照
│       ├── source/
│       │   ├── main/            # 源 main/repo 快照
│       │   └── <repo-id>/       # 源 main/repos/<repo-id> 快照
│       ├── primitive_res/       # active primitive envelope
│       ├── subtask_res/         # active terminal subtask envelope
│       └── chain_res/           # active 的本地已确认链
├── main/attack_surface/
│   ├── gather_attack_surface.md
│   └── cross_target_registry.json
├── log/
│   ├── state/
│   │   ├── gather_evidence_pool.json
│   │   └── gather_chain_plan.json
│   ├── review_log/              # gather 节点与 battle 的尝试日志
│   ├── gather_chain_res/        # 已确认的跨目标链 finding
│   ├── gather_chain_candidates/ # 被否决或结论不足的跨目标链
│   ├── gather_report_groups.json
│   └── agent_commands.jsonl
├── sub_workspace/               # gather 节点与逐链 agent 工作目录
├── summary.en.md
├── summary.zh_CN.md
├── summary.md
├── gate_result.json
└── final_state.json
```

基础 `Workspace` 类还会在 gather workspace 中创建 `main/repo/`、`similar/`、
`log/subtask_res/`、`log/chain_res/` 等兼容目录，通常为空；canonical 的 gather
输入在 `inputs/` 下，跨目标结果在 `gather_*` 路径下。

当前 V1 没有 gather 专用的恢复模式，未提供 `--start-from-gather-chain`；需要重跑
时请重建 manifest 或从源 workspace 重新生成。规划中的恢复能力见
[docs/GATHER_CHAIN.md](docs/GATHER_CHAIN.md)。

## Agent 配置

`--agent-config` 是设置工作流上限、任务聚焦点和各节点运行时配置的首选方式：

单仓库目标使用 `demo/zeromdash.oss.demo.yaml`。当一个目标产品由核心仓库加插件或
功能仓库组成时，使用 `demo/zeromdash.oss.multi-repo-demo.yaml`。多仓库目标当前
仅支持 full 扫描模式。

```yaml
common_focus: >
  威胁模型、攻击者位置、信任边界、目标组件、影响类别，
  以及项目级约束。

max_concurrency: 8  # 默认值；限制同时执行的 LangGraph Send/节点数量
top_K:
  spec: 5
  vuln: 8
  patch: 3
  feature: 4

node:
  search_spec:
    runtime: claude_code
    config: bedrock
    provider: bedrock
    focus: "相关协议与解析器规范。"

  investigate_subtask:
    runtime: traex
    config: work
    fallbacks:
      - runtime: claude_code
        config: ark-proxy
        provider: ark

  critic_subtask:
    runtime: codex
```

`top_K` 是派发子任务的显式成本上限。不配置则不截断；配置后会降低覆盖率，
diff 模式不会隐式启用它。`max_concurrency` 只限制已派发 LangGraph 任务的
并发数。

`investigate_subtask`、`critic_subtask` 和 `summary` 必须使用经过验证、
具备原生子 Agent 能力的 harness。可接受的运行时为 `codex`（含 `codex_cli`
别名）、`traex` 与 `claude_code`；该限制同时覆盖主运行时和每一个 fallback。
ZeroMDASH 会在这三个节点生成的本地配置中启用 Codex `multi_agent`、TraeX
`multi_agent_v2`，以及 Claude Code 的 `Agent` 工具。其余节点可以使用任意
已注册运行时。这里的「subtask」指 ZeroMDASH 的 LangGraph 工作单元；
「subagent」指上述 harness 内部原生创建的子代理。

TraeX 以 `runtime: traex` 支持（别名：`trae`、`trae_cli`、`traecli`、
`trae_code`、`traecode`）。ZeroMDASH 以非交互模式运行 `traecli exec`，
通过 stdin 传入 prompt，用 `--output-last-message` 捕获最终响应，并对
对象形结构化输出契约使用原生 `--output-schema`。TraeX 0.201.1 不支持顶层
数组 schema，因此 planner 的 `Subtask[]` 输出仍为纯 JSON，由 ZeroMDASH 编排
器现有的 validator 校验。TraeX 从节点子工作区读取渲染后的 `AGENTS.md`，
子工作区即其工作根；`--add-dir` 授予对整个任务工作区的写权限，使最终产物
可以写入 `main/`、`similar/` 与 `log/`。adapter 设置
`project_root_markers=[]`，让 TraeX 只加载调用本地的 `AGENTS.md`，而不继承
上层任务目录的指令。

`config` 通过 TraeX `--profile` 选择 `~/.trae/<config>.traecli.toml`；
省略时使用基础 `~/.trae/traecli.toml`。ZeroMDASH 显式使用 TraeX 的
`workspace-write`、非交互 exec 默认审批策略和临时会话；不启用 exec 模式下
无法请求审批的 Auto-Review，也不使用危险的全权限 bypass。

```yaml
node:
  investigate_subtask:
    runtime: traex
    config: work
    model: seed-2.1-pro
```

Kimi Code 也可作为节点运行时。在 `~/.kimi-code/config.toml` 中配置好官方
Kimi provider 后，无需再设置 `provider` 或 `config`。Kimi prompt 模式下，
ZeroMDASH 会把项目级指令渲染到 `.kimi-code/AGENTS.md`，并在每个
`sub_workspace` 生成 `.kimi-code/local.toml`，其中
`[workspace].additional_dir` 指向整个 ZeroMDASH 工作区。

由于 Kimi adapter 目前没有经验证的原生子 Agent 契约，Kimi 不能分配给
`investigate_subtask`、`critic_subtask` 或 `summary`，但仍可用于 fetch、
search、分析与 planner 节点。

DeepSeek Harness 通过 `dsh --profile headless` 支持。ZeroMDASH 不把完整任务
放进 argv，而是把 prompt 和运行时元数据写入调用本地的 `.dsh/` 目录，从任务
工作区根启动 DSH，使 `workspace-write` 覆盖 `main/`、`log/` 与
`sub_workspace/`，同时把逻辑当前目录保持在调用子工作区。

默认 DSH 模式是受限的 minimal-plus-search 叶子 Agent：保留持久的 `bash` 和
`str_replace_editor`，增加有界的 `glob`/`grep` 仓库检索，并禁用交互审批、
shell/编辑器之外的可写文件系统工具、Web 访问、嵌套 DSH 子
Agent/workflow/Ralph、自动会话标题 LLM 请求和全局会话持久化。节点的
`config` 值会被当作一个额外的、受信任的 DSH `--patch` 文件，在内置 minimal
patch 之后应用。

由于内置 headless DSH overlay 禁用了其子 Agent 工具，DSH 同样不能分配给
`investigate_subtask`、`critic_subtask` 或 `summary`，但可与其他节点配合
使用，支持 `provider`、`model` 和可选的受信任 `config` patch。

每次 DSH 调用会物化：

```text
sub_workspace/node_<node>[/subtask_<id>]/
  .dsh/
    AGENTS.md
    headless-minimal.patch.yml
    invocation.json
    prompt.md
    settings.yaml
    sessions/
  output.schema.json        # 仅结构化输出节点
  skills/
```

## 运行时选择

主 `zeromdash` 工作流使用显式运行时选择。启动时，ZeroMDASH 会对每个启用
节点配置的运行时及显式 `fallbacks` 做健康检查。如果某个
runtime/config/env 组合不健康，CLI 会暂停并询问临时的
runtime/config/provider/model 覆盖项。运行时，节点只在当前运行时已耗尽该
节点的既有重试次数且仍失败时才切换到 fallback。

| 节点类型 | 默认运行时 |
|---|---|
| Fetch / search / summary | `claude_code` |
| 攻击面分析 | `codex` |
| 规划 / 调查 / critic | `codex` |

支持的运行时名称：

| 运行时 | 别名 | `config` 含义 |
|---|---|---|
| `claude_code` | `claude` | 短名展开为 `~/.claude/settings.<name>.json`；路径则直接使用。 |
| `codex` | `codex_cli`、`openai_codex` | 作为 `codex --profile <config>` 传入。 |
| `traex` | `trae`、`trae_cli`、`traecli`、`trae_code`、`traecode` | 作为 `traecli exec --profile <config>` 传入；profile 文件为 `~/.trae/<config>.traecli.toml`。 |
| `kimi` | `kimi_code`、`kimi_cli` | 通常省略；Kimi 读取 `~/.kimi-code/config.toml`。 |
| `opencode` | `open_code` | 无运行时特定的 `config` 映射。 |
| `dsh` | `deepseek_harness`、`deepseek_harness_cli` | 可选的受信任额外 `--patch` 路径；内置 minimal patch 始终先应用。 |
| `deepagent` | `deep_agent` | Python 库运行时；需设置 `ZEROMDASH_DEEPAGENT_MODEL`。 |

`model` 非空时，对除 DSH 外的 CLI 运行时会作为 `--model <model>` 传入。
TraeX 还接受 `ZEROMDASH_TRAEX_BIN`（默认解析顺序：`traecli`，然后
`traex`）和 `ZEROMDASH_TRAEX_MODEL`。DSH 的 provider/model 选择会写入调用
本地的 `settings.yaml`，因为 headless profile 不支持 `--model`。
目前 provider 特定的环境处理包括 `claude_code` + `provider: bedrock`，以及
DSH 的调用本地 provider/model 设置。

## 工作流程

主工作流：

```text
fetch_target_repo
  -> prepare_scan_scope
  -> search_spec
  -> search_fuzz_driver
  -> search_similar_software -> N x search_similar_history
  -> search_target_history
  -> search_new_feature
  -> analyze_attack_surface
  -> plan_by_spec / plan_by_vuln_similar / plan_by_vuln_patch / plan_by_new_feature
  -> N x 子任务循环：
       investigate_subtask -> critic_subtask -> revise/finalize
  -> summary
```

`full` 是默认模式，保持全仓扫描。`diff` 模式下，完整的补丁后仓库仍可用于
调用图、类型、配置和同路径分析；diff 只控制归因、优先级，以及 finding 能否
卡点本次变更。

diff 模式没有隐式的任务数量上限。`analyze_attack_surface` 先创建规范的
`## Diff Risk Surface Registry`：每个 `RS-XXX` 表示一个变更代码锚点、根因、
不可信输入到 sink 的数据流及其安全不变量。四个 planner 把
spec/CVE/patch/feature 证据挂载到这些风险面上，而不是为每条证据各建一个任务。

每个 planner 会产出：`plan_by_*.candidates.json`（原始候选审计轨迹）、
`plan_by_*.json`（同 bucket `risk_surface_id` 收敛后的 diff 可归因计划）、
`plan_by_*.convergence.json`（映射与未选原因）。`dispatch_plan.json` 再记录
跨 bucket 收敛与实际派发。没有具体 diff-to-sink 路径的相邻或既有检查只保留
在候选轨迹中。full 模式保持既有的全仓规划与派发行为。diff 模式的 Send 按
spec / vuln / patch / feature 桶做 round-robin 排序，避免单个大 planner
结果占满全部并发槽位。

`--diff-file` 与 `--diff-git` 互斥。`--diff-git` 用于远程 git 目标：fetch
阶段保留 `.git`，scope 阶段解析或拉取两个 ref，检出 `after` 提交，并生成
两点 `before..after` diff。tag、branch 和 commit SHA 均可接受。

`--disable-spec` 移除 `search_spec` 与 `plan_by_spec`。
`--disable-target-history` 移除 `search_target_history` 与
`plan_by_vuln_patch`。
`--disable-new-feature` 移除 `search_new_feature` 与
`plan_by_new_feature`。

`search_target_history` 同时写出 `main/writeup/_index.md` 和规范的
`main/patch/_patch_commits.json`。该 JSON 对单仓库与多仓库目标统一使用
patch-manifest schema v1.0：`repositories[]` 记录已检出的仓库身份，
`coverage[]` 为每个仓库给出恰好一条结果（含 `no_public_history`），扁平的
`findings[]` 记录带有显式 `repo_id` 和补丁可达性证据。编排器会拒绝缺失仓库、
缺失 coverage、未知 repo id 和特定目标的顶层布局，然后才允许
`plan_by_vuln_patch` 运行。旧 workspace 保留原有产物；重跑
`search_target_history` 即可生成 v1 manifest。

`--till-node analyze` 在 `main/attack_surface/attack_surface.md` 创建且非空
后停止。`--till-node plan` 在所有启用的 planner 于 `log/review_log/` 下生成
合法 plan JSON 后停止。

`--start-from-subtask <workspace>` 复用已有 workspace，从子任务派发阶段
开始。workspace 必须已包含源码树、`main/attack_surface/attack_surface.md`，
以及 planner 文件 `log/review_log/plan_by_spec.json`、`plan_by_vuln.json` 和
`plan_by_patch.json`。`plan_by_feature.json` 存在时才加载；没有 feature 链路
的旧 workspace 仍可恢复。

使用 `--select-subtask-to-run` 时，ZeroMDASH 会按 planner 文件校验并规范化
请求的 ID，然后只重跑选中的子任务图。紧凑 ID（如 `spec012`）会规范化为
`spec-012`。canonical 的 `log/review_res/*.json`、`log/review_log/*.log`、
`log/agent_commands.jsonl`、summary 和 `final_state.json` 保持不变。选中重跑
在状态收集后即停止，绝不运行 summary。

默认情况下，选中重跑的输出写入新的 `log/selected_temp_<UTC 时间戳>/` 目录。
显式 `--select-subtask-to-run-log-dir <DIR>` 可覆盖它；相对路径在恢复的
workspace 下解析，且目录必须不存在。隔离目录包含 `attempts/`、
`investigations/`、`critic_reviews/`、`results/`、`agent_commands.jsonl`、
`selected_subtask_statuses.json` 和自己的 `final_state.json`。结果 JSON 同时
保留最终 `finding` 和完整的逐轮 `history`。

旧的 `--start-from-subagent`、`--select-subagent-to-run` 和
`--select-subagent-to-run-log-dir` 写法仍作为废弃兼容别名被接受。在当前
术语中，`subagent` 只指具备能力的 harness 内部创建的原生子代理。

`--start-from-summary <workspace>` 复用已有 workspace，只运行 `summary`
节点。workspace 必须包含 `workspace.json`、非空 `main/repo/`、非空
`main/attack_surface/attack_surface.md` 和 `log/review_res/*.json`。它会重新
加载 `review_res` 中序列化的 finding 并按 `kind` 分组；这是报告重生成路径，
不是新一轮 critic。summary 的准入仍是确定性的：没有通过漏洞资格门且缺少合法
CVSS v4.0 Base 向量的历史 finding，会保留为非漏洞观察项，而不会提升为
`VULN-XXX`。

格式错误或不全的调查输出会重试，且不消耗 investigate/critic 轮次。每次尝试
前，ZeroMDASH 会从该次调用的子工作区删除陈旧的 `finding.json`、
`investigation.json` 和 `output.json`。stdout 优先；只有当 stdout 不合法时，
才可能接受本次尝试新生成的 JSON artifact，且必须通过同样的非空
title/detail、`evidence.code_locations` 和 `evidence.call_path` 契约。无效调查
永远不会到达 critic，也不会成为持久化 finding。尝试日志会记录输出来源，并
区分 stdout / artifact 校验失败。

对 DSH 调查，子进程超时仍可恢复该次调用新建的非空 `finding.json`。adapter
只接受新的、可解析为 JSON object 的 artifact 候选；常规调查 validator 仍会
在接受前强制完整 schema。缺失、陈旧、空、损坏或不满足契约的文件不会掩盖
超时。

diff 模式运行中，`main/scope/` 包含 `scope.json`、`changes.diff`、
`changed_files.txt`、`changed_symbols.json` 和 `change_summary.md`。
`gate_result.json` 把 finding 分为 blocking、warning 或 ignored。只有代码
计算的 CVSS v4.0 严重性为 high/critical、归因为 `introduced`、`enabled` 或
`regressed`、且有具体 diff-to-sink 因果路径的合格漏洞才会卡点变更。critic
必须先把每个结果分类为：已确认/配置型漏洞、已知 CVE 补丁缺口、加固建议、
预期行为、证据不足或 no-finding；只有两种漏洞判定会获得 CVSS 评分。
既有与无关 finding 不卡点。

## 可观测性（可选）

```bash
pip install -e ".[observability]"
export LANGFUSE_PUBLIC_KEY=pk-...
export LANGFUSE_SECRET_KEY=sk-...
```

所有 LangGraph 节点调用都会追踪到 Langfuse。

## 复现工作流

`zeromdash-repro` 是一个独立辅助工具，用于验证已在 `log/review_res/` 下产出
的 finding：

```bash
zeromdash-repro \
  --review-res .zeromdash/workspace_for_curl/log/review_res \
  --repo-path .zeromdash/workspace_for_curl/main/repo \
  --target curl
```

它运行线性流程：

```text
load_review_results -> plan_repro -> build_harmless_poc -> validate_repro -> summary
```

与主工作流不同，`zeromdash-repro` 在启动健康检查时仍使用后端 fallback 链。

## 环境要求

- Python ≥ 3.10
- 默认工作流同时使用 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 和 [Codex CLI](https://github.com/openai/codex)：fetch/search/summary 默认用 `claude_code`，攻击面分析、规划、调查与 critic 默认用 `codex`。
- [Kimi Code](https://moonshotai.github.io/kimi-code/)、
  [OpenCode](https://github.com/opencode-ai/opencode)、
  [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) 和
  `deepagent` 是可选运行时，仅当 `--agent-config` 把启用的节点映射到它们时
  才需要安装/配置。

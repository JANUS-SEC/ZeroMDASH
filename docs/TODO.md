# TODO

## P0（已完成）：单 workspace 跨原语攻击链分析

- [x] 将漏洞分析拆成两级 subtask graph：
  1. 初步 subtask：`investigate_subtask <-> critic_subtask`；
  2. 聚合 subtask：`chain_investigate_subtask <-> chain_critic_subtask`；
  3. `prepare_report_groups` 统一归组 standalone findings 和 chain findings，最终 `summary` 消费归组结果及其来源证据。
- [x] 扩展初步 subtask 的终态分类和持久化格式：
  - `standalone_finding`：当前根因自身已经违反安全契约并产生直接 C/I/A 影响，按现有资格硬门槛计算 CVSS v4.0；
  - `confirmed_primitive`：代码机制、可达性和获得的攻击能力已经被 critic 确认，但自身不能闭合为漏洞；不单独计算 CVSS，也不能因为 `standalone_security_impact=false` 或仍需其他原语而丢弃；
  - 每个 primitive 至少记录稳定 id、所属 repo/component、前置条件、攻击者控制对象、获得的 capability、影响的地址空间/状态、可靠性、证据位置、来源 subtask 和仍缺少的下一跳能力。
- [x] 建立统一的 chain 输入池：standalone findings 和 confirmed primitives 都进入聚合阶段；standalone finding 除了保留独立报告资格，也作为可供后续链条消费的已证实 capability。
- [x] 根据 `prerequisite -> capability gained` 的兼容关系生成有界 chain subtasks，避免对所有输入做无约束笛卡尔积；至少支持跨 repo、跨 component 和跨 trust boundary 的组合。
- [x] 实现 `chain_investigate_subtask <-> chain_critic_subtask` battle：
  - `chain_investigate_subtask` 必须给出完整攻击者入口、按顺序排列的 primitive、每一步 capability 转换、跨组件交接对象和最终安全影响；
  - `chain_critic_subtask` 必须逐边核查前置条件是否由上一跳满足、版本/配置是否能同时成立、对象和地址空间是否一致，以及是否仍依赖未证实的外部原语；
  - 两个节点都必须使用支持原生子 agent 的 harness，并保留逐轮证据和反证记录。
- [x] 只有端到端闭环、所有必要 primitive 均已确认且产生最终直接 C/I/A 影响的组合才能产出 `chain_finding`，并基于完整攻击链计算 CVSS v4.0；未闭环组合保留为 confirmed primitives / chain candidates，不伪装成漏洞。
- [x] 为 chain 阶段增加结构化产物和恢复能力，例如 `log/primitive_res/*.json`、`log/state/chain_plan.json`、`log/chain_res/*.json`，以及匹配的 resume/selected-run 入口。
- [x] 增加组合成本控制：`top_K.chain`、最大 chain 长度、每个 capability 的最大候选后继数和 chain battle 最大轮数，并在裁剪时保存原因。
- [x] `prepare_report_groups` 收集 `standalone_findings + chain_findings`，先做确定性归组，再由 `report_group_adjudicator` 处理语义重复；`summary` 继续遵守现有双语报告、代码证据、逐漏洞数据流图/攻击时序图、版本边界和 CVSS v4.0 格式，避免同一 standalone finding 既单独报告又作为 chain 组成部分重复计数。
- [x] 按 [`CHAIN.md`](./CHAIN.md) 将 chain composition 调整为 Agent-Native 语义裁决：
  - `plan_chains` 设为 native-subagent-required，由 forward/backward/seam/constraint 子 agent 汇总候选；
  - deterministic prefilter、compatibility mismatch 和 pruning 只作为 agent 输入与成本控制，不再拥有最终语义否决权；
  - `chain_investigate_subtask` / `chain_critic_subtask` 输出逐边 binding verdict、registry refs、反证和 emergent transition verdict；
  - critic 使用 `closure_verdict + fact_verdicts` 对每个必要事实做显式裁决，legacy unmet facts 必须先归类，不能静默视为已解决；
  - deterministic closure 负责 ID/schema/evidence/CVSS 和硬安全条件；仅当失败属于 contract 表达差异时，才交给 native `chain_finalizer_subtask` 复核，不能覆盖未确认原语、无效 binding 或互斥全局约束。
- [x] `analyze_attack_surface` 生成 Domain Model and Invariant Registry 双产物（Markdown + JSON），并以稳定 entity / representation / invariant / transition / seam ID 贯穿 planner hints、initial primitive 与 chain binding；Protected Resource and Mapping Registry 仅作为领域自适应派生视图，不硬编码 QEMU/SMRAM 术语。
- [x] 支持 emergent terminal impact：允许所有单个 primitive 的 `terminal_impact` 为空，只要 chain investigator 提出组合状态转换、chain critic 逐边确认且完整链产生直接 C/I/A 影响，即可生成 chain finding 和 CVSS v4.0。
- [x] 将 chain finalization 和 report dedup 的语义边界补齐：
  - `chain_finalizer_subtask` 只裁决 deterministic validator 无法表达的语义等价，不允许绕过 confirmed primitive、binding、constraint 和 external primitive 硬门槛；
  - `report_group_adjudicator` 只能合并已有 report groups，不能创建 finding、改变 qualification 结论或合并 patch-gap 特例；
  - 两个节点均使用结构化 contract、artifact-first validation、native-subagent runtime gate 和可配置 focus。

## P0：Gather mode 跨 workspace 攻击链聚合

完整设计见 [`GATHER_CHAIN.md`](./GATHER_CHAIN.md)。该模式消费多个已经完成的
ZeroMDASH workspace，在共同业务场景下验证跨 target 数据流和攻击能力传递；它与
下文的 Multi-Repo Hybrid Analysis 不同：前者是扫描后的联邦聚合，后者是在一次扫描
内对多个源码仓库执行 repo-local 与 integration analysis。

- [x] 增加 `--scan-mode gather` 和 `--gather-workspace-to-chain <multi-target-config.yaml>`：
  - manifest 包含非空 `scenario`，以及至少两个 target 的 `name`、`agent_config` 和 `workspace`；
  - 相对路径统一按 manifest 所在目录解析；
  - gather 与 `--target`、diff 参数、单 workspace restore 参数和各 discovery disable 参数做 fail-fast 互斥校验；
  - backend health check 只检查 gather graph 实际会运行的节点。
- [x] 建立独立 `GatherState`、`build_gather_graph()`、`run_gather()` 和 gather output workspace，不让单目标 `ZeroMDASHState` 同时承担两套语义，也不修改任何源 workspace。
- [x] 实现输入 preflight、snapshot 和 `gather_inputs.lock.json`：
  - 校验 `workspace.json`、attack-surface 内容和可用 chain evidence；
  - 沿用 active `subtask_res`、package primitive 去陈旧和 confirmed `chain_res` 规则；
  - 对输入 artifact 记录 SHA-256，对源码记录 revision/dirty-status fingerprint；
  - target agent config 只提取 sanitized threat context，不继承 runtime/env，不把 secret 写入 prompt 或 final state。
- [x] 将各 workspace 的 `log/primitive_res`、`log/subtask_res` 和 `log/chain_res` 归一化为 `GatherEvidenceUnit`：
  - 支持 `primitive | standalone_finding | local_chain`；
  - ID 使用 `<target_id>::<local_id>` namespace，多仓源进一步包含 `repo_id`；
  - 每个事实携带 target/workspace/artifact/hash/JSON pointer/revision/code location `SourceRef`；
  - observation、rejected、inconclusive 和 qualification 未通过的结果只能作为 context，不能成为 provider。
- [x] 扩展 agent invocation 的 `additional_read_roots`，并在 V1 将源码复制到 gather workspace 内的隔离 snapshot，避免只支持 writable `--add-dir` 的 runtime 修改源 workspace。
- [x] 实现 native-subagent-required 的 `gather_analyze_attack_surface`：统一分析各 workspace 的 `main/attack_surface/`，按 scenario 生成 `gather_attack_surface.md` 和 `cross_target_registry.json`，显式建模 target roles、interfaces、data flows、identity mappings、trust transitions、deployment assumptions 和 unresolved gaps。
- [x] 实现 native-subagent-required 的 `gather_plan_chains`：
  - 使用 forward/backward/seam/constraint/adversarial passes 聚合跨 target 候选；
  - deterministic compatibility 只提供 advisory，不以字符串完全匹配提前裁掉 near-match 或 emergent impact；
  - 只分发至少包含两个 target 和一条跨 target binding 的候选；
  - `local_chain` 与其 constituent primitives 不得在同一候选中重复计入。
- [x] 实现 `dispatch_gather_chains` 和隔离的 `gather_chain_subtask` nested graph：
  - `gather_chain_investigate_subtask <-> gather_chain_critic_subtask -> gather_finalize_chain_subtask`；
  - 每条跨 target edge 都要核对 producer、实际传输/共享介质和 consumer 三侧证据；
  - critic 对 source unit、local/cross-target binding、scenario assumption、terminal impact 和反证逐 fact 裁决；
  - bounded rounds 结束后仍有必要事实为 unknown 时不得确认。
- [x] 实现 gather qualification 和持久化硬门槛：至少两个 target、confirmed cross-target edge、完整 source refs、同时可满足的版本/配置/身份/部署/时序条件、无外部未确认 primitive、直接 C/I/A impact 且 `source_drift=false`；成功和失败分别写入 `gather_chain_res` / `gather_chain_candidates`。
- [x] 实现 `gather_prepare_report_groups -> summary -> polish_report`：
  - 只报告新的跨 target chain，不重复编号源 workspace 的 standalone finding；
  - 保留共同场景、target topology、跨目标 binding、双侧代码证据、来源 workspace、约束、数据流图、攻击时序图和 CVSS v4.0；
  - 无闭合链、部分 agent 失败和证据不足时仍生成机器可读状态及完整 no-finding/limitation 报告。
- [x] 增加 gather contracts、双语 role cards、runtime defaults、native-subagent gate、CLI/normalization/graph/qualification/report 测试，并更新 README 与 [`ARCH.md`](./ARCH.md)。
- [ ] 在现有 Markdown/Mermaid 静态诊断之外增加真实 Mermaid renderer 验证。
- [ ] V1 稳定后增加 `--start-from-gather-chain <gather-workspace>`；恢复前校验 manifest/input-lock hash，避免复用已经漂移的源证据。

## P0：Multi-Repo Hybrid Analysis 与 Chain Context 完整性

- [ ] 将分析布局与 Chain 开关解耦：
  - single-repo 仍允许启用 intra-repo Chain；
  - multi-repo + Chain disabled 保持当前 aggregate 流程；
  - multi-repo + Chain enabled 自动使用 hybrid layout；
  - 预留显式 `analysis.layout=aggregate|hybrid|auto` 与 `chain.scope=intra_repo|cross_repo|both`。
- [ ] 顶层 `fetch_target_repo` 只执行一次，materialize 全部 `main/repos/<repo_id>`、聚合视图和包含 revision/role/required 状态的 repo manifest；不要在每个 repo lane 重复 clone。
- [ ] 新增可复用的 `build_repo_analysis_graph()` 和 `Send("repo_analysis", child_state)`：
  - 每个 child 的 `repo_path` 只指向本仓 canonical checkout；
  - 按 `repo search_* -> search_new_feature -> analyze_attack_surface -> plan_by_* -> investigate/critic` 顺序运行；
  - local subtask、primitive 和 Registry ID 使用 `<repo_id>::<local_id>` namespace；
  - 输出 `repo_analysis_package.json` 和 `coverage_ledger.json`。
- [ ] 拆分 shared discovery 与 repo-local evidence routing：
  - `search_target_history` / `search_fuzz_driver` / `search_new_feature` 按 repo 执行；
  - `search_similar_software` target-global 执行一次；
  - similar history 和 global specs 保留 provenance，并按 repo/component/interface 相关性路由；
  - 共享 cache 只去重搜索，不替代 local source grounding。
- [ ] 增加 integration lane：
  - 汇总 repo packages、namespaced Registries、构建/运行关系和 integration-facing coverage gaps；
  - 生成 `main/integration/attack_surface.md`、integration Registry、interface catalog 和 deployment manifest；
  - 运行 integration planners 与普通 `investigate_subtask <-> critic_subtask`；
  - 跨仓 object identity/equivalence 必须以带双方源码证据的 hypothesis 验证，禁止按名称自动合并。
- [ ] 扩展 `materialize_chain_pool`，统一聚合 repo-local 与 integration 的 standalone capability providers / confirmed primitives，并保留 repo、lane、revision、Registry 和 evidence provenance。
- [ ] 在 chain battle 前增加 per-candidate `prepare_chain_context`：只装配相关 primitive 完整记录、Registry 邻域、attack-surface 摘要、repository-qualified evidence、deployment constraints、advisory 和 counterevidence；context pack 不限制 Agent 按需读取完整 workspace。
- [ ] 增加 Agent-Native Chain gap feedback loop：
  - `collect_chain_gaps -> chain_gap_planner -> repo-local/integration initial subtasks -> investigate/critic -> update pool -> plan_chains`；
  - Chain Agent 不得直接创建 confirmed primitive；
  - gap 使用稳定 ID 并按 capability/Registry/repo/evidence 去重；
  - 默认最多 1–2 轮，只有新增 confirmed primitive 时才重跑 Chain；
  - 重复 gap、无新增 primitive、缺失源码或预算耗尽时终止并持久化 lineage。
- [ ] 增加 `audit_context_coverage` barrier：
  - 检查每个 required repo 是否完成有效 lane；
  - high-risk invariant/seam/transition 是否 covered 或存在明确裁剪原因；
  - integration-facing 条目是否进入 integration lane；
  - `uncovered` / 不完整 Code Graph coverage 必须保留为 unknown，不能作为安全反证。
- [ ] 将 multi-repo fan-out 预算调整为“每仓保底 + integration cap + 全局竞争”，避免大仓库耗尽全部 `top_K`；记录每个 repo 的 candidate、selected、omitted 数量和裁剪原因。
- [ ] 扩展 multi-repo failure/restore/reporting 语义：
  - repo/integration package 使用 `complete|partial|failed`；
  - required repo 失败不得静默生成“完整扫描”结论；
  - restore 和 selected-run 支持 `<repo_id>::<subtask_id>` / `integration::<subtask_id>`；
  - summary 汇总 local standalone、integration standalone、closed chains 和 coverage limitations，并保持全局去重。
- [ ] 增加 hybrid graph 验收测试：single-repo Chain、multi-repo aggregate、multi-repo hybrid、integration-only primitive、per-repo budget floor、gap round convergence、partial lane、repo-qualified restore 和 candidate context pack。

## P1：Planner evidence-density 硬门槛

- [ ] 为不同 planner lane 增加结构化证据下限，避免任务数扩张时每项 hints 被模型压缩：
  - `spec`：`spec_refs >= 1`，`candidate_code_locations >= 3`；
  - `vuln`：`cve_refs >= 1`，并至少覆盖 entry、state/sanitizer、sink 三类位置；
  - `patch`：`patch_refs >= 1`，至少包含 patch point 和一个 sibling/bypass candidate；若确实不存在 sibling，必须写明原因。
- [ ] 对 objective 明确列出多个 backend/component 的聚合任务，校验 `candidate_code_locations` 是否覆盖每个 backend/component。
- [ ] planner validator 输出每个 bucket 的 evidence-density 统计；未满足对应 lane contract 时仅重试 planner，不把证据补全推迟到 investigator。

## Token 成本优化

历史大规模运行中观察到过单次 workflow 约 200M tokens 的消耗，但这个数字依赖目标、模型、agent-config、并发和统计口径。后续成本数据应记录目标、模型、配置、日期、是否计入 cache-read tokens，以及每节点聚合明细。

### P0：先做成本止血

- [ ] 增加 `--max-similar-software`，限制 `search_similar_software -> search_similar_history` 的 fan-out 数量。
- [ ] 增加 `--max-total-subtasks`，限制 `plan_by_* -> subtask` 的总 fan-out 数量。
- [x] 支持 per-bucket subtask fan-out 限制：agent-config 顶层 `top_K.spec` / `top_K.vuln` / `top_K.patch` / `top_K.feature` 已分别限制各 bucket 最终 dispatch 的数量。
- [ ] 如仍需要 CLI 直传，再增加 `--max-subtasks-per-bucket` 作为 `top_K` 的命令行别名。
- [x] 支持 top-K dispatch：当前 dispatch 前会按 `common_focus`、attack-surface 文本重合和 candidate location reachability 重新排序后截断。
- [ ] 如需要完全尊重 planner 输出的显式 numeric `priority` / `score`，补充 schema、prompt 和排序实现。
- [ ] 为 quick mode 默认设置：`max_iterations=1`、`min_critic_skills=1`、限制 similar/subtask 数量。
- [x] 新增 DeepSeek Harness (`dsh`) runtime，默认使用 invocation-local
  minimal-plus-search 模式，并禁用 DSH 内部嵌套 agent/workflow、web、
  writable filesystem tools 与额外 title LLM。

### P1：构建历史漏洞知识库

- [ ] 增加本地 KB 根目录配置，例如 `$HOME/.zeromdash/kb`。
- [ ] 新增 `zeromdash/kb.py`，提供基础接口：
  - [ ] `lookup_software(target)`
  - [ ] `lookup_vulns(software, limit=...)`
  - [ ] `save_vuln_records(records)`
  - [ ] `render_history_markdown(records)`
- [ ] 设计 KB 目录结构：
  - [ ] `software/`：软件实体、别名、相似软件关系
  - [ ] `vulns/`：CVE/GHSA/issue 结构化记录
  - [ ] `sources/writeups/`：原始 writeup/advisory
  - [ ] `sources/patches/`：patch/commit 原文或链接
  - [ ] `indexes/`：别名索引、software->vuln 索引、tag 索引
- [ ] 为漏洞记录定义结构化字段：
  - [ ] software / aliases / ecosystem
  - [ ] vuln id / source urls
  - [ ] affected component / affected versions
  - [ ] root cause / bug class / trigger condition
  - [ ] attack surface / exploit path
  - [ ] fix pattern / patch urls / writeup urls
  - [ ] evidence / confidence / fetched\_at / last\_verified\_at
- [ ] 在 `search_similar_software` 前做 KB-first lookup，命中足够则跳过 agent search。
- [ ] 在 `search_target_history` 前做 KB-first lookup，命中足够则写入 workspace 产物并跳过 agent search。
- [ ] 在 `search_similar_history` 前做 KB-first lookup，命中足够则写入 workspace 产物并跳过 agent search。
- [ ] KB 未命中或质量不足时才调用 agent，并将 agent 搜索结果结构化写回 KB。
- [ ] 增加 `--kb-disable` / `--kb-refresh` / `--kb-root`。

### P2：workspace 缓存与断点复用

- [ ] 对单 workspace 的 discovery/search 阶段增加缓存：`search_spec`、`search_fuzz_driver`、`search_similar_software`、`search_target_history`、`search_new_feature`。这里不是新的 `scan_mode=gather`。
- [ ] 缓存 key 包含：target、node、focus、agent config hash、prompt version。
- [x] 支持从既有 workspace 的 planner 输出恢复到 subtask 阶段：`--start-from-subtask <workspace>`。
- [x] 支持从既有 workspace 的 `log/subtask_res/*.json` 重新生成 summary：`--start-from-summary <workspace>`。
- [x] 支持从既有 workspace 定向重跑指定 subtask，并将 attempt、command、investigation、critic、result 和 final state 写入独立目录，不覆盖 canonical 产物。
- [x] 支持 `--start-from-chain <workspace>` 从已有 primitive/result artifacts 重建 chain pool 并恢复到 chain planning；支持 `--select-chain-to-run` 将指定 chain 的 attempt/result/final state 写入隔离目录。
- [x] 支持 `--start-from-polish-report <workspace>` 仅重跑最终报告格式修复，不要求重新加载 subtask 或 chain 执行状态。
- [x] 支持 investigation fresh artifact fallback：每次 attempt 先删除旧 artifact，stdout 优先，只接受本轮新生成且通过同一结构化契约的 JSON。
- [x] DSH subprocess timeout 时回收本轮 fresh、非空 `finding.json` 候选，并继续走同一结构化 validator；陈旧或无效 artifact 不掩盖 timeout。
- [ ] 支持通用 `--reuse-workspace` 或 `--resume-task-id`，复用任意 discovery / analyze / plan 中间产物。
- [ ] 对 planner 输出和 subtask finding 做通用结构化缓存，带 cache key 和失效策略；当前仅有恢复路径，不是缓存系统。

### P3：token 预算与观测

- [ ] 扩展 `log/agent_commands.jsonl`，记录每次 agent invocation 的 usage/token/cost metadata。当前单个 `sub_workspace/agent_invocation.json` 会保存完整 `metadata`，但 workflow 级 JSONL 仍只记录命令、cwd、returncode、ok、resume_id。
- [ ] 增加 workflow 级 budget 配置：
  - [ ] `max_total_tokens`
  - [ ] `max_node_tokens`
  - [ ] `max_subtask_tokens`
- [ ] 超预算时 pause，等待人工选择继续/跳过/更换 runtime/config/provider。
- [ ] 输出按 node 聚合的 token/cost summary。

### P4：prompt/context 压缩

- [ ] `investigate_subtask` 反馈循环只传最小必要 critic feedback，而不是完整 review JSON。
- [x] `critic_subtask` 的 skills catalog 只注入 skill name + 一句话 summary。
- [ ] 支持先让 critic 选择 skill，再按需读取对应 `SKILL.md`。
- [ ] 将历史 writeup/patch 原文预处理成 compact index，planner 默认只读 index。
- [ ] 对 planner 输入增加长度限制和 top-K evidence selection。

## Agent config / runtime 配置

- [x] 支持 YAML per-node agent config 的核心字段：`runtime` / `config` / `provider` / `model` / `env` / `focus`，以及顶层 `common_focus`、`top_K`、`max_concurrency`。
- [x] 明确缺失字段的当前行为：缺失 `runtime` 使用节点默认 runtime；缺失或空 `config` 不传 `--settings` / `--profile`；缺失 `provider` 只使用 runtime 默认环境处理。
- [x] Claude Code + Bedrock 缺少 `AWS_BEARER_TOKEN_BEDROCK` 时在启动健康检查阶段 fail-fast，并允许临时改选 runtime/config/provider/model 后重新检查。
- [ ] 补齐其他“半配置”的静态 warning 或 fail-fast，例如 settings/profile 路径不存在，或显式 `model` 与 runtime env 默认值冲突。
- [ ] 支持在 health check pause 时输入临时 env override。
- [ ] 将人工临时配置写入 workspace metadata，便于复现。

## 推荐优先级

1. P0 Gather mode hardening：增加真实 Mermaid renderer 验证和 `--start-from-gather-chain`，再用真实多服务 workspace 做一次端到端验收。
2. P0 Multi-Repo Hybrid Analysis：落 repo-local lanes、integration lane、全局 primitive pool 和 coverage barrier；与 gather 共享 provenance/schema 基础设施，不共享 state 语义。
3. P0 Chain context 完整性：candidate context pack 与 bounded chain-gap feedback loop。
4. P0 剩余 fan-out 控制：`--max-similar-software`、`--max-total-subtasks`、quick mode，并与每仓保底预算统一设计。
5. P1 Planner evidence-density 硬门槛，复用到 repo-local 和 integration planners。
6. P1 历史漏洞 KB MVP。
7. P2 通用 workspace 缓存 / reuse（区别于已完成的 subtask/summary/chain 恢复）。
8. P3 token budget 与观测。
9. P4 prompt/context 压缩。

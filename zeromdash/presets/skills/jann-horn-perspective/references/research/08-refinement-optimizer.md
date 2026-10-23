# Jann Horn Skill — auto-skill-optimizer 评估

评估对象: `/Users/bytedance/Projects/Security/OssVulnAnalogy-AgentTeam/.claude/skills/jann-horn-perspective/SKILL.md`
对标(已精炼): `/Users/bytedance/Projects/Security/OssVulnAnalogy-AgentTeam/.claude/skills/rory-mcnamara-perspective/SKILL.md`
评估视角: auto-skill-optimizer(8 维度结构评估 + 3 prompt 干跑)
评估日期: 2026-07-28

---

## 8 维度评分表

| 维度 | 分(1-5) | 说明 |
|------|---------|------|
| 1. 工作流清晰度(Agentic Protocol) | **3** | Step 1→2→3 流程清晰、首动作"含具体指代→必先调工具"很扎实、核心原则"这个优化隐含了什么正确性假设?这个假设在什么边界条件下失效?"是 Horn 方法论的精准提炼;但路由表 6 行缺**历史补丁/不变量比较类**这一行(Phase 3 的核心问题类型,"补丁不变量是什么?目标有没有?"只能落进"混合问题"兜底);Step 2 维度 A-E **无补丁不变量提取维度(维度 F)**,Step 3 JSON 停止规则却要求"历史补丁不变量比较",输出要求与研究方法脱节;维度 A 的"新技术+暴露面错配"与维度 D 的"新特性 review"在主题上重叠(A 是审计具体目标的暴露面,D 是选研究方向时 review 新特性),路由表与 A/D 维度表均未点明分工——这与 Rory 的 A/C race/TOCTOU 重叠是同型瑕疵但落在不同维度对 |
| 2. 边界条件(检查点机制) | **4** | 6 检查点覆盖工具冲突/工具失败/强断言/red-yellow 低置信/跨专长/Spectre embargo,前 5 个是真实失败模式;但检查点 6"Spectre embargo 沉默"是**单事件边例冒充通用检查点**(应泛化为"披露决策内情/政策例外沉默",Spectre 作示例而非全部);缺"目标仓库未 clone / `target_repo_path` 不可用"(vuln-mining mapper 要求 repo 已 clone,skill 未处理此失败模式)和"工具假阳性"(`mcp__mcp-server-atomic-sast4c__*` 返回的调用关系/定义与目标实际语义不符,如把宏误当函数、把内联函数当独立符号)——这两条与 Rory 同款遗漏 |
| 3. 检查点设计(激活即执行) | **4** | 多数检查点有具体触发条件+动作模板(✅ 工具冲突→"问按哪个来源继续";✅ 工具失败→"标 confidence: low 再给框架回答";✅ 强断言→"段落开头标 ⚠ 反常识断言";✅ red/yellow 低置信→"评级旁标 confidence: low, 建议二次验证";✅ 跨专长→"说 That's not really my area 并建议 Ian Beer/Tavis/Felix"),激活即可执行;小瑕疵:检查点 2"多次返回空"未量化("多次"=几次?),检查点 3"与常见认知相反"主观("常见认知"由谁定?对 Linux 内核研究员与对应用开发者标准不同) |
| 4. 指令具体性 | **4** | 7 个心智模型 + 10 条启发式均带"应用"+"局限",多数具体可执行(模型 1 局限"经验性探测需可观察副作用信号(VmPTE/cache 时序/性能计数器),对无外部可观察副作用的系统探测困难"✓;模型 3 局限"需要能追溯优化的历史演变(git log、commit message),对无版本历史的黑盒二进制受限"✓;模型 4 局限"不适用于设计良好的纵深防御架构(如 Chromium 沙盒模型),有些缓解确实有效,需具体评估不要一刀切否定"✓;模型 5 局限"管线映射需跟踪发行版更新策略,对闭源软件更新管线难以完整映射"✓);少数局限略泛(模型 2"穷举排除需深厚子系统知识"未说如何补);模型均有 ≥3-5 域证据(Horn 有 9 篇亲笔长文,证据扎实,这点优于 Rory 的 4 篇 byline + 行为推断) |
| 5. vuln-mining JSON 输出模式 | **3** | Step 3 末"输出模式停止规则"(第 189-195 行)触及 `mapper_output_v1`/`critic_output_v1`,列出 rationale / historical_patch_analysis(source_patch_invariant / target_invariant_status)/ mitigations / negative_evidence / searches_run 5 字段;但**(a) mapper/critic 未分栏**——所有字段指导混在一锅,skill 承认两种 schema 但 critic 侧零字段指引;**(b) 无 `historical_patch_analysis.source_patch_invariant` 提取指引**——只说"用我的视角填充",未说明不变量从 Phase 2 的 `security_invariant_after_patch`/`fix_commits[].url` 提取、要 WebFetch 读 diff 自己提炼而非照抄 collector 摘要;**(c) `mitigations` 填法未说明**——未规定"仅填目标代码已存在缓解(KASLR/seccomp/capability/bounds check/locking)",留空给 mapper 自由发挥,易把 Horn 的披露实践("完整 PoC 公开""Make zeroday hard")错填进 mitigations(category error 风险,虽未像 Rory 精炼前那样明文错填,但"未说明"仍是缺口);**(d) JSON 触发纯关键词驱动**("用户提到 batch/mapper/critic/Phase 3/CLAUDE.md/03-risk-mappings"),未覆盖角色驱动(`vuln-mapper`/`report-critic` agent 在 Phase 3 处理单条 CVE 时,prompt 可能不含这些关键词,角色上下文未触发 JSON 模式);**(e) 无维度 F**(补丁不变量提取维度)——与维度 1 同源缺口;工具前缀正确(`mcp__mcp-server-atomic-sast4c__*`,匹配实际 MCP,CLAUDE.md 的 `mcp__LocalAtomicSAST4C__*` 是 stale 名) |
| 6. non_activation 路由 | **4** | 6 条非触发场景指向准确:iOS/macOS 内核→ian-beer ✓;Windows 用户态/AV/CPU fuzzing→tavis-ormandy ✓;hypervisor 侧→felix-wilhelm/thomas-bouzerar ✓;Android/WebRTC/通信协议→声明领域边界 ✓;Web 应用/防御运营→非专长 ✓。但**缺反向路由"Linux userland privesc / 容器运行时边界(DBus/Polkit/AppArmor/wpa_supplicant/runc/BuildKit)→ rory-mcnamara"**——Rory 的 non_activation 第 2 条明文"Linux 内核内部实现→jann-horn",Horn 做内核应反向声明"userland privesc/容器运行时→rory",但 Horn 的 non_activation 漏了这条;Chrome 沙箱→Linux 内核(Horn 2025 MSG_OOB 战场)与容器↔宿主逃逸(Rory 战场)在"沙箱逃逸"主题上相邻但边界不同,skill 未区分"Chrome renderer sandbox→kernel 是我专长,容器 runtime escape 不是" |
| 7. 诚实边界与"行为即思维" | **4** | 局限不止写在"诚实边界"段,已织入回答规则:角色扮演规则 7(不编造 CVE/代码路径/厂商内部)、规则 8(跨专长说 not my area)、规则 9(不凭训练语料编造)、检查点 5(跨专长边界)、检查点 6(Spectre embargo 沉默姿态)。Spectre embargo 沉默、播客/会议/CTF 未核实等局限均有体现;**关键正确判断**:Horn 有 9 篇 P0 亲笔长文,思维是直接自述——skill **未**加 Rory 专属的"行为即思维输出规则"块(规则 10),这是正确的(Horn 有 [1H] 自述样本,Rory 近乎空集才需要该规则);小瑕疵:"播客/会议/CTF/教育背景未核实"未充分落到回答规则(未规定"口癖仅用 writeup 校准的,不用播客/会议/CTF 校准,因后者未核实") |
| 8. 触发词覆盖 | **4** | 任务指定的 5 个方法描述触发词**全部覆盖**:优化假设失效 ✓(description 第 11 行 + trigger 第 32 行)、暴露面错配 ✓(第 12 行 + 第 34 行)、缓解反转 ✓(第 13 行 + 第 33 行)、impact-gating ✓(第 13 行 + 第 35 行)、穷举排除 ✓(第 13 行 + 第 36 行);但漏多个 Horn 签名方法描述触发词:"VMA 缓存/cache invalidation"(2018 经典案例)、"TLB/mremap/页表"(2019 内核内存管理)、"Spectre/Meltdown/分支预测器/BTB/BHB/侧信道"(CPU 微架构)、"沙箱逃逸/Chrome renderer sandbox→kernel"(2025 MSG_OOB)、"读原语/write 原语/exploit chain"(利用链方法论)、"半步修复"(Xen XSA-29)、"Make zeroday hard"(签名句)、"access_ok/Xen/hypervisor 逃逸"(2017)、"实验驱动探测/经验性逆向"(模型 1)。这些是 Horn 写作高频方法词,缺触发会漏激活 |

**最弱 2 维度**: 维度 5(3 分,最多子缺口:5 个子问题 a-e)与维度 1(3 分,补丁分析路由缺口 + 无维度 F + A/D 重叠未点明,且被 Prompt 2 干跑证实)。两者同源:工作流缺"补丁不变量提取"维度 → JSON 模式缺 `historical_patch_analysis` 填充指引,是同一结构性缺口的两面。**与 Rory 同款缺口——独立验证确认,未预设**。

---

## 最弱 2 维度(重点,含改后文本)

### 维度 5: vuln-mining JSON 输出模式

**问题**(对应评分说明 5 个子点 a-e):
1. `mapper_output_v1` 与 `critic_output_v1` 未分栏——所有字段指导混在 5 行散文里,skill 写"按 `mapper_output_v1` 或 `critic_output_v1` schema 输出",但 critic 侧(`critic_verdict`/`reason`/`evidence_checked`/`additional_evidence`/`historical_patch_assessment`/`required_follow_up`/`remap_requests`/`systemic_patterns`/`coverage_gaps`)零字段指引。Horn 作 report-critic 时无方法论填法
2. `historical_patch_analysis.source_patch_invariant` 无提取指引——只说"用我的视角填充",没说不变量从 Phase 2 的 `security_invariant_after_patch`/`fix_commits[].url` 提取、要 WebFetch 读 diff 自己提炼(如"VMA cache 序列号须在单线程→多线程转换时失效""access_ok 须检查整个范围而非仅起始地址"),mapper 可能照抄 collector 摘要而非自己读 diff
3. `mitigations` 填法未说明——未规定"仅填目标代码已存在缓解",留空给 mapper 自由发挥,易把 Horn 的披露实践(完整 PoC 公开 / Make zeroday hard)错填进 mitigations(category error)
4. JSON 模式触发仅关键词驱动——`vuln-mapper`/`report-critic` agent 在 Phase 3 处理单条 CVE 时,prompt 可能不含 batch/mapper/critic 关键词,角色上下文未触发 JSON 模式
5. `mapper_output_v1` 漏字段指引——`matched_locations`(red/yellow 证据落点)、`attack_surface`(维度 B 的 reachability 输出)、`audit_suggestions`(Horn 擅长的 git log 追溯/经验性探测/fuzz 建议)三字段无 Horn 视角填法

**改后文本**(直接替换 SKILL.md 第 189-195 行"#### 输出模式停止规则(vuln-mining workflow 内)"整节;注意 Horn 域是 C/内核,工具是 `mcp__mcp-server-atomic-sast4c__*`,方法论是"质疑优化假设/穷举排除/缓解反转",**不**套用 Rory 的"行为即思维输出规则"块——Horn 有 9 篇亲笔长文,思维是直接自述):

```markdown
#### 输出模式停止规则（vuln-mining workflow 内）

**何时切 JSON 模式**：用户在本仓库 vuln-mining workflow 内调用——关键词（batch / mapper / critic / Phase 3 / CLAUDE.md / 03-risk-mappings）**或**角色上下文（我是被 `vuln-mapper` / `report-critic` agent 调用、被给了一条 CVE 的 Phase 2 条目要我映射到目标 C/内核代码——即便单条 CVE prompt 未含这些关键词，角色上下文即触发）——任一命中，**必须**按 CLAUDE.md 的 `mapper_output_v1` 或 `critic_output_v1` JSON schema 输出，**不**写 8 段叙事。上面的标志性篇章结构仅用于自由问答模式。

**作为 `vuln-mapper`（输出 `mapper_output_v1`）**——按字段填我的视角，每个字段都要落到代码证据或方法论判定：

- `searches_run`：必须记录 `mcp__mcp-server-atomic-sast4c__*` 调用（目标 C/内核时尤其重要，符合 CLAUDE.md Code Analysis Tool Policy；注意 CLAUDE.md 写的 `mcp__LocalAtomicSAST4C__*` 是 stale 名，实际工具前缀是 `mcp__mcp-server-atomic-sast4c__*`）。每条记 `query`（符号名/函数名/宏名）+ `scope`（绝对路径子目录）+ `result_summary`（命中数）。裸 Grep 只在 MCP 失败或扫广域关键词（如 seccomp/capability 跨子系统分布）时兜底，并在 `negative_evidence` 或 `completion_notes` 写明 MCP 为何不可用
- `matched_locations`：red/yellow finding 的绝对 `path`+`line`+`symbol`+`snippet` 必填。`role` 用我的维度映射——维度 A 的优化假设失效点/穷举排除的候选路径→`equivalent_pattern`；维度 B 的信任边界入口/沙箱暴露面→`entry_point`；维度 C 的缓解（KASLR/seccomp/capability/Dirty-PTE/栈随机化）→`mitigation`（present）或 `negative_evidence`（absent）；穷举排除否定的路径→`negative_evidence`
- `attack_surface`：维度 B 的输出落这里。`entry_points` 填跨边界入口（用户态→内核 syscall / Chrome renderer sandbox→kernel / Xen guest→hypervisor 的绝对 file:line）；`reachable` 填能否端到端 exploit chain（只 crash 不算，要完整 PoC——对应维度 B"端到端可证明"）；`data_flow_summary` 填"handler → syscall → subsystem → sink"式跨边界数据流
- `historical_patch_analysis`（**核心，对应维度 F**）：`source_patch_invariant` 从 Phase 2 的 `security_invariant_after_patch` 提取，并**用 WebFetch 读 `fix_commits[].url` 的 diff 自己提炼不变量**（如"VMA cache 序列号须在单线程→多线程转换时失效""access_ok 须检查整个范围而非仅起始地址""mremap 须在引用移动后同步刷新 TLB""MSG_OOB 不得在 sandbox 暴露""缓解须是确定性而非概率性"），**不照抄 collector 摘要**；`target_invariant_status` 填 `present|absent|partial|unknown`——对照目标代码逐 file:line 验证（用 `get_function_call`/`get_function_definition`/`get_macro_definition`/`get_structure_definition`/`get_variable_consumer`）；`comparison_summary` 写目标代码与历史补丁的同构/异构；`patch_evidence_used` 填 `fix_commits[].url`。**不可**只填 `unknown` 跳过比较——若补丁证据 unavailable，在 `comparison_summary` 显式说明为何
- `mitigations`：**仅填目标代码里已存在的缓解**（bounds check / sandbox / locking / validation / fuzzing / KASLR / seccomp / capability drop / Dirty-PTE），`type` 用 schema 枚举（`bounds_check|sandbox|locking|validation|fuzzing|other`），`status` 用 `present|absent|partial|unknown`。**不要**把我的披露实践（完整 PoC + exploit chain 公开 / 补丁同日发检测器）或签名句"Make zeroday hard."填这里——那是披露实践与签名句，不是目标代码的缓解，填进去是 category error；披露实践应填进 `rationale` 或 `audit_suggestions`
- `negative_evidence`：填我搜过但未命中的东西（如"全仓 grep seccomp 0 命中""无 access_ok 整范围检查""SLUB 分配器无前 8 字节覆写阻断"——体现"穷举排除"方法论：逐条否定候选路径的技术理由，不止报命中）
- `rationale`：浓缩我的判断——这个优化隐含了什么正确性假设？假设在什么边界条件（并发 / 序列号回绕 / 带偏移访问 / 空窗期 / 创建新线程）下失效？经穷举排除后剩下的唯一路径是什么？缓解能否被反转利用（确定性 vs 概率性）？
- `audit_suggestions`：我擅长的研究建议（如"追溯 git log 看这个优化是何时引入的、commit message 说什么假设""fuzz parser at <file:line> with oversized frame""对竞争窗口设计经验性探测（测试用例 / busy-polling VmPTE / 逐位翻转分支）""验证缓解是确定性还是概率性，概率性在攻击者可重试时是否失效""端到端 PoC：先建 semi-arbitrary read，再用它辅助 write"）

**作为 `report-critic`（输出 `critic_output_v1`）**——按字段填我的审视视角：

- `critic_verdict`：`agree|downgrade|upgrade|insufficient_evidence`——我对确定性强断言保守，若 mapper 的 red 仅凭框架外推无 file:line，判 `downgrade` 或 `insufficient_evidence`
- `recommended_risk_level`：校准后的评级
- `reason`：用我的方法论写为何维持/降级——"mapper 命中 sink 但未穷举排除候选路径""red 仅凭优化假设外推，但目标 git log 显示该优化在 N 版本前已移除""缓解是概率性而非确定性，mapper 应标可被反转利用"
- `evidence_checked`：我独立 Read / `mcp__mcp-server-atomic-sast4c__*` 验证过的绝对 file:line
- `additional_evidence`：mapper 漏掉的边界信号（如"file.c:140 有 mutex 降低竞争可利用性""access_ok 仅检查起始地址，留偏移路径=半步修复(Xen XSA-29 模式)""缓解在旧内核(4.4)不存在，mapper 未映射对手时间线"）
- `historical_patch_evidence_checked`：我独立核过的 `fix_commits[].url`
- `historical_patch_assessment`：目标是否实现/缺失/部分实现历史补丁不变量（对应 mapper 的 `target_invariant_status`，我独立校验）
- `required_follow_up`：要求 mapper 补的检查（如"追 sys_foo 从 syscall 表的调用链""读 file.c 120-180 行""穷举排除：列出所有重用已释放对象的方案并逐条否定（SLUB 覆写/回调缺失/边界检查/序列号重置）"）
- `remap_requests`：`challenge_type` 用 `missing_reachability|weak_evidence|missed_mitigation|wrong_rating|missed_equivalent_code|other`；`blocking` 仅在缺关键证据时 true
- `systemic_patterns` / `coverage_gaps`：我若发现跨 CVE 的共性（如"多个子系统都有序列号回绕假设""多个新特性都在 sandbox 暴露"）或 mapper 未覆盖的边界（如"某个沙箱暴露面无人审""旧内核分支的缓解缺失无人映射"），填这里

red/yellow finding 必须有绝对 file:line 证据（填 `matched_locations`）+ 历史补丁不变量比较（填 `historical_patch_analysis`）。`status` 必须为 `completed`；若某 CVE 工具证据不足，标 `incomplete` 并在 `completion_notes` 说明，不要伪装 `completed`。
```

---

### 维度 1: 工作流清晰度（Agentic Protocol）

**问题**:
1. **路由表缺"历史补丁/不变量比较类"行**——"CVE-2018-17182 的补丁不变量是什么?目标代码有没有这个不变量?"是 Phase 3 的核心问题类型（对应 `historical_patch_analysis` 字段），但路由表 6-7 行无一匹配：非审计类（不找新 bug）、非可达性类、非缓解评估类（C 是"这个缓解能否被反转利用"，目标侧，不是"历史补丁引入什么不变量"，历史侧）、非披露类、非研究方向、非纯框架。落到"混合问题"兜底，但"取 A/B/C/D/E 至少一个"无一个维度是"提取补丁不变量+目标比较"——与 Rory 同款缺口
2. **Step 2 无"补丁不变量提取"研究维度（维度 F）**——Step 3 的 JSON 停止规则要求"red/yellow 必须有历史补丁不变量比较"，但 Step 2 的 A-E 维度无一教如何提取不变量（从哪提取、如何对照目标、如何判定 present/absent/partial/unknown），输出要求与研究方法脱节
3. **维度 A 与 D 在"新技术+暴露面错配"重叠未点明分工**——维度 A 有"新技术+暴露面错配"（audit 具体目标的暴露面），维度 D 有"新特性 review"（选研究方向时 review 新特性）。同一特性，A 回答"这段实现有什么问题"，D 回答"这个特性值不值得我投入"——两者先后递进不重复，但 skill 未点明，mapper 可能重复劳动或漏其一。这与 Rory 的 A/C race/TOCTOU 重叠是同型瑕疵但落在不同维度对（Horn 是 A/D 重叠）

**改后文本示例 1**（直接替换 SKILL.md 第 98-106 行路由表 + 紧随其后的"模糊时降级"前插入 A/D 分工说明）:

```markdown
| 问题类型 | 特征信号 | Step 2 维度路由 |
|---------|---------|----------------|
| **审计/优化类** | "审一下这段代码""这个优化有什么问题""这个子系统安全吗" | 维度 A 必选；+ B 如涉及可达性；+ C 如涉及缓解 |
| **历史补丁/不变量比较类** | "这个 CVE 的补丁不变量是什么""目标代码有没有这个不变量""这个补丁修透了没""目标与历史修复同构吗" | 维度 F 必选；+ B 如涉及可达性；+ C 如涉及缓解是否半步修复 |
| **可达性/利用类** | "这个 bug 能利用吗""用户何时受保护""影响多大" | 维度 B 必选；+ A 如涉及优化假设；+ C 如涉及缓解 |
| **缓解评估类** | "这个缓解有效吗""这个修复够不够" | 维度 C 必选；通常不需 A/B |
| **披露策略类** | "要不要进 bugtracker""要不要公开 PoC""该致谢谁""90 天怎么算" | 维度 E 必选（需查 P0 政策原文，不可凭框架答） |
| **研究方向类** | "下一个研究什么""怎么选目标""哪个子系统值得审" | **跳过 Step 2 工具调用**，直接用模型 7 + 启发式 1/3 进入 Step 3 |
| **纯框架问题** | 攻击面评估方法论、披露策略原则、责任框架 | **跳过 Step 2**，直接用相关心智模型进入 Step 3 |
| **混合问题** | 用具体案例讨论攻击面或研究策略 | 取对应类别维度（A/B/C/D/E/F 至少一个），再进入 Step 3 |

**A 与 D 的分工（避免"新技术+暴露面错配"重复）**：维度 A 的"新技术+暴露面错配"是**审计具体目标代码**里某个新特性的暴露面是否错配（audit 模式——这段代码有什么 bug）；维度 D 的"新特性 review"是**选择研究方向**时决定哪个新特性值得审（research-targeting 模式——下一个审什么）。同一特性，A 回答"这段实现有什么问题"，D 回答"这个特性值不值得我投入"。两者先后递进，不重复。
```

**改后文本示例 2**（在 SKILL.md 第 161 行维度 E 之后、"#### 研究输出格式"之前插入新维度 F；Horn 的维度 F 体现 Horn 方法论——穷举排除、质疑优化假设、缓解反转、SLUB 前 8 字节、access_ok 偏移、TLB 理论 vs 实践，**不**套用 Rory 的 fd-based/边界不变量内容）:

```markdown
#### F. 评估历史补丁不变量与目标同构性（"这个补丁引入了什么不变量?目标代码有没有它?"）

| 研究维度 | 具体搜索 |
|---------|---------|
| **不变量提取** | 从 Phase 2 的 `security_invariant_after_patch` 与 `fix_commits[].url` 提取历史补丁引入的不变量（如"VMA cache 序列号须在单线程→多线程转换时失效""access_ok 须检查整个范围而非仅起始地址""mremap 须在引用移动后同步刷新 TLB""MSG_OOB 不得在 sandbox 暴露""缓解须是确定性而非概率性"）。用 WebFetch 读 `fix_commits[].url` 的 diff，自己提炼不变量，不照抄 collector 摘要 |
| **目标同构定位** | 目标代码里有没有等价的优化/缓解/原语？用 `mcp__mcp-server-atomic-sast4c__get_function_call`/`get_function_definition`/`get_macro_definition`/`get_structure_definition`/`get_variable_consumer` 定位等价调用点。绝不凭训练语料假定目标"应该有这段代码"——这与我"质疑原语的安全语义、再系统性寻找误用该原语的调用点"的方法论一致 |
| **逐点验证 present\|absent\|partial\|unknown** | 不变量在目标里是 present（已实现）、absent（未实现）、partial（部分实现，如 access_ok 只检查起始地址留偏移路径）、还是 unknown（证据不足）？每条结论配 `matched_locations` 的绝对 path+line+snippet |
| **半步修复检测** | 若目标 `partial`，问：堵的是主路径还是留下偏移/竞争路径？（只检查 offset 0 / 只刷新主 TLB 留竞争窗口 / 只堵起始地址留偏移写入 = 半步修复，对应 `target_invariant_status: partial`）——Xen XSA-29 的 access_ok 只检查起始地址是半步修复典范；2019 TLB"理论单次足够但实践失效"是缓解不完整的另一形态 |
| **穷举排除迁移** | 把我在 2016 recursion / 2018 cache invalidation 用过的穷举排除法搬到新目标：列出所有看似可行的重用已释放对象的方案，逐条给出否定的技术理由（SLUB 分配器覆写前 8 字节阻断地址范围检查 / 回调缺失 / 边界检查 / 序列号重置），导出经排除后剩下的唯一路径。显式标注同构来源——"这是我在 2018 cache invalidation 用过这个否定理由，在这里是否成立取决于分配器行为是否同构"——避免把方法论迁移伪装成对当前目标的直接判断 |
```

---

## 3 prompt 干跑结果

假设我是 `vuln-mapper` / `report-critic` agent（CLAUDE.md Phase 3 workflow 内），带着这个 skill 回答。

### Prompt 1: "审一下这段 Linux 内核 VMA 缓存代码，这个优化有什么问题?"

- **触发维度**：维度 A 必选（审计/优化类）✓；"这个优化有什么问题"直接命中维度 A"优化假设审计""质疑优化中的正确性假设"（模型 3）。涉及可达性（VMA 缓存 UAF 可利用）→ +B 条件触发；涉及缓解（KASLR/Dirty-PTE）→ +C 条件触发。B/C 是条件触发，skill 路由表"+B 如涉及可达性""+C 如涉及缓解"——mapper 需自行推断 VMA 缓存 UAF 的利用相关性与缓解相关性。
- **是否提示用 C SAST 工具**：✓ 是。Step 2 第 113 行明确"对于本仓库的目标代码审计，优先使用 `mcp__mcp-server-atomic-sast4c__*` / `mcp__mcp-server-atomic-sast4go__*` / `mcp__mcp-server-atomic-sast4rust__*` 的符号感知工具（`get_function_call`、`get_function_definition`、`get_macro_definition`、`get_structure_definition`、`get_variable_consumer`），而非裸 Grep"。Linux 内核是 C，`mcp__mcp-server-atomic-sast4c__*` 被显式推荐且工具名正确。
- **是否知道先做什么**：✓ 是。Step 1 首动作"扫描用户提问是否含具体指代——具体文件/函数/CVE 编号/补丁 URL/内核子系统名/缓解机制名。含→必须先调工具，绝不凭训练语料直接答"。"VMA 缓存"是具体内核子系统名，mapper 知道先 `get_function_definition`（定位 `find_vma`/`vma_cache` 等）/`get_macro_definition`（定位序列号宏）/`get_structure_definition`（定位 `mm_struct`/`vm_area_struct`），再下判断。
- **卡点**：① "这段…代码"是 deictic 指代，若用户未给绝对路径，mapper 需先 `grep_code`/`get_function_definition` 定位——skill 支持（Step 1 含"具体文件/函数"触发工具），但未明确"deictic 指代无路径时先定位还是先问用户"；② 维度 A"优化假设审计"要求"追溯优化的历史演变（git log、commit message）"——模型 3 局限已说明"需要能追溯优化的历史演变"，但 Step 2 维度 A 未教如何用工具查 git log（需 Bash `git log -p --follow`）；③ 跨域类比规则触发——Horn 的 2018 cache invalidation（CVE-2018-17182）正是 VMA 缓存案例，mapper 应回忆该案例作历史类比（SLUB 前 8 字节覆写否定理由），但 skill 未显式提示"对 VMA 缓存回忆 2018 cache invalidation 的穷举排除"。

### Prompt 2: "CVE-2018-17120（CVE 编号可能记错，实指 2018 cache invalidation）的补丁不变量是什么?目标代码有没有?"

- **触发维度**：❌ **无干净路由**。这是"历史补丁/不变量比较类"问题，路由表 6 行无一匹配。落到"混合问题"兜底→"取 A/B/C/D/E 至少一个"——但 A-E 无一维度是"提取补丁不变量+目标比较"。维度 C（缓解评估）最近，但 C 是"这个缓解能否被反转利用"（目标侧），不是"历史补丁引入什么不变量"（历史侧）。**这是 skill 最大的路由缺口，直接证实维度 1 的批评——与 Rory 同款。**
- **是否触发历史补丁比较**：⚠️ 部分。Step 1 首动作"含 CVE 编号→必须先调工具"触发（WebFetch 补丁/Read 目标代码）；Step 3 JSON 停止规则要求"历史补丁不变量比较"——但仅在 JSON 模式下。本 prompt 单独看不含 batch/mapper/critic 关键词，**JSON 模式不触发**（skill 的 JSON 触发是关键词驱动，未覆盖角色驱动）→ `historical_patch_analysis` 字段填充指引不激活。即便 mapper 在 Phase 3 角色上下文内，skill 的关键词触发也会漏。
- **JSON 输出模式是否激活**：❌ 不激活（关键词驱动触发漏掉角色上下文）。这是维度 5 批评点 d（JSON 触发纯关键词驱动）的实证。
- **是否知道先做什么**：⚠️ 知道"先调工具"（Step 1），但**不知道用哪个维度研究**（Step 2 无 F 维度），也不知道"不变量从 Phase 2 的 `security_invariant_after_patch`/`fix_commits[].url` 提取"（skill 未说源在哪）。mapper 会凭自觉 WebFetch 补丁、提炼不变量、grep 目标——能做，但 skill 未教，mapper 可能照抄 collector 摘要的 `security_invariant_after_patch` 字段而非自己读 diff 提炼。
- **不变量提取源教了没**：❌ 未教。skill 只说"用我的视角填充 `historical_patch_analysis`（`source_patch_invariant`/`target_invariant_status`）"，未说明源在 Phase 2 的 `security_invariant_after_patch`/`fix_commits[].url`，未教 WebFetch 读 diff 自己提炼。**这是 Horn 最可能的缺口，对照 Rory 维度 F——Rory 已补此指引，Horn 未补。**
- **卡点**：① 路由缺口（无 F 维度）；② JSON 模式不激活（关键词触发漏角色上下文）；③ 不变量提取源未说明（mapper 可能不读 diff，只抄 `security_invariant_after_patch` 字段）；④ `target_invariant_status` 逐点验证方法未教。**Prompt 2 是 skill 处理最差的，正是维度 1+5 同源缺口的体现——与 Rory 精炼前 Prompt 2 完全同构。**

### Prompt 3: "这个缓解（栈随机化）能被反转利用吗?"

- **触发维度**：✓ 维度 C 必选（缓解评估类）。"缓解反转"是 Horn 标志性立场（维度 C"缓解反转"+ 模型 4"缓解反转与半步修复批判"）。skill 路由"缓解评估类→维度 C 必选；通常不需 A/B"✓。模型 4 应用明确："这个缓解能否被攻击者反转利用（如栈随机化变成攻击者的信息源——`That is supposed to be a security mitigation, but works to my advantage.`）"——直接命中。
- **穷举排除/缓解反转填 rationale**：⚠️ 部分。维度 C"缓解反转"命中，但"穷举排除"是维度 A 的方法论，Prompt 3 是缓解评估，穷举排除是否填 rationale？skill 未说明 C 是否要带穷举排除。其实 Horn 方法论里，**缓解反转的证明需要穷举"攻击者如何把缓解变成信息源/原语"的候选方案，逐条给出技术理由**——这与 Horn 的穷举排除是同一思维。skill 维度 C 未点明"缓解反转也要穷举排除候选利用方式"，mapper 可能只给一条反转路径就停，违反 Horn"穷举排除"方法论。
- **是否知道先做什么**：⚠️ 知道德 C 研究路径（缓解反转/半步修复/确定性 vs 概率性/缓解存在≠用户受保护）。"栈随机化"是具体缓解机制名，Step 1 首动作触发工具——但"栈随机化"在目标代码里怎么搜？skill 未教（栈随机化在 Linux 内核是 `CONFIG_RANDOMIZE_BASE` 编译期配置 + `arch/x86/kernel/` 代码，不是单一函数）。Step 1 说"缓解机制名→含→必须先调工具"，但未说怎么用 MCP SAST 工具搜缓解机制（因缓解常是编译期宏/配置/Kconfig，不是函数，`get_function_call` 不命中，需 `get_macro_definition`/`grep_code` 搜 `RANDOMIZE`/`KASLR`）。
- **卡点**：① "栈随机化"是缓解机制名，但 MCP SAST 工具搜函数/宏/结构体——栈随机化是编译期配置 + arch 代码，skill 未教如何用 `get_macro_definition`/`grep_code` 搜编译期配置与 Kconfig；② "缓解反转"是强断言（检查点 3"强断言前标注"应触发"⚠ 反常识断言"——因"缓解被反转利用"对一般开发者反常识），但触发判据"与常见认知相反"主观，mapper 可能不标；③ 维度 C 未点明"缓解反转也要穷举排除候选利用方式"——Horn 方法论里，缓解反转的证明需穷举"攻击者如何把缓解变成信息源/原语"的候选，逐条给技术理由，skill 未教这点。

---

## 总结

**是否"激活即执行"**:
- Prompt 1：✓ 基本激活即执行（A 触发、C SAST 工具提示正确、先调工具明确）；B/C 条件触发略软，deictic 定位略模糊，git log 追溯未教
- Prompt 2：❌ **未达激活即执行**——路由缺口（无 F 维度）+ JSON 模式不激活（关键词触发漏角色上下文）+ 不变量提取源未教（mapper 可能照抄 `security_invariant_after_patch` 而非读 diff 提炼）。这是 skill 最大缺陷——与 Rory 精炼前 Prompt 2 完全同构
- Prompt 3：✓ 激活即执行（C 触发、缓解反转明确）；缓解机制名 MCP 搜索方法未教（栈随机化是 Kconfig + arch 代码，非函数），穷举排除与缓解反转的关系未点明

**最需改的（优先级）**:
1. **维度 5 + 维度 1 同源缺口**：加"历史补丁/不变量比较类"路由行 + 维度 F（补丁不变量提取+目标比较），并把 `historical_patch_analysis` 字段填充指引写实（源从 Phase 2 `security_invariant_after_patch`/`fix_commits[].url`，WebFetch 读 diff 自己提炼，`target_invariant_status` 逐点验证）。这一改同时修 Prompt 2 路由缺口和 JSON 模式 `historical_patch_analysis` 薄弱。**注意 Horn 的维度 F 体现 Horn 方法论（穷举排除、质疑优化假设、缓解反转、SLUB 前 8 字节、access_ok 偏移、TLB 理论 vs 实践），不套用 Rory 的 fd-based/边界不变量内容**
2. **维度 5 mapper/critic 分栏**：补 `critic_output_v1` 各字段（`critic_verdict`/`reason`/`evidence_checked`/`additional_evidence`/`historical_patch_assessment`/`required_follow_up`/`systemic_patterns`）的 Horn 视角填法——目前零指引。同时补 mapper 侧 `matched_locations`/`attack_surface`/`audit_suggestions` 三字段
3. **维度 5 mitigations 填法纠偏**：明文规定 `mitigations` 仅填目标代码已存在缓解（KASLR/seccomp/capability/bounds check/locking），不要把 Horn 的披露实践（完整 PoC 公开 / Make zeroday hard）填进 mitigations（category error）
4. **维度 5 JSON 触发**：从纯关键词驱动改为"关键词或角色上下文驱动"（`vuln-mapper`/`report-critic` agent 在 Phase 3 即触发，即便单条 CVE prompt 不含关键词）
5. **维度 2 检查点 6 泛化**：把"Spectre embargo 沉默"泛化为"披露决策内情/政策例外沉默"，Spectre 作示例；补检查点 7"目标仓库未 clone/`target_repo_path` 不可用"和检查点 8"工具假阳性（`mcp__mcp-server-atomic-sast4c__*` 返回指向错误符号，如把宏误当函数、把内联函数当独立符号）"
6. **维度 6 non_activation 反向路由**：补"Linux userland privesc / 容器运行时边界（DBus/Polkit/AppArmor/wpa_supplicant/runc/BuildKit）→ rory-mcnamara"——Rory 的 non_activation 明文指向 Horn，Horn 应反向指向 Rory；并区分"Chrome renderer sandbox→kernel 是我专长，容器 runtime escape 不是"
7. **维度 8 触发词补全**：加"VMA 缓存/cache invalidation""TLB/mremap/页表""Spectre/Meltdown/分支预测器/BTB/BHB/侧信道""沙箱逃逸/Chrome renderer sandbox→kernel""MSG_OOB""读原语/write 原语/exploit chain""半步修复""Make zeroday hard""access_ok/Xen/hypervisor 逃逸""实验驱动探测/经验性逆向"

**优点（记录）**:
- **核心原则精准**：Step 2 开头"一切归结为：这个优化隐含了什么正确性假设？这个假设在什么边界条件下失效？"——这是 Horn 模型 3（质疑优化中的正确性假设）的方法论精髓，比 Rory 的"特权边界在哪"更贴 Horn
- **工具命名正确**：skill 用 `mcp__mcp-server-atomic-sast4c__*`（匹配实际 MCP 工具前缀），且 Step 2 列全 sast4c/sast4go/sast4rust 三个前缀——比 CLAUDE.md 的 stale 名 `mcp__LocalAtomicSAST4C__*` 更准
- **诚实边界处理正确**：Horn 有 9 篇 P0 亲笔长文，思维是直接自述——skill **未**加 Rory 专属的"行为即思维输出规则"块（角色扮演规则止于 9 条，无 Rory 的 Rule 10）。这是正确的领域判断，不硬套 Rory 专属改动
- non_activation 路由 5 条指向准确（维度 6 = 4，仅缺反向路由 Rory）
- 检查点 1-5 是真实失败模式且"激活即执行"（维度 3 = 4），有具体触发条件+动作模板
- 首动作"含具体指代→必先调工具，绝不凭训练语料直接答"是强约束，防编造
- 模型证据扎实（7 个模型均 ≥3-5 域 [1H] 证据，Horn 有 9 篇亲笔长文，优于 Rory 的 4 篇 byline + 行为推断）

**是否需调整**：是，需调整。优先级 1-4 是结构性改动（加路由行 + 维度 F + mapper/critic 分栏 + mitigations 纠偏 + JSON 触发），直接修 Prompt 2 暴露的缺口；优先级 5-7 是增量改动（检查点泛化 + non_activation 反向路由 + 补触发词）。改后 Prompt 2 应从"未达激活即执行"升至"激活即执行"。**改后文本必须保留 Horn 方法论底色（穷举排除、质疑优化假设、缓解反转、SLUB/access_ok/TLB 历史 case），不可套用 Rory 的 fd-based/边界不变量——team lead 已提示 Horn 有自述样本，不需"行为即思维"块，本评估的改后文本已遵守此约束。**

**文件写入**：成功写入 `/Users/bytedance/Projects/Security/OssVulnAnalogy-AgentTeam/.claude/skills/jann-horn-perspective/references/research/08-refinement-optimizer.md`

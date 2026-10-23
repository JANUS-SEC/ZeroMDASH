# Rory Skill — auto-skill-optimizer 评估

评估对象: `/Users/bytedance/Projects/Security/OssVulnAnalogy-AgentTeam/.claude/skills/rory-mcnamara-perspective/SKILL.md`
评估视角: auto-skill-optimizer(8 维度结构评估 + 3 prompt 干跑)
评估日期: 2026-07-28

---

## 8 维度评分

| 维度 | 分(1-5) | 说明 |
|------|---------|------|
| 1. 工作流清晰度(Agentic Protocol) | **3** | Step 1→2→3 流程清晰、首动作"含具体指代→必先调工具"很扎实;但路由表缺**历史补丁/不变量比较类**这一行(Phase 3 的核心问题类型),CVE-补丁不变量问题只能落进"混合问题"兜底;维度 A 与 C 在 race/TOCTOU 上重叠(A 的"race/TOCTOU 优先" vs C 的"mount cleanup 时序/cache race"),路由表用"+C 如涉及逃逸可达性"打补丁但未说明 A/C 分工 |
| 2. 边界条件(检查点机制) | **4** | 6 检查点覆盖工具冲突/工具失败/强断言/red-yellow 低置信/跨专长/Leaky Vessels 归属,前 5 个是真实失败模式;但检查点 6"Leaky Vessels 归属沉默"是**单 CVE 边例冒充通用检查点**(应泛化为"命名/发现权归属沉默");缺"目标仓库未 clone / `target_repo_path` 不可用"(vuln-mining mapper 要求 repo 已 clone,skill 未处理此失败模式)和"工具假阳性"(工具返回结果但指向错误符号) |
| 3. 检查点设计(激活即执行) | **4** | 多数检查点有具体触发条件+动作模板(✅ 工具冲突→"问按哪个来源继续";✅ 强断言→"段落开头标 ⚠ 反常识断言";✅ red/yellow 低置信→"评级旁标 confidence: low, 建议二次验证"),激活即可执行;小瑕疵:检查点 2"多次返回空"未量化("多次"=几次?),检查点 3"与常见认知相反"主观("常见认知"由谁定?) |
| 4. 指令具体性 | **4** | 7 个心智模型 + 10 条启发式均带"应用"+"局限",多数具体可执行(模型 3 局限"竞争窗口需 strace -tt 时序信号,对确定性无并发代码不适用";模型 4 局限"闭源/混淆二进制 strace 信号弱");少数局限略泛(模型 5"需工程判断区分金矿与荒地"),模型 7 应用自承"不太用于分析新问题"——诚实但弱 |
| 5. vuln-mining JSON 输出模式 | **3** | Step 3 末"输出模式停止规则"触及 `mapper_output_v1`,列出 rationale/historical_patch_analysis/mitigations/negative_evidence/searches_run 5 字段;但**漏 3 个 mapper 字段**(`matched_locations`/`attack_surface`/`audit_suggestions` 无填充指引);**`critic_output_v1` 零字段指引**(skill 承认两种 schema 但所有字段指导都是 mapper 侧,Rory 作 report-critic 时无 critic_verdict/reason/evidence_checked/historical_patch_assessment/required_follow_up 的填法);**mitigations 概念错位**——把"补丁同日发检测器"填进 mitigations 是 category error(那是披露实践,不是目标代码缓解);JSON 模式触发是关键词驱动("用户提到 batch/mapper/..."),未覆盖角色驱动(mapper agent 单条 CVE prompt 可能不含这些关键词) |
| 6. non_activation 路由 | **5** | 6 条非触发场景指向准确:CPU 微架构→jann-horn ✓;iOS/macOS 内核→ian-beer ✓;Windows 用户态/AV/CPU fuzzing 工具→tavis-ormandy ✓;hypervisor 侧→felix-wilhelm/thomas-bouzerar ✓;云控制平面→Wiz/Aqua 方向(非 skill,声明领域边界)✓;Web 应用/防御运营→非专长 ✓。跨 skill 切换段 + 检查点 5 + non_activation 三处一致指向同一组 skill,无错误指向 |
| 7. 诚实边界与"行为即思维" | **4** | 局限不止写在"诚实边界"段,已织入回答规则:角色扮演规则 10(行为即思维:"任何'我这样想'都要落在'我这样做…因此可推断我这样想'上")、规则 7(不编造 CVE/补丁 SHA)、规则 3(精确标注不知道什么)、检查点 6、模型 7 局限。口头维度空集 + 社交媒体样本极小 + 行为推断非自述三处均有体现;小瑕疵:"5 条归档推文 + 2024-2026 社交媒体缺失"未充分落到回答规则(未规定"容器研究期口癖仅用 writeup 校准的,不用推学校准") |
| 8. 触发词覆盖 | **4** | 任务指定的 5 个方法描述触发词**全部覆盖**:race condition/TOCTOU ✓、边界不变量违反 ✓、容器逃逸面 ✓、fd-vs-path ✓、strace 驱动审计 ✓;但漏多个 Rory 签名方法描述触发词:"半步修复/partial fix"、"协调披露/多变体合并披露"、"DBus/Polkit/AppArmor"(Ubuntu privesc 域)、"openat/O_NOFOLLOW"(fd-based 倡导)、"eBPF 检测器/静态检测器"(工具化交付签名)。这些是 Rory 写作高频方法词,缺触发会漏激活 |

**最弱 2 维度**: 维度 5(3 分,最多子缺口)与维度 1(3 分,补丁分析路由缺口,且被 Prompt 2 干跑证实)。两者同源:工作流缺"补丁不变量提取"维度 → JSON 模式缺 `historical_patch_analysis` 填充指引,是同一结构性缺口的两面。

---

## 最弱 2 维度(重点)

### 维度 5: vuln-mining JSON 输出模式

**问题**:
1. `mapper_output_v1` 字段指引不全 —— 漏 `matched_locations`(red/yellow 证据落点)、`attack_surface`(维度 C 的 reachability 输出)、`audit_suggestions`(Rory 擅长的手工审计/fuzz 建议)三字段,Rory 视角无处可落
2. `critic_output_v1` 零字段指引 —— skill 写"按 `mapper_output_v1` 或 `critic_output_v1` schema 输出",但所有字段指导都是 mapper 侧。Rory 作 report-critic 时,`critic_verdict`/`reason`/`evidence_checked`/`additional_evidence`/`historical_patch_assessment`/`required_follow_up`/`remap_requests` 全无填法
3. `mitigations` 概念错位 —— skill 让"补丁同日发检测器"填进 `mitigations`,但 `mitigations` 是目标代码已存在的缓解(fd-based/seccomp/capability),而"补丁同日发检测器"是 Rory 的披露实践,填进去是 category error
4. JSON 模式触发仅关键词驱动 —— "用户提到 batch/mapper/critic/Phase 3/CLAUDE.md/03-risk-mappings"才触发;但 mapper agent 在 Phase 3 内处理单条 CVE 时,该条 prompt 可能不含这些关键词,角色上下文未触发 JSON 模式
5. `historical_patch_analysis` 指引太薄 —— 只说"填 `source_patch_invariant`/`target_invariant_status`",没说不变量从哪提取(Phase 2 的 `security_invariant_after_patch`/`fix_commits[].url`)、`target_invariant_status` 怎么逐点验证、`unknown` 何时可用

**改后文本示例**(直接替换 SKILL.md 第 201-208 行"#### 输出模式停止规则(vuln-mining workflow 内)"整节):

```markdown
#### 输出模式停止规则(vuln-mining workflow 内)

如果用户在本仓库 vuln-mining workflow 内调用(提到 batch / mapper / critic / Phase 3 / CLAUDE.md / 03-risk-mappings,**或**你作为 `vuln-mapper` / `report-critic` agent 被编排进 Phase 3——即便单条 CVE prompt 未含这些关键词,角色上下文即触发),**必须**按 CLAUDE.md 的 `mapper_output_v1` 或 `critic_output_v1` JSON schema 输出,**不**写多段叙事。上面的标志性篇章结构仅用于自由问答模式。

**作为 `vuln-mapper`(输出 `mapper_output_v1`)**——按字段填我的视角,每个字段都要落到代码证据或行为推断:

- `searches_run`:必须记录 `mcp__mcp-server-atomic-sast4go__*` 调用(目标 Go 时尤其重要,符合 CLAUDE.md Code Analysis Tool Policy;注意 CLAUDE.md 写的 `mcp__LocalAtomicSAST4C__*` 是 stale 名,实际工具前缀是 `mcp__mcp-server-atomic-sast4go__*`/`sast4c__*`/`sast4rust__*`)。每条记 `query`(符号名/函数名)+ `scope`(绝对路径子目录)+ `result_summary`(命中数)。裸 Grep 只在 MCP 失败时兜底,并在 `negative_evidence` 或 `completion_notes` 写明 MCP 为何不可用
- `matched_locations`:red/yellow finding 的绝对 `path`+`line`+`symbol`+`snippet` 必填。`role` 用我的维度映射——维度 A 边界违反→`equivalent_pattern`;维度 C 入口→`entry_point`;fd-based/seccomp/capability/O_NOFOLLOW→`mitigation`(present)或 `negative_evidence`(absent)
- `attack_surface`:维度 C 的输出落这里。`entry_points` 填跨边界入口(容器↔宿主 / fd↔path / mount↔cleanup 的绝对 file:line);`reachable` 填能否端到端逃逸(只 crash 不算,要完整 PoC);`data_flow_summary` 填"handler → parser → sink"式跨边界数据流
- `historical_patch_analysis`(**核心**):`source_patch_invariant` 从 Phase 2 的 `security_invariant_after_patch` 提取(如"子进程 cwd 不得落在宿主 mount namespace");`target_invariant_status` 填 `present|absent|partial|unknown`——对照目标代码逐 file:line 验证;`comparison_summary` 写目标代码与历史补丁的同构/异构;`patch_evidence_used` 填 `fix_commits[].url`。**不可**只填 `unknown` 跳过比较——若补丁证据 unavailable,在 `comparison_summary` 显式说明为何
- `mitigations`:**仅填目标代码里已存在的缓解**(fd-based 操作 / seccomp / capability drop / O_NOFOLLOW / locking),`type` 用 schema 枚举(`bounds_check|sandbox|locking|validation|fuzzing|other`),`status` 用 `present|absent|partial|unknown`。**不要**把我历史披露的"补丁同日发检测器"填这里——那是我的披露实践,不是目标代码的缓解,填进去是 category error;披露实践应填进 `rationale` 或 `audit_suggestions`
- `negative_evidence`:填我搜过但未命中的东西(如"全仓 grep seccomp 0 命中""无 openat+O_NOFOLLOW 调用点")——体现"特权边界先行 / race-TOCTOU 优先 / fd-vs-path / 半步修复检测"方法论
- `rationale`:浓缩我的判断——特权边界在哪、什么跨过、哪个不变量在边界处被违反、是 bug 还是"按预期工作的特性"、半步修复还是根除
- `audit_suggestions`:我擅长的手工审计建议(如"strace -tt 跟 mount cleanup 时序""toy C 程序注入 signal 复现 race""fuzz parser at <file:line> with oversized frame""配静态 AST + eBPF 动态检测器")

**作为 `report-critic`(输出 `critic_output_v1`)**——按字段填我的审视视角:

- `critic_verdict`:`agree|downgrade|upgrade|insufficient_evidence`——我倾向保守,若 mapper 的 red 仅凭框架外推无 file:line,判 `downgrade` 或 `insufficient_evidence`
- `recommended_risk_level`:校准后的评级
- `reason`:用我的方法论写为何维持/降级——"mapper 命中 sink 但未证跨边界可达性""red 仅凭 path-based 推断,但目标已用 openat+O_NOFOLLOW(fd-based),应降为 yellow"
- `evidence_checked`:我独立 Read/Grep/MCP 验证过的绝对 file:line
- `additional_evidence`:mapper 漏掉的边界信号(如"file.go:140 有 mutex 降低可利用性""cleanup 在 mount 前,有 race 窗口 mapper 未报")
- `historical_patch_evidence_checked`:我独立核过的 `fix_commits[].url`
- `historical_patch_assessment`:目标是否实现/缺失/部分实现历史补丁不变量(对应 mapper 的 `target_invariant_status`,我独立校验)
- `required_follow_up`:要求 mapper 补的检查(如"追 foo_ioctl 从外部 ioctl dispatch 的调用链""读 file.c 120-180 行")
- `remap_requests`:`challenge_type` 用 `missing_reachability|weak_evidence|missed_mitigation|wrong_rating|missed_equivalent_code|other`;`blocking` 仅在缺关键证据时 true
- `systemic_patterns` / `coverage_gaps`:我若发现跨 CVE 的共性(如"多个 cleanup 路径都缺 cwd 校验")或 mapper 未覆盖的边界(如"CLI 参数入口无人审"),填这里

red/yellow finding 必须有绝对 file:line 证据(填 `matched_locations`)+ 历史补丁不变量比较(填 `historical_patch_analysis`)。`status` 必须为 `completed`;若某 CVE 工具证据不足,标 `incomplete` 并在 `completion_notes` 说明,不要伪装 `completed`。
```

---

### 维度 1: 工作流清晰度(Agentic Protocol)

**问题**:
1. **路由表缺"历史补丁/不变量比较类"行** —— "CVE-2024-21626 的补丁不变量是什么?目标代码有没有这个不变量?"是 Phase 3 的核心问题类型(对应 `historical_patch_analysis` 字段),但路由表 8 行无一匹配:非审计类(不找新 bug)、非逃逸类(不问能否逃)、非文件类、非缓解类(D 是"这个缓解能否被绕过",目标侧,不是历史补丁侧)、非披露类、非研究方向、非纯框架。落到"混合问题"兜底,但"取 A/B/C/D/E 至少一个"无一个维度是"提取补丁不变量+目标比较"
2. **维度 A 与 C 在 race/TOCTOU 重叠** —— A 有"race/TOCTOU 优先"和"边界不变量违反",C 有"mount cleanup 时序""cache race""entitlements 校验"。路由表用"A 必选;+C 如涉及逃逸可达性"打补丁,但未说明 A/C 分工:同一份 mount cleanup 代码,A 回答"这里有没有新 race",C 回答"这个 race 能不能逃到宿主"——两者先后递进,不重复,但 skill 未点明,mapper 可能重复劳动或漏其一
3. **Step 2 无"补丁不变量提取"研究维度** —— Step 3 的 JSON 停止规则要求"red/yellow 必须有历史补丁不变量比较",但 Step 2 的 A-E 维度无一教如何提取不变量,输出要求与研究方法脱节

**改后文本示例 1**(直接替换 SKILL.md 第 107-118 行路由表 + 紧随其后的"模糊时降级"前插入分工说明):

```markdown
| 问题类型 | 特征信号 | Step 2 维度路由 |
|---------|---------|----------------|
| **审计类** | "审一下这段容器/运行时代码""这个 mount/cleanup 有没有问题""这个 syscall 安全吗" | 维度 A 必选;+ B 如涉及文件操作;+ C 如涉及逃逸可达性 |
| **历史补丁/不变量比较类** | "这个 CVE 的补丁不变量是什么""目标代码有没有这个不变量""这个补丁修透了没""目标与历史修复同构吗" | 维度 F 必选;+ C 如涉及逃逸可达性;+ D 如涉及缓解是否半步修复 |
| **逃逸/可达性类** | "这个 bug 能逃逸吗""能越权到宿主吗""影响多大" | 维度 C 必选;+ A 如涉及边界不变量;+ B 如涉及 fd/path |
| **文件操作/路径类** | "这个文件操作安全吗""路径校验够不够" | 维度 B 必选;+ A 如涉及边界 |
| **缓解评估类** | "这个缓解有效吗""这个修复够不够""要不要发检测器" | 维度 D 必选 |
| **披露策略类** | "要不要报上游""留多久窗口""要不要发 PoC""该致谢谁" | 维度 E 必选(需查我的披露案例,不可凭框架答) |
| **研究方向类** | "下一个研究什么""怎么选容器运行时目标""哪个组件值得审" | **跳过 Step 2 工具调用**,直接用模型 5 + 启发式 5 进入 Step 3 |
| **纯框架问题** | 边界分析方法论、披露策略原则、轻工具哲学 | **跳过 Step 2**,直接用相关心智模型进入 Step 3 |
| **混合问题** | 用具体案例讨论边界或研究策略 | 取对应类别维度(A/B/C/D/E/F 至少一个),再进入 Step 3 |

**A 与 C 的分工(避免 race/TOCTOU 重复)**:维度 A 的"race/TOCTOU 优先"是**找新的竞争窗口**(audit 模式——目标里有没有尚未报告的 race);维度 C 的"mount cleanup 时序/cache race"是**已知/疑似违反能否端到端逃逸**(reachability 模式)。同一份 mount cleanup 代码,A 回答"这里有没有 race",C 回答"这个 race 能不能逃到宿主"。两者先后递进,不重复。
```

**改后文本示例 2**(在 SKILL.md 第 172 行维度 E 之后、"#### 研究输出格式"之前插入新维度 F):

```markdown
#### F. 历史补丁不变量提取与目标比较("这个补丁引入了什么不变量?目标代码有没有它?")

| 研究维度 | 具体搜索 |
|---------|---------|
| **补丁不变量提取** | 从 Phase 2 的 `security_invariant_after_patch` / `fix_commits` / `patch_diff_summary` 提取历史补丁引入的不变量(如"子进程 cwd 不得落在宿主 mount namespace""mount stub 须在 cleanup 前完成""entitlements 须校验")。用 WebFetch 读 `fix_commits[].url` 的 diff,自己提炼不变量,不照抄 collector 摘要 |
| **目标同构定位** | 目标代码里是否存在同构的边界?用 `mcp__mcp-server-atomic-sast4go__get_function_call` / `get_function_definition` / `grep_code` 定位对应 cleanup/mount/cwd/entitlements 处理点。绝不凭训练语料假定目标"应该有这段代码" |
| **不变量逐点验证** | 逐 file:line 验证不变量在目标是否成立——`present`(已实现)/`absent`(缺失)/`partial`(部分实现)/`unknown`(证据不足)。每条结论配 `matched_locations` 的绝对 path+line+snippet |
| **半步修复检测** | 若目标 `partial`,问:堵的是主路径还是留下偏移/竞争路径?(只补 offset 0 / 只校验主 mount 留下 cleanup 窗口 = 半步修复,对应 `target_invariant_status: partial`) |
| **跨域类比显式标注** | 把 Leaky Vessels/BuildKit 的方法论搬到新目标时,标注同构来源——"这是 Leaky Vessels 的 process.cwd 落点分析,在此是否成立取决于边界条件是否同构",避免把方法论迁移伪装成对当前目标的直接判断 |
```

---

## 3 prompt 干跑结果

假设我是 vuln-mapper agent(Phase 3 内),带着这个 skill 回答。

### Prompt 1: "审一下这段 runc 的 mount cleanup 代码有没有问题"

- **触发维度**: 维度 A 必选(审计类)✓;涉及 mount cleanup(文件/路径)→ +B;涉及逃逸可达性(runc mount cleanup 正是 Leaky Vessels 战场)→ +C。A+C 触发,但 **C 是条件触发**("如涉及逃逸可达性"),skill 未强制——mapper 需自行推断 runc mount cleanup 的逃逸相关性。维度 A 的"race/TOCTOU 优先""边界不变量违反"直接命中。
- **是否提示用 Go SAST 工具**: ✓ 是。Step 2 明确"runc/BuildKit/containerd/podman/Incus/snapd 都是 Go,优先使用 `mcp__mcp-server-atomic-sast4go__*` 的符号感知工具(`get_function_call`/`get_function_definition`/`grep_code` 等),而非裸 Grep"。runc 被点名,Go SAST 工具被显式推荐。
- **是否知道先做什么**: ✓ 是。Step 1 首动作"扫描用户提问是否含具体指代——容器运行时组件名(runc/BuildKit/...)→ 含→必须先调工具,绝不凭训练语料直接答"。runc 是被点名的 runtime 组件,mount cleanup 是具体子系统,mapper 知道先 `grep_code`/`get_function_definition` 定位 mount cleanup 代码,再下判断。
- **卡点**: ① "这段…代码"是 deictic 指代,若用户未给绝对路径,mapper 需先 grep 定位——skill 支持(Step 1 含"具体文件"触发工具),但未明确"deictic 指代无路径时先 grep 定位还是先问用户";② C 条件触发可能漏(runc mount cleanup 的逃逸相关性是隐含的,保守 mapper 应主动加 C,但 skill 不强制);③ skill 未显式提示"对 runc mount cleanup 回忆 Leaky Vessels CVE-2024-21626/23652 作历史类比"——跨域类比规则会触发,但要 mapper 自觉。

### Prompt 2: "CVE-2024-21626 的补丁不变量是什么?目标代码有没有这个不变量?"

- **触发维度**: ❌ **无干净路由**。这是"历史补丁/不变量比较类"问题,路由表 8 行无一匹配。落到"混合问题"兜底→"取 A/B/C/D/E 至少一个"——但 A-E 无一维度是"提取补丁不变量+目标比较"。维度 D(缓解评估)最近,但 D 是"这个缓解能否被绕过"(目标侧),不是"历史补丁引入什么不变量"(历史侧)。**这是 skill 最大的路由缺口,直接证实维度 1 的批评。**
- **是否触发历史补丁比较**: ⚠️ 部分。Step 1 首动作"含 CVE 编号→必须先调工具"触发(WebFetch 补丁/Read 目标代码);Step 3 JSON 停止规则要求"历史补丁不变量比较"——但仅在 JSON 模式下。本 prompt 单独看不含 batch/mapper/critic 关键词,**JSON 模式不触发**(skill 的 JSON 触发是关键词驱动,未覆盖角色驱动)→ historical_patch_analysis 字段填充指引不激活。即便 mapper 在 Phase 3 角色上下文内,skill 的关键词触发也会漏。
- **JSON 输出模式是否激活**: ❌ 不激活(关键词驱动触发漏掉角色上下文)。这是维度 5 批评点 4 的实证。
- **是否知道先做什么**: ⚠️ 知道"先调工具"(Step 1),但**不知道用哪个维度研究**(Step 2 无 F 维度),也不知道"不变量从 Phase 2 的 `security_invariant_after_patch`/`fix_commits[].url` 提取"(skill 未说源在哪)。mapper 会凭自觉 WebFetch 补丁、提炼不变量、grep 目标——能做,但 skill 未教,mapper 可能照抄 collector 摘要而非自己读 diff 提炼。
- **卡点**: ① 路由缺口(无 F 维度);② JSON 模式不激活(关键词触发漏角色上下文);③ 不变量提取源未说明(mapper 可能不读 diff,只抄 `security_invariant_after_patch` 字段);④ `target_invariant_status` 逐点验证方法未教。**Prompt 2 是 skill 处理最差的,正是维度 1+5 同源缺口的体现。**

### Prompt 3: "这个文件操作用 path-based,安全吗?"

- **触发维度**: ✓ 维度 B 必选(文件操作/路径类)。"path-based 默认不安全"是 Rory 标准立场(维度 B "fd vs path"+ 启发式 4)。是否 +A(边界)?skill 路由"文件操作/路径类→B 必选;+A 如涉及边界"——path-based 操作涉及 fd↔path 边界,保守应加 A。
- **是否推动 fd-based**: ✓ 是。维度 B"设计修复方向:如果有漏洞,修复是否应推动 fd-based?只补单点 path 校验=半步修复";启发式 4"路径操作默认不安全,推动 fd-based(openat+O_NOFOLLOW+f* family)。点名生态级 gap(Node.js 缺 openat/O_NOFOLLOW='a significant gap';Go os.Root='gold standard')"。维度 B 还查"TOCTOU 窗口"和"生态级 gap"。push fd-based 明确。
- **是否知道先做什么**: ⚠️ 知道德 B 研究路径(fd vs path / TOCTOU / 生态 gap / 设计修复方向),但"这个文件操作"deictic 无路径——Step 1 首动作扫描"具体文件/函数",deictic 指代不明确时 skill 未规定"先 grep 定位还是先问用户要路径"。
- **卡点**: ① deictic 指代无路径,skill 无"先定位或先问"规则(同 Prompt 1 卡点 ①);② "path-based 默认不安全"是强断言,检查点 3"强断言前标注"可能触发("⚠ 反常识断言"——因"path-based 不安全"对一般开发者反常识),但触发判据"与常见认知相反"主观,mapper 可能不标;③ 维度 B 是 skill 最完整的维度之一,干跑表现最好。

---

## 总结

**是否"激活即执行"**:
- Prompt 1: ✓ 基本激活即执行(A 触发、Go SAST 提示、先调工具明确);C 条件触发略软,deictic 定位略模糊
- Prompt 2: ❌ **未达激活即执行**——路由缺口(无 F 维度)+ JSON 模式不激活(关键词触发漏角色)+ 不变量提取源未教。mapper 拿到 skill 不知先做什么维度、不知不变量从哪来。这是 skill 最大缺陷
- Prompt 3: ✓ 激活即执行(B 触发、push fd-based 明确);deictic 定位略模糊

**最需改的(优先级)**:
1. **维度 5 + 维度 1 同源缺口**:加"历史补丁/不变量比较类"路由行 + 维度 F(补丁不变量提取+目标比较),并把 `historical_patch_analysis` 字段填充指引写实(源从 Phase 2 `security_invariant_after_patch`/`fix_commits[].url`,`target_invariant_status` 逐点验证)。这一改同时修 Prompt 2 路由缺口和 JSON 模式 `historical_patch_analysis` 薄弱。
2. **维度 5 critic 字段指引**:补 `critic_output_v1` 各字段(`critic_verdict`/`reason`/`evidence_checked`/`historical_patch_assessment`/`required_follow_up`)的 Rory 视角填法——目前零指引。
3. **维度 5 mitigations category error**:把"补丁同日发检测器"从 `mitigations` 移到 `rationale`/`audit_suggestions`,`mitigations` 仅填目标代码已存在缓解。
4. **维度 5 JSON 触发**:从纯关键词驱动改为"关键词或角色上下文驱动"(`vuln-mapper`/`report-critic` agent 在 Phase 3 即触发,即便单条 CVE prompt 不含关键词)。
5. **维度 2 检查点 6 泛化**:把"Leaky Vessels 归属沉默"泛化为"命名/发现权归属沉默",Leaky Vessels 作示例;补检查点 7"目标仓库未 clone/`target_repo_path` 不可用"和检查点 8"工具假阳性(工具返回指向错误符号)"。
6. **维度 8 触发词补全**:加"半步修复/partial fix""协调披露/多变体合并披露""DBus/Polkit/AppArmor""openat/O_NOFOLLOW""eBPF 检测器/静态检测器"。

**优点(记录)**:
- non_activation 路由准确无误(维度 6 = 5),三处一致指向
- 诚实边界织入回答规则而非仅写在 诚实边界 段(维度 7 = 4),角色扮演规则 10"行为即思维"给出模板句"我这样做…因此可推断我这样想"
- 检查点 1-5 是真实失败模式且"激活即执行"(维度 3 = 4),有具体触发条件+动作模板
- 工具命名正确:skill 用 `mcp__mcp-server-atomic-sast4go__*`(匹配实际 MCP 工具前缀),而 CLAUDE.md 的 `mcp__LocalAtomicSAST4C__*` 是 stale 名——skill 在这点上比 CLAUDE.md 更准
- 首动作"含具体指代→必先调工具,绝不凭训练语料直接答"是强约束,防编造

**是否需调整**: 是,需调整。优先级 1-4 是结构性改动(加路由行+维度 F+critic 字段指引+mitigations 纠偏+JSON 触发),直接修 Prompt 2 暴露的缺口;优先级 5-6 是增量改动(检查点泛化+补触发词)。改后 Prompt 2 应从"未达激活即执行"升至"激活即执行"。

**文件写入**: 成功写入 `/Users/bytedance/Projects/Security/OssVulnAnalogy-AgentTeam/.claude/skills/rory-mcnamara-perspective/references/research/08-refinement-optimizer.md`

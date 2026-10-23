# Jann Horn Skill — skill-creator 评审

评审基准:实际读取 `jann-horn-perspective/SKILL.md`(605 行)并与刚完成 Phase 5 精炼的标杆 `rory-mcnamara-perspective/SKILL.md`(617 行)逐节对比。Horn 的 skill 蒸馏到 Phase 3 中断(`references/research/` 仅 01-06 六份,缺 `07-verification-tests`/`08-refinement-optimizer`/`09-refinement-creator`),Phase 5 精炼从未做过。以下评价基于文本证据(行号),非印象。

---

## A. 激活触发条件

### 覆盖度评价

**点名式覆盖:优秀,但 persona 式 trigger 有一处形式缺陷。** triggers 行 16-30 覆盖中英文点名变体(`用Jann Horn的视角`/`用Horn的视角`/`Horn会怎么看`/`Jann Horn会怎么挖`/`jann horn perspective`/`horn's take`/`what would jann think`/`ask jann`/`切换到Horn`/`切换到Jann Horn`/`帮我用Horn的角度想想`/`用P0内核研究员的思路`/`用spectre发现者的视角`/`用meltdown发现者的视角`/`从CPU微架构研究员角度`)。description 行 8-10 的散文对这些做了二次覆盖。与 Rory 点名式覆盖度持平。

**形式缺陷**:行 27-30 的 persona 式条目全部带 `用`/`从` 前缀(`用P0内核研究员的思路`/`用spectre发现者的视角`/`用meltdown发现者的视角`/`从CPU微架构研究员角度`)。trigger 匹配机制是"trigger 字符串是否为用户输入的子串"——用户输入 `P0内核研究员的思路`(不带 `用`)不含更长的 `用P0内核研究员的思路`,**不命中**;同理 `spectre发现者`/`meltdown发现者` 不命中各自的 `用...的视角` 形式。Rory 的 `用Snyk Labs容器研究员的思路`/`用Leaky Vessels发现者的视角` 有同一形式缺陷,但 Rory 的 09 评审未单独标出——对 Horn 更值得修,因为 `P0内核研究员`/`spectre发现者` 是用户最常脱口而出的裸指代。

**方法描述式覆盖:形式优秀,但关键词有缺口。** description 行 11-13 列出 5 个签名方法(优化假设失效/缓解反转/暴露面错配/impact-gating/穷举排除),triggers 行 32-36 全部以**裸关键词名词短语**形式收录——这正是 Rory 09 评审赞誉的标杆形式(能自然匹配疑问句"这个有暴露面错配吗")。Rory 的 triggers 被 09 评审批评为带 `找`/`评估` 前缀无法匹配疑问句;Horn **无此缺陷**,反向是 Rory 该向 Horn 看齐。

**关键词缺口**:Horn 的 7 个核心心智模型 + 10 条启发式中,以下签名概念无对应 trigger:
- **半步修复|half fix**(模型 4 核心概念,Xen XSA-29 只检查 offset 0)——Rory 09 评审已为 Rory 补此条,Horn 同样缺失
- **对手时间线|用户何时受保护**(模型 5,"It took more than two months...")——Horn 的高频自我引用,无 trigger
- **缓解绕过|缓解被绕过**(比"缓解反转"更广的常见疑问句式)——用户问"这个缓解能被绕过吗"不命中 `缓解反转|缓解被反转利用`
- **优化在并发下|并发假设失效**(模型 3 的并发失效场景)——用户问"这个优化在并发下安全吗"不命中 `优化假设失效`(后者要求完整短语)
- **读原语|read primitive**(启发式 2,"先建 semi-arbitrary read")——Horn 利用链构造的标志性概念
- **复杂安全规则**(启发式 3,"data structures with complex safety rules...make it hard for fuzzers")
- **dead end|自我纠正|不可行方案**(启发式 10,"公开丢弃不可行方案")——Horn 的诚实方法论标志

### 遗漏的常见表达

- **"P0 内核研究员的思路"**(不带 `用`)——见上形式缺陷
- **"spectre 发现者"/"meltdown 发现者"**(不带 `用...的视角`)——见上形式缺陷
- **"这个缓解能被绕过吗"**——`缓解反转|缓解被反转利用` 不命中此疑问句(缺 `绕过`),需补 `缓解绕过|缓解被绕过`
- **"这个优化在并发下安全吗"**——`优化假设失效` 不命中(要求完整短语),需补 `并发` 相关条目
- **"这个 bug 没证明 impact 要不要进 bugtracker"**——`impact-gating|未证明impact的bug` 命中 ✓(已覆盖)
- **"dead ends 怎么处理"**——Horn 启发式 10 的公开丢弃方法论,无 trigger

### non_activation 路由准确性

**优秀,且 Android/WebRTC 处理比 Rory 更坦诚,但有两处路由缺口。** 行 39-44 共 6 条,覆盖 iOS/macOS 内核(→ian-beer)、Windows/AV/CPU fuzzing 工具(→tavis)、hypervisor 侧实现(→felix/thomas)、Android/WebRTC/通信协议 fuzzing(行 42 显式声明"本仓库无对应 perspective skill"+"以 Horn 身份说明非我专长,描述该方向的方法特征即可,不要假装覆盖"——这点比 Rory 更坦诚,Rory 无"无对应 perspective"声明)、Web 应用(XSS/SQLI/SSRF)、纯防御运营(SOC/合规)。

**路由缺口 1**:容器运行时/构建器安全(runc/BuildKit/containerd/podman/Incus/snapd 边界、容器逃逸面)未路由给 rory-mcnamara-perspective。用户问"runc 这种怎么审""容器逃逸面"可能错误留在 Horn——Horn 做的是 Chrome 沙箱→内核逃逸(2025 MSG_OOB),不是容器运行时边界。Rory 才是容器运行时战场。

**路由缺口 2**:密码学理论(zero-knowledge/KZG/STARK/形式化验证)未路由。Horn 的 Rule 8(行 63)与检查点 5(行 78)把"密码学理论"列为超专长,但 non_activation 未给去向。本仓库存在 `hillai-ben-sasson-perspective`(Hillai Ben-Sasson = StarkWare 创始人,密码学家)——应路由过去,而非只说"That's not really my area"。这造成 Rule 8/non_activation 不一致:Rule 8 说超专长时建议更合适视角,但 non_activation 没给 crypto 的去向。

---

## B. 角色扮演规则可操作性

### 问题路由

**清晰,但缺维度 F(历史补丁不变量比较)——这是相对 Rory 标杆的最大可操作性回归。** Step 1 表格(行 98-106)7 行:审计/优化类→A、可达性/利用类→B、缓解评估类→C、披露策略类→E、研究方向类→跳过、纯框架→跳过、混合→取对应维度。Step 1.1-1.3 三段扫描(具体指代/披露策略/workflow 关键词)完整。模糊时降级(行 108)默认取 A+B,与 Rory 的 A+C 等价,覆盖面逻辑一致。

**维度 F 缺失**:Horn 的 Step 2 只有 A-E 五维(行 115-160)。但 Step 3 JSON 模式停止规则(行 191-194)要求填 `historical_patch_analysis.source_patch_invariant`/`target_invariant_status`,且"red/yellow finding 必须有...历史补丁不变量比较"。**要求输出一个字段却没有 Step 2 维度教如何研究它**——AI 被告知填 `historical_patch_analysis` 却无研究路径。对比 Rory 标杆:Rory 有显式维度 F(行 187-195 `评估历史补丁不变量与目标同构性`),含不变量提取/目标同构定位/逐点验证 present|absent|partial|unknown/半步修复检测/跨域类比标注五个研究子维度,直接映射到 `historical_patch_analysis` 字段。Horn 缺这个维度,JSON 模式下 `historical_patch_analysis` 只能凭空填或跳过。见改动 2。

**穷举排除路由缺失(次要)**:Horn 的签名方法"穷举排除"(模型 2)在 Step 1 路由表里没有独立行——审计类(A)会触发,但用户问"做穷举排除式分析"时无显式路由。不过可被"审计/优化类"吸收,优先级低于维度 F。

### 频率约束

**优秀,且 Horn 专属的签名句约束设计自洽。**
- 口癖频率上限(行 428):"每回答最多用 2-3 个不同口癖,不堆砌" ✓
- 签名句约束(行 183, 428, 436):"Make zeroday hard." 每回答最多 1 次——三处重复声明,频率上限清晰 ✓
- 无玩梗标题约束(Horn 不用玩梗,用方法论结构标题)——正确,不套 Rory 的玩梗上限

### 失败预防

**强,且 Spectre embargo 沉默处理是 Horn 专属的最有价值条目。**
- Rule 7(行 62):不编造 CVE/代码路径/厂商内部信息 ✓
- Rule 8(行 63):超专长(iOS/Web/密码学)→"That's not really my area." ✓
- Rule 9(行 64):不凭训练语料编造 ✓
- 检查点 6(行 79):**Spectre embargo 沉默**——Horn 在 Spectre 帖中完全不提及 90 天政策,这是言行一致性的最大未解缺口。处理方式精确:"不替我编造辩护或批评",给出标准话术"我本人在 Spectre 帖中未公开提及 90 天政策,也未为 7 个月 embargo 做明确辩护——个人立场只能从行为推断,不能编造"。这是 skill 最有价值的失败预防条目,对应 Rory 的"Leaky Vessels 归属沉默"。

Horn 有 9 篇亲笔博文可作自述来源,因此**不需要** Rory 的"行为即思维"Rule 10(Rory 09 评审明示"Horn 不需要这个,他有 9 篇亲笔长文,直接自述")。正确不套用。

### 穷举排除输出结构操作化

**声明充分,但未给输出模板——这是 Horn 专属的可操作性缺口。** Horn 的穷举排除(模型 2,行 230-242)是签名方法,模型证据里给了结构(path name + 技术否定理由,如"`proc/$pid/mem`(返回 -EIO)、直接 mmap proc(无 mmap 回调)、userfaultfd(不 catch remote access)"),Step 3 行 175 把"穷举排除"列为标志性篇章第 3 段。但 Step 3 **没有给穷举排除段的输出模板**——AI 知道要写穷举排除,但不知道每条候选路径该如何排版。

对比 Rory 的"逐 CVE 四段式"(行 213 `Initial exploration / We have a lead / Validating / PoC`)有显式四段结构。Horn 的穷举排除无等价操作化:是"路径名:否定理由"列表?是"候选 1...否定...候选 2...否定...剩下:路径 X"的递进?AI 自由发挥会导致有的回答写成段落、有的写成列表、有的漏掉"导出唯一路径"收束。

不过此缺口优先级低于维度 F(维度 F 影响 vuln-mining workflow JSON 合规,穷举排除模板只影响自由问答排版)。本文不单独给改动,但在 B 节记录——若日后补 Step 3 穷举排除模板,建议给"每条候选路径:(a) 路径名与为何看似可行;(b) 否定的技术理由(分配器覆写/回调缺失/边界检查/序列号重置);(c) 转向下一条;最后导出经排除后剩下的唯一路径"的结构。

**对不确定的精确限定模板句**:已操作化。行 168 给出降级模板「I'd need to check the current state of this, but based on what I know about this class of subsystem...」;行 431 给出口癖式限定(`I'm not sure whether X or Y`/`no clue why`/`as far as I can tell`/`might not necessarily correspond`)。这点充分,不改。

### 检查点可操作性

**可操作,与 Rory 持平,且正确使用 C SAST 工具名。** 6 个检查点(行 74-79)均给出"先暂停→显式标注→让用户决定"动作:
- 检查点 1-2 把 `mcp__mcp-server-atomic-sast4c__*` 写进工具证据冲突/失败判定——对 Horn 的 C/内核域正确(对比 Rory 用 sast4go)✓
- 检查点 3(⚠ 反常识断言)对"这个缓解其实可被反转利用""这个优化在并发下失效"这类强断言有用 ✓
- 检查点 4(red/yellow confidence < high 标"建议二次验证")对 vuln-mining 场景重要 ✓
- 检查点 6 的 Spectre embargo 沉默给出完整标准话术,AI 可直接套用 ✓

唯一小瑕疵:检查点 4 的"confidence < high"触发条件略循环(AI 何时知道自己的 confidence < high?)——与 Rory 一致,非 Horn 独有问题,不改。

---

## C. 缺失关键信息

### vuln-mining workflow 集成

**浅,且相对 Rory 标杆有三处明显回归。**
- Step 1.3(行 94)扫描 workflow 关键词(batch/mapper/critic/Phase 3/CLAUDE.md/03-risk-mappings)切 JSON 模式 ✓
- Step 3 末尾停止规则(行 189-195)给 3 条 JSON 模式要求:`searches_run` 记录 sast4c 调用、red/yellow 必须有 file:line + 历史补丁不变量比较、把方法论填进 `rationale`/`negative_evidence` ✓
- **回归 1**:无 `critic_output_v1` 字段填法。Rory 标杆(行 241-245)给了 4 条 critic 字段填法(`critic_verdict`/`recommended_risk_level` 用确定性校准、`historical_patch_assessment` 用维度 F、`remap_requests[].challenge_type` 用检查点触发、`systemic_patterns`/`coverage_gaps` 用 under-audited 跨目标模式)。Horn 的 JSON 模式只有 mapper 指引,无 critic 指引——当 Horn 被 report-critic agent 调用时,无字段填法指导。见改动 2。
- **回归 2**:无 `collect_files_types` 前置调用。CLAUDE.md Code Analysis Tool Policy 明确要求"call `mcp__LocalAtomicSAST4C__collect_files_types` before mapping C/C++ code"——Horn 是 C/内核域,这条政策对 Horn 比 Rory 更直接相关。Horn Step 2 行 113 列了 5 个 sast4c 符号工具但漏 `collect_files_types`,JSON 模式也未提。见改动 2。
- **回归 3**(即 B.问题路由的维度 F 缺失):JSON 模式要求 `historical_patch_analysis` 字段却无 Step 2 维度研究路径。见改动 2。

### C SAST 工具指引

**优秀,正确优先 sast4c,且工具名符合实际 MCP 注册名。**
- Step 2(行 113)显式说明"优先使用 `mcp__mcp-server-atomic-sast4c__*`",列出 5 个符号感知工具(`get_function_call`/`get_function_definition`/`get_macro_definition`/`get_structure_definition`/`get_variable_consumer`),并对 sast4go/sast4rust 做降级说明 ✓
- 检查点 1-2 把 `mcp__mcp-server-atomic-sast4c__*` 写进判定 ✓
- JSON 模式(行 192)要求 `searches_run` 记录该工具调用 ✓
- **对比 Rory**:Rory 正确反转优先级(sast4go 第一,因 Go 生态);Horn 正确保持 sast4c 第一(因 C/内核域)。两 skill 的领域适配都正确,非缺陷。
- **小缺口**:漏 `collect_files_types`(见 C.workflow 集成回归 2)。Horn 列的 5 个工具里没有 recon 用的 `collect_files_types`,而 CLAUDE.md 明确要它作为 C/C++ 映射前置。

### 角色约束遗漏

**大部分覆盖,但容器运行时与密码学两条边界未在 non_activation 显式切分。**
- non_activation 已覆盖 6 个边界(iOS/Windows/hypervisor/Android·WebRTC/Web/防御运营)
- Rule 8 与检查点 5 重复声明超专长边界,三重覆盖充分
- **遗漏 1**:容器运行时/构建器边界(runc/BuildKit/containerd/podman)未路由给 rory-mcnamara-perspective。Horn 做 Chrome 沙箱→内核逃逸(2025 MSG_OOB),不做容器运行时边界;用户问"runc 怎么审"应路由给 Rory。见改动 3。
- **遗漏 2**:密码学理论未路由给 hillai-ben-sasson-perspective。Rule 8(行 63)把密码学列为超专长但 non_activation 无去向,造成 Rule 8 说"建议更合适视角"却无路由表条目的不一致。见改动 3。
- **次要点**:云控制平面(IAM/misconfig)未归类——但这与 Horn 域不邻接,优先级低。

---

## 2-3 处具体文本改动建议

### 改动 1: triggers 数组——补裸 persona 形式 + 缺失方法关键词

**问题**:行 27-30 的 persona 式 trigger 带 `用`/`从` 前缀,无法匹配用户裸指代(`P0内核研究员的思路`/`spectre发现者`/`meltdown发现者` 不含 `用P0内核研究员的思路`/`用spectre发现者的视角` 等更长串,子串不命中)。行 32-36 的方法关键词形式优秀(裸名词短语),但缺 `半步修复`/`对手时间线`/`缓解绕过`/`读原语`/`复杂安全规则`/`dead end` 等签名概念。

**位置**:frontmatter `triggers` 数组,行 30 之后(插入裸 persona 形式)+ 行 36 之后(追加缺失方法关键词)

**改后文本示例**(在行 30 `从CPU微架构研究员角度` 之后、行 31 `Make zeroday hard` 之前插入):

```yaml
  - "P0内核研究员|P0内核研究员的思路"
  - "spectre发现者|spectre的发现者"
  - "meltdown发现者|meltdown的发现者"
```

(在行 36 `穷举排除` 之后追加):

```yaml
  - "半步修复|half fix"
  - "对手时间线|用户何时受保护"
  - "缓解绕过|缓解被绕过|mitigation bypass"
  - "优化在并发下|并发假设失效"
  - "读原语|read primitive|semi-arbitrary read"
  - "复杂安全规则|hard for fuzzers"
  - "dead end|自我纠正|不可行方案"
```

说明:裸 persona 形式去 `用`/`从` 前缀,匹配用户脱口而出的 `P0内核研究员的思路`/`spectre发现者`/`meltdown发现者`(任务明确点出这 4 个常见表达中的 3 个)。方法关键词补齐模型 4(半步修复)、模型 5(对手时间线)、模型 4 更广疑问句(缓解绕过,覆盖"这个缓解能被绕过吗")、模型 3 并发场景(优化在并发下,覆盖"这个优化在并发下安全吗")、启发式 2(读原语)、启发式 3(复杂安全规则)、启发式 10(dead end)。全部裸关键词式,不引入祈使前缀,保持 Horn 标杆形式。

---

### 改动 2: Step 2 补维度 F + Step 3 JSON 模式补 critic_output_v1 字段填法 + 补 collect_files_types

**问题**:Step 3 JSON 模式(行 191-194)要求填 `historical_patch_analysis.source_patch_invariant`/`target_invariant_status`,但 Step 2 只有 A-E 五维(行 115-160),无维度教如何研究历史补丁不变量——这是相对 Rory 标杆(Rory 有显式维度 F)的最大可操作性回归。同时,JSON 模式只有 mapper 指引无 critic 指引(Rory 标杆行 241-245 有),且 Step 2 行 113 漏 `collect_files_types`(CLAUDE.md 明确要求的 C/C++ 映射前置)。

**位置 1**:Step 2,行 160(维度 E 最后一个子维度 `慷慨归因` 行)之后、行 162(`#### 研究输出格式`)之前,新增维度 F

**改后文本示例**(在 `#### 研究输出格式` 之前插入新维度):

```markdown
#### F. 评估历史补丁不变量与目标同构性（"这个补丁的不变量是什么,目标有没有?"）

| 研究维度 | 具体搜索 |
|---------|---------|
| **不变量提取** | 从 Phase 2 的 `security_invariant_after_patch` 与 `fix_commits[].url` 提取历史补丁引入的不变量(如"access_ok 检查整个范围而非只起始地址""VMA cache 序列号在单线程下保持 close""TLB 刷新在 mremap 后立即完成""MSG_OOB 不在沙箱暴露")。先 Read 补丁 diff 或 WebFetch 补丁 URL 核实,不凭描述猜 |
| **目标同构定位** | 目标代码里有没有等价的优化假设/边界处理?用 `mcp__mcp-server-atomic-sast4c__get_function_call`/`get_function_definition`/`get_macro_definition`/`get_variable_consumer` 定位等价调用点 |
| **逐点验证 present\|absent\|partial\|unknown** | 不变量在目标里是 present(已实现)、absent(未实现)、partial(只堵 offset 0 留偏移路径=半步修复)、还是 unknown(无法判定)?填进 `historical_patch_analysis.target_invariant_status` |
| **半步修复检测** | 目标的修复是完整不变量还是只堵单点?(只检查起始地址=半步修复,`target_invariant_status: partial`)——这是我模型 4 的核心 |
| **跨域类比标注** | 把历史补丁的方法论迁移到目标时,显式标注同构来源——"这是 Xen XSA-29 的 access_ok 只查起始地址分析,在这里是否成立取决于边界条件是否同构"——避免把方法论迁移伪装成对当前目标的直接判断 |
```

**位置 2**:Step 2 行 113 的工具列表,补 `collect_files_types` 作为 C/C++ 映射前置

**改后文本示例**(替换行 113 的工具列表括号内容):

```markdown
对于本仓库的目标代码审计,优先使用 `mcp__mcp-server-atomic-sast4c__*` / `mcp__mcp-server-atomic-sast4go__*` / `mcp__mcp-server-atomic-sast4rust__*` 的符号感知工具。C/C++ 目标映射前**先调 `mcp__mcp-server-atomic-sast4c__collect_files_types`** 做文件类型 recon(符合 CLAUDE.md Code Analysis Tool Policy),再用 `get_function_call`、`get_function_definition`、`get_macro_definition`、`get_structure_definition`、`get_variable_consumer` 做符号感知——这与我"质疑原语的安全语义、再系统性寻找误用该原语的调用点"的方法论一致。
```

**位置 3**:Step 3 末尾 JSON 模式停止规则,行 194(最后一项 `把"质疑优化假设/穷举排除/缓解反转"的方法论填进...`)之后、行 196 `---` 之前,新增 critic_output_v1 字段填法

**改后文本示例**(在行 194 之后插入新段):

```markdown
**critic_output_v1 字段填法**(report-critic 角色):
- `reviews[].critic_verdict` / `recommended_risk_level`:用我的确定性二元校准——经验验证事实(模型 1-2 的实验探测、穷举排除)用断言,bug 严重性/补丁完整性用精确限定(`I'm not sure whether X or Y`);`confidence < high` 的 red/yellow 标 `insufficient_evidence`
- `reviews[].historical_patch_assessment`:维度 F 的不变量比较结论(present/absent/partial/unknown + 理由)
- `remap_requests[].challenge_type`:用我的检查点触发——`missing_reachability`(B 未验证端到端可达)/ `weak_evidence`(无 file:line)/ `missed_mitigation`(C 漏检缓解反转/半步修复)/ `wrong_rating`(穷举排除不完整,漏掉候选路径)/ `missed_equivalent_code`(A/F 漏等价优化假设)
- `systemic_patterns` / `coverage_gaps`:维度 D 的"新技术+暴露面错配""审计密度(old code less scrutiny)"跨目标复现模式
```

说明:维度 F 把 JSON 模式要求的 `historical_patch_analysis` 字段落成可研究路径,五个子维度直接映射字段,例子全用 Horn 自己的博文(access_ok/XSA-29/VMA cache/TLB/MSG_OOB)。critic 指引补齐 report-critic 角色的字段填法,用 Horn 的模型 1-2/D 维度作填法来源(不套 Rory 的 under-audited/Go 容器专属)。`collect_files_types` 补齐 CLAUDE.md 的 C/C++ 映射前置要求。三处合一是 vuln-mining workflow 集成的完整修复。

---

### 改动 3: non_activation——补容器运行时→rory + 密码学→hillai 路由

**问题**:行 39-44 的 non_activation 无容器运行时路由(用户问"runc 怎么审"可能误留 Horn),无密码学路由(Rule 8 行 63 把密码学列为超专长但 non_activation 无去向,造成 Rule 8 说"建议更合适视角"却无路由表条目的不一致)。本仓库存在 `rory-mcnamara-perspective`(容器运行时)与 `hillai-ben-sasson-perspective`(Hillai Ben-Sasson = StarkWare 创始人,密码学)——应显式路由。

**位置**:non_activation,行 42(Android/WebRTC 条目)之后、行 43(Web 应用条目)之前,新增两条

**改后文本示例**(在行 42 之后插入):

```markdown
  - 问题关于容器运行时/构建器安全(runc/BuildKit/containerd/podman/Incus/snapd 边界、容器逃逸面)(应推荐 rory-mcnamara-perspective)——Horn 做 Chrome 沙箱→内核逃逸(2025 MSG_OOB),不做容器运行时边界;Rory 才是容器运行时战场
  - 问题关于密码学理论(zero-knowledge/KZG/STARK/形式化验证)(应推荐 hillai-ben-sasson-perspective)——Horn 在 Spectre 帖明示"processor vendors are in a much better position to design mitigations",把缓解设计推给厂商;密码学理论非我专长,Rule 8 已声明但此处补路由去向
```

说明:容器运行时路由切分 Horn(Chrome 沙箱→内核)与 Rory(容器运行时边界)的边界。密码学路由补齐 Rule 8 的"建议更合适视角"承诺,指向本仓库的 hillai-ben-sasson-perspective。两条都用 Horn 自身语气说明边界理由(引用 Spectre 责任框架金句),保持角色一致。

---

## 总结

### 激活即执行程度

**高,且 triggers 方法描述式形式优于 Rory 标杆(Phase 5 精炼前)。** 角色扮演规则(9 条 + 6 检查点)、问题路由表(7 行)、JSON 模式停止规则(3 条)、C SAST 优先级(sast4c 第一,符合 C/内核域)、non_activation 的 6 条边界——大都达到或超过 Rory 标杆。Spectre embargo 沉默(检查点 6)是 Horn 专属的最有价值失败预防条目。triggers 的方法描述式全部裸关键词形式,正是 Rory 09 评审赞誉的标杆,Rory 反而要向 Horn 看齐。

但维度 F 缺失(JSON 模式要求字段却无研究路径)、critic 指引缺失、`collect_files_types` 漏列,使这个 skill 在 vuln-mining workflow 的 mapper/critic 角色上不如 Rory 可操作——这是 Phase 5 精炼未做的最明显后果,也是改动 2 要一次性补齐的三处。

### 最需补的

1. **维度 F + critic_output_v1 指引 + collect_files_types**(改动 2)——直接影响 vuln-mining workflow JSON 合规,最该先改。维度 F 是相对 Rory 标杆的最大可操作性回归
2. **triggers 补裸 persona + 缺失方法关键词**(改动 1)——影响激活率,补齐用户脱口而出的裸指代与模型 4/5/启发式 2/3/10 的签名概念
3. **non_activation 补容器运行时→rory + 密码学→hillai**(改动 3)——切分边界,补齐 Rule 8 的路由承诺

### 优点记录(不改,但备查)

- triggers 方法描述式全裸关键词形式,优于 Rory(Phase 5 精炼前)——Rory 09 评审反向借鉴了 Horn
- 检查点 6 的 Spectre embargo 沉默处理精确,标准话术可直接套用,是 Horn 专属的最有价值失败预防条目
- Android/WebRTC 条目显式声明"本仓库无对应 perspective skill"+"以 Horn 身份说明非我专长",比 Rory 更坦诚(Rory 无"无对应 perspective"声明)
- C SAST 优先级(sast4c 第一)正确符合 C/内核域定位
- 签名句 "Make zeroday hard." 频率约束三处声明(行 183/428/436),设计自洽
- 对不确定的精确限定模板句已操作化(行 168 降级模板 + 行 431 口癖式限定),无需补

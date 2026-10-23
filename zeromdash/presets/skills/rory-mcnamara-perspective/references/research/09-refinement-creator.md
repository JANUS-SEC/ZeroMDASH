# Rory Skill — skill-creator 评审

评审基准:实际读取 `rory-mcnamara-perspective/SKILL.md`(617 行)并与标杆 `jann-horn-perspective/SKILL.md`(605 行)逐节对比。以下评价基于文本证据,非印象。

---

## A. 激活触发条件

### 覆盖度评价

**点名式覆盖:优秀。** triggers 行 20-32 覆盖中英文点名变体(`用Rory McNamara的视角`/`rory mcnamara perspective`/`rory's take`/`what would rory think`/`ask rory`/`切换到Rory`/`切换到McNamara`/`用Snyk Labs容器研究员的思路`/`用Leaky Vessels发现者的视角`)。description 行 11-13 的散文也对"切换到 Rory""Snyk Labs 容器研究员的视角"做了二次覆盖。与 jann-horn 点名式覆盖度持平。

**方法描述式覆盖:中等偏上,但有形式缺陷。** description 行 14-17 列出 8 个签名方法(race/TOCTOU、边界不变量、容器逃逸面、strace、fd-vs-path、features-as-expected、under-audited、Leaky Vessels),散文覆盖到位。但 `triggers` 数组(实际机械匹配机制)中,方法描述条目混用了**祈使/后缀式**与裸关键词式:
- 行 33 `"找race condition|找TOCTOU"`、行 34 `"找边界不变量违反"`、行 35 `"评估容器逃逸面"`、行 36 `"strace驱动审计"` —— 带 `找`/`评估`/`驱动` 前缀
- 行 41 `"process.cwd逃逸"`、行 42 `"entitlements校验"`、行 43 `"mount cleanup竞争"` —— 带 `逃逸`/`校验`/`竞争` 后缀
- 行 37-40 才是裸关键词(`fd-based vs path-based`/`按预期工作的特性`/`under-audited低层组件`/`Leaky Vessels`)

**对比 jann-horn(行 32-36)**:`优化假设失效`/`缓解反转|缓解被反转利用`/`暴露面错配`/`impact-gating|未证明impact的bug`/`穷举排除` —— 全部纯裸关键词名词短语,无祈使前缀。jann-horn 的形式能自然匹配"这个有暴露面错配吗"这类疑问句;Rory 的 `找race condition` **无法匹配**"这个有 race condition 吗""这里是不是 TOCTOU""这个容器运行时有竞态吗"——因为缺 `找` 前缀就不命中。这是相对标杆的回归。

### 遗漏的常见表达

- **疑问句式**:用户问"这个容器运行时有竞态吗""这个 path 校验够不够""这里有 TOCTOU 吗""这个 mount 安全吗"——`找`/`评估` 前缀的 trigger 不命中
- **裸关键词"竞态"**:triggers 里只有 `找race condition|找TOCTOU`,没有中文裸词 `竞态`;讲中文的用户最常说"有竞态"
- **"path 校验/路径校验"**:完全无对应 trigger,但这是 B 维度(文件操作/路径类)最高频的用户提问
- **"Snyk 容器"**:只有祈使式 `用Snyk Labs容器研究员的思路`;用户说"Snyk 那帮人怎么挖容器洞""Snyk Labs 那个容器研究员"不命中
- **"fd 泄漏/fd leak"**:只有 `fd-based vs path-based`;CVE-2024-21626 attack 1 的核心是 fd 泄漏,用户常直接说"fd 泄漏"
- **"半步修复/half fix"**:D 维度核心概念,无 trigger
- **组件名单独出现**:`runc`/`BuildKit`/`containerd`/`podman`/`Incus`/`snapd` 单独出现不触发——但用户常问"runc 这种怎么审";description 行 13 提到"切换到 Rory"但组件名本身不是 trigger

### non_activation 路由准确性

**优秀,且比 jann-horn 更细。** 行 46-52 共 7 条,覆盖 CPU 微架构(→jann-horn)、iOS/macOS 内核(→ian-beer)、Windows/AV(→tavis)、hypervisor 侧(→felix/thomas)、纯云控制平面(Wiz/Aqua,显式说明"Rory 不做控制平面")、Web 应用(SSRF to IMDS 的"相邻但非主线"边界很精确)、纯防御运营(SOC/合规)。比 jann-horn 的 6 条多了"云控制平面"和"防御运营"两条,且 SSRF-to-IMDS 的邻接边界描述是 jann-horn 没有的精细度。

**一个路由缺口**:行 46 只把"CPU 微架构侧信道 / transient execution"路由给 jann-horn,但 **Linux 内核内存管理 / 调度器 / syscall 内部实现**(jann-horn 的核心战场)未路由。Rory 的方向是"Linux userland privesc"(行 221,身份卡自述),即 DBus/Polkit/AppArmor/wpa_supplicant 等**用户态守护进程**边界——不审计内核内部实现。用户问"这个 Linux 内核内存管理代码有 bug 吗"可能错误激活 Rory。见改动 3。

---

## B. 角色扮演规则可操作性

### 问题路由

**清晰且比 jann-horn 多一行。** Step 1 表格(行 107-116)7 行,比 jann-horn 多"文件操作/路径类 → 维度 B"独立一行——这是 Rory 的核心维度(fd-vs-path),独立路由合理。模糊时降级(行 118)默认取 A+C(审计+可达性双线)与 jann-horn 的 A+B 等价,覆盖面逻辑一致。Step 1.1(行 101)要求含具体指代时必须先调工具,Step 1.2 披露策略类走 Step 2.E 查案例事实,Step 1.3 vuln-mining workflow 切 JSON 模式——三段扫描完整。

### 频率约束

**优秀,且比 jann-horn 更全。**
- 口癖频率上限(行 437):"每回答最多用 2-3 个不同口癖,不堆砌"——与 jann-horn 一致
- 玩梗章节标题(行 419, 437):"每篇最多 4-5 个"——这是 Rory 专属的频率约束(jann-horn 无此条,因为 jann-horn 无玩梗标题),且行 419 末尾"避免模仿秀"点出过度模仿风险
- 签名句约束:Rory 无 Horn 式签名句(行 444 明确"无 Horn 式格言签名句"),因此无需"每回答最多 1 次"约束——设计自洽

### 失败预防

**强,且针对 Rory 的特有归因风险做了专门处理。**
- Rule 7(行 70):不编造 CVE/advisory/补丁 SHA/内部协调私信 ✓
- Rule 8(行 71):超专长(CPU/iOS/Web/云控制平面)→ "That's not really my area." ✓
- Rule 9(行 72):不凭训练语料编造 ✓
- Rule 10(行 73):行为即思维原则 ✓
- 检查点 6(行 88):**"Leaky Vessels" 归属沉默**——这是 Rory 专属的归因风险(GHSA credit 是 attack 1 reporter,但 oss-security 由 Sarai 署名,Snyk 站点无 writeup),对应 jann-horn 的"Spectre embargo 沉默"。处理方式精确:"不替我编造命名内情",并给出标准话术"我在 GHSA credit 是 attack 1 的 credited reporter;公开叙事主笔是 runc 维护者 Aleksa Sarai;'Leaky Vessels' 品牌名的命名者我未公开声明过——只能从行为推断"。这是 skill 最有价值的失败预防条目之一。

### "行为即思维"体现度

**声明充分,但未操作化到 Step 3 输出规则——这是可操作性的最大缺口。**
- Rule 10(行 73)声明原则 ✓
- 诚实边界(行 547)再次声明 ✓
- 模型 7 局限(行 336)承认这是行为推断 ✓
- **但 Step 3(行 183-208)的输出指引没有告诉 AI 如何把"我这样想"落成行为锚定的措辞**。Step 3 只列了标志性篇章结构(背景/边界/工具/逐 CVE/gadget/Timeline/Mitigations/致谢/玩梗)和跨域类比显式标注(行 199),却没有一条输出规则说"当你要表达'我认为 X'时,必须重写成'我做了 Y(发现选择/披露通道/技术定位),因此可推断我这样想 X',且不伪装成我的口头自述"。
- 这对 Rory 比对 jann-horn 更关键:jann-horn 有 9 篇亲笔博文可作自述来源,Rory 的口头/书面自述近乎空集(行 546-547,诚实边界明示)。原则在最需要操作化的角色上反而只声明不落地。见改动 2。

### 检查点可操作性

**可操作,与 jann-horn 持平。** 6 个检查点(行 79-90)均给出"先暂停→显式标注→让用户决定"的具体动作,且:
- 检查点 1-2 把 `mcp__mcp-server-atomic-sast4go__*` 写进工具证据冲突/失败的判定条件——这对 Go 生态目标正确
- 检查点 4(red/yellow confidence < high 标"建议二次验证")对 vuln-mining 场景尤其重要,行 86 明确"避免把框架外推伪装成代码证据"
- 检查点 6 的 Leaky Vessels 归属沉默给出了完整标准话术,AI 可直接套用

唯一小瑕疵:检查点 4 的触发条件"confidence < high"略循环(AI 何时知道自己的 confidence < high?)——但这与 jann-horn 一致,非 Rory 独有问题,不改。

---

## C. 缺失关键信息

### vuln-mining workflow 集成

**优秀,且比 jann-horn 多一条 disclosure 专属指引。**
- Step 1.3(行 103)扫描 workflow 关键词(batch/mapper/critic/Phase 3/CLAUDE.md/03-risk-mappings)切 JSON 模式 ✓
- Step 3 末尾停止规则(行 201-208)给出 4 条 JSON 模式要求,第 4 条"把'补丁同日发检测器 / 协调式合并披露'填进 `mitigations` 与 `historical_patch_analysis`"是 jann-horn 没有的——把 Rory 的披露哲学(模型 6)直接映射进 schema 字段,设计精到
- 行 204 要求 `searches_run` 记录 `mcp__mcp-server-atomic-sast4go__*` 调用,符合 CLAUDE.md 的 Code Analysis Tool Policy

### Go SAST 工具指引

**优秀,正确优先 sast4go,且强于 jann-horn 的泛化写法。**
- Step 2(行 123)显式说明"研究目标几乎全是 Go 生态(runc/BuildKit/containerd/podman/Incus/snapd 都是 Go),**优先使用 `mcp__mcp-server-atomic-sast4go__*`**",列出 7 个符号感知工具(`get_function_call`/`get_function_definition`/`get_method_definition`/`get_struct_definition`/`get_type_definition`/`get_interface_definition`/`grep_code`),并对 C/C++ → sast4c、Rust → sast4rust 做了降级说明 ✓
- 检查点 1-2(行 83-84)把 `mcp__mcp-server-atomic-sast4go__*` 写进工具证据冲突/失败的判定 ✓
- JSON 模式(行 204)要求 `searches_run` 记录该工具调用 ✓
- **对比 jann-horn(行 113)**:jann-horn 把 sast4c 列第一、sast4go/sast4rust 列第二(因为 Horn 的目标是内核 C 代码)。Rory 正确地反转了优先级(sast4go 第一),符合其 Go 生态定位。这是正确的领域适配,非缺陷。

### 角色约束遗漏

**大部分覆盖,但 Linux 内核边界与 jann-horn 的分野不 crisp。**
- non_activation 已覆盖 7 个边界(CPU/iOS/Windows/hypervisor/云控制平面/Web/防御运营)
- Rule 8 与检查点 5 重复声明超专长边界,三重覆盖充分
- **遗漏**:Rory 做"Linux userland privesc"(身份卡行 221),与 jann-horn 的"Linux 内核内存管理/调度器/syscall 内部"边界未在 non_activation 显式切分。用户问"这个 Linux 内核 syscall 有没有 bug"可能错误留在 Rory——Rory 审的是与内核交互的 userland 守护进程(DBus/Polkit),不是内核内部。见改动 3。
- 次要遗漏:Kubernetes operator/controller 安全、供应链/SBOM——这些介于"云控制平面"与"容器运行时"之间,non_activation 未显式归类。但可被"纯云控制平面"条目吸收,优先级低于内核边界问题。

---

## 2-3 处具体文本改动建议

### 改动 1: triggers 数组——把祈使/后缀式改为裸关键词式,并补常见疑问句表达(对标 jann-horn 的裸关键词形式)

**问题**:行 33-36、41-43 的方法描述 trigger 带祈使前缀(`找X`/`评估Y`/`strace驱动审计`)或后缀(`X逃逸`/`X校验`/`X竞争`),无法匹配疑问句式用户输入("这个有竞态吗""这个 path 校验够不够")。jann-horn 用纯裸关键词名词短语(`优化假设失效`/`暴露面错配`),能自然匹配疑问句。Rory 相对标杆回归。

**位置**:frontmatter `triggers` 数组,行 33-43 的方法描述段

**改后文本示例**(直接替换行 33-43):

```yaml
  - "race condition|竞态|TOCTOU"
  - "边界不变量违反|不变量违反"
  - "容器逃逸|container escape|逃逸面"
  - "strace"
  - "fd-based|path-based|fd泄漏|fd leak"
  - "按预期工作的特性|features that work as expected"
  - "under-audited|低层组件"
  - "Leaky Vessels"
  - "process.cwd|cwd逃逸|cwd落点"
  - "entitlements|entitlements校验"
  - "mount cleanup|mount清理|cleanup竞争"
  - "path校验|路径校验"
  - "半步修复|half fix"
  - "Snyk容器|Snyk Labs容器"
```

说明:全部改为裸关键词(去 `找`/`评估`/`驱动` 前缀),新增中文裸词 `竞态`、新增 `path校验|路径校验`(覆盖 B 维度最高频提问)、`半步修复`(D 维度核心概念)、`Snyk容器`(覆盖"Snyk 那帮人怎么挖容器洞"的口语表达)。保留行 37-40 原裸关键词条目。

---

### 改动 2: Step 3 输出规则——把"行为即思维"从声明操作化为可执行措辞规则

**问题**:Rule 10(行 73)声明了"行为即思维"原则,诚实边界(行 547)与模型 7 局限(行 336)也重复声明,但 Step 3(行 183-208)的输出指引**没有任何一条规则告诉 AI 如何把"我这样想"落成行为锚定的措辞**。Rory 的口头/书面自述近乎空集(诚实边界行 546-547 明示"均未核实到一手来源""社交媒体样本极小"),这使得"行为即思维"对 Rory 比对 jann-horn(有 9 篇亲笔博文)更关键——但恰好在最该操作化的角色上只声明不落地。AI 容易写成"我一直认为 path-based 不安全"这种伪装成口头自述的表述。

**位置**:Step 3 末尾,行 199(跨域类比显式标注段)之后、行 201(输出模式停止规则)之前,新增一段

**改后文本示例**(直接在行 199 之后插入新段):

```markdown
**行为即思维输出规则**(对应 Rule 10):由于我的公开自述近乎空集(无播客、无会议演讲、无作者聚合页互动),任何「我会这样想」「我的看法是」「我一直认为 X」的表述都要落在具体行为上——「我做了 Y(发现选择 / 披露通道 / 技术定位),因此可推断我这样想」。例如:不说「我认为 path-based 操作不安全」,而说「我在 Safe Path Handling 整篇推动 fd-based,由此可推断我默认 path-based 不安全」;不说「我主张留部署窗口」,而说「我在 Istio CVE-2024-23326 留了 16 天窗口,由此可推断我倾向保守协调」。**不**伪装成我的口头自述(「我一直这么说」「我多次强调」「我在 X 时说过」)——我的口头自述样本近乎空集,任何引用我的原话都要有附录来源佐证,或显式标注为行为推断。跨域类比(下行)是这一规则的延伸:把方法论迁移显式标注同构来源,而非伪装成对当前目标的直接判断。
```

---

### 改动 3: non_activation——补 Linux 内核内部实现路由给 jann-horn,切分 userland privesc 边界

**问题**:行 46 只把"CPU 微架构侧信道 / transient execution"路由给 jann-horn,但 jann-horn 的另一核心战场"Linux 内核内存管理 / 调度器 / syscall 内部实现"未路由。Rory 的方向是"Linux userland privesc"(身份卡行 221)——DBus/Polkit/AppArmor/wpa_supplicant 等**用户态守护进程**边界,不审计内核内部。用户问"这个 Linux 内核 syscall 实现有问题吗""这个内核内存管理代码有 bug 吗"可能错误激活 Rory。non_activation 需要显式切分这条边界。

**位置**:non_activation,行 46 之后新增一条(置于 CPU 微架构条目与 iOS 条目之间,保持"底层边界"归类连续)

**改后文本示例**(在行 46 之后、行 47 之前插入新条目):

```markdown
  - 问题关于 Linux 内核内存管理 / 调度器 / page table / syscall 内部实现(应推荐 jann-horn-perspective)——Rory 做 Linux userland privesc(DBus / Polkit / AppArmor / wpa_supplicant 等用户态守护进程边界),不审计内核内部实现;与内核边界交互的 userland 守护进程是我的战场,内核内部不是
```

---

## 总结

### 激活即执行程度

**高,但 triggers 形式是执行链路的最弱一环。** 角色扮演规则(10 条 + 6 检查点)、问题路由表(7 行)、JSON 模式停止规则(4 条)、Go SAST 优先级、non_activation 的 7 条边界——这些都达到或超过 jann-horn 标杆,且针对 Rory 的特有归因风险(Leaky Vessels 命名归属、行为即思维、Go 生态)做了 jann-horn 没有的专门处理。Step 1.3 与 Step 3 末尾的 workflow 集成让这个 skill 可直接被 vuln-mapper/report-critic agent 调用并产出合规 JSON。

但 triggers 数组的方法描述条目用了祈使/后缀式(相对 jann-horn 的裸关键词式是回归),会漏掉疑问句式的真实用户输入——这是"激活"环节最该修的一处。

### 最需补的

1. **triggers 改裸关键词式**(改动 1)——直接影响激活率,最该先改
2. **Step 3 行为即思维输出规则**(改动 2)——Rory 的自述近乎空集,这条原则只声明不落地会导致 AI 伪装口头自述,是角色保真度的最大隐患
3. **non_activation 补 Linux 内核内部路由**(改动 3)——切分 userland privesc 与 kernel internals 边界,避免内核问题误激活 Rory

### 优点记录(不改,但备查)

- non_activation 的 SSRF-to-IMDS"相邻但非主线"边界描述比 jann-horn 更精细
- 检查点 6 的 Leaky Vessels 归属沉默处理精确,标准话术可直接套用
- Step 3 末尾 JSON 模式第 4 条把披露哲学映射进 `mitigations`/`historical_patch_analysis`,是 jann-horn 没有的设计
- Go SAST 优先级反转(sast4go 第一)正确符合 Go 生态定位
- 玩梗章节标题频率上限(4-5 个/篇)是 Rory 专属且 jann-horn 无对应的设计

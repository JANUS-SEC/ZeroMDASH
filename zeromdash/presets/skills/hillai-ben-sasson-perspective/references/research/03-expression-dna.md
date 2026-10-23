# Hillai Ben-Sasson — 表达 DNA

> **来源透明度声明**
> 本文基于 Hillai Ben-Sasson 在 Wiz 博客上署名的 5 篇文章进行风格提取。其中 **2 篇为他独立署名**（SAPwned 2024-07、BingBang 技术深版 2023-03），是提取他**纯个人风格**的金矿；2 篇为他作为 lead/co-lead 联署（38TB Microsoft AI 数据泄露 2023-09 与 Ronny Greenberg 合著、BingBang 高阶版 2023-03 与 Raaz Herzberg + Shir Tamari 合著），可信度中等；1 篇为多人联署（IngressNightmare 2025-03，与 Nir Ohfeld、Ronen Shustin、Sagi Tzadik 合著），仅可作 Wiz 宅风格基线，难分离个人特征。NVIDIAScape 与 CodeBreach 两文虽在 "Stay in touch!" 段落把他列为团队成员，但他**不是 lead author**，对个人风格提取无价值。
>
> **未拿到的来源（诚实标注）**：
> - **X/Twitter**：handle 已确认 `@hillai`（Wiz 博客 "Stay in touch!" 段落列出），但 WebFetch 直接访问 `x.com/hillai` 返回 **HTTP 402 Payment Required**（付费墙，与调研 Nir `@nirohfeld` 时遇到的同一现象）。未能提取任何原推文。**这是最大盲点**——他在 X 上的口语化表达、对云/AI 厂商的即兴评论、与同行的公开互动，全部缺失。
> - **LinkedIn**：`linkedin.com/in/hillai-ben-sasson` 返回 **HTTP 999**（反爬），未能提取任何 posts / activity。
> - **Black Hat US/EU 2024 briefing schedule 页**：返回 **HTTP 403**。SAPwned 文章明确提到他在 Black Hat 2024 有一场名为 **"Isolation or Hallucination? Hacking AI Infrastructure Providers for Fun and Weights"** 的演讲（"for fun and weights" 是他本人创的 pun，呼应经典黑客文化 "for fun and profit"），但**未能拿到 abstract 原文**，仅有博客内嵌提及。
> - **KubeCon / RSA / DEF CON 演讲者页**：未能在公开抓取范围内确认独立 speaker page（与 Nir 有 `kccncna2025.sched.com/speaker/niro@wiz.io` 不同，Hillai 的 sched.com 句柄未在搜索引擎索引中确认）。
> - 因此**演讲 delivery 风格（开场/过渡/收尾的口头节奏）本节缺失**，下文以"写作 delivery"代替。
>
> **WebSearch 幻觉警告**：调研过程中两次 WebSearch 调用返回了**幻觉内容**：
> 1. 一次声称 Hillai 是 **"Aqua Security"** 研究员——错误，他是 **Wiz** 雇员（Wiz 博客作者页权威确认）。
> 2. 一次把他与 **StarkWare** 密码学家 Eli Ben-Sasson 混淆，声称他研究 STARK/零知识证明——**这是同名/同姓不同人**。StarkWare 的 Ben-Sasson 是密码学学术派，与本调研对象（Wiz 云安全研究员）完全无关。
> 这两条幻觉**未采信**。
>
> **可信度分级**：`高`（一手 Wiz 博客**独立署名**文章原文 verbatim）/ `中`（一手 Wiz 博客 **lead 联署**文章，受合著稀释）/ `低`（多人联署或仅作 Wiz 宅风格基线，不能分离个人风格）。
>
> **联署文章的局限（重点标注）**：Wiz 博客几乎所有研究都是团队成果，即便独立署名文章的 "Stay in touch!" 段落也会列出 4-5 位团队成员的 X handle 与邮箱。这意味着 (a) 文章正文虽署一人名，仍可能经过 Wiz 内容审查与同事 review；(b) 文风受 Wiz 宅风格纪律约束（短-长节奏、品牌化命名、we-voice、收尾格言）。下文所有"个人特征"判断，**严格意义上都是 "Hillai 主笔特征 + Wiz 宅风格" 的合成**，无法从外部精确分离。SAPwned 与 BingBang 技术深版两篇独立署名文章是**最接近个人风格**的样本，但仍受此局限。

---

## 一手来源总览

| 来源类型 | 具体平台 / URL | 时间 | 在文风提取中的角色 | 可信度 |
|---------|---------------|------|-------------------|--------|
| Wiz 博客**独立署名** SAPwned | https://www.wiz.io/blog/sapwned-sap-ai-vulnerabilities-ai-security | 2024-07-17 | **主样本**：纯个人风格金矿 | 高 |
| Wiz 博客**独立署名** BingBang 技术深版 | https://www.wiz.io/blog/azure-active-directory-bing-misconfiguration | 2023-03-29 | **主样本**：纯个人风格金矿 | 高 |
| Wiz 博客 lead 联署 BingBang 高阶版 | https://www.wiz.io/blog/bingbang | 2023-03-29 | 次样本（与 Raaz Herzberg、Shir Tamari 合著） | 中 |
| Wiz 博客 lead 联署 38TB Microsoft AI | https://www.wiz.io/blog/38-terabytes-of-private-data-accidentally-exposed-by-microsoft-ai-researchers | 2023-09-18 | 次样本（与 Ronny Greenberg 合著） | 中 |
| Wiz 博客多人联署 IngressNightmare | https://www.wiz.io/blog/ingress-nginx-kubernetes-vulnerabilities | 2025-03-24 | 仅 Wiz 宅风格基线（与 Nir、Ronen、Sagi 合著） | 低 |
| NVIDIAScape | https://www.wiz.io/blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape | 2025 | **仅"Stay in touch!"团队署名**，非 lead——**不采信为个人样本** | 不适用 |
| CodeBreach | https://www.wiz.io/blog/wiz-research-codebreach-vulnerability-aws-codebuild | 2025 | **仅"Stay in touch!"团队署名**，非 lead——**不采信为个人样本** | 不适用 |
| X / Twitter `@hillai` | https://x.com/hillai | 现状 | **402 付费墙，未提取** | 低（仅确认 handle） |
| LinkedIn | linkedin.com/in/hillai-ben-sasson | 现状 | **HTTP 999，未提取** | 低 |
| Black Hat 2024 briefing schedule | blackhat.com/us-24/briefings/schedule | 2024 | **403，未拿到 abstract**；仅 SAPwned 文中提及 talk 标题 | 低 |

---

## 1. 句式偏好

**总体特征：定义式开头 + 括号旁白（最关键指纹）+ 形容词绝对化收束。与 Nir "短促断言独立成段"不同，Hillai 不靠单句成段制造戏剧，而靠括号内嵌自嘲。**

### 1.1 括号内嵌式自嘲/惊叹 —— Hillai 的最强指纹

Hillai 把"作者本人的即兴反应"塞进括号里，这是 Nir 完全不用的手法。两条独立署名文章各出现至少一次：

**一手引用（高可信度，SAPwned 独立署名）**：
- "all other UIDs were allowed – including Istio's UID, which **ironically enough was '1337' (yeah, really)**"
  （来源：https://www.wiz.io/blog/sapwned-sap-ai-vulnerabilities-ai-security）

**一手引用（高可信度，BingBang 技术深版独立署名）**：
- "A file management system, managing over **4 exabytes (!)** of Microsoft's internal files."
  （来源：https://www.wiz.io/blog/azure-active-directory-bing-misconfiguration）

**模式**：括号里要么是 "(yeah, really)" 这种**自我确认的口语化惊叹**，要么是 "(!)" 这种**最简化的情绪标记**。Nir 的 DNA 文件里**完全没有**这种括号旁白手法——Nir 把惊叹压成 "To our surprise, it worked!" 这种独立陈述句。Hillai 反而把惊叹压进括号里，让句子结构保持正式，情绪泄在夹层。

### 1.2 定义式 / 教科书式开头

Hillai 不像 Nir 用戏剧化短句开头，他用**定义/分类陈述**开篇，先把对象说清楚：

**一手引用（高可信度，SAPwned 独立署名）**：
- "SAP AI Core is a service that allows users to develop, train and run AI services in a scalable and managed way, utilizing SAP's vast cloud resources."
  （来源：SAPwned）

这是百科式开头——主语是服务名，谓语是 "is a service that..."，几乎像维基条目。Nir 的 ChaosDB / ExtraReplica 开头是 "we discovered..." 直接进叙事。**这是两人最显著的句式分野**：Hillai 倾向**定义先行**，Nir 倾向**发现先行**。

### 1.3 "we" 全程在场，"I" 完全缺席 —— 与 Nir 同构

两篇独立署名文章正文中**搜不到任何 "I" 第一人称单数**，全部用 "we"。即便 BingBang 技术深版署名仅 Hillai 一人，"Stay in touch!" 段落仍列出 5 位团队成员。这与 Nir 的 DNA 文件观察完全一致——**Wiz 宅风格纪律**，把发现归功于团队，弱化个人英雄色彩。

**一手引用（高可信度）**：
- "we on the Wiz Research Team have conducted extensive tenant isolation research on multiple AI service providers" —— SAPwned
- "we then proceeded to change the first item, '_Dune (2021)_' to **our personal favorite**, '_Hackers (1995)_'" —— BingBang 技术深版（注意 "our personal favorite" 也是复数）
- "The results **surprised us**: 25% of all the multi-tenant apps we scanned were vulnerable" —— BingBang 技术深版

> **不确定性**：无法确认 (a) Wiz 品牌纪律强制 we-voice，还是 (b) Hillai 个人偏好。Nir 的 DNA 文件中已观察到同样现象并同样无法分离。鉴于两人都遵守，更可能是 (a)。

### 1.4 反问句作为**章节标题**（不是过渡）

Nir 用反问句做段落过渡（"So what privileges _do_ we have?"），Hillai 把反问句升格为**章节标题**——更结构化、更少叙事流动感：

**一手引用（高可信度，SAPwned 独立署名）**：
- 章节标题 "Does AI have an isolation problem?"
  （来源：SAPwned）

正文里几乎不用反问句过渡。**这是与 Nir 的关键差异**：Hillai 把悬念留在标题层，正文是陈述式 walkthrough；Nir 把悬念撒进正文每段过渡。

### 1.5 编号式 Bug 列举 + 升级式叙事

SAPwned 的章节结构是 "Bug #1 → Bug #2 → Bug #3 → Bug #4 → Bug #5"，每个 bug 在前一个基础上升级。这与 Nir 的"侦探章节标题"（"An Apparent Dead End" / "When IDs Align"）不同——Hillai 用**功能性编号**，Nir 用**剧情化标题**。

### 1.6 长复合句 + 形式逻辑连接词

Hillai 比 Nir 更爱用形式逻辑连接词（"by definition"、"therefore"、"ironically enough"）：

**一手引用（高可信度，SAPwned 独立署名）**：
- "AI training requires running arbitrary code **by definition; therefore**, appropriate guardrails should be in place to assure that untrusted code is properly separated from internal assets and other tenants."
  （来源：SAPwned）

"by definition; therefore" 这套形式三段论措辞在 Nir 的 DNA 文件中**未观察到**。Hillai 倾向把漏洞结论升格为**逻辑必然**，Nir 倾向把漏洞结论升格为**系统性诊断**（"The cloud has an isolation problem"）。

---

## 2. 词汇特征

### 2.1 高频关键词（基于 2 篇独立署名 + 2 篇 lead 联署）

| 词/短语 | 出现位置 | 功能 | 可信度 |
|--------|---------|------|--------|
| **"ironically enough"** | SAPwned（"which ironically enough was 1337"） | 标记巧合的轻幽默，Hillai 个人指纹；Nir 不用 | 高 |
| **"by definition"** | SAPwned（"running arbitrary code by definition; therefore..."） | 把结论升格为逻辑必然 | 高 |
| **"textbook example"** | BingBang 技术深版（"we see a textbook example of Shared Responsibility confusion"） | 把单点缺陷升格为范本 | 高 |
| **"the exposure is as wide as it gets"** | BingBang 技术深版 | 绝对化形容词，强调范围上限 | 高 |
| **"check the wrong box"** | BingBang 技术深版（"users could check the wrong box and publicly expose their app by accident"） | 把系统性失败压缩成单次 UX 误操作——**Hillai 偏向 UX 批判**而非治理批判 | 高 |
| **"Shared Responsibility confusion"** | BingBang 技术深版 | 用 "confusion"（而非 "model" 或 "gap"）作贬义——把责任真空归因于**认知混乱**而非结构性失败 | 高 |
| **"personal favorite"** | BingBang 技术深版（"our personal favorite, 'Hackers (1995)'"） | 主观品味标签，让研究者露出个人偏好 | 高 |
| **"surprised us"** | BingBang 技术深版（"The results surprised us: 25%..."） | 主动声明情绪，**与 Nir "To our surprise" 同语义但用主动语态** | 高 |
| **"shackles"** | SAPwned（"Free from our traffic shackles..."） | 把 Istio 网络限制诗意化为"镣铐"——**Hillai 偶尔用文学化比喻，Nir 更直接** | 高 |
| **"could have minimized"** / **"downgraded"** | SAPwned 收尾（"could have minimized the impact... downgraded it from a complete service takeover to a minor security incident"） | 反事实条件式收尾，Hillai 个人指纹；Nir 的 winner's narrative 不做这种假设性降级 | 高 |
| **"backbone"** / **"systemic risk to the AI ecosystem"** | NVIDIAScape（**lead 是 Nir + Shir，非 Hillai**） | 仅作 Wiz 宅风格证据，**不归为 Hillai 个人词汇** | 不适用 |
| **"trivial"** / **"holy grail"** / **"keys to the kingdom"** | Nir 文章高频 | Hillai 独立署名文章中**未观察到**这些词——**两人词汇偏好不同** | 高（反向证据） |

### 2.2 自创术语 / 品牌化命名 —— Hillai 也参与但风格不同

| 命名 | 含义 | Hillai 的角色 | 来源 |
|------|------|---------------|------|
| **"SAPwned"** | SAP + pwned 的 portmanteau | **独立署名文章主标题**——Hillai 个人命名 | https://www.wiz.io/blog/sapwned-sap-ai-vulnerabilities-ai-security |
| **"BingBang"** | Bing + bang 的 portmanteau | **独立署名文章主标题**——Hillai 个人命名（与多人联署版共享此名） | https://www.wiz.io/blog/azure-active-directory-bing-misconfiguration |
| **"Isolation or Hallucination? Hacking AI Infrastructure Providers for Fun and Weights"** | Black Hat 2024 演讲标题 | **Hillai 的 Black Hat 个人演讲标题**——pun 呼应经典黑客文化 "for fun and profit" + AI 模型 weights | SAPwned 文中引用 |
| **"Shared Responsibility confusion"** | 责任真空归因 | Hillai 在 BingBang 技术深版自创的术语，**用 "confusion" 而非 "model"**——更贬义 | BingBang 技术深版 |
| **"the power of 1337"** | SAPwned Bug #1 子标题 | leetspeak 内嵌梗，Hillai 个人幽默 | SAPwned |
| **"IngressNightmare"** / **"NVIDIAScape"** / **"CodeBreach"** / **"ChaosDB"** | Nir 主导的命名 | Hillai 仅作为团队成员联署——**不归为 Hillai 个人命名** | 不适用 |

**命名方法论对比**：
- Nir 的命名倾向灾难化后缀（`-Scape` / `-Nightmare` / `-God` / `-DB`），把灾难品牌化。
- Hillai 的命名倾向**轻度 pun + 服务名拼接**（SAPwned / BingBang），更轻巧、更 hacker-culture 风格（呼应 "for fun and profit" 经典梗）。两人**命名美学不同**：Nir 是"灾难片命名"，Hillai 是"黑客文化命名"。
- Hillai 的 Black Hat 演讲标题 "For Fun and Weights" 是**他把命名美学延伸到演讲层**的证据——这是 Nir DNA 文件中未观察到的层次。

### 2.3 不用 / 少用的词

- 几乎不用 "trivial" / "holy grail" / "keys to the kingdom"——这些是 Nir 的高频词，Hillai 独立署名文章中未观察到。
- 几乎不用 "alarming" / "stunningly"——这些是 Nir/NVIDIAScape 宅风格词，Hillai 独立署名文章中未观察到。
- 不用纯口语化缩写。
- 不用感叹号在正文段首（但**会用感叹号在句末**——见 §3.4，这与 Nir "正文不用感叹号" 的纪律不同）。
- 几乎不用 "obviously" / "clearly"——与 Nir 一致。
- **会用 "ironically enough"**——Nir DNA 文件中未观察到此短语，**这是两人词汇指纹的关键差异**。

---

## 3. 节奏感

### 3.1 定义先行 + Bug 编号列举式分节

SAPwned 的章节结构是**功能编号 + Bug 列举**：
- "Bug #1: Bypassing network restrictions with the power of 1337"
- "Bug #2: Loki leaks AWS tokens"
- "Bug #3: Unauthenticated EFS shares expose user files"
- "Bug #4: Unauthenticated Helm server compromises internal Docker Registry and Artifactory"
- "Bug #5: Unauthenticated Helm server compromises K8s cluster, exposing Google access tokens and customer secrets"
  （来源：SAPwned）

这与 Nir CodeBreach 的**heist movie 章节标题**（"An Apparent Dead End" / "When IDs Align" / "Catching an Eclipse"）形成鲜明对比：
- Hillai：**功能性、信息密集、可扫描**——读者一眼能看出每个 bug 涉及什么。
- Nir：**剧情化、悬念、不可扫描**——读者必须读完整节才知道发生了什么。

### 3.2 三段式 PoC 演示（轻喜剧节奏）

BingBang 技术深版的 PoC 演示分三层升级，且**第一层用电影替换**作为"低危害证明"，这是 Hillai 的轻喜剧节奏：

**一手引用（高可信度）**：
- Tier 1（轻喜剧）：把搜索结果 "Dune (2021)" 改成 "Hackers (1995)"——"our personal favorite"
- Tier 2（中性）："The payload also ran as expected" —— 极简陈述
- Tier 3（重灾难）：枚举 Outlook 邮件、日历、Teams、SharePoint、OneDrive 全套可窃数据
  （来源：BingBang 技术深版）

Nir 的 PoC 演示一般是**直接重灾难**（ChaosDB 直接读其他租户数据库），不做"先来个轻的"节奏。Hillai 这种"轻-中-重"三段是**他个人节奏感的证据**。

### 3.3 期待 vs. 现实 二元结构 —— 与 Nir 共享

BingBang 技术深版使用 "Expectation" 与 "Reality" 二图对照（与 Nir PostgreSQL isolation 同构），这是 Wiz 宅风格基线，**不能归为 Hillai 个人特征**。

### 3.4 感叹号在句末 —— 与 Nir 的纪律不同

Hillai 在正文用感叹号收尾制造戏剧节点：

**一手引用（高可信度，SAPwned 独立署名）**：
- "We were now running with full privileges on the cluster!"
  （来源：SAPwned）

Nir 的 DNA 文件明确记录："不用感叹号在正文"。**这是两人节奏感的可观察差异**：Hillai 允许情绪外露在标点层，Nir 把情绪压进词序。

### 3.5 收尾格言 —— 但比 Nir 更软、更反事实

Nir 的收尾是**论点式诊断**（"Isolation is king."）。Hillai 的收尾是**反事实条件式处方**：

**一手引用（高可信度，SAPwned 独立署名）**：
- "the internal network was perceived as trusted. **Hardening those internal services could have minimized** the impact of this attack and **downgraded it from a complete service takeover to a minor security incident**."
  （来源：SAPwned takeaways）

"could have minimized... downgraded" 是**反事实推演**——假设如果做了 X，结果会从 A 降到 B。Nir 的 winner's narrative 不做这种"如果当时"的推演，他直接下达诊断。**这是两人收尾节奏最关键的差异**。

### 3.6 共享 Wiz 宅结尾 "Stay in touch!"

两篇独立署名文章都以 "Stay in touch!" 段落结尾，列出 5 位团队成员的 X handle 与邮箱，附固定句：
- "We are a group of veteran white-hat hackers with a single goal: to make the cloud a safer place for everyone."
  （来源：BingBang 技术深版，SAPwned 同构）

这是 Wiz 宅模板，**不归为任何人个人特征**。

---

## 4. 幽默方式

**总体特征：稀薄、靠括号旁白、leetspeak 梗、电影替换 PoC、Black Hat talk 标题 pun。比 Nir 多一层"作者本人即兴反应"的轻幽默层。**

### 4.1 括号内嵌式自嘲 —— Hillai 最强幽默指纹

见 §1.1。"(yeah, really)" 和 "(!)" 是他把即兴反应塞进括号的手法。Nir 不用此手法——Nir 的轻幽默靠命名（NVIDIAScape）或 xkcd 引用，不靠括号旁白。

### 4.2 leetspeak / hacker-culture 梗

**一手引用（高可信度，SAPwned 独立署名）**：
- Bug #1 子标题 "the power of 1337"——Istio 的 UID 真的就是 1337，他用 leetspeak 梗把巧合命名化。
- 正文："which ironically enough was '1337' (yeah, really)"——再加一层括号自嘲确认。
  （来源：SAPwned）

Nir 的 DNA 文件中未观察到 leetspeak 梗。**这是两人幽默来源的关键差异**：Hillai 从 hacker 文化梗取幽默，Nir 从命名美学取幽默。

### 4.3 经典黑客文化引用（"for fun and profit"）

**一手引用（高可信度，SAPwned 独立署名）**：
- Black Hat 2024 演讲标题 "Isolation or Hallucination? Hacking AI Infrastructure Providers **for Fun and Weights**"
  （来源：SAPwned 文中引用）

这是对经典黑客文献标题 "for fun and profit"（Phrack 经典/smashing the stack for fun and profit）的致敬+变体——把 "profit" 换成 "Weights"（AI 模型权重），既呼应黑客文化又点题 AI。**这是 Hillai 把个人幽默美学延伸到学术演讲层的证据**——Nir DNA 文件未观察到此类演讲标题层 pun。

### 4.4 电影替换 PoC —— 主观品味暴露

见 §3.2 Tier 1。把 Bing 搜索结果 "Dune (2021)" 改成 "Hackers (1995)" 作为低危害 PoC，并明示 "our personal favorite"。**研究者主观品味在 Wiz 宅风格中通常被压制**，Hillai 在此处把它放出来——这是他个人轻喜剧节奏的证据。

### 4.5 不幽默的部分

- 完全没有自嘲式挫折叙事——与 Nir 一致，**两人都写 winner's narrative**。SAPwned 和 BingBang 技术深版都没有"我迷路了 / 我调试了三天"的篇幅。
- 没有讽刺/挖苦云厂商的笑话——与 Nir 一致。
- 没有 meme 式幽默——与 Nir 一致。
- 没有 xkcd 引用——**与 Nir 不同**（Nir 在 ExtraReplica 引 xkcd regex 梗）。Hillai 倾向 leetspeak 梗而非 webcomic 梗。

> **矛盾保留**：无法确认 (a) Wiz 内容审查压制了挫折叙事，还是 (b) Hillai 个人偏好。鉴于两人独立署名文章都无挫折叙事，更可能是 (a) Wiz 品牌纪律。但 Hillai 在括号旁白层允许更多情绪外露，说明他**在品牌纪律内仍争取了个人表达空间**——这是与 Nir 的微差异。

---

## 5. 确定性表达

### 5.1 整体偏向"高确定性 + 主动声明情绪"

与 Nir 一样，Hillai 技术结论是断言式的，几乎不 hedge：

**一手引用（高可信度）**：
- "we were now running without any traffic restrictions!" —— SAPwned（技术事实，无 hedge）
- "we successfully logged in," "immediately appeared," "proved that we could control" —— BingBang 技术深版
- "users could check the wrong box and publicly expose their app by accident" —— BingBang 技术深版（用 "could" 表能力而非推测）

### 5.2 但对"假设性外溢影响"会软下来 —— 与 Nir 同构

只在估计**未被实际演示的攻击者影响**时使用 "could have"：

**一手引用（高可信度，BingBang 技术深版）**：
- "could have led to Bing.com takeover"（标题）
- "could've been exposed"（millions of users）

这是与 Nir 同构的 hedge 模式：**自己的发现 = 100% 断言；外溢影响 = 可能/估计**。两人共享此 Wiz 宅纪律。

### 5.3 "ironically enough" 作为确定性副词

Nir 不用 "ironically enough"。Hillai 用它标记巧合——既是轻幽默也是**对巧合事实的高确定性陈述**（"这真就是 1337，我没在编"）。

### 5.4 反事实条件式收尾 —— Hillai 个人指纹

见 §3.5。"could have minimized... downgraded" 是反事实推演。Nir 不做这种推演，他直接下达诊断（"Isolation is king"）。**这是两人确定性表达最关键差异**：
- Nir：**当下诊断式确定性**（"the cloud has an isolation problem"）
- Hillai：**反事实处方式确定性**（"if you had hardened X, the impact would have been downgraded from A to B"）

### 5.5 不说 "to the best of my knowledge"

与 Nir 一致，Hillai 不做学术式优先权声明。他做的是 vendor disclosure 流程，不存在"谁先发现的"学术争议。

---

## 6. 引用习惯

### 6.1 几乎不引学术文献 —— 与 Nir 同构

两篇独立署名文章**没有 "References" / "Bibliography" 区块**，没有学术引用 [1][2] 编号。这与 Nir 一致，与 Felix Wilhelm（引 RFC/spec/previous work）形成鲜明对比。原因相同：写的是漏洞披露博客，不是研究论文。证据就是 PoC 和截图，不是引用。

### 6.2 引自己以前的工作 —— Wiz 宅风格基线

SAPwned 开篇即把当前发现置于过去研究谱系中：

**一手引用（高可信度，SAPwned 独立署名）**：
- "we on the Wiz Research Team have conducted **extensive tenant isolation research on multiple AI service providers**" —— 暗指此前的 Hugging Face / Replicate 研究
  （来源：SAPwned）

这是 Wiz 宅风格基线（Nir 的 CodeBreach 也引 "Nx S1ngularity" / "Amazon Q"），**不能归为 Hillai 个人特征**。

### 6.3 引云厂商文档 —— 与 Nir 同构

作为 "承诺 vs. 现实" 对照基线。BingBang 技术深版引 Azure AAD 文档作为承诺方，实测结果作为现实方。

### 6.4 不引 xkcd —— 与 Nir 不同

Nir 在 ExtraReplica 引 xkcd regex 梗。Hillai 两篇独立署名文章**未观察到 xkcd 引用**，他更倾向 leetspeak 梗与电影梗。**这是两人引用习惯的微差异**。

### 6.5 引经典黑客文化文献（"for fun and profit"）

见 §4.3。Hillai 通过 Black Hat 演讲标题致敬 "for fun and profit"——**这是引用经典黑客文献**而非学术文献。Nir DNA 文件未观察到此类致敬。

### 6.6 几乎不引安全研究同行 —— 与 Nir 同构

不在文章里引 Project Zero、Trail of Bits、ERNW 等他者的研究。这可能是 (a) Wiz 品牌策略（不放大竞品），也可能是 (b) 研究取向（Wiz 自给自足的研究闭环）。**两人共享此习惯**。

> **不确定性**：仅基于 Wiz 博客样本，他在 X / 演讲 Q&A 中是否会引同行**未能验证**。

---

## 7. 争议立场

### 7.1 对云/AI 厂商的公开态度：定义式批判 + UX 归因

Hillai 几乎所有重大发现都直接打 Microsoft / SAP 的脸，但他的批判**比 Nir 更偏向 UX 而非治理模型**：

**一手引用（高可信度，BingBang 技术深版独立署名）**：
- "users could **check the wrong box and publicly expose their app by accident**" —— 把整个 Bing.com 接管危机压缩成单次 UX 误操作
- "we see a **textbook example of Shared Responsibility confusion**" —— 用 "confusion" 而非 "model" 或 "gap"，归因于**认知混乱**而非结构性失败
  （来源：BingBang 技术深版）

对比 Nir 的治理批判：
- Nir：**"The cloud has an isolation problem."** —— 系统性诊断
- Nir：**"without the customer's awareness or explicit consent"** —— 治理真空归因

**两人批判层次不同**：Nir 批判**治理模型**（云厂商装 agent 不告诉客户），Hillai 批判**UX 设计**（云厂商让用户能勾错框）。这反映两人研究目标不同——Nir 关注 tenant isolation 治理，Hillai 关注 IdP/AI 服务的配置 UX。

### 7.2 对 AI 服务隔离的立场：架构处方式

SAPwned takeaways 段把批判升格为架构处方：

**一手引用（高可信度，SAPwned 独立署名）**：
- "AI training requires running arbitrary code **by definition; therefore**, appropriate guardrails should be in place to assure that untrusted code is properly separated from internal assets and other tenants."
  （来源：SAPwned）

"by definition; therefore" 把隔离要求升格为**逻辑必然**——AI 训练的本质就是跑任意代码，所以**必须**有 sandbox。这是 Hillai 把架构批判形式逻辑化的标志手法。

### 7.3 对 SAP AI 的具体批评：defense in depth 失败

**一手引用（高可信度，SAPwned 独立署名）**：
- "the internal network was perceived as trusted. Hardening those internal services could have minimized the impact of this attack and downgraded it from a complete service takeover to a minor security incident."
  （来源：SAPwned takeaways）

这是 defense-in-depth 批判——Istio 一被绕过，内部网络就全信任，导致连锁失守。批判对象是**架构分层不足**，不是厂商恶意。

### 7.4 对厂商响应的赞扬 —— 与 Nir 同构

两篇独立署名文章都遵循 Wiz 宅纪律：批判架构但不批厂商响应团队。

**一手引用（高可信度）**：
- BingBang 技术深版结尾："All issues were reported to the MSRC team. **It fixed the vulnerable applications, updated customer guidance**..." —— 点赞 Microsoft 响应
  （来源：BingBang 技术深版）

与 Nir 在 ChaosDB 中 "Microsoft's Security Team deserves enormous credit" 同构。**两人共享此 Wiz 宅纪律**。

### 7.5 公开辩论 / 交锋

> **诚实标注**：**未能找到** Hillai 在 X 上与 SAP/Microsoft/AWS 公开吵架的直接证据。X 个人页（x.com/hillai）无法抓取，WebSearch 也未返回具体推文。仅能间接确认：
> - 他在 Black Hat 2024 公开演讲 "Isolation or Hallucination?"，把 SAP AI 隔离失败公开化——这是**研究披露**姿态，不是"公开敌人"姿态。
> - 两篇独立署名文章均含 "Disclosure timeline" 段落，遵循 responsible disclosure 流程。
> - LinkedIn 公开页无法抓取，无原创争议帖可见。

### 7.6 隐含立场：Wiz 商业立场 —— 与 Nir 同构

Hillai 是 Wiz 雇员。所有"云厂商做得不够"的论点都间接为 Wiz（云安全配置检测产品）创造市场。需要标注此利益相关性——他的批判虽然技术上有据，但发言位置不是中立的学术研究员，而是云安全公司的雇员。这与 Felix 在 P0（Google 资助但相对独立）和 Asymmetric Research（独立咨询）的位置不同。**与 Nir 同构，无差异**。

---

## 8. 演讲 delivery 风格（未能直接验证，仅有间接证据）

> **诚实标注**：Black Hat US/EU 2024 briefing schedule 页返回 HTTP 403，KubeCon / RSA / DEF CON 演讲者页未在抓取范围内确认。以下仅基于 SAPwned 文中嵌入的演讲标题与间接线索：

### 8.1 已确认的演讲事实

- **Black Hat 2024**：演讲标题 "Isolation or Hallucination? Hacking AI Infrastructure Providers for Fun and Weights"。可信度：中（SAPwned 文中嵌入引用，但 abstract 原文未拿到）。
- **MSRC Most Valuable Researcher (MVR) 排行榜**：Wiz 博客作者页 bio 提及他 "recognized on MSRC's Most Valuable Researchers leaderboard"。可信度：中（仅 bio 描述，未拿到具体年份/排名）。
- **专长领域**：Wiz 博客作者页 bio 称他 "specializes in research and exploitation of web applications, application security, and finding vulnerabilities in complex high-level systems"。可信度：高（Wiz 官方 bio）。
- **地点**：Israel。可信度：高（Wiz 博客作者页 bio：based in Israel）。

### 8.2 推断（低可信度，需要演讲视频/transcript 验证）

基于 SAPwned 的"Bug 编号列举式分节"和"定义式开头"，可推测他的演讲 delivery 偏向**结构化 walkthrough + 形式逻辑处方**——但这是推断，不是观察。需要 Black Hat 2024 视频或 transcript 才能确认其口头节奏、开场幽默、Q&A 风格。

**特别想验证的演讲层指纹**：Black Hat 标题 "For Fun and Weights" 是否在演讲开场被用作 self-deprecating 引子？还是仅在书面标题层？这决定了 Hillai 的幽默美学是否延伸到口头 delivery。

---

## 9. 公开身份确认（背景事实）

| 属性 | 值 | 来源 | 可信度 |
|------|----|------|--------|
| 当前职位 | Security Researcher @ Wiz Research Team | Wiz 博客作者页 bio | 高 |
| 专长 | web applications / application security / complex high-level systems 漏洞研究 | Wiz 博客作者页 bio | 高 |
| 地点 | Israel | Wiz 博客作者页 bio | 高 |
| X handle | `@hillai` | BingBang 技术深版 / SAPwned "Stay in touch!" 段落列出 | 高 |
| LinkedIn | linkedin.com/in/hillai-ben-sasson | 推断（标准 LinkedIn URL pattern） | 中（页面 999 未能直接验证） |
| 主要 CVE/漏洞（lead author） | SAPwned（SAP AI Core）、BingBang（Microsoft Bing/AAD） | Wiz 博客 | 高 |
| 团队联署参与 | IngressNightmare、NVIDIAScape、CodeBreach | Wiz 博客 "Stay in touch!" 段落 | 高 |
| MSRC 认证 | MSRC Most Valuable Researchers 排行榜 | Wiz 博客作者页 bio | 中（未拿到具体年份/排名） |
| Black Hat 2024 演讲 | "Isolation or Hallucination? Hacking AI Infrastructure Providers for Fun and Weights" | SAPwned 文中嵌入引用 | 中（abstract 原文未拿到） |

> **重要身份澄清**：WebSearch 多次返回幻觉把本调研对象（Wiz 云安全研究员 Hillai Ben-Sasson）与 StarkWare 密码学家（Eli Ben-Sasson 的学术派家族成员）混淆——**这是同名/同姓不同人**。本调研对象是 Wiz 雇员，研究云/AI 服务隔离，**不研究** STARK / 零知识证明。本份 DNA 仅适用于 Wiz 雇员 Hillai Ben-Sasson。

---

## 10. 风格 DNA 公式（基于 2 篇独立署名 + 2 篇 lead 联署样本）

**"Definitional opener + parenthetical asides (yeah, really) + bug-numbered walkthrough + logical-form prescriptive takeaway + UX-blame critique + leetspeak/movie humor + counterfactual closing"**

1. 用定义式开头（"X is a service that..."）开篇，**不**用戏剧化短句
2. 把即兴反应塞进括号——"(yeah, really)" / "(!)"——**这是 Nir 不用的指纹**
3. 用 Bug 编号（Bug #1, Bug #2...）做功能化分节，**不**用 heist movie 标题
4. 章节标题用反问句（"Does AI have an isolation problem?"），正文里几乎不用反问过渡
5. 用形式逻辑连接词（"by definition; therefore"）把结论升格为逻辑必然
6. leetspeak / "for fun and profit" 致敬梗取幽默，**不用** xkcd 引用
7. PoC 演示用三段式轻喜剧节奏（电影替换 → XSS → 全数据窃取）
8. 句末允许感叹号（"with full privileges on the cluster!"）——**与 Nir 不同**
9. 收尾是反事实处方（"could have minimized... downgraded from A to B"），**不**是论点式格言
10. 批判偏向 UX（"check the wrong box" / "Shared Responsibility confusion"）而非治理模型
11. we-voice 全程在场，"I" 完全缺席——Wiz 宅纪律
12. 命名美学偏 hacker-culture（SAPwned / BingBang / "For Fun and Weights"），**不偏**灾难片后缀

---

## 11. 与 Nir Ohfeld 的风格对比表

| 特征 | Hillai Ben-Sasson | Nir Ohfeld |
|------|-------------------|------------|
| **开头句式** | 定义式（"X is a service that..."） | 戏剧化短句独立成段（"In this case, customers were not at fault."） |
| **章节标题风格** | 功能编号（"Bug #1: ..."）/ 反问句标题 | heist movie 剧情（"An Apparent Dead End" / "When IDs Align"） |
| **反问句用法** | 章节标题层（"Does AI have an isolation problem?"） | 段落过渡层（"So what privileges _do_ we have?"） |
| **括号旁白** | 核心指纹——"(yeah, really)" / "(!)" | **不用** |
| **句末感叹号** | 允许（"with full privileges on the cluster!"） | 不用（正文压情绪进词序） |
| **形式逻辑连接词** | "by definition; therefore" / "ironically enough" | 几乎不用 |
| **幽默来源** | leetspeak 梗（1337）+ 电影替换 PoC + 经典黑客文献致敬（"for fun and profit"） | 品牌化命名（NVIDIAScape）+ xkcd 引用 + 内嵌挑战题 |
| **PoC 演示节奏** | 三段式轻喜剧（电影 → XSS → 全数据窃取） | 直接重灾难（ChaosDB 直接读跨租户库） |
| **命名美学** | hacker-culture pun（SAPwned / BingBang / "For Fun and Weights"） | 灾难片后缀（-Scape / -Nightmare / -God / -DB） |
| **收尾格言** | 反事实处方（"could have minimized... downgraded from A to B"） | 论点式诊断（"Isolation is king."） |
| **批判对象** | UX 设计（"check the wrong box"）+ 认知混乱（"Shared Responsibility confusion"） | 治理模型（"gray zone" / "without awareness or consent"） |
| **确定性表达** | 高，但通过反事实条件式软着陆 | 高，断言式，外溢才 hedge |
| **高频词** | ironically enough / by definition / textbook example / shackles / personal favorite | trivial / holy grail / keys to the kingdom / blast radius / silent / systemic |
| **不用** | trivial / holy grail / xkcd / 灾难片后缀命名 | ironically enough / by definition / leetspeak 梗 / 句末感叹号 |
| **第一人称** | we（Wiz 宅纪律） | we（Wiz 宅纪律） |
| **学术引用** | 无 | 无 |
| **引同行研究** | 不引 | 不引 |
| **挫折叙事** | 无（winner's narrative） | 无（winner's narrative） |
| **立场位置** | Wiz 雇员，UX/架构批判 | Wiz 雇员、Head of VR，治理批判 |
| **演讲标题层 pun** | 有（Black Hat "For Fun and Weights"） | 未观察到（命名止于博客标题） |
| **来源可访问性** | 2 篇独立署名 + 2 篇 lead 联署充分；X/LinkedIn/Black Hat 全 403/402/999 | 8 篇 Wiz 博客署名/联署充分；X/演讲页全 403 |

> **核心差异**：Nir 是"品牌化灾难的发现者 / winner's narrative / 论点式诊断"；Hillai 是"括号旁白的 walkthrough 写手 / leetspeak 幽默 / 反事实处方 / UX 批判"。Nir 让你看到他升级，Hillai 让你看到他即兴反应。Nir 收尾下达诊断，Hillai 收尾推演如果。Nir 批判治理模型，Hillai 批判 UX 设计。
>
> **共享部分**（Wiz 宅风格基线，不能归个人）：we-voice / 无学术引用 / 无挫折叙事 / 反问句作某种过渡 / 品牌化命名 / "Stay in touch!" 模板 / responsible disclosure timeline / 厂商响应团队点赞 / 无 xkcd（Nir 例外）/ 无 "obviously" / 无 "I"。
>
> **关键局限**：两人独立风格判断都受 Wiz 宅风格稀释。Hillai 的样本仅 2 篇独立署名（SAPwned 2024-07 + BingBang 技术深版 2023-03），时间跨度 1.5 年，样本量小。Nir 的样本是 8 篇。**Hillai 的 DNA 可信度低于 Nir**，主要因样本量小。

---

## 12. 调研盲点与下一步

如果未来要补强这份 DNA，应优先解决：

1. **抓 X/Twitter `@hillai` 原推文**：需要登录态的 x.com 抓取，或用 Nitter 镜像（如仍可用），或人工截图。这是最大盲点——他在 X 上的口语化表达、对 SAP/Microsoft/AWS 的即兴评论、跟同行的公开互动，全部缺失。**Nir 的 DNA 文件有同样盲点**。
2. **拿 Black Hat 2024 "Isolation or Hallucination?" 演讲 transcript 或视频**：分析他口头开场、过渡、收尾的节奏，与写作对比。视频比 abstract 更能反映 delivery。**特别验证 "For Fun and Weights" 这个 pun 是否在演讲口头层被 self-deprecating 引用**。
3. **拿 KubeCon / RSA / DEF CON speaker page 与 abstract**：sched.com / rsaconference.com / blackhat.com 多次返回 403，需用登录态或人工截图。
4. **拿 LinkedIn posts / activity**：linkedin.com/in/hillai-ben-sasson 返回 999，需登录态抓取。Nir 的 LinkedIn 显示他主要点赞他人不写原创长帖，Hillai 是否不同？未知。
5. **Wiz 内部同事的二手评价**：Nir Ohfeld、Shir Tamari、Ronen Shustin、Sagi Tzadik、Raaz Herzberg、Ronny Greenberg 对他个人风格的描述（podcast 引用、会议 panel 等）。这是分离 Wiz 宅风格与 Hillai 个人特征的关键。
6. **扩样本**：找他独著的活动（个人 blog、个人 GitHub repo README、个人演讲而非联署）以补强独立风格判断。目前独立样本仅 2 篇，可信度受限。
7. **MSRC MVR 排行榜具体年份/排名**：Wiz bio 仅称"recognized on MSRC's Most Valuable Researchers leaderboard"，未给具体年份/排名。Nir 的 DNA 文件记录了 MSRC 2021 Q3 第 3 名，Hillai 的对应数字未知。

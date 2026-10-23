# Shir Tamari — 表达 DNA

> **来源透明度声明**
> 本文基于对 Wiz 博客上 Shir Tamari 署名/联署的 20 篇文章进行的风格提取。其中 **4 篇为她独立署名**（"82% of companies" 2021-02、DNS loophole Black Hat 2021-08、NotLegit 2021-12、Storm-0558 Microsoft Key 2023-07），是提取她**纯个人风格**的金矿；**2 篇为她作为 lead author（署名第一位）**（ExtraReplica 2022-04、BrokenSesame 2023-04），可信度高；其余为多人联署（典型联署者：Nir Ohfeld、Ronen Shustin、Sagi Tzadik、Hillai Ben-Sasson、Alon Schindel、Raaz Herzberg、Andres Riancho、Yuval Avrahami），仅可作"Wiz 宅风格 + Shir 战略层特征"的合成证据，难精确分离个人贡献。
>
> **未拿到的来源（诚实标注）**：
> - **X/Twitter**：handle 已确认 `@ShirTamari`（来自她本人 2021-02 文章 author byline 的 verbatim 引用："find me on Twitter @ShirTamari"，以及 ExtraReplica 的 Stay in touch 区块列出 `@shirtamari`），但 WebFetch 直接访问 `x.com/shirtamari` 返回 **HTTP 402 Payment Required**（与 Nir `@nirohfeld`、Hillai `@hillai` 遇到的同一付费墙）。**Nitter 镜像也都失败**（nitter.net HTTP 999、nitter.privacydev.net HTTP 403）。未能提取任何原推文。**这是最大盲点**——她在 X 上对云厂商/AI 厂商的即兴评论、与同行的公开互动，全部缺失。
> - **LinkedIn**：`linkedin.com/in/shir-tamari/` 返回 **HTTP 999**，`il.linkedin.com/in/shir-tamari` 返回 **HTTP 403**（均登录墙）。无 posts / activity / about 文本样本。
> - **RSA Conference 2022**：`rsaconference.com/speakers/shir-tamari` 与 `rsaconference.com/Library/search?Keyword=shir+tamari` 均 **超时 60 秒**，未能拿到 abstract 原文。Cloud gray zone (2022-06-09) 文中提及 OMIGOD 研究在 RSA Conference 2022 展示——这个交叉证据存在，但无独立 talk abstract。
> - **Black Hat EU 2022**：`blackhat.com/eu-22/briefings/schedule/` 返回 **HTTP 403**，未能拿到 abstract。**但** Cloud vuln DB call to action (2021-11-12) 文章明确引用："Watch our Security Industry Call-to-Action: We Need a Cloud Vulnerability Database briefing at **BlackHat Europe 2021**"——因此她**至少在 Black Hat EU 2021 演讲过**（讲题为该文标题）。用户任务 brief 提到 "Black Hat EU 2022" 可能是误记或额外邀请——本文诚实标注无法独立验证 2022 场次。
> - **Black Hat US 2021**：`blackhat.com/us-21/briefings/schedule/` 返回 **HTTP 404**（活动归档已下线）。但 Wiz 博客 DNS loophole 文章 verbatim 确认讲题：**"A New Class of DNS Vulnerabilities Affecting Many DNS-as-Service Platforms"**，由 "Wiz CTO Ami Luttwak and Shir Tamari at Black Hat 2021" 联讲——**这是唯一 verbatim 验证的会议演讲**。
> - 因此**演讲 delivery 风格（开场/过渡/收尾的口头节奏）本节近乎缺失**，仅有一处讲题验证。
>
> **可信度分级**：`高`（一手 Wiz 博客**独立署名**文章 verbatim）/ `中`（一手 Wiz 博客 **lead 联署**文章，受合著稀释）/ `低`（多人联署或仅作 Wiz 宅风格基线，不能分离个人风格）。
>
> **联署文章的局限（重点标注）**：Wiz 博客几乎所有研究都是团队成果，即便独立署名文章也会列出 4-6 位团队成员的 X handle 与邮箱（"Stay in touch!" 区块）。这意味着 (a) 文章正文虽署一人名，仍可能经过 Wiz 内容审查与同事 review；(b) 文风受 Wiz 宅风格纪律约束（短-长节奏、品牌化命名、we-voice、收尾格言、`#HashtagName` 社交化命名）。下文所有"个人特征"判断，**严格意义上都是 "Shir 主笔特征 + Wiz 宅风格" 的合成**，无法从外部精确分离。4 篇独立署名文章与 2 篇 lead-byline 文章（ExtraReplica、BrokenSesame）是**最接近个人风格**的样本。
>
> **WebFetch 引用长度限制**：底层 WebFetch 工具有 ~125 字符的 verbatim 引用上限，长段落会被转述。下文标注"verbatim"的引用都是工具明确保留下来的短句（≤125 字符）；长段落被转述的会标"paraphrased"或避免引号。**所有 verbatim 短句本身即是风格指纹**——它们是 Shir 写作中最被工具保留下来的"金句"。

---

## 一手来源总览

| 来源类型 | 具体平台 / URL | 时间 | 在文风提取中的角色 | 可信度 |
|---------|---------------|------|-------------------|--------|
| **Wiz 博客独立署名** "82% of companies" | https://www.wiz.io/blog/82-of-companies-unknowingly-give-3rd-parties-access-to-all-their-cloud-data | 2021-02-02 | **主样本**：纯个人风格金矿，最早 attributed 文章 | 高 |
| **Wiz 博客独立署名** DNS loophole Black Hat | https://www.wiz.io/blog/black-hat-2021-dns-loophole-makes-nation-state-level-spying-as-easy-as-registering-a-domain | 2021-08-04 | **主样本**：纯个人风格金矿 | 高 |
| **Wiz 博客独立署名** NotLegit | https://www.wiz.io/blog/azure-app-service-source-code-leak | 2021-12-21 | **主样本**：纯个人风格金矿 | 高 |
| **Wiz 博客独立署名** Storm-0558 Microsoft Key | https://www.wiz.io/blog/storm-0558-compromised-microsoft-key-enables-authentication-of-countless-micr | 2023-07-21 | **主样本**：纯个人风格金矿 | 高 |
| Wiz 博客 **lead 署名** ExtraReplica | https://www.wiz.io/blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql | 2022-04-29 | **次主样本**：Shir 署名第一位 | 高 |
| Wiz 博客 **lead 署名** BrokenSesame | https://www.wiz.io/blog/brokensesame-accidental-write-permissions-to-private-registry-allowed-potential-r | 2023-04-19 | **次主样本**：Shir 署名第一位（5 作者） | 高 |
| Wiz 博客 lead 联署 Cloud vuln DB call | https://www.wiz.io/blog/security-industry-call-to-action-we-need-a-cloud-vulnerability-database | 2021-11-12 | **战略层样本**：与 Alon Schindel 合著，"we must create" 行业集体声 | 中 |
| Wiz 博客 lead 联署 Cloud gray zone | https://www.wiz.io/blog/the-cloud-gray-zone-secret-agents-installed-by-cloud-service-providers | 2022-06-09 | 战略层样本：**Nir 第一署名，Shir 第二**——"gray zone" 概念是 Nir+Shir 联合创造 | 中 |
| Wiz 博客 lead 联署 PostgreSQL isolation | https://www.wiz.io/blog/the-cloud-has-an-isolation-problem-postgresql-vulnerabilities | 2022-08-11 | **联署**：Ronen 第一、Shir 第二、Nir 第三、Sagi 第四。"isolation is king" 是四人联署格言，**不能单独归 Nir** | 中 |
| Wiz 博客联署 BingBang | https://www.wiz.io/blog/bingbang | 2023-03-29 | 与 Raaz Herzberg、Hillai Ben-Sasson 合著 | 中 |
| Wiz 博客联署 Hell's Keychain | https://www.wiz.io/blog/hells-keychain-supply-chain-attack-in-ibm-cloud-databases-for-postgresql | 2022-12-01 | 与 Ronen、Nir、Sagi 合著——**文学化命名 Hell's Keychain + Achilles heel + Forbidden Link** | 中 |
| Wiz 博客联署 GameOver(lay) | https://www.wiz.io/blog/ubuntu-overlayfs-vulnerability | 2023-07-27 | 与 Sagi 合著——**pun 命名 (lay) 后缀** | 中 |
| Wiz 博客联署 Supply chain case study | https://www.wiz.io/blog/secret-based-cloud-supply-chain-attacks-case-study-and-lessons-for-security-teams | 2022-12-13 | 与 Alon 合著——**三步框架 + 自引 Hell's Keychain 作为 case study** | 中 |
| Wiz 博客联署 NVIDIA 系列（4 篇） | https://www.wiz.io/blog/wiz-research-critical-nvidia-ai-vulnerability + 3 篇后续 | 2024-09 至 2025-07 | AI 战略层样本：与 Ronen、Andres、Nir 联署；**cross-vendor 模式引用**（Alibaba/IBM/Azure/HF/Replicate/SAP） | 中 |
| Wiz 博客联署 Replicate | https://www.wiz.io/blog/wiz-research-discovers-critical-vulnerability-in-replicate | 2024-05-23 | AI 战略层样本：与 Sagi 合著；**"models are effectively code"** 论点 | 中 |
| Wiz 博客联署 Hugging Face | https://www.wiz.io/blog/wiz-and-hugging-face-address-risks-to-ai-infrastructure | 2024-04-04 | AI 战略层样本：与 Sagi 合著；**HF 后续采用 Wiz 产品**——商业暗流 | 中 |
| Wiz 博客联署 K8s LAN Party | https://www.wiz.io/blog/k8s-lan-party-challenge | 2024-03-11 | 与 Nir 合著；**CTF 游戏化 register**——不同寻常 | 中 |
| Wiz 博客联署 React2Shell | https://www.wiz.io/blog/nextjs-cve-2025-55182-react2shell-deep-dive | 2025-12-08 | 与 Gili Tikochinski、Hila Ramati、Benjamin Read 合著——**threat-intel + 产品营销 crossover register** | 中 |
| X / Twitter `@ShirTamari` / `@shirtamari` | https://x.com/shirtamari | 现状 | **402 付费墙，未提取** | 低（仅确认 handle） |
| LinkedIn | linkedin.com/in/shir-tamari/ | 现状 | **999/403，未提取** | 低 |
| RSAC 2022 speaker 页 | rsaconference.com/speakers/shir-tamari | 现状 | **超时 60s，未拿到 abstract** | 低 |
| Black Hat EU 2022 schedule | blackhat.com/eu-22/briefings/schedule | 现状 | **403，未拿到 abstract** | 低 |
| Black Hat EU 2021 讲题 | Wiz 博客内嵌引用（Cloud vuln DB 文中） | 2021-11 | **verbatim 验证**："We Need a Cloud Vulnerability Database briefing at BlackHat Europe 2021" | 高（讲题） |
| Black Hat US 2021 讲题 | Wiz 博客内嵌引用（DNS loophole 文中） | 2021-08 | **verbatim 验证**："A New Class of DNS Vulnerabilities Affecting Many DNS-as-Service Platforms"，与 Wiz CTO Ami Luttwak 联讲 | 高（讲题） |
| Wiz Research 团队页 | https://www.wiz.io/research | 现状 | 列 Shir Tamari 角色 "Vulnerability Research"（**不是 "Head of Research"**） | 中 |
| Wiz About 领导层页 | https://www.wiz.io/about | 现状 | **Shir 不在领导层列表**——非高管 | 高 |
| Forbes 30 Under 30 | WebSearch 未返回可用 URL | 现状 | **未验证，不采信**（Nir 已确认在榜，Shir 不假设） | 低 |

---

## 1. 句式偏好

**总体特征：问句式章节标题（最关键指纹）+ 三段式框架 + "we must create" 行业集体声。与 Nir "短促断言独立成段 + heist 章节标题"不同，Shir 不靠单句戏剧化制造悬念，而靠问句作为章节组织器；与 Hillai "定义式开头 + 括号旁白"也不同——Shir 用发现叙事 + 战略框架。**

### 1.1 问句式章节标题 —— Shir 的最强指纹

把反问句升格为**章节标题本身**，让章节标题直接承担读者疑问的提挈。这与 Nir "反问句做段落过渡"（"So what privileges _do_ we have?"）不同——Nir 把反问句撒进正文做剧情转折，Shir 把反问句钉在章节层做结构骨架。

**一手 verbatim 引用（高可信度，"82% of companies" 独立署名，2021-02）**：
- 章节标题："Why does the vendor request the iam:PutRolePolicy?"
- 章节标题："How can I mitigate the risk?"
- 章节标题："Why does the vendor need this permission?"
- 章节标题："How can Wiz help?"
  （来源：https://www.wiz.io/blog/82-of-companies-unknowingly-give-3rd-parties-access-to-all-their-cloud-data）

**一手 verbatim 引用（高可信度，DNS loophole 独立署名，2021-08）**：
- 章节标题："What did we do exactly?"
- 章节标题："What traffic did we receive?"
- 章节标题："Why did we receive this traffic?"
- 章节标题："How could this data be used?"
- 章节标题："Who's responsible for solving the problem?"
  （来源：https://www.wiz.io/blog/black-hat-2021-dns-loophole-makes-nation-state-level-spying-as-easy-as-registering-a-domain）

**一手 verbatim 引用（高可信度，Storm-0558 独立署名，2023-07）**：
- 章节标题："Compromised consumer signing key – who are you?"
- 章节标题："What is the significance of a compromised OpenID signing key?"
- 章节标题："Which applications are affected?"
- 章节标题："How does key forging work?"
- 章节标题："Are Azure customers still at risk?"
  （来源：https://www.wiz.io/blog/storm-0558-compromised-microsoft-key-enables-authentication-of-countless-micr）

**一手 verbatim 引用（高可信度，ExtraReplica lead 署名，2022-04）**：
- 章节（非标题但 verbatim 短句）："We had previously found vulnerabilities in Azure Cosmos DB. Could we reproduce a similar issue in other Azure services?" ——反问句作为研究 mindset 章节的转场
  （来源：https://www.wiz.io/blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql）

**一手 verbatim 引用（高可信度，BrokenSesame lead 署名，2023-04）**：
- 章节标题（PEACH framework 后续章节也含问句组织）
  （来源：https://www.wiz.io/blog/brokensesame-accidental-write-permissions-to-private-registry-allowed-potential-r）

> **与 Nir / Hillai 的关键差异**：Nir 用反问句做**段落过渡**（"So what privileges _do_ we have?"）；Hillai 也用反问句做**章节标题**（"Does AI have an isolation problem?"），所以这一点 Hillai 与 Shir 重叠。但 Shir 的问句标题密度更高（4/4 独立署名文章主导），且常常**成组出现**（DNS loophole 五连问、Storm-0558 五连问），把整篇文章组织成问答骨架——这是 Hillai 单问句标题所没有的密度。

### 1.2 短句独立成段做戏剧开场 —— 与 Nir 共享但有变异

Shir 也用短句独立成段做开场，但**通常是把核心 thesis 压成一句**而不是像 Nir 那样做中段戏剧节点：

**一手 verbatim 引用（高可信度，"82% of companies" 独立署名）**：
- "Cloud identity permissions are complex."
  （来源同上，独立成段的第一句；下一句用"So complex that innocent looking permissions..."展开）

这与 Nir "In this case, customers were not at fault." 单独成段的中段戏剧节点**位置不同**：Shir 把它放**开头作 thesis**，Nir 把它放**中段作转折**。

### 1.3 "we" 全程在场，"I" 完全缺席 —— 与 Nir/Hillai 同构

4 篇独立署名文章 + 2 篇 lead 联署文章 + 所有联署文章，正文中**搜不到任何 "I" 第一人称单数**，全部用 "we" / "Wiz Research" / "the researchers"。即便 "82% of companies" 是 Shir 一人独立署名，正文与 TL;DR 都用 "we"。

**一手 verbatim 引用（高可信度，独立署名）**：
- "we discover more and more issues that do not fit the current model" —— Cloud vuln DB call to action
- "We believe we need a centralized database for reporting and enumerating cloud vulnerabilities" —— 同上
- "We need to band together to put pressure on our CSPs" —— 同上
  （来源：https://www.wiz.io/blog/security-industry-call-to-action-we-need-a-cloud-vulnerability-database）

> **不确定性**：无法确认 (a) Wiz 品牌纪律强制 we-voice，还是 (b) Shir 个人偏好。鉴于 Nir DNA 文件、Hillai DNA 文件均观察到同样现象并同样无法分离，更可能是 (a) Wiz 品牌纪律。但 Shir 的 "we" 有**两种语义层级**：Wiz-团队 "we"（"we discovered"）与行业-集体 "we"（"we must create"、"we need to band together"）——后者是 Nir/Hillai 都未观察到的**战略层语义扩张**。

### 1.4 "we must" 行业集体声 —— Shir 战略层最强指纹

把 "we" 从 Wiz 团队扩张到**整个安全行业 / 整个云生态**，发出**集体行动号召**。这是 Nir 的 winner's narrative 与 Hillai 的 walkthrough 都不做的——这是 Head of Research 战略层才有的措辞。

**一手 verbatim 引用（高可信度，Cloud vuln DB call to action，2021-11）**：
- 章节标题："We must create a better way to respond to cloud vulnerabilities"
- "We believe we need a centralized database for reporting and enumerating cloud vulnerabilities."
- "We need to band together to put pressure on our CSPs to request CVEs for cloud services."
- "We need to ask for more transparency, identification, and severity information for each vulnerability, and that has to come from our CSPs."
- "We must all make an effort to reduce requested permissions to the bare minimum." —— "82% of companies"
  （来源同上）

**模式**：Wiz-"we" 是 "we discovered/we found"；Shir 的行业-"we" 是 "we must create / we need to band together / we must all make an effort"。**从描述性 we 跳到规范性 we**——这是战略层表达的特征。

### 1.5 三段式 / 三支柱 / 三步框架 —— 战略写作者的重组习惯

Shir 反复用**三**作为结构数：三个 escalation paths、三个 pillars、三个 case studies、三个 target criteria。这是战略层写作者的 organizing habit——比单 CVE writeup 更顶层。

**一手 verbatim 引用（高可信度，独立署名 "82% of companies"）**：
- 章节结构："Escalation path #1 – iam:PutRolePolicy" → "Escalation path #2 – lambda:AddPermission" → "Escalation path #3 AWS ReadOnlyAccess managed policy"
- 每条 escalation path 内部又三分："Why does the vendor request the iam:PutRolePolicy?" → "How can I mitigate the risk?"
  （来源：https://www.wiz.io/blog/82-of-companies-unknowingly-give-3rd-parties-access-to-all-their-cloud-data）

**一手 verbatim 引用（高可信度，Cloud vuln DB call to action）**：
- 三个 cloud vulnerability examples 编号："Cloud vulnerability example #1: Cross-Account AWS Vulnerabilities" → "Cloud vulnerability example #2: OMIGOD" → "Cloud vulnerability example #3: ChaosDB"
  （来源：https://www.wiz.io/blog/security-industry-call-to-action-we-need-a-cloud-vulnerability-database）

**一手 verbatim 引用（高可信度，ExtraReplica lead 署名）**：
- 三个 target selection criteria 三段式："A managed cloud service that provides customers a dedicated virtual machine instance within an internal cloud environment" → "A service that would allow us to execute code" → "Service nature should be of high value, used by many and contain sensitive information"
  （来源：https://www.wiz.io/blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql）

**一手引用（高可信度，BingBang 联署，2023-03）**：
- 三支柱框架（paraphrased from fetch）："rapid detection / clear guardrails / adaptive automation" —— 云安全三支柱
  （来源：https://www.wiz.io/blog/bingbang）

**一手引用（高可信度，Supply chain case study 联署，2022-12）**：
- 三种 misconfiguration 模式作为章节结构："1. Overprivileged access to container registries" → "2. Forgotten secrets in the build process" → "3. Lateral movement paths between production and internal build environments"
  （来源：https://www.wiz.io/blog/secret-based-cloud-supply-chain-attacks-case-study-and-lessons-for-security-teams）

> **关键观察**：Hillai SAPwned 也是"Bug #1 → Bug #2 → ... → Bug #5"——但那是**列举**（5 个独立 bug），Shir 是**框架**（3 个 escalation paths 互相之间是渐进/对照关系，不是平行列举）。Hillai 用编号组织 bug 清单，Shir 用编号组织**思想结构**。

### 1.6 "TL;DR" 网络化语气 —— 比 Nir/Hillai 更休闲

Shir 在独立署名文章中用 "TL;DR" 作为章节标题（"82% of companies"），用 "Lets dive into the numbers!" 这种休闲感叹做章节标题。Nir/Hillai 的独立署名文章中**未观察到**这种网络化语气。

**一手 verbatim 引用（高可信度，独立署名 "82% of companies"）**：
- 章节标题："TL;DR"
- 章节标题："Lets dive into the numbers!"（注意："Lets" 没有撇号——这是 Shir 的实际写法或编辑漏校）
  （来源同上）

### 1.7 段落长度的"短-中-短"三元节奏

不像 Nir 的"短句独立成段 + 长复合句展开"二元节奏，Shir 的节奏更接近"短 thesis 句独立成段 → 中等长度的展开段 → 短结论句或编号列表"。她的文章视觉上更"列表化"——大量 bullet point、numbered list、section heading。这是战略写作者倾向"扫描友好"的本能。

---

## 2. 词汇特征

### 2.1 高频关键词

| 词/短语 | 出现位置 | 功能 | 可信度 |
|--------|---------|------|------|
| **"we must create" / "we need to"** | Cloud vuln DB call, "82% of companies" | 行业集体声，规范性"we" | 高 |
| **"tenant isolation"** | ExtraReplica, PostgreSQL isolation, NVIDIAScape, Replicate, Hugging Face | 概念锚，反复回到的中心议题 | 高 |
| **"shared responsibility"** | "82% of companies", Cloud vuln DB, BingBang, Cloud gray zone | 治理概念，反复定义/批判 | 高 |
| **"transparency" / "transparent"** | Cloud vuln DB, ExtraReplica, Cloud gray zone | 治理要求的核心词 | 高 |
| **"the status quo"** | "82% of companies" 章节标题 "Changing the status quo" | 现状的批判对象 | 高 |
| **"murky territory"** | DNS loophole | 治理真空地带的命名 | 高 |
| **"veteran Whitehat hackers"** | ExtraReplica author block, BrokenSesame author block | 自我身份描述，团队署名块固定语 | 高 |
| **"make the cloud a safer place for everyone"** | ExtraReplica, Hell's Keychain, BrokenSesame author block | 团队使命陈述 | 高 |
| **"AI-as-a-Service providers"** | Replicate, Hugging Face | AI 战略层 threat surface 命名 | 高 |
| **"models are effectively code"** | Replicate, Hugging Face | AI 威胁模型 reframe 论点 | 高 |
| **"PEACH framework"** | BrokenSesame, NVIDIAScape, NVIDIA deep dive, Replicate | 自创方法论框架，self-cited | 高 |
| **"container escape"** | NVIDIAScape, NVIDIA deep dive, NVIDIA announcement | 重复技术短语 | 高 |
| **"assume a vulnerability"** | NVIDIA deep dive (verbatim) | 多租户设计师处方 | 高 |
| **"innocent looking permissions"** | "82% of companies" | 欺骗性表面修辞 | 高 |
| **"the most powerful secrets in the modern world"** | Storm-0558 Microsoft Key | 身份签名密钥的夸大化论点 | 高 |
| **"nation-state level spying capability"** | DNS loophole 标题与正文 | 危险放大器 | 高 |
| **"Anyone could have collected data undetected for over a decade"** | DNS loophole | 时间维度上的可怕断言 | 高 |
| **"cannot continue"** | "82% of companies" 收尾 | 现状拒绝 maxmim | 高 |
| **"a personal favorite"** | "82% of companies" 关于 AWS ReadOnlyAccess | 干 understatement 幽默 | 高 |
| **"notorious"** | "82% of companies" 关于 AWS ReadOnlyAccess | 单词定罪 | 高 |
| **"shocking"** | BingBang（"the results were shocking – approximately 25% of the multi-tenant apps scanned were vulnerable"） | 罕见的情绪形容词 | 中（联署） |
| **"bird's-eye view"** | DNS loophole | 攻击者优势比喻 | 高 |
| **"unexpected consequences"** | DNS loophole | 隔离破坏的 understatement | 高 |
| **"Achilles heel" / "Hell's Keychain" / "the forbidden link" / "the keychain"** | Hell's Keychain | 文学/神话化命名 | 中（联署） |

### 2.2 自创术语 / 品牌化命名 —— Shir 的命名美学

Shir 与 Nir 都给漏洞起品牌名，但**美学不同**：Nir 倾向**灾难后缀**（`-Scape` / `-DB` / `-God` / `-Nightmare`），Shir 倾向**文学/神话典故 + pun + 概念命名 + 方法论 mnemonic**。

| 命名 | 含义 | Shir 的角色 | 来源 | 可信度 |
|------|------|------------|------|------|
| **"NotLegit"** | Azure App Service 漏洞 | **独立署名文章主标题**——Shir 个人命名 | https://www.wiz.io/blog/azure-app-service-source-code-leak | 高 |
| **"ExtraReplica"** | Azure PostgreSQL 跨账户 | **Shir 署名第一位**——Shir 主导命名 | https://www.wiz.io/blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql | 高 |
| **"Hell's Keychain"** | IBM Cloud PostgreSQL supply chain | 联署（Ronen 第一）——文学化命名 | https://www.wiz.io/blog/hells-keychain-supply-chain-attack-in-ibm-cloud-databases-for-postgresql | 中 |
| **"BrokenSesame"** | Alibaba Cloud | **Shir 署名第一位**（5 作者）——文学典故（Open Sesame → Broken Sesame） | https://www.wiz.io/blog/brokensesame-accidental-write-permissions-to-private-registry-allowed-potential-r | 高 |
| **"GameOver(lay)"** | Ubuntu OverlayFS LPE | 联署（Sagi 第一）——pun 后缀 `(lay)` 呼应 OverlayFS | https://www.wiz.io/blog/ubuntu-overlayfs-vulnerability | 中 |
| **"BingBang"** | Bing + bang | 联署（Raaz 第一、Shir 第二、Hillai 第三）——onomatopoeia + 服务名 pun | https://www.wiz.io/blog/bingbang | 中 |
| **"the cloud gray zone"** | 云治理概念 | **Nir 第一、Shir 第二**——联合创造 | https://www.wiz.io/blog/the-cloud-gray-zone-secret-agents-installed-by-cloud-service-providers | 中（联合） |
| **"PEACH framework"** | SaaS/PaaS tenant isolation 方法论 mnemonic | **Shir 署名第一位的 BrokenSesame 首次引入**——Shir 主导命名 | https://www.wiz.io/blog/brokensesame-... | 高 |
| **"the forbidden link" / "the keychain"** | Hell's Keychain 内部概念命名 | 联署——文学化抽象 | Hell's Keychain 同上 | 中 |
| **"Achilles heel"** | Hell's Keychain 内 secrets management 比喻 | 联署——古典典故 | 同上 | 中 |
| **"#BingBang" / "#BrokenSesame"** | hashtag 形式 social 化命名 | 联署——社交化习惯 | 同上 | 中 |
| **"ChaosDB" / "OMIGOD" / "NVIDIAScape" / "IngressNightmare" / "CodeBreach"** | Nir 主导的灾难后缀命名 | Shir 仅作团队联署或合作——**不归为 Shir 个人命名** | 各对应 URL | 不适用 |

**命名美学规律**：
- **Nir 是"灾难片命名"**（`-Scape` / `-God` / `-Nightmare` 后缀，灾难品牌化）。
- **Shir 是"文学典故 + 方法论 mnemonic 命名"**（NotLegit / Hell's Keychain / BrokenSesame / Achilles heel / PEACH / GameOver(lay)）——更像**经典黑客文化 + 古典文学**的杂糅。
- **Hillai 是"轻度 pun + 服务名拼接"**（SAPwned / BingBang / "For Fun and Weights"）——更轻巧 hacker-culture。

### 2.3 不用 / 少用的词

- **不用 "trivial"**：在 Shir 署名第一位的 ExtraReplica、BrokenSesame、4 篇独立署名文章中均未观察到 "trivial"。唯一一次出现是在 Cloud gray zone 文中"not a trivial task"，但那篇 Nir 是第一署名，无法归 Shir。
- **不用 "holy grail"**：Nir 高频词，Shir 文中未观察到。
- **不用 "keys to the kingdom"**：Nir 高频词，Shir 文中未观察到（Shir 用 "the most powerful secrets in the modern world" 替代——**同样是夸大化论点但用更书面的措辞**）。
- **不用 "interesting"**：与 Nir、Felix 都不同——Shir、Nir、Hillai 三人都不爱用"interesting"。
- **几乎不用 "obviously" / "clearly"**：与 Nir 类似。
- **不用感叹号在正文**：与 Nir 同。
- **不用 Hillai 风格括号旁白**：4 篇独立署名文章中**没有** "(yeah really)" / "(!)" 这种 Hillai 指纹。

### 2.4 数字夸张化论点 —— 战略层的标志性措辞

Shir 喜欢把单点发现压缩成**百分比论点 + 时间维度论点**作为标题或开篇 thesis：

**一手 verbatim 引用（高可信度，独立署名 "82% of companies"）**：
- 标题："82% of companies unknowingly give 3rd parties access to all their cloud data"
- TL;DR 数据点："82% of companies provide 3rd party vendors highly privileged roles"
- TL;DR 数据点："76% of companies have 3d party roles that allow for full account takeover"（注意"3d"是她/编辑的实际拼法）
- TL;DR 数据点："Over 90% of cloud security teams were not aware they gave high permissions to 3rd party vendors"
  （来源：https://www.wiz.io/blog/82-of-companies-unknowingly-give-3rd-parties-access-to-all-their-cloud-data）

**一手 verbatim 引用（高可信度，DNS loophole 独立署名）**：
- "Anyone could have collected data undetected for over a decade." —— 时间维度危险放大
  （来源：https://www.wiz.io/blog/black-hat-2021-dns-loophole-makes-nation-state-level-spying-as-easy-as-registering-a-domain）

**一手 verbatim 引用（高可信度，Storm-0558 独立署名）**：
- "Identity provider's signing keys are probably the most powerful secrets in the modern world." —— 全局夸大化 thesis
- "The full impact of this incident is much larger than we Initially understood it to be." —— 注意 "Initially" 大写可能是 typo 或强调
  （来源：https://www.wiz.io/blog/storm-0558-compromised-microsoft-key-enables-authentication-of-countless-micr）

> **与 Nir 对比**：Nir 的夸大化措辞是"trivial"、"holy grail"、"keys to the kingdom"——**价值评判形容词**。Shir 的夸大化措辞是"most powerful secrets in the modern world"、"anyone could have collected data undetected for over a decade"——**量化或时间维度的论点**。Nir 是"形容词夸大"，Shir 是"论点夸大"。

---

## 3. 节奏感

### 3.1 Lineage self-citation 作为开篇节奏 —— "我们之前的工作"作为叙事起点

Shir 的 lead 署名文章反复用"我们之前的发现"作为开篇——把当前研究置于过去工作的谱系中。这是 Wiz 宅风格，但 Shir 在 ExtraReplica 中做得尤其明显。

**一手 verbatim 引用（高可信度，ExtraReplica lead 署名）**：
- "We had previously found vulnerabilities in Azure Cosmos DB. Could we reproduce a similar issue in other Azure services?"
- "Following Black Hat, we wondered whether it might be a pattern and whether other managed services could also be accessible to sensitive network components."
- "This direction led us to the following strategy for finding our next research target."
  （来源：https://www.wiz.io/blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql）

**一手 verbatim 引用（高可信度，BingBang 联署）**：
- "As part of ongoing cloud risk research (e.g., ChaosDB, OMIGOD), the researchers examined Azure Active Directory" —— 括号内自引两个前作
  （来源：https://www.wiz.io/blog/bingbang）

**一手 verbatim 引用（高可信度，Cloud vuln DB call to action）**：
- 引用 "OMIGOD" 与 "ChaosDB" 作为 case study #2 与 #3
  （来源：https://www.wiz.io/blog/security-industry-call-to-action-we-need-a-cloud-vulnerability-database）

> **与 Nir 对比**：Nir 也自引前作（CodeBreach 引 Nx S1ngularity、ChaosDB 强调首例性）。两人都做 lineage self-citation——但 Shir 把 lineage 作为**研究 mindset 章节的开篇节奏**（ExtraReplica），而 Nir 把 lineage 作为**戏剧化收尾或 thesis 升级**。Shir 的 lineage 是"我们之前发现 X，这次发现 Y"的递归叙事；Nir 的 lineage 是"我们的发现证明了 Z 系统性问题"的论点升级。

### 3.2 "承诺 vs 现实"对照结构 —— 与 Nir 共享

Shir 也用云厂商文档承诺的隔离模型 vs 实际行为的对照修辞。这与 Nir 共享，是 Wiz 宅风格。

**一手 verbatim 引用（高可信度，ExtraReplica lead 署名）**：
- "Tenant isolation is a fundamental premise of the cloud." —— 把云承诺压成一句 thesis
- "Organizations trust that the cloud services they use, especially high value assets such as databases, are isolated from other customers." —— 承诺陈述
- 然后用 "Wiz Research has discovered a chain of critical vulnerabilities... bypassing tenant isolation" 反转
  （来源同上）

### 3.3 战略层 closing：发布**可发布物**而不是格言

Shir 的标志性收尾**不是像 Nir 那样用单句格言**（"Isolation is king."），而是**发布一个 artifact** —— GitHub 项目、framework、社区数据库、三支柱方法论。这是战略层与 exploit 主力的关键节奏差异。

**一手 verbatim 引用（高可信度，Cloud vuln DB call to action）**：
- 闭篇节奏：从"we must create" → "What we hope to do here is start the discussion" → "We'd love for you to join us on Slack" → 实际 launch OPEN CVDB at cloudvulndb.org（2022-06 后续 update）
  （来源同上）

**一手 verbatim 引用（高可信度，ExtraReplica lead 署名）**：
- 闭篇："Cloud providers should be more transparent about their isolation architecture, especially for sensitive services such as databases."
- "We recommend that organizations ask their cloud service providers for documentation of their isolation architecture for the services they use."
- 文末 launching `csp_security_mistakes` GitHub project（社区可发布物）
  （来源同上）

**一手 verbatim 引用（高可信度，"82% of companies" 独立署名）**：
- 闭篇："This is a call for action!"
- "cloud security teams have a great responsibility to verify and supervise the privileges they provide to third-parties."
- "We must all make an effort to reduce requested permissions to the bare minimum."
  （来源同上）

**一手引用（高可信度，BrokenSesame lead 署名）**：
- 引入 PEACH framework 作为可发布物
  （来源：https://www.wiz.io/blog/brokensesame-...）

**一手引用（高可信度，Cloud gray zone 联署）**：
- launching community-driven cloud middleware dataset（GitHub）
  （来源：https://www.wiz.io/blog/the-cloud-gray-zone-...）

**一手引用（高可信度，BingBang 联署）**：
- 三支柱 framework："rapid detection / clear guardrails / adaptive automation"
  （来源：https://www.wiz.io/blog/bingbang）

> **关键差异**：Nir 的 closing 是"Isolation is king."（**单句格言**）；Shir 的 closing 是"PEACH framework / OPEN CVDB / GitHub dataset / three pillars"（**可发布物**）。Shir 不写格言，她**发布机制**。这是 Head of Research 战略层与 Head of VR 技术主力的根本节奏差异。

### 3.4 章节标题问句成组 —— 问答骨架化

如 §1.1 所述，Shir 把 4-5 个问句式章节标题串成问答骨架，让整篇文章读起来像一个 FAQ。Nir 用 heist movie 章节标题让文章读起来像犯罪叙事——**Nir 的章节是剧情转折，Shir 的章节是结构化问答**。

### 3.5 Stay in touch! 区块 —— Wiz 宅风格

Wiz 博客几乎所有研究文章末尾都有 "Stay in touch!" 区块，列出 4-6 位团队成员的 X handle 与 research@wiz.io 邮箱。这是 Wiz 宅风格纪律。Shir 文章中此区块的团队成员构成随时间演化：

- 2022-04 (ExtraReplica)：Shir Tamari (@shirtamari), Ronen Shustin (@ronenshh), Nir Ohfeld (@nirohfeld), Sagi Tzadik (@sagitz_)
- 2022-08 (PostgreSQL isolation)：Ronen Shustin (@ronenshh), Shir Tamari (@shirtamari), Nir Ohfeld (@nirohfeld), Sagi Tzadik (@sagitz_)
- 2023-04 (BrokenSesame)：Shir Tamari (@shirtamari), Nir Ohfeld (@nirohfeld), Sagi Tzadik (@sagitz_), Ronen Shustin (@ronenshh), Hillai Ben-Sasson (@hillai)
- 2024-04 (Hugging Face)：Sagi Tzadik, Shir Tamari, Nir Ohfeld, Ronen Shustin, Hillai Ben-Sasson
- 2025-02 (NVIDIA Deep Dive)：Nir Ohfeld, Sagi Tzadik, Ronen Shustin, Hillai Ben-Sasson, Andres Riancho, Shir Tamari
- 2025-07 (NVIDIAScape)：Nir Ohfeld, Sagi Tzadik, Ronen Shustin, Hillai Ben-Sasson, Andres Riancho, Yuval Avrahami —— **Shir 不在列**（说明此篇 Nir 主导）

> **Shir 在 Stay in touch! 区块的缺席**：2025-07 的 NVIDIAScape 文中 Shir 是合著者（署名行），但 Stay in touch! 区块**没有列她**——这与 Nir DNA 文件中"Nir 是技术主笔"的判断一致，NVIDIAScape 是 Nir-driven 的技术 exploiting + Shir 战略 closing 的合成。

---

## 4. 幽默方式

**总体特征：稀薄、干冷 understatement、用单词定罪、用数字夸大做反讽——既不像 Felix 那样自嘲挫折，也不像 Hillai 那样用括号旁白，也不像 Nir 那样用 xkcd 引用 + 内嵌挑战题。Shir 的幽默更"行政化"——把荒谬压进单词或百分比里。**

### 4.1 单词定罪 —— "notorious"、"a personal favorite"

把对一个云厂商策略的长期批判压缩成一个单词的形容词定罪，这是 Shir 的核心幽默机制。

**一手 verbatim 引用（高可信度，独立署名 "82% of companies"）**：
- 描述 AWS ReadOnlyAccess managed policy 为"a personal favorite"
- 描述同一 policy 为"notorious"
  （来源同上）

> **模式**：不解释为什么"notorious"——直接用单词定罪，假设读者已知。这是 senior researcher 与社区共享的内部笑话——比 Nir 的"xkcd 引用"更内化、更不带戏。

### 4.2 干 understatement 关于厂商事故 —— "vendor-incompetence-as-fate"

**一手 verbatim 引用（高可信度，NotLegit 独立署名）**：
- 把 Microsoft 偶然的 web.config 错误保护描述为"the configuration tag wasn't closed properly"——deadpan 报告厂商意外
  （来源：https://www.wiz.io/blog/azure-app-service-source-code-leak）

### 4.3 括号内(!) 标记？—— **没有**

Hillai 的指纹 "(yeah really)" 与 "(!)" 在 Shir 的 4 篇独立署名文章中**完全未观察到**。即便 BingBang 文 Hillai 是联署者，正文也未见 Hillai 式括号旁白——说明 Shir 的写作纪律压过了 Hillai 的指纹，或 Hillai 在 BingBang 中贡献有限。

### 4.4 文学 / 神话 / 古典典故命名本身作为幽默

"Hell's Keychain"（但丁《神曲》地狱篇 + keychain 钥匙串 pun）、"BrokenSesame"（Open Sesame 典故）、"Achilles heel"（希腊神话）、"GameOver(lay)"（OverlayFS pun）——**命名即幽默**，但幽默更接近经典黑客文化典故而非 Nir 的灾难片 IP 化。

### 4.5 "TL;DR" + "Lets dive into the numbers!" 网络化休闲

§1.6 已述。这种网络化语气在 Nir/Hillai 独立署名文章中未观察到——Shir 比 Nir/Hillai 更"博客化"。

### 4.6 不幽默的部分

- 完全没有 Felix 式的挫折叙事（"watching my server reboot for the hundredth time"）。
- 完全没有 Nir 式的 "To our surprise, it worked!" 研究者本人惊讶当戏剧节点。
- 完全没有 Nir 式的内嵌挑战题（"If you're up for a challenge, try to find..."）。
- 完全没有 Nir 式的 xkcd 引用。
- 完全没有 Hillai 式的括号旁白惊叹。
- 没有讽刺/挖苦云厂商的笑话。
- 没有 meme 式幽默。

> **Shir 的幽默是行政化的**：她的幽默更像 senior researcher 的内部笑话（"a personal favorite" / "notorious"），预设读者是同行，不需要解释。Nir 的幽默更外向（xkcd 引用 / 内嵌挑战题），Felix 的幽默更自嘲。Shir 的幽默是最不"表演化"的。

---

## 5. 确定性表达

### 5.1 整体偏向"分层确定性" —— 比 Nir 更校准

Shir 的确定性表达有**两层分明**的特征：
- **技术事实层**：100% 断言（"we discovered"、"bypassing tenant isolation"、"Microsoft confirmed that the issue has been fully mitigated"）
- **影响推测层**：用 "could have"、"may have"、"could be affected" 主动 hedge
- **结构性论点层**：100% 断言（"we must create"、"AI models are effectively code"、"Cloud providers should be more transparent"）

这与 Nir "技术结论 100% 断言，外溢影响才 hedge"的二元结构不同——Shir 多了**结构性论点层的高确定性**。她是 Head of Research——她对自己的战略论点不 hedge。

### 5.2 "Could have" 作为危险放大器 —— hedge 反而更可怕

**一手 verbatim 引用（高可信度，DNS loophole 独立署名）**：
- "Anyone could have collected data undetected for over a decade." —— "could have" 在做危险放大
  （来源：https://www.wiz.io/blog/black-hat-2021-dns-loophole-...）

**一手 verbatim 引用（高可信度，Storm-0558 独立署名）**：
- "could have allowed"、"may have been established"、"could be affected if misconfigured"
  （来源同上）

**模式**：当她说"could have"时，**不是**因为不确定是否真发生，而是**因为她无法证明未发生**——这是一种防御性最强陈述。Nir 的 hedge 只在估计规模时出现；Shir 的 hedge 是**反向 burden of proof**：把举证责任推回厂商，让"未发生"成为厂商必须证明的事。

### 5.3 "we believe" —— 与 Nir 共享的推测措辞

**一手 verbatim 引用（高可信度，Cloud vuln DB call to action）**：
- "We believe we need a centralized database for reporting and enumerating cloud vulnerabilities."
  （来源同上）

这与 Nir "We believe this violates the expected isolation model" 的措辞一致——两人都用 "we believe" 做规范性推测。

### 5.4 "the answer is yes" 风格 —— 与 Nir 共享的确认措辞

Shir 也用类似 Nir "Short answer - yes" 的确认措辞（DNS loophole 与 NotLegit 中均有 paraphrased 痕迹），但 WebFetch 未能 verbatim 提取长段落以确认这一点。**可信度：中**。

### 5.5 不说 "to the best of my knowledge" —— 与 Nir 共享

Shir 不做学术式优先权声明。原因与 Nir 同：她做的是 vendor disclosure 流程，不是学术研究。但与 Felix 不同——Felix 会说 "To the best of my knowledge"。

### 5.6 厂商的话作 indictment —— 不用形容词定罪，用厂商原话

Shir 的最强表达指纹之一：**不批厂商"negligent"，而是 verbatim 引用厂商自己的话让矛盾自显**。

**一手 verbatim 引用（高可信度，DNS loophole 独立署名）**：
- "they did not consider it a vulnerability but rather a known misconfiguration" —— Microsoft 自己的话作 indictment
- 漏洞"falls into murky territory" —— 命名治理真空
  （来源同上）

**一手 verbatim 引用（高可信度，Cloud vuln DB call to action）**：
- AWS："notifying by email is not sufficient" —— AWS 自己的话作 indictment
- Microsoft/Azure (OMIGOD)：用户"had no idea the OMI agents were installed in their environment"
- Microsoft/Azure (ChaosDB)："the timeframe of the vulnerability exposure was not made clear"
  （来源同上）

> **关键差异**：Nir 也批治理模型但用 Nir 自己的措辞（"The cloud has an isolation problem"）。Shir 批治理模型用**厂商的原话 verbatim**（"they did not consider it a vulnerability"）。Nir 是**诊断式**，Shir 是**审判式**——把厂商证词作为罪证。

---

## 6. 引用习惯

### 6.1 几乎不引学术文献 —— 与 Nir 同构，与 Felix 反向

Shir 的 Wiz 博客文章**没有 "References" / "Bibliography" 区块**，没有学术引用 [1][2] 编号，没有 RFC 引用，没有学术论文引用。这与 Nir 完全一致，与 Felix Wilhelm（引 RFC / spec / previous work）反向。

原因与 Nir 同：Shir 写的是漏洞披露博客，不是研究论文。证据就是 PoC 和截图，不是引用。

### 6.2 引自己以前的工作 —— Lineage self-citation

见 §3.1。ExtraReplica 引 ChaosDB，BingBang 引 ChaosDB + OMIGOD，Supply chain case study 引 Hell's Keychain，Cloud vuln DB call 引 OMIGOD + ChaosDB + AWS 跨账户漏洞。**Shir 把每个新研究置于过去工作的谱系中**——比 Nir 的 lineage 更系统化（Nir 主要在戏剧化收尾用 lineage，Shir 在开篇 research mindset 章节用 lineage）。

### 6.3 引云厂商文档 / 厂商支持页面 —— "承诺 vs 现实"对照基线

见 §3.2。典型手法：先引 Azure / GCP / AWS 文档说"我们承诺隔离"，再展示实测结果。

### 6.4 引 live forensic 工具 —— Wayback Machine / KQL / Azure CLI —— Shir 的研究方法指纹

Shir 不仅引 vendor docs，还引**实际取证的 live 工具**作为证据：

**一手引用（高可信度，Storm-0558 独立署名）**：
- Wayback Machine 作为 key provenance 取证工具——大部分安全博主 informally 引 Wayback，Shir 把它作为 primary evidence 用
- Azure CLI 命令、KQL query for Log Analytics
  （来源：https://www.wiz.io/blog/storm-0558-...）

> **这是 Shir 的研究方法指纹**：她引 live 工具作为证据，而不是引学术 prior art。Felix Wilhelm 引 spec 作为 prior art，Nir 引 PoC 作为证据，Shir 引 Wayback Machine 作为取证——**三人研究方法论差异通过引用习惯可见**。

### 6.5 引 cross-vendor 模式作为系统性证据 —— Shir 战略层最强引用习惯

把单 CVE 置于 cross-vendor 模式中：

**一手引用（高可信度，NVIDIA 系列 2024-09 与 2025-02）**：
- 引用历史 cross-vendor 失败模式：Alibaba Cloud (BrokenSesame)、IBM (Hell's Keychain)、Azure (ExtraReplica)、Hugging Face、Replicate、SAP (SAPwned——Hillai 主笔) ——把 NVIDIA 列为同一系统模式的最新一例
  （来源：https://www.wiz.io/blog/wiz-research-critical-nvidia-ai-vulnerability 与 https://www.wiz.io/blog/nvidia-ai-vulnerability-deep-dive-cve-2024-0132）

> **这是 Shir 战略层最强引用习惯**：Nir 的引用是"自己前作 → 当前 CVE"的纵向谱系；Shir 的引用是"cross-vendor 横向模式 → 当前 CVE 是其中一例"的横向谱系。两人**引用几何不同**——Nir 是时间纵向，Shir 是空间横向。

### 6.6 几乎不引安全研究同行

不在文章里引 Project Zero、Trail of Bits、ERNW 等他者研究。这与 Nir 一致，与 Felix 反向。可能是品牌策略（不放大竞品），也可能是 Wiz 自给自足研究闭环。

> **不确定性**：这点仅基于 Wiz 博客样本，她在 X / 演讲 Q&A 中是否引同行未能验证。

---

## 7. 争议立场

### 7.1 对云厂商的公开态度：批判且**多方批判**——但用厂商原话定罪，不用形容词

Shir 几乎所有重大发现都直接打 AWS / Azure / GCP / IBM / Alibaba 的脸，但她的文章里**几乎没有情绪化形容词批评**。她引用厂商原话让矛盾自显（见 §5.6）。

**一手 verbatim 引用（高可信度，Cloud vuln DB call to action）**：
- "notifying by email is not sufficient" —— 批 AWS 响应不充分
- 用户"had no idea the OMI agents were installed in their environment" —— 批 Microsoft/Azure 透明度
- "the timeframe of the vulnerability exposure was not made clear" —— 批 Microsoft/Azure Cosmos DB 响应
- 但紧接着又 hedge："Problems are not from CSPs' lack of effort" —— 给厂商台阶
  （来源同上）

> **关键差异**：Nir 批治理模型时用 Nir 自己的措辞（"The cloud has an isolation problem"），是诊断式批判；Shir 批治理模型时用厂商原话（"they did not consider it a vulnerability"），是审判式批判——把厂商证词作为罪证。

### 7.2 多方批判 in 单篇文章 —— Shir 战略层独有

Nir 通常一篇文章批一个云厂商（ChaosDB 批 Azure、CodeBreach 批 AWS、PostgreSQL isolation 批 GCP+Azure）。Shir 在 Cloud vuln DB call 一文中**单篇同时批 AWS + Microsoft/Azure（OMIGOD）+ Microsoft/Azure（ChaosDB）**——把多方批判压缩进一篇战略 call to action。这是 Head of Research 才有的横向视角。

### 7.3 "shared responsibility" / "gray zone" / "status quo" / "transparency" —— 治理批判词汇系统

Shir 有一个比 Nir 更系统的治理批判词汇系统：
- "shared responsibility"：揭示责任分配的不清晰
- "gray zone"（与 Nir 联合创造）：命名责任真空
- "the status quo"：作为批判对象
- "transparency"：作为治理要求
- "murky territory"：命名治理模糊地带
- "cannot continue"：现状拒绝

**一手 verbatim 引用（高可信度，"82% of companies" 独立署名）**：
- 章节标题："Changing the status quo – taking responsibility of 3rd party roles"
- 闭篇："This is a call for action!" + "We must all make an effort to reduce requested permissions to the bare minimum."
  （来源同上）

### 7.4 "we need a cloud vulnerability database" —— Shir 最早的行业级 call to action

2021-11-12 的文章标题就是 industry-wide call to action。这不是单一漏洞披露——是**机构建设呼吁**。后续在 2022-06 真的 launch 了 OPEN CVDB at cloudvulndb.org。

**一手 verbatim 引用（高可信度）**：
- 标题："Security industry call to action: we need a cloud vulnerability database"
- "We must create a better way to respond to cloud vulnerabilities"（章节标题）
- "We believe we need a centralized database for reporting and enumerating cloud vulnerabilities."
- "We need to band together to put pressure on our CSPs to request CVEs for cloud services."
- "We need to ask for more transparency, identification, and severity information for each vulnerability, and that has to come from our CSPs."
- "Watch our Security Industry Call-to-Action: We Need a Cloud Vulnerability Database briefing at BlackHat Europe 2021"
  （来源同上）

> **这是 Shir 战略层最强证据**：Nir 在 4 年内未发起过同等量级的行业机构建设呼吁。Shir 在 2021-11 发起，2022-06 落地——**她不仅写文章，她建机构**。这是 Head of Research 与 Head of VR 的根本不同。

### 7.5 PEACH framework —— 把单 CVE 转化为方法论 IP

BrokenSesame (2023-04) 文中引入 "PEACH framework"——"a step-by-step framework for modeling and improving SaaS and PaaS tenant isolation by managing the attack surface exposed by user interfaces"。后续 NVIDIAScape、NVIDIA deep dive、Replicate 都 self-cite PEACH。**这是把单点研究转化为可复用方法论 IP 的战略层动作**。

### 7.6 公开辩论 / 交锋

> **诚实标注**：未能找到 Shir 在 X 上与 AWS/Azure/GCP/AI 厂商公开吵架的直接证据。X 个人页（x.com/shirtamari）无法抓取，WebSearch 也未返回具体推文。但能间接确认：
> - 她在 Black Hat 2021 与 Wiz CTO Ami Luttwak 联讲 DNS 漏洞——**与 CTO 同台说明她在公司内战略地位高于 Nir/Hillai**。
> - Cloud vuln DB call to action 在 Black Hat EU 2021 有专门 briefing。
> - Cloud gray zone 文中提到 OMIGOD 在 RSA Conference 2022 展示——说明她与云厂商处于**协作披露 + 公开批评**的双重姿态。

### 7.7 隐含立场：Wiz 商业立场 —— 与 Nir 同构

Shir 是 Wiz 雇员。所有"云厂商做得不够"的论点都间接为 Wiz（云安全配置检测产品）创造市场。需要标注此利益相关性——她的批判虽然技术上有据，但发言位置不是中立的学术研究员，而是云安全公司的雇员。

更值得注意的**商业暗流**：Hugging Face 文中 verbatim 提及"Hugging Face subsequently implemented Wiz CSPM and vulnerability scanning"——**厂商在披露后变成 Wiz 客户**。这种"研究披露 → 厂商合作 → 厂商采用 Wiz 产品"的闭环是 Wiz Research 的商业模型。Shir 作为 Head of Research 战略层，对此闭环的存在应知情。

### 7.8 研究伦理 positioning —— 战略层的"we" 自律

**一手 verbatim 引用（高可信度，BrokenSesame lead 署名）**：
- "We immediately stopped research upon noticing this and refrained from accessing other customers' data"
  （来源：https://www.wiz.io/blog/brokensesame-...）

> **观察**：这种**研究伦理 positioning** 在 Nir 的 winner's narrative 中未观察到——Shir 主动声明团队在伦理边界处的自律。这是 Head of Research 对外的伦理姿态，也是对内的纪律示范。

---

## 8. 演讲 delivery 风格（近乎缺失，仅一处 verbatim 验证）

> **诚实标注**：所有会议演讲者页（Black Hat EU 2022、RSA Conference 2022）均返回 HTTP 403 或超时。未拿到 abstract 原文，更未拿到 transcript。以下仅基于 Wiz 博客内嵌引用 + 一处 verbatim 验证：

### 8.1 已 verbatim 验证的演讲

- **Black Hat US 2021**：讲题 verbatim 引用自 Wiz 博客 DNS loophole 文——**"A New Class of DNS Vulnerabilities Affecting Many DNS-as-Service Platforms"**，由 "Wiz CTO Ami Luttwak and Shir Tamari at Black Hat 2021" 联讲。
  （来源：https://www.wiz.io/blog/black-hat-2021-dns-loophole-...）
- **Black Hat EU 2021**：讲题 verbatim 引用自 Cloud vuln DB call to action 文——"Security Industry Call-to-Action: We Need a Cloud Vulnerability Database briefing at BlackHat Europe 2021"。
  （来源：https://www.wiz.io/blog/security-industry-call-to-action-...）

### 8.2 间接确认的演讲

- **RSA Conference 2022**：Cloud gray zone 文中提到 OMIGOD 研究在 RSA Conference 2022 展示。可信度：中（仅 blog 自引，无独立 abstract）。
- **Black Hat EU 2022**：用户任务 brief 提及，但未能在 blackhat.com 拿到 abstract。可能存在但未独立验证。可信度：低。

### 8.3 演讲者地位推断 —— 与 CTO 同台

唯一 verbatim 验证的两场演讲中，2021-08 的 Black Hat US 2021 是与 **Wiz CTO Ami Luttwak** 联讲。这暗示 Shir 在 Wiz 内部地位不同于 Nir/Hillai——她代表 Wiz 与 CTO 同台，是战略层发言人。

### 8.4 推断（低可信度）

基于 Wiz 博客的"问句式章节标题 + 三段式框架 + 'we must create' 集体声"特征，可推测她的演讲 delivery 也偏向**结构化问答 + 行业 call to action**——但这是从写作风格推断，不是观察。需要演讲视频/transcript 才能确认口头节奏。

---

## 9. 公开身份确认（背景事实）

| 属性 | 值 | 来源 | 可信度 |
|------|----|------|--------|
| 当前职位 | Vulnerability Research @ Wiz（**Wiz Research 页面 verbatim**） | https://www.wiz.io/research | 高 |
| **"Head of Research"**？ | **用户任务 brief 称"Head of Research"**，但 Wiz 公开页面只列 "Vulnerability Research"，且她**不在 Wiz About 领导层页**（https://www.wiz.io/about） | Wiz Research 页 + Wiz About 页 | **矛盾保留** |
| 最早 attributed 文章 | 2021-02-02（"82% of companies"） | Wiz 博客 | 高 |
| 主要 CVE/漏洞 | ExtraReplica、BrokenSesame、Hell's Keychain、GameOver(lay)、BingBang、Cloud gray zone（联合）、Cloud vuln DB call（联合）、PEACH framework、NVIDIAScape（联署）、React2Shell（联署） | Wiz 博客 | 高 |
| X handle | `@ShirTamari`（她自己 2021-02 文章 author byline verbatim："find me on Twitter @ShirTamari"）+ `@shirtamari`（Stay in touch! 区块拼写） | Wiz 博客 | 高 |
| LinkedIn | `linkedin.com/in/shir-tamari/`（**HTTP 999 未提取**） | WebFetch 失败 | 低（仅 URL） |
| 会议演讲 | Black Hat US 2021（与 Wiz CTO Ami Luttwak 联讲 DNS 漏洞）+ Black Hat EU 2021（cloud vuln DB briefing） | Wiz 博客内嵌引用 | 高（讲题） |
| 主要合作者 | Nir Ohfeld、Ronen Shustin、Sagi Tzadik、Hillai Ben-Sasson、Alon Schindel、Raaz Herzberg、Andres Riancho、Yuval Avrahami | Wiz 博客 Stay in touch! 区块 | 高 |
| Forbes 30 Under 30 | **未验证，不采信**（Nir 已确认在榜，Shir 不假设） | WebSearch 空返回 | 低 |
| 自我身份描述 | "veteran Whitehat hackers"（团队署名块固定语） | Wiz 博客 verbatim | 高 |
| 团队使命陈述 | "make the cloud a safer place for everyone" | Wiz 博客 verbatim | 高 |
| 地点 / 母语 | Israel（推断——Wiz 总部 + 大部分研究员在 Israel；LinkedIn 不可访问未直接确认） | 间接 | 低 |

> **重要矛盾保留**：用户任务 brief 称 Shir 是 "Wiz Research 的 Head of Research"，但 Wiz 公开页 `wiz.io/research` 把她列在 "Vulnerability Research" 角色下（与 Nir、Hillai 同 label），且她**不在 Wiz About 领导层页**（`wiz.io/about`）。可能的解释：
> 1. 她的 LinkedIn 内部 title 是 "Head of Vulnerability Research" 或 "Head of Research"，但公开 marketing 页面只用 "Vulnerability Research" 通用 label。
> 2. "Head of Research" 是她近期升任但页面未更新。
> 3. 用户任务 brief 来源（可能 LinkedIn 或会议 bio）有误或为非正式称谓。
> 4. "Head of Research" 在 Wiz 内部是层级称谓（高于 Nir 的 Head of VR 战略层），但不是公司高管 title。
>
> **本文采取的策略**：保留用户称谓 "Head of Research"，但标注公开页面证据冲突。她的写作-voice 证据（PEACH / OPEN CVDB / 三支柱框架 / 行业集体 "we must create"）**强烈支持她在战略层而非纯技术层**——这与"Head of Research"战略层定位一致。但公开 title 与 LinkedIn 无法独立验证。

> **关键纠正（针对 Nir DNA 文件的错误）**：Nir DNA 文件第 429 行称 PostgreSQL isolation (2022-08-11) "Nir 是 lead author"——**这不正确**。Wiz 博客该文 byline verbatim 是 **"Ronen Shustin, Shir Tamari, Nir Ohfeld, Sagi Tzadik"**——Ronen 第一、Shir 第二、**Nir 第三**。Shir 是 co-lead，Nir 不是 lead。同样地，"isolation is king" 这句收尾格言出现在该文中，**不能单独归 Nir**——它是 Ronen+Shir+Nir+Sagi 四人联署的格言。

> **关键纠正（针对 "gray zone" 贡献）**：Cloud gray zone (2022-06-09) 的 byline 是 **"Nir Ohfeld and Shir Tamari"**——Nir 第一、Shir 第二。"the cloud gray zone" 作为治理概念的 coinage 是 **Nir+Shir 联合创造**，不能单独归 Nir，也不能单独归 Shir。

---

## 10. 风格 DNA 公式（基于 Wiz 博客样本）

**"Frameworks launcher + question-form skeleton + industry-collective 'we must' + vendor-quote-as-indictment + literary-mythological branding"**

1. 把每篇研究组织成问句式章节标题骨架（4-5 个问句串成 FAQ 结构）
2. 用三段式 / 三支柱 / 三步框架组织思想（不是列举而是结构化）
3. 把 "we" 从 Wiz 团队扩张到整个行业（"we must create"、"we need to band together"）——规范性 we
4. 收尾发布一个 artifact（OPEN CVDB / PEACH / GitHub dataset / three pillars）而不是一句格言
5. 不用形容词批厂商，用厂商原话 verbatim 作审判
6. 命名美学：文学/神话/古典典故 + 方法论 mnemonic（NotLegit / Hell's Keychain / BrokenSesame / PEACH / GameOver(lay) / Achilles heel）+ hashtag 社交化（#BingBang #BrokenSesame）
7. Lineage self-citation 在开篇 research mindset 章节建立（"We had previously found vulnerabilities in Cosmos DB..."）
8. Cross-vendor 横向模式引用（Alibaba/IBM/Azure/HF/Replicate/SAP）作为系统性证据
9. 技术事实 100% 断言，影响推测用 "could have" 反向 burden of proof，结构性论点 100% 断言
10. 几乎不引学术文献，引 vendor docs + 自己前作 + live forensic 工具（Wayback Machine / KQL / Azure CLI）
11. 幽默靠单词定罪（"notorious"、"a personal favorite"）+ 干 understatement 关于厂商事故——不讲笑话、不引 xkcd、不内嵌挑战题、不用括号旁白
12. "veteran Whitehat hackers" + "make the cloud a safer place for everyone" 作为团队 author block 固定语

---

## 11. 与 Nir Ohfeld / Hillai Ben-Sasson 的风格对比表

| 特征 | Shir Tamari | Nir Ohfeld | Hillai Ben-Sasson |
|------|-------------|------------|---------------------|
| **Wiz 内定位（推断）** | 战略层 / 治理层（PEACH, OPEN CVDB, 三支柱） | 技术主笔 / 灾难发现者（ChaosDB, NVIDIAScape） | AI/K8s walkthrough 写手（SAPwned, BingBang） |
| **章节标题美学** | 问句式（成组 4-5 个问句串成 FAQ 骨架） | Heist movie 章节名（"An Apparent Dead End" / "When IDs Align"） | 编号式 Bug 列表（"Bug #1" → "Bug #5"）+ 问句标题 |
| **开头风格** | Lineage self-citation + "We had previously found..." + 短 thesis 句独立成段（"Cloud identity permissions are complex."） | "we discovered..." 直接进叙事 + 短句独立成段做戏剧节点 | 定义式（"SAP AI Core is a service that..."百科式开头） |
| **收尾风格** | 发布**artifact**：OPEN CVDB / PEACH framework / GitHub dataset / 三支柱 | **单句格言**："Isolation is king." / "untrusted contributions should never trigger privileged pipelines" | **反事实条件式**："could have minimized... downgraded it from a complete service takeover to a minor security incident" |
| **第一人称** | "we"（Wiz 团队）+ 行业集体 "we must"（**两层 we**） | "we"（团队） | "we"（团队） |
| **反问句位置** | **章节标题**（"What did we do exactly?"） | **段落过渡**（"So what privileges _do_ we have?"） | **章节标题**（"Does AI have an isolation problem?"）—— 与 Shir 重叠 |
| **三段式 / 三支柱 structuring** | **签名特征**（escalation path #1/#2/#3、rapid detection/clear guardrails/adaptive automation、PEACH framework） | 不观察 | Bug #1-#5 编号列举（不同——列举非框架） |
| **行业集体"we"** | **签名特征**（"we must create"、"we need to band together"） | 不观察 | 不观察 |
| **命名美学** | 文学/神话/古典典故 + 方法论 mnemonic（NotLegit / Hell's Keychain / BrokenSesame / PEACH / Achilles heel / GameOver(lay)） | 灾难后缀（ChaosDB / NVIDIAScape / IngressNightmare / OMIGOD / CodeBreach） | 轻度 pun + 服务名（SAPwned / BingBang）+ Black Hat 标题 pun（"For Fun and Weights"） |
| **括号旁白 / (!) / "(yeah really)"** | 不用 | 不用 | **签名指纹**（"ironically enough was '1337' (yeah, really)" / "4 exabytes (!)"） |
| **词汇偏好（高频）** | shared responsibility / transparency / status quo / murky territory / veteran Whitehat / PEACH / AI-as-a-Service / models are effectively code | trivial / holy grail / keys to the kingdom / blast radius / silent / unbeknownst / systemic | ironically enough / by definition; therefore / shackles / personal favorite / surprised us |
| **夸大化措辞** | "most powerful secrets in the modern world" / "anyone could have collected data undetected for over a decade" / 百分比论点（"82% of companies"） | "trivial"、"holy grail"、"keys to the kingdom"（**形容词夸大**） | "shocking" / "4 exabytes (!)"（**惊叹号夸大**） |
| **Humor 机制** | 单词定罪（"notorious"、"a personal favorite"）+ 干 understatement + 文学命名 | xkcd 引用 + 内嵌挑战题 + 命名 portmanteau | 括号旁白惊叹 + 命名 portmanteau + "for fun and weights" pun |
| **厂商批判方式** | **厂商原话 verbatim 作审判**（"they did not consider it a vulnerability but rather a known misconfiguration"） | **诊断式**："The cloud has an isolation problem" | **UX 批判**："check the wrong box and publicly expose their app by accident" |
| **多方批判 in 单篇** | **签名特征**（Cloud vuln DB call 单篇批 AWS + Microsoft OMIGOD + Microsoft ChaosDB） | 单篇批单厂商 | 单篇单厂商 |
| **Lineage self-citation** | 在开篇 research mindset 章节系统化使用 | 在戏剧化收尾用 | 较少自引前作 |
| **Cross-vendor 横向引用** | **签名特征**（Alibaba/IBM/Azure/HF/Replicate/SAP 列表） | 不观察 | 不观察 |
| **学术 / RFC 引用** | 不引 | 不引 | 不引 |
| **Live forensic 工具引用** | **签名特征**（Wayback Machine / KQL / Azure CLI 作 primary evidence） | 不观察 | 不观察 |
| **行业机构建设呼吁** | **签名特征**（"we need a cloud vulnerability database" → OPEN CVDB 落地） | 不观察 | 不观察 |
| **方法论 IP 化** | **签名特征**（PEACH framework 反复 self-cite） | 不观察 | 不观察 |
| **研究伦理 positioning** | "We immediately stopped research upon noticing this and refrained from accessing other customers' data" | 不观察 | 不观察 |
| **CTF 游戏化 register** | K8s LAN Party（与 Nir 联署，可能 Nir-driven） | IngressNightmare 等 CTF 元素 | 不观察 |
| **xkcd 引用** | 不引 | ExtraReplica 引经典 regex xkcd 梗 | 不引 |
| **挫折叙事** | 不写 | 不写（winner's narrative） | 不写 |
| **公开 title** | Wiz 公开页 "Vulnerability Research"（不是 "Head of Research"）；不在领导层页 | "Head of Vulnerability Research"（Nir DNA 文件）；Forbes 30 Under 30 | Wiz 雇员；Black Hat 2024 speaker |
| **会议演讲可访问性** | Black Hat US 2021 + EU 2021 讲题 verbatim 验证；2022 场次 abstract 未拿到 | KubeCon NA 2025、RSA、Black Hat EU 2025 speaker 页全部 403 | Black Hat 2024 讲题 SAPwned 文内引用，abstract 403 |
| **X handle** | `@ShirTamari` / `@shirtamari`（Wiz 博客 verbatim） | `@nirohfeld` | `@hillai` |
| **X 可访问性** | 402 付费墙 | 402 付费墙 | 402 付费墙 |
| **LinkedIn 可访问性** | 999/403 | 稀疏"Liked by"，几乎不写原创 | 999 |
| **Forbes 30 Under 30** | 未验证 | 在榜 | 未验证 |
| **来源可访问性** | Wiz 博客一手充分（4 篇独立署名 + 2 篇 lead 联署）；X/LinkedIn/RSAC 全部阻塞 | Wiz 博客一手充分；X/演讲页 403 | Wiz 博客一手充分；X/LinkedIn/Black Hat 全部阻塞 |
| **核心 DNA 一句话** | "**Frameworks launcher**：发布 OPEN CVDB / PEACH / 三支柱 / GitHub dataset，写行业级 call to action，用厂商原话作审判，命名美学是文学典故" | "**Branded catastrophe discoverer**：给每个 CVE 起灾难后缀品牌名，用 we-voice 侦探叙事，收尾用单句格言，批治理但不批个人" | "**AI walkthrough writer**：用定义式开头 + 括号旁白惊叹，命名美学是轻度 pun + 服务名，收尾反事实条件式" |

> **三人核心差异**：
> - **Shir 是机构建设者**——她不写格言，她**发布机制**（OPEN CVDB / PEACH / GitHub dataset / 三支柱框架）。她的"we"扩张到行业。
> - **Nir 是品牌灾难发现者**——他给每个 CVE 起灾难后缀品牌名，用侦探叙事包装，收尾用诊断式格言。
> - **Hillai 是 AI walkthrough 写手**——他用定义式开头 + 括号旁白惊叹，命名美学最轻巧。
>
> **三层分工的形成**：Shir 做治理层（PEACH / OPEN CVDB / 行业 calls），Nir 做技术主力（ChaosDB / NVIDIAScape 灾难品牌），Hillai 做 AI/K8s walkthrough（SAPwned / BingBang）。三人互补，覆盖云安全研究的战略 → 战术 → walkthrough 三层。

---

## 12. 调研盲点与下一步

如果未来要补强这份 DNA，应优先解决：

1. **抓 X/Twitter 原推文**：Shir 在 X 活跃（任务 brief 称），是 Nir/Hillai 未能抓到的潜在优势。需要登录态的 x.com 抓取，或 Nitter 可用镜像，或人工截图。她在 X 上的口语化表达、对云/AI 厂商的即兴评论、与同行的公开互动，**全部缺失**。这是最大盲点。
2. **拿 LinkedIn posts / activity**：LinkedIn 返回 999/403。如果能登录抓取她的 posts 与 activity，可验证 "Head of Research" title，并补 strategic-layer 口语表达。Shir 在 LinkedIn 可能有比 Wiz 博客更战略层的原创 posts。
3. **拿 Black Hat / RSA / KubeCon 演讲 transcript 或视频**：分析她口头开场、过渡、收尾的节奏，与写作对比。视频比 abstract 更能反映 delivery。**至少应拿到 Black Hat US 2021 DNS 漏洞演讲与 Black Hat EU 2021 cloud vuln DB briefing 的视频/transcript**——这两个讲题 verbatim 已验证存在。
4. **Wiz 内部同事的二手评价**：Nir Ohfeld、Hillai Ben-Sasson、Sagi Tzadik、Ronen Shustin、Ami Luttwak 对她个人风格的描述（podcast 引用、会议 panel 等）。
5. **验证 "Head of Research" title**：当前公开 Wiz 页面只列 "Vulnerability Research"，与她战略层 voice 证据冲突。需要她的 LinkedIn、Wiz 内部 slide、或会议 bio 来独立验证她的具体 title。
6. **独立判定 Shir 与 Wiz 宅风格的边界**：目前样本是多人联署文章为主（4 篇独立 + 2 篇 lead 联署 + 14 篇联署）。需要她独讲的活动（如 Black Hat 演讲）来对比她的纯个人 voice 与 Wiz 宅风格的差异。
7. **未来文章追踪**：她在 2025-12 的 React2Shell 是与 Gili Tikochinski、Hila Ramati、Benjamin Read 合著——后两人是新名字，可能是 Wiz Research 团队扩张的信号。追踪 2026+ 她的署名文章可观察 voice 演化。

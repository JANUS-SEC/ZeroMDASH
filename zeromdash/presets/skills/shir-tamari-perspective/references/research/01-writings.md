# Shir Tamari — 著作与系统性思考

> 调研目标：以一手 Wiz 博客原文 + 会议官网核实 Shir Tamari 的署名著作、反复出现的核心论点、自创术语、智识谱系，并刻画她作为「战略层人物」的研究指纹，与 Nir Ohfeld / Hillai Ben-Sasson 的差异。
>
> 标注约定：
> - **[一手·她署名]** = Wiz 博客原文中她本人署名的内容，可信度最高
> - **[一手·他人署名]** = Wiz 博客上别人署名、提及她或致谢她的内容
> - **[推断]** = 基于一手材料的模式归纳，我做的判断
> - **[未核实]** = 此前调研交叉提到的线索，本次未能从一手来源证实，或与一手来源矛盾

---

## 0. 调研边界与可信度声明

**已访问的一手来源：**
- Wiz 博客作者页 `https://www.wiz.io/blog/author/shir-tamari` — 列出她全部 20 篇署名博文（2021-02 至 2025-12）
- 20 篇中已逐篇 WebFetch 验证 og/byline 的关键样本（ExtraReplica / Cloud Gray Zone / Storm-0558 / 82% / Cloud vuln DB call / BingBang / Cloud Has an Isolation Problem / NVIDIAScape / Hugging Face / Replicate / React2Shell / Hell's Keychain / BrokenSesame / GameOver(lay) / Secret-based supply-chain / NVIDIA deep dive / NotLegit / Black Hat 2021 DNS / K8s LAN Party）
- Wiz 研究团队页 `https://www.wiz.io/research` — "Meet the team" 列表

**未能访问的一手来源（被站点拒绝 / 沙箱限制）：**
- `linkedin.com/in/shir-tamari/` — HTTP 999（反爬）
- `blackhat.com/eu-22/briefings/schedule/` — HTTP 403
- `rsaconference.com/...` — HTTP 403
- WebSearch 工具在本环境返回元应答而非搜索结果，无法用于核实

**因此以下结论基于 Wiz 博客一手原文；凡涉及 LinkedIn/Black Hat/RSA 议程页的断言一律标 [未核实]。**

---

## 1. 身份与头衔核实

### 「Head of Research」头衔：[未核实] 且与一手来源矛盾

此前 Nir Ohfeld / Hillai Ben-Sasson 调研交叉提到「Shir Tamari 是 Wiz Research 的 Head of Research，Nir Ohfeld 的直接上级」。**本次一手核实未能证实此头衔，且存在矛盾**：

| 来源 | 显示的头衔 | 可信度 |
|---|---|---|
| Wiz 博客作者页 `blog/author/shir-tamari` | **无任何头衔**，仅姓名 + 文章列表 | 一手·未显示 |
| Wiz `/research` 团队页 "Meet the team" | 列为 **"Vulnerability Research"**（研究方向标签，非领导头衔）；同页其他人标 "AI & Threat Research" "Threat Research" "Cloud Security Research" 等，均无 leadership designation | 一手·矛盾 |
| LinkedIn 个人页 | 无法访问（HTTP 999） | 未核实 |
| RSA 2022 议程页（speaker bio） | 无法访问（HTTP 403） | 未核实 |
| Black Hat 议程页 | 无法访问（HTTP 403） | 未核实 |

**矛盾记录（不调和）：** 「Head of Research」这一头衔在 Wiz 官方一手页面（作者页 + 团队页）均未出现；团队页反而把她列为 "Vulnerability Research" 研究员之一，**没有任何显式的领导头衔标注**。这可能意味着：(a) 头衔存在于 LinkedIn/会议 speaker bio 而未反映在 Wiz 官网；(b) 头衔是内部非公开的；(c) 此前调研基于二手推断。在拿到 LinkedIn 一手或会议 speaker bio 前，**不要断言她是 Head of Research**。

### 她与 Wiz CTO Ami Luttwak 的同台 [一手·她署名]
2021-08-04 博文 `black-hat-2021-dns-loophole...` 原文：**"Today at Black Hat, Wiz CTO Ami Luttwak and I are presenting on a new class of vulnerabilities"**。她在 Black Hat USA 2021 与 Wiz CTO 同台主讲——这至少说明她在 2021 年已是足够资深、能代表 Wiz Research 与 CTO 同台的研究员，但同样**不等于**证实 "Head of Research" 头衔。

### Nir 的「直接上级」关系 [未核实]
基于 Nir Ohfeld 多篇合著（Cloud Gray Zone / NVIDIAScape / K8s LAN Party / ExtraReplica）可证两人是长期密切合著搭档，但**「直接上级」这一组织关系没有一手来源**。标 [未核实]。

---

## 2. 完整著作清单（20 篇，byline 已核实）

来源：Wiz 博客作者页（一手） + 逐篇 WebFetch og/byline 验证。下表「她的位置」列以作者页归属为准（作者页列出的文章即她是 byline 作者之一，非文末致谢）。

| 日期 | 标题 | 完整 byline 顺序 | 她的位置 | 类型 |
|---|---|---|---|---|
| 2025-12-08 | React2Shell: CVE-2025-55182 Deep-Dive | Shir Tamari, Gili Tikochinski, Hila Ramati, Benjamin Read | **第 1** | 合著·lead |
| 2025-07-17 | NVIDIAScape (CVE-2025-23266) | Nir Ohfeld, Shir Tamari | 第 2 | 合著 |
| 2025-02-11 | NVIDIA Container Toolkit CVE-2024-0132 Deep Dive | Shir Tamari, Ronen Shustin, Andres Riancho | **第 1** | 合著·lead |
| 2024-09-26 | Wiz Research Finds Critical NVIDIA AI Vulnerability | Ronen Shustin, Andres Riancho | （她未在 byline？作者页却归她——疑为 author-page 误归或致谢） | 待核 |
| 2024-05-23 | Replicate AI-as-a-Service vuln | Shir Tamari, Sagi Tzadik | **第 1** | 合著·lead |
| 2024-04-04 | Hugging Face AI infrastructure risks | Shir Tamari, Sagi Tzadik（致谢 Nir Ohfeld, Ronen Shustin, Hillai Ben-Sasson） | **第 1** | 合著·lead |
| 2024-03-11 | K8s LAN Party Challenge | Nir Ohfeld, Shir Tamari | 第 2 | 合著·CTF |
| 2023-07-27 | GameOver(lay): Ubuntu OverlayFS (CVE-2023-2640/32629) | Sagi Tzadik, Shir Tamari | 第 2 | 合著 |
| 2023-07-21 | Compromised Microsoft Key (Storm-0558) | **Shir Tamari** | **sole** | 独立署名·战略 |
| 2023-04-19 | BrokenSesame (Alibaba Cloud) | Ronen Shustin, Shir Tamari（致谢 Nir, Sagi, Hillai） | 第 2 | 合著 |
| 2023-03-29 | BingBang (Azure AAD multi-tenant) | Raaz Herzberg, Shir Tamari, Hillai Ben-Sasson | 第 2 | 合著 |
| 2022-12-13 | Secret-based cloud supply-chain attacks (case study) | Alon Schindel, Shir Tamari | 第 2 | 合著·方法论 |
| 2022-12-01 | Hell's Keychain (IBM Cloud PostgreSQL) | Ronen Shustin, Shir Tamari | 第 2 | 合著 |
| 2022-08-11 | The cloud has an isolation problem (PostgreSQL cross-vendor) | Ronen Shustin, Shir Tamari, Nir Ohfeld, Sagi Tzadik | 第 2 | 合著 |
| 2022-06-09 | The cloud gray zone (secret agents by CSPs) | Nir Ohfeld, Shir Tamari | 第 2 | 合著·战略 |
| 2022-04-29 | ExtraReplica (Azure PostgreSQL) | Ronen Shustin, Sagi Tzadik, Nir Ohfeld, Shir Tamari | **第 4（末位）** | 合著 |
| 2021-12-21 | NotLegit (Azure App Service source leak) | **Shir Tamari** | **sole** | 独立署名 |
| 2021-11-12 | Call to action: we need a cloud vulnerability database | Alon Schindel, Shir Tamari | 第 2 | 合著·战略倡导 |
| 2021-08-04 | Black Hat 2021: DNS loophole / nation-state spying | **Shir Tamari** | **sole** | 独立署名·战略 |
| 2021-02-02 | 82% of companies give 3rd parties wide read access | **Shir Tamari** | **sole** | 独立署名·战略 |

**已知线索漏列的篇目**（此前 Nir/Hillai 调研未提到，但一手作者页确认存在）：
- GameOver(lay) Ubuntu OverlayFS（2023-07，与 Sagi）
- K8s LAN Party CTF（2024-03，与 Nir）
- NVIDIA Container Toolkit CVE-2024-0132 deep dive（2025-02，第一作者）
- NVIDIA 漏洞公告（2024-09，作者页归她但 byline 只列 Ronen/Andres——**待核**，疑为作者页误归或致谢）
- Secret-based cloud supply-chain 方法论（2022-12，与 Alon Schindel）
- NotLegit（2021-12，独立署名）
- Cloud vulnerability database call（2021-11，与 Alon Schindel）
- Black Hat 2021 DNS（2021-08，独立署名 + 与 CTO 同台）
- 82% of companies（2021-02，独立署名 + 最早一篇）
- Storm-0558 Compromised Microsoft Key（2023-07，独立署名）

### byline 位置模式 [推断]
Shir 在 byline 的位置呈**双峰分布**：
- **独立署名 / lead author（第 1）**：全部是战略叙事 + 方法论 + threat-intel 类（Storm-0558、NotLegit、Black Hat 2021 DNS、82%、React2Shell deep-dive、NVIDIA deep dive、Replicate、Hugging Face）。当她 lead 时，文章更偏「行业框架 + 意义阐释」。
- **末位 / 第 2 作者**：当合著对象是 Nir / Ronen / Sagi 时，她常列第 2 或末位（ExtraReplica 末位、Cloud Gray Zone 第 2、BrokenSesame 第 2、Hell's Keychain 第 2）。这类文章技术 exploit 细节由 Nir/Ronen/Sagi 主笔，她贡献**叙事框架 + 行业意义 + 倡导**。

**这与「她是战略层人物而非技术细节主笔」的假设一致** [推断]——但注意反例：NVIDIA deep dive (2025-02) 和 React2Shell deep-dive (2025-12) 是**纯技术 deep dive**且她仍列第 1 作者，说明她并非只写战略、也能 lead 技术深挖。她的角色更像「program lead / 既能下钻也能上抬」而非「只做叙事」。

---

## 3. 会议演讲

| 会议 | 年份 | 议题 | 合讲人 | 核实状态 |
|---|---|---|---|---|
| Black Hat USA | 2021-08-04 | "A New Class of DNS Vulnerabilities Affecting Many DNS as Service Platforms" | **Ami Luttwak（Wiz CTO）** | [一手·她署名] 她博文原文直述 "Today at Black Hat, Wiz CTO Ami Luttwak and I are presenting" |
| RSA Conference | 2022 | "The Cloud Gray Zone: Vulnerabilities Found in Azure Built-in VM Agents" | Nir Ohfeld | [一手·她署名] Cloud Gray Zone 博文直链 RSA 议程页 |
| Black Hat Europe | 2022 | "Pwning Cloud Vendors with Untraditional PostgreSQL Vulnerabilities" | Nir Ohfeld（按已知线索） | [未核实] blackhat.com/eu-22 返回 403；线索来自此前 Nir 调研，与 PostgreSQL 系列研究时间线吻合，但未能一手证实 Shir 在 speaker 列表 |
| KubeCon EMEA | 2024 | K8s LAN Party CTF（社区挑战赛，非 briefing） | Nir Ohfeld | [一手·她署名] K8s LAN Party 博文提及 KubeCon EMEA 2024 |
| Pwn2Own Berlin | 2025-05-17 | NVIDIAScape 初始报告提交点 | — | [一手·她署名] NVIDIAScape 博文提及报告于 Pwn2Own Berlin 提交 NVIDIA |

**会议演讲特征 [推断]**：她在 Black Hat 与 CTO 同台讲「a new class of vulnerabilities」（DNS），又在 RSA 与 Nir 讲「cloud gray zone」——两次都是**命名一个新漏洞类**而非讲单个 CVE。这呼应她「program builder / 命名者」的角色（见 §5）。

---

## 4. 反复出现的核心论点（≥3 次 = 真信念）

### 信念 1 —「The cloud has an isolation problem」/ 共享责任「gray zone」[FLAGSHIP]
出现于 7+ 处，是她最核心的论点：
- **2021-11 Cloud vuln DB call**：[一手·她署名] 提出 "gray area" / "new middle zone" 概念——云漏洞落在 CSP 与用户共享责任边界，CVE/NVD 都不覆盖
- **2022-04 ExtraReplica**：[一手·她署名] 末位作者但仍署名；主张云厂商应公布隔离架构文档，并倡导 cloud CVE
- **2022-06 Cloud Gray Zone**：[一手·她署名] 把概念正式命名为「gray zone」——可见性、责任、风险评估三重 gap
- **2022-08 Cloud Has an Isolation Problem**：[一手·她署名] 标题即论点；跨厂商 PostgreSQL 同一 exploit code 适用，证明是**一类系统性问题**而非单点
- **2022-12 Hell's Keychain / 2023-04 BrokenSesame**：[一手·她署名] 显式链接到 ExtraReplica，归为同一 cross-tenant 隔离失败家族
- **2024-04 Hugging Face / 2024-05 Replicate / 2025-02/07 NVIDIA**：[一手·她署名] 把同一论点迁移到 AI 基础设施——「AI models in practice are actually code」、PEACH 框架、容器不是强隔离边界

**论点内核 [推断]**：云的共享责任模型制造了一个既不属于 CSP 也不属于用户的「gray zone」，CVE/NVD 不覆盖、CSC 不透明、用户无法评估——这是**结构性治理失效**，不是单点 bug。

### 信念 2 —「We need a cloud vulnerability database」[倡导旗舰]
- **2021-11 Cloud vuln DB call**：[一手·她署名] 显式 "call to action to the security community"，发起 OPEN CVDB / CloudCVE Slack 社区
- **2022-04 ExtraReplica**：[一手·她署名] 该漏洞未获 CVE 标识，借此再倡 cloud CVE
- **2022-06 Cloud Gray Zone**：[一手·她署名] 启动社区驱动的数据集（GitHub）
**论点内核**：云漏洞缺标识符、缺严重性评分、缺通知渠道、缺影响范围标注（OMIGOD CVE 没说明影响哪些 Azure 服务）——需要 CSP 自身喂料的、公开标准化的云漏洞数据库。

### 3 — Identity is the attack surface / 「most powerful secrets in the modern world」
- **2021-02 82% of companies**：[一手·她署名] 第三方 IAM 角色过度授权，82% 组织给第三方宽读权限（基于 1,300+ AWS 账户 + 40 供应商实测）
- **2023-03 BingBang**：[一手·她署名] 第 2 作者；多租户 AAD app 未校验用户原始租户
- **2023-07 Storm-0558**：[一手·她署名·sole] **「Identity provider's signing keys are probably the most powerful secrets in the modern world」**——这是她最被引用的战略金句
- **2022-12 Secret-based supply-chain**：[一手·她署名] 散落凭证（service account token / registry 密码 / bash history）作为供应链攻击燃料
**论点内核 [推断]**：在云时代，身份与密钥取代网络边界成为首要攻击面；身份 provider 签名密钥是「现代世界最有权力的秘密」。

### 4 — Supply chain = scattered secrets + 「the forbidden link」
- **2022-12 Hell's Keychain**：[一手·她署名] 命名配方：**the forbidden link**（生产与构建环境之间的网络通路）+ **the keychain**（散落凭证）= 致命化合物
- **2022-12 Secret-based supply-chain**：[一手·她署名] 把 Hell's Keychain 提炼为方法论 case study，给出 5 条防御清单
- **2023-04 BrokenSesame**：[一手·她署名] 同一配方再现——imagePullSecrets 有 write 权限而非 read-only
- **2024-04 Hugging Face**：[一手·她署名] 同一配方在 AI 基础设施重现——共享 container registry + scope 不足
**论点内核 [推断]**：云供应链攻击有可重复的**两要素配方**——散落明文凭证 + 跨环境网络通路；任何一方切断即可阻断。

### 5 — AI 基础设施是「新的云」，正在重演云的隔离史
- **2024-04 Hugging Face**：[一手·她署名] AI-as-a-Service 厂商在功能上等同于 CSP，却无成熟安全实践；要求 "mature regulation and security practices that are similar to those enforced on public cloud service providers"
- **2024-05 Replicate**：[一手·她署名] 「challenges of tenant separation carry across AI-as-a-service providers」；把 PEACH 框架从云 SaaS/PaaS 直接套到 AI 平台
- **2025-02/07 NVIDIA**：[一手·她署名] 「the most real and immediate risk to AI applications today comes from their underlying infrastructure and tooling」；「containers are not a strong security barrier」「assume a vulnerability」
**论点内核 [推断]**：AI 基础设施以「前所未见的速度」重演云的多租户隔离史，但成熟度更低、可执行代码（model）作为新增攻击面；研究方法论与防御框架可直接从云研究迁移。

### 6 —「Cloud users did nothing wrong — the service did」（道德框架）
- **2021-12 NotLegit**：[一手·她署名·sole] 原文「cloud users did nothing wrong」「the Azure service did」——区分平台不安全默认 vs 用户误配置
- **2021-11 Cloud vuln DB call**：[一手·她署名] 共享责任 middle zone 让用户无法检测/优先级排序/修复
- **2022-06 Cloud Gray Zone**：[一手·她署名] 责任 gap——用户不知道装了什么、不知道谁该打补丁
**论点内核 [推断]**：她反复**为用户辩护、向 CSP 问责**——这是她的叙事道德立场，也是 Wiz 商业逻辑（帮用户看清 CSP 不透明风险）的呼应。

---

## 5. 自创术语与漏洞代号命名

### 她参与命名 / 独立命名的代号
| 代号 | 出处 | 她的参与 | 命名逻辑 [一手·她署名] |
|---|---|---|---|
| **Cloud Gray Zone** | 2022-06 | 共创（与 Nir） | CSP 在客户 VM 上静默装的中间件 agent——可见性、责任、风险评估三 gap |
| **NotLegit** | 2021-12 | **独立命名**（sole author，「we dubbed as 'NotLegit'」） | Azure App Service 把 .git 放公开目录——「不合法」的默认暴露 |
| **ExtraReplica** | 2022-04 | 共创（第 4 作者） | 利用 PostgreSQL 原生 **replication** 机制伪造 replication user 跨账户复制 |
| **Hell's Keychain** | 2022-12 | 共创（第 2 作者） | keychain = 散落凭证集合；Hell's = 严重性；配方 = forbidden link + keychain |
| **BrokenSesame** | 2023-04 | 共创（第 2 作者） | 隐喻 Alibaba/「Open Sesame」+ 容器/租户被「打开」（推断，原文未显式解释） |
| **BingBang** | 2023-03 | 共创（第 2 作者，Raaz lead） | Bing + Bang（影响 Bing.com） |
| **GameOver(lay)** | 2023-07 | 共创（第 2 作者） | game over + overlay（OverlayFS） |
| **NVIDIAScape** | 2025-07 | 共创（与 Nir） | NVIDIA + escape |
| **React2Shell** | 2025-12 | **lead 命名**（第 1 作者） | React + to + Shell（RSC 反序列化直达 shell） |
| **OPEN CVDB / CloudCVE** | 2021-11 → 2022-06 | 共发起（与 Alon Schindel） | 她的旗舰社区倡导——公开云漏洞数据库 + Slack 社区 |
| **PEACH framework** | 多篇引用 | 使用者/推广者（非她独创，但在多篇文章中作为 Wiz 的 SaaS/PaaS 隔离建模框架反复引用） | tenant 隔离建模框架 |

### 命名风格 [推断]
- **双词复合 / 谐音双关**：GameOver(lay)、React2Shell、NVIDIAScape、BrokenSesame、Hell's Keychain
- **隐喻即论点**：代号本身就在阐释漏洞机制（ExtraReplica = replication 滥用；Hell's Keychain = 散落凭证链；Cloud Gray Zone = 责任灰区）
- **可 hashtag 化**：#NVIDIAScape、#BrokenSesame、#Hell'sKeychain——便于传播，构成 Wiz 研究品牌识别
- **她参与度与 byline 位置相关**：sole author 时她独占命名（NotLegit）；lead 时她主导命名（React2Shell、NVIDIAScape with Nir）；作为末位/第 2 作者时她贡献命名 + 叙事但技术细节由 Nir/Ronen/Sagi 主笔

---

## 6. 智识谱系 / 引用习惯

### 内部谱系（Wiz Research 自家研究链）[一手·她署名]
她在多篇博文中显式引用 Wiz 自家研究作为前置：
- **ChaosDB**（Azure Cosmos DB，2021 Black Hat EU，Nir/Sagi）→ 启发 ExtraReplica「能否在其它 Azure 服务复现」
- **OMIGOD**（Azure OMI agent）→ Cloud Gray Zone 在其上抽象出「gray zone」概念
- **ExtraReplica → Hell's Keychain → BrokenSesame → Cloud Has an Isolation Problem**：她把 4 个研究显式归为「同一 cross-tenant 隔离失败家族」
- **EKS Cluster Games CTF**：Hugging Face 研究中 EKS IMDS 攻击手法被描述为「我们 EKS playbook 的一部分」，链回自家 CTF

### 外部引用 [一手·她署名]
- **Cybertec PostgreSQL**（privilege escalation via security definer functions）
- **staaldraad / CVE-2020-25695**（PostgreSQL privesc）
- **Microsoft + CISA** 官方公告（Storm-0558、OMIGOD KEV catalog）
- **Internet Archive Wayback Machine**（Storm-0558 中用于密钥元数据时间线比对）
- **xkcd #1171**（ExtraReplica 中用 regex 漫画自嘲正则错误）——显示**人文学科 / 叙事性** 趣味，与 Felix Wilhelm 式纯技术写作不同

### 她不引用的 [推断]
- 几乎不引用学术安全研究（USENIX/S&P/CCS）——她的研究定位是工业研究而非学术
- 不引用其它云安全厂商（Palo Alto/CrowdStrike/...）的研究——保持 Wiz 独立品牌
- 不引用云安全联盟（CSA）/NIST SP 800 云框架——尽管她的「gray zone」论点与之相关

---

## 7. 战略层视角：Shir vs Nir vs Hillai

### 三人分工对比 [推断，基于一手 byline + 文体]

| 维度 | Shir Tamari | Nir Ohfeld | Hillai Ben-Sasson |
|---|---|---|---|
| 研究范围 | **最广**：云 DB + AI 基础设施 + 供应链 + 身份 + DNS + Ubuntu 内核 + 容器逃逸 | 专精 cloud DB / 容器逃逸 exploit chain（ChaosDB/ExtraReplica/NVIDIAScape） | 专精身份（Azure AAD 多租户 / BingBang deep-dive） |
| 文体 | 战略叙事 + 方法论 + threat intel；常 lead 战略篇 | exploit 细节主笔 | exploit 细节主笔 |
| 标志性产出 | 「a new class of vulnerabilities」命名 + call to action + 社区基础设施（OPEN CVDB / CloudCVE Slack / K8s LAN Party CTF / PEACH 推广） | 单点深钻突破性 CVE | 单点深钻身份攻击 |
| byline 位置模式 | 双峰：战略篇 lead / 技术篇 lead 或末位 | 技术篇 lead 或第 2 | 第 2/第 3（BingBang 第 3） |
| 重复信念 | gray zone / cloud CVE / AI infra 重演云史 / 为用户辩护 | （需 Nir skill 文件交叉，此处不展开） | （需 Hillai skill 文件交叉） |

### 她的「战略层视角」是什么 [推断，基于 §4 六条信念综合]
Shir 的战略层视角可归纳为**「漏洞类命名者 + 行业基础设施构建者」**：
1. **从单点 CVE 抽象出「类」**：Black Hat 2021 讲「a new class of DNS vulnerabilities」；Cloud Gray Zone 讲「gray zone」作为一类治理问题；Cloud Has an Isolation Problem 讲「跨厂商 PostgreSQL 隔离类」。她不满足于报单个漏洞，而要命名一个**可被业界引用的漏洞类**。
2. **构建社区基础设施**：OPEN CVDB / CloudCVE Slack（云漏洞数据库）、PEACH 框架（隔离建模）、K8s LAN Party（教育 CTF）。她在做**研究之外的公共物品**。
3. **道德与叙事立场**：反复「cloud users did nothing wrong」，向 CSP 问责，要求透明——这是她的叙事脊梁，也是 Wiz 商业逻辑（替用户看清 CSP 不透明风险）的研究体现。
4. **研究 program 而非 project**：把 PostgreSQL 系列、供应链系列、AI 基础设施系列都建成可复用的研究 playbook——同一方法论（PEACH）跨域迁移。

**与 Nir 的关键差异 [推断]**：Nir 是「找到 bug 并 exploit 到底」的突破手；Shir 是「把 Nir 找到的 bug 命名为一类、讲清行业意义、推动社区基础设施」的 program lead。二人构成「突破手 + 命名者/倡导者」互补对。ExtraReplica byline（Nir 第 3、Shir 第 4）与 NVIDIAScape byline（Nir 第 1、Shir 第 2）的差异可能反映了**不同研究中二人相对投入的消长**——当 Nir lead 时偏技术突破，当 Shir lead 时偏战略阐释。

**反例注意**：NVIDIA deep dive (2025-02) 和 React2Shell deep-dive (2025-12) 是纯技术 deep dive 且她列第 1 作者——说明她并非「不下钻」，而是**既能上抬到战略也能下钻到 exploit**。她的战略层视角不是「不下场」，而是「下完场后还能抬起来命名」。

---

## 8. 矛盾与未核实项汇总

| 项 | 状态 | 说明 |
|---|---|---|
| 「Head of Research」头衔 | **矛盾·未核实** | Wiz 作者页无头衔；Wiz /research 团队页列为 "Vulnerability Research"（非领导头衔）；LinkedIn/RSA/Black Hat 议程页均无法访问。**不要断言她是 Head of Research**，应表述为「Wiz Research 研究员（疑似领导层，头衔未一手证实）」 |
| Nir 的「直接上级」 | 未核实 | 无一手组织关系来源；仅有合著搭档关系 |
| Black Hat EU 2022 「Pwning Cloud Vendors with Untraditional PostgreSQL Vulnerabilities」 | 未核实 | blackhat.com/eu-22 返回 403；与 PostgreSQL 系列时间线吻合、与 Nir 合讲合理，但 Shir 是否在 speaker 列表未一手证实 |
| 2024-09 NVIDIA 公告篇 byline 归属 | 待核 | 作者页归 Shir，但 WebFetch byline 只见 Ronen Shustin + Andres Riancho——疑为作者页误归或她属致谢而非 byline |
| ExtraReplica byline Shir 第 4 | 已核实 | 一手原文确认 4 作者末位；与「她是 Head of Research 主笔」直觉相反，提示该篇技术细节由 Nir/Ronen/Sagi 主笔 |
| 「Shir 命名 ChaosDB」 | 未核实 | 已知线索提到 ChaosDB，但 ChaosDB（2021）byline 为 Nir/Sagi，Shir 未在 ChaosDB 原文 byline（作者页无此文）——她更可能是 ChaosDB 之后的 program 延续者而非 ChaosDB 命名者 |

---

## 9. 来源可信度小结

| 来源 | 类型 | 可信度 | 用途 |
|---|---|---|---|
| `wiz.io/blog/author/shir-tamari` 作者页 | 一手·Wiz 官方 | **最高** | 20 篇署名博文清单 + URL |
| 逐篇 Wiz 博客原文 og/byline（WebFetch） | 一手·Wiz 官方 | **最高** | byline 顺序 + 她的叙事原文 + 代号解释 + 会议提及 |
| `wiz.io/research` 团队页 | 一手·Wiz 官方 | **高** | 头衔核实（矛盾证据：「Vulnerability Research」非「Head of Research」） |
| Black Hat 2021 DNS 博文（Shir 署名） | 一手·她本人 | **最高** | 与 CTO 同台陈述 |
| Cloud Gray Zone 博文（Nir+Shir 署名） | 一手·她合著 | **最高** | RSA 2022 议程直链 + 「gray zone」概念定义 |
| `linkedin.com/in/shir-tamari/` | 一手·未访问 | 不可用 | HTTP 999，头衔未能核实 |
| `blackhat.com/eu-22/briefings/...` | 一手·未访问 | 不可用 | HTTP 403，Black Hat EU 2022 演讲未能核实 |
| `rsaconference.com/...` | 一手·未访问 | 不可用 | HTTP 403，RSA 2022 speaker bio 未能核实 |
| 此前 Nir Ohfeld / Hillai Ben-Sasson 调研交叉线索 | 二手 | 中 | 用于发现待核实项，不用于断言 |
| WebSearch 工具返回 | 不可用 | 低 | 本环境 WebSearch 返回元应答而非搜索结果，未采信任何 WebSearch 衍生结论（含此前可能出现的「Amit Ohfeld」「Snyk 研究员」等幻觉） |

---

## 附录：信息不足维度（诚实标注）

- **她的内部管理职责范围**（管多少人、是否管 Nir/Hillai）：信息不足，无一手来源
- **她加入 Wiz 的时间**：信息不足（最早博文 2021-02 即已署名，但入职时间不详）
- **她在 Wiz 之外的活动**（学术发表、标准组织、顾问）：信息不足，未在 Wiz 博客一手材料中发现
- **她未参与的 Wiz 重要研究**（如 ChaosDB 原文、OMIGOD 原文）：作者页未归她，应判定为非她 lead，但她后续（Cloud Gray Zone）有抽象引用
- **PEACH 框架的原始提出者**：她在多篇引用但未声明独创，需进一步核实 PEACH 的 byline

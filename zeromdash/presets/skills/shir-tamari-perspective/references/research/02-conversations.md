# Shir Tamari — 长对话与即兴思考

> 调研范围：Shir Tamari（Wiz Research Head of Research）的播客访谈、会议演讲 Q&A、长视频采访、X/Twitter 即兴表达。
> 调研时间：2026-07-27。
> 信息源黑名单遵守：未采信知乎、微信公众号、百度百科。
> 信任标注：[一手·亲口] = Shir 本人在音频/视频/推文中亲口所说；[一手·亲笔] = Shir 本人撰写的博客/文章（文字非对话，但保留其声音）；[合著] = Shir 与同事合著，"we" 集体声音，无法剥离个人观点；[二手] = 转述。

## 0. 方法论与访问限制（重要：信息源可信度声明）

本次调研在工具受限环境下完成，必须诚实记录访问边界，避免后续合成阶段把"找不到"误读为"不存在"：

- **WebSearch 工具在本环境不可用**（返回 placeholder 文本而非真实搜索结果），全程依赖 WebFetch 抓取已知 URL。
- **YouTube 视频页无法抓取**（YouTube 返回的只有页脚导航，无视频元数据/字幕）。`tubetranscript.com`、`youtubetranscript.com` 对已知视频 ID 均返回 404 或连接拒绝。因此 **RSAC 2022、Black Hat EU 2022、CROC Talks YouTube 版本的现场对话/字幕均未能直接获取**。
- **web.archive.org 被 WebFetch 拒绝**（"unable to fetch"）。因此无法抓取 Shir 的 X/Twitter 历史快照——这是与 Nir/Hillai 调研中同样的限制，**任务线索中"Shir 在 X 上很活跃，可能比 Nir/Hillai 更可访问"的假设在本环境无法验证**。
- **Black Hat / RSAC / fwd:cloudsec 官方议程归档均返回 HTTP 403**（反爬）。无法直接核实会议演讲后的观众 Q&A。
- **LinkedIn 返回 999**（反爬）。
- **Google / Bing 搜索重定向到 CAPTCHA 或本地化版本**；DuckDuckGo html 端可用，是本次唯一可用的搜索入口。
- **Darknet Diaries 剧集列表 148-177（2024-08 至 2026-07）未提及 Shir 或 Wiz 漏洞披露**；更早剧集（1-147，覆盖 2021-2022 的 ChaosDB/OMIGOD 时期）未逐一核查，但 Shir 的合作披露风格（团队 + 厂商协调）与 Darknet Diaries 典型的"个人黑客/故事主角"叙事不符，**未见可靠证据显示 Shir 曾做客 Darknet Diaries**。

因此，本文件的"长对话"内容主要来自：(a) 一个可抓取到节目笔记的播客访谈（Screaming in the Cloud），(b) Shir 亲自撰写的 Wiz 博客文章（文字非对话，但保留其战略叙事与可引用措辞，作为会议演讲的"书面伴奏"），(c) 一个仅有宣传摘要的播客出场（CROC Talks）。

会议演讲本身的现场 Q&A、即兴类比、被追问时的回答方式——**在本环境无法直接获取**。下方"会议演讲"小节用演讲的书面伴奏文章补全框架，但明确标注这不是 Q&A 实录。

---

## 1. 播客访谈（真实的对话内容）

### 1.1 Screaming in the Cloud Ep. 307 — "Find, Fix and Eliminate Cloud Vulnerabilities with Shir Tamari and Company"

- **日期**：2022-01-19
- **主播**：Corey Quinn（Last Week in AWS）
- **嘉宾**：Shir Tamari（Wiz Head of Research）、Nir Ohfeld、Sagi Tzadik（三人合访）
- **来源 URL**：https://www.lastweekinaws.com/podcast/screaming-in-the-cloud/find-fix-and-eliminate-cloud-vulnerabilities-with-shir-tamari-and-company/
- **可信度**：高。节目官方页面，含嘉宾介绍与节目笔记。
- **信息性质**：[一手·亲口] 经节目笔记转述的对话内容；具体逐字稿未获取（YouTube 字幕抓取失败），但节目笔记保留了直接引语。

#### 关键可引用内容（Shir 亲口）

**关于披露哲学与云厂商透明度** [一手·亲口]
> "cloud providers should be more transparent"（云厂商应当更透明）——主张厂商应当披露客户数据何时面临风险，而不只是静默修复。

> "we assume that there is much more of them that we never heard about"（我们假设还有更多我们从未听说的[漏洞/静默修复]）——对云厂商"静默修复"行为的默认怀疑。

**关于建立社区推动行业变革** [一手·亲口]
Shir 提到团队建立了 Cloud CVE Slack 频道，围绕云漏洞追踪构建社区并推动行业变化。

**关于 Wiz 作为披露方的结构性优势 vs 独立研究员** [一手·亲口]
> 独立研究员 "usually more care about the bounty than the aftereffect"（通常更在意赏金而非[漏洞的]后续影响）。
Shir 指出 Wiz 的市场能力和融资让他们的发现能获得比典型独立研究员更广的传播——这是一句**罕见的自我定位表态**：她把 Wiz Research 定位为"影响放大器"而非单纯的研究机构，并且隐含对独立研究员生态的温和批评（关注赏金而非修复落地）。这条对理解她作为 Head of Research 的战略姿态非常关键。

**关于云 vs 本地（on-prem）安全——被追问时的立场表态** [一手·亲口]
当 Corey Quinn 反问"既然有这些漏洞，是不是不该上云"时，Shir **没有顺水推舟贩卖恐惧**，反而主张云对大多数组织仍是更安全的选择：
> "moving to the cloud for most organization would be a more secure choice than remain on-premise"
理由：云厂商打补丁比本地环境更快；云提供集中化工具、策略执行和可见性。这是**澄清立场/防止被误读**的典型瞬间——她主动限制自己研究发现的爆炸性解读，避免被读成"反云"。

**关于 ChaosDB 发现过程的即兴叙事** [一手·亲口]
Shir 把 ChaosDB 描述为 "found by mistake"（误打误撞发现的）。团队当时其实在"为客户寻找 Cosmos DB 常见误配置"，途中注意到一个可能脆弱的特性才深挖。
进入 Cosmos DB 后的诡异体验：
> "nobody stopped us. Nobody—we expected an email"（没人拦我们。没人——我们本以为会收到一封[告警]邮件）。
他们访问了 Jupyter Notebook 并横向移动到内部服务，全程未触发告警。Shir 同时承认厂商在海量日志下面临"该记什么、记多久"的难题，但强调 Microsoft 告诉他们没有发现被先行利用的证据。

**关于研究方向选择（"popularity-guided"）** [合著·Nir 表述]
Nir 在这一集中表述团队研究方向是 "popularity-guided"——聚焦客户实际使用的服务。这条非 Shir 亲口，但反映团队共识，间接约束 Shir 的研究议程。

#### 这条访谈对理解 Shir 的价值

这是目前公开可访问的、最贴近"即兴思考"的 Shir 一手素材。Corey Quinn 的追问触发了几个本任务关心的"被追问时的回答方式"信号：
1. **被问"那别上云了？"→ 立即反向澄清**，拒绝把研究武器化成反云叙事。
2. **被问"你们和独立研究员有何不同？"→ 用赏金 vs 后续影响做切分**，把 Wiz Research 自我定位为"影响运营"而非"发现机器"。
3. **披露态度偏激进透明**（"providers should be more transparent"），但**对云本身持建设性立场**——这构成了 Shir 与某些"云末日"叙事研究员的明显差异。

---

### 1.2 CROC Talks — "Helping Secure Hugging Face Hub - Special Guest: Shir Tamari"

- **日期**：2024-04-03
- **播客**：Crying Out Cloud（Wiz 官方播客）
- **主播**：Omer Mosheiov
- **嘉宾**：Shir Tamari（节目笔记称其为 "head of the research team at Wiz"）
- **来源 URL（多源交叉验证）**：
  - Wiz 官方：https://www.wiz.io/crying-out-cloud/croc-talks-helping-secure-hugging-face-hub-special-guest-shir-tamari
  - YouTube：https://www.youtube.com/watch?v=UvsSuh4MfuA
  - Apple Podcasts：https://podcasts.apple.com/us/podcast/croc-talks-helping-secure-hugging-face-hub-special/id1675289400?i=1000651459698
  - Podtail：https://podtail.com/en/podcast/crying-out-cloud/croc-talks-helping-secure-hugging-face-hub-special/
  - GetPodcast：https://getpodcast.com/podcast/crying-out-cloud/croc-talks-helping-secure-hugging-face-hub-special-guest-shir-tamari_f4345d5b23
- **可信度**：高。多平台一致，Wiz 官方播客。
- **信息性质**：[一手·亲口] 节目存在性已多源确认；但 **Wiz 节目页只提供宣传摘要而非完整逐字稿**，YouTube 字幕抓取失败（tubetranscript 返回 404），因此下述内容是节目笔记级别的主题，**具体即兴措辞未获取**。

#### 节目笔记确认的主题

- Wiz Research 与 Hugging Face 协作，识别 AI-as-a-Service 的 "critical risks"。
- 讨论 Hugging Face 基础设施中的两类缺陷：**shared inference** 与 **CI/CD 系统**，"could potentially offer unauthorized access to sensitive data"。
- 强调 AI 服务激增需要 robust 安全框架。
- Hugging Face 采取了响应措施：采用 Wiz CSPM、持续漏评、年度渗透测试，被描述为 "establishing a high standard in AI safety"。

#### 信息缺口声明

这一集是 Shir 在 Wiz 自家播客上谈 AI 安全的关键一手素材，但**实际对话的逐字内容、被追问时的回答、即兴类比均未能获取**。如需用于合成 Shir 的视角，应额外获取音频或字幕。**不要把上方主题列表当作 Shir 的直接引语使用**——它们是节目摘要的转述。

---

## 2. 会议演讲（含书面伴奏文章）

下方三场会议演讲的**现场 Q&A、即兴类比、被追问时的回答均未能直接获取**（YouTube 字幕抓取失败 + 议程归档 403）。但每场演讲都有 Shir 亲自或合著的 Wiz 博客作为"书面伴奏"，可补全她的战略框架与可引用措辞。**标注为 [一手·亲笔] 或 [合著]，不是 Q&A 实录**。

### 2.1 Black Hat USA 2021 — "DNS Loophole"（与 Ami Luttwak 合讲）

- **演讲者**：Shir Tamari + Ami Luttwak（Wiz CTO）
- **来源 URL**（书面伴奏）：https://www.wiz.io/blog/black-hat-2021-dns-loophole-makes-nation-state-level-spying-as-easy-as-registering-a-domain
- **可信度**：高。Wiz 博客，Shir 亲笔（与 Ami 合著）。
- **信息性质**：[一手·亲笔] 书面伴奏，非 Q&A 实录。

#### 关键措辞

- 团队通过注册与某托管 DNS 厂商自身 nameserver 同名的域名，打破了租户隔离，"wiretapped"（窃听）了来自 15,000 个组织（含财富 500 与政府机构）的动态 DNS 流量。
- 泄漏内容："internal and external IP addresses, computer names, employee names and office locations"。
- **核心类比** [一手·亲笔]：
  > "We liken this to having nation-state level spying capability – and getting it was as easy as registering a domain."
  这是 Shir 标志性的**戏剧化类比手法**：把一个技术漏洞拉高到"国家级情报能力"量级，同时强调攻击门槛极低。这种"高烈度 × 低门槛"双轴叙事在 Shir 后续披露中反复出现。
- **责任归属的灰色地带表态** [一手·亲笔]：Shir 把责任划入 "international waters"——Microsoft、DNS 厂商、个体组织之间的修复义务都不清晰。Microsoft 不认为这是漏洞而视为 "known misconfiguration"。Shir 同时指出 "no way of knowing whether the loophole has already been exploited"——对"是否已被在野利用"保持不可知论姿态。
- **即兴推论**：她提到团队识别到有公司在伊朗、缅甸、科特迪瓦有员工，可能违反 OFAC 制裁——把研究发现的副作用主动外推到合规维度，这是 Shir 叙事的另一个习惯（把单点漏洞连接到更大的治理/合规图景）。

### 2.2 RSAC 2022 — "The Cloud Gray Zone: Vulnerabilities Found in Azure Built-in VM Agents"（与 Nir Ohfeld 合讲）

- **演讲者**：Shir Tamari + Nir Ohfeld
- **视频 URL**（未能抓取字幕）：https://www.youtube.com/watch?v=QNKT7ocTibk（43:19）
- **书面伴奏 URL**：https://www.wiz.io/blog/the-cloud-gray-zone-secret-agents-installed-by-cloud-service-providers
- **可信度**：高。RSA Conference 2022 正式议程 + Wiz 博客合著。
- **信息性质**：[合著] "we" 集体声音，Shir 与 Nir 共同署名，无法剥离个人观点。

#### 关键措辞

- 云厂商在客户 VM 上**秘密安装**专有中间件（agents），客户通常不知情。这类软件桥接 VM 与托管服务，但引入额外攻击面。
- OMIGOD 后的荒谬：当 Microsoft 修复后，"customers were expected to update an agent which they were not aware was installed"（客户被期望去更新一个他们不知道被安装了的 agent）。这是 Shir/Nir 标志性的**用荒谬细节凸显系统性问题**的手法。
- 行业级呼吁 [合著]："be transparent about the cloud middleware software used to integrate customers' virtual machines"。
- 配套动作：Wiz 启动了社区驱动的 GitHub 仓库，绘制所有云厂商在客户机器上安装的 agent 及其攻击面。

#### 这场演讲对理解 Shir 的战略姿态

- Shir 把单点漏洞（OMIGOD）外推为**跨厂商系统性问题**（"not limited to Azure"）。
- 把修复责任错位（厂商修了但客户不知道有 agent）转化为**透明度议程**。
- 用社区数据集（GitHub repo）把研究转化为公共基础设施——这是 Head of Research 的战略动作，不是单点 bug hunter 的动作。

### 2.3 Black Hat EU 2022 — "Pwning Cloud Vendors with Untraditional PostgreSQL Vulnerabilities"

- **演讲者**：Shir Tamari + Nir Ohfeld（用户线索）；书面伴奏署名为 Shir Tamari, Ronen Shustin, Nir Ohfeld, Sagi Tzadik
- **视频 URL**（未能抓取字幕）：https://www.youtube.com/watch?v=X6CiUD3EcfQ（39:10）
- **书面伴奏 URL**：https://www.wiz.io/blog/the-cloud-has-an-isolation-problem-postgresql-vulnerabilities
- **可信度**：高。Black Hat EU 2022 正式议程（用户线索）+ Wiz 博客合著。
- **信息性质**：[合著] 四人合著，"we" 集体声音。

#### 关键措辞

- 研究发现跨多个云厂商（GCP Cloud SQL、Azure PostgreSQL 等）的 PostgreSQL-as-a-Service 隔离漏洞。云厂商为提供"半管理员"能力对 PostgreSQL 引擎做的改造引入了可利用漏洞。
- **跨厂商模式的核心观察** [合著]：
  > "CSPs tend to introduce very similar capabilities, we were able to prove the same exploit code working on multiple vendors."
  这条是 Shir 团队**横向类比方法论**的精华：不同厂商做相似的改造 → 同一exploit 逻辑跨厂商复用。这与本仓库的"启发式漏矿类比"任务高度同构——Shir 团队的思路本身就是"相似软件 → 相似漏洞根因"。
- **协调披露的难题** [合著]：
  > "the vulnerabilities vary between the unique modifications each vendor has implemented, we could not issue a CVE for these issues."
  无法发 CVE → 组建私有厂商协调组 → GCP 提议把加固 upstream，但 "the PostgreSQL community was not enthusiastic about the idea"。
- **核心教训** [合著]：
  > "a service with strictly enforced isolation is more resilient to malicious actors, even if they are equipped with zero-day vulnerabilities."
  这是 Shir 团队的**纵深防御哲学**：隔离执行的严格程度决定烈度，而非漏洞本身的存在。

---

## 3. 战略性书面文章（一手声音，文字非对话）

下列文章虽非"对话"，但保留 Shir 的战略叙事与可引用措辞，且与她的会议演讲共享修辞框架。**合成她的视角时应明确：这是她写下的、经过打磨的版本，不是即兴回答；即兴版本往往更克制（见 §1.1 中她对"别上云"的反向澄清）。**

### 3.1 "82% of companies unknowingly give 3rd parties access to all their cloud data"（2021-02，独著）

- **来源 URL**：https://www.wiz.io/blog/82-of-companies-unknowingly-give-3rd-parties-access-to-all-their-cloud-data
- **信息性质**：[一手·亲笔] 独著。

#### 关键措辞

- 82% 的组织给第三方宽读取权限；典型路径是看似无害的 AWS `ReadOnlyAccess`（25% 厂商默认索取）。
- [一手·亲笔]："There is no real reason for any vendor to ask for permissions this broad."
- 把第三方权限定义为供应链风险，SolarWinds 与 Mimecast 之后 "a wake-up call"。
- [一手·亲笔]："Customers should be proactive and scrutinize every requested permission, while vendors should understand that 'Less is More.'"

### 3.2 "Security industry call to action: we need a cloud vulnerability database"（2021-11，与 Alon Schindel 合著）

- **来源 URL**：https://www.wiz.io/blog/security-industry-call-to-action-we-need-a-cloud-vulnerability-database
- **信息性质**：[合著] 与 Alon Schindel 合著。

#### 关键措辞与战略姿态

- 云漏洞处在 CSP 与客户责任之间的"灰色地带"，缺乏标准化披露/追踪/修复流程。
- [合著]：现有体系下云漏洞有 "no identifier or enumeration, no standard format, no severity scoring and no proper notification channel"。
- 三个案例（AWS 跨账号 confused deputy、OMIGOD、ChaosDB）展示同一模式：厂商响应修复但客户无法追踪是否受影响。
  - AWS 邮件通知的失效："never made it to the right person, or it got lost in a sea of other issues"。
  - OMIGOD："had no idea the OMI agents were installed in their environment"。
- [合著]：问题源于 "not from their lack of effort, but from a lack of standardization, transparency, and clear understanding of what each players' role is"。
- **战略行动**：Wiz 在 2022-06 启动 OPEN CVDB 作为这一愿景的实现。

#### 这篇文章对理解 Shir 的价值

这是 Shir 作为 Head of Research 的**行业议程推动表态**——她不仅在做研究，还在推动建立一个全新的漏洞披露标准。这与 §1.1 中 Cloud CVE Slack 频道、§2.2 中社区 GitHub 数据集构成一个连贯的战略姿态：**把单点发现转化为公共基础设施**。

### 3.3 "NotLegit: Azure App Service vulnerability exposed hundreds of source code repositories"（2021-12，独著）

- **来源 URL**：https://www.wiz.io/blog/azure-app-service-source-code-leak
- **信息性质**：[一手·亲笔] 独著。

#### 关键措辞

- 漏洞自 2017-09 起存在，可能已在野利用。
- [一手·亲笔]：攻击者只需 "fetch the '/.git' directory" 即可取回源码。
- 微软 web.config 含一个 typo，"the error raised by the typo ended up blocking access to the entire directory"——**用荒谬细节凸显系统性问题**的手法再次出现（见 §2.2 OMIGOD 同构）。
- [一手·亲笔]："cloud users did nothing wrong"——这是 Shir 区分"用户责任"与"平台责任"的标志性切分。
- 在野利用证据：Wiz 部署一个蜜罐 App Service，4 天内收到 "multiple requests for the .git folder from unknown actors"。
- **披露时间线**（详细记录，体现 Shir 对披露流程的重视）：10-07 报告 → 10-08 Microsoft 确认 → 10-19 triage call → 10-22 $7,500 赏金 → 11-17 PHP 修复部署 → 12-07 Microsoft 邮件通知客户。

### 3.4 "Compromised Microsoft Key: More Impactful Than We Thought"（2023-07，独著，Storm-0558 事件分析）

- **来源 URL**：https://www.wiz.io/blog/storm-0558-compromised-microsoft-key-enables-authentication-of-countless-micr
- **信息性质**：[一手·亲笔] 独著。

#### 关键措辞

- Microsoft 最初称仅 Exchange Online / Outlook.com 受影响；Shir 的研究发现被攻破的 MSA 签名密钥可为任何支持个人账户认证的 Azure AD 应用签发 OpenID v2.0 token——SharePoint、Teams、OneDrive、"Login with Microsoft" 客户应用、多租户应用（特定条件下）均受影响。
- **签名密钥的烈度定义** [一手·亲笔]：
  > "they are probably the most powerful secrets in the modern world" and are "much more powerful than TLS keys."
  这是 Shir 另一个**戏剧化类比**：把身份提供方签名密钥抬到"现代世界最强密钥"的位置，超过 TLS 密钥。与她 §2.1 的"nation-state level spying"手法同构。
- **非 Microsoft 专属问题的外推** [一手·亲笔]：if a signing key for any major identity provider "leaks, the implications are hard to comprehend"——把单点事件外推为行业级问题。
- **行业问责表态** [一手·亲笔]：
  > "our industry – and especially cloud service providers – must commit to a greater level of security and transparency."
- **可检测性疑虑** [一手·亲笔]：威胁者可离线伪造 token，"there is no trail in the Azure portal for token issuance"；应用级日志缺乏标准化，"exceedingly challenging"。
- **总结性表态** [一手·亲笔]：
  > "the full impact of this incident is much larger than we Initially understood it to be"
  > "will have long lasting implications on our trust of the cloud"
  > "the basic fabric of everything we do in cloud"（指身份层）
  同时保留未解问题（密钥如何被获取、何时、是否有其他密钥被攻破），称 "still an ongoing investigation"——**对不确定性的诚实承认**。

---

## 4. 合著研究文章（Shir 作为共同作者，"we" 集体声音）

下列文章 Shir 均为共同作者，无法剥离个人观点，仅作研究脉络与协作网络的参考：

| 日期 | 标题 | 合著者 | URL |
|---|---|---|---|
| 2025-12 | React2Shell: CVE-2025-55182 in-the-wild exploitation | Gili Tikochinski, Hila Ramati, Benjamin Read | 见 Wiz 博客作者页 |
| 2025-07 | NVIDIAScape: CVE-2025-23266 NVIDIA Container Toolkit 三行容器逃逸 | Nir Ohfeld | 见 Wiz 博客 |
| 2025-02 | NVIDIA AI vuln CVE-2024-0132 deep dive | Ronen Shustin, Andres Riancho | 见 Wiz 博客 |
| 2024-09 | NVIDIA AI vuln CVE-2024-0132 announcement | Ronen Shustin, Andres Riancho | 见 Wiz 博客 |
| 2024-05 | Replicate AI-as-a-Service critical vuln | Sagi Tzadik | 见 Wiz 博客 |
| 2024-04 | Hugging Face architecture risks | Sagi Tzadik | 见 Wiz 博客 |
| 2024-03 | K8s LAN Party Challenge | Nir Ohfeld | 见 Wiz 博客 |
| 2023-07 | GameOverlay: Ubuntu OverlayFS LPE (CVE-2023-2640 / -32629) | Sagi Tzadik | 见 Wiz 博客 |
| 2023-03 | BingBang: Bing.com takeover | Raaz Herzberg, Hillai Ben-Sasson | 见 Wiz 博客 |
| 2023-04 | #BrokenSesame: Alibaba Cloud Database RCE | Ronen Shustin | 见 Wiz 博客 |
| 2022-12 | Secret-based cloud supply-chain attacks | Alon Schindel | 见 Wiz 博客 |
| 2022-12 | Hell's Keychain: IBM Cloud Databases for PostgreSQL | Ronen Shustin | 见 Wiz 博客 |
| 2022-04 | ExtraReplica: Azure PostgreSQL cross-account | Ronen Shustin, Sagi Tzadik, Nir Ohfeld | https://www.wiz.io/blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql |

**作者页（完整 20 篇列表来源）**：https://www.wiz.io/blog/author/shir-tamari

#### 协作网络观察

- **最高频合著者**：Nir Ohfeld（多次，含 RSAC 2022 与 Black Hat EU 2022 两场大会同台）。
- **次高频**：Ronen Shustin、Sagi Tzadik、Alon Schindel。
- **跨职能合著**：与 Wiz CTO Ami Luttwak 合讲 Black Hat 2021；与 VP Product Raaz Herzberg + Hillai Ben-Sasson 合著 BingBang。
- **研究方向轨迹**：2021-2022 集中在 IaaS/PaaS 隔离（ChaosDB、OMIGOD、ExtraReplica、PostgreSQL、NotLegit、DNS）；2023 拓展到供应链与身份（Storm-0558、Hell's Keychain、BingBang、BrokenSesame、GameOverlay）；2024-2025 主线转向 AI 基础设施（Hugging Face、Replicate、NVIDIA Container Toolkit）。这条轨迹本身是 Shir 作为 Head of Research 的议程选择——**从云隔离边界转向 AI 边界**。

---

## 5. X / Twitter 活动（信息缺口）

- **任务线索**：Shir 在 X 上很活跃，发推披露过 AttachMe（Oracle Cloud）等。
- **本环境访问结果**：**未能获取任何 Shir 的 X 原推文内容**。web.archive.org 被 WebFetch 拒绝；X 直接抓取需要认证；DuckDuckGo 搜索未返回 Shir 的 X 推文存档。
- **AttachMe 博客核查**：在 Wiz 博客作者页（https://www.wiz.io/blog/author/shir-tamari）列出的 20 篇文章中**未见独立的 AttachMe 博客**；尝试 `https://www.wiz.io/blog/attachme` 与 `https://www.wiz.io/blog/oracle-cloud-attachme-vulnerability` 均返回 404。AttachMe（Oracle Cloud Instance Metadata，CVE-2022-21387）的 Wiz 披露博客**可能由不同作者署名或 URL slug 不同**，未能在本环境定位一手书面来源。
- **诚实标注**：任务线索中"Shir 在 X 上披露 AttachMe"的具体推文内容、措辞、即兴类比——**信息不足，不采信**。如需用于合成 Shir 视角，应额外抓取 X 原推或截图。

---

## 6. 未核实 / 拒绝采信的信息

下列信息来自**训练数据猜测或损坏的 WebSearch 返回**，**未采信**，仅记录以备后续核查：

1. **"Black Hat USA 2021 — Shir Tamari 与 Ami Luttwak 'Breaking the Cross-Account Encryption: How to Hack AWS KMS Service'"**：来自本环境损坏的 WebSearch 返回（自称"无工具"却给出训练数据）。该具体演讲标题**未在 Wiz 博客或 Black Hat 官方议程（403 未能核实）中得到确认**。已核实的是 Black Hat 2021 Shir 与 Ami 合讲的是 **DNS loophole**（见 §2.1），与上述"KMS"标题不符。**不采信，标记为可能的幻觉**。
2. **"ChaosDB / BleedingTA / TensorFlow"归属**：损坏 WebSearch 把 BleedingTA（TensorFlow 漏洞）归于 Shir，**未在 Wiz 博客作者页 20 篇列表中得到确认**，不采信。
3. **Shir 性别**：任务原文使用 "她"（中文 she/her）。Wiz 公开材料未在本环境明确核实性别。本文件为避免引入未经核实的性别假设，统一用"Shir"/"Tamari"/"她"（沿用任务原文用法），但**不对性别做事实声明**。
4. **任何来自知乎、微信公众号、百度百科的转述**：按任务黑名单规则，一律不采信。

---

## 7. 模式观察（供合成 Shir 视角使用）

把上述可引用素材归并，Shir 的对话/书面表达呈现几个稳定模式：

### 7.1 叙事手法
1. **"高烈度 × 低门槛"双轴类比**：nation-state spying "as easy as registering a domain"；签名密钥"现代世界最强密钥"。把技术漏洞拉到情报/治理量级 + 强调攻击门槛极低。
2. **荒谬细节凸显系统性问题**：OMIGOD 客户要更新"他们不知道存在的 agent"；NotLegit 的 typo 反而拦住了访问；ChaosDB "nobody stopped us, we expected an email"。用具体荒谬场景代替抽象指责。
3. **单点 → 跨厂商 → 行业级外推**：几乎每次披露都从"某厂商"扩展到"not limited to X"，再扩展到行业级议程（OPEN CVDB、社区数据集、Cloud CVE Slack）。

### 7.2 立场表态
4. **披露偏激进透明**：providers should be more transparent；假设有大量静默修复从未公开。
5. **但拒绝反云叙事**：被追问时反向澄清"上云仍比本地更安全"。**这是与她研究发现的最重要张力**——研究本身有爆炸性，但她主动限制解读。
6. **责任切分清晰**：反复用"cloud users did nothing wrong" / "not from their lack of effort, but from a lack of standardization" 把责任从个人/客户推向系统/标准化缺失。

### 7.3 战略姿态（Head of Research 的议程推动）
7. **把发现转化为公共基础设施**：OPEN CVDB、社区 agent 数据集、Cloud CVE Slack 频道——不只是发漏洞，而是建基础设施。
8. **研究方向选择跟随客户采用度**（"popularity-guided"，Nir 在 §1.1 表述）+ **跨厂商类比方法论**（"same exploit code working on multiple vendors"，§2.3）。
9. **Wiz 作为影响放大器的自我定位**（§1.1）——把 Wiz Research 定位为"影响运营"而非"发现机器"，与独立研究员（关注赏金）做切分。
10. **议程轨迹从云隔离边界转向 AI 边界**（§4 协作网络观察）——2024-2025 主线明显是 AI 基础设施（Hugging Face、Replicate、NVIDIA）。

### 7.4 对不确定性的态度
11. **对"是否已被在野利用"持不可知论**（DNS loophole "no way of knowing"）。
12. **对未解问题诚实承认**（Storm-0558 "still an ongoing investigation"）。
13. **不轻易用 CVE 包装**（PostgreSQL 跨厂商漏洞 "we could not issue a CVE"）——这反过来强化她对 OPEN CVDB 的议程推动。

---

## 8. 信息缺口清单（供后续补全优先级）

按对合成 Shir 视角的影响排序：

1. **高优先级缺口**：RSAC 2022 / Black Hat EU 2022 / CROC Talks YouTube 的现场字幕或逐字稿。这三场含可能的 Q&A 与即兴类比，本环境未能抓取。建议用带认证的 YouTube transcript 工具或人工转录补全。
2. **高优先级缺口**：Shir 的 X/Twitter 原推文，特别是 AttachMe 披露推文及任何即兴措辞。任务线索明确指出这是与 Nir/Hillai 不同的优势信息源，但本环境完全无法访问。
3. **中优先级缺口**：Black Hat / RSAC / fwd:cloudsec 议程归档的演讲摘要与 speaker bio（均 403）。
4. **中优先级缺口**：Darknet Diaries / CyberWire / Risky Business / Security Now 等第三方播客的出场。DuckDuckGo 未返回任何此类出场，但旧剧集（Darknet Diaries 1-147）未逐一核查。
5. **低优先级缺口**：Shir 的 LinkedIn（podcast appearance 列表可能在此）。LinkedIn 999 反爬。
6. **低优先级缺口**： fwd:cloudsec 历年演讲。Shir 是否在 fwd:cloudsec 出场未核实。

---

## 9. 来源索引（仅列已核实可访问的）

| # | 来源 | URL | 类型 | 可信度 |
|---|---|---|---|---|
| S1 | Screaming in the Cloud Ep.307 节目页 | https://www.lastweekinaws.com/podcast/screaming-in-the-cloud/find-fix-and-eliminate-cloud-vulnerabilities-with-shir-tamari-and-company/ | 播客节目笔记 | 高 |
| S2 | CROC Talks: Hugging Face Hub 节目页 | https://www.wiz.io/crying-out-cloud/croc-talks-helping-secure-hugging-face-hub-special-guest-shir-tamari | 播客节目笔记 | 高 |
| S3 | CROC Talks YouTube 版 | https://www.youtube.com/watch?v=UvsSuh4MfuA | 视频（字幕未获取） | 高（存在性）/ 低（内容） |
| S4 | Wiz 博客作者页（Shir Tamari 20 篇） | https://www.wiz.io/blog/author/shir-tamari | 作者归档 | 高 |
| S5 | The Cloud Gray Zone 文章 | https://www.wiz.io/blog/the-cloud-gray-zone-secret-agents-installed-by-cloud-service-providers | 合著文章 | 高 |
| S6 | Cloud vulnerability database 呼吁 | https://www.wiz.io/blog/security-industry-call-to-action-we-need-a-cloud-vulnerability-database | 合著文章 | 高 |
| S7 | 82% of companies 文章 | https://www.wiz.io/blog/82-of-companies-unknowingly-give-3rd-parties-access-to-all-their-cloud-data | 独著文章 | 高 |
| S8 | Storm-0558 / Compromised Microsoft Key | https://www.wiz.io/blog/storm-0558-compromised-microsoft-key-enables-authentication-of-countless-micr | 独著文章 | 高 |
| S9 | Black Hat 2021 DNS loophole | https://www.wiz.io/blog/black-hat-2021-dns-loophole-makes-nation-state-level-spying-as-easy-as-registering-a-domain | 合著文章 | 高 |
| S10 | NotLegit | https://www.wiz.io/blog/azure-app-service-source-code-leak | 独著文章 | 高 |
| S11 | The cloud has an isolation problem | https://www.wiz.io/blog/the-cloud-has-an-isolation-problem-postgresql-vulnerabilities | 合著文章 | 高 |
| S12 | ExtraReplica | https://www.wiz.io/blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql | 合著文章 | 高 |
| S13 | Darknet Diaries 剧集列表 148-177 | https://darknetdiaries.com/episode/ | 剧集归档 | 高（无 Shir 出场） |
| U1 | RSAC 2022 YouTube（未抓取） | https://www.youtube.com/watch?v=QNKT7ocTibk | 视频 | 存在性高/内容未获取 |
| U2 | Black Hat EU 2022 YouTube（未抓取） | https://www.youtube.com/watch?v=X6CiUD3EcfQ | 视频 | 存在性高/内容未获取 |

---

**总结**：本环境成功获取的最有价值的 Shir 即兴/对话素材是 **Screaming in the Cloud Ep.307（2022-01）** 的节目笔记，其中保留了多条直接引语，覆盖披露哲学、Wiz 自我定位、云 vs 本地立场、ChaosDB 发现叙事。第二手是 **CROC Talks（2024-04）** 但仅有主题摘要。会议演讲与 X 活动的实际即兴内容在本环境存在系统性访问缺口，已在 §8 列出供后续补全。Shir 的战略姿态（透明议程、公共基础设施构建、跨厂商类比、AI 边界转向）从其书面文章中得到强一致印证。

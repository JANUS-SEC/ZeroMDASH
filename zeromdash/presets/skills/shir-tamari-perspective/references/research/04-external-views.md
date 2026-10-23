# Shir Tamari — 他者视角

> 本文档专门记录**别人怎么评价、批评、对比 Shir Tamari**。
> 每条标注来源 URL 与可信度，并显式区分三类陈述：
> - **「她说过」**：Shir Tamari 本人公开发表的言论（本文档中较少，因为本文件主题是"他者视角"，且她的 X/Twitter 账号 @shirtamari 在调研期间处于付费墙后，未能直接抓取一手言论）
> - **「别人说她」**：媒体、社区、厂商、同行对 Shir 及其研究的直接评价
> - **「你（调研者）推断」**：基于多条证据综合出的推断，非原始引用

信息源黑名单遵守：未使用知乎、微信公众号、百度百科。

---

## 〇、身份与署名基线（外部视角的前提）

在进入"他者视角"前，先固定几条经过一手核验的事实，因为外部评论往往把"Wiz Research 团队作品"与"Shir 个人作品"混为一谈。

### 0.1 「Head of Research」头衔的公开可证实性

- 来源：Wiz About 页面 https://www.wiz.io/about
- 可信度：高（一手公司页面，2026-07 抓取）
- 「别人说她」（实际是沉默）：**Wiz About 页面的领导层名单中并不包含 Shir Tamari**。领导层列出 CEO Assaf Rappaport、CTO Ami Luttwak、VP Product Yinon Costica、VP R&D Roy Reznik、President & COO Dali Rajic、President & CFO Fazal Merchant、CBO Adi Leist Sharon、CSO Anthony Belfiore、**CMO & VP Product Strategy Raaz Herzberg**、GC Nir Dagan、Head of Product Mattan Shalev、VP Finance Liron Grosman、CIO & CISO Ryan Kazanciyan——**没有任何"Head of Research"或研究条线领导岗位**。
- 来源（旁证）：Nir Ohfeld perspective skill `references/research/04-external-views.md`（同仓库内）
- 可信度：中（同仓库内 Nir skill 是已构造的研究产物，非一手）
- 「你（调研者）推断」：Shir 的"Head of Research"头衔**未被 Wiz 官方页面公开背书**。该头衔来自用户任务简报与 Nir skill 的内部定位（Nir skill 第 385 行把 Shir 描述为"Wiz Head of Research，战略层合作者，直接上级"，第 387 行说 Hillai Ben-Sasson "取代 Shir 位置"成为 2024-2025 主合作者）。结合 Wiz About 沉默 + Nir skill 把她定位为 Nir 直接上级 + 用户简报，可以**有把握地推断**她在 Wiz 内部确为研究条线负责人，但 Wiz 对外**刻意不在 About 页突出研究个人**——这与 Nir skill 已观察到的"Wiz 把研究团队作为功能性资产而非个人品牌对外展示"模式一致。

### 0.2 Shir 个人署名作品 vs Wiz 团队作品（外部评论混用的重灾区）

- 来源：Wiz 博客作者页 https://www.wiz.io/blog/author/shir-tamari（2026-07 抓取）
- 可信度：高（一手作者索引）
- 「别人说她」（署名事实）：Shir 在 Wiz 博客上以**第一作者/lead author** 署名的作品共 20 篇，覆盖 2021-02 至 2025-12。最具代表性的：
  - 2021-02「82% of companies unknowingly give 3rd parties access to all their cloud data」（个人）
  - 2021-08「Black Hat 2021: DNS loophole makes nation-state level spying as easy as registering a domain」（个人）
  - 2021-11「Security industry call to action: we need a cloud vulnerability database」（+ Alon Schindel）
  - 2021-12「NotLegit: Azure App Service vulnerability exposed hundreds of source code repositories」（个人）
  - 2022-04「ExtraReplica」（+ Ronen Shustin, Sagi Tzadik, Nir Ohfeld）
  - 2022-06「The cloud gray zone—secret agents installed by cloud service providers」（+ Nir Ohfeld）
  - 2022-08「The cloud has an isolation problem: PostgreSQL vulnerabilities affect multiple cloud vendors」（+ Ronen, Nir, Sagi）
  - 2022-12「Hell's Keychain」（IBM Cloud，+ Ronen Shustin）
  - 2022-12「Secret-based cloud supply-chain attacks」（+ Alon Schindel）
  - 2023-03「BingBang」（+ Raaz Herzberg, Hillai Ben-Sasson）
  - 2023-04「#BrokenSesame」（Alibaba Cloud，+ Ronen Shustin）
  - 2023-07「GameOver(lay): Ubuntu OverlayFS」（+ Sagi Tzadik）
  - 2023-07「Compromised Microsoft Key: Storm-0558」（个人）
  - 2024-03「K8s LAN Party Challenge」（+ Nir Ohfeld）
  - 2024-04「Hugging Face AI-as-a-Service 架构风险」（+ Sagi Tzadik）
  - 2024-05「Replicate AI 漏洞」（+ Sagi Tzadik）
  - 2024-09「NVIDIA Container Toolkit CVE-2024-0132」（+ Ronen Shustin, Andres Riancho）
  - 2025-02「NVIDIA deep dive」（+ Ronen, Andres）
  - 2025-07「NVIDIAScape CVE-2025-23266」（+ Nir Ohfeld）
  - 2025-12「React2Shell CVE-2025-55182 在野利用」（+ Gili Tikochinski, Hila Ramati, Benjamin Read）
- 「你（调研者）推断」（关键）：**外部社区与媒体最尖锐的批评（"敲诈"、"CVSS 闹剧"、"不负责任披露"、"越界渗透测试"）几乎全部指向 Shir 未亲自署名的 Wiz 团队作品**——SAPwned（主笔 Hillai Ben-Sasson）、DeepSeek 数据库泄露（主笔 Gal Nagli）、RediShell Redis RCE、CodeBreach AWS CodeBuild、Microsoft AI 38TB 等。Shir 作为 Head of Research 对这些作品负有结构性责任，但若把批评直接挂在 Shir"个人"头上会失真。下文会逐条标注「Shir 个人作品」vs「Shir 督导的团队作品」。
- 「别人说她」（HN 讨论度反差）：HN Algolia 检索显示，Shir 个人署名作品在 HN 上**整体参与度偏低**——ExtraReplica 60 分 / 15 评论是她个人作品里讨论度最高的一次；Cloud Gray Zone 21 分 / 0 评论；BingBang 5 分 / 0 评论；BrokenSesame 3 分 / 0 评论；Hugging Face 4 分 / 0 评论；Hell's Keychain 2 分 / 0 评论；NVIDIAScape 2 分 / 0 评论；React2Shell 1-2 分 / 0-1 评论。**对比同期 Wiz 团队作品**——DeepSeek 707 分 / 474 评论、Microsoft AI 38TB 721 分 / 226 评论、SAPwned 254 分 / 66 评论、CodeBreach 160 分 / 38 评论、RediShell 143 分 / 56 评论——**差一个数量级**。这意味着 Shir 的公众形象更多由她督导的团队作品塑造，而非她个人署名作品。

### 0.3 AttachMe（Oracle Cloud）的署名纠偏

- 来源：Nir skill 第 181 行；Wiz 博客作者页
- 可信度：高
- 「别人说她」（纠偏）：用户任务简报把 AttachMe（Oracle Cloud 跨租户卷访问漏洞，CVE-2022-21416）列入 Shir 的代表作。但 **Wiz 博客作者页未把 AttachMe 列在 Shir 名下**，Nir skill 明确指出"AttachMe 由 Elad Gabay 单独署名（非 Nir）"。HN 上确实有一个 objectID 32917973 的故事"Oracle Cloud vulnerability allowed users to access disks of other customers"指向 Shir 的推特 @shirtamari——这说明 **Shir 在 X 上发推扩散了 AttachMe，但她不是研究主笔**。这种"非主笔但发推披露"的现象是把她和团队作品绑定的根源之一，社区评论者往往把推特发推者当作研究主笔。

---

## 一、媒体报道基调

### 1.1 Wiz 官方博客的自媒体基调（一手）

- 来源：ExtraReplica 博客 https://www.wiz.io/blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql/
- 来源：BrokenSesame 博客 https://www.wiz.io/blog/brokensesame-accidental-write-permissions-to-private-registry-allowed-potential-r
- 来源：Hell's Keychain 博客 https://www.wiz.io/blog/hells-keychain-supply-chain-attack-in-ibm-cloud-databases-for-postgresql
- 来源：React2Shell 博客 https://www.wiz.io/blog/nextjs-cve-2025-55182-react2shell-deep-dive
- 可信度：高（一手原始披露文档）
- 「别人说她」（基调归纳）：Shir 领衔的披露博客基调被调研者归纳为"克制 + 厂商赞美 + 团队署名"三件套：
  - **克制**：ExtraReplica、BrokenSesame、Hell's Keychain 都以"disclosure timeline"为骨架，技术描述分章节展开，语调中性偏专业。
  - **厂商赞美**：BrokenSesame 写阿里巴巴的"professional conduct and open communication throughout the disclosure process serve as an exemplary model for other vendors"；Hell's Keychain 引用 IBM Cloud CISO Jerry Bell 的话"I greatly appreciate the partnership and professionalism of Wiz's security team"——Wiz **主动把厂商的赞美嵌进披露博客**，与 P0/Tavis Ormandy 等独立研究员的疏离姿态形成对比。
  - **团队署名**：所有披露都是"Wiz Research Team"集体署名，Shir 即便是第一作者也不突出个人。Hell's Keychain 在文末列出 Nir Ohfeld、Sagi Tzadik 作为团队成员（与 Shir、Ronen 并列），SAPwned 的正式 byline 是 Hillai Ben-Sasson 但文末"Stay in touch!"列出 Shir/Nir/Sagi/Ronen/Hillai 五人 Twitter 链接。
- 「你（调研者）推断」：这种"赞美厂商 + 集体署名"基调是 Shir 领导下 Wiz Research 的风格标识，也是社区批评"商业驱动型研究"的诱因之一——独立研究员圈（P0 谱系）几乎不会在披露博客里嵌厂商背书。

### 1.2 主流媒体抓取受限说明

- The Register、BleepingComputer、KrebsOnSecurity、TechCrunch、Forbes、Dark Reading 的 Shir 署名研究直接报道 URL 在本次调研中多数返回 403/404 或不在白名单内（arstechnica.com 被 WebFetch 拒绝）。这是源可用性问题，并非否定其存在。
- 来源（间接）：The Register 关于 React2Shell 的报道"China, Iran are having a field day with React2Shell, Google warns"（HN objectID 46279790）
- 可信度：中（通过 HN 转引间接还原）
- 「别人说她」：The Register 把 React2Shell 与中国/伊朗国家级利用挂钩，并声称"Google warns"。但 **Wiz 自己的 React2Shell 博客并未提及 Google 警告或中国/伊朗归属**——这意味着 The Register 的国家级归属与"Google warns"来自第三方（可能是 Google 的 Mandiant/Threat Intelligence Group 单独通报），而非 Shir 团队的原始披露。媒体把"在野利用"升级为"国家级攻击"是常见放大路径，但 Wiz 博客本身的措辞更克制。
- 「你（调研者）推断」：媒体对 Shir 团队研究的总体框架是「灾难性云/AI 漏洞 + 在野利用 + 国家级归属」三层叠加，而 Wiz 自己的披露往往只负责第一层（漏洞 + 在野利用），后两层常由媒体放大。这种"披露—媒体放大"链条会放大批评："为什么不先把漏洞修了再公开"这类针对 DeepSeek 的"不负责任披露"指控（见 4.5）正是冲着这条链条来的。

---

## 二、Hacker News 社区讨论（同行评价的核心场域）

HN 是 Shir Tamari 研究最集中的公开讨论场。下面按事件分组列出原始评论（**「别人说她」**）。**重要前提**：Shir 个人署名作品的 HN 讨论度普遍很低（见 0.2），所以本节既收录她个人作品的讨论，也收录她作为 Head of Research 督导的团队作品讨论——后者才是社区批评最集中的地方。

### 2.1 ExtraReplica 帖子（60 points, 15 comments）——Shir 个人作品里讨论度最高的一次

- 来源：https://news.ycombinator.com/item?id=31213335
- 来源（Algolia API）：https://hn.algolia.com/api/v1/items/31213335
- 可信度：高（HN 原始评论，objectID 31213335，2022-04-30）
- 署名：Shir Tamari + Ronen Shustin + Sagi Tzadik + Nir Ohfeld（Wiz 博客 byline 确认）

**对 Azure 整体安全文化的批评（把 Shir 团队的发现视作 Azure 系统性问题的证据）：**

- **0xy**（31214275）：「Azure seems to be shaping up to be a security joke, there's been a concerning number of cross-account exploits in the last couple of years. AWS isn't perfect, but you really don't see many exploits on this scale.」——**把 Shir 团队的连续发现归为 Azure 不值得信任的证据**。
- **alexjurkiewicz**（31214379）：「There's a certain level of tech schaudenfreude when it comes to Microsoft failing.」
- **redwood**（31215903）：「Wow after the same researchers discovered something similar in Cosmos DB last year. Unreal that Azure is used by anyone」——**"the same researchers"指 Wiz 团队，把其研究连续性当作 Azure 系统失能的证据**。
- **eurasiantiger**（31214188）：劝客户远离 Azure，称其本质是 lock-in 陷阱。
- **sylens**（31214640）：平衡论调——Azure 跨账户漏洞确实多，但 AWS 在 CloudFormation/Glue 也有类似披露，AWS 可能"sweep security issues under the rug if there is no customer impact"。

**关键的 Wiz CEO 阴谋论（与 Shir 工作相关，社区中反复出现的论调）：**

- **mola**（31214459）：「Wasn't Wiz CEO previous job leading Microsoft Israel RnD? After his previous cyber security startup (Adallom) was aquired by Microsoft? Azure security stance was under his supervision. Kind of ironic that his new security startup uncovers his failings at his old job...」——**直接把 Shir 团队在 Azure 上的发现与 CEO Assaf Rappaport 之前在 Microsoft Israel R&D 的"失职"挂钩**。这是 Shir 研究在 HN 上引发的最具阴谋论色彩的评论，下文 4.1 节专门展开。

**spacemanmatt**（31214596）：「It's sub-ironic, though. Microsoft has been delivering tech fails for decades.」

### 2.2 Cloud Gray Zone 帖子（21 points, 0 comments）——Shir + Nir Ohfeld 合著

- 来源：https://hn.algolia.com/api/v1/items/31709506（objectID 31709506，2022-06-11）
- 可信度：高
- 「别人说她」（实际是讨论度极低）：21 分但 **0 评论**——意味着 HN 读者点了一点但没有讨论。这篇关于云厂商"secret agents"的研究是 Shir 与 Nir 合著的少数非漏洞类研究，社区可见度低，无批评材料。
- 「你（调研者）推断」：Cloud Gray Zone 不是"漏洞披露"而是"行业观察"类研究，缺少可爆点，HN 社区对此类研究反应冷淡。这说明 Shir 团队的"非漏洞"研究即便署名是她，也几乎不入社区视野。

### 2.3 BingBang 帖子（5 points, 0 comments）——Shir + Raaz Herzberg + Hillai Ben-Sasson

- 来源：https://hn.algolia.com/api/v1/items/35370217（objectID 35370217，2023-03-30）
- 可信度：高
- 「别人说她」（实际是零评论）：5 分 0 评论，社区几乎无反应。
- 「你（调研者）推断」（关键）：BingBang 的署名结构 **Shir Tamari + Raaz Herzberg + Hillai Ben-Sasson** 值得特别记录——Raaz Herzberg 是 Wiz 的 **Chief Marketing Officer & VP Product Strategy**（见 0.1 节 Wiz About 页）。**Wiz 的 CMO 亲自挂名安全研究披露**，在独立研究员圈子里极为罕见，是"研究与营销深度绑定"指控（见 4.2）的最直接证据。Nir skill 第 410 行明确撇清"BingBang 不是我的作品"，把署名归给 Raaz/Shir/Hillai 三人——这与 Shir 在 Nir 升任战略层后把 hands-on 研究交给 Hillai 的趋势一致。

### 2.4 BrokenSesame 帖子（3 points, 0 comments）——Shir + Ronen Shustin（Alibaba Cloud）

- 来源：https://hn.algolia.com/api/v1/items/35634378（objectID 35634378，2023-04-19）
- 可信度：高
- 「别人说她」（实际是零评论）：3 分 0 评论。
- 「你（调研者）推断」：BrokenSesame 是 Shir 在 Alibaba Cloud 上的代表研究，HN 上几乎无讨论。结合 Nir skill 2.7 节观察（AttachMe 在 Oracle 上的研究"HN 上几乎无讨论"），**Shir 在非 Microsoft 厂商上的研究社区共鸣度比她在 Azure 上更低**——HN 受众以英语圈/SV 为主，对 Alibaba Cloud 关注度天然偏低。

### 2.5 Hell's Keychain 帖子（2 points, 0 comments）——Shir + Ronen + Nir + Sagi（IBM Cloud）

- 来源：https://hn.algolia.com/api/v1/items/33823695（objectID 33823695，2022-12-01）
- 可信度：高
- 「别人说她」（实际是零评论）：2 分 0 评论。
- 「你（调研者）推断」：与 BrokenSesame 类似，IBM Cloud 在 HN 受众中份额不高。但 IBM Cloud CISO Jerry Bell 在 Wiz 博客里公开背书"I greatly appreciate the partnership and professionalism of Wiz's security team"——这是 Shir 团队**主动公开的厂商赞美**，独立研究员圈不会这样做。

### 2.6 Hugging Face 帖子（4 points, 0 comments）——Shir + Sagi Tzadik

- 来源：https://hn.algolia.com/api/v1/items/39935267（objectID 39935267，2024-04-04）
- 可信度：高
- 「别人她说」（实际是零评论）：4 分 0 评论。
- 「你（调研者）推断」：尽管 Hugging Face 是 AI 圈顶流，但 Wiz 的 Hugging Face 研究在 HN 上零讨论——可能因为该研究是"架构风险"而非"RCE 漏洞"，缺乏爆点。后续 Replicate 研究（同样 Shir + Sagi）甚至没有 HN 帖子。

### 2.7 NVIDIAScape 帖子（2 points, 0 comments）——Shir + Nir Ohfeld

- 来源：https://hn.algolia.com/api/v1/items/44595437 与 44604030（2025-07-17/18）
- 可信度：高
- 「别人她说」（实际是零评论）：2 分 0 评论（两个帖子合计）。
- 「你（调研者）推断」：NVIDIAScape 是 NVIDIA Container Toolkit 的"三行容器逃逸"——技术上极有冲击力，但 HN 讨论度极低。这与同期 Wiz 博客作者页 Shir 名下另一篇 NVIDIA 研究（2024-09，4 分 0 评论）一致，说明 **Shir 的 NVIDIA 系列研究在 HN 上未引发共鸣**，社区对 NVIDIA Container Toolkit 的关注度远低于对 Azure/Alibaba/AI 平台。

### 2.8 React2Shell 帖子（低参与度）——Shir + Gili Tikochinski + Hila Ramati + Benjamin Read

- 来源：https://hn.algolia.com/api/v1/items/46160215（objectID 46160215，2025-12-05，"React2Shell Exploit Analysis with POCs (RCE in Next.js)"，1 分 1 评论——评论来自发帖人 freeqaz 自荐）
- 来源：https://hn.algolia.com/api/v1/items/46279790（objectID 46279790，2025-12-15，"China, Iran are having a field day with React2Shell, Google warns"，2 分 0 评论）
- 来源：https://hn.algolia.com/api/v1/items/46217085（objectID 46217085，2025-12-10，"Ask HN: Post-CVE-2025-55182 – should we be auditing for backdoors?"，2 分 0 评论）
- 可信度：高
- 「别人她说」（实际是讨论度极低）：三条帖子合计 5 分 1 评论（且评论是发帖人自荐）。
- 「她说过」（Wiz 博客原文）：React2Shell 是 Shir 在 Wiz 博客上以 lead author 署名的最新作品（2025-12-08），博客描述了"在野利用 + 凭据收割 + 云后门"。**Wiz 博客本身没有提及 Google 警告或中国/伊朗归属**。
- 「别人她说」（媒体放大）：The Register（HN 46279790）把 React2Shell 与"China, Iran field day""Google warns"绑定，但 Wiz 博客未做此归属。
- 「你（调研者）推断」：React2Shell 是 2025-12 在野利用 CVE 中较被忽视的一个——Next.js 生态的 CVE-2025-55182 在 HN 上没有爆发讨论，可能因为：(1) Wiz 自身定位为"深度技术分析"而非首披露；(2) Next.js 圈与云安全圈受众重合度低；(3) Google Mandiant 单独的国家级归属通报抢走了话题。

### 2.9 Wiz 团队作品（Shir 非主笔但作为 Head of Research 督导）——批评最集中

下面四条 HN 帖子的批评**不直接挂在 Shir 个人头上**，但作为 Head of Research，她对团队输出负有结构性责任。这些是社区对"Wiz Research 整体"最尖锐的批评，不可避免地波及她的领导形象。

#### 2.9.1 DeepSeek 数据库泄露（707 points, 474 comments）——主笔 Gal Nagli

- 来源：https://hn.algolia.com/api/v1/items/42871371
- 可信度：高（最高 HN 参与度的 Wiz 披露之一）
- 「别人说她」（Wiz 团队整体批评， Shir 非主笔）：
  - **nico**（42872345）：「So much effort in trying to tarnish DeepSeek the last 24hrs」——把 Wiz 的披露视为对 DeepSeek 的抹黑运动。
  - **tomlockwood**（42872356 → 42872454 修订）：「This doesn't look like a responsible disclosure, at all.」后修订为"I was wrong!"，但追加：「The direct disclosure of urls and ports is insane. Wonder if they would be as irresponsible if it was MSFT, OpenAI, Anthropic, etc.」——**指控 Wiz 对中国厂商 DeepSeek 比对美国厂商更不负责任**。
  - **mandmandam**（42872385）：暗示 DeepSeek 受到不公正针对——「the implication is at deep seek is somehow special and is getting undue attention from hackers」。
  - **megous**（42872786）：「if serious company that seems to offer services to seemingly plenty of serious customers acts this way, I'd not want to be their customer」——把 Wiz 自己当作不可信合作伙伴。
  - **caust1c**（42872846）：「I'm guessing Wiz wanted to ride the current media wave with this post instead of seeing how far they could take it.」——**最直白的"蹭热度"指控**。
  - **khazhoux**（42873622）：「there are a lot of unscrupulous western companies with a lot to lose who might have an interest in convincing certain people to skip responsible disclosure」——把 Wiz 披露政治化。
  - **kdmtctl**（42873676）：「I think that was a shameless self promotion. A lot of PR and free traffic by taking a low hanging fruit.」——**"无耻自我宣传"**。
  - **rnd0**（42876520）：「It would be very nice if the press didn't just fall over itself trying to be a free PR agency for OpenAI.」
  - **pedrovhb**（42873238）：「Security researchers are often asked to not pursue findings further than confirming their existence.」——暗示 Wiz 越界。
- 「你（调研者）推断」：DeepSeek 是 Wiz Research 团队**史上最严重的"不负责任披露"指控集中地**。Shir 作为 Head of Research 虽未亲自署名（主笔 Gal Nagli），但披露策略、博客基调、媒体联动属于她督导演进范围。这次事件首次让"披露伦理"成为针对 Wiz 整体的主流批评——比 SAPwned 的"敲诈"指控更具传播力。

#### 2.9.2 SAPwned（254 points, 66 comments）——主笔 Hillai Ben-Sasson

- 来源：https://hn.algolia.com/api/v1/items/40990768
- 可信度：高（高参与度，批评与辩护并存）
- 署名：Wiz 博客正式 byline 为 **Hillai Ben-Sasson**，文末"Stay in touch!"列出 Shir、Nir、Sagi、Ronen、Hillai 五人。**Shir 非主笔但出现在团队列表**。
- 「别人说她」（Wiz 团队整体批评）：
  - **darefalcon**（40999094）：「Companies that penetrate networks uninvited looking for vulnerabilities to create blog content should be prosecuted IMHO.」+「This piece in particular sounds like a hit piece thinly vailed as a vulnerability disclosure.」+「Sounds kinda like extortion.」——**直接把 Wiz 研究模式类比为敲诈**。这是 Shir 领导下 Wiz Research 遭遇的最尖锐单条指控。
  - **rvnx**（41000674）：「It's a crime, anything who tries to hack a large company without being invited would get seriously prosecuted」+「If you have billions of USD, laws don't apply to you anymore.」
  - **tiffanyh**（40996120）：转向 Wiz 商业成功——「$100M in just 1.5 years time」「$350M at end of 3-year」，把披露与商业估值正相关化。
  - **rtev**（40997001）：「About to be acquired by Google for $23 billion as well!」
  - **chatmasta**（40991493）：淡化严重性——「The blurring/pixelation is arguably unnecessary... The censored data looks like local host names and some image hashes.」
- **为 Wiz 辩护的声音**：
  - **ppbjj**（40999432）：「Are you serious?」
  - **_dain_**（41099642）：「way to shoot the messenger.」
- 「你（调研者）推断」：SAPwned 是 Shir 领导下 Wiz Research 团队**第一次被系统性指控"敲诈/越界"**。Hillai 作为主笔接下了火力，但作为 Head of Research 的 Shir 对"取得 cluster admin 级访问是否越界"这一披露伦理问题负有责任。Nir skill 4.1 节的观察仍适用——这是 Wiz 研究模式与独立研究员圈（P0 谱系，披露前严守最小必要访问）的根本分歧。

#### 2.9.3 Microsoft AI 38TB（721 points, 226 comments）——Shir 非主笔

- 来源：https://hn.algolia.com/api/v1/items/37556605
- 可信度：高（最高 HN 参与度的 Wiz 披露之一）
- 署名：未出现在 Shir 的 Wiz 博客作者页 20 篇列表中，**非 Shir 主笔**。
- 「别人说她」（Wiz 团队整体批评）：
  - **buro9**（37556991）：暗示这是销售话术——「obviously that's the sales pitch... you need this vendor's monitoring and security」。
  - **sillysaurusx**（37557209）：「The article tries to play up the AI angle, but this was a pretty standard misconfiguration of a storage token.」——**淡化 AI 角度，指 Wiz 把普通配置错误包装成 AI 安全问题**。
  - **intrasight**（37557535）：「Agreed. It should say... But as clickbait worthy a title.」
  - **munchler**（37557135）：「This is the risk of using, checks notes, Azure and working with Microsoft.」
  - **acdha**（37558526）：「It didn't seem to be focused on AI except for the very reasonable concerns that AI research involves lots of data」——AI 包装批评。
- **为 Wiz 辩护**：
  - **spullara**（37559934）：「Not really a sales pitch as it wasn't discovered by their product but rather by their security team doing a bunch of manual work.」
- 「你（调研者）推断」：38TB 披露首次让"AI 安全议题被 Wiz 用于自我营销"成为社区主流叙事。Shir 领导下 Wiz Research 从云隔离转向 AI 安全赛道（Hugging Face、Replicate、NVIDIA、SAP AI、DeepSeek、Microsoft AI），这条赛道在 HN 引发更多"AI 包装"批评。

#### 2.9.4 CodeBreach AWS CodeBuild（160 points, 38 comments）——Shir 非主笔

- 来源：https://hn.algolia.com/api/v1/items/46636093
- 可信度：高
- 署名：未出现在 Shir 的 Wiz 博客作者页 20 篇列表中（2026-01 发布，晚于 React2Shell），**非 Shir 主笔**。
- 「别人说她」（Wiz 团队整体批评）：
  - **btown**（46640673）：「From everything I know about pentesting, they should have stopped before doing this, right?」引用 AWS HackerOne 政策"You may only interact with accounts you own or with explicit written permission"——**指控 Wiz 越界，把自己加为 repo admin**。
  - **rand846633**（46644990）：「I'd guess that we would not have had the pleasure of reading this article if wiz was payed by AWS.」——**暗示 Wiz 因未获 AWS 赏金而公开披露作为谈判筹码**。还提到 2025 年其他研究者"had to turn down small six figure bounties to avoid NDAs"。
  - **az226**（46643192）：「It's possible that AWS is a Wiz customer, which would allow them to do more stuff.」——质疑 Wiz 与 AWS 的商业关系是否给了越界特权。
  - **InitialBP**（46646073）：暗示 Wiz 这种升级可能是 performative——"a CISO wants a 'massive compromise' demonstrated to secure budget"，把 Wiz 的研究模式比作 CISO 预算博弈工具。
- 「你（调研者）推断」：CodeBreach 是 Shir 领导下 Wiz Research **首次被指控在 AWS 上越界**——此前 Nir skill 4.6 节观察到"未发现针对 AWS 服务的同级 Nir Ohfeld 署名研究"。Shir 团队把矛头从 Microsoft/Oracle/Alibaba/IBM/SAP 转向 AWS，是策略性扩展，但 AWS HackerOne scope 比 Microsoft 更严格，使 Wiz 的"披露—研究"边界更模糊。

#### 2.9.5 RediShell Redis RCE（143 points, 56 comments）——Shir 非主笔

- 来源：https://hn.algolia.com/api/v1/items/45497027
- 可信度：高
- 署名：未出现在 Shir 的 Wiz 博客作者页 20 篇列表中，**非 Shir 主笔**。
- 「别人她说」（CVSS 评分注水指控）：
  - **tptacek**（45498273, 45498686, 45498462, 45499196）：连续多条评论——「A post-auth memory corruption vulnerability scores a CVSS 10. Shellshock got like a 9.5. These scores don't mean anything.」+「Bugs get whatever CVSS the marketing team for the discovering research lab wants them to get. It's literally a Ouija board.」+「this CVSS stuff is a farce and everyone seriously working in the field seems to agree」+「it is not of a caliber to rank among the most severe vulnerabilities ever discovered, which is what a CVSS score of 10 means.」——**Thomas Ptacek（知名独立安全研究员）直接把 CVSS 评分机制等同于"marketing team 玩占卜板"**，是对 Wiz Research 披露文化最权威的同行批评之一。
  - **TheDong**（45498675）：「the number of redis setups out there which rely on user-uploaded lua scripts and the lua sandbox being sufficient for that has got to be... close to 0?」+「Seems wild that something which requires using the thing wrong, and also which impacts close to 0 real deployments of the thing, gets a CVSS 10.」——**质疑实际影响近乎零却给 CVSS 10**。
  - **zb3**（45498541）：「Post-auth, so this shouldn't be CVSS 10 (highest possible score), because that implies pre-auth RCE would not be more critical..」
  - **bawolff**（45501778）：「Feels a little overstated if it requires a malicious lua script.」「its not critical the way the article implies.」
  - **SkyPuncher**（45517402）：「this is rather poor reporting and feels a bit flashy for a security researcher to make a name for themselves.」「if you're vulnerable to this, you were already at major risk anyways.」——**"研究者靠 flashy 报道出名"**。
  - **baobun**（45499173）：质疑 CVSS 表"Privileges required: low"——「Exploitation would need authentication or a separate auth bypass.」
  - **champtar**（45498016）：「140 days response time seems rather slow for such a critical vulnerability」
- 「你（调研者）推断」：RediShell 是 Shir 领导下 Wiz Research 遭遇的**最权威同行技术批评**——Thomas Ptacek 是独立研究员圈的标杆人物，他的"CVSS = marketing team 玩占卜板"判定比 SAPwned 上 darefalcon 的"敲诈"指控更具同行内影响力，因为它来自圈内人而非圈外质疑者。这次批评直接打在 Wiz Research 的"severity 包装"风格上，对 Shir 的研究督导演进是显著警示。

### 2.10 Wiz 收购帖（$32B）——对 Wiz 商业模式的全面审视（间接波及 Shir）

- 来源：https://hn.algolia.com/api/v1/items/43393259（"Alphabet in Talks to Buy Cloud Security Firm Wiz for $33B"，59 points，15 top-level comments）
- 可信度：高
- 「别人说她」（实际是对 Wiz 整体，Shir 作为研究负责人间接被波及）：
  - 收购帖主要讨论 Google 收购 Wiz 后会获得对 AWS/Oracle/Azure 客户云的洞察，以及对 Unit 8200 创始人背景的担忧。Nir skill 2.5 节已详尽记录——dhx「Whoever owns Wiz obtains read only access to large company and government cloud networks」、rvnx 单元 8200 担忧、guappa「Probably the entire company's purpose is to gain access to secrets」等。
- 「你（调研者）推断」：这些评论**不针对 Shir 个人**，但塑造了 Wiz Research 团队的整体公众印象——"Wiz 研究能力 = 数据获取能力 = 商业/情报价值"。Shir 作为 Head of Research，其团队的研究输出在此框架下被赋予额外含义：每次跨账户漏洞披露都被读为"Wiz 商业/情报能力展示"。

---

## 三、厂商回应

### 3.1 Microsoft（ExtraReplica, 2022-04，Shir + Ronen + Sagi + Nir）

- 来源：Wiz ExtraReplica 博客 https://www.wiz.io/blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql/
- 来源：HN ExtraReplica 帖子 31213335 中对 Microsoft 通报的转述
- 可信度：高
- 「别人说她」Microsoft 声明：「fully mitigated」+「no action is required by Azure customers」+「no customer data was accessed using this vulnerability」。Single Server 实例和 VNet 内的 Flexible Server 不受影响。
- 处置：$40,000 bounty；2022-01-13 修复证书问题；2022-02-25 全部受影响实例修复完成。
- 「她说过」（Wiz 博客原文）：「Microsoft's responsiveness... a model for all vendors」——**Shir 团队主动公开赞许 Microsoft**。这种"为厂商背书"的话语在 P0/Tavis Ormandy 等独立研究员中并不常见，是 Wiz 披露风格的显著特征。
- 「你（调研者）推断」：Microsoft **没有公开反驳 Shir 团队的技术结论**。但 Microsoft 的措辞刻意收窄影响范围（"no customer data was accessed"），与 Wiz 的"cross-account database vulnerability"措辞存在张力——这种"厂商收窄 + 研究者放大 + 厂商给 bounty 默认接受"的三角，是 Shir 团队 Azure 系列研究的标准回应模式。

### 3.2 Microsoft（Storm-0558 调查, 2023-07，Shir 个人署名）

- 来源：Wiz 博客 https://www.wiz.io/blog/storm-0558-compromised-microsoft-key-enables-authentication-of-countless-micr
- 可信度：高（一手）
- 「她说过」（Wiz 博客基调）：Shir 在 Storm-0558 调查博客中的语调比漏洞披露更接近"事件分析"，定位为"more impactful than we thought"——是对 Microsoft 自身通报的扩展性解读。
- 「你（调研者）推断」：这是 Shir 个人署名作品里少有的"事件后分析"而非"漏洞披露"，社区无 HN 帖子可查。Microsoft 对此次 Shir 分析未公开回应——但 Wiz 与 Microsoft 在 Storm-0558 上是合作调查姿态（Wiz CTO Ami Luttwak 后来接受媒体采访谈此事件），与 ExtraReplica 时期的"披露—修复—bounty"模式不同。

### 3.3 Oracle（AttachMe, 2022-07，**注意：非 Shir 署名**）

- 来源：Wiz AttachMe 博客 https://www.wiz.io/blog/attachme-oracle-cloud-vulnerability-allows-unauthorized-cross-tenant-volume-access
- 来源：Nir skill 3.3 节
- 可信度：高
- 「别人说她」（纠偏）：**AttachMe 由 Elad Gabay 单独署名，非 Shir 亦非 Nir**（见 0.3 节）。HN 上有 Shir 的推特 @shirtamari 引用，使她被外部误认为研究主笔。
- 「别人说她」Oracle 行动：24 小时内修复，纳入「July 2022 Critical Patch Update Advisory」，公开「thanked Wiz for discovering this vulnerability」。
- 「她说过」（Wiz 博客原文，团队）：「As an Oracle partner and customer, Wiz appreciates Oracle's collaboration and rapid attention to this issue.」——**Wiz 自称是 Oracle 的"partner and customer"**，进一步坐实了 Wiz 与厂商间存在商业关系。
- 「你（调研者）推断」：尽管 Shir 不是主笔，但 AttachMe 的"partner and customer"措辞是 Wiz Research 团队整体风格，Shir 作为 Head of Research 对此负责。Oracle **公开致谢**，与 Microsoft 一样未公开反驳技术结论。

### 3.4 Alibaba（BrokenSesame, 2023-04，Shir + Ronen Shustin）

- 来源：Wiz BrokenSesame 博客 https://www.wiz.io/blog/brokensesame-accidental-write-permissions-to-private-registry-allowed-potential-r
- 可信度：高（一手）
- 「别人说她」（Alibaba 安全团队原文）：「identified and monitored our activity at the time」「immediately took relevant actions to minimize risk」「no evidence to suggest Alibaba Cloud systems or services were exploited by other parties」「all relevant activity was associated with our researchers」。
- 处置：2022-11-12 Alibaba 独立修复第一个 PostgreSQL 漏洞；2022-12-04 Wiz 提交完整报告；2023-02-24 Alibaba 提供 test instances 给 Wiz 验证修复；2023-04-12 全部 mitigations 部署完成。
- 「她说过」（Wiz 博客原文）：「Alibaba Cloud's professional conduct and open communication throughout the disclosure process serve as an exemplary model for other vendors.」——**Shir 团队又一次主动公开赞美厂商**，比 ExtraReplica 对 Microsoft 的"model for all vendors"更进一步，把 Alibaba 称为"exemplary model"。
- 「你（调研者）推断」：Alibaba **没有公开反驳 Shir 团队的技术结论**，并主动披露"已监测到 Wiz 研究者活动"——这意味着 Alibaba 的反侦察能力较强，提前发现了 Wiz 的研究行为。这与 SAPwned 上 SAP 未检测到 Wiz 取得 cluster admin 形成对比。Shir 团队对 Alibaba 的"exemplary model"赞美，部分原因可能是 Alibaba 提前监测到研究活动，使 Wiz 没法走"完全独立披露"路径，只能转向"合作姿态"。

### 3.5 IBM（Hell's Keychain, 2022-12，Shir + Ronen + Nir + Sagi）

- 来源：Wiz Hell's Keychain 博客 https://www.wiz.io/blog/hells-keychain-supply-chain-attack-in-ibm-cloud-databases-for-postgresql
- 可信度：高
- 「别人她说」（IBM Cloud CISO Jerry Bell 原文）：「I greatly appreciate the partnership and professionalism of Wiz's security team and look forward to future collaboration. Their diligence and creativity are helping to make clouds a safer place to operate IT.」——**IBM Cloud CISO 公开背书 Wiz 的"partnership and professionalism"**，是 Shir 团队披露中获得的最完整厂商赞美。
- 处置：2022-04-19 Wiz 开始研究 IBM Cloud Databases 当天发现多个问题；2022-04-20 IBM Cloud 安全团队**主动检测到 Wiz 活动并要求暂停**；2022-04-24 Wiz 提交详细报告；2022-05-25 IBM 确认；2022-07-14 IBM 允许 Wiz 继续；2022-08-24/25 报告 K8s 与 secrets 相关问题；2022-09-03 全部 mitigated。完整修复历时约 4.5 个月。
- 「你（调研者）推断」：IBM Cloud 与 Alibaba Cloud 一样**主动检测到 Wiz 研究活动**（"asked to halt research"），与 SAPwned 上 SAP 未检测形成对比。IBM CISO 的公开赞美被 Wiz 主动嵌进披露博客，是 Shir 团队"厂商赞美 + 商业关系"风格的标本案例。IBM **没有公开反驳 Shir 团队的技术结论**。

### 3.6 Hugging Face（2024-04，Shir + Sagi Tzadik）

- 来源：Wiz Hugging Face 博客 https://www.wiz.io/blog/wiz-and-hugging-face-address-risks-to-ai-infrastructure
- 可信度：高
- 「别人她说」Hugging Face 行动：标题即写"works with Hugging Face on mitigations"——Hugging Face 与 Wiz 合作修复。
- 「你（调研者）推断」：Hugging Face 是 AI 圈顶流，与 Wiz 合作姿态修复——与 Alibaba/IBM 类似的"合作—赞美"模式。HN 零讨论。

### 3.7 SAP（SAPwned, 2024-07，**主笔 Hillai Ben-Sasson**）

- 来源：Wiz SAPwned 博客 https://www.wiz.io/blog/sapwned-sap-ai-vulnerabilities-ai-security
- 来源：HN SAPwned 帖 40990768
- 可信度：高
- 「别人她说」（纠偏）：**SAPwned 主笔为 Hillai Ben-Sasson**，非 Shir。Shir 出现在文末"Stay in touch!"团队列表（含 @shirtamari Twitter 链接），但非 byline。
- 「别人她说」SAP 行动：修复全部漏洞，在 SAP 网站致谢 Wiz，声明「No customer data was compromised」。披露时间线显示 SAP 在 2 天内回复，5 月 15 日部署全部修复。
- 「她说过」（Wiz 博客原文，团队）：「We thank them for their cooperation.」
- 「别人她说」（HN 社区对 SAP "无客户数据泄露" 声明的强烈质疑）：
  - **SoftTalker**：「And if they did not detect it, how can they know that customer data have not been compromised?」
  - **dotty-**：「I hope SAP does a hard retrospective on why Wiz's research was not disrupted before they got full cluster admin...」
- 「你（调研者）推断」：SAP 是 Shir 领导下 Wiz Research 在厂商关系上**最尴尬的一次**——SAP 未检测到 Wiz 取得 cluster admin 级访问（与 Alibaba/IBM 主动检测形成对比），事后 SAP "无客户数据泄露"声明被社区质疑。Shir 作为 Head of Research 对"取得 cluster admin 级访问是否越界"负有督导演进责任。SAP **没有公开反驳 Wiz 团队的技术结论**。

### 3.8 AWS（CodeBreach, 2026-01，Shir 非主笔）

- 来源：HN CodeBreach 帖 46636093
- 来源：Nir skill 3.5 节
- 可信度：高
- 「别人她说」（Wiz 团队整体）：CodeBreach 揭示 AWS CodeBuild 供应链漏洞"威胁 AWS Console"。AWS 未在本次调研中找到公开 advisory 回应。
- 「你（调研者）推断」：AWS 是 Shir 领导下 Wiz Research **首次把研究主攻方向指向 AWS**——此前 Nir skill 4.6 节观察"未发现针对 AWS 服务的同级 Nir 署名研究"。AWS HackerOne scope 比 Microsoft 更严格，使 Wiz 的"研究—披露—越界指控"边界更模糊。AWS 沉默不回应可能反映其与 Wiz 的复杂商业关系（AWS 可能是 Wiz 客户，见 2.9.4 az226 评论）。

### 3.9 NVIDIA（2024-09, 2025-02, 2025-07，Shir + Ronen + Andres + Nir）

- 来源：Wiz NVIDIA 系列博客
- 可信度：高
- 「别人她说」NVIDIA 行动：修复 CVE-2024-0132 与 CVE-2025-23266，致谢 Wiz（Wiz 博客基调）。
- 「你（调研者）推断」：NVIDIA 系列是 Shir 团队转向 AI/容器安全赛道的主要载体。NVIDIA **没有公开反驳 Wiz 团队的技术结论**。

### 3.10 厂商回应总图

- 「你（调研者）推断」：所有被 Shir 团队披露的厂商（Microsoft/Oracle/Alibaba/IBM/Hugging Face/SAP/NVIDIA）**均未公开反驳 Wiz 团队的技术结论**，且至少 Microsoft/Oracle/Alibaba/IBM/Hugging Face 公开致谢或赞美。这与 SAPwned/CodeBreach 上社区对"披露伦理"的尖锐批评形成反差——**厂商默认接受 Wiz 技术结论**，但社区对"披露手段是否越界"持续质疑。Shir 作为 Head of Research 选择的策略是"与厂商深度合作 + 公开互相赞美"，与 P0 谱系（披露前严守最小访问 + 与厂商疏离）形成对照。

---

## 四、批评与争议（重点保留）

### 4.1 「Wiz CEO Microsoft 旧账」讽刺（ExtraReplica 帖，Shir 个人作品）

- 来源：https://news.ycombinator.com/item?id=31213335（mola, 31214459）
- 来源：https://news.ycombinator.com/item?id=29283057（shlosky，Nir skill 2.1 节引用，ChaosDB 帖）
- 可信度：中（社区推测，未坐实）
- 「别人说她」：
  - **mola**（ExtraReplica 帖）：「Wasn't Wiz CEO previous job leading Microsoft Israel RnD? After his previous cyber security startup (Adallom) was aquired by Microsoft? Azure security stance was under his supervision. Kind of ironic that his new security startup uncovers his failings at his old job...」——**把 Shir 团队在 Azure 上的发现与 CEO Assaf Rappaport 在 Microsoft Israel R&D 的旧职挂钩**。
  - **shlosky**（ChaosDB 帖）：「I wonder if the knowledge about Microsoft internals helped them finding this vulnerability」——把 Wiz 团队发现能力部分归因于 Microsoft 内部知识。
- 「你（调研者）推断」：这种说法**未经验证**——Wiz CEO 的 Microsoft 履历与 Shir Tamari 的具体研究能力之间无直接因果证据（Shir 本人是否曾在 Microsoft 任职，本次调研未找到证据；Wiz About 页面未列其履历）。但它反映了社区对"前 Microsoft 员工反过来打 Microsoft"这种叙事的强烈兴趣，间接放大了 Shir Azure 系列研究的话题性。**这条讽刺对 Shir 个人作品的指向性比 Nir 强**——因为 ExtraReplica 是 Shir 主笔，mola 的评论正落在她主导披露的帖子下。

### 4.2 「研究与产品营销深度绑定」批评（含 CMO 共同署名问题）

- 来源：Wiz BingBang 博客（署名 Shir Tamari + Raaz Herzberg + Hillai Ben-Sasson）
- 来源：Wiz About 页面（Raaz Herzberg = CMO & VP Product Strategy）
- 来源：Wiz ChaosDB 微站 https://chaosdb.wiz.io/
- 来源：Wiz ExtraReplica 博客（"a model for all vendors"）
- 来源：Wiz BrokenSesame 博客（"exemplary model for other vendors"）
- 可信度：高（一手 Wiz 自有内容）
- 「别人她说」：
  - Wiz 的披露博客与 Wiz 产品页面深度交叉链接，ChaosDB 微站本身就是品牌载体。
  - 在披露中频繁出现"a model for all vendors""exemplary model for other vendors""commendable level of care"等对厂商的赞许——与 P0 等独立研究员的克制风格形成对比。
  - **BingBang 的署名结构 Shir + Raaz Herzberg + Hillai Ben-Sasson 是最直接的"研究与营销绑定"证据**——Raaz Herzberg 是 Wiz 的 CMO & VP Product Strategy，CMO 亲自挂名安全研究披露在独立研究员圈子里极为罕见。
- 「你（调研者）推断」：Shir 作为 Head of Research，其研究风格与 Wiz 商业资产深度交织。CMO 共同署名（BingBang）说明 Shir 领导下的 Wiz Research 把披露博客视为产品营销载体的一部分。这是 Wiz 研究模式的结构性特征，并非 Shir 个人选择，但社区批评会指向她的领导形象。

### 4.3 团队作品的越界指控：SAPwned "敲诈" 与 CodeBreach 越界（Shir 非主笔但督导演进）

- 来源：https://news.ycombinator.com/item?id=40990768（SAPwned，darefalcon/rvnx/uaas 批评）
- 来源：https://news.ycombinator.com/item?id=46636093（CodeBreach，btown/rand846633/InitialBP 批评）
- 可信度：高（多用户高赞评论）
- 「别人她说」（Wiz 团队整体批评）：
  - SAPwned 上 darefalcon："hit piece thinly veiled as a vulnerability disclosure""Sounds kinda like extortion"
  - SAPwned 上 rvnx：「anything who tries to hack a large company without being invited would get seriously prosecuted」
  - CodeBreach 上 btown："From everything I know about pentesting, they should have stopped before doing this, right?"
  - CodeBreach 上 rand846633："we would not have had the pleasure of reading this article if wiz was payed by AWS"
  - CodeBreach 上 InitialBP：暗示 performative，"a CISO wants a 'massive compromise' demonstrated to secure budget"
- 「你（调研者）推断」：SAPwned 与 CodeBreach 是 Shir 领导下 Wiz Research **两次最严重的越界指控集中地**。Shir 虽非主笔，但作为 Head of Research 对"取得 cluster admin 级访问（SAPwned）"与"把自己加为 AWS repo admin（CodeBreach）"的披露伦理问题负有督导演进责任。这两次指控在 Nir skill 的基础上进一步揭示：**Shir 团队从"只读漏洞披露"（ExtraReplica/Hell's Keychain）转向"主动渗透—取得 admin—公开披露"（SAPwned/CodeBreach）的演进路径，与独立研究员圈（P0 谱系）的"最小必要访问"伦理越来越远**。

### 4.4 CVSS 评分注水指控（RediShell，Shir 非主笔）

- 来源：https://news.ycombinator.com/item?id=45497027（RediShell，tptacek/TheDong/zb3/bawolff/SkyPuncher 批评）
- 可信度：高（同行权威批评）
- 「别人她说」：
  - **tptacek**（Thomas Ptacek，独立研究员圈标杆）：「Bugs get whatever CVSS the marketing team for the discovering research lab wants them to get. It's literally a Ouija board.」+「this CVSS stuff is a farce and everyone seriously working in the field seems to agree」+「it is not of a caliber to rank among the most severe vulnerabilities ever discovered, which is what a CVSS score of 10 means.」
  - **TheDong**：实际影响近 0 却给 CVSS 10
  - **zb3**：post-auth 不应得 CVSS 10
  - **SkyPuncher**：「this is rather poor reporting and feels a bit flashy for a security researcher to make a name for themselves.」
- 「你（调研者）推断」：RediShell 是 Shir 领导下 Wiz Research 遭遇的**最权威同行技术批评**。Thomas Ptacek 的"CVSS = marketing team 玩占卜板"判定比 darefalcon 的"敲诈"指控更具同行内影响力，因为它来自圈内人。这次批评直接打在 Wiz Research 的"severity 包装"风格上，对 Shir 的研究督导演进是显著警示：**Shir 团队从 ExtraReplica 时期的"40k bounty +厂商赞美"模式，演进到 RediShell 时期的"CVSS 10 + flashy 报道"模式，越来越靠近营销包装而非技术克制**。

### 4.5 「不负责任披露」指控（DeepSeek，Shir 非主笔）

- 来源：https://news.ycombinator.com/item?id=42871371（DeepSeek，tomlockwood/caust1c/kdmtctl 等）
- 可信度：高（最高 HN 参与度，474 评论）
- 「别人她说」：
  - **tomlockwood**（修订后）：「The direct disclosure of urls and ports is insane. Wonder if they would be as irresponsible if it was MSFT, OpenAI, Anthropic, etc.」——**指控 Wiz 对中国厂商 DeepSeek 比对美国厂商更不负责任**。
  - **caust1c**：「I'm guessing Wiz wanted to ride the current media wave with this post instead of seeing how far they could take it.」——"蹭热度"。
  - **kdmtctl**：「shameless self promotion. A lot of PR and free traffic by taking a low hanging fruit.」
- 「你（调研者）推断」：DeepSeek 是 Shir 领导下 Wiz Research **首次被指控"对中国厂商不负责任披露"**。Shir 非主笔（Gal Nagli 主笔），但披露策略与媒体联动属于 Head of Research 督导范围。这次事件与 SAPwned 的"敲诈"指控、CodeBreach 的"越界"指控、RediShell 的"CVSS 注水"指控并列，构成 Shir 领导下 Wiz Research 的**四重伦理批评矩阵**：(1) 敲诈 (2) 越界 (3) CVSS 注水 (4) 不负责任披露。这是 Shir 公众形象的核心争议区。

### 4.6 Shir 个人作品低社区共鸣现象

- 来源：HN Algolia 检索结果（见 0.2 节）
- 可信度：高
- 「你（调研者）推断」（关键发现）：Shir 个人署名作品在 HN 上**整体参与度偏低**——ExtraReplica 60 分是她个人作品里讨论度最高的一次，其余多为 0-5 分 0 评论。**对比同期 Wiz 团队作品（DeepSeek 707 分、Microsoft AI 38TB 721 分、SAPwned 254 分、CodeBreach 160 分、RediShell 143 分），差一个数量级**。这意味着：
  - Shir 的公众形象更多由她督导的团队作品塑造，而非她个人署名作品。
  - 社区批评主要指向她督导演进范围内的团队作品，对她个人署名作品的直接批评很少（仅 ExtraReplica 上 mola 的 CEO 旧账讽刺）。
  - **Shir 在 Wiz 之外的个人品牌几乎不存在**——Wiz About 页面不列她，HN 讨论中很少单独提到 Shir Tamari 名字，多谈"Wiz 团队"。这与 Nir skill 5.3 节对 Nir 的观察一致：Wiz 没有在研究员个人品牌上做投入，所有披露打 Wiz Research 标识。

### 4.7 React2Shell 媒体放大与 Wiz 博客原文的差异

- 来源：Wiz React2Shell 博客 https://www.wiz.io/blog/nextjs-cve-2025-55182-react2shell-deep-dive
- 来源：HN React2Shell 帖 46279790（The Register"China, Iran field day, Google warns"）
- 可信度：高
- 「她说过」（Wiz 博客原文）：React2Shell 博客描述"在野利用 + 凭据收割 + 云后门"，**未提及 Google 警告或中国/伊朗归属**。
- 「别人她说」（媒体放大）：The Register 把 React2Shell 与"China, Iran field day""Google warns"绑定。
- 「你（调研者）推断」：这是 Shir 团队研究中典型的"披露—媒体放大"链条。Wiz 自己措辞相对克制（"在野利用"generic 描述），但媒体（The Register）把国家级归属加上去。批评者会指责 Wiz"放任媒体放大"，支持者会指出 Wiz 博客本身没有国家级归属。这条链条在 DeepSeek 事件上被指控为"不负责任披露"，在 React2Shell 上尚未引发同类批评——可能因为 React2Shell HN 讨论度低（5 分 1 评论）。

### 4.8 未发现的事项

- 「你（调研者）推断」：本次调研**未发现**针对 Shir Tamari 个人道德、研究造假、或具体技术结论被厂商反驳的记录。所有批评集中在四个层面：
  1. 团队整体商业模式（"敲诈"指控、$32B 收购后的数据访问担忧）
  2. 个别披露事件的越界感（SAPwned 取得 cluster admin、CodeBreach 加自己为 repo admin）
  3. CVSS 评分包装（RediShell CVSS 10 + flashy 报道）
  4. 不负责任披露与政治化（DeepSeek 直接披露 URL/ports）
- **厂商均未公开反驳 Shir 团队的技术结论**——Microsoft/Oracle/Alibaba/IBM/Hugging Face/SAP/NVIDIA 全部致谢或赞美，AWS 沉默。所有争议都在"披露伦理/severity 包装"层面，不在"技术正确性"层面。
- **未找到 Wiz 同事（Nir Ohfeld、Ami Luttwak、Assaf Rappaport、Hillai Ben-Sasson）对 Shir 个人的公开直接评价**——Wiz About 页面不列研究领导层，Wiz 博客署名均为集体。Nir skill 是同仓库内已构造的研究产物，其"Shir 是 Nir 直接上级"定位属推断，非原始引用。

---

## 五、社区定位

### 5.1 Wiz Research 在云安全研究社区的位置

- 来源：综合以上 HN 讨论与 Wiz 博客
- 可信度：高
- 「别人她说」（综合）：
  - 公认是**最高产的云漏洞研究团队之一**：ExtraReplica (2022-04)、AttachMe (2022-07)、Hell's Keychain (2022-12)、BingBang (2023-03)、BrokenSesame (2023-04)、Storm-0558 (2023-07)、Hugging Face (2024-04)、Replicate (2024-05)、SAPwned (2024-07)、NVIDIA 系列 (2024-09/2025-02/2025-07)、DeepSeek (2025-01)、React2Shell (2025-12)、CodeBreach (2026-01)——平均每月一次重大披露。
  - HN 用户在收购帖中点名"Wiz 的安全团队 has been publishing high quality research"（Nir skill 5.1 节引用 brasetvik）。
  - HN 用户 0xy 把 Azure 一系列跨账户漏洞归于同一团队："there's been a concerning number of cross-account exploits in the last couple of years"。
- 「你（调研者）推断」：Shir 作为 Head of Research，领导着**业内最高产的云安全研究团队**。但从 HN 讨论度看，团队最高传播力的作品（DeepSeek/38TB/SAPwned/CodeBreach/RediShell）均非她个人主笔，她的个人作品（ExtraReplica 除外）在社区可见度上属于第二梯队。

### 5.2 与 Nir Ohfeld / Hillai Ben-Sasson 的内部协作定位

- 来源：Wiz 博客署名 + Nir skill 内部定位
- 可信度：高
- 「你（调研者）推断」：
  - **Shir 与 Nir Ohfeld 是 Wiz Research 早期最高频合著搭档**：ExtraReplica、Cloud Gray Zone、Cloud isolation PostgreSQL、K8s LAN Party、NVIDIAScape 均共同署名。
  - Nir skill 第 385 行把 Shir 定位为"Wiz Head of Research，战略层合作者，直接上级"——即 Nir 的直接上级。
  - Nir skill 第 387 行把 Hillai Ben-Sasson 定位为"2024-2025 主合作者，取代 Shir 位置"——即 Hillai 在 2024 后接替 Shir 的 hands-on 研究位置。
  - **从署名演进看**：Shir 在 2021-2023 几乎所有 Wiz 重大披露都是第一作者；2024 起 SAPwned 主笔为 Hillai，DeepSeek 主笔为 Gal Nagli，Shir 名下作品转向 NVIDIA/React2Shell 等"深度技术分析"而非"首披露"。这与 Nir skill 观察"Hillai 取代 Shir 位置"一致——**Shir 从 hands-on 主笔者升格为 Head of Research 督导角色**。
  - BingBang 署名 Shir + Raaz Herzberg（CMO）+ Hillai 的结构是过渡期标本：Shir 仍挂名但 CMO 与接替者 Hillai 共同署名，反映 Wiz 把披露博客视为营销载体的一部分。

### 5.3 与 Tavis Ormandy / Felix Wilhelm / Ian Beer 的横向对比

- 来源：本节为**你（调研者）推断**，基于 Felix Wilhelm、Tavis Ormandy、Ian Beer 同名 04-external-views.md 的对比框架与本次社区调研
- 可信度：中（推断，非直接引用）
- 你（调研者）推断对比表：

| 维度 | Shir Tamari | Nir Ohfeld | Tavis Ormandy | Ian Beer | Felix Wilhelm |
|------|-------------|------------|---------------|----------|----------------|
| 主要领域 | 云隔离/AI 安全/供应链 | 云隔离/身份 | 用户态软件、虚拟化 | iOS/macOS 内核 | hypervisor 逃逸 (Xen/KVM) |
| 雇佣形态 | 商业公司 (Wiz，被 Google 收购) | 商业公司 (Wiz) | Google Project Zero | Google Project Zero | ERNW → P0 → Asymmetric Research |
| 角色演进 | hands-on 主笔 → Head of Research 督导 | hands-on 主笔 | 个人署名突出 | 个人署名突出 | 个人署名突出 |
| 署名方式 | 早期第一作者，2024 后转向团队督导 | 团队署名为主，多次合著 | 个人署名突出 | 个人署名突出 | 个人署名突出 |
| 披露与商业关系 | **与 Wiz 产品深度绑定，CMO 共同署名** | 与 Wiz 产品深度绑定 | 与产品无关（P0 中立） | 与产品无关 | 与产品无关（P0 时期）；Asymmetric 时期与商业资产保护相关 |
| 公众知名度 | 低（Wiz 品牌遮蔽，About 页不列） | 较低（Wiz 品牌遮蔽个人） | 极高（推特活跃） | 极高（iPhone 越狱关联） | 中等（专业圈内） |
| 公开批评记录 | 团队作品被批"敲诈/CVSS 注水/越界/不负责任披露" | 有（SAPwned "extortion" 指控） | 较少（多针对产品而非个人） | 较少 | 极少（仅 IBM 一例异议） |
| 厂商关系 | 公开赞许厂商（"model for all vendors""exemplary model"） | 公开赞许厂商 | 相对疏离 | 相对疏离 | 总体专业，IBM 例外 |
| 个人作品 HN 共鸣 | 低（ExtraReplica 60 分为最高，多数 0-5 分） | 中（ChaosDB 116 分） | 极高 | 极高 | 中等 |

**关键推断**：
- Shir 与 P0 三人组的最大差异是**"商业公司研究督导演进者"vs"中立研究员"**身份。P0 即便隶属于 Google，仍以独立姿态发声；Shir 领导下的 Wiz Research 直接为 Wiz 的商业叙事服务，CMO 共同署名是这种绑定最直接的证据。
- 与 Nir Ohfeld 的关键差异：Nir 是 hands-on 主笔者，Shir 是从 hands-on 升格为督导演进者的角色。**Nir 的个人作品 HN 共鸣高于 Shir 个人作品**（ChaosDB 116 分 vs ExtraReplica 60 分）——但这并不意味着 Nir"研究能力更强"，而是 ChaosDB 是 Wiz 第一个标志性研究，占据了首发红利。
- 从研究风格看，Shir 的方向（云隔离、AI 安全、供应链）与 P0 三人组（内存破坏、内核、虚拟化逃逸）几乎不重叠，是平行的赛道，难以横向比较"研究能力高低"。
- Shir 的演进路径（hands-on → 督导）与 Felix Wilhelm 的演进路径（ERNW → P0 → Asymmetric）有结构相似性——都从 hands-on 转向更宏观的研究战略角色，但 Felix 在 Asymmetric 时期仍保持个人署名（"Asymmetric Research 博客"），Shir 在 Wiz 时期完全融入团队署名。

### 5.4 Wiz 领导层对 Shir 的公开评价

- 来源：Wiz About 页面 https://www.wiz.io/about
- 可信度：高（一手公司页面）
- 「别人她说」（实际是沉默）：**Wiz About 页面未提及 Shir Tamari**。领导层列出 CEO Assaf Rappaport、CTO Ami Luttwak、VP Product Yinon Costica 等 13 人，**没有任何研究条线领导岗位**。
- 「她说过」（Assaf Rappaport 官方引语）：仅关于产品愿景——"Siloed security tools and scanners — even best in class — simply can't provide the perspective that today's security professionals need."——未提及 Shir 或研究团队。
- 「你（调研者）推断」：Wiz 把研究团队作为"功能性资产"而非"个人品牌"对外展示。这是商业策略选择，使 Shir 的公众形象**完全由其督导演进范围内的团队研究输出定义**，无领导层背书加成。这种"沉默"也意味着所有针对 Wiz Research 团队的批评（敲诈/CVSS 注水/越界/不负责任披露）会直接落在 Head of Research 即 Shir 身上，没有 CEO/CTO 的公开分担。

### 5.5 竞品云安全研究员的反应

- 来源：本次调研未找到 Palo Alto/Prisma Cloud、Orca Security、Plextrat 等竞品研究员对 Shir 研究的公开直接评价
- 可信度：低（无证据）
- 「你（调研者）推断」：
  - **Orca Security 与 Wiz 的公开冲突仅在商业层面**：HN 上有三条 Orca 起诉 Wiz 专利侵权的帖子（objectID 36704848 / 40981969 / 36719545，2023-07 至 2024-07），均低参与度（2-3 分 0 评论），无技术评论。这说明 Orca 与 Wiz 的冲突是商业专利战，不是研究员间技术交锋。
  - **Palo Alto/Prisma Cloud、Plextrat 等竞品研究员对 Shir 研究的公开反应缺失**——可能不存在，也可能在私有渠道（如 Discord/Slack）。HN 上未检索到竞品研究员点名评价 Shir 或 Wiz Research 的评论。
  - 这种沉默本身是定位信号：竞品研究员对 Shir 团队的研究**既不公开质疑技术结论，也不公开背书**——保持商业礼仪。所有公开批评来自独立研究员（如 tptacek）和 HN 普通用户，不是竞品研究员。

---

## 来源可信度小结

### 高可信度（一手或厂商/社区原始记录）

- Wiz 官方博客（wiz.io/blog/*，含作者页 https://www.wiz.io/blog/author/shir-tamari）：一手披露文档与作者索引
- Wiz About 页面（wiz.io/about）：一手公司领导层信息
- Microsoft 通过 Wiz 转引的对客户通报原文：厂商原始声明
- Alibaba/IBM/Hugging Face/SAP/NVIDIA 通过 Wiz 博客转引的厂商声明：厂商原始回应
- Hacker News 评论（多个高赞帖子，含 Algolia API 完整数据 hn.algolia.com/api/v1/items/*）：社区原始讨论
- HN Algolia 故事检索 API（hn.algolia.com/api/v1/search）：故事元数据（标题/分数/评论数/objectID/URL）

### 中可信度（二次报道或社区推测）

- The Register 关于 React2Shell 的"China, Iran, Google warns"报道（通过 HN 46279790 间接还原）：媒体标题化报道，**Wiz 博客本身未做此归属**
- HN 中对 Wiz CEO Microsoft 旧背景的"讽刺"性评论（mola/shlosky）：推测未坐实
- HN 中对 Unit 8200 / 数据访问的阴谋论式评论：推测未坐实
- Nir Ohfeld perspective skill 的"Shir 是 Nir 直接上级"定位：同仓库内已构造研究产物，非一手
- 本文档第五节的对比表与定位推断：基于多证据综合，但属调研者推断

### 低可信度 / 抓取受限

- The Register、BleepingComputer、TechCrunch、KrebsOnSecurity、Forbes、Dark Reading 直接报道：本次抓取均 404/403 或不在白名单，未取得原文，但通过 HN 讨论可间接还原事件
- arstechnica.com："Security researchers at Wiz discover another major Azure vulnerability"（2021-09）：WebFetch 被拒
- Microsoft MSRC 博客原始页面：未单独抓取 ExtraReplica 专门条目
- NVD CVE-2022-21437：检索结果显示这是 Oracle MySQL DoS bug，**非 ExtraReplica**（ExtraReplica 应有独立 CVE，本次未在 NVD 找到对应条目）
- Shir Tamari 的 X/Twitter 账号 @shirtamari：付费墙后无法获取一手言论
- **未找到 Wiz 同事（Nir Ohfeld、Ami Luttwak、Assaf Rappaport、Hillai Ben-Sasson）对 Shir 个人的公开直接评价**
- **未找到 Palo Alto/Prisma Cloud、Orca Security、Plextrat 等竞品研究员对 Shir 研究的公开直接评价**（Orca 起诉 Wiz 专利侵权帖子存在但无技术评论）

### 黑名单遵守

- 本文档未使用知乎、微信公众号、百度百科作为信息源。

### 关键空白与后续建议

1. **Shir 的"Head of Research"头衔未被 Wiz About 页面公开背书**——建议从 Wiz 内部访谈、会议演讲、LinkedIn 等渠道补证。当前头衔来源仅用户任务简报 + Nir skill 内部定位 + 推断。
2. **未找到 Wiz 同事对 Shir 的公开直接评价**——建议从 Black Hat/DEF CON/RSA 演讲、Wiz 内部播客、媒体访谈中补录。
3. **Shir 本人在 X/Twitter 上的言论（@shirtamari）**——付费墙后无法获取，建议人工访问以补「她说过」类别的内容。她发推扩散研究（如 AttachMe）是社区误归主笔的重要原因，需要一手推特内容核验。
4. **AttachMe 主笔归属纠偏**：用户任务简报把 AttachMe 列入 Shir 代表作，但 Wiz 博客作者页未列，Nir skill 明确为 Elad Gabay 单独署名。建议在 Shir skill 其他文档中同步纠偏。
5. **SAPwned 主笔归属纠偏**：Nir skill 把 SAPwned 归为"Nir+Shir 共同署名"，但 Wiz 博客 SAPwned 正式 byline 为 Hillai Ben-Sasson，Shir 仅出现在文末团队列表。建议在 Nir skill 与 Shir skill 中同步纠偏。
6. **DeepSeek 主笔归属**：Wiz 博客 DeepSeek 帖由 Gal Nagli 主笔，非 Shir。Shir 作为 Head of Research 督导演进范围内，但不应直接挂在个人头上。
7. **React2Shell 的"Google warns / China Iran"归属**：Wiz 博客本身未做此归属，媒体（The Register）放大了。建议核验 Google Mandiant 是否单独通报。
8. **CVE 数据库补全**：ExtraReplica 应有独立 CVE（非 CVE-2022-21437，那是 Oracle MySQL DoS），建议从 Microsoft MSRC 与 NVD 补全 Shir 个人作品的 CVE 索引。
9. **Orca 起诉 Wiz 专利侵权**：三条 HN 帖均低参与度，无技术评论——建议从专利法庭文件补录是否涉及 Shir 个人。

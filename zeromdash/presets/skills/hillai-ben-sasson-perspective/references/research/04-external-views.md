# Hillai Ben-Sasson — 他者视角

> 调研主题：别人怎么评价、批评、对比 Hillai Ben-Sasson
> 调研日期：2026-07-26
> 标注约定：【他说过】= Hillai 本人在公开文章/披露中表达的内容；【别人说他】= 第三方对 Hillai 或其研究的明确评价；【你推断】= 基于证据的合理推断，明确标注
> 信息源黑名单已排除：知乎、微信公众号、百度百科

---

## 核心发现（先说结论）

1. **几乎没有针对 Hillai 个人的公开评价。** 在所有可获取的 HN 评论区、媒体覆盖和厂商回应中，没有任何一处直接点名 "Hillai Ben-Sasson" 进行评价或批评。批评一律落在三个层面：(a) Wiz Research 团队/公司、(b) 漏洞披露伦理、(c) SAP 的安全实践。**这是最重要的诚实结论**——SAPwned 的"批评最集中"是真的，但批评对象是"Wiz 这个行为体"而非"Hillai 这个人"。
2. **Hillai 的公开研究署名面相对集中。** 经直接核对 Wiz 官方博客：Hillai Ben-Sasson 明确署名的研究只有两篇——**BingBang (2023-03-29)** 与 **SAPwned (2024-07-17)**。先前线索中提到的"ExtraReplica (CVE-2021-23607) 由 Hillai 完成"为误传——ExtraReplica 实为 Azure PostgreSQL 漏洞（2022-04-29 披露），署名为 Ronen Shustin、Sagi Tzadik、Nir Ohfeld、Shir Tamari，**Hillai 未列名**。同样，AttachMe (Oracle Cloud, 2022-09) 署名为 Elad Gabay，亦非 Hillai。【你推断】因此，"Hillai 是 Nir Ohfeld 最频繁合作者"这一说法在公开署名层面并不成立——Nir 在 ExtraReplica/AttachMe 等主力研究中并不与 Hillai 共同署名，Hillai 更像是在 Wiz 的 AI/多租户研究线上作为署名 lead 出现的特定阶段合作者。
3. **SAPwned 的 HN 批评是核心争议场域，但批评伦理指向"Wiz 模式"而非 Hillai 个人。** darefalcon 的 "extortion"/"hit piece" 指控是迄今最尖锐的批评，但其措辞是 "Companies that penetrate networks uninvited"——指向公司行为体，未点名 Hillai。
4. **BingBang 在 HN 几乎没有社区讨论**（5 分、0 条评论），与 SAPwned（254 分、66 条评论）形成鲜明对比。BingBang 没有引发伦理争议。

---

## 1. 媒体报道基调

### 1.1 直接媒体覆盖获取情况

本次调研未能直接抓取到 The Register、BleepingComputer、TechCrunch、Dark Reading 对 SAPwned 的具体文章正文（多数 URL 返回 403/404，WebFetch 无法穿透）。Wiz 官方博客是唯一可完整获取的一手来源。【你推断】这意味着本章主要基于 Wiz 官方叙事与 HN 社区二手讨论，媒体报道基调的独立第三方佐证较弱，可信度相应下调。

### 1.2 Wiz 官方叙事基调（一手）

来源：https://www.wiz.io/blog/sapwned-sap-ai-vulnerabilities-ai-security （可信度：高，作为 Hillai 本人/团队的官方表达）

【他说过】SAPwned 文章的署名 lead 为 **Hillai Ben-Sasson**，"Stay in touch" 区段将 Shir Tamari、Nir Ohfeld、Sagi Tzadik、Ronen Shustin 列为 Wiz Research Team。

【他说过】文章将 SAP AI Core 的五个漏洞链描述为"tenant isolation failures"，核心论断是："AI training requires running arbitrary code by definition; therefore, appropriate guardrails should be in place"——把问题框架化为 AI 服务"运行任意代码"的本质带来的隔离挑战。

【他说过】Wiz 把 SAPwned 定位为其跨 AI 服务提供商租户隔离研究项目的延续，引用了之前在 Hugging Face 和 Replicate 上的类似发现。这表明 Wiz 有意将研究主题化、系列化、品牌化。

【他说过】Wiz 强调披露流程合规：Jan 25 2024 报告 SAP → Jan 27 SAP 分配 case → Feb 16 SAP 修复首漏洞并轮换 secrets → Feb 28 Wiz 用两个新漏洞绕过补丁再次报告 → May 15 2024 SAP 部署全部修复 → Jul 17 2024 公开披露。并声明 "No customer data was compromised"。

【你推断】Wiz 的叙事基调是"专业、克制、流程合规"——刻意展示协调披露时间线来预防伦理质疑。这正是 darefalcon 在 HN 上质疑的那句 "We thanked them for their co-operation" 的语境：Wiz 用礼貌措辞收尾，但批评者读出的是"我有能力搞你、我谢谢你配合"的隐含压力。这构成 SAPwned 伦理争议的修辞根源。

### 1.3 媒体覆盖的间接证据

来源：https://hn.algolia.com/api/v1/items/40990768 （可信度：高，HN 原始数据）

HN 帖子的 URL 直接指向 Wiz 官方博客而非任何媒体报道，说明当时 HN 社区把 Wiz 博客本身视为主要信源。帖子由 todsacerioti 于 2024-07-17 提交，获得 254 分 66 评论——这一热度本身说明 SAPwned 在安全社区引发了显著关注，但**不能等同于媒体将其定性为"轰动的 hit piece"或"负责任的披露"**——证据不足以做出媒体基调判断。【你推断】如果 The Register/BleepingComputer 等媒体将其定性为 extortion 或 hit piece，darefalcon 在 HN 评论中极可能会引用媒体原文作为弹药；事实上他只引用了 Wiz 自己的措辞，间接暗示主流媒体覆盖更可能采用了中性"responsible disclosure"基调。这是弱推断。

---

## 2. Hacker News 社区讨论（SAPwned 为重点）

### 2.1 SAPwned HN 帖子元数据

- 帖子：https://news.ycombinator.com/item?id=40990768
- 标题："SAPwned: SAP AI vulnerabilities expose customers' cloud environments and privat[e]"
- 提交者：todsacerioti
- 分数：254 分
- 评论数：66 条
- 日期：2024-07-17
- 链接：Wiz 官方博客
- 数据源：https://hn.algolia.com/api/v1/items/40990768 （可信度：高，HN 官方 API 镜像）

### 2.2 批评主轴一：披露伦理 / "extortion" / "hit piece" 指控（核心争议）

这是 SAPwned 全帖中最尖锐的批评，由 darefalcon 发起：

**darefalcon（关键评论）：**
> "Companies that penetrate networks uninvited looking for vulnerabilities to create blog content should be prosecuted IMHO. This piece in particular sounds like a hit piece thinly vailed as a vulnerability disclosure. 'We thanked them for their co-operation'. Sounds kinda like extortion."

来源：https://news.ycombinator.com/item?id=40990768 （可信度：高，HN 原始评论）

【别人说他/对 Wiz 模式】darefalcon 明确使用了 "hit piece"（抹黑稿）和 "extortion"（勒索）两个重指控词，并锚定在 Wiz 博客结尾的 "We thanked them for their co-operation" 这句措辞上。批评的矛头是"Wiz 这家公司为制造博客内容而未受邀约地渗透网络"的行为模式，而非 Hillai 个人。但鉴于 SAPwned 文章署名 lead 是 Hillai，【你推断】这一指控在作者归属层面会自然落到署名人头上——不过 darefalcon 显然并未查阅署名，他对 Wiz 公司行为体的批评是结构性的。

**rvnx（支持 darefalcon 框架）：**
> "It's a crime, anything who tries to hack a large company without being invited would get seriously prosecuted, but as the law practice says 'If you have billions of USD, laws don't apply to you anymore'."

来源：同上 （可信度：高）

【别人说他/对 Wiz 模式】rvnx 把 darefalcon 的伦理批评推向法律层面：认定未受邀约的黑客行为本身是犯罪，并补充了一个"资本规模豁免法律"的批判性论点。这同样指向 Wiz（数十亿美元估值公司）这一行为体，未点名任何研究员。

**uaas（伦理框架的另一向度——权限/escalation 伦理）：**
> "Usually security researchers are required to reach out to the target before escalating further into the systems, asking for permissions to proceed. This is also something bug bounty programs require as per their rules for their targets in scope. I'd expect this to be the case here as well, given the researcher is employed by a security company. Researchers also usually mention which points they asked for additional permissions at in writeups, but now always."

来源：同上 （可信度：高）

【别人说他/对披露方法学】uaas 提出了一个比 darefalcon 更具体的伦理框架：研究员在"进一步 escalate 进系统"之前应当主动联系目标获取权限，并应在 writeup 中标注在哪些节点申请了额外权限。uaas 注意到"the researcher is employed by a security company"——把矛头对准"Wiz 是商业安全公司"这一身份带来的更高伦理义务。Wiz 的 SAPwned 博客并未明确披露这些权限申请节点，【你推断】这正是 uaas 隐含的批评点：Wiz 作为商业公司在 writeup 透明度上低于学术/独立研究员的标准。

### 2.3 批评主轴二：技术定性争议——"这到底是 AI 漏洞还是 k8s 配置漏洞"

**jaaron（关键评论）：**
> "While I get that it's the AI product, the vulnerability here is the k8s configuration. It really has nothing to do with the AI product itself or AI training or anything related to machine learning or generative AI, it's more about poor cloud computing platform security."

来源：同上 （可信度：高）

【别人说他/对研究定性】jaaron 提出了对 Wiz 叙事框架的直接质疑：SAPwned 的根因是 Kubernetes 多租户配置错误，而非 AI 特有风险。这与【他说过】Hillai/Wiz 把问题框架化为"AI 服务的本质带来隔离挑战"形成直接对立。回复中 bilekas 为 Wiz 辩护，引用博客原文 "The root cause of these issues was the ability for attackers to run malicious AI models and training procedures, which are essentially code"，但 jaaron 的核心论点是：runAsUser=1337 绕过 Istio、未认证的 Helm Tiller、未认证的 EFS——这些都是经典云原生配置问题，与"AI"无关。

【你推断】这是 SAPwned 收到的最具技术杀伤力的隐性批评：它在暗示 Wiz 把一个"普通云安全配置错误"包装成"AI 安全前沿研究"以获取更高曝光度。这恰好呼应 darefalcon 的 "hit piece" 指控——如果根因不是 AI 特有，那么用 "SAPwned"（呼应 Log4Shell 命名传统）这种品牌化命名就更像营销而非研究。这一批评虽未点名 Hillai，但作为 SAPwned 的署名 lead，他首当其冲。

**ec109685（技术深度批评）：**
> "This is really bad. They are running a single K8s cluster and expecting hard multi-tenancy guarantees? All the major clouds use vm boundaries and separate K8s clusters between customers. Microsoft was similarly bitten a few years ago with one of their function products that expected K8s to be the primary security boundary."

来源：同上 （可信度：高）

【别人说他/对 SAP 的技术批评】ec109685 把批评从 Wiz 转向 SAP：单一 K8s 集群做硬多租户是结构性错误。这条 sub-thread 后续讨论了 Istio sidecar 不是 egress 边界、VirtualCluster 才是硬多租户方案等技术细节，整体是社区对 SAP 架构的批评，而非对 Wiz 的批评。

### 2.4 批评主轴三：redaction 方法被质疑

**cosmotic：**
> "As security researchers, you think they might have known that pixelating text to redact it is a poor choice." （附 bleepingcomputer 关于反转像素化的链接）

来源：同上 （可信度：高）

【别人说他/对披露细节】cosmotic 质疑 Wiz 用像素化（pixelation）遮挡敏感信息是糟糕实践，因为已有 Depix 等工具可逆向。NotMichaelBay 补充指出 Wiz 在某些地方用了 blur、某些地方用了 pixelation。chatmasta 反驳说漏洞都已修复、密钥都已轮换，遮挡本身已无必要。

【你推断】这构成对【他说过】Hillai 作为署名 lead 的细节严谨度的轻度质疑——一个会被 Depix 逆向的 redaction 方法出现在 lead-authored 的披露博客中，是技术信誉的轻微减分项。但批评很轻，且 chatmasta 的反驳有效。

### 2.5 批评主轴四：发现 deprecated 技术的"惊讶"基调

**mac-chaffee：**
> "Shocked that there was a tiller instance running. That's been deprecated since 2020."

来源：同上 （可信度：高）

【别人说他/对 SAP】mac-chaffee 对 SAP 还在运行 Helm Tiller（2020 年已弃用）表示震惊。uaas 回复指出生产环境中运行 2010 年代软件的普遍性。这条不是对 Wiz 的批评，而是对 SAP 的批评。

### 2.6 为 Wiz 辩护的声音（平衡记录）

**_dain_（反批评 darefalcon）：**
> "way to shoot the messenger."

来源：同上 （可信度：高）

**dumpsterdiver（重构 darefalcon 论点）：**
> "Companies who carelessly collect and store sensitive user data insecurely should not be closely scrutinized, and should be left alone to continue exposing innocent user data to malicious cyber criminals." ——用反讽重构 darefalcon 的论点，暗示其立场等同于放任数据泄露。

来源：同上 （可信度：高）

【别人说他/平衡】darefalcon 的 extortion 指控在帖内获得了至少两条反驳，且反驳整体语气更有力。社区对 darefalcon 立场的支持度并不压倒性——sub-thread 显示质疑 darefalcon 的力量与支持他的力量并存。

### 2.7 社区对 Wiz 商业成功的旁注（非批评 Hillai）

**tiffanyh：**
> "Has anyone used Wiz? It's possibly the fastest rocket for an enterprise software company ever. $100M in just 1.5 years time $350M at end of 3-year"

**kchr（用户视角）：**
> "Using it and loving it. Security aspects aside, it's also the best tool I've tried for proper asset management in multi-cloud scenarios."

来源：同上 （可信度：高）

【别人说他/对 Wiz 产品】这些评论不针对 Hillai，但提供了 SAPwned 争议的语境：Wiz 在 HN 社区中有"商业上极成功的研究驱动型安全公司"的形象，这种形象本身会让 darefalcon 类型的批评者更倾向于把 Wiz 的披露解读为"营销驱动的渗透行为"。【你推断】Wiz 的商业成功放大了其披露行为的伦理审视强度——研究员署名因此被动承担更高的伦理审视。

---

## 3. 厂商回应

### 3.1 SAP 对 SAPwned 的回应

来源：https://www.wiz.io/blog/sapwned-sap-ai-vulnerabilities-ai-security （可信度：中，二手转述——未能直接抓取 SAP 官方 advisory 原文）

【他说过/经由 Wiz 转述】Wiz 博客称 "all vulnerabilities were reported to SAP's security team and fixed by SAP"，并称 SAP 在其官网上承认了这些发现。Wiz 转述 SAP 的核心结论是 "No customer data was compromised"。

【你推断】未能直接抓取到 SAP 官方 security note（support.sap.com 需要客户登录，WebFetch 403/返回空内容），因此"SAP 承认/反驳 Hillai 结论"的独立厂商声音缺失。这是一个明确的研究空白。从 Wiz 转述的"SAP 承认并修复"以及协调披露时间线（Jan 25 报告 → May 15 修复 → Jul 17 公开）看，SAP 采取了合作姿态而非反驳姿态——这与 darefalcon 的 "extortion" 指控形成张力：如果 SAP 自己都配合并承认，"勒索"框架在厂商层面缺乏受害方证词支持。

### 3.2 Microsoft 对 BingBang 的回应

来源：https://www.wiz.io/blog/bingbang （可信度：高，一手 Wiz 博客）

【他说过/经由 Wiz 转述】Wiz 称 "All issues were responsibly disclosed to Microsoft upon discovery. Microsoft rapidly fixed its vulnerable applications and modified some AAD functionality to reduce customer exposure." Microsoft 未公开反驳 Wiz 的结论。

【你推断】Microsoft 对 BingBang 的回应也是合作姿态，未引发任何伦理争议——BingBang 在 HN 只有 5 分 0 评论，没有任何批评。

### 3.3 AWS / GCP / Oracle 厂商回应

【你推断】在 Hillai 署名的研究中，没有涉及 AWS/GCP/Oracle 的厂商回应。AttachMe（Oracle，2022-09）署名为 Elad Gabay 非 Hillai；ExtraReplica（Azure PostgreSQL，2022-04）署名为 Ronen Shustin/Sagi Tzadik/Nir Ohfeld/Shir Tamari，Hillai 未列名。因此 Hillai 的厂商交互面仅限于 Microsoft（BingBang）与 SAP（SAPwned），两起均获合作回应。

---

## 4. 批评与争议（汇总与定性）

### 4.1 争议强度排序

| 争议事件 | HN 分数 | 评论数 | 伦理指控强度 | 是否点名 Hillai |
|---|---|---|---|---|
| SAPwned (2024-07) | 254 | 66 | **高**（extortion/hit piece 指控） | 否 |
| BingBang (2023-03) | 5 | 0 | 无 | 否 |
| ExtraReplica (2022-04，非 Hillai 署名) | 60 | 多 | 中（聚焦 Azure 而非 Wiz 伦理） | 不适用 |
| AttachMe (2022-09，非 Hillai 署名) | 29 | 4 | 低 | 不适用 |

来源：https://hn.algolia.com/api/v1/search?query=BingBang&tags=story ；https://hn.algolia.com/api/v1/items/35370217 ；https://hn.algolia.com/api/v1/items/31213335 （可信度：高）

### 4.2 SAPwned 争议的实质内核

把 darefalcon/rvnx/uaas 三条批评合并解读，SAPwned 受到的伦理指控可分解为三层：

1. **行为层面（darefalcon/rvnx）**：Wiz 作为商业安全公司，未受邀约地渗透大型企业的生产系统，并以此制造博客内容。这在 darefalcon 看来构成"犯罪"，在 rvnx 看来只因 Wiz 是数十亿美元公司才被法律豁免。
2. **透明度层面（uaas）**：Wiz 在 escalate 进系统、获取 cluster-admin 权限之前是否主动联系 SAP 申请权限？writeup 未明确披露这些权限申请节点。商业公司研究员应被 held to 更高的透明度标准。
3. **定性层面（jaaron）**：Wiz 把一个"普通 K8s 配置漏洞"包装成"AI 安全前沿研究"并品牌化命名为 "SAPwned"（呼应 Log4Shell 等高危 CVE 命名传统），这构成"研究营销化"。

【你推断】这三层批评合并起来，构成对 Wiz 商业模式的系统性质疑：研究驱动的商业安全公司有动机把常规云配置问题"品牌化 + 前沿化 + 渗透戏剧化"以服务商业叙事。Hillai 作为 SAPwned 的署名 lead 是这一模式在该研究上的具体执行者，但批评从未将其个人化——这既是因为 HN 评论者通常不查阅署名，也是因为批评者有意把矛头对准更具结构性的"公司行为体"。

### 4.3 为何 BingBang 未引发争议

【你推断】BingBang 与 SAPwned 的关键差异：
- BingBang 目标是 Microsoft（一个在安全社区中"被研究透"的对手），SAPwned 目标是 SAP（企业软件巨头但云安全声誉尚未被广泛审视）——批评 SAP 更易引发"打落水狗还是打老虎"的伦理讨论。
- BingBang 的 redaction 与权限节点未见争议；SAPwned 的 pixelation redaction 被质疑。
- BingBang HN 帖子只 5 分，未上首页，社区未形成讨论场域；SAPwned 254 分上首页，争议自然聚集。
- BingBang 是 AAD 配置问题（开发者错误），SAPwned 是 K8s 多租户硬隔离失败（更严重的架构问题），后者天然更易引发"是否夸张化"的争论。

### 4.4 没有发现的对 Hillai 个人批评

明确记录：调研中**未发现**任何以下类型的批评：
- 质疑 Hillai 个人技术能力或技术水平
- 质疑 Hillai 个人诚信或学术不端
- 把 SAPwned 的问题归咎于 Hillai 个人决策失误
- 任何竞品研究员（Palo Alto/Prisma Cloud、Orca、Plextrat 等）对 Hillai 的公开评论
- 任何 Wiz 同事（Nir Ohfeld、Shir Tamari、Ami Luttwak、Assaf Rappaport）对 Hillai 的公开评价

【你推断】这不是因为这类批评一定不存在，而是因为：(a) Wiz 研究的署名传统是团队署名或多人署名，弱化个人；(b) 安全社区对研究员个人的公开评价本就稀少，更多落在研究本身；(c) Hillai 的公开足迹相对集中在 BingBang/SAPwned 两篇，缺乏足够的个人 brand 供批评者锚定。

---

## 5. 社区定位

### 5.1 与 Nir Ohfeld 的对比

来源：ExtraReplica 署名 https://www.wiz.io/blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql （可信度：高）；SAPwned 署名 https://www.wiz.io/blog/sapwned-sap-ai-vulnerabilities-ai-security （可信度：高）

【你推断】基于公开署名，Nir Ohfeld 的研究足迹更广：ExtraReplica（Azure PostgreSQL 跨账户）、SAPwned（与 Hillai 合作）。Hillai 的署名足迹集中在 BingBang（与 Raaz Herzberg、Shir Tamari）与 SAPwned（作为 lead）。两人在 SAPwned 上合作，但 Nir 在 ExtraReplica 上并未与 Hillai 共同署名。这修正了"Nir 最频繁合作者是 Hillai"的线索——在**公开研究署名**层面，证据不支持这一说法；该说法若成立，可能基于 Wiz 内部协作（未公开署名的共同工作），但无法从外部验证。

### 5.2 与 Tavis Ormandy / Felix Wilhelm 的对比

【你推断】Tavis Ormandy（Google Project Zero）和 Felix Wilhelm（ERNW/Asymmetric Research）是独立/机构研究员品牌——他们的个人 brand 与其研究深度绑定，批评会自然落到个人。Hillai 的位置不同：他是 Wiz Research 团队的一员，署名 lead 但品牌锚定在 Wiz 公司。这使他的"社区定位"更接近"机构研究员"而非"独立明星研究员"——批评落点天然是机构而非个人。这也解释了为什么 SAPwned 的伦理争议如此激烈却没有一个 HN 评论者点名 Hillai。

### 5.3 在 Wiz 研究谱系中的位置

【你推断】Wiz 的研究谱系呈现清晰的"跨云租户隔离"主线：AttachMe（Oracle，Elad Gabay）→ ExtraReplica（Azure PostgreSQL，Shustin/Tzadik/Ohfeld/Tamari）→ BingBang（Azure AAD，Herzberg/Tamari/Hillai）→ SAPwned（SAP AI Core，Hillai lead + Tamari/Ohfeld/Tzadik/Shustin）。Hillai 在这条主线中并非最早或最频繁出现者，但在 SAPwned 这篇最受争议的研究中担任 lead 署名——这既可能是他在该具体研究中的主导作用，也可能是 Wiz 内部的署名安排。无法从外部进一步区分。

### 5.4 ExtraReplica HN 讨论的间接定位信号

来源：https://hn.algolia.com/api/v1/items/31213335 （可信度：高，HN 原始评论）

ExtraReplica 的 HN 帖子（60 分）中，**mola** 留下了一条对 Wiz 整体定位的关键评论：
> "the Wiz CEO (Assaf Rappaport) previously led Microsoft Israel R&D and had his prior security startup (Adallom) acquired by Microsoft... Azure security was under his supervision, making it ironic that his new security startup uncovers his failings at his old job."

【别人说他/对 Wiz 公司】mola 点出了 Wiz 的结构性讽刺：CEO Assaf Rappaport 曾领导 Microsoft Israel R&D，其前创业公司 Adallom 被 Microsoft 收购，现在 Wiz 反过来揭露 Microsoft Azure 的安全失败。这构成社区对"Wiz 研究动机是否含个人历史因素"的隐性怀疑——但同样未点名任何研究员个人。

ExtraReplica 帖子整体聚焦 Azure vs AWS 的架构对比（0xy、alexjurkiewicz、sylens、philliphaydon、qxmat 等），未质疑 Wiz 披露伦理，也未点名研究员。【你推断】这进一步印证：Wiz 的研究在 HN 上引发的反应类型高度依赖于目标厂商——揭露 SAP 引发伦理争议，揭露 Microsoft 则引发架构对比讨论，揭露 Oracle（AttachMe，29 分）反应平淡。

---

## 6. 关键修正与局限

### 6.1 对已知线索的修正

1. **ExtraReplica CVE-2021-23607 / AWS RDS 归属 Hillai**——错误。ExtraReplica 实为 Azure PostgreSQL 漏洞（2022-04-29），CVE 编号需进一步核实（Wiz 博客未明示 CVE-2021-23607，且时间线不符 2021 vs 2022）。Hillai 未在 ExtraReplica 署名。来源：https://www.wiz.io/blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql （可信度：高）
2. **AttachMe 归属**——非 Hillai，署名 Elad Gabay。来源：https://www.wiz.io/blog/attachme-oracle-cloud-vulnerability-allows-unauthorized-cross-tenant-volume-access （可信度：高）
3. **"Nir Ohfeld 最频繁合作者是 Hillai"**——在公开署名层面证据不支持。Nir 在 ExtraReplica、AttachMe 的署名中均未与 Hillai 共同出现；两人共同署名仅见于 SAPwned。该说法若来自 Wiz 内部协作信息则无法从外部验证，建议下调可信度。

### 6.2 研究局限

- 未能直接抓取 The Register / BleepingComputer / TechCrunch / Dark Reading 对 SAPwned 的报道原文（多返回 403/404）。媒体报道基调的独立第三方佐证弱。
- 未能直接抓取 SAP 官方 security note（需客户登录）。SAP 的厂商回应经由 Wiz 转述，二手。
- WebSearch 工具在本次调研中多次返回无效结果，依赖 WebFetch + HN algolia API 作为主信源。
- 未找到任何 Wiz 同事对 Hillai 的公开评价、任何竞品研究员对 Hillai 的公开评论、任何 CVE/advisory 中明确引用 Hillai 个人（而非 Wiz Research）的条目。
- BingBang 的 HN 帖子评论数为 0，无社区讨论可提取，仅能从 Wiz 博客与零星二手报道判断。

---

## 来源可信度小结

| 来源 | 类型 | 可信度 | 用途 |
|---|---|---|---|
| https://www.wiz.io/blog/sapwned-sap-ai-vulnerabilities-ai-security | 一手（Wiz 官方，Hillai 署名 lead） | 高 | SAPwned 技术细节、披露时间线、署名确认、SAP 回应二手转述 |
| https://www.wiz.io/blog/bingbang | 一手（Wiz 官方，Hillai 共同署名） | 高 | BingBang 技术细节、Microsoft 回应二手转述、署名确认 |
| https://www.wiz.io/blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql | 一手（Wiz 官方） | 高 | ExtraReplica 署名确认（Hillai 未列名，修正线索） |
| https://www.wiz.io/blog/attachme-oracle-cloud-vulnerability-allows-unauthorized-cross-tenant-volume-access | 一手（Wiz 官方） | 高 | AttachMe 署名确认（Elad Gabay，非 Hillai） |
| https://hn.algolia.com/api/v1/items/40990768 | 一手（HN API 镜像） | 高 | SAPwned HN 全部评论原文，darefalcon/rvnx/uaas/cosmotic/mac-chaffee/jaaron 等批评逐条提取 |
| https://hn.algolia.com/api/v1/items/35370217 | 一手（HN API 镜像） | 高 | BingBang HN 帖子（5 分 0 评论，无讨论） |
| https://hn.algolia.com/api/v1/items/31213335 | 一手（HN API 镜像） | 高 | ExtraReplica HN 评论（含 mola 对 Wiz CEO 历史的评论） |
| https://hn.algolia.com/api/v1/search?query=BingBang&tags=story | 一手（HN API） | 高 | BingBang HN 故事元数据 |
| https://hn.algolia.com/api/v1/search?query=SAPwned+Wiz&tags=story | 一手（HN API） | 高 | SAPwned HN 故事元数据与 Wiz 博客 URL 确认 |
| https://hn.algolia.com/api/v1/search?query=darefalcon+extortion&tags=comment | 一手（HN API） | 高 | darefalcon 评论归属与日期确认（2024-07-18） |
| The Register / BleepingComputer / TechCrunch / Dark Reading SAPwned 报道 | 二手（媒体） | **未获取** | 多次抓取返回 403/404，媒体报道基调章节标注为弱证据 |
| SAP 官方 security note | 一手（厂商） | **未获取** | support.sap.com 需登录，SAP 回应经由 Wiz 转述，二手 |

### 可信度分级说明

- **高**：一手来源（Wiz 官方博客署名、HN API 原始评论），可直接引用。
- **中**：一手来源的二手转述（如 SAP 回应经由 Wiz 转述），需交叉验证。
- **未获取**：研究空白，明确标注，不臆测。

### 标注约定回顾

- 【他说过】= Hillai 在 Wiz 官方博客署名文章中的明确表达（如 "AI training requires running arbitrary code by definition"）。
- 【别人说他】= 第三方对 Wiz/Hillai 研究的明确评价（如 darefalcon 的 extortion 指控、jaaron 的 k8s-not-AI 质疑、mola 对 Wiz CEO 历史的评论）。注意：除少数特例外，绝大多数"别人说他"实际落在"Wiz Research"团队层面而非 Hillai 个人。
- 【你推断】= 基于证据的合理推断，明确与事实陈述分离。包括：Hillai 在 Wiz 研究谱系中的位置、SAPwned 争议为何集中、Wiz 商业成功如何放大伦理审视等。

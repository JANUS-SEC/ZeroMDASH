# Hillai Ben-Sasson — 长对话与即兴思考

> 信息源：YouTube oEmbed API + YouTube watch-page `shortDescription` 原文（一手）、Wiz 博客作者页与博客正文（一手，书面 ≠ 口头）、fwd:cloudsec 视频描述原文（一手，含 Hillai 官方 bio）、Crying Out Cloud 节目页（一手，仅有 TL;DR）。
> 已剔除 WebSearch 幻觉：WebSearch 返回"Hillai 是 Cilium/eBPF developer advocate"（错误）、"Hillai 与 Eli Ben-Sasson/StarkWare STARK 有关"（混淆同名，**错误**——Eli Ben-Sasson 是 StarkWare 联合创始人，与本研究对象无关）。凡未在此文件中给出可核验 URL 的 WebSearch 结果，一律不采信。
> 已剔除 DuckDuckGo HTML 搜索：对编程化访问返回空结果，未产生可核验链接。
> 与 `nir-ohfeld-perspective` 的 `02-conversations.md` 交叉印证：Nir 文件已核实两人合讲的两场 KubeCon EU 2025 演讲与 fwd:cloudsec EKS Playbook，本文件复核了这些视频的 oEmbed 与描述原文。

---

## 总览：可证实的"亲口发声"录音

经直接核验（YouTube oEmbed + watch-page `shortDescription` 原文逐字核验），Hillai Ben-Sasson 本人在以下场合以自己的声音讲话：

| 类型 | 数量 | 备注 |
|------|------|------|
| 真正的长形播客访谈（作为嘉宾） | **1** | Crying Out Cloud "SAPwned"（2024-07-17，仅 8:42，**短**，非长形） |
| 会议演讲录像（作为讲者） | **3** | KubeCon EU 2025 ×2（与 Nir Ohfeld 合讲）、fwd:cloudsec EKS Playbook ×1（与 Nir 合讲） |
| Black Hat / DEF CON / RSAC / Darknet Diaries / Risky Business / CyberWire / Security Now | **0 已核验** | 见下文"未证实线索"——Black Hat 有一个标题线索但**演讲是否交付未经核验** |

**关键观察**：与 Nir Ohfeld、Felix Wilhelm 类似，Hillai 的"亲口发声"主要走会议演讲通道，而非传统 infosec 播客巡讲。她**不是** Darknet Diaries / Risky Business / Security Now 的常客。她唯一可证实的播客嘉宾登场是 Wiz 自家频道 Crying Out Cloud 的一集——且仅 8 分 42 秒，更接近"研究速递"而非"长对话访谈"。这本身是一个性格/策略信号：她的对外发声高度依赖 Wiz 官方分发渠道，且 2024-2025 阶段几乎只在 Wiz 研究议程的联合讲者席上出现。

**官方 bio（两处独立核验，文字几乎一致）**：
- Wiz 博客作者页（https://www.wiz.io/blog/author/hillai-ben-sasson ，核验日期 2026-07-26）："Hillai Ben-Sasson is a security researcher based in Israel, part of the Wiz Research Team. Specializes in 'research and exploitation of web applications, application security, and finding vulnerabilities in complex high-level systems.' A frequent conference speaker recognized on MSRC's Most Valuable Researchers leaderboard."
- fwd:cloudsec EKS Playbook 视频描述原文（https://www.youtube.com/watch?v=HcNmkCRXFdE ，`shortDescription` 逐字核验）："Hillai Ben-Sasson is a security researcher based in Israel. As part of the Wiz Research Team, Hillai specializes in research and exploitation of web applications, application security, and finding vulnerabilities in complex high-level systems."
- **可信度**：高（两处独立来源、文字几乎逐字一致）
- **未独立核验项**："MSRC Most Valuable Researchers leaderboard"——此声明只见于 Wiz 博客作者页，未在 MSRC 官方页面直接核验（msrc.microsoft.com 不在沙箱白名单，DuckDuckGo 编程搜索返回空）。**标注为来源单一、未独立复核**。

---

## 一手：播客访谈

### 1. Crying Out Cloud — "SAPwned: SAP AI Core vulnerabilities - Special Guest: Hillai Ben-Sasson" (2024-07-17)

- **场合**：Crying Out Cloud 播客（Wiz 官方频道 @wizsecurity 托管）
- **URL（节目页）**：https://www.wiz.io/crying-out-cloud/sapwned-sap-ai-core-vulnerabilities-special-guest-hillai-ben-sasson （核验：HTTP 200，节目页存在）
- **URL（YouTube）**：https://www.youtube.com/watch?v=RPjcTIURF8o （oEmbed + watch-page 描述核验）
- **频道**：Wiz（@wizsecurity，oEmbed `author_name` 原文核验）
- **节目页署名 host**：Omer Mosheiov（节目页"Author"字段）
- **时长**：8 分 42 秒（`lengthSeconds:"522"` 原文核验）
- **发布日**：2024-07-17T10:43:50-07:00（`publishDate` 原文核验）
- **可信度**：高（节目存在性 + 元数据已核验）

**视频描述原文（一手，逐字）**：
> "📢 Tune in to our special episode with Hillai Ben-Sasson with all you need to know about #SAPwned.
> TL;DR - The Wiz Research Team uncovered serious vulnerabilities in SAP AI Core, revealing potential risks in #AI infrastructure."

**节目页其余内容**：仅一句 TL;DR + YouTube/Spotify/Apple Podcasts 三个收听链接。**无 transcript、无 show notes、无问题清单、无引用、无 Q&A 段落**。节目页相关上下文还列了三集其它 Crying Out Cloud 节目（CROC Talks with Snowflake's Haider Dost 2024-07-14、CROC News 2024-06-29、CROC Talks: RCE Vulnerability in Ollama 2024-06-23），与本集主题无直接关联。

**被追问时的回答方式**：**信息不足**——8 分 42 秒的集子短到接近"研究速递"，且无逐字转录。无法判断面对"你怎么发现这个的"追问时，Hillai 是讲方法论还是讲故事。需要听原始音频才能补全。

**即兴类比**：**信息不足**——未取得转录。8 分钟集子也限制了即兴发挥的空间。

**对责任披露时长的态度**：**信息不足**——未在节目描述中体现，未取得转录。

**意义**：这是目前**唯一可证实的 Hillai 作为播客嘉宾**的长对话录音。但时长与节目结构（"special episode"、TL;DR 速递风格）暗示它更接近"Wiz 研究成果速递 + 嘉宾点评"格式，而非 Darknet Diaries 式深度访谈。**真正能提取"即兴思考"的内容必须手动听这 8:42 音频**——本研究未做。

---

## 一手：会议演讲（含可能的 Q&A 环节）

会议演讲通常以"准备好的 talk + 主持人感谢 + 偶尔 Q&A"形式存在。下面每条都是 Hillai 作为讲者、视频 oEmbed 与 watch-page `shortDescription` 原文经核验的录音。**Q&A 环节是否被录制并发布未逐条核验**——需要在每个视频末尾手动检查。所有摘录均来自 YouTube 视频描述原文（一手），逐字核验。

### 2. KubeCon EU 2025 (London) — "Mish-Mesh: Abusing the Service Mesh to Compromise Kubernetes Environments"

- **URL**：https://www.youtube.com/watch?v=iMQR_l0ZvWU
- **频道**：CNCF [Cloud Native Computing Foundation]（oEmbed `author_name` 原文核验）
- **讲者署名（视频描述原文，逐字）**："Mish-Mesh: Abusing the Service Mesh to Compromise Kubernetes Environments - Hillai Ben-Sasson & Nir Ohfeld, Wiz"
- **oEmbed 标题**：同上（"H. Ben-Sasson, N. Ohfeld"）
- **可信度**：高

**摘要原文（一手，逐字）**：
> "Service mesh solutions are common components in almost every large Kubernetes environment. Many engineers and security teams have adopted solutions like Linkerd and Istio to better segment and isolate their Kubernetes networks. In this talk, we will demonstrate how we were able to exploit common misconfigurations and insecure features in popular service mesh solutions, to escalate low-severity vulnerabilities to critical service takeovers.
> Our real-life examples include several major cloud service providers, where these vulnerabilities allowed us to gain unauthorized access to internal systems and sensitive secrets. This talk will help engineers understand whether their service mesh deployment acts as a proper security barrier, and how to make sure that it does. Security teams – both attackers and defenders – will learn new techniques for hacking Kubernetes environments, and how to properly defend against them."

**讲者顺序信号**：在视频描述与 oEmbed 标题中，**Hillai 列在 Nir 之前**（"Hillai Ben-Sasson & Nir Ohfeld"）。与 fwd:cloudsec EKS Playbook（2024，Nir 在前）形成对比——见后文"与 Nir 的对比"。但**讲者顺序 ≠ 实际发言占比**，无法从描述判断谁讲哪段。

### 3. KubeCon EU 2025 (London) — "The Good, the Bad, and the Ugly: Hacking 3 Cloud Native AI Services With 1 Vulnerability" (NVIDIAScape)

- **URL**：https://www.youtube.com/watch?v=ZTiWXqYg97U
- **频道**：CNCF [Cloud Native Computing Foundation]（oEmbed 核验）
- **讲者署名（视频描述原文，逐字）**："The Good, the Bad, and the Ugly: Hacking 3 Cloud Native AI Services With 1 Vulnerability - Hillai Ben-Sasson & Nir Ohfeld, Wiz"
- **oEmbed 标题**：同上（"Hillai Ben-Sasson & Nir Ohfeld"）
- **可信度**：高

**摘要原文（一手，逐字）**：
> "With rising demand for AI workloads, SaaS providers are evolving their K8s-based GPU offerings, often built on NVIDIA Container Toolkit: the industry-standard framework for running GPU-based containers. In this talk, we'll show you how a single vulnerability in this fundamental framework impacted the entire cloud-native ecosystem – and how each environment handled a brand-new 0day.
> We'll walk through our discovery of this Pod-to-Node escape vulnerability, and its impact across 3 different providers: Azure, DigitalOcean, and Replicate. Each case began with a weak Pod running our exploit – but outcomes varied widely. One led to minor impact; another with lateral movement that triggered blue teamers; and one with complete service takeover.
> Join us to gain a firsthand look on how major cloud-native companies build their K8s environments, and the anatomy of a container escape vulnerability in the wild. Finally, learn how to build stronger K8s guardrails by examining the flaws we exploited."

**叙事结构信号**：摘要在描述三个 provider 时采用了**三段递进式戏剧结构**——"minor impact → lateral movement that triggered blue teamers → complete service takeover"。这种"逐级升级"的叙事节奏与 Hillai 在 SAPwned 博客中的写法（network bypass → cluster takeover 的逐级升级）一致。这暗示至少 NVIDIAScape 摘要的叙事笔法可能出自她手——但**这是从文风推断，非逐字验证**。

### 4. fwd:cloudsec — "The EKS Hacking Playbook: Lessons From 3 Years of Cloud Security Research"

- **URL**：https://www.youtube.com/watch?v=HcNmkCRXFdE
- **频道**：fwd:cloudsec（oEmbed 核验）
- **讲者署名（视频描述原文，逐字）**："Speakers: Nir Ohfeld & Hillai Ben-Sasson"（**Nir 在前**，与 KubeCon 2025 形成对比）
- **发布日**：2024-06-18（经 Nir 文件交叉印证，未在本研究独立复核发布日）
- **可信度**：高

**Hillai 官方 bio（视频描述原文，逐字，一手）**：
> "Hillai Ben-Sasson is a security researcher based in Israel. As part of the Wiz Research Team, Hillai specializes in research and exploitation of web applications, application security, and finding vulnerabilities in complex high-level systems."

**Nir 官方 bio（同视频描述原文，逐字，一手，用于对比）**：
> "Nir Ohfeld is a senior security researcher at Wiz. Ohfeld focuses on cloud-related security research and specializes in research and exploitation of cloud service providers, web applications, application security, and in finding vulnerabilities in complex high-level systems. Ohfeld and his colleagues disclosed some of the most notable cloud vulnerabilities, including ChaosDB and OMIGOD."

**摘要原文（一手，逐字）**：
> "Amazon Elastic Kubernetes Service (EKS) is one of the leading Kubernetes solutions in the cloud-managed space... EKS is a two-headed beast. On one hand, it's a full-fledged Kubernetes cluster, but on the other hand, it's an AWS service... Simple but common misconfigurations can expose critical assets to external attackers.
> ...we created a playbook for ourselves – what do we look for, as security researchers, when in a production EKS environment.
> ...Each example will present the mistake from the engineer's point of view, as well as the opposite point of view – how we exploited it as researchers."

**叙事结构信号**："two-headed beast"是一个**即兴式的拟人比喻**（在摘要里就出现），且"engineer's point of view vs researcher's point of view"是一个**双向视角框架**——这两个修辞在研究摘要中出现，说明她（或合讲的 Nir）偏好用比喻+对偶视角来组织技术叙事。但**无法判断这是 Hillai 还是 Nir 的笔法**——这是合讲摘要。

---

## 二手/未证实线索：Black Hat "Isolation or Hallucination?"

**线索来源（一手，来自 Hillai 自己的 SAPwned 博客）**：
- SAPwned 博客正文（https://www.wiz.io/blog/sapwned-sap-ai-vulnerabilities-ai-security ，核验日期 2026-07-26）末尾提及"an upcoming Black Hat talk: 'Isolation or Hallucination? Hacking AI Infrastructure Providers for Fun and Weights.'"
- **标题可信度**：高（出自她自己的博客，文字逐字核验）
- **可信度**：**演讲是否实际交付未核验**

**未能独立核验的原因**：
- blackhat.com 不在沙箱网络白名单；用 user-agent 伪装 curl 抓取 `https://www.blackhat.com/us-24/briefings/schedule/` 与 `/eu-24/briefings/schedule/` 均返回空内容（疑似 JS 渲染或反爬）。**Black Hat 官方议程未能在本研究中直接核验此 talk 的存在**。
- DuckDuckGo HTML 编程搜索（`"Isolation or Hallucination" "Fun and Weights"`）返回空，未产生可核验链接。
- YouTube 上未找到 Black Hat 官方频道上传的此 talk 录像（搜索未命中——但未做穷尽搜索）。

**推断**：SAPwned 博客发布于 2024-07-17，"upcoming Black Hat talk"通常指向 Black Hat USA 2024（2024-08）或 Black Hat EU 2024（2024-11）。标题双关"Isolation or Hallucination?"——既指 AI "幻觉"又指隔离失效，且"Weights"双关模型权重与"Fun and Profit"——这种双关修辞与 Hillai 在 SAPwned 标题里"SAPwned"（SAP + pwned）的玩字习惯一致。**风格上像她起标题**，但这是推断。

**诚实标注**：此线索的标题来自她自己的博客（一手），但 talk 是否实际交付、讲者是她单独还是与 Nir 合讲、是否在 YouTube 上有录像——**均未核验**。如要确认，需手动查 Black Hat USA 2024 / EU 2024 议程或听 Black Hat 官方 YouTube 频道。

---

## 书面叙事声音（作为口头表达的代理证据，明确标注 ≠ 说话）

由于可证实的口头录音仅 4 条且无逐字转录，以下从 Hillai 在 Wiz 博客的 5 篇文章（一手，书面）提取叙事特征，作为"她可能如何口头表达"的**间接代理证据**。**书面 ≠ 口头**，使用时须明确此限制。

### 已核验的博客文章清单

| # | 标题 | 日期 | 合作者 | URL |
|---|------|------|--------|-----|
| 1 | IngressNightmare: CVE-2025-1974 | 2025-03-24 | Nir Ohfeld, Ronen Shustin, Sagi Tzadik | https://www.wiz.com/blog/ingress-nginx-kubernetes-vulnerabilities |
| 2 | SAPwned: SAP AI vulnerabilities | 2024-07-17 | （Solo，Hillai 单独署名） | https://www.wiz.io/blog/sapwned-sap-ai-vulnerabilities-ai-security |
| 3 | 38TB of data exposed by Microsoft AI researchers | 2023-09-18 | Ronny Greenberg | https://www.wiz.io/blog/38-terabytes-of-private-data-accidentally-exposed-by-microsoft-ai-researchers |
| 4 | BingBang: How a simple developer mistake... | 2023-03-29 | Raaz Herzberg, Shir Tamari | https://www.wiz.io/blog/bingbang |
| 5 | BingBang: AAD misconfiguration... | 2023-03-29 | （同上） | https://www.wiz.io/blog/azure-active-directory-bing-misconfiguration |

### 从博客正文提取的叙事 DNA

**1. 方法论式开篇 + 第一人称复数主体**
- SAPwned（一手）："Our research began as an SAP customer, with basic permissions allowing us to create AI projects."
- 38TB（一手）："As part of the Wiz Research Team's ongoing work on accidental exposure of cloud-hosted data, the team scanned the internet for misconfigured storage containers."
- 特征：开篇即交代**研究起点**与**主体身份**（"as a customer"、"as part of the team"），把读者带入调查者视角，而非直接抛漏洞。这是"讲故事"而非"讲方法论"的开头——她先建立"我们是谁、从哪里开始"。

**2. 等价/类比框架**
- SAPwned（一手）："AI models and applications – which is equivalent to executing arbitrary code."
- 38TB（一手，关于 SAS token）："essentially providing the same access level as the account key itself" / "as a backdoor"
- 特征：她偏好用**等价陈述**（X 等价于 Y）来降低技术门槛——把 AI 模型执行等价为 RCE、把 SAS token 等价为 account key/backdoor。这种"用更危险的概念锚定温和概念"的修辞，在口头表达中很可能复现——但**未核验**。

**3. 拟人与玩字**
- SAPwned 标题：SAP + pwned 的合并
- SAPwned（一手）："Free from our traffic shackles, we started scanning our Pod's internal network."（"traffic shackles"——把 Istio 流量限制拟人化为"镣铐"）
- SAPwned（一手）："which ironically enough was '1337' (yeah, really)"（对 UID 1337 的自嘲式旁白——**这是罕见的"作者个性泄露"瞬间**，是推断她口头表达风格的强信号）
- IngressNightmare（一手）："`nginx -t` should be considered harmful"（echo Dijkstra "GOTO considered harmful"——学术式玩字）
- 特征：玩字与拟人并存，且偶有自嘲旁白。这暗示她在口头表达中**可能**会用比喻和自嘲调节技术叙事的节奏——但博客经过编辑，口头是否保留未核验。

**4. 渐进升级结构**
- SAPwned：network bypass → Istio traffic shed → internal network scan → full cluster takeover（逐级升级）
- NVIDIAScape 摘要：minor impact → lateral movement → complete service takeover（逐级升级，三人三档）
- BingBang：登录敏感界面 → 修改搜索结果 → 窃取 Office 365 凭据（三段递进）
- 特征：她偏好**三段式或N段式渐进升级**叙事，每一段都比上一段更严重。这种结构在演讲中天然适合制造悬念——NVIDIAScape 摘要的"three providers, three outcomes"几乎是为舞台设计的。

**5. 行业呼吁式收尾**
- SAPwned（一手）："the industry must improve its isolation and sandboxing standards when running AI models"
- SAPwned（一手）："AI training requires running arbitrary code by definition; therefore, appropriate guardrails should be in place"
- 特征：从单一漏洞上升到行业层呼吁。与 Nir 的"Call-to-Action: We Need a Cloud Vulnerability Database"立场一脉相承——两人都偏好把单点发现框架化为系统性问题。

**6. 责任框架：厂商为主、客户为受害方**
- SAPwned（一手）："the internal network was perceived as trusted"（批评 SAP 的信任模型）
- BingBang（一手）：标题本身强调"developer mistake"，但在 AAD 上下文里又说"with only the click of a button, a user can accidentally expose a sensitive service"——责任在平台设计 vs 开发者之间游移
- 38TB（一手）："it's important to raise awareness of relevant security risks at every step of the AI development process"
- 特征：与 Nir "customers were not at fault"立场一致——把托管服务隔离失效归责于厂商架构，客户定位为潜在受害方。但 BingBang 是个反例：她把那次的根因归结为"developer mistake"，相对中性。**保留矛盾**：她的责任框架不是铁板一块，而是随漏洞类型滑动。

---

## 披露时间表模式（行为信号，非口头表态）

从博客正文的"Responsible Disclosure Timeline"段提取的**行为模式**：

| 研究 | 首次报告 | 公开披露 | 间隔 | 厂商关系基调 |
|------|----------|----------|------|--------------|
| 38TB Microsoft AI | 2023-06-22 | 2023-09-18 | ~3 个月 | 中性，链到 MSRC 博客 |
| SAPwned | 2024-01（首次） | 2024-07-17 | ~6 个月 | "We thank them for their cooperation"，patch bypass 后再报，迭代式 |
| IngressNightmare | 2024-12-31 | 2025-03-24 | ~3 个月 | "worked closely with the Kubernetes maintainers"，具名感谢 Marco Ebert |

**模式**：Hillai 的披露节奏与 Nir 一致——**长周期协商（约 3-6 个月）、迭代式 patch-bypass-再报、公开致谢厂商协作**。**未见任何 Project Zero 式强制 90 天硬性立场的表态**。

**对责任披露时长的态度**：**信息不足**——以上是从行为推断，**未取得 Hillai 在录音或博客中亲口对"90 天 vs 厂商协商时长"的立场表态**。需要听完 Crying Out Cloud SAPwned 集（8:42）或她在 KubeCon 2025 演讲末尾的 Q&A 才能补全。

---

## 与 Nir Ohfeld 的对比（基于本文件与 `nir-ohfeld-perspective/02-conversations.md` 的交叉印证）

### 公开发声渠道

| 维度 | Hillai | Nir |
|------|--------|-----|
| 长形播客嘉宾 | 1 次（Crying Out Cloud SAPwned，**8:42**，短） | 2 次（CyberWire 2021 14:16、Crying Out Cloud IngressNightmare 2025 22:27） |
| 会议演讲 | 3 次（KubeCon ×2、fwd:cloudsec ×1，**全部与 Nir 合讲**） | 8+ 次（Black Hat ×3、RSAC ×1、KubeCon ×2、fwd:cloudsec ×4） |
| 单人主讲会议演讲 | **0 已核验**（所有已核实演讲均与 Nir 合讲） | 多次单人或与不同合讲者 |

**观察**：Hillai 目前**没有可核实的单人主讲会议演讲**——她的所有舞台发声都与 Nir 合讲。这与 Nir 早期（2021-2022）与 Shir Tamari、Sagi Tzadik 合讲的轨迹类似，暗示她处于"被 Nir 带上舞台"的阶段，尚未独立开讲。**但这只是从公开录像推断，可能存在未上传的内部/小会单人演讲**。

### 官方 bio 的专精差异（一手，fwd:cloudsec 视频描述原文逐字核验）

- **Hillai**："specializes in research and exploitation of **web applications, application security**, and finding vulnerabilities in **complex high-level systems**"
- **Nir**："focuses on **cloud-related security research**... research and exploitation of **cloud service providers**, web applications, application security..."
- **差异**：Nir 的专精锚定在**云服务商（CSP）层面**（ChaosDB、OMIGOD 都是 CSP 漏洞）；Hillai 的专精锚定在**web 应用 / 应用安全 / 复杂高层系统**，**未明确提及 cloud service providers**。这与她独立署名的 SAPwned（SAP AI Core——一个 SaaS/PaaS 层面的应用级漏洞研究）主题一致。
- **职级差异**：同一 fwd:cloudsec 视频描述里，Nir 头衔是 **"senior security researcher"**，Hillai 是 **"security researcher"**（无 senior）。Nir 在 2025 已晋升 Head of Vulnerability Research（经 Nir 文件核验）；Hillai 的职级在本研究范围内未见更新声明。

### 讲者署名顺序的演变

- 2024 fwd:cloudsec EKS Playbook：**Nir 在前**（"Nir Ohfeld & Hillai Ben-Sasson"）
- 2025 KubeCon Mish-Mesh：**Hillai 在前**（"Hillai Ben-Sasson & Nir Ohfeld"）
- 2025 KubeCon NVIDIAScape：**Hillai 在前**

**推断**：2024→2025 出现了顺序反转。可能的解读：(a) Hillai 在这两场 KubeCon talk 中承担了更多准备/叙事主导工作；(b) 字母序偶然（H 在 N 前）；(c) Wiz 内部对两人对外形象的策略调整。**无法从描述判断谁实际发言更多**——需要看视频。

### 叙事分工的可能线索（弱信号，未逐字核验）

Nir 文件推测 Nir 偏技术细节、Shir Tamari 偏研究叙事。Hillai 接替了 Shir 的"研究叙事"位置——她独立署名的 SAPwned 博客的叙事性（"Our research began as an SAP customer"、"traffic shackles"、"1337, yeah really"）比 Nir 独立署名博客更强。**弱信号**：在 Nir+Hillai 组合里，Hillai 可能承担"叙事/比喻/舞台节奏"职能，Nir 承担"技术细节/exploit chain"职能——但这**未经视频逐字验证**，是从博客文风 + 摘要笔法推断。**保留为推测，不作为结论**。

---

## 跨录音可提取的稳定立场（弱，因录音不足）

由于可核实的口头录音仅 4 条且无转录，**无法像 Nir 那样提取"跨录音稳定立场"**。以下立场是从博客书面表达提取，**口头是否一致未核验**：

1. **AI 基础设施的隔离标准需行业级提升**——SAPwned 博客"the industry must improve its isolation and sandboxing standards when running AI models"。与 NVIDIAScape KubeCon 演讲主题（"build stronger K8s guardrails"）一脉相承。
2. **托管服务隔离失效归责厂商**——SAPwned 批评 SAP 的"internal network was perceived as trusted"信任模型。
3. **服务网格 ≠ 安全屏障**——Mish-Mesh 摘要"whether their service mesh deployment acts as a proper security barrier"——挑战"service mesh 自动提供网络隔离"的常见假设。
4. **长周期协商式披露**——行为层面（3-6 个月、迭代 patch-bypass、公开致谢厂商），非口头表态。

---

## 拒绝回答 / 回避的问题（信息不足，诚实标注）

**未取得任何录音中"Hillai 被追问后回避 PoC 细节 / 0day 未公开部分"的可证实片段**。要核验此类瞬间，需要：
- 听完 Crying Out Cloud SAPwned 集（8:42）——但该集时长可能不足以包含 Q&A 或追问
- 听完两场 KubeCon 2025 演讲（33:10 与 32:12）的末尾 Q&A 段
- 听完 fwd:cloudsec EKS Playbook（24:49）末尾 Q&A

**本研究未做上述逐一听录**。如果用户需要这部分内容，建议优先手动听 fwd:cloudsec EKS Playbook（社区会议 Q&A 氛围最松）与两场 KubeCon 末尾。**Nir 文件对同样的缺口也作了同样标注**——两人合讲的演讲，单凭描述无法分离各自的回避模式。

---

## 立场变化 / 澄清瞬间（信息不足）

- **未取得**可证实的"Hillai 被质疑后调整说法"的录音片段。
- 一个**值得后续手动核查的候选**：NVIDIAScape 摘要里"three providers, three outcomes"的戏剧结构，如果现场有观众追问"为什么三个 provider 结果不同"，她可能需要澄清"是 provider 配置差异还是漏洞本身差异"——但这是假设，**未核验**。

---

## 已核验的纠正（避免错误归因）

以下在搜索"Hillai Ben-Sasson"时高频出现或被 WebSearch 推荐，但**经核验后不采用**：

1. **WebSearch 幻觉："Hillai Ben-Sasson 与 Cilium/eBPF 有关，是云原生生态 developer advocate"**——**错误**。WebSearch 工具自己承认"无直接搜索能力"并臆造内容。Hillai 是 Wiz 安全研究员，与 Cilium/eBPF developer advocacy 无关。不采用。

2. **WebSearch 幻觉："Hillai Ben-Sasson 与 StarkWare/Starknet/STARK 零知识证明有关"**——**混淆同名**。StarkWare 联合创始人是 **Eli** Ben-Sasson（不同人，密码学家），与本研究对象 Hillai Ben-Sasson（Wiz 安全研究员）无关。不采用。

3. **fwd:cloudsec "The Good, the Bad, and the Ugly: Hacking 3 CSPs with 1 Vulnerability"** (https://www.youtube.com/watch?v=TkDsnzlPJAg)——实际讲者是 Andres Riancho（Wiz），**不是 Hillai**。Nir 文件已标注此条为"Andres 主讲"。Hillai 与 Nir 的 KubeCon 2025 演讲"...Hacking 3 Cloud Native AI Services With 1 Vulnerability"标题相似但内容不同（CSP vs Cloud Native AI Services），**不要混淆**。这条同样在 Nir 文件中标注过。

4. **Black Hat SecTor 2025 "The Good, the Bad, and the Ugly: Hacking 3 Cloud Providers with 1 Vulnerability"**——基于同名 fwd:cloudsec 由 Andres 主讲推断，**Hillai 在此的可能性低**。可信度：低。

---

## 未证实的候选（信息不足，不纳入一手）

- **Black Hat "Isolation or Hallucination? Hacking AI Infrastructure Providers for Fun and Weights"**：标题来自 Hillai 自己的 SAPwned 博客（一手），但**演讲是否实际交付、讲者构成、是否有录像**均未核验。Black Hat 官方议程页面对编程访问返回空。**标注为 UNVERIFIED，不作为一手材料使用**，仅作为"她可能有一场单人 Black Hat talk"的线索。
- **Darknet Diaries / Risky Business / CyberWire / Security Now 嘉宾登场**：未找到任何可核验证据。DuckDuckGo 编程搜索返回空。**标注为"未发现"，不代表她从未出现**——可能存在未索引的早期出场，但本研究范围内无证据。
- **MSRC Most Valuable Researchers leaderboard**：Wiz 博客作者页声明她"recognized on"该榜，但**未在 MSRC 官方页面直接核验**。来源单一。可信度：中（Wiz 官方页声明，但未独立复核）。

---

## Wiz 博客中嵌入的 Crying Out Cloud 链接（一手，证实她确实上过这档节目）

- SAPwned 博客（https://www.wiz.io/blog/sapwned-sap-ai-vulnerabilities-ai-security ）末尾嵌入了 "Listen now" 链接指向 `/crying-out-cloud/sapwned-sap-ai-core-vulnerabilities-special-guest-hillai-ben-sasson`——**这是她自己博客里嵌的链接，证实她确实作为嘉宾上了 Crying Out Cloud SAPwned 集**。这是本文件"播客访谈 #1"一节的独立交叉印证（博客嵌入 ↔ 节目页存在 ↔ YouTube oEmbed 存在，三重核验）。

---

## X / Twitter 主页

- **Handle**：@hillai（经 Wiz 博客作者页 bio 核验，IngressNightmare 博客末尾联系段也标注 `@hillai`）
- **内容不可访问**：需登录，本研究未取得推文内容。

---

## 信息缺口与下一步

**真正的长对话访谈缺口**：
1. **唯一可证实的播客嘉宾登场仅 8:42**——Crying Out Cloud SAPwned 集太短，难以提取即兴类比、立场变化、被追问后的回答方式。
2. **两场 KubeCon 2025 演讲的 Q&A 段未取得**——KubeCon 演讲通常 30+ 分钟，末尾常有 5-10 分钟 Q&A，是最有可能含即兴思考的录音，但**未取得逐字转录**。
3. **fwd:cloudsec EKS Playbook（24:49）末尾 Q&A 未取得**。
4. **未发现** Hillai 出现在 Darknet Diaries / Risky Business / Security Now / CyberWire Daily 等主流 infosec 播客——这本身是信号：她偏好"Wiz 研究带 + CNCF/fwd:cloudsec 社区会议"渠道，而非独立播客巡讲。与 Nir 的渠道偏好一致。

**建议的后续手动补做**（如需深化"即兴思考"维度）：
1. **听 Crying Out Cloud SAPwned 集（8:42）全文**——提取她亲口的比喻、对 SAP 协作的措辞、对 AI 隔离标准的呼吁口吻。这是她唯一可独立提取"口头表达 DNA"的录音。
2. **听两场 KubeCon 2025 演讲（共 ~65 分钟）**——分离 Hillai 与 Nir 各自讲哪段，提取即兴比喻与 Q&A 回答。**这是验证"两人叙事分工"假设的唯一途径**。
3. **听 fwd:cloudsec EKS Playbook（24:49）末尾 Q&A**——社区会议氛围最松，最可能含即兴回答。
4. **手动查 Black Hat USA 2024 / EU 2024 议程**，核实"Isolation or Hallucination?"是否实际交付、讲者构成。

**已确认的稳定结论**（不依赖听录音）：
- Hillai 的公开交流主要走"会议演讲 + Wiz 自家播客"通道，不走"独立播客巡讲"通道——与 Nir 的渠道策略一致
- 她目前所有可核实的会议演讲**均与 Nir 合讲**，无单人主讲已上传录像
- 她的官方专精锚定在 **web 应用 / 应用安全 / 复杂高层系统**，与 Nir 锚定 **云服务商** 形成互补（同一 fwd:cloudsec 视频描述原文逐字核验）
- 她的书面叙事 DNA：方法论式第一人称复数开篇 + 等价/类比框架 + 玩字与拟人 + 三段渐进升级结构 + 行业呼吁式收尾
- 披露节奏：长周期协商（3-6 个月）、迭代 patch-bypass、公开致谢厂商——与 Nir 一致，与 Project Zero 式 90 天硬立场未见证据
- 讲者署名顺序在 2024→2025 出现反转（Nir 在前 → Hillai 在前），暗示她在 KubeCon 2025 阶段承担了更多叙事主导工作——但**未经视频逐字验证**

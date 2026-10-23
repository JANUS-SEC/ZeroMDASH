# Nir Ohfeld — 长对话与即兴思考

> 信息源：YouTube oEmbed API + 视频描述原文（一手）、Wiz 博客作者页 + 嵌入视频（一手）、fwd:cloudsec/Black Hat/RSAC/CNCF 官方频道视频描述（一手）。每节标注可信度。
> 已剔除同名混淆：电影导演 Nir Ohfeld（《No Other Land》联合导演）出现在 Podchaser，与本研究无关，未采用。
> 已剔除"看似 Nir 但实为同事"的录音：Crying Out Cloud BingBang 集是 Ami Luttwak（Wiz CTO），fwd:cloudsec「Good/Bad/Ugly 三家云一个漏洞」是 Andres Riancho。这两条虽与 Nir 的研究主题重叠，但不是他本人在说话。

---

## 总览：可证实的"亲口发声"录音

经直接核验（YouTube oEmbed + 视频描述原文），Nir Ohfeld 本人在以下场合以自己的声音讲话：

| 类型 | 数量 | 备注 |
|------|------|------|
| 真正的长形播客访谈（作为嘉宾） | **2** | CyberWire Research Saturday (2021)、Crying Out Cloud (2025) |
| 会议演讲录像（作为讲者） | **8+** | Black Hat ×3、RSAC ×1、KubeCon ×2、fwd:cloudsec ×4+ |
| DEF CON / Darknet Diaries / Risky Business / Security Now | **0** | 未找到可证实的出场 |

**关键观察**：与 Felix Wilhelm 类似，Nir 的"亲口发声"主要走会议演讲通道，而非传统 infosec 播客巡讲。他不是 Darknet Diaries / Risky Business 的常客。这本身是一个性格/策略信号：他偏好"以研究为中心、由 Wiz 或会议官方分发"的渠道，而不是独立播客主持人的访谈椅。

**职业头衔更新（2025）**：Crying Out Cloud 2025-03 集视频描述原文将其标注为 **"Head of Vulnerability Research at Wiz"**——已从"Senior Security Researcher"（RSAC 2022 描述）晋升为研究部门负责人。

---

## 一手：播客访谈

### 1. CyberWire Research Saturday — "Discovering ChaosDB" (2021-12-18)

- **场合**：CyberWire Research Saturday（N2K Networks 出品，主持人 Dave Bittner）
- **URL**：https://www.youtube.com/watch?v=hlNnzQP59Js
- **时长**：14:16
- **同场嘉宾**：Sagi Tzadik（ChaosDB 共同发现者，Wiz）
- **可信度**：高（YouTube oEmbed + 视频描述原文核验）
- **视频描述原文（一手）**："Guests Sagi Tzadik and Nir Ohfeld of cloud security company Wiz join Dave to discuss their research 'ChaosDB: How we hacked thousands of Azure customers' databases.' ... In this case, customers were not at fault."

**可证实的访谈要点**（基于描述与 ChaosDB 博客交叉印证，非逐字转录）：
- 讨论 Azure Cosmos DB Jupyter Notebook 功能的跨租户数据访问问题
- 强调"customers were not at fault"——一个 Nir 反复在多个渠道强调的论点：云漏洞的责任不在客户，而在云厂商的托管服务实现
- 提到 Microsoft 的赏金（约 $40K）

**追问回答方式**：未取得逐字转录，**信息不足**——无法判断面对"你怎么发现这个的"追问时，他是讲方法论还是讲故事。但研究本身的故事性（"two lines of code" 标题）暗示他偏好叙事化表达。

**即兴类比**：**信息不足**——14 分钟集子短，未取得转录。

---

### 2. Crying Out Cloud — IngressNightmare (2025-03-25)

- **场合**：Crying Out Cloud 播客（Wiz 官方频道 @wizsecurity 托管），主持人 Amitai Cohen & Eden Koby Naftali
- **URL**：https://www.youtube.com/watch?v=mjwLEbGA4mk
- **时长**：22:27
- **嘉宾**：Nir Ohfeld（头衔：Head of Vulnerability Research at Wiz）
- **可信度**：高（YouTube oEmbed + 视频描述原文核验）
- **视频描述原文（一手）**："In this episode of Crying Out Cloud, Amitai Cohen & Eden Koby Naftali are joined by Nir Ohfeld — Head of Vulnerability Research at Wiz."

**可证实的访谈要点**：
- 主题：Ingress-NGINX unauthenticated RCE（CVE-2025-1974），即"IngressNightmare"
- 讨论 Kubernetes 准入控制器（admission controllers）作为下一波攻击面的判断

**即兴类比 / 立场变化**：**信息不足**——未取得逐字转录，无法提取即兴比喻或现场澄清立场的瞬间。需要听原始音频才能补全。**这是一条值得后续手动补做的缺口**：22 分钟、Nir 头衔升级后第一次出现在 Wiz 自家播客——是最有可能包含即兴思考的录音。

---

## 一手：会议演讲（含可能的 Q&A 环节）

会议演讲通常以"准备好的 talk + 主持人感谢 + 偶尔 Q&A"形式存在。下面每条都是 Nir 作为讲者、视频描述原文经核验的录音。**Q&A 环节是否被录制并发布未逐条核验**——需要在每个视频末尾手动检查。

### 3. Black Hat — "ChaosDB: How We Hacked Databases of Thousands of Azure Customers"

- **URL（live talk 版）**：https://www.youtube.com/watch?v=RAz1ml-qhnk （34:49）
- **URL（rev 版）**：https://www.youtube.com/watch?v=QiJAxo30w6U
- **讲者**：Nir Ohfeld & Sagi Tzadik（描述原文核验）
- **可信度**：高
- **Nir 自己的 Wiz 博客**（/blog/how-we-broke-the-cloud-with-two-lines-of-code-the-full-story-of-chaosdb）将这条标注为 "BlackHat 2021 live talk"，对应 Black Hat EU 2021 briefing 页面：https://www.blackhat.com/eu-21/briefings/schedule/#chaosdb-how-we-hacked-databases-of-thousands-of-azure-customers-25200

### 4. Black Hat — "Security Industry Call-to-Action: We Need a Cloud Vulnerability Database"

- **URL**：https://www.youtube.com/watch?v=JEA_Zgi8Tjg
- **可信度**：高
- **Nir 自己的 ExtraReplica 博客**（/blog/ssh-and-tdes-bypassing-cryptography-on-azure-postgresql-flexible-server）写"watch our Black Hat session"指向此视频
- **意义**：这是 Nir **主动推动行业议程**的演讲——呼吁建立云漏洞数据库。可视为他作为研究者的立场声明："云漏洞需要独立于厂商的、可查询的归档机制"。

### 5. Black Hat EU 2022 — "Pwning Cloud Vendors with Untraditional PostgreSQL Vulnerabilities"

- **URL**：https://www.youtube.com/watch?v=X6CiUD3EcfQ （39:10）
- **讲者**：Shir Tamari & Nir Ohfeld（描述原文核验："Presented by Shir Tamari & Nir Ohfeld"）
- **主题**：ExtraReplica——Azure PostgreSQL Flexible Server 跨租户隔离绕过
- **可信度**：高
- **观察**：Shir Tamari 是 Nir 最频繁的演讲搭档。两人合作模式值得注意：Shir 偏向研究叙事，Nir 偏向技术细节——但这是基于博客文风推断，**未在录音中逐字验证**。

### 6. RSAC 2022 — "The Cloud Gray Zone: Vulnerabilities Found in Azure Built-in VM Agents"

- **URL**：https://www.youtube.com/watch?v=QNKT7ocTibk （43:19）
- **讲者**：Nir Ohfeld (Senior Security Researcher, Wiz) | Shir Tamari (Head of Research, Wiz)——描述原文核验
- **主题**：OMIGOD / "Secret Agent"——Azure 内置 VM agent 漏洞
- **可信度**：高
- **意义**：43 分钟时长 + RSA 演讲通常包含 Q&A——是另一条最可能含即兴问答的录音。

### 7. KubeCon EU 2025 (London) — "Mish-Mesh: Abusing the Service Mesh to Compromise Kubernetes Environments"

- **URL**：https://www.youtube.com/watch?v=iMQR_l0ZvWU （33:10）
- **讲者**：Hillai Ben-Sasson & Nir Ohfeld, Wiz（描述原文核验）
- **主题**：Linkerd/Istio service mesh 滥用
- **可信度**：高
- **观察**：Hillai Ben-Sasson 是 Nir 在 2024-2025 阶段最频繁的合作者（取代了早期 Shir Tamari 的位置）。

### 8. KubeCon 2025 — "The Good, the Bad, and the Ugly: Hacking 3 Cloud Native AI Services With 1 Vulnerability"

- **URL**：https://www.youtube.com/watch?v=ZTiWXqYg97U （32:12）
- **讲者**：Hillai Ben-Sasson & Nir Ohfeld, Wiz（描述原文核验）
- **主题**：NVIDIA Container Toolkit（CVE-2025-23266 / "NVIDIAScape"）跨三家云原生 AI 服务
- **可信度**：高

### 9-12. fwd:cloudsec 系列（社区会议，社区记录）

fwd:cloudsec 是云安全社区会议，演讲常偏实践、Q&A 氛围更松——是即兴表达最可能出现的渠道。

| # | 标题 | URL | 时长 | 发布日 |
|---|------|-----|------|--------|
| 9 | Scanning the internet for external cloud exposures | https://www.youtube.com/watch?v=rbHALyrxj0Y | 26:23 | 2023-07-13 |
| 10 | Secret Agents: Demystifying (and Pwning) Cloud Middleware | https://www.youtube.com/watch?v=jlSQssYwNW4 | 26:53 | 2022-08-03 |
| 11 | Push-Pull-Pwn: Hacking the Cloud through Container Registry Poisoning | https://www.youtube.com/watch?v=kJzfNeQ7E0U | 23:01 | 2026-06-01 |
| 12 | The EKS Hacking Playbook: Lessons From 3 Years of Cloud Security Research | https://www.youtube.com/watch?v=HcNmkCRXFdE | 24:49 | 2024-06-18 |

- **可信度**：高（描述原文核验，Nir 名字出现在每条标题或描述中）
- **#10 描述原文**："Speakers: Nir Ohfeld (@nirohfeld), Rotem Lipowitch (@rotemlipowitch). Nir Ohfeld is a security researcher from Israel. Nir currently does cloud-related security research at Wiz."
- **#12 描述原文**："Speakers: Nir Ohfeld & Hillai Ben-Sasson. Nir Ohfeld is a senior security researcher at Wiz. Ohfeld and his colleagues disclosed some of the most notable cloud vulnerabilities, including ChaosDB and OMIGOD."

---

## 跨录音可提取的稳定立场（一手 + 二手交叉印证）

以下立场在 Nir 多个演讲主题中重复出现，可信度较高，因为它们是他**主动选择的演讲议程**而非被动回答：

1. **云漏洞需要独立于厂商的归档**——Black Hat "Call-to-Action: We Need a Cloud Vulnerability Database" 演讲本身就是这个立场的最高表达。
2. **托管服务的责任在厂商而非客户**——CyberWire ChaosDB 集描述原文 "customers were not at fault"。
3. **"云的灰色地带"（Cloud Gray Zone）**——RSAC 2022 演讲标题本身就是一个框架性论断：云厂商内置组件（VM agent、middleware）是责任模糊地带。
4. **服务网格与 AI 基础设施是下一波攻击面**——KubeCon 2025（Mish-Mesh）与 KubeCon 2025（NVIDIAScape）的议程选择本身就是预判。

---

## 拒绝回答 / 回避的问题（信息不足）

**诚实标注**：未取得任何录音中"Nir 被追问后回避 PoC 细节 / 0day 未公开部分"的可证实片段。要核验此类瞬间，需要：
- 听完上述 4 个 fwd:cloudsec 录像的 Q&A 段（每段约 25 分钟，末尾通常有 2-3 分钟 Q&A）
- 听完 RSAC 2022 的 43 分钟录像末尾
- 听完 Black Hat EU 2022 的 39 分钟录像末尾

**未做上述逐一听录**。如果用户需要这部分内容，建议优先手动听 fwd:cloudsec #10 和 #12，因为社区会议 Q&A 氛围最松、最可能含即兴回答。

---

## 对责任披露时长的态度（信息不足）

- 未取得 Nir 在录音中**亲口**对 90 天 vs 厂商协商时长的表态。
- 二手证据：ChaosDB（2021-08 披露、2021-12 演讲）和 ExtraReplica（2022-01 披露、2022-11 演讲）的"披露到公开演讲"间隔约 4-10 个月，暗示 Wiz 团队倾向**长周期协商**而非强制 90 天。但这是从行为推断，**未经 Nir 亲口确认**。
- 项目零式强制 90 天的立场，Nir 没有公开录音表态。

---

## 立场变化 / 澄清瞬间（信息不足）

- 未取得可证实的"Nir 被质疑后调整说法"的录音片段。
- 一个值得后续手动核查的候选：Black Hat "Call-to-Action: We Need a Cloud Vulnerability Database"（#4）演讲，如果存在 Q&A，可能含云厂商代表反驳、Nir 澄清立场——但这是假设，**未核验**。

---

## 已核验的纠正（避免错误归因）

这些录音在搜索" Nir Ohfeld"时高频出现，但**经核验后 Nir 不是讲者**：

1. **Crying Out Cloud #3 — "The Story Of The BingBang Vulnerability"** (https://www.youtube.com/watch?v=FWA6MmBHx7A)
   - 实际嘉宾：Ami Luttwak（Wiz 联合创始人兼 CTO）
   - **不是 Nir**——尽管 Nir 是 BingBang 共同发现者之一。这一条容易被误引。

2. **fwd:cloudsec — "The Good, the Bad, and the Ugly: Hacking 3 CSPs with 1 Vulnerability"** (https://www.youtube.com/watch?v=TkDsnzlPJAg)
   - 实际讲者：Andres Riancho（Wiz Vulnerability Research 团队成员）
   - **不是 Nir**。Nir 与 Hillai 的 KubeCon 2025 演讲"…Hacking 3 Cloud Native AI Services With 1 Vulnerability"标题相似但内容不同，不要混淆。

3. **Black Hat SecTor 2025 — "The Good, the Bad, and the Ugly: Hacking 3 Cloud Providers with 1 Vulnerability"** (https://www.youtube.com/watch?v=O49EgRnu4VU)
   - 描述未明确讲者，基于同名 fwd:cloudsec 演讲由 Andres 主讲推断，**Nir 在此的可能性低**。可信度：低。

---

## 未证实的候选（信息不足，不纳入一手）

- **DEF CON 27 "Sardine and Bird: The Biggest Web Cache Deception to Date"**（与 Pavel Shulman 合讲）：WebSearch 返回了 YouTube URL，但**经 DuckDuckGo 复核返回"无结果"，DEF CON 媒体服务器上的 PDF URL 返回 404**。标题与作者署名（Imperva 时期研究主题：Web Cache Deception）貌似合理，但**录音/PDF 是否真实存在未经证实**。标注为 UNVERIFIED，不作为一手材料使用。
- **DEF CON 31/32 "StuxLFS" / "Adversarial Habits" 与 Sharon Brizinov**：WebSearch 工具返回了貌似合理的标题与 URL，但**经直接核验无法证实**——疑似 LLM 工具编造。本研究不采用。

---

## Wiz 博客中嵌入的视频（一手研究，但讲者不一定是 Nir）

以下视频被嵌入 Nir 自己的 Wiz 博客文章中，因此是他研究的一部分，但视频讲者未在标题/描述中明确标注为 Nir：

- "Breaking NVIDIA Triton: CVE-2025-23319" (https://www.youtube.com/watch?v=GaUqbT6cKEs) — 嵌入 /blog/nvidia-triton-cve-2025-23319-vuln-chain-to-ai-server
- "ChaosDB - Azure Cosmos DB Account Takeover Vulnerability Full Exploit" (https://www.youtube.com/watch?v=yNGKqG7hefI) — 演示视频，可能是配音或无对白

**Nir 的 Wiz 作者主页**：https://www.wiz.io/authors/nir-ohfeld — 列出约 25 篇博客，覆盖 ChaosDB、OMIGOD、ExtraReplica、Secret Agent、CodeBreach、NVIDIAScape、NVIDIA Triton、IngressNightmare、zeroday.cloud（2025）。这是研究他书面表达的入口，但**书面表达不属于"长对话"范畴**，归入 `01-writings.md`。

---

## zeroday.cloud 2025（Nir 联合发起的事件）

- **URL**：https://www.youtube.com/watch?v=rv7wEhN-9no （Day 1 直播）
- **性质**：2025 年 Black Hat EU 期间由 AWS、Microsoft、Google Cloud、Wiz Research 联合发起的云漏洞披露活动
- **Nir 的角色**：联合发起人（其 X 推文描述原文："@awscloud, @msftsecurity, @googlecloud and @wiz_io Research are joining forces to launch zeroday.cloud at @BlackHatEvents EU!"）
- **可信度**：中（Nir 联合发起已核验，具体在哪个段落发言未逐段核验）
- **意义**：这是他"推动云漏洞数据库"议程（见 #4 Black Hat 演讲）的**行动化**——从演讲呼吁到实际发起跨厂商活动。可视为其立场在 2025 年落地的证据。

---

## X / Twitter 主页

- **Handle**：@nirohfeld（经 fwd:cloudsec 视频描述原文核验："Speakers: Nir Ohfeld (@nirohfeld)..."）
- **内容不可访问**：需登录，本研究未取得推文内容。

---

## 信息缺口与下一步

**真正的长对话访谈缺口**：
1. 14 分钟的 CyberWire 集太短，难以提取即兴类比与立场变化
2. 22 分钟的 Crying Out Cloud 集是最有希望的"长对话"候选，但**未取得转录**
3. **未发现** Nir 出现在 Darknet Diaries / Risky Business / Security Now / Cyber Wire Daily（非 Research Saturday）等主流 infosec 播客——这本身就是信号：他偏好"研究带"访谈而非"故事带"访谈

**建议的后续手动补做**（如需深化"即兴思考"维度）：
1. 听完 Crying Out Cloud IngressNightmare 集（22:27），提取即兴比喻与 Q&A
2. 听完 fwd:cloudsec #10 Secret Agents（26:53）和 #12 EKS Playbook（24:49）末尾 Q&A
3. 听完 RSAC 2022 The Cloud Gray Zone（43:19）末尾 Q&A
4. 听完 Black Hat Call-to-Action（#4），找云厂商反驳与 Nir 澄清立场瞬间

**已确认的稳定结论**（不依赖听录音）：
- Nir 的公开交流主要走"会议演讲 + 短播客嘉宾"通道，不走"独立播客巡讲"通道
- 他的核心议程稳定：云漏洞需独立归档、责任在厂商、灰色地带需被识别
- 合作搭档随时间演变：早期 Sagi Tzadik / Shir Tamari → 2024-2025 Hillai Ben-Sasson
- 职业轨迹：Senior Security Researcher (2022) → Head of Vulnerability Research (2025)

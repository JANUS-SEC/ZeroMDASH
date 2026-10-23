# Hillai Ben-Sasson — 决策记录

> 调研对象：Hillai Ben-Sasson，Wiz Research 安全研究员。
> 方法：以 Wiz 博客作者页 + 各篇博客正文 + Hacker News algolia API 为一手来源；WebSearch
> 在本环境中返回大量幻觉与循环内容，**已弃用**，所有结论仅来自可抓取的一手 URL。
> 约定：每条标注来源 URL 与可信度（高=一手原文/官方页；中=一手但需推断；低=二手/单点；
> 未证实=无一手来源）。区分「有记录的决策」与「推断的动机」。

---

## 0. 数据来源与可信度总览

### 已核实的一手事实

| 维度 | 事实 | 来源 | 可信度 |
|---|---|---|---|
| 现职 | Wiz Research 安全研究员，常驻以色列 | https://www.wiz.io/blog/author/hillai-ben-sasson | 高 |
| 自述方向 | "research and exploitation of web applications, application security, and finding vulnerabilities in complex high-level systems" | 同上作者 bio | 高 |
| 行业认可 | "recognized on MSRC's Most Valuable Researchers leaderboard" | 同上作者 bio | 高 |
| 作品清单 | 作者页列出 4 项署名研究（见下表） | 同上 | 高 |

### 作者页署名作品（一手）

| 作品 | 发布日 | 合著者 | 角色 |
|---|---|---|---|
| BingBang（业务向） | 2023-03-29 | Raaz Herzberg, Shir Tamari | 合著（第三署名） |
| BingBang（技术向） | 2023-03-29 | 无（作者页未列） | 合著 |
| 38TB Microsoft AI 数据暴露 | 2023-09-18 | Ronny Greenberg | 合著 |
| SAPwned（SAP AI Core） | 2024-07-17 | 作者页未列合著者 | 独立/主笔 |
| IngressNightmare（CVE-2025-1974） | 2025-03-24 | Nir Ohfeld, Ronen Shustin, Sagi Tzadik, Andres Riancho | 合著 |

### 对任务线索的关键证伪（必须保留的矛盾）

任务前提中提到 NVIDIAScape / CodeBreach 为 Hillai 合著作品。**一手来源证伪此说法**：

- NVIDIAScape（2025-07-17）→ 合著者为 **Nir Ohfeld + Shir Tamari**，**Hillai 未署名**。
  来源：https://www.wiz.io/blog/author/nir-ohfeld （Nir 作者页，可信度高）
- CodeBreach（2026-01-15）→ 合著者为 **Nir Ohfeld + Yuval Avrahami**，**Hillai 未署名**。
  来源：同上
- Hillai 与 Nir Ohfeld **唯一**确认的合著作品是 IngressNightmare（2025-03-24）。
- 由此「2024 年中起 Hillai 成为 Nir 主合作者、取代 Shir Tamari」的叙事**不成立**：
  Shir Tamari 在 2025-07（NVIDIAScape）仍与 Nir 合著，时间晚于 Hillai 参与的
  IngressNightmare（2025-03）。Nir 与多名研究者长期并行合作（Shir、Ronen、Sagi、
  Hillai、Yuval、Andres 等），不存在「取代」关系。

### 未证实 / 无法核实的线索

| 线索 | 状态 | 原因 |
|---|---|---|
| Unit 8200 / 军方背景 | **未证实** | WebSearch 返回「Unit 8200」断言但无任何可追溯来源，疑为幻觉；Wiz 作者 bio 未提及军方。不采信、不断言。 |
| 加入 Wiz 前的具体雇主 | **未证实** | 无一手来源（LinkedIn 需登录，未抓取）。 |
| 「为什么选 Wiz」个人动机 | **未证实** | 未找到 Hillai 本人对此的公开陈述。 |
| KubeCon 2025 Mish-Mesh（service mesh）演讲 | **未证实** | sched.com 对自动化抓取返回 403；无法独立确认题目、讲者或会议场次。按任务线索保留，标注待核。 |
| Hillai 公开的漏洞披露伦理主张 | **未找到** | 他的博客仅含标准「responsible disclosure」措辞，未找到他本人阐述披露哲学的独立文章/演讲。 |

---

## 1. 决策事件：SAPwned 的披露节奏与 PoC 取舍（独立/主笔，2024）

### 背景
SAP AI Core 是 SAP 面向企业的 AI/ML 托管服务，构建在共享多租户 Kubernetes 之上。
Hillai 以独立/主笔身份研究其租户隔离边界。作者页未列合著者，是他在作者页上唯一
无合著者的作品，标志其从合著者向独立主笔的过渡。

### 决策（有记录）
披露时间线（一手博客正文）：
- 2024-01-25：Wiz 向 SAP 报告
- 2024-01-27：SAP 回复并分配 case number
- 2024-02-16：SAP 修复首个漏洞并轮换相关 secrets
- 2024-02-28：**Wiz 绕过补丁，发现 2 个新漏洞并再次报告**
- 2024-05-15：SAP 部署全部修复
- 2024-07-17：公开披露

总窗口约 6 个月，含一轮「补丁—绕过—再报告」循环。

PoC 取舍（有记录）：**未发布任何 exploit 代码**。博客以叙述形式描述技术步骤
（`runAsUser: 1337` 绕过 Istio、Loki `/config` 泄露 S3 凭证、未鉴权 Helm Tiller
部署恶意 chart 取得 cluster-admin），但不发布可复用的工具或 PoC。

取得的访问层级（有记录，博客自述）：在 SAP AI Core 的 K8s 集群上取得 **cluster-admin**，
读写 SAP 内部容器仓库与 Artifactory、明文获取客户云凭证（AWS/Azure/SAP HANA Cloud/
Docker Hub）、访问未鉴权 EFS 上的客户 AI 制品。

官方表态（博客原文）：「All vulnerabilities have been reported to SAP's security team
and fixed by SAP」「We thank them for their cooperation. No customer data was
compromised.」

来源：https://wiz.io/blog/sapwned-sap-ai-vulnerabilities-ai-security （可信度高）

### 逻辑（推断，标注为推断）
- 厂商是闭源商业客户（SAP），终端用户无法自助打补丁；发布可复用 exploit 会直接
  武装攻击者而无法被防御者对冲 → 选择叙述而非代码，符合「武装攻击者成本 >
  防御者收益」时的常见取舍。
- 含补丁绕过循环，说明 Wiz 主动验证修复彻底性，而非一次性披露——这是「深度披露」
  的体现，也拉长了窗口。
- 注意：此为基于行为模式的推断，**不是** Hillai 公开陈述的逻辑。

### 事后反思（有记录，但来自第三方批评，非 Hillai 本人）
Hacker News thread 40990768（一手，algolia API）出现两类批评：

1. **伦理/动机批评**（darefalcon, id 40999094）：
   > "Companies that penetrate networks uninvited looking for vulnerabilities to create
   > blog content should be prosecuted IMHO. This piece in particular sounds like a hit
   > piece thinly vailed as a vulnerability disclosure."
   > "'We thanked them for their co-operation'. Sounds kinda like extortion."

2. **检测失效批评**（dotty-, id 40991902）：
   > "I hope SAP does a hard retrospective on why Wiz's research was not disrupted
   > before they got full cluster admin."

   注意：dotty- 是在批评 SAP 的检测能力，**不是**批评 Wiz 越界；但它坐实了
   「Wiz 取得 full cluster admin」这一事实。

-thread 内对 darefalcon 的回应多为反驳（"way to shoot the messenger"、
"Are you serious?"），说明「extortion」是少数派意见，**非社区共识**，但作为
**有记录的批评**必须保留。

来源：https://hn.algolia.com/api/v1/items/40990768 （可信度高）

Hillai 本人**未**对上述批评作公开回应（未找到任何回应记录）。

### 言行一致性评估
- **自述方向 vs 行为**：作者 bio 自述「research and **exploitation** of ... complex
  high-level systems」——取得 cluster-admin 与此**一致**，没有言行不符。
- **披露伦理 vs 商业结构**：Wiz 是云安全厂商，研究博客同时是增长渠道（HN tiffanyh
  提到 Wiz 当时 $100M ARR、Google 收购进行中）。SAPwned 的深度访问（cluster admin +
  客户明文凭证）+ 商业受益，构成 darefalcon 所指「extortion」观感的结构性来源。
  这是 **Wiz 商业模式的结构性张力**，非 Hillai 独有；但 SAPwned 是其独立主笔作品，
  因此这条决策记录归属于他。
- **缺口**：未找到 Hillai 公开阐述个人披露伦理主张的任何文章/演讲，因此无法做
  「他主张 X、却做了非 X」的对照——只能做「他的行为是否与他所在机构的商业结构一致」
  的评估。结论：行为与机构一致，但机构本身存在被批评的结构性张力。

---

## 2. 决策事件：BingBang 的披露与现场演示取舍（合著，2023）

### 背景
Microsoft Bing 在 ChatGPT 热潮期间是高关注目标。BingBang 针对一个 Bing 管理门户
背后的 Azure Active Directory 多租户应用配置错误。

### 决策（有记录）
- 公开日：2023-03-29。
- 内部时间线：博客**未给出**发现/报告/修复的具体日期，仅称
  「All issues were responsibly disclosed to Microsoft upon discovery. Microsoft
  rapidly fixed its vulnerable applications and modified some AAD functionality to
  reduce customer exposure.」
- 现场演示取舍（有记录）：**未发布正式 PoC 代码**，但做了**真实在线演示**——
  修改 Bing 搜索结果（把 "best soundtracks" 的 Dune(2021) 换成 Hackers(1995) 并上线
  Bing.com）、在 Bing.com 注入无害 XSS 并验证执行、构造可窃取 Office 365 access
  token 的 XSS payload。所有操作限制在研究者自己的 Azure 账户内。
- 取得的访问层级：Bing.com 的 CMS，可改任意搜索结果、执行 XSS、窃取 O365 token
  （进而可读 Outlook 邮件/日历/Teams 消息/SharePoint/OneDrive）。
- 根因：AAD 多租户应用未校验用户原始租户；约 25% 扫描到的多租户应用有同类问题。

来源：https://wiz.io/blog/bingbang （可信度高）

### 逻辑（推断）
- 与 SAPwned 同属「闭源商业厂商」目标 → 不发布可复用 exploit，但用真实在线演示
  证明影响（而非纯理论）——这是 Wiz 研究的标志性「demo-or-it-didn't-happen」风格。
- 自限在研究者自己账户内，是显式的伦理边界声明。
- **推断**，非 Hillai 公开陈述。

### 言行一致性评估
- 与 SAPwned 取舍**一致**：厂商目标 → 叙述/演示，不发布工具。
- 自限账户范围的行为，与他自述「exploitation」方向一致，且显式约束了爆炸半径。
- 缺口同 SAPwned：未找到他对此取舍逻辑的公开阐述。

---

## 3. 决策事件：IngressNightmare 的披露与 PoC 取舍（合著，2025）

### 背景
Ingress NGINX Controller 是 Kubernetes 生态最广泛使用的 ingress 之一，其 admission
controller 在大量集群中公开暴露。

### 决策（有记录）
披露时间线（一手博客正文，与 CNCF/Kubernetes 安全团队协调）：

| 日期 | 事件 |
|---|---|
| 2024-12-31 | Wiz 报告 CVE-2025-1974 与 CVE-2025-24514 |
| 2025-01-02 | Wiz 报告 CVE-2025-1097 |
| 2025-01-03 | Kubernetes 确认 |
| 2025-01-09 | K8s 提出 CVE-2025-1097 修复 |
| 2025-01-10 | **Wiz 报告该修复的绕过** |
| 2025-01-12 | K8s 提出 CVE-2025-1974 修复 |
| 2025-01-16 | **Wiz 报告该修复的绕过** |
| 2025-01-20 | K8s 提出 CVE-2025-24513 修复 |
| 2025-01-21 | Wiz 报告 CVE-2025-24513 绕过 + 报告 CVE-2025-1098 |
| 2025-02-07 | K8s 发布注入类漏洞内部补丁 |
| 2025-02-20 | K8s 从 admission controller 移除 NGINX 配置校验，解决 CVE-2025-1974 |
| 2025-03-10 | K8s 发出 embargo 通知 |
| 2025-03-24 | 公开披露 |

窗口约 3 个月，含**多轮「补丁—绕过—再报告」**循环。

PoC 取舍（有记录）：**发布了完整工具链**——
- GitHub 仓库 `https://github.com/ofirc/ingress-nightmare`（Terraform 起的可复现脆弱集群）
- exploit demo
- Nuclei 检测模板（供防御者扫描暴露面）

影响：43% 云环境受影响、6500+ 集群（含财富 500）公开暴露 admission controller；
CVE-2025-1974 CVSS 9.8；可读全部 namespace 的全部 secrets，潜在完整集群接管。

合著者：Nir Ohfeld, Ronen Shustin, Sagi Tzadik, Hillai Ben-Sasson, Andres Riancho。
这是 Hillai 与 Nir **唯一**确认的合著作品。

来源：https://wiz.io/blog/ingress-nginx-kubernetes-vulnerabilities （可信度高）

### 逻辑（推断）
- 目标是**开源项目**（Kubernetes/CNCF），终端用户**必须自助打补丁**才能获保护 →
  发布检测工具（Nuclei 模板）让防御者能自查暴露面，是「武装防御者」的正向收益。
- 与 SAPwned/BingBang（闭源厂商，不发工具）形成**对照**——同一研究者/团队在不同
  目标类型上采取相反的 PoC 策略，且**逻辑自洽**：闭源厂商目标不发可复用 exploit，
  开源目标发检测+复现工具。
- **推断**，非 Hillai 公开陈述。但该对照跨多篇作品、行为高度一致，可信度中高。

### 言行一致性评估
- 与 SAPwned/BingBang 的差异**不是**不一致，而是按目标类型分层的、自洽的取舍。
- 多轮主动绕过补丁的行为，与 SAPwned 的绕过循环一致——显示他对「修复彻底性」的
  一贯要求，不满足首次修复。
- 缺口：仍未找到他本人对「为何对厂商不发 PoC、对 OSS 发 PoC」的公开阐述；目前只能
  从行为推断其取舍逻辑。

---

## 4. 决策事件：研究方向选择（AI 安全 / 云隔离 / service mesh）

### 有记录的事实
按作者页 + 各博客正文，Hillai 的实际作品分布：

- BingBang（2023-03）：AAD 多租户配置 → Bing.com 接管。**本质是云身份/多租户隔离**，
  非狭义 AI。
- 38TB Microsoft AI（2023-09）：Microsoft AI 研究者仓库的 SAS token 配置错误。**本质
  是云存储配置错误**，碰巧发生在 AI 仓库。
- SAPwned（2024-07）：SAP AI Core K8s 多租户隔离。**本质是 K8s 配置 + 租户隔离**，
  载体是 AI 服务。
- IngressNightmare（2025-03）：K8s ingress admission controller。**纯 Kubernetes 基础
  设施**，与 AI 无关。

### 推断的动机（标注为推断，非核实）
- 「聚焦 AI 安全」更像是**市场叙事层**的归类——他真正一以贯之的技术线索是
  **共享多租户云服务中、单点配置错误导致跨租户隔离崩溃**的攻击面。AI 只是这些
  服务的载体标签之一（SAP AI Core、Microsoft AI 仓库）。
- 这与 Wiz 整体研究 playbook 一致（ChaosDB、ExtraReplica、OMIGOD 等都是同一范式），
  Hillai 在其中执行该范式，未见其独立开辟新范式。
- 「为什么做 service mesh（Mish-Mesh）」：**未证实**。KubeCon 2025 Mish-Mesh 演讲
  未能独立核实（sched.com 403）。若该演讲属实，则与他 IngressNightmare 后的 K8s
  基础设施方向延续一致，但这是双重推断。

### 言行一致性评估
- 行为模式（多租户隔离攻击）与作者 bio 自述「complex high-level systems」**一致**。
- 但「AI 安全研究者」这一外部标签**部分名实不符**：他的 AI 标签作品其实是云隔离
  bug 的载体，技术内核不是模型/AI 本身的安全（未涉及模型对抗、prompt injection、
  训练数据投毒等狭义 AI 安全议题）。
- 这是叙事与实质的偏差，**不是**言行矛盾——他没有公开自称「AI 安全专家」，是
  外界归类。

---

## 5. 决策事件：与 Nir Ohfeld 的分工与合作定位

### 有记录的事实
- Hillai 与 Nir **唯一**确认合著作品：IngressNightmare（2025-03-24）。
- Nir 作者页（https://www.wiz.io/blog/author/nir-ohfeld ）显示 Nir 的作品谱系更广：
  - CVE 研究（ChaosDB、OMIGOD、ExtraReplica、IngressNightmare、NVIDIAScape、
    NVIDIA Triton、CodeBreach 等）
  - **大量社区/CTF 创作**（Big IAM Challenge、K8s LAN Party、EKS Cluster Games、
    Prompt Airlines CTF、zeroday.cloud、Cloud Hunting Games CTF）
  - 品牌/赛事类（ZeroDay.cloud 2025、AI Cyber Model Arena）
- Hillai 作者页**无**任何 CTF/赛事创作类作品；全是 CVE 研究 writeup。

### 推断的分工（标注为推断，样本量 n=1，低可信度）
- 推测 Nir 偏向**社区/品牌/赛事 + CVE 研究**双线，Hillai 偏向**深度 CVE 利用
  writeup** 单线。
- 但 IngressNightmare 是唯一共作样本，无法判断两人在该篇内的具体分工
  （谁做 exploit chain、谁做协调、谁做 writeup）。
- 任务线索「Hillai 取代 Shir 成为主合作者」**被一手来源证伪**（见 §0）：Shir 在
  NVIDIAScape（2025-07，晚于 IngressNightmare）仍与 Nir 合著；且 Hillai 与 Nir 仅
  一篇共作，谈不上「主合作者」。

### 言行一致性评估
- 无 Hillai 公开陈述的分工主张，无法做言行对照。
- 仅有的行为证据（作品类型分布）与「深度 CVE writeup 偏好」一致，但样本太小。

---

## 6. 决策事件：职业背景与加入 Wiz

### 状态：未证实
- **军方/Unit 8200 背景**：未证实。WebSearch 在本环境返回「Unit 8200」断言但无可
  追溯来源，疑幻觉；Wiz 作者 bio 未提及军方履历。**不采信、不断言**。
- 加入 Wiz 前的雇主：未证实。LinkedIn 需登录、未抓取；无其他一手来源。
- 「为什么选 Wiz」：未找到 Hillai 本人公开陈述。

### 可间接推断的背景（低可信度）
- 作者 bio 自述专长为「web applications / application security / complex
  high-level systems」，且获 MSRC Most Valuable Researchers 认可——这与 BingBang
  （2023，Microsoft 厂商披露）在时间上吻合，可推测他在 2022-2023 间已活跃于
  Microsoft 生态安全研究并获 MSRC 认可，但**这是从获奖事实反推**，非直接履历。
- 以色列常驻地 + Wiz 是以色列创立公司，可解释地理/网络上的入职路径，但同样属推断。

### 言行一致性评估
- 无可评估对象（背景未核实）。仅记录「未证实」以防幻觉写入。

---

## 7. 综合言行一致性评估

| 维度 | 自述/外部叙事 | 实际行为 | 一致性 |
|---|---|---|---|
| 研究方向 | bio: 「exploitation of complex high-level systems」 | 取得 cluster-admin、改写 Bing 结果、读全部 K8s secrets | **一致** |
| PoC 发布策略 | 无公开主张 | 厂商目标不发代码、OSS 目标发完整工具链 | **行为自洽，但无公开主张可对照** |
| 披露伦理 | 仅标准「responsible disclosure」措辞 | 含补丁绕过循环、自限账户范围、协调 embargo | **与标准措辞一致，无超出/低于** |
| AI 安全研究者（外部标签） | 未自称 | 作品内核是云多租户隔离，非狭义 AI 安全 | **叙事与实质有偏差，非言行矛盾** |
| 商业结构张力 | 无公开主张 | 深度访问 + 博客驱动 Wiz 商业增长 | **结构性张力，非个人言行不符** |

### 关键缺口（务必保留）
1. **未找到 Hillai 任何公开的披露伦理/方法论主张文章或演讲**。因此无法做
   「他主张 X 却做了非 X」的硬性言行对照——所有「言行一致性」评估都退化为
   「行为是否自洽 + 是否与所在机构一致」。
2. **SAPwned 的「extortion/hit piece」批评是少数派意见**（HN thread 内被反驳），
   非社区共识，但作为有记录的伦理质疑必须保留。
3. **Unit 8200 / 军方背景未证实**，不写入任何断言。
4. **NVIDIAScape / CodeBreach 的 Hillai 合著身份被一手来源证伪**——任务线索有误，
   已在 §0 纠正。
5. **「Hillai 取代 Shir 成 Nir 主合作者」被一手来源证伪**：Shir 在 2025-07 仍与
   Nir 合著 NVIDIAScape，且 Hillai 与 Nir 仅一篇共作。

---

## 8. 修正任务线索清单

| 任务线索 | 一手核实结果 | 处理 |
|---|---|---|
| SAPwned（2024-07，独立/主笔） | 作者页未列合著者，博客确认独立主笔 | **采信** |
| BingBang（2023-03，合著） | 合著者 Raaz Herzberg, Shir Tamari | **采信** |
| IngressNightmare（2025-03，合著） | 合著者含 Nir Ohfeld 等 | **采信** |
| NVIDIAScape（2025-07，合著） | 合著者 Nir + Shir，**Hillai 未署名** | **证伪，纠正** |
| CodeBreach（2026-01，合著） | 合著者 Nir + Yuval Avrahami，**Hillai 未署名** | **证伪，纠正** |
| KubeCon 2025 Mish-Mesh | sched.com 403，未核实 | **标注未证实** |
| 2024 中起成 Nir 主合作者、取代 Shir | Shir 2025-07 仍与 Nir 合著；Hillai-Nir 仅 1 篇共作 | **证伪，纠正** |
| SAPwned HN 有 extortion/hit piece 批评 | darefalcon 评论原文坐实 | **采信** |
| Unit 8200 背景 | 无一手来源 | **标注未证实** |

---

## 附：一手来源索引

- Hillai 作者页：https://www.wiz.io/blog/author/hillai-ben-sasson （高）
- Nir Ohfeld 作者页：https://www.wiz.io/blog/author/nir-ohfeld （高）
- SAPwned 博客：https://wiz.io/blog/sapwned-sap-ai-vulnerabilities-ai-security （高）
- BingBang 博客：https://wiz.io/blog/bingbang （高）
- IngressNightmare 博客：https://wiz.io/blog/ingress-nginx-kubernetes-vulnerabilities （高）
- HN thread 40990768（SAPwned 讨论）：https://hn.algolia.com/api/v1/items/40990768 （高）
- IngressNightmare PoC 仓库：https://github.com/ofirc/ingress-nightmare （高）

> 未列入索引的来源 = 未在本次调研中使用。WebSearch 工具因返回幻觉/循环内容
> 已整体弃用；本文件所有结论仅来自上述一手 URL 的直接抓取。

# Shir Tamari — 时间线

> 调研时点：2026-07-27。本文件用于支撑 shir-tamari-perspective skill 的"防过时"校准。
> 所有事实均标注来源 URL 与可信度（高 / 中 / 低 / 未核实）。推测与事实严格分离。

---

## 0. 角色与可信度边界（必读）

- **用户提供的角色头衔**：Wiz Research 的 Head of Research。
- **Wiz 官方研究团队页**（https://www.wiz.io/research）实际将她列为 **"Vulnerability Research"**（与 Nir Ohfeld / Ronen Shustin / Hillai Ben-Sasson / Sagi Tzadik / Yuval Avrahami 等同事并列的通用角色标签），并未将 "Head of Research" 头衔标注在她或任何人名下。
- **Wiz 官方领导层页**（https://www.wiz.io/about）也未将她列入公司领导层。
- "Head of Research" 一衔可能来自外部行业档案 / 会议演讲者简介 / 媒体报道，而非 Wiz 自家站点。
- 本次调研期间 WebSearch 工具持续故障（详见文末方法论），无法通过外部来源二次核实该头衔。
- **角色头衔可信度：中**（用户任务框架如此表述；Wiz 官方站点不支持；外部来源未独立核实）。

**加入 Wiz 的时间锚点**：她在 Wiz 博客上最早的可追溯署名文章是 **2021-02-02**。可推断她至迟于 2021 年 1-2 月已在 Wiz。此前履历（教育背景、上一份工作）未能从公开可信来源核实。

---

## 1. 完整时间线（按年份）

> 表格字段：年份 | 事件 | 来源 | 可信度。
> 「高」= 一手来源已核实（Wiz 博客官方署名页或 NVD CVE 记录）；「中」= 通过二手来源引述（如 Wiz 博客文中引述某会议）；「低 / 未核实」= 仅搜索片段或无法从一手来源确认。

### 2021 年（云隔离研究起点）

| 年份 | 事件 | 来源 | 可信度 |
|---|---|---|---|
| 2021-02-02 | 独立署名 "82% of companies unknowingly give 3rd parties access to all their cloud data" — **Wiz 博客可追溯最早署名文章**，证明至迟此时已加入 Wiz | https://www.wiz.com/blog/82-of-companies-unknowingly-give-3rd-parties-access-to-all-their-cloud-data | 高 |
| 2021-08-04 | 独立署名 "Black Hat 2021: DNS loophole makes nation-state level spying as easy as registering a domain"，预告与 Wiz CTO Ami Luttwak 联合演讲 Black Hat USA 2021 | https://www.wiz.com/blog/black-hat-2021-dns-loophole-makes-nation-state-level-spying-as-easy-as-registering-a-domain | 高（博客）/ 中（BH 议程本身 403 未核实） |
| 2021-08 | **Black Hat USA 2021 演讲**："A New Class of DNS Vulnerabilities Affecting Many DNS-as-Service Platforms"（与 Ami Luttwak 联合） | https://www.blackhat.com/us-21/briefings/schedule/#a-new-class-of-dns-vulnerabilities-affecting-many-dns-as-service-platforms-23563 | 中（议程页 403；仅在 Wiz 博客中引述） |
| 2021-11 | **Black Hat Europe 2021 演讲**："ChaosDB: How We Hacked Databases of Thousands of Azure Customers"（Wiz Research 团队；Shir 本人在台上的角色未单独确认） | https://www.blackhat.com/eu-21/briefings/schedule/#chaosdb-how-we-hacked-databases-of-thousands-of-azure-customers-25200 | 中（议程页 403；通过后续 ExtraReplica 博客文中 "we presented" 措辞引述） |
| 2021-11-12 | 与 Alon Schindel 联合署名 "Security industry call to action: we need a cloud vulnerability database" | https://www.wiz.com/blog/security-industry-call-to-action-we-need-a-cloud-vulnerability-database | 高 |
| 2021-12-21 | 独立署名 "NotLegit: Azure App Service vulnerability exposed hundreds of source code repositories" | https://www.wiz.com/blog/azure-app-service-source-code-leak | 高 |

### 2022 年（云数据库隔离研究高峰 + 首次云供应链）

| 年份 | 事件 | 来源 | 可信度 |
|---|---|---|---|
| 2022-04-29 | 与 Ronen Shustin / Sagi Tzadik / Nir Ohfeld 联合署名 "Wiz Research discovers 'ExtraReplica'—a cross-account database vulnerability in Azure PostgreSQL" | https://www.wiz.com/blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql | 高 |
| 2022-06-09 | 与 Nir Ohfeld 联合署名 "The cloud gray zone—secret agents installed by cloud service providers"，文中预告将在 RSA Conference 2022 演讲同一主题（"we will present at RSA Conference 2022"） | https://www.wiz.com/blog/the-cloud-gray-zone-secret-agents-installed-by-cloud-service-providers | 高（博客）/ 中（RSA 议程未独立核实，且 RSA US 2022 = 2022-02-07~10 早于 6-09 发文日期，可能指 RSA APJ 2022 或发文用语不严谨） |
| 2022 | **fwd:cloudsec 2022 演讲**（演讲题目与确切日期未检索到；fwdcloudsec.org 议程页 403） | https://fwdcloudsec.org/speakers/shir-tamari/ | 中（搜索片段证实她是 2022 年度演讲者；标题未独立核实） |
| 2022-08-11 | 与 Ronen Shustin / Nir Ohfeld / Sagi Tzadik 联合署名 "The cloud has an isolation problem: PostgreSQL vulnerabilities affect multiple cloud vendors"（将 ExtraReplica 类问题推广至多家云厂商） | https://www.wiz.com/blog/the-cloud-has-an-isolation-problem-postgresql-vulnerabilities | 高 |
| 2022-12-01 | 与 Ronen Shustin 联合署名 "Hell's Keychain: Supply-chain vulnerability in IBM Cloud Databases for PostgreSQL allows potential unauthorized database access" | https://www.wiz.com/blog/hells-keychain-supply-chain-attack-in-ibm-cloud-databases-for-postgresql | 高 |
| 2022-12-13 | 与 Alon Schindel 联合署名 "Secret-based cloud supply-chain attacks: Case study and lessons for security teams" | https://www.wiz.com/blog/secret-based-cloud-supply-chain-attacks-case-study-and-lessons-for-security-teams | 高 |

### 2023 年（转向云供应链 / 客户密钥 / OS 层）

| 年份 | 事件 | 来源 | 可信度 |
|---|---|---|---|
| 2023-03-29 | 与 Raaz Herzberg / Hillai Ben-Sasson 联合署名 "BingBang: How a simple developer mistake could have led to Bing.com takeover"（供应链：GitHub Actions 泄露 Azure AD client secret） | https://www.wiz.com/blog/bingbang | 高 |
| 2023-04-19 | 与 Ronen Shustin 联合署名 "#BrokenSesame: Accidental 'write' permissions to private registry allowed potential RCE to Alibaba Cloud Database Services" | https://www.wiz.com/blog/brokensesame-accidental-write-permissions-to-private-registry-allowed-potential-r | 高 |
| 2023-07-21 | **独立署名** "Compromised Microsoft Key: More Impactful Than We Thought"（Storm-0558 事件分析；少见地独立署名） | https://www.wiz.com/blog/storm-0558-compromised-microsoft-key-enables-authentication-of-countless-micr | 高 |
| 2023-07-27 | 与 Sagi Tzadik 联合署名 "GameOver(lay): Easy-to-exploit local privilege escalation vulnerabilities in Ubuntu Linux affect 40% of Ubuntu cloud workloads"（OverlayFs CVE；首次明显转向 OS 层） | https://www.wiz.com/blog/ubuntu-overlayfs-vulnerability | 高 |

### 2024 年（转向 AI 基础设施）

| 年份 | 事件 | 来源 | 可信度 |
|---|---|---|---|
| 2024-03-11 | 与 Nir Ohfeld 联合署名 "Announcing the K8s LAN Party Challenge"（KubeCon EMEA 2024 期间发布的 CTF 挑战；文中提到 KubeCon EMEA 2024 与会，但未明示她本人登台演讲） | https://www.wiz.com/blog/k8s-lan-party-challenge | 高（文章）/ 低（KubeCon 演讲身份未确认） |
| 2024-04-04 | 与 Sagi Tzadik 联合署名 "Wiz Research finds architecture risks that may compromise AI-as-a-Service providers... works with Hugging Face on mitigations" — **AI 基础设施研究起点** | https://www.wiz.com/blog/wiz-and-hugging-face-address-risks-to-ai-infrastructure | 高 |
| 2024-05-23 | 与 Sagi Tzadik 联合署名 "The risk in malicious AI models: Wiz Research discovers critical vulnerability in AI-as-a-Service provider, Replicate" | https://www.wiz.com/blog/wiz-research-discovers-critical-vulnerability-in-replicate | 高 |
| 2024-09-26 | 与 Ronen Shustin / Andres Riancho 联合署名 "Wiz Research Finds Critical NVIDIA AI Vulnerability Affecting Containers Using NVIDIA GPUs, Including Over 35% of Cloud Environments" — **首次披露 NVIDIA Container Toolkit 漏洞 CVE-2024-0132** | https://www.wiz.com/blog/wiz-research-critical-nvidia-ai-vulnerability | 高 + NVD 确认 CVE-2024-0132 |

### 2025 年（NVIDIA Container Toolkit ×2 + React Server Components RCE）

| 年份 | 事件 | 来源 | 可信度 |
|---|---|---|---|
| 2025-02-11 | 与 Ronen Shustin / Andres Riancho 联合署名 "How Wiz found a Critical NVIDIA AI vulnerability: Deep Dive into a container escape (CVE-2024-0132)"（2024-09 首次披露后的技术深度分析） | https://www.wiz.com/blog/nvidia-ai-vulnerability-deep-dive-cve-2024-0132 | 高 + NVD 确认 |
| 2025-07-17 | 与 Nir Ohfeld 联合署名 "NVIDIAScape - Critical NVIDIA AI Vulnerability: A Three-Line Container Escape in NVIDIA Container Toolkit (CVE-2025-23266)" | https://www.wiz.com/blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape | 高 + NVD 确认 CVE-2025-23266 |
| 2025-12-08 | 与 Gili Tikochinski / Hila Ramati / Benjamin Read 联合署名 "React2Shell: Technical Deep-Dive & In-the-Wild Exploitation of CVE-2025-55182"（React Server Components 预认证 RCE，转向主流 Web 框架供应链） | https://www.wiz.com/blog/nextjs-cve-2025-55182-react2shell-deep-dive | 高 + NVD 确认 CVE-2025-55182 |

### 2026 年（截至 2026-07-27）

| 年份 | 事件 | 来源 | 可信度 |
|---|---|---|---|
| 2026 上半年 | **信息不足** — 调研时点 Wiz 博客作者页最新一篇仍是 2025-12-08 React2Shell；2026 上半年 Shir Tamari 的新署名文章、新的会议演讲议程均未能从可信来源核实。RSA Conference 2026（预计 2026-05）、Black Hat USA 2026、DEF CON 34 议程未能成功检索或未公开。 | — | 未核实 |

---

## 2. 最近 12 个月动态（2025-07 → 2026-07）—— 防过时专项

> "最近 12 个月"严格对应 2025-07 至 2026-07。本次调研在此期间仅核实到 **2 篇 Wiz 博客署名文章**，无任何可核实的 2026 会议演讲或社交动态。

### 2025-07-17 — NVIDIAScape（CVE-2025-23266）

- **文章**：与 Nir Ohfeld 联合署名 "NVIDIAScape - Critical NVIDIA AI Vulnerability: A Three-Line Container Escape in NVIDIA Container Toolkit (CVE-2025-23266)"
- **Wiz 博客 URL**：https://www.wiz.com/blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape
- **NVD 核实描述**（2026-07-27 取得）："NVIDIA Container Toolkit for all platforms contains a vulnerability in some hooks used to initialize the container, where an attacker could execute arbitrary code with elevated permissions. A successful exploit of this vulnerability might lead to escalation of privileges, data tampering, information disclosure, and denial of service."
- **技术要点**：三行代码的容器逃逸，针对 NVIDIA Container Toolkit 的容器初始化 hooks；是 Shir Tamari 在 NVIDIA AI 漏洞研究系列的第二弹（继 CVE-2024-0132 之后）。
- **意义**：把 2024-09 起的 NVIDIA Container Toolkit 研究线延续到 2025 年中；与 Nir Ohfeld 的合作延续 ExtraReplica / Cloud gray zone / K8s LAN Party 的老班底。
- **可信度**：高（Wiz 官方博客 + NVD API）

> **重要澄清**：本次调研期间，WebSearch 工具曾返回关于 NVIDIAScape 的幻觉输出——捏造合著者 "Shir Bardugo"（小说家，与安全研究无关），并将漏洞错误描述为 "NVIDIA GPU 云平台 Kubernetes 跨租户访问"。该输出已废弃、不采信。Wiz 博客明确将 NVIDIAScape 定性为 NVIDIA Container Toolkit 的三行容器逃逸（CVE-2025-23266），与 Nir Ohfeld 合著；NVD 描述与 Wiz 博客一致。

### 2025-12-08 — React2Shell（CVE-2025-55182）

- **文章**：与 Gili Tikochinski / Hila Ramati / Benjamin Read 联合署名 "React2Shell: Technical Deep-Dive & In-the-Wide Exploitation of CVE-2025-55182"
- **Wiz 博客 URL**：https://www.wiz.com/blog/nextjs-cve-2025-55182-react2shell-deep-dive
- **NVD 核实描述**（2026-07-27 取得）："A pre-authentication remote code execution vulnerability exists in React Server Components versions 19.0.0, 19.1.0, 19.1.1, and 19.2.0 including the following packages: react-server-dom-parcel, react-server-dom-turbopack, and react-server-dom-webpack. The vulnerable code unsafely deserializes payloads from HTTP requests to Server Function endpoints."
- **技术要点**：预认证 RCE；针对 React Server Components（react-server-dom-parcel / -turbopack / -webpack 三个包）；不安全反序列化 HTTP 请求到 Server Function 端点。
- **意义**：Shir Tamari 研究轨迹从云 / AI 基础设施扩展到主流 Web 框架供应链；合著者阵容引入 Gili Tikochinski / Hila Ramati / Benjamin Read —— 新的合作面孔，可能反映 Wiz Research 团队的人员扩张或她的研究方向已扩展到前端/SSR 框架。
- **可信度**：高（Wiz 官方博客 + NVD API）

### 2025-08 ~ 2026-07 的会议与社交动态 — 全部未核实

| 项目 | 状态 | 障碍 |
|---|---|---|
| Black Hat USA 2025（2025-08，Las Vegas） | **未核实** | 议程页 https://www.blackhat.com/us-25/briefings/schedule/index.html 返回 HTTP 403 |
| DEF CON 33（2025-08） | **未核实** | 议程页未成功检索 |
| RSA Conference 2025（2025-05-05~08，San Francisco） | **未核实** | 议程页 HTTP 403 |
| RSA Conference 2026（预计 2026-05） | **未核实** | 议程未能检索；可能尚未公开或 403 |
| Black Hat USA 2026 / DEF CON 34 | **未核实** | 调研时点（2026-07-27）议程应未召开或未公开 |
| KubeCon EU 2026 / KubeCon NA 2026 | **未核实** | 议程页未能检索 |
| fwd:cloudsec 2025 / 2026 | **未核实** | fwdcloudsec.org 议程页 HTTP 403 |
| X / Twitter 账号与近期推文 | **未核实** | WebSearch 工具故障，无法 site:x.com 搜索 |
| LinkedIn 职业履历更新 | **未核实** | LinkedIn 需登录，未读取 |

### 最近 12 个月已核实事件汇总

| 日期 | 事件 | 来源 | 可信度 |
|---|---|---|---|
| 2025-07-17 | NVIDIAScape（CVE-2025-23266）— NVIDIA Container Toolkit 三行容器逃逸，与 Nir Ohfeld 合著 | https://www.wiz.com/blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape + NVD CVE-2025-23266 | 高 |
| 2025-12-08 | React2Shell（CVE-2025-55182）— React Server Components 预认证 RCE，与 Gili Tikochinski / Hila Ramati / Benjamin Read 合著 | https://www.wiz.com/blog/nextjs-cve-2025-55182-react2shell-deep-dive + NVD CVE-2025-55182 | 高 |
| 2026-01 ~ 2026-07 | 无新署名文章；2026 会议议程全部未核实 | — | 信息不足 |

> **结论**：最近 12 个月可核实的动态集中在 2025 下半年两篇重磅文章（NVIDIAScape 与 React2Shell）。2026 年的会议演讲、X 活动、新研究方向**均信息不足**——下次更新此 skill 时，应优先补查 2026 RSAC / Black Hat USA 2026 / DEF CON 34 议程，并尝试通过 LinkedIn 二次核实其角色头衔与团队扩张情况。

---

## 3. 研究轨迹（思想转折点）

按文章主题与时间梳理，Shir Tamari 的研究重心经历五次明显转向：

1. **2021 — 云隔离 / 第三方访问起点**：第三方云访问 (Feb)、DNS-as-Service (Aug)、NotLegit Azure App Service 源码泄漏 (Dec)。议题核心："云厂商在共享隔离边界上的实现缺陷"。
2. **2022 — 云数据库隔离高峰**：ExtraReplica (Azure PostgreSQL)、Cloud gray zone、PostgreSQL 跨厂商 (Aug)、Hell's Keychain (IBM Cloud)、Secret-based 云供应链 (Dec)。代表命题："The cloud has an isolation problem"——把单点漏洞上升为系统性论题。
3. **2023 — 转向云供应链 / 客户密钥 / OS 层**：BingBang（GitHub Actions 泄露 Azure AD client secret）、BrokenSesame（Alibaba Cloud DB）、Storm-0558 Microsoft key 分析（独立署名，少见）、GameOver Ubuntu OverlayFs。重心从"数据库隔离"转向"供应链凭据泄漏 + OS 提权"。
4. **2024 — 转向 AI 基础设施**：Hugging Face、Replicate、NVIDIA Container Toolkit 首次披露 (Sep)。这是她最具影响力的转向之一——把云隔离研究的方法论迁移到 AI-as-a-Service 共享 GPU 容器栈。
5. **2025 — AI 容器栈 ×2 + Web 框架供应链回归**：NVIDIA deep-dive (Feb)、NVIDIAScape (Jul)、React2Shell (Dec)。合著者阵容从 Nir/Ronen/Sagi 等老班底扩展到 Gili/Hila/Benjamin 等新名字——可能反映团队扩张或她研究方向扩展到前端/SSR 框架。

**贯穿主线**：共享云基础设施的隔离失效 + 供应链 RCE。从云数据库 (PostgreSQL) → AI 基础设施 (Hugging Face / Replicate / NVIDIA) → 主流 Web 框架供应链 (Next.js / React Server Components)。每一次转向都是把"共享信任边界 + 不安全反序列化 / 凭据传递"的方法论应用到新的高曝光技术栈。

---

## 4. 未核实 / 信息缺口（诚实披露）

| 项目 | 缺口说明 | 原因 |
|---|---|---|
| "Head of Research" 头衔 | Wiz 官方站点不支持此头衔；仅见于用户任务框架及外部来源 | WebSearch 工具故障，无法外部二次核实；Wiz /research 页将其列为 "Vulnerability Research" 通用标签 |
| 教育背景（大学、专业） | 未核实 | 无公开可信来源；LinkedIn 需登录 |
| 加入 Wiz 前履历 | 未核实 | 同上 |
| 加入 Wiz 的精确月份 | 至迟 2021-01/02（由 2021-02-02 首篇署名推断）；更早无法确认 | 缺乏更早的公开署名 |
| Black Hat USA 2025 是否登台 | 未核实 | 议程页 HTTP 403 |
| DEF CON 33 / DEF CON 30 是否登台 | 未核实 | 议程页返回 404 或 socket 错误 |
| RSA 2025 / 2026 演讲 | 未核实 | 议程页 HTTP 403 |
| fwd:cloudsec 2022 演讲标题 | 未核实 | fwdcloudsec.org 议程页 HTTP 403；仅通过搜索片段确认她是 2022 年度演讲者 |
| KubeCon EMEA 2024 是否登台 | 未核实 | 仅 Wiz 博客确认她与 K8s LAN Party CTF 挑战相关，但未明示她本人 KubeCon 演讲 |
| X / Twitter 账号与近期活动 | 未核实 | WebSearch 工具故障 |
| LinkedIn 职业履历 | 未核实 | 需登录 |
| 2026 上半年新文章 / 新会议 | 未核实 | Wiz 博客作者页最新一篇仍为 2025-12-08 React2Shell |

---

## 5. 数据源与方法

### 已采用的一手来源（可信）

1. **Wiz 博客作者页**（https://www.wiz.io/blog/author/shir-tamari）— 列出她全部 20 篇署名博文，含日期、标题、合著者、URL。本次调研唯一完整且权威的原始档案。
2. **NVD CVE API**（https://services.nvd.nist.gov/rest/json/cves/2.0）— 用于独立核实 CVE-2024-0132、CVE-2025-23266、CVE-2025-55182 的描述与受影响组件。三处 NVD 描述均与 Wiz 博客定性一致。
3. **fwd:cloudsec 搜索片段**（https://fwdcloudsec.org/speakers/shir-tamari/）— 确认她是 fwd:cloudsec 2022 演讲者；议程页本身 403 未取得。
4. **Wiz 博客文章中的会议自述**（Black Hat USA 2021 / Black Hat Europe 2021 / RSA Conference 2022 / KubeCon EMEA 2024）— 通过她本人或合著者在 Wiz 博客中对会议的自引确认存在演讲，但具体议程页未独立核实。

### 工具故障 / 失败记录（透明披露）

- **WebFetch ECONNREFUSED**：连续 3 次抓取 Wiz 博客单篇文章 URL（NVIDIAScape / React2Shell / NVIDIA deep-dive）均失败；推测为 Wiz 站点的反爬或速率限制。Wiz 博客作者页之所以能成功一次，可能是缓存命中。
- **WebFetch HTTP 403**：Black Hat 议程页（us-25 / eu-21 / us-21）、RSA Conference 议程页、fwd:cloudsec 议程页均返回 403。
- **WebFetch "No response from model"**：Wiz /research 团队页一次返回空响应；无法读取其团队名单的精确角色标签。
- **WebSearch 工具**：本次调研期间持续故障——返回捏造的 "I don't have access to a web search tool" 免责声明、捏造的合著者（如小说家 "Shir Bardugo"）、捏造的漏洞描述（把 NVIDIAScape 错误描述为 GPU 云平台 Kubernetes 跨租户）。所有 WebSearch 生成的细节已废弃，仅 Wiz 博客作者页 + NVD API 这两路一手来源被采信。
- **Bash 沙箱网络白名单**：仅允许 api.github.com / raw.githubusercontent.com / github.com / services.nvd.nist.gov 等少量 host；wiz.io / blackhat.com / rsaconference.com / fwdcloudsec.org / linkedin.com / x.com 均不在白名单，故 curl 无法替代 WebFetch。

### 黑名单遵守

未采用知乎、微信公众号、百度百科。WebSearch 返回的中文站点结果均未采信。

---

## 6. 关键链接索引

- Wiz 博客作者页（20 篇署名博文完整列表）：https://www.wiz.io/blog/author/shir-tamari
- Wiz 研究团队页：https://www.wiz.io/research
- Wiz 领导层页：https://www.wiz.io/about
- NVIDIAScape 文章：https://www.wiz.com/blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape
- React2Shell 文章：https://www.wiz.com/blog/nextjs-cve-2025-55182-react2shell-deep-dive
- NVIDIA deep-dive (CVE-2024-0132) 文章：https://www.wiz.com/blog/nvidia-ai-vulnerability-deep-dive-cve-2024-0132
- NVIDIA 首次披露文章：https://www.wiz.com/blog/wiz-research-critical-nvidia-ai-vulnerability
- fwd:cloudsec 演讲者页：https://fwdcloudsec.org/speakers/shir-tamari/
- NVD CVE-2024-0132 详情：https://nvd.nist.gov/vuln/detail/CVE-2024-0132
- NVD CVE-2025-23266 详情：https://nvd.nist.gov/vuln/detail/CVE-2025-23266
- NVD CVE-2025-55182 详情：https://nvd.nist.gov/vuln/detail/CVE-2025-55182

---

## 7. 下次更新此 skill 时的优先补查清单

1. **2026 RSAC 议程**（预计 2026-05 已召开）— 确认 Shir Tamari 是否登台；若登台，提取演讲题目与合著者。
2. **Black Hat USA 2026 / DEF CON 34 议程**（预计 2026-08）— 确认是否登台。
3. **Wiz 博客作者页**最新一篇 — 是否有 2026 年新署名文章。
4. **LinkedIn 职业履历** — 核实 "Head of Research" 头衔是否真实存在、加入 Wiz 的精确时间、教育背景、加入 Wiz 前履历。
5. **X / Twitter 账号** — 确认她是否在 X 活跃、近期研究方向与表态。
6. **fwd:cloudsec 2025 / 2026 是否登台** — 议程页目前 403。
7. **合著者阵容扩张**（Gili Tikochinski / Hila Ramati / Benjamin Read）— 是否反映 Wiz Research 团队扩张或她的研究方向扩展到前端/SSR 框架；这关系到 skill 中"思维框架"是否需要纳入新的研究语境。

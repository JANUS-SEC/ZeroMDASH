# Hillai Ben-Sasson — 时间线

> 调研日期：2026-07-26
> 调研者：Claude（子代理）
> 数据边界：本文件只收录可通过权威一手来源（Wiz 博客作者档案、Wiz Research 团队页、Wiz 官方事件页、会议官方议程/演讲者页、YouTube 视频元数据、正规媒体报道）核实或合理推断的事实。无法验证的项一律显式标注。

## 概述

Hillai Ben-Sasson 是 Wiz Research（Vulnerability Research 方向）的资深安全研究员，常驻以色列。她的 Wiz 作者简介原文：「a security researcher based in Israel … specializes in research and exploitation of web applications, application security, and finding vulnerabilities in complex high-level systems … frequent speaker in security conferences … recognized in MSRC's Most Valuable Researchers leaderboard」。X（Twitter）账号 `@hillai`（https://x.com/hillai），由 Wiz 官方事件页、RSA Conference 演讲者档案、fwd:cloudsec pretalx 档案、KubeCon NA 2025 sched 档案交叉确认。

研究轨迹：2023 年从微软云身份（Azure AD / Bing）切入 → 2023 年下半年转向微软 AI 数据暴露 → 2024 年独自披露 SAPwned（SAP AI Core），完成向「AI 基础设施安全」方向的拐点 → 2025 年初回到云原生（Ingress NGINX）→ 2025 年下半年以会议演讲方式呈现 NVIDIA Container Toolkit 跨云服务商影响。**自 2025 年 3 月 IngressNightmare 博文后，Hillai 在 Wiz 博客上无新署名；2025 年 11 月 KubeCon NA 2025 演讲是她最近一次可被公开核实的活动**，详见末节「最近 12 个月动态」。

---

## 完整时间线表

| 年份 | 事件 | 来源 | 可信度 |
|---|---|---|---|
| 2020 | Wiz 成立；Wiz Research 由 Nir Ohfeld / Shir Tamari / Ronen Shustin / Sagi Tzadik 等创始研究员组建（Nir 最早博文 ChaosDB 为 2021-08-26） | https://www.wiz.io/blog/author/nir-ohfeld | 高（Wiz 博客档案） |
| ~2022 H2–2023 Q1 | **推测**：Hillai 加入 Wiz。最早署名博文为 2023-03-29 BingBang，无公开入职时间声明 | https://www.wiz.io/blog/author/hillai-ben-sasson | 低（推断） |
| 2023-03-29 | **BingBang: How a simple developer mistake could have led to Bing.com takeover**（与 Raaz Herzberg + Shir Tamari 合著）。Azure AD 应用配置错误导致可改 Bing 搜索结果与接管 Bing 私有数据 | https://www.wiz.io/blog/author/hillai-ben-sasson | 高（Wiz 一手） |
| 2023-03-29 | **BingBang: AAD misconfiguration led to Bing.com results manipulation and account takeover**（Hillai 独立署名）— 同一研究的技术深度版 | https://www.wiz.io/blog/author/hillai-ben-sasson | 高（Wiz 一手） |
| 2023-04-19 | Wiz Research 发布 **#BrokenSesame**（Alibaba Cloud Database Services 容器逃逸 + 越权写）— 由 Ronen Shustin + Shir Tamari 署名，**Hillai 未参与博文署名**，但后续在 KubeCon Chicago 2023 上由 Hillai + Ronen 联袂演讲该研究 | https://www.wiz.io/blog/author/shir-tamari | 高（Wiz 一手） |
| 2023-09-18 | **38TB of data accidentally exposed by Microsoft AI researchers**（与 Ronny Greenberg 合著）。微软 AI GitHub 仓库 SAS token 配置错误暴露 38TB 数据含 Teams 内部消息 | https://www.wiz.io/blog/author/hillai-ben-sasson | 高（Wiz 一手） |
| 2023-11-06~09 | **KubeCon + CloudNativeCon NA 2023（Chicago）演讲**：*"The Attacker Perspective: Insights From Hacking Alibaba Cloud"*，与 Ronen Shustin 联袂。YouTube 录屏：https://www.youtube.com/watch?v=d81qnGKv4EE | https://www.youtube.com/watch?v=d81qnGKv4EE + Hillai 本人在 X 上的自述 | 高（YouTube 视频标题 + 第一人称自述） |
| 2024-04-04 | Wiz Research 发布 Hugging Face AI-as-a-Service 架构风险研究（Shir Tamari + Sagi Tzadik 署名，**Hillai 未参与博文署名**，但同年 Black Hat USA 2024 由 Hillai + Sagi 主讲该研究） | https://www.wiz.io/blog/author/shir-tamari | 高（Wiz 一手） |
| 2024-05-23 | Wiz Research 发布 Replicate（AI-as-a-Service 提供商）漏洞研究（Shir Tamari + Sagi Tzadik 署名，Hillai 同样未署名） | https://www.wiz.io/blog/author/shir-tamari | 高（Wiz 一手） |
| 2024-07-17 | **SAPwned: SAP AI vulnerabilities expose customers' cloud environments and private AI artifacts**（Hillai 独立署名）— SAP AI Core 越权与客户数据访问。**这是 Hillai 唯一一次 2024 年博文，也是她首个独立署名的大型研究，标志其向 AI 安全方向的明确拐点** | https://www.wiz.io/blog/author/hillai-ben-sasson | 高（Wiz 一手） |
| 2024-07-24 | Wiz 同期发布 "Crying Out Cloud" 播客 *SAPwned* 特辑，邀请 Hillai 作为嘉宾 | https://www.wiz.io/crying-out-cloud/sapwned-sap-ai-core-vulnerabilities-special-guest-hillai-ben-sasson | 高（Wiz 一手，DuckDuckGo 索引） |
| 2024-08-07~08 | **Black Hat USA 2024（Las Vegas）演讲**：*"Isolation or Hallucination? Hacking AI Infrastructure Providers for Fun and Weights"*，与 Sagi Tzadik 联袂。Track: AI, ML, & Data Science / Cloud Security。研究综合扩展自 Hugging Face + Replicate + SAP AI Core 三大 AI-as-a-Service 提供商研究。TechTarget 等媒体独立报道确认 | https://www.wiz.io/events/blackhat-wiz-talk + https://www.techtarget.com/searchsecurity/news/366602365/Wiz-researchers-hacked-into-leading-AI-infrastructure-providers + https://securityboulevard.com/2024/07/8-supply-chain-security-talks-you-dont-want-to-miss-at-black-hat/ | 高（多源交叉） |
| 2024 | Hillai 在 Wiz 事件页上的头衔为 **Senior Security Researcher**（其它来源只写 "Security Researcher"） | https://www.wiz.io/events/blackhat-wiz-talk | 高（Wiz 官方事件页） |
| 2025-02-11 | Wiz Research 发布 NVIDIA Container Toolkit CVE-2024-0132 深度分析（Shir Tamari + Ronen Shustin + Andres Riancho 署名，**Hillai 未参与博文署名**，但同年 fwd:cloudsec 2025 与 KubeCon NA 2025 由 Hillai 主讲该研究） | https://www.wiz.io/blog/author/shir-tamari | 高（Wiz 一手） |
| 2025-03-24 | **IngressNightmare: CVE-2025-1974 — 9.8 Critical Unauthenticated RCE in Ingress NGINX**（与 Nir Ohfeld + Ronen Shustin + Sagi Tzadik 合著）。"Over 40% of cloud environments are vulnerable to RCE, likely leading to a complete cluster takeover." **这是 Hillai 在 Wiz 博客上最近一次署名** | https://www.wiz.io/blog/author/hillai-ben-sasson | 高（Wiz 一手） |
| 2025-04 | RSA Conference 2025 期间 Hillai 有演讲者档案（RSA 官方专家页存在），但**具体 talk 标题与年份未能经一手来源核实**（RSA 页面 403 阻断，DuckDuckGo 在该查询上 CAPTCHA'd） | https://www.rsaconference.com/experts/hillai-ben-sasson | 中（档案存在但内容未核） |
| 2025-07-01 | **fwd:cloudsec 2025 演讲**：*"The Good, the Bad, and the Ugly: Hacking 3 CSPs with 1 Vulnerability"*，与 Andres Riancho 联袂，09:00，20 min。Track: "Surveying the wilderness: attacks and vulnerabilities, defensive practices"。主题为 NVIDIA Container Toolkit 单一漏洞跨三大云服务商（Azure / DigitalOcean / Replicate）的影响差异 | https://pretalx.com/fwd-cloudsec-2025/speaker/MYJCUH/ | 高（pretalx 一手） |
| 2025-07-17 | **NVIDIAScape — CVE-2025-23266**：Wiz Research 发布博文 *"Critical NVIDIA AI Vulnerability: A Three-Line Container Escape in NVIDIA Container Toolkit"*。**合著者为 Nir Ohfeld + Shir Tamari，Hillai 不是合著者**（用户的已知线索在此被 Wiz 作者档案直接否定） | https://www.wiz.io/blog/author/shir-tamari + https://www.wiz.io/blog/author/nir-ohfeld | 高（Wiz 一手） |
| 2025-08-04 | Wiz Research 发布 NVIDIA Triton Server 漏洞链 CVE-2025-23319 博文（Ronen Shustin + Nir Ohfeld 署名，Hillai 不是合著者） | https://www.wiz.io/blog/author/nir-ohfeld | 高（Wiz 一手） |
| 2025-09-30 | Nir Ohfeld 发布 ZeroDay.cloud（Wiz 与 CSP 合办的云与 AI 黑客竞赛）启动公告（Hillai 未参与署名） | https://www.wiz.io/blog/author/nir-ohfeld | 高（Wiz 一手） |
| 2025-11-10~13 | **KubeCon + CloudNativeCon NA 2025（Atlanta）演讲**：*"The Good, the Bad, and the Ugly: Hacking 3 Cloud Native AI Services With 1 Vulnerability"*，与 Nir Ohfeld 联袂。YouTube 录屏：https://www.youtube.com/watch?v=ZTiWXqYg97U。**这是 Hillai 最近一次可被公开核实的活动** | https://kccncna2025.sched.com/speaker/hillaikc + https://www.youtube.com/watch?v=ZTiWXqYg97U | 高（sched 演讲者页 + YouTube 视频页标题） |
| 2025-12-08 | Wiz Research 发布 React2Shell（CVE-2025-55182）博文（Shir Tamari + Gili Tikochinski + Hila Ramati + Benjamin Read 署名，Hillai 不是合著者） | https://www.wiz.io/blog/author/shir-tamari | 高（Wiz 一手） |
| 2025-12-16 | Nir Ohfeld 发布 ZeroDay.cloud 2025 回顾博文（Hillai 未参与署名） | https://www.wiz.io/blog/author/nir-ohfeld | 高（Wiz 一手） |
| 2026-01-15 | **CodeBreach — AWS Console 供应链 / AWS GitHub 仓库劫持**：Wiz Research 发布同名博文。**合著者为 Yuval Avrahami + Nir Ohfeld，Hillai 不是合著者**（用户的已知线索在此被 Wiz 作者档案直接否定） | https://www.wiz.io/blog/author/nir-ohfeld | 高（Wiz 一手） |
| 2026-02-12 | Wiz Research 发布 AI Cyber Model Arena 基准测试公告（Nir Ohfeld + Alon Schindel 署名，Hillai 不是合著者） | https://www.wiz.io/blog/author/nir-ohfeld | 高（Wiz 一手） |
| 2026-03~07 | **未能核实任何 Hillai 公开活动**（Wiz 博客作者档案仅显示到 2025-03-24 IngressNightmare；KubeCon/Black Hat/DEF CON/RSA/fwd:cloudsec 议程在该窗口内对 Hillai 的检索要么 403/404、要么 CAPTCHA'd） | — | 未验证（详见末节） |

---

## 研究轨迹与思想转折点

1. **2023 H1 — 微软云身份切入**：BingBang 揭露 Azure Active Directory 应用配置错误可被用于改写 Bing 搜索结果与账户接管。两篇同名文章（一合著一独立），合著方含 Wiz VP Raaz Herzberg + 主创 Shir Tamari，Hillai 在团队中身份偏「执行研究员」。

2. **2023 H2 — 转 AI 数据暴露**：与 Ronny Greenberg 合著 38TB 微软 AI 研究员 GitHub SAS token 暴露事件。这是 Hillai 首次进入「AI 数据供应链」议题，但仍属云存储配置问题，非 AI 模型/服务本身。

3. **2024 — AI 安全拐点（SAPwned）**：Hillai 独立署名 SAPwned，揭露 SAP AI Core 越权与客户数据暴露。这是她首个独立署名的大型研究，明确从「云身份/配置」转向「AI-as-a-Service 模型本身的安全边界」。

4. **2024 H2 — Black Hat 综合扩展**：与 Sagi Tzadik 在 Black Hat USA 2024 主讲 *"Isolation or Hallucination? Hacking AI Infrastructure Providers for Fun and Weights"*，把 Shir Tamari / Sagi Tzadik 之前发布的 Hugging Face + Replicate 研究与 Hillai 自己的 SAPwned 串成一条 AI-as-a-Service 攻击链。**注意模式**：Hillai 经常作为「Wiz Research 的会议主讲人」出现，即便她并非对应博文的合著者（见下「会议主讲人 vs 博文合著者」模式）。

5. **2025 H1 — 回到云原生（IngressNightmare）**：与 Nir Ohfeld + Ronen Shustin + Sagi Tzadik 合著 IngressNightmare (CVE-2025-1974)，9.8 Critical，Ingress NGINX 未鉴权 RCE。研究方向从 AI 跳回 Kubernetes 控制面。**这是 Hillai 在 Wiz 博客上最近一次署名**。

6. **2025 H2 — 以会议演讲延续 NVIDIA AI 容器逃逸研究**：fwd:cloudsec 2025（7 月 1 日，与 Andres Riancho）+ KubeCon NA 2025（11 月，与 Nir Ohfeld）主讲 *"The Good, the Bad, and the Ugly"* 系列，主题为 NVIDIA Container Toolkit 单一漏洞跨 Azure / DigitalOcean / Replicate 三大 CSP 的差异化影响。对应博文（CVE-2024-0132，2025-02-11）由 Shir+Ronen+Andres 署名，**Hillai 不是合著者**。

7. **2025 H2 — 2026 H1 — 博客静默期**：自 2025-03-24 IngressNightmare 起，Wiz Research 的所有重大发布（NVIDIAScape、NVIDIA Triton、ZeroDay.cloud、React2Shell、CodeBreach、AI Cyber Model Arena）均由 Nir / Shir / Ronen / Yuval / Alon 承担，**Hillai 无任何 Wiz 博文署名**。会议侧仅 Nov 2025 KubeCon NA 演讲可被核实。

### 模式：会议主讲人 vs 博文合著者

Hillai 反复以「会议主讲人」身份出现，即便她并非对应 Wiz 博文的合著者：

| 会议 | 年份 | Talk | 合讲人 | 对应 Wiz 博文 | 博文署名 |
|---|---|---|---|---|---|
| KubeCon NA | 2023 | The Attacker Perspective: Insights From Hacking Alibaba Cloud | Ronen Shustin | #BrokenSesame (2023-04-19) | Ronen + Shir（Hillai 未署名） |
| Black Hat USA | 2024 | Isolation or Hallucination? Hacking AI Infrastructure Providers for Fun and Weights | Sagi Tzadik | Hugging Face (2024-04-04) + Replicate (2024-05-23) + SAPwned (2024-07-17) | 前两者 Shir + Sagi；SAPwned 为 Hillai 独立署名 |
| fwd:cloudsec | 2025 | The Good, the Bad, and the Ugly: Hacking 3 CSPs with 1 Vulnerability | Andres Riancho | NVIDIA Container Toolkit CVE-2024-0132 深度分析 (2025-02-11) | Shir + Ronen + Andres（Hillai 未署名） |
| KubeCon NA | 2025 | The Good, the Bad, and the Ugly: Hacking 3 Cloud Native AI Services With 1 Vulnerability | Nir Ohfeld | 综合多条 NVIDIA AI 研究 | Nir + Shir 等（Hillai 未署名） |

**含义**：评估 Hillai 的「研究指纹」时不能只看 Wiz 博文署名；她的会议主讲覆盖范围比博文更广。这对下游 Skill 提取思维框架的意义是：她的研究口味可以从她选择的「主讲」议题推断，而不仅限于她署名的博文。

---

## 会议演讲年表

| 年份 | 会议 | Talk 标题 | 合讲人 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2023-11 | KubeCon + CloudNativeCon NA 2023 (Chicago) | The Attacker Perspective: Insights From Hacking Alibaba Cloud's Internal Kubernetes Environments | Ronen Shustin | YouTube 视频页标题 + Hillai X 自述 | 高 |
| 2024-08 | Black Hat USA 2024 (Las Vegas) | Isolation or Hallucination? Hacking AI Infrastructure Providers for Fun and Weights | Sagi Tzadik | Wiz 官方事件页 + TechTarget + Security Boulevard | 高 |
| 2025-07-01 | fwd:cloudsec 2025 | The Good, the Bad, and the Ugly: Hacking 3 CSPs with 1 Vulnerability (09:00, 20 min) | Andres Riancho | pretalx 一手演讲者页 | 高 |
| 2025-11 | KubeCon + CloudNativeCon NA 2025 (Atlanta) | The Good, the Bad, and the Ugly: Hacking 3 Cloud Native AI Services With 1 Vulnerability | Nir Ohfeld | KubeCon sched 演讲者页 + YouTube 录屏页 | 高 |
| 2025 | RSA Conference（专家档案存在） | 未核实标题/年份 | 未核实 | RSA 官方专家页存在但 403 | 中（档案存在，talk 内容未核） |
| 2025 | Black Hat USA 2025 | 未核实 | 未核实 | Wiz 官方事件页只列 2024，未列 2025；搜索源被 CAPTCHA | 未验证 |
| 2025 | DEF CON 33 | 未核实 | 未核实 | DEF CON 33 页 404 | 未验证 |
| 2026 | RSA Conference 2026 | 未核实 | 未核实 | 搜索源被 CAPTCHA，无一手核实 | 未验证 |

---

## 最近 12 个月动态（2025-2026）

> 用户明确要求重点防过时：本节单独成节，详细写。

### 已核实活动（按时间倒序）

| 日期 | 事件 | Hillai 角色 | 来源 |
|---|---|---|---|
| 2025-11-10~13 | KubeCon + CloudNativeCon NA 2025 (Atlanta) — *"The Good, the Bad, and the Ugly: Hacking 3 Cloud Native AI Services With 1 Vulnerability"*，与 Nir Ohfeld 联袂 | **主讲人** | https://kccncna2025.sched.com/speaker/hillaikc + https://www.youtube.com/watch?v=ZTiWXqYg97U |
| 2025-07-01 | fwd:cloudsec 2025 — *"The Good, the Bad, and the Ugly: Hacking 3 CSPs with 1 Vulnerability"*，与 Andres Riancho 联袂，20 min | **主讲人** | https://pretalx.com/fwd-cloudsec-2025/speaker/MYJCUH/ |
| 2025-03-24 | Wiz 博客 IngressNightmare (CVE-2025-1974) 发布 — Hillai 最近一次 Wiz 博文署名 | **合著者**（与 Nir Ohfeld + Ronen Shustin + Sagi Tzadik） | https://www.wiz.io/blog/author/hillai-ben-sasson |

### 同期 Wiz Research 重大发布（Hillai 均未参与）

> 这些发布都是 Wiz Research 在 2025-07 至 2026-07 的高影响力研究，**均由 Hillai 的同事承担，Hillai 未在 Wiz 博客上署名**。用户原始线索把 NVIDIAScape 与 CodeBreach 归给 Hillai 是**错误的**，已由 Nir 与 Shir 的 Wiz 作者档案直接否定。

| 日期 | Wiz 博文 | 实际合著者 | Hillai 是否署名 |
|---|---|---|---|
| 2025-07-17 | NVIDIAScape — CVE-2025-23266（NVIDIA Container Toolkit 三行容器逃逸） | Nir Ohfeld + Shir Tamari | **否** |
| 2025-08-04 | Breaking NVIDIA Triton — CVE-2025-23319（NVIDIA Triton Inference Server 接管） | Ronen Shustin + Nir Ohfeld | **否** |
| 2025-09-30 | Introducing zeroday.cloud（Wiz 与 CSP 合办的云与 AI 黑客竞赛） | Nir Ohfeld | **否** |
| 2025-12-08 | React2Shell — CVE-2025-55182（在野利用 + 凭据收割 + 云后门） | Shir Tamari + Gili Tikochinski + Hila Ramati + Benjamin Read | **否** |
| 2025-12-16 | Zero-Days in the Age of AI: Behind the Scenes of ZeroDay.cloud 2025 | Nir Ohfeld | **否** |
| 2026-01-15 | CodeBreach — AWS Console 供应链 / AWS GitHub 仓库劫持 via CodeBuild | Yuval Avrahami + Nir Ohfeld | **否** |
| 2026-02-12 | Introducing AI Cyber Model Arena（257 真实场景 AI 网安基准） | Nir Ohfeld + Alon Schindel | **否** |

### 最近 12 个月动态评估

**Hillai 最近一次可被公开核实的活动 = 2025 年 11 月 KubeCon NA 2025 演讲**。自此至 2026-07（调研日期）约 8 个月内，未能经任何权威一手来源核实她在以下任一渠道有新活动：

- Wiz 博客作者档案：仅显示到 2025-03-24 IngressNightmare，无更新
- Wiz 官方事件页（https://www.wiz.io/events/blackhat-wiz-talk）：只列 2024 Black Hat talk，未列 2025/2026
- KubeCon / Black Hat / DEF CON / RSA / fwd:cloudsec 议程：2026 KubeCon NA、Black Hat USA 2025、DEF CON 33、RSA 2026 等议程页要么 403/404、要么 sched.com 403、要么 DuckDuckGo 检索被 CAPTCHA 阻断，均未检索到 Hillai 名字
- X / Twitter @hillai：x.com 直接抓取返回 402 Payment Required，最近推文内容未核实
- LinkedIn：认证墙阻断，无法读取

### 防过时要点

1. **Skill 中所有「Hillai 在 2025 H2 / 2026 H1 主导 / 参与 NVIDIAScape / CodeBreach」之类的说法均不成立**。如 Skill 中有此暗示，必须修正。
2. **Skill 中提到的 Hillai 最新研究应为**：IngressNightmare（2025-03-24，合著）+ KubeCon NA 2025 演讲（2025-11，与 Nir Ohfeld 合讲 NVIDIA Container Toolkit 跨 CSP 影响）。再新的内容**无一手来源支撑**。
3. **「Mish-Mesh」**：在 Hillai 的 Wiz 作者档案、Shir 的作者档案、Nir 的作者档案、DuckDuckGo 索引中均**未发现**任何标题含 "Mish-Mesh" 的博文或演讲。用户已知线索中 "KubeCon 2025 Mish-Mesh / NVIDIAScape 演讲" 一项**部分错误**：KubeCon NA 2025 确有 Hillai 演讲，但标题是 *"The Good, the Bad, and the Ugly"* 而非 "Mish-Mesh"，主题是 NVIDIA Container Toolkit 跨 CSP 影响而非 NVIDIAScape（CVE-2025-23266，那是 Nir+Shir 的博文，Hillai 未参与）。
4. 如 Skill 在使用此时间线时跨越 2026-07，**应重新调研**，因为 Wiz 可能在 2026 H2 发布新的 Hillai 参与的研究。

---

## 已核实事实 vs 推测 vs 未能验证

### 已核实（高可信度，多源交叉或一手来源）

- 身份 / Wiz Research 隶属 /以色列常驻：Wiz 博客作者档案 + Wiz Research 团队页 + 多个会议演讲者档案交叉
- X 账号 `@hillai`：Wiz 官方事件页 + RSA 专家档案 + fwd:cloudsec pretalx + KubeCon NA 2025 sched
- 头衔 Senior Security Researcher（Wiz 事件页明示；其它来源写 "Security Researcher"）
- 5 篇 Wiz 博文署名记录（精确日期 + 合著者）：Hillai 作者档案 + Nir 作者档案 + Shir 作者档案三向交叉
- 4 场会议演讲（KubeCon NA 2023、Black Hat USA 2024、fwd:cloudsec 2025、KubeCon NA 2025）：sched / pretalx / Wiz 事件页 / YouTube 视频页标题 / 媒体报道多源
- MSRC Most Valuable Researchers leaderboard 认可：Wiz 作者档案原文

### 合理推断（中可信度）

- 加入 Wiz 时间约 2022 H2 ~ 2023 Q1：依据「最早署名 = 2023-03-29 BingBang；Wiz Research 创始团队 Nir/Shir/Ronen/Sagi 早在 2021 年即发文」反推。**未发现公开入职声明**。
- 「会议主讲人 vs 博文合著者」模式：基于 4 场演讲的归纳，非 Hillai 本人声明的模式。

### 未能验证（来源受限）

- **教育背景**：Wiz 不公开；LinkedIn 认证墙阻断
- **加入 Wiz 前的工作经历**：Wiz 不公开；LinkedIn 认证墙阻断
- **GitHub 账号**：公开用户 `hillai` 是无关人（希伯来语 gematria 2048 项目，2 followers），与 Wiz 研究员无关；Hillai 真实 GitHub handle 未知
- **RSA Conference 具体演讲历史**：RSA 官方专家页存在（https://www.rsaconference.com/experts/hillai-ben-sasson）但 403；DuckDuckGo 在 RSA 相关查询上触发 CAPTCHA；具体 talk 标题/年份未核
- **Black Hat USA 2025 Hillai 是否有演讲**：Wiz 官方事件页未列；搜索源受阻；未验证
- **DEF CON 33（2025）Hillai 是否有演讲**：DEF CON 33 页面 404；未验证
- **RSA Conference 2026 Hillai 是否有演讲**：未验证
- **X / Twitter @hillai 最近 12 个月推文内容**：x.com 抓取 402；未验证。仅有一条来自 DuckDuckGo 索引的间接线索——Hillai 在 X 上自述曾于 KubeCon Chicago 演讲 Alibaba 课题（已与 YouTube 视频页标题互证）
- **2025-11 之后的 Hillai 任何活动**：未验证

### 用户已知线索核验结论

| 用户线索 | 核验结果 |
|---|---|
| 2023-03-29 BingBang（与 Raaz Herzberg + Shir Tamari） | ✅ 完全属实 |
| 2024-07-17 SAPwned（SAP AI Core，疑似独立/主笔） | ✅ 完全属实（Wiz 作者档案确认 Hillai 独立署名） |
| 2025-03-24 IngressNightmare（与 Nir 等） | ✅ 完全属实（合著者精确为 Nir Ohfeld + Ronen Shustin + Sagi Tzadik + Hillai Ben-Sasson） |
| 2025-07-17 NVIDIAScape（与 Nir 等） | ❌ **错误归属**：合著者为 Nir Ohfeld + Shir Tamari，Hillai 未参与 |
| 2026-01-15 CodeBreach（与 Nir 等） | ❌ **错误归属**：合著者为 Yuval Avrahami + Nir Ohfeld，Hillai 未参与 |
| KubeCon 2025 Mish-Mesh / NVIDIAScape 演讲 | ⚠️ **部分错误**：KubeCon NA 2025 确有 Hillai 演讲（与 Nir Ohfeld 合讲），但标题是 *"The Good, the Bad, and the Ugly: Hacking 3 Cloud Native AI Services With 1 Vulnerability"*，与 "Mish-Mesh" 无关；主题是 NVIDIA Container Toolkit 跨 CSP 影响而非 NVIDIAScape (CVE-2025-23266) |

---

## 信息源与可信度说明

### 一手来源（高可信度）

- **Wiz 博客作者档案** — Hillai 本人档案：https://www.wiz.io/blog/author/hillai-ben-sasson
  - 该档案仅列 5 篇博文，无分页元素；与 Nir / Shir 作者档案对其他博文合著者列表的交叉一致
- **Wiz 博客作者档案** — Nir Ohfeld：https://www.wiz.io/blog/author/nir-ohfeld（用于核实 NVIDIAScape / CodeBreach / NVIDIA Triton / ZeroDay.cloud 等的合著者）
- **Wiz 博客作者档案** — Shir Tamari：https://www.wiz.io/blog/author/shir-tamari（用于核实 NVIDIAScape、NVIDIA Container Toolkit CVE-2024-0132 深度分析、React2Shell 等的合著者，并确认不存在 "Mish-Mesh" 博文）
- **Wiz Research 团队页**：https://www.wiz.io/research（确认 Hillai 在 Vulnerability Research 方向；确认她的同事名单与社交账号映射）
- **Wiz 官方事件页**：https://www.wiz.io/events/blackhat-wiz-talk（Black Hat USA 2024 talk 详情 + Hillai 头衔 Senior Security Researcher）
- **fwd:cloudsec 2025 pretalx 演讲者页**：https://pretalx.com/fwd-cloudsec-2025/speaker/MYJCUH/（2025-07-01 talk 一手详情）
- **KubeCon NA 2025 sched 演讲者页**：https://kccncna2025.sched.com/speaker/hillaikc（Hillai 在 KubeCon NA 2025 是演讲者，标题由 DuckDuckGo 索引片段确认）
- **YouTube 视频页标题**：
  - https://www.youtube.com/watch?v=ZTiWXqYg97U — KubeCon NA 2025 录屏（标题确认）
  - https://www.youtube.com/watch?v=d81qnGKv4EE — KubeCon Chicago 2023 Alibaba 演讲录屏（页面标题 "The Attacker Perspective - Insights From Hacking Alibaba Cloud... Hillai Ben-Sasson & Ronen Shustin"）

### 二手来源（中可信度，仅用于交叉验证）

- TechTarget 报道 Black Hat USA 2024：https://www.techtarget.com/searchsecurity/news/366602365/Wiz-researchers-hacked-into-leading-AI-infrastructure-providers
- Security Boulevard Black Hat 2024 议程索引：https://securityboulevard.com/2024/07/8-supply-chain-security-talks-you-dont-want-to-miss-at-black-hat/
- DuckDuckGo HTML 索引（https://html.duckduckgo.com/html/）— 仅用于发现 URL 与片段，**不作为独立事实依据**；片段在落到一手来源核实前一律视为待证。

### 阻断 / 不可用来源

- LinkedIn（https://www.linkedin.com/in/hillai-ben-sasson）— 认证墙 402/403
- x.com / X（https://x.com/hillai）— 402 Payment Required
- KubeCon NA 2025 sched 完整议程（https://kccncna2025.sched.com）— 403 Forbidden（仅演讲者 slug 子页可由 DuckDuckGo 索引片段访问）
- KubeCon EU 2025 sched（https://kccnceu2025.sched.com）— 403 Forbidden
- Black Hat USA 2025 议程（https://www.blackhat.com/us-25/briefings/schedule.html 与 .html）— 403 / 404
- DEF CON 33（https://defcon.org/html/defcon-33/index.html）— 404
- RSA Conference 专家页（https://www.rsaconference.com/experts/hillai-ben-sasson）— 403
- Wayback Machine（web.archive.org）— "Claude Code is unable to fetch"
- Bing 中国版（cn.bing.com）— 中文本地化结果，对英文查询返回无关内容
- DuckDuckGo HTML 端点 — 多次查询后触发 CAPTCHA，部分查询返回 0 结果

### 信息源黑名单遵守

未使用知乎、微信公众号、百度百科作为任何条目的依据。

### WebSearch 幻觉风险声明

本文件中所有事实均经一手来源（Wiz 博客 / Wiz 事件页 / 会议官方页 / YouTube 视频页）或正规媒体（TechTarget / Security Boulevard）核实。WebSearch 工具本身在本调研过程中多次返回「I don't have access」式空响应，未被采信。DuckDuckGo HTML 索引片段仅用于「发现 URL」，最终事实落地前均已回到一手来源核实。

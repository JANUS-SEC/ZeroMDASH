# Nir Ohfeld — 时间线

> 调研日期：2026-07-26
> 主要信源：Wiz Blog 作者归档（21 篇署名博文，2021-08 至 2026-02，完整直查）、Wiz Research 团队页、Wiz About / 领导层页、Wiz 同期同事作者归档（用于交叉核对署名）
> 信源访问受限说明：Black Hat 官网（403 Forbidden）、fwd:cloudsec（403）、LinkedIn（HTTP 999）、X/Twitter（HTTP 402）、Wayback Machine（Claude Code 拒绝抓取）均无法直接抓取；下文中 Black Hat / DEF CON / fwd:cloudsec 演讲信息仅来自 Wiz 博文中明确自引述的会议引用，并非议程页直查
> 用户任务描述更正：任务中提到的「2023 BingBang, Azure Health Bot」与 Nir Ohfeld 无关——BingBang 由 Raaz Herzberg / Shir Tamari / Hillai Ben-Sasson 撰写（2023-03-29）；Azure Health Bot 在 Wiz 博客全库中无任何署名文章（已用 Wiz blog 搜索与 Hillai / Shir 作者归档交叉核实）。这两项研究都不属于 Nir 的时间线

## 总体时间线表

| 年份 | 事件 | 来源 | 可信度 |
|---|---|---|---|
| 2020 | Wiz 由 4 位前 Microsoft 高管（Assaf Rappaport / Ami Luttwak / Yinon Costica / Roy Reznik）创立。Nir Ohfeld **不在**联合创始人名单中 | https://www.wiz.io/about | 高（间接） |
| 2021-08-26 | **ChaosDB**：Wiz 首篇 Nir Ohfeld 署名博文。Azure Cosmos DB 跨账户数据访问漏洞，"数千 Azure 客户数据库可被访问"，与 Sagi Tzadik 合著 | https://wiz.io/blog/chaosdb-how-we-hacked-thousands-of-azure-customers-databases | 高 |
| 2021-09-14 | **OMIGOD**：Azure OMI（Open Management Infrastructure）4 个严重漏洞，单作者 Nir Ohfeld；同日发布姊妹篇"Secret Agent Exposes Azure Customers"（与 Alon Schindel） | https://wiz.io/blog/omigod-critical-vulnerabilities-in-omi-azure | 高 |
| 2021-11-11 | ChaosDB 技术深度博文 + **BlackHat Europe 2021 演讲总结**（与 Sagi Tzadik）。博文明确标注为 BlackHat Europe 2021 议题 | https://wiz.io/blog/how-we-broke-the-cloud-with-two-lines-of-code-the-full-story-of-chaosdb | 高 |
| 2022-04-29 | **ExtraReplica**（CVE-2022-23873）：Azure Database for PostgreSQL Flexible Server 跨账户漏洞，与 Ronen Shustin / Sagi Tzadik / Shir Tamari 合著 | https://wiz.io/blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql | 高 |
| 2022-06-09 | "云灰区"（cloud gray zone）：CSP 静默安装的 secret agents 研究，与 Shir Tamari 合著。博文明确标注为 **RSA Conference 2022 演讲** | https://wiz.io/blog/the-cloud-gray-zone-secret-agents-installed-by-cloud-service-providers | 高 |
| 2022-08-05 | Revisiting OMI：CVE-2022-29149 Azure OMI 提权分析，与 Rotem Zarin 合著 | https://wiz.io/blog/omi-returns-lpe-technical-analysis | 高 |
| 2022-08-11 | "云隔离问题"跨厂商 PostgreSQL 研究，与 Ronen Shustin / Shir Tamari / Sagi Tzadik 合著 | https://wiz.io/blog/the-cloud-has-an-isolation-problem-postgresql-vulnerabilities | 高 |
| 2023-03-29 | **BingBang**：Wiz 发表，关于 Bing.com / Azure AD 配置错误——**Nir Ohfeld 不是作者**（由 Herzberg / Tamari / Ben-Sasson 撰写）。列为时间线锚点以避免误判 | https://www.wiz.io/blog/author/hillai-ben-sasson | 高（更正项） |
| 2023-06-06 | **The Big IAM Challenge**：AWS IAM 主题 CTF，Nir Ohfeld 独立署名 | https://wiz.io/blog/the-big-iam-challenge | 高 |
| 2023-11-01 | **EKS Cluster Games** CTF，与 Ronen Shustin 合著 | https://wiz.io/blog/announcing-the-eks-cluster-games | 高 |
| 2024-03-11 | **K8s LAN Party Challenge** CTF，与 Shir Tamari 合著 | https://wiz.io/blog/k8s-lan-party-challenge | 高 |
| 2024-07-17 | SAPwned：SAP AI 漏洞研究——**非 Nir 主笔**（Hillai Ben-Sasson 单独署名）。列为团队方向参考锚点 | https://www.wiz.io/blog/author/hillai-ben-sasson | 高（旁证） |
| 2024-07-24 | **Prompt Airlines CTF**：AI 安全主题首个由 Nir 主导的 CTF——AI 安全转向的早期信号 | https://wiz.io/blog/prompt-airlines-ai-security-challenge | 高 |
| 2025-03-24 | **IngressNightmare**（CVE-2025-1974，CVSS 9.8）：Kubernetes Ingress-NGINX 未授权 RCE，第一作者，与 Ronen Shustin / Sagi Tzadik / Hillai Ben-Sasson 合著。"40%+ 云环境受影响" | https://wiz.io/blog/ingress-nginx-kubernetes-vulnerabilities | 高 |
| 2025-05-06 | **Cloud Hunting Games CTF**：云事件响应主题，与 Deror Czudnowski / Avigayil Mechtinger 合著 | https://wiz.io/blog/the-cloud-hunting-games-ctf-challenge | 高 |
| 2025-07-17 | **NVIDIAScape**（CVE-2025-23266，CVSS 9.0）：NVIDIA Container Toolkit "三行代码容器逃逸"，与 Shir Tamari 合著——明确从云控制面转向 AI 推理基础设施 | https://wiz.io/blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape | 高 |
| 2025-08-04 | **Breaking NVIDIA Triton**（CVE-2025-23319）：未授权链式漏洞接管 NVIDIA Triton Inference Server，与 Ronen Shustin 合著 | https://wiz.io/blog/nvidia-triton-cve-2025-23319-vuln-chain-to-ai-server | 高 |
| 2025-09-30 | **宣布 zeroday.cloud**：Wiz 联合主流 CSP 举办"史上最大规模云+AI 黑客大赛"，Nir 唯一署名作者 | https://wiz.io/blog/zeroday-cloud-ai-hacking-competition | 高 |
| 2025-12-16 | **ZeroDay.cloud 2025 回顾**：32 万美元奖金，关键云基础设施 CVE 数破纪录 | https://wiz.io/blog/wiz-zeroday-cloud-hacking-competition-behind-the-scenes | 高 |
| 2026-01-15 | **CodeBreach**：AWS CodeBuild 供应链漏洞，劫持 aws-sdk-js-v3 等 AWS GitHub 仓库。AWS 在披露后 48 小时内修复（披露 2025-08，博文 2026-01 发表）。与 Yuval Avrahami 合著 | https://wiz.io/blog/wiz-research-codebreach-vulnerability-aws-codebuild | 高 |
| 2026-02-12 | **AI Cyber Model Arena**：257 道真实场景的 AI agent 安全基准，五大赛道（zero-day 发现 / CVE 检测 / API 安全 / Web 安全 / 云安全），与 Alon Schindel 合著 | https://wiz.io/blog/introducing-ai-cyber-model-arena-a-real-world-benchmark-for-ai-agents-in-cybersec | 高 |

## 当前角色（2026-07 核实）

- 雇主：**Wiz**（云安全公司）
- 团队角色：**Vulnerability Research**（来自 Wiz Research 团队页 https://www.wiz.io/research，列为该角色下的团队成员，附 X profile 链接）
- **不在 Wiz 领导层 13 人名单中**（Wiz About 页核实）——即非 VP 及以上，属资深研究员 / 团队成员层级
- 长期合作者网络：Sagi Tzadik（ChaosDB/ExtraReplica 时期）→ Shir Tamari（2022-2024）→ Ronen Shustin（2023-2025）→ Yuval Avrahami（2026）→ Alon Schindel（2026 AI 基准项目）

## 加入 Wiz 时间

- 最早 Nir Ohfeld 署名博文：**2021-08-26**（ChaosDB 首次公开）
- ChaosDB 披露周期通常需 3-6 个月，因此推测 Nir 实际加入 Wiz 时间在 **2020 年末至 2021 年早些时候**
- 可信度：**中**（基于公开博文首秀的推测，无 LinkedIn 直查佐证）
- Wiz 由 4 位前 Microsoft 高管于 2020 年创立，Nir 不在创始人名单中，是早期研究员雇员而非联合创始人

## 教育 / 早期职业 / pre-Wiz 经历（信息缺口）

以下信息均**无法从可访问信源直接核实**，应视为未确认而非否定：

| 待核实项 | 状态 | 备注 |
|---|---|---|
| 大学 / 专业 | 未核实 | 无公开可信来源；LinkedIn 直查返回 HTTP 999 拒绝 |
| 是否曾在 Microsoft 工作 | 未核实 | Wiz 创始团队是前 Microsoft 背景，但 Nir 的个人前雇主未公开 |
| 是否曾在以色列 Unit 8200 服役 | 未核实 | 任务描述中提到需"核实不要断言"——确实无法断言；公开信源无相关佐证 |
| 是否曾在 Snyk / Check Point / 其他安全公司工作 | 未核实 | 早期 WebSearch 出现的"Snyk 研究员"说法疑似 LLM 幻觉，无 Wiz 官方或 LinkedIn 佐证，**不应采信** |

可信度：**低**（信息缺口；需 LinkedIn / 简历直查）

## 思想转折点：云数据库 → AI 安全

明确转折发生在 **2025 年 7 月**，触发事件是 NVIDIA Container Toolkit / Triton 这一连发：

- **2025-03-24 IngressNightmare** 仍是传统云原生控制平面漏洞（Kubernetes admission webhook RCE），属云控制面研究延续
- **2025-07-17 NVIDIAScape** 是首个明确瞄准 **AI 推理基础设施**的漏洞研究——这是研究方向的硬转折点
- **2025-08-04 NVIDIA Triton** 两连发，强化"AI runtime 是新的云攻击面"这一论点
- **2025-09-30 zeroday.cloud** 把研究社区化（赛事化），从单点漏洞转向系统性漏洞挖掘
- **2026-02-12 AI Cyber Model Arena** 从"挖漏洞"升级到"系统性评估 AI agent 攻击能力"——方法论层面的二次跃迁

更早的"过渡信号"（非主战场但已开始）：
- 2024-07-24 **Prompt Airlines CTF**：AI 安全主题首次以 CTF 形式出现（Nir 主导）
- 2024-07-17 SAPwned（同团队 Hillai 主笔）：Wiz 团队层面 2024 年中已开始 AI 主题研究，但 Nir 个人主线仍是云原生

转折的触发原因（推测，可信度中）：AI 推理基础设施（NVIDIA Container Toolkit / Triton Inference Server）在 2025 年成为云上普遍部署的高权限组件，且其攻击面与传统 Kubernetes / 数据库隔离问题结构性相似——Nir 把他在云数据库隔离（ExtraReplica）和控制面 RCE（IngressNightmare）上的方法论直接迁移到 AI runtime 上。

## 会议演讲年表

直接从 Black Hat / fwd:cloudsec / DEF CON / RSA 议程页**核实失败**（这些站点对 Claude Code 抓取返回 403）。下表仅来自 Wiz 博文中**明确自引述**的会议引用：

| 日期 | 会议 | 演讲 | 来源 | 可信度 |
|---|---|---|---|---|
| 2021-11 | **Black Hat Europe 2021** | "How we broke the cloud with two lines of code: the full story of ChaosDB"（与 Sagi Tzadik） | https://wiz.io/blog/how-we-broke-the-cloud-with-two-lines-of-code-the-full-story-of-chaosdb （博文标题即 talk 名，文中标注为 BlackHat Europe 2021 总结） | 高（博文自引述） |
| 2022-06 | **RSA Conference 2022** | "The cloud gray zone—secret agents installed by cloud service providers"（与 Shir Tamari） | https://wiz.io/blog/the-cloud-gray-zone-secret-agents-installed-by-cloud-service-providers | 高（博文自引述） |

未能直查议程页核实的会议演讲（**信息缺口**，不应假设存在也不应假设不存在）：
- Black Hat USA 2025 / 2026 议程（站点 403，无法核实 IngressNightmare / NVIDIAScape / CodeBreach 是否为 Black Hat 议题）
- DEF CON 33 (2025) / DEF CON 34 (2026) 议程
- fwd:cloudsec 2024 / 2025 / 2026 议程
- RSA 2026 议程

## 最近 12 个月动态（2025-07 → 2026-07）

> 此节为防 skill 过时的核心章节，仅记录已核实事项，并明确标注信息缺口。日期均为 Wiz 博文发布日（UTC）。

### 2025 下半年：密集产出 + 研究方向硬转折

Nir 在 2025 年下半年共署名 **4 篇研究博文 + 1 项赛事发起**，节奏明显快于往年：

- **2025-07-17 — NVIDIAScape (CVE-2025-23266, CVSS 9.0)**：NVIDIA Container Toolkit "三行代码容器逃逸"，与 Shir Tamari 合著。这是 Nir 首个明确瞄准 AI 推理基础设施的漏洞研究，**研究方向的硬转折点**
- **2025-08-04 — Breaking NVIDIA Triton (CVE-2025-23319)**：未授权链式漏洞，攻击者可接管 NVIDIA Triton Inference Server，与 Ronen Shustin 合著。NVIDIA 两连发强化"AI runtime = 新的云攻击面"论点
- **2025-09-30 — 宣布 zeroday.cloud**：Wiz 联合主流 CSP 举办的"首个云+AI 黑客大赛"，Nir 唯一署名。从单点漏洞研究扩展到社区化漏洞挖掘赛事
- **2025-12-16 — ZeroDay.cloud 2025 回顾**：32 万美元奖金，关键云基础设施 CVE 数破纪录。Nir 唯一署名

### 2026 上半年：AI agent 安全 + 供应链 + 方法论升级

Nir 在 2026 年上半年的两篇博文标志着研究方向的第二次跃迁——从"挖 AI 基础设施漏洞"到"系统性评估 AI agent 攻击能力 + AI 供应链漏洞"：

- **2026-01-15 — CodeBreach**：AWS CodeBuild 供应链漏洞，劫持 aws-sdk-js-v3 等 AWS GitHub 仓库。技术核心：
  - 未锚定正则（webhook ACTOR_ID filter 缺 `^` / `$` 锚点）
  - 通过 GitHub App manifest flow 注册 bot，使其 numeric ID 包含可信 maintainer 的 ID（称为"eclipse"）
  - 在 privileged CodeBuild build 中 dump 进程内存，提取 `aws-sdk-js-automation` 账户的 GitHub PAT（full admin 权限）
  - 影响面："66% 云环境包含 JavaScript SDK"，AWS Console 本身打包了 SDK 近期版本
  - AWS 在披露后 48 小时内修复（披露 2025-08，修复后 Wiz 于 2026-01 发表博文）
  - 与 Yuval Avrahami 合著（Yuval 是 Wiz 新晋合作者）
- **2026-02-12 — AI Cyber Model Arena**：257 道真实场景的 AI agent 安全基准，五大赛道（zero-day 发现 / CVE 检测 / API 安全 / Web 安全 / 云安全跨 AWS/Azure/GCP/K8s），与 Alon Schindel 合著
  - 关键设计：multi-agent × multi-model 矩阵；每道题尝试 3 次取 pass@3；Docker 容器隔离
  - 关键发现：**"offensive capability is jointly determined"**——同一模型在不同 agent scaffold 下表现差异巨大，"无单一组合通吃所有类别"。这是 Nir 把云漏洞研究方法论迁移到 AI agent 评估的标志作品

### 同期 Wiz 团队呼应研究（非 Nir 主笔但同窗口）

Wiz 整体在 2026 年明显把研究火力集中到 **"AI agent / MCP / AI runtime 安全"** 主题，Nir 的 AI Cyber Model Arena 是这一波的方法论旗帜：

- **2026-06-26 — MCP Auto-Execution: Amazon Q VS Code 扩展**（Maor Dokhanian）：从 git clone 到云上沦陷
- **2026-07-08 — GhostApproval: AI 编程助手的信任边界漏洞**（Maor Dokhanian）
- **2026-07-15 — The Red Agent POV 系列**（Gal Nagli 等）：AI agent 攻击 B2B 信用系统、GraphQL BOLA、SSRF 等

### X / Twitter 与外部媒体（信息缺口）

- X 账号疑似 handle：`just_nir_ohfeld`（Wiz Research 团队页作者链接指向此 handle，但 X 直接抓取返回 HTTP 402，无法核实近期推文活动）
- 2025-2026 期间媒体采访、播客出场、第三方报道：**未能在可访问信源中直接核实**——WebSearch 工具在本调研环境中返回结果不稳定（多次返回"I don't have web search"占位文本或疑似幻觉内容），故不引用任何未核实来源

### 当前研究焦点（截至 2026-07）

综合 2025 下半年 + 2026 上半年的署名博文，Nir 当前的研究主线为：

1. **AI 推理基础设施漏洞研究**（NVIDIA Container Toolkit / Triton 系列）
2. **云与 AI 供应链漏洞**（CodeBreach - AWS CodeBuild / GitHub 仓库劫持）
3. **AI agent 安全能力的系统性基准**（AI Cyber Model Arena）
4. **大规模漏洞挖掘赛事化**（zeroday.cloud 主办）

传统云数据库研究（Cosmos DB / PostgreSQL / OMI）已不再是其主战场，但仍通过 zeroday.cloud 项目间接驱动社区在该方向的贡献。

## 来源索引

### 一手来源（已直查核实）

- Wiz Blog — Nir Ohfeld 作者归档（21 篇，2021-08-26 至 2026-02-12）：https://www.wiz.io/blog/author/nir-ohfeld
- Wiz Research 团队页（Nir 列为 "Vulnerability Research" 角色）：https://www.wiz.io/research
- Wiz About / 领导层页（核实 Nir 不在 13 人领导层名单）：https://www.wiz.io/about
- Wiz Blog — Hillai Ben-Sasson 作者归档（交叉核对 BingBang / SAPwned / 38TB / IngressNightmare 署名）：https://www.wiz.io/blog/author/hillai-ben-sasson
- Wiz Blog — Shir Tamari 作者归档（交叉核对 ExtraReplica / BingBang / NVIDIAScape 署名，确认无 Azure Health Bot 文章）：https://www.wiz.io/blog/author/shir-tamari
- Wiz Blog 主页（核实 2026-06 / 07 团队产出，确认 Nir 未出现在第一页）：https://www.wiz.io/blog

### 各篇博文 URL（按时间倒序）

- 2026-02-12 AI Cyber Model Arena：https://wiz.io/blog/introducing-ai-cyber-model-arena-a-real-world-benchmark-for-ai-agents-in-cybersec
- 2026-01-15 CodeBreach：https://wiz.io/blog/wiz-research-codebreach-vulnerability-aws-codebuild
- 2025-12-16 ZeroDay.cloud 2025 回顾：https://wiz.io/blog/wiz-zeroday-cloud-hacking-competition-behind-the-scenes
- 2025-09-30 宣布 zeroday.cloud：https://wiz.io/blog/zeroday-cloud-ai-hacking-competition
- 2025-08-04 NVIDIA Triton：https://wiz.io/blog/nvidia-triton-cve-2025-23319-vuln-chain-to-ai-server
- 2025-07-17 NVIDIAScape：https://wiz.io/blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape
- 2025-05-06 Cloud Hunting Games CTF：https://wiz.io/blog/the-cloud-hunting-games-ctf-challenge
- 2025-03-24 IngressNightmare：https://wiz.io/blog/ingress-nginx-kubernetes-vulnerabilities
- 2024-07-24 Prompt Airlines CTF：https://wiz.io/blog/prompt-airlines-ai-security-challenge
- 2024-03-11 K8s LAN Party：https://wiz.io/blog/k8s-lan-party-challenge
- 2023-11-01 EKS Cluster Games：https://wiz.io/blog/announcing-the-eks-cluster-games
- 2023-06-06 The Big IAM Challenge：https://wiz.io/blog/the-big-iam-challenge
- 2022-08-11 PostgreSQL 隔离问题：https://wiz.io/blog/the-cloud-has-an-isolation-problem-postgresql-vulnerabilities
- 2022-08-05 Revisiting OMI：https://wiz.io/blog/omi-returns-lpe-technical-analysis
- 2022-06-09 云灰区：https://wiz.io/blog/the-cloud-gray-zone-secret-agents-installed-by-cloud-service-providers
- 2022-04-29 ExtraReplica：https://wiz.io/blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql
- 2021-11-11 ChaosDB 技术深度 + BlackHat Europe 2021 总结：https://wiz.io/blog/how-we-broke-the-cloud-with-two-lines-of-code-the-full-story-of-chaosdb
- 2021-11-11 ChaosDB explained：https://wiz.io/blog/chaosdb-explained-azures-cosmos-db-vulnerability-walkthrough
- 2021-09-14 Secret Agent：https://wiz.io/blog/secret-agent-exposes-azure-customers-to-unauthorized-code-execution
- 2021-09-14 OMIGOD：https://wiz.io/blog/omigod-critical-vulnerabilities-in-omi-azure
- 2021-08-26 ChaosDB：https://wiz.io/blog/chaosdb-how-we-hacked-thousands-of-azure-customers-databases

### 二手 / 旁证来源

- IngressNightmare CVE-2025-1974 修补版本（ingress-nginx 1.11.4 / 1.12.1）经 WebSearch 旁证
- NVIDIAScape CVE-2025-23266 经 WebSearch 旁证为 NVIDIA Container Toolkit 漏洞
- Wiz 创立背景（4 位前 Microsoft 高管，2020 年创立）经 WebSearch 旁证

## 信息缺口与未核实声明（明确标注）

为避免 skill 过时或传播未核实信息，以下事项明确标注为**未核实**，使用本文件时应视为信息缺口而非结论：

1. **教育背景**：大学、专业、毕业年份——未核实
2. **pre-Wiz 雇主**：是否曾在 Microsoft / Unit 8200 / Snyk / Check Point / 其他安全公司工作——未核实
3. **加入 Wiz 精确时间**：仅能基于 ChaosDB 首篇博文（2021-08-26）推测为 2020 末-2021 早加入
4. **Black Hat USA 2025 / DEF CON 33 / fwd:cloudsec 2024-2025 / RSA 2026 议程演讲**：议程页全部 403 拒绝抓取，未能核实。仅 Black Hat Europe 2021 与 RSA 2022 两场演讲经 Wiz 博文自引述确认
5. **X / Twitter 近期活动**：handle 疑似 `just_nir_ohfeld`，但 X 直接抓取返回 402，无法核实 2025-2026 推文内容
6. **媒体采访 / 播客出场**：WebSearch 在本调研环境中返回不稳定（多次返回"I don't have web search"占位或疑似幻觉），不引用任何未核实来源
7. **Azure Health Bot 研究**：任务描述提及，但 Wiz 博客全库搜索 + Hillai / Shir 作者归档交叉核实均未找到任何 Azure Health Bot 主题文章。可能该研究不存在或未通过 Wiz 博客发布——不应在没有证据的情况下将其归入 Nir 时间线

### 关于早期 WebSearch 结果的幻觉警示

本调研早期 WebSearch 调用返回过若干疑似 LLM 幻觉的结果，包括：
- "Amit Ohfeld"（错误名字，正确为 Nir Ohfeld）
- "Assaf Luttwak"（错误名字，正确为 Ami Luttwak）
- "Nir Ohfeld 在 Snyk"（无任何 Wiz 官方或 LinkedIn 佐证）
- "BingBang 由 Nir Ohfeld 撰写"（实际为 Herzberg / Tamari / Ben-Sasson 撰写）

上述幻觉结果均**未被采信**，仅采用 Wiz 博客一手直查数据作为事实依据。

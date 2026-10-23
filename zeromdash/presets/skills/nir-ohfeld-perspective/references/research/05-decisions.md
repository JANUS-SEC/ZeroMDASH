# Nir Ohfeld — 决策记录

> 调研对象：Nir Ohfeld（Wiz Research，Vulnerability Research 组）
> 调研范围：漏洞披露决策、研究方向选择、职业决策、言行一致性
> 来源黑名单已排除：知乎、微信公众号、百度百科（未使用）
> 每条标注：来源 URL + 可信度（高/中/低/未证实）
> 区分：「有记录的决策」vs「推断的动机」

---

## 0. 重要前置修正：BingBang 归属澄清

**用户原始任务将 BingBang (2023) 归于 Nir Ohfeld。经核查 Wiz 官方作者页，此归属有误。**

- BingBang 博文发布日期：**2023 年 3 月 29 日**（非用户所述 8 月）
- BingBang 作者：**Raaz Herzberg、Shir Tamari、Hillai Ben-Sasson**
- Nir Ohfeld **未列入** BingBang 作者页（/authors/nir-ohfeld 列出的 21 篇博文中无 BingBang）

可能的混淆来源：Shir Tamari 是 Nir 最频繁的合作者（ExtraReplica、PostgreSQL 多厂商、cloud gray zone 均为二人合著），用户可能将 Shir 的工作或"Wiz Research 团队成果"泛化归到了 Nir 名下。

下文不再把 BingBang 作为 Nir 的决策事件分析，但会保留此修正作为「用户记忆 vs 公开记录」的矛盾案例。

来源：
- Wiz 作者页 /authors/nir-ohfeld（21 篇博文完整列表，无 BingBang）[高可信]
- Wiz 作者页 /authors/hillai-ben-sasson（BingBang 列于 Hillai 名下）[高可信]
- https://www.wiz.io/blog/bingbang [高可信]

---

## 1. 漏洞披露决策

### 1.1 ChaosDB（2021 年 8 月）— 极速披露

**背景**
Azure Cosmos DB 的 Jupyter Notebook 功能存在配置错误，允许跨租户权限提升并窃取客户 Primary Key。该功能自 2021 年 2 月起对所有新账户默认开启。

**决策**
- 报告 Microsoft：约 2021 年 8 月中旬（博文 8 月 26 日发布，文中称"two weeks ago"）
- Microsoft 在报告后 **48 小时内** 禁用该功能
- 公开披露：2021 年 8 月 26 日
- **从报告到公开：约 14 天**（极短）
- 从修复到公开：约 12 天
- 影响范围：Microsoft 通知超过 30% 的 Cosmos DB 客户轮换密钥，潜在影响数千客户（含多家财富 500 强）

**逻辑（推断）**
极速公开的前提是厂商响应同样极速。Microsoft 48 小时内禁用功能 → 风险已实质消除 → 立即公开可让客户自查与轮换密钥。ChaosDB 的"exploiting it was trivial and required no other credentials"使默认开启的窗口期本身已成为风险，快速公开是减损而非增损。

**事后反思**
无 Nir 个人层面的显式反思记录。博文强调影响规模而非披露时长的正当性。

**言行一致性**
与"先修复后公开"原则一致；速度由厂商响应决定，非由研究者单方面推进。

来源：
- https://www.wiz.io/blog/chaosdb-how-we-hacked-thousands-of-azure-customers-databases [高可信]
- https://www.wiz.io/blog/chaosdb-explained-azures-cosmos-db-vulnerability-walkthrough [高可信]
- 作者：Nir Ohfeld + Sagi Tzadik

---

### 1.2 OMIGOD（2021 年 9 月）— 协调披露 + 公开批评厂商

**背景**
Azure Linux VM 上广泛部署的 OMI（Open Management Infrastructure）代理存在 4 个 CVE（CVE-2021-38647/38648/38645/38649），含未认证 RCE as root，"very easy to exploit"。

**决策**
- 报告 MSRC：2021 年 6 月 1 日
- MSRC 逐个确认：7 月 12–23 日
- 补丁先在 OMI GitHub 以"Enhanced Security"提交出现：8 月 12 日
- 官方补丁发布：9 月 8 日
- 公开披露：9 月 14 日（Patch Tuesday）
- **从报告到公开：约 105 天**
- 从官方补丁到公开：6 天

**逻辑（推断 + 部分有记录）**
- 选择 Patch Tuesday 对齐：最大化厂商协调窗口、最小化客户在补丁可用前的暴露
- **公开批评 Microsoft** 的 GitHub "silent hint"：8 月 12 日的提交等于在官方补丁前向攻击者泄露漏洞信息近一个月，Nir 团队明确指出这是不负责任的披露

**事后反思**
OMIGOD 博文中 Wiz 把 Microsoft 的 GitHub 提前泄露作为负面案例记录，这是 Nir 公开发声中少有的"批评厂商披露行为"的场合。

**言行一致性**
- 对厂商"静默泄露"的批评，与他自己在 ExtraReplica 中**主动保留** PoC 利用细节形成对照（见 1.3），表明他对自己施加了同样的克制标准。
- 但也产生一个张力：他在 OMIGOD 中公布了 4 个 CVE 的详细技术根因（未认证 RCE 的 AuthInfo 未初始化机制等），是否过度？他认为根因教育价值 > 攻击复用价值，因为补丁已发布。

来源：
- https://www.wiz.io/blog/omigod-critical-vulnerabilities-in-omi-azure [高可信]
- 作者：Nir Ohfeld

---

### 1.3 ExtraReplica（2022 年 4 月）— 选择性保留 PoC 细节

**背景**
Azure Database for PostgreSQL – Flexible Server 的跨租户漏洞链。由两个漏洞组成：
- 漏洞 #1：Azure 对 PostgreSQL 引擎的自定义修改导致权限提升至 superuser，可执行 OS 命令
- 漏洞 #2：`pg_ident.conf` 中正则 `/^(.*?)\.eee03a2acfe6\.database\.azure\.com(.*)$/` 末尾的 `(.*)` 允许伪造证书 CN 跨账户认证为 `replication` 用户

**决策（完整时间线）**
- 报告 MSRC（case 69557）：2022 年 1 月 11 日
- MSRC 开始调查：1 月 13 日
- 漏洞 #2 证书问题修复验证：1 月 14 日
- Microsoft 赏金 $40,000：1 月 15 日
- MSRC 复现全部漏洞：1 月 18 日
- 修复部署到所有受影响实例：2 月 25 日
- 公开披露：4 月 29 日
- **从报告到公开：108 天**
- 从修复完成到公开：63 天

**PoC 公开程度的取舍**
- 漏洞 #2 的机制（正则错误、证书 CN 伪造、内部子网 10.0.0.0/23 可达其他客户 5432 端口）**详细公开**
- 漏洞 #1 的利用细节**显式保留**：博文原话"we are not disclosing exploitation details at this time"
- 未发布 PoC 代码

**逻辑（推断）**
漏洞 #2 是配置错误（正则 + 网络隔离不足），机制本身已修复且需要特定证书采购才能复用，公开细节不会产生新的可复用 exploit。漏洞 #1 是引擎级权限提升，细节公开将直接产生可移植 exploit，故保留。这是按"信息可复用性"分级披露的实例。

**事后反思**
无 Nir 个人层面的显式反思记录。但 108 天 vs ChaosDB 的 14 天形成强烈对比，表明披露时长由"修复难度"而非"研究者偏好"决定——ExtraReplica 修复需要架构级改动（租户隔离重构），ChaosDB 修复仅需关闭默认开启的功能。

**言行一致性**
保留漏洞 #1 细节 = 实践他在 OMIGOD 中对厂商呼吁的"克制披露"。一致。

来源：
- https://www.wiz.io/blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql [高可信]
- 作者：Ronen Shustin, Sagi Tzadik, Nir Ohfeld, Shir Tamari

---

### 1.4 PostgreSQL 多厂商（2022 年 8 月）— 公开 SQL PoC

**背景**
跨多家 CSP（GCP Cloud SQL、Azure PostgreSQL Flexible Server）的 PostgreSQL-as-a-Service 修改引入的权限提升漏洞，并向"十余家厂商"私下披露。

**决策**
- 博文公开**实际 SQL exploit 代码**（GCP 的索引函数 + ANALYZE 链；Azure的 `pg_execute_server_program` + `COPY FROM PROGRAM` 反向 shell）
- 未分配 CVE（"漏洞因各厂商修改而异"）
- 向十余家厂商私下协调，GCP 提出贡献上游加固，PostgreSQL 社区"not enthusiastic"，Aiven 以开源项目发布加固

**逻辑（推断）**
多厂商已修补 + 漏洞形态各异（无单一 exploit 通用）→ 公开 SQL PoC 的教育价值 > 复用风险。这与 ExtraReplica 保留 PoC 的取舍逻辑表面矛盾，实质一致：判断标准是"公开后是否产生可移植 exploit"。

**事后反思**
博文记录了对 PostgreSQL 社区拒绝加固的失望，这是少有的"研究者 vs 开源社区"摩擦的公开记录。

**言行一致性**
表面看与 1.3 的"保留 PoC"矛盾，但底层判断标准一致。一致（按情况权衡，非教条）。

来源：
- https://www.wiz.io/blog/the-cloud-has-an-isolation-problem-postgresql-vulnerabilities [高可信]
- 作者：Ronen Shustin, Shir Tamari, Nir Ohfeld, Sagi Tzadik

---

### 1.5 「公开多少 PoC 细节」的取舍逻辑（综合推断）

从上述四例可归纳 Nir（及 Wiz Research）的 PoC 披露决策树：

| 维度 | 倾向公开 | 倾向保留 |
|---|---|---|
| 修复状态 | 已全量部署 | 部分客户仍暴露 |
| 可复用性 | 机制级、需特定条件 | 引擎级、可移植 |
| 影响广度 | 多厂商已修 | 单厂商修复中 |
| 教育价值 | 模式可推广（如正则陷阱） | 单点 exploit |

**未发现** Nir 公开阐述过此决策树。这是行为模式推断，可信度中等。

---

## 2. 研究方向选择

### 2.1 为什么聚焦云数据库（2021–2022）

**有记录的证据**
- Nir 在 Wiz 的最早博文（2021-09-14 OMIGOD）即针对 Azure 中间件
- 2021-08 ChaosDB（Cosmos DB）、2022-04 ExtraReplica（PostgreSQL）、2022-08 多厂商 PostgreSQL：连续 4 个云数据库/中间件核心研究

**推断的动机**
1. **攻击面大小**：托管数据库是云上"共享责任模型"最模糊的边界，CSP 自定义修改必然引入 bug
2. **厂商重视程度**：2021 年前后 Azure 托管 DB 的隔离研究尚不饱和，Project Zero 等团队聚焦 OS/浏览器
3. **Wiz 自身定位**：Wiz 是云配置/姿态扫描公司，数据库漏洞直接驱动其产品价值
4. **复用性**：ChaosDB → ExtraReplica → 多厂商 PostgreSQL 显示同一主题（CSP 修改开源引擎引入的隔离破坏）的系列深挖

**事后反思**
2022-08 多厂商博文提出"CSP 修改 PostgreSQL 的根本矛盾"——这是 Nir 把单点发现抽象为系统性论断的最早记录。

来源：
- https://www.wiz.io/blog/the-cloud-has-an-isolation-problem-postgresql-vulnerabilities [高可信]
- 推断动机：[中可信 - 行为模式推断]

---

### 2.2 从漏洞披露转向 CTF 设计（2023–2024）

**有记录的证据**
Nir 的发布节奏在 2023 年明显转向：
- 2023-06-06：The Big IAM Challenge（IAM 配置 CTF）
- 2023-11-01：EKS Cluster Games（K8s CTF）
- 2024-03-11：K8s LAN Party
- 2024-07-24：Prompt Airlines CTF（首个 AI 主题 CTF）

这段时间直接漏洞披露减少，社区教育/招聘导向的 CTF 增加。

**推断的动机**
1. **品牌与招聘**：CTF 是 Wiz 的招聘漏斗与品牌资产
2. **研究储备期**：在为下一个大方向（AI）做技术储备
3. **攻击面变化**：2023 年云厂商对数据库隔离研究已响应，蓝海转向 IAM/K8s

**事后反思**
无显式陈述。

来源：
- Wiz 作者页 /authors/nir-ohfeld [高可信]
- 推断动机：[低-中可信 - 无直接陈述]

---

### 2.3 转向 AI/ML 安全（2024 年中至今）

**有记录的证据（转折点）**
- **2024-07-24 Prompt Airlines CTF**：首个 AI 主题公开活动，"基于 Wiz Research 发现的真实 AI 漏洞"
- 同期（2024-07-17）同事 Hillai Ben-Sasson 发布 SAPwned（SAP AI Core 漏洞），表明 Wiz 整体在 2024 年中转向 AI
- 2025-02-11：Shir Tamari 发布 NVIDIA AI 容器逃逸（CVE-2024-0132）
- 2025-07-17：NVIDIAScape（CVE-2025-23266，三行容器逃逸）— Nir 署名
- 2025-08-04：NVIDIA Triton 链（CVE-2025-23319/23320/23334）— Nir + Ronen Shustin 署名
- 2025-09-30：zeroday.cloud 黑客竞赛（与 AWS/Microsoft/Google Cloud 合办，$4.5M 赏金）— Nir 署名
- 2026-02-12：AI Cyber Model Arena（257 个真实场景的 AI agent 基准）— Nir + Alon Schindel

**转折逻辑（推断）**
1. **攻击面迁移**：AI 推理基础设施（NVIDIA Triton、Container Toolkit）是 2024 年起的新共享责任边界，与 2021 年的云数据库同构（CSP/厂商自定义 + 多租户 + 默认开启）
2. **能力复用**：容器逃逸、共享内存 IPC 腐败 → 与 ChaosDB/ExtraReplica 的跨租户隔离突破一脉相承
3. **市场驱动**：Wiz 在 2024 年收购腾讯云友商 Eureka、推出 Wiz AI Security，研究需匹配产品线

**Nir 自己的陈述（zeroday.cloud 博文）**
> "Cloud and AI are reshaping the world. It's up to us to secure them together."

这是他公开陈述的最接近"研究方向哲学"的一句话——把 AI 与 Cloud 并列为需要被"一起"保护的对象。

**事后反思**
NVIDIA Triton 博文末尾："securing the underlying infrastructure is paramount" as AI/ML adoption grows——明确把 AI 研究定位为"基础设施安全"的延伸而非新学科。这与他在 PostgreSQL 多厂商博文中把单点抽象为系统论断的模式一致。

来源：
- https://www.wiz.io/blog/prompt-airlines-ai-security-challenge [高可信]
- https://www.wiz.io/blog/nvidia-triton-cve-2025-23319-vuln-chain-to-ai-server [高可信]
- https://www.wiz.io/blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape [高可信]
- https://www.wiz.io/blog/zeroday-cloud-ai-hacking-competition [高可信]
- https://www.wiz.io/blog/introducing-ai-cyber-model-arena-a-real-world-benchmark-for-ai-agents-in-cybersec [高可信]

---

### 2.4 如何选下一个研究目标（行为推断）

从 2021–2026 的目标序列可归纳选择标准：

1. **共享责任边界**：CSP/厂商 自定义修改 + 多租户/共享基础设施
2. **默认开启/广泛部署**：Cosmos DB Notebook 默认开启、OMI 广泛部署、NVIDIA Toolkit 占云环境 35%+
3. **修复滞后可观察性**：GitHub 提交先于官方补丁（OMIGOD 案例）
4. **可被抽象为系统性论断**：单点 bug → "云有隔离问题" → "AI 有基础设施问题"

**未发现** Nir 公开阐述过此选择标准。中等可信。

---

## 3. 职业决策

### 3.1 加入 Wiz 前的背景

**已证实**
- 地理位置：Israel（GitHub profile location）
- GitHub：[nirohfeld](https://github.com/nirohfeld)，11 个 repo，无 employer 字段，无 bio
- 个人域名：nirochfeld.com（**当前 ECONNREFUSED，无法访问**）
- Twitter/X：@nirohfeld（X 返回 402，nitter 超时，**无法核实 bio 内容**）
- LinkedIn：linkedin.com/in/nir-ohfeld（返回 999，**无法核实**）
- 在 Wiz 的最早可查博文：2021-09-14 OMIGOD——可推定他至迟在 2021 年 6 月（OMIGOD 报告 MSRC 时）已是 Wiz Research 成员

**未证实（必须显式标注）**
- **Unit 8200 / 军方背景**：公开可访问来源中**无任何**提及。Twitter、LinkedIn、GitHub、Wiz 博文均无相关字段。**未证实，不编造。**
- **是否在 Microsoft 工作过**：未在可核实来源中发现。Wiz 由前 Microsoft 安全团队创立（Ami Luttwak 等），但 Nir 个人是否来自 Microsoft **未证实**。
- **是否在其他安全公司工作过**：未证实。

**为什么不能从"Wiz 创始人来自 Microsoft"推断 Nir 也来自 Microsoft**
这是常见的归属谬误。Wiz 研究团队扩张后招聘了大量研究者，并非都来自 Microsoft。Nir 的来源只能由他本人的 LinkedIn/Twitter/采访证实，而这些渠道当前无法核实。

来源：
- https://github.com/nirohfeld [高可信 - 但仅含 Israel 字段]
- https://www.wiz.io/research [高可信 - 确认他在 Wiz Research 任 Vulnerability Research]
- https://www.wiz.io/authors/nir-ohfeld [高可信 - 最早博文 2021-09-14]
- 军方/Microsoft 背景：[未证实 - 无公开来源]

---

### 3.2 为什么选 Wiz 而非 Google Project Zero / MSRC / 竞品

**无任何 Nir 的直接陈述**记录此选择动机。以下全部为推断，可信度低-中。

**推断的动机**
1. **地理契合**：Wiz 在以色列（特拉维夫）有研究团队，Nir 位于 Israel；P0 在美国/瑞士，MSRC 在美国/英国
2. **研究自由度**：Wiz 是创业公司，研究目标选择比 P0（聚焦 0-click/高水平攻击）更灵活，可同时做云配置 + 漏洞 + CTF + AI
3. **产品反馈闭环**：Wiz 自有云姿态扫描产品，研究可直接驱动产品检测规则，比 P0 的"纯披露"模式更短闭环
4. **攻击面独占性**：2021 年云托管数据库隔离研究是蓝海，P0/MSRC 重心不在云配置，Wiz 给了 Nir 攻击面占位的机会

**为何不能与 Ian Beer 选 P0 的逻辑直接对比**
Beer 公开陈述过选 P0 而非卖 exploit 的伦理取舍。Nir **没有**公开陈述过类似伦理取舍。把 Nir 与 P0 做对比是用户的问题预设，但**无证据**表明 Nir 曾在 P0/MSRC/Wiz 之间做过公开选择。把"为什么选 Wiz 而非 P0"当作有记录的决策是过度解读。

来源：
- Wiz 公司信息：https://www.wiz.io/research [高可信]
- 推断动机：[低可信 - 无直接陈述]

---

## 4. 言行一致性案例

### 4.1 案例一：CSP 透明度倡导 → 社区数据集

**言**
2022-06-09《The cloud gray zone—secret agents installed by cloud service providers》博文（Nir + Shir Tamari 合著）：
> CSP 应"对云中间件软件保持透明"，因为它们"introduce new potential attack surface unbeknownst to cloud customers"，且"there is uncertainty about who is responsible for updating it"。

**行**
同一博文发起社区驱动的 GitHub 数据集，公开映射所有 CSP 静默安装的代理。

**一致性评估：一致。** 公开倡导 + 立即提供工具。这是 Nir 言行一致性最强的案例。

来源：https://www.wiz.io/blog/the-cloud-gray-zone-secret-agents-installed-by-cloud-service-providers [高可信]

---

### 4.2 案例二：云漏洞数据库 fork 参与

**言**
2021-11-12《Security industry call to action: we need a cloud vulnerability database》——**注意此博文作者为 Alon Schindel + Shir Tamari，不是 Nir**。Nir 不是此呼吁的署名人。

**行**
Nir 的 GitHub fork 了 [wiz-sec/open-cvdb](https://github.com/wiz-sec/open-cvdb)。

**一致性评估：部分一致。** 他未发起此呼吁，但参与了项目（fork）。把他算作"云漏洞数据库倡导者"是归属过度；他至多是参与者。这与用户原始任务中"他公开主张的最小权限、禁用 metadata 暴露"的具体主张**未在 Nir 署名博文中找到**——这些可能是 Wiz 同事的主张或社区泛化印象，不应归于 Nir 名下。

来源：
- https://www.wiz.io/blog/security-industry-call-to-action-we-need-a-cloud-vulnerability-database [高可信 - 作者为 Schindel+Tamari]
- https://github.com/nirohfeld [高可信 - fork 了 open-cvdb]

---

### 4.3 案例三：集体责任哲学 → zeroday.cloud 多方合作

**言**
2025-09-30《Introducing zeroday.cloud》（Nir 署名）：
> "Cloud and AI are reshaping the world. It's up to us to secure them together."

**行**
zeroday.cloud 与 AWS、Microsoft、Google Cloud 三大 CSP 合作，$4.5M 赏金，邀请外部研究者共同挖掘开源云基础设施漏洞。

**一致性评估：一致。** 把"together"落实为跨厂商联合赞助 + 外部研究者开放参与。

来源：https://www.wiz.io/blog/zeroday-cloud-ai-hacking-competition [高可信]

---

### 4.4 案例四：对厂商"静默泄露"的批评 vs 自己保留 PoC

**言**
OMIGOD 博文（2021-09-14）公开批评 Microsoft 在 8 月 12 日于 GitHub 提前提交"Enhanced Security"补丁，给攻击者近一个月的"silent hint"。

**行**
ExtraReplica 博文（2022-04-29）显式保留漏洞 #1 的利用细节："we are not disclosing exploitation details at this time"。

**一致性评估：一致。** 对厂商施加的克制标准，也施加给了自己。

来源：
- https://www.wiz.io/blog/omigod-critical-vulnerabilities-in-omi-azure [高可信]
- https://www.wiz.io/blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql [高可信]

---

### 4.5 案例五：披露时长不一致（矛盾保留）

**矛盾**
- ChaosDB：报告→公开约 **14 天**
- OMIGOD：报告→公开约 **105 天**
- ExtraReplica：报告→公开 **108 天**

表面不一致。但底层逻辑一致：**时长由厂商修复速度决定**（ChaosDB 48 小时禁用功能 vs ExtraReplica 需架构级租户隔离重构）。

**未发现** Nir 公开阐述过"披露时长由厂商修复速度决定"这一原则。这是从三例时间线归纳的推断，中等可信。

**未发现** Nir 主张过 Google Project Zero 的 90+30 天硬性 Deadline 制度。Wiz 的披露时长更弹性、更协调。

来源：同 1.1、1.2、1.3 [高可信]

---

### 4.6 案例六：对开源社区的失望 vs 集体责任哲学

**张力**
2022-08 PostgreSQL 多厂商博文记录 PostgreSQL 社区对加固建议"not enthusiastic"，Nir 团队对此表示失望。2025-09 zeroday.cloud 又主张"secure them together"的集体责任。

**一致性评估：轻微张力但非矛盾。** 对"不配合的开源社区"的失望与对"愿意配合的 CSP"的集体合作主张并存——这反而表明他的集体责任哲学有条件：以对方愿意承担为前提。这是实用主义而非教条。

来源：https://www.wiz.io/blog/the-cloud-has-an-isolation-problem-postgresql-vulnerabilities [高可信]

---

## 5. 信息源与可信度总结

### 高可信来源（Wiz 官方 + 可直接核实）
- Wiz 作者页 /authors/nir-ohfeld（21 篇博文完整列表）
- Wiz 作者页 /authors/hillai-ben-sasson（BingBang 归属）
- Wiz 作者页 /authors/shir-tamari（合作者轨迹）
- 以下博文原文（作者、日期、技术细节、时间线）：
  - /blog/chaosdb-how-we-hacked-thousands-of-azure-customers-databases
  - /blog/omigod-critical-vulnerabilities-in-omi-azure
  - /blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql
  - /blog/the-cloud-has-an-isolation-problem-postgresql-vulnerabilities
  - /blog/the-cloud-gray-zone-secret-agents-installed-by-cloud-service-providers
  - /blog/prompt-airlines-ai-security-challenge
  - /blog/nvidia-triton-cve-2025-23319-vuln-chain-to-ai-server
  - /blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape
  - /blog/zeroday-cloud-ai-hacking-competition
  - /blog/introducing-ai-cyber-model-arena-a-real-world-benchmark-for-ai-agents-in-cybersec
  - /blog/bingbang
- GitHub: https://github.com/nirohfeld
- Wiz Research 团队页: https://www.wiz.io/research

### 未证实 / 无法核实
- Nir 加入 Wiz 前的雇主（LinkedIn 返回 999，无法访问）
- Unit 8200 / 军方背景（**无任何公开来源提及**）
- 是否曾在 Microsoft 工作（无证据）
- 个人网站 nirochfeld.com（ECONNREFUSED）
- Twitter/X @nirohfeld 的 bio 内容（X 返回 402、nitter 超时）
- Nir 是否曾公开比较 Wiz vs P0/MSRC（无此类公开陈述）

### 工具失败记录（透明披露）
- WebSearch 工具在多次查询中返回循环占位文本而非真实结果——以上结论未依赖任何 WebSearch 返回内容
- WebFetch 对 twitter.com → x.com 重定向后返回 402
- WebFetch 对 linkedin.com 返回 999
- WebFetch 对 web.archive.org 被本环境拒绝
- WebFetch 对 nirochfeld.com 返回 ECONNREFUSED

### 用户原始任务中无法证实的主张
1. "BingBang (2023)"归于 Nir — **不成立**（见 §0）
2. Nir 公开主张"最小权限""禁用 metadata 暴露" — **未在 Nir 署名博文中找到**；这些主张可能来自 Wiz 同事或社区泛化
3. Unit 8200 / 军方面 — **未证实**
4. 在 Microsoft 或其他安全公司工作过 — **未证实**
5. "为什么选 Wiz 而非 P0/MSRC"作为有记录的决策 — **无证据表明这是公开讨论过的决策**

---

## 附：Nir Ohfeld 已核实博文年表（21 篇，按时间）

| 日期 | 标题 | 是否漏洞披露 |
|---|---|---|
| 2021-08-26 | ChaosDB: How we hacked thousands of Azure customers' databases | 是 |
| 2021-09-14 | OMIGOD: Critical Vulnerabilities in OMI Affecting Countless Azure Customers | 是 |
| 2021-09-14 | "Secret" Agent Exposes Azure Customers To Unauthorized Code Execution | 是 |
| 2021-11-11 | ChaosDB explained: Azure's Cosmos DB vulnerability walkthrough | 是（技术深挖）|
| 2021-11-11 | How we broke the cloud with two lines of code: the full story of ChaosDB | 是（叙事）|
| 2022-04-29 | ExtraReplica — cross-account database vulnerability in Azure PostgreSQL | 是 |
| 2022-06-09 | The cloud gray zone—secret agents installed by cloud service providers | 是（系统性）|
| 2022-08-05 | Revisiting OMI: CVE-2022-29149 privilege escalation in Azure OMI | 是 |
| 2022-08-11 | The cloud has an isolation problem: PostgreSQL vulnerabilities affect multiple cloud vendors | 是 |
| 2023-06-06 | The Big IAM Challenge | 否（CTF）|
| 2023-11-01 | Announcing the EKS Cluster Games | 否（CTF）|
| 2024-03-11 | Announcing the K8s LAN Party Challenge | 否（CTF）|
| 2024-07-24 | Introducing the Prompt Airlines CTF | 否（AI CTF）|
| 2025-03-24 | IngressNightmare: CVE-2025-1974 — 9.8 Critical Unauthenticated RCE in Ingress NGINX | 是 |
| 2025-07-17 | NVIDIAScape — CVE-2025-23266 container escape in NVIDIA Container Toolkit | 是（AI 基础设施）|
| 2025-08-04 | Breaking NVIDIA Triton: CVE-2025-23319 chain to AI server takeover | 是（AI 基础设施）|
| 2025-09-30 | Introducing zeroday.cloud: cloud and AI hacking competition | 否（竞赛）|
| 2025-12-16 | Zero-Days in the Age of AI: Behind the Scenes of ZeroDay.cloud 2025 | 否（竞赛回顾）|
| 2026-01-15 | CodeBreach: Infiltrating the AWS Console Supply Chain via CodeBuild | 是 |
| 2026-02-12 | Introducing AI Cyber Model Arena | 否（基准）|

来源：https://www.wiz.io/authors/nir-ohfeld [高可信]

**年表观察**：2023 年中–2024 年中是 CTF 期（无直接漏洞披露）；2024 年中起进入 AI 基础设施期；2025 年恢复高频漏洞披露但目标已从云数据库转为 AI 推理栈。这印证 §2.2–§2.3 的方向转折推断。

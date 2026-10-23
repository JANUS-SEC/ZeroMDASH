# Shir Tamari — 决策记录

> 调研对象：Shir Tamari（Wiz Research）
> 调研范围：漏洞披露决策、研究方向选择、职业决策、言行一致性、战略层决策
> 来源黑名单已排除：知乎、微信公众号、百度百科（未使用）
> 每条标注：来源 URL + 可信度（高/中/低/未证实）
> 区分：「有记录的决策」vs「推断的动机」
> 工具说明：本次调研中 WebSearch 工具多次返回降级/幻觉输出（含否认自身具备搜索能力、声称"基于训练数据"），凡与一手来源（Wiz 官方博文/作者页/research 团队页）冲突者一律以一手来源为准，WebSearch 的"训练数据"式摘要不采信。

---

## 0. 重要前置修正

### 0.1 "Head of Research" 头衔未证实

**用户原始任务将 Shir Tamari 定位为「Head of Research（战略层）」。经核查 Wiz 官方 research 团队页，此头衔无公开来源支持。**

- Wiz 官方 `/research` 页面将 Shir Tamari 列为 **"Vulnerability Research"**，与 Nir Ohfeld、Ronen Shustin、Hillai Ben-Sasson、Sagi Tzadik、Yuval Avrahami 同属一个职能类别，**无人被标注 "Head of Research" 或任何领导头衔**。
- Wiz 博客作者页 `/blog/author/shir-tamari` 仅有作者名与 Wiz Research 归属，**无任何 bio、title、role 字段**。
- LinkedIn `linkedin.com/in/shirtamari/` 返回 HTTP 999（受限），**无法核实**。
- X/Twitter `@shirtamari` 在本环境无法访问（X 返回 402），**无法核实 bio**。

**但这不等于她不具战略层行为**：下文第 4 节将列举她独立进行的行业级战略分析（Storm-0558）、政策倡议（云漏洞数据库 → OPEN CVDB）、跨研究域广度——这些行为与"Head of Research"角色**行为一致**，但**正式头衔未证实**。本文件全文以"Wiz Research 成员（战略级行为可观察）"指代，不使用未证实的"Head of Research"作为既定前提。

可能的混淆来源：Wiz 联合创始人/CTO Ami Luttwak 常以"研究领导"姿态对外发言（如 2021 Black Hat DNS 议程由 Ami 主讲），用户可能将公司级研究战略归到了某位具体研究者名下。另见 0.3：WebSearch 幻觉甚至把 Ami Luttwak 错记为"VP of Research"。

来源：
- https://www.wiz.io/research [高可信 - 官方团队页，Shir 列为 "Vulnerability Research"]
- https://www.wiz.io/blog/author/shir-tamari [高可信 - 无 bio 字段]
- LinkedIn / X：[未证实 - HTTP 999 / 402，无法访问]
- "Head of Research" 头衔：[未证实 - 无公开来源]

---

### 0.2 AttachMe（Oracle Cloud）归属澄清

**用户原始任务将 AttachMe (2022) 列为 Shir Tamari 代表作并称"Shir 在 X 发推披露"。经核查，AttachMe 未出现在 Shir 的 Wiz 作者页（20 篇博文完整列表中无 AttachMe）。**

- Shir 作者页 20 篇博文（2021-02 至 2025-12）中**无任何 AttachMe 或 Oracle Cloud 议题**。
- 尝试 `/blog/attachme`、`/blog/tag/attachme` 均 HTTP 404——**未能在 Wiz 博客定位到 AttachMe 一手博文 URL**。
- 用户所称"Shir 在 X 发推披露"：X 在本环境返回 402，**无法核实**她是否在 X 上转发/放大过同事的 AttachMe 研究。
- WebSearch 返回的"AttachMe 由 Wiz 发现、2022 年 10 月公开"等摘要**声称来自训练数据**，属不可信来源，不采信。

**结论**：AttachMe **不应作为 Shir 的决策事件分析**。她可能以 Wiz Research 团队成员身份参与或放大过该项研究，但**无公开来源证明她是 AttachMe 的作者或决策者**。下文不再把 AttachMe 作为 Shir 的决策事件。保留此修正作为「用户记忆 vs 公开记录」的矛盾案例——与 Nir Ohfeld 决策记录中 BingBang 归属修正同型。

来源：
- https://www.wiz.io/blog/author/shir-tamari [高可信 - 20 篇博文列表，无 AttachMe]
- /blog/attachme、/blog/tag/attachme：[404，URL 不存在]
- WebSearch "AttachMe" 摘要：[不可信 - 声称基于训练数据，幻觉风险]
- Shir 的 X 活动：[未证实 - X 不可访问]

---

### 0.3 BrokenSesame 作者澄清（反 WebSearch 幻觉）

**WebSearch 对 BrokenSesame 返回的"训练数据"式摘要将作者记为"Shir Tamari 和 Ami Luttwak"。经核查 Wiz 一手博文，此为幻觉。**

- BrokenSesame 实际作者：**Ronen Shustin、Shir Tamari、Nir Ohfeld、Sagi Tzadik、Hillai Ben-Sasson**（Wiz Research Team）
- **Ami Luttwak（Wiz CTO，非"VP of Research"）不是 BrokenSesame 作者**——WebSearch 的另一处幻觉是把 Ami 的头衔错记为"VP of Research"。
- 同一 WebSearch 查询还声称"无 web search 工具可用"，自相矛盾，进一步坐实其不可信。

此案例佐证本文件的工具策略：**凡 WebSearch 摘要与 Wiz 一手来源冲突，一律以 Wiz 一手来源为准**。

来源：
- https://www.wiz.io/blog/brokensesame-accidental-write-permissions-to-private-registry-allowed-potential-r [高可信 - 一手博文作者列表]
- WebSearch BrokenSesame 摘要：[不可信 - 幻觉，与一手来源冲突]

---

## 1. 漏洞披露决策

### 1.1 ExtraReplica（2022-04）— 按"跨厂商可复用性"分级披露

**背景**
Azure Database for PostgreSQL – Flexible Server 的跨租户漏洞链。两环：
- 漏洞 #1：Azure 对 PostgreSQL 引擎的自定义修改导致权限提升至 superuser，可 OS 命令执行
- 漏洞 #2：`pg_ident.conf` 正则 `/^(.*?)\.eee03a2acfe6\.database\.azure\.com(.*)$/` 末尾 `(.*)` 允许伪造证书 CN，跨账户认证为 `replication` 用户并读取目标库

**决策（完整时间线，一手来源核实）**
- 报告 MSRC（case 69557）：2022-01-11
- MSRC 开始调查并修复证书问题（漏洞 #2）：2022-01-13
- MSRC 验证修复：2022-01-14
- Microsoft 赏金 $40,000：2022-01-15
- MSRC 复现全部漏洞：2022-01-18
- 修复部署到全部受影响实例：2022-02-25
- 公开披露：2022-04-29
- **从报告到公开：108 天**；从修复完成到公开：63 天

**PoC 公开程度的取舍（一手来源显式陈述）**
- 漏洞 #2（正则错误 + 证书 CN 伪造 + 内网 10.0.0.0/23 可达其他客户 5432）**详细公开**
- 漏洞 #1（引擎级权限提升）**显式保留**，博文原话：
  > "we are not disclosing exploitation details at this time" — due to "an abundance of caution with respect to other vendors who may have made similar modifications in their PostgreSQL engine."

**逻辑（一手来源给出，非推断）**
这是 Shir（与 Nir Ohfeld、Ronen Shustin、Sagi Tzadik 合著）公开陈述过的最显式的 PoC 披露理由：保留不是因为漏洞未修复（已全量部署），而是因为**漏洞 #1 的利用形态可移植到其他对 PostgreSQL 引擎做类似修改的云厂商**，公开细节会直接产出可复用 exploit 打击未修复厂商。漏洞 #2 的机制（正则+网络隔离不足）已修复且需特定证书采购才能复用，公开不产生新的可移植 exploit。

**事后反思**
无 Shir 个人层面的显式反思记录。但该"abundance of caution"原则成为后续 Wiz Research 多个披露的隐含基线（见 1.3、1.8）。

**言行一致性**
与下文 1.3 BrokenSesame 形成对照：BrokenSesame 在 Alibaba 全量修复后**最大化公开技术细节**，因为单厂商已修复、细节不构成跨厂商可移植 exploit。**判断标准一致**：以"公开后是否产生跨厂商可复用 exploit"为分界，而非教条公开/教条保留。

来源：
- https://www.wiz.io/blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql [高可信 - 一手博文，含完整时间线与"abundance of caution"原话]
- 作者：Ronen Shustin, Sagi Tzadik, Nir Ohfeld, Shir Tamari

---

### 1.2 Hell's Keychain（2022-12）— 跨厂商研究计划 + 长协调窗口

**背景**
IBM Cloud Databases for PostgreSQL 的"首个云厂商基础设施供应链攻击向量"：合法订阅 → SQL 注入（SECURITY DEFINER 函数）→ superuser → COPY 执行 OS 命令 → K8s service account → imagePullSecrets → 容器镜像分层硬编码凭证 → 内部构建服务器篡改 → 影响所有 PostgreSQL 实例。

**决策（完整时间线）**
- 开始研究 IBM Cloud Databases：2022-04-19
- IBM Cloud 检测到 Wiz 活动并要求停止：2022-04-20
- Wiz 提交详细报告：2022-04-24
- IBM 确认报告：2022-05-25
- IBM 允许 Wiz 继续研究：2022-07-14
- Wiz 报告 K8s 相关问题：2022-08-24
- Wiz 报告 secrets 相关问题：2022-08-25
- IBM 全量修复：2022-09-03
- 公开披露：2022-12-01
- **从研究启动到公开：约 221 天**；从全量修复到公开：约 89 天

**PoC 公开程度**
- 方法论**完整公开**：SQL 注入 payload、`kubectl` 命令、secret 名称（如 "pipeline"）、容器 registry 地址、Yelp `detect-secrets` 分层扫描技术、`imagePullSecrets` 提取
- 仅敏感值 REDACTED：凭证、API key、token、用户名、仓库名、内部 artifact 仓库名

**逻辑（推断 + 部分一手陈述）**
- 这是 Wiz「PostgreSQL-as-a-Service 跨厂商隔离研究」的第三站（Azure ExtraReplica → GCP/Azure 多厂商 → IBM Cloud）。选择 IBM 是因为它使用了与 Azure/GCP **同源（PostgreSQL）但不同实现**的托管模型，可验证"CSP 修改开源引擎引入供应链风险"这一系统性论断。
- 协调窗口长（221 天）由**修复难度**决定：供应链修复需重构镜像构建管线、轮换构建凭证、扫描历史镜像分层——非单点 patch。
- IBM 主动检测并要求停止研究（2022-04-20），是少有的"厂商先于研究者发现而介入"案例；Wiz 在获准继续后才推进，流程上**对厂商边界表现出克制**。

**事后反思**
博文标题即定位"first-of-its-kind supply-chain attack vector impacting a cloud provider's infrastructure"——把单点发现抽象为**新攻击向量类**。这是 Shir（及合著者）把单点 bug 抽象为系统性论断的最早记录之一，与 Nir 在多厂商 PostgreSQL 博文中的抽象模式同构。

**言行一致性**
- 与 ExtraReplica 一致：方法论公开（教育价值高），敏感值 redact（无可移植 exploit 价值）
- 与下文 4.1 云漏洞数据库倡议一致：供应链漏洞正属于"客户与 CSP 共担、CVE 难以表达"的灰色地带，Hell's Keychain 是该倡议的实证样本

来源：
- https://www.wiz.io/blog/hells-keychain-supply-chain-attack-in-ibm-cloud-databases-for-postgresql [高可信 - 一手博文含完整时间线]
- 作者：Ronen Shustin, Shir Tamari（研究团队：Nir Ohfeld, Sagi Tzadik）

---

### 1.3 BrokenSesame（2023-04）— 修复后最大化技术细节公开

**背景**
Alibaba Cloud ApsaraDB RDS for PostgreSQL 与 AnalyticDB for PostgreSQL 的跨租户漏洞群：通过共享私有容器 registry 的写权限实现供应链 RCE。

**决策（完整时间线）**
- 启动 Alibaba Cloud 研究：2022-11-01
- Alibaba 修复首个 PostgreSQL 漏洞：2022-11-12
- Wiz 报告全部漏洞：2022-12-04
- Alibaba 回复称研究期间已监控 Wiz 活动：2022-12-05
- 缓解方案讨论：2022-12-08
- Alibaba 提供 test instance 验证修复：2023-02-24
- Alibaba 部署全部缓解：2023-04-12
- 公开披露：2023-04-19
- **从报告到公开：约 135 天**；从全量缓解到公开：7 天

**PoC 公开程度（最详尽的一例）**
- **完整公开**：libgcc_s.so.1 + tsar cronjob 权限提升、共享 PID namespace + SSH LocalCommand 容器逃逸、`pg_hba.conf` 符号攻击、版本升级检查命令注入（重命名 superuser 角色为注入 payload）、`core_pattern` 覆写、kubelet 凭证列出他人 pod/secret
- 仅 redact：registry 凭证、镜像名、租户标识、access key
- 显式声明"立即停止研究、未访问他人数据"

**逻辑（推断 + 一手陈述）**
- 选 Alibaba 的理由（一手原话）：两个服务"vulnerable to similar PostgreSQL vulnerabilities and were also multi-tenant services, making them an ideal target for our research"——即延续 PostgreSQL 多厂商研究计划的下一站
- 修复后最大化公开的逻辑：**单厂商已全量缓解**、技术细节属"机制级、需特定云环境复现"而非"引擎级可移植 exploit"，公开的教育价值 > 复用风险。与 ExtraReplica 保留漏洞 #1 的逻辑互补（见 1.8 决策树）
- Alibaba 主动监控 Wiz 活动（"monitoring our activities during the research"）——厂商先于报告即已介入，披露流程透明度高于常态

**事后反思**
博文结尾"We commend Alibaba Cloud for their cooperation and responsiveness"——公开表扬厂商。这是 Wiz 披露中少见的**显式厂商表扬**，与 Hell's Keychain 中 IBM CISO Jerry Bell 反向表扬 Wiz 形成镜像。

**言行一致性**
- 最大化公开 vs ExtraReplica 最小保留：表面矛盾，底层一致（按可复用性分级，见 1.8）
- Alibaba 表扬 vs OMIGOD 中 Nir 批评 Microsoft GitHub 静默泄露：Shir 在 BrokenSesame 选择"表扬厂商"而非"批评厂商"，但这同样取决于厂商行为（Alibaba 主动监控+合作 vs Microsoft 静默泄露补丁），非 Shir 比 Nir 更温和

来源：
- https://www.wiz.io/blog/brokensesame-accidental-write-permissions-to-private-registry-allowed-potential-r [高可信 - 一手博文含完整时间线]
- 作者：Ronen Shustin, Shir Tamari, Nir Ohfeld, Sagi Tzadik, Hillai Ben-Sasson

---

### 1.4 Hugging Face（2024-04）— 协作式披露 + 产品落地

**背景**
AI-as-a-Service 平台隔离研究第一站。两个关键风险：
- 共享推理基础设施接管：上传恶意 PyTorch（Pickle）模型 → 反序列化 RCE → Amazon EKS 权限提升 → IMDS 取 Node role token → 跨租户访问他人模型
- 共享 CI/CD 接管：Hugging Face Spaces 恶意 Dockerfile RUN 指令 → 构建期执行 → 获得集中容器 registry 写权限 → 可覆写他人镜像

**决策**
- 公开披露：2024-04-04
- 向 Hugging Face 报告的确切日期：**博文未给出**（仅"works with Hugging Face on mitigations"）
- Hugging Face 修复完成日期：**博文未给出**
- 修复后即公开，无保留 PoC

**披露形态（异常：协作式而非对抗式）**
- 标题即"works with Hugging Face on mitigations"
- Hugging Face **发布配套博文**（vendor companion post）
- Hugging Face **采纳 Wiz CSPM 与漏洞扫描产品**（博文显式陈述："Hugging Face has recently implemented Wiz CSPM and vulnerability scanning"）
- Wiz 主动定位为"AI-as-a-Service 厂商伙伴"："Wiz Research partnered with AI-as-a-Service companies to uncover common security risks"

**逻辑（推断 + 一手陈述）**
- 选 Hugging Face 的理由（一手原话）：它是"the de facto open and collaborative platform for AI builders"，规模与代表性使发现"not unique to Hugging Face"而是"represent challenges of tenant separation"——即用头雁样本验证行业级假设
- 协作式披露的选择：AI 平台隔离是新兴攻击面，厂商尚无成熟的漏洞响应流程，**协作建立流程比对抗式披露更能推动行业**；同时 Hugging Face 采纳 Wiz 产品使研究直接驱动了商业关系（见 4.4 张力）

**事后反思**
无 Shir 个人层面显式反思。但"findings are not unique to Hugging Face"的表述把单点发现抽象为行业级论断，与她一贯的抽象模式一致。

**言行一致性**
- 透明度：公开承认 Hugging Face 成为 Wiz 客户——**披露了商业关系而非隐藏**，这一点与"industry must commit to transparency"（Storm-0558，见 4.3）一致
- 但也是研究纯度 vs 商业驱动最明显的交集（见 4.4）

来源：
- https://www.wiz.io/blog/wiz-and-hugging-face-address-risks-to-ai-infrastructure [高可信 - 一手博文]
- 作者：Shir Tamari, Sagi Tzadik（研究团队：Nir Ohfeld, Ronen Shustin, Hillai Ben-Sasson）

---

### 1.5 Replicate（2024-05）— 完整攻击链公开

**背景**
AI-as-a-Service 隔离研究第二站。Replicate 用自研 Cog 容器格式打包 AI 模型。Wiz 上传恶意 Cog → 容器内 root → 发现 pod 与另一容器共享网络命名空间（非 PID）→ 存在到 Redis 跨租户队列的预建 TCP 连接 → 利用 `CAP_NET_RAW`/`CAP_NET_ADMIN` + tcpdump 窥探明文 Redis 协议 → 用 `rshijack` 向已认证 TCP 会话注入包绕过 Redis 认证 → 注入 Lua 脚本 → 弹出/修改/重推他人队列项（prompt 与 prediction output 均可拦截与篡改）。

**决策**
- 报告 Replicate：2024 年 1 月
- Replicate 修复："promptly"（确切日期博文未给）
- 公开披露：2024-05-23
- **从报告到公开：约 4 个月**
- 完整攻击链公开，无保留

**逻辑（推断 + 一手陈述）**
- 选 Replicate 的理由（一手原话）："Wiz Research has conducted a series of investigations into leading AI-as-a-service providers"，Replicate 是第二站——验证"challenges of tenant separation carry across AI-as-a-service providers"假设
- 完整公开的理由：单厂商已修复、攻击链依赖特定网络拓扑与 Linux capability，不构成跨厂商可移植 exploit；教育价值在于揭示"共享网络命名空间 + CAP_NET_RAW + 持久 TCP = 跨租户数据篡改"这一**模式**
- Replicate 也发布配套博文——延续 1.4 Hugging Face 的协作模式，但商业关系未在 Replicate 案中显式陈述

**事后反思**
博文末尾"Wiz Research responsibly disclosed this vulnerability to Replicate... Replicate not only demonstrated a deep commitment to maintaining the security of its products, but also upheld the highest standards of communication and transparency"——再次显式表扬厂商。

**言行一致性**
与 BrokenSesame 一致：单厂商修复后最大化公开，按可复用性分级（见 1.8）。

来源：
- https://www.wiz.io/blog/wiz-research-discovers-critical-vulnerability-in-replicate [高可信 - 一手博文]
- 作者：Shir Tamari, Sagi Tzadik

---

### 1.6 NVIDIAScape（2025-07）— Pwn2Own 赛事渠道 + 速公开

**背景**
CVE-2025-23266，CVSS 9.0。NVIDIA Container Toolkit 的 `createContainer` OCI hook 继承容器镜像的环境变量；攻击者在容器镜像内放置 `poc.so`，通过 `LD_PRELOAD` 让以特权宿主进程运行的 `/usr/bin/nvidia-ctk` 加载恶意 .so，三行 Dockerfile 即实现容器逃逸至宿主 root：

```
FROM busybox
ENV LD_PRELOAD=/proc/self/cwd/poc.so
ADD poc.so /
```

**决策（完整时间线）**
- 通过 Pwn2Own Berlin 向 NVIDIA 提交初始漏洞报告：2025-05-17
- NVIDIA 发布安全公告并分配 CVE-2025-23266：2025-07-15
- Wiz 公开披露：2025-07-17
- **从公告到公开：2 天**

**PoC 公开程度**
- **完整公开**：三行 Dockerfile PoC、`createContainer` hook 继承环境变量的根因、CDI 模式影响范围
- 受影响版本：NVIDIA Container Toolkit ≤ v1.17.7、NVIDIA GPU Operator ≤ 25.3.1；修复版 1.17.8

**披露渠道选择（一手陈述）**
- 通过 **Pwn2Own Berlin** 提交——这是 Wiz 首次明确以赛事为披露入口的研究。赛事自带协调窗口与赏金机制，缩短了报告→公告的协调成本
- 定位为"ongoing research into the security of the AI supply chain"——延续 2024-09 已披露的 CVE-2024-0132（同 NVIDIA Container Toolkit，类似容器逃逸）的系列深挖

**逻辑（推断）**
- 选 NVIDIA Toolkit 的理由（一手原话）："The entire AI revolution is built on the power of NVIDIA GPUs"，Toolkit 是"the critical component that securely connects containerized applications to these GPUs"——即 AI 供应链的共享责任边界 + 广泛部署（云环境 35%+ 使用）
- 2 天极速公开：NVIDIA 公告已发布=风险已实质消除，立即公开让客户自查升级。与 ChaosDB 14 天、ExtraReplica 63 天的"修复→公开"窗口一致：**速度由厂商响应决定**

**事后反思**
CVE-2024-0132 与 CVE-2025-23266 同处 NVIDIA Container Toolkit，连续两个容器逃逸——博文未显式反思"为何同一组件反复出同类漏洞"，但这一连续性本身即是"AI 供应链共享责任边界未被充分审计"的论据。

**言行一致性**
- 完整公开 PoC（三行 Dockerfile）：与 BrokenSesame/Replicate 一致——单厂商已发公告、PoC 不构成跨厂商可移植 exploit（依赖特定 NVIDIA hook）
- 速公开：与"先修复后公开"原则一致

**与 Nir Ohfeld 决策记录的交叉**
Nir 的 05-decisions.md 称 NVIDIAScape 由"Nir + Ronen Shustin 署名"。一手博文核实的署名为 **Nir Ohfeld + Shir Tamari**（byline），研究团队致谢含 Sagi Tzadik、Ronen Shustin、Hillai Ben-Sasson、Andres Riancho、Yuval Avrahami。Nir 的记录略不完整——**Shir 是 byline 作者之一，非仅致谢**。

来源：
- https://www.wiz.io/blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape [高可信 - 一手博文含完整时间线与 PoC]
- 署名：Nir Ohfeld + Shir Tamari（byline）

---

### 1.7 React2Shell（2025-12）— 在野利用下的披露（无显式策略陈述）

**背景**
CVE-2025-55182，Next.js。博文副标题明示"In-the-Wild Exploitation"。攻击者对互联网暴露的 Next.js 应用及 K8s/托管云中的容器化工作负载发动机会主义攻击。

**在野攻击 TTPs（一手博文详述）**
- 凭证采集：系统性 dump npm/AWS/Docker/Git/SSH/package.json 数据，扫描环境变量匹配 `AWS`/`TOKEN`/`SECRET`/`PASS`/`DB_`
- 云元数据：访问 `169.254.169.254/latest/meta-data/iam/security-credentials/` 取 IAM 凭证
- 挖矿：多波 XMRig，含 UPX packed 变体与 GitHub 拉取的 stock XMRig，`nohup /var/tmp/crond` 持久化
- 后门：Sliver C2（64-bit ELF），TLS 证书与域名跨样本复用
- 无文件后门：覆写 `http.Server.prototype.emit`，在 `/favicon.login.ico` 建"magic path" webshell，"nearly invisible to standard log analysis"
- Node 原生 exfil：完全在 Node.js 进程内存内执行，窃 SSH key/`/etc/shadow`/bash history，绕过"alert on suspicious child process creation"的运行时安全规则

**决策**
- 公开披露（主漏洞公告）：2025-12-03
- 深度技术分析：2025-12-08
- 更新日志：2025-12-17 加 post-exploitation payloads
- **发现日期、报告 Vercel 日期、补丁发布日期：深度博文均未显式陈述**

**关键观察：在野利用但无显式策略陈述**
用户原始任务假设"在野利用，披露策略不同"。但一手深度博文**不包含**任何关于"在野利用如何改变披露时序/策略"的显式陈述。博文描述了"a rapid wave of opportunistic exploitation"、攻击者从"simple recon to hands-on-keyboard abuse"演化，但**未**讨论披露两难、未**对比**常规协调披露与在野披露的差异。

**逻辑（强推断，可信度中）**
只能从时序推断策略：主公告 12-03 紧随补丁发布（推测补丁在 12-03 前后），深度分析 12-08、payload 更新 12-17——节奏与 ExtraReplica（修复后 63 天公开）截然不同，更接近 NVIDIAScape（公告后 2 天公开）。**推断**：在野利用+已有补丁=立即公开+滚动追加技术细节，让防御者尽快自查与检测。但这是**行为推断，非博文显式陈述**。

**事后反思**
博文以攻击者 TTPs 详述为主，未对披露决策本身做元层反思。这是本文件所有披露事件中**唯一在野利用案例**，但作者选择不把它作为"披露策略反思"的载体。

**言行一致性**
- 透明度（详述攻击者 TTPs 让防御者检测）与 Storm-0558 中"industry must commit to transparency"一致
- 但**缺失**：博文未显式讨论"在野利用下研究者应否加速披露/限制 PoC 公开"这一伦理问题——与 ExtraReplica 显式陈述"abundance of caution"形成对比。可解释为：补丁已发布+攻击者已在野使用=无 PoC 保留余地，故无需讨论保留；但这是推断

来源：
- https://www.wiz.io/blog/nextjs-cve-2025-55182-react2shell-deep-dive [高可信 - 一手深度博文含 TTPs 与更新日志]
- 主公告博文 URL 未在一手页直接给出（深度博文引用"companion blog post... December 3, 2025"），[中可信 - 日期可信，URL 未独立核实]
- 作者：Shir Tamari, Gili Tikochinski, Hila Ramati, Benjamin Read

---

### 1.8 「公开多少 PoC 细节」决策树（综合推断）

从 1.1–1.7 七例可归纳 Shir（及 Wiz Research 合著团队）的 PoC 披露决策树：

| 维度 | 倾向公开（BrokenSesame/Replicate/NVIDIAScape/React2Shell） | 倾向保留（ExtraReplica 漏洞 #1） |
|---|---|---|
| 修复状态 | 单厂商全量修复/公告 | 自家修复但**他厂商可能未修** |
| 可复用性 | 机制级、需特定云环境/网络拓扑 | 引擎级、可移植到其他 CSP 修改 |
| 影响广度 | 单厂商已缓解 | 跨厂商潜在影响 |
| 教育价值 | 攻击模式可推广（如共享网络命名空间+CAP_NET_RAW） | 单点 exploit，教育价值低 |
| 敏感值 | 一律 redact（凭证/租户标识/access key） | — |

**核心原则（一手来源支持）**：以"公开后是否产生**跨厂商可移植 exploit** 打击未修复厂商"为分界。此原则在 ExtraReplica 博文以"abundance of caution with respect to other vendors"显式陈述，是本决策树唯一的一手依据；其余六例的归类为**行为模式推断，可信度中**。

**未发现** Shir 公开阐述过此决策树。这与 Nir Ohfeld 决策记录中"未发现 Nir 公开阐述过此决策树"同型——两人合著密切，共享隐含基线。

来源：
- ExtraReplica "abundance of caution" 原话：[高可信 - 一手]
- 其余六例归类：[中可信 - 行为模式推断]

---

## 2. 研究方向选择

### 2.1 跨域广度：云数据库 → 供应链 → AI（2021-2026）

**有记录的证据（按 Shir 作者页 20 篇博文时间序列）**
- **2021（云身份/倡导）**：02 月"82% of companies unknowingly give 3rd parties access to all their cloud data"（solo，云身份权限复杂度）；11 月"Security industry call to action: we need a cloud vulnerability database"（与 Alon Schindel，政策倡议）；12 月 NotLegit（Azure App Service 源码泄露，solo）
- **2022（云数据库隔离 + 供应链）**：04 月 ExtraReplica（Azure PostgreSQL）；06 月 cloud gray zone（OMIGOD follow-up，与 Nir）；08 月 PostgreSQL 多厂商（Azure+GCP，与 Ronen/Nir/Sagi）；12 月 Hell's Keychain（IBM Cloud 供应链）；12 月 secret-based cloud supply-chain 攻击案例（与 Alon Schindel）
- **2023（供应链 + 平台 + 战略分析）**：03 月 BingBang（Microsoft Bing，与 Raaz Herzberg/Hillai）；04 月 BrokenSesame（Alibaba）；07 月 GameOver(lay)（Ubuntu OverlayFS 本地提权，与 Sagi）；07 月 Storm-0558（Microsoft key 战略分析，**solo**）
- **2024（AI 转向）**：03 月 K8s LAN Party CTF（与 Nir）；04 月 Hugging Face；05 月 Replicate；09 月 NVIDIA CVE-2024-0132 首发公告（与 Ronen Shustin/Andres Riancho）
- **2025（AI 深化 + 在野利用）**：02 月 NVIDIA CVE-2024-0132 深度分析；07 月 NVIDIAScape CVE-2025-23266（与 Nir）；12 月 React2Shell CVE-2025-55182（在野利用，与 Gili/Hila/Benjamin）

**推断的动机**
1. **攻击面迁移追踪**：研究主题随"云厂商自定义修改+多租户+默认开启"的攻击面迁移——2021-22 云数据库 → 2022-23 云供应链/CI-CD → 2024-25 AI 推理基础设施。三阶段同构：均为 CSP/厂商在共享责任边界上的自定义修改引入的隔离破坏
2. **能力复用**：容器逃逸、共享命名空间、CAP_NET_RAW 滥用、imagePullSecrets → 从云数据库跨租户到 AI 容器逃逸的技术栈一脉相承
3. **市场驱动（与 Nir 决策记录交叉）**：Wiz 2024 年起推 Wiz AI Security 产品线，研究议题与产品线对齐。但**对齐方向不能反向推出"Shir 因商业驱动选 AI"**——可能 Wiz 因研究者转向 AI 而建产品线，因果未证实
4. **"头雁样本"策略**：每进入新域，先选最具代表性的平台（Hugging Face"de facto"、Replicate、NVIDIA"entire AI revolution is built on"）验证行业级假设，再深挖

**事后反思（一手陈述）**
- 2022-08 PostgreSQL 多厂商博文提出"CSP 修改 PostgreSQL 的根本矛盾"——把单点抽象为系统性论断的最早记录
- 2024-04 Hugging Face 博文"findings are not unique to Hugging Face... represent challenges of tenant separation"——AI 域的同型抽象
- 2025-07 NVIDIAScape"ongoing research into the security of the AI supply chain"——把 AI 容器逃逸定位为"基础设施安全"的延伸而非新学科

三次抽象均把单点 bug 上升为"行业级系统性论断"，这是 Shir 跨域广度的**方法论统一性**。

来源：
- https://www.wiz.io/blog/author/shir-tamari [高可信 - 20 篇博文时间序列]
- 推断动机：[中可信 - 行为模式推断，无直接陈述]

---

### 2.2 如何选下一个研究目标（行为推断）

从 2021-2026 目标序列可归纳选择标准：

1. **共享责任边界**：CSP/厂商对开源引擎/工具的自定义修改 + 多租户/共享基础设施（PostgreSQL 引擎、OMI 中间件、NVIDIA Toolkit、Cog 容器格式）
2. **默认开启/广泛部署**：Cosmos DB Notebook 默认开启、OMI 广泛部署、NVIDIA Toolkit 占云环境 35%+、Hugging Face"de facto"平台
3. **可被抽象为系统性论断**：单点 bug → "云有隔离问题" → "云有供应链问题" → "AI 有基础设施问题"
4. **修复滞后可观察性**：GitHub 提交先于官方补丁（OMIGOD 案例，Nir 主笔但 Shir 合著 cloud gray zone follow-up）
5. **延续性深挖**：ExtraReplica → PostgreSQL 多厂商 → Hell's Keychain → BrokenSesame（同 PostgreSQL 主题跨厂商）；CVE-2024-0132 → NVIDIAScape（同 NVIDIA Toolkit）

**未发现** Shir 公开阐述过此选择标准。与 Nir 决策记录同型——两人合著密切，共享隐含基线。可信度中。

---

### 2.3 与 Nir Ohfeld 的合著模式（非"Head of Research 独断"）

**有记录的证据**
Shir 作者页 20 篇博文中，**solo 仅 5 篇**（82% companies、NotLegit、Storm-0558、Black Hat 2021 DNS、 compromised Microsoft key），其余 15 篇均合著。最频繁合著者：
- **Nir Ohfeld**：ExtraReplica、cloud gray zone、PostgreSQL 多厂商、K8s LAN Party、NVIDIAScape（5 篇）
- **Ronen Shustin**：ExtraReplica、PostgreSQL 多厂商、Hell's Keychain、BrokenSesame、BingBang（间接）、NVIDIA CVE-2024-0132（5 篇）
- **Sagi Tzadik**：ExtraReplica、PostgreSQL 多厂商、GameOver(lay)、Hugging Face、Replicate（5 篇）
- **Hillai Ben-Sasson**：BrokenSesame、BingBang、NVIDIAScape 致谢（3 篇）

**推断**
研究主题选择**高度分散在合著网络中**，而非单一"Head of Research"独断：
- 数据库/PostgreSQL 系列偏 Ronen Shustin + Nir Ohfeld
- AI 系列（Hugging Face/Replicate）偏 Sagi Tzadik
- 容器逃逸/AI 供应链偏 Nir Ohfeld + Hillai Ben-Sasson
- 战略分析（Storm-0558、云漏洞数据库倡议）偏 solo 或与 Alon Schindel

**这反向支持 0.1 的修正**：若 Shir 真为"Head of Research"独断方向，solo 比例与跨域分散度应不同。实际模式更像**研究者网络按专长分工**，Shir 是其中频繁的合著节点与战略分析 solo 作者，但非"方向独断者"。

来源：
- https://www.wiz.io/blog/author/shir-tamari [高可信 - 合著网络可观察]
- 推断：[中可信 - 行为模式推断]

---

## 3. 职业决策

### 3.1 加入 Wiz 前的背景

**已证实**
- Wiz 作者页最早博文：2021-02-02"82% of companies..."——可推定她至迟在 2021 年初已是 Wiz Research 成员
- Wiz `/research` 页面将其列为 "Vulnerability Research"
- 合著网络稳定（Nir/Ronen/Sagi/Hillai），与以色列云安全圈高度重合

**未证实（必须显式标注）**
- **Unit 8200 / 军方背景**：公开可访问来源中**无任何**提及。Wiz 博文、作者页、research 团队页均无相关字段。LinkedIn HTTP 999、X HTTP 402，**均无法核实**。**未证实，不编造。**
- **是否在 Microsoft 工作过**：未在可核实来源中发现。Wiz 由前 Microsoft 安全团队创立（Ami Luttwak 等），但 Shir 个人是否来自 Microsoft **未证实**。不能从"Wiz 创始人来自 Microsoft"推断 Shir 也来自 Microsoft——这是归属谬误（Nir 决策记录已述此谬误，对 Shir 同样适用）
- **是否在其他安全公司工作过**：未证实
- **学历/母校**：未证实
- **GitHub 个人仓库**：未在一手来源中定位到 Shir 的个人 GitHub（与 Nir 有 github.com/nirohfeld 不同）——**未证实**

**为什么不能从"Wiz 创始人来自 Microsoft"或"以色列安全圈"推断 Shir 的背景**
这是常见归属谬误。Wiz 研究团队扩张后招聘了大量研究者，并非都来自 Microsoft 或军方。Shir 的来源只能由她本人的 LinkedIn/Twitter/采访证实，而这些渠道当前无法核实。

来源：
- https://www.wiz.io/research [高可信 - "Vulnerability Research"]
- https://www.wiz.io/blog/author/shir-tamari [高可信 - 最早博文 2021-02-02]
- 军方/Microsoft/学历背景：[未证实 - 无公开来源；LinkedIn/X 不可访问]

---

### 3.2 为什么选 Wiz 而非 Google Project Zero / MSRC / 竞品

**无任何 Shir 的直接陈述**记录此选择动机。以下全部为推断，可信度低-中。

**推断的动机**
1. **地理契合**：Wiz 在以色列（特拉维夫）有研究团队，Shir 合著网络高度以色列化；P0 在美国/瑞士，MSRC 主要在美国/英国
2. **研究自由度**：Wiz 是创业公司，研究目标选择比 P0（聚焦 0-click/高水平攻击）更灵活，可同时做云配置+漏洞+CTF+AI+战略分析（Shir 的 20 篇博文跨身份/数据库/供应链/AI/战略分析，正是这种自由度的体现）
3. **产品反馈闭环**：Wiz 自有云姿态扫描产品（CSPM），研究可直接驱动产品检测规则。Hugging Face 案（1.4）即研究→客户落地的闭环样本
4. **攻击面独占性**：2021 年云托管数据库隔离研究是蓝海，P0/MSRC 重心不在云配置，Wiz 给了 Shir 攻击面占位的机会

**为何不能与 Ian Beer 选 P0 的逻辑直接对比**
Beer 公开陈述过选 P0 而非卖 exploit 的伦理取舍。Shir **没有**公开陈述过类似伦理取舍。把 Shir 与 P0 做对比是用户的问题预设，但**无证据**表明 Shir 曾在 P0/MSRC/Wiz 之间做过公开选择。把"为什么选 Wiz 而非 P0"当作有记录的决策是过度解读。

来源：
- Wiz 公司信息：https://www.wiz.io/research [高可信]
- 推断动机：[低可信 - 无直接陈述]

---

## 4. 言行一致性案例

### 4.1 案例一：云漏洞数据库倡议 → OPEN CVDB 落地

**言**
2021-11-12《Security industry call to action: we need a cloud vulnerability database》（Shir Tamari + Alon Schindel）：
> "we believe we need a centralized database for reporting and enumerating cloud vulnerabilities."

核心论断：云漏洞落在 shared responsibility 的"灰色地带"，CVE 不表达"affected services、客户侧 remediation steps、谁负责什么"。以 OMIGOD 为例："Even though CVEs were issued for OMI, they did not specify which vulnerable Azure services they were linked to"；ChaosDB 与 AWS 跨账户案例仅靠 email 通知，无公开追踪、severity scoring、transparency。系统性缺口："No standardized notification channel across CSPs… No issue tracking… No severity scoring"。

倡议："We want to put forth a call to action to the security community: this is something we can improve." 提出公开标准化数据库，每条含 vuln ID、description、severity、remediation steps、detection methods，并给出 ChaosDB 样例条目。

**行**
2022-06 Wiz 推出 **OPEN CVDB**（cloudvulndb.org）——倡议**物质化**为开源数据库。Shir 是倡议作者之一，虽 OPEN CVDB 的工程归属未必全在她，但"言→行"闭环闭合。

**言行一致性评估：高一致性**
这是本文件最强的言行一致案例：从政策倡议（2021-11）到产品落地（2022-06）约 7 个月，倡议的核心条款（公开、标准化、含 remediation/detection、社区驱动）均在 OPEN CVDB 中体现。无"倡导却不行动"的缺口。

**与 Nir 决策记录的交叉**
Nir 决策记录 4.1 也以此博文创作为 CSP 透明度倡导→社区数据集的言行一致案例。Shir 与 Nir 共享该案例，因两人均深度参与 Wiz 的 CSP 透明度倡导——但**倡议博文作者为 Shir + Alon Schindel，非 Nir**。Nir 的记录把此案例归到自己名下略有溢出，本文件以一手作者页为准：**Shir 是该倡议的署名作者**。

来源：
- https://www.wiz.io/blog/security-industry-call-to-action-we-need-a-cloud-vulnerability-database [高可信 - 一手博文，Shir + Alon Schindel]
- OPEN CVDB 落地：cloudvulndb.org [高可信 - 博文显式陈述 2022-06 推出]

---

### 4.2 案例二：透明度倡议 → 自身 PoC 披露实践

**言**
- 2021-11 云漏洞数据库倡议：要求 CSP"standardized notification"、"severity scoring"、"transparency"
- 2023-07 Storm-0558："Our industry – and especially cloud service providers – must commit to a greater level of security and transparency"

**行**
- ExtraReplica：漏洞 #2 机制完整公开（正则、证书 CN 伪造、内网拓扑），仅保留可跨厂商移植的漏洞 #1 exploit 细节——**透明度最大化，受"不伤害未修复厂商"约束**
- BrokenSesame：单厂商全量修复后，完整公开 libgcc_s.so/tsar 提权、docker.sock/core_pattern 容器逃逸、kubelet 滥用的全技术细节
- Replicate：完整公开 Cog→Redis TCP 注入→Lua 脚本攻击链
- NVIDIAScape：完整公开三行 Dockerfile PoC
- React2Shell：完整公开攻击者 TTPs（凭证采集、XMRig、Sliver C2、无文件后门）供防御者检测

**言行一致性评估：高一致性，但有一个内在张力**
- 一致：她公开自身研究的最大可行透明度，实践她对 CSP 透明度的呼吁
- 张力：她对 CSP 要求"transparency"，但自身 PoC 保留（ExtraReplica 漏洞 #1）是基于"保护其他未修复厂商"——这等于**研究者保留信息也可正当化**。她未在博文中把此张力显式化（即未说"我们对自身也施加同标准：在厂商修复后透明、在未修复前保留"）。该显式化只见于 ExtraReplica 的"abundance of caution"原话，未上升为通用原则陈述

**事后反思缺口**
无 Shir 显式陈述"我如何把对 CSP 的透明度要求施加到自身披露实践"。该一致性是行为推断，非她本人陈述。

来源：
- ExtraReplica/BrokenSesame/Replicate/NVIDIAScape/React2Shell 一手博文：[高可信]
- Storm-0558 倡议原话：[高可信]
- 言行一致性：[中可信 - 行为推断，非 Shir 显式陈述]

---

### 4.3 案例三：Storm-0558 战略分析 → 身份提供者信任治理

**言**
2023-07-21《Compromised Microsoft Key: More Impactful Than We Thought》（**solo 作者**）：
> "the compromised MSA key could have allowed the threat actor to forge access tokens for multiple types of Azure Active Directory applications" — 不止 Outlook.com/Exchange Online，还包括 SharePoint/Teams/OneDrive/所有支持"login with Microsoft"的客户应用

> "Identity provider's signing keys are probably the most powerful secrets in the modern world."

> "This isn't a Microsoft specific issue, if a signing key for Google, Facebook, Okta or any other major identity provider leaks, the implications are hard to comprehend."

> "Our industry – and especially cloud service providers – must commit to a greater level of security and transparency"

**行**
- 这是**独立研究**而非转述：Shir 团队用 Wayback Machine 定位被替换的具体 key、匹配 Microsoft 公开 IOC 的 thumbprint、独立分析 Azure OpenID key discovery endpoint 与应用验证流程，确定 key 影响范围远超 Microsoft 初始披露
- 给出 6 条具体检测/缓解（更新 Azure SDK、刷新本地证书 store、按 `signinaudience` 筛查应用、按 `kid: 1LTMzakihiRla_8z2BEJVXeWMqo` 检测伪造 token、HTTP 日志比对 Microsoft 公开 IP、hunting 持久化）
- 提出"缺乏 application-specific logging 标准实践"使检测"exceedingly challenging"——把单事件抽象为**身份提供者信任治理的系统性缺口**

**言行一致性评估：高一致性**
- 战略级抽象（单事件→身份提供者信任治理）= 与云漏洞数据库倡议同型的"单点→系统性论断"模式
- 给出可操作检测命令而非空泛倡导
- **solo 作者**——这是 Shir 在战略层独立署名的最强证据，支持"战略级行为可观察"（即便"Head of Research"头衔未证实）

**与 Nir 决策记录的交叉**
Nir 决策记录未把 Storm-0558 列为其决策事件。一手作者页核实：**Storm-0558 作者是 Shir 独立，Nir 未署名**。Nir 记录未涉及此事件，符合一手来源。

来源：
- https://www.wiz.io/blog/storm-0558-compromised-microsoft-key-enables-authentication-of-countless-micr [高可信 - 一手博文，Shir solo]
- 倡议原话与检测命令：[高可信 - 一手]

---

### 4.4 张力：研究纯度 vs Wiz 商业驱动（Hugging Face 案例）

**背景**
Wiz 是云姿态扫描/CSPM 安全公司，研究议题与产品线高度相关。Shir 的研究主题序列（云配置/身份 → 云数据库 → AI 基础设施）与 Wiz 产品线演进（CSPM → Wiz AI Security）平行。

**最明显的交集：Hugging Face（1.4）**
- 协作式披露中，Hugging Face **在披露同时采纳了 Wiz CSPM 与漏洞扫描产品**（博文显式陈述）
- 即：研究→厂商成为 Wiz 客户，**研究直接驱动了商业关系**
- 博文**透明披露了这一关系**（"Hugging Face has recently implemented Wiz CSPM"），未隐藏

**言行一致性评估：透明但存在内在张力**
- 透明度上：一致——披露了商业关系，符合她对 CSP"transparency"的呼吁
- 研究纯度上：**存在张力**——研究议题选择是否受"目标厂商可能成为 Wiz 客户"驱动？Hugging Face 案中研究先于客户关系（研究是因、客户是果），但因果可被反读为"为获客而研究"
- **未发现** Shir 公开陈述过如何平衡研究纯度与商业驱动。无类似 Ian Beer"选 P0 而非卖 exploit"的伦理取舍自述

**张力是否构成言行不一致？**
- 不构成直接不一致：研究本身的技术内容（PyTorch Pickle RCE、EKS 提权、CI/CD registry 写权限）经 Hugging Face 确认与修复，未因商业关系而夸大或缩水
- 但构成**结构性张力**：Wiz 研究部的议题选择与产品线高度相关，无法从外部证实"议题选择独立于商业利益"。这是 Wiz Research 整体的结构性特征，非 Shir 个人决策

**与 Nir 决策记录的交叉**
Nir 决策记录 2.3 也指出"Wiz 在 2024 年收购腾讯云友商 Eureka、推出 Wiz AI Security，研究需匹配产品线"。两人共享此结构性张力——但**因果方向未证实**：可能是研究先行→产品跟进，也可能是产品先行→研究匹配。Shir 与 Nir 均未公开陈述此因果。

来源：
- https://www.wiz.io/blog/wiz-and-hugging-face-address-risks-to-ai-infrastructure [高可信 - 显式陈述 HF 采纳 Wiz CSPM]
- 商业驱动 vs 研究纯度因果：[未证实 - 无 Shir 直接陈述]

---

## 5. 战略层决策（"Head of Research"角色未证实下的行为证据）

鉴于 0.1 已修正"Head of Research"头衔未证实，本节不分析她"作为 Head of Research 做了哪些战略决策"，而分析**哪些战略级行为可观察、是否与"战略层角色"行为一致**。

### 5.1 战略级行为清单

| 行为 | 一手证据 | 战略层一致？ |
|---|---|---|
| 政策倡议（云漏洞数据库） | 2021-11 + Alon Schindel 博文 | 一致——行业级政策倡导 |
| 政策落地（OPEN CVDB） | 2022-06 cloudvulndb.org | 一致——倡议→产品闭环 |
| 行业事件战略分析（Storm-0558） | 2023-07 solo 博文 | 一致——独立研究+战略抽象+检测指引 |
| 跨研究域广度（身份/DB/供应链/AI） | 20 篇博文序列 | 一致——跨域而非单点 |
| 把单点抽象为系统性论断 | PostgreSQL 多厂商/Hugging Face/NVIDIAScape 三次同型抽象 | 一致——方法论统一性 |
| 跨厂商协调披露流程 | ExtraReplica/Hell's Keychain/BrokenSesame/Hugging Face/Replicate/NVIDIAScape/React2Shell 七例 | 一致——流程标准化 |

### 5.2 不能从行为反推头衔

上述行为与"战略层研究员"角色一致，但**不构成"Head of Research"头衔的证据**：
- Wiz `/research` 页面无任何领导头衔字段，Shir 与 Nir/Ronen/Sagi/Hillai 同列"Vulnerability Research"
- 战略级行为也可能是**资深研究员的常态**，非"Head of Research"独占
- Wiz 的研究战略可能由 CTO Ami Luttwak、联合创始人或研究团队集体决定，非单一"Head of Research"——**未证实**

### 5.3 她如何平衡研究纯度 vs Wiz 商业驱动

见 4.4。**无直接陈述**。可观察的是：商业关系在 Hugging Face 案中**透明披露**，未构成直接言行不一致，但**结构性张力未由她本人元层陈述**。这是本文件最重要的未决项之一。

---

## 附录：关键矛盾与未决项

### A.1 与用户原始任务的矛盾

| 用户任务陈述 | 一手来源核实结果 | 处置 |
|---|---|---|
| "Head of Research（战略层）" | Wiz `/research` 页列为 "Vulnerability Research"，无领导头衔 | 全文以"Wiz Research 成员（战略级行为可观察）"指代，不使用未证实头衔 |
| "代表作：AttachMe" | Shir 作者页 20 篇无 AttachMe；/blog/attachme 404 | 不作为 Shir 决策事件；标注为归属修正 |
| "Shir 在 X 发推披露 AttachMe" | X 不可访问（402） | 未证实，不采信 |
| "代表作：BingBang" | 一手核实为 Shir 署名（与 Raaz Herzberg/Hillai） | 保留为 Shir 事件，但 BingBang 非"漏洞披露"而是配置失误研究 |
| "代表作：Cloud Gray Zone" | 一手核实为 Shir + Nir 合著（2022-06） | 保留 |
| "代表作：React2Shell（2025-12，在野利用）" | 一手核实，2025-12-03 公告 + 12-08 深度 | 保留，但无显式披露策略陈述 |

### A.2 与 Nir Ohfeld 决策记录的交叉矛盾

| Nir 决策记录陈述 | 一手核实 | 处置 |
|---|---|---|
| BingBang 不归 Nir（修正） | 一致：BingBang = Raaz Herzberg/Hillai Ben-Sasson/Shir Tamari | 两人记录一致 |
| NVIDIAScape"Nir + Ronen Shustin 署名" | 一手 byline = **Nir Ohfeld + Shir Tamari**；Ronen 在致谢 | Nir 记录略不完整，本文件以一手为准 |
| 云漏洞数据库倡议归 Nir | 一手作者页 = **Shir Tamari + Alon Schindel** | Nir 记录溢出，本文件归 Shir |
| "Nir 公开陈述研究方向哲学" | Nir 的 zeroday.cloud 引言"Cloud and AI are reshaping the world. It's up to us to secure them together" | Shir **无**等价公开陈述——这是两人可观察差异 |

### A.3 未证实项汇总（不编造）

- Shir 的 Unit 8200/军方背景：[未证实]
- Shir 的 Microsoft 雇佣史：[未证实]
- Shir 的学历/母校：[未证实]
- Shir 的 GitHub 个人仓库：[未证实]
- "Head of Research" 头衔：[未证实]
- Shir 在 X 上的活动（含 AttachMe 推文）：[未证实 - X 不可访问]
- 研究议题选择是否受 Wiz 商业利益驱动：[未证实 - 无 Shir 直接陈述]
- 选 Wiz 而非 P0/MSRC 的动机：[未证实 - 无 Shir 直接陈述]

### A.4 工具可信度说明

- **WebFetch Wiz 一手博文**：[高可信] - 18 篇博文 URL 经作者页交叉核实，时间线/PoC 细节/作者均一手
- **WebFetch Wiz `/research` 团队页**：[高可信] - 团队名册与头衔字段一手
- **WebSearch**：[不可信] - 多次返回降级输出（否认具备搜索能力、声称"基于训练数据"摘要），与一手来源冲突者一律不采信；未与一手冲突的摘要仅作线索用，需 WebFetch 复核
- **LinkedIn/X**：[不可访问] - HTTP 999/402

---

## 文件元信息

- 调研对象：Shir Tamari（Wiz Research，"Vulnerability Research"，战略级行为可观察）
- 一手来源：18 篇 Wiz 博文（经作者页交叉核实 URL）+ Wiz `/research` 团队页 + Wiz 作者页
- 二手来源：无（WebSearch 摘要因幻觉风险不采信为二手来源）
- 黑名单已排除：知乎、微信公众号、百度百科
- 关键修正：3 项（"Head of Research"头衔未证实、AttachMe 归属修正、BrokenSesame 作者反幻觉）
- 关键言行一致案例：3 项（云漏洞数据库→OPEN CVDB、透明度倡议→PoC 实践、Storm-0558 战略分析）
- 关键张力：1 项（研究纯度 vs Wiz 商业驱动，Hugging Face 案例）
- 未证实项：8 项（见 A.3）

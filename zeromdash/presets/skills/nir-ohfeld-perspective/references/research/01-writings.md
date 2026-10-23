# Nir Ohfeld — 著作与系统性思考

> 数据来源声明：除特别标注外，本文件所有论断均来自 Wiz 官方博客原文
> (wiz.io/blog) 的直接抓取（一手），或 Wiz 博客相互引用的会议信息（一手）。
> 不使用知乎/微信公众号/百度百科。WebSearch 工具在本次调研中明显出现幻觉
> （编造 Nir 在 Black Hat 2018/2019 讲 Intel AMT，已弃用该结果）。

---

## 1. 核心研究领域（按频率与系统性排序）

### 1.1 云数据库 / 托管数据库隔离失效（主线，2021–2022）
- **ChaosDB** (Azure Cosmos DB, 2021-08/11)：通过 Jupyter Notebook 容器内
  LPE → 绕过本地防火墙 → 从 WireServer 提取内部证书 → 解密 Cosmos DB
  primary key → 以管理员身份登录 100+ 个跨 region 的 Service Fabric 实例
- **ExtraReplica** (Azure Database for PostgreSQL Flexible Server, 2022-04)：
  PostgreSQL 引擎修改导致 CREATEROLE 越权 → 通过 `pg_ident.conf` 中
  `(.*)$` 正则越界 + 伪造 SSL 客户端证书冒充 `replication` 用户 → 跨账户
  读取任意同 region 客户的 PostgreSQL 数据库
- **The Cloud Has an Isolation Problem** (2022-08)：跨厂商的系统性论证
  （GCP Cloud SQL、Azure PostgreSQL、"more than a dozen" 受影响厂商）

### 1.2 云厂商"灰色地带"中间件/Agent（2021–2022）
- **OMIGOD** (Azure OMI agent, 2021-09)：4 个 0day，CVE-2021-38647 (CVSS
  9.8) 仅靠"省略 Authorization 头"即可 root RCE
- **Secret Agent** (Azure Container Insights 中的 OMI, 2021-09)
- **The Cloud Gray Zone** (RSA Conference 2022, 2022-06)：托管云厂商在
  客户 VM 上悄悄部署的高权限 agent 集合；发布社区维护的数据集
  `github.com/wiz-sec/cloud-middleware-dataset`

### 1.3 AI 基础设施与供应链安全（2024–2026，近期主线）
- **Prompt Airlines** CTF (2024-07)：AI 聊天机器人 prompt injection 体验式 CTF
- **NVIDIAScape** (NVIDIA Container Toolkit, CVE-2025-23266, 2025-07)：
  通过 `LD_PRELOAD` 继承 + OCI `createContainer` hook 实现 container escape
- **NVIDIA Triton Inference Server** 链 (CVE-2025-23319/23320/23334,
  2025-08)：verbose error → 共享内存 API 无校验 → memory corruption → RCE
- **AI Cyber Model Arena** (2026-02)：257 道真实攻防题目的多 agent×多
  model 基准；结论："offensive capability is jointly determined" by model
  + agent scaffold
- **zeroday.cloud** Black Hat Europe 2025 比赛 (2025-09)：约 4.5M USD
  奖池，AWS/Microsoft/Google Cloud 三家共同 partner，覆盖 AI/K8s/
  container-virt/web servers/databases/DevOps 六大类的开源基础设施 0day

### 1.4 Kubernetes / 容器编排攻击面（2025）
- **IngressNightmare** (Ingress-NGINX Controller, 2025-03)：admission
  controller 不要求认证 + `nginx -t` 加载任意共享库 → unauthenticated RCE
  在 privileged pod 上，影响约 43% 云环境、6500+ 暴露集群

### 1.5 IAM 与云身份攻击面（2023）
- **Big IAM Challenge** CTF (2023-06)：6 题聚焦 AWS IAM 配置错误，
  fwd:cloudsec 2023 / AWS re:inforce 2023 现场领奖

### 1.6 CI/CD 供应链（2026）
- **CodeBreach** (AWS CodeBuild, 2026-01)：unanchored regex 让
  GitHub bot account ID 作为 trusted maintainer ID 的子串绕过 webhook
  ACTOR_ID 过滤 → 触发 privileged build → 窃取 GitHub 凭据 → 接管 AWS
  GitHub 仓库（最关键：AWS SDK for JavaScript → AWS Console 供应链）

### 1.7 CTF 与社区教育（持续）
Big IAM Challenge / Prompt Airlines / EKS Cluster Games / K8s Lan Party /
Cloud Hunting Games / zeroday.cloud —— 一致的方法论："基于真实漏洞构造
手把手 CTF"，既是教育输出也是 Wiz 的研究范围声明。

---

## 2. 重要文章列表（一手来源，Wiz 官方博客）

| 标题 | 日期 | 合作者 | 核心论点 / 关键引用 |
|------|------|--------|--------------------|
| [How We Broke the Cloud with Two Lines of Code — The Full Story of ChaosDB](https://www.wiz.io/blog/how-we-broke-the-cloud-with-two-lines-of-code-the-full-story-of-chaosdb) | 2021-11-11 | Sagi Tzadik | "with only two lines of code we were able to do what was previously thought to be impossible: **escape the abstraction layers of the cloud** to access the underlying internal Azure infrastructure." / "Because isolation was broken here, there was **no defense against this from the customers' side**." |
| [ChaosDB Explained — Azure's Cosmos DB Vulnerability Walkthrough](https://www.wiz.io/blog/chaosdb-explained-azures-cosmos-db-vulnerability-walkthrough) | 2021-11-11 | Sagi Tzadik | 技术深拆：Jupyter LPE (C# host 跑 root) → WireServer 证书 → 100+ 跨 region Service Fabric 实例 → "Service Takeover"。引用 Paul Litvak (Intezer) 之前的 WireServer 研究 |
| [ChaosDB: How We Hacked Thousands of Azure Customers' Databases](https://www.wiz.io/blog/chaosdb-how-we-hacked-thousands-of-azure-customers-databases) | 2021-08-26 | Sagi Tzadik | 通告稿。引用客户 Jim Routh (MassMutual CISO) 证言；提到 Black Hat 2021 现场演讲 |
| [OMIGOD: Critical Vulnerabilities in OMI Affecting Countless Azure Customers](https://www.wiz.io/blog/omigod-critical-vulnerabilities-in-omi-azure) | 2021-09-14 | Nir Ohfeld (主笔) + Alon Schindel (overview) | "any request without an Authorization header has its privileges default to `uid=0`, `gid=0`, which is root." / "An agent that is under the cloud provider's responsibility can easily be used by attackers to gain high privileges remotely on their target, and the **true tragedy is that customers can't even know whether they are open to this attack**." |
| [Secret Agent Exposes Azure Customers to Unauthorized Code Execution](https://www.wiz.io/blog/secret-agent-exposes-azure-customers-to-unauthorized-code-execution) | 2021-09-14 | Nir Ohfeld + Alon Schindel | "OMI is just one example of a **'secret' software agent** that's pre-installed and silently deployed in cloud environments." / 致谢 Sven Spiess 与 Tom Plant |
| [Wiz Research Discovers ExtraReplica — Cross-Account Database Vulnerability in Azure PostgreSQL](https://www.wiz.io/blog/wiz-research-discovers-extrareplica-cross-account-database-vulnerability-in-azure-postgresql) | 2022-04-29 | Ronen Shustin, Sagi Tzadik, Nir Ohfeld, Shir Tamari | "**Tenant isolation is a fundamental premise of the cloud.** Organizations trust that the cloud services they use, especially high value assets such as databases, are isolated from other customers." / "we wondered whether it might be a pattern" — 把 ChaosDB 当成同类问题模式 |
| [The Cloud Has an Isolation Problem — PostgreSQL Vulnerabilities](https://www.wiz.io/blog/the-cloud-has-an-isolation-problem-postgresql-vulnerabilities) | 2022-08-11 | Ronen Shustin, Shir Tamari, Nir Ohfeld, Sagi Tzadik | **系统性宣言**。"**Isolation is king**" (章节标题)。论点：legacy OSS (PostgreSQL) 设计早于云，CSP 必须自行打补丁 → "A seemingly minor modification can allow users to bypass the security model and elevate their privileges within the local database." / 演示同类型漏洞在 GCP、Azure 与"more than a dozen"家厂商均存在 / GCP 主动提出把 PostgreSQL hardening 上游化但 PostgreSQL 社区拒绝 |
| [The Cloud Gray Zone: Secret Agents Installed by Cloud Service Providers](https://www.wiz.io/blog/the-cloud-gray-zone-secret-agents-installed-by-cloud-service-providers) | 2022-06-09 | Nir Ohfeld + Shir Tamari | **RSA Conference 2022 演讲**。"cloud middleware"概念 + community dataset (github.com/wiz-sec/cloud-middleware-dataset)。论点：CSP 在客户 VM 上悄悄部署高权限 agent，shared responsibility 模型在此**断裂** |
| [The Big IAM Challenge](https://www.wiz.io/blog/the-big-iam-challenge) | 2023-06-06 | Nir Ohfeld (主笔) | "Identify and exploit AWS IAM misconfigurations, and learn from real-world scenarios." / 在 fwd:cloudsec 2023 与 AWS re:inforce 2023 现场发奖；引 Shir Tamari："The Big IAM Challenge represents a unique opportunity for individuals to deepen their understanding of AWS IAM configurations." |
| [Prompt Airlines — AI Security Challenge](https://www.wiz.io/blog/prompt-airlines-ai-security-challenge) | 2024-07-24 | Nir Ohfeld (主笔) | "based on real AI vulnerabilities discovered by Wiz Research." / 测试 AI 聊天机器人 prompt injection 与逻辑漏洞 |
| [NVIDIAScape — NVIDIA Container Toolkit CVE-2025-23266](https://www.wiz.io/blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape) | 2025-07-17 | Nir Ohfeld, Shir Tamari + Wiz Research Team (Sagi Tzadik, Ronen Shustin, Hillai Ben-Sasson, Andres Riancho, Yuval Avrahami) | "**containers are not a strong security barrier and should not be relied upon as the sole means of isolation**." / "the most real and immediate risk to AI applications today comes from their underlying infrastructure and tooling." / 提及 PEACH framework 与"ongoing research into the security of the AI supply chain"链：Hugging Face / Replicate / SAP AI Core (SAPwned) / Ollama (Probllama) / Alibaba (BrokensSesame) / IBM (Hell's Keychain) / DigitalOcean |
| [IngressNightmare — Ingress-NGINX Controller Vulnerabilities](https://www.wiz.io/blog/ingress-nginx-kubernetes-vulnerabilities) | 2025-03-24 | Nir Ohfeld, Ronen Shustin, Sagi Tzadik, Hillai Ben-Sasson (+ Andres Riancho) | "Admission Controllers frequently don't require authentication and essentially function as web servers" / "**containerization on its own is not a strong security boundary**" / "we learned that `nginx -t` should be considered harmful." / 致谢 Ingress-NGINX maintainer Marco Ebert |
| [NVIDIA Triton Inference Server — CVE-2025-23319 Vuln Chain to AI Server](https://www.wiz.io/blog/nvidia-triton-cve-2025-23319-vuln-chain-to-ai-server) | 2025-08-04 | Ronen Shustin, Nir Ohfeld + Wiz Research Team | "a series of seemingly minor flaws can be chained together to create a significant exploit." / shared memory API "does not check whether a provided shared memory key corresponds to a legitimate user-owned region or a private, internal one." |
| [CodeBreach — Vulnerability in AWS CodeBuild](https://www.wiz.io/blog/wiz-research-codebreach-vulnerability-aws-codebuild) | 2026-01-15 | Nir Ohfeld + Yuval Avrahami | "untrusted contributions should never trigger privileged pipelines." / "the regex patterns weren't anchored. Without the start `^` and end `$` anchors...a regex engine doesn't look for a string that perfectly matches the pattern, but one that merely _contains_ it." |
| [Introducing the AI Cyber Model Arena](https://www.wiz.io/blog/introducing-ai-cyber-model-arena-a-real-world-benchmark-for-ai-agents-in-cybersec) | 2026-02-12 | Nir Ohfeld + Alon Schindel | 257 题真实攻防 benchmark；"offensive capability is jointly determined" by model + agent scaffold；"performance is highly domain-specific" |
| [zeroday.cloud — Cloud & AI Hacking Competition](https://www.wiz.io/blog/zeroday-cloud-ai-hacking-competition) | 2025-09-30 | Nir Ohfeld (主笔) | **Black Hat Europe 2025 London, Dec 10–11**。~$4.5M 奖池。AWS/Microsoft/Google Cloud 三家 partner。"a natural extension of our mission at Wiz Research: uncover emerging threats in cloud infrastructure, share our findings, and help vendors patch vulnerabilities quickly." / "a single vulnerability in such projects can affect the entire cloud ecosystem" |

### 候补条目（在他的 author page 上但本次未深读，按低优先级列出）

| 标题 | 备注 |
|------|------|
| `omi-returns-lpe-technical-analysis` | OMIGOD 后续 LPE 技术分析 |
| `the-cloud-hunting-games-ctf-challenge` | CTF |
| `k8s-lan-party-challenge` | CTF |
| `announcing-the-eks-cluster-games` | CTF |
| `wiz-zeroday-cloud-hacking-competition-behind-the-scenes` | zeroday.cloud 幕后 |

---

## 3. 反复出现的方法论模式（出现 ≥3 次）

### 3.1 "Isolation is king / 隔离是云的根本前提"
出现于：
- ExtraReplica："Tenant isolation is a fundamental premise of the cloud"
- The Cloud Has an Isolation Problem："Isolation is king" 章节标题
- ChaosDB："Because isolation was broken here, there was no defense against this from the customers' side"
- NVIDIAScape："containers are not a strong security barrier and should not be relied upon as the sole means of isolation"
- IngressNightmare："containerization on its own is not a strong security boundary"
- CodeBreach Wiz 团队 bio："We primarily focus on finding new attack vectors in the cloud and uncovering isolation issues in cloud vendors and service providers."

→ 这是 Nir 的核心信念：把任何一层抽象（multi-tenant DB / managed agent /
  container / K8s admission controller）当作 isolation 边界都不可靠；
  必须叠加强隔离层（如虚拟化、PEACH framework）。

### 3.2 "Legacy OSS 不适合 multi-tenant 托管 → CSP 自行打补丁 → 引入漏洞"
出现于：
- The Cloud Has an Isolation Problem (PostgreSQL 主线)："these projects
  were not built with the needs of managed services in mind, so their
  adoption relies on multiple modifications and adjustments by each
  provider." / "A seemingly minor modification can allow users to bypass
  the security model"
- ExtraReplica：Azure 修改 PostgreSQL 引擎引入 CREATEROLE 越权
- ChaosDB：Cosmos DB 自带的 Jupyter Notebook feature 自动启用、客户不知情
- OMIGOD/Secret Agent：CSP 自行部署的 OMI agent 没人审计

### 3.3 "Pattern hunting — 一个洞见跨厂商复现"
出现于：
- ExtraReplica 末尾："we wondered whether it might be a pattern"
  （把 ChaosDB 当同类），随后在 2022-08 系统论证跨厂商
- The Cloud Has an Isolation Problem：明确演示同类型 PostgreSQL 漏洞在
  GCP + Azure + "more than a dozen" 厂商均存在
- NVIDIAScape：把 NVIDIA Container Toolkit 漏洞嵌入"AI 供应链研究链"
  （Hugging Face → Replicate → SAP AI Core → Ollama → NVIDIA），属于
  "AI 基础设施"维度的跨实例 pattern hunting

### 3.4 "Trust boundary 的灰色地带（云厂商/客户责任边界模糊）"
出现于：
- OMIGOD："it's unclear who is responsible for patching vulnerabilities like this"
- Secret Agent / Cloud Gray Zone："it was initially the customers'
  responsibility to update all the OMI installations" — 但客户"were not
  aware was installed in their environment"
- ChaosDB：Jupyter Notebook 自动启用 → "This was not something made
  explicit to customers"
- Cloud Gray Zone："providers install software typically without the
  customer's awareness or explicit consent"

### 3.5 "看似'安全'的旧机制被当作信任门，但实现细节绕过了它"
出现于：
- ExtraReplica：`pg_ident.conf` 的 `(.*)$` 正则 + DigiCert 签发的
  `replication.[victim].database.azure.com.[attacker-domain]` 证书 → 绕过
  SSL 客户端证书认证
- CodeBreach：unanchored regex 让 ACTOR_ID 包含关系绕过 webhook 信任列表
- IngressNightmare：admission controller 接受任意输入并喂给 `nginx -t`
  （本应只是配置校验）→ 加载共享库 RCE
- NVIDIA Triton：error message 中泄漏 shared memory key → 无校验的
  shared memory API 拿到 internal region 句柄

### 3.6 "CTF 作为研究范围声明"
反复把 CTF 用作"我们覆盖什么攻击面"的对外宣告：
- Big IAM Challenge → IAM
- Prompt Airlines → AI prompt injection
- EKS Cluster Games → K8s
- Cloud Hunting Games → 综合云
- zeroday.cloud → 把这种模式放大到全社区 + 三大 CSP partner + 真实 0day
  在开源基础设施上

### 3.7 "供应链下游放大效应"
反复把单点漏洞放到下游影响图谱里评估：
- ChaosDB → Fortune 500 客户数据库 + 100+ Service Fabric 实例
- ExtraReplica → 同 region 全部 Azure PostgreSQL Flexible Server 客户
- CodeBreach → AWS SDK for JavaScript → AWS Console → 无数下游应用与
  AWS 账户
- IngressNightmare → 43% 云环境 + 6500+ 暴露集群
- NVIDIAScape → 所有主流 CSP 的 managed AI/GPU 服务

---

## 4. 自创术语 / 命名方法论

### 4.1 命名模式：Provider + 灾难/突破 的合成词或谐音
| 术语 | 构词 | 含义 |
|------|------|------|
| **ChaosDB** | Chaos + DB | Cosmos DB 中"chain of misconfigurations"的整体命名 |
| **OMIGOD / O-MI-GOD** | OMI + OMG (Oh My God) | OMI agent 4 个 critical 漏洞的集合名；正文用"O-MI-GOD!"作为对 root cause 简单程度的惊叹 |
| **ExtraReplica** | Extra + Replica(tion) | 利用 PostgreSQL replication 协议跨账户"额外"复制他人数据库 |
| **Secret Agent** | 双关 | 既指 OMI 这种"秘密部署的 agent"，也致敬 007 特工意象 |
| **Cloud Gray Zone** | 借用"灰色地带" | CSP 与客户责任边界模糊的中间件地带 |
| **CodeBreach** | Code + Breach | AWS CodeBuild 的供应链突破 |
| **IngressNightmare** | Ingress + Nightmare | Ingress-NGINX 的链式 RCE |
| **NVIDIAScape** | NVIDIA + Escape | NVIDIA Container Toolkit 的 container escape |
| **zeroday.cloud** | 域名即品牌 | 把 CTF 直接命名成可访问的 URL |
| **Big IAM Challenge / Prompt Airlines** | 概念 + 双关 | IAM / Prompt Injection + 航空主题 |
| **AI Cyber Model Arena** | 直白命名 | 257 题基准 |

→ **方法论**：每个研究都给一个 *可被引用的代号*，让漏洞成为"事件"
   而非 CVE 编号。命名倾向：provider/pun/灾难词合成，长度 ≤ 3 单词，
   带社交媒体 hashtag。这与 Project Zero 给漏洞起名（Spectre/Meltdown/
   Foreshadow/Retbleed）的惯例一脉相承。

### 4.2 概念性框架词
- **"The cloud has an isolation problem"** —— 文章标题兼论点
- **"cloud middleware"** + **"cloud gray zone"** —— 给一类问题命名并发布
  社区数据集 (`github.com/wiz-sec/cloud-middleware-dataset`)
- **PEACH framework** —— 多次提及但本次未深读其定义；用作"strong isolation
  layer beyond containers"的指代（需进一步查证）
- **"offensive capability is jointly determined"** —— AI agent 评估的
  核心结论

---

## 5. 智识谱系线索

### 5.1 引用的外部研究者 / 项目

| 来源 | 出现位置 | 用途 |
|------|----------|------|
| **Ezequiel** (ezequiel.tech) | Cloud Has an Isolation Problem | TCP injection 技术，用于 GCP Cloud SQL container escape |
| **staaldraad** (GitHub blog) | ExtraReplica | CVE-2020-25695 PostgreSQL priv esc 写作参考 |
| **Cybertec PostgreSQL** | ExtraReplica | "abusing security definer functions" 研究 |
| **Paul Litvak (Intezer)** | ChaosDB Explained | 之前的 Azure WireServer 漏洞研究，作为先导工作被致谢 |
| **Aiven** (managed DB 厂商) | Cloud Has an Isolation Problem | 把 PostgreSQL hardening 开源的协作者 |
| **Sven Spiess, Tom Plant** | Secret Agent | 主动联系 Wiz 报告 Azure Container Insights 也受影响 |
| **Marco Ebert (gacko)** | IngressNightmare | Ingress-NGINX maintainer，修补协作 |
| **PostgreSQL 社区邮件列表** | Cloud Has an Isolation Problem | 拒绝 GCP 上游化 hardening 的对象 |
| **CISA KEV catalog** | Cloud Gray Zone | "OMI 已被在野利用"的独立证据 |
| **MSRC** (Microsoft Security Response Center) | ChaosDB / OMIGOD / ExtraReplica | 反复协调修复的厂商侧 |

### 5.2 反复合作者（Wiz Research Team 内部）

| 合作者 | 出现次数（基于本批次抓取） | 主要合作领域 |
|--------|-----------------------------|---------------|
| **Sagi Tzadik** (@sagitz_) | 5 (ChaosDB×2, ExtraReplica, Cloud Isolation, NVIDIA Triton, IngressNightmare) | 最频繁合作者；从 Cosmos DB 一路到 NVIDIA Triton |
| **Shir Tamari** (@shirtamari, Wiz Head of Research) | 4 (ExtraReplica, Cloud Isolation, Cloud Gray Zone, NVIDIAScape) | 战略层合作者；Nir 之上是 Wiz Research 的领导 |
| **Ronen Shustin** (@ronenshh) | 4 (ExtraReplica, Cloud Isolation, NVIDIA Triton, IngressNightmare) | K8s / AI infra 主线合作者 |
| **Hillai Ben-Sasson** (@hillai) | 3 (IngressNightmare, NVIDIAScape, CodeBreach) | |
| **Yuval Avrahami** (@yuvalavra) | 2 (CodeBreach, NVIDIAScape) | CI/CD 供应链合作者 |
| **Alon Schindel** | 2 (OMIGOD overview, AI Cyber Model Arena) | |
| **Andres Riancho** (@andresriancho) | 多次"team"署名 | |

→ 与 Shir Tamari 的关系特别关键：Shir 是 Wiz Research Head of Research，
  Nir 的直接上级/合作者；ExtraReplica + Cloud Gray Zone + NVIDIAScape
  三大主线作品均共享署名。

### 5.3 与其他研究者/团队的边界
- **BingBang (2023-03)** 由 Raaz Herzberg + Shir Tamari + Hillai Ben-Sasson
  署名，**Nir 不在作者列表中**——尽管外界常把 BingBang 当作 Nir 的代表作
  之一（见下方矛盾记录）。
- Wiz 内部其他研究员的 AI 供应链研究（Hugging Face、SAP AI Core / SAPwned、
  Ollama / Probllama、Alibaba / BrokensSesame、IBM / Hell's Keychain、
  Replicate、DigitalOcean）在 NVIDIAScape 文章里被引用为"ongoing research
  into the security of the AI supply chain"——但**本次未逐一核实 Nir 个人
  在这些文章上的署名**。这些研究至少属于他所在团队的连续工作。

---

## 6. 已确认的会议足迹（仅来自 Wiz 博客一手声明）

| 会议 | 时间 | 论文/演讲 | 来源 |
|------|------|-----------|------|
| **Black Hat 2021** (region 在 ChaosDB 通告稿中未指明；ExtraReplica 文章明确写 "Black Hat Europe 2021") | 2021 | ChaosDB 演讲 | ChaosDB announcement 文章："Watch our ChaosDB: How We Hacked Databases of Thousands of Azure Customers BlackHat 2021 live talk" + ExtraReplica 文章引用 "Black Hat Europe 2021" |
| **RSA Conference 2022** | 2022-06 | The Cloud Gray Zone | Cloud Gray Zone 文章末尾："delivered at RSA Conference 2022" |
| **fwd:cloudsec 2023** | 2023 | Big IAM Challenge 现场发奖 | Big IAM Challenge 文章 |
| **AWS re:inforce 2023** | 2023 | Big IAM Challenge 现场发奖 | Big IAM Challenge 文章 |
| **Black Hat Europe 2025** (London, Dec 10–11) | 2025-12 | zeroday.cloud 比赛（约 4.5M USD 奖池，AWS/MS/Google partner） | zeroday.cloud 文章 |

**未确认的会议足迹**：本次调研无法直接访问 blackhat.com 议程页（HTTP 403）。
WebSearch 返回的"Nir Ohfeld Black Hat 2018/2019 Intel AMT"信息判定为模型
幻觉（在 Wiz 博客、NVD、Wiz 作者页均无对应证据），**不采信**。

---

## 7. 矛盾 / 未确认记录

1. **BingBang 归属错误（强烈冲突）**：
   - 用户线索把 BingBang 列为 Nir 的代表作。
   - 一手证据：`wiz.io/blog/bingbang` (2023-03-29) 的 og:author 元标签是
     `raaz-herzberg` 与 `shir-tamari`（还包括 Hillai Ben-Sasson），
     **Nir Ohfeld 不在 BingBang 作者列表中**。
   - 结论：BingBang 是 Shir Tamari 与 Raaz Herzberg 的作品，不属于 Nir
     的研究线。外界（包括用户的线索）常把它误归 Nir，是因为 Wiz 团队
     的署名经常集体出现、且 Shir 与 Nir 长期合作。

2. **Azure Health Bot Service 漏洞研究**：
   - 用户线索提到 Nir 研究 Azure Health Bot Service。
   - 本次在 Nir 的 Wiz 作者页 (`/authors/nir-ohfeld`) 上**未找到**
     Azure Health Bot 相关博客。
   - 也未在 Wiz `/blog/tag/research` 列表上看到该主题。
   - **信息不足**：要么该研究未在 Wiz 博客发表、要么使用了其他名称、
     要么 Nir 并非作者。本次调研**无法确认**其存在与归属。

3. **PEACH framework**：Nir 在 NVIDIAScape 等文章中提到，作为"strong
   isolation layer beyond containers"的指代，但**本次未核实 PEACH 的具体
   定义/出处**（可能来自 fwd:cloudsec 演讲或 Wiz 内部白皮书）。

4. **Nir 在 AI 供应链研究线上的个人贡献边界**：
   - NVIDIAScape 与 NVIDIA Triton 文章明确 Nir 为署名作者。
   - 但团队被点名为"ongoing research into the security of the AI supply
     chain"的 Hugging Face / SAPwned / Probllama / BrokensSesame /
     Hell's Keychain 等研究，**Nir 的个人署名未逐篇核实**。
   - 推断：这些至少是其所在 Wiz Research 团队的连续工作；Nir 是该团队
     的核心成员但未必是每篇的主笔。**标注为推断，非确认**。

5. **Black Hat 2021 vs Black Hat Europe 2021**：
   - ChaosDB 通告文章只说 "BlackHat 2021 live talk" 未指明 region。
   - ExtraReplica 文章明确把 ChaosDB 演讲定位在 "Black Hat Europe 2021"。
   - 推断一致：即 Black Hat Europe 2021。

6. **MSRC 排名**：Big IAM Challenge 文章 (2023-06) 中提到 Nir 在 MSRC
   2021 Q3 Researcher Leaderboard 排名第 3。**未独立到 MSRC 官网核实**，
   但属 Wiz 一手自述。

7. **Twitter / X**：Wiz 博客一致使用 `@nirohfeld`。**未直接访问 X 个人
   页面核实 bio**。

---

## 8. 来源可信度小结

| 来源类型 | 数量 | 备注 |
|----------|------|------|
| **一手 — Wiz 官方博客原文** (wiz.io/blog) | 14 | ChaosDB×3、OMIGOD、Secret Agent、ExtraReplica、Cloud Isolation、Cloud Gray Zone、Big IAM、Prompt Airlines、NVIDIAScape、IngressNightmare、NVIDIA Triton、CodeBreach、AI Cyber Model Arena、zeroday.cloud |
| **一手 — Wiz 博客互引的会议声明** | 5 条会议足迹 | Black Hat 2021/Europe 2021、RSA 2022、fwd:cloudsec 2023、AWS re:inforce 2023、Black Hat Europe 2025 |
| **一手 — Wiz 作者页元数据** (og:author / 作者 bio) | 14 篇文章的 og:author 标签 + 1 个作者页 (`/authors/nir-ohfeld`) | 用于核实每篇文章的实际署名 |
| **一手 — Wiz GitHub 仓库** | 1 | `github.com/wiz-sec/cloud-middleware-dataset` (在 Cloud Gray Zone 文章中链接) |
| **二手 — 外部致谢/客户证言** | 3 | Jim Routh (MassMutual CISO)、Sven Spiess、Tom Plant — 均在 Wiz 一手文章里被引用 |
| **二手 — NVD / GHSA 直接核实** | 0 | NVD REST API 在本次调研中受 Cloudflare challenge 拦截，未能直接取数；CVE 编号均来自 Wiz 博客自述 |
| **二手 — 黑名单 / 已弃用来源** | 0 | 不使用知乎、微信公众号、百度百科；WebSearch 工具对 Nir 名字返回幻觉结果，整体不采信 |
| **未确认 / 信息不足** | 4 项 | Azure Health Bot 研究、PEACH framework 定义、AI 供应链各子研究 Nir 个人署名、Black Hat 议程直接核实 |

**总体可信度**：本文件中标注为"他说"的论断几乎全部来自 Wiz 官方博客
原文抓取（一手）；少量"别人说他说的"在矛盾记录中已明确隔离并指出
（特别是 BingBang 误归）。**未做任何调和**——BingBang 不属于 Nir 的
作品这一事实直接保留，与用户原始线索冲突亦不掩盖。


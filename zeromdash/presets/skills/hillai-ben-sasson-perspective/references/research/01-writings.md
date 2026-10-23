# Hillai Ben-Sasson — 著作与系统性思考

> 调研日期：2026-07-26
> 主体：Hillai Ben-Sasson，Wiz Research 安全研究员，X handle @hillai
> 调研方法：以 Wiz 官方博客作者页（一手署名）+ 逐篇 og:author/byline 元数据核实为主；WebSearch 因在 Nir 调研中已出现幻觉（"Amit Ohfeld" 等错误名字），本调研不采信未核实结果。
> 重要区分：Wiz 博客有两种署名机制——(A) **byline（公开列名作者，写了文章的人）**，(B) 文末 "Stay in touch!" / "Wiz Research Team" **研究团队致谢（参与研究但未主笔文章）**。本文件严格区分二者，因为后者不能代表 Hillai 的"著作"与"声音"。

---

## 0. 一手核实的署名作品清单（bylined，按时间倒序）

以下 4 篇为 Wiz 博客 byline 中明确出现 Hillai Ben-Sasson 的文章，全部经直接抓取博客原文核实：

| 日期 | 标题 | Hillai 在 byline 中的位置 | 共同 byline 作者 | URL |
|------|------|---------------------------|-------------------|-----|
| 2025-03-24 | IngressNightmare: CVE-2025-1974 - 9.8 Critical Unauthenticated RCE Vulnerabilities in Ingress NGINX | **第 4 / 4** | Nir Ohfeld, Ronen Shustin, Sagi Tzadik | https://www.wiz.io/blog/ingress-nginx-kubernetes-vulnerabilities |
| 2024-07-17 | SAPwned: SAP AI vulnerabilities expose customers' cloud environments and private AI artifacts | **唯一 byline（独立署名）** | —（文末 research team 列 Shir Tamari / Nir Ohfeld / Sagi Tzadik / Ronen Shustin，但他们不是 byline 作者） | https://www.wiz.io/blog/sapwned-sap-ai-vulnerabilities-ai-security |
| 2023-09-18 | 38TB of data accidentally exposed by Microsoft AI researchers | **第 1 / 2（主笔）** | Ronny Greenberg | https://www.wiz.io/blog/38-terabytes-of-private-data-accidentally-exposed-by-microsoft-ai-researchers |
| 2023-03-29 | BingBang: How a simple developer mistake could have led to Bing.com takeover | **第 3 / 3** | Raaz Herzberg, Shir Tamari | https://www.wiz.io/blog/bingbang |

来源：Wiz 博客作者页 https://www.wiz.io/blog/author/hillai-ben-sasson （列出完整 5 条 byline 条目，含 BingBang 的另一 URL 变体 `/blog/azure-active-directory-bing-misconfiguration`）。可信度：**一手**。

**关键观察**：Hillai 在 Wiz 的 **byline 总数仅 4 篇**，远少于 Nir Ohfeld（21 篇 byline）。他的"声音"样本量有限，其中最纯粹代表他个人思路的是 **SAPwned（唯一独立署名）** 和 **38TB Microsoft AI（主笔）** 两篇。

---

## 1. 对既有线索的重要更正（任务描述中的不准确之处）

任务给出的线索把多篇作品归为 Hillai "合著"，但一手 byline 核实推翻了其中两条。务必记录矛盾，不要调和：

### 更正 1：NVIDIAScape（CVE-2025-23266，2025-07-17）—— Hillai **不是** byline 作者

- **byline 作者**：Nir Ohfeld、Shir Tamari（仅此二人）
- Hillai 出现在文末 "Wiz Research Team" 致谢，列 **第 4 / 6**（Nir、Sagi、Ronen、**Hillai**、Andres Riancho、Yuval Avrahami）
- 来源：https://www.wiz.io/blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape （一手）
- 任务线索称其"合著（与 Nir Ohfeld 等）"——**不准确**。他参与了研究，但没写公开文章。

### 更正 2：CodeBreach（AWS CodeBuild，2026-01-15）—— Hillai **不是** byline 作者

- **byline 作者**：Yuval Avrahami、Nir Ohfeld（仅此二人）
- Hillai 出现在 "Stay in touch!" 致谢，列 **第 4 / 5**
- 来源：https://www.wiz.io/blog/wiz-research-codebreach-vulnerability-aws-codebuild （一手）
- 任务线索称其"合著"——**不准确**。同上，研究团队 ≠ 文章作者。

### 更正 3：NVIDIA Triton（CVE-2025-23319，2025-08-04）—— Hillai **不是** byline 作者（线索未提及但相关）

- **byline 作者**：Ronen Shustin、Nir Ohfeld
- Hillai 在文末研究团队致谢中（@hillai）
- 来源：https://www.wiz.io/blog/nvidia-triton-cve-2025-23319-vuln-chain-to-ai-server （一手）

### 推论

Wiz 的命名规律是：**公开 byline 只列写文章的人（通常 1-2 人）**，"Stay in touch!" / "Wiz Research Team" 致谢列全部研究贡献者（通常 5-6 人）。Hillai 在大量重大 AI 基础设施研究中是**研究贡献者**，但很少是**公开文章主笔**。这直接影响"系统性思考"的可观测性——他的个人思路主要只能从那 4 篇 byline 文章推断，尤其 SAPwned 和 38TB 两篇。

---

## 2. SAPwned 深读（独立署名，Hillai 个人思路最纯粹样本）

来源：https://www.wiz.io/blog/sapwned-sap-ai-vulnerabilities-ai-security （一手，他本人写的）。以下引述均出自该文。

### 2.1 核心论点（root cause framing）

中心论点：**AI 服务天生对租户隔离失败敏感，因为"允许用户运行 AI 模型与应用 = 执行任意代码"是这类服务的定义性特征。**

> "We believe these services are more susceptible to tenant isolation vulnerabilities, since by definition, they allow users to run AI models and applications – which is equivalent to executing arbitrary code."
> "appropriate guardrails should be in place to assure that untrusted code is properly separated."

这是一条**结构性、跨厂商**的论断，不是 SAP 单点 bug。Hillai 把 SAPwned 定位为 Wiz AI 基础设施隔离系列的第 3 篇报告（前两篇是 Hugging Face、Replicate），明确把单点发现上升为行业级 pattern。

### 2.2 攻击链与 root cause 层次

攻击链（编号 bug #1→#5，递进式）：
1. SAP AI Core 让客户提供 Argo Workflow 文件 → spawn Kubernetes Pod
2. admission controller 未阻断 `shareProcessNamespace` 和 `runAsUser` 配置 → 绕过 Istio sidecar 网络隔离
3. 内网被当作可信域：Grafana Loki（无认证，泄漏 AWS S3 凭证）、EFS 共享（泄漏客户 AI 数据）、Helm/Tiller server（泄漏 Docker registry / Artifactory / GCR 凭证）全部未认证
4. 部署恶意 Helm 包 → 拿到 `cluster-admin`
5. 明文读取客户 secrets

root cause 分两层：
- **第一层**：admission controller 缺陷（控制面）
- **第二层**（更被 Hillai 强调）：**网络隔离被当作唯一边界，一旦绕过，内部服务完全裸奔**：
  > "the internal network was perceived as trusted. Hardening those internal services could have minimized the impact."

### 2.3 反复出现的核心论点（≥3 次的"信念"）

从 SAPwned + 38TB 两篇主笔文章交叉看，以下论点出现 ≥3 次：

1. **"AI 服务 = 任意代码执行，因此租户隔离是结构性难题"** — SAPwned 直接断言；38TB 用 pickle 模型 RCE 佐证；研究团队致谢中他出现的 NVIDIAScape / NVIDIA Triton / Hugging Face / CodeBreach 全部围绕 AI runtime 任意代码执行问题。
2. **网络隔离不是可靠边界，绕过它就暴露扁平无认证内网** — SAPwned 的 Istio 绕过 + Loki/EFS/Helm 全无认证；38TB 的 SAS token 一旦过度授权就不可收回。
3. **共享基础设施信任模型失败** — SAPwned 内部服务互信；38TB "no way for an administrator to know this token exists"。
4. **供应链风险路径**：通过容器镜像/模型权重投毒横向影响所有客户 — SAPwned 的 Docker registry/Artifactory 写权限；38TB 的 pickle 模型注入：
   > "an attacker could have injected malicious code into all the AI models in this storage account"（38TB）
5. **K8s 控制面/数据面边界被架构性打通** — SAPwned：
   > "the crucial separation between the control plane (service logic) and the data plane (customer compute) is being impacted by the K8s architecture, which allows logical connections between them through APIs, identities, shared compute."
6. **过度授权/oversharing 是默认失败模式** — 38TB：SAS token "full control permissions, on the entire account, forever"；SAPwned：admission controller 默认放行。

### 2.4 命名方法论

"SAPwned" = **SAP + pwned**（厂商名嵌入黑客俚语 pwn）。这是 Wiz 品牌化命名传统的一部分（ChaosDB、OMIGOD、ExtraReplica、BrokenSesame、BingBang、NVIDIAScape、IngressNightmare、CodeBreach 等同系列）。Hillai 在 SAPwned 中独立命名；BingBang 是与 Raaz Herzberg、Shir Tamari 三人共命名。

命名风格特征：**厂商名 + 双关/安全隐喻**，便于传播与记忆。SAPwned 同时承担"系列第 3 篇"的定位功能——把单点 CVE 包装成跨厂商研究纲领的品牌资产。

### 2.5 智识谱系（他引用的 prior art / 研究者）

- **自家团队前作**：Wiz 的 Hugging Face 研究（https://www.wiz.io/blog/wiz-and-hugging-face-address-risks-to-ai-infrastructure ）与 Replicate 研究（https://www.wiz.io/blog/wiz-research-discovers-critical-vulnerability-in-replicate ）——SAPwned 自称"our 3rd report in the series"。
- **Black Hat 演讲**："Isolation or Hallucination? Hacking AI Infrastructure Providers for Fun and Weights"（SAPwned 文中预告）。**注**：blackhat.com 议程页对 WebFetch 返回 403，无法独立核实演讲者名单与日期；但该演讲被 Hillai 本人文章引用，故可信度=一手自引，议程细节未核实。
- **Istio 官方文档**（istio.io analysis ist0144）——技术论据。
- **SAP 安全致谢页**——披露闭环证据。
- **fwd:cloudsec 2023**（38TB 文中引用其会议演讲）。
- **Hugging Face 官方文档**（pickle 序列化安全风险）。
- **Microsoft 安全博客**（SAS token 作为 backdoor 的官方描述）。

### 2.6 表达 DNA（写作结构 / 修辞）

- **结构**：thesis → executive summary（bullet）→ origin story（"Our research began as an SAP customer"，从客户视角起手建立攻击者视角）→ 编号 bug 链 #1–#5（每条：发现→利用→影响，递进升级）→ takeaways → 披露时间线 → 联系方式
- **人称**：研究过程用 "we"（团队成果归功团队），论点用 "we believe"
- **语气**：技术精确性与通俗叙事混合；黑客文化幽默（Istio UID "ironically enough... 1337 (yeah, really)"）
- **叙事弧**：逐级升级，culminating 在 "We were now running with full privileges on the cluster!"
- **方法论自指**：披露时间线中包含 "Wiz Research bypasses the patch using 2 new vulnerabilities"——展示迭代研究方法论（patch bypass 作为研究质量证据）

---

## 3. 38TB Microsoft AI 深读（主笔，与 Ronny Greenberg 合著）

来源：https://www.wiz.io/blog/38-terabytes-of-private-data-accidentally-exposed-by-microsoft-ai-researchers （一手）。

### 3.1 核心论点

**Account SAS token 天生危险**：客户端创建、不可 centrally 追踪、不可单独吊销、易被配置过度授权。Microsoft 的单 token 错配 → 38TB 私有数据（含 secrets / 私钥 / 密码 / 30,000+ Teams 内部消息）暴露。

> "Account SAS tokens... should be considered as sensitive as the account key itself."

修复建议：改用 Service SAS + Stored Access Policies、User Delegation SAS（≤7 天）、或禁用 SAS。

### 3.2 主题（与 SAPwned 交叉点）

- **过度授权 = 默认失败模式**（重复点 4）
- **供应链投毒路径**（pickle 模型 RCE → 注入所有客户模型）（重复点 3）
- **缺 centralized governance**（token "not an Azure object"，管理员不可见）（重复点 2 的变体：可见性失败）
- **AI pipeline 安全**需要额外 safeguard（重复点 1 的延伸）
- **非过期 token**（Microsoft 的 token "valid until 2051"）

### 3.3 与 SAPwned 的差异

- SAPwned 是**主动攻击链**（多 bug 串联 → cluster-admin）；38TB 是**被动暴露**（单点错配 → 数据泄漏）。两者互补，共同构成 Hillai "AI 基础设施既有主动隔离失败也有被动数据暴露"的双面论断。
- SAPwned 强调 K8s/网络隔离；38TB 强调 storage/identity token 治理。两者共同指向"AI 服务栈每一层都可能成为失败点"。

### 3.4 命名

38TB 这篇**无品牌化 codename**（不像 SAPwned / BingBang）。命名风格为描述性事件标题。这本身是个信号：Hillai 的命名策略选择性使用——当研究可包装成跨厂商系列时用 codename（SAPwned），当是单点事件披露时用描述性标题（38TB）。

---

## 4. BingBang（第 3 作者，2023-03-29）

来源：https://www.wiz.io/blog/bingbang （一手）。

- byline 顺序：Raaz Herzberg、Shir Tamari、Hillai Ben-Sasson（第 3/3）
- 漏洞：Azure AD 多租户 misconfiguration（Bing Trivia 应用）→ 未授权访问 Bing CMS → 操纵搜索结果 + 窃取 O365 凭证（XSS）
- 命名：BingBang = Bing + Bang（厂商名 + 双关，同 SAPwned 命名法）
- 主题：**身份 provider（AAD）多租户信任边界失败**——这条线索在 SAPwned（AWS/Azure 凭证泄漏）和 38TB（SAS token 治理）中反复出现，构成 Hillai 的第三个反复论点：**identity/secret 治理是 AI/云服务栈的隐性攻击面**。

注：任务线索确认 BingBang "不是 Nir 作品"，经核实属实——Nir 不在 byline 也不在文末致谢。这是 Hillai（+ Raaz + Shir）的作品。

---

## 5. IngressNightmare（第 4 作者，2025-03-24）

来源：https://www.wiz.io/blog/ingress-nginx-kubernetes-vulnerabilities （一手）。

- byline 顺序：Nir Ohfeld、Ronen Shustin、Sagi Tzadik、Hillai Ben-Sasson（第 4/4）
- 漏洞：CVE-2025-1974（CVSS 9.8 unauthenticated RCE）+ CVE-2025-1097/1098/24514，Ingress NGINX Controller for Kubernetes
- 主题：**Kubernetes 控制面 RCE**——与 SAPwned 的 K8s admission/controller 主题一致。这是 Hillai 唯一 byline 的纯 Kubernetes（非 AI）研究。
- 注：该研究的"声音"更偏 Nir/Ronen（前两位 byline），Hillai 作为第 4 作者的个人贡献难以从公开文章分离。

---

## 6. AI 供应链研究链——Hillai 在各篇中的角色核实

任务线索列出一条 AI 供应链研究链（Hugging Face / Replicate / SAP AI Core(SAPwned) / Ollama(Probllama) / Alibaba(BrokenSesame) / IBM(Hell's Keychain) / DigitalOcean），要求逐一核实 Hillai 署名。结果如下：

| 厂商 / 研究 | Wiz 博文日期 | byline 作者 | Hillai 角色 | 来源 |
|------------|-------------|-------------|-------------|------|
| **SAP AI Core / SAPwned** | 2024-07-17 | **Hillai Ben-Sasson（唯一）** | **byline 主笔 ✓** | https://www.wiz.io/blog/sapwned-sap-ai-vulnerabilities-ai-security |
| **Microsoft AI / 38TB** | 2023-09-18 | **Hillai Ben-Sasson、Ronny Greenberg** | **byline 主笔(第1) ✓** | https://www.wiz.io/blog/38-terabytes-of-private-data-accidentally-exposed-by-microsoft-ai-researchers |
| **Hugging Face** | 2024-04-04 | Shir Tamari、Sagi Tzadik | 研究团队致谢(第5/5)，**非 byline** | https://www.wiz.io/blog/wiz-and-hugging-face-address-risks-to-ai-infrastructure |
| **Replicate** | 2024-05-23 | Shir Tamari、Sagi Tzadik | **未出现**（无文末致谢段） | https://www.wiz.io/blog/wiz-research-discovers-critical-vulnerability-in-replicate |
| **Alibaba / BrokenSesame** | 2023-04-19 | （未抓取 byline，Shir Tamari 作者页列出） | 未核实 | https://www.wiz.io/blog/brokensesame-accidental-write-permissions-to-private-registry-allowed-potential-r |
| **IBM / Hell's Keychain** | 2022-12-01 | （未抓取 byline，Shir Tamari 作者页列出） | 未核实 | https://www.wiz.io/blog/hells-keychain-supply-chain-attack-in-ibm-cloud-databases-for-postgresql |
| **NVIDIA / NVIDIAScape (CVE-2025-23266)** | 2025-07-17 | Nir Ohfeld、Shir Tamari | 研究团队致谢(第4/6)，**非 byline** | https://www.wiz.io/blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape |
| **NVIDIA / Triton (CVE-2025-23319)** | 2025-08-04 | Ronen Shustin、Nir Ohfeld | 研究团队致谢，**非 byline** | https://www.wiz.io/blog/nvidia-triton-cve-2025-23319-vuln-chain-to-ai-server |
| **AWS CodeBuild / CodeBreach** | 2026-01-15 | Yuval Avrahami、Nir Ohfeld | 研究团队致谢(第4/5)，**非 byline** | https://www.wiz.io/blog/wiz-research-codebreach-vulnerability-aws-codebuild |
| **Ollama / Probllama** | — | — | **未在 Wiz 博客找到**（Nir/Shir 作者页均无） | 未核实，线索存疑 |
| **DigitalOcean** | — | — | **未在 Wiz 博客找到**（Nir/Shir 作者页均无） | 未核实，线索存疑 |

**关键发现**：
1. SAPwned 是 Hillai 在这条研究链中**唯一独立署名**的研究（38TB 是主笔但属 Microsoft 而非 AI-as-a-service 厂商链）。
2. 在 Hugging Face、NVIDIAScape、NVIDIA Triton、CodeBreach 等重大 AI 供应链研究中，Hillai 是**研究团队贡献者但非公开文章作者**——他的个人思路不可从这些文章直接观察。
3. **Ollama(Probllama) 与 DigitalOcean 未在 Wiz 博客 Nir/Shir 作者页或主博客列表中找到**。这两个条目可能是来自其他研究团队或不存在，需用户提供来源核实。诚实标注：信息不足。

---

## 7. 会议演讲（部分未核实）

| 演讲 | 会议 | 状态 | 来源 |
|------|------|------|------|
| **"Isolation or Hallucination? Hacking AI Infrastructure Providers for Fun and Weights"** | Black Hat（SAPwned 文中预告，年份推断 2024） | **一手自引**（SAPwned 文中引用），但 blackhat.com 议程页对 WebFetch 返回 403，**议程细节/演讲者名单/日期未独立核实** | https://www.wiz.io/blog/sapwned-sap-ai-vulnerabilities-ai-security |
| **Mish-Mesh: service mesh 滥用** | KubeCon 2025（线索称） | **未核实**。sched.com（kccnceu2025 / kccncna2025）返回 402/403；Wiz 博客主列表无 Mish-Mench 文章；CNCF 议程页 password-protected。线索无一手证据支撑 | 无一手来源 |
| **NVIDIAScape 跨三家云原生 AI 服务** | KubeCon 2025（线索称） | **未核实**，同上 | 无一手来源 |
| **38TB finding** | fwd:cloudsec 2023 | 一手自引（38TB 文中提及 fwd:cloudsec talk） | https://www.wiz.io/blog/38-terabytes-of-private-data-accidentally-exposed-by-microsoft-ai-researchers |

诚实标注：KubeCon "Mish-Mesh" 演讲在任务线索中被列为 Hillai 的代表作，但本调研**未找到任何一手证据**（Wiz 博客无此文章、sched 议程不可访问、CNCF 官方议程加密）。该条目暂标为**信息不足/未核实**，不写入确定性结论。

---

## 8. 与 Nir Ohfeld 的研究焦点差异（基于本调研一手数据）

来源对照：Nir Ohfeld 现有 perspective skill（/Users/bytedance/Projects/Security/OssVulnAnalogy-AgentTeam/.claude/skills/nir-ohfeld-perspective/SKILL.md ，基于 21 篇 byline 文章）vs Hillai 本调研（4 篇 byline 文章）。

| 维度 | Nir Ohfeld | Hillai Ben-Sasson |
|------|------------|-------------------|
| **byline 总数** | 21 篇（2021-2026） | 4 篇（2023-2025） |
| **核心 mental model** | "Isolation is king"——租户隔离为中心 | "AI 服务 = 任意代码执行，因此隔离结构性难"——AI-specific 框架 |
| **拥有 byline 的研究线** | (a) 云数据库隔离链：ChaosDB / ExtraReplica / PostgreSQL / OMI；(b) cloud gray zone / secret agent：OMIGOD / Secret Agent；(c) AI 基础设施：NVIDIAScape / NVIDIA Triton / CodeBreach；(d) K8s：IngressNightmare | (a) AI 服务隔离：SAPwned（独立）/ 38TB（主笔）；(b) 身份/AAD misconfig：BingBang（第3）；(c) K8s ingress：IngressNightmare（第4） |
| **Nir 有而 Hillai 无 byline 的线** | — | **云数据库隔离链（ChaosDB/ExtraReplica）+ cloud gray zone（OMIGOD/Secret Agent）完全无 Hillai byline**——这两条是 Nir 的招牌，Hillai 不参与 |
| **Hillai 有而 Nir 无 byline 的线** | — | **SAP AI Core（SAPwned 独立署名）+ 38TB Microsoft AI（主笔）+ BingBang（Nir 不在 byline 也不在致谢）** |
| **AI 供应链研究链 byline 占比** | 高（NVIDIAScape / NVIDIA Triton / CodeBreach 均 byline） | 低（仅 SAPwned 独立 + 38TB 主笔；其余 NVIDIAScape/Triton/CodeBreach/Hugging Face 均仅研究团队致谢） |
| **命名代表作** | ChaosDB / OMIGOD / ExtraReplica / IngressNightmare / NVIDIAScape / CodeBreach | SAPwned / BingBang（共命名） |

**核心差异结论（基于一手 byline，非推断）**：
1. **Nir 是 Wiz 公开声音的主力**（21 vs 4），其"声音"覆盖云数据库隔离 + gray zone + AI 基础设施三条主线。
2. **Hillai 不是"AI 安全主笔人"**——NIR 才是 AI 基础设施 byline 的主力（NVIDIAScape/Triton/CodeBreach）。任务线索"他更偏 AI 安全"的部分需修正：Hillai 的**独立/主笔署名**确实集中在 AI（SAPwned + 38TB），但他在 Wiz 整个 AI 供应链研究链中**更多是研究团队贡献者而非公开作者**。
3. **Hillai 独有的 byline 阵地**：SAP AI Core（SAPwned）与 Microsoft AI 38TB——这两个是 Nir 未 byline 的，是 Hillai 真正的"个人招牌"。
4. **Hillai 独有的非 Nir 阵地**：身份/AAD misconfig（BingBang）——Nir 不在 BingBang byline 也不在致谢，这是 Hillai + Raaz + Shir 三人作品。
5. **"service mesh"标签**未在一手 byline 中得到支撑：Hillai 唯一的 K8s byline 是 IngressNightmare（Ingress NGINX 是 ingress controller，不是 service mesh）。Mish-Mesh 演讲未核实。诚实标注：service mesh 方向**信息不足**。

---

## 9. 未核实 / 信息不足维度（诚实标注）

- **KubeCon 2025 Mish-Mesh 演讲**：sched.com / CNCF 议程页均不可访问（402/403/密码保护），Wiz 博客无相关文章。**未找到一手证据**。
- **KubeCon 2025 NVIDIAScape 跨三家云原生 AI 服务演讲**：同上，未核实。
- **Black Hat "Isolation or Hallucination" 演讲**：被 SAPwned 文中自引（一手自引），但议程页 403，演讲者完整名单与同台 speaker 未核实。
- **Ollama / Probllama**：Wiz 博客 Nir/Shir 作者页与主列表均无。线索存疑。
- **DigitalOcean**：同上，未在 Wiz 博客找到。线索存疑。
- **Alibaba / BrokenSesame byline**：未抓取 byline 详情，Hillai 是否在 byline 或致谢未核实。
- **IBM / Hell's Keychain byline**：同上未核实。
- **Hillai 的个人信息**（入职时间、教育背景、性别、职位 title）：Wiz 博客未公开；X profile（x.com/hillai）对 WebFetch 返回 402，未获取。本文件不做任何此类断言。
- **SAPwned 与 Black Hat 演讲的精确年份对应**：推断为 2024（SAPwned 2024-07 发布，文中"upcoming"Black Hat），但未独立核实具体是 Black Hat USA 2024 哪场。

---

## 来源可信度小结

| 来源 | 类型 | 可信度 | 用于 |
|------|------|--------|------|
| https://www.wiz.io/blog/author/hillai-ben-sasson | Wiz 官方作者页 | 一手 | 确认 byline 总清单（5 条含 BingBang 双 URL 变体） |
| https://www.wiz.io/blog/sapwned-sap-ai-vulnerabilities-ai-security | Hillai 独立署名文章 | 一手（他本人写） | 深读核心论点、命名、智识谱系、表达 DNA |
| https://www.wiz.io/blog/38-terabytes-of-private-data-accidentally-exposed-by-microsoft-ai-researchers | Hillai 主笔文章 | 一手 | 深读论点、与 SAPwned 交叉 |
| https://www.wiz.io/blog/bingbang | BingBang 文章 | 一手 | 确认第 3/3 byline、Nir 不在列 |
| https://www.wiz.io/blog/ingress-nginx-kubernetes-vulnerabilities | IngressNightmare 文章 | 一手 | 确认第 4/4 byline |
| https://www.wiz.io/blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape | NVIDIAScape 文章 | 一手 | 更正线索：Hillai 非 byline，仅研究团队致谢(第4/6) |
| https://www.wiz.io/blog/wiz-research-codebreach-vulnerability-aws-codebuild | CodeBreach 文章 | 一手 | 更正线索：Hillai 非 byline，仅致谢(第4/5) |
| https://www.wiz.io/blog/nvidia-triton-cve-2025-23319-vuln-chain-to-ai-server | NVIDIA Triton 文章 | 一手 | 确认 Hillai 仅致谢，非 byline |
| https://www.wiz.io/blog/wiz-and-hugging-face-address-risks-to-ai-infrastructure | Hugging Face 文章 | 一手 | 确认 Hillai 仅致谢(第5/5)，非 byline |
| https://www.wiz.io/blog/wiz-research-discovers-critical-vulnerability-in-replicate | Replicate 文章 | 一手 | 确认 Hillai 未出现 |
| https://www.wiz.io/blog/author/nir-ohfeld | Nir 作者页 | 一手 | 构建 AI 供应链研究链全图、对照差异 |
| https://www.wiz.io/blog/author/shir-tamari | Shir 作者页 | 一手 | 同上 + BrokenSesame/Hell's Keychain URL |
| https://nvd.nist.gov/vuln/detail/CVE-2025-23266 | NVD CVE 详情 | 一手 | 确认 CVE 描述、CVSS、受影响产品、参考 URL |
| Wiz 博客主列表 https://www.wiz.io/blog | Wiz 官方 | 一手 | 确认无 Mish-Mesh / Ollama / DigitalOcean 文章 |
| Nir Ohfeld perspective SKILL.md（本仓库） | 二手（前序调研产物） | 二手，可信度中 | 用于差异对比，非 Hillai 直接证据 |
| 任务给出的线索清单 | 二手（用户提供的待核实清单） | 待核实 | 经核实后：4 条 byline 准确，2 条（NVIDIAScape/CodeBreach）被更正为"非 byline 仅致谢"，1 条（BingBang 非 Nir）准确，2 条（Mish-Mesh / KubeCon）未找到一手证据 |
| blackhat.com 议程页 / sched.com KubeCon 议程 / CNCF 议程页 / x.com/hillai | 一手但不可访问 | 不可访问（403/402/密码保护） | Black Hat 演讲细节、KubeCon 演讲、X profile 均未核实 |
| WebSearch 工具结果 | — | **不采信**（Nir 调研中曾出现幻觉错误名字，本调研中返回伪造的 MCP 工具调用） | 全部弃用 |

---

## 附录：Hillai 反复论点速查（≥3 次出现，跨 byline 文章）

1. **AI 服务 = 任意代码执行 = 隔离结构性难题**（SAPwned 主论点；38TB 佐证；研究团队致谢中他出现的 NVIDIAScape/Triton/HuggingFace/CodeBreach 全围绕此）
2. **网络隔离不是可靠边界，绕过即暴露扁平无认证内网**（SAPwned：Istio 绕过→Loki/EFS/Helm 全无认证；38TB：SAS token 不可收回）
3. **共享基础设施信任模型失败 + 可见性失败**（SAPwned：内部服务互信；38TB："no way for an administrator to know this token exists"）
4. **供应链投毒横向传播**（SAPwned：Docker registry/Artifactory 写权限；38TB：pickle 模型注入所有客户模型；BingBang：CMS 操纵搜索结果）
5. **过度授权/oversharing 是默认失败模式**（SAPwned：admission controller 默认放行；38TB：SAS token "full control, forever"）
6. **K8s 控制面/数据面边界被架构性打通**（SAPwned 主论点；IngressNightmare 同主题但 Hillai 非主笔）
7. **identity/secret 治理是隐性攻击面**（BingBang：AAD 多租户；SAPwned：AWS/Azure 凭证泄漏；38TB：SAS token 治理）

命名方法论：厂商名 + 安全双关（SAPwned=SAP+pwned；BingBang=Bing+Bang）；选择性使用（系列化研究用 codename，单点事件用描述性标题）。
智识谱系：自家 Wiz AI 基础设施研究系列（Hugging Face→Replicate→SAPwned）+ Black Hat "Isolation or Hallucination" + Istio/HuggingFace 官方文档 + fwd:cloudsec。

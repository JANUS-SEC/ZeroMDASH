# Rory McNamara — 他者视角与批评

> 调研对象:Rory McNamara,Snyk Security Labs 安全研究员
> 调研日期:2026-07-28
> 调研者:team-lead 派发的子 agent

---

## 调研方法

**主要手段**(因 WebSearch 工具在该环境返回空结果,改用直接 API + Wayback Machine):

1. **GitHub 用户搜索 / GHSA 致谢页** — 通过 `api.github.com` 搜到账号 `rmcnamara-snyk`(id 139076586),bio 为 "Staff Security Researcher",company 为 "Snyk",profile 显示 "7 security advisory credits"。GitHub Security Advisories 页面 `github.com/advisories?query=credit:rmcnamara-snyk` 实际列出 **9 条**致谢。逐条访问每个 GHSA 详情页核实 credited discoverer 字段——这是 CVE 归属最权威的一手来源。
2. **Wayback Machine CDX API** — `snyk.io` 不在 sandbox 直连白名单,故用 `web.archive.org/cdx/search/cdx` 找回 Snyk 博客原文快照,再用 `curl` 拉取存档 HTML 并解析。共定位到两篇 Leaky Vessels 主文:
   - `snyk.io/blog/leaky-vessels-docker-runc-container-breakout-vulnerabilities/`(总览,2024-01-31)
   - `snyk.io/blog/leaky-vessels-container-vuln-deep-dive/`(深度技术文,2024-02-06,Rory 独立署名)
3. **BleepingComputer 存档** — 通过 CDX 找到 `bleepingcomputer.com/news/security/leaky-vessels-flaws-allow-hackers-to-escape-docker-runc-containers/`,拉取 Wayback 快照核实媒体如何引用 Rory。
4. **同行团队主页** — Wiz(`wiz.io/blog`)和 Aqua Security(`aquasec.com/blog/`)的现网主页可直接取,用于横向对比研究方向。
5. **GitHub 仓库搜索** — 在 `github.com/snyk` 下定位到 Leaky Vessels 配套开源检测工具两个仓库,核实作者归属与 star 数。

**可信度标注规则**:
- **一手**:Rory 本人产出(他署名的博客、他 credited 的 GHSA 条目、他名下的 GitHub 账号)
- **二手**:他人对他工作的引用/报道(BleepingComputer、维护者致谢)
- **推测**:基于一二手证据的推断

**黑名单遵守**:未使用知乎、微信公众号、百度百科。Bing/DuckDuckGo 在该环境下 WebFetch 取不到结果(重定向到 cn 域且返回无关内容),故全部改用 GitHub API + Wayback CDX 两条硬证据通道。

**信息源黑名单遵守**:所有 CVE 归属以 GHSA 条目 credited 字段为准,不以媒体描述为准。

---

## CVE 发现记录(credited discoverer)

全部来源于 GitHub Security Advisory(GHSA)条目页的 "Credits" 段——这是比 NVD 更精确的发现者归属源(NVD 关键词搜索 "Rory McNamara" 返回 0 条,因为 NVD 描述里不写发现者姓名)。

| CVE / GHSA | 受影响项目 | 语言/生态 | 严重度 | Rory 角色 | 共同 credited | 日期 | 来源 |
|-----|------|------|------|------|------|------|------|
| CVE-2024-21626 (GHSA-xr7r-f8xq-vfvv) | opencontainers/runc | Go | High (8.6) | "discovered and disclosing the original vulnerability (attack 1)" | lifubang (acmcoder, attack 3a); Aleksa Sarai (SUSE, attacks 2 & 3b) | 2024-01-31 | https://github.com/advisories/GHSA-xr7r-f8xq-vfvv |
| CVE-2024-23651 (GHSA-m3r6-h7wv-7xxv) | moby/buildkit | Go | High (8.7) | Reporter(sole credited) | 无 | 2024-01-31 | https://github.com/advisories/GHSA-m3r6-h7wv-7xxv |
| CVE-2024-23652 (GHSA-4v98-7qmw-rqr8) | moby/buildkit | Go | Critical (10.0) | Reporter(sole credited) | 无;advisory 由 tonistiigi 发布 | 2024-01-31 | https://github.com/advisories/GHSA-4v98-7qmw-rqr8 |
| CVE-2024-23653 (GHSA-wr6v-9f75-vh2g) | moby/buildkit | Go | Critical (9.8) | Reporter(sole credited) | 无 | 2024-01-31 | https://github.com/advisories/GHSA-wr6v-9f75-vh2g |
| GHSA-pmf3-c36m-g5cf | containers/buildah | Go | High | credited finder | — | 2024-03-19 | https://github.com/advisories/GHSA-pmf3-c36m-g5cf |
| CVE-2024-1753 (GHSA-874v-pj72-92f3) | containers/podman v4 | Go | Moderate (6.3) | finder(credited under Credits) | 无;advisory 由 TomSweeneyRedHat 发布,patch 由 @nalind 提供 | 2024-03-18 | https://github.com/advisories/GHSA-874v-pj72-92f3 |
| CVE-2024-5138 (GHSA-p9v8-q5m4-pf46) | snapcore/snapd | Go | Moderate (4.0) | Reporter(sole credited) | 无 | 2025-01-16 | https://github.com/advisories/GHSA-p9v8-q5m4-pf46 |
| CVE-2026-23953 (GHSA-x6jc-phwx-hp32) | lxc/incus v6 | Go | High (8.7) | Finder | stgraber(remediation developer,兼 advisory 发布者) | 2026-01-22 | https://github.com/advisories/GHSA-x6jc-phwx-hp32 |
| CVE-2026-23954 (GHSA-7f67-crqm-jgh7) | lxc/incus v6 | Go | High (8.7) | Finder | stgraber(remediation developer) | 2026-01-22 | https://github.com/advisories/GHSA-7f67-crqm-jgh7 |

**重要说明 — "7" vs "9" 的差异**:GitHub profile 徽章显示 "7 security advisory credits",但 `github.com/advisories?query=credit:rmcnamara-snyk` 页面实际列出 **9 条**。差异可能源于徽章计数不含部分条目(如未分配 CVE 的 GHSA-pmf3,或 2026 年新加的两条 Incus 未刷新徽章)。以实际页面列表为准——**至少 9 条 credited 发现**。

**集中度观察(推测)**:9 条全部命中 **Go 生态的容器/构建运行时低层组件**——runc、buildkit、buildah、podman、snapd、incus。无一例外。这比任何博客自述都更精确地刻画了 Rory 的研究方向:**容器运行时与构建链的 userland 安全**。他没有去碰云控制平面(AWS/GCP IAM)、K8s API server、应用层依赖混淆这些"热门"方向,而是扎在容器引擎这一层。

---

## 同行致谢与引用

GHSA "Credits" 段是结构化的同行致谢——维护者在 advisory 里显式写明 Rory 的贡献:

- **runc 维护组(Aleksa Sarai / SUSE)** 在 CVE-2024-21626 致谢中明确写道:"Rory McNamara (Snyk) — discovered and disclosing the original vulnerability (attack 1)"。这是 runc 这类核心基础组件的维护者对 Rory 发现权的正式承认。 —— https://github.com/advisories/GHSA-xr7r-f8xq-vfvv (一手/结构化致谢)
- **BuildKit 维护者 tonistiigi**(Docker/Tonis Tiigi)将 CVE-2024-23651 / 23652 / 23653 三条 advisory 的 Reporter 都记为 rmcnamara-snyk,并作为 advisory 发布者——说明 Snyk 把漏洞报给 Docker/BuildKit 后,维护者认可 Rory 为唯一发现来源。 —— https://github.com/advisories/GHSA-4v98-7qmw-rqr8 等 (一手/结构化致谢)
- **Podman/buildah 维护者 TomSweeneyRedHat**(Red Hat)在 CVE-2024-1753 advisory 的 Credits 段把 rmcnamara-snyk 列为 finder。 —— https://github.com/advisories/GHSA-874v-pj72-92f3 (一手/结构化致谢)
- **Incus 维护者 stgraber**(Stéphane Graber)在 CVE-2026-23953 / 23954 两条 advisory 中将 rmcnamara-snyk 列为 Finder,自己仅记为 Remediation developer。 —— https://github.com/advisories/GHSA-7f67-crqm-jgh7 (一手/结构化致谢)
- **snapd/snapcore 维护组** 在 CVE-2024-5138 中将 rmcnamara-snyk 列为唯一 Reporter。 —— https://github.com/advisories/GHSA-p9v8-q5m4-pf46 (一手/结构化致谢)

**非结构化的口头/博客致谢**:本次调研未在可访问范围内(BleepingComputer 存档、Snyk 官方博客、各 GHSA 致谢段)找到同行在推特/独立博客里额外给 Rory 写的 "shoutout" 类致谢。 sandbox 网络白名单不含 twitter/x.com,无法核验 X 上的同行反应。**标记为"未核实到"**,而非"不存在"。

---

## 媒体引用

- **BleepingComputer(Bill Toulas,2024-02-04 10:17 AM)**:报道 Leaky Vessels 时写"The flaws were discovered by Snyk security researcher Rory McNamara in November 2023, who reported them to impacted parties for fixing."——把 Rory 作为唯一具名发现者,且明确归属 Snyk。报道还引用了 Snyk 的演示图("Demonstration of Leaky Vessels exploit to access data on host — Source: Snyk")。 —— Wayback 存档 https://web.archive.org/web/20240204180634/https://www.bleepingcomputer.com/news/security/leaky-vessels-flaws-allow-hackers-to-escape-docker-runc-containers/ (二手)
- **The Register / The Hacker News / Dark Reading / SecurityWeek**:通过 Wayback CDX 搜索 `theregister.com`、`thehackernews.com`、`darkreading.com` 在 2024-01-31 ~ 2024-02-10 窗口的 URL,**未检索到** Leaky Vessels 相关条目被 Wayback 抓取(可能未被存档而非未报道)。**标记为"未核实到"这些媒体是否引用 Rory**。 —— CDX 返回空(信息不足,而非证据缺失)

---

## 他人总结的 Rory 研究风格

主要来源是 Rory **本人**在 Snyk 深度博客里的自述,以及 Snyk 官方总览博客对团队的描述。**严格区分"他说过" vs "别人说他"**——本节大量是"他自己说的",媒体/同行对他风格的二次总结未核实到。

**Rory 本人在《Leaky Vessels deep dive: Escaping from Docker one syscall at a time》(2024-02-06,Snyk 博客)中自述(一手)**:

- "I had the opportunity to perform what is arguably my favorite kind of research using my favorite selection of tools."—— 把这类研究定位为"我最爱的研究类型 + 我最爱的工具组合"。这不是客套,是对自我方法风格的明确宣誓。
- 研究对象定位:"userland operating system security area",并称其 "relatively unrepresented"(相对被忽视的领域)。**这是他选题哲学的核心**:主动避开热门,钻进被忽视的 userland OS 层。
- 方法工具箱:以 **strace** 为核心——"strace is a powerful tool on Linux that allows us to attach to specific processes and output a list of all the syscalls made by the process and its associated arguments."他认为这类工具"不需要 complicated and expensive tooling to achieve significant results"——**明确轻工具、重手工审阅**的取向。
- 漏洞类目:聚焦 **race condition** 与 **confused deputy**(混淆代理)。他把漏洞成因归纳为"application assuming that its actions occurred in isolation, therefore failed to appropriately guard against outside interference"。
- 验证方式:每个发现都 "turned our research into a proof of concept"——POC 驱动,不只报漏洞要打出来。
- "manual review of system functionality to identify potential cases of a race condition, which can then be exploited"——**手工审计驱动**,而非纯模糊测试或纯静态扫描。

**Snyk 官方总览博客对 Rory 角色(二手,Snyk 自家口径)**:
- "Snyk security researcher Rory McNamara, with the Snyk Security Labs team, identified four vulnerabilities — dubbed 'Leaky Vessels' — in core container infrastructure components that allow container escapes." —— https://web.archive.org/web/20240131221313/https://snyk.io/blog/leaky-vessels-docker-runc-container-breakout-vulnerabilities/
- Snyk 把 Rory 与 Security Labs 团队并列陈述——他在这次研究里既是发现者也是披露执行者(GHSA collaborator)。

**他人(非 Snyk)对 Rory 风格的二次总结**:未核实到。BleepingComputer 仅陈述"由他发现"这一事实,未做风格评价。**信息不足,如实标注。**

---

## 主要批评与争议(重点)

**结论:未发现针对 Rory McNamara 本人研究方法、披露策略或结论可靠性的公开批评。**

调研路径与发现:

1. **GHSA 致谢段** —— 9 条 advisory 无一出现 "disputed" / "partial credit dispute" / "false positive" 字样;相反,维护者均明确承认其发现权。无任何 advisory 被标记为 disputed。 —— 一手,可信度高
2. **BleepingComputer 报道** —— 报道口径中性偏正面,引用 Snyk 官方声明"no signs of active exploitation",无批评性措辞。 —— 二手
3. **披露时序** —— Leaky Vessels 的披露严格走协调流程(Nov 20 发现 → Dec 11 报 Docker → Dec 转 runc → Jan 17 邮件列表预警 + embargo → Jan 31 公开 + 同日发补丁 + 同日发检测工具)。这是教科书式 coordinated disclosure,没有抢跑或逼宫迹象。 —— 一手(Snyk 自家 timeline)
4. **Snyk 商业化争议(整体,非 Rory 个人)** —— 在可访问的存档范围内未检索到针对 Snyk Security Labs 研究可信度的具体争议报道。Snyk 作为商业化漏洞情报厂商,业界对其"商业 vs 开源"定位偶有议论,但这些议论不指向 Rory 个人研究产出,且本次调研未取到可直接引用的具体批评文章。**标记为"未核实到具体批评",不编造。**

**诚实声明**:找不到批评本身是有信息量的结论——Rory 的公开研究足迹高度集中在结构化 GHSA 致谢里,几乎没有游离于披露流程之外的争议性公开发声。这可能反映(a)他研究确实扎实、(b)他个人在社交媒体/会议上的曝光较低、或(c)白名单内信息源不足以覆盖 X/Twitter 等讨论场。**三种解释都成立,不强行取舍。**

---

## 与同行对比定位

> 维度对比基于各团队公开博客与 GHSA 致谢的可核验事实。"研究风格"一行为推测,标注。

| 维度 | Rory McNamara (Snyk) | Aqua Security (Nautilus) | Sysdig | Wiz Research | Trail of Bits |
|------|-------------|---------------|--------|-----|---------------|
| 主攻方向(可核验) | 容器运行时低层:runc/buildkit/buildah/podman/snapd/incus;全部 Go 生态 | 云原生栈:容器/K8s/serverless/CI-CD,年度 cloud-native 威胁报告;Trivy/Tracee 开源 | (CDX 未取到具体博客,信息不足) | 云运行时盲区、agentless 威胁检测、AI/MCP 安全、供应链;Atlas AI 漏洞研究 | (本次未取,但公开以密码学/合约审计/编译器著称,方向与容器运行时不同) |
| 研究风格(推测) | strace 驱动、userland 手工审计、race condition / confused deputy、POC 驱动、"轻工具重手工"、刻意钻"被忽视的领域" | 威胁情报导向、年度综合报告、AI 生成恶意软件分析、shadow resource 攻击演示 | (信息不足) | exploit 验证(Atlas AI 自动出 exploit)、agentless 监测、Red Agent 端到端打穿、business logic / BOLA | (推测)审计重于发现,偏密码学/形式化 |
| 披露策略(可核验) | 严格 coordinated disclosure,多周 embargo,同日补丁+检测工具发布;GHSA collaborator 全程参与 | (未取到具体披露时序案例) | (信息不足) | "responsible disclosure",建议用户优先打补丁/WAF | (未取) |
| 输出形态(可核验) | 深度技术 blog(Snyk)+ GHSA 致谢 + 配套开源检测工具(leaky-vessels-static/dynamic-detector) | 综合年度威胁报告 + 博客 + Trivy/Tracee 开源项目 | (信息不足) | 博客为主,AI 工具(Atlas)作为研究产出 | 审计报告 + 工具(yojson/solc 等) |
| 与 CVE 维护组关系(可核验) | 深度嵌入:runc(BuildKit/Podman/Incus)维护者直接在 GHSA 致谢他,tonistiigi/stgraber/TomSweeneyRedHat 等维护者与其协作 | (未取到同等粒度的 GHSA 致谢数据) | (信息不足) | (未取) | (未取) |

**关键差异点(推测,基于上表)**:

1. **粒度差异**:Rory 是"单点深挖型"——一次研究只攻一个低层组件(runc/buildkit),挖出 4 个 CVE 写一篇深度技术博客。Wiz/Aqua 偏"面状覆盖型"——跟踪云控制平面、AI、供应链等横向趋势,出报告与产品。Rory 的 9 条 CVE 全在同一技术层(容器运行时),Wiz/Aqua 的研究产出横跨多个不相邻域。
2. **工具哲学差异**:Rory 明确表态"不需要 complicated and expensive tooling",推崇 strace + 手工审计;Wiz 走相反路线,自研 Atlas AI 自主产出并验证 exploit。这是两种几乎对立的研究哲学。
3. **披露参与度差异**:Rory 在 GHSA 流程里以 collaborator 身份深度参与(被维护者正式致谢),说明他与上游维护组关系紧密,而非"披露完就走"的商业研究方。
4. **曝光差异**:Rory 几乎只在 Snyk 博客和 GHSA 出现,个人 GitHub(rmcnamara-snyk)0 公开仓库、8 follower;Wiz/Aqua 研究有更强的内容运营与媒体触达。Rory 是典型的"低曝光深技术"型研究员。

**信息不足维度**:Sysdig 与 Trail of Bits 的具体研究方向未在本次可访问源内核实到足够粒度,对比表对应单元格留白,不编造。

---

## Snyk Security Labs 团队定位

- **Rory 在团队中的角色**:GitHub bio 为 "Staff Security Researcher"(Staff 级别 = 资深个人贡献者,高于 Senior,通常低于 Principal)。从研究产出看,他是 Security Labs 内 **容器/运行时低层方向的核心承担者**——Leaky Vessels 这种旗舰研究由他主笔深度博客、独立署名,9 条 credited CVE 全部集中在容器运行时生态。 —— 一手(GitHub bio + 署名)
- **团队规模与构成**:Snyk 官方博客称 "Snyk's Security Labs team has helped to responsibly disclose over 3,200 vulnerabilities in key packages across a variety of ecosystems"。团队累计披露 3,200+ 漏洞,横跨多生态。具体人数与其它成员名单**未在可访问存档里核实到**——Snyk 的 author 列表页未被 Wayback 索引到 `snyk.io/blog/author/rory*` 路径(CDX 返回空)。**标记信息不足。** —— 一手(累计数) + 信息不足(团队名单)
- **配套产出**:Leaky Vessels 期间 Snyk 以组织名义(非 Rory 个人)在 GitHub `snyk` org 下发布两个开源检测工具:`snyk/leaky-vessels-dynamic-detector`(105 stars,eBPF 动态检测,2024-01-31 创建)和 `snyk/leaky-vessels-static-detector`(95 stars,基于 BuildKit Dockerfile 解析器 AST + 正则的静态检测,2024-01-31 创建)。这体现 Snyk Labs "研究 + 工具化 + 商业产品联动" 的产出闭环,而非纯博客。 —— 一手(GitHub 仓库)

---

## 媒体 vs 同行差异

- **媒体口径(BleepingComputer)**:把 Rory 描述为"Snyk security researcher Rory McNamara"——身份标签化、机构归属化,只说他"发现了漏洞",不评价研究风格。媒体关心的是漏洞本身的影响(container escape、Docker/K8s 受影响、需打补丁)。 —— 二手
- **同行口径(GHSA 致谢)**:更精确——区分 "discovered and disclosing the original vulnerability (attack 1)"(runc 维护组)与 "Finder"/"Reporter"(其他维护组),把 Rory 的贡献定位到具体攻击变体或 advisory 角色,而非笼统"发现者"。同行更关心他在哪一个攻击变体上贡献、披露流程中承担什么角色。 —— 一手/结构化
- **差异**:媒体把 Rory 当"机构新闻"的一部分,同行把他当"具体漏洞归属的具体贡献者"。媒体未提及他的方法学(strace/race condition),同行致谢也未提——他的方法学主要来自**他本人的博客自述**,而非第三方评价。**这是关键空白**:没有任何二手来源独立验证或评价他的研究风格,所有"风格"描述都是他自己说的。

---

## 矛盾与未解之处

1. **GitHub 徽章 "7" vs 实际页面 "9"**:profile 徽章显示 7 credits,advisories 搜索页显示 9 条。差异未解决,可能是徽章计数滞后或排除部分类型(如无 CVE 的 GHSA-pmf3)。**以 9 条为准**,因页面列表是可逐条核实的实据。
2. **"no signs of active exploitation"(Snyk/BleepingComputer)vs 97th percentile EPSS**:CVE-2024-21626 的 EPSS 为 18.087%(97th 百分位),即 NVD 估计 30 天内被利用概率约 18%。Snyk 在披露时声称"无在野利用",EPSS 是概率预测非实际利用——两者不矛盾,但读者易混淆"无在野利用"与"低利用概率"。并列记录,不取舍。
3. **Incus 两条 CVE 标 "No patched version is listed"(GHSA-7f67)vs "patched in 6.21.0"(GHSA-x6jc)**:同一批 Incus 漏洞,一条 advisory 标注已修,一条未列修复版本。可能源于 advisory 维护状态差异,非 Rory 研究本身矛盾。如实记录。

---

## 信息不足之处

明确标注以下维度**未能核实**:

1. **同行在 X/Twitter、独立博客对 Rory 的口头评价/批评** —— sandbox 白名单不含 x.com/twitter.com,无法核验;本次调研未取到。
2. **Rory 在会议(Black Hat、DEF CON、KubeCon、DockerCon)的演讲记录** —— 黑名单内 `www.blackhat.com` 可访问但未检索 Rory 名字的演讲条目;**未核实到**,不等于未演讲过。
3. **Rory 的个人 Twitter/LinkedIn/博客** —— 未在 GitHub profile 列出;其 GitHub 账号 0 公开仓库、bio 仅含职位与公司。**无独立个人发声渠道被核实到。**
4. **Sysdig、Trail of Bits 的具体研究方向对比** —— 本次可访问源内未取到足够粒度的同行数据,对比表对应单元格留白。
5. **Snyk Security Labs 完整成员名单与团队规模** —— Snyk author 列表页未被 Wayback 索引,无法列出 Rory 的同事与他的相对资深度。
6. **针对 Snyk 研究可信度的具体争议报道** —— 未检索到可直接引用的具体文章。Snyk 商业化定位在业内偶有议论,但本次调研未取到针对 Rory 个人或 Leaky Vessels 这类具体研究的可引用批评。
7. **Rory 是否还 credited 了更多 CVE**(除已核实的 9 条外)—— GitHub advisories 页面显示 9 条,但 NVD 关键词搜索返回 0(NVD 不在描述里写发现者)。可能存在 credited 字段未结构化、或 credited 名字写法不同的 advisory 未被本次检索覆盖。**本次以 9 条为已核实下限。**

---

## 关键文件与 URL 索引(便于后续复核)

- Rory GitHub profile(Staff Security Researcher, Snyk):https://github.com/rmcnamara-snyk
- GHSA 致谢搜索页(9 条):https://github.com/advisories?query=credit%3Armcnamara-snyk
- Leaky Vessels Snyk 总览博客(存档):https://web.archive.org/web/20240131221313/https://snyk.io/blog/leaky-vessels-docker-runc-container-breakout-vulnerabilities/
- Leaky Vessels 深度博客(Rory 独立署名,存档):https://web.archive.org/web/20240208015227/https://snyk.io/blog/leaky-vessels-container-vuln-deep-dive/
- BleepingComputer 报道(存档):https://web.archive.org/web/20240204180634/https://www.bleepingcomputer.com/news/security/leaky-vessels-flaws-allow-hackers-to-escape-docker-runc-containers/
- 配套开源工具 1:https://github.com/snyk/leaky-vessels-static-detector
- 配套开源工具 2:https://github.com/snyk/leaky-vessels-dynamic-detector
- Wiz 研究博客(对比用):https://www.wiz.io/blog
- Aqua Security 博客(对比用):https://www.aquasec.com/blog/

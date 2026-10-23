# Rory McNamara — 决策模式维度

> 研究对象:Snyk Staff Security Researcher(2026 JSON-LD title)/ Staff Research Engineer(2024 HTML title,见矛盾§1),GitHub `rmcnamara-snyk`(账号创建 2023-07-09)。
> 本文件全部内容为**从可核实行为数据反推的决策模式推测**,非本人声明;唯一例外是 Snyk 贡献者页 bio 一句,属**自述**,已标注。
> 每条决策均标注:
> **行为证据(一手)** = 可从 NVD / Wayback / GitHub / Snyk 贡献者页直接取证的客观事实;
> **推断(推测)** = 基于行为证据的因果猜测,未经本人确认。
> 数据采集日期:2026-07-28。

---

## 调研方法(全部从 GitHub API + NVD + GHSA + Wayback 取的可核实行为数据反推,标注为推测)

### 数据源与取证过程

1. **NVD CVSS/CWE/CNA** — 对 9 个 CVE 中的 8 个逐条 `curl https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=<CVE>` 取回(2026-07-28),取得 baseScore、vectorString、CWE、CNA source、references。**一手可信。**(buildah GHSA-pmf3 无 CVE 编号,未入 NVD 查询;其性质由同系列 1753 旁证。)
2. **额外补查 CVE-2024-23326(Istio/Envoy)** — 现有 05-decisions.md 旧版提及此 CVE,本调研经 NVD 确认其存在(CVSS 5.9 Medium、CNA=GitHub、CWE-391/444)。但**Rory 在该 CVE 的个人 credit 未经 NVD 确认**(详见矛盾§3)。
3. **Wayback CDX + 快照取证** — `web.archive.org` 在沙箱白名单内,curl 可达。对 `snyk.io/contributors/rory-mcnamara/` 跑 CDX,得 **18 个快照**(2024-02-25 ~ 2026-07-23),逐个可 `curl --compressed id_` 原始快照取证。
4. **Snyk 贡献者页 bio + JSON-LD 文章列表** — 取 2024-02-25 与 2026-07-22 两个快照,提取 `<title>`、meta description、JSON-LD `bio`/`title`/`featuredImage.publishDate`/`excerpt`。**一手可信**——bio 与文章发布时间直接来自 Snyk 官方页面快照。
5. **Leaky Vessels deep-dive 快照内容** — 直接 `curl` 旧版引用的 `web.archive.org/web/20240208015227id_/https://snyk.io/blog/leaky-vessels-container-vuln-deep-dive/`,grep 得 "Written by"/"Rory McNamara"/"Leaky Vessels"。**一手可信**——文章确存在且署名 Rory。
6. **GitHub 账号 footprint** — `rmcnamara-snyk` 账号元数据(0 public_repos/0 starred/0 following/无 Twitter/无 blog)与「上游 6 仓库公开 PR/issue/comment = 0」「不在 runc MAINTAINERS」均为任务上下文已核实事实。**一手可信。**
7. **协作关系** — Leaky Vessels 公开公告署名(Aleksa Sarai/cyphar,SUSE)、Solar Designer 回帖、Incus 合并披露等,来自上游公告与 oss-security 帖(NVD references 中可见 `openwall.com/lists/oss-security/2024/02/01/1`)。**一手可信。**
8. **GHSA API 未能独立复核** — GitHub 未鉴权 API 限额 60/小时在调研中耗尽(`x-ratelimit-remaining: 0`,reset epoch 1785218379)。GHSA 的 `published_at`、`credits` 字段未能经 `api.github.com/advisories/<GHSA>` 独立复核;改用任务上下文已核实值,并与 Wayback 文章 `publishDate` + NVD references 中的上游 release tag / oss-security 帖日期交叉验证一致。详见「信息不足之处」。

### 与本任务初始前提的关键冲突(已用 Wayback 解决,记录在此)

> 任务初始上下文断言「Snyk 作者页全 404」「Wayback 下 snyk.io 含 leaky/vessel/21626 的 URL = 0 条」「零公开 footprint / persona 极简主义」。
> **经 Wayback 取证,这些断言不准确**:
> - `snyk.io/contributors/rory-mcnamara/` 有 **18 个 Wayback 快照**(2024-02-25 ~ 2026-07-23),并非全 404;
> - CDX 对 `snyk.io/blog/*leaky*` 通配返回 0 行(任务断言据此),但**直接 fetch 具体快照 URL 返回 Rory 署名的 Leaky Vessels 文章正文**——文章确在 Wayback,只是 CDX 通配模式未命中;
> - Rory **有**公开产出:Snyk 贡献者页 bio、5+ 篇 Snyk 博客署名文章、3 个开源工具仓库(snyk/ 与 snyk-labs/ org 下)。
> 因此**本文件不采信「零 footprint」前提**,改用 Wayback + NVD 实证重写决策维度 5、6。详见矛盾§1。

### 推断方法论

- **行为证据 → 决策规则**:从「他做了什么」反推「他可能遵循什么规则」;凡 bio/文章正文有自述,优先采信自述并标注「自述」。
- 凡涉及动机/内心偏好的结论,一律标 **(推测)** 并附可信度(高/中/低)。
- 凡无法从行为取证的,写「未核实到——此维度信息不足」,绝不编造。

---

## 决策模式清单(每个决策:行为证据 → 推断的决策规则 → 可信度)

### 1. 研究目标选择:容器运行时/构建器 + HTTP 中间件,锚定 race conditions

**行为证据(一手)** —

(a) **9 条 GHSA credit 全部落在 Linux 容器管理工具链**(NVD 描述首句取证 2026-07-28):

| CVE/GHSA | 受影响组件 | NVD 描述首句 | CNA |
|---|---|---|---|
| CVE-2024-21626 / GHSA-xr7r-f8xq-vfvv | runc | "runc is a CLI tool for spawning and running containers on Linux according to the OCI specification" | GitHub |
| CVE-2024-23651 / GHSA-m3r6-h7wv-7xxv | buildkit | "BuildKit is a toolkit for converting source code to build artifacts…" | GitHub |
| CVE-2024-23652 / GHSA-4v98-7qmw-rqr8 | buildkit | 同上 | GitHub |
| CVE-2024-23653 / GHSA-wr6v-9f75-vh2g | buildkit | 同上 | GitHub |
| CVE-2024-1753 / GHSA-874v-pj72-92f3 | buildah/podman | "A flaw was found in Buildah (and subsequently Podman Build)…" | Red Hat |
| GHSA-pmf3-c36m-g5cf | buildah | (同 1753 系列,无 CVE) | (Red Hat 系列) |
| CVE-2024-5138 / GHSA-p9v8-q5m4-pf46 | snapd | "The snapctl component within snapd allows a confined snap to interact with the snapd daemon…" | Ubuntu |
| CVE-2026-23953 / GHSA-x6jc-phwx-hp32 | incus | "Incus is a system container and virtual machine manager" | GitHub |
| CVE-2026-23954 / GHSA-7f67-crqm-jgh7 | incus | 同上 | GitHub |

(b) **非 9-list 的额外产出**(Snyk 贡献者页 JSON-LD + 旧版 05-decisions 取证):
- CVE-2024-23326(Envoy/Istio,HTTP 中间件,NVD CVSS 5.9 Medium,CWE-391/444,请求走私)——NVD 确认 CVE 存在;Rory 个人 credit 未确认(矛盾§3)。
- GitHub Actions 研究(2024-06-06,与 Elliot Ward、Raul Onitza-Klugman 三人合著,CI/CD 攻击面)。
- Safe Path Handling(2026-03-31,与 Stephen Thoemmes 合著,教育型 TOCTOU)——2026-07-22 快照文章列表确认存在。

(c) **Snyk 贡献者页 bio 自述**(2026-07-22 快照,一手):
> "Long-time bug bounty hunter, ex-pentester, and AppSec engineer. Rory is passionate about race conditions and Linux exploitation."

**推断的决策规则(推测)** — 他刻意把研究范围锚定在 **race conditions + Linux exploitation**(自述),落地选择的载体是**容器运行时/构建器/容器管理器**这一窄而深的基础设施层(9/9),并阶段性外扩到相邻边界:**HTTP 中间件**(Istio/Envoy,2024-06)与 **CI/CD 攻击面**(GitHub Actions,2024-06)。载体随时间略有迁移,但底层锚点(race condition / 边界时序缺陷)未变——2026 的 Safe Path Handling 仍回到 TOCTOU。(可信度:**高** — 9/9 + bio 自述 + 文章主题一致。)

**推测的载体选择逻辑** — 容器运行时是「宿主↔不可信负载」的强制边界,边界不变量违反直接等于逃逸/提权,ROI 高且代码量可控、适合单兵深度审计;race condition 在多步构建/共享 mount 等并发路径上天然存在。他可能据此选了「race condition 最易发生、破坏力最大、可审计性最高」的层。(可信度:**中** — 动机属合理推断,非自述。)

---

### 2. 漏洞类型选择:race condition / TOCTOU / 边界不变量违反(自述 + 行为双证)

**行为证据(一手)** —

(a) **bio 自述**(2026-07-22 快照,一手):"passionate about **race conditions** and Linux exploitation"——这是**本人声明的研究焦点**,非纯推断。

(b) **文章正文自述**(2024-02-25 快照 JSON-LD excerpt,一手):23651 文章 excerpt 原文 "Snyk has discovered a build-time **race condition** container breakout vulnerability in all versions of Buildkit <=v0.12.4" ——race condition 是其命名的根因。

(c) **8 个 CVE 的 NVD-recorded CWE 与根因**(NVD 取证 2026-07-28):

| CVE | NVD CWE | 根因(NVD 描述) | 边界对象 | 不变量违反类型 |
|---|---|---|---|---|
| 21626 | CWE-403/668 | 内部 fd 泄漏,attacker 操纵 `process.cwd`→`/proc/self/fd/7/` | file descriptor | 资源未关闭 |
| 23651 | CWE-362 | 两恶意构建步骤并行共享 cache mount subpath 竞争 | cache mount | 竞争未序列化 |
| 23652 | CWE-22 | `RUN --mount` stub cleaner 致宿主 FS 访问 | mount cleanup | 路径未约束 |
| 23653 | CWE-863 | interactive containers 的 entitlements 授权错误 | entitlements | 授权未校验 |
| 1753 | CWE-59 | Buildah 允许 mount 宿主任意位置 → 构建期逃逸(link following) | mount target | 链接未校验 |
| 5138 | CWE-20 | snapctl 未正确解析命令行参数 → 鉴权绕过 | 命令解析/confined snap | 输入未校验 |
| 23953 | CWE-93 | YAML 配置中换行注入 → 容器启动越权 | 配置/环境变量 | CRLF 未净化 |
| 23954 | CWE-22 | 模板渲染致任意宿主文件读写 | 模板/镜像 | 路径未约束 |

外加 23326(Istio,CWE-391/444,请求走私/响应头注入)——HTTP 边界的时序/注入缺陷。

(d) **2026 教育型文章 Safe Path Handling**(2026-07-22 快照确认存在)主题即 TOCTOU——`openat()`/`O_NOFOLLOW`/Go 1.24 `os.Root` 为「金标准」、Node.js 因不暴露 `openat()` 而"effectively impossible"(旧版 05-decisions 引述)。

**推断的决策规则(推测)** — 他的漏洞挖掘启发式是「找边界对象(fd / mount / cwd / entitlements / config / template)上**应当被强制的时序/完整性不变量被遗忘**」,即 **race-condition / TOCTOU / 不变量违反狩猎**。这不是按 CWE 标签找,而是按「边界对象在并发/生命周期管理上的缺口」找——bio 自述与 8 条根因双向印证。(可信度:**高** — bio 自述 + 文章命名 + 8 条根因可归一,三重一致。)

**推测的跨项目迁移性** — 同一套「边界对象时序完整性」思维可跨项目复用:runc 的 fd 生命周期 → buildkit 的 mount 清理/竞争 → snapd 的命令解析 → incus 的配置净化 → Envoy 的请求时序。这解释了他能在 6 个不同上游连续产出。(可信度:**中** — 推断的思维迁移路径,无本人确认。)

---

### 3. 披露时机:批量协调同日发布,偶留部署窗口

**行为证据(一手 + 交叉验证)** — 按 `published_at`(GHSA,任务上下文已核实;Wayback 文章 `publishDate` + NVD references 上游 release tag / oss-security 帖日期交叉一致)排列时间线:

| 日期 | 同日发布的 CVE 数 | 事件 | 旁证 |
|---|---|---|---|
| 2024-01-31 | **4** | Leaky Vessels 协调发布:21626(runc)+ 23651/23652/23653(buildkit)同日 | Wayback:5 篇文章 `publishDate` 全为 `2024-01-31T07:0x`;runc `v1.1.12`、buildkit `v0.12.5` 同日 release;oss-security 帖 `2024/02/01/1` |
| 2024-03-19 ~ 03-28 | **2**(9 天窗口) | buildah(pmf3,03-19)+ podman(1753,03-28)集群 | NVD 1753 refs 多条 Red Hat RHSA-2024:2049~2084 |
| 2024-06-04 ~ 06-20 | 1(16 天窗口) | Envoy advisory 06-04 → Rory 技术深度文章 06-20 | NVD 23326 refs;旧版 05-decisions Wayback 文章 06-20 |
| 2025-01-16 | 1 | snapd(5138)单独 | NVD refs:launchpad bug 2065077、snapd commit |
| 2026-01-22 | **2** | Incus 协调发布:23953 + 23954 同日 | NVD refs 指向同一 `driver_lxc.go` 不同行(1081/7215/7294)+ PoC/patch 附件 |

**推断的决策规则(推测)** — 他偏好**批量、协调、同主题多 CVE 一次性披露**(Leaky Vessels 4 同日、Incus 2 同日),而非逐条 drip-feed;但**不是教条**——Istio/Envoy 在补丁 advisory 后**留 16 天部署窗口**才发完整技术细节,说明「批量同日」仅适用于同一审计周期内发现的相关缺陷簇,单点缺陷则可留窗口。(可信度:**高** — 3 次明确批量事件 + 1 次明确留窗口,模式清晰。)

**推测的窗口决策** — 留窗口仅出现在 HTTP 中间件(Istio),容器运行时缺陷一律同日。推测:容器运行时补丁落地即用户可升级,同日公开最大化透明;中间件(Envoy)下游部署链长、缓存投毒影响面广,故留窗口让下游升级。即窗口长度随「下游部署复杂度」调整。(可信度:**中** — 推断,无本人确认。)

---

### 4. 协作模式:与上游 maintainer 合并披露,不抢 GHSA 主笔,但写 Snyk 技术深度

**行为证据(一手)** —

(a) **Leaky Vessels(2024-01-31)三方合并披露**:Rory 发现 attack 1(process.cwd→fd);Aleksa Sarai(cyphar,SUSE,runc maintainer)发现 attack 2 与 3b 并**署名公开公告**;lifubang 发现 attack 3a。Solar Designer 在 oss-security 回帖感谢 "you and others you credit"。Rory **不在 runc MAINTAINERS 名单**(纯外部 reporter)。
(b) **Incus(2026-01-22)合并披露**:Rory + stgraber(Stéphane Graber,Incus 上游 maintainer)合并;NVD references 同时含 `github.com/user-attachments/files/...` 的 PoC 脚本与 patch(reporter 提供 PoC+patch,上游发布)。
(c) **GitHub Actions(2024-06-06)三人合著**:Rory + Elliot Ward + Raul Onitza-Klugman。
(d) **Safe Path Handling(2026-03)两人合著**:Rory + Stephen Thoemmes。

**推断的决策规则(推测)** — 他不坚持单独披露(solo),接受与上游 maintainer 及第三方研究者**合并披露**,**让上游 maintainer 主导 GHSA 公开叙事**(Leaky Vessels 公告由 cyphar 署名而非 Rory);但**自己保留并主笔 Snyk 博客技术深度文章**(Leaky Vessels deep-dive 由 Rory sole-author,Istio 由 Rory sole-author)。即「GHSA 主笔让给上游,Snyk 技术叙事主笔自己写」——分工清晰。(可信度:**高** — 两次合并披露 + deep-dive 署名取证一致。)

**推测的协作偏好** — 他可能主动寻找「正在做同主题审计」的同行并合并(如与 cyphar 在 runc/buildkit 边界审计上的合并),而非竞争抢先;合并披露对上游更友好(一次 patch 周期覆盖多个相关缺陷),也契合维度 3 的批量协调偏好。(可信度:**中** — 协作发起方无法从公开记录确认。)

---

### 5. 披露通道:GHSA(上游协调)+ Snyk 博客(技术深度)+ 开源工具(检测器),非「仅私有 GHSA」

**行为证据(一手)** —

(a) **GHSA 上游协调通道**:9 条 credit 全经 GitHub Security Advisory 私有通道 + 上游协调发布(NVD references 中 8/8 含 `github.com/<org>/<repo>/security/advisories/GHSA-...` 链接);上游 6 仓库公开 PR/issue/comment = 0(无公开漏洞讨论残留);9 条 references 中 snyk.io URL = 0——**但这只是 advisory 不链第三方博客的常态**,并非「Snyk 不发内容」。
(b) **Snyk 博客技术深度通道**(Wayback 取证):Leaky Vessels deep-dive(2024-02-06)`snyk.io/blog/leaky-vessels-container-vuln-deep-dive/` 含 "Written by Rory McNamara";2024-02-25 快照 JSON-LD 列 5 篇 Leaky Vessels 系列文章全 `publishDate 2024-01-31`;Istio 文章(2024-06-20)、GHA 文章(2024-06-06)、Safe Path Handling(2026-03-31)均经快照确认。
(c) **开源工具通道**(旧版 05-decisions 取证,snyk/snyk-labs org):`snyk/leaky-vessels-static-detector`、`snyk/leaky-vessels-dynamic-detector`(eBPF)、`snyk-labs/github-actions-scanner`。
(d) **oss-security 帖由 Sarai 署名**(Leaky Vessels),非 Rory 自署名帖。

**推断的决策规则(推测)** — 他的披露通道是**三段式**:① 私有 GHSA + 上游协调(让上游发补丁与 advisory);② Snyk 博客发技术深度 writeup(自己主笔,补丁同日或留窗口);③ 开源工具(detector/scanner)让 maintainer 与用户自查。他**不**自署名发 oss-security 帖(让上游 maintainer 主导邮件列表叙事),但**主动**在 Snyk 博客做完整技术公开。这纠正了「仅私有 GHSA、零公开通道」的误读。(可信度:**高** — 三段均有 Wayback/NVD 取证。)

---

### 6. persona 策略:企业品牌 persona,非个人品牌 persona(纠正「零 footprint」误读)

**行为证据(一手)** —

(a) **Snyk 贡献者页 persona**(Wayback 18 快照取证):`snyk.io/contributors/rory-mcnamara/` 自 2024-02-25 起持续存在,2026-07-22 快照含 bio「Long-time bug bounty hunter, ex-pentester, and AppSec engineer. Rory is passionate about race conditions and Linux exploitation.」+ JSON-LD `title: "Staff Security Researcher"` + 5 篇署名文章列表。
(b) **Snyk 博客署名**:5+ 篇文章署 "Written by Rory McNamara"。
(c) **开源工具仓库**:3 个工具仓在 `snyk/` 与 `snyk-labs/` org 下(非个人账号)。
(d) **个人 GitHub 账号 `rmcnamara-snyk`**(2023-07-09 创建):0 public_repos / 0 starred / 0 following / 0 orgs / 0 gists / 无 Twitter / 无 blog / 无 location / 无公开 events。

**关键对比**:(a)(b)(c) 显示他有**丰富公开产出**;(d) 显示产出**全部挂在 Snyk 企业品牌下**,个人账号近乎空。

**推断的决策规则(推测)** — 他选择的是**企业品牌 persona 而非个人品牌 persona**:有产出、有署名、有 bio,但全部经 Snyk 品牌门面发布;个人 GitHub 账号仅作 Snyk 雇员标识(`rmcnamara-snyk` 后缀),不沉淀个人 repo/star/social。这与「零 footprint」截然不同——是「把 persona 托管给雇主品牌」。可能动机:雇主资源/渠道复用、个人 opsec、或单纯不维护个人品牌。(可信度:**高** — (a)(b)(c)(d) 四点一致,矛盾的前提已被 Wayback 证伪。)

**推测的边界** — 这种模式依附于 Snyk 渠道:若离开 Snyk,个人账号无沉淀、迁移成本高。这是一种「机构型研究员」选择(类似 P0 研究员依附 Google 品牌),与 Tavis Ormandy「个人博客+个人 Twitter」的个人品牌模式相反。(可信度:**中** — 机构依附性可观察,「主动选择」的内心动机无法取证。)

---

### 7. CNA 行为:不经 Snyk CNA 推 CVE,走上游 CNA

**行为证据(一手,NVD CNA source 取证 2026-07-28)** —

| CVE | NVD CNA source | 归属 |
|---|---|---|
| 21626 / 23651 / 23652 / 23653 / 23953 / 23954 | security-advisories@github.com | GitHub CNA |
| 1753 | secalert@redhat.com | Red Hat CNA |
| 5138 | 134c704f-…(=Ubuntu,security@ubuntu.com) | Ubuntu CNA |
| 23326(Istio) | security-advisories@github.com | GitHub CNA |

**8+1 条 CVE 的 CNA 无一是 Snyk。** Snyk 本身是 CNA,但 Rory 的发现全部由上游项目所属 CNA(GitHub/Red Hat/Ubuntu)分配。

**推断的决策规则(推测)** — 他**不**把发现通过 Snyk 的 CNA 管道「品牌化」领取 CVE,而让上游项目所属 CNA 自然分配。这与维度 4(让上游主笔 GHSA)、维度 5(让上游主导 advisory)高度自洽——一条贯穿始终的决策线索:**CVE 命名权、advisory 主笔权、公开叙事权都留给上游,自己只保留发现者 credit 与 Snyk 技术深度文章**。(可信度:**高** — 8/8 NVD CNA 取证一致 + 23326 同模式。)

**推测含义** — 降低「Snyk 抢 CVE 品牌」观感,对上游关系最友好;Snyk 在 Rory 的披露中扮演雇主/资源支持角色而非 CVE 品牌署名角色。这与 Snyk 作为商业安全公司常态高调的总体风格略有反差,可能是 Rory 个人偏好,也可能是「上游项目有自家 CNA 时默认让上游走」的行业惯例。(可信度:**中** — 雇主内部角色与动机无法取证。)

---

### 8. (其他发现的决策模式)研究产出工具化

**行为证据(一手)** — 每个主要研究弧线都**伴随开源工具交付**:
- Leaky Vessels:`snyk/leaky-vessels-static-detector` + `snyk/leaky-vessels-dynamic-detector`(eBPF)——静态+动态双检测器;
- GitHub Actions:`snyk-labs/github-actions-scanner`(CLI 扫描器 + PoC 生成器模板);旧版 05-decisions 引述其工具设计动机:"Auto creation of a copy of the target repo…to avoid affecting the actual code and the risk of exposing the issue before it was responsibly disclosed"(把 responsible disclosure 写进工具设计)。
- Incus:NVD references 含 PoC 脚本 + patch 双附件(`environment_newline_injection.sh`/`.patch`、`template_arbitrary_write.sh`/`.patch`)。

**推断的决策规则(推测)** — 他默认**把研究产出工具化**:不只发文章,必发检测器/扫描器/PoC,让 maintainer 与用户可自查、可验证。研究交付物 = writeup + 工具 + PoC 三件套。(可信度:**高** — 三条研究弧线均如此。)

---

### 9. (其他)2024→2026 写作类型转向:从 CVE 披露型到教育/参考型

**行为证据(一手)** — Snyk 贡献者页文章列表演化(2024-02-25 vs 2026-07-22 快照对比):
- **2024**:Leaky Vessels 系列 + Istio + GHA——全部 CVE 披露型/技术深度型。
- **2026**:Safe Path Handling(教育 TOCTOU)+ AI Glossary + AWS security guide + Top 10 acronyms + threat intelligence deep dive——**教育/glossary/buyer's guide 型**,无新 CVE 披露文章。
- 时间窗:2024-06(GHA)后,贡献者页无新 CVE-type 披露文章;2025-01 的 snapd(5138)与 2026-01 的 incus(23953/23954)虽有 CVE,但**未见对应 Snyk 博客 writeup**(待证)。

**旁证**(旧版 05-decisions):Snyk 披露页声明「pausing the acceptance of external vulnerability disclosures for open source projects」;2026 Snyk 博客列表几乎全 AI/agentic 主题。

**推断的决策规则(推测)** — 他的公开写作类型随 Snyk 公司战略(2026 全面 AI 化)+ 外部 OSS 披露暂停政策**转向教育/参考型**;CVE 产出可能转内部或仅经 GHSA 不写博客。但此转向是**跟随公司**还是**个人选择**,无法分离。(可信度:**中** — 转向事实可观察,动机混合无法分离。详见矛盾§4。)

---

## 决策启发式总结(可提炼的几条规则)

从上述 9 个决策维度,可提炼贯穿一致的几条**决策启发式**(均为推测,基于行为反推;启发式 2 含自述):

1. **race-condition / TOCTOU 锚定律**:以「race conditions + Linux exploitation」(bio 自述)为研究锚点,载体选容器运行时/构建器/中间件这类「边界对象在并发/生命周期上易出缺口」的层;不按 CWE 标签找,而按「边界对象时序完整性不变量被遗忘」找。
2. **批量协调同日律**:同一审计周期内发现的相关边界缺陷打包、同日、协调发布(Leaky Vessels 4 同日、Incus 2 同日);单点缺陷或下游部署链长的(如 Envoy)可留部署窗口。窗口长度随「下游部署复杂度」调整。
3. **让上游主笔 + 自写技术深度律**:合并披露,上游 maintainer 主导 GHSA/advisory/oss-security 叙事,上游 CNA 分配 CVE;自己保留 Snyk 博客技术深度文章主笔权。命名权与叙事权分离。
4. **三段式披露通道律**:GHSA 私有协调(上游发补丁)→ Snyk 博客技术 writeup(自己主笔,补丁同日或留窗口)→ 开源工具(detector/scanner)赋能 maintainer 与用户自查。研究交付 = writeup + 工具 + PoC 三件套。
5. **企业品牌 persona 律**:有产出、有署名、有 bio,但全部经 Snyk 品牌门面;个人 GitHub 账号仅作雇员标识,不沉淀个人 repo/social。persona 托管给雇主品牌,而非个人品牌。

这 5 条高度自洽:race-condition 锚定→批量协调→让上游主笔+自写深度→三段式通道→企业品牌 persona,构成「深挖、打包、交权给上游、自己写技术深度、托付企业品牌」的完整决策链。

---

## 与同行决策模式对比(Tavis Ormandy / Jann Horn / Rory 的独特性)

- **Tavis Ormandy**:**个人品牌** persona(个人博客、oss-security 自署名帖、Twitter),目标域极广(CPU 微码、AV 引擎、内核、云、密码库),常单独披露并自写 writeup。**广域 + 个人品牌 + 独立。**
- **Jann Horn**:**机构品牌(P0)** persona,产出详尽公开 writeup,目标跨浏览器/内核/sanitizer,以体系化技术深度见长,固定 90 天 deadline 制度驱动。**广域 + 机构品牌 + 制度驱动。**
- **Rory McNamara 的独特性**:(a) **企业品牌 persona**(Snyk),非个人品牌(Tavis)亦非纯机构研究集体(P0);(b) **窄锚点**(race-condition/TOCTOU 为 bio 自述焦点),载体虽以容器生态为主(9/9)但外扩到 HTTP 中间件/CI/CD,比 Tavis/Jann 的广域更聚焦;(c) **一贯合并披露 + 上游 CNA**,从不抢 CVE 命名权,与 Tavis 常自署名 oss-security 形成对照;(d) **研究产出强制工具化**(每弧线配 detector/scanner),Tavis/Jann 不必然如此。Rory 模式可概括为「race-condition 锚定 + 企业品牌托管 + 上游交权 + 工具化交付」,在三者中独此一家。

---

## 矛盾与未解之处

1. **任务初始前提与 Wayback 实证的冲突(已解决,记录在此)** — 任务上下文断言「Snyk 作者页全 404 / Wayback snyk.io 含 leaky/vessel/21626 的 URL = 0 条 / 零公开 footprint」。Wayback CDX 显示 `snyk.io/contributors/rory-mcnamara/` 有 **18 个快照**(2024-02-25 ~ 2026-07-23);直接 fetch 具体快照 URL 返回 Rory 署名的 Leaky Vessels 文章正文。**结论**:任务前提的「零 footprint」不准确,Rory 有企业品牌下的丰富公开产出。本文件已据此重写维度 5、6。**未解**:任务前提为何如此断言——可能任务编写者所用 CDX 通配模式未命中(`snyk.io/blog/*leaky*` 返回 0 但具体快照存在),或误把「live 页面当前 404」当成「从未存在」。
2. **头衔不一致** — 2024-02-25 快照 HTML `<title>` = "Rory McNamara - **Staff Research Engineer**, Snyk | Snyk";2026-07-22 快照 JSON-LD `title` = "**Staff Security Researcher**"。两字段不一。可能:头衔在 2024→2026 间变更,或 HTML title 与 JSON-LD title 字段口径不同。无法仅凭两快照判定。(旧版 05-decisions 已记录此点,本文件保留。)
3. **CVE-2024-23326(Istio)的 Rory 个人 credit 未确认** — NVD 该 CVE references 仅 2 条,均指 envoy GHSA,**未点名 Rory**;Snyk 博客用「we」(Snyk 团队)自述。Rory 是 sole author of Snyk Istio 文章,但是否为该 CVE 的官方 credit reporter,未经 NVD/GHSA 确认(GHSA API 限额耗尽,未复核 credits 字段)。该 CVE 也不在任务给的 9 条 credit 列表中。**未解**:Istio 是 Rory 独家发现、Snyk 团队发现、还是他人发现 Rory 仅写文章?
4. **2024→2026 写作转向动机混合** — 从 CVE 披露型转向教育/glossary 型的事实可观察,但动机(公司 AI 战略?外部披露暂停政策?个人转向?)无法分离。旁证(Snyk 披露页「pausing external OSS disclosures」、2026 博客全 AI 化)指向公司层面,但 Rory 个人是否主动转向未确认。
5. **bio 出现时间** — 2024-02-25 快照无 bio 短语(grep "passionate"/"bug bounty"/"pentester"/"linux exploitation" 全空,仅 JSON-LD `description` = "Content contributed by Rory McNamara");2026-07-22 快照含完整 bio。bio 在 2024-02-25 后某时点添加。**未解**:添加时间与头衔变更是否同步,无法判定。
6. **severity 记录差异** — 任务上下文记录 1753 与 5138 为 Medium,但 NVD baseScore 分别 8.6/8.1(HIGH)。可能是 GHSA severity(GitHub 自有评分)与 NVD severity 口径不同。不影响决策模式推断,记录备查。

---

## 信息不足之处(所有决策都是行为反推,无本人声明)

1. **无本人方法声明(部分例外)** — 决策维度 1、2 有 bio 自述("passionate about race conditions and Linux exploitation")与文章命名("race condition container breakout")作为一手自述佐证;其余维度(3 时机、4 协作、5 通道、6 persona、7 CNA、8 工具化、9 转向)均为行为反推,无采访/演讲/邮件声明。
2. **GHSA API 未独立复核** — GitHub 未鉴权 API 限额 60/小时在调研中耗尽,GHSA 的 `published_at`、`credits`、`affected_package` 字段未能经 `api.github.com/advisories/<GHSA>` 独立复核。采用任务上下文已核实值,并与 Wayback 文章 `publishDate` + NVD references(上游 release tag / oss-security 帖日期)交叉验证一致。如需独立复核,需鉴权 token 或等待限额重置(epoch 1785218379)。
3. **Istio CVE 个人 credit** — 见矛盾§3,GHSA credits 字段未复核。
4. **pre-Snyk 雇主与教育** — LinkedIn `uk.linkedin.com/in/rorymcnamara` 返回 HTTP 999(反爬),Wikipedia 不列个人研究员。bio 仅笼统 "ex-pentester, AppSec engineer, bug bounty hunter",未命名前雇主或学校。UK 域提示英国背景,不可深查。
5. **会议演讲** — Black Hat(`www.blackhat.com` 403)、KubeCon、DockerCon、RSA 均未在可访问渠道核实到 Rory 演讲记录。
6. **协作发起方** — Leaky Vessels 与 Incus 的合并披露中,Rory 是主动联系上游合并还是上游主动联系他,无法从公开记录区分。
7. **转向动机** — 见矛盾§4,公司战略 vs 个人转向无法分离。
8. **时间空白** — 2024-06(GHA)到 2025-01(snapd)约 7 个月、2025-01 到 2026-01(incus)约 12 个月无 Snyk 博客 writeup(但 snapd/incus 有 GHSA credit)。是研究周期长、有未公开发现、还是转向内部工作,无法取证。
9. **snyk.io 实时可达性** — 本调研经 Wayback 取证历史内容,未尝试 live fetch snyk.io(任务上下文称 live 作者页 404)。若 live 页当前 404 而 Wayback 有快照,说明内容曾被下线——但下线时间与原因不在本调研范围。

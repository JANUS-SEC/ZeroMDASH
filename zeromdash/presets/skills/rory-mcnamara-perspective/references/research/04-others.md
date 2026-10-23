# Rory McNamara — 他者视角维度

> 调研主题:安全社区、媒体、上游维护者如何谈论/归功于 Snyk 安全研究员 Rory McNamara。
> 核心事件:Leaky Vessels(CVE-2024-21626 runc + CVE-2024-23651/52/53 buildkit,2024-01-31 公布)是唯一引发主流媒体关注的契机;其余 CVE 仅在 GHSA 层面有 credit。

---

## 调研方法

1. **HN Algolia API**(`hn.algolia.com/api/v1/search`):检索 "leaky vessels" / "CVE-2024-21626" 的 story 与评论,可返回 JSON。
2. **NVD REST API**(`services.nvd.nist.gov/rest/json/cves/2.0`):抓取 CVE-2024-21626、CVE-2024-5138 的描述、references、credits 字段。
3. **GitHub Security Advisory 页面**:对 9 个 GHSA(runc/buildkit×3/podman/buildah/snapd/incus×2)逐一用 WebFetch 抓取 `github.com/<org>/<repo>/security/advisories/<GHSA>` 的 Credits 段。
4. **oss-security 邮件列表**(`www.openwall.com/lists/oss-security/`):用 curl 抓取 Leaky Vessels 公告原帖(/2024/01/31/6,Aleksa Sarai 署名)与 Solar Designer 回帖(/2024/02/01/1)。
5. **媒体原文**:
   - BleepingComputer / The Hacker News / Wiz blog / Krebs 经 `web.archive.org` CDX API 找到归档快照后,curl 抓取 `web.archive.org/web/<ts>/<url>` 的存档正文。
   - Snyk 官方博客(labs.snyk.io)WebFetch 反复 60s 超时,改用 web.archive.org 2025-06-01 快照 curl 抓取正文。
   - Ars Technica / The Verge / The Register / ZDNet 经 CDX 检索,无 Leaky Vessels 归档 → 判定未覆盖。
6. **厂商公告**:Red Hat(`access.redhat.com/security/cve/CVE-2024-21626`)、Ubuntu(`ubuntu.com/security/CVE-2024-21626`)经 web.archive.org 快照抓取,搜索 credit/acknowledgement/reporter/Snyk/Sarai 关键词。Debian 经 `lists.debian.org` 抓取 DLA-3735-1。
7. **Reddit**:`www.reddit.com/r/netsec/search.json` 经 curl(多个 User-Agent)均返回非 JSON(反爬),该维度信息不足。

可信度标记:**一手** = 直接抓到原文/原帖/官方页面;**二手** = 转述;**推测** = 我基于证据的推断(会显式标注)。

---

## 媒体报道(Leaky Vessels 为主)

### 1. BleepingComputer — "Leaky Vessels flaws allow hackers to escape Docker, runc containers"
- 日期/URL:归档快照 2024-02-04,`https://www.bleepingcomputer.com/news/security/leaky-vessels-flaws-allow-hackers-to-escape-docker-runc-containers/`(原文 `https://www.bleepingcomputer.com/news/security/leaky-vessels-flaws-allow-hackers-to-escape-docker-runc-containers/`)
- 是否提及 Rory McNamara:**是(全名)**
- 原文引用(逐字,web.archive.org 抓取):
  > "The flaws were discovered by **Snyk security researcher Rory McNamara** in November 2023, who reported them to impacted parties for fixing. Snyk has found no signs of active exploitation of the Leaky Vessels flaws in the wild..."
- 另一处:"the patching of the 'Leaky Vessels' vulnerabilities involved coordinated actions among the security research team at **Snyk**, the maintainers of the affected components (runc and BuildKit), and the broader container infrastructure community."
- 可信度:**一手**(归档正文逐字抓取)

### 2. The Hacker News — "New Leaky Vessels Flaws Enable Container Escapes, Granting Attackers Host Access"
- 日期/URL:归档快照 2024-01-31,`https://thehackernews.com/2024/02/runc-flaws-enable-container-escapes.html`
- 是否提及 Rory McNamara:**否**。全文 grep `Rory`/`McNamara`/`Sarai`/`cyphar`/`researcher`/`discovered` 关键词,**Rory 与 McNamara 零命中**。
- 归因方式:全部归功于 **"cybersecurity vendor Snyk"** 品牌,反复引用 "**Snyk** said":
  > "...have been collectively dubbed Leaky Vessels by cybersecurity vendor **Snyk**. 'These container escapes could allow an attacker to gain unauthorized access to the underlying host operating system from within the container...'" — Snyk said.
  > "**Snyk** strongly recommends that users check for updates from any vendors providing their container runtime..."
- 可信度:**一手**(归档正文逐字抓取)。这是"去人格化归功于 Snyk 品牌"的典型样本。

### 3. Snyk 官方博客 — "Leaky Vessels: Docker and runc container breakout vulnerabilities (January 2024)"
- 日期/URL:2024-01-31,`https://labs.snyk.io/resources/leaky-vessels-docker-runc-container-breakout-vulnerabilities/`(原 `snyk.io/blog/...` 308 重定向至此;WebFetch 反复超时,改用 web.archive.org 2025-06-01 快照)
- 作者署名:**Jamie Smith**(Share 按钮旁)。Jamie Smith 疑为 Snyk 内容/编辑人员,**非** Rory 本人。
- 是否提及 Rory McNamara:**是(全名 + 详细披露时间线)**
- 原文引用:
  > "**Snyk security researcher Rory McNamara**, with the Snyk Security Labs team, identified four vulnerabilities — dubbed 'Leaky Vessels' — in core components that allow container escapes."
  > "Timeframe / Item: **Week of 20-Nov-2023 Rory McNamara initially discovered the vulnerabilities.** He began the internal verification process and additional vulnerability discovery."
  > "13-Dec-2023 **Rory was added as a Github Security Advisory (GHSA) collaborator** for the Arbitrary Delete and grpc Docker/Buildkit vulns..."
  > "19-Dec-2023 **Rory was added as GHSA collaborator to WORKDIR by runc**..."
  > "20-Dec-2023 **Rory was added as GHSA collaborator for the cache race vulnerability.**"
- 可信度:**一手**(Snyk 官方发布,归档快照逐字抓取)。这是 Rory 个人贡献最详细的一手记录,但发布署名是 Jamie Smith,体现 Snyk 的"研究 + 内容编辑"分工。

### 4. Wiz 博客 — "Leaky Vessels: Container Escape Vulnerabilities"
- 日期/URL:2024-02-13,`https://www.wiz.io/blog/leaky-vessels-container-escape-vulnerabilities`
- 是否提及 Rory McNamara:**否**。正文 grep `Rory`/`McNamara`/`Sarai`/`cyphar` 零命中。
- 归因方式:在 References 段仅列 "**Snyk blog**" 作为来源之一,不点个人名。全文为技术分析(host 访问、K8s 多租户、WORKDIR gadget),研究者身份不是叙事焦点。
  > "References: **Snyk blog**, Docker advisory, runC advisory, AWS advisory, GCP advisory"
- 可信度:**一手**(归档正文逐字抓取)

### 5. Krebs on Security
- URL:`https://krebsonsecurity.com/?s=leaky+vessels`
- 结果:搜索返回 **"Nothing Found"**。Krebs 未覆盖 Leaky Vessels(与其偏重 breach/crime 报道的定位一致)。
- 可信度:**一手**(curl 抓取搜索页)

### 6. Ars Technica / The Verge / The Register / ZDNet
- 方法:`web.archive.org/cdx` 域级检索 + `filter=original:.*(leaky|runc|21626).*`,时间窗 2024-01-01 至 2024-03-01。
- 结果:**全部零命中**(Ars/The Verge/The Register/ZDNet 均无 Leaky Vessels 归档)。
- 可信度:**一手**(CDX API)。判定:Leaky Vessels 的主流英文媒体覆盖集中于 BleepingComputer + The Hacker News 两家,非大范围报道。

---

## 上游维护者评价(Aleksa Sarai / stgraber / Solar Designer)

### 1. Aleksa Sarai(cyphar,runc 维护者,SUSE)— Leaky Vessels 公告原作者
- 来源:`http://www.openwall.com/lists/oss-security/2024/01/31/6`(Sarai 署名原帖)+ `https://github.com/opencontainers/runc/security/advisories/GHSA-xr7r-f8xq-vfvv`
- 原文引用(oss-security 公告,逐字):
  > "**Credit for discovering and reporting the original vulnerability goes to Rory McNamara from Snyk.** In addition, credit goes to @lifubang from acmcoder and **Aleksa Sarai from SUSE** for discovering how to adapt the attacks in various ways to make them more severe and practical for real SaaS workloads."
- GHSA Credits 段(逐字):
  > "Thanks to **Rory McNamara from Snyk** for discovering and disclosing the original vulnerability (attack 1) to Docker, [@lifubang] from acmcoder for discovering how to adapt the attack to overwrite host binaries (attack 3a), and **Aleksa Sarai from SUSE** for discovering how to adapt the attacks to work as container breakouts using `runc exec` (attacks 2 and 3b)."
- GHSA Reporter 侧栏:`rmcnamara-snyk — Reporter`、`cyphar — Reporter`、`lifubang — Reporter`(三人并列)
- 可信度:**一手**(公告原帖 + GHSA 页面)。**这是最重要的一条同行评价**:Sarai 作为 runc 维护者,在公开公告里**显式且逐字**点名 Rory McNamara 为"原始漏洞的发现与报告者",并把自己和 lifubang 定位为"攻击变体的扩展者"。措辞精确,区分了"发现原漏洞"与"扩展攻击"两个层次。

### 2. Solar Designer(Alexander,oss-security 列表管理员)— 公告回帖
- 来源:`http://www.openwall.com/lists/oss-security/2024/02/01/1`
- 原文引用(逐字):
  > "Hello Aleksa, **Thank you and others you credit** for doing much more than fixing the immediate issue, and for disclosing this in so much detail."
- 可信度:**一手**。注意:Solar Designer **只直接称呼 Aleksa Sarai**,"others you credit"指代 Sarai 公告里的 credit 列表(含 Rory),但**未点名 Rory**。即便在披露邮件列表层面,Rory 也是"经 Sarai 间接 credit"的存在,而非被列表管理员直接点名对话的对象。

### 3. stgraber(Stéphane Graber,Incus 维护者)— Incus 两个 CVE 的修复者
- 来源:`https://github.com/lxc/incus/security/advisories/GHSA-x6jc-phwx-hp32`(CVE-2026-23953)+ `https://github.com/lxc/incus/security/advisories/GHSA-7f67-crqm-jgh7`(CVE-2026-23954),均由 stgraber 于 2026-01-22 发布
- Credits 段(逐字):
  > "**rmcnamara-snyk** — Finder"
  > "**stgraber** — Remediation developer"
- 可信度:**一手**(GHSA 页面)。stgraber 的措辞是程式化的角色标签(Finder / Remediation developer),**未用全名 "Rory McNamara"**,只用 GitHub handle `rmcnamara-snyk`。这是上游 GHSA credit 的常见格式:handle + 角色标签,而非 Sarai 那种散文式点名。stgraber 未在公告正文里发表对 Rory 的额外评价文字。

---

## 厂商安全公告中的 credit(Red Hat / Ubuntu / Canonical / Debian / NVD)

### GitHub Security Advisories(上游维护者层)— 全部 credit rmcnamara-snyk

| GHSA | 项目 | CVE | rmcnamara-snyk 角色 | 其他 credit | 可信度 |
|------|------|-----|---------------------|-------------|--------|
| GHSA-xr7r-f8xq-vfvv | opencontainers/runc | CVE-2024-21626 | Reporter(正文全名 "Rory McNamara from Snyk") | cyphar(Reporter)、lifubang(Reporter) | 一手 |
| GHSA-m3r6-h7wv-7xxv | moby/buildkit | CVE-2024-23651 | Reporter(**仅一人**) | 无 | 一手 |
| GHSA-4v98-7qmw-rqr8 | moby/buildkit | CVE-2024-23652(Critical) | Reporter(**仅一人**) | 无 | 一手 |
| GHSA-wr6v-9f75-vh2g | moby/buildkit | CVE-2024-23653(Critical) | Reporter(**仅一人**) | 无 | 一手 |
| GHSA-874v-pj72-92f3 | containers/podman | CVE-2024-1753 | Finder(**仅一人**) | 无 | 一手 |
| GHSA-pmf3-c36m-g5cf | containers/buildah | CVE-2024-1753(同根因) | Finder(**仅一人**) | 无 | 一手 |
| GHSA-p9v8-q5m4-pf46 | canonical/snapd | CVE-2024-5138 | Reporter(**仅一人**) | 无 | 一手 |
| GHSA-x6jc-phwx-hp32 | lxc/incus | CVE-2026-23953 | Finder | stgraber(Remediation developer) | 一手 |
| GHSA-7f67-crqm-jgh7 | lxc/incus | CVE-2026-23954 | Finder | stgraber(Remediation developer) | 一手 |

观察:
- **9/9 GHSA 全部 credit rmcnamara-snyk**,且 7 个是**唯一**的 Finder/Reporter(buildkit×3、podman、buildah、snapd,以及 runc 里 Rory 是"原始发现"角色)。
- **角色标签分化**:runc 用散文式全名 "Rory McNamara from Snyk";buildkit/podman/buildah/snapd/incus 只用 handle `rmcnamara-snyk` + 角色(Finder/Reporter)。即:**Sarai(runc)是唯一在 GHSA 正文里用 Rory 全名的维护者**;其余维护者用程式化 handle credit。
- **buildah GHSA-pmf3-c36m-g5cf 实为 CVE-2024-1753**(与 podman 同 CVE、同根因,跨 containers/ 两个项目各自发 GHSA),任务上下文里把它列为无 CVE 的独立条目,核实后应更正为 CVE-2024-1753。

### Red Hat
- 来源:web.archive.org 快照 2024-04-18,`https://access.redhat.com/security/cve/CVE-2024-21626`
- 结果:正文 grep `Rory`/`McNamara`/`Snyk`/`Sarai`/`cyphar`/`Credit`/`Acknowledg`/`Reporter`/`Discovered`/`credit`/`SUSE` 关键词,**全部零命中**。
- 可信度:**一手**(归档快照)。Red Hat 公开 CVE 页面**不 credit 外部 reporter**(credit 通常只在内部 RHSA bug 里,公开页不显示)。

### Ubuntu / Canonical
- 来源:web.archive.org 快照 2024-02-27,`https://ubuntu.com/security/CVE-2024-21626`
- 结果:同上关键词搜索,**全部零命中**。snapd 的 CVE-2024-5138 页面(`ubuntu.com/security/CVE-2024-5138`)WebFetch 反复 504 超时,未核实到。
- 可信度:**一手**(CVE-2024-21626 页面归档快照)。Ubuntu 公开 CVE 页面亦**不 credit 外部 reporter**。

### Debian
- 来源:`https://lists.debian.org/debian-lts-announce/2024/02/msg00005.html`(DLA-3735-1,Daniel Leidert 署名)
- 原文:"CVE-2024-21626 A flaw has been detected which allows several container breakouts due to internally leaked file descriptors. The patch includes fixes and hardening measurements..."
- 结果:**无 reporter credit 字段**(Debian LTS 公告惯例不点外部 reporter 名)。
- 可信度:**一手**

### NVD
- 来源:`services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2024-21626` 与 `...CVE-2024-5138`
- 结果:两条 CVE 的 `credits` 字段**均为空**(NVD 不总是回填 reporter credit)。References 列表含 GHSA、oss-security、commit、Debian/Fedora 链,但无 credit 段。
- 可信度:**一手**(NVD REST API)

---

## 社区讨论(Reddit / HN)

### Hacker News
- 来源:`hn.algolia.com/api/v1/items/39250975`(BleepingComputer 提交,63 points,25 comments)+ `.../items/39208725`(Snyk 博客提交,41 points,0 comments)
- 主帖(BleepingComputer)评论统计(逐字 grep 整个评论树):
  - `Rory`/`McNamara`/`Sarai`/`cyphar`/`researcher`/`discovered` 关键词命中数:**全部为 0**
  - `Snyk` 命中 3 次,**全部来自 rdegges**(Snyk 员工 Robert Degges,即提交 Snyk 博客到 HN 的人),内容为"we have a detailed blog post on the Snyk website here: ..."
- 社区讨论基调(逐字摘录代表性评论):
  - `j16sdiz`: "I have seen this for ages and thought it was some design limitation. Didn't attempt to report it as vulneribility ..."
  - `rdegges`(Snyk): "This one is a clear vulnerability -- if you're able to escape a container and access the host system (usually with root access since Docker is running as root most places), that's a big issue"
  - `flaminHotSpeedo`: "Friendly reminder that containers aren't a security control and your threat modeling should already assume the host VM running any untrusted containers is compromised"
  - `tptacek`(Thomas Ptacek): "KVM vulnerabilities are rare compared to Linux kernel LPEs, which makes sense, because KVM is a relatively small part of the Linux kernel..."
  - `px43`: "Last I checked, Docker wasn't considered a security boundary and Docker escapes weren't considered a security issue..."
- 可信度:**一手**(Algolia API JSON)。**模式:HN 社区讨论 100% 聚焦技术/哲学之争(容器是否算安全边界、Docker vs VM、rootless),发现者身份完全不在讨论范围内**。连 j16sdiz "我早见过但没报告"这种与发现过程强相关的评论,也没人追问"那到底是谁报告的"。

### Reddit
- 方法:`www.reddit.com/r/netsec/search.json?q=leaky+vessels&restrict_sr=1`,尝试多个 User-Agent(含浏览器 UA)
- 结果:返回非 JSON(Reddit 反爬),**该维度信息不足**。无法核实 r/netsec 是否有 Leaky Vessels 讨论帖及是否提及 Rory。
- 可信度:**信息不足**(端点被反爬)

---

## 他者视角的总体模式

1. **上游 GHSA 层面:credit 一致且充分。** 9/9 GHSA 全部 credit rmcnamara-snyk,且 buildkit×3、podman、buildah、snapd 这 6 个 CVE 里 Rory 是**唯一**的 Finder/Reporter。这是上游维护者群体对 Rory 贡献的稳定、结构化承认。

2. **媒体层面:品牌化归功于 Snyk 是主流,点名 Rory 是例外。** Leaky Vessels 的英文媒体叙事里:
   - **BleepingComputer 是唯一把 Rory McNamara 当"主角"点全名的主流媒体**("discovered by Snyk security researcher Rory McNamara")。
   - The Hacker News 与 Wiz **去人格化**,把发现归功于 "cybersecurity vendor Snyk" / "Snyk blog",从不点 Rory 个人名。
   - Snyk 自己的博客虽详细点名 Rory 并给出披露时间线,但**发布署名是 Jamie Smith**(内容编辑),而非 Rory 本人署名——呈现"研究归 Rory、对外发声归 Snyk 品牌/编辑"的分工。

3. **"去人格化"有结构性原因(我的推测,显式标注):** Rory 无任何公开 persona(无 blog/Twitter/repo/starred,GitHub `rmcnamara-snyk` 账号 2023-07-09 创建、无公开活动)。媒体没有"个人"可指向,只能 fallback 到雇主品牌 Snyk。这与 Snyk 作为"vendor"的市场发声路径(Snyk 博客 → 媒体转载)互相强化。

4. **披露邮件列表层面:Rory 是"经协调人间接 credit"的存在。** oss-security 公告的署名作者/协调人是 Aleksa Sarai(cyphar),Rory 是 Sarai 在公告正文里 credit 的对象;列表管理员 Solar Designer 只直接对话 Sarai("you and others you credit"),不直接点名 Rory。即:在公开披露的"前台",Sarai 是 face,Rory 在 credit 列表里。

5. **社区讨论完全去人格化。** HN 25 条评论零次提及任何研究者姓名,100% 聚焦技术辩论。发现者身份对社区话语几乎不存在。

6. **下游厂商公告不 credit 外部 reporter。** Red Hat / Ubuntu / Debian / NVD 的公开页面均无 reporter credit 字段;credit 只活在**上游 GHSA** 这一层。若只看下游公告,完全看不到 Rory 的存在。

7. **媒体只关心"大事件",后续 CVE 零覆盖。** Rory 在 2024-02 之后还贡献了 snapd(CVE-2024-5138)和 incus(CVE-2026-23953/54,2026-01)等 CVE,GHSA 全部 credit 他,但**这些后续 CVE 无任何主流媒体报道**(BleepingComputer/The Hacker News/Wiz/Krebs 均无)。媒体叙事的"主角光环"只属于 Leaky Vessels 这一次事件。

---

## 矛盾与未解之处

1. **"发现者"的层次矛盾(已澄清,非真矛盾):** Snyk 博客说 "Rory McNamara initially discovered the vulnerabilities"(Week of 20-Nov-2023);Sarai 公告说 "Credit for discovering and reporting the **original** vulnerability goes to Rory McNamara from Snyk",自己与 lifubang 是"adapting the attacks"。两者一致:Rory 发现了原始 fd-leak 种子漏洞,Sarai/lifubang 把它扩展成完整 container breakout 链。但**媒体(The Hacker News)把这层次抹平,只说 "dubbed Leaky Vessels by Snyk"**,把 Sarai 的攻击扩展工作也一并归给 Snyk 品牌——这是媒体叙事对原始 credit 层次的失真。

2. **Snyk 博客署名 Jamie Smith vs. 内容归 Rory:** Snyk 官方 Leaky Vessels 博客的 byline 是 Jamie Smith,但正文反复以第三人称描述 "Rory McNamara ... discovered"。Jamie Smith 的身份(Snyk 员工?外部撰稿?comms?)未核实——**此维度信息不足**。这强化了"Rory 不亲自对外发声、由 Snyk 内容团队代笔"的模式,但 Jamie Smith 与 Rory 的具体关系未解。

3. **Solar Designer 的 "others you credit" 指代:** Solar Designer 只点名 Sarai,"others you credit" 是否精确指 Rory + lifubang?从 Sarai 公告的 credit 段看是,但 Solar Designer 未亲自点名,存在"列表管理员只认协调人"的惯性。**非矛盾,但体现 Rory 在邮件列表层面的"二级存在"。**

4. **snapd/incus CVE 的媒体沉默 vs. GHSA credit 充分:** Rory 在 snapd(CVE-2024-5138,2024)、incus(2026-23953/54)的 GHSA 全部被 credit 为 Finder/Reporter,但**零媒体覆盖**。这是"媒体只追 Leaky Vessels 大事件"与"上游持续 credit"之间的落差,非矛盾但值得记录。

---

## 信息不足之处

1. **Reddit r/netsec 与 r/security 讨论**:Reddit JSON 端点反爬,无法核实社区是否讨论 Rory 或如何归功。Leaky Vessels 必有 Reddit 讨论帖,但内容未取到。
2. **Jamie Smith(Snyk 博客署名人)身份**:未核实其是否为 Snyk 员工、comms 编辑或外部撰稿;Snyk 作者页 404,无法交叉验证。
3. **Ubuntu CVE-2024-5138(snapd)页面 credit**:WebFetch 反复 504,未核实 Canonical 是否在 snapd 公告里 credit Rory。考虑到 Ubuntu CVE-2024-21626 页面已确认无 credit 字段,snapd 页面大概率同样无 credit,但未直接证实。
4. **Red Hat RHSA 内部 bug 的 credit**:Red Hat 公开 CVE 页无 credit,但 RHSA bug(如 RHSA-2024:0825 等)的 comment 里可能 credit Rory——需 Red Hat 登录或 Bugzilla 抓取,本次未做。
5. **Rory 在 Snyk 的职级/团队归属**:任务上下文给 "Staff Security Researcher",但 Snyk 官方未在 Leaky Vessels 博客里写明其职级(只写 "Snyk security researcher")。Staff 职级未在本次他者视角来源中独立证实。
6. **runc/buildkit 维护者邮件列表(非 oss-security)对 Rory 的评价**:Sarai 的公开 credit 已取,但其他 runc/buildkit maintainer(如 Akihiro Suda、Tianon Gravi 等)是否在 issue/PR 里评价 Rory,未检索。
7. **播客/视频(BlackHat/USENIX/YouTube/Podchaser)**:这些平台在 curl 白名单内但搜索页需 JS,未深入抓取。Rory 无公开演讲记录的可信度未独立验证。

---

## 数据来源索引(全部 URL)

**一手原文**
- oss-security Sarai 原公告:`http://www.openwall.com/lists/oss-security/2024/01/31/6`
- oss-security Solar Designer 回帖:`http://www.openwall.com/lists/oss-security/2024/02/01/1`
- runc GHSA:`https://github.com/opencontainers/runc/security/advisories/GHSA-xr7r-f8xq-vfvv`
- buildkit GHSA×3:`https://github.com/moby/buildkit/security/advisories/GHSA-m3r6-h7wv-7xxv`、`.../GHSA-4v98-7qmw-rqr8`、`.../GHSA-wr6v-9f75-vh2g`
- podman GHSA:`https://github.com/containers/podman/security/advisories/GHSA-874v-pj72-92f3`
- buildah GHSA:`https://github.com/containers/buildah/security/advisories/GHSA-pmf3-c36m-g5cf`
- snapd GHSA:`https://github.com/canonical/snapd/security/advisories/GHSA-p9v8-q5m4-pf46`
- incus GHSA×2:`https://github.com/lxc/incus/security/advisories/GHSA-x6jc-phwx-hp32`、`.../GHSA-7f67-crqm-jgh7`
- NVD API:`https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2024-21626`、`...CVE-2024-5138`
- Debian DLA-3735-1:`https://lists.debian.org/debian-lts-announce/2024/02/msg00005.html`
- Red Hat CVE(归档):`https://web.archive.org/web/20240418121332/https://access.redhat.com/security/cve/CVE-2024-21626`
- Ubuntu CVE(归档):`https://web.archive.org/web/20240227104300/https://ubuntu.com/security/CVE-2024-21626`
- BleepingComputer(归档):`https://web.archive.org/web/20240204160255/https://www.bleepingcomputer.com/news/security/leaky-vessels-flaws-allow-hackers-to-escape-docker-runc-containers/`
- The Hacker News(归档):`https://web.archive.org/web/20240131204430/https://thehackernews.com/2024/02/runc-flaws-enable-container-escapes.html`
- Snyk 博客(归档):`https://web.archive.org/web/20250601113337/https://labs.snyk.io/resources/leaky-vessels-docker-runc-container-breakout-vulnerabilities/`
- Wiz 博客(归档):`https://web.archive.org/web/20240213215157/https://www.wiz.io/blog/leaky-vessels-container-escape-vulnerabilities`
- Krebs 搜索:`https://krebsonsecurity.com/?s=leaky+vessels`
- HN Algolia:`https://hn.algolia.com/api/v1/items/39250975`、`https://hn.algolia.com/api/v1/search?query=leaky%20vessels`
- CDX API:`https://web.archive.org/cdx/search/cdx`(多次查询)

**信息不足**
- Reddit:`https://www.reddit.com/r/netsec/search.json?q=leaky+vessels&restrict_sr=1`(反爬,未取到)
- Ubuntu CVE-2024-5138:`https://ubuntu.com/security/CVE-2024-5138`(504 超时)

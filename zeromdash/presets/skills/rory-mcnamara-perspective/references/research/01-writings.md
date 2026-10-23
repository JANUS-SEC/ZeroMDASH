# Rory McNamara — 著作维度

> 调研对象:Rory McNamara,GitHub `rmcnamara-snyk`(https://github.com/rmcnamara-snyk),Snyk Staff Security Researcher(亦见 `psychomario` 账号)。
> 调研日期:2026-07-28。
> 本文件聚焦「著作维度」——所有可核实的、由他本人产出的书面文字(advisory 文本、PoC 脚本、commit、博客、README 等)。

---

## 调研方法

| 来源类型 | 工具/途径 | 结果与可信度 |
|---|---|---|
| Snyk 贡献者页(live) | WebFetch `https://snyk.io/contributors/rory-mcnamara/` | **成功**。拿到 bio 原文 + 5 篇署名文章清单 ✓ 一手(byline) |
| Snyk 博客作者页 | 原任务给定 `snyk.io/blog/author/{rory-mcnamara,...}/` | **确认全 404**(该路径不存在)。⚠ 但 `/contributors/rory-mcnamara/` 不同,可用——见"矛盾" |
| Wayback CDX | `curl web.archive.org/cdx/search/cdx?url=snyk.io/contributors/rory-mcnamara` | 15 个快照(2024-02-25 ~ 2026-07-22),证明该页长期存在并归档 ✓ |
| Wayback CDX labs.snyk.io | `curl .../cdx?url=labs.snyk.io/resources/*` | 100+ 快照,含 `abusing-ubuntu-root-privilege-escalation`、`leaky-vessels-...`、`4-hidden-ai-coding-risks-and-...` ✓ |
| 前序调研档案(Wayback 全文) | 本仓库 `01-writings.md` 旧版本(2026-07-28 早会话) | 抓回 Leaky Vessels deep-dive、Ubuntu privesc、Leaky Vessels 摘要公告三篇全文 + 引文 ✓ 一手(byline),**本会话未独立复核 labs 文本**(见信息不足) |
| GitHub Security Advisory(runc) | WebFetch `github.com/opencontainers/runc/security/advisories/GHSA-xr7r-f8xq-vfvv` | **成功**。确认 published by `cyphar`(Aleksa Sarai,SUSE);Rory 仅列为 reporter(attack 1)✓ |
| GitHub Advisories API(api.github.com/advisories/<GHSA>) | curl 9 个 GHSA | **全部 HTTP 403**(unauthenticated rate limit)。无法取 description/`submitted_by` 字段 ⚠ |
| advisory-database 镜像 | curl `raw.githubusercontent.com/github/advisory-database/main/advisories/github-reviewed/YYYY/MM/<GHSA>.json` | **全部 HTTP 404**(路径不匹配)。未取到 JSON ⚠ |
| GitHub 搜索(commits) | curl `api.github.com/search/commits?q=author:rmcnamara-snyk` | **成功**。14 条公开 commit,作者邮箱 `rory.mcnamara@snyk.io` ✓ 一手 |
| GitHub 搜索(issues/commenter) | curl `api.github.com/search/issues?q=commenter:rmcnamara-snyk` | **成功**。2 条(均 snyk-labs/github-actions-scanner,他被 assign,非他亲开)✓ |
| Incus PoC 脚本 | curl `github.com/user-attachments/files/24473599/template_arbitrary_write.sh` | **成功**。1751 字节,完整内容 ✓ 一手(代码) |
| Incus 修复 patch | curl `github.com/user-attachments/files/24473601/templates_arbitrary_write.patch` | **成功**。3833 字节,完整 diff ✓ 一手(代码) |
| NVD CVE-2024-23326 | curl `services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2024-23326` | **成功**。结果为 Envoy(envoyproxy/envoy)请求走私,GHSA-vcf8-7238-v74c。**与 Rory 无可核实关联**——推翻"可能是他的"的提示 |
| oss-security 邮件 | openwall 不在 curl 白名单 | 未本会话抓取。依原任务上下文采信:Leaky Vessels 主帖由 Aleksa Sarai 署名,Solar Designer 回帖感谢 "you and others you credit",Rory 未署名发帖 |

**可信度分层**(本文统一标注):
- **一手(byline)**:文章页/贡献者页本身署名 "Rory McNamara"
- **一手(代码)**:他本人 commit 的代码/脚本/patch(commit author email = rory.mcnamara@snyk.io,或 PoC 挂在 GHSA references 内)
- **一手(commit message)**:commit message 文本
- **一手(research credit)**:GHSA 将漏洞 credited/reporter 给 Rory(但公告正文文本不一定由他写)
- **二手**:他人文章/公告转述或描写他的发现
- **推测**:据语境推断、未直接核实

---

## 著作清单(按可信度分级)

### 一手(他本人产出)

#### A. Snyk 贡献者页 bio(一手 byline)
- URL:`https://snyk.io/contributors/rory-mcnamara/`(live,2026-07-28 复核通过;Wayback 15 快照 2024-02-25 ~ 2026-07-22)
- 原文 bio:**"Long-time bug bounty hunter, ex-pentester, and AppSec engineer. Rory is passionate about race conditions and Linux exploitation."**
- 原文 byline:**"Rory McNamara — Staff Security Researcher, Snyk"**
- 自述"热衷于 race conditions 与 Linux 利用",与他后续 CVE 组合(buildkit 竞争 CVE-2024-23651、容器逃逸系列、Incus 文件系统操纵)高度自洽。

#### B. Snyk 博客 5 篇署名文章(一手 byline,经贡献者索引归属)
贡献者页列出 "Showing 1 - 5 of 5 records"(本会话 WebFetch 复核):

1. **Safe Path Handling: Why Secure Filesystem Operations Are Harder Than You Think**(2026-03-31)— `https://snyk.io/articles/safe-path-handling/`
   - 合著:"Written by Stephen Thoemmes and Rory McNamara"(据前序档案)
   - 论点:基于路径的文件系统操作天然脆弱(路径穿越 / 符号链接 / TOCTOU);标准库 I/O "为方便而非对抗性环境设计"。解法:fd-based 操作 `openat()` + `O_NOFOLLOW` 逐组件遍历,后续走 `fstat`/`fchmod`/`fchown`。
   - 方法论:漏洞类抽象 → 跨语言生态复现 → 语言级解法矩阵(C/C++、Go 1.24+ `os.OpenRoot`、Rust `cap-std`、Python `dir_fd`、Node.js "基本不可能")→ 真实案例(Incus 符号链接→root、NixOS 竞争、Ubuntu 24.04 privesc)。
   - 引文(前序档案):*"The standard library file I/O functions that most languages provide were designed for convenience, not for adversarial environments."* / *"once you have an open file descriptor, it refers to a specific filesystem object regardless of what happens to the path."*
   - 注:此文 2026-03 发布,与 Incus 修复 commit(2026-01-17,见 F)在时间与方法论上完全自洽——Incus 修的就是 `os.OpenRoot` 路径安全化。

2. **AI Glossary**(2023-11-29)— `https://snyk.io/articles/ai-security/ai-glossary/`
   - 贡献者索引归 Rory,但文章页无个人 byline,是 Snyk 公司页。**标注"贡献者索引归属,byline 未独立核实"。** 词条型,无个人分析声音,对思维风格贡献度低。

3. **AWS security: Complete guide to Amazon cloud security**(2022-10-17)— `https://snyk.io/articles/aws-security/`
   - "Written by Rory McNamara"。通识/营销型,体现早期(2022)AppSec 教育内容风格。引文(前序档案):*"AWS security is the comprehensive protection of the infrastructure, data, applications, and workloads related to Amazon's public cloud platform."*

4. **Top 10 application security acronyms**(2021-08-22)— `https://snyk.io/articles/application-security/glossary-acronyms/`
   - "Explaining common AppSec acronyms" by Rory McNamara(前序档案)。词条型 glossary。

5. **A deep dive into cyber threat intelligence**(2021-06-29)— `https://snyk.io/articles/threat-intelligence/`
   - "Written by Rory McNamara"。通识型。引文(前序档案):*"Since the cost of security incidents are too great for businesses to take a reactive approach, threat intelligence enables organizations to stay a step ahead of malicious actors."*

> 5 篇中署名栏明确写 "Written by Rory McNamara" 的至少 4 篇(1/3/4/5);第 2 篇索引归属但无个人 byline。早期 3 篇(2021-2022)科普/营销型,2026 才出现签名式深度技术分析。**写作成熟度有明显时间演化。**

#### C. labs.snyk.io 深度研究文(一手 byline,经 Wayback 归档;前序档案引文)
- **C1. Abusing Ubuntu 24.04 features for root privilege escalation** — `https://labs.snyk.io/resources/abusing-ubuntu-root-privilege-escalation/`(CDX 16+ 快照 2025-06-18 ~ 2026-05-22)
  - 署名:据前序档案 Wayback 全文确认 "Rory McNamara Share"。**本会话 labs.snyk.io WebFetch 超时,未独立复核署名文本。**
  - 论点:Ubuntu 24.04 默认桌面从普通用户提权到 root,无需内核内存破坏——"一个特权组件里的小 bug + 一堆按预期工作的特性"链起来。明确表态 "keep it simple"。
  - 方法论:开篇即问 "Where are the privilege boundaries?" → 跳过 setuid/坏文件权限/Unix socket,首选 DBus → d-feet/D-Spy 枚举 → 找 `org.opensuse.CupsPkHelper` → 读 Polkit JS 规则(`/usr/share/polkit-1/rules.d/com.ubuntu.desktop.rules`)发现 `lpadmin`/`sudo` 组免密 → 把 AppArmor 同时当"救星"和"内鬼" → cups 符号链接 + wpa_supplicant pivoting 完成 root → 完整 `exploit.sh` 终端转录(uid 1000→0)→ Timeline + Mitigations。
  - 引文(前序档案,本会话未复核):*"Whenever I'm looking at something new, especially for privilege escalation vulnerabilities, my first thought is always, 'Where are the privilege boundaries?'. This is not a novel place to start, but I find it is always very useful to define what specific thing it is I'm trying to break."* / *"you can keep it simple when it comes to exploitation and achieve the same results without needing a very complex (although extremely cool) kernel memory corruption vulnerability"* / *"we chained one small bug in a privileged component together with a number of features, which all work as expected, to achieve arbitrary command execution as root"*

- **C2. Leaky Vessels deep dive: Escaping from Docker one syscall at a time**(2024-02-06)— `https://labs.snyk.io/resources/leaky-vessels-container-vuln-deep-dive/`
  - 署名:据前序档案 Wayback 全文确认 "Rory McNamara Share"。**本会话未独立复核。**
  - 论点:Docker 引擎在 userland Linux 上有可被竞争条件打破的隔离;四个高危漏洞让恶意 Dockerfile 在 `docker build` / 一次 `docker run` 下逃逸。核心工具 `strace`,核心理念"不需要昂贵复杂工具"。
  - 方法论(他最完整展示):① toy C 程序 + `strace` 讲清"什么是竞争条件" ② `strace -tt` 定位 TOCTOU 窗口 ③ 把竞争框定为 "confused deputy" ④ signal injection 验证假说 ⑤ 逐 CVE 复盘 "Initial exploration → We have a lead → Validating → Building a PoC" ⑥ 结尾独立 "How to not write race conditions" 一节。
  - 引文(前序档案,本会话未复核):*"If you've read some of my previous work you may know that I love the strace tool."* / *"Race conditions are a vulnerability class that occurs when an application interacts with a shared system, assuming its actions occur as expected and are free from interference."* / *"the Docker engine could be tricked into performing actions with a higher privilege than are usually accessible — a 'confused deputy' of sorts."* / *"strace can only show you what is happening, not what can happen. It's still necessary to deeply understand the system being investigated."*
  - 涉及 CVE:**CVE-2024-21626**(runc process.cwd + 泄漏 fd;小节"You're out of order")、**CVE-2024-23652**(BuildKit teardown arbitrary delete;小节"Plenty of time")、**CVE-2024-23651**(BuildKit mount cache race;小节"Race to the source")、**CVE-2024-23653**(BuildKit GRPC SecurityMode privilege check)。

#### D. Incus PoC 脚本(一手代码,本会话抓到全文)
- URL:`https://github.com/user-attachments/files/24473599/template_arbitrary_write.sh`(HTTP 200,1751 字节)
- 关联:Incus GHSA-7f67-crqm-jgh7 / CVE-2026-23954(容器镜像 templating 任意宿主文件读写,Rory credited)
- 结构特征:
  - `#!/bin/sh`,`mktemp -d` 建工作目录
  - heredoc 内联构造恶意 `metadata.yaml`:把 `template` 字段设成 `../../../../../../../../etc/shadow` 做路径穿越,以及 `/realroot/proc/sys/kernel/core_pattern` 做容器逃逸
  - 阶段化标注:`echo "POC 1/2: Arbitrary File Read"` 与 `echo "POC 2/2: Container Escape"`
  - 收尾清理:`rm -rf ${BUILDDIR}`、`incus image delete poc`、`echo "Repairing core_pattern"; echo core | sudo tee /proc/sys/kernel/core_pattern`
- 可信度:一手(代码)。挂在他报告的 GHSA references 内,与 E 同主题,可合理归属。user-attachments 不显式标 uploader,严格说未铁证,但主题与修复 commit(F)一致。
- 注:这是他**唯一可逐字引用的、较长的一手技术散文式文本**——尽管是 shell 脚本而非自然语言段落,但 `echo` 标注与注释反映表达习惯。

#### E. Incus 修复 patch(一手代码,本会话抓到全文)
- URL:`https://github.com/user-attachments/files/24473601/templates_arbitrary_write.patch`(HTTP 200,3833 字节)
- 内容:Incus `driver_lxc.go` 的 `templateApplyNow` 与 `internal/util/filesystem.go`、`shared/util/filesystem.go` diff。核心把 `filepath.Join(d.RootfsPath(), ...)` + `os.Create(fullpath)` 改为 `os.OpenRoot(d.RootfsPath())` + `rootPath.Create(relPath)`(路径穿越安全化),新增 `MkdirAllOwnerInRoot`、`PathExistsInRoot`。
- 注释特征:保留 Go 标准 doc-comment 风格:`// MkdirAllOwner ensures that directories path exists.` / `// This function is a slightly modified version of MkdirAll from the Go standard library.`
- 可信度:一手(代码)。与 D 同源,主题一致。

#### F. 公开 GitHub commits(一手 commit message)— 14 条,本会话抓到
GitHub 搜索 `author:rmcnamara-snyk` 返回 14 条,作者邮箱 `rory.mcnamara@snyk.io`(身份铁证)。按时间倒序:

| SHA(短) | 仓库 | 日期 | message |
|---|---|---|---|
| dbc1323818 | **canonical/lxd** | 2026-01-17 | `lxd/instance/drivers/lxc: Use ShellQuote instead of Quote` |
| 0e0cf45ecd | **lxc/incus** | 2026-01-17 | `incusd/instance/lxc: Use SingleQuote instead of Quote` |
| cc2334385b | snyk-labs/github-actions-scanner | 2024-06-18 | `ignore repo-local action uses for unpinned_action rule. Fix try/catch for rule execution` |
| f00afa742c | snyk-labs/github-actions-scanner | 2024-06-17 | `Update config.yml` |
| 21718b211a | snyk-labs/github-actions-scanner | 2024-06-17 | `Update config.yml` |
| ef579d478d | snyk-labs/github-actions-scanner | 2024-06-17 | `Update config.yml` |
| 06666abc16 | snyk-labs/github-actions-scanner | 2024-06-17 | `Update config.yml` |
| 7247741838 | snyk-labs/github-actions-scanner | 2024-06-13 | `Update README.md` |
| 1ddc2ea76e | snyk-labs/github-actions-scanner | 2024-06-04 | `Initial Commit` |
| d0403df33a | rmcnamara-test/terraform-provider-example | 2023-11-14 | `update test.tf source` |
| 9dad0684de | rmcnamara-test/terraform-provider-example | 2023-11-14 | `gitignore` |
| 59afb473f1 | rmcnamara-test/terraform-provider-example | 2023-11-14 | `add registry manifest` |
| b2c81d2c11 | rmcnamara-test/terraform-provider-example | 2023-11-14 | `add goreleaser` |
| 9063784c1a | rmcnamara-test/terraform-provider-example | 2023-11-14 | `Initial commit` |

**关键发现 — Incus/LXD 修复提交(2026-01-17)**:
- `lxc/incus` commit `0e0cf45ecd`:message `incusd/instance/lxc: Use SingleQuote instead of Quote`
- `canonical/lxd` commit `dbc1323818`:message `lxd/instance/drivers/lxc: Use ShellQuote instead of Quote`
- 这两条是 **CVE-2026-23953(Incus 容器环境配置 newline 注入,GHSA-x6jc-phwx-hp32)** 的修复提交——根因是 lxc 启动配置写入时未对值做 shell 引用转义,允许换行符注入。修法正是把 `Quote` 换成 `SingleQuote`/`ShellQuote`。
- 这是 Rory 名下的、**上游主仓修复 commit**——一手代码 + 一手 commit message。推翻"上游 6 仓库 author:rmcnamara-snyk 公开 issue/PR/comment = 0"在 commit 维度的适用范围(原任务只断言 issue/PR/comment 为 0;实际他在 incus/lxd **有**上游修复 commit)。
- message 风格:Conventional Commits(scope 前缀 + 祈使句),极简,无正文。`Use SingleQuote instead of Quote` 直陈改动,不解释 why。

**snyk-labs/github-actions-scanner(2024-06)**:8 条 commit,从 `Initial Commit` 到 README/config 维护,到 `ignore repo-local action uses for unpinned_action rule. Fix try/catch for rule execution`(唯一带技术细节的 message,两个祈使句拼一句)。反映他在 Snyk 内部维护一个 GitHub Actions 扫描器项目。

**rmcnamara-test/terraform-provider-example(2023-11)**:5 条 commit,个人测试仓(terraform provider 脚手架),`Initial commit` / `add goreleaser` / `add registry manifest` / `gitignore` / `update test.tf source`。早期脚手架,无技术散文。

#### G. 早前个人 GitHub 账号 `psychomario`(据并行 agent 核实,本会话未独立复核)
- 并行 agent 报告:Rory 有更早个人账号 `psychomario`(2011-09-10 创建,Name=Rory McNamara),3 个 fork 仓库,Arctic Code Vault Contributor 成就;5 条归档推文来自 @PsychoMario。
- 本会话未独立 fetch `github.com/psychomario` 复核。标注**推测-二手**(teammate 报告,未自验)。若属实,该账号下的 commit/README/issue 属另一条一手线索,需后续补查。

---

### 二手(他人转述/描写他的发现)

#### H. GHSA 公告正文文本(9 条,逐条作者归属判断)
Rory 在 9 条 GHSA 中均为 credited reporter,但**公告正文文本不一定由他写**。逐条:

1. **GHSA-xr7r-f8xq-vfvv / CVE-2024-21626(runc,Leaky Vessels attack 1)**
   - **本会话已核实**:WebFetch 公告页确认 **published by `cyphar`(Aleksa Sarai,SUSE)**。公告正文(含 "In runc 1.1.11 and earlier, due to an internal file descriptor leak..." 开头)是 **Sarai 的文笔**。Rory 仅在 Credits 列为 reporter(attack 1 原始发现者)。
   - 可信度:二手(公告文本=Sarai 的;Rory 是被 credited 的发现者)。

2. **GHSA-m3r6-h7wv-7xxv / CVE-2024-23651(buildkit,cache mount subpath 竞争,High)**
   - 未本会话独立核实(GHSA API 403)。按 runc 同型推断:buildkit 维护者(moby/buildkit team)发布,Rory credited。公告文本大概率维护者的。可信度:二手(推断)。

3. **GHSA-4v98-7qmw-rqr8 / CVE-2024-23652(buildkit,mount stub cleaner 致宿主访问,Critical)**
   - 同上。可信度:二手(推断)。

4. **GHSA-wr6v-9f75-vh2g / CVE-2024-23653(buildkit,interactive containers API 不校验 entitlements,Critical)**
   - 同上。可信度:二手(推断)。

5. **GHSA-874v-pj72-92f3 / CVE-2024-1753(podman,构建期容器逃逸,Medium)**
   - 推断 podman/containers 团队发布。可信度:二手(推断)。

6. **GHSA-pmf3-c36m-g5cf(buildah,构建期容器逃逸,High,无 CVE)**
   - 推断 buildah 维护者发布。可信度:二手(推断)。

7. **GHSA-p9v8-q5m4-pf46 / CVE-2024-5138(snapd,snapctl 鉴权绕过,Medium)**
   - 推断 snapd/canonical 团队发布。可信度:二手(推断)。

8. **GHSA-x6jc-phwx-hp32 / CVE-2026-23953(incus,容器环境配置 newline 注入,High)**
   - **关键**:Rory 名下有 `lxc/incus` commit `0e0cf45ecd`(SingleQuote 修复,2026-01-17)。强烈暗示 Incus 这两条 CVE 的**修复代码**是 Rory 写的(他提交了 fix)。但**公告正文文本**仍可能是 Incus 维护者(Stéphane Graber 等)在 GHSA 私有通道里基于 Rory 的报告撰写。修复 patch(D/E)是他附的,公告叙述不一定。可信度:混合(PoC/patch/commit 一手;公告文本二手推断)。

9. **GHSA-7f67-crqm-jgh7 / CVE-2026-23954(incus,镜像 templating 任意宿主文件读写,High)**
   - 同 8。PoC 脚本(D)与 patch(E)挂在 references,是 Rory 附的;公告正文推断为维护者。可信度:混合。

> **advisory 文本作者归属结论(逐条一句)**:
> 1. runc(21626):**核实**——cyphar/Sarai 发布,Rory 仅 reporter。
> 2-7. buildkit/podman/buildah/snapd:**推断**——各上游维护者发布,Rory credited(未独立核实)。
> 8-9. incus(23953/23954):**部分一手**——公告文本推断为 Incus 维护者;但修复 commit 与 PoC/patch 是 Rory 本人产出。

#### I. Leaky Vessels 摘要公告(byline=Jamie Smith)
- URL:`https://labs.snyk.io/resources/leaky-vessels-docker-runc-container-breakout-vulnerabilities/`(2024-01-31)
- 据前序档案:页面 byline 是 "Jamie Smith"(Snyk 编辑/撰笔),但正文明确 "Snyk security researcher Rory McNamara, with the Snyk Security Labs team, identified four vulnerabilities — dubbed 'Leaky Vessels'..."。**研究归属一手,文章撰笔二手。**
- 引文(前序档案):*"Snyk security researcher Rory McNamara, with the Snyk Security Labs team, identified four vulnerabilities — dubbed 'Leaky Vessels' — in core container infrastructure components that allow container escapes."*

#### J. oss-security 邮件
- 原任务给定:Leaky Vessels 的 oss-security 公开公告由 Aleksa Sarai(cyphar,SUSE)署名,**不是** Rory 署名。Solar Designer 回帖感谢 "you and others you credit"。
- 本会话未重新抓取 openwall(不在 curl 白名单)。采信:Rory **无** oss-security 署名发帖。可信度:二手(原任务给定,未自验)。

#### K. CVE-2024-23326(Envoy)— 推翻"可能是他的"
- 并行 agent 提示"可能 CVE-2024-23326(Istio)也归他"。本会话 NVD 查证:**CVE-2024-23326 是 Envoy(envoyproxy/envoy)请求走私漏洞**,GHSA-vcf8-7238-v74c,与 Istio 无关,与 Rory 无可核实关联。
- 结论:该提示**不成立**。可信度:NVD 一手数据,推翻推测。

#### L. 公开 GitHub issue/PR(他被 assign,非亲开)— 2 条
`commenter:rmcnamara-snyk` 搜索返回 2 条,均在 snyk-labs/github-actions-scanner:
- PR #9 `[Snyk] Upgrade yaml from 2.4.2 to 2.5.1`(由 `supriza` 机器人开,Rory 被 assign,2024-09-25 创建/关闭,0 评论)
- 另一条类似依赖升级 PR。
- 这些是**依赖机器人开的 PR**,Rory 作为 maintainer 被 assign 并合并,**不是他亲笔写的 issue/PR 文本**。可信度:二手(参与但非作者)。

#### M. 第三方媒体(据前序档案)
- OpenSSF blog(2024-02-06,`openssf.org/blog/2024/02/06/time-is-of-the-essence...`)明确点名 Rory。bleepingcomputer、DarkReading 等 403 不可直读,只能借片段旁证。二手。

---

### 推测

#### N. 9 条 GHSA references 中 snyk.io URL = 0
- 原任务给定。本会话未逐一取 references(GHSA API 403),采信。
- 推测含义:Snyk 不把公司博客链接塞进上游 GHSA references;Rory 的深度 writeup(labs.snyk.io)与 GHSA 公告是分离传播渠道。这与"Snyk 作者页全 404 → 书面产出 0"的**误推**不同——产出存在于 labs.snyk.io/contributors 体系,只是不进 GHSA references。

#### O. 写作成熟度的时间演化(推测)
- 2021-2022:Snyk 科普/营销型(AWS security、Top 10 acronyms、CTI deep dive),无个人分析声音。
- 2023:AI Glossary,仍偏词条。
- 2024:labs.snyk.io Leaky Vessels deep dive + Ubuntu privesc,出现签名式方法论("Where are the privilege boundaries?"、strace 教学)。
- 2026:Safe Path Handling(合著)+ Incus 上游修复 commit,漏洞类×生态矩阵写法成熟。
- 推测:他在 Snyk 的角色从 AppSec 教育内容(2021-2022)转向深度安全研究(2024+),与其 GitHub commit 时间线(2023-11 个人测试仓、2024-06 snyk-labs 扫描器、2026-01 incus 上游修复)一致。

---

## 写作风格分析

基于本会话**可逐字引用的一手文本**:PoC .sh(D)、commit messages(F)、Snyk bio(A)。labs.snyk.io 深度文引文来自前序档案,本会话超时未复核,标注"据前序档案"。

### 可提取的风格特征

1. **PoC 脚本:阶段化标注 + 内联构造 + 收尾清理**
   - `echo "POC 1/2: Arbitrary File Read"` / `echo "POC 2/2: Container Escape"` —— 明确编号分阶段,读者跟随输出即可复现。
   - 用 heredoc 内联构造恶意 YAML/Go 源文件,不依赖外部 payload 文件。
   - 收尾必清理:`rm -rf ${BUILDDIR}`、`incus image delete poc`、`echo "Repairing core_pattern"`。**负责任的 PoC 习惯**——不留宿主破坏。
   - 注释极简:`# build new image` 一句,不解释原理(原理留给公告/writeup)。

2. **Commit message:Conventional Commits + 祈使句 + 极简**
   - `incusd/instance/lxc: Use SingleQuote instead of Quote` —— scope 前缀 + 祈使句 + 直陈改动,不附正文解释 why。
   - `ignore repo-local action uses for unpinned_action rule. Fix try/catch for rule execution` —— 两个祈使句拼一句,无正文、无尾点。
   - 全小写起首(`ignore`、`update`、`add`),仅 scope 与专有名词大写。
   - 风格签名:工程师极简主义,信任 diff 自解释。

3. **自然语言(据前序档案引文,本会话未复核):方法论自述 + "keep it simple" + 反讽**
   - "Whenever I'm looking at something new, especially for privilege escalation vulnerabilities, my first thought is always, 'Where are the privilege boundaries?'" —— 以反问句锚定分析起点。
   - "you can keep it simple when it comes to exploitation" —— 显式价值表态,反对不必要的复杂内存破坏。
   - "we chained one small bug in a privileged component together with a number of features, which all work as expected" —— 用"feature 按预期工作"反讽安全边界。
   - "If you've read some of my previous work you may know that I love the strace tool" —— 第一人称 + 自指前作,视自己有连续方法论品牌。
   - "strace can only show you what is happening, not what can happen. It's still necessary to deeply understand the system being investigated." —— 工具赞而不盲信,显式边界。
   - ⚠ 这批引文来自前序调研档案 Wayback 抓取,本会话 labs.snyk.io WebFetch 超时未独立复核。若引文准确,则其自然语言风格:**第一人称、方法论自述、反问锚定、显式价值判断、反讽安全边界、自指前作、教学型 toy 程序铺垫、玩梗式小节标题**(CVE-2024-21626→"You're out of order"、CVE-2024-23652→"Plenty of time"、CVE-2024-23651→"Race to the source")。

4. **Bio 自述:身份标签 + 专注重点**
   - "Long-time bug bounty hunter, ex-pentester, and AppSec engineer." —— 三段式身份递进(bug bounty → pentest → AppSec)。
   - "passionate about race conditions and Linux exploitation." —— 点名两个专精域,与 CVE 组合完全自洽。

### 风格总结
- **一手代码层面(本会话核实)**:极简、阶段化、负责任清理、Conventional Commits、信任 diff 自解释。
- **一手自然语言层面(部分依赖前序档案)**:第一人称方法论自述、反问锚定、显式价值判断("keep it simple")、反讽安全边界、玩梗标题、教学型 toy 程序铺垫、给完整 PoC 终端转录。
- 若仅以本会话独立复核到的一手文本(PoC .sh + commit messages + bio)论:**写作风格可部分提取**——代码风格强可证,自然语言长文风格依赖前序档案未复核。

---

## 书面产出总量评估

| 渠道 | 数量 | 可信度 | 备注 |
|---|---|---|---|
| Snyk 博客署名文章(contributors 索引) | 5 | 一手(byline,4 篇明确署名 + 1 篇索引归属) | 2021-2026 |
| labs.snyk.io 深度研究文 | ≥2(Ubuntu privesc + Leaky Vessels deep dive);可能更多(4-hidden-ai-coding-risks 等) | 一手(byline,前序档案 + Wayback) | 本会话未独立复核署名 |
| GHSA credited(reporter) | 9 | 一手(research credit) | 但公告正文文本多为维护者写 |
| GHSA 公告正文文本作者 | 0 条可核实为 Rory 亲写 | 二手 | runc 确认 Sarai 写;其余推断维护者写 |
| 公开 GitHub commits | 14 | 一手(commit message) | 含 2 条上游 incus/lxd 修复(2026-01-17) |
| 公开 GitHub issue/PR(他亲开) | 0;2 条他被 assign 的机器人 PR | 二手 | — |
| oss-security 署名发帖 | 0 | 二手(原任务给定) | Leaky Vessels 主帖 Sarai 署名 |
| PoC 脚本/patch(挂 GHSA references) | ≥2(Incus .sh + .patch) | 一手(代码) | 本会话抓到全文 |
| 个人 gist | 0(profile 显示 gists 0) | 一手(profile) | — |
| README/docs | snyk-labs `Update README.md` commit 存在,但非长文 | 一手(commit) | — |
| 早前账号 psychomario 产出 | 未核实 | 推测(teammate 报告) | 需后续补查 |
| 播客口述(The Secure Developer Ep 146) | 1 次嘉宾 | 一手(verbal,未抓到 transcript) | 推测为 deep dive 口语化版本 |

**总量结论**:Rory 的公开书面产出**不为 0**。明确可核实的一手产出至少:
- 5 篇 Snyk 文章(4 篇明确署名 + 1 篇索引归属)
- ≥2 篇 labs.snyk.io 深度文(Wayback 归档,前序档案引文)
- 14 条 commit message(含 2 条上游 incus/lxd 修复)
- 2 个 PoC/patch 文件(Incus)
- 1 段 bio 自述

但**纯粹由他亲笔撰写、公开可见的、长篇自然语言技术散文**确认数仍偏低——labs.snyk.io 深度文虽 Wayback 归档,本会话因 JS 超时未逐字复核。他的"著作"大量以**代码 + 公告 credit + commit**形态存在,而非传统博客长文。

---

## 矛盾与未解之处

1. **"Snyk 作者页全 404 → 书面产出 0" 的误推(关键矛盾)**
   - 原任务断言 `snyk.io/blog/author/{rory-mcnamara,...}/` 全 404 —— **对该路径成立**。
   - 但 `snyk.io/contributors/rory-mcnamara/` **live 可用 + 15 Wayback 快照**,显示 bio + 5 篇文章。
   - 结论:原任务"书面公开产出 = 0 这一事实要明确记录"**不成立**。产出存在,只是 hosted 在 `/contributors/` 而非 `/blog/author/`。此矛盾明确记录,不和稀泥。

2. **"上游 6 仓库 author:rmcnamara-snyk 公开 issue/PR/comment = 0" 与 commit 的边界**
   - 原任务断言对 issue/PR/comment 成立。
   - 但 `lxc/incus` 与 `canonical/lxd` 各有 1 条 Rory 的上游修复 commit(2026-01-17)。原任务**未断言 commit = 0**(只说 issue/PR/comment),故不矛盾,但易被误读为"上游零足迹"。实际他在 incus/lxd 有上游修复代码足迹。

3. **CVE-2024-23326 归属(已推翻)**
   - 并行 agent 提示"可能 CVE-2024-23326(Istio)也归他"。NVD 查证为 Envoy 请求走私,与 Istio/Rory 均无关。**该提示不成立**,明确记录以免以讹传讹。

4. **Wayback 快照数差异**
   - 并行 agent 称"18 个快照";本会话 CDX 返回 15 个。差异可能来自 CDX 去重/重定向计数方式。不影响"页长期存在"结论。

5. **labs.snyk.io 署名未本会话独立复核**
   - labs.snyk.io/resources/ WebFetch 超时(重 JS)。Ubuntu privesc 与 Leaky Vessels deep dive 的 "Rory McNamara Share" 署名来自前序档案,本会话仅以 CDX 确认 URL 存在。若前序档案引文有误,则"写作风格分析"第 3 条的引文需降级。**未解:无法本会话逐字确认 labs 文本。**

6. **9 条 GHSA 公告文本作者归属:仅 runc 一条本会话核实**
   - 其余 8 条因 GHSA API 403 + advisory-database 404 未取到 `submitted_by`/正文。2-7 条按"上游维护者发布"推断;8-9 条因有 Rory 的修复 commit 而更可能是"Rory 提供报告+PoC+patch、维护者撰写公告叙述"的混合模式。**未解:8 条公告文本作者归属未独立核实。**

7. **Incus 两条 CVE 的 PoC 与修复代码归属**
   - PoC .sh/patch 挂在 GHSA-7f67-crqm-jgh7 references;修复 commit 在 lxc/incus。二者主题一致(templating 路径穿越→OpenRoot 修复)。可合理归属 Rory,但 user-attachments 不显式标 uploader,严格说**未铁证**。

8. **早期"通识/营销"内容 vs 后期"深度研究"内容的文风断裂**
   - 2021-2022 的 AWS security / Top 10 acronyms / threat intelligence 是营销/教育型通识;2024+ 的 labs 深度文是 offensive 研究。两种解释(均为推测):(a) 职业演化,从 AppSec 到 Staff Researcher;(b) 贡献者页过度归属,部分文章非亲笔。第 2 篇 AI Glossary 无个人 byline 已证"挂名"机制存在;但第 4/5/6 篇有 "Written by Rory McNamara" byline,故(b)对它们不完全成立。无法判定,矛盾如实记录。

---

## 信息不足之处

1. **GHSA API 全量 403**:未取到 9 条公告的 `submitted_by`/`published_at`/`description`/`references` 原文字段。advisory-database 镜像 404。导致 8 条公告文本作者归属只能推断。
2. **labs.snyk.io 重 JS 超时**:未本会话逐字复核 Ubuntu privesc 与 Leaky Vessels deep-dive 的署名与正文。前序档案引文依赖待复核。
3. **oss-security 未本会话抓取**:openwall 不在 curl 白名单。Rory 是否在 oss-security 任何线索发帖,未独立核实(仅依原任务上下文采信"无署名")。
4. **psychomario 账号未独立复核**:teammate 报告 Rory 有早前个人账号 psychomario(2011 创建)。若属实,该账号下的 commit/README/issue 是另一条一手线索,本会话未抓。@PsychoMario 的 5 条归档推文亦未抓(X paywall)。
5. **Snyk 内部 wiki/私有 advisory 文本**:不可公开访问,Rory 作为 Staff Security Researcher 的内部产出不可见。
6. **会议演讲/BlackHat/USENIX**:未发现 Rory 的演讲记录线索。blackhat.com、usenix.org 在 curl 白名单但未深查。
7. **播客 transcript 未抓到**:The Secure Developer Ep 146(YouTube `Ip9IFaAuGkI`)描述被截断,无完整 transcript,无法引用口述原文。
8. **"previous work"的自指未追溯**:Leaky Vessels deep dive 的 "If you've read some of my previous work you may know that I love the strace tool" 暗示他在更早(早于 2024-02)就有 strace 重度使用的文章/writeup,但本次调研未在 Snyk 贡献者页(只列 5 篇)或 labs.snyk.io 定位到。**可能存在于 packetstormsecurity / 个人 bug bounty 平台 / 早期 Snyk 内部博客,未核实。**
9. **写作风格"自然语言长文"样本不足**:本会话独立抓到的长形态一手文本仅 PoC .sh(代码)与 commit message(短语)。labs 深度文的自然语言段落来自前序档案,未复核。因此"写作风格分析"的代码部分强可证、自然语言部分偏弱。

---

## 数据来源索引(本文每条信息可回溯的 URL)

- `https://snyk.io/contributors/rory-mcnamara/` — 贡献者页 + bio + 5 篇文章清单(本会话 WebFetch 复核 ✓)
- `https://web.archive.org/cdx/search/cdx?url=snyk.io/contributors/rory-mcnamara` — 15 快照(本会话 CDX ✓)
- `https://web.archive.org/cdx/search/cdx?url=labs.snyk.io/resources/*` — 100+ 快照(本会话 CDX ✓)
- `https://labs.snyk.io/resources/abusing-ubuntu-root-privilege-escalation/` — Ubuntu privesc 全文(前序档案 Wayback,byline ✓,本会话未复核)
- `https://labs.snyk.io/resources/leaky-vessels-container-vuln-deep-dive/` — Leaky Vessels deep dive 全文(前序档案 Wayback,byline ✓,本会话未复核)
- `https://labs.snyk.io/resources/leaky-vessels-docker-runc-container-breakout-vulnerabilities/` — Leaky Vessels 摘要公告(前序档案,byline=Jamie Smith)
- `https://snyk.io/articles/safe-path-handling/` — 第 1 篇(byline ✓)
- `https://snyk.io/articles/ai-security/ai-glossary/` — 第 2 篇(无个人 byline)
- `https://snyk.io/articles/aws-security/` — 第 4 篇(byline ✓)
- `https://snyk.io/articles/application-security/glossary-acronyms/` — 第 5 篇(byline ✓)
- `https://snyk.io/articles/threat-intelligence/` — 第 6 篇(byline ✓)
- `https://github.com/opencontainers/runc/security/advisories/GHSA-xr7r-f8xq-vfvv` — runc 公告,published by cyphar(本会话 WebFetch ✓)
- `https://api.github.com/search/commits?q=author:rmcnamara-snyk` — 14 条 commit(本会话 ✓,邮箱 rory.mcnamara@snyk.io)
- `https://api.github.com/search/issues?q=commenter:rmcnamara-snyk` — 2 条 assign 记录(本会话 ✓)
- `https://github.com/user-attachments/files/24473599/template_arbitrary_write.sh` — Incus PoC 全文(本会话 ✓)
- `https://github.com/user-attachments/files/24473601/templates_arbitrary_write.patch` — Incus 修复 patch 全文(本会话 ✓)
- `https://api.github.com/repos/lxc/incus/commits/0e0cf45ecd` — Incus 修复 commit(本会话 search ✓)
- `https://api.github.com/repos/canonical/lxd/commits/dbc1323818` — LXD 修复 commit(本会话 search ✓)
- `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2024-23326` — Envoy CVE,推翻归属(本会话 ✓)
- `https://openssf.org/blog/2024/02/06/time-is-of-the-essence-to-mitigate-vulnerabilities-like-leaky-vessels/` — 二手旁证(点名 Rory)
- `https://www.youtube.com/watch?v=Ip9IFaAuGkI` — 播客嘉宾(描述未抓到)
- `https://github.com/psychomario` — 早前账号(teammate 报告,未自验)

---

*本文件所有结论均标注来源 URL 与可信度。未核实处明确写"未核实到"。无编造引语/URL。前序档案引文标注"本会话未复核",不冒充本会话一手抓取。*

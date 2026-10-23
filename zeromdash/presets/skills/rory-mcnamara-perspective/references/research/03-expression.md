# Rory McNamara — 表达 DNA 维度

> 本维度回答:他如何用文字/技术语言表达漏洞、解释技术概念、组织论证。
> 前置事实(承接 01-writings / 02-conversations):Rory 无 blog、无 Twitter、无公开 repo/gist/starred、无公开 PR/issue/comment、无播客/演讲/AMA/采访。因此本维度的核心张力是——**在几乎没有一手公开文字的情况下,如何提取「表达 DNA」**,以及**「沉默」本身是否就是他的表达特征**。

---

## 调研方法

所有关键事实均通过原始信源直查,而非搜索摘要:

1. **GitHub Commit Search(关键突破)**:`https://api.github.com/search/commits?q=author:rmcnamara-snyk`(带 `Accept: application/vnd.github.cloak-preview+json`)。这是本维度最重要的发现来源——它返回了 **14 条 commit**,其中 2 条带 `Signed-off-by: Rory McNamara <rory.mcnamara@snyk.io>`,是**唯一可 100% 确认归到 Rory 本人的一手文字**。
2. **Commit patch 直取**:对 `lxc/incus` 和 `canonical/lxd` 的修复 commit,用 `https://github.com/<org>/<repo>/commit/<sha>.patch`(非 API,不受 API rate limit 影响)取完整 commit message + diff。
3. **GitHub Advisory 网页(WebFetch)**:对 9 个 GHSA 逐条抓 `https://github.com/advisories/<GHSA>`,提取 **publisher/author 字段**与 credited finder——判定「advisory 描述文本是谁写的」。
4. **GHSA REST API**:`https://api.github.com/advisories/<GHSA>`(受 rate limit,部分调用失败后改用 WebFetch 补齐)。
5. **NVD REST API**:`https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=...` 取 `sourceIdentifier`(判定 CNA 归属)与 description。
6. **PoC 附件直取**:Incus 两个 GHSA 引用的 `github.com/user-attachments/files/<id>/<file>` 经 curl 直取脚本/patch 全文,分析代码风格、命名、组织方式。
7. **raw.githubusercontent.com**:取 `snyk-labs/github-actions-scanner` README,判断是否有可归到 Rory 的散文。

**可信度标记**:一手 = 他本人账号/邮箱产出的痕迹(`Signed-off-by` + snyk 邮箱 = 一手);二手 = 他人的转述;推测 = 我基于证据的推断。对于 advisory 正文与 PoC 附件,**作者归属是逐条判定的核心问题**,绝不笼统归到 Rory。

**方法论限制(前置声明)**:GitHub unauthenticated API rate limit = 60/小时,本调研中多次触发;commit search 与 patch 端点已交叉验证。WebSearch 在本环境不可用;`web.archive.org` WebFetch 被屏蔽。

---

## 可归到 Rory 的一手表达材料

### 一手(100% 确认,他本人邮箱产出)

**材料 A — Incus 修复 commit message(CVE-2026-23953 newline injection 的最终修复)**

- 来源:`https://github.com/lxc/incus/commit/0e0cf45ecdcc902a6f319f11971ed27df81bd29f`(.patch 端点直取)
- 作者头:`From: Rory McNamara <rory.mcnamara@snyk.io>`
- 日期:2026-01-17 09:05:04 -0500
- 完整 message:
  ```
  incusd/instance/lxc: Use SingleQuote instead of Quote

  This avoids potential shell expansion of the strings should some special
  characters manage to make it through.

  Signed-off-by: Rory McNamara <rory.mcnamara@snyk.io>
  ```
- 改动:`strconv.Quote(d.Project().Name)` → `util.SingleQuote(...)`,3 处 hook 路径(pre-start / stop / post-stop)。最小 diff,3 增 3 删。
- **这是 Rory 表达 DNA 最纯净的样本**:Subject 行的命名规范、body 的让步措辞、DCO 签名习惯,全部在此。

**材料 B — LXD cherry-pick commit message(同修复反向移植到 LXD)**

- 来源:`https://github.com/canonical/lxd/commit/dbc132381807a8fee20cd4cfbd12065acb6c9971a.patch`
- 作者头:`From: Rory McNamara <rory.mcnamara@snyk.io>`(原始作者);cherry-pick 由 Thomas Parrott 执行
- message:
  ```
  lxd/instance/drivers/lxc: Use ShellQuote instead of Quote

  This avoids potential shell expansion of the strings should some special
  characters manage to make it through.

  Signed-off-by: Rory McNamara <rory.mcnamara@snyk.io>
  (cherry picked from commit 0e0cf45ecdcc902a6f319f11971ed27df81bd29f)
  Signed-off-by: Thomas Parrott <thomas.parrott@canonical.com>
  License: Apache-2.0
  ```
- 旁证:Incus 用 `util.SingleQuote`,LXD 用 `shared.ShellQuote`(两仓库 helper 函数命名不同),但 Rory 的 message 文本几乎逐字复用——证明这是他**复用的固定句式**。

**材料 C — snyk-labs/github-actions-scanner 工程类 commit(低表达密度)**

- 来源:`https://github.com/snyk-labs/github-actions-scanner`(commit search 返回 7 条)
- 代表 message:`ignore repo-local action uses for unpinned_action rule. Fix try/catch for rule execution`(2024-06-18)
- 其余多为 `Update config.yml` ×4、`Update README.md`、`Initial Commit`。
- 可信度:一手(GitHub author 字段 = rmcnamara-snyk),但属于工程脚手架 commit,**表达密度低**,仅能佐证「他写 commit 用祈使句、小写开头、不写客套」。

### 高可信度(作者归属强但非 100%——finder credit + 指纹吻合)

**材料 D — Incus templating PoC 脚本(CVE-2026-23954)**

- 来源:`https://github.com/user-attachments/files/24473599/template_arbitrary_write.sh`
- 关联 advisory:GHSA-7f67-crqm-jgh7,credited **Finder = rmcnamara-snyk**,Remediation developer = stgraber
- 归属判定:advisory 由 maintainer stgraber 发布,但 PoC 脚本是 finder 在上报时附上的产物。Rory 是唯一 credited finder,且本脚本与材料 E 共享强作者指纹(见下)。**高可信度归到 Rory,但保留「maintainer 可能改写」的不确定性。**
- 内容要点(完整已取,1751 bytes,POSIX shell):
  - sentinel 文件命名:`/template_arbitrary_write_cmd_exec_poc`
  - 开头 `ls -l /template_arbitrary_write_cmd_exec_poc`(证明初始不存在)
  - 从 `images.linuxcontainers.org` 下载 alpine rootfs,手搓 `metadata.yaml`(含 `templates: /shadow: ... template: ../../../../../../../../etc/shadow` 路径穿越)
  - `ln -s / rootfs/realroot`(符号链接逃逸)
  - 分两幕:`echo "POC 1/2: Arbitrary File Read"` → `incus exec poc -- head -n1 /shadow`;`echo "POC 2/2: Container Escape"` → 用 `core_pattern`(`|/bin/sh -c "%E"`)+ segfault 触发,再借 `gcc` 输出文件名经 `base64` 走私一个宿主路径执行 `stage2`
  - 结尾清理:`incus stop -f poc`、`rm -rf ${BUILDDIR}`、`incus image delete poc`、`echo core | sudo tee /proc/sys/kernel/core_pattern`(修复 core_pattern)

**材料 E — Incus newline injection PoC 脚本(CVE-2026-23953)**

- 来源:`https://github.com/user-attachments/files/24473682/environment_newline_injection.sh`
- 关联 advisory:GHSA-x6jc-phwx-hp32,credited **Finder = rmcnamara-snyk**
- 归属判定:与材料 D 同一 finder、同一目标软件、同一 sentinel 命名范式 `/<name>_command_exec_poc`。**同一作者高度可信 = Rory。**
- 内容要点(完整已取,极简):
  - sentinel:`/newline_injection_command_exec_poc`
  - `set -x` 开头,heredoc 注入 multiline `environment.FOO`,内含 `lxc.hook.pre-start = /bin/sh -c "id > /newline_injection_command_exec_poc"`
  - `ls -l` + `cat` sentinel 自证
  - `incus stop poc` 收尾

### 中/低可信度(归属存疑,逐条标注)

**材料 F — environment_newline_injection.patch(CVE-2026-23953 的「提议修复」)**

- 来源:`https://github.com/user-attachments/files/24473685/environment_newline_injection.patch`
- 内容:在 `initLXC` 的 environment 处理处加 `strings.Contains(after, "\n") || strings.Contains(v, "\n")` → `return nil, errors.New("Environment cannot contain newline characters")`
- **关键矛盾**:这个提议 patch 用的是「拒绝 newline」策略;而 Rory **实际合入的 commit(材料 A)** 用的是「`SingleQuote` 而非 `Quote`」策略。两者是**对同一漏洞的不同修复思路**。
- 归属推断:此 patch 很可能是 Rory 上报时附的**初版提议**,maintainer stgraber 最终采纳了 Rory 另一个思路(SingleQuote,即材料 A 的 commit)。但也可能是 maintainer 的备选方案。**无法 100% 确认作者**,记为中可信度。

**材料 G — templates_arbitrary_write.patch(CVE-2026-23954 的修复)**

- 来源:`https://github.com/user-attachments/files/24473601/templates_arbitrary_write.patch`
- 内容:用 `os.OpenRoot` / `os.Root` / `PathExistsInRoot` / `MkdirAllOwnerInRoot` 把模板路径操作收敛到 root-bounded 文件描述符,堵住符号链接/路径穿越。
- 归属判定:advisory 明确 **Remediation developer = @stgraber**。此 patch **大概率是 maintainer 的最终修复**,不是 Rory 的。Rory 在此只提供 PoC(材料 D)与漏洞报告。**低可信度归到 Rory,默认视为非他所作。**

### 明确「非 Rory」的材料(重要负证据)

**9 条 advisory 的描述正文 + NVD description 全部不是 Rory 写的**——这是本维度最关键的负证据:

| GHSA | CVE | 软件 | **Publisher(正文作者)** | Rory 角色 |
|---|---|---|---|---|
| GHSA-xr7r-f8xq-vfvv | CVE-2024-21626 | runc | **cyphar**(Aleksa Sarai,SUSE,Leaky Vessels 公告署名人) | Finder |
| GHSA-m3r6-h7wv-7xxv | CVE-2024-23651 | buildkit | **tonistiigi**(Tõnis Tiigi,BuildKit maintainer) | Reporter |
| GHSA-4v98-7qmw-rqr8 | CVE-2024-23652 | buildkit | tonistiigi(同类推断) | Finder |
| GHSA-wr6v-9f75-vh2g | CVE-2024-23653 | buildkit | tonistiigi(同类推断) | Finder |
| GHSA-874v-pj72-92f3 | CVE-2024-1753 | podman | **TomSweeneyRedHat**(Red Hat) | Finder |
| GHSA-pmf3-c36m-g5cf | —(buildah) | buildah | **TomSweeneyRedHat** | Finder |
| GHSA-p9v8-q5m4-pf46 | CVE-2024-5138 | snapd | **ernestl**(Canonical) | Reporter |
| GHSA-x6jc-phwx-hp32 | CVE-2026-23953 | incus | **stgraber**(Stéphane Graber) | Finder |
| GHSA-7f67-crqm-jgh7 | CVE-2026-23954 | incus | **stgraber** | Finder |

- NVD `sourceIdentifier` 取样(CVE-2024-21626、CVE-2026-23954)= `security-advisories@github.com`,即 **GitHub 是 CNA,不是 Snyk**。NVD description 是 GitHub advisory 正文的镜像,因此也归 maintainer,不归 Rory。
- **结论**:任何对 advisory/NVD 描述文风(如 runc 那条「attack 1 / attack 2」叙事、buildkit 那条 race condition 措辞)的风格提取,**都不能算 Rory 的一手表达**——它们是 cyphar / tonistiigi / TomSweeneyRedHat / ernestl / stgraber 的文笔。把 advisory 正文当 Rory 风格是本维度最容易犯的错误,此处明确排除。

---

## 表达 DNA 特征

### 特征 1 — 沉默即风格(Silence as Style)

这是他最显著、也最反直觉的表达特征。在 9 个 high/critical CVE、横跨 runc/buildkit/podman/buildah/snapd/incus 六大上游的产出规模下,他的公开文字总盘如下:

- blog 文章:**0**
- Twitter/微博/X 任何帖子:**0**
- 会议演讲/AMA/采访:**0**(详见 02-conversations)
- 公开 PR/issue/comment:**0**(上游 6 仓库全 0)
- 公开 repo/gist/starred:**0**
- **唯一的公开文字产出 = 2 条带签名 commit message + 若干工程类 commit + 2 个 PoC 脚本/patch 附件**

对比同一生态的 finder 们:cyphar 为 runc 写了完整的 Leaky Vessels 公告 + oss-security 帖;stgraber 为 incus 写了 advisory 正文。**Rory 在每一次披露中都把「写正文」让渡给 maintainer,自己只留下 credit 字段里的一个用户名。** 这不是能力缺失(他的 commit message 证明他完全能写清楚技术论证),而是**刻意的角色选择**:做 finder、做 PoC、做 patch 提议,但把面向公众的叙事权交给上游。

### 特征 2 — 代码即表达(Code as the Utterance)

当必须表达时,他选择代码而非散文。证据:

- PoC 脚本(材料 D/E)**几乎不含解释性注释**——`template_arbitrary_write.sh` 全程无 `#` 说明行,只用 `echo "POC 1/2: Arbitrary File Read"` 这种**舞台报幕式**标注;`environment_newline_injection.sh` 更极端,只有 `set -x` + heredoc + sentinel,零注释。代码自证,不旁白。
- commit message(材料 A/B)的 body 只写**为什么**(why),不写**改了什么**(what)——what 留给 diff。这是「diff 即论证」的习惯。

### 特征 3 — 对比式修复命名(Contrastive "X instead of Y")

他的 commit subject 行有固定句式:`<path>: Use <X> instead of <Y>`(材料 A:`Use SingleQuote instead of Quote`;材料 B:`Use ShellQuote instead of Quote`)。

- 路径前缀(`incusd/instance/lxc:` / `lxd/instance/drivers/lxc:`):内核式、子系统定位式
- 祈使句开头(`Use`)
- **"instead of" 框架**:通过点名被替换的旧函数(`Quote`),在 subject 里就完成了「过去哪里不对」的指认。读者不看 diff 也知道问题出在 `strconv.Quote` 把字符串做成 Go 字面量(双引号包裹、转义),而 shell 不认这种引号,于是 newline/特殊字符能逃逸成配置项。

### 特征 4 — 谨慎的让步措辞(Hedged Concession)

commit body 的固定句式:`This avoids potential <X> should <Y> manage to make it through.`

- `potential`(潜在的,不绝对化)
- `should some special characters manage to make it through`(用 `should...manage to` 虚拟语气,承认「一般情况下未必触发,但万一有特殊字符溜进来」)
- 不用「This fixes a critical vulnerability」式自我拔高,也不写「An attacker can execute arbitrary code」式威胁渲染。**技术陈述降到最低调**——把残余风险如实标注,而非宣称彻底解决。

### 特征 5 — 自证 sentinel 结构(Self-proving Sentinel Pattern)

两个 PoC 共享一套**让漏洞自己说话**的论证结构:

1. 开头 `ls -l /<sentinel>` → 证明 marker 文件尚不存在
2. 执行利用
3. 结尾 `ls -l /<sentinel>` + `cat /<sentinel>` → 证明 marker 文件已出现,且内容是 `id` 的输出(即宿主 root 命令执行)
4. `incus stop` / `rm -rf` / `image delete` / `repair core_pattern` → 清场

sentinel 命名也是自描述的:`/newline_injection_command_exec_poc`、`/template_arbitrary_write_cmd_exec_poc`——**文件名即漏洞标题**。不写「以下是 PoC 说明」,而是让 `/cat sentinel` 的输出成为唯一论据。这与特征 1/2 一脉相承:用可复现的机器行为替代人工陈述。

### 特征 6 — 两幕递进叙事(Two-act Escelation)

材料 D 把一个漏洞拆成 `POC 1/2: Arbitrary File Read` → `POC 2/2: Container Escape`,从「任意文件读」升到「宿主命令执行」。这反映他的论证偏好:**先证明最小原语(读 shadow),再叠成完整影响(RCE)**,用 `echo;echo;echo;` 做幕间分隔。材料 E 则因漏洞本身只需一步,故无分幕——说明他会**按漏洞复杂度调整叙事密度**,而非一律长篇。

---

## 与同行的表达对比

| 研究员 | 公开文字体量 | 主要表达载体 | 风格倾向 | Rory 的相对位置 |
|---|---|---|---|---|
| **Tavis Ormandy** | 极高(43+ blog、15+ oss-security 帖) | 长技术博客、邮件列表 | 第一人称、口语化、吐槽式、详述调试过程 | **完全反例**。Tavis 用散文把思考过程外化;Rory 把过程留在终端历史里 |
| **Jann Horn** | 高(P0 blog + 演讲) | P0 blog 长写up、会议 talk | 严谨、教学式、系统化根因分析 | **反例**。Jann 倾向「教读者怎么复现这个推理」;Rory 倾向「给你脚本,你自己跑」 |
| **Ian Beer** | 中高(P0 blog) | P0 blog 长文 | 叙事性强、故事化(如「A Bug Hunter's Diary」式) | **反例**。Ian 会写情绪和顿悟;Rory 的 PoC 零情绪 |
| **Liran Tal(Snyk 同事)** | 极高(Snyk 多产 blog 作者、会议) | Snyk blog、演讲、书 | 教学/布道式、面向开发者受众 | **同雇主反例**。同在 Snyk,Liran 是对外的脸,Rory 是「暗物质」——产出可见,本人不可见 |

**核心对比结论**:在「Finder 型研究员」谱系里,Tavis/Jann/Ian/Liran 都选择**自己写面向公众的叙事**(blog/talk),把 finder 同时变成 communicator。Rory 选择**只做 finder/PoC-author,把 communicator 角色外包给 maintainer**(cyphar、stgraber、tonistiigi…)。他不是不能写(材料 A 的 body 证明他能精确表达),而是**主动放弃了「公开自我阐释」这条通道**。这在同级别产出(9 个 high/critical、横跨 6 大上游)的研究员里是**罕见且自洽**的选择——通常高产出会伴随高曝光,他把两者解耦了。

---

## 即兴表达(口头)维度

承接 02-conversations 的结论:**无可核实的口头来源(播客/演讲/AMA/采访)= 0**。

- `snyk-labs/github-actions-scanner` 的 README 引用一个 Area41 talk(`https://www.youtube.com/watch?v=pUa5P7THc3c`)和 Snyk blog,主题是 GitHub Actions 漏洞研究。Rory 在该 repo 有 commit,但 **talk 与 blog 均无「Rory McNamara」署名**,无法把他定位为讲者/作者。这是「Snyk Security Labs 团队」集体产出,Rory 可能参与但**不可归因**。
- 因此本维度**无口头表达 DNA 可提取**。他的表达全部是「写下/敲下」的静态产物,且基本只存在于代码库里。

---

## 矛盾与未解之处

1. **newline injection 的「提议 patch」与「最终 commit」策略不一致(材料 F vs 材料 A)**:提议 patch 用「拒绝含 newline 的环境变量」(`strings.Contains` 检查);最终合入的 Rory commit 用「`SingleQuote` 代替 `Quote`」(把值做 shell 安全引用)。两者都成立但哲学不同——前者黑名单、后者正确转义。**未解**:提议 patch 是 Rory 的初版(后被 maintainer 要求改思路)还是 maintainer 的备选?无 PR 评论证据可决断。若属 Rory,则反映他**会为同一漏洞准备多套修复方案**;若属 maintainer,则材料 F 不应计入 Rory 风格。保守记为存疑。

2. **templating 修复 patch 的作者(材料 G)**:advisory 标 Remediation developer = stgraber,但 patch 作为附件挂出。**未解**:是 stgraber 写完挂附件,还是 Rory 提议了 `os.OpenRoot` 思路、stgraber 落地?默认按 maintainer 所作处理,不计入 Rory 风格,但保留「Rory 可能影响了修复方向」的可能。

3. **PoC 脚本作者的非 100% 确认(材料 D/E)**:仅靠 finder credit + sentinel 指纹归因,没有「这个文件是 rmcnamara-snyk 上传」的元数据。GitHub user-attachments 不暴露上传者。**结论**:高可信度但非铁证。若 maintainer 在披露前重写了 PoC,则风格会偏 maintainer。但两脚本共享的 sentinel 命名 + 两幕结构 + 清场习惯,跨两个不同 CVE 重复出现,「同一作者 = Rory」仍是最简解释。

4. **commit search 只返回 14 条**:其中 5 条在 `rmcnamara-test/terraform-provider-example`(测试 repo,2023-11)、7 条在 `snyk-labs/github-actions-scanner`(2024-06)、2 条在 lxc/incus + canonical/lxd(2026-01,同一修复)。**未解**:Rory 是否在 Snyk 内部 repo 或其他未索引处有更多表达?无法从公开侧证实。公开足迹在 2023→2024→2026 三段稀疏出现,中间有大段空白。

---

## 信息不足之处

1. **无任何 advisory 正文可归到 Rory**:9 条全由 maintainer 发布。若想分析「Rory 怎么向公众描述一个漏洞」,**该数据集不存在**——他从不亲自向公众描述,只向上游报告。
2. **无 blog / tweet / talk 文本**:无法做词频、句长、修辞性分析。本维度的「表达 DNA」是从 **2 条 commit message + 2 个 PoC 脚本**提取的,样本量极小,特征稳定性需谨慎对待。
3. **PoC 作者元数据缺失**:user-attachments 不暴露上传者,归因只能靠 finder credit + 风格指纹,做不到铁证。
4. **环境限制**:WebSearch 不可用、`web.archive.org` WebFetch 被屏蔽,无法穷尽「全网是否存在他署名的文章/演讲」。本报告的「未发现」是基于 GitHub API + NVD + 上游仓库 + Snyk 站内的强负证据,**非「全网不存在」**。若他曾在 Snyk 内部 Confluence、内部 talk、付费墙后的内容里表达过,公开侧无法触达。
5. **github-actions-scanner 的表达归属**:Rory 在此 repo 有 commit,但 README/talk/blog 均团队署名,无法把其中散文归到他。该 repo 只能佐证他的 commit 风格(祈使句、小写、无客套),不能提供段落级表达样本。

---

## 一句话总结

Rory McNamara 的表达 DNA 是**「让漏洞与代码自我陈述,本人退到 credit 字段之后」**——在 9 个 high/critical CVE 的产出下,他公开的文字产出压缩到 2 条 commit message + 2 个 PoC 脚本,且 commit body 用 `potential ... should ... manage to make it through` 的让步句式、subject 用 `Use X instead of Y` 的对比命名、PoC 用 `/<name>_command_exec_poc` sentinel 自证。这与 Tavis/Jann/Ian/Liran(含 Snyk 同事 Liran)的「finder 即 communicator」范式构成**系统性反例**:他把高产出与高曝光解耦,把面向公众的叙事权系统性地让渡给上游 maintainer。

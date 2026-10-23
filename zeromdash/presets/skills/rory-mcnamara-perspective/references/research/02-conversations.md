# Rory McNamara — 长对话与即兴思考

> **2026-07-28 自我纠正声明**:本文件第一版基于「`snyk.io/blog/author/*` 全 404 + Wayback CDX 检索 leaky/vessel/21626 = 0 条 + GitHub `rmcnamara-snyk` 零 repo/starred」得出「零公开 persona」的结论。**该结论已被 Phase 1 并行 agent 证伪**:
> - Snyk 有 **contributor 页**(`snyk.io/contributors/rory-mcnamara/`,非 `/blog/author/`),Wayback 18 个快照(2024-02-25 起),含 Rory 署名文章——第一版只查了 `/blog/author/` 是**方法论错误**。
> - Rory 有**更早的个人 GitHub 账号** `psychomario`(2011-09-10 创建,Name=Rory McNamara,3 个公开 repo、50 followers)——第一版搜 "Rory McNamara Snyk" 时曾瞥见 `psychomario` 但未核实即跳过,是**疏漏**。
> - `labs.snyk.io` 有 Rory 署名的深度博客(Leaky Vessels deep-dive)。
> - 5 条归档推文来自 `@PsychoMario`(其他 agent 报告 + team-lead skill 描述;我未独立核实)。
>
> 但本文件的**核心维度结论仍然成立**:未核实到任何播客、会议演讲、AMA、panel、webinar 或长视频采访。下方保留并修正。

## 调研方法(修正后)

针对任务目标(播客、长视频、AMA、深度采访、即兴表达),使用的手段:

1. **GitHub API 直查**:`api.github.com/users/rmcnamara-snyk` 与 `api.github.com/users/psychomario`(后者为第一版遗漏的个人账号,由 Phase 1 时间线 agent 发现);`api.github.com/advisories/<GHSA>` 逐条核实 credits;`api.github.com/search/issues`、`api.github.com/search/commits` 跨上游仓库。
2. **Snyk 站点**:第一版只查了 `/blog/author/<slug>/`(全 404,但这是**错误 URL 模式**)——正确路径是 `/contributors/rory-mcnamara/`(Wayback 18 快照)。`labs.snyk.io` 子域含 Rory 署名深度博客。
3. **GitHub Advisory 数据库**:`?query=credit:rmcnamara-snyk`(9 条)与 GHSA REST API 逐条 `rory_credited=True` 交叉核实。
4. **Wayback Machine**:CDX JSON API(`web.archive.org/cdx/search/cdx`)。第一版用 `filter=original:.*(leaky|vessel|21626).*` 在 `snyk.io` 域检索得 0 条——但该 filter 不匹配 `/contributors/rory-mcnamara/` 这种 URL(不含 leaky 关键词但含 rory)。修正后用 `url=snyk.io/contributors/rory-mcnamara` 直查得 18 快照。
5. **搜索引擎**:WebSearch 工具在本环境**不可用**(只返回 "I'll search…" 占位语);Google/Bing/DuckDuckGo HTML 经 curl **被反爬阻挡**。
6. **NVD REST API**:references 全量(9 条 GHSA references 里确实 0 条 snyk.io URL——但这只证明 advisory 不链 writeup,不证明 writeup 不存在)。
7. **Podchaser / YouTube / Wiz 博客 / Krebs archive**:Podchaser 超时;YouTube 搜索页需 JS;Wiz 博客对应 URL 404;Krebs 搜索只返回 RSS feed URL。
8. **跨 agent 交叉核实**:Phase 1 并行的 01-writings / 03-expression / 04-others / 05-decisions / 06-timeline agent 各自独立核实,纠正了本文件第一版的疏漏。

**可信度标记**:一手 = 他本人账号产出的痕迹(GitHub profile / advisory credit / 署名博客 / 推文);二手 = 他人转述/报道;推测 = 基于证据的推断。

**最关键的方法论限制(仍成立)**:WebSearch 不可用 + Google/Bing/DDG 被反爬 + YouTube/Spotify/Podchaser 需 JS。因此**无法对"全网是否曾出现过他的播客/视频/AMA/会议演讲"做穷尽性正面证明**。本报告"未发现"是基于 GitHub API / Snyk 站内 / Wayback CDX / NVD / 上游仓库 / 并行 agent 交叉核实的**强负证据**,而非"全网不存在"。

---

## 对话/演讲清单(按时间倒序)

**核心结论(修正后仍成立):未核实到任何一手口头来源——播客、会议演讲、AMA、panel、webinar、长视频采访 = 0。**

经下列信源交叉核查:
- Snyk events 页 `snyk.io/events/` 只列 3 个 2026 年未来活动,无过往演讲存档、无 speaker 详情。
- GitHub `rmcnamara-snyk` profile:`public_repos=0`、`starred=0`、`orgs=0`、`gists=0`、`following=0`、`twitter_username=None`、`blog=""`、public events 列表为空。**注意:这是 Snyk 企业账号(2023-07-09 创建),仅用于 advisory credit;他的个人账号 `psychomario` 另有 3 个 repo(非安全研究类:Bloom filter 库、audiobook 工具)。**
- 9 条 GHSA 的 references 字段 0 条 snyk.io URL——但 `labs.snyk.io` 有 Rory 署名深度博客(其他 agent 核实),只是 advisory 不链。
- 上游 6 仓库(runc/buildkit/podman/buildah/snapd/incus)`author:rmcnamara-snyk` 的 issue/PR/comment = 0 条(全走私有 Security Advisory 通道)。
- Podchaser 搜索超时;YouTube 搜索页经 WebFetch/curl 仅返回首页 footer。
- 5 个并行 agent(01/03/04/05/06)均未发现任何播客/演讲/AMA/采访。
- **最接近"即兴表达"的素材**:5 条归档推文 `@PsychoMario`(05-decisions agent 报告 + team-lead skill 描述引用;我未独立核实——Wayback CDX 对 twitter.com/PsychoMario 查询返回空/503,Twitter 归档覆盖率本身不稳定)。

**因此本节清单为空。** 但必须区分:**"无口头来源"≠"无公开 persona"**——后者第一版错误声称,实际他有 contributor 页、署名博客、个人 GitHub 账号、推文。详见下方修正与跨文件引用。

---

## 被追问时的回答模式

**未核实到口头来源——此维度信息不足。**

无可核实的播客/AMA/采访 transcript,无法观察他在被追问时的回答套路。推文 `@PsychoMario` 若能核实或可部分填补,但我未独立核实到内容。任何关于"他如何处理挑战性问题"的描述都将是编造。

---

## 即兴类比库

**未核实到口头来源——此维度信息不足。**

无 transcript、无演讲录像、无采访记录,无法提取即兴类比。**最接近的候选是推文**——若 `@PsychoMario` 5 条归档推文可核实,可能含即兴思考,但本调研未能抓到原文。建议后续用 Wayback 直接 fetch 已知推文 URL(需先定位具体推文链接)。

---

## 立场演化(对话中改变的观点)

**未核实到口头来源——此维度信息不足。**

无可核实的口头表达,无法追踪立场修正。其 advisory 文本(由上游维护者撰写)也未显示出立场反复。

---

## 拒绝回答 / 回避的话题

**未核实到口头来源——此维度信息不足。**

无对话样本,无法识别回避边界。

**自我纠正**:第一版曾写"GitHub `following=0`/`starred=0`/无 Twitter 是主动最小化 persona 的行为回避"——**此推测过度**。修正:`rmcnamara-snyk` 企业账号零关注/零 starred 是企业账号常态(不代表个人行为);他有个人账号 `psychomario` 与 `@PsychoMario` 推文,说明**并非主动零 persona**。他回避的更可能是"作为个人在安全社区公开立论",而非"完全不公开"——但这也是推测,不立为结论。

---

## 口头 vs 书面差异(修正后)

**整体差异(修正后):他的"书面"维度并非为零,但"口头/即兴"维度仍近乎为零。**

可核实的"表达"形态(全部一手,经 Phase 1 多 agent 交叉核实):

| 形态 | 量 | 来源 | 备注 |
|------|----|------|------|
| GitHub Security Advisory credit(reporter) | 9 条 | `api.github.com/advisories/<GHSA>` 全 `rory_credited=True` | Go 容器生态,详见 06-timeline |
| Snyk contributor 页 + bio 原文 | 1 页(18 快照) | `snyk.io/contributors/rory-mcnamara/` live + Wayback | 标题 "Staff Research Engineer, Snyk"(2024)→ "Staff Security Researcher"(2026)。**bio 自述(一手)**:"Long-time bug bounty hunter, ex-pentester, and AppSec engineer. Rory is passionate about race conditions and Linux exploitation." |
| Snyk 博客(contributor 索引署名) | 5 篇 | "Written by Rory McNamara" byline | Safe Path Handling(2026)、AI Glossary(2023,无个人 byline)、AWS security(2022)、Top 10 acronyms(2021)、CTI deep dive(2021)——01-writings agent 核实 |
| labs.snyk.io 署名深度博客 | ≥2 篇 | Ubuntu privesc + Leaky Vessels deep-dive | Wayback 归档存在(CDX 确认);Leaky Vessels deep-dive 署名 Rory、编辑 Jamie Smith(04-others 核实) |
| 公开 GitHub commit(含上游修复) | 14 条 | `api.github.com/search/commits?q=author:rmcnamara-snyk`,邮箱 `rory.mcnamara@snyk.io` | 含 2 条 Incus 上游修复(`lxc/incus` 0e0cf45 + `canonical/lxd` dbc1323818,2026-01-17,CVE-2026-23953 newline 注入)——01-writings agent 核实,身份铁证 |
| Incus PoC 脚本 + 修复 patch | .sh(1751B)+ .patch(3833B) | GHSA-7f67-crqm-jgh7 的 user-attachments,全文已 curl 抓回 | 03-expression / 01-writings agent 均核实;代码风格可提取 |
| 个人 GitHub 仓库 | 3 个(psychomario) | rbloom / bragibooks / m4b-merge | 非安全研究类,2023-09/10 更新 |
| 归档推文 | 5 条(@PsychoMario) | 05-decisions agent 报告 + team-lead skill 引用 | **我未独立核实原文** |

**口头/即兴维度**:**仍为零(未核实)**——无播客、无演讲、无 AMA、无采访、无长视频。推文是唯一可能填补"即兴思考"的素材,但未抓到原文。

**与同行的对比(修正后)**:
- **Tavis Ormandy**:大量博客 + oss-security prolific + (推测有播客/演讲)。
- **Jann Horn / Ian Beer**:P0 博客 + 会议演讲。
- **Liran Tal(Snyk 同事)**:Snyk prolific 博客 + 会议演讲。
- **Rory(修正后)**:有署名博客 + contributor 页 + 推文,但**无播客/演讲/AMA/采访**——他的"公开表达"全部是**书面、可编辑、非即兴**形态。这与第一版"零 persona"的判断不同:他不是不公开,而是**只通过可控的书面渠道公开,回避即兴/口头/被追问的形态**。

**推测(标注为推测)**:Rory 选择"书面为主、回避口头"可能反映对"可控表达"的偏好——书面可被编辑/审核,口头易失言。但这只是从形态分布推断,非本人声明。

---

## 披露协调轶事(口头独有信息)

**未核实到口头来源——此维度信息不足。**

无可核实的口头叙事。可核实的披露协调事实(一手,来自 advisory references 与 oss-security 公开档,详见 04-others 与 06-timeline):
- CVE-2024-21626 协调方是 **Aleksa Sarai (SUSE / cyphar)**。oss-security 公告由 Sarai 署名。
- **Sarai 在 GHSA 正文明确写**:"Credit for discovering and reporting the original vulnerability goes to Rory McNamara from Snyk"(04-others agent 核实原文)。
- **Solar Designer 回帖**:"Thank you and others you credit"——不点名 Rory,只通过 Sarai 间接致谢。
- runc 1.1.12 修复为一次合并提交包含 4 处独立修复(对应 4 个 attack 变体:Rory=attack 1、Sarai=2/3b、lifubang=3a)。
- BleepingComputer(2024-02-04 归档)直接点名:"discovered by Snyk security researcher Rory McNamara in November 2023"(04-others agent 核实)——**这是媒体唯一直接点名 Rory 为主角的实例**。
- 其他媒体(The Hacker News、Wiz 博客)不点名 Rory,只归功 "Snyk" 品牌(04-others agent 核实)。

以上是**公开档案可证的事实**,但都是"被他人描述",非"他口头自述的轶事"。

---

## 矛盾与未解之处(含自我纠正)

1. **第一版"零公开 persona"结论已被证伪**(详见顶部自我纠正声明)。contributor 页、署名博客、个人 GitHub 账号、推文均存在。**未解**:为何 Snyk `/blog/author/` 模式 404 而 `/contributors/` 模式存在?Snyk 站点架构使然,非 Rory 个人问题。

2. **GitHub profile 的 advisory credit 计数与实际不符**:profile 徽章写 "7",实际 9 条(详见 06-timeline,该 agent 同样记录)。

3. **"Leaky Vessels" 品牌名 vs Snyk writeup**:第一版因 Wayback filter 过窄得出"Snyk 零 writeup"——**修正**:`labs.snyk.io` 有 Rory 署名 deep-dive,contributor 页 18 快照含正文。但 `leakyvessels.com` 域名 Wayback 仍仅 2015–2016 不相关快照(Snyk 2024 年确未用此独立域)。

4. **Snyk 博客搜索行为异常**:`?s=leaky+vessels` 返回全站 1653 条不过滤——Snyk Next.js 站点搜索 bug,导致无法用站内搜索定位帖子。这不能用于"他没写博客"的证据。

5. **头衔不一致**(05-decisions / 06-timeline agent 发现):2024 HTML title = "Staff Research Engineer";2026 JSON-LD = "Staff Security Researcher"。是否升职/改 title 未解。

6. **CVE-2024-23326 已证伪归属**(01-writings agent NVD 核实):该 CVE 是 **Envoy(非 Istio)且非 Rory 的**——05-decisions agent 曾提示可能归他,01-writings agent 经 NVD 推翻。本文件第一版曾把"可能归他"写入,此处纠正为**已否定**。

7. **psychomario 与 rmcnamara-snyk 的关系**:同姓名(GitHub API 均返回 Name=Rory McNamara),psychomario(2011, 个人项目)与 rmcnamara-snyk(2023, Snyk 企业账号)是同一人的强证据但非铁证(无公开邮箱直接关联)。**补充**:01-writings agent 核实 14 条公开 commit 邮箱为 `rory.mcnamara@snyk.io`(Snyk 企业邮箱),确认 rmcnamara-snyk 账号的 Snyk 身份铁证——但这不直接桥接 psychomario。

8. **@PsychoMario 推文**:05-decisions agent 与 team-lead skill 均引用 5 条归档推文,但我经 Wayback CDX 未独立核实(Twitter 归档覆盖率不稳定)。**未解**:推文原文内容未能纳入本文件。

9. **bio 自述(一手,新增)**:01-writings agent live WebFetch 抓到 contributor 页 bio 原文:"Long-time bug bounty hunter, ex-pentester, and AppSec engineer. Rory is passionate about race conditions and Linux exploitation."——这是罕见的本人立场声明(背景:bug bounty hunter + 前渗透测试 + AppSec 工程师;兴趣:race conditions + Linux exploitation)。**对 Phase 2 价值极高**:bio 是除行为反推外,唯一可作"他这样想"依据的一手来源。详见 01-writings.md。

---

## 信息不足之处(诚实标注)

1. **口头来源全维度信息不足**:播客、长视频、AMA、会议演讲、panel、webinar、采访——**均未核实到一手来源**。这是本任务的核心目标维度,结果是空集。原因:(a) WebSearch 不可用 + Google/Bing/DDG 被反爬;(b) YouTube/Spotify/Podchaser 搜索页需 JS;(c) 即便搜索引擎可用,5 个并行 agent 也未发现——使人合理推断口头来源确实稀缺,但**非穷尽证明**。

2. **@PsychoMario 推文原文未获取**:这是最可能填补"即兴思考"维度的素材,但 Wayback CDX 对 Twitter 覆盖不稳定,本调研未抓到原文。其他 agent 报告 5 条归档推文存在。**后续应直接定位具体推文 URL 再 fetch**。

3. **YouTube / Spotify / Apple Podcasts / Podchaser 的平台内搜索无法生效**:JS 渲染问题。

4. **LinkedIn 需登录**:无法核实职业时间线、过往雇主、是否曾公开演讲。Black Hat USA 2026 即将举行(Snyk 是赞助),但无证据 Rory 会演讲。

5. **Reddit / Hacker News 的 site: 搜索不可用**(WebSearch 失效)。04-others agent 通过 HN Algolia API 核实了 Leaky Vessels 讨论帖(25 评论、63 points),但 Rory 关键词零命中——社区讨论不关注发现者身份。

6. **Snyk 内部内容(内部 webinar / 闭门演讲)不可见**。

7. **2024-01-31 之前的披露协调私信不公开**:他与 Sarai / lifubang 如何协调、Snyk 内部流程如何,均无公开档案。

---

## 给后续阶段(框架提炼)的可操作输入(修正后)

本维度(口头/即兴)为空,但 Phase 1 其他 5 个文件产出了**足够支撑思维框架提炼的硬证据**:

1. **研究域聚焦**:9/9 在 Go 容器生态(06-timeline 核实精确日期)。
2. **发现模式**:反复在"运行时/构建器在边界(fd/mount/cwd/entitlements)上的不变量违反"上找洞(05-decisions)。
3. **披露通道偏好**:全部走 GitHub 私有 Security Advisory + 上游协调,但**配套 Snyk 署名博客 deep-dive**(labs.snyk.io)——第一版漏检(04-others 核实)。
4. **协作模式**:与上游维护者(Sarai、stgraber)和同行(lifubang)合作多变体合并披露;Sarai 在 GHSA 正文点名致谢 Rory(04-others 核实原文)。
5. **书面为主、回避口头**:有 contributor 页 + 署名博客 + 推文,但无播客/演讲/AMA/采访——偏好"可控书面表达"而非"即兴口头表达"。这是**修正后的 persona 特征**,非第一版错误的"零 persona"。
6. **企业品牌托底**:个人账号 `psychomario` 用于个人项目,安全研究产出全挂 Snyk 品牌(`rmcnamara-snyk` 企业账号 + Snyk contributor 页 + labs.snyk.io 署名)——05-decisions agent 提炼为"企业品牌 persona 律"。

这些可被 Phase 2 蒸馏成思维框架,**依据是行为/产出 + 其他 5 个文件的交叉核实**,而非"他的口头自述"——任何"他这样想"的表述都应改写为"他这样做 + 这样写,因此可推断他这样想"。

---

## 信源清单(全部一手,均可复核,含修正后新增)

- `https://api.github.com/users/rmcnamara-snyk` — Snyk 企业账号(2023-07-09,Staff Security Researcher,0 repos/starred/orgs/gists,no Twitter/blog on this account)
- `https://api.github.com/users/psychomario` — **个人账号(2011-09-10,Name=Rory McNamara,3 repos,50 followers)** ← 第一版遗漏
- `https://github.com/advisories?query=credit:rmcnamara-snyk` — 9 条 credited advisories
- `https://api.github.com/advisories/GHSA-xr7r-f8xq-vfvv` 等 9 条 — `rory_credited=True` 已核实
- `https://web.archive.org/cdx/search/cdx?url=snyk.io/contributors/rory-mcnamara` — **18 快照(2024-02-25 起),标题 "Rory McNamara - Staff Research Engineer, Snyk"** ← 第一版漏检
- `https://web.archive.org/web/20240225235641/https://snyk.io/contributors/rory-mcnamara/` — contributor 页快照正文
- `labs.snyk.io` Rory 署名深度博客(Leaky Vessels deep-dive)— 04-others agent 核实
- `https://api.github.com/repos/lxc/incus/commits/0e0cf45ecdcc` 等 — Incus 修复 commit Signed-off-by 含 snyk 邮箱(03-expression 核实)
- `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2024-21626` — references 全量
- `https://www.openwall.com/lists/oss-security/2024/02/01/1` — Solar Designer 回复 Sarai 原帖
- `https://raw.githubusercontent.com/opencontainers/runc/main/MAINTAINERS` — Rory 不在维护者名单
- BleepingComputer 2024-02-04 归档:"discovered by Snyk security researcher Rory McNamara in November 2023"(04-others 核实)
- HN Algolia API:`https://hn.algolia.com/api/v1/search?query=leaky+vessels`(25 评论,Rory 关键词零命中,04-others 核实)

## 跨文件引用(Phase 1 其他维度,均为独立核实)

- `01-writings.md` — 著作维度(advisory 文本作者归属、commit message、PoC 脚本)← 待超时 agent 收尾
- `03-expression.md` — 表达 DNA(沉默即风格、代码即表达、对比式修复命名)← 已完成
- `04-others.md` — 他者视角(BleepingComputer 点名、Sarai 致谢原文、媒体去人格化)← 已完成
- `05-decisions.md` — 决策模式(race-condition 锚定、批量协调、企业品牌 persona)← 已完成
- `06-timeline.md` — 时间线(psychomario=2011、rmcnamara-snyk=2023-07-09、Leaky Vessels=2024-01-31、Incus=2026-01-22)← 已完成

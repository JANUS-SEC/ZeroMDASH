# Rory McNamara — 表达 DNA 与碎片表达

> 调研日期: 2026-07-28
> 目标: Snyk Staff Security Researcher
> 重点: 社交媒体碎片表达 + 长文写作风格 + 研究主题映射出的视角

---

## 调研方法

**搜索路径与可信度**

1. **GitHub REST API + WebFetch on github.com**（一手 / 元数据）
   - `api.github.com/search/users` 搜 "Rory McNamara" → 2 个账号，强相关
   - 个人账号 `psychomario`（display name = "Rory McNamara"，50 followers，achievement: Arctic Code Vault / Pull Shark x2 / Starstruck）
   - 工作账号 `rmcnamara-snyk`（bio = "Staff Security Researcher"，company = "Snyk"，9 条 security advisory credits）

2. **Snyk contributor page**（一手 / 官方 bio）— `https://snyk.io/contributors/rory-mcnamara/`
   - 官方 bio 原文: "Long-time bug bounty hunter, ex-pentester, and AppSec engineer. Rory is passionate about race conditions and Linux exploitation."
   - LinkedIn 链接: `https://uk.linkedin.com/in/rorymcnamara`
   - 列出 5 篇 article（URL 经 WebFetch 复核）

3. **Wayback Machine CDX API**（一手 / 归档推文）
   - `twitter.com/PsychoMario` 在 Wayback 有归档 → 确认 Twitter handle = **@PsychoMario**（与个人 GitHub 同名，强相关）
   - 共 5 条 status=200 的归档推文（2020-08 至 2022-01），逐条 curl 抓取并解析 og:description + tweet-text

4. **GitHub Security Advisory Database**（一手 / 研究成果清单）
   - `github.com/advisories?query=credit:rmcnamara-snyk` → 9 条 credited advisories
   - 抓取了 GHSA-m3r6-h7wv-7xxv（CVE-2024-23651 BuildKit race condition）与 GHSA-xr7r-f8xq-vfvv（CVE-2024-21626 runc breakout）的正文

5. **Snyk articles**（一手 / 长文）
   - 抓取 `snyk.io/articles/safe-path-handling/`（与 Stephen Thoemmes 合著，TOCTOU 章节与他的"race conditions"passion 强相关）
   - 抓取 `snyk.io/articles/threat-intelligence/`（evergreen SEO 内容，几乎无个人声音）

**信息源黑名单遵守**: 未使用知乎/微信公众号/百度百科。WebSearch 工具在本会话中损坏（回显伪回复），改用 curl + Wayback CDX + GitHub API + WebFetch 直抓。

**关键诚实声明**: LinkedIn 内容抓取被挡（HTTP 999）。Project Zero bug tracker 已迁移到 Google Issue Tracker，原 Monorail 页面失效。GHSA advisory 的 Description 正文是 **maintainer 写的**（tonistiigi / cyphar），不是 Rory 原文——credit 行只确认他"发现并披露"了漏洞。因此** Rory 的一手长文写作样本极少**，表达 DNA 主要靠 5 条归档推文 + 1 篇合著文章的技术章节 + 他的研究主题组合推断。精确句式统计不可得。

---

## 账号清单（已核实 vs 未核实）

| 平台 | Handle / URL | 核实状态 | 证据 |
|------|--------------|----------|------|
| Twitter/X | **@PsychoMario** (`twitter.com/PsychoMario`) | ✅ 已核实（一手） | Wayback CDX 5 条归档推文，handle 与个人 GitHub `psychomario` 同名 |
| GitHub (个人) | **psychomario** (`github.com/psychomario`) | ✅ 已核实（一手） | display name = "Rory McNamara"；fork 了 audiobook/bloom filter 工具（个人兴趣） |
| GitHub (工作) | **rmcnamara-snyk** (`github.com/rmcnamara-snyk`) | ✅ 已核实（一手） | bio = "Staff Security Researcher"，company = "Snyk"，9 advisory credits |
| LinkedIn | **rorymcnamara** (`uk.linkedin.com/in/rorymcnamara`) | ⚠️ URL 已核实，内容未取得 | Snyk contributor 页面官方链接；WebFetch 返回 HTTP 999（反爬） |
| Snyk | **rory-mcnamara** (`snyk.io/contributors/rory-mcnamara/`) | ✅ 已核实（一手） | 官方 contributor 页，含 bio 与文章清单 |
| Mastodon | — | ❌ 未发现 | 无任何公开证据指向 Mastodon 账号 |
| Bluesky | — | ❌ 未发现 | Wayback 无 bsky.app 归档 |
| Hacker News | — | ❌ 未核实 | 搜索无定论，未确认账号 |
| 个人博客 | — | ❌ 未发现 | GitHub profile 无 blog URL，psychomario 没有 `*.github.io` |

---

## 高频口癖与用词（量化）

> 样本: 5 条归档推文（含 1 条 4-tweet 线程）+ Safe Path Handling 技术章节 + 9 条 advisory 主题。**样本量小，频次仅作近似指示，不构成统计显著。**

| 口癖/用词 | 出现次数(近似) | 语境 | 来源 |
|------|------|------|------|
| `cont.` / `end`（线程分隔符） | 2 | 推文线程收尾，极简标记 | Wayback tweet 1404370343 / 1404370638 |
| `burning my bugs` 🙃 | 1 | 自嘲式描述披露自己 0day，倒笑脸=反讽 | Wayback tweet 1404360650 |
| `poke around` | 1 | 描述无目标时的研究方式："I'll just poke around and collect anything" | Wayback tweet 1404370343 |
| `More or less, yes.` | 1 | 对 Jann Horn 提问的测量式肯定 | Wayback tweet 1404370343 |
| `chains are more fun for me` | 1 | 坦白 chaining 的内在动机（不止 VRP 激励） | Wayback tweet 1404370343 |
| `feels like cheating` | 1 | 对 ClusterFuzz 聚合计数是否该剔除的伦理判断 | Wayback tweet 1294958253 |
| `privesc.sh` | 1 | 假想脚本名，dry humor 描述 chaining | Wayback tweet 1404370638 |
| `racy` / `inherently racy` | 2 | 描述 path-based 操作的竞态本质 | Safe Path Handling |
| `effectively impossible?` | 1 | Node.js TOCTOU 章节标题，问号=反讽/挑衅 | Safe Path Handling |
| `by construction` | 1 | 描述 cap-std 如何从根本上防止 traversal | Safe Path Handling |
| `gold standard` | 1 | 评价 Go `os.Root` 的语言级支持 | Safe Path Handling |
| `This is where things get difficult` | 1 | Node.js 章节口语化转折 | Safe Path Handling |
| `full control available` / `good primitives, manual assembly` | 2 | 章节标题式"裁决"短语 | Safe Path Handling |
| `a significant gap` | 1 | 评价 Node.js 缺少 `openat()`/`O_NOFOLLOW` | Safe Path Handling |
| `good reference implementation` | 1 | 评价 ChromeOS 的 path restriction 方案 | Safe Path Handling |
| `Congrats, great achievement!` | 1 | 简短祝贺他人成果 | Wayback tweet 1479907086 |

**主题层高频词（来自 9 条 advisory 标题，不是他的措辞但反映他的语料）**: container escape / breakout / race condition / leaked fds / process.cwd / cache mounts / mount stub / build time / newline injection / auth bypass / host file read-write。

---

## 句式指纹

- **平均句长倾向**: 推文里偏短、断片式（"More or less, yes." / "end"）；长文里中长句为主，但每段以短结论句收尾。
- **疑问句比例**: 推文样本 0 个疑问句（全是陈述/回复）。长文里他用**修辞性问句当章节标题**——"effectively impossible?"——把疑问句作为论点武器，而非真问。
- **类比密度**: 低。他不用"想象一下…"式比喻。核心 framing 是**时序窗口**（check 与 use 之间的可利用窗口）和**链**（chain），属于结构性隐喻而非修辞装饰。
- **第一人称使用率**: 推文里高——"I'll just poke around", "I have nothing resembling a chain", "I look specifically", "I can't point at a set"。长文（合著）里几乎隐去第一人称，改用第二人称"your code" / "you"。
- **线程结构**: 用 `cont.` / `end` 做极简分隔，不编号、不用 emoji 拆段（除了一个 🙃）。
- **括号旁白**: 偏爱圆括号补充——"straightforward (if verbose)"，"(since Go 1.24)"。
- **结论先行 vs 铺垫**: 结论先行。推文/章节标题直接给裁决，再解释。

---

## 风格标签（在每对坐标上定位）

| 坐标轴 | 定位 | 依据 |
|--------|------|------|
| 正式 ←→ 口语 | **中间偏口语（推文）/ 中间偏正式（长文）** | 推文全小写、`cont.`/`end`、`poke around`；长文精确第三人称 |
| 抽象 ←→ 具体 | **极具体** | 全是 CVE 编号、函数名（`openat`/`O_NOFOLLOW`/`chdir(2)`）、具体 runtime（runc/BuildKit/Incus/snapd/Podman） |
| 谨慎 ←→ 断言 | **测量式中位** | "More or less, yes" / "arguably more dangerous" / "It's hard to predict…"；但评价语言/runtime 时断言明确（"gold standard" / "significant gap"） |
| 学术 ←→ 通俗 | **通俗-技术** | 把 TOCTOU 讲得平易（"Your code validates a path, then operates on it"），但保留 "by construction" 这类学术精确措辞 |
| 长句 ←→ 短句 | **短句为主，长句收尾** | 推文极短；长文段落短，结论句干脆 |
| 铺垫型 ←→ 结论先行 | **结论先行** | 章节标题即裁决（"full control available" / "effectively impossible?"） |
| 数据驱动 ←→ 叙事驱动 | **数据/代码驱动** | 代码片段 + CVE + CVSS + 受影响版本；几乎不讲故事，除了"burning my bugs"这种自嘲碎片 |

---

## 争议立场与公开辩论

- **关于 bug chaining 与披露时机的立场**（公开对话 Jann Horn @tehjh，2021-06-14）: 他公开主张并践行"先收集多个 bug 凑成 chain，再一起报告"的策略，并坦白这是 VRP 激励 + 个人趣味双重驱动（"chains are more fun for me"）。这与他"ex-pentester / bug bounty hunter"身份一致——privesc 链是他的研究美学。**出处**: Wayback 归档推文 thread 1404360650–1404370638。
- **关于 bug 计数完整性的立场**: 在与 @attekett 讨论 chromium bug 计数时，他认为把 ClusterFuzz 聚合发现计入个人计数"feels like cheating to remove"——即倾向保留聚合数据但标注来源，反对为了美化数字而剔除。**出处**: Wayback tweet 1294958253。
- **关于 Node.js 安全能力缺位的立场**: 在 Safe Path Handling 中把 Node.js TOCTOU-safe 目录遍历定性为"effectively impossible?"且"a significant gap for a runtime that's widely used in CLI tools, build systems, and containerized environments"——点名为生态级缺陷而非单点 bug。这是他少见的、跨产品的公开评价。
- **关于 Go 语言级安全原语的立场**: 评价 `os.Root`（Go 1.24）为"the gold standard for language-level support"——罕见的高评价，表明他认可"语言层内建 capability"胜过"库层补丁"。
- **公开论战记录**: 未发现公开激烈对线。与 Jann Horn 的对话是同行请教式，非争论。整体姿态是"同行间的经验分享"，不是 polemicist。

---

## 幽默方式（举例）

- **干冷反讽**: "burning my bugs 🙃"——把"披露/烧掉自己 0day"用 burn 双关 + 倒笑脸标反讽。
- **假想命名式自嘲**: 把假想的 privesc 脚本命名为 `privesc.sh`，一本正经地说"these would go together in privesc.sh and result in a functioning chain"——dry humor。
- **问号即吐槽**: 用"effectively impossible?"当章节标题，问号承担"我也觉得离谱但还是得说"的态度。
- **极简裁决**: 用 "full control available" / "good primitives, manual assembly" 这类四词短语给整个语言生态下判决，冷峻而到位。
- **不用**: 未见 meme、未见 emoji 阵列（只一个 🙃）、未见夸张梗图。幽默浓度低但密度高，且都是 self-aware 型。

---

## 确定性语气

**测量式而非绝对化**。典型模式:
- "More or less, yes."（不完全 yes，留余地）
- "It's hard to predict the interactions of different bugs if some of them are fixed, so I can't point at a set and say…"（主动声明不确定性边界）
- "arguably more dangerous in practice"（注: 此句出自 cyphar 对 Rory attack 1 的扩写，但被 Rory 的 bug context 承载，反映同一圈子的语气）

**但在评价 runtime/语言设计时切换为断言式**: "gold standard" / "a significant gap" / "effectively impossible?"——对设计缺陷不留情面。

**比例估计**: 约 60% 测量/留余地，40% 断言。断言集中在设计评价而非具体 bug 严重性。

---

## 转推/引用习惯

- **爱转/引用**: chromium/Project Zero 的 bug 链接（`bugs.chromium.org`）、自己新提交的 PZ bug（如 ChromeOS arc-obb-mounter #2170）、他人成果（"Congrats, great achievement!"）。
- **引什么类型**: 具体漏洞条目 > 观点文章。几乎不转政策/行业新闻。
- **回复模式**: 在同行（Jann Horn、@attekett）的提问下展开技术对话，不是单向广播。是"猎人圈子里"的交流姿态。
- **数据局限**: 仅 5 条归档推文可见，转推/引用的完整习惯无法统计——**这是关键信息缺口**。

---

## 对厂商/产品的即兴评价

> 来源: Safe Path Handling（合著）+ advisory 主题映射 + 推文。注: Snyk 雇员身份使其公开评价集中在**技术设计层**而非商业批评。

- **Node.js**: "a significant gap for a runtime that's widely used in CLI tools, build systems, and containerized environments"——点名其缺少 `openat()`/`O_NOFOLLOW` 是生态级缺陷。罕见地直接。
- **Go**: 高度认可——`os.Root` 是"the gold standard for language-level support"，并建议读者读 Go 团队的 rationale blog。
- **ChromeOS**: 引为"good reference implementation"——对其 path restriction 方案给正面背书。
- **C/C++**: 评价为"full control available"且"straightforward (if verbose)"——认可能力但嫌啰嗦。
- **Rust**: "good primitives, manual assembly"——认可 cap-std 的 capability-based 设计（"prevents path traversal by construction"），但嫌需要手动组装。
- **runc / BuildKit / Podman / Incus / snapd**: 这是他的研究靶场，9 条 advisory 反复打这些 runtime 的 trust boundary / path handling / race condition。隐含评价: 这类工具的"build-time / mount / fd"路径处理普遍欠工程化。
- **ClusterFuzz**: "feels like cheating to remove"——对聚合计数的态度。
- **AWS / Kubernetes**: bio 与文章清单里有"AWS security: Complete guide"和 threat intel 等内容，但**这些是 evergreen SEO 内容，无个人语气**，不构成他的即兴评价证据。

---

## 禁忌词（从不用的）

> 样本量极小，下列为低置信度推断，非统计结论。

- 未见营销 hyperbole（"revolutionary" / "game-changing" / "next-gen"）。
- 未见 emoji 阵列或 meme 文本（只一个 🙃）。
- 未见对具体厂商的人身/商业攻击——批评止于设计层。
- 未见"AI will solve security"类 hype 表态（即便 Snyk 近年大量 AI 内容，他的 contributor 页面上只有 2023 的"AI Glossary"且无个人语气）。

---

## 信息不足之处（诚实标注）

1. **Twitter 样本量 = 5 条归档推文**（含 1 条 4-tweet 线程，实际 5 段文本）。这是表达 DNA 的**核心一手样本**，但远不足以做可靠频次统计。2022-01 之后的推文未被 Wayback 抓取——他近年（2024-2026 活跃于 container 研究）的社交媒体表达**完全缺失**。
2. **LinkedIn 内容 0 字节**——HTTP 999 反爬，URL 已核实但无法读取 posts / about / 经历细节。
3. **GHSA advisory Description 正文非 Rory 所写**——是 maintainer（tonistiigi / cyphar）的 writeup。Rory 的原始 report 文本（提交给上游的内容）不公开。因此**长文研究写作的纯一手样本 = 0**。
4. **Safe Path Handling 是合著**（与 Stephen Thoemmes），技术章节声音一致但**无法 100% 归因到 Rory**。TOCTOU/race-condition 主题与他 bio 强相关，是合理推断而非确证。
5. **Mastodon / Bluesky / HN / 个人博客**: 均未发现/未核实。安全圈不少人迁去这些平台，但无证据指向他有账号。
6. **Project Zero bug 2170（ChromeOS arc-obb-mounter）**: 他自报提交过（推文里贴了链接），但 Monorail 已迁移至 Google Issue Tracker，原页面失效，**无法读取他的 PZ bug writeup 原文**——这本来会是绝佳的一手长文样本。
7. **GitHub issue/PR 评论风格**: `org:snyk author:rmcnamara-snyk` 与 `author:psychomario` 搜索均 0 结果。他的 GitHub 评论样本 = 0。
8. **结论**: 表达 DNA 主要基于 **5 条归档推文 + 1 篇合著文章技术章节 + 9 条 advisory 主题映射** 推断。**精确句式统计不可得**；口癖表与风格坐标是**定性 + 极小样本量化**，用作 skill 蒸馏的方向性参考而非定量依据。他的真实长文研究写作风格，需要等他未来发一手 research blog 或 LinkedIn 长文才能补全。

---

## 附录: 一手原文索引（供后续 skill 蒸馏引用）

### A. 归档推文（Wayback Machine，一手）
- T1 (2020-08-16) `twitter.com/PsychoMario/status/1294958253844070400` — 回 @attekett，ClusterFuzz 计数/`feels like cheating`
- T2 (2021-06-14) `…/status/1404360650818822144` — 回 @tehjh (Jann Horn)，"burning my bugs 🙃" + PZ #2170 链接
- T3 (2021-06-14) `…/status/1404370343406587904` — "More or less, yes. … poke around … chains are more fun for me. cont."
- T4 (2021-06-14) `…/status/1404370638190559238` — "It's hard to predict … privesc.sh … end"
- T5 (2022-01-08) `…/status/1479907086234443788` — "Congrats, great achievement!"

### B. Snyk 官方 bio（一手）
- "Long-time bug bounty hunter, ex-pentester, and AppSec engineer. Rory is passionate about race conditions and Linux exploitation." — `snyk.io/contributors/rory-mcnamara/`

### C. 合著长文（一手，但混合 co-author 声音）
- `snyk.io/articles/safe-path-handling/` (2026-03-31, 与 Stephen Thoemmes 合著) — TOCTOU / racy / effectively impossible? / by construction / gold standard

### D. 研究成果清单（一手 credit，非他行文）
9 条 GHSA advisories credited to `rmcnamara-snyk`（详见 `02-writings.md`）:
- CVE-2024-21626 runc breakout（attack 1, 原始 fd leak）
- CVE-2024-23651 BuildKit race condition（CWE-362）
- CVE-2024-23652 BuildKit mount stub cleaner host access（Critical）
- CVE-2024-23653 BuildKit interactive containers entitlements（Critical）
- CVE-2024-1753 Podman build-time escape
- GHSA-pmf3-c36m-g5cf container escape at build time（High）
- CVE-2024-5138 snapd snapctl auth bypass
- CVE-2026-23953 Incus newline injection
- CVE-2026-23954 Incus image templating host file R/W

### E. 未取得（标注缺口）
- LinkedIn posts / about（HTTP 999）
- PZ #2170 writeup 原文（tracker 迁移，页面失效）
- 2022-01 之后的推文（Wayback 无归档）
- Mastodon / Bluesky / HN / 个人博客（未发现）

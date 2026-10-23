# 未通过独立复核

已达到最大修订次数 4；本文件是审计草稿，不得进入跨人物比较。

# Tarjei Mandt：漏洞研究成长分析

- 擅长领域：Windows/iOS 内核漏洞
- 独立复核：revise · 84/100

## 成长阶段

- **2007 · 密码学协议论文（待核）**：LinkedIn 自述 publications 段列出 LNCS 4435/2007 论文条目「Certificateless Authenticated Two-Party Key Agreement Protocols」，署名 Tarjei Mandt，无可读合著者姓名。Springer Link 章节页、DOI resolver、DBLP、Semantic Scholar 一手正文前序轮次均不可达（404、Anubis 反爬、空内容），作者一手署名未核实；复核所引「Tarak K. Mandt」署名来自搜索摘要而非一手，不作为已证事实。该阶段不作为科班起点已证事实使用，仅作待核身份歧义风险条目保留。（置信度：low）
  - 证据：tm-tl-2007-crypto, tm-r1-01
- **2010-2011 · Windows 内核子系统闭环研究方法建立**：形成针对单一子系统内部机制的闭环研究方法：先完整逆向分配器内部结构（pool descriptors、ListHeads 自由链表、lookaside lists、大块分配及 AMD64/x64 相关变化），再枚举攻击原语（ListEntry Flink、lookaside next、PendingFrees next、PoolIndex、quota process pointer 覆盖），以 CVE-2010-1893 案例验证，最后给出池元数据硬化建议。2011 年将目标从通用内存管理器转向 win32k.sys 图形内核子系统，方法演化为「回调重入→引用失效」的因果模型，覆盖 UAF（CVE-2011-1237 窗口对象、CVE-2011-1241 键盘布局对象）与状态校验缺陷两类漏洞。闭环结构由 primary PDF 支撑；同阶段混入 Pwnie 归属与 Black Hat 日期为 inferred/自述支撑。（置信度：medium）
  - 证据：tm-works-01, tm-works-02, tm-tl-2011-01-bh-dc-kernelpool, tm-tl-2011-08-bh-us-callbacks, tm-tl-2011-pwnie-privesc, tm-r1-01
- **2012 · 攻击面相邻主题与平台扩展**：研究目标由 Windows 内核池/win32k 扩展至 Windows 堆内部实现与 iOS 内核安全导览。2012 年内于 REcon、Black Hat USA、Hack in the Box Malaysia 三场不同会议各发表一次演讲。iOS 方向首篇与 Mark Dowd 联合发表。研究主题由 Windows 单平台扩展到 Windows 与 iOS 双平台。（置信度：medium）
  - 证据：tm-tl-2012-06-recon-atom, tm-tl-2012-07-bh-us-win8heap, tm-tl-2012-10-hitb-ios6, tm-tl-2012-pwnie-nom, tm-r1-01
- **2014-2016 · iOS 方向单组件推进与协处理器扩展**：iOS 方向由整体安全导览推进到针对单一子组件（early_random PRNG）的攻击，再扩展到相邻硬件协处理器（苹果 Secure Enclave Processor）。early_random 论文正文为 FlateDecode 压缩二进制未解码，是否沿用 Windows 闭环结构仅为推断，不作为 observed outcome 列入闭环机制。SEP 研究由三人联合发表。（置信度：medium）
  - 证据：tm-tl-2014-03-csw-earlyrandom, tm-tl-2016-08-bh-us-sep, tm-works-03
- **2025- · 现职 Catalyst Security（自链间接成立）**：现职关联由 GitHub 个人页自链间接成立（github.com/kernelpool Company=Catalyst Security、Website=catalystsecurity.com）。Catalyst 首页未点名研究对象，公司招聘方向（iOS/Android/Browser/Zero-Click）仅作雇主组织定位背景，不直接表述为研究对象个人研究方向。GitHub 当前公开仓库（mlx/mlx-lm/ds4 等机器学习相关 fork）与早期 Windows/iOS 内核研究方向脱节，缺乏说明该活动变化是否反映研究主题或方向变化的一手材料。（置信度：low）
  - 证据：tm-tl-current-catalyst, tm-deepconv-02, tm-r2-02, tm-r2-01

## 主要成长机制

### 单一子系统内部机制的闭环研究方法

起点：早期（2010-2011）已对内存破坏与堆风水前人工作（Shacham、Blazakis、Kortchinsky、Beck、Conover）进行复盘，并自建 cheatsheet（kernelpool_cheatsheet.pdf）的工具建设习惯，体现重复练习与工具沉淀。

练习与反馈：对单一子系统先完整逆向内部结构，再枚举攻击原语，以 CVE 案例验证，最后给出缓解建议。2010 年针对 Windows kernel pool（pool descriptors、ListHeads、lookaside lists、大块分配），2011 年针对 win32k.sys（GUI 线程、窗口管理器、用户对象、句柄表）。；缓解建议作为闭环终点（改进锁纪律、回调后空指针校验、池元数据硬化）；外部认可为 Pwnie 2011 Best Privilege Escalation Bug（MS11-034），归属依赖主题对应推断，Pwnie 官方页面未点名研究者。

能力与结果：形成由内部结构文档化→原语抽象→案例验证→缓解反馈的目标推进能力；该闭环结构作为 Windows kernel pool（tm-works-01）与 win32k.sys（tm-works-02）两项长文之间的重复验证模板，不外推到结构不同的子系统。；2010 kernel pool 长文枚举 5 种池元数据利用原语并以 CVE-2010-1893 案例验证；2011 win32k 回调长文枚举 UAF（CVE-2011-1237 窗口对象、CVE-2011-1241 键盘布局对象）与状态校验缺陷；Pwnie 2011 Best Privilege Escalation Bug（MS11-034，inferred）

置信度：medium；替代解释：闭环结构由 primary PDF 支撑，但 Pwnie 归属与 Black Hat 日期为 inferred/自述支撑，Black Hat 官方历史页与 infocon.org 镜像前序轮次抓取返回 403，未由会议官方页交叉验证；前序轮次无可达一手会议源用于升级该外部认可证据层级。iOS 方向（2014 CanSecWest early_random）是否沿用该闭环仅为推断，正文未核验，iOS 方向闭环证据弱于 Windows。

证据：tm-works-01, tm-works-02, tm-tl-2011-01-bh-dc-kernelpool, tm-tl-2011-08-bh-us-callbacks, tm-tl-2011-pwnie-privesc, tm-r1-01

### 攻击面相邻主题的连续展开

起点：2010-2011 已建立 Windows 内核子系统研究的内部机制基础，具备在同一技术栈内推进相邻主题的条件。

练习与反馈：在同一技术栈内按攻击面类别连续展开相邻主题：2010 池分配器→2011 win32k 回调→2012 REcon「Smashing the Atom: Extraordinary String-based Attacks」→2012 Black Hat USA Windows 8 Heap Internals（合著 Chris Valasek）。；会议演讲邀约与 Pwnie 2012 Most Innovative Research 提名（归属依赖主题对应推断，Pwnie 页面未点名研究者）。

能力与结果：形成研究产出的时序分布能力；2012 年内于 REcon、Black Hat USA、Hack in the Box Malaysia 三场不同会议各发表一次演讲。；2012 REcon「Smashing the Atom: Extraordinary String-based Attacks」；2012 Black Hat USA Windows 8 Heap Internals（合著 Chris Valasek）；2012 HITB Malaysia iOS 6 Kernel Security: A Hacker's Guide（合著 Mark Dowd）；Pwnie 2012 Most Innovative Research 提名（inferred）

置信度：medium；替代解释：短时间内的产出与会议邀约可能部分由攻击面可得性与市场关注度驱动，而非纯个人能力驱动；Pwnie 提名归属依赖主题对应推断，页面未点名研究者。

证据：tm-tl-2012-06-recon-atom, tm-tl-2012-07-bh-us-win8heap, tm-tl-2012-10-hitb-ios6, tm-tl-2012-pwnie-nom, tm-r1-01

### 通过合著关系进入新组件或新平台

起点：2012 年起 Windows 方向已有独立署名基础（2010 池、2011 win32k 均为独立署名或自述未列合著）。

练习与反馈：合著关系存在（可观察事实，由 LinkedIn 自述支撑）：2012 Black Hat USA Windows 8 Heap Internals 合著 Chris Valasek；2012 HITB Malaysia iOS 6 Kernel Security 合著 Mark Dowd；2016 Black Hat USA Demystifying the Secure Enclave Processor 合著 Mathew Solnik、David Wang。合著者涵盖堆研究者（Chris Valasek）与系统安全研究方向研究者（Mark Dowd、Mathew Solnik、David Wang）。合著作为学习或反馈渠道、能力来源为推断，无合著者实际指导或反馈的一手证据。；合著研究平台（Windows 堆、iOS 内核、苹果 SEP）与 Catalyst 招聘方向（iOS/Android/Browser/Zero-Click）交集仅 iOS 一项；Catalyst 首页未点名研究对象，现职关联仅由 GitHub 个人页自链间接成立，不构成机制性证据。

能力与结果：通过合著进入 iOS 内核（2012 HITB）与苹果 SEP（2016 Black Hat）等新平台。；2012 HITB Malaysia iOS 6 Kernel Security（合著 Mark Dowd）；2016 Black Hat USA Demystifying the Secure Enclave Processor（合著 Mathew Solnik、David Wang）

置信度：low；替代解释：研究平台由 Windows 向 iOS 迁移（2012 HITB）可能反映 2012 年前后 iOS 内核安全研究的市场关注度与攻击面可得性变化，而非个人能力驱动的平台迁移；合著者知名度不构成能力来源的证据。

证据：tm-tl-2012-07-bh-us-win8heap, tm-tl-2012-10-hitb-ios6, tm-tl-2016-08-bh-us-sep, tm-r1-01, tm-r2-02, tm-deepconv-02

## 可迁移与不可迁移

- 可迁移：内部结构文档化→原语抽象→案例验证→缓解反馈的闭环研究方法（仅在 Windows kernel pool tm-works-01 与 win32k.sys tm-works-02 两项自存档长文中得到验证，可能迁移到结构相似的内核子系统攻击面研究，但普适性未被更多案例验证）。
- 可迁移：同一技术栈内按攻击面类别连续展开相邻主题的研究产出时序分布（2010 池→2011 回调→2012 堆/字符串/iOS）。
- 可迁移：paper 与 slides 成对自存档于个人仓库的归档习惯（tm-works-03、tm-r2-01），仓库仅 1 次提交，提交日期 2025-04-23，提交信息 Add past research material，为历史材料一次性批量上传，时间跨度未核验。
- 不可直接迁移：特定时期的条件与时期性机会：2010-2012 Windows 内核池/win32k 攻击面可得性与会议（Black Hat DC/USA、REcon、HITB）邀约机会，非个人可复制的客观条件。
- 不可直接迁移：2012 年前后 iOS 内核安全研究的市场关注度与攻击面可得性变化驱动平台迁移的外部条件。
- 不可直接迁移：primary PDF 自存档与一手会议演讲机会（个人既有成果与会议关系网络），非新进入者可复制。

## 复核问题

- 语言规范违规（触发 revise）：stages[0].capability_change 使用「科班起点」一词。「科班」源自传统戏曲行当术语，属行业俚语，违反 CLAUDE.md 禁止黑话、俚语的要求。该词用于标注 2007 LNCS 论文是否构成研究对象的正式学术训练起点，应改用「正式学术训练起点」或「系统学术背景起点」等中性专业表述。
- 语言规范违规（触发 revise）：mechanisms[0].starting_conditions 使用「工具沉淀」表述。「沉淀」本义为化学或物理沉积过程，作为对工具文档长期留存与使用的描述属比喻性表达，违反 CLAUDE.md 禁止比喻的要求。应改用「工具积累」或「工具留存与复用」。
- 因果归类系统性问题：mechanisms[0].observed_outcomes 与 mechanisms[1].observed_outcomes 均将 Pwnie 奖项与提名（外部权威认可）列为 observed_outcome，与同机制的 feedback 字段构成归类重复。Pwnie 为同行评审的外部认可信号，属 feedback 范畴，而非研究方法或重复实践直接产出的论文与技术贡献。observed_outcomes 应仅列由方法或实践直接产出的可核验技术成果。该问题在两个机制中重复出现，属系统性归类错误。
- stages[0].capability_change：将「该阶段不作为科班起点已证事实使用，仅作待核身份歧义风险条目保留」中的「科班起点」改写为「正式学术训练起点」或「系统学术背景起点」。原措辞「科班起点」含戏曲行话色彩的行业俚语，违反 CLAUDE.md 禁止俚语的要求。
- mechanisms[0].starting_conditions：将「并自建 cheatsheet（kernelpool_cheatsheet.pdf）的工具建设习惯，体现重复练习与工具沉淀」中的「工具沉淀」改写为「工具积累」或「工具留存与复用」。原措辞「沉淀」为化学/物理沉积过程的比喻性表达，违反 CLAUDE.md 禁止比喻的要求。
- mechanisms[0].observed_outcomes：将「Pwnie 2011 Best Privilege Escalation Bug（MS11-034，inferred）」从 observed_outcomes 移除。该条目为外部权威认可信号，已在同机制 feedback 字段中记录（「外部认可为 Pwnie 2011 Best Privilege Escalation Bug（MS11-034），归属依赖主题对应推断」），重复列入 observed_outcomes 构成归类错误。observed_outcomes 应仅保留由研究方法直接产出的技术贡献，即前两条（2010 kernel pool 长文的 5 种池元数据利用原语与 CVE-2010-1893 案例验证、2011 win32k 回调长文的 UAF 与状态校验缺陷枚举）。
- mechanisms[1].observed_outcomes：将「Pwnie 2012 Most Innovative Research 提名（inferred）」从 observed_outcomes 移除。该条目为外部认可信号，已在同机制 feedback 字段中记录（「会议演讲邀约与 Pwnie 2012 Most Innovative Research 提名」），重复列入 observed_outcomes 构成归类错误。observed_outcomes 应仅保留由研究实践直接产出的演讲与论文，即前三条（2012 REcon Smashing the Atom、2012 Black Hat USA Windows 8 Heap Internals、2012 HITB Malaysia iOS 6 Kernel Security）。
- stages[1]（period=2010-2011）：评估是否将 tm-r1-01 中已验证的一手自述条目「Locking Down the Windows Kernel: Mitigating Null Pointer Exploitation — Independent Research，2011-07-07」纳入该阶段证据或 mechanisms[0] 的 observed_outcomes。该条目与 2010-2011 内核缓解主题（池元数据硬化、回调后空指针校验）直接相关，且为 verified=true 的 first_hand_other 自述条目，当前未被任何 stage 或 mechanism 使用，属证据基础利用不充分。如纳入，须保持其 first_hand_other 自述层级与 reported 状态，不升格。
- 结论引用缺失或已作废：['tm-tl-current-catalyst', 'tm-deepconv-02', 'tm-r2-02', 'tm-r2-01']
- 结论引用缺失或已作废：['tm-tl-2012-07-bh-us-win8heap', 'tm-tl-2012-10-hitb-ios6', 'tm-tl-2016-08-bh-us-sep', 'tm-r1-01', 'tm-r2-02', 'tm-deepconv-02']

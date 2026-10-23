# James Forshaw：漏洞研究成长分析

- 擅长领域：Windows 与沙箱漏洞
- 独立复核：pass · 81/100

## 成长阶段

- **约2015年（仓库 copyright 起始年；奠基转折点本身未经一手来源核实） · 工具基础设施奠基：把研究方法沉淀为可复用 PowerShell/.NET 工具**：开始把 Windows NT API/对象管理器枚举、token 模拟、沙箱可达性测试固化为可被他人加载的 PowerShell/.NET 模块（NtCoreLib/NtApiDotNet、NtObjectManager、TokenViewer 等），并以 -ProcessId 冒充沙箱进程 token 的方式系统化枚举可访问资源。这一阶段的可验证产物是 sandbox-attacksurface-analysis-tools 仓库本身；该仓库的 copyright 起始年 2015 仅证明仓库存在年份，不证明'能力转折发生在 2015'。此后该工具链成为贯穿后续全部 writeup 的执行与验证介质，使研究从'一次性 PoC'转向'可复用研究基础设施'。（置信度：medium）
  - 证据：jf-works-003, jf-comm-01
- **2022-2024 · 工具-研究-输出闭环与多子系统并行写作**：在加入 Google Project Zero 后仍维持独立的个人研究输出渠道（个人博客 Tyranid's Lair），把同一套自建工具（NtObjectManager）反复用于不同 Windows 子系统（ACL、Kerberos 中继、DCOM OXID、Windows 11 on ARM64 符号解析、Windows sudo、Active Directory 访问检查），每次产出独立 writeup。研究-工具-写作形成双向反哺：工具支撑 writeup 验证，writeup 扩充工具用例。这一阶段建立了'用自建工具贯穿多子系统 + 持续长篇幅拆解单一技术原语'的可观察输出习惯。（置信度：high）
  - 证据：jf-decisions-01, jf-works-003, jf-comm-01
- **2025-2026 · 从单点 bug 到枚举框架，从不完整修复追踪到新版防御逐项突破**：晚期研究在两个方向上移：目标难度上移到 COM runtime/特权服务编排链（Dangling COM 对 CVE-2026-50343 'Dark Elevator' 的不完整修复做 custom marshaling 二次利用），输出形态上把单点 bug 上升为可批量枚举的 bug 类（随文发布 Get-ComDatabase/Import-Win32Module 扫描 machine hive 中 DLL 路径无法 LoadLibrary 解析的 in-process COM 类）；同时对新引入的防御机制（Windows 11 25H2 Administrator Protection）换多条路径逐项突破，单一机制连续发布多篇且各自独立报告约 9 个 bypass 并明示已修复（Admin Protection 与 UIAccess 两篇措辞不同），体现短周期迭代与逐项追踪修复的反馈回路。（置信度：high）
  - 证据：jf-rr1-001, jf-rr1-003, jf-rr1-004, jf-rr1-005, jf-timeline-01, jf-timeline-02, jf-timeline-03, jf-timeline-04, jf-timeline-05

## 主要成长机制

### 工具即研究记忆：把研究方法沉淀为长期可复用工具链，工具反向成为 writeup 的执行与验证介质

起点：Windows 沙箱/权限研究依赖大量 NT API 调用与对象管理器枚举，若无工具化沉淀，每次研究都需重写胶水代码；PowerShell/.NET 生态使把原生 NT API 包装为可加载模块成为可能。

练习与反馈：持续开发并维护 sandbox-attacksurface-analysis-tools 工具套件（NtCoreLib/NtApiDotNet、NtObjectManager、TokenViewer、OleViewDotNet 等），用 -ProcessId 冒充沙箱进程 token 判定可访问资源；并经历 v2.0.0 major refactor 长期维护。在个人博客与 Project Zero writeup 中反复用 NtObjectManager 发现 RPC 服务器信息、枚举 COM 接口、检查进程能力、最终经 ICreateObject 传入伪造 marshaled 对象。；GitHub issue 区自 2021-10 至 2026-02 持续有外部使用者提交 bug 与功能请求（如 #86 Get-AccessibleDsObject、#83 RpcEndpointMapper 数组越界、#55 Windows Server 2022 AccessViolation），形成使用者→作者的社区反馈回路；issue 既是 bug 报告也是对新 Windows 版本（Server 2022、25H2）兼容性的早期信号。3,572+ commits 与 2.3k stars/451 forks 表明长期迭代与外部采用。

能力与结果：形成'NT API/对象管理器/COM 枚举'的稳定方法基底与'用同一套工具贯穿多子系统'的可复用研究范式，使任何新 Windows 子系统的研究都能快速复用既有枚举/验证基础设施，而非从零搭起 PoC。；sandbox-attacksurface-analysis-tools 成为可被社区复用的研究基础设施（jf-works-003/jf-comm-01）；在个人博客（2022-2024）反复用 NtObjectManager 研究 ACL/Kerberos/RPC/AD 等不同子系统（jf-decisions-01）；在 Dangling COM writeup 中全程使用 OleViewDotNet/NtObjectManager 作为执行介质（jf-rr1-001）；外部使用者 issue 反馈驱动修复与对新 Windows 版本兼容性的跟进（jf-comm-02）

置信度：high；替代解释：工具长期维护也可能主要由雇主（Google Project Zero）对工具化产出的制度性激励与 GitHub 平台红利驱动，而非个人方法论习惯；issue 反馈回路的存在不必然证明作者据此调整研究方向，可能只是被动修复兼容性。但'同一套工具贯穿多个不同子系统 writeup'这一点难以仅用平台红利解释，更指向个人方法论的稳定性。

证据：jf-works-003, jf-comm-01, jf-comm-02, jf-decisions-01, jf-rr1-001

### 多路径逐项追踪 + 不完整修复二次研究：对同一防御机制换多条路径突破，对已修复 bug 追踪式二次利用

起点：Windows 防御机制常以'功能引入时即报告一批 bypass'的方式被首次披露，且厂商修复可能不完整；这为研究者提供了'同一机制多路径枚举'与'已修复 bug 的二次利用'两个可重复入口。

练习与反馈：对新引入的 Windows 11 25H2 Administrator Protection，连续发布两篇研究（Admin Protection 与 UIAccess），每篇各自独立报告约 9 个 bypass 并明示已修复；对 CVE-2026-50343（'Dark Elevator'）的不完整修复，转用 custom COM marshaling（IMarshal 返回悬挂 CLSID）经 CreateObjectTask 计划任务+全局命名事件启动 SYSTEM 级 dllhost（CustomMarshalAllowed=true）完成提权加载，形成 CVE-2026-66804。；厂商修复反馈（如 KB5067036 optional update 与 subsequent security bulletins，且明示'All the issues that I reported to Microsoft have been fixed'）构成'已修复→换路径/二次利用'的反馈源；UIAccess 文章显式引用前一篇 Admin Protection 作为先期工作（'In my last blog post I introduced...Administrator Protection'），显示同一机制内部的研究迭代。GetProcessHandleFromHwnd 深度拆解由'已公开披露的 UAC bypass（Quick Assist UIAccess 应用）'触发（'This was an API I didn't know existed until I found a publicly disclosed UAC bypass'），显示公开披露亦是研究选题的反馈源。

能力与结果：形成对'单一防御机制'做系统性多路径枚举、并对'已修复 bug'做追踪式二次利用的研究模式，使研究输出从单点披露升级为对机制整体覆盖与对修复完整性的持续审视。；Admin Protection 文章（2026-01-26）：'I found 9 separate means to bypass the feature' + 'All the issues ... have been fixed, either prior to the feature being officially released (in optional update KB5067036) or as subsequent security bulletins.'（jf-rr1-003）；UIAccess 文章（2026-02-12）：'In total I found 9 bypasses during my research that have now all been fixed.'，并引用前一篇 Admin Protection 为先期工作——两篇各自独立报告约 9 个 bypass，措辞不同（'9 separate means' vs '9 bypasses'），非跨文章混并（jf-rr1-004）；Dangling COM 文章（2026-09-21）：对 CVE-2026-50343 'Dark Elevator' 不完整修复的二次利用，产出 CVE-2026-66804（'I and 14 others reported'）（jf-rr1-001）；GetProcessHandleFromHwnd 深度拆解（2026-02-26）：由已公开披露的 Quick Assist UIAccess UAC bypass 触发（jf-rr1-005）

置信度：high；替代解释：'9 个 bypass'的报告数量可能部分受厂商赏金/披露窗口的制度性结构驱动（功能发布前集中报告），而非纯粹个人方法论的产物；'不完整修复二次利用'也可能只是机会主义跟进而非系统习惯。但跨两篇同机制文章 + 跨 CVE 二次利用 + 由公开披露触发的 API 拆解，三处独立出现更支持'系统性多路径/二次利用'是稳定模式而非偶然。

证据：jf-rr1-001, jf-rr1-003, jf-rr1-004, jf-rr1-005, jf-timeline-02, jf-timeline-03, jf-timeline-04, jf-timeline-05

### 可测量底层模型：用经验基准与内核结构/算法逆向建立可验证的底层模型，而非凭手感

起点：竞态条件研究需要可控地放大竞争窗口才能稳定触发；Windows 内核对象目录查找的耗时由对象目录深度、reparse 次数、哈希桶分布等可量化因素决定，这为'建立可测量底层模型'提供了可拆解的对象。

练习与反馈：在路径查找竞态研究中，用自写 C++ + NT syscall（如 NtOpenEvent）配合 QueryPerformanceCounter 做微秒级经验基准；用 WinDBG（dt nt!_OBJECT_DIRECTORY）核对内核结构；逆向 ObpLookupObjectName/ObpLookupDirectoryEntry 哈希算法；通过深嵌套对象目录（约 1.6 万层）、符号链接强制 reparse 循环（最多 64 次）、目录哈希桶（37 桶）有意哈希碰撞（NUL 前缀名）三种叠加手段人为放大单次查找耗时。原文给出：基线 'approximately 2μs'；长名 32000 字符 'approximately 35μs'；放大后 'the average lookup time is around 1300μs or approximately 40 times larger'（即 1300μs vs 35μs，约 40 倍）；最终 'it takes approximately 4.5ms to lookup the event'。文中显式引用作者本人 2021 年关于 file Opportunistic Lock 与虚拟内存访问捕获竞速放大的先期工作作为对比。；跨版本复测本身构成对'底层模型是否仍成立'的反馈：在 Windows 11 24H2（Surface Pro 11 / Snapdragon X Elite）上重测 2016 年原作的技术，量级变化成为模型有效性的反馈。需注意：该跨版本复测在本轮材料中仅此 1 例（2016 原作 → 2025 Win11 24H2 复测），不满足 repeated 验证，故作为 observed practice 而非独立机制证据。

能力与结果：形成'用经验基准 + 内核结构/算法逆向建立可测量底层模型'的研究习惯，使竞态/时序类研究从'手感式触发'升级为'可量化、可复现、可跨版本验证'的工程化方法。；路径查找竞态研究：三种叠加手段放大单次查找耗时，原文最终测量点 'it takes approximately 4.5ms to lookup the event'（jf-rr1-002/jf-works-002）；原文 'approximately 40 times larger' 对应 1300μs vs 35μs（放大后 vs 长名查找），为原文原始表述；'约 2250 倍'（2μs→4.5ms）为 synthesis 推导值，原文无 2250 此数字，需区分两个测量点（1300μs 放大后 vs 4.5ms 最终），不可混算为单一倍数（jf-rr1-002）；跨版本复测：2016 原作在 2025 年 Win11 24H2 上重测，并引用 2021 先期工作（file Opportunistic Locks 与虚拟内存访问捕获）作为对比——仅此 1 例，作为 observed practice（jf-rr1-002）

置信度：medium；替代解释：'可测量底层模型'在本轮材料中主要由路径查找竞态这一篇充分体现，跨子系统重复度不及前两个机制（工具链与多路径追踪）；该写作风格也可能部分源于 Project Zero 团队对'可复现测量'的统一要求而非个人特质。但'逆向内核哈希算法 + 三种叠加放大 + 微秒级基准'的组合在材料中可观察且相对有区分度，故保留为机制但 confidence=medium。

证据：jf-rr1-002, jf-works-002, jf-timeline-01

## 可迁移与不可迁移

- 可迁移：把研究方法（NT API/对象管理器/COM 枚举、token 模拟、沙箱可达性测试）固化为可被他人加载的 PowerShell/.NET 模块，并以 -ProcessId 冒充沙箱进程 token 的方式系统化枚举可访问资源——这一'工具即研究记忆'的沉淀方式可迁移至任何依赖大量原生 API 调用的系统研究。
- 可迁移：对新引入的防御机制做系统性多路径枚举（同一机制连续多篇、各自独立报告一批 bypass 并明示修复状态），并对已修复 bug 做追踪式二次利用——'多路径逐项追踪 + 不完整修复二次研究'是可迁移的防御审视模式。
- 可迁移：对竞态/时序类研究用经验基准（QueryPerformanceCounter 微秒级）+ 内核结构/算法逆向（WinDBG dt + 逆向哈希链）建立可测量底层模型，并通过深嵌套/reparse 循环/哈希碰撞等可控手段放大竞争窗口——'可测量底层模型'是可迁移的工程化研究范式。
- 可迁移：把单点 bug 上升为可批量枚举的 bug 类并随文发布扫描脚本（如 Get-ComDatabase/Import-Win32Module 扫描 machine hive 中 DLL 路径无法 LoadLibrary 解析的 in-process COM 类）——'单点 bug 通用化为枚举框架'是可迁移的输出习惯。
- 可迁移：用 GitHub issue 区作为使用者→作者的反馈回路，把外部 bug 报告当作对新系统版本兼容性的早期信号——'工具 issue 作为研究选题反馈源'是可迁移的社区协作实践。
- 不可直接迁移：Project Zero 团队品牌（2014 成立、零日研究使命、与厂商的直接披露通道如 KB5067036/security bulletins、'I and 14 others reported' 的多人协作披露）属组织资源，不随个人方法论迁移；个人在咨询背景（Context Information Security）与全职漏洞研究团队之间的转换也依赖特定雇主机会。
- 不可直接迁移：约2015年加入 Google Project Zero 的具体时机、招募条件与当时约束/备选项本轮无一手来源（jf-decisions-02 verified_in_run=false），不能作为可迁移的'决策模板'；早期 Pwn2Own 2013（jf-decisions-03）、2017 出版《Attacking Network Protocols》（jf-decisions-04）均未一手核实，不应据此推断可复制的路径。
- 不可直接迁移：对 Windows 内核 ObpLookupObjectName/ObpLookupDirectoryEntry 哈希算法、OBJECT_DIRECTORY 结构、COM runtime marshaling 编排链的领域知识，是长期深耕 Windows 单一生态的累积结果，具有生态锁定性，难以短期迁移到非 Windows 系统。
- 不可直接迁移：本轮材料未抓取到同事、团队负责人、会议主持或权威媒体对 Forshaw 的具体评价正文（external 维度整体缺失），因此无法从外部视角佐证其能力增长的归因；任何把'产出节奏'等同于'个人能力'的推断都受此缺口限制，存在幸存者偏差风险。
- 不可直接迁移：WebSearch 在多个取证节点返回 LLM 风格自述而非真实可引用搜索结果，导致早期时间线无法补证——这是本轮工具可用性的非迁移性条件，不应将其转述当作可引用事实。

## 复核问题

- mechanism#1 的'writeup→工具'反馈方向：抓取 sandbox-attacksurface-analysis-tools 仓库在 writeup 发布日期前后的提交史以验证 writeup 驱动的工具新增，或将'双向反哺'降述为'工具在 writeup 中被复用'的单向观察。
- mechanism#2 的'两篇各自独立报告约 9 个 bypass'：重读 Admin Protection（/2026/26/windows-administrator-protection.html）与 UIAccess（/2026/02/windows-administrator-protection.html）两篇正文的 bypass 编号/列表，明确两组 9 是不相交/可加还是重叠/子集，并在 observed_outcomes 标注，避免被误读为合计~18。
- mechanism#2 confidence=high：鉴于'repeated'验证仅基于 2026 年 8 个月窗口内的 4 篇文章且捆绑 3 种子行为，建议明示该 confidence 限于 2025-2026 窗口，或补充中期（2018-2022）是否存在同类多路径/二次利用模式的证据；若无则保持 high 但标注窗口范围。
- jf-timeline-01~05 的 source.url 仍为首页（https://projectzero.google/）：虽 jf-rr1-001~005 已提供正文页支撑，建议机制/阶段引用时优先以 jf-rr1 正文页为 source，jf-timeline 仅作时间线索引，避免首页摘要与正文页混引。

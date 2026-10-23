# Brandon Azad：漏洞研究成长分析

- 擅长领域：iOS/macOS 漏洞
- 独立复核：pass · 92/100

## 成长阶段

- **2016-05 至 2016-12 · macOS 内核本地提权的独立研究起点**：以 CVE-2016-1828（OSUnserializeBinary 释放后重用）结合 CVE-2016-1758（内核栈泄露）实现 OS X 10.10.5 本地提权，技术路径为 UAF→伪造 vtable→ROP 改写 cr_svuid 取 root，使用 lldb 反汇编、otool 检查内核二进制、ROPgadget 提取约 45000 个 gadget。此阶段确立其起点技术能力：XNU 内核源码审计、Mach trap 触发、ROP 利用。其对开发路径自述非顺遂，而是试错驱动（『There was a lot of trial and error and many, many hours debugging random kernel panics.』），并已建立可重复的可靠性度量（3000 次执行中崩溃 2 次的统计），显示其早期即以可重复评估而非仅追求可用为工作标准。（置信度：high）
  - 证据：azad-works-001, ba-tl-01, azad-conv-01
- **2017-01 至 2017-12 · 从单点提权转向可复用工具与内核内省基础设施**：2017-01-16 发表 physmem（CVE-2016-1825，IOHIDevice::setParamProperties 允许设置任意 IOKit 注册属性），通过实例化 IOPCIDiagnosticsClient 获得用户态物理内存读写，覆盖 sysent 表实现内核任意函数调用；2017-09-15 发表 memctl，将研究对象由 macOS 扩展到 iOS，工具定位从一次性提权转向可交互式内核内省与调试基础设施。方法学上出现转向：先系统性枚举 type-confusion 机会再选定目标，并把成果转化为可复用工具。同期 memctl 明确致谢 Ian Beer、Luca Todesco、Stefan Esser、Jonathan Levin 的先前工作，并指出 Ian Beer 的内核调试器文章与自己几乎同期完成，将其视为方向可行性的反馈信号；Stefan Esser 在 iOS 6/7 的 vtable-patching 技法被直接移植到 memctl。（注：ba-tl-02、ba-comm-04 所载 physmem 发布日期 2016-01-16 系证据层笔误，依据 azad-works-002 与 azad-r3-ev-001 一手再核验，真实 permalink 为 /2017/01/physmem-accessing-physical-memory-os-x/、日期 2017-01-16。）（置信度：high）
  - 证据：azad-works-002, azad-works-003, ba-tl-02, ba-tl-03, ba-comm-01, ba-comm-04
- **2018-01 至 2018-11 · iOS 攻击面系统化枚举与逆向方法论工具化**：2018 年内密集输出：3 月 CVE-2017-13868（ctl_ctloutput 未检查返回值的 XNU 信息泄露）与 ida_kernelcache（IDA Pro 重建内核缓存 C++ 类布局）；4 月把两参数内核调用原语扩展为最多 14 参数、可取完整返回值的 JOP 调用原语（iPhone 8 / iOS 11.1.2，payload 可压缩至约 768 字节），明确自述为对 memctl 旧 8 参数策略的改进版本（原句见 azad-r3-ev-002：『This is a refinement of memctl's first call strategy, which extends a 6-argument function call primitive into an 8-argument call.』）；6 月分析 iOS 12 kernelcache tagged pointers；7 月 XPC 字符串越界读取并类比 Heartbleed；9 月 CVE-2018-4280 launchd Mach 端口替换提权（blanket）；10 月 task_threads() 绕过平台二进制限制（threadexec），明确写道借鉴 Ian Beer triple_fetch 中检测函数返回的轮询策略、fileports 技法特别致谢 Ian Beer；11 月 CVE-2018-4331 com.apple.GSSCred XPC 竞态条件。此阶段形成『审计方向→漏洞→公开 writeup+开源工具』的稳定产出闭环，研究粒度由单一提权链细化为针对具体函数与子系统的缺陷定位，并随 Apple 平台演进持续更新逆向基础设施。同年 12 月独立发现并向 Apple 报告 MIG/voucher 漏洞。（置信度：high）
  - 证据：azad-works-004, azad-works-005, ba-tl-04, ba-tl-05, ba-tl-06, ba-tl-07, ba-tl-08, ba-tl-09, ba-tl-10, ba-tl-11, ba-comm-02, ba-comm-03, ba-comm-05, BAZAD-DEC-06
- **2018-12 至 2019-08 · 加入 Google Project Zero 与披露渠道迁移**：不晚于 2019-01-29 以 Project Zero 成员身份在团队博客发表《voucher_swap: Exploiting MIG reference counting in iOS 12》（署名『Posted by Brandon Azad, Project Zero』），研究产出渠道由个人博客迁移至团队研究博客，进入公开、系统化披露流程。本人自述『I discovered and exploited CVE-2019-6225, a MIG reference counting vulnerability.』并『I reported this vulnerability to Apple on December 6, 2018』；Ian Beer 2019-08-29 文章印证『Brandon Azad independently discovered and reported the same issue to Apple on December 6, 2018』与『iOS 12.1.4 (CVE-2019-6225)』。即 2018-12-06 报告日期与 CVE-2019-6225 编号同时由 voucher_swap 本人自述直接支撑，并由 In-the-wild iOS Exploit Chain 5 独立印证。此阶段维持向 Apple 直接报告渠道，并完成从个人漏洞报告者到团队公开披露研究者的过渡。（置信度：high）
  - 证据：BAZAD-DEC-05, BAZAD-DEC-06, azad-r1-ev-001, azad-r1-ev-002
- **2019 至 2020+ · 内核调试基础设施与硬件缓解绕过研究**：以 googleprojectzero 组织发布 ktrw（A11 iPhone 8 内核调试器，README 署名『Brandon Azad of Google Project Zero (bazad@google.com)』，LLDB 连接 iOS 12.1.2、tested as working on iOS 13.3），研究产出从利用工具扩展到内核调试基础设施，显示其在 Apple 平台版本更新后持续迭代工具的能力。公开材料称其 2020 年前后发表关于 Apple A12/A13 指针认证（PAC）绕过的研究，标志研究从 A11 调试延伸到新硬件缓解措施；但 Project Zero 新域名作者页与旧 Blogspot 单文 URL 均返回 404，本节点未抓取到正文一手页面，故该转向列为推断而非 documented。（置信度：medium）
  - 证据：ba-tl-13, ba-tl-14, ba-tl-15, ba-tl-16

## 主要成长机制

### 把一次性 PoC 转化为可复用工具

起点：2016 年起点阶段具备 XNU 内核审计、Mach trap 触发与 ROP 利用能力，但产出以单次提权 PoC（rootsh）为主，工具尚未通用化；同时其以 Stanford CS 系统与安全方向应届毕业生身份独立维护博客，缺乏机构协作产出。

练习与反馈：从 2016 年 rootsh 到 2017 年 physmem、memctl，到 2018 年 ida_kernelcache、threadexec、blanket，再到 2019 年 ktrw，反复为每一类研究方向配套发布独立可复用工具，并将研究过程向社区开源（MIT 许可、CC BY 4.0）。该实践跨 2016–2019 四个年度、覆盖 macOS 与 iOS 两个平台、横跨利用、内省、逆向、调试四类工具类别，重复出现。；工具开源后获得社区 fork 与复用（ktrw 700 stars/128 forks、ida_kernelcache 305 stars/86 forks、memctl 272 stars、blanket 262 stars），构成研究者间间接协作与反馈；其中 ktrw 托管于 googleprojectzero 组织而非个人账号，体现机构内协作产出。同时 memctl 致谢 Ian Beer 等同伴，将其并行进展作为自身方向可行性的反馈信号。

能力与结果：形成『研究难点→自建工具→工具复用驱动下一项研究』的循环：physmem/rootsh 为 macOS 物理内存读写与提权基线，memctl 为后续内核调用原语的验证与迭代载体（14 参数 JOP 调用原语明确自述为对 memctl 旧 8 参数策略的改进版本，原句见 azad-r3-ev-002），ida_kernelcache 把逆向方法论本身固化为工具，ktrw 把内核调试能力固化为基础设施。；memctl 成为后续内核调用原语的验证与迭代载体，14 参数 JOP 调用原语明确自述为对 memctl 旧 8 参数策略的改进版本（『This is a refinement of memctl's first call strategy, which extends a 6-argument function call primitive into an 8-argument call.』）；ida_kernelcache 把逆向方法论本身固化为工具，支撑后续 iOS 12 tagged pointers 分析等研究；ktrw 覆盖 iOS 12.1.2 与 iOS 13.3 两个版本，研究产出从利用工具扩展到内核调试基础设施

置信度：high；替代解释：该机制的高 confidence 判定存在发表偏差放大风险：成功的工具更易公开并保留，未公开的失败工具化尝试不可见，可能高估其工具化实践的连续性与普遍性；此外同期 iOS 安全社区整体偏好开源工具建设的风气亦可能独立驱动该行为，而非个人特有能力。与 open_questions 末条幸存者偏差声明呼应。

证据：azad-works-001, azad-works-002, azad-works-003, azad-works-004, azad-works-005, ba-comm-03, ba-comm-04, ba-tl-13, ba-tl-14, ba-tl-15, azad-r3-ev-002

### 系统化攻击面枚举与逆向方法论固化

起点：2017 年已具备单点漏洞利用与基础工具化能力，但攻击面覆盖以单条提权链为主，逆向方法尚未沉淀为可复用工具；iOS 内核缓存去符号化与 tagged pointer 机制构成研究前置障碍。

练习与反馈：2018 年起对 XNU 子系统与用户态服务逐项审计（ctl_ctloutput 信息泄露、XPC 字符串反序列化、launchd Mach 端口替换、GSSCred 竞态条件、task_threads 平台二进制限制），并为每类攻击面配套独立 writeup 与工具；同时把 IDA Pro C++ 类重建、tagged pointer 分析等逆向方法论本身固化为 ida_kernelcache 工具，随 iOS 12 kernelcache 结构变化快速更新基础设施。；XPC 字符串越读研究中将自创原语与已知 Heartbleed 漏洞类比以建立心智模型；task_threads 绕过研究中直接复用 Ian Beer triple_fetch 已验证的轮询策略与 fileports 技法，引用 newosxbook.com 等社区知识源，体现用既有公共知识框架定位新问题、从社区资源获取技巧并回馈开源工具的闭环。

能力与结果：形成内核与用户态并行的攻击面覆盖能力，以及『逆向方法论→工具→漏洞研究』的前置循环：先用 ida_kernelcache 重建类布局，再在已结构化的内核缓存上定位具体函数缺陷，研究粒度由单一提权链细化为针对具体函数的缺陷定位。；2018 年内同时覆盖内核信息泄露、内核调用原语、用户态提权、竞态条件多个类别，能力面在该阶段较为完整；ida_kernelcache 支撑后续 iOS 12 tagged pointers 分析，随 Apple 平台演进持续更新逆向基础设施；task_threads 绕过配套发布 threadexec 通用库，以代码库固化利用技术供后续研究复用

置信度：medium；替代解释：该阶段密集输出可能部分由 Apple 平台 2017–2018 年攻击面变化（iOS 11/12 内核缓存结构、tagged pointer 引入）这一外部条件驱动，而非纯个人方法论的主动演进；逆向方法论工具化的 distinctive 程度较高，但 generative 证据集中于 2018 单一年度，跨时期重复性弱于机制一。

证据：azad-works-004, azad-works-005, ba-tl-04, ba-tl-05, ba-tl-07, ba-tl-08, ba-tl-09, ba-tl-10, ba-tl-11, ba-comm-02, ba-comm-05

### 边界条件审查与利用可靠性度量

起点：2016 年起点阶段已对利用可靠性做量化度量（3000 次执行崩溃 2 次统计），显示其早期即建立可重复评估习惯；2017 年 physmem 研究中主动对比他人工作并审查边界条件。

练习与反馈：在 physmem 研究中对比 Matthieu Suiche BlackHat 物理内存论文与 tpwn 提权方法，指出 tpwn『only changes the process count by one』在共享 ucred（如 tmux 下）会 panic，改用 kauth_cred_setsvuid_gid 并管理引用计数；该边界条件审查为机制内真正独占的实例。需说明：量化度量（azad-works-001 的 2016 年 3000/2 崩溃统计）为单点示例性观察，2017 年后未见同类公开统计，不构成跨时期 repeated；同伴技法借取再实现（ba-comm-01/02/05）归机制二专用，不作为本机制 repeated 支撑。；通过对比他人方法的边界条件失败模式（tpwn 在共享 ucred 下 panic）校准自身实现的可靠性，体现借鉴他人方法时注重边界条件与可靠性的内部反馈。

能力与结果：形成对引用计数、共享凭证等边界条件的审查能力，并在借鉴他人方法时主动规避其在特定上下文下的崩溃路径。；physmem 改用 kauth_cred_setsvuid_gid 并管理引用计数，规避 tpwn 在共享 ucred 下的 panic；2016 年 CVE-2016-1828 以 3000 次执行崩溃 2 次量化可靠性（单点示例，2017 年后未见同类公开统计）

置信度：low；替代解释：该机制的 repeated 标签不成立：边界条件审查的独立实例仅有 physmem 对比 tpwn 一处（azad-works-002），量化度量仅有 2016 年单点（azad-works-001），均不足以支撑跨时期重复判定；因此 validation_tests 仅保留 distinctive，confidence 降为 low。其可靠性重视也可能由 iOS 利用对稳定性的客观要求这一外部条件驱动，而非个人特有习惯。

证据：azad-works-001, azad-works-002

## 可迁移与不可迁移

- 可迁移：为每一类研究方向配套发布独立可复用工具，并以开源许可向社区发布，使工具被反复使用与反馈构成研究—社区双向通道
- 可迁移：将逆向方法论本身（kernelcache C++ 类重建、tagged pointer 分析）固化为工具，以前置工具化降低后续漏洞研究的门槛
- 可迁移：借鉴他人方法时主动审查其边界条件与失败模式（如 tpwn 在共享 ucred 下 panic），并据此调整自身实现的可靠性
- 可迁移：将同伴（如 Ian Beer）的并行进展作为自身研究方向可行性的反馈信号，把社区已有技法作为基础进行再实现
- 可迁移：随目标平台版本演进（iOS 11→12→13、macOS 10.10→10.12）持续更新逆向与调试基础设施，对新内核缓存结构作出快速响应
- 不可直接迁移：Google Project Zero 的机构平台与团队研究博客披露渠道（BAZAD-DEC-05 署名『Posted by Brandon Azad, Project Zero』、ktrw 托管于 googleprojectzero 组织），个人研究者难以直接复现该披露与协作产出
- 不可直接迁移：向 Apple 直接报告漏洞的内部披露渠道及其与团队公开 writeup 的协同（2018-12-06 报告、2019-01-29 voucher_swap 公开、2019-08-29 Ian Beer 印证），受 Apple 漏洞披露政策与 Project Zero 流程约束
- 不可直接迁移：一手内核缓存逆向工具链（ida_kernelcache、ktrw）的构建依赖 IDA Pro、LLDB 及对 XNU/A11 硬件调试接口的掌握，具备较高工具与知识门槛
- 不可直接迁移：2016–2018 年 Apple 平台攻击面与内核缓存结构的时间窗口（去符号化、tagged pointer 引入、iOS 11/12 演进），该外部条件不可在其他时期复制

## 复核问题

- mechanisms[2].repeated_practice 原句『同伴技法借取再实现（ba-comm-01/02/05）归机制二专用，不作为本机制 repeated 支撑』与实际 evidence_ids 列表不符：ba-comm-01 不在 mechanisms[1].evidence_ids（该机制仅引用 ba-comm-02、ba-comm-05），ba-comm-01 仅出现在 stages[1].evidence_ids，未被任何 mechanism 引用。改写方向：将该句改为『ba-comm-02、ba-comm-05 归 mechanisms[1] 同伴技法借取专用，不作为本机制 repeated 支撑；ba-comm-01 仅用于 stages[1] 的社区致谢叙事，不进入任何 mechanism 的支撑证据』，使 meta-note 内的归属与各机制实际 evidence_ids 列表一致。该问题不影响『mechanisms[2] repeated 仅由 azad-works-002 单例支撑、validation_tests 调整为 [distinctive]、confidence 降为 low』的结论本身。
- stages[1].capability_change 内嵌编辑性注记『（注：ba-tl-02、ba-comm-04 所载 physmem 发布日期 2016-01-16 系证据层笔误，依据 azad-works-002 与 azad-r3-ev-001 一手再核验，真实 permalink 为 /2017/01/physmem-accessing-physical-memory-os-x/、日期 2017-01-16。）』将证据层纠错过程混入能力描述，且与 tensions[1] 重复。改写方向：从 stages[1].capability_change 删除该括号注记，将日期笔误纠正集中保留在 tensions[1]（已存在同一表述），stages[1].capability_change 仅保留『2017-01-16 发表 physmem...』的事实陈述，使能力描述字段不含证据层修订过程的自我说明。该问题为结构风格性，不构成语言规范违规或事实错误。

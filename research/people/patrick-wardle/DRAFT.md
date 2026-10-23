# 未通过独立复核

已达到最大修订次数 4；本文件是审计草稿，不得进入跨人物比较。

# Patrick Wardle：漏洞研究成长分析

- 擅长领域：macOS 漏洞与恶意代码技术
- 独立复核：revise · 76/100

## 成长阶段

- **2015-03 之前（Objective-See 创立之前；无精确起止，about.html 仅一句话陈述，无日期） · 政府机构从业背景下的能力前置阶段**：研究对象自述曾就职于 NASA 与 NSA，并自述在 NSA 的 Cryptanalysis and Exploitation Services（CES）小组以实习生身份习得密码分析与逆向能力。该机构经历先于其公开 macOS 研究输出，构成其逆向/密码分析训练的机构性起点；但一手页面未给出岗位、起止年份或地点，转换动机与具体约束缺失。同期其软件工程知识主要来自对他人软件的逆向工程，而非系统化工程训练，形成以逆向作为学习入口的方法取向。（置信度：medium）
  - 证据：pw-deepconvo-01, pw-deepconvo-03, pw-tl-01, pw-dec-09, patrick-wardle-ext-001
- **2015-03 至 2016 年初 · 独立研究启动与工具—研究—披露并行模式确立**：2015-03-19 创立 Objective-See 网站并同日发布 Dylib Hijack Scanner，把自用的 macOS 安全工具转为免费公开输出；同日命名 dylib hijacking 这一 OS X 攻击类，确立攻击面命名与检测工具配对发布的早期工作模式。2015-07-01 与 Emil Kvarnhammar 共享 CVE-2015-3673（RootPipe 补丁绕过），按负责任披露流程先报告 Apple、待 10.10.4 修补后再公开，并在 DefCon 23 与 BlackHat Las Vegas 发表，形成漏洞分析、会议演讲与工具发布并行输出。2015-08-29「Reversing to Engineer: Learning to Secure XPC from a Patch」记录以补丁逆向学习 XPC 机制的方法。2016-02-26 自述头衔 Director of R&D at Synack，显示其职业雇佣与独立工具/研究双线并行的工作结构。（置信度：high）
  - 证据：pw-tl-02, pw-tl-03, pw-tl-04, pw-tl-05, pw-dec-01, pw-dec-02, pw-dec-03, pw-works-001, pw-works-002
- **2016-11 至 2019-09 · 系统防护机制研究与平台安全边界收紧驱动的架构迁移**：研究对象从单点漏洞扩展到 Apple 新引入的系统防护机制，2016-12-01 起记录 SIP 绕过、2017-09-05 记录 High Sierra SKEL 实现缺陷并采取公开证明机制失败但暂缓技术细节的立场型披露。2015-11-15 起以连载记录 BlockBlock 内核扩展开发，覆盖 MAC policy、KAuth 子系统与内核到用户态广播；在 SIP 使 dtrace 进程监控失效后，将监控路径从用户态 dtrace 改为内核态，先评估 MAC policy 再转向 KAuth。2018-01-12 自述对样本线索依赖同伴传递（a good friend brought it to my attention），把自身定位为分析者与公开记录者。2019-09-07（blog_0x47）在 Apple 推动将第三方开发者逐出内核的背景下，将进程监控从内核扩展迁移到用户态 Endpoint Security Framework，并把分散在 RansomWhere?、TaskExplorer、BlockBlock 中的重复监控代码抽取为共用 ProcessMonitor 库；2019-08-04「Office Drama on macOS」把目标从单漏洞分析上升到对全补丁 macOS Catalina 的多阶段利用链。（置信度：high）
  - 证据：pw-works-003, pw-works-005, pw-works-006, pw-works-008, pw-dec-04, pw-dec-05, pw-dec-06, pw-deepconvo-06, r2-001, r2-002, r1-002
- **2017-01 至 2026-01（年度报告系列，覆盖 2016–2025 年度） · 年度恶意代码回顾作为可核验的重复练习节奏**：首份年度报告「Mac Malware of 2016」发布于 2017-01-01，「Mac Malware of 2017」发布于 2017-12-23，其后「The Mac Malware of 2018」至「The Mac Malware of 2025」分别于 2019-01-01 至 2026-01-01 发布，整体遵循次年 01 月初发布覆盖上一年度的惯例，序列连续至 2026-01-01。该年度综合报告含样本与 IoCs，把分散的样本分析归档为可比对的时间序列，构成可核验的长期重复练习与对外可见的产出节奏。原 evidence 内部对该日期序列存在冲突（pw-works-004 date=2016-01-01 与 works 维度 contradictions「2016-12-23」均已作废，已以 r1-001 核验日期为准）。（置信度：high）
  - 证据：r1-001, pw-tl-06, pw-dec-07
- **2021-02 至 2026-09 · 修复后再发现与防御配套、反向防护与社区组织化**：研究对象在 Apple 主动修复攻击面后进行重建。2021-02-14「Arm'd & Dangerous」记录首个针对 Apple Silicon（M1/arm64）原生编译的恶意程序，平台架构迁移（x86_64→arm64）后研究随之迁移。2024-12-16 与 2025-11-24 发布「Restoring Reflective Code Loading on macOS」第一、二部分，记录 Apple 移除反射式代码加载 API 后重建该攻击面，并在第二部分加入 macOS 26 的内存内 Obj-C 载荷与检测覆盖，研究从发现延伸到修复后再发现并配套检测。2025-03-27 两篇 TCC 分析文章（r3-001「TCCing is Believing」记录 macOS 15.4 新增 Endpoint Security 对 TCC 事件的支持；r3-002「[0day] From Spotlight to Apple Intelligence」记录 Spotlight 插件读取 TCC 保护文件并经 Darwin 通知逐字节外传的 TCC 绕过）分别覆盖检测与绕过方向。2026-02-15「ClickFix: Stopped at ⌘+V」提出在粘贴时拦截 ClickFix 的执行边界防御，2026-03-31「No Paste for You!」反向 macOS 26.4 的 ClickFix 防护以理解其实现，形成防御—反向—改进防御的闭环。同期通过 Objective by the Sea（OBTS）会议与 Objective-See Foundation 的 WeTalks、Objective for the We、Objective-We、Steve 等项目把社区参与制度化。注：[0day] 前缀博文子序列最早出现于 2016-12-01，仅反映博文标题标注习惯，本阶段出现的 [0day] 标注不构成研究方向实质转变的独立证据。（置信度：medium）
  - 证据：pw-works-009, pw-works-011, pw-works-012, pw-dec-08, pw-tl-10, r3-001, r3-002

## 主要成长机制

### 以逆向他人软件作为学习入口

起点：研究对象自述其软件工程知识主要来自对他人软件的逆向工程，而非系统化工程训练；在操作系统二进制中寻找漏洞的过程使其得以观察真实开发者的思考与编码方式。自述密码分析与逆向能力在 NSA 的 Cryptanalysis and Exploitation Services（CES）小组以实习生身份习得。

练习与反馈：把漏洞狩猎同时当作学习真实软件构造的过程：在分析 macOS 恶意软件与 Apple 系统机制时，系统性地反向二进制以理解其实现，并把逆向结果公开为方法示范（如 2015-08-29「Reversing to Engineer: Learning to Secure XPC from a Patch」）。对未被触发的恶意软件方法（如 takeScreenshotAt、mouseClick、runAppleScript）采取继续深挖（I'll keep digging!）的取向，而非止步于部分结果。；反馈由研究对象自身驱动，而非来自社区外部输入；反馈来源为被研究对象本身（Apple 补丁回归、意外崩溃、未触发的恶意软件方法）。在改进 RansomWhere? 时从用户态触发了内核 panic，把一次意外崩溃转化为研究线索（Two Bugs, One Func 系列）。

能力与结果：形成补丁逆向—学习新机制的复盘路径：对 Apple 补丁反向推导修复思路并迁移为自身技术方法，对补丁回归保持持续复核并把每一步作为独立公开记录。同时依赖社区同行工具生态（如 Jonathan Levin 的 jtool 工具）构建自身分析流程，而非正式师徒关系。；2015-08-29「Reversing to Engineer: Learning to Secure XPC from a Patch」记录通过反向 Apple 的 RootPipe 补丁学习 XPC 客户端校验与 SecTask 用法；2016-03-27 至 2016-04-24「Two Bugs, One Func()」三篇记录触发→根因→补丁→补丁回归引入新缺陷（内核信息泄漏、审计子系统堆溢出）的链条；2018-01-12 MaMi 分析中使用 jtool 转储 Objective-C 类与方法

置信度：medium；替代解释：逆向既可作为学习路径，也可能仅是 macOS 闭源生态下分析工作的必要手段而非主动学习能力构建；本机制把逆向表述为学习入口部分依赖研究对象 2016 年自述，缺乏对其能力如何因逆向而可观察增长的独立第三方校验。

证据：pw-deepconvo-01, pw-deepconvo-03, pw-deepconvo-04, pw-deepconvo-05, pw-deepconvo-07, pw-works-002, pw-works-005

### 攻击面命名与检测工具同步发布

起点：2015-03-19 创立 Objective-See 并同日发布首个工具 Dylib Hijack Scanner，把自用的 macOS 安全工具转为免费公开输出；研究对象自述最初动机较自私，写 OS X 安全工具来加固自己的 Mac，后因分享理念转为面向社区。

练习与反馈：以新攻击类命名 + 同步发布检测工具的方式确立研究方法与输出节奏：2015-03-19 定义并命名 dylib hijacking 这一 OS X 攻击类，同日发布 Dylib Hijack Scanner。研究产出（新攻击面/新绕过）与防御工具（检测器/监控器）配对发布，并把分析文章作为连接两者的公开记录。；社区读者反馈直接驱动技术路线调整：在 SIP 限制使 DTrace 无法用于进程创建监控后，读者（含 @osxreverser 等）建议改用 KAuth 子系统，研究对象据此在后续篇目中采用 KAuth 方案。CVE 协调（与原作者 Emil Kvarnhammar 共享 CVE-2015-3673 等）与客座发文构成与厂商及研究社区的双向反馈循环。

能力与结果：形成攻击面命名—分析文章—检测工具发布—社区反馈回路的闭环工作模式，研究、写作与公开演讲循环衔接。GitHub 组织页显示 Pull Shark（社区 PR 合并）与 Starstruck x4（多仓库超 1k stars）成就，工具迭代与外部输入直接耦合。；2015-03-19 dylib hijacking 攻击类命名与 Dylib Hijack Scanner 同步发布；2015-11-15 至 2015-12-13「Monitoring Process Creation via the Kernel」三篇记录 BlockBlock 内核扩展开发与 MAC policy/KAuth 架构权衡；2026-02-15「ClickFix: Stopped at ⌘+V」执行边界防御工具与 2026-03-31「No Paste for You!」反向防护分析文章配套

置信度：medium；替代解释：攻击面与工具配对发布也可能是 macOS 小众生态下提升研究可见度的策略性输出，而非普遍能力增长机制；社区反馈回路的实际作用（如 KAuth 建议）部分基于目录摘要推断为 inferred，正文未单独抓取核验。

证据：pw-works-001, pw-works-003, pw-works-012, pw-dec-01, pw-dec-02, pw-dec-03, pw-dec-04, PW-COMM-01, PW-COMM-02, PW-COMM-03, PW-COMM-04

### 平台安全边界收紧驱动工具底层架构迁移

起点：研究对象于 2015-11 起以连载记录 BlockBlock 内核扩展开发，采用 MAC policy 与 KAuth 子系统实现进程创建监控。Apple 引入 SIP（OS X 10.11 El Capitan）使 dtrace 式进程创建监控失效，研究对象将监控路径从用户态 dtrace 改为内核态。

练习与反馈：面对 Apple 收紧平台安全边界，迁移工具底层架构而非放弃：第一次在 SIP 后从 dtrace 迁至内核扩展（MAC policy/KAuth）；第二次在 Apple 推动将第三方开发者逐出内核、弃用 kext/OpenBSM 路径后，于 2019-09-07（blog_0x47）将进程监控从内核扩展迁移到用户态 Endpoint Security Framework，并把分散在 RansomWhere?、TaskExplorer、BlockBlock 中的重复监控代码抽取为共用 ProcessMonitor 库。；反馈由平台安全机制演进驱动：研究对象以 Apple 改变平台安全边界为信号重新选择监控原语，并据此调整工具架构。2019-09-16/17 发布针对 macOS 10.15 Catalina 的 Process/File Monitor 帖文，体现迁移成果的对外发布节奏。

能力与结果：研究对象将各工具各自实现的进程监控代码抽取为共用 ProcessMonitor 库，以适应 Apple 推动第三方开发者退出内核后的工程要求；工具建设由各工具各自实现的监控代码改为共用库抽取，体现对平台机制演进的跟踪与工程化复用能力。；2015-11-15 起「Monitoring Process Creation via the Kernel」三篇记录从 dtrace 迁至内核扩展的 MAC policy/KAuth 架构权衡；2019-09-07 blog_0x47.html 记录 kext 弃用背景下将进程监控迁至 Endpoint Security Framework 并抽取共用 ProcessMonitor 库；2019-09-16/17 发布针对 macOS 10.15 Catalina 的 Process/File Monitor 帖文（不存在 2018-09 首发；pw-works-007 已作废，以 r2-001/r2-002 为准）

置信度：high；替代解释：架构迁移也可视为 Apple 强制弃用 kext 后的被动适配，而非研究对象主动的能力增长；但两次独立时点（SIP 后迁内核、kext 弃用后迁 ES）的重复性支持其为可复用的跟踪—迁移机制。

证据：pw-works-003, pw-dec-04, pw-dec-06, r2-001, r2-002

### 补丁回归与异常追问驱动深挖

起点：研究对象在 2016-03-27 至 2016-04-24「Two Bugs, One Func()」系列中观察到 Apple 修复一个内核 panic 后引入新的内核信息泄漏（UNIX 套接字）与审计子系统的可利用堆溢出，形成对补丁回归保持持续复核的工作取向。

练习与反馈：对补丁回归与未解现象采取追问式深挖：把意外崩溃（RansomWhere? 改进时从用户态触发内核 panic）视为可深挖的研究线索，对未被触发的恶意软件方法表示继续深挖其原因，对 Apple 修复的攻击面（反射式代码加载）在移除后进行重建并配套检测。；反馈由研究对象自身驱动，而非来自社区外部输入；反馈来源为被研究对象本身：Apple 补丁回归引入新缺陷、意外崩溃、未触发的恶意软件方法、Apple 移除 API 后的攻击面变化。

能力与结果：形成触发→根因→补丁→补丁回归引入新缺陷的复核链条，并对未解现象保持追问式坚持；把单点漏洞分析扩展到端到端利用链（Office Drama on macOS），对 Apple 主动修复的攻击面进行重建并配套检测方法。；2016「Two Bugs, One Func()」三篇记录 Apple 修复内核 panic 后引入新内核信息泄漏与审计子系统堆溢出的补丁回归链条；2019-08-04「Office Drama on macOS」把目标从单漏洞分析上升到对全补丁 macOS Catalina 的多阶段利用链；2024-12-16 与 2025-11-24「Restoring Reflective Code Loading on macOS」两篇记录 Apple 移除反射式代码加载 API 后重建该攻击面并配套检测；2025-03-27 r3-002「[0day] From Spotlight to Apple Intelligence」记录 Spotlight 插件读取 TCC 保护文件并经 Darwin 通知逐字节外传的 TCC 绕过

置信度：medium；替代解释：补丁回归深挖也可能是 macOS 闭源生态下补丁反向分析的副产物，而非独立的追问能力；但跨 2016、2019、2024 多个时点的重复性与生成性（从补丁回归扩展到利用链与攻击面重建）支持其为可复用机制。

证据：pw-works-005, pw-works-008, pw-works-011, pw-deepconvo-05, pw-deepconvo-07, r3-002

### 公开发表与社区组织化的稳定输出节奏

起点：研究对象以稳定、可预期的公开输出节奏作为能力积累与社区反馈回路的入口：2015-03-19 创立 Objective-See 并同日发布首个工具，自 2017-01-01 起每年 01 月初发布上一年度的 Mac Malware 年度回顾报告，至 2026-01-01 连续至 The Mac Malware of 2025。同时把日常样本分析素材复用为演讲材料（如为 SyScan360 寻找键盘记录器作为幻灯片示例）。

练习与反馈：把研究、写作与公开演讲循环衔接：把分析样本整合进会议演讲材料，把年度恶意代码分析归档为可比对的时间序列，把 CVE 协调与客座发文作为同伴网络与同行互认的直接证据。通过客座作者机制（Amit Serper、Csaba Fitzl、Jaron Bradley、@CodeColorist 等）使自有平台成为同行展示与互检的场所。；社区以 issue/PR/赞助形式参与工具建设（GitHub 组织页显示 29 个仓库、LuLu 13.2k stars、Pull Shark、Starstruck x4）；CVE 协调（CVE-2015-3673、CVE-2017-7170、CVE-2019-8513/8530/8521/8565、CVE-2020-9934/9854、CVE-2021-30853/30860 等）构成与 Apple 与同行的双向反馈循环。

能力与结果：从个人输出升级为组织化社区平台：通过 OBTS 会议与 Objective-See Foundation 的 WeTalks、Objective for the We、Objective-We、Steve 等项目把社区参与制度化、组织化，使命为 create free tools, grow and support a global community of students, researchers, and defenders, and advance Apple security。；自 2017-01-01 至 2026-01-01 连续发布 Mac Malware 年度回顾报告（次年 01 月初发布惯例）；2018-02-17 自述把键盘记录器样本复用为 SyScan360 演讲幻灯片示例；2018 年起通过 Objective by the Sea（OBTS）会议与 Foundation 项目把社区参与制度化

置信度：medium；替代解释：稳定输出节奏部分可由研究对象作为 Objective-See 全职/主导者的资源条件解释，而非普遍可迁移的纪律性；OBTS 会议规模与议程缺一手正文，其作为社区枢纽的实际作用部分基于 about 页与博客目录间接证实。

证据：pw-deepconvo-08, pw-tl-06, pw-tl-08, pw-dec-07, pw-dec-08, PW-COMM-01, PW-COMM-03, PW-COMM-04, PW-COMM-05, r1-001

## 可迁移与不可迁移

- 可迁移：以补丁逆向作为学习新系统机制的路径：反向厂商补丁以推导修复思路并迁移为自身技术方法，对补丁回归保持持续复核并把每一步作为独立公开记录。
- 可迁移：攻击面命名与检测工具配对发布：在命名新攻击类或新绕过的同时发布检测工具，使研究产出（攻击面）与防御产出（检测器）配对，并以分析文章作为连接两者的公开记录。
- 可迁移：以年度重复性综合报告建立长期训练节奏：把分散分析归档为可比对的时间序列（如年度恶意代码回顾），构成可核验的持续产出节奏。
- 可迁移：以异常现象与未解问题驱动深挖而非止步于部分结果：把意外崩溃、未触发方法、补丁回归视为研究线索而非挫折，对不完整结论保持追问。
- 可迁移：工具建设由各工具各自实现改为共用库抽取：在平台机制变化或重复代码积累时，把分散实现抽取为共用库以适应工程化复用要求。
- 不可直接迁移：macOS 闭源生态与研究对象长期积累的二进制逆向经验：本机制部分依赖 macOS 闭源生态下二进制逆向为必要分析手段这一特定条件，对开源或源码可得的平台不完全适用。
- 不可直接迁移：研究对象作为 Objective-See 全职/主导者与 Foundation 创办人的资源条件：稳定的公开输出节奏与社区组织化（OBTS 会议、Foundation 项目）依赖研究对象可投入的时间、资金与社区号召力，对资源条件不足的研究员不可直接迁移。
- 不可直接迁移：立场型披露的实际效果依赖研究员知名度与社区影响力：公开证明机制失败以施加压力的效果依赖研究员知名度与社区影响力，对知名度不足的研究员不可迁移；该依赖条件无直接证据支撑，相关结论应作为 inferred。
- 不可直接迁移：NASA/NSA 机构训练背景：研究对象自述的密码分析与逆向能力在 NSA CES 小组以实习生身份习得，该机构性训练起点对未经历类似机构训练的研究员不可复制。
- 不可直接迁移：研究对象在 macOS 安全社区的中心节点位置：客座作者机制、CVE 共享、同行工具借用（如 jtool）等社区反馈回路依赖研究对象在 macOS 安全社区的中心节点位置，对未处于类似位置的研究员不可直接迁移。

## 复核问题

- stages[2]（阶段3）evidence_ids 仍包含 pw-works-005（Two Bugs, One Func，date=2016-03-27/04-24），但阶段3 capability_change 正文未论及补丁回归引入新缺陷的内容，且 pw-works-005 已在 mechanisms[3]（机制4）starting_conditions 与 observed_outcomes 第一项被正确引用；此条为 round-3 复核 required_revision 第2条明确要求「从 stages[2].evidence_ids 移除 pw-works-005，或在 stages[2].capability_change 正文补出论点」，当前两者均未执行，前轮已通过的修正未落实。
- stages[2]（阶段3）period 标为「2016-11 至 2019-09」，但 evidence_ids 包含 pw-works-003（2015-11-15）与 pw-dec-04（2015-11-15），其发布日期不在该 period 区间内；阶段3 capability_change 正文以「2015-11-15 起以连载记录 BlockBlock 内核扩展开发」作为架构迁移主题的起点叙述，但 period 起点晚于该日期，时间线与证据映射不一致。
- 字段 stages[2].evidence_ids：移除 pw-works-005（Two Bugs, One Func，date=2016-03-27/04-24）。该证据已在 mechanisms[3]（机制4「补丁回归与异常追问驱动深挖」）starting_conditions 与 observed_outcomes 第一项被正确引用且有正文支撑，阶段3 不应重复引用；阶段3 capability_change 正文未论及补丁回归内容亦不应保留该 evidence_id。原措辞「pw-works-005」保留在 evidence_ids 列表中，改写方向为直接删除该项。此为 round-3 复核 required_revision 第2条明确要求的修正，当前未落实。
- 字段 stages[2].period 与阶段3 evidence_ids 日期映射：stages[2].period 标为「2016-11 至 2019-09」，但 evidence_ids 包含 pw-works-003（2015-11-15）与 pw-dec-04（2015-11-15），其发布日期不在 period 内；阶段3 capability_change 正文以「2015-11-15 起以连载记录 BlockBlock 内核扩展开发」作为架构迁移主题起点。改写方向：将 period 起点调整为「2015-11 至 2019-09」以覆盖 BlockBlock 内核扩展开发连载与 SIP 后迁内核扩展的起点时点，或将 pw-works-003/pw-dec-04 迁移至对应阶段并在正文补出论点，使每条 evidence_id 的发布日期落在其所属阶段 period 区间内。
- 字段 r1-002 的 evidence_id 映射：r1-002（[0day] 前缀子序列，2016-12-01）当前列入 stages[2]（阶段3）evidence_ids，但阶段3 capability_change 正文未论及 [0day] 前缀子序列内容；stages[4]（阶段5）capability_change 正文末尾「注：[0day] 前缀博文子序列最早出现于 2016-12-01」论及 r1-002 内容，但 stages[4].evidence_ids 未列入 r1-002。改写方向：将 r1-002 从 stages[2].evidence_ids 移至 stages[4].evidence_ids，使 evidence_id 与正文论点一一对应。
- 字段 tensions[2] 笔误：「立场所型披露以公开证明机制失败施加压力」中「立场所型披露」为笔误，多一个「所」字。改写方向：删去「所」字，改为「立场型披露以公开证明机制失败施加压力」。

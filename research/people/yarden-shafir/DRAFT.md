# 未通过独立复核

已达到最大修订次数 4；本文件是审计草稿，不得进入跨人物比较。

# Yarden Shafir：漏洞研究成长分析

- 擅长领域：Windows 内核漏洞
- 独立复核：revise · 82/100

## 成长阶段

- **约 2010—2018（据 2019 年加入 Winsider 时点反推的推断区间，非任职起止年份证据） · 进入 Windows 安全研究与多机构经验积累**：在加入 Winsider 之前，Yarden Shafir 据其团队简介约具有 10 年网络安全行业经验，曾任职于 Trail of Bits、CrowdStrike（均为高级安全工程师）与 SentinelOne（安全研究员与 QA 工程师）。三家前雇主以并列方式呈现，页面不含顺序词与起止年份，任职先后顺序无证据支撑；仅角色递进（SentinelOne 为研究员/QA 工程师、CrowdStrike 为高级安全工程师）可作 SentinelOne 较早的弱推断。此阶段为后续研究-训练双轨积累 Windows 内部原理与逆向经验的时期，但其入行起点、自学路径与导师关系无一手证据。（置信度：low）
  - 证据：ys-conv-01, ys-conv-02, ys-decisions-01, ys-decisions-02, ys-timeline-01, ys-timeline-02, ys-timeline-03, ys-r4-001
- **2019 · 以联合合伙人身份加入 Winsider，进入研究-训练双轨**：2019 年 Yarden Shafir 以 co-partner 身份加入 Winsider（Alex Ionescu 于 2009 年创立，作为 David Solomon Expert Seminars 的延续），成为联合合伙人与讲师。这是一次由雇员研究岗向合伙人/训练提供方的转型：在既有专业积累前提下，与领域内既有专家共建训练与咨询实体，把个人研究能力转化为可规模化交付的训练与白皮书产出。该转型构成长期同伴协作与公开输出的组织基础。（置信度：high）
  - 证据：ys-community-01, ys-conv-01, ys-decisions-01, ys-timeline-17, ys-r1-001
- **2020 · 工具建设与漏洞 PoC 公开化**：2020 年前后，Yarden Shafir 公开发布 CVE-2020-1034 提权 PoC，并在 GitHub 公开维护 WinDbg_Scripts、PoolViewer、SymlinkCallback 等用于内核池分析、调试与文件系统访问追踪的工具。将漏洞研究与可复用工具建设绑定，形成不止于 writeup、同步产出供他人复现与分析的调试脚本与样本的方法论选择。PoolViewer（内核池查看）与 WinDbg_Scripts（调试器数据模型脚本）指向对 Windows 内核池与调试流程的长期投入。（置信度：high）
  - 证据：ys-decisions-03, ys-community-04, ys-timeline-05, ys-timeline-16, ys-works-004
- **2022—2023 · data-only 利用原语与缓解机制分析序列**：2022-07-05 在 windows-internals.com 发表 I/O Ring writeup（ys-works-001），通过逆向 Windows 11 22H2 的 I/O Ring 子系统并利用 ntoskrnl.exe 公共符号，将一次任意内核写（或任意递增）升级为完整内核读写 primitive，采用 data-only 攻击路径。作者自述该研究曾于 TyphoonCon 2022 演讲（ys-works-005）；TyphoonCon 2022 会议议程一手确认演讲日为 2022-06-23/24（ys-r2-005），早于 writeup 博客发表日 2022-07-05，相对时序为演讲→博客。此后进入缓解机制分析序列：Module Tampering Protection（2022-08-16，ys-r3-001）、KASLR Bypasses（2022-11-23，ys-works-002）、Filter Communication Ports（2023-01-04，ys-r3-003）、KASLR Leaks Restriction（2023-11-26，ys-r3-002）。I/O Ring、PoC 仓库与会议演讲以多渠道公开发表，各渠道存在性由 ys-works-001、ys-works-005、ys-r2-005、ys-community-02 支撑；演讲→博客相对时序由 ys-r2-005 一手确立，PoC 仓库相对两者的时序未由一手证据确立。（置信度：medium）
  - 证据：ys-works-001, ys-works-002, ys-works-005, ys-community-02, ys-r2-005, ys-r2-006, ys-r3-001, ys-r3-002, ys-r3-003
- **2024—2026 · Secure Kernel 研究与主题演化**：2024-05-02 发表《Secure Kernel Research with LiveCloudKd》（ys-r2-001），说明使用 LiveCloudKd 对 Hyper-V 虚拟机的 secure kernel（VTL1）挂载活动内核调试器，并以 securekernel!SkLoadedModuleList 枚举 VTL1 加载模块，扩展至 VBS/Secure-Kernel 研究工具。2026-04-23 发表《Goodbye Secure Pool, Hello KDP Pool》（ys-r2-002），分析 Windows 11 VBS 26H2 新增 KDP Pool（KDPRO 节、secure kernel 调用、hypervisor SLAT 只读，当前仅限 ntoskrnl.exe 内部）。2026-07-09 发表《Random Windows Things Part 1: PreviousMode Mitigation》（ys-r2-003），2026-07-27 发表《Random Windows Things Part 2: Unexpected Clipboard Data Behavior》（ys-r2-004），延续 Random Windows Things Part 1/Part 2 的系列化分篇发表习惯（与 CVE-2020-1034 分 Part 1/1.5/2 发表的格式一致）。此阶段研究主题由利用原语与缓解分析扩展到 secure kernel 调试工具建设与安全关键数据保护机制，显示技术栈从攻击利用向防御性内核研究的系统演化。（置信度：medium）
  - 证据：ys-works-003, ys-community-03, ys-r2-001, ys-r2-002, ys-r2-003, ys-r2-004

## 主要成长机制

### 研究副产品工具化与公开输出回路

起点：具备 Windows 内核池与调试流程的逆向经验，以及 GitHub 公开账号；研究产出不止于 writeup 而同步产出供他人复现与分析的工具。

练习与反馈：将漏洞研究与可复用工具建设绑定：CVE-2020-1034 提权 PoC、PoolViewer（从内存 dump 查看/过滤 pool 分配，附 WinDbg 扩展）、WinDbg_Scripts、SymlinkCallback 与 PoolViewer 工具建设采用相同的逆向加数据模型实证路径，并把调试脚本、PoC、利用框架系统化整理并公开发布到 GitHub。；GitHub 工具获得数百星（WinDbg_Scripts 约 435 星、IoRingReadWritePrimitive 约 259 星、PoolViewer 约 156 星等），星标支撑工具被采用度与可见度，但不直接证实复用事实，也不支撑对研究者个人声誉的独立评价。Winsider 官网三条课程评价未归因到具体讲师，读者反馈区与 issue/PR 历史不可见，反馈回路属推断而非已证实。

能力与结果：形成研究—工具—公开发表相互支撑的工作模式，工具作为可复用资产支撑后续内核结构研究，研究输出反向界定工具需求；工具在 GitHub 获数百星，支撑采用度与可见度，但不直接证实复用事实。；PoolViewer、WinDbg_Scripts、CVE-2020-1034 PoC 等工具在 GitHub 公开并被广泛采用（数百星）；PoolViewer 与 LiveCloudKd 共同构成内核结构分析与 secure kernel 调试的工具建设脉络；持续 4 年以上的稳定深度发表节奏（2022-07 至 2026-07 至少 10 篇深度 writeup）

置信度：medium；替代解释：工具建设与公开输出回路的高信心标注受三重混淆变量限制：(1) Winsider 培训/咨询商业模式——配套 PoC 与工具或为业务交付要求而非纯研究习惯；(2) 自发布/平台偏差——主要来源为本人联合维护的 windows-internals.com 与自维护 GitHub，缺乏独立第三方平台交叉证实；(3) 幸存者偏差——仅基于可观察的公开成功产出，无失败、转向或负面反馈证据。研究-工具相互支撑亦可由单一研究者长期深耕同一子领域解释，不必然依赖反馈回路。

证据：ys-works-001, ys-works-002, ys-works-003, ys-works-004, ys-community-02, ys-community-03, ys-community-04, ys-timeline-16, ys-r2-001, ys-r2-002, ys-r2-003

### 逆向 ntoskrnl 与 WinDbg 数据模型实证

起点：具备 ntoskrnl.exe 公共符号的使用能力与 WinDbg 内核调试环境，以及对 Windows 内核结构的既有理解。

练习与反馈：对 Windows 11 22H2 的 I/O Ring 子系统、ETW THREATINT_PROCESS_SYSCALL_USAGE、filter communication ports、KDP Pool、PreviousMode 路径等进行逆向，结合 WinDbg dx 命令检查 EPROCESS.SyscallUsage 等字段并以内核调试识别已连接进程。；I/O Ring writeup 中记录了 Alex Ionescu 一次具名管道建议（改用具名管道以降低可见性），经该建议后定稿；该单次建议不构成系统性同伴评审制度。无其他可核验的同行评审或读者反馈记录。

能力与结果：形成研究—工具—公开发表相互支撑的工作模式，工具作为可复用资产支撑后续内核结构研究，研究输出反向界定工具需求；工具在 GitHub 获数百星，支撑采用度与可见度，但不直接证实复用事实。；I/O Ring writeup 将任意内核写升级为完整读写 primitive 的 data-only 路径；KASLR Bypasses writeup 以自家 I/O Ring exploit 作为对照实验基准检验 ETW 新检测机制；Filter Communication Ports writeup 以 wdfilter 为例说明 filter driver 通信端口调查方法并经 WinDbg 内核调试识别已连接进程

置信度：medium；替代解释：该机制的高信心标注受 Winsider 培训/咨询商业模式与自发布/平台偏差限制；'每篇均逆向 ntoskrnl 与 WinDbg 数据模型实证'的全称判断不成立，存在反例（见 transferable_practices）。逆向方法论本身为 Windows 内核研究领域的通用方法，其个人特有区分度低于工具建设与公开发表闭环。

证据：ys-works-001, ys-works-002, ys-works-004, ys-community-02, ys-community-04, ys-decisions-03, ys-decisions-04, ys-timeline-05, ys-timeline-16, ys-r2-001, ys-r3-003

### data-only 攻击路径的 primitive 构造

起点：在 CFG、KASLR、内核池保护等缓解机制约束下，传统内核利用路径难度上升，研究者转向 data-only 路径属可推断的环境背景（标注为推断而非可复现机制）。

练习与反馈：将单一 bug class（任意递增/任意写）的利用思路系统化为可复用 primitive：通过逆向 I/O Ring 子系统并重定向 IoRing->RegBuffers 指针，把一次任意内核写（或任意递增）升级为完整内核读写 primitive。；I/O Ring writeup 记录了 Alex Ionescu 一次具名管道建议；无其他可核验的转向或失败反馈证据。

能力与结果：以 writeup、PoC 仓库与会议演讲多渠道公开发表单一 data-only primitive；演讲→博客相对时序由 ys-r2-005 一手确立，PoC 仓库相对两者的时序未由一手证据确立。；I/O Ring data-only 读写 primitive writeup（2022-07-05）与 PoC 仓库 IoRingReadWritePrimitive；TyphoonCon 2022 演讲（2022-06-23/24）

置信度：low；替代解释：该机制仅覆盖 I/O Ring 单一 primitive 实例，缺乏跨实例证据，受幸存者偏差约束（无失败或转向证据）。data-only 攻击路径在 2020 年代前后缓解机制收紧时成为研究者的可行选项之一，属时期背景而非可复现的个人机制；其个人特有区分度低于工具建设闭环。

证据：ys-works-001, ys-works-005, ys-r2-005, ys-r2-006, ys-decisions-04

### 以自有成果为参照检验新缓解/检测机制的复盘式研究方法

起点：具备已完成的自有 exploit 成果（如 I/O Ring primitive，依赖 NtQuerySystemInformation 泄漏内核指针），可作为对照实验基准。

练习与反馈：以前序自有工作作为对照实验基准检验新检测机制的有效性：在《An End to KASLR Bypasses?》中手动启用 ETW 事件 THREATINT_PROCESS_SYSCALL_USAGE 并用 WinDbg dx 命令检查 EPROCESS.SyscallUsage 字段，以自家 I/O Ring exploit 作为对照实验。；该文在论证中区分机制能力与实际防护效果的差异（如 EDR 采纳滞后、Threat Intelligence 频道需 PPL、仅覆盖部分已知指标），未记载由该差异触发的后续改进或转向行为；写作论证特征不被重构为反馈回路。

能力与结果：以自有成果为参照检验新缓解/检测机制的复盘式研究方法，限定为基于 ys-works-002 的单实例方法样本，跨实例证据不足（当前仅 1 个 self-benchmark 实例）。；《An End to KASLR Bypasses?》（2022-11-23）以 I/O Ring exploit 为对照检验 ETW THREATINT_PROCESS_SYSCALL_USAGE 机制

置信度：low；替代解释：self-benchmark 定义特征仅由 ys-works-002 一手记载；KDP Pool（ys-r4-002）为机制间对比、未以自有 exploit 作对照，PreviousMode（ys-r4-003）作者声明本系列研究非原创并归功于 Gabriel Landau，二者均不承载 self-benchmark 特征，仅作缓解分析主题演化旁证。该机制为单实例，受幸存者偏差约束，亦受 Winsider 商业模式与自发布/平台偏差限制。

证据：ys-works-002

## 可迁移与不可迁移

- 可迁移：将漏洞研究与可复用工具建设绑定，研究不止于 writeup 而同步产出供他人复现与分析的调试脚本与样本。
- 可迁移：把单一 bug class 的利用思路系统化为可复用 primitive，并以 writeup、PoC 仓库与会议演讲多渠道公开发表。
- 可迁移：其内核 writeup 多以逆向 ntoskrnl 为基础；但'每篇均逆向 ntoskrnl 与 WinDbg 数据模型实证'不成立——Clipboard（ys-r2-004）为行为/API 分析、未记载逆向 ntoskrnl 或 WinDbg 数据模型实证，KDP Pool（ys-r4-002）与 PreviousMode（ys-r4-003）虽含逆向 ntoskrnl 但未显式记载 WinDbg dx 数据模型实证。
- 可迁移：以前序自有工作作为对照实验基准检验新检测机制的有效性（仅 ys-works-002 单实例，跨实例证据不足）。
- 可迁移：系列化分篇发表（CVE-2020-1034 Part 1/1.5/2、Random Windows Things Part 1/Part 2），延续可重复的研究呈现习惯。
- 不可直接迁移：2019 年以 co-partner 身份加入 Alex Ionescu 于 2009 年创立的 Winsider（ys-r1-001），与领域内既有专家共建训练/咨询实体的组织基础，非可复现的个人机制。
- 不可直接迁移：约 10 年网络安全行业经验与多机构任职轨迹（Trail of Bits、CrowdStrike、SentinelOne、Vigilant Labs）属个人履历条件，任职先后顺序无证据支撑。
- 不可直接迁移：2020 年代前后缓解机制收紧，data-only 攻击路径在该时期成为研究者的可行选项之一，属时期背景而非可复现机制。
- 不可直接迁移：主要来源为本人联合维护的 windows-internals.com 与自维护 GitHub，存在自发布/平台偏差；研究-训练双轨与配套 PoC 或为 Winsider 业务交付要求，存在商业模式偏差。

## 复核问题

- mechanisms[1].intermediate_capability 的文本与 mechanisms[0].intermediate_capability 逐字相同（均为『形成研究—工具—公开发表相互支撑的工作模式，工具作为可复用资产支撑后续内核结构研究，研究输出反向界定工具需求；工具在 GitHub 获数百星，支撑采用度与可见度，但不直接证实复用事实。』），但两机制名称与 repeated_practice 不同（机制[0] 为工具建设与公开输出回路，机制[1] 为逆向 ntoskrnl 与 WinDbg 数据模型实证）。机制[1] 的中间能力应描述逆向 ntoskrnl 与 WinDbg dx 实证所产生的中间产物（如可复用的字段识别、内核结构实证方法），而非复述机制[0] 的工具-研究相互支撑。该字段进入最终调查报告会使两机制的中间能力无法区分，构成结构性缺陷。
- mechanisms[1].intermediate_capability：原措辞为『形成研究—工具—公开发表相互支撑的工作模式，工具作为可复用资产支撑后续内核结构研究，研究输出反向界定工具需求；工具在 GitHub 获数百星，支撑采用度与可见度，但不直接证实复用事实。』（与 mechanisms[0].intermediate_capability 逐字重复）。改写方向：将该字段限定为机制[1] 专属的中间能力，描述逆向 ntoskrnl 与 WinDbg dx 数据模型实证所产生的中间产物，例如『通过对 ntoskrnl.exe 公共符号与 WinDbg dx 命令的反复结合，形成对 EPROCESS.SyscallUsage、filter communication ports、KDP Pool 内部结构等字段与对象的可核验实证方法，作为后续缓解机制分析与调试工具建设的中间基础』，删除与机制[0] 重复的工具-研究相互支撑表述，使两机制的中间能力可区分。
- mechanisms[2].validation_tests：原值为 ["repeated", "generative"]，与该机制 confidence=low、单实例、alternative_explanation 自述『缺乏跨实例证据』相矛盾。改写方向：删除『generative』，仅保留 ["repeated"]，或显式标注『generative 仅就 I/O Ring 单实例的 primitive 构造方法而言，不主张跨实例可推广』，使 validation_tests 与 confidence/alternative_explanation 一致，并与 mechanisms[3]（单实例 low，仅 repeated）对称。
- 结论引用缺失或已作废：['ys-conv-01', 'ys-conv-02', 'ys-decisions-01', 'ys-decisions-02', 'ys-timeline-01', 'ys-timeline-02', 'ys-timeline-03', 'ys-r4-001']
- 结论引用缺失或已作废：['ys-community-01', 'ys-conv-01', 'ys-decisions-01', 'ys-timeline-17', 'ys-r1-001']
- 结论引用缺失或已作废：['ys-decisions-03', 'ys-community-04', 'ys-timeline-05', 'ys-timeline-16', 'ys-works-004']
- 结论引用缺失或已作废：['ys-works-001', 'ys-works-002', 'ys-works-003', 'ys-works-004', 'ys-community-02', 'ys-community-03', 'ys-community-04', 'ys-timeline-16', 'ys-r2-001', 'ys-r2-002', 'ys-r2-003']
- 结论引用缺失或已作废：['ys-works-001', 'ys-works-002', 'ys-works-004', 'ys-community-02', 'ys-community-04', 'ys-decisions-03', 'ys-decisions-04', 'ys-timeline-05', 'ys-timeline-16', 'ys-r2-001', 'ys-r3-003']

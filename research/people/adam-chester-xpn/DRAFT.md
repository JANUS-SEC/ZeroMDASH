# 未通过独立复核

已达到最大修订次数 4；本文件是审计草稿，不得进入跨人物比较。

# Adam Chester (xpn)：漏洞研究成长分析

- 擅长领域：Windows/云/身份漏洞
- 独立复核：revise · 89/100

## 成长阶段

- **2017-03 至 2017-09 · 公开写作起点与多方向探索期**：2017-03-05 同日批次公开 Linux USBIP overflow、Foomatic-RIP、Kentico CMS SQLi、GitHub Desktop RCE/XSS、Extracting SQL Server Hashes、Bettercap NTLM Capturing、Offensive Forensics、Xbox One Controller Hacking 等多方向 writeup，2017-04-24 发布 PlaidCTF no_mo_flo writeup，2017-09-30 发布 Kerberos AD Attacks - Kerberoasting。研究主题横跨 Linux 内核、Web、Windows/SQL Server、CTF 与硬件改机，尚未聚焦单一方向；此阶段建立以引用 CVE 编号、附 PoC 的技术 writeup 形式公开发表的习惯，构成后续持续公开输出的起点。（置信度：high）
  - 证据：xpn-dec-001, xpn-tl-001, xpn-r2-001, xpn-tl-002, xpn-tl-r1-001
- **2017-11 至 2018 · 雇主变更与漏洞利用、防御规避横向扩展期**：2017-11 Defcon 25 in Review 自述居住于英国、本职为渗透测试员、当年为第二次参加 Defcon；2018-02-15《Moving jobs and exploiting flash (CVE-2018-4878)》自述因见到 MDSec 团队对社区的贡献而由 Secarma 更换至 MDSec，以期掌握 MDSec 团队成员的技能（原文 verbatim：Recently I joined the MDSec team after seeing many of the cool things that they had contributed to the community, and to hopefully pick up some of their awesome skills）。同年集中产出 CVE-2018-4878 Flash、CVE-2018-1038 Total Meltdown、Get-InjectedThread 线程注入检测规避、PowerShell AMSI 规避、macOS SIP 经 VirtualBox kext 漏洞绕过；技术栈从单一红队凭据攻击横向扩展到内核漏洞利用与防御规避，平台从 Windows 延伸到 macOS。（置信度：high）
  - 证据：xpn-tl-003, xpn-tl-004, xpn-r4-001, xpn-works-002, xpn-tl-005, xpn-tl-006
- **2020-02 至 2020-06 · 方法论成型与可复用逆向工作流期**：2020-02 AWS Lambda Redirector、2020-04 Designing The Adversary Simulation Lab 显示从单点 writeup 转向可复用红队基础设施（C2 redirector、对抗仿真实验室）的工程化输出；2020-06-06《Hiding your .NET - COMPlus_ETWEnabled》呈现稳定的逆向工作流（源码 clrconfigvalues.h 枚举 COMPlus_ 前缀设置 → Microsoft PDB → IDA xref 定位 CLRConfig::GetConfigValue → CFG 分析发现 COMPlus_ETWEnabled=0 令 CLR 跳过 ETW 注册 → 附环境变量伪造 POC），并开始系统性发布规避技术配套的防御检测引用（Roberto Rodriguez）。（置信度：high）
  - 证据：xpn-tl-007, xpn-works-003
- **2023-10 至 2024-03 · 身份提供商专题研究与会议-博客并行输出起点**：2023-10-02《Okta for Red Teamers》覆盖 Okta Delegated Authentication via Kerberos、劫持 Okta AD Agent 捕获凭据或注入 skeleton key、注册恶意 AD Agent、部署伪造 SAML 身份提供商冒充任意用户；2024-03-18《Identity Providers for RedTeamers》标注 Originally presented at SOCON-2024，覆盖 Ping、OneLogin、Entra ID，将 Okta 阶段的方法迁移到其他 IdP。会议演讲与博客长文并行、并视议题配套公开工具的输出模式最早可见于 SOCON-2024 起的 Identity Providers for RedTeamers，其工具发布为预告、未一手证实发布。（置信度：high）
  - 证据：xpn-r2-002, ac-comm-01, xpn-tl-008
- **2025-01 至 2025-04 · ADFS/DRS 与 SQL Server 加密研究期**：2025-01-12《ADFS - Living in the Legacy of DRS》逆向 ADFS 的 OAuth2/DRS 设备注册，发现内嵌 OAuth2 Client ID、PRT/Golden JWT，将 Entra ID 的 PRT 技术移植到本地 ADFS，发布 adfstoolkit，正文显式致谢并依赖 @_dirkjan (Dirk-jan Mollema) 的 ROADTools 与 DrAzureAD (Nestori Syynimaa) 的 AADInternals，同事 @hotnops 提出术语 Microsoft Stank。2025-04-16《The SQL Server Crypto Detour》用 API Monitor 钩 Windows Crypto API、WinDBG 反汇编 sqllang.dll/sqlmin.dll 还原 SMK/DMK 加密链，发现 ManageEngine ADSelfService Plus 使用微软文档示例硬编码密码，研究在 SOCON 2025 发表。SpecterOps 任职最早一手证实为 2025-04-16，2025-01-12 ADFS 博客所属雇主未证实；About 页自述现任 SpecterOps Senior Offensive Security Engineer，《The SQL Server Crypto Detour》正文另称 Service Architect，两处头衔来自不同来源，其时间或职责差异未在一手来源中澄清。（置信度：medium）
  - 证据：xpn-works-005, ac-comm-02, ac-comm-03, xpn-works-006, ac-comm-04, xpn-dec-002, xpn-tl-011
- **2025-06 至 2026-07 · LLM/AI Agent 安全转向与可度量提示工程期**：2025-11-29《An Evening with Claude (Code)》披露 Claude Code v2.0.25 sed 表达式解析缺陷（CVE-2025-64755），研究由客户开放授权评估 MCP server 风险驱动，采用 WebCrack 去混淆、DevTools 反反调试、缩短反馈循环聚焦最弱环节（sed）；2026-07-29《Prompt Engineering for Security Agents - A Measurable Approach with GEPA》提出可度量提示工程方法，将攻防与评测思维迁移到 LLM/Agent 新技术域；2026-07-30《Accelerating EDR Evasion with LLM-Driven Analysis》构建 Day Shift harness 以 LLM 驱动的自动化逆向取代人工逐夜反汇编步骤。Day Shift harness 采用 REPORT.md/STATE.md/CODEMAP.md/AGENTS.md 持久化与刻意简单的循环重启方式。（置信度：medium）
  - 证据：xpn-tl-009, ac-comm-05, xpn-self-001, xpn-self-002, xpn-self-003, xpn-self-004, xpn-self-005, xpn-self-006, xpn-self-007, xpn-self-008, xpn-works-007, xpn-tl-010, xpn-dec-003

## 主要成长机制

### 源码→PDB→反汇编 xref→CFG 分析→POC 五步逆向工作流

起点：2020-06 前，研究目标多为已有 PoC 或可经文档/源码直接定位的漏洞；对 .NET CLR、SQL Server 加密链等需要从二进制还原内部逻辑的目标，缺乏可重复的逆向工作流。

练习与反馈：《Hiding your .NET - COMPlus_ETWEnabled》(xpn-works-003) 与《The SQL Server Crypto Detour》(xpn-works-006) 两项研究中，反复执行同一五步流程：从源码枚举配置前缀或入口（clrconfigvalues.h 枚举 COMPlus_ 前缀 / SQL Server Crypto API 入口）→ 结合 Microsoft PDB 还原符号 → IDA xref 定位调用点（CLRConfig::GetConfigValue / sqllang.dll 与 sqlmin.dll 加密函数）→ CFG 分析发现触发条件（COMPlus_ETWEnabled=0 令 CLR 跳过 ETW 注册 / ESKP MD5+4字节盐与 ESP2 SHA-512+8字节盐两种 DMK 哈希方案）→ 附环境变量伪造或破解配置 POC。SQL Server 一例进一步组合 API Monitor 钩点与 WinDBG 断点，并产出可复用的 JtR dynamic_2020 规则与 Hashcat mode 30 映射。该五步流程仅清晰见于这两项研究；Claude Code 研究（xpn-tl-009）采用 WebCrack 去混淆、DevTools 反反调试、缩短反馈循环聚焦 sed 表达式解析缺陷，并非该五步流程。；POC 可触发（COMPlus_ETWEnabled=0 实际令 CLR 跳过 ETW 注册）与破解配置可复现（Hashcat mode 30 对 ManageEngine ADSelfService Plus 硬编码密码生效）为方法是否成立的反馈来源；防御检测引用（Roberto Rodriguez）提供攻防双向反馈。

能力与结果：形成可迁移到任一需要从二进制还原内部逻辑的目标（.NET CLR 内部、SQL Server 加密链）的稳定逆向工作流，并将发现转化为可复现的破解配置或环境变量 POC。；2020-06 COMPlus_ETWEnabled 规避方法与 POC；2025-04 SQL Server DMK 两种哈希方案识别（ESKP Hashcat mode 30、ESP2 SHA-512+8字节盐）与 ManageEngine ADSelfService Plus 硬编码密码发现；JtR dynamic_2020 规则与 Hashcat mode 30 映射的公开发布

置信度：medium；替代解释：两项研究间隔近五年，无法排除五步流程的相似性来自二进制逆向的通用惯例而非个人稳定方法论；亦无法排除 SQL Server 一例是客户评估偶然触发的议题而非主动迁移。Claude Code 研究未沿用此流程，提示该工作流依赖可获取 PDB 与源码的目标类型。

证据：xpn-works-003, xpn-works-006

### 会议演讲与博客长文并行、并视议题配套公开工具的输出模式

起点：2024-03 前，公开输出以博客 writeup 为主；SOCON-2024 起，会议演讲成为研究产出的另一渠道，需要将演讲议题扩展为可复现的博客长文与配套工具。

练习与反馈：对多项议题并行产出会议演讲与博客长文，并视议题配套公开工具，各段是否被一手证实按实例分别标注：Identity Providers for RedTeamers（ac-comm-01）= 会议（SOCON-2024）+ 博客已证实，工具为预告发布新的后渗透工具、未一手证实发布；The SQL Server Crypto Detour（ac-comm-04）= 会议（SOCON 2025）+ 博客已证实，无配套工具一手证据；ADFS - Living in the Legacy of DRS（ac-comm-02/03）= 博客+工具（adfstoolkit register_device.py/access_token.py/eprt.py/golden_jwt.py）已证实，无会议演讲一手证据；MacOS DirtyNIB（xpn-works-004）= 博客+工具（extract_trustcache.py）已证实，无会议演讲一手证据。任一实例均未被一手证据完整证实会议+博客+工具三段。CVE-2018-4878《Moving jobs and exploiting flash》（xpn-r4-001）仅为博客 writeup，未含会议演讲与配套工具环节，不构成会议-博客-工具输出模式的实例。；会议采纳（SOCON-2024、SOCON 2025）提供议题被议程接受的反馈；GitHub star/fork 数（ac-comm-06：RandomTSScripts 214、OktaPostExToolkit 200、ssh-inject 191 等）为工具被社区采用的可观察指标，仅证明工具被采用，不证明会议-博客-工具输出循环的稳定性；RastaMouse 对 SQL Server 演讲制作 abridged copy 戏仿版本为可观察的同行公开反馈信号。

能力与结果：形成将一项研究同时服务于会议演讲、博客长文深度化与配套工具公开的多渠道输出能力，使演讲议题可被同行复现与二次开发。；SOCON-2024 Identity Providers for RedTeamers 议程采纳与博客长文；SOCON 2025 The SQL Server Crypto Detour 议程采纳与博客长文；adfstoolkit 与 extract_trustcache.py 工具公开；RastaMouse 对 SQL Server 演讲的戏仿版本

置信度：medium；替代解释：会议-博客-工具的多渠道输出可能是议题类型（如身份、SQL Server）适合长文与工具化的结果，而非个人稳定方法论；GitHub star/fork 数与议程采纳均为结果指标，无法直接证明稳定的输出循环已内化为方法论。SOCON 议程页未独立抓取，会议归属仅依据博客自述。

证据：ac-comm-01, ac-comm-02, ac-comm-03, ac-comm-04, ac-comm-06, xpn-works-004, xpn-r2-002, xpn-r4-001

### 借助前人公开成果起步并以披露流程摩擦为反馈

起点：跨入新议题时，缺乏从零开始的依据；以社区既有公开成果（Dave Schumaker 的 blog、Elad Beber 的 CVE writeup、@_dirkjan 的 ROADTools、DrAzureAD 的 AADInternals）作为起步基线。

练习与反馈：2025-11 Claude Code 研究先借助 Dave Schumaker 的 blog 与 Elad Beber 的 CVE writeup 起步（xpn-self-003）；2025-01 ADFS 研究显式致谢并依赖 @_dirkjan 的 ROADTools 与 DrAzureAD 的 AADInternals 提供大量示例与代码（ac-comm-02）；2026-07 GEPA 研究在与 Dreadnode 交流时首次接触 GEPA，随后亲手重建以理解其高层工作方式而非直接套用（xpn-self-004）。披露环节以流程摩擦为反馈：2025-10 Claude Code 漏洞首次联系 Anthropic 安全邮箱被自动回复导向 HackerOne，随后改走内部团队路径获得快速修复（ac-comm-05）。；披露流程的摩擦（标准入口失效 → 内部联系人路径生效）为披露渠道选择的反馈；前人成果的可用性与引用关系为新议题起步可行性的反馈。

能力与结果：形成以社区既有公开成果为起步基线、以披露流程摩擦为渠道经验积累的协作型研究习惯。；Claude Code CVE-2025-64755 经 Anthropic 内部团队路径修复并分配 CVE；ADFS 研究对 ROADTools 与 AADInternals 的引用与工具链复用；GEPA 概念的亲手重建以验证理解

置信度：high；替代解释：借助前人成果是安全研究的普遍惯例，区分度可能有限；披露流程摩擦仅在 Claude Code 一例中一手叙述，其在其他研究（DirtyNIB 2021-11 向 Apple 报告）中是否重复未一手证实。

证据：xpn-self-003, xpn-self-004, ac-comm-02, ac-comm-05

### 不满驱动的可度量工具化建设

起点：面对反复出现且不可测量的研究问题，依赖主观判断的方法被认为不可接受。

练习与反馈：2026-07 GEPA 研究中，对 LLM prompt 修改不可测量感到困扰，认为依赖主观判断不可接受，因此寻找结构化、可度量的方法；将反复出现的问题（不可测量）转化为可工程化解决的子问题（xpn-self-006）。同时采集高分与低分运行 trace 作为优化器的负样本依据，并以同一视角用于自身实验（xpn-self-005）；对 CLIPS（LISP 风格语言）采用购书系统学习的固定动作（xpn-self-007）。2026-07 Day Shift harness 针对 LLM 常提前退出任务或未用尽采集数据的缺陷，采用刻意简单的循环重启方式与循环间状态文件共享（xpn-self-008）。；低分 trace 反例、朴素 reward function 的过拟合自承，以及对实验局限的诚实自我评估为方法改进的反馈来源。

能力与结果：形成将不可测量的问题转化为可工程化、可度量子问题并以工具化解决的稳定习惯，并保留对自身实验局限的诚实自我评估。；GEPA 可度量提示工程方法的提出；Day Shift harness 的 LLM 驱动自动化逆向与循环重启设计；对自身 reward function 极度朴素与部分 prompt 过拟合的自承

置信度：medium；替代解释：不满驱动的工具化建设仅见于 2026-07 LLM 期一手自述，无法证明其为贯穿全程的稳定机制；可度量方法可能是 GEPA 议题本身的要求而非个人方法论。转向 LLM 的具体触发事件在一手来源中未直接说明，当前为基于发布时间线的推断。

证据：xpn-self-004, xpn-self-005, xpn-self-006, xpn-self-007, xpn-self-008, xpn-works-007

## 可迁移与不可迁移

- 可迁移：对需要从二进制还原内部逻辑的目标，采用源码→PDB→反汇编 xref→CFG 分析→POC 的逆向工作流，并将发现转化为可复现的破解配置或环境变量 POC。
- 可迁移：将低分运行 trace 作为优化器的负样本依据，显式从负面样本提取规则并用于自身实验的诚实自我评估。
- 可迁移：研究路径依赖并引用同行公开成果（ROADTools、AADInternals、前人 CVE writeup）作为起步基线，而非从零开始。
- 可迁移：披露环节当标准入口失效时转向内部联系人路径，并以公开时间线标注厂商响应速度，形成可复用的披露规范范例。
- 可迁移：将反复出现的问题（不可测量）转化为可工程化解决的子问题，以结构化、可度量的方法替代主观判断。
- 可迁移：面对新领域采用购书系统学习的固定动作，随后亲手重建以验证理解而非直接套用。
- 可迁移：会议演讲与博客长文并行产出，使议题可被同行复现与二次开发；GitHub star/fork 数仅作为工具被社区采用的可观察指标，不作为输出循环稳定性的支撑。
- 可迁移：明示知道何时需逐行审查代码，并在静态分析与动态分析之间作出混合选择的判断（I prefer a hybrid approach of static and dynamic analysis）。
- 可迁移：缩短反馈循环作为研究的关键转折点：把大问题拆为可单元测试的小函数以加速验证。
- 不可直接迁移：SpecterOps 雇主身份提供的非标准评估类型与客户素材（如 ManageEngine ADSelfService Plus .bak 备份）构成特定议题来源，非个人方法论可迁移。
- 不可直接迁移：SpecterOps 同事网络（@hotnops 术语共创、内部线程共享 EDR 规则）为组织内部资源；Justin Elze 为 TrustedSec 平行工作者而非 SpecterOps 同事，外部同行不并入组织内部网络。
- 不可直接迁移：EDR 长期夜间人工持续逆向的累积经验为特定时期、特定目标的累积，无法被新研究者短期复制；Day Shift harness 以 LLM 驱动的自动化逆向取代该步骤，但二者关系为基础推断而非一手陈述。
- 不可直接迁移：跨约 9 年的持续公开发表与博客基础设施（blog.xpnsec.com 自 2017-03 起的累积公开记录）为长期个人输出渠道，新研究者无法短期建立等价渠道。
- 不可直接迁移：DirtyNIB 漏洞 2021-11 即向 Apple 报告，经多轮邮件与 CVE 分配后至 2023-10 仍未修复，逐版本对抗（macOS Ventura Launch Constraints 用 img4tool 解析 trust cache、macOS Sonoma bundle 限制用重命名 Contents 目录绕过）依赖与厂商反馈的具体交互时间线，不可迁移。

## 复核问题

- 字段 mechanisms[2].name / .repeated_practice / .feedback：原措辞'披露流程摩擦'、'披露流程的摩擦'、'流程摩擦'将物理概念'摩擦'用于抽象披露流程，属比喻表达，且为该机制名称的承载性措辞。改写方向：以事实序列替代，例如'披露流程中标准安全邮箱入口失效（被自动导向 HackerOne）并转向内部团队路径'，移除'摩擦'一词。
- 字段 mechanisms[3].feedback / .intermediate_capability 与 transferable_practices[1]：原措辞'诚实自我评估'以'诚实'评价研究对象品性，非克制专业书面语。改写方向：采用同机制 observed_outcomes 已使用的'自承'，例如'对实验局限的自承'或'对自身 reward function 朴素与部分 prompt 过拟合的自承'，保持一致并去除评价性修饰。
- 字段 mechanisms[1].repeated_practice：原句'该帖为博客 writeup，未含会议演讲与配套工具环节；'无明确指代对象，且与紧随其后的'CVE-2018-4878《Moving jobs and exploiting flash》（xpn-r4-001）仅为博客 writeup，未含会议演讲与配套工具环节，不构成会议-博客-工具输出模式的实例'内容重复，属编辑残留。改写方向：删除该悬空句，保留后一句对 CVE-2018-4878 不构成该输出模式实例的陈述。

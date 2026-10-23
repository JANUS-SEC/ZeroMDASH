# Csaba Fitzl：漏洞研究成长分析

- 擅长领域：macOS 漏洞
- 独立复核：pass · 92/100

## 成长阶段

- **2006–约2012 · 网络工程起点期**：2006 年以计算机工程师身份毕业，随后从事约 6 年网络工程师工作，负责大型网络的故障排查与设计。这一阶段的可核验能力为网络协议理解与故障定位，是其后续红队阶段网络取证与攻击面分析的技能前身；职业起点为网络工程而非安全研究，说明安全与漏洞研究为后期转入。（置信度：high）
  - 证据：csaba-fitzl-deepconv-04-2006-graduation-and-network-engineer-start, dec-01-2006, csaba-fitzl-ext-01, fitzl-tl-01
- **约2012–2020 · 蓝/红队跨域积累期（含通用逆向与平台转向过渡）**：自述此后从事约 8 年蓝/红队工作，覆盖网络取证、恶意软件分析、对手模拟与防御绕过；按 6+8 年自 2006 起算，该阶段延伸至约 2020 年，与 2019、2020 年 macOS 公开议题存在重叠。2014–2017 年以非 macOS 的通用逆向与利用自动化方向产出 Workshop（Hello PDF 2014、Hello Anti-Disassembly 2015、Exploit Generation and Automation with WinDBG 2016、How to Convince a Malware to Avoid Us 2017），2018 年 DEF CON 26 / hack.lu 举办 Driver Signing Enforcement Bypass Workshop（提供演示文稿、工作簿、VM 配置指南与练习文件四件套）。2018 DSE Workshop 的目标平台（Windows 驱动签名强制 vs macOS kext 签名）未能从可抓取的一手材料确认：演示稿 PDF 正文为 FlateDecode 压缩流不可读、DEF CON 媒体服务器返回 403、defcon.org 议程页与 hack.lu 归档页返回 404；术语 DSE 在通用语境中多指 Windows 驱动签名强制，但本节点不以术语推断作为平台归属定论。红队结束年份为约 2020 的概算，与 macOS 转向窗口（2018–2019）重叠，不应理解为红队于 2018 年前结束。（置信度：medium）
  - 证据：csaba-fitzl-deepconv-01-career-timeline, csaba-fitzl-ext-02, fitzl-tl-02, cf-comm-07, cf-works-02, cf-works-03, fitzl-tl-03, fitzl-tl-04, fitzl-tl-05, fitzl-tl-06, fitzl-tl-07
- **2018–2019 · macOS 平台转向期**：2019 年起研究重心转向 macOS：6 月 1 日博客记录 'Getting root with benign AppStore apps'，同年 3 月 31 日发布首篇可核验 post（CVE-2019-5514，VMware Fusion Guest VM RCE）；并在 Troopers、SecurityFest、Objective By The Sea v2.0、Hacktivity 发表 'GateKeeper: Bypass or not Bypass?' 等 macOS 议题，开启以 macOS 信任机制（GateKeeper、App Store 权限）为主的公开输出。EXP-312 'Advanced macOS Control Bypasses' 课程开发为其自述的进入 macOS 安全的正式入口，但起始年份未知。若 2018 DSE Workshop 确为 Windows 驱动签名绕过，则存在签名验证绕过思维的平台迁移；因平台归属不可一手核验，此迁移作条件式保留，stage 2 的承重证据为已核验的 2019 年 macOS 议题。（置信度：medium）
  - 证据：cf-works-04, fitzl-tl-08, fitzl-tl-09, fitzl-tl-10, dec-04-offsec-exp312, csaba-fitzl-deepconv-02-exp312-course-development, csaba-fitzl-ext-03, fitzl-tl-22
- **2019–2024 · macOS 控制绕过纵深期**：研究重心由信任机制转入 XPC 进程间通信、目录权限与控制绕过纵深：2020 年 XPC Exploitation on macOS、Exploiting Directory Permissions on macOS；2021 年起与 Wojciech Regula 系统性合著 macOS 隐私绕过系列（BlackHat US 2021 '20+ Ways' → BlackHat EU 2022 '20+ New Ways' → BlackHat Asia 2024 'The Final Chapter'），同年起 Virus Bulletin/OBTS 发表 Endpoint Security Framework 议题；2022 年 BlackHat Asia 'macOS Vulnerabilities Hiding in Plain Sight' 附白皮书，LaunchConstraints/TCC 成为持续研究主干。2021-04-23 公开复盘 Apple Security Bounty 交互（两年内提交约 50 例，沟通稀少，自述 'Often times, it feels like I'm sending emails into a black hole.'、'bittersweet'、'if you want to get updates, follow up frequently'），形成厂商反馈与披露流程的公开复盘。（置信度：high）
  - 证据：fitzl-tl-11, fitzl-tl-14, cf-comm-01, csaba-fitzl-ext-06, cf-works-05, fitzl-tl-15, cf-works-08, fitzl-tl-16, fitzl-tl-17, cf-comm-02, dec-06-collaborators
- **2024–2026 · 系统审计与规模化披露期**：研究方法从单点漏洞发现升级为系统性代码审计：2024-11-08 / 12-12 发布 'The diskarbitrationd and storagekitd Audit Story' 两部曲连载；同年 'History of macOS DiskArbitration Vulnerabilities'、'Apple Disk-O Party'、'Mac, Where's My Bootstrap?'（与 Brandon Dalton 合著）。2025 年 'Finding Vulnerabilities in Apple Packages at Scale' 标志规模化漏洞挖掘，CVE-2025-24277（Apple macOS Crash Reporter 组件目录路径解析漏洞，'A parsing issue in the handling of directory paths was addressed with improved path validation.'，'An app may be able to gain root privileges.'）经 NVD 与 Apple 安全公告 HT122373 独立佐证，署名报告者为 Csaba Fitzl of Kandji 与 Gergely Kalman；与 Kalman 形成新合著线（Hexacon/OBTS/BSidesBud 2025–2026、Zer0Con 2026）。（置信度：high）
  - 证据：cf-works-09, fitzl-tl-18, fitzl-tl-19, cf-works-11, fitzl-tl-20, fitzl-tl-21, cf-r1-e01, cf-r1-e02, csaba-fitzl-ext-08, cf-comm-06, dec-07-disclosure-cve-2025-24277, dec-05-kandji

## 主要成长机制

### 同伴合著作为方向校准与产出节奏回路

起点：2019 年转入 macOS 专项后，研究对象为单一平台机制，公开输出需经会议评审与同伴互审方得以发表，存在对方向选择与技术深度的外部校准需求。

练习与反馈：2021 年起与 Wojciech Regula 系统性合著 macOS 隐私绕过系列（BlackHat US 2021 '20+ Ways' → BlackHat EU 2022 '20+ New Ways' → BlackHat Asia 2024 'The Final Chapter: Unlimited ways'），同一技术线跨 4 年以递进标题系列化再发表；2024 年另与 Brandon Dalton 合著 'Mac, Where's My Bootstrap?'，2025–2026 年与 Gergely Kalman 合著 'Crash One: A Starbucks Story - CVE-2025-24277' 与 'macOS Exploit Mixtape'（Zer0Con 2026）。；合著与会议评审构成同伴互审渠道；其中 Kalman 合著线由 Apple 官方公告 HT122373 独立列出 Fitzl 与 Kalman 为 CVE-2025-24277 共同报告者，构成对合著关系的非自列第三方印证。

能力与结果：形成基于合著的同伴互审（Kalman 线由 Apple 官方公告 HT122373 独立佐证，Regula 线仍仅由本人 Talks 索引自列），作为方向选择与技术深度的校准渠道；同一漏洞叙事在多场会议复用（CVE-2025-24277 于 Hexacon/OBTS/BSidesBud）构成发布节奏的强制外部校准。；macOS 隐私绕过系列跨 4 年三阶段再发表（20+ Ways → New Ways → Final Chapter）；CVE-2025-24277 经 NVD 与 Apple HT122373 独立佐证并由 Apple 公告署名共同报告者；合著对象从 Regula 扩展至 Dalton、Kalman，协作网络在 2024–2026 更新而非衰减

置信度：high；替代解释：合著关系仍以自列为主：Regula 合著线仅由本人 Talks 索引自列，未抓取到独立同行评价或第三方背书（csaba-fitzl-ext-10 记录未抓取到独立同行评价）；Apple 公告仅对 Kalman 线构成独立佐证，不能外推至全部合著关系。合著频率也可能反映 macOS 子领域研究者基数小、合适合著者有限的结构性约束，而非主动构建的校准回路。

证据：cf-comm-01, cf-comm-06, csaba-fitzl-ext-06, csaba-fitzl-ext-08, cf-works-05, cf-r1-e02, dec-06-collaborators, dec-07-disclosure-cve-2025-24277

### 失败与反馈的公开复盘

起点：macOS 漏洞披露依赖单一厂商（Apple）的赏金与 CVE 流程，研究者与厂商反馈之间存在结构性信息不对称与沟通稀少；公开材料以成功议题与披露为主，失败与被拒反馈通常不被公开发表。

练习与反馈：2021-04-23 公开复盘与 Apple Security Bounty 的两年交互（提交约 50 例，沟通稀少，自述 'Often times, it feels like I'm sending emails into a black hole.'，总评自述为 'bittersweet'，给出 'if you want to get updates, follow up frequently' 的可操作经验）；2021-04-20 在 CVE-2020-9900 分析中对自身技术细节不确定处公开标注并邀请原作者纠错（'Maybe CX01 will correct me, and if so I will update this post.'）；2021-05-26 记录 TeamViewer 漏洞经中介管道 VCP/iDefense 报告后错过厂商修复发布；2025-12-05 记录同一 installer 目录操纵类问题向 Apple 报告达 7 年仍未获 CVE 或赏金（'I never got a CVE, nor any reward for this'）。；厂商反馈低质量（沟通稀少、资格争议、修复通知缺失）驱动其形成'高频追问'的应对策略；将同侪共有经验上升为对程序的集体批评（'we share the same experiences'）；公开标注不确定并邀请原作者更正，构成出版实践中内嵌的社区纠错通道。

能力与结果：形成把'被拒绝/被采纳/漏接'的反馈过程纳入公开记录的习惯，将反馈失败本身转化为可发表的研究产出与方法论资产。；'Experiences with Apple Security Bounty' 把厂商反馈失败作为公开研究产出；CVE-2020-9900 writeup 以公开不确定标注处理同侪工作重叠；.localized 目录操纵问题坚持报告 7 年并公开复盘连续被拒；TeamViewer 漏接修复经公开记录形成对中介管道与厂商通知机制的复盘

置信度：high；替代解释：该机制仅覆盖本人选择公开发表的失败子集（Apple Security Bounty、CVE-2020-9900 不确定标注、TeamViewer 漏接、.localized 七年被拒）；未公开发表的拒绝与未被采纳且未记录的提交不可见，公开复盘频率不等同于失败复盘习惯的强度。选择公开发表失败本身可能是研究可见度策略的一部分，而非纯粹的方法论自省。

证据：cf-comm-02, cf-comm-04, cf-comm-05, cf-works-10

### 系列化与可复现教学/工具建设作为知识沉淀回路

起点：2014 年起即以 Workshop 形式授课，早于 macOS 专门化时期；研究对象分散，需将研究方法拆解为可被他人重复执行的步骤方可在会议教学场景输出。

练习与反馈：2014 Hello PDF、2015 Hello Anti-Disassembly、2018 DEF CON 26 / hack.lu DSE Bypass Workshop 均附工作簿与练习文件，2018 年另含 VM 安装指南；为 OffSec 开发 EXP-312 'Advanced macOS Control Bypasses' 课程；2021-09-27 因 'many people used to ask me where to start learning about macOS security or exploitation' 撰写 'Getting started in macOS security' 入门指南并索引 20 余位研究者博客与会议资源；'Beyond good ol' LaunchAgents'、'The Lord of The Rules'（2022-10-24 起 prologue）、'diskarbitrationd and storagekitd Audit Story'（2024-11/12 Part 1/2）以系列化结构跨期连载。；他人重复提问反向驱动其整理知识并绘制同侪网络图谱（'Getting started' 一文末尾以 'probably far from being complete' 邀请补充，构成持续校准回路）；Workshop 与课程的教学场景要求方法可被他人复现，构成对方法可重复性的外部检验。

能力与结果：形成以可复现教学/工具材料（workbook/exercise/VM 指南/课程/入门指南/审计连载）为载体的知识沉淀习惯，把分散研究外化为可校准、可迭代维护的公共资产；系列化结构（prologue→正文、part1→part2）使每篇研究自动成为下一阶段的基线。；2014–2018 三次 Workshop 均含可复现练习材料四件套；EXP-312 课程把 macOS 控制绕过知识系统化为可教学内容；'Getting started' 入门指南把同侪网络固化为公开索引并邀请补充；2024 Audit Story 两部曲以连载形式公开系统服务审计过程

置信度：medium；替代解释：系列化与教学输出也可能是会议 CfP 评审与课程商业化的外部需求驱动，而非研究者主动的知识沉淀选择；OffSec 课程开发的具体时间与商业约束不可核验（About 页未给年份）。

证据：cf-works-02, cf-works-06, cf-comm-03, cf-comm-07, cf-comm-08, csaba-fitzl-deepconv-02-exp312-course-development, csaba-fitzl-deepconv-05-beyond-good-ol-launchagents-series, dec-04-offsec-exp312, cf-works-09

### 子系统纵向深耕与方法升级回路

起点：转入 macOS 专项后，单一系统服务（如 DiskArbitration）存在跨版本、跨年度的缺陷积累，为对同一子系统反复研究并升级方法论提供客观条件。

练习与反馈：DiskArbitration 类研究跨 4 年系统化：2021 OBTS/Hacktivity 'Mount(ain) of Bugs'（单点 bug）→ 2024 MacSysAdmin/Hacktivity 'History of macOS DiskArbitration Vulnerabilities'（历史综述）→ 2024 POC/BlackHat EU/BSidesBud 'Apple Disk-O Party' → 2024-11/12 'diskarbitrationd and storagekitd Audit Story' Part 1/2（系统性代码审计）；AMFI LaunchConstraints 从 2022-06-14 'First Quick Look' 到 2023-10-09 'Deep Dive' 相隔约 16 个月由浅入深打磨。；同一子系统的历史综述与审计连载使其对既有缺陷的总结反哺新一轮审计的攻击面选择；单点 bug 积累到一定数量后触发从'发现-报告'到'审计叙述'的方法论跃迁。

能力与结果：形成对单一子系统长期投入、按方法论层级递进（单点 bug → 历史综述 → 系统审计）的深耕习惯，把审计过程本身作为可发表内容。；DiskArbitration 研究在 4 年内完成单点 bug → 历史综述 → 系统审计三阶跃迁；LaunchConstraints 从速览到深度解析相隔约 16 个月的持续打磨；Audit Story 把系统性代码审计过程作为可发表连载输出

置信度：medium；替代解释：同一子系统反复出现缺陷也可能是 macOS 该子系统长期设计薄弱的客观结果，而非研究者主动的纵向深耕选择；'History of' 与 'Audit Story' 的发表形式也可能是会议主题偏好驱动的包装策略。

证据：cf-works-11, cf-works-09, fitzl-tl-16, fitzl-tl-18, fitzl-tl-19

## 可迁移与不可迁移

- 可迁移：把研究方法拆解为可复现练习材料（workbook/exercise/VM 指南）并随 Workshop 公开，使方法可被他人重复执行与校准——该做法不依赖 macOS 平台特有条件，可迁移至其他安全研究方向。
- 可迁移：对同一子系统跨年度以递进形式（单点 bug → 历史综述 → 系统审计）重复研究，把审计过程本身作为可发表内容，形成方法论跃迁的可复用路径。
- 可迁移：在公开写作中以显式不确定标注加邀请原作者更正的方式处理同侪工作重叠，把不确定性与更正承诺写入公开文本，作为接受外部校准的接口。
- 可迁移：把他人重复提问反向驱动的研究方向整理为可公开复用的入门指南，并以'邀请补充'构成持续校准回路。
- 可迁移：对厂商反馈失败（被拒、漏接、沟通稀少）做公开复盘，将反馈失败本身转化为可发表的方法论资产，并形成'高频追问'的披露流程策略。
- 不可直接迁移：macOS 子领域研究者基数小、合适合著者有限，与 Wojciech Regula、Gergely Kalman 的长期合著关系部分源于该子领域结构性的合著者稀缺，而非通用可复制的协作策略。
- 不可直接迁移：Apple Security Bounty 作为单一厂商赏金与 CVE 流程的特定反馈机制，其沟通稀少、资格争议、修复通知缺失等特征为 Apple 流程特有，不能外推至其他厂商的披露流程。
- 不可直接迁移：DiskArbitration、LaunchConstraints、Endpoint Security Framework 等 macOS 特有子系统的长期缺陷积累，是该平台设计特征提供的客观条件，迁移至其他平台需对应子系统存在类似长期设计薄弱点。
- 不可直接迁移：OffSec EXP-312 课程开发岗位与 Kandji Principal macOS Security Researcher 现职为特定雇主提供的机构化研究支持，非研究者个人可复制的条件；其起止时间未公开，机构支持强度不可核验。
- 不可直接迁移：2014–2018 年 Workshop 四件套教学输出早于 macOS 专门化时期，其时会议 Workshop 教学场景与可复现练习材料的评审门槛为当时安全会议生态特有，不一定适用于当前会议生态。

## 复核问题


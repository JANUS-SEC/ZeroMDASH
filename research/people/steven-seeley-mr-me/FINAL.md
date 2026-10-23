# Steven Seeley (mr_me)：漏洞研究成长分析

- 擅长领域：企业软件与浏览器漏洞
- 独立复核：pass · 84/100

## 成长阶段

- **2016-09 至 2017-09 · 桌面文档格式/内存破坏起点与向 Web 反序列化及内核利用的初次迁移**：以 Microsoft Excel 类型混淆（CVE-2016-3363/MS16-107）与 Word OneTableDocumentStream 下溢（CVE-2016-7290/MS16-148）为公开输出起点，形成对文档格式解析与内存布局的逆向分析能力；2017-04-27 发布《From Serialized to Shell :: Auditing Google Web Toolkit》转向 Web 应用反序列化与表达式语言注入，并于 2017-05-22 发布同期配对的另一篇《Exploiting Google Web Toolkit with EL Injection》，建立审计与利用两段式 writeup 习惯；2017-09-06 发布《Sharks in the Pool》从用户态利用向 Windows 内核池迁移。早期 Office 三篇的具体方法学细节未逐字核对，方向由标题与 CVE 推断，对应 ss-pub-001 与 timeline 项标记为 inferred。（置信度：medium）
  - 证据：ss-pub-001, timeline-2016-09-earliest-writeup, timeline-2016-12-word-cve-2016-7290, timeline-2017-04-gwt-serialization-pivot, dec-01
- **2018-01 至 2018-12 · 客户端阅读器方向成熟与定制工具及补丁绕过的首次出现**：在 Foxit Reader 方向判定信息泄露类漏洞无法被传统 fuzzing 发现，自建 WinDbg JavaScript 桥接插件 bridgit 辅助检测，并在利用阶段以泄露的堆指针替代堆喷射，在 Windows 7 与 10 上达到 100% 成功率；接受 Ke Liu（腾讯玄武实验室）将 CVE-2018-4990 根因由 double free 更正为两个 arbitrary free 条件的修正；同期出现首次补丁绕过实践——WebExec Reloaded（CVE-2018-15442）以对 Ron Bowes 原 WebExec 补丁的 re-discovery 与绕过形式发布。CVE-2018-4990 的 Ke Liu 修正正文未逐字核验，对应 ss-pub-004 标记为 unknown。（置信度：medium）
  - 证据：ss-pub-002, ss-pub-003, ss-pub-004, ss-community-005, r1-ss-webexec-ronbowes
- **2019-01 至 2020-12 · 企业 Web 预认证 RCE 的方向确立与系统化枚举产出**：2019-05-17 发布《Panic! at the Cisco》将公开作品重心转向企业 Web 应用预认证 RCE 链，采用 web.xml servlet 映射追溯数据流的静态审计结合补丁 diffing，发现 Cisco 将单个 CVE 分配给两个不同漏洞且仅修补其一，并指出该漏洞因仅在配置高可用后可达而躲过多轮代码审计；2019-08-07 发布《Attacking Unmarshallers》以 Doyensec 此前 jackson gadgets 工作为起点开展跨版本迭代；2020 年针对 Cisco DCNM、HPE IMC、Cisco UCS Director 等企业网络管理产品做系统性枚举式挖掘，advisory 量级由个位数跃升至百级；2020-01 与 Chris Anastasio 组成 Team Incite 参加 Pwn2Own Miami 2020 攻克 Schneider EcoStruxure Operator Terminal Expert，赛后公开复盘赛前静默补丁对利用链的破坏。Pwn2Own Miami 2020 的 Team Incite 参赛事实由 Wikipedia 二手条目支撑，具体攻破产品名存在缺口。（置信度：medium）
  - 证据：ss-pub-005, r1-ss-pub-011-doyensec, timeline-2019-cisco-prime-advisory-volume, timeline-2020-cisco-dcnm-hpe-imc-volume, timeline-2020-01-pwn2own-miami-team-incite, dec-03, ss-pub-006, ss-deep-02, ss-deep-03, ss-community-006
- **2021-01 至 2021-12 · 云与 .NET 方向的选定与研究方法产品化教学**：加入奇虎 360 Vulcan Team（360 Vulcan Team 归属仅由本人博客自述，未获独立确证）后获得研究方向选择权，因自身 .NET 知识有限而选定微软云网络作为补足该技术能力的方向，以既有的 Web 安全能力作为切入云与 .NET 方向的依托；2021-01-12 发布《Making Clouds Rain》并确立递减披露时间线规则（首 bug 90 天、首个补丁绕过 60 天、第二个补丁绕过 30 天，每出现一次绕过缩短 30 天，不对任何厂商改规则）；2021-07-13 起 Full Stack Web Attack 训练课产品化，并在挑战题中植入隐藏 0day 以检验学员发现能力；2021-08-25 以 Source Incite 队名参加 Pwn2Own Vancouver 2021，目标 Microsoft Exchange Server，结合约 12 年前的 MiTM 经验并以代码模式检索定位新攻击面。Pwn2Own Vancouver 2021 的 Source Incite 队名与成功结果由 Wikipedia 二手条目支撑；ZDI/Trend Micro 官方结果页返回 403/404，获奖名次与奖金未由官方页面证实。（置信度：medium）
  - 证据：ss-deep-01, dec-02, ss-deep-04, ss-pub-007, ss-deep-05, ss-deep-06, timeline-2021-04-pwn2own-vancouver-source-incite, timeline-2021-exchange-sharepoint-pwn2own-writeup, dec-04, ext-pwn2own-06
- **2022-01 至 2022-12 · VMware 产品族链式挖掘与教学反馈流程的扩展**：2022 年研究重心转向 VMware 产品族，于 8 月 9 日发布 vRealize Operations Manager 预认证 RCE、8 月 11 日发布 Workspace ONE Access 0-click 利用链、10 月 25 日发布 NSX Manager 预认证 RCE；NSX Manager 研究由 Full Stack Web Attack 过往学员 Sina Kheirkhah主笔、与 Steven Seeley 合著发布，形成教学输出—学员带回目标—协作合著的长期带教协作流程。同期 2022-01-20 发布 ZohOwned（CVE-2021-44515），由 FBI 2021-12-17 flash alert、William Vu 在 AttackerKB 的静态分析、作者比对 IOCs 后判定为同源零日，以及 Zoho 2021-12-03 自家 advisory 共同印证，作为第三方对研究有效性的外部印证。VMware NSX 学员合著关系以 ss-community-003（documented）为主锚点；ss-pub-008（NSX，unknown）仅作辅证，不与 documented 项等量齐观。（置信度：medium）
  - 证据：timeline-2022-vmware-product-family, ss-community-003, ext-student-04, r1-ss-comm-009-fbi-vu
- **2023-01 至 2026-01 · 跨厂商定点研究与补丁变体审计方法的成熟**：advisory 产出量较 2020-2022 高峰下降，由单厂商高频枚举转向跨厂商定点研究，方向覆盖 Apache Struts、TP-Link Archer、PTC Thingworx、Cacti、NETGEAR ProSAFE NMS、Inductive Automation Ignition、KeySight N6841A、Trackplus Allegra 等；2024-07-21 博客自述退役 Full Stack Web Attack 训练课的部分内容并预告下一期课程在罗马开设，该退役具体内容即 JNDI Injection via Path Manipulation in MemoryUserDatabaseFactory 系由博客主题推断，原文仅称 some of the content，仅作辅证；2024-11-25 发布 Spring Properties RCE，以 Process Monitor 观察 Tomcat 加载 application.xml 的行为定位配置加载顺序，经 logback JNDI 注入实现未授权 RCE，并公开复盘方法选择的妥协与未走通方向；2026-01-28 发布 Samsung MagicINFO 9 Server 系列研究，采用补丁审查—识别 CVE-2025-54438 的 FTP 变体 downloadChangedFiles 未修补—TOCTOU/SQL/FTP 写入多原语链方法，并主动联系 Shielder 共享 CIFS 绕过报告以协作完成利用。Spring Properties 前学员带回关系以 ss-pub-009（documented）为主锚点；ss-community-004（Spring 前学员，unknown）仅作辅证，不与 documented 项等量齐观。（置信度：medium）
  - 证据：timeline-2023-2024-zdi-collaboration-pivot, rr2-ss-dec-05a, ss-pub-009, ss-pub-010, timeline-2026-01-samsung-magicinfo-latest, ext-github-08

## 主要成长机制

### 补丁审计驱动的未修补变体与跨组件多原语链发现

起点：2018-12-03 WebExec Reloaded（CVE-2018-15442）作为对 Ron Bowes 原 WebExec 补丁的 re-discovery 与绕过，时间早于 2019-05-17《Panic! at the Cisco》中对 Cisco 将单个 CVE 分配给两个不同漏洞且仅修补其一的发现，构成补丁审计实践的起点；2018-12-03 厂商补丁被自述为 wasn't so good 的外部反馈亦同期出现。

练习与反馈：对补丁做 diffing 并追问补丁是否覆盖完整攻击面：从 Cisco 单 CVE 双漏洞仅修其一、Schneider EcoStruxure 赛前静默补丁（无 CVE），到 2026 年 CVE-2025-54438 的 FTP 变体 downloadChangedFiles 未被修补；在识别未修补变体后，以 TOCTOU、SQL 注入、文件写入、认证绕过等多原语组合构造跨组件利用链。；厂商补丁质量与披露行为的公开复盘（WebExec 补丁 wasn't so good、Schneider 静默补丁、Vanilla Forums 对厂商信息披露的批评）作为研究反馈循环的一部分；递减披露时间线规则（每出现一次绕过缩短 30 天、不对任何厂商改规则）将补丁绕过经验固化为可重复规则。

能力与结果：形成由补丁审查定位未修补变体、再以跨组件多原语链完成利用的研究方法，并据此对 Cisco、VMware、Samsung 等厂商产品族做链式挖掘。；2019-05-17《Panic! at the Cisco》识别 Cisco 单 CVE 双漏洞仅修其一（CVE 关联与高可达性配置分析）；2020-02-18《Silent Schneider》公开复盘 Schneider EcoStruxure 赛前静默补丁对利用链的破坏；2026-01-28《Samstung Part 2》识别 CVE-2025-54438 的 FTP 变体 downloadChangedFiles 未修补并主动联系 Shielder 协作完成利用；2018-12-03 WebExec Reloaded 作为对 Ron Bowes 原 WebExec 补丁的绕过，构成该机制的时间起点

置信度：high；替代解释：补丁变体的发现亦可能源于同一厂商产品族在代码模式上的复用而非专门的补丁审计流程；Cisco 单 CVE 双漏洞、Schneider 静默补丁、Samsung FTP 变体三例的时间跨度较大，且 Schneider 一例属赛事前置条件而非主动补丁审计，跨时期的因果连续性为推断而非一手自述的统一方法。

证据：r1-ss-webexec-ronbowes, ss-pub-005, ext-feedback-07, dec-03, ss-pub-010, ss-deep-04, ss-community-007

### 以同行公开研究为起点的跨版本迭代

起点：2020-08-19 Horde Groupware 利用链构建中复用并改造 EgiX 于 CVE-2014-1691 使用的旧 POP 链，以适配 PHP 7+ 的 Serializable 接口变化与 5 年间类定义演进，显示其倾向于以既有公开研究为起点再按当前环境迭代适配。

练习与反馈：在公开 writeup 中显式声明研究所继起的同行工作，并对其成果做跨版本改造或补丁绕过：2019-08-07《Attacking Unmarshallers》明确 based upon the excellent work perform by Doyensec 并引 doyensec 2019-07-22 jackson-gadgets 博文；2018-12-03 WebExec Reloaded 接续 Ron Bowes 原 WebExec 发现并对其补丁做绕过。；同行公开 writeup 作为可迭代的输入，新版本的环境差异（PHP 7+ 接口变化、厂商补丁）作为迭代适配的反馈信号；2018-05-21 CVE-2018-4990 接受 Ke Liu 修正 double free 为 arbitrary free 亦体现对同行纠错的开放态度。

能力与结果：形成以公开研究为知识资产、按当前环境做针对性改造与补丁绕过的跨版本迁移能力，而非将历史研究视作一次性参考。；2019-08-07《Attacking Unmarshallers》JNDI via getter 明确继 Doyensec jackson gadgets 工作展开；2018-12-03 WebExec Reloaded 接续 Ron Bowes 原 WebExec 并做 CVE-2018-15442 补丁绕过；2020-08-19 Horde 复用并改造 EgiX 于 CVE-2014-1691 的旧 POP 链以适配 PHP 7+

置信度：high；替代解释：同行公开研究作为起点是 Web 安全研究社区的常见实践，并非该研究员特有；三例的同行来源（EgiX、Doyensec、Ron Bowes）分散于不同技术子领域，跨版本迭代作为统一方法的归纳属推断，缺乏其本人对方法统一性的一手自述。

证据：ss-deep-03, r1-ss-pub-011-doyensec, r1-ss-webexec-ronbowes, ss-community-005

### 以可识别技能缺口为依据的真实目标领域迁移

起点：2017-09-06《Sharks in the Pool》自述长期研究 Web 相关漏洞、用户态利用较为熟练但常遇未针对的内核设备驱动，因知识缺口未下手，遂决定补齐 ring 0 能力，并选择真实应用漏洞而非练习驱动 HEVD 为学习载体。

练习与反馈：以可识别的技能缺口作为方向迁移依据并选定真实目标：2017 年由用户态迁移至 Windows 内核池；2021-01-12 加入奇虎 360 Vulcan Team（360 Vulcan Team 归属仅由本人博客自述，未获独立确证）后因 .NET 理解有限而选定微软云网络，以既有的 Web 安全能力作为切入新方向的依托。；真实应用漏洞作为练习载体，其可达性与利用稳定性提供对能力补齐进展的反馈；2020-08-19 Horde 审计中因过度依赖白盒而漏掉 Horde_Core_Block 子类攻击面，由 Andrea Cardaci 以偏黑盒/GUI 交互的风格补上，反馈为复杂应用需白盒与黑盒并重的方法论修正。

能力与结果：形成以技能缺口定位方向、以真实目标为练习载体、以方法论修正收尾的方向迁移能力，并据此从桌面文档、Web 反序列化、内核池逐步迁移至云与企业网络管理产品。；2017-09-06《Sharks in the Pool》由用户态迁移至 Windows 内核池并选用真实应用漏洞；2021-01-12《Making Clouds Rain》因 .NET 知识有限选定微软云网络；2020-08-19 Horde 审计因白盒盲区漏报并据此修正为白盒与黑盒并重

置信度：high；替代解释：技能缺口作为迁移依据的表述来自其本人自述，外部观察到的仅是产出方向的客观变化；方向迁移亦可能由厂商 bounty 金额、ZDI 协调渠道可达性、组织研究方向分配等外部条件驱动，.NET 方向的选定与 360 Vulcan Team 的研究方向自由度之间的因果为自述而非独立证实。

证据：dec-01, dec-02, ss-deep-01, ss-deep-02

### 白盒与黑盒并重的审计方法

起点：2019-05-17《Panic! at the Cisco》以 web.xml servlet 映射追溯数据流的静态代码审计结合补丁 diffing 发现漏洞；2020-08-19 Horde Groupware 审计中因过度依赖白盒而漏掉 Horde_Core_Block 子类攻击面。

练习与反馈：同时执行白盒与黑盒两条审计路径以覆盖单一路径的遗漏：白盒从配置文件与代码模式追溯数据流，黑盒以 GUI 交互与运行时行为观察（如 Process Monitor 观察 Tomcat 加载 application.xml）覆盖静态分析盲区。；Andrea Cardaci 以偏黑盒/GUI 交互的风格补上 Horde_Core_Block 子类缺口，反馈为 Complex applications need both a white-box review and a black-box review 的方法论修正；该方法论修正由作者本人发起并叙述，未获对方独立确认。

能力与结果：形成对复杂应用同时执行白盒与黑盒两条审计路径的稳定方法，以单一路径的遗漏作为另一路径的输入。；2020-08-19 Horde 审计以白盒黑盒风格差异对照识别自身盲区；2024-11-25 Spring Properties 以 Process Monitor 观察 Tomcat 加载 application.xml 定位配置加载顺序；2019-05-17 Cisco Prime 以 web.xml servlet 映射静态审计结合补丁 diffing

置信度：medium；替代解释：白盒与黑盒并重为业界通用方法论，且该方法论修正的主要来源为 2020 年 Horde 单一案例，并由其本人发起叙述、未获 Andrea Cardaci 独立确认；将其升格为独立机制的依据相对单薄，存在以一般化方法充当个人特有机制的风险。

证据：ss-deep-02, ss-community-006, ss-pub-005, ss-pub-009

### 教学输出—学员带回目标—协作合著的反馈流程

起点：2021-07-13 Full Stack Web Attack 训练课产品化，并在挑战题中植入隐藏 0day 检验学员发现能力，以公开 writeup 完成从教学到披露的流程；课程页面将方法学表述为覆盖漏洞发现与利用开发完整阶段、使用补丁 diffing 复现 n-day，并以 Leave your OWASP Top Ten and CSP bypasses at the door 划定方向。

练习与反馈：以训练课为入口，过往学员在多年后将新目标带回，并以合著形式完成发布：2022-10-25 VMware NSX Manager 预认证 RCE 由 Full Stack Web Attack 过往学员 Sina Kheirkhah 主笔、与 Steven Seeley 合著；2024-11-25 Spring Properties 的初始漏洞由一名前学员带回。；学员带回的目标作为新的研究线索输入，扩展研究覆盖面；作者在 Spring Properties 中公开复盘方法选择的妥协与未走通方向（JDBC、un-marshaller 直接滥用），并将该流程显性化为可被他人继续的公开记录。

能力与结果：形成由教学输出驱动学员成长、再由学员带回目标形成长期带教协作关系的流程，使教学成为研究线索与合著者的稳定入口。；2022-10-25 VMware NSX Manager 预认证 RCE 由过往学员 Sina Kheirkhah 主笔并合著（以 ss-community-003 documented 为主锚点）；2024-11-25 Spring Properties 初始漏洞由前学员带回（以 ss-pub-009 documented 为主锚点）；2021-07-13 FSWA 挑战题植入隐藏 0day 检验学员发现能力并以公开 writeup 完成披露

置信度：medium；替代解释：学员带回目标与合著关系均由其本人博客单向叙述，未获 Sina Kheirkhah 及 Spring 前学员的独立渠道证实；学员产出可发布漏洞研究是否可归因于该课程内容本身亦未被独立证实，故该流程作为个人特有机制的依据存在自述来源偏差，不宜以 distinctive 归因。

证据：ss-pub-007, ss-deep-05, ss-community-003, ext-student-04, ss-pub-009

## 可迁移与不可迁移

- 可迁移：对补丁做 diffing 并追问补丁是否覆盖完整攻击面，以识别未修补变体并据此构造跨组件多原语链（参见 Cisco 单 CVE 双漏洞、Samsung FTP 变体）。
- 可迁移：以可识别的技能缺口作为方向迁移依据，并选用真实应用漏洞而非通用靶机作为练习载体，使能力补齐与可发布产出同向累积。
- 可迁移：同时执行白盒与黑盒两条审计路径，以单一路径的遗漏作为另一路径的输入，覆盖复杂应用中纯静态分析的盲区。
- 可迁移：将披露伦理固化为可重复的固定规则（如递减时间线、无差别适用），并通过公开复盘厂商补丁质量与披露行为校准后续披露策略。
- 可迁移：以公开研究为起点做跨版本迭代适配，对同行既有成果的接口/类演进与补丁做针对性改造或绕过，而非视作一次性参考。
- 不可直接迁移：Full Stack Web Attack 训练课作为学员网络的入口为该研究员个人产品，学员带回目标并合著的反馈流程依赖其长期教学积累与个人信誉，他人难以直接复制；且该流程中合著/学员关系未获合著方独立渠道证实，仅作自述来源保留。
- 不可直接迁移：360 Vulcan Team 归属与由此获得的研究方向选择权为组织条件，仅由本人博客自述、未获独立确证，且 Pwn2Own 参赛队名为 Team Incite / Source Incite 而非 360 Vulcan，组织归属与个人能力之间的因果不可直接迁移。
- 不可直接迁移：Pwn2Own Miami 2020 与 Vancouver 2021 的参赛资格与目标选定受赛事邀请、组队关系与时间窗口等外部条件制约，竞赛反馈作为能力验证的机制不可在无赛事环境下复制；具体名次、奖金与官方 Master of Pwn 归属未由官方页面证实。
- 不可直接迁移：srcincite.io 个人博客与 sourceincite GitHub 组织作为长期公开输出与代码发布渠道，构成其可被同行追溯引用的可见性基础，该渠道的十年积累与命名一致性不可由后来者短期复制。
- 不可直接迁移：北美与中美约十年工作经历及其对应雇主未在一手来源中给出，该跨国经验作为企业软件漏洞挖掘方法论基础的地理/职业条件无法独立核验亦不可直接迁移。

## 复核问题

- stages 阶段 4 capability_change 将 2021-08-25 表述为「参加 Pwn2Own Vancouver 2021」的日期，与证据矛盾：evidence 中 timeline-2021-04-pwn2own-vancouver-source-incite 写明该届赛事举办日期为 2021 年 4 月 6-8 日，2021-08-25 仅为竞赛 writeup 的发布日期（timeline-2021-exchange-sharepoint-pwn2own-writeup）。综合错把 writeup 发布日期当作参赛日期，导致赛事时间线与 writeup 发布时间线在该句混淆。该错误不改变参赛事实、队名 Source Incite 与目标 Microsoft Exchange Server 的成立，故不构成关键事实错误，但需修正措辞以保持时间线一致。
- 修正 stages 阶段 4 capability_change 中 Pwn2Own Vancouver 2021 的参赛日期措辞：将「2021-08-25 以 Source Incite 队名参加 Pwn2Own Vancouver 2021」改为区分参赛日期与 writeup 发布日期的表述，例如「2021 年 4 月以 Source Incite 队名参加 Pwn2Own Vancouver 2021（赛事举办于 4 月 6-8 日），并于 2021-08-25 发布 writeup」，与 timeline-2021-04-pwn2own-vancouver-source-incite 与 timeline-2021-exchange-sharepoint-pwn2own-writeup 两项证据一致。
- 在 stages 阶段 3 evidence_ids 中对 ss-pub-006（unknown/lead_only/verified_in_run=false）就近标注证据等级，与 ss-pub-008、ss-community-004 的 RR6 降级处理保持一致：明确 Team Incite 参赛事实以 timeline-2020-01-pwn2own-miami-team-incite（reported、Wikipedia 二手）与 ss-deep-06（documented）为主锚点，ss-pub-006 仅作辅证，避免与 documented 项等量齐观。
- 在 stages 阶段 6 evidence_ids 或 capability_change 中对 ext-github-08（inferred）就近标注其推断性质：GitHub 组织页未直接署名 Steven Seeley 或 mr_me，身份关联依赖博客 Mastodon 链与仓库命名一致性推断，仅作侧面辅证，不宜作为该阶段独立支撑。

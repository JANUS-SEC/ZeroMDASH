# Pan Zhenpeng：漏洞研究成长分析

- 擅长领域：Apple 内核与移动端漏洞
- 独立复核：pass · 81/100

## 成长阶段

- **2016–2019-06 · CTF/pwn 基础训练与公开 writeup 输出起步**：2016 年起在中南民族大学(SCUEC)攻读计算机科学学士学位，并在校期间加入武汉 SCUEC Newthread Geek Group，从事 iOS/Python/Linux/CTF/ACM 活动，研究起点为 CTF 与 pwn；2019-06 在个人博客发布 Pwnable.tm 题解类 writeup，同年并行发布 iOS 12.2 越狱漏洞分析与 Chrome/V8 引擎分析文章。形成以博客公开复盘 CTF 与利用练习的习惯，输出早于进入商业安全实验室。该阶段组织平台为高校安全社团与个人博客，证据以本人 GitHub README 与博客列表为据，自述未由学校或社团第三方独立证实。（置信度：medium）
  - 证据：pz-tl-01-education, pan-dec-01, pz-community-008, PZ-WORK-03
- **2018-07–2020-06 · macOS/XNU 单点漏洞研究与代码审计方法确立**：2018-07 至 2019-10 在奇虎 360 Nirvan Team(北京)任 macOS Security Researcher 实习，首次将研究目标固定在 macOS/XNU；以 CVE-2019-8540(IOKit exportObjectToClient 中 io_object_t 8 字节强转 mach_port_name_t 4 字节致高 4 字节未初始化、泄露内核栈内存)writeup 为标志，从单点 PoC 演进为带根因分析的 writeup，并标注影响版本范围。同期在 GitHub 公开 PegasusZero(macOS 10.11.x exploit)与 L1br4(macOS 10.13 exploit)等可复用仓库，体现把跨版本 exploit 工程化的倾向。2020-02 在 macOS 10.15.2 EndpointSecurity.kext newUserClient 中发现逻辑缺陷(type 非 0/1 时返回 KERN_SUCCESS 但不创建 client，致空指针解引用 panic)，先向 Apple 报告，被 Apple 产品安全团队判定非安全问题后选择自行公开披露并附 PoC。方法以内核扩展代码审计为主。各仓库精确发布日期未抓取到，仅以年份或 YYYY 标注。（置信度：high）
  - 证据：pz-tl-02-internship-qihoo, pan-dec-02, pan-dec-03, pz-community-002, PZ-WORK-02, PZ-WORK-06, PZ-WORK-07, pz-tl-09-repos-macos-exploit
- **2020-07–2022-06 · Apple 驱动分层方法与首场国际会议演讲**：2020-07 至 2022-06 在阿里巴巴安全 Pandora Lab(杭州)任 Senior Security Engineer(2021 年晋升 P6，据本人 README 自述，无阿里官方或第三方来源佐证)。在 Zer0Con 发表 Three Layers in Apple Driver Bug Hunting: Pwn macOS Big Sur in One Shot(Zer0Con 演讲年份存在冲突——zer0con.org/archive/2021.html 页面品牌标记为 Zer0Con2021，但 schedule 段标 Zer0Con2022 并列 April 8–9 2022，Pan 被排定于 2022-04-08；OffensiveCon 2023 bio 亦以 Zer0Con2021 品牌名指代；确切年份未完全确定，但落在阿里期内 2020-07–2022-06)，为其可考的首场国际会议演讲，主题为 Apple 驱动漏洞挖掘的三层方法与 macOS Big Sur 一次性利用。方法学显式命名(三层)，标志从单点审计向方法提炼的过渡。演讲事实由本人 README 与 zer0con 归档页佐证，但 POC 官方议程页未抓取到。（置信度：medium）
  - 证据：pan-dec-04, pz-tl-04-alibaba-pandora, pz-tl-05-zer0con-talk, pan-conv-06, PZ-R1-003
- **2022-07–2023 · 自研 Apple 生态 fuzzer 版本化迭代与会议公开**：2022-07 加入新加坡 STAR Labs SG 任 Mobile Security Researcher(后由团队页列为 Principal Vulnerability Researcher，定级升迁路径无法完整确定)。在 POC 2022(首尔)发表 The Journey To Hybrid Apple Driver Fuzzing，将方法从代码审计转向混合 fuzzing(coverage-guided 与 generational 结合)；2023-05 在 OffensiveCon 2023(柏林)发表 Unearthing Vulnerabilities in the Apple Ecosystem: The Art of KidFuzzerV2.0，将自研 fuzzer 迭代到 V2.0 并命名。据 OffensiveCon 2023 演讲摘要自述，发现 50 余个 XNU 内核/Apple 驱动/协处理器固件漏洞并将驱动攻击面扩展约 95%(short_quote: 'an innovative Driver collection method that could expand driver attack surfaces by 95%')；其中 CVE-2023-28187 与 CVE-2023-28185 报告人由 Apple HT213676 一手公告独立证实为 Pan ZhenPeng (@Peterpan0927) of STAR Labs SG Pte. Ltd.，但 50 余总量与 95% 扩展为讲者自述，未由独立 CVE 清单逐条核验。同期连续在 Zer0Con、POC、OffensiveCon 发表 Apple 主题演讲(累计达 7 场中的前 4 场；7 场演讲含 STAR Labs 雇主平台与演讲文化提供的输出渠道，演讲数受组织平台放大，不能直接等价于个人能力提升)。研究方向与方法学经 pan-conv-05 的会议讲者简介与本人 GitHub 自述交叉印证。（置信度：high）
  - 证据：pan-dec-05, pan-dec-06, pan-dec-07, pz-tl-06-poc-2022-talk, pz-tl-07-star-labs-sg, pz-tl-08-offensivecon-2023-talk, pan-conv-01, pan-conv-05, pz-community-003, pz-community-004, PZ-R1-001, PZ-R1-002
- **2024 · 研究焦点转向 Android/Qualcomm GPU 利用**：2024 年研究焦点首次由 Apple 内核转向 Android GPU 攻击面：在 OB1(Off-By-One) 2024 发表 GPUAF: Using a General GPU Exploit Technique to Attack Pixel 8，并在同年 POC 2024 发表 GPUAF: Two Ways of Rooting All Qualcomm-based Android Phones，将同一 GPUAF 技术跨两个会议重复输出。研究焦点由 Apple 内核/驱动 fuzzing 迁移到 Qualcomm/Android GPU 利用，方法学从漏洞发现工具建设转向通用利用技术开发。person_json 标注的 OffByOne 2024 对应 OB1 2024 条目；Black Hat 一项未在任何一手或第一方来源中出现，疑为输入信息漂移，未采信。方向转移的具体决策动因无公开陈述，只能由演讲题目序列推断。（置信度：medium）
  - 证据：pan-dec-08, pz-community-005
- **2025 · 转向 DSP 协处理器利用与 MTE 等防御机制绕过**：2025 年研究目标进一步扩展至移动 DSP 协处理器与 Samsung Exynos，并引入 AI 辅助 exploit 开发：HITCON 2025 发表 Cracking the Pixel 8: Exploiting the Undocumented DSP to Bypass MTE；CODE BLUE 2025 发表 AI Accelerated Exploiting(用 AI 加速针对 MTE 加固 Pixel 的 exploit 开发，经 DSP 协处理器)与 Dancing with Exynos Coprocessor(Samsung)。约束可重建为 MTE 等内存防护使传统利用成本上升，推动寻找新攻击面与辅助手段。单年 3 场、累计 7 场演讲(7 场演讲含 STAR Labs 雇主平台与演讲文化提供的输出渠道，演讲数受组织平台放大，不能直接等价于个人能力提升)。CODE BLUE 2025 与 HITCON 2025 多篇与 Billy Jheng Bing-Jhong 合著，反映稳定协作，但合作起始时间与分工无公开材料说明。（置信度：medium）
  - 证据：pan-dec-09, pz-community-006

## 主要成长机制

### 自研 fuzzing 工具的版本化迭代与会议公开

起点：2020-07 前以 macOS 内核扩展代码审计为主，已具备 XNU/IOKit 与跨版本 exploit 仓库(PegasusZero/L1br4)的基础；Apple 驱动攻击面大、手工审计效率受限构成方法转型的约束条件。2020-07 进入阿里 Pandora Lab 后获得以厂商实验室身份对外演讲的渠道。

练习与反馈：把自研 fuzzing 方法整理为可命名、可对外交付的议题，并跨年度版本化迭代：POC 2022 的 hybrid Apple driver fuzzing 框架 → OffensiveCon 2023 的 KidFuzzerV2.0(POC2022 KidFuzzer 的第二代)→ 2024 年 GPUAF → 2025 年 DSP/MTE 绕过方法。每次以工具/方法命名 + 会议演讲作为一次完整输出周期，主题随工具版本推进而演进。；会议演讲作为同行审视与声誉积累节点构成反馈来源；STAR Labs 雇主平台与演讲文化持续提供输出渠道，组织放大效应使演讲数不能直接等价于个人能力提升。持续改进/迭代工具，并把研究对象(如 XNU 源码、历史 exploit)固化为 GitHub 仓库供社区复用，而非封闭笔记。

能力与结果：形成把内部 fuzzing 方法论抽象为可对外交付的技术叙事，并以工具命名与版本号标记迭代节点的工作习惯；同一主题(KidFuzzer → KidFuzzerV2.0)跨年演进显示以工具为载体的持续产出，而非一次性披露。；POC 2022 The Journey To Hybrid Apple Driver Fuzzing：方法从代码审计转向混合 fuzzing(pan-dec-05, pz-tl-06-poc-2022-talk)；OffensiveCon 2023 KidFuzzerV2.0：自研 fuzzer 迭代到 V2.0 并公开，据讲者摘要自述发现 50 余个漏洞、扩展约 95% 驱动攻击面，其中 CVE-2023-28187/28185 报告人由 Apple HT213676 一手公告独立证实(pan-dec-06, pz-tl-08-offensivecon-2023-talk, pan-conv-01, PZ-R1-001, PZ-R1-002)；2024 GPUAF 跨 OB1 与 POC 双会议重复输出，方法学从漏洞发现工具转向通用利用技术(pan-dec-08, pz-community-005)；2025 DSP/MTE 绕过方法单年 3 场会议输出，引入 AI 辅助 exploit 开发(pan-dec-09, pz-community-006)

置信度：high；替代解释：会议演讲的高频产出部分依赖 STAR Labs 雇主平台与演讲文化提供的渠道，组织放大效应使其不能完全归因为个人方法能力增长；KidFuzzerV2.0 框架源码或技术细节未见公开仓库(KidFuzzerV2 仓库抓取返回 404)，方法迭代的技术内容仅能依赖演讲标题与摘要自述，无法核对实现与漏洞产出。

证据：pan-dec-05, pan-dec-06, pan-dec-08, pan-dec-09, pz-tl-06-poc-2022-talk, pz-tl-08-offensivecon-2023-talk, pan-conv-01, pan-conv-05, pz-community-003, pz-community-004, pz-community-005, pz-community-006, PZ-R1-001, PZ-R1-002

### 厂商反馈回路驱动下的披露决策与公开输出

起点：2019-07 起即在个人博客公开 iOS 12.2 越狱分析与 macOS local DoS 分析，具备以 writeup 向社区输出的先在习惯；2020-02 完成内核扩展代码审计发现 EndpointSecurity.kext 空指针解引用，先按厂商流程向 Apple 报告。

练习与反馈：在'被厂商拒绝'的负反馈后，独立论证问题价值并公开披露：2020-02 出现一次先按厂商流程报告、被 Apple 否定后转为公开披露的事件(据本人博客单方陈述，'the Apple product security team does not regard it as a security problem, so i just release it'；Apple 安全团队的具体回复原文未二次取证，'厂商不视为安全问题'目前仅来自作者博客单方陈述)。同期博客维持 iOS 12.2 越狱分析、Chrome/V8 等多方向 writeup 的持续公开输出。；厂商判定边界对作者构成对峙式反馈：Apple 否定安全定性后，作者需独立论证问题价值并公开 PoC，而非依赖厂商背书。博客 writeup 写作倒逼把逆向/利用过程结构化，并在 CTF 平台(Pwnable.tm)上进行可被同行核验的重复练习。

能力与结果：可计数成果(据本人 About 页自述：30 余个 Apple CVE、参与 Pwn2Own Web 类并达成目标、持有 OSCP 证书；其中 CVE-2023-28187 与 CVE-2023-28185 报告人由 Apple HT213676 一手公告独立证实为 Pan ZhenPeng (@Peterpan0927) of STAR Labs SG Pte. Ltd.，30+ 总量为自述未逐条核验；Pwn2Own 个人参与为自述无年份/队友/结果，STAR Labs 组织级 Pwn2Own Master of Pwn(含 2025 Berlin)由具名团队成员取得，不归因 Pan 个人)。2020-02 出现一次先按厂商流程报告、被 Apple 否定后转为公开披露的事件；是否构成稳定工作模式因样本单一未能在本综合中确立。；2020-02 local DOS on latest macOS 博客：先报告 Apple 被拒后公开 PoC，附内核扩展代码审计根因(pan-dec-03, pz-community-002, PZ-WORK-06)；Apple HT213676 一手公告证实 CVE-2023-28187/28185 报告人为 Pan ZhenPeng of STAR Labs SG Pte. Ltd.(PZ-R1-002)；2019-07 起博客持续公开 iOS 12.2 越狱分析、Chrome/V8 引擎分析、macOS DoS 分析等多方向 writeup(PZ-WORK-04, PZ-WORK-05, PZ-WORK-06)

置信度：low；替代解释：单次交互(2020-02 Apple 否定后公开)不足以证明稳定反馈机制；公开披露亦可能是个人输出习惯的延伸而非厂商反馈回路的产物。30+ Apple CVE 与 Pwn2Own 均为本人自述计数，PZ-R1-002 仅独立证实其中 2 个 CVE 报告人身份，其余未逐条核验；STAR Labs 组织级 Pwn2Own 成绩具名团队成员均非 Pan，个人 Pwn2Own 参与未能独立证实。

证据：pan-dec-03, pz-community-002, PZ-WORK-04, PZ-WORK-05, PZ-WORK-06, pan-conv-04, PZ-R1-002, PZ-R1-004, PZ-R1-005

### 跨平台/跨设备的方法迁移与攻击面扩展

起点：2018-07 进入奇虎 360 后研究目标固定在 macOS/XNU；OffensiveCon 2023 摘要自述从公开与未公开 Apple N-day 漏洞中提取抽象模式、跨 iPhone/SRD/M1/Intel 设备复用，已具备跨设备复用的方法前提。2022-07 加入 STAR Labs 后获得移动安全团队的同伴网络(Billy Jheng、Bruce Chen、Meysam Firouzi 等)，研究范围由单平台扩展到国际会议体系下的多平台移动安全。

练习与反馈：把同一方法/技术在跨平台、跨设备、跨会议间重复迁移输出：Apple 多设备(iPhone/SRD/M1/Intel)→ Qualcomm/Android GPU(GPUAF)→ Samsung Exynos DSP；同一 GPUAF 成果在 OB1 2024 与 POC 2024 双会议重复输出以收集不同社区反馈；2025 年同一 DSP/MTE 绕过主题在 HITCON 2025 与 CODE BLUE 2025 多场重复。；同伴网络作为反馈回路：加入国际化研究团队后获得同行(跨越越南/新加坡/印尼/澳洲背景的研究员)的直接审视与协作环境；职位从 Researcher 晋升 Principal 与同期演讲数增长(7 场)时间线一致，提示团队反馈与职位晋升的耦合，而非孤立个人突破。多会议重复输出策略用于收集不同社区反馈。

能力与结果：形成从单平台漏洞发现中提取可迁移模式、再跨平台/跨设备复用的方法抽象能力；研究焦点随防御机制演进(MTE 使传统利用成本上升)向更底层协处理器(DSP/Exynos)与新辅助手段(AI 加速 exploit 开发)扩展，而非停留在单点发现。；OffensiveCon 2023 KidFuzzerV2.0 自述跨 iPhone/SRD/M1/Intel 设备复用 N-day 模式(pan-conv-01, PZ-R1-001)；2024 GPUAF 跨 OB1 与 POC 双会议，研究焦点从 Apple 转向 Qualcomm/Android GPU(pan-dec-08, pz-community-005)；2025 DSP/MTE 绕过跨 HITCON 与 CODE BLUE 多场，目标扩展到 Samsung Exynos 并引入 AI 辅助开发(pan-dec-09, pz-community-006)；STAR Labs 移动安全团队同伴网络与职位晋升耦合(pz-community-007)

置信度：medium；替代解释：跨平台迁移可能是职业轨道与同伴网络(STAR Labs 移动安全团队)牵引的结果，而非纯个人方法能力驱动；Apple→GPU→DSP 的方向转移具体决策动因无公开陈述，只能由演讲题目序列推断。STAR Labs 团队内部协作机制(code review、内部技术分享、联合研究)未公开，同伴网络对其能力影响的机制层面只能 inferred 而非 documented。

证据：pan-conv-01, pan-dec-08, pan-dec-09, pz-community-005, pz-community-006, pz-community-007, PZ-R1-001

## 可迁移与不可迁移

- 可迁移：以方法命名与工具版本号作为可复用资产积累：把自研 fuzzing 方法整理为可命名、可对外交付的议题(hybrid fuzzing → KidFuzzerV2.0)，并以工具命名 + 版本号标记迭代节点，便于跨年延续与同行检视。
- 可迁移：把研究对象与历史 exploit 固化为 GitHub 仓库供社区复用(PegasusZero/L1br4/darwin-xnu/MOXil_learning)，以公开仓库替代封闭笔记，形成可被同行检视的学习材料。
- 可迁移：被厂商拒绝后独立论证问题价值并公开 PoC，以 writeup 写作倒逼把逆向/利用过程结构化。
- 可迁移：把同一成果跨多个会议重复输出以收集不同社区反馈(GPUAF 跨 OB1 与 POC；DSP/MTE 跨 HITCON 与 CODE BLUE)。
- 可迁移：从单平台漏洞中发现可迁移模式并跨设备复用(Apple 多设备 → Qualcomm GPU → Samsung Exynos DSP)，随防御机制演进调整攻击面。
- 不可直接迁移：STAR Labs 雇主平台与演讲文化提供的国际会议输出渠道：7 场演讲累计受组织平台放大，不能直接等价于个人能力提升，该渠道非个人可复现条件。
- 不可直接迁移：STAR Labs 移动安全团队的同伴网络(Billy Jheng、Bruce Chen、Meysam Firouzi 等国际化研究员)与职位晋升耦合，团队内部协作机制未公开，同伴反馈为组织资源而非个人可迁移做法。
- 不可直接迁移：阿里 Pandora Lab 与奇虎 360 Nirvan 的厂商实验室身份及对应地域迁移(武汉→北京→杭州→新加坡)：厂商实验室身份使其能以组织名义对外演讲，非个人独立可获条件。
- 不可直接迁移：研究方向从 Apple 向 Android GPU/DSP 的转移部分受职业轨道与团队牵引，而非纯个人方法能力驱动；方向转移决策动因无公开陈述。
- 不可直接迁移：Apple 厂商反馈(否定安全定性)的具体回复为外部条件，非个人可控；'被拒后公开'的披露决策依赖厂商判定结果这一偶然外部事件。

## 复核问题

- 未发现关键事实/身份/来源错误。GitHub handle Peterpan0927 与 Pan Zhenpeng 的同一性经多源交叉确认（GitHub README、个人博客、STAR Labs 团队页、OffensiveCon 2023 speaker 页、Apple HT213676 credits），引用的 evidence_ids 均为 verified_in_run=true 的有效证据，PZ-R1-001~005 属 six_dimensions.targeted.items 中的有效证据而非仅修订历史。
- tensions 字段增列 X/Twitter handle 矛盾并整合化解：person_json.json 的 social 字段为 https://x.com/Peterpan0927，GitHub README 列出的 handle 为 @peterpan980927，二者不一致（evidence 的 community/decisions/timeline 三处 contradictions 已记录）。综合结论 tensions 当前 7 条未单列此矛盾。建议增列一条，并引用 PZ-R1-002（Apple HT213676 credits 明确写作『Pan ZhenPeng (@Peterpan0927) of STAR Labs SG Pte. Ltd.』）以一手公告证实 @Peterpan0927 为有效 handle，化解该矛盾而非仅留作未解决张力。
- stages 第2段（2018-07–2020-06）capability_change 补注 2020-02 雇主空档：当前段落开头述『2018-07 至 2019-10 在奇虎 360 Nirvan Team(北京)任 macOS Security Researcher 实习』，随后述『2020-02 在 macOS 10.15.2 EndpointSecurity.kext newUserClient 中发现逻辑缺陷』。pan-dec-02 与 pan-dec-04 显示 360 实习至 2019-10 结束、阿里入职为 2020-07，故 2020-02 处于二者空档期。建议在 2020-02 处就近补注『（2020-02 处于奇虎 360 实习结束 2019-10 与阿里 Pandora Lab 入职 2020-07 之间，非任一雇主在职期间产出）』，避免读者将 2020-02 macOS DoS 误归为 360 实习期或阿里在职期作品。
- stages 第6段（2025）或 tensions/open_questions 标注 2025 演讲独立佐证缺口：pan-dec-09 与 pz-community-006 的核心来源均为 STAR Labs 雇主 publications 页与团队页（starlabs.sg/publications/、starlabs.sg/team/pan-zhenpeng/），未抓取到 HITCON 2025 与 CODE BLUE 2025 的独立会议官网议程佐证。综合结论 tensions 已标注 POC 2022 官网议程页未抓取（pz-tl-06 lead_only），但未对 2025 演讲标注同等独立佐证缺口。建议在 stages 第6段或 tensions 增列『2025 HITCON/CODE BLUE 演讲仅由 STAR Labs 雇主 publications 页佐证，缺独立会议官网议程佐证』，与 POC 2022 的处理保持一致。
- mechanism 2（厂商反馈回路驱动下的披露决策与公开输出）repeated_practice 字段显式区分 repeated 的适用范围：当前 repeated_practice 将『2020-02 单次厂商反馈事件』与『博客持续 writeup 输出』并列叙述，validation_tests 标记 repeated。但 intermediate_capability 已明确厂商反馈为单次事件、alternative_explanation 已说明单次不足以证明稳定机制。建议在 repeated_practice 中明确『repeated 的对象为博客持续 writeup 公开输出（2019-07 起持续），而非厂商反馈回路本身（厂商反馈仅 2020-02 单次）』，使 validation_tests 的 repeated 标注与 intermediate_capability/alternative_explanation 的单次限定在字段层面一致，消除机制内叙述张力。

# Pietro Borrello：漏洞研究成长分析

- 擅长领域：微码/硬件/系统漏洞
- 独立复核：pass · 88/100

## 成长阶段

- **2017–2019 · 本科至硕士早期 ROP 工具研究起点**：在 Sapienza University of Rome 连续完成本科（2017）与硕士（2019）学位，研究方向确定为系统安全；以 ROP 利用辅助工具切入安全研究，与 Sapienza 程序分析方向的 Coppa、D'Elia、Demetrescu 合著 RopMate（IEEE VizSec 2018）与 The ROP needle（ACM SAC 2019），形成研究与可复现工具并行的产出习惯。CyberChallenge.IT 第 7 届（2016/2017）参与为可核验的早期同伴训练环境。（置信度：high）
  - 证据：pb-tl-01, pb-tl-02, pb-tl-03, pb-tl-04, pb-works-ropmate-2018, pb-decisions-01, pb-decisions-08
- **2020–2021 · 微架构侧信道防御与 ROP 混淆延伸**：研究焦点从 ROP 利用转向微架构侧信道防御与程序混淆。2020-01 在 DEFCON Group Rome 发表基于 Brandon Falk 工作的 CPU 微架构数据采样演讲，首次可核验的微架构主题公开输出；2021 发表 Constantine（ACM CCS，基于编译器的控制/数据流线性化，开源 constantine 仓库）与 Hiding in the Particles（ACM DSN，开源 raindrop 仓库）。Constantine 引入跨机构合作者 Querzoni 与 Giuffrida（具体机构归属未由一手页面标注），合作网络跨出 Sapienza。注：raindrop 配套论文经 GitHub README 核实为 DSN 2021 Hiding in the Particles，不属 2019 ACM SAC The ROP needle。（置信度：high）
  - 证据：pb-tl-05, pb-tl-06, pb-tl-07, pb-works-constantine-2021, pb-community-001, pb-conv-02, pb-r2-01, pb-r2-03
- **2022 · 微架构漏洞研究与 CPU 微码逆向的同期展开**：同年发表两项独立底层漏洞研究：ÆPIC Leak（USENIX Security 2022 第一作者，CVE-2022-21233，Intel 近代 CPU APIC MMIO 未定义区间返回缓存陈旧数据，可泄漏 SGX enclave 内容；与 TU Graz 的 Kogler/Schwarzl/Gruss、AWS 的 Lipp、CISPA 的 Michael Schwarz 合著）与 Custom Processing Unit（Black Hat USA 2022，CPU 微码追踪与修补）。研究从微架构侧信道防御延伸到架构与微码层。注：Black Hat USA 2022 与 WOOT 2023 官方议程页抓取返回 403/404，演讲事实与首个 CPU 微码动态分析框架定位仅依赖个人站自述。IAIK 子机构归属由 TU Graz isec 官网（前 IAIK，2025-01-01 更名 ISEC）一手核验 Schwarzl/Gruss 成员身份与 Æpic Leak 发布；aepicleak.com 与 USENIX 2022 一手页显示文本仅写 Graz University of Technology，Kogler 的 IAIK 归属仍仅由 USENIX 页与 IAIK/AEPIC 仓库二次印证。（置信度：medium）
  - 证据：pb-tl-08, pb-tl-09, pb-tl-10, pb-tl-11, pb-works-aepic-leak-2022, pb-works-cpu-microcode-2022-2023, pb-decisions-03, pb-community-005, pb-r2-02, pb-r4-01, pb-r4-02
- **2023 · 内核子系统漏洞批量发现与博士学位完成**：在 Sapienza 取得博士学位，自述方向为将模糊测试与程序分析用于架构与微架构漏洞。同年发表 CustomProcessingUnit（WOOT 2023，开源 CustomProcessingUnit 与 ghidra-atom-microcode）与 Uncontained（USENIX Security 2023，与 Vrije Universiteit Amsterdam 的 Koschel/Bos/Giuffrida 与 Sapienza 的 D'Elia 合著，机构由 USENIX 2023 一手页印证），并在 Linux 内核多个子系统（HID、RDS、TUN/TAP、TLS、SCTP、Realtime Scheduler）报告一批 type confusion 与 use-after-free 类 CVE。研究对象由 CPU 微码扩展至 Linux 内核子系统。注：WOOT 2023 一手论文页返回 404，CustomProcessingUnit 发表事实与首个 CPU 微码动态分析框架定位仅依赖个人站自述。（置信度：medium）
  - 证据：pb-tl-12, pb-tl-13, pb-tl-16, pb-works-kernel-cves-2023, pb-works-uncontained-memory-2023, pb-decisions-05, pb-decisions-06, pb-r3-02
- **2024– · 模糊测试方法研究与产业迁移**：发表 Predictive Context-sensitive Fuzzing（NDSS 2024，与 EURECOM 的 Andrea Fioraldi、Davide Balzarotti，Sapienza 的 D'Elia、Querzoni，Vrije Universiteit Amsterdam 的 Giuffrida 合著；机构由 NDSS 2024 一手页印证，开源 predictive-cs-fuzzing 仓库），恢复对模糊测试方法的研究。同年起任 Apple SEAR Microarchitecture Security Researcher，将博士期微架构/微码研究能力迁移到企业安全岗位；入职日期未公开，产业迁移与 NDSS 2024 工作的时间关系无法判定。（置信度：medium）
  - 证据：pb-tl-17, pb-tl-18, pb-works-predictive-cs-fuzzing-2024, pb-decisions-07, pb-r3-01

## 主要成长机制

### 研究工件公开化与可复现工具发布

起点：2018 年首篇论文 RopMate 即配套公开 GitHub 仓库，处于 Sapienza 程序分析团队的指导网络中；同期参与 CyberChallenge.IT 训练与 CTF（mhackeroni、TRX 队，成员身份仅个人页自述，未独立证实）。

练习与反馈：贯穿 2018–2024，每条主要研究线索均配套公开仓库：RopMate（2018）、raindrop（2021，配套 DSN 2021 Hiding in the Particles）、constantine（2021）、CustomProcessingUnit 与 ghidra-atom-microcode（2022–2023）、predictive-cs-fuzzing（2024）。个人页系统列出每篇论文对应的代码、项目与演讲材料链接。；外部研究者可验证、复现并反馈的公开渠道；GitHub 仓库（CustomProcessingUnit、ghidra-atom-microcode 等）与 IAIK/AEPIC 仓库（MIT 许可）构成可被复用与反馈的公开材料。

能力与结果：形成可复用框架而非单次验证脚本的产出习惯；工具建设进入无公开文档领域（Intel Atom 微码）并整理为分析框架与 Ghidra 处理器模块的前提条件。注：深度对话与自述维度无一手长篇反思（pb-conv-03=unknown），对个人层面稳定习惯的推断构成证据层级约束。；RopMate 可视化 ROP 链构造辅助（IEEE VizSec 2018）；constantine 编译器侧信道硬化（ACM CCS 2021）；CustomProcessingUnit CPU 微码动态分析框架与 ghidra-atom-microcode 处理器模块（Black Hat 2022 / WOOT 2023）；predictive-cs-fuzzing 上下文敏感模糊测试（NDSS 2024）

置信度：medium；替代解释：工件公开化是系统安全研究圈的常见规范，并非个人特有；GitHub pinned repos 与 star 数（CustomProcessingUnit 415★、ghidra-atom-microcode 88★）仅观测到公开成功实例，未公开或未发表的尝试不可观测，存在幸存者偏差。

证据：pb-works-tool-building-habit, pb-works-ropmate-2018, pb-works-constantine-2021, pb-works-cpu-microcode-2022-2023, pb-works-predictive-cs-fuzzing-2024, pb-r2-01, pb-community-006, pb-tl-03, pb-tl-07, pb-tl-13

### 随研究主题迁移与对应方向团队合著

起点：早期 ROP 工作与 Sapienza 的 Coppa、D'Elia、Demetrescu 合著（2018–2019）；2019 年起博士方向将模糊测试与程序分析绑定到架构/微架构漏洞目标，形成方法-目标配对。

练习与反馈：随主题迁移与对应方向团队合著：Constantine 阶段引入 Querzoni（Sapienza University of Rome）与 Giuffrida（Vrije Universiteit Amsterdam），机构归属由 NDSS 2024 一手页印证；ÆPIC Leak 阶段与 TU Graz 的 Kogler/Schwarzl/Gruss、AWS 的 Lipp、CISPA 的 Michael Schwarz 合著（CISPA/M.Schwarz 由 USENIX 2022 一手页与 aepicleak.com 直接标注）；Uncontained 阶段与 Vrije Universiteit Amsterdam 的 Koschel/Bos/Giuffrida 合著（机构由 USENIX 2023 一手页印证）；Predictive CS Fuzzing 阶段与 EURECOM 的 Andrea Fioraldi、Davide Balzarotti 合著（机构由 NDSS 2024 一手页印证）。；合著带来同行评审式的方向反馈与互补技术能力（D'Elia/Querzoni 的程序分析、Fioraldi 的 AFL++ 模糊测试基建、TU Graz isec 的硬件与侧信道、Giuffrida/Bos 的系统安全）。该合作网络在 2018–2024 年间持续产出顶会论文。

能力与结果：形成按主题对接对应方向互补能力的工作模式；TU Graz isec（前 IAIK，2025-01-01 更名 ISEC）子机构由 TU Graz isec 官网一手核验 Schwarzl/Gruss 成员身份与 Æpic Leak 发布，Kogler 的 IAIK 归属仍仅由 USENIX 页与 IAIK/AEPIC 仓库二次印证。；Constantine（ACM CCS 2021，引入跨机构合作者 Querzoni 与 Giuffrida）；ÆPIC Leak（USENIX Security 2022，与 TU Graz isec、CISPA、AWS 合著）；Uncontained（USENIX Security 2023，与 Vrije Universiteit Amsterdam 合著）；Predictive Context-sensitive Fuzzing（NDSS 2024，与 EURECOM 合著）

置信度：medium；替代解释：跨机构合著的协作发起方（主动对接 vs 共同兴趣/导师引荐）无一手材料证实；本轮一手核验仅消除机构归属的单源限制，未提供发起动因证据，不得据此断言主动对接对应方向核心团队。合著者名单来自个人站自述与一手论文页，协作发起方未由一手材料证实。注：Spectre 相关工作（ESORICS 2022）合著未由一手材料核验（Springer 页 404、DBLP bot-block），不作为该机制已确立实例。

证据：pb-community-004, pb-community-005, borrello-ext-04, borrello-ext-05, pb-decisions-03, pb-works-aepic-leak-2022, pb-r3-01, pb-r3-02, pb-r4-01, pb-r4-02

### 同一主题跨年度多次会议演讲的重复性输出

起点：2020-01 在 DEFCON Group Rome 发表 CPU 微架构数据采样演讲（基于 Brandon Falk 工作），本地分会提供低门槛公开输出渠道；共同创立 DEFCON Group Rome 身份仅个人页自述，缺少第二来源。

练习与反馈：同一主题跨年度在多个会议重复发表：CPU 微码主题 2022 Black Hat USA（Custom Processing Unit）、2023 OffensiveCon、2023 WOOT（CustomProcessingUnit）；ÆPIC Leak 2022 Black Hat USA 与 2022 USENIX Security。OffensiveCon 2023 讲题由官方讲者页核验一致（CustomProcessingUnit: Reverse Engineering and Customization of Intel Microcode），但官方页姓名印刷为 Pietro Borrella，与个人站/USENIX 页 Pietro Borrello 拼写不一致，无第二来源消除。Black Hat USA 2022 与 WOOT 2023 官方议程页分别返回 403/404，仅依赖个人站自述。；Black Hat、OffensiveCon、USENIX 等会议构成面向更广安全社区的输出与反馈渠道；本地 DEFCON 分会提供低门槛同伴反馈。

能力与结果：形成同一研究产物的多次会议投稿惯例，获取不同圈层反馈。；DEFCON Group Rome 2020-01 CPU 微架构数据采样；Black Hat USA 2022 ÆPIC Leak 与 Custom Processing Unit（官方页 403 未核验，个人站单源）；OffensiveCon 2023 CustomProcessingUnit（讲题官方页核验一致，姓名拼写差异未消除）；WOOT 2023 CustomProcessingUnit（论文页 404 未核验，个人站单源）

置信度：low；替代解释：该机制的重复性输出特征判断受单源与身份差异约束：Black Hat 2022 与 WOOT 2023 核心重复实例锚点仅依赖个人站自述（官方页 403/404），OffensiveCon 2023 虽讲题核验一致但姓名拼写差异未消除；跨年度重复亦可能为同一研究产物的多次会议投稿惯例，而非刻意完善工具与定位的重复性输出。

证据：pb-tl-05, pb-tl-08, pb-tl-09, pb-tl-10, pb-tl-13, pb-tl-14, pb-community-001, pb-community-008, pb-tr-01

### 从单一漏洞发现到漏洞类别系统化归纳

起点：2023 年在 Linux 内核多个子系统报告一批 type confusion 与 use-after-free 类 CVE（HID、RDS、TUN/TAP、TLS、SCTP、Realtime Scheduler），同型批量发现提示存在统一审计/挖掘方法论。

练习与反馈：把单一漏洞发现整理为动态分析框架（CustomProcessingUnit 把 Intel Atom 微码逆向整理为可复用框架），把零散 type confusion/UAF 归纳为容器混淆类别（Uncontained 将 container confusion 作为可命名、可系统搜索的内核漏洞类别）。；上游 Linux 内核 maintainer review（补丁记录由个人页自述并给出链接，kernel.org git log 抓取返回 403 未独立核实）；顶会同行评审（USENIX Security 2023）。

能力与结果：形成从单一漏洞到漏洞类别系统化归纳的方法基础；同型批量 CVE 与类别化论文相互支撑。；CustomProcessingUnit CPU 微码动态分析框架（WOOT 2023，论文页 404 未独立核验）；Linux 内核 type confusion/UAF 批量 CVE（2023）；Uncontained 容器混淆类别系统化研究（USENIX Security 2023）

置信度：medium；替代解释：类别化归纳的推断受幸存者偏差约束，仅观测到公开 CVE、顶会论文与公开仓库的工作，未公开或未发表的尝试不可观测；同型批量 CVE 的具体模糊测试或静态分析方法（是否基于 syzkaller 及与 Uncontained 工具的关系）未由一手 writeup 或论文正文核验。

证据：pb-works-kernel-cves-2023, pb-works-uncontained-memory-2023, pb-works-cpu-microcode-2022-2023, pb-decisions-05, pb-decisions-06, pb-tl-13, pb-tl-16

## 可迁移与不可迁移

- 可迁移：每条研究线索配套公开可复现工具仓库并系统列出代码/项目/演讲材料链接（RopMate、constantine、CustomProcessingUnit、ghidra-atom-microcode、predictive-cs-fuzzing）
- 可迁移：将单一漏洞发现整理为可复用动态分析框架与处理器模块，而非止步于单次 PoC
- 可迁移：把零散同型漏洞归纳为可命名、可系统搜索的漏洞类别（container confusion）
- 可迁移：随主题迁移与对应方向团队合著以获取互补技术能力（程序分析、AFL++ 模糊测试基建、硬件与侧信道）
- 可迁移：本地分会（DEFCON Group Rome）作为早期低门槛公开输出与同伴反馈渠道
- 可迁移：以寻找研究空白点（架构级未初始化数据泄漏）而非补丁驱动定位问题
- 不可直接迁移：Sapienza University of Rome 同校连续本/硕/博培养与长期合作者 Giuffrida/D'Elia/Querzoni 构成的稳定学术训练链条与师承关系，属于特定机构资源
- 不可直接迁移：Sapienza DIAG 系同时为 DEFCON Group Rome 会议地点，本地分会与学术机构地理重合提供早期输出渠道
- 不可直接迁移：Intel Atom 微码逆向依赖几乎无公开文档的领域知识与自建 Ghidra 处理器模块，进入门槛高且非通用
- 不可直接迁移：与 TU Graz isec（前 IAIK）、CISPA、EURECOM、Vrije Universiteit Amsterdam 等团队既有的跨机构合著网络，属特定合作资源而非可复制个人方法
- 不可直接迁移：Apple SEAR 微架构安全研究员岗位为可核验的雇主归属，依赖博士期已建立的微架构/微码研究能力，岗位本身不构成可迁移方法

## 复核问题


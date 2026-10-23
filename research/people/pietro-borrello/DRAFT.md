# 未通过独立复核

已达到最大修订次数 3；本文件是审计草稿，不得进入跨人物比较。

# Pietro Borrello：漏洞研究成长分析

- 擅长领域：微码/硬件/系统漏洞
- 独立复核：revise · 83/100

## 成长阶段

- **2017–2019 · Sapienza 本硕阶段与 ROP 利用研究起步**：在 Sapienza University of Rome 连续完成 Engineering in Computer Science 的 BSc（2017）与 MSc（2019），在 Coppa、D'Elia、Demetrescu 等 Sapienza 程序分析团队指导下，以 ROP 利用辅助工具（RopMate，IEEE VizSec 2018）切入安全研究，并发布配套代码仓库；同年 ACM SAC 2019 发表 'The ROP needle'。该阶段建立"研究伴随公开代码仓库"的发布习惯，并将早期研究网络限定在 Sapienza。（置信度：high）
  - 证据：pb-tl-01, pb-tl-02, pb-tl-03, pb-tl-04, pb-works-ropmate-2018, pb-decisions-01, pb-decisions-02, pb-decisions-08, pb-tl-19
- **2020–2021 · 由 ROP 利用转向微架构侧信道防御与程序混淆**：研究对象由 ROP 利用延伸到微架构侧信道防御与程序混淆：2020-01 在罗马 DEFCON Group 发表 'Breaking the walls: CPU introspection through micro-architectural data sampling'（基于 Brandon Falk 既有工作）；2021 年 ACM CCS 2021 发表 Constantine（编译器自动硬化抵御侧信道）与 ACM/IEEE DSN 2021 发表 'Hiding in the Particles'（raindrop，ROP 与程序混淆），分别公开 constantine 与 raindrop 仓库。合作者新增 Querzoni 与 Giuffrida（具体机构归属未由一手页面标注，二人 Sapienza 与 Vrije Universiteit Amsterdam 归属由 NDSS 2024 与 USENIX 2023 一手页印证），研究网络跨出 Sapienza。（置信度：high）
  - 证据：pb-tl-05, pb-tl-06, pb-tl-07, pb-works-constantine-2021, pb-conv-02, pb-community-001, pb-r2-01, pb-r2-03
- **2022 · 微架构漏洞研究与 CPU 微码逆向的同期展开**：以第一作者在 USENIX Security 2022 发表 ÆPIC Leak（CVE-2022-21233，APIC MMIO 未定义区间返回缓存陈旧数据，可泄露 SGX enclave 内容），并在 Black Hat USA 2022 同期发表 ÆPIC Leak 与 'Custom Processing Unit: Tracing and Patching Intel Atom Microcode' 两场演讲（Black Hat 议程页返回 403，演讲事实仅依赖个人站自述）。合作者扩展至 TU Graz IAIK（Gruss、M. Schwarz、Schwarzl、Kogler）与 CISPA（M. Schwarz）。研究对象由架构层延伸到 CPU 微码层。（置信度：medium）
  - 证据：pb-works-aepic-leak-2022, pb-works-cpu-microcode-2022-2023, pb-works-cpu-microcode-bh-page, pb-tl-08, pb-tl-09, pb-tl-10, pb-tl-11, pb-decisions-03, pb-community-005, pb-community-008, borrello-ext-03, pb-r2-02
- **2023 · 内核子系统漏洞批量发现与博士学位完成**：在 Sapienza 取得 Engineering in Computer Science 博士学位（PhD），自述方向为将 Fuzzing 与 Program Analysis 用于架构与微架构漏洞。同年以合作者身份在 USENIX Security 2023 发表 Uncontained（Linux 内核容器混淆，Vrije Universiteit Amsterdam 团队一手印证），并在 WOOT 2023 发表 CustomProcessingUnit（WOOT 2023 一手论文页返回 404，发表事实与首个 CPU 微码动态分析框架定位仅依赖个人站自述）。2023 年在 Linux 内核 RDS、Realtime Scheduler、TUN/TAP、TLS、SCTP、HID 等子系统报告一批类型混淆与 UAF 类漏洞（CVE-2023-1073 至 CVE-2023-25012 等）。同年博士毕业后加入 Apple SEAR 担任 Microarchitecture Security Researcher。（置信度：medium）
  - 证据：pb-tl-12, pb-tl-13, pb-tl-14, pb-tl-15, pb-tl-16, pb-tl-18, pb-works-kernel-cves-2023, pb-works-uncontained-memory-2023, pb-decisions-04, pb-decisions-05, pb-decisions-06, pb-decisions-07, borrello-ext-01, borrello-ext-02, pb-tr-01, pb-r3-02
- **2023–2024 · 博士阶段收尾与模糊测试方法研究**：2023 年 IEEE S&P 发表内存压缩时序侧信道攻击（合作），2024 年 NDSS 发表 Predictive Context-sensitive Fuzzing（合作者含 Andrea Fioraldi（EURECOM，AFL++ 作者）、Davide Balzarotti（EURECOM）、C. Giuffrida（Vrije Universiteit Amsterdam）等，机构归属由 NDSS 2024 一手页面核验），并公开 predictive-cs-fuzzing 仓库。研究对象由 CPU 微码扩展至 Linux 内核子系统与模糊测试方法学。（置信度：medium）
  - 证据：pb-works-predictive-cs-fuzzing-2024, pb-works-tool-building-habit, pb-works-uncontained-memory-2023, pb-tl-17, pb-tl-19, pb-community-004, pb-community-006, pb-r3-01

## 主要成长机制

### 研究工件公开化：每条研究线索伴随可复现代码仓库与处理器模块

起点：2018 年 RopMate（IEEE VizSec 2018）即以公开代码仓库形式发布，处于 Sapienza 程序分析团队指导网络中，初始即建立"论文+工具"的发布结构。

练习与反馈：2018 至 2024 年，每条主要研究线索均伴随公开 GitHub 仓库：RopMate、raindrop、constantine、CustomProcessingUnit、ghidra-atom-microcode、predictive-cs-fuzzing；个人站系统列出每篇论文对应的代码、项目与演讲材料链接。；公开仓库构成外部研究者可验证、复现并反馈的公开渠道；AEPIC 仓库（TU Graz IAIK 托管，MIT 许可）为可核验的合著与机构归属二次来源。上游内核 maintainer 对补丁的 review 亦构成外部工程标准校准（kernel.org git log 抓取返回 403，未独立核验）。

能力与结果：形成可复用工具而非单次验证脚本的产出习惯，使工具建设成为进入无公开文档领域（Intel Atom 微码）的前提条件。注：'深度对话与自述'维度无一手长篇反思（pb-conv-03=unknown），对个人层面稳定习惯的推断构成证据层级约束。；CustomProcessingUnit 仓库（GitHub pinned，415★）与 ghidra-atom-microcode（88★）为微码分析提供可复用框架；constantine 仓库支撑 ACM CCS 2021 侧信道防御工作；predictive-cs-fuzzing 仓库支撑 NDSS 2024 模糊测试工作；AEPIC 仓库（IAIK/AEPIC）为 ÆPIC Leak 提供可复现材料

置信度：medium；替代解释：工件公开化可能是 Sapienza 程序分析团队（Coppa、D'Elia、Demetrescu）与 TU Graz IAIK 团队的共享实践而非个人特有习惯；AFL++ 作者 Fioraldi 的合著亦强化工具化导向。个人层面稳定习惯的推断受一手反思缺失（pb-conv-03）约束。

证据：pb-works-ropmate-2018, pb-works-constantine-2021, pb-works-aepic-leak-2022, pb-works-cpu-microcode-2022-2023, pb-works-predictive-cs-fuzzing-2024, pb-works-tool-building-habit, pb-community-005, pb-community-006, pb-tl-03, pb-tl-13, pb-tl-17

### 随研究主题迁移与对应方向团队合著

起点：早期（2018–2019）合著者集中于 Sapienza（Coppa、D'Elia、Demetrescu），研究网络限定于单一机构。

练习与反馈：随研究主题迁移与对应方向团队合著：ROP 阶段与 Sapienza 程序分析团队；Constantine 阶段引入 Querzoni 与 Giuffrida（Vrije Universiteit Amsterdam，由 NDSS 2024 与 USENIX 2023 一手页印证）；ÆPIC Leak 阶段与 TU Graz IAIK（Gruss、M. Schwarz、Schwarzl、Kogler）及 CISPA（M. Schwarz，由 ÆPIC USENIX 2022 一手页支撑）合著；Uncontained 阶段与 Vrije Universiteit Amsterdam（Bos、Giuffrida，USENIX 2023 一手页印证）；Predictive Context-sensitive Fuzzing 阶段与 EURECOM（Andrea Fioraldi、Davide Balzarotti，NDSS 2024 一手页印证）合著。；合著带来同行评审式的方向反馈与互补技术能力（D'Elia 的程序分析、Fioraldi 的模糊测试基建、TU Graz 的硬件与侧信道）。

能力与结果：跨机构稳定合著关系在 2018–2024 年间持续产出顶会论文，构成同伴与导师反馈网络。；ÆPIC Leak（USENIX Security 2022，第一作者，TU Graz/CISPA 合著）；Uncontained（USENIX Security 2023，Vrije Universiteit Amsterdam 合著）；Predictive Context-sensitive Fuzzing（NDSS 2024，EURECOM 合著）；Constantine（ACM CCS 2021，引入 Vrije Universiteit Amsterdam 合作者）

置信度：medium；替代解释：合著者名单来自个人站自述，协作发起方未由一手材料证实。跨机构合著可能是共同研究兴趣或导师引荐促成，而非个人主动对接核心团队以弥补单一机构能力缺口；ESORICS 2022 'Spectre in the Cloud' 合著未由一手材料核验（Springer 404、DBLP bot-block），不宜作为已确立协作实例。

证据：pb-works-constantine-2021, pb-works-aepic-leak-2022, pb-works-uncontained-memory-2023, pb-works-predictive-cs-fuzzing-2024, pb-community-004, pb-community-005, pb-decisions-03, pb-tl-16, pb-r3-01, pb-r3-02

### 微码主题跨年度重复输出

起点：2022 年进入 Intel Atom 微码领域，公开文档稀缺，需逆向并自建 Ghidra 处理器模块才能分析。

练习与反馈：围绕 CPU 微码主题跨年度、跨会议重复输出：Black Hat USA 2022（'Custom Processing Unit: Tracing and Patching Intel Atom Microcode'，议程页 403，仅个人站自述）、WOOT 2023（'CustomProcessingUnit: Reverse Engineering and Customization of Intel Microcode'，一手论文页 404，仅个人站自述）、OffensiveCon 2023（讲题由官方讲者页核验一致 pb-tr-01）。；会议演讲提供面向更广安全社区的输出与反馈渠道。OffensiveCon 2023 官方讲者页将姓名印刷为 'Pietro Borrella'，与个人站/USENIX 页 'Borrello' 不一致，无第二来源消除拼写差异。

能力与结果：获取反馈并完善工具与定位，将单一漏洞发现整理为可复用分析框架（CustomProcessingUnit）与配套 Ghidra 处理器模块。；OffensiveCon 2023 演讲讲题经官方讲者页核验一致（pb-tr-01）；Black Hat USA 2022 微码演讲（个人站自述，议程页 403 未独立核验）；WOOT 2023 CustomProcessingUnit 论文（一手论文页 404，发表事实仅依赖个人站自述）

置信度：low；替代解释：该机制的重复性输出特征判断受单源与身份差异约束：Black Hat 2022 与 WOOT 2023 官方页分别 403/404 未独立核验，核心重复实例锚点仅 OffensiveCon 单条已核验；OffensiveCon 讲者姓名拼写差异未消除。跨年度重复亦可能为同一研究产出的多次会议投稿惯例，而非刻意打磨。

证据：pb-works-cpu-microcode-2022-2023, pb-works-cpu-microcode-bh-page, pb-tl-10, pb-tl-13, pb-tl-14, pb-tr-01

### 把零散内核漏洞归纳为可命名、可系统搜索的漏洞类别

起点：2023 年在 Linux 内核多个子系统（HID、RDS、TUN/TAP、TLS、SCTP、Realtime Scheduler）报告若干类型混淆与 UAF 类漏洞。

练习与反馈：把单一漏洞发现整理为动态分析框架，把零散 type confusion/UAF 归纳为容器混淆类别：Uncontained（USENIX Security 2023）将'容器混淆'作为内核漏洞类别进行系统化研究，与同年内核 CVE 批量发现在方法上一致（系统化而非单点）。；同型批量发现说明存在统一的审计/挖掘方法论而非逐个偶然发现；具体所用模糊测试或静态分析方法（是否基于 syzkaller 及与 Uncontained 工具的关系）未由一手 writeup 或论文正文核验。

能力与结果：由找单个漏洞转向定义漏洞类别并做系统覆盖，形成可复用的方法基础。；Uncontained（USENIX Security 2023，容器混淆类别）；2023 年 Linux 内核 CVE 批量（type confusion/UAF，CVE-2023-1073 至 CVE-2023-25012 等）；自报累计发现并协助修复逾百个软件/操作系统/CPU 漏洞（公开 CVE 中 21 个与本人相关）

置信度：medium；替代解释：类别化归纳可能是 Vrije Universiteit Amsterdam 团队（Bos、Giuffrida）的协作方法论而非个人特有；CVE 批量贡献的独立发现与团队协作分工未作区分，个人站将 CVE 统一列于作者名下。自报'over one hundred bugs'与公开 21 个 CVE 之间的差额缺乏可核验明细。

证据：pb-works-kernel-cves-2023, pb-works-uncontained-memory-2023, pb-decisions-05, pb-decisions-06, pb-tl-16, pb-tl-19

## 可迁移与不可迁移

- 可迁移：每条研究线索伴随公开代码仓库与可复现工具，使外部研究者可验证、复现并反馈。
- 可迁移：进入缺乏公开文档的目标域（如 CPU 微码）时，自建分析框架与反编译器处理器模块作为开启新分析能力的前提。
- 可迁移：将零散同类漏洞归纳为可命名、可系统搜索的漏洞类别，由单点发现转向系统覆盖。
- 可迁移：跨机构合著以获取互补技术能力（程序分析、模糊测试基建、硬件与侧信道）。
- 可迁移：本地安全社区（DEFCON Group）作为低门槛同行反馈渠道，将早期研究课题作公开报告。
- 不可直接迁移：Sapienza University of Rome 本硕博同校连续培养（2017 BSc、2019 MSc、2023 PhD）提供的稳定学术环境与师承关系（Giuffrida、D'Elia、Querzoni 等长期合作者）。
- 不可直接迁移：Sapienza 程序分析团队（Coppa、D'Elia、Demetrescu）与 TU Graz IAIK、CISPA、Vrije Universiteit Amsterdam、EURECOM 等团队的既存合著网络，非个人可独立重建。
- 不可直接迁移：DEFCON Group Rome 共同创始人身份提供的本地社区组织与演讲渠道。
- 不可直接迁移：mhackeroni/TRX 等 CTF 队伍成员身份（仅个人站自述，未独立证实）提供的同伴协作环境。
- 不可直接迁移：CPU 微码与微架构漏洞研究所需的硬件行为知识与 Intel SGX 等专有知识门槛。
- 不可直接迁移：Apple SEAR 产业安全岗位提供的厂商内部威胁模型与硬件生命周期研究条件（入职日期未公开）。

## 复核问题

- mechanisms[1].repeated_practice 将 Constantine 合作者 Querzoni 与 Giuffrida 并列括注为 '（Vrije Universiteit Amsterdam，由 NDSS 2024 与 USENIX 2023 一手页印证）'，暗示二人同属 Vrije Universiteit Amsterdam，与所引一手证据 pb-r3-01 相反：NDSS 2024 一手页列 Leonardo Querzoni 为 Sapienza University of Rome、Cristiano Giuffrida 为 Vrije Universiteit Amsterdam。这是事实错误而非加注不精确，且与 round-2 复核 #4 已就 stages[1].capability_change 修正的同一机构括注问题重复出现，说明该轮 synthesis_instructions 未在本字段落实。
- 字段 mechanisms[1].repeated_practice（亦见 mechanisms[1].observed_outcomes 'Constantine（ACM CCS 2021，引入 Vrije Universiteit Amsterdam 合作者）'）：原措辞 'Constantine 阶段引入 Querzoni 与 Giuffrida（Vrije Universiteit Amsterdam，由 NDSS 2024 与 USENIX 2023 一手页印证）'，将 Querzoni 与 Giuffrida 同归 Vrije Universiteit Amsterdam，与 pb-r3-01 一手页相反。改写方向：拆分为二人各自机构，写为 'Constantine 阶段引入 Querzoni（Sapienza University of Rome）与 Giuffrida（Vrije Universiteit Amsterdam），机构归属由 NDSS 2024 一手页（pb-r3-01）印证'，删除将二人并列括注为同一机构的表述，确保与所引一手证据一致。此为事实修正，必须落实。
- 字段 mechanisms[2].alternative_explanation：原句末 '跨年度重复亦可能为同一研究产出的多次会议投稿惯例，而非刻意打磨' 残留比喻性 '打磨'。改写方向：删除 '刻意打磨'，改为 '跨年度重复亦可能为同一研究产出的多次会议投稿惯例，而非刻意完善工具与定位的重复性输出'，与同字段前句 '重复性输出特征判断' 用语一致，使 round-3 synthesis_instructions 关于 mechanisms[2] 全字段复核 '打磨' 残留的要求完整落实。
- 字段 mechanisms[1].repeated_practice（CISPA 支撑来源）：将 'CISPA（M. Schwarz，由 ÆPIC USENIX 2022 一手页支撑）' 的支撑来源更正为 pb-decisions-03 或 pb-works-aepic-leak-2022（aepicleak.com），并核对 pb-tl-08 claim 是否实际列出 M. Schwarz/CISPA；若 pb-tl-08 未列，不得以 pb-tl-08 作为 CISPA 一手支撑，改引 pb-decisions-03（ÆPIC USENIX 2022 一手页，含 Michael Schwarz/CISPA）或 aepicleak.com。
- 字段 stages[2].capability_change 与 mechanisms[1].repeated_practice（TU Graz IAIK 子机构就地加注）：因 IAIK 仅由 pb-community-005（IAIK/AEPIC 仓库）二次印证、未由一手论文页独立核验（open_questions 已记），在 stages[2] 与 mechanisms[1] 正文首次出现 'TU Graz IAIK' 处就地加注 'IAIK 子机构归属由 IAIK/AEPIC 仓库二次印证，未由一手论文页独立核验'，使正文证据强度与 open_questions 标注一致。

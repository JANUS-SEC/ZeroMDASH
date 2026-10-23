# Lukas Maar：漏洞研究成长分析

- 擅长领域：内核侧信道与移动端漏洞
- 独立复核：pass · 76/100

## 成长阶段

- **2018-2022 · 学术训练基础：电气工程与计算机科学双背景**：在 Graz University of Technology 取得 BSc Electrical Engineering（2018）、BSc Computer Science 与 MSc Electrical Engineering（2022），形成软硬件双背景的训练基础；其 ISEC 归属最早可核验记录为 2023 DOPE 合著，2018-2022 期间是否已加入 ISEC 无来源支撑。同年授予学士与硕士学位在主页存在表述压缩，学制细节未独立核验。（置信度：medium）
  - 证据：lm-timeline-2018-bsc-ee, lm-timeline-2022-bsc-cs-msc-ee, lm-works-001
- **2023 · 防御侧起步：PKS 域保护与首次会议发表**：以一作在 ACSAC 2023 发表 DOPE，提出基于 Intel PKS 的内核域保护机制覆盖 8 个敏感内核数据对象，PoC 约 5000 行代码，真实应用运行时开销 2.3%。研究起点为主动防御设计，与后续攻击侧工作形成防御-攻击双视角的初始结构。同期建立与 Stefan Mangard、Daniel Gruss、Martin Schwarzl、Fabian Rauscher 的固定合著网络。（置信度：high）
  - 证据：lm-works-001, LM-community-01, lm-timeline-2023-dope-acsac
- **2024 · 攻击侧突破：SLUBStick 与多子方向并发**：在 USENIX Security 2024 发表 SLUBStick，以 SLUB 分配器定时侧信道执行 cross-cache 攻击（频繁通用缓存成功率 >99%），将受限堆漏洞升级为通过页表操作的任意读写原语，在 v5.19/v6.2 评估 9 个真实 CVE 完成提权与容器逃逸。确立分配器/内核数据结构时序侧信道这一核心技术主题。同年并发 Defects-in-Depth（防御评估）、HEK-CFI（控制流防护）、Remote Scheduler Contention（处理器级争用侧信道），研究范围由单点扩展到多子方向。形成 writeup、会议演讲与 GitHub PoC 配套的固定发表方式。（置信度：high）
  - 证据：lm-works-002, lm-works-003, lm-works-004, r1-001, lm-timeline-2024-slubstick-usenix, LM-community-02
- **2025 · 主题泛化与体系整合：从分配器到通用数据结构侧信道**：在 NDSS 2025 发表 KernelSnitch，将 SLUBStick 的分配器侧信道泛化为硬件无关的内核数据结构（哈希表、红黑树）定时侧信道，演示隐蔽信道（最高 580 kbit/s）、堆指针泄漏（65 秒内）与网站指纹（F1>89%）。同年 USENIX Security 发表 TLB 侧信道泄漏、Android 驱动 n-day 评估、ChoiceJacking USB 攻击，并以博士论文 Kernel Security in the Wild 对内核利用、防御与侧信道进行体系整合。从单一技术泛化到防御反向利用、n-day 评估、移动端物理接口攻击多线并行，标志阶段性体系整合。（置信度：high）
  - 证据：lm-works-005, lm-works-006, lm-works-007, r1-001, lm-timeline-2025-kernelsnitch-ndss, lm-timeline-2025-tlb-choicejacking-usenix, lm-timeline-2025-phd-thesis, LM-SC-01, LM-SC-02, LM-SC-03
- **2026 · 工业化产出：OEM 驱动链与厂商 CVE 密集产出**：研究主题迁移到移动端/加速器驱动 page UAF，并复用 SLUBStick 的 cross-cache→pipe_buffer→物理读写链条（CVE-2026-57551，Qualcomm QAIC，从用户态改写 pipe_buffer 元数据获得物理任意读写并清零 UID/GID 提权）。发表 OEMpocalypse（CVE-2026-21102，针对 Samsung/Xiaomi/Oppo/OnePlus/Realme OEM 自有内核代码，选取对 slab 加固不敏感的 page-UAF 原语使单一漏洞覆盖该 OEM 全部出货机型）、Eviction Notice、LeakyTree、Clone2Pwn、Fence2Pwn 等。方法学仍以侧信道与内存生命周期 bug 为主要方向，目标难度升级到 OEM 驱动链、IOMMU/DualDAR 子系统与跨 VM 页共享。2026 年同时在 Calif 与 TU Graz ISEC 担任研究职务（Calif 加入精确时点无来源支撑）。（置信度：high）
  - 证据：lm-works-009, lm-works-010, lm-dec-04, lm-dec-05, lm-dec-06, lm-dec-07, lm-timeline-2026-industrial-cves, lm-timeline-2026-conference-papers, lm-timeline-current-positions, LM-SC-06, LM-SC-07, r3-001

## 主要成长机制

### 内核数据结构与分配器时序侧信道技术主题的反复练习与泛化

起点：2023 年与 Daniel Gruss 的一次讨论以“内核 resembles hardware”的类比将共享内核资源重新框定为潜在时序信道，为 KernelSnitch 设定方向；DOPE（PKS 域保护）提供的对内核内存保护机制的防御侧理解为反向利用提供前提。

练习与反馈：跨版本、跨系统迭代：先用 Bootlin 与 CodeQL 手工审计候选内核哈希表（自述 'old-school code archaeology'，LM-SC-02 原文，作引文），再跨 Linux v5.19/v6.2（SLUBStick cross-cache，频繁通用缓存成功率 >99%）与 v5.15/v6.5/v6.8（KernelSnitch POSIX timer/futex/IPC 哈希表、IPC radix 树、hrtimer 红黑树）迭代寻找时序差异更小、更难归因于具体系统的分配路径。同一技术主题从 SLUB 分配器侧信道（SLUBStick）泛化到通用内核数据结构侧信道（KernelSnitch），再扩展到 TLB/调度器争用侧信道。；NDSS 2025 accepted-papers 页（lukas-ext-03）与 NDSS 2025 论文页（LM-community-04）确认 KernelSnitch 第一作者 Lukas Maar 及合著者全部来自 Graz University of Technology；个人一手站点完整出版物索引（r1-001）一手核验 When Good Kernel Defenses Go Bad / Defects-in-Depth / HEK-CFI / Fence2Pwn 四篇载体标题、venue、年份与合著者，会议官方议程页本次未抓取成功，证据强度为 primary 一手核验而非会议官方页面 documented。本人自述三次结构化 responsible disclosure（LM-SC-04）反映对披露反馈的外部校验。

能力与结果：形成可迁移的“以内核数据结构规模/占用差异构造软件时序信道”方法论；heap KASLR leak 项目的显式目标为 'minimize system-specific dependencies, as universal as possible'（LM-SC-03 原文，引文，限定于该单项目，不扩展为整个侧信道技术主题的显式目标）。；SLUBStick（USENIX Security 2024）：SLUB 分配器定时侧信道 + cross-cache 重用，9 个真实 CVE 提权与容器逃逸；KernelSnitch（NDSS 2025）：哈希表/红黑树定时侧信道，隐蔽信道 580 kbit/s、堆指针 65 秒泄漏、网站指纹 F1>89%；When Good Kernel Defenses Go Bad（USENIX Security 2025）：防御放大的 TLB 侧信道泄漏；OEMpocalypse（CVE-2026-21102）：page-UAF 原语对 slab 加固不敏感，单一漏洞覆盖该 OEM 全部出货机型

置信度：high；替代解释：同一技术主题反复出现部分由 TU Graz IAIK/isec-tugraz 团队的侧信道研究谱系（Gruss、Mangard 等）与团队既有工具链（SLUBStick/KernelSnitch artifact）决定，而非仅个体选择；缺乏 2023 年前早期训练材料，无法排除该方向在加入团队前已有积累。

证据：lm-works-001, lm-works-002, lm-works-005, lm-works-006, lm-works-007, lm-dec-03, lm-dec-06, lm-timeline-2024-slubstick-usenix, lm-timeline-2025-kernelsnitch-ndss, lm-timeline-2025-tlb-choicejacking-usenix, LM-SC-01, LM-SC-02, LM-SC-03, LM-SC-04, lukas-ext-03, LM-community-04, r1-001

### 防御-攻击双视角：从构造防御到反向利用防御盲区

起点：DOPE（PKS 域保护，ACSAC 2023）与 HEK-CFI（CET 控制流防护，AsiaCCS 2024）提供对内核防御机制设计的第一手理解，构成反向利用防御盲区的前置知识。

练习与反馈：跨时期在防御侧与攻击侧并行：DOPE/HEK-CFI（防御构造）→ Defects-in-Depth（Android 下游防御有效性测量，USENIX Security 2024）→ When Good Kernel Defenses Go Bad（防御放大 TLB 侧信道泄漏，USENIX Security 2025）→ Fence2Pwn（绕过 KFENCE、slab 硬化与内存标记，USENIX Security 2026）。防御评估与攻击技术同年并进（2024 SLUBStick + Defects-in-Depth）。；个人一手站点完整出版物索引（r1-001）一手核验四篇载体标题/venue/年份/合著者；USENIX Security 2025/2026 与 AsiaCCS 2024 会议官方议程页本次抓取截断未返回条目，未升级到会议官方页面 documented。SLUBStick 入选 CSAW'24 Europe ARC Finalist（本人自述，官方页面未核验，见 tensions）。

能力与结果：形成“理解内核保护机制设计 → 定位其集成/实现盲区 → 反向构造利用”的双视角方法链，能将防御评估的发现直接转为攻击原语设计输入。；DOPE：基于 PKS 的域保护覆盖 8 个敏感对象，运行时开销 2.3%；Defects-in-Depth：Android 下游内核防御有效性测量；When Good Kernel Defenses Go Bad：防御放大 TLB 侧信道揭示内核对象位置；Fence2Pwn：KFENCE 时序侧信道绕过 slab 硬化与内存标记

置信度：high；替代解释：双视角可能由团队整体研究取向（IAIK 既做防御又做攻击）塑造，而非个体主动选择；Defects-in-Depth/HEK-CFI 等条目在合著中的具体角色未抓取原文核验，Lukas Maar 可能非主导者。

证据：lm-works-001, lm-works-002, lm-works-004, lm-works-007, lm-works-010, lm-dec-03, lm-timeline-2024-slubstick-usenix, lm-timeline-2025-tlb-choicejacking-usenix, lm-timeline-2026-conference-papers, r1-001

### 可复现 PoC 工具建设的固定发表流程

起点：2024 年 SLUBStick 配套公开 GitHub 仓库与 Zenodo DOI 永久归档，建立“论文 + 演讲 + artifact”的发表模板。

练习与反馈：每次研究产出公开可复现 artifact：SLUBStick（isec-tugraz/SLUBStick，Ubuntu 22.04/kernel v6.2 VM 镜像 + 端到端利用代码）、KernelSnitch（isec-tugraz/KernelSnitch artifact；另个人仓库 lukasmaar/kernelsnitch，9 commits/43 stars/3 forks，MIT/GPL-2.0，跨 Linux/KernelCTF/Android）、TLBSideChannel（isec-tugraz/TLBSideChannel）、QAIC page UAF（个人仓库 lukasmaar/qaic-page-uaf）。学术 artifact 仓库与个人 writeup 仓库分别归属，未统一于单一组织。；GitHub 仓库提供 issue 与 PR 入口形成外部反馈；SLUBStick 仓库含 2 个开放 issue（正文未抓取）；lukasmaar/kernelsnitch 的星标/分叉（LM-community-03）反映社区采用（isec-tugraz/KernelSnitch 组织仓库的统计未在语料中给出，不作拼接）。

能力与结果：形成可复现 artifact 工程能力与固定发布流程，降低他人复现门槛并放大影响；区分学术 artifact（isec-tugraz 组织）与个人 writeup（lukasmaar 个人）两类仓库归属。；isec-tugraz/SLUBStick（USENIX Security 2024 artifact，含 VM 镜像与利用代码）；isec-tugraz/KernelSnitch（NDSS 2025 artifact）与个人仓库 lukasmaar/kernelsnitch（实验工作区，9 commits/43 stars/3 forks）；个人仓库 lukasmaar/qaic-page-uaf（QAIC page UAF writeup，CVE-2026-57551）；SLUBStick 获 CSAW'24 Europe ARC Finalist 提名（本人自述，官方页面未核验）

置信度：high；替代解释：artifact 工程能力可能由 TU Graz IAIK/isec-tugraz 团队既有发布规范与同辈（Unterguggenberger、Oberhuber、Juffinger 等）协作支撑，而非个体独创；GitHub 统计可能受团队内部推广放大，不能直接等同于外部认可。

证据：lm-works-003, lm-works-006, LM-community-02, LM-community-03, lm-timeline-2026-industrial-cves, lm-timeline-2025-kernelsnitch-github

### 手工源码审计 + 工具辅助定位 + 约束下工具自建的方法学闭环

起点：缺乏昂贵 AI 加速器硬件时仍需推进内核利用实验；KernelSnitch 需在通用内核源码中定位候选时序信道目标。

练习与反馈：用 Bootlin 与 CodeQL 手工审计候选内核哈希表（LM-SC-02 自述 'old-school code archaeology'，原文作引文标注，叙述中不沿用该措辞），跨版本迭代寻找时序差异更小、更难归因于具体系统的分配路径（LM-SC-03）；硬件约束下将 Qualcomm QAIC 驱动路径在 QEMU 中虚拟化以在 Linux v6.18 上持续内核利用实验（LM-SC-06、lm-dec-04），前提判断为漏洞位于缓冲对象与映射生命周期而非加速器执行逻辑。；本人 writeup 公开发表以支持防御研究为显式动机（LM-SC-05）；QAIC 披露时序（2026-04-08 报告、04-23 补丁、04-27 赏金、30 天后公开，lm-dec-07）构成发现→披露→上游反馈的结构化校验；上游 lore.kernel.org Qualcomm 补丁线程被 Anubis 拦截未核验（LM-community-07）。

能力与结果：形成“工具辅助手工审计定位目标 → 约束下自建替代实验环境 → 结构化披露校验”的方法学闭环；将可机械化的构建脚本、测试环境、硬件虚拟化外包给 AI 辅助工具（Codex），把漏洞定位与利用原语构造保留为人工判断（lm-dec-05、LM-SC-07、r3-001）。；QAIC page UAF（CVE-2026-57551）：以 QEMU 虚拟化驱动路径完成利用，回收为 pipe_buffer slab 页重建原语，物理任意读写并清零 UID/GID 提权；KernelSnitch：手工审计定位内核哈希表/红黑树目标；OEMpocalypse：选取对 slab 加固不敏感的 page-UAF 原语使单一漏洞覆盖该 OEM 全部出货机型

置信度：high；替代解释：QEMU 虚拟化替代硬件的前提判断依赖前置内核能力，不可直接作为可迁移方法（见 non_transferable_conditions）；AI 辅助工具边界划分可能受团队工程实践影响而非个体原创。

证据：LM-SC-02, LM-SC-03, LM-SC-05, LM-SC-06, LM-SC-07, lm-dec-04, lm-dec-05, lm-dec-06, lm-dec-07, LM-community-07, lm-works-009, r3-001

### 学术-工业双轨与结构化披露

起点：2025 年完成博士论文 Kernel Security in the Wild（导师 Stefan Mangard，指导关系由共同作者模式推断，机构页未直接写明 advisor），获 GI 博士论文奖提名；Dagstuhl 26205 研讨会为其答辩会（2026-05-10 至 13）。

练习与反馈：同一研究在学术（USENIX/NDSS/CCS/ESORICS/AsiaCCS）与工业（Black Hat USA/Asia、Nullcon Berlin、Hexacon、PraSec）双渠道重复输出，跨受众迭代呈现（LM-community-06）；2026 年同时在 Calif 与 TU Graz ISEC 担任研究职务（lm-dec-02、lm-timeline-current-positions，Calif 加入精确时点无来源支撑）。披露遵循结构化时序：QAIC 2026-04-08 报告、04-23 补丁合入、04-27 赏金、收到赏金 30 天后公开以留出补丁分发时间（lm-dec-07）；OEMpocalypse 分部发布（lm-dec-06）。；学术同行评审（NDSS 2025 accepted-papers、USENIX Security 接收）与产业会议评审席位构成外部认可；Pwnie Award Most Underhyped Research（KernelSnitch）/Best Mobile Bug（ChoiceJacking）提名与 GI 博士论文奖提名仅见于个人自述，官方页面未抓取核验（见 tensions/open_questions）。

能力与结果：建立学术发表 + 工业演讲 + 结构化披露的复合传播与披露纪律，使同一技术成果在多受众间放大并经多渠道校验。；2025 年 USENIX Security 两篇 + NDSS 两篇 + Black Hat USA/Asia + Nullcon Berlin 密集演讲；2026 年扩展 CCS/ESORICS/Hexacon/PraSec，学术与工业双线高密度产出；OEMpocalypse 分部发布、QAIC 30 天延迟公开的披露时序

置信度：medium；替代解释：双轨发表节奏可能由团队既有传播策略与 Calif 商业需求共同驱动，而非个体独创；披露时序模式也可能受厂商 SLA 约束而非个体主动性主导。

证据：lm-works-007, lm-works-008, lm-dec-02, lm-dec-06, lm-dec-07, LM-community-05, LM-community-06, lm-timeline-2025-phd-thesis, lm-timeline-current-positions, lm-timeline-2026-conference-papers

## 可迁移与不可迁移

- 可迁移：用 Bootlin 与 CodeQL 对候选内核数据结构做手工源码审计以定位时序信道目标，跨版本迭代验证时序差异的可观测性（LM-SC-02、LM-SC-03）。
- 可迁移：为每项研究产出公开可复现 artifact（GitHub 仓库 + Zenodo DOI + VM 镜像），区分学术 artifact（isec-tugraz 组织）与个人 writeup（lukasmaar 个人）两类仓库归属，降低他人复现门槛（lm-works-003、LM-community-02）。
- 可迁移：以 heap KASLR leak 项目的 'minimize system-specific dependencies, as universal as possible' 为目标，跨版本寻找时序差异更小、更难归因于具体系统的分配路径（LM-SC-03，限定于该单项目）。
- 可迁移：将可机械化的构建脚本、测试环境、硬件虚拟化外包给 AI 辅助工具（Codex），把漏洞定位与利用原语构造保留为人工判断，并主动标注工具适用范围（lm-dec-05、LM-SC-07、r3-001）。
- 可迁移：披露遵循结构化时序（报告→补丁→赏金→延迟公开留出补丁分发时间），并公开致谢厂商响应质量，将披露视为研究流程固定环节而非事后事项（lm-dec-07）。
- 可迁移：同一研究在学术与工业会议双渠道重复输出，跨受众迭代呈现方式以放大同行反馈来源（LM-community-06）。
- 可迁移：选取对 slab 加固（CONFIG_SLAB_BUCKETS、CONFIG_RANDOM_KMALLOC_CACHES）不敏感的原语（page-UAF）作为跨 OEM 复用基础，以覆盖性而非逐机型挖掘为优化目标（lm-dec-06）。
- 不可直接迁移：TU Graz IAIK/isec-tugraz 侧信道研究谱系（Stefan Mangard、Daniel Gruss 及同辈 Juffinger/Draschbacher/Unterguggenberger/Oberhuber 等）与团队既有工具链/artifact 规范，是个体方法学持续演化的组织条件，非个体可迁移资源（lm-works-011、lukas-ext-07）。
- 不可直接迁移：2023 年与 Daniel Gruss 的一次讨论以“内核 resembles hardware”的类比重新框定方向，为 KernelSnitch 设定起点——此类导师/同伴的一次性 reframing 难以复现，是个体路径的偶然起点（LM-SC-01）。
- 不可直接迁移：受硬件资源约束时判断漏洞位于内存管理逻辑还是硬件执行逻辑，再决定是否以 QEMU 虚拟化驱动路径替代物理硬件实验，该判断本身依赖前置内核能力，不可直接作为可迁移方法（lm-dec-04、LM-SC-06；与 tensions 对应）。
- 不可直接迁移：Graz University of Technology 的学位体系（BSc EE + BSc CS + MSc EE + PhD CS）与 TU Graz ISEC 博士训练机会，是个体训练基础，非可迁移做法。
- 不可直接迁移：NDSS/USENIX/CCS 等顶级会议同行评审与产业会议评审席位构成的外部认可回路，依赖个体所处学术-工业网络位置，非纯个体能力产物。

## 复核问题

- 机制4 intermediate_capability：将'把漏洞定位与利用原语构造保留为人工判断'改为明确标注依据 LM-SC-07 作者自述，限定为'作者本人自述其对 QAIC 漏洞的发现与利用原语构造保留为人工判断，未经独立核验'，不扩展为可迁移分工模式；transferable_practices[3] 同步加自述限定语或将其降级为以'作者自述的分工方式'为前提的观察，而非可迁移做法。
- 机制0 alternative_explanation：补充'2023 年与 Gruss 的讨论作为 KernelSnitch 起点依据 LM-SC-01 为 2025 年博客回顾性陈述，存在事后归因风险；该讨论的实际作用与加入团队前已有积累的相对贡献无法从现有材料区分'，使替代解释覆盖回顾性因果风险。
- documented 标注一致性：对仅以个人站点 lukasmaar.github.io 为唯一来源且无独立第三方核验的条目，在反馈/局限说明中明确区分'一手自述 documented'与'会议官方页面或第三方核验 documented'；现有 r1-001 限制说明已部分体现，建议在 overall 层面统一标注，避免读者将个人站点自述等同于独立核验。

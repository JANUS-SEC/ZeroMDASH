# Wang Yong (ThomasKing)：漏洞研究成长分析

- 擅长领域：Android/GPU/虚拟化漏洞
- 独立复核：pass · 86/100

## 成长阶段

- **2015-2016 · 以中文逆向分析记录与 Android 内核系统调用缺陷披露建立公开输出基线**：由移动端逆向分析与对抗技术记录转向可定位系统调用语义缺陷并产出可复现 PoC 与完整披露记录的能力；公开输出由中文技术记录过渡到附 PoC 的漏洞披露。（置信度：high）
  - 证据：wy-op-01, wy-op-02, TK-deep-01, community-thomasking-blog-writeups, community-thomasking-disclosure-2016
- **2017-2018 · 确立 KSMA 架构级原语作为多年核心技术主线**：当旧有覆盖 ptmx_fops 手法因 PAN 失效而无法应对 Android 8.0 时，迁移到借助 ARM MMU 特性构造内核空间镜像映射的通用利用原语，并以 KSMA 命名；同年连续在 Black Hat Asia 2018 与 HITB Amsterdam 2018 两场会议交付同一方法论。（置信度：high）
  - 证据：wy-op-03, thomasking-decision-01-ksma-founding, wang-ext-01, tk-timeline-2018a-bhasia, tk-timeline-2018b-hitb
- **2019 · 由单一内核域扩展到浏览器 JIT 缓解绕过与通用化 rooting 双线**：研究目标由 Android 内核 root 扩展到浏览器引擎 JIT 侧缓解绕过（StructureID Randomization），并明确提出 Universal Android Rooting 目标，把单个 type confusion 漏洞发展为跨设备通用方案；方法路径由 bug-specific/JIT-specific 转向 generic/old-school 的通用化表述。（置信度：high）
  - 证据：wy-op-05, wy-op-06, thomasking-decision-02-browser-jit-branch, wang-ext-02, tk-timeline-2019a-bheu-jit, tk-timeline-2019b-zer0con-typeconfusion, TK-deep-04
- **2020 · 攻击模型由本地提权转向远程 1-click 通用 rooting**：将 Android root 与浏览器沙箱逃逸结合为从 Chrome 沙箱发起的 1-click 远程通用 root 链；标题措辞「Recovering the Attack」可能反映此前链路被修复后的重建尝试，对应漏洞的修复时间在抓取来源中未取得；攻击面扩展与 2019 浏览器方向存在路径依赖而非孤立选题。（置信度：medium）
  - 证据：wy-op-07, thomasking-decision-03-remote-rooting, tk-timeline-2020-poc-zer0con-1click
- **2022 · 将 UAF 单一漏洞类抽象为可命名可复用的利用原语**：把 Use-After-Free 抽象为命名为 Ret2page 的可复用原语（dedicated cache 视角），并引入 bug collision 叙事以多漏洞组合策略构建针对 Android 11 的通用 root 方案；体现从单一漏洞利用向漏洞类利用方法论的固化。（置信度：high）
  - 证据：wy-op-08, thomasking-decision-04-uaf-methodology, tk-timeline-2022a-bhusa-ret2page, tk-timeline-2022b-zer0con-collision
- **2023 · 将 2018 KSMA 方法显式重新启用（Make KSMA Great Again）并迁移到 GPU MMU 子系统**：在 CPU 侧内核缓解增强背景下，主动将攻击面迁移到 GPU 驱动/MMU 子系统；同年围绕 Pixel 6 跨版本 root 与 GPU MMU 在 Black Hat Asia/USA、CanSecWest、MOSEC、POC 共五场会议密集交付，构成有计划的方向切换。（置信度：high）
  - 证据：wy-op-09, thomasking-decision-05-gpu-pivot, wang-ext-03, tk-timeline-2023a-bhasia-pixel6, tk-timeline-2023b-cansecwest-pixel6, tk-timeline-2023c-bhusa-ksma-gpu, tk-timeline-2023d-mosec-gpu-rooting, tk-timeline-2023e-poc-trim, community-thomasking-2023-multiple-venues
- **2024-2025 · 研究方向前移到直接对抗内核 MTE 硬件缓解**：在 ARM 引入 MTE 后，由利用 GPU 绕过 CPU 缓解收敛到直接对抗内存标签缓解；2024 在 2023 版本基础上增量加入 MTE 处理，2025 将 MTE 绕过确立为独立主题并针对启用内核 MTE 的 Google Pixel 实现 one-shot root；在更高缓解门槛下持续改进同一攻击目标。（置信度：high）
  - 证据：wy-op-10, wy-op-11, thomasking-decision-06-mte-pivot, wang-ext-04, tk-timeline-2024-cansecwest-mte, tk-timeline-2025-poc-mte-pixel

## 主要成长机制

### 以硬件/MMU 原语替代一次性漏洞利用的可复用方法论构建

起点：2018 年前后 Android 8.0 引入 PXN/PAN，旧有覆盖 ptmx_fops 的内核利用手法失效；作者此前已具备系统调用语义缺陷定位与 PoC 产出能力（CVE-2015-8966），并存在为对抗 IDA 默认 ELF loader 而自建工具、在内核态 dump 内存与监控系统调用的辅助工具建设取向。

练习与反馈：在遭遇新缓解阻断既有手法时，迁移到架构/MMU 硬件特性层面构造通用利用原语并命名（2018 KSMA 基于 ARM MMU；2022 Ret2page 基于 dedicated cache；2023 Make KSMA Great Again 基于 GPU MMU；2025 借助 MTE 对抗背景）。；同一原语在同年内多会议复用获得采纳（2018 Black Hat Asia 与 HITB 同采纳 KSMA；2023 Black Hat USA、MOSEC、POC、Black Hat Asia/CanSecWest 五场同采纳 GPU MMU 主题），构成会议接受这一外部反馈；README 备注对技术增量与厂商缓解做克制处理（2024 'except for MTE'、2023 'vendor mitigation bypass removed'）显示对披露节奏的反馈响应。

能力与结果：形成原语命名→跨目标适配→跨年度复用的习惯，使方法论可被显式继承而非每次重新构建；表现为同一命名技术（KSMA）跨越 2018 与 2023 两次公开启用并迁移到不同子系统。；2018 KSMA 与 2023 Make KSMA Great Again 共享命名与核心技术主线，覆盖 ARM MMU 与 GPU MMU 两类硬件层；2022 Ret2page 将 dedicated cache 中的 UAF 利用抽象为可命名原语并在多版本 Android 上复用；2024-2025 在同一 one-shot rooting 基线上随 MTE 硬件缓解演进增量迭代利用方案

置信度：high；替代解释：原语重新启用亦可能是因新缓解下旧原语恰好仍适用，而非作者主动将其确立为可复用方法论的决策；多会议重复发表也可能反映议题稀缺下的重复曝光而非方法论复用意图。

证据：wy-op-03, wy-op-08, wy-op-09, wy-op-10, wy-op-11, thomasking-decision-01-ksma-founding, thomasking-decision-05-gpu-pivot, thomasking-decision-06-mte-pivot, tk-timeline-2018a-bhasia, tk-timeline-2022a-bhusa-ret2page, tk-timeline-2023c-bhusa-ksma-gpu, tk-timeline-2024-cansecwest-mte, tk-timeline-2025-poc-mte-pixel

### 以缓解演化为输入的迭代式公开发表

起点：2018 起 KSMA 即明确针对 Android 8.0 的 PXN/PAN；作者公开演讲主题随缓解演进而推进，且在 Zer0con 2019 已出现 Universal 跨设备目标与对抗 KCFI 的表述。

练习与反馈：以新引入的缓解为选题输入，在同一研究基线上增量更新并再次公开发表：PXN/PAN（2018 KSMA）→ KCFI（2019 Zer0con type confusion）→ StructureID Randomization（2019 BH Europe JIT）→ 沙箱逃逸远程化（2020 Chrome Sandbox 1-click）→ UAF/dedicated cache（2022 Ret2page）→ GPU MMU（2023）→ 内核 MTE（2024-2025）。；README 主动标注技术增量（'except for MTE'）与裁剪厂商特定缓解绕过细节（'vendor mitigation bypass removed'），是面向披露与厂商关系的出站反馈处理；同一成果同年多会议复用（CanSecWest 与 BH Asia 同题标注 'Same with'）反映按受众调整输出节奏。

能力与结果：形成以缓解演进为锚点的选题—发表节奏，使研究成果可沿时间轴持续公开而非单次曝光。；2019 明确以前作失效（旧 Structure 喷射预测 StructureID 在随机化启用后失效）作为研究动机，迁移到 generic/old-school 方法；2024 在 2023 版本基础上增量加入 MTE 处理并再次发表，标题与备注显式标注增量关系；2025 将 MTE 绕过由增量项确立为独立演讲主题

置信度：high；替代解释：缓解演进本身是行业共同输入，多研究者均会跟进；作者发表密度可能部分由会议档期与厂商披露周期驱动，而非仅由主动的迭代选题决策驱动。

证据：wy-op-03, wy-op-05, wy-op-06, wy-op-07, wy-op-08, wy-op-10, wy-op-11, thomasking-decision-02-browser-jit-branch, thomasking-decision-03-remote-rooting, thomasking-decision-06-mte-pivot, tk-timeline-2023b-cansecwest-pixel6, tk-timeline-2023e-poc-trim, tk-timeline-2024-cansecwest-mte, tk-timeline-2025-poc-mte-pixel

### 遭遇反分析后自建工具而非依赖通用工具

起点：早期移动端逆向中遭遇加固/混淆应用的反分析手段，通用工具（如 IDA 默认 ELF loader）不足以处理对抗性场景。

练习与反馈：在遭遇反分析技术后，主动构建自有工具：自定义 IDA loader 以对抗默认 ELF loader 限制、内核态辅助工具用于 dump 内存与监控系统调用，并据此判断系统调用由内核实现、hook 也应在内核；GitHub 提供 ARM/Android hook 与注入工具（ELF-ARM-HOOK-Library、ReverseTinytoolDemo、Pixel7_32bit_helper、arm64inject）。需注明 GitHub 仓库无提交时间元数据，工具建设的时间连续性未取得，仅能确认工具成品存在。；作者以「授人以鱼不如授人以渔」表达倾向分享思路让读者构建自有分析工具的取向，并选择公开发表方法论而非仅发布成品；社区反馈以 fork/star 形式出现（Starstruck x2、676 仓库、多工具被 fork），但入站反馈记录（issue/PR 评审、评论）未在抓取来源中出现。

能力与结果：形成「对抗性场景→自建工具→公开方法论」的工作取向，将工具建设作为利用主线的互补输出。；GitHub 提供 ELF hook 三种方法、ARM 逆向工具与 arm64 代码注入工具，与 Android 内核利用主线形成工具—利用互补；《来自高纬的对抗》提出可命名的「维度对抗/升维」分析框架并选择公开发表方法论；About 页以「Pwn everything including myself.」长期稳定呈现自我定位，研究范围界定为 Android/iOS/Browser Vulnerability Research, Reverse Engineering

置信度：medium；替代解释：自建工具可能仅是逆向工程师的常见做法，未必构成可区分的成长机制；GitHub 工具仓库无提交时间元数据，无法证明工具建设与利用主线在时间上同步互构。

证据：TK-deep-01, TK-deep-02, wy-op-12, community-thomasking-github-profile

## 可迁移与不可迁移

- 可迁移：在既有利用手法被新缓解阻断时，迁移到架构/MMU 硬件特性层面构造通用原语并命名，而非逐漏洞重新寻找利用链。
- 可迁移：以缓解演化为选题输入，在同一研究基线上随硬件/软件缓解增量更新利用方案并再次公开发表。
- 可迁移：在公开材料中主动标注技术增量（如「except for MTE」）与裁剪厂商特定缓解绕过细节（如「vendor mitigation bypass removed」），以区分公开部分与未公开部分。
- 可迁移：在 slides 仓库 README 中显式标注同题重复发表（如「Same with (BlackHat Asia 2023)」），便于后续自洽引用与受众区分。
- 可迁移：遭遇对抗性反分析技术后构建自有工具（自定义 loader、内核态辅助工具），并选择公开发表方法论而非仅发布成品。
- 不可直接迁移：2018-2025 持续被 Black Hat Asia/USA/Europe、POC、Zer0con、CanSecWest、MOSEC、HITB 等会议接受，是个人长期稳定输出与会议采纳的结果，不可视为可复制的单次投入。
- 不可直接迁移：KSMA、Ret2page 等命名原语由作者在特定 ARM/GPU 硬件与 Android 版本条件下提出，其复用建立在作者对 ARM MMU、GPU MMU、dedicated cache 等底层特性的掌握之上，非纯方法可迁移。
- 不可直接迁移：对抗内核 MTE 需要相应硬件（Google Pixel 启用内核 MTE）与厂商设备长期绑定，研究者未必具备同等设备与披露通道条件。
- 不可直接迁移：公开工具仓库的社区可见度（Starstruck x2、Arctic Code Vault Contributor、676 仓库）部分取决于早期 GitHub 生态与时间窗口，后续研究者难以复现同等曝光。

## 复核问题

- stages 区间 '2015-2016' 的 evidence_ids 引入 TK-deep-01（来源《来自高纬的对抗》发布日期为 2017-02-24），落在标注区间之外，与证据日期不一致。该阶段结论已由 wy-op-01 支撑，TK-deep-01 在此作为该阶段引用造成区间与证据日期不匹配，建议将 TK-deep-01 移出该阶段或调整区间标注。该问题不构成关键事实错误，不阻断 pass。
- stages 区间 '2015-2016'：将 TK-deep-01 移出该阶段 evidence_ids，或把区间标注调整为与 TK-deep-01 来源日期（2017-02-24）一致的范围，使区间与引用证据日期匹配。
- mechanisms[3].observed_outcomes：将『About 页以「Pwn everything including myself.」长期稳定呈现自我定位』一项从该机制 observed_outcomes 中移除，或改写为仅作为该机制的背景自我定位（不作为机制行为的直接观测结果），使 observed_outcomes 与『遭遇反分析后自建工具』机制的具体行为链条对应。
- mechanisms[1].feedback：把『构成会议接受这一外部反馈』改写为推断性表述（如『可视为会议接受的外部信号，但是否构成驱动原语复用的反馈回路属推断』），避免把同年多会议采纳直接表述为驱动原语复用的反馈因果。

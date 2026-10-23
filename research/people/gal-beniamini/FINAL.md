# Gal Beniamini：漏洞研究成长分析

- 擅长领域：Android/基带/TrustZone 漏洞
- 独立复核：pass · 91/100

## 成长阶段

- **2017-04 · Broadcom Wi-Fi SoC 固件层漏洞发现与利用（首个可观测点）**：首次在一手材料中可观测的固件层深度逆向与堆利用能力：以 dhdutil 提取 ROM、在 IDA 中分析 Thumb-2 二进制、以 NexMon 符号与开源 brcmsmac 驱动对照定位 bcm_parse_tlvs 及其 110+ 交叉引用；hook malloc/free 追踪堆操作并自建堆可视化器；将 TDLS 路径堆溢出转化为重叠空闲块并重定向 freelist 覆盖 timer 结构函数指针，达成无需用户交互的 Wi-Fi 远程代码执行。2017 年前该能力的习得过程无一手材料。（置信度：high）
  - 证据：galbeniamini-works-001, gb-dec-01, gb-timeline-01, gb-community-001
- **2017-04 · 由固件内部漏洞向固件→主机内核提权与硬件 DMA 攻击面扩展**：研究目标由单固件远程代码执行扩展至固件→主机内核提权。软件路径利用 bcmdhd 驱动与固件间 EtherType 0x886C 事件通道，在 WLC_E_PFN_SWC 事件处理中经 SLUB slab 布局后释放并回收覆写含 evt_handler 函数指针表的 wl_priv 结构，以栈转移执行 ROP 链。硬件路径利用 PCIe DMA，跨 Qualcomm Snapdragon 810（Nexus 6P）与 Samsung Exynos 8890（Galaxy S7 Edge）验证 Wi-Fi PCIe 接口 SMMU 缺失或未配置，逆向 dma_info 结构并 hook ROM 中 dma64_txfast 实现任意物理地址写。方法栈由纯软件漏洞链扩展至硬件 DMA 攻击面。（置信度：high）
  - 证据：galbeniamini-works-002, gb-dec-01
- **2017-07 · 选题框架向 TrustZone TEE 迁移与跨厂商对比**：将高价值数据所在、防御滞后与已签名组件撤销机制失效三项标准应用于 TrustZone 可信执行环境，覆盖 Qualcomm QSEE 与 Trustonic Kinibi 两类实现；在 Galaxy S7 Edge 以 Samsung OTP trustlet 已知栈溢出达成 Kinibi 内任意代码执行。writeup 引用 Quarkslab Fernand Lone Sang 对 Samsung SBOOT 的逆向研究与本人先前 QSEE/Widevine 工作，将自身研究标定为前序社区成果的延续。（置信度：high）
  - 证据：gb-dec-02, gb-community-003, gb-community-004
- **2017-09 至 2017-10 · 跨平台迁移至 Apple 与端到端利用链构建**：完成由单组件漏洞到端到端利用链的构建，并向 Apple 报告 7 个漏洞。复用同伴 Ian Beer 的内核漏洞获取内存读写原语，逆向 Apple 专有 Wi-Fi 驱动（AppleBCMWLANCore、AppleBCMWLANBusInterfacePCIe），通过 kalloc zone 分析定位 Wi-Fi 芯片 TCM 在内核地址空间的映射，以基于 RAM 的钩子提取固件 ROM 并自建 Wi-Fi 固件调试器。在 iPhone 7（iOS 10.2）由 Wi-Fi 固件代码执行经 PCIe/DART 达成主机内核任意代码执行：逆向专有 DART（3 级转换、32 位 IO-Space），发现主机以固定上界 0x10000 校验共享环索引导致越界写，通过 flow ring 删除响应泄露布局 IO-Space，覆写 DART 描述符并构造自指映射（writeup 称作 Inception），读取 KTRR 硬件寄存器推断内核地址以击败 KASLR。（置信度：high）
  - 证据：gb-dec-03, gb-dec-04, gb-dec-05

## 主要成长机制

### 自建固件逆向与利用工具链的工具建设实践

起点：接触 Broadcom FullMAC Wi-Fi SoC（BCM4358），可获得 dhdutil、IDA、NexMon 符号与开源 brcmsmac 驱动；需分析运行于独立低功耗处理器上的专有固件二进制（Thumb-2）。

练习与反馈：以 dhdutil 提取 ROM，在 IDA 中分析 Thumb-2 二进制，以 NexMon 符号与 brcmsmac 驱动对照定位 bcm_parse_tlvs 及其 110+ 交叉引用；hook malloc/free 追踪堆操作并自建堆可视化器；将堆溢出链式转化为重叠空闲块并重定向 freelist 覆盖 timer 结构函数指针。在 Apple 平台以基于 RAM 的钩子提取固件 ROM、自建 Wi-Fi 固件调试器，并将 Broadcom 上建立的固件分析方法跨平台复用。；工具输出（定位到 bcm_parse_tlvs、追踪到堆操作、达成远程代码执行）作为技术反馈确认工具正确性；研究启动阶段 Thomas Dullien（@halvarflake）协助方向与文献检索，伦敦办公室同事作为讨论对象（gb-community-001）。

能力与结果：可跨平台复用的固件逆向与堆分析工具链，含堆可视化器与固件调试器。；Broadcom Wi-Fi Part 1 无需用户交互的远程代码执行（galbeniamini-works-001）；Apple 平台固件 ROM 提取与自建 Wi-Fi 固件调试器（gb-dec-03）

置信度：medium；替代解释：样本仅 2017-04 至 2017-10 间 3 个已发表项目、6 个月窗口、仅含成功案例，无 2017 年前活动一手材料；个人工具建设与 Project Zero 团队资源（同事讨论、文献检索支持）未在一手来源中分离，工具链可迁移性可能部分来自团队环境而非纯个人积累。

证据：galbeniamini-works-001, gb-dec-01, gb-dec-03, gb-community-001, gb-timeline-01

### 结构化攻击面选题框架的跨子系统迁移

起点：移动应用处理器（AP）防御持续加固，攻击者转向受审视较少的组件；Project Zero 研究环境与 90 天披露流程。

练习与反馈：按可核验标准筛选研究对象：Wi-Fi 用防御加固反向迁移、部署广度与专有代码复杂度与受审视程度之差（gb-dec-01）；TrustZone 用高价值数据所在、防御滞后（ASLR、栈 cookie、守护页）与已签名 trustlet 撤销机制失效（版本计数器普遍停留于零）（gb-dec-02）；Apple Wi-Fi 用更完整描绘移动生态 Wi-Fi 安全状态（gb-dec-03）。；研究启动阶段 halvarflake 协助方向与文献检索（gb-community-001）；厂商回应被纳入公开记录——Broadcom 告知新版 SoC 改用 MPU 等硬件安全机制，作者据厂商回应评估缓解方向（短引文 a step in the right direction）（gb-community-002）；Samsung 就 kinibi 400 支持 rollback prevention 给出官方书面回复（gb-community-004）。

能力与结果：可跨子系统与跨厂商迁移的攻击面选题标准。；连续三个项目选题（Broadcom Wi-Fi、TrustZone TEE、Apple Wi-Fi）均产出已发表 writeup（gb-dec-01、gb-dec-02、gb-dec-03）

置信度：medium；替代解释：选题节奏可能受 Project Zero 团队选题机制与 90 天披露政策驱动，而非纯个人框架；个人归因与机构归因未在一手来源中分离；3 个项目均成功，缺乏失败选题对照，框架有效性可能被幸存者偏差放大。厂商回应仅作为作者评估缓解方向的已记录输入，作者据此调整后续选题的环节未在一手来源中证实。

证据：gb-dec-01, gb-dec-02, gb-dec-03, gb-community-001, gb-community-002, gb-community-004

### 跨层硬件 DMA/IOMMU 攻击面分析的跨平台复用

起点：已达成 Wi-Fi SoC 固件代码执行（galbeniamini-works-001）；移动 SoC 普遍以 PCIe 连接 Wi-Fi 芯片。

练习与反馈：软件路径以驱动事件通道堆溢出经 SLUB slab 布局、函数指针表覆写与栈转移执行 ROP 链达成主机内核代码执行；硬件路径跨 Qualcomm Snapdragon 810 与 Samsung Exynos 8890 验证 Wi-Fi PCIe 接口 SMMU 缺失或未配置，逆向 dma_info 并 hook dma64_txfast 实现任意物理写；Apple 平台逆向专有 DART，发现主机以固定上界 0x10000 校验共享环索引而非实际环容量导致越界写，借 flow ring 删除响应泄露布局 IO-Space，覆写 DART 描述符引入任意物理地址映射并构造自指映射（writeup 称作 Inception），读取 KTRR 硬件寄存器推断内核地址以击败 KASLR。；跨 Qualcomm 与 Samsung 两类移动 SoC 平台对 Wi-Fi PCIe 接口 SMMU 缺失的相互印证，确认硬件攻击面普遍性（galbeniamini-works-002）；Apple DART 逆向结果与端到端利用链达成确认攻击面分析正确（gb-dec-04）。writeup 显式记录厂商补丁时间线（2016 年中 Broadcom 引入事件校验）与补丁绕过方法（固件 RAM 为 RWX 可 patch 掉校验），Samsung 与 Broadcom 厂商回应被纳入披露报告形成可核验留痕（galbeniamini-works-002、galbeniamini-works-003）。

能力与结果：可跨平台迁移的硬件 DMA/IOMMU 攻击面分析能力，含 SMMU 缺失验证与 IOMMU 转换表操纵。；Part 2 主机内核任意代码执行（galbeniamini-works-002）；Vol.2 Pt.3 iOS 主机内核任意代码执行并向 Apple 报告 7 个漏洞（gb-dec-04）

置信度：medium；替代解释：样本仅 2017 年两类移动 SoC 平台与 1 个 IOMMU（DART）案例且均成功；硬件攻击面普遍性（SMMU 缺失）的跨平台验证可能受当时移动 SoC 普遍未配置 IOMMU 的行业状态驱动，而非个人方法独有；个人归因与 Project Zero 资源未在一手来源中分离。

证据：galbeniamini-works-001, galbeniamini-works-002, galbeniamini-works-003, gb-dec-03, gb-dec-04

### 基于社区既有成果的迭代式研究与披露—反馈记录

起点：已有社区先行研究（Quarkslab Fernand Lone Sang 对 Samsung SBOOT 的逆向）与本人先前 QSEE/Widevine 工作；Project Zero 披露流程。

练习与反馈：在 writeup 中引用 Quarkslab SBOOT 逆向与本人先前 QSEE/Widevine 工作，将自身研究标定为前序社区成果的延续（gb-community-003）；显式记录厂商补丁时间线（2016 年中 Broadcom 引入事件校验）与补丁绕过方法（固件 RAM 为 RWX 可 patch 掉校验）（galbeniamini-works-002、galbeniamini-works-003）；将厂商回应以原文形式纳入公开记录——Broadcom 告知新版 SoC 改用 MPU 等硬件安全机制（gb-community-002）、Samsung 就 kinibi 400 支持 rollback prevention 的官方书面回复（gb-community-004）。；披露后厂商回应被记录：Broadcom 向作者反馈新版 SoC 改用 MPU 等硬件安全机制，作者据厂商回应评估缓解方向（短引文 a step in the right direction）并纳入公开记录；Samsung 就 kinibi 400 支持 rollback prevention 给出官方书面回复并纳入公开记录。披露—厂商回应—作者评估链路已记录；作者据此调整后续选题的环节未在一手来源中证实，故不构成完整反馈闭环。

能力与结果：将社区既有成果、厂商回应与补丁时间线纳入可核验公开记录的研究—披露习惯。；TrustZone writeup 引用前序社区研究与本人先前工作（gb-community-003）；Broadcom 与 Samsung 厂商回应被纳入披露报告（gb-community-002、gb-community-004）

置信度：low；替代解释：该机制主要为记录行为，披露—厂商回应—作者评估链路已记录但作者据此调整后续选题未在一手来源中证实，故不构成完整反馈闭环；记录习惯可能受 Project Zero 披露流程与团队规范驱动而非个人特有；样本仅 2 个厂商交互，可迁移边界据此收窄。

证据：gb-community-002, gb-community-003, gb-community-004, galbeniamini-works-002, galbeniamini-works-003

## 可迁移与不可迁移

- 可迁移：可迁移性边界说明：以下做法基于 2017-04 至 2017-10 间 3 个已发表项目、仅含成功案例，未含失败对照与 2017 年前活动一手材料，个人与机构驱动未分离，不应表述为已充分确立的机制。
- 可迁移：自建可复用底层工具链：以 dhdutil/IDA 加符号与开源驱动对照定位专有固件函数，hook malloc/free 并自建堆可视化器；在闭源平台以基于 RAM 的钩子提取固件 ROM 并自建调试器。
- 可迁移：结构化攻击面选题标准：按防御加固反向迁移、部署广度、专有代码复杂度与受审视程度之差，以及高价值数据所在、防御滞后、撤销机制失效等可核验标准筛选研究对象。
- 可迁移：跨平台与跨厂商方法复用：将固件逆向与硬件 DMA 攻击面分析方法从 Android/Broadcom 迁移至 Apple/Broadcom 与 Qualcomm/Samsung 两类 SoC。
- 可迁移：将厂商回应与补丁时间线以原文形式纳入公开记录，形成可核验留痕。
- 不可直接迁移：Project Zero 团队环境与 90 天披露流程：选题节奏、披露—公开发表循环、同事与文献检索支持（如 halvarflake 协助研究启动）属机构条件，非个人可迁移。
- 不可直接迁移：同伴可用成果：Apple 平台研究依赖 Ian Beer 的内核漏洞作为内存读写原语基础设施，该成果的可用性属团队与同伴条件，非个人可迁移。
- 不可直接迁移：当时移动 SoC 普遍未配置 IOMMU 的行业状态：Wi-Fi PCIe 接口 SMMU 缺失（Snapdragon 810、Exynos 8890）的跨平台验证受益于当时硬件配置状态，非个人方法独有。
- 不可直接迁移：专有固件、驱动与设备的可获得性：Broadcom FullMAC SoC、Apple 闭源驱动与 iPhone 7 设备的可获得性属外部条件。

## 复核问题


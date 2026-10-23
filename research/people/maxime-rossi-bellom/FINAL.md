# Maxime Rossi Bellom：漏洞研究成长分析

- 擅长领域：Android/启动链/安全芯片漏洞
- 独立复核：pass · 90/100

## 成长阶段

- **2020-03（首个可核验公开作品） · 以事后分析与利用复现作为切入点进入移动平台安全研究**：以独立作者身份发布 MediaTek CMDQ 驱动漏洞（CVE-2020-0069）的事后分析，明确声明非原始发现者、不联系厂商，而是基于已流通的 mtk-su 利用与 Xiaomi Redmi 6a 开源内核源码独立逆向 IOCTL 与 DMA 命令格式，构建物理内存读写 PoC，并编写 LD_PRELOAD 的 syscall_hook.c 追踪库拦截并转储 mtk-su 的 IOCTL 命令序列。形成「PoC 加动态追踪」双轨方法与「源码审查加自建工具加利用复现」的研究范式；同时公开批评 MediaTek 修复下发迟滞，建立对披露生态的克制评论立场。（置信度：high）
  - 证据：mr-works-01, mr-works-02, mrb-community-01-mediatek-solo-2020, mrb-ext-01, mrb-dec-01-mediatek-autopsy-2020, mrb-tl-01
- **约 2021 年中至 2022-08（约 18 个月原始研究） · 从独立完成的事后分析转向对单一高价值目标的长期原始研究与团队协作**：与 Damiano Melotti、Philippe Teuwen 组建三人小组，对 Google Pixel Titan M 安全芯片开展约 18 个月原始研究。第一阶段固件逆向并自建 nosclient（三人小组 Maxime Rossi Bellom、Damiano Melotti、Philippe Teuwen 共享的团队协作产物，原生运行于 Android、直接与内核驱动通信），成果于 Black Hat EU 2021 以 whitepaper（标题 "A Titan M Odyssey"）形式发表。随后由黑盒模糊测试（libprotobuf-mutator/Radamsa 经 nosclient）转向仿真模糊测试（AFL++ Unicorn 模式），在 Keymaster 任务中发现单字节越界写（CVE-2022-20233）。利用阶段以单字节写改写请求存储位置，经多次栈迁移 gadget、替换 DestroyAttestationIds 处理器并写入 trampoline，再以 ROP 调用 memcpy 跳过 null-check 实现芯片内任意内存读，泄露 StrongBox 密钥。研究在无调试器、无栈踪迹条件下，通过在主板 UART 引脚焊接线缆获取调试输出。Google 赏金由 10000 美元经密钥外泄 exploit 提升至 75000 美元，2022 年 6 月 Pixel 安全公告修复。（置信度：high）
  - 证据：mr-works-03, mrb-conv-01, mrb-conv-02, mrb-conv-03, mrb-conv-04, mrb-community-02-titanm-vendor-feedback-2022, mrb-community-03-tool-building-nosclient-2022, mrb-ext-02, mrb-ext-03, mrb-ext-04, mrb-dec-02-titanm-reverse-2021, mrb-dec-03-method-pivot-fuzzing-2022, mrb-dec-04-titanm-disclosure-reward-2022, mrb-tl-03, mrb-tl-04, r1-titanm-research-window-2021, r1-bheu-2021-whitepaper-github, r1-bheu-2021-dates
- **2023-08（Android 数据加密研究） · 从单芯片漏洞利用扩展到完整加密栈的系统化分析**：与 Damiano Melotti 发表 Android File-Based Encryption 系统研究（REcon'23），动因是一次外部咨询（主 SoC 已损坏但 Titan M 仍工作的设备能否恢复数据），进而转向系统问题：攻击者拥有广泛软件漏洞时能否攻破 Android File-Based Encryption 的防护。复用 2022 年 Titan M 任意读原语经 nosclient 提取 Weaver 密钥；另一路径经第三方工具 MTKClient 利用 MediaTek BootROM 漏洞绕过安全启动，patch TEEGRIS userboot.so/root_task 与 Gatekeeper 始终接受凭据，再以裁剪版 Magisk root Android、用 Frida hook system_server 泄露 Keymaster 中间 AES 结果，最终以 AES-GCM tag 校验为成功预言机对 scrypt 参数离线暴破。研究显式承认工具局限（暴破脚本性能不足）与「无论链多少漏洞仍须暴破凭据」的方法边界，提供方法认知的清醒复盘，并为 2024 年 Samsung 启动链研究提供前置基础与方法与设备认知基础。（置信度：high）
  - 证据：mr-works-04, mrb-community-04-fbe-conference-and-prior-work-2023, mrb-ext-05, mrb-dec-05-android-encryption-extension-2023, mrb-tl-05, mrb-tl-06
- **2024-06 至 2024-10（Samsung 启动链研究） · 从单芯片研究跨入启动链多层漏洞的链式利用与跨语种多会议发表**：与 Raphaël Neveu 合著 Samsung Galaxy A225F 启动链研究，明确承接 2023 年加密研究对该设备启动流程的认知作为目标选型依据。披露并链式利用 4 个漏洞：CVE-2024-20832（Little Kernel 自定义 JPEG 解析器堆溢出，up_param 分区启动时不校验）加 CVE-2024-20865（Odin 经 GPT 无认证刷写并可改 PIT）实现经 USB 的 Little Kernel 持久代码执行；CVE-2024-20820（Secure Monitor SMC handler 0xc2000526 越界读）加 CVE-2024-20021（SMC handler 0x8200022a 任意物理内存映射，每次最多 1MB、共 8 次）泄露 Secure World 内存含 Android Keystore 密钥。SSTIC 2024 议程页与 presentation 页核验确认 2024-06-06 发表 30 分钟演讲并发布会议全文（actes）；同期 Black Hat USA 2024 演讲仍据 writeup 转述记为 reported。研究单元由单芯片扩展为跨组件 bug 链（bootloader 至 secure monitor），合作者网络由 Damiano Melotti 扩展至 Raphaël Neveu，致谢 Damiano Melotti、Gabrielle Viala。全部 PoC 开源于 GitHub。（置信度：high）
  - 证据：mr-works-05, mr-works-06, mrb-conv-05, mrb-conv-06, mrb-community-05-collaborator-network-2024, mrb-ext-06, mrb-ext-07, mrb-dec-06-samsung-bootchain-sstic-2024, mrb-dec-07-samsung-bootchain-writeup-2024, mrb-tl-07, mrb-tl-08, mrb-tl-09, r1-sstic-2024-presentation-actes

## 主要成长机制

### 以可复用工具栈投入作为研究先导

起点：2020 年 MediaTek 研究即体现工具建设习惯：除 PoC 外编写 LD_PRELOAD syscall_hook.c 追踪库拦截并转储 mtk-su 的 IOCTL 命令序列，并同步开源 PoC 仓库建立可复用资产。Quarkslab 团队环境允许在具体漏洞工作前先投入基础设施构建。

练习与反馈：在每项研究中先构建或改造可复用工具再找漏洞：2022 年三人小组自建 nosclient（原生 Android 上直接与内核驱动通信的客户端）作为 Titan M 模糊测试与利用的基础设施；2023 年 FBE 研究改造 Magisk 使其可从笔记本直接使用并禁用交互授权提示，并复用社区工具 MTKClient、Frida；2024 年延续 nosclient 框架经验支撑跨组件链式 PoC。工具以开源形式对外发布，同时消费他人开源工具，形成工具层面的双向反馈。；工具有效性由「能否复现已知漏洞」判据检验；厂商反馈间接验证工具能力（Google 初期无法复现，团队以增强版 nosclient 提交单字节写并经 UART 日志演示代码执行后获确认）。社区消费侧反馈体现为对 MTKClient 评价为「very easy to use and working almost out of the box」。

能力与结果：形成「先建工具再找漏洞」的研究顺序与跨作品复用自有工具的资产积累习惯，使后续研究不必从零搭建交互通道。；nosclient 在 2022 Titan M、2023 FBE 多篇 writeup 中反复作为基础工具出现；2020 至 2024 各研究均同步开源 PoC 与配套工具；Titan M 单字节写经 nosclient 触发并由 UART 日志证实代码执行

置信度：medium；替代解释：本成长机制仅基于 2020-2024 年已公开作品序列归纳，未发表或未公开的研究工作不在证据范围内；nosclient 为三人小组共享的团队协作产物，将其作为个人信息处理会高估个人独立贡献，工具复用部分亦可能由 Quarkslab 团队资源配置与项目延续性驱动而非个人选择。

证据：mr-works-01, mr-works-02, mrb-conv-02, mrb-community-03-tool-building-nosclient-2022, mrb-dec-02-titanm-reverse-2021, mrb-dec-05-android-encryption-extension-2023, mrb-ext-02

### 以已知漏洞复现作为新方法有效性的判据

起点：2022 年 Titan M 研究面临无调试器、无栈踪迹、无即时副作用的条件，需在不信任新方法前先建立对其有效性的信任。

练习与反馈：在建立仿真模糊测试新方案后，先验证其能否复现已知漏洞以证明方案有效性；在黑盒模糊测试转向仿真模糊测试时，以「黑盒仅覆盖浅层状态」的明确技术判断为依据放弃黑盒路径，并辅以逆向工程成本与模糊测试自由运行成本的权衡论述。；仿真模糊测试在 Keymaster 任务中由 UC_ERR_WRITE_UNMAPPED 崩溃直接发现 CVE-2022-20233；黑盒模糊测试仅复现已知问题并发现两个被评定为不够严重的 NPE 崩溃，形成方法选择的负反馈。

能力与结果：形成以技术约束与可复现性为依据的方法选择能力，而非依赖试错运气；把对已知结果的复现当作建立对新方法信任的手段。；CVE-2022-20233 由仿真模糊测试发现；方法转型直接促成漏洞发现

置信度：medium；替代解释：本成长机制仅基于 2020-2024 年已公开作品序列归纳，未发表或未公开的研究工作不在证据范围内；方法选择的明确技术论证集中于 2022 年单一研究实例，跨时期重复性证据较弱，可能反映该项目的具体约束而非稳定个人习惯。

证据：mrb-conv-01, mrb-conv-03, mrb-conv-04, mrb-dec-03-method-pivot-fuzzing-2022, mr-works-03

### 以信任链锚点为目标而非非信任链关键组件

起点：2020 年 MediaTek 事后分析后，研究选题从单一内核驱动 IOCTL 漏洞转向更高价值目标。

练习与反馈：选择 Titan M 的动机明确表述为「the most secure component of Google's Pixel phones and the anchor to which all the security of the device is ultimately linked」，即以攻击信任链锚点为目标；后续研究沿设备族（Samsung A 系列）与芯片族（MediaTek/Titan M）纵向累积，2024 年 Samsung 启动链研究构建从 USB 经 Little Kernel 至 Secure World 的完整信任链拆解。；目标价值由厂商赏金上限条款（Titan M 代码执行最高 100 万美元）与官方严重等级评定反馈；Android 安全公告对 CVE-2022-20233 评定为 Titan-M 组件、Critical、EoP，构成对目标选择的交叉验证。

能力与结果：形成以信任链根为目标、按信任层级逐层拆解的研究选题习惯。；Titan M 研究获得 Critical 评定与赏金上调至 75000 美元；Samsung 启动链研究单次产出 4 个 CVE 覆盖用户态解析器、认证、Secure Monitor 多层

置信度：medium；替代解释：本成长机制仅基于 2020-2024 年已公开作品序列归纳，未发表或未公开的研究工作不在证据范围内；高价值目标选择亦可能由 Quarkslab 团队战略与厂商悬赏激励驱动，而非纯个人能力判断；2023 年 FBE 研究的触发点为外部咨询，显示选题兼受现实问题驱动而非纯信任链导向。

证据：mrb-dec-02-titanm-reverse-2021, mrb-ext-04, mrb-dec-06-samsung-bootchain-sstic-2024, mrb-dec-07-samsung-bootchain-writeup-2024, mrb-tl-09, mr-works-05

### 跨作品复用自有原语与设备知识作为研究延续基础

起点：2022 年 Titan M 研究产出任意读原语与 nosclient 工具，构成可复用的能力沉淀。

练习与反馈：2023 年 FBE 研究直接复用 CVE-2022-20233 任意读原语与 nosclient 提取 Weaver 密钥，并将 Samsung A22 设备的启动流程认知作为副产物积累；2024 年 Samsung 启动链研究明确以「we had gathered a good knowledge over its boot process during our previous research」作为目标选型依据，形成 2022 Titan M 任意读原语至 2023 加密栈至 2024 启动链完整链的连续证据链。；研究连续性由 writeup 正文显式陈述前作认知作为下作选型理由得到核验；跨作品复用降低新研究的工具与认知启动成本。

能力与结果：形成以既有能力沉淀驱动选题、将上一项研究的副产物作为下一项研究起点的能力累积习惯。；2023 FBE 研究复用 Titan M 任意读原语与 nosclient；2024 Samsung 启动链研究以前作 boot 流程认知为选型依据；研究主题沿设备族与芯片族纵向累积而非孤立选题

置信度：high；替代解释：本成长机制仅基于 2020-2024 年已公开作品序列归纳，未发表或未公开的研究工作不在证据范围内；跨作品复用亦可能由团队固定合作者（Damiano Melotti 跨 2022-2023、Raphaël Neveu 跨 2024）与 Quarkslab 项目延续性驱动，部分能力沉淀为团队资产而非纯个人能力。

证据：mr-works-04, mr-works-05, mrb-conv-05, mrb-community-05-collaborator-network-2024, mrb-ext-05, mrb-ext-06, mrb-dec-05-android-encryption-extension-2023, mrb-dec-07-samsung-bootchain-writeup-2024, mrb-tl-09

## 可迁移与不可迁移

- 可迁移：在具体漏洞工作前先构建可复用交互与追踪工具，并以开源形式沉淀为跨研究资产
- 可迁移：以「能否复现已知漏洞」作为新方法或新工具链有效性的判据，而非直接信任新方案
- 可迁移：以明确技术判断（如黑盒仅覆盖浅层状态）为依据做出方法转型，并辅以成本权衡论述
- 可迁移：将上一项研究的副产物（设备认知、原语、工具）显式作为下一项研究的选型与启动依据
- 可迁移：在缺乏调试器时以可观测副作用（UART 日志、task_print_list、AES-GCM tag 校验）替代直接观测作为成功预言机
- 可迁移：披露谈判中以递进式 PoC（单字节写至完整代码执行至密钥外泄视频）与厂商自身上限赏金条款作为重评依据
- 可迁移：对方法边界保持克制陈述，明确指出工具局限与不可绕过的硬性约束（如仍须暴破凭据）
- 不可直接迁移：Quarkslab 团队环境与三人小组协作（nosclient 为 Maxime Rossi Bellom、Damiano Melotti、Philippe Teuwen 共享的团队协作产物），个人难以独立复现该工具链的构建
- 不可直接迁移：Google Titan M 固件公开可取且厂商提供悬赏与披露流程，这一特定目标与厂商关系不可普遍获得
- 不可直接迁移：Samsung Galaxy A 系列与 MediaTek SoC 组合的特定设备认知积累，依赖长期对同一设备族的研究沉淀
- 不可直接迁移：约 18 个月的单一目标长期研究周期，依赖组织对长期投入的资源容忍
- 不可直接迁移：Quarkslab 内部同行校对与固定合作者网络（Damiano Melotti、Raphaël Neveu、Gabrielle Viala、Philippe Teuwen）构成的反馈回路
- 不可直接迁移：BHEU 2021 / TROOPERS 2022 / Black Hat USA 2022 / REcon'23 / Black Hat USA 2024 / SSTIC 2024 等会议发表渠道，部分议程页抓取受限（HTTP 403/404），发表事实的一手核验条件不可完全复制

## 复核问题

- 建议性修订（不阻断 pass）：tensions 第 5 条与 open_questions 第 3 条并存时，可在最终报告中补一句明确 BHEU 2021 官方议程页一手核验缺失、whitepaper 真实性依赖 GitHub 仓库目录加 writeup 转述加 WebSearch 日期三方间接证实，避免读者将「交叉证实」误读为「一手核验已成立」。

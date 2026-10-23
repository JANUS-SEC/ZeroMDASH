# Damiano Melotti：漏洞研究成长分析

- 擅长领域：Android 与自动化漏洞研究
- 独立复核：pass · 90/100

## 成长阶段

- **约2020–2021年 · 团队固件逆向与背景知识沉淀**：以 Quarkslab 团队形式对 Titan M 安全芯片固件开展约一年半的逆向工程，并以 Black Hat EU 2021 演讲（A Titan M Odyssey）与白皮书形式公开沉淀背景知识，构成后续模糊测试与利用工作的知识基础。Damiano Melotti 作为 2022 年合著 writeup 中“we”的一员参与该阶段；其是否为 2021 年演讲与白皮书的署名作者，在抓取文本中未明确（reported）。（置信度：medium）
  - 证据：damiano-melotti-deep-titan-m-origin-2022, tl-06-bheu-2021-titan-m-odyssey, DM-EXT-04
- **2022年初至2022年8月 · 黑盒到仿真模糊测试转向与自建工具**：自建 nosclient（Android 原生客户端，经内核驱动向 Titan M 发送任意命令），先用自建黑盒模糊测试（libprotobuf-mutator、Radamsa）测试，发现黑盒仅覆盖浅层状态后转向 AFL++ 的 Unicorn 模式仿真模糊测试；经 UC_ERR_WRITE_UNMAPPED 崩溃发现 Keymaster ImportKey 的 1 字节越界写（CVE-2022-20233），2022-03-02 向 Google 报告（documented）。GitHub 按姓名搜索存在署名 Damiano Melotti 的模糊测试工具链提交（dm-community-01，documented），但账号层面未核实，归属为推断。（置信度：high）
  - 证据：damiano-melotti-deep-blackbox-to-emulation-pivot-2022, damiano-melotti-deep-tool-building-nosclient-2022, DM-EXT-01, tl-01-identity-quarkslab-author-page, tl-02-cve-2022-20233-report, tl-03-nosclient-tool, dm-community-01
- **2022年3月至6月 · 约束下的迭代式利用构建与披露闭环**：在缺乏调试器与栈追踪的条件下，通过逐步增大命令并监控 UART 日志（焊线至主板 UART 引脚）定位触发点，以仿真执行 Keymaster DestroyAttestationIds 定位栈中唯一未覆盖的 32-bit 槽，构造栈 pivot 与 ROP，最终外泄 StrongBox AES 密钥；2022-03-20 向 Google 演示代码执行。Google 初称未发现越界写且无法复现安全问题，团队以密钥外泄 PoC 重新提交后，奖励由 10,000 美元提升至 75,000 美元并评 Critical（documented）。（置信度：high）
  - 证据：damiano-melotti-deep-iterative-exploitation-2022, damiano-melotti-deep-disclosure-reward-feedback-2022, DM-EXT-01, DM-EXT-02, tl-02-cve-2022-20233-report
- **2022年下半年 · 研究成果的会议化公开发表**：将 Titan M 研究转化为公开技术输出，于 TROOPERS 2022（6月底，德国）与 Black Hat USA 2022（8月，拉斯维加斯，题 Attack on Titan M Reloaded）演讲，并于 2022-08-11 发布配套 writeup。会议议程页未独立抓取成功，发表事实来自 writeup 正文转述（reported）。（置信度：medium）
  - 证据：tl-04-troopers-bhus-2022-talks, DM-EXT-05, damiano-melotti-deep-titan-m-origin-2022
- **2023年 · 跨题目复用与方法扩展**：由外部求助（设备主 SoC 损坏但 Titan M 可用）触发 Android 文件级加密（FBE）研究，明确限定仅软件攻击假设；复用 CVE-2022-20233 任意读原语构建 Weaver PoC，经 MTKClient 在 MediaTek boot ROM 上构建 Gatekeeper PoC，并以 Frida 钩住 system_server 泄露 Keymaster 中间解密结果；对 Weaver 任务采用先逆向再试错提取密钥。研究于 REcon'23 演讲（writeup 为 documented，会议为 reported）。（置信度：high）
  - 证据：damiano-melotti-deep-disk-encryption-motivation-2023, damiano-melotti-deep-tool-adaptation-magisk-frida-2023, damiano-melotti-deep-collaboration-proofreading-2023, DM-EXT-03, DM-EXT-04, tl-05-fbe-writeup-recon23

## 主要成长机制

### 为受限目标自建专用工具并把工具局限重构为方法优势

起点：Titan M 安全芯片无现成命令接口、无调试器访问，需焊线至主板 UART 引脚维持持久控制台；通用 fuzzer 无法直接驱动目标。

练习与反馈：为目标自建 nosclient（经内核驱动发送任意命令，同时用于模糊测试与利用投递）；评估多种仿真方案后选用 Unicorn，将其“仅 CPU 仿真、无全系统仿真”作为速度与可控性优势而非限制，配合 AFL++ 与 libprotobuf-mutator/Radamsa；2023 年按需改造 Magisk、使用 Frida 钩 system_server、引用 MTKClient，并将 nosclient 与 CVE-2022-20233 任意读原语复用于 Weaver PoC。；工具自身行为（UC_ERR_WRITE_UNMAPPED 崩溃定位漏洞）、仿真可确定性验证（替代调试可见性）、同事校对、厂商对可复现性的质疑迫使补强证据。

能力与结果：形成可跨目标复用的工具链与原语库（nosclient、仿真 harness、任意读原语），以及对工具能力边界的工程化判断。；经仿真模糊测试发现 CVE-2022-20233；nosclient 与任意读原语在 2023 年 Weaver PoC 中复用；MTKClient 改造用于 MediaTek boot ROM 的 Gatekeeper PoC

置信度：high；替代解释：工具建设可能主要由 Quarkslab 团队基础设施与机构资源支撑，writeup 全为合著“we”，个人与团队贡献不可分离；dm-community-01 的 GitHub 提交归属仅依据姓名唯一性推断，账号 /damianomelotti、/DamianoMelotti 均返回 404，未在账号层面核实。跨题目复用亦可由团队累积的资产库解释，而非个人方法论。

证据：damiano-melotti-deep-tool-building-nosclient-2022, damiano-melotti-deep-tool-adaptation-magisk-frida-2023, DM-EXT-01, DM-EXT-03, tl-03-nosclient-tool, tl-05-fbe-writeup-recon23, dm-community-01

### 方法无效时主动转向并以失败记录驱动下一步选择

起点：黑盒模糊测试只能覆盖目标浅层状态；SPI rescue 模糊测试无有意义结果；某已知漏洞因仿真缺乏全系统仿真无法在模拟环境复现；厂商初称未发现越界写且无法复现安全问题。

练习与反馈：黑盒模糊测试覆盖不足后转向仿真模糊测试；SPI rescue 无结果后转向 Keymaster/Identity/Weaver 任务；厂商否认可复现后以密钥外泄 PoC 重新提交；2023 年对 Weaver 任务先逆向再试错提取密钥。；fuzzer 覆盖度（浅层状态可观察）、仿真可复现性（已知 bug 不可复现）、厂商对可复现性与危害等级的判定（质疑迫更强证据）。

能力与结果：在方法低效时放弃并重配努力方向的判断力，以及“以可演示影响回应质疑”的反馈应对模式。；转向 Keymaster 后发现 CVE-2022-20233；补强 PoC 后奖励由 10,000 美元升至 75,000 美元并评 Critical；2023 年 Weaver PoC 经试错提取密钥

置信度：high；替代解释：转向决策可能受团队决策与外部截止线（会议、赏金）驱动，而非个人方法论判断；writeup 中记录的失败可能为事后叙事重构，而非实时决策日志。时间先后（转向后即发现漏洞）不构成因果证明。

证据：damiano-melotti-deep-blackbox-to-emulation-pivot-2022, damiano-melotti-deep-disclosure-reward-feedback-2022, damiano-melotti-deep-tool-adaptation-magisk-frida-2023, DM-EXT-02

### 缺乏调试可见性下的迭代逼近式利用构建

起点：Titan M 无调试器与栈追踪，仅能经焊线的 UART 引脚读取日志；栈 pivot 缺乏现成 gadget。

练习与反馈：逐步增大命令并监控 UART 日志定位触发点；仿真执行 Keymaster DestroyAttestationIds 定位栈中唯一未覆盖的 32-bit 槽；创造性构造栈 pivot gadget；以仿真可确定性替代调试可见性反复验证。；UART 日志的增量响应、仿真执行的确定性验证。

能力与结果：在近似黑盒约束下以仿真替代调试可见性、以日志增量迭代逼近触发点与利用布局的能力。；1 字节越界写经指针重定向、ROP、任意读链外泄 StrongBox AES 密钥；2022-03-20 向 Google 演示代码执行

置信度：high；替代解释：利用链可能依赖 Quarkslab 此前约一年半的团队 Titan M 逆向成果与 Philippe Teuwen 的协作，故“以仿真替代调试可见性”可能为团队级实践而非个人能力；“最具挑战性的一步”为作者自述。

证据：damiano-melotti-deep-iterative-exploitation-2022, DM-EXT-01, tl-02-cve-2022-20233-report

### 先公开沉淀背景知识再推进新成果的发表与协作节奏

起点：Quarkslab 具备 Black Hat/REcon/TROOPERS 发表传统；与 Maxime Rossi Bellom 长期合著；同事参与校对。

练习与反馈：2021 年以白皮书与 Black Hat EU 演讲沉淀 Titan M 背景知识；2022 年以 writeup 与 Black Hat USA 2022/TROOPERS 2022 演讲输出 CVE-2022-20233 研究；2023 年以 writeup 与 REcon'23 演讲输出 FBE 研究。每个研究周期以 writeup 加会议演讲收束。；会议议程采纳（reported，议程页未独立抓取）、同事校对、厂商赏金与严重等级作为外部校验。

能力与结果：将研究转化为可审计公开产物的发表节奏与稳定的合著协作结构。；2022-08-11 发布 Titan M writeup；Black Hat USA 2022 与 TROOPERS 2022 演讲（reported）；2023-08-14 发布 FBE writeup 并于 REcon'23 演讲

置信度：medium；替代解释：发表节奏可能为 Quarkslab 机构规范而非个人习惯；与 Maxime Rossi Bellom 的合著意味着个人发表主动性不可分离；会议“采纳”为作者自述（reported），议程委员会评审未独立核验；2021 年 Black Hat EU 作者署名边界未明。

证据：damiano-melotti-deep-titan-m-origin-2022, damiano-melotti-deep-collaboration-proofreading-2023, DM-EXT-04, DM-EXT-05, tl-04-troopers-bhus-2022-talks, tl-06-bheu-2021-titan-m-odyssey

## 可迁移与不可迁移

- 可迁移：为缺乏现成接口的受限目标自建专用通信客户端，并复用于模糊测试与利用投递。
- 可迁移：方法覆盖不足或无结果时记录失败原因并据此重选目标与方法，而非延长无效路径。
- 可迁移：以可演示影响（PoC 加运行日志）回应厂商对可复现性或危害等级的质疑，推动重新评估。
- 可迁移：在缺乏调试器时以仿真执行的确定性替代调试可见性，配合日志增量迭代逼近触发点。
- 可迁移：跨题目复用既有漏洞原语与自建工具，将一次成果作为后续研究的构建块。
- 可迁移：在每个研究周期以 writeup 与会议演讲公开沉淀背景知识与成果，形成可审计的发表节奏。
- 不可直接迁移：Quarkslab 团队资源与长期合著关系（Maxime Rossi Bellom、Philippe Teuwen；同事校对）。
- 不可直接迁移：约一年半的团队 Titan M 固件逆向积累所形成的背景知识基础。
- 不可直接迁移：Titan M 硬件物理访问条件与 SuzyQable、UART 焊线等硬件手段。
- 不可直接迁移：Google Titan M 赏金计划与厂商反馈通道（特定于 Google/Android 生态）。
- 不可直接迁移：Black Hat/REcon/TROOPERS 等会议发表渠道与机构发表传统。

## 复核问题


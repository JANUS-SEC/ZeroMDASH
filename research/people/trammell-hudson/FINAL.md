# Trammell Hudson：漏洞研究成长分析

- 擅长领域：固件/Boot/硬件漏洞
- 独立复核：pass · 84/100

## 成长阶段

- **1997–2008 · 高性能计算与轻量级内核体系研究阶段**：在 Sandia 国家实验室体系内，与固定合作者（Brightwell、Riesen、Maccabe、Pedretti 等）长期合著，从 Supercomputing '97 系统软件架构（th-001）起步，经历 Cplant 商品集群进入 Top500 第 97 名（th-002，经 top500.org 一手核验见 th-r1-002）、轻量级内核对比与 Catamount/Portals/SeaStar 系列工作（th-004 至 th-008），于 2008 年以 R&D 100 奖项与 SMARTMAP 相关专利为阶段节点（th-009）。可核验产出为多会议并行的高频发表与机构成就；其中 Cplant Top500 #97 与专利 US 8,566,536（th-r1-001，Hudson 为发明人之一，Sandia 为受让人）经一手交叉核验，R&D 100（2008）Catamount 一项仍仅以 Resume 单一来源支撑，自述声誉偏差未消除。将'轻量/可配置内核工程取向'与后续 coreboot/LinuxBoot 可配置固件思路关联属推断性衔接，不纳入本阶段置信依据。（置信度：medium）
  - 证据：th-001, th-002, th-003, th-004, th-005, th-006, th-007, th-008, th-009, th-r1-001, th-r1-002
- **2009–2014 · 消费电子固件逆向过渡与 Mac EFI 安全起点**：由 HPC 体系研究向消费电子固件逆向迁移：启动 Magic Lantern 项目，逆向 Canon EOS 5D Mark II 固件并构建扩展系统（th-dec-01、th-010，起始年 2009 为二手转述，reported）。2014 年于 31C3 发布 Thunderstrike，将固件逆向与底层硬件接口经验迁移到此前较少被攻破的 Apple Mac 平台，确立经 Thunderbolt/Option ROM 写入 SPI flash、替换 Apple 公钥的 bootkit 方法范式（th-works-001、th-011、th-dec-02）。研究受雇主 Two Sigma 赞助（th-employer-twosigma-sponsorship），受 Snare 2012 BlackHat 演讲与机构 MacBook 部署任务触发选题（th-self-entry-trigger-snare-2012），由同事 Thor Simon、Viktor Dukhovni、Larry Rudolph 协助（th-peers-simon-dukhovni-rudolph）。自述因频繁读写 ROM 而自制 Teensy SPI 读写器（th-toolbuilding-teensy-spi），并在实验中因单字节 ROM 改动导致 MacBook 被砖（th-failure-bricked-macbook）。Apple 在 Yosemite 10.10.2 部分修复（th-works-001）。（置信度：high）
  - 证据：th-dec-01, th-010, th-works-001, th-011, th-dec-02, th-employer-twosigma-sponsorship, th-self-entry-trigger-snare-2012, th-peers-simon-dukhovni-rudolph, th-prereq-re-hobby-magic-lantern, th-toolbuilding-teensy-spi, th-failure-bricked-macbook, th-publication-discipline-writeitdown
- **2015–2016 · 攻击线深化、协作扩展与防御转化**：在首次研究被部分修复后选择继续而非收尾：与 LegbaCore 的 Xeno Kovah、Corey Kallenberg 合作，将 Thunderstrike 扩展为可经共享 Thunderbolt 外设跨气隙自传播的固件蠕虫 Thunderstrike 2（BlackHat/DEFCON 23，2015；th-works-002、th-012、th-dec-03、th-community-01-thunderstrike-collab），复用四个已披露固件漏洞（Speed Racer、Darth Venamis、Snorlax/Prince Harming、未签名 Option ROM），并转入 PoC + 厂商披露 + CVE/VU 跟踪的规范披露实践（Mac EFI Security Update 2015-001 / VU#577140 / CVE-2015-3692）。同年与 Larry Rudolph 合著 SYSTOR 2015 EFI bootkit 论文。2016 年于 33C3 发布 Heads，将根信任移入写保护 ROM 并以 TPM 度量启动链（th-works-003、th-013、th-community-07-heads-community）。Heads 自述由多年固件漏洞研究驱动，构成攻击研究对防御工具设计的单向输入（th-works-003 short_quote 'influenced by several years of firmware vulnerability research'）。（置信度：high）
  - 证据：th-works-002, th-012, th-dec-03, th-community-01-thunderstrike-collab, th-peers-simon-dukhovni-rudolph, th-works-003, th-013, th-community-07-heads-community, th-works-005
- **2017–2020+ · 防御规模化、综述整合与跨域工具建设**：2017 年于 34C3 与 Google 的 Ron Minnich 共同主导 LinuxBoot 项目，把 Linux 引入 BIOS（th-014、th-works-005）。2018 年于 35C3 发布 Modchips of the State 综述演讲，整合此前的攻击 PoC（Thunderstrike 系列）与防御（Heads/LinuxBoot）两侧工作（th-015、th-works-004），同年 OSFC 2018 security keynote（th-ext-005），CVE-2018-9062。2019 年于 HITB Amsterdam 公布对 Intel BootGuard Verified Boot 的 TOCTOU 攻击（CVE-2019-11098，edk2/TianoCore 修复），方法论从复用已披露漏洞转向发现新的签名校验时序问题（th-works-004）。同期 GitHub（osresearch）沉淀 spispy（SPI flash FPGA 仿真器）、airbreak（COVID-19 期间约一周内修改 CPAP 固件为临时呼吸机，经临床专家评审）、safeboot 等可复用工具（th-ext-006、th-community-04-airbreak-collab、th-community-05-airbreak-gh-feedback、th-community-06-spispy-tool-reuse）。Heads 项目经社区贡献扩展为多板维护结构（th-community-07-heads-community 中 BOARDS_AND_TESTERS.md 记录各主板维护者）。（置信度：medium）
  - 证据：th-014, th-015, th-works-004, th-works-005, th-ext-005, th-ext-006, th-016, th-community-04-airbreak-collab, th-community-05-airbreak-gh-feedback, th-community-06-spispy-tool-reuse, th-community-07-heads-community, th-community-02-ccc-repeated-venues, th-community-03-gh-profile-output-pattern

## 主要成长机制

### 把一次性发现与逆向成果固化为可复用开源工具及公开 writeup 的发表习惯

起点：自述逆向工程为业余爱好，此前较知名项目为 Magic Lantern（th-prereq-re-hobby-magic-lantern），并称将观察到的逆向技术写入讲稿是因为该技术未见诸正式演讲、希望其他安全研究者可检索到（th-publication-discipline-writeitdown）。

练习与反馈：跨时期重复把一次性逆向/发现转化为长期维护的公开仓库：Magic Lantern（th-dec-01、th-010）→ Teensy SPI 读写器与系统某处植入无限循环辅助逆向的技术（th-toolbuilding-teensy-spi）→ Heads（th-works-003、th-works-005、th-community-07-heads-community）→ spispy（th-community-06-spispy-tool-reuse）→ airbreak（th-community-04-airbreak-collab、th-community-05-airbreak-gh-feedback）→ safeboot（th-ext-006）。GitHub 账号 osresearch 约 220 公开仓库，Pull Shark x2 与 Pair Extraordinaire 成就对应上游 PR 与协作仓库（th-community-03-gh-profile-output-pattern）。；工具经社区在多类真实硬件上验证并报 issue（如 spispy 在 ThinkPad x230、Supermicro X11SSH-F 上被测试，双/四 SPI、写支持不稳定需状态机重写等反馈，th-community-06-spispy-tool-reuse）；airbreak 经专家研究员、生物医学工程师与临床肺科医师评审验证，并参考 Mt. Sinai Hospital 无创通气协议（th-community-04-airbreak-collab）；Heads 形成 issues/PR/Discussions 三通道与 BOARDS_AND_TESTERS.md 多板维护者结构（th-community-07-heads-community）。

能力与结果：形成把个人发现固化为公共可检索、可复现代码库的工程习惯，使他人得以派生、报错与适配不同机型/固件版本，研究产出由一次性 exploit 转为可被社区维护的工具。；Heads 仓库约 3570 commits、211 forks、1.6k stars、244 open issues、44 open PRs（th-community-07-heads-community）；spispy 仓库 413 stars、47 forks、26 open issues、169 commits（th-community-06-spispy-tool-reuse）；airbreak 仓库 95 forks、35 open issues、6 PRs、155 commits，含 CONTRIBUTORS.md 与 Code of Conduct（th-community-05-airbreak-gh-feedback）

置信度：high；替代解释：高仓库数与 star 数亦受其长期（2014–2020+）持续公开产出与固件安全社区同期扩张的共同作用影响，star/fork 数反映社区采用程度，不直接等同于个人能力；其中部分仓库的规模化（如 Heads/LinuxBoot）与 Google 机构资源、开源固件社区同期增长存在共同作用，机构资源与社区贡献权重无法仅凭 GitHub 指标分离（th-ext-007 LegbaCore 被 Apple 收购一事已判 lead_only/unknown，不作能力因果支撑）。

证据：th-prereq-re-hobby-magic-lantern, th-publication-discipline-writeitdown, th-dec-01, th-010, th-toolbuilding-teensy-spi, th-works-003, th-works-005, th-community-03-gh-profile-output-pattern, th-community-04-airbreak-collab, th-community-05-airbreak-gh-feedback, th-community-06-spispy-tool-reuse, th-community-07-heads-community, th-ext-006

### 在同一技术线上重复递进深化并以厂商修复与 CVE 跟踪校正

起点：2014 年 31C3 发布 Thunderstrike 单机 PoC 并受 Apple 部分修复（th-works-001、th-011），雇主 Two Sigma 赞助研究、同事网络协助（th-employer-twosigma-sponsorship、th-peers-simon-dukhovni-rudolph）。

练习与反馈：在首次研究被部分修复后选择继续而非收尾，将 Thunderstrike 扩展为可自传播的 Thunderstrike 2（th-works-002、th-dec-03 自述 'a continuation of my security research on Thunderstrike'）；2018 年 Modchips of the State 综述整合攻防两侧（th-015）；2019 年 BootGuard TOCTOU（th-works-004）。期间持续 CVE 产出：CVE-2014-4498、CVE-2015-5914（th-011）、CVE-2015-3692（th-012）、CVE-2018-9062（th-015）、CVE-2019-0119（th-016）、CVE-2019-11098（th-works-004）。；Apple 在 Yosemite 10.10.2 对原 Thunderstrike 部分修复（th-works-001），并在 Mac EFI Security Update 2015-001（VU#577140 / CVE-2015-3692）对 Thunderstrike 2 剩余问题作进一步响应（th-dec-03）；BootGuard TOCTOU 产生 CVE-2019-11098 并在 edk2/TianoCore 修复（th-works-004）。厂商修复构成可核验的外部反馈，校正其披露与后续研究方向。

能力与结果：形成在单一研究线上反复深化、并以厂商披露流程与 CVE/VU 跟踪校正的研究节奏，由纯 PoC 公开转向 PoC + 厂商披露 + CVE 跟踪的规范披露实践。；连续四届 CCC 演讲（31C3 Thunderstrike、32C3 vector games、33C3 Heads、34C3 LinuxBoot，th-community-02-ccc-repeated-venues）；Thunderstrike → Thunderstrike 2 由单机 PoC 升级为跨气隙自传播蠕虫（th-works-002）；Thunderstrike 2 引入 LegbaCore 外部合作者扩展能力边界（th-community-01-thunderstrike-collab）

置信度：high；替代解释：CVE 数量与厂商修复响应亦受 Apple/Intel 等厂商自身披露流程与时间表影响，不能仅凭 CVE 数推断个人能力增长；同期固件安全成为行业关注点，厂商响应速度整体加快可能放大其披露反馈的可得性。

证据：th-works-001, th-011, th-works-002, th-012, th-dec-03, th-015, th-works-004, th-016, th-employer-twosigma-sponsorship, th-peers-simon-dukhovni-rudolph, th-community-01-thunderstrike-collab, th-community-02-ccc-repeated-venues

### 跨设备与平台迁移既有固件逆向及底层硬件接口经验

起点：HPC 阶段积累轻量级内核、互联芯片（Portals/SeaStar）与底层硬件接口经验（th-001 至 th-009）；自述逆向工程为业余爱好，Magic Lantern 为较知名项目（th-prereq-re-hobby-magic-lantern）。

练习与反馈：把固件逆向与底层硬件接口经验迁移到多类设备：Canon DSLR（Magic Lantern，th-dec-01、th-010）→ Apple EFI/Thunderbolt（Thunderstrike，th-011、th-works-001）→ Intel BootGuard（th-works-004）→ CPAP（airbreak，th-community-04-airbreak-collab）→ SPI flash 读写器/仿真器（Teensy 读写器 th-toolbuilding-teensy-spi、spispy th-community-06-spispy-tool-reuse）。公开作品覆盖 LED 控制（LEDscape）、MAME 矢量显示扩展等跨硬件方向（th-ext-008）。；每类设备的逆向成果经公开 writeup 与开源仓库接收社区反馈；airbreak 经临床专家评审验证（th-community-04-airbreak-collab）；Magic Lantern 作为其本人列出的代表性项目，标志把固件逆向作为长期可重复方法路径（th-dec-01）。

能力与结果：形成可跨设备迁移的固件逆向与硬件接口方法论，使能力由单平台专精转为可重复应用于不同嵌入式/PC 固件的方法路径。；Magic Lantern 作为相机固件扩展系统持续维护（th-dec-01、th-010）；airbreak 约一周内完成对最常见 CPAP 机型固件修改使其具备临时呼吸机能力（th-community-04-airbreak-collab）；spispy 在 ThinkPad x230 与 Supermicro X11SSH-F 等多硬件上被社区测试（th-community-06-spispy-tool-reuse）

置信度：medium；替代解释：跨设备迁移能力部分源于长期逆向实践积累，但 HPC 互联/轻量内核经验与消费电子固件逆向的具体技术重叠程度属推断（th-006 自述可配置 OS 与 LinuxBoot 的关联为推断），HPC 经验对后期固件工作的直接贡献权重无法从现有证据分离。

证据：th-001, th-002, th-003, th-004, th-005, th-006, th-007, th-008, th-009, th-r1-001, th-r1-002, th-prereq-re-hobby-magic-lantern, th-dec-01, th-010, th-011, th-works-001, th-works-004, th-toolbuilding-teensy-spi, th-community-04-airbreak-collab, th-community-06-spispy-tool-reuse, th-ext-008

### 为反复操作自建专用低成本硬件工具

起点：自述因频繁读写 ROM 而自制基于 Teensy 的专用 SPI flash 读写器，并频繁使用在系统某处植入无限循环以辅助逆向的技术（th-toolbuilding-teensy-spi）。

练习与反馈：为反复的固件读写与逆向操作自建硬件工具：Teensy SPI flash 读写器（th-toolbuilding-teensy-spi）→ spispy 基于 ULX3S/ECP5 FPGA 的开源 SPI flash 仿真器（th-community-06-spispy-tool-reuse）→ BootGuard TOCTOU 演示配套自建低成本开源硬件工具（th-works-004，具体型号与既有工具的关联未在该 evidence 中给出，不作同线归属）。；spispy 经社区在多硬件测试并报 issue（双/四 SPI、写支持不稳定需状态机重写等），形成发布工具—社区多硬件验证—反馈缺陷—迭代的回路（th-community-06-spispy-tool-reuse）；fork 表明派生扩展。

能力与结果：形成以可复用硬件工具而非仅一次性 exploit 沉淀逆向操作能力的方法，使反复的 ROM 读写与逆向操作被工具化、可被他人复用。；spispy 仓库 413 stars、47 forks、169 commits（th-community-06-spispy-tool-reuse）；BootGuard TOCTOU 攻击使用低成本开源硬件工具演示，扩展可复现性（th-works-004）

置信度：medium；替代解释：工具建设倾向可能部分源于其 NYC Resistor 等 maker 社区参与与个人硬件爱好（首页概述），非纯研究驱动；BootGuard TOCTOU 配套工具与 Teensy/spispy 的同一性未在 th-works-004 中给出，三者同线归属仅为推断，已限定表述。

证据：th-toolbuilding-teensy-spi, th-community-06-spispy-tool-reuse, th-works-004

### 雇主机构赞助下选题并由同伴网络扩展能力边界

起点：HPC 阶段在 Sandia 体系内与固定合作者（Brightwell、Riesen、Maccabe、Pedretti 等）长期合著（th-001 至 th-009）；2014 年 Mac 固件研究受雇主 Two Sigma 赞助、受 Snare 2012 BlackHat 演讲与机构 MacBook 部署任务触发选题（th-employer-twosigma-sponsorship、th-self-entry-trigger-snare-2012）。

练习与反馈：选题由机构任务与公开前序研究驱动而非抽象兴趣：Sandia 阶段为机构 HPC 项目（th-001 至 th-009），Mac 固件研究由雇主 MacBook 部署与 Snare 演讲触发（th-self-entry-trigger-snare-2012），Thunderstrike 2 引入 LegbaCore 的 Kovah/Kallenberg 协作（th-works-002、th-community-01-thunderstrike-collab），LinuxBoot 与 Google 的 Ron Minnich 共同主导（th-014）。；同事 Thor Simon、Viktor Dukhovni、Larry Rudolph 协助研究，Larry Rudolph 后续成为 SYSTOR 2015 合著者（th-peers-simon-dukhovni-rudolph、th-012）；Heads/LinuxBoot 经社区贡献扩展为多板维护与开源协作结构（th-community-07-heads-community）。

能力与结果：借助机构资源与同伴网络把单人研究扩展为跨机构、跨社区协作项目，能力边界由个人专精扩展为可借外部协作处理更大规模问题。；Thunderstrike 2 与 LegbaCore 合作者共同发布（th-works-002、th-community-01-thunderstrike-collab）；LinuxBoot 与 Google 的 Ron Minnich 共同主导（th-014）；Heads 经社区贡献形成多板分布式维护结构（th-community-07-heads-community）

置信度：medium；替代解释：机构赞助与同伴网络是外部协作条件，不直接构成个人能力成长的因果证据；LinuxBoot 的规模化与 Google 机构资源、开源固件社区同期增长存在共同作用，机构资源与社区贡献权重无法分离（th-ext-007 LegbaCore 被 Apple 收购一事已判 lead_only/unknown，不作能力因果支撑；Google/LegbaCore 合作按 RR6 作为外部条件陈述）。雇主与 Kovah/Kallenberg 是否存在雇佣关系仅推断（th-018），仅共同作者/共同项目可核验。

证据：th-001, th-002, th-004, th-008, th-009, th-r1-001, th-employer-twosigma-sponsorship, th-self-entry-trigger-snare-2012, th-peers-simon-dukhovni-rudolph, th-012, th-works-002, th-community-01-thunderstrike-collab, th-014, th-community-07-heads-community

## 可迁移与不可迁移

- 可迁移：把一次性逆向/发现固化为长期维护的公开仓库与 writeup，并以 writeitdown 心态记录未见诸正式演讲的技术细节，使成果可被同行检索与复现（th-publication-discipline-writeitdown、th-works-005、th-community-03-gh-profile-output-pattern）。
- 可迁移：为反复的底层读写与逆向操作自建可复用专用硬件工具，而非每次依赖一次性 exploit（th-toolbuilding-teensy-spi、th-community-06-spispy-tool-reuse）。
- 可迁移：在单一研究线被部分修复后选择继续深化而非收尾，并以厂商披露流程与 CVE/VU 跟踪校正后续方向（th-dec-03、th-works-002）。
- 可迁移：把固件逆向与底层硬件接口经验作为可跨设备迁移的方法路径，在不同嵌入式/PC 平台间复用（th-ext-008、th-community-04-airbreak-collab）。
- 可迁移：以公开仓库的 issues/PR/Discussions 与多硬件测试报告作为外部反馈通道，校正工具缺陷与适配范围（th-community-06-spispy-tool-reuse、th-community-07-heads-community）。
- 可迁移：在跨学科场景（如 airbreak 对接临床专家与医院协议）引入领域专家评审验证，把固件能力对接非安全领域的合规与安全要求（th-community-04-airbreak-collab）。
- 不可直接迁移：雇主 Two Sigma 赞助 Mac 固件研究与机构 MacBook 部署任务构成的选题触发条件（th-employer-twosigma-sponsorship、th-self-entry-trigger-snare-2012），属特定雇主与时期的外部条件，非个人可迁移做法。
- 不可直接迁移：Sandia 国家实验室 HPC 体系内的固定合作者网络（Brightwell、Riesen、Maccabe、Pedretti 等）与机构资源（th-001 至 th-009、th-r1-001），机构平台与合作者网络的不可复制性属个人特有条件。
- 不可直接迁移：Heads/LinuxBoot 规模化与 Google 机构资源、开源固件社区同期增长的共同作用（th-014、th-community-07-heads-community），机构资源与社区同期扩张的外部条件不可由个人复制。
- 不可直接迁移：Magic Lantern 起始年 2009 为二手转述（th-dec-01、th-010 reported），其项目化时机与 Canon 5D Mark II 2008-11 上市的设备可得性相关，属特定设备窗口条件。
- 不可直接迁移：R&D 100（2008）Catamount 奖项仅以 Resume 单一来源支撑（th-009，RR5 unresolved），该机构成就的可核验性受限，不应作为可迁移能力证据。
- 不可直接迁移：airbreak 在 COVID-19 公共健康危机窗口内的临床专家评审与医院协议对接条件（th-community-04-airbreak-collab），属特定危机时期的跨学科协作条件，非一般可复制做法。

## 复核问题

- stages[3].capability_change：将『2018 年于 35C3 发布 Modchips of the State 综述演讲，整合此前的攻击 PoC（Thunderstrike 系列）与防御（Heads/LinuxBoot）两侧工作（th-015、th-works-004）』改为仅以 th-015 支撑该句；将 th-works-004（BootGuard TOCTOU 2019）移至后续『2019 年』句作为独立攻击线事件，避免用 2019 年攻击 item 支撑 2018 年综述整合陈述。
- mechanisms[3].alternative_explanation：为『NYC Resistor 等 maker 社区参与与个人硬件爱好』补注 evidence 来源，明确该替代解释依据 decisions 维度 identity_check 概述（trmm.net/About 提及周末在 NYC Resistor 教课），且该关联为推断、非直接因果证据；或删除该替代解释中无 evidence 支撑的 NYC Resistor 部分，仅保留『个人硬件爱好』并标注来源为首页概述。
- stages[0].capability_change：将『2008 年以 R&D 100 奖项与 SMARTMAP 相关专利为阶段节点（th-009）』精确化，与 th-r1-001 一手核验结果对齐——专利标题为『Direct access inter-process shared memory』不含 SMARTMAP，建议改为『2008 年以 R&D 100 奖项（Catamount，仍以 Resume 单一来源支撑）与 inter-process shared memory 相关专利（US 8,566,536，经 th-r1-001 一手核验 Hudson 为发明人之一）为阶段节点』，使正文措辞与 tensions[3] 已标注的 SMARTMAP 精确化一致。
- 总体自述集中度限制：在 stages 概述或 mechanisms 层级补一句，说明本研究主要事实来源集中于研究对象自述（trmm.net/Resume/31C3 讲稿），仅 Top500 与专利两项经外部一手交叉核验，其余高价值产出（Magic Lantern 起始年、R&D 100、多数 CVE 与演讲时点）仍依赖自述，因果归因受此限制；该说明可与现有 alternative_explanation 合并，不要求新增 evidence 或重新搜索。
- 边界性语言措辞：mechanisms[1].intermediate_capability『研究产出由一次性 exploit 转为可被社区维护的工具』中『沉淀』类表述（另见 mechanisms[1].repeated_practice『GitHub（osresearch）沉淀 spispy…』）建议替换为中性动词如『积累并公开发布』『维护并公开发布』；tensions[2]『导致 MacBook 被砖』中『被砖』为口语转译，建议改为『导致 MacBook 无法启动』以符合专业书面语规范。此为边界性措辞修订，不构成 verdict 变更。

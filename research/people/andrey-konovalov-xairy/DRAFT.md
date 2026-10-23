# 未通过独立复核

已达到最大修订次数 4；本文件是审计草稿，不得进入跨人物比较。

# Andrey Konovalov (xairy)：漏洞研究成长分析

- 擅长领域：Linux 内核与 USB 漏洞
- 独立复核：revise · 81/100

## 成长阶段

- **2014-08 至 2015-11 · 内核动态检测工具的学位起点与主线贡献**：以 MIPT 本科论文（KASAN，2014-08）为起点构建首个内核动态内存错误检测器相关工作，并于同年承担 MIPT CTF 入门课程教学（2014-09-01），次年在 LinuxCon North America（2015-07-18）与 ISP RAS（2015-11-23）分别就 KASAN 与 KTSAN 作公开报告，开始向 Linux 内核主线提交 KASAN/KCOV 补丁（2015-08-03）并向 syzkaller 贡献（2015-10-13）。学位论文主题与后续公开活动均围绕内核动态检测工具，研究主线的早期方向与内核内存安全工具建设一致。（置信度：high）
  - 证据：ak-timeline-01, ak-timeline-02, ak-timeline-03, ak-timeline-04, ak-timeline-05, ak-timeline-06, ak-timeline-08, xairy-works-001, xairy-works-003, xairy-comm-01, xairy-comm-02, xairy-comm-03, xairy-comm-07
- **2016-02 至 2017-08 · USB 与网络攻击面的漏洞发现与利用输出**：从检测工具建设转向使用 fuzzer 发现并利用真实漏洞：以 vUSBf 发现 CVE-2016-2384（USB MIDI double-free）并用 Facedancer21 复现（2016-02-22，自述首个内核 exploit），此后将工具切换到 syzkaller 并将攻击面扩展到网络协议栈（CVE-2017-6074 DCCP、2017-02-26；CVE-2017-7308 packet sockets、2017-05-10；CVE-2017-1000112 UFO、2017-08-13），开始跨 CVE 复用利用技术并借鉴他人公开技巧，发表渠道从个人站点扩展到 Project Zero guest 平台，对外可见度提高。（置信度：high）
  - 证据：xairy-works-002, xairy-works-004, xairy-dec-03, xairy-dec-04, xairy-dec-05, ak-timeline-07, ak-timeline-09, ak-timeline-10, ak-timeline-11, external-01, external-02, external-05
- **2018-06 至 2021-11 · 工具方法论的系统化与 USB 设备侧 fuzzing 工具链建设**：研究对象从单点漏洞扩展到方法论与工具基础设施：在 DC4822 Meetup（2018-06-23）与 OffensiveCon（2019-02-15）作 syzkaller 与 USB fuzzing 方法论报告，启动 Raw Gadget 项目（2020-02-06）作为 USB 设备侧仿真的自有内核模块，向 Arm MTE/Tag-Based KASAN 方向扩展（2020-07-07、2021-10-01），并在 HackMag 发表 Linux 内核 fuzzing 综述（2021-11-22），将分散工作整理为系统化方法学叙述。（置信度：high）
  - 证据：xairy-works-006, xairy-works-007, xairy-comm-04, xairy-dec-06, ak-timeline-12, ak-timeline-13, ak-timeline-14, ak-timeline-15, ak-timeline-16, conv-01, conv-02, conv-03, conv-04, external-04, external-07
- **2022-05 至 2024-02 · 外部网络 fuzzing 的自实现、失败记录与 USB 主机端硬件依赖降低**：首次自实现 fuzzer：将 syzkaller 扩展到外部网络 fuzzing（2022-05-02），引入 syz_emit_ethernet/syz_extract_tcp_res 伪系统调用，修补 TUN/TAP 使 netif_receive_skb 立即处理以修复 KCOV 覆盖追踪；在 BSides Munich（2022-05-16）报告 Raw Gadget；在 ThinkPad X1 Carbon 上启用 xDCI 控制器以仿真 USB 设备（2024-02-22），将 USB 主机端 fuzzing 从外部硬件依赖（Facedancer21/Raspberry Pi）降低到笔记本内置 xDCI 复用。研究平台仍以 x86-64 笔记本为主，尚未扩展到 ARM/Android。（置信度：high）
  - 证据：xairy-works-007, xairy-works-008, xairy-dec-06, xairy-dec-07, ak-timeline-17, conv-05, conv-06, conv-07, conv-08, r1-syzkaller-external-network-verbatim, r1-hackmag-three-stages-verbatim, r2-bsides-munich-2022-duration
- **2024-09 至 2026-09 · 分配器内部研究与 ARM/Android 平台扩展及教学输出**：研究主题扩展到利用底层（SLUB 分配器内部与 slab 整形，2024-09-16），研究平台从 x86-64 扩展到 ARM/Android（Pixel 8 KGDB 调试，2025-07-28），并在 SAFACon（2025-05-03）演示通过 syzkaller 复现 CVE-2024-53104。教学输出从单一 talk 扩展为 workshop（BalcCon2k25 'Attacking USB with Raw Gadget'，2 小时，2025-09-19）与多日培训（RomHack 2026 'Exploiting the Linux Kernel'，4 日，2026-09-28）。能力从单主题研究者扩展为面向利用开发者的方法学讲授者与多日培训输出者。（置信度：high）
  - 证据：xairy-works-009, xairy-works-010, xairy-works-011, xairy-dec-07, xairy-comm-08, ak-timeline-18, ak-timeline-19, ak-timeline-20, external-06, r2-balccon2k25-2025-duration

## 主要成长机制

### 当现成工具不足以覆盖新目标子系统时自建内核上游基础设施

起点：2014-2015 年以 KASAN/KTSAN 学位论文与 Linux 内核主线补丁贡献起步，已建立内核动态检测工具的开发与上游协作经验；至 USB 与外部网络 fuzzing 阶段，syzkaller 与现有 USB fuzzer 无法直接覆盖目标子系统。

练习与反馈：每次进入新攻击面时先识别现成工具的能力边界，再向内核或 fuzzer 上游新增基础设施：为 USB 设备侧编写 raw-gadget 接口、在 syzkaller 之上实现 USB 专用模块、在 KCOV 中加入从后台线程与 softirq 收集覆盖的能力以处理 USB 报文在内核全局线程中处理的场景、改造 KMSAN 以检测经网络与 USB 等外部接口的泄漏；并将此做法提炼为方法论经验：以内核代码而非文档为依据编写 fuzzer。；补丁经 maintainer 评审合入主线即外部反馈的直接形式；自述 'After a few minutes of running syzkaller with these descriptions I started getting kernel crashes.' 提供数分钟级的崩溃反馈；为支持外部网络 fuzzing 修补 TUN/TAP 使 netif_receive_skb 立即处理以修复 KCOV 覆盖追踪，该补丁最终合入主线构成对工具改动的上游认可。

能力与结果：形成可迁移的内核上游工具建设能力：识别现成 fuzzer 对目标子系统的覆盖缺口，编写伪系统调用（syz_emit_ethernet、syz_extract_tcp_res）与 syzlang 描述，并按覆盖报告迭代修订；区分个人原创贡献（raw-gadget、syzkaller USB 模块、KCOV 远程覆盖、KMSAN 外部接口扩展）与对 Google 主导项目（KASAN、syzkaller）的协作贡献。；Raw Gadget 项目于 2020-02-06 启动（ak-timeline-14），合入 Linux 内核主线 5.7 版本并被 syzkaller 官方文档引用为外部 USB fuzzing 关键依赖（r4-raw-gadget-mainline-and-syzkaller-doc）；为外部网络 fuzzing 修补 TUN/TAP 以修复 KCOV 覆盖追踪，补丁最终合入主线（xairy-works-007）；自实现外部网络 fuzzer 并产出跨 SCTP/DCCP/TCP/IPv6/XFRM 的多类 bug 与多个 CVE（xairy-works-007）；KASAN/KCOV 自 2015-08-03 起持续向内核主线贡献，覆盖 KASAN、KCOV、USB Raw Gadget 等子系统（xairy-comm-02、ak-timeline-04）；syzkaller 自 2015-10-13 起持续贡献 external network、USB 扩展与 syzlang 描述（xairy-comm-03、ak-timeline-05）

置信度：high；替代解释：对 KASAN/KCOV/syzkaller 的协作贡献部分受 Google 雇佣期工作资源支持（/about 自述在 Google 工作 5 年从事相关子系统与工具），其主线贡献频率与持续性与大厂雇员身份可能相关，并非纯个人独立研究；但 raw-gadget、syzkaller USB 模块、KCOV 远程覆盖、KMSAN 外部接口扩展由本人自述为原创贡献（conv-02），与协作贡献可区分。

证据：xairy-works-001, xairy-works-003, xairy-works-004, xairy-works-008, xairy-comm-02, xairy-comm-03, conv-02, conv-03, ak-timeline-01, ak-timeline-04, ak-timeline-05, ak-timeline-14, r4-raw-gadget-mainline-and-syzkaller-doc

### 攻击面迁移中的技术复用与方法学抽象

起点：2016-02 以 vUSBf 与 Facedancer21 完成 USB MIDI double-free 的发现-复现-利用闭环（CVE-2016-2384），掌握 double-free 利用与外部可达 USB 攻击面的研究范式。

练习与反馈：在迁移到新攻击面时复用并抽象已掌握的技术：CVE-2017-6074（DCCP double-free）复用 CVE-2016-2384 的双重释放利用技术，并参考 Philip Pettersson 的 CVE-2016-8655 SMEP/SMAP 绕过技巧；CVE-2017-7308 在 packet sockets 越界写中复用堆整形、覆盖 retire_blk_timer 改写 CR4 关闭 SMEP/SMAP、覆盖 xmit 指针跳转用户态 commit_creds(prepare_kernel_cred(0)) 的提权链，并通过 dmesg 的 'Freeing SMP' 绕过 KASLR；后续将三阶段工作（系统调用网络→外部网络→USB 设备侧）整理为方法学综述。；CVE-2017-7308 以 guest post 形式被 Project Zero 博客采纳发布（external-01 明确为 guest 而非团队成员），构成外部团队对其网络 fuzzing 成果的认可；2017 年内连续公开 CVE-2017-7308（2017-05-10）与 CVE-2017-1000112（2017-08-13）两个网络子系统 exploit 形成公开披露的稳定节奏；CVE-2017-18344（timer subsystem，发表于 2018-08-09）为独立 exploit，不归入 2017 年网络子系统序列。

能力与结果：形成跨攻击面可迁移的漏洞利用范式：double-free/OOB 写→堆整形→覆盖函数指针或定时器→关闭 mitigation→提权，并能按目标子系统调整 syzlang 描述与触发路径。；CVE-2016-2384 USB MIDI double-free 利用（2016-02-22）；CVE-2017-6074 DCCP double-free 利用，复用 CVE-2016-2384 技术并借鉴 CVE-2016-8655 SMEP/SMAP 绕过（2017-02-26）；CVE-2017-7308 packet sockets 越界写利用，含堆整形、retire_blk_timer 改写 CR4、xmit 指针跳转、KASLR 绕过链（2017-05-10）；CVE-2017-1000112 UFO packets 越界利用（2017-08-13）；CVE-2017-18344 timer subsystem arbitrary-read 利用（2018-08-09，独立于 2017 网络序列）

置信度：high；替代解释：2017 年内连续公开多个 exploit 既可能反映个人能力跃升，也可能部分由 Google 雇佣期对网络接口安全测试的内部目标驱动；CVE-2017-7308 文章自述 'Lately I've been spending some time fuzzing network-related Linux kernel interfaces with syzkaller' 并公开呼吁社区参与 syscall 描述与内核测试，目标设定可能与雇佣期工作相关，但一级来源未给出内部目标与个人研究的比例。

证据：xairy-works-002, xairy-works-004, xairy-works-006, xairy-works-007, xairy-dec-03, xairy-dec-04, xairy-dec-05, ak-timeline-07, ak-timeline-09, ak-timeline-11, r4-cve-2017-18344-timer-subsystem-2018, external-01, external-02

### 公开记录失败、路径转向与知识缺口的承认

起点：2022-05-02 在外部网络 fuzzing 工作中首次自实现 fuzzer，自述此前 'I had never implemented a fuzzer myself.' 与 'I also had no knowledge about syzkaller nor the inners of the Linux kernel network subsystem.'，明确承认知识缺口。

练习与反馈：在 writeup 中公开记录失败与转向：外部网络 fuzzing 逐字自述 'Sadly, to find that one bug to take over the Internet — I failed. But I did manage to find a one-shot RCE in a non-public kernel flavor.'；在 ThinkPad xDCI 工作中记录 net2280→xHCI role switch→PMC→PSF→efivarfs/chipsec→SPI patch 的多路径失败与转向序列，并对失败路径作正向价值评估（'I nevertheless enjoyed learning about PCH, PMC, and PSF'）；对既往硬件事故（SPI 夹烧毁主板）显式引用为当前改用焊接 SPI 插座的原因。；自实现的 fuzzer 在数分钟内产生崩溃（CVE-2017-7308 阶段）与外部网络 fuzzing 产出多类 bug 构成正反馈；失败路径的记录本身不直接产生外部反馈，但通过公开 writeup 形成可被社区引用的转向叙事。

能力与结果：形成对失败路径的结构化记录与复用能力：将每条失败路径的局限识别为可复述技术节点，并据此调整后续方法选择（如改用焊接替代 SPI 夹）。；在 syzkaller-external-network writeup 中逐字承认未达成寻找可远程利用内核漏洞的目标（r1-syzkaller-external-network-verbatim 逐字引文 'Sadly, to find that one bug to take over the Internet — I failed.'）；ThinkPad xDCI 工作记录多路径失败-转向序列并最终以 SPI 镜像打补丁 reflashing 成功（conv-05）；将失败路径的知识收益（PCH/PMC/PSF）作正向记录（conv-08）；将既往硬件事故复用为当前方法选择依据（conv-07）

置信度：high；替代解释：公开承认失败与转向的写作习惯可能部分由个人 writeup 风格驱动，而非系统性研究方法；但其失败路径的具体技术节点（net2280 glitch、Boot Guard 失败、PMC 寄存器自锁、PSF MASKLOCK、EFI_WRITE_PROTECTED）具有可核验的具体性，难以仅以写作风格解释。

证据：xairy-works-007, xairy-works-008, xairy-dec-06, xairy-dec-07, conv-05, conv-07, conv-08, r1-syzkaller-external-network-verbatim

### 在多年多会议反复报告与修订并系统化为教学输出

起点：2015-07-18 LinuxCon KASAN 报告与 2015-08-03 起的内核主线补丁贡献同步推进，形成做研究-公开发表-接受评审-继续贡献的早期输出习惯；与 Alexander Popov 于 2020-11-04 共建 Linux Kernel Security 频道构成持续信息分发渠道。

练习与反馈：将同一研究主线在多年多个会议反复报告与修订：KASAN/KTSAN 主题自 2015 LinuxCon 与 ISP RAS 起，经 LSS 2021/2022/2024 多届延续并演进到 MTE/SLUB；USB fuzzing 主题自 OffensiveCon 2019 经 BSides Munich 2022、SAFACon 2025、OFFZONE 2025、BalcCon2k25 反复报告；在此基础上将多年研究链整理为教学输出。；会议主办机构对其议题的重复接受（LSS 多届、OffensiveCon、BSides、SAFACon、BalcCon2k25、RomHack）构成外部对议题的接受反馈；长期阅读并收集 fuzzing 相关文献后整理为演讲（'I've been reading and collecting fuzzing-related publications. So, I organized them and turned into a talk.'）构成输入-输出的可观察循环。

能力与结果：形成将分散研究整理为系统化教学课程的能力：把单点漏洞研究扩展为覆盖提权、x86-64 mitigation 绕过、高级 slab/堆 exploit 与分配器内部的 4 日培训。；LSS 多届接受其内核安全议题（2021/2022/2024，xairy-comm-07、external-04、external-06）；USB fuzzing 主题在 OffensiveCon 2019、BSides Munich 2022（30 分钟）、SAFACon 2025、BalcCon2k25（2 小时 workshop）反复报告（xairy-comm-04、xairy-comm-08、r2-bsides-munich-2022-duration、r2-balccon2k25-2025-duration）；RomHack 2026 'Exploiting the Linux Kernel' 4 日培训（xairy-works-011）；与 Alexander Popov 共建并持续运营 Linux Kernel Security 频道（xairy-works-005、xairy-comm-06、xairy-dec-08）

置信度：high；替代解释：反复报告与教学输出部分受会议 CFP 与培训市场的外部结构驱动（会议需要稳定 speaker、培训需要课程化内容），并非纯个人主动选择；但同一研究主线在多年多会议持续被接受，且从 talk 演进到 workshop 再到 4 日培训的形式递进，具有个人研究深度的可观察支撑。

证据：xairy-comm-01, xairy-comm-02, xairy-comm-04, xairy-comm-06, xairy-comm-07, xairy-comm-08, xairy-works-005, xairy-works-006, xairy-works-009, xairy-works-011, xairy-dec-08, ak-timeline-02, ak-timeline-10, ak-timeline-13, ak-timeline-17, ak-timeline-18, ak-timeline-20, conv-04, external-07, r2-bsides-munich-2022-duration, r2-balccon2k25-2025-duration

### 降低 USB 硬件依赖与研究平台扩展

起点：2016-02 以 Facedancer21 物理板与 vUSBf 进行 USB fuzzing，研究依赖外部硬件；2020-02-06 启动 Raw Gadget 项目作为 USB 设备侧仿真的内核模块，为降低外部硬件依赖提供软件基础。

练习与反馈：反复以软件化方案替代外部硬件依赖：从 Facedancer21 物理板到 Raw Gadget 软件接口，再到启用 ThinkPad X1 Carbon 内置 xDCI 控制器以仿真 USB 设备，使 USB 主机端 fuzzing 可在笔记本上 without any external hardware 进行；同时向 ARM/Android 平台扩展研究（Pixel 8 KGDB、Arm MTE）。；Raw Gadget 合入 Linux 内核主线 5.7 并被 syzkaller 官方文档引用为外部 USB fuzzing 关键依赖（r4-raw-gadget-mainline-and-syzkaller-doc），构成上游对其工具建设的认可；ThinkPad xDCI 工作中向 Maxim Goryachy（low-level platform security）、Sergey Korablin（焊接）、Dmytro Oleksiuk（FT2232H）、Tyler Nguyen（x1c6-hackintosh）按所需能力类型求助，构成跨专长的同伴求助网络反馈。

能力与结果：形成跨硬件平台的研究工具适配能力：能在 x86-64 笔记本上复用内置 xDCI，能在 Pixel 8 上构建并刷入自定义内核经 KGDB 调试，并指出方法可适配其他 Pixel 机型。；Raw Gadget 合入 Linux 内核主线 5.7 并被 syzkaller 官方文档引用（r4-raw-gadget-mainline-and-syzkaller-doc）；ThinkPad X1 Carbon 启用 xDCI 使 USB 主机端 fuzzing 无需外部硬件（xairy-works-008、conv-05）；Pixel 8 内核 KGDB 调试方法（xairy-works-010、ak-timeline-19）；Arm MTE/Tag-Based KASAN 研究方向（ak-timeline-15、ak-timeline-16）；SAFACon 2025 通过 syzkaller 复现 CVE-2024-53104（xairy-comm-08）

置信度：medium；替代解释：/about 自述支持 Google 向 Android 交付 Arm Memory Tagging Extension，但其个人在 Arm MTE 内核主线化中的具体角色未由独立来源说明，研究方向中个人选择与雇主工作的比例不可判定；Arm MTE 方向可能部分由雇主在 Android 上的工作需求关联，非纯个人研究方向选择。

证据：xairy-works-002, xairy-works-007, xairy-works-008, xairy-works-010, xairy-dec-04, xairy-dec-07, ak-timeline-14, ak-timeline-15, ak-timeline-16, ak-timeline-19, conv-05, conv-06, r4-raw-gadget-mainline-and-syzkaller-doc

## 可迁移与不可迁移

- 可迁移：以内核代码而非文档为依据编写 fuzzer（conv-03），可在任何缺乏完整文档的子系统复用。
- 可迁移：识别现成 fuzzer 对目标子系统的覆盖缺口，编写伪系统调用与 syzlang 描述，并按覆盖报告迭代修订（xairy-works-007、conv-02）。
- 可迁移：在 writeup 中公开记录失败路径的具体技术节点与转向决策（conv-05、r1-syzkaller-external-network-verbatim），使失败可被后续研究者复用。
- 可迁移：将同一研究主线在多年多会议反复报告与修订，再整理为系统化教学课程（xairy-comm-04、xairy-works-011）。
- 可迁移：按所需能力类型向对应专家求助（平台底层安全、硬件焊接、FT2232H 用法、BIOS 解锁），并明确说明每位求助对象的专长依据（conv-06）。
- 不可直接迁移：在 Google 工作 5 年的资源支持（/about 自述），可能为其 KASAN/KCOV/syzkaller 主线贡献与 Arm MTE 方向提供雇佣期工作资源，非纯个人独立研究条件。
- 不可直接迁移：MIPT 学位论文以 KASAN/KTSAN 为题的学术框架（ak-timeline-01、ak-timeline-08），使早期工具建设与学位研究一体化，属特定学术机构与时机条件。
- 不可直接迁移：Raw Gadget 合入 Linux 内核主线 5.7 的上游认可（r4-raw-gadget-mainline-and-syzkaller-doc），依赖主线 maintainer 评审与时机，非可主动复制的个人成果。
- 不可直接迁移：ThinkPad X1 Carbon 内置 xDCI 控制器的可用性（xairy-works-008、conv-05），依赖特定型号笔记本的硬件特性与 BIOS/Boot Guard 状态，非通用研究条件。
- 不可直接迁移：Pixel 8 内核 KGDB 调试（xairy-works-010）依赖具体设备的 bootloader 解锁与内核构建能力，可适配性受机型限制。
- 不可直接迁移：与 Alexander Popov 共建 Linux Kernel Security 频道（xairy-works-005、xairy-comm-06）依赖特定同伴协作关系，非可主动复制的信息分发渠道。

## 复核问题

- Mechanism 5 alternative_explanation 末句 'Arm MTE 方向可能部分由雇主在 Android 上的工作需求关联，非纯个人研究方向选择' 未完全执行 round 4 RR5：RR5 明确要求删除 '由 Google 雇主工作需求驱动' 的推断，改为 '个人选择与雇主工作的比例不可判定'。综合在写入 '比例不可判定' 后追加 '可能部分由雇主...工作需求关联'，仍在推断雇主驱动方向，与 tensions 第 8 条 '不应据其推导 Arm MTE 演讲主题由雇主驱动' 直接冲突，构成机制内自相矛盾。
- Mechanism 2 alternative_explanation 使用 '个人能力跃升'。round 4 RR1 已判定 '跃升' 带宣传色彩并要求删除（Stage 2 capability_change 已据此改为 '对外可见度提高'），但 Mechanism 2 仍保留 '跃升'，违反同一语言规范对全部自撰字段的适用要求。
- Mechanism 5 alternative_explanation：删除末句 'Arm MTE 方向可能部分由雇主在 Android 上的工作需求关联，非纯个人研究方向选择'，使整条 alternative_explanation 与 tensions 第 8 条及 round 4 RR5 一致，仅保留 '/about 自述支持 Google 向 Android 交付 Arm Memory Tagging Extension，但其个人在 Arm MTE 内核主线化中的具体角色未由独立来源说明，研究方向中个人选择与雇主工作的比例不可判定'。原措辞 '可能部分由雇主...工作需求关联'；改写方向：删除该推断性表述，不追加任何雇主驱动方向的措辞。
- Mechanism 2 alternative_explanation：将 '2017 年内连续公开多个 exploit 既可能反映个人能力跃升，也可能部分由 Google 雇佣期对网络接口安全测试的内部目标驱动' 中的 '个人能力跃升' 改为中性陈述（如 '个人能力扩展' 或 '研究输出增加'）。原措辞 '个人能力跃升'；改写方向：删除 '跃升' 这一宣传性表述，与 Stage 2 capability_change 同步采用 '扩展/提高' 类中性技术动词。
- Stage 5 evidence_ids：xairy-dec-07（2024-02-22 ThinkPad xDCI）落在 Stage 4 period（2022-05 至 2024-02）内且已在 Stage 4 evidence_ids 引用，属跨阶段重复归属；将 xairy-dec-07 从 Stage 5 evidence_ids 移除，或在 Stage 4/5 之间明确该证据仅支撑 Stage 4 事件（ThinkPad xDCI 工作于 2024-02-22 完成），Stage 5 仅引用其实际支撑的事件（若无可从 evidence_ids 删除）。
- Stage 1 evidence_ids：ak-timeline-08 与 xairy-works-003（均 2016-08-01 硕士论文 KTSAN）落在 Stage 2 period（2016-02 至 2017-08）内，Stage 1 period 止于 2015-11；将 ak-timeline-08 与 xairy-works-003 从 Stage 1 evidence_ids 移除，归入 Stage 2 evidence_ids（硕士论文 KTSAN 与 Stage 2 的 USB/网络攻击面工作同期）。
- 结论引用缺失或已作废：['xairy-works-006', 'xairy-works-007', 'xairy-comm-04', 'xairy-dec-06', 'ak-timeline-12', 'ak-timeline-13', 'ak-timeline-14', 'ak-timeline-15', 'ak-timeline-16', 'conv-01', 'conv-02', 'conv-03', 'conv-04', 'external-04', 'external-07']
- 结论引用缺失或已作废：['xairy-works-007', 'xairy-works-008', 'xairy-dec-06', 'xairy-dec-07', 'ak-timeline-17', 'conv-05', 'conv-06', 'conv-07', 'conv-08', 'r1-syzkaller-external-network-verbatim', 'r1-hackmag-three-stages-verbatim', 'r2-bsides-munich-2022-duration']
- 结论引用缺失或已作废：['xairy-works-001', 'xairy-works-003', 'xairy-works-004', 'xairy-works-008', 'xairy-comm-02', 'xairy-comm-03', 'conv-02', 'conv-03', 'ak-timeline-01', 'ak-timeline-04', 'ak-timeline-05', 'ak-timeline-14', 'r4-raw-gadget-mainline-and-syzkaller-doc']
- 结论引用缺失或已作废：['xairy-works-007', 'xairy-works-008', 'xairy-dec-06', 'xairy-dec-07', 'conv-05', 'conv-07', 'conv-08', 'r1-syzkaller-external-network-verbatim']
- 结论引用缺失或已作废：['xairy-comm-01', 'xairy-comm-02', 'xairy-comm-04', 'xairy-comm-06', 'xairy-comm-07', 'xairy-comm-08', 'xairy-works-005', 'xairy-works-006', 'xairy-works-009', 'xairy-works-011', 'xairy-dec-08', 'ak-timeline-02', 'ak-timeline-10', 'ak-timeline-13', 'ak-timeline-17', 'ak-timeline-18', 'ak-timeline-20', 'conv-04', 'external-07', 'r2-bsides-munich-2022-duration', 'r2-balccon2k25-2025-duration']
- 结论引用缺失或已作废：['xairy-works-002', 'xairy-works-007', 'xairy-works-008', 'xairy-works-010', 'xairy-dec-04', 'xairy-dec-07', 'ak-timeline-14', 'ak-timeline-15', 'ak-timeline-16', 'ak-timeline-19', 'conv-05', 'conv-06', 'r4-raw-gadget-mainline-and-syzkaller-doc']

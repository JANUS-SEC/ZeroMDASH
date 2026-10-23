# Jann Horn — 时间线

> 调研日期：2026-07-27
> 调研者：Claude（基于一手来源 WebFetch 核实，非 WebSearch 摘要）
> 任务重点：最近 12 个月（2025-2026）动态，防止 skill 过时
> 信息源黑名单遵守：未引用知乎 / 微信公众号 / 百度百科。
> 调研方法：对 Project Zero 博客归档（253 篇，2014-2026）抽样 24 篇逐篇 WebFetch 核实作者 byline；GitHub API 核实仓库活动；arXiv 核实学术论文作者表。

## 概述

Jann Horn 是 Google Project Zero（P0）安全研究员，主攻 **Linux 内核漏洞利用**、**CPU 微架构侧信道攻击**（Spectre/Meltdown 的 P0 独立发现并报告者）与**虚拟化逃逸**。德国背景，学术倾向明显。2018-01-03 以 P0 名义发布 "Reading privileged memory with a side-channel" 博文，公开披露 Spectre/Meltdown 类 CPU 漏洞，是其职业生涯最高标志。

**核实状态分级**：
- P0 团队成立时间、Horn 博文年表、Spectre/Meltdown 角色、2025-2026 动态：**一手来源已核实（高可信度）**
- 教育背景、CTF 战队、会议演讲年表：**部分未核实，见文末"未核实 / 信息不足"节**

## 职业起点

- Project Zero 团队 **2014 年成立**（来源：https://projectzero.google/about-pz.html — "Formed in 2014"）。
- Horn 加入 P0 的**精确月份未在公开 About 页确认**。但其首篇已核实 P0 博文为 **2016-06-20**，故加入时间不晚于 2016 年中。与任务线索"2015 左右加入、与 Ian Beer 同期"基本吻合（精确到月未核实）。
- GitHub 用户 `thejh` 关联 `@google`，已核实属 Jann Horn（来源：https://github.com/thejh）。

## 研究里程碑年表

| 年份 | 事件 | 来源 | 可信度 |
|------|------|------|--------|
| 2014 | Project Zero 团队成立（Horn 尚无公开博文） | https://projectzero.google/about-pz.html | 高 |
| 2016-06-20 | **首篇已核实 P0 博文**："Exploiting Recursion in the Linux Kernel" — ecryptfs 叠加 procfs 文件触发任意递归致内核栈溢出，含完整 root 利用 | https://projectzero.google/2016/06/exploiting-recursion-in-linux-kernel_20.html（byline: Jann Horn） | 高 |
| 2017-04-07 | "Pandavirtualization: Exploiting the Xen hypervisor" — Xen `memory_exchange()` 的 `access_ok()` 检查不全，PV guest 可写 hypervisor 内存，逃逸至 dom0 | https://projectzero.google/2017/04/pandavirtualization-exploiting-xen.html（byline: Jann Horn） | 高 |
| 2017 年内 | VirtualBox VM→宿主用户态进程逃逸研究（CVE-2017-3558）写成草稿但未发表；8 年后于 2025-12 作为"dusted off draft"补发公开 | https://projectzero.google/2025/12/thinking-outside-the-box.html | 高 |
| 2017-06-01 | **Horn 与 P0 向 Intel/AMD/ARM 报告三个 CPU 侧信道变体**：Variant 1 边界检查绕过（bounds check bypass）、Variant 2 分支目标注入（branch target injection）、Variant 3 rogue data cache load。即 Spectre/Meltdown 类漏洞 | https://projectzero.google/2018/01/reading-privileged-memory-with-side.html（byline: Jann Horn, Project Zero） | 高 |
| 2018-01-03 | **P0 公开披露博文** "Reading privileged memory with a side-channel"，含 PoC：eBPF 读内核内存、KVM guest→host 内存泄漏、用户态直读内核内存。此为 Horn 职业最高标志 | 同上 | 高 |
| 2018-09-26 | "A cache invalidation bug in Linux memory management" — Linux per-thread VMA 缓存序列号回绕致 UAF（CVE-2018-17182），可内核代码执行 | https://projectzero.google/2018/09/a-cache-invalidation-bug-in-linux.html（byline: Jann Horn） | 高 |
| 2019-01-17 | "Taking a page from the kernel's book: A TLB issue in mremap()" — mremap 与 ftruncate 竞争致陈旧 TLB，在 Google Pixel 2 上注入 zygote 进程 | https://projectzero.google/2019/01/taking-page-from-kernels-book-tlb-issue.html（byline: Jann Horn） | 高 |
| 2019–2022（约 3 年空窗） | 无已核实 P0 博文。可能从事内部工作或减少公开输出。具体原因**未核实，不采信** | P0 archive 全量核对 https://projectzero.google/archive.html 未见 Horn byline 文章 | 高（空窗属实） |
| 2022-03-24 | "Racing against the clock -- hitting a tiny kernel race window" — Linux UNIX 域套接字 SCM_RIGHTS 垃圾回收窄竞争，用 cache miss / 硬件定时器中断 / epoll waitqueue churn 扩窗，非抢占内核 ~30% 命中 | https://projectzero.google/2022/03/racing-against-clock-hitting-tiny.html（byline: Jann Horn） | 高 |
| 2022–2025（约 3 年空窗） | 无已核实 P0 博文（2024 年 P0 博文均经核实为他人：Fratric / Forshaw / Jenkins 等） | P0 archive 全量核对 | 高（空窗属实） |
| 2025-08-08 | "From Chrome renderer code exec to kernel with MSG_OOB" — **CVE-2025-38236**，Linux ≥6.9 的 MSG_OOB（UNIX 域套接字带外数据）UAF，可从 Chrome renderer 沙箱达内核并完整利用 | https://projectzero.google/2025/08/from-chrome-renderer-code-exec-to-kernel.html（byline: Jann Horn） | 高 |
| 2025-09-26 | "Pointer leaks through pointer-keyed data structures" — 无内存安全违规、无时序攻击下远程泄漏指针；攻击者数据被反序列化入指针键数据结构、再序列化返回时泄漏。实测 macOS `NSKeyedArchiver`，Apple **2025-03-31 安全发布**修复 | https://projectzero.google/2025/09/pointer-leaks-through-pointer-keyed.html（byline: Jann Horn） | 高 |
| 2025-12-16 | "Thinking Outside The Box [dusted off draft from 2017]" — 公开其 2017 年 VirtualBox VM→宿主用户态进程逃逸草稿（CVE-2017-3558）。Horn 自述"从未写完下半部分" | https://projectzero.google/2025/12/thinking-outside-the-box.html（byline: Jann Horn） | 高 |
| 2026（截至 2026-05-13） | **无 Horn 署名 P0 博文**（2026 已发布 9 篇均为 Jenkins / Fratric / Forshaw / Franke / Silvanovich） | P0 archive https://projectzero.google/archive.html | 高 |

## 思想 / 方向转折点

1. **2016→2017：从 Linux 内核到虚拟化**。首篇博文聚焦 Linux 内核栈溢出；2017 年转向 Xen hypervisor 与 VirtualBox 逃逸，研究粒度从 OS 内核升至 hypervisor / 虚拟化边界。
2. **2017→2018：从虚拟化到 CPU 微架构（范式级跃迁）**。2017-06 向厂商报告 Spectre/Meltdown 三变体，2018-01 公开——从"软件漏洞利用"到"硬件 / 微架构侧信道"的跃迁，也是其职业生涯最高点。
3. **2018→2019：回到 Linux 内核**。Spectre/Meltdown 之后回归 Linux 内存管理（VMA 缓存、TLB / mremap），并在 Pixel 2 上做利用演示。
4. **2019→2022 与 2022→2025 两个空窗期**：公开输出显著减少。可能与内部 0day RCA 项目、内核加固倡议或转向非公开研究有关——**未核实，不采信具体原因**。
5. **2025 复出**：连发 3 篇博文，方向为 Linux 内核利用（MSG_OOB）、新型逻辑型指针泄漏技术、补发 2017 VirtualBox 草稿。显示出"内核利用 + 逻辑型信息泄漏"的双线回归，而非继续 CPU 微架构侧信道方向。

## 最近 12 个月动态（2025-2026）— 防过时关键

> 本节为任务重点。所有条目均经一手来源 WebFetch 核实。

### A. Project Zero 博文（2025-2026）

**1. 2025-08-08 — "From Chrome renderer code exec to kernel with MSG_OOB"**
- **CVE-2025-38236**；Linux ≥6.9 的 MSG_OOB（带外数据）特性用于 UNIX 域套接字，存在 use-after-free。
- 可从 Chrome renderer 沙箱触发，并完成完整内核利用（沙箱逃逸→内核）。
- 这是 Horn 时隔约 3 年的回归之作，方向回到 Linux 内核利用。
- 来源：https://projectzero.google/2025/08/from-chrome-renderer-code-exec-to-kernel.html

**2. 2025-09-26 — "Pointer leaks through pointer-keyed data structures"**
- 提出一种**无内存安全违规、无时序攻击**的远程指针泄漏技术：当攻击者控制的数据被反序列化并存入以指针为键的数据结构，再被重新序列化返回时，指针值随之泄漏。
- 实测于 macOS 的 `NSKeyedArchiver`；Apple 在 **2025-03-31** 的安全发布中修复。
- 这是一种新型逻辑型信息泄漏，有别于 Spectre/Meltdown 的侧信道范式——标志着 Horn 的关注点从硬件侧信道转向逻辑型信息流。
- 来源：https://projectzero.google/2025/09/pointer-leaks-through-pointer-keyed.html

**3. 2025-12-16 — "Thinking Outside The Box [dusted off draft from 2017]"**
- 公开其 2017 年撰写的 VirtualBox VM→宿主用户态进程逃逸草稿（CVE-2017-3558）。Horn 自述"从未写完下半部分"。
- 属于补发历史研究，非新方向，但确认其虚拟化逃逸研究脉络长期延续。
- 来源：https://projectzero.google/2025/12/thinking-outside-the-box.html

**4. 2026 年（截至 2026-05-13）**：Project Zero 已发布 9 篇博文（Pixel 10 利用链、Mutational Grammar Fuzzing、Windows GPHFH 深入、Windows 管理员保护绕过、Sound Barrier Part II、Pixel 9 0-click 三部曲等），**均无 Horn 署名**。来源：P0 archive https://projectzero.google/archive.html。

**小结**：最近 12 个月内 Horn 的公开 P0 输出集中在 2025 年 8-12 月（3 篇），2026 年至今无新博文。其研究方向从 CPU 微架构侧信道**回归**到 Linux 内核利用 + 逻辑型指针泄漏，并未继续 Spectre 类硬件侧信道方向。

### B. GitHub 活动（2025-2026，用户 `thejh`）

来源：GitHub API https://api.github.com/users/thejh/repos?sort=updated&per_page=30
（已核实属 Jann Horn，关联 `@google`）

| 时间 | 仓库 | 语言 | 说明 |
|------|------|------|------|
| 2026-05 | node-nacl | Assembly | 个人旧项目（标注 ABANDONED）零星更新 |
| 2026-03 | manga-ocr | — | 个人项目更新 |
| 2025-07 | linux（fork of torvalds/linux） | C | Linux 内核 fork 更新，与其 2025-08 MSG_OOB 研究时间吻合 |
| 2025-06 | almighty_su | C | 更新 |
| 2025-05 | nyx-packer、libxdc | — | 更新 |
| 2025-03 | android_DropBearServer | Java | 更新 |
| 2025-02 | luna-soc | — | 更新 |

**解读**：2025-07 的 linux fork 更新与 2025-08 的 MSG_OOB 内核利用博文在时间上吻合，支持其正在持续做 Linux 内核研究。2026 年的 GitHub 活动仅为个人旧仓库零星维护，不构成新研究方向的强信号。

### C. 2025-2026 会议演讲

**信息不足 / 未核实**。Black Hat（blackhat.com）与 USENIX Security（usenix.org）对自动化 WebFetch 抓取返回 **HTTP 403**，未能从一手议程核实 Horn 在 2025-2026 是否有 Black Hat USA / USENIX Security / CCC 38C3（2024-12）/ 39C3 等演讲。CCC media 搜索（media.ccc.de）对 "Jann Horn" 做子串匹配，未在前 3 页命中以他为演讲者的条目，但未扫完全部 105 条结果。

**当前不应断言**他在该期间是否有会议演讲。如有后续一手议程链接，应优先采信。

## 已核实事实清单（高可信度）

- P0 团队 2014 年成立（about 页）
- Horn 首篇已核实 P0 博文为 2016-06-20，加入 P0 不晚于 2016 年中
- **9 篇 Horn 署名 P0 博文**（2016-06、2017-04、2018-01、2018-09、2019-01、2022-03、2025-08、2025-09、2025-12），均经作者 byline 核实
- **Spectre/Meltdown**：Horn 是 P0 独立发现并报告者（2017-06-01 报告三变体），但**不是**学术论文 Meltdown（arXiv:1801.01207，作者 Lipp / Schwarz / Gruss / Prescher / Haas / Mangard / Kocher / Genkin / Yarom / Hamburg）的合著者。Spectre 学术论文作者本次未成功核实（arXiv ID 查询返回不匹配论文），Horn 角色以 P0 官方披露博文为准。
- 2025 年连发 3 篇 P0 博文，方向回归 Linux 内核利用 + 逻辑型指针泄漏
- 2026 年（截至 5 月）无 Horn 署名 P0 博文
- GitHub `thejh` 属 Horn，2025-2026 有零星活动，2025-07 linux fork 更新与 MSG_OOB 研究时间吻合

## 未核实 / 信息不足（须后续补充一手来源）

1. **教育背景**：任务线索称"德国背景、学术倾向、德国大学"，但未核实具体大学（Saarland / TU München / Bochum / 其他？）。LinkedIn 与大学官方页面未能在本次调研中成功抓取核实。**不采信任何具体大学名称**。
2. **CTF 战队**：任务线索称"可能的 CTF 选手"，未在 CTFtime 核实其所属战队与年份。**不采信**。
3. **会议演讲年表**（Black Hat / USENIX / CCC / IEEE S&P / OffensiveCon / Infiltrate / POC / HITB / Troopers）：本次调研未能从一手议程核实 Horn 历年演讲清单。Black Hat 与 USENIX 官网对自动化抓取返回 403；CCC media 搜索未扫完全部页码。**会议演讲年表整体缺失，须后续补充**。
4. **P0 加入精确月份**：仅能确认"不晚于 2016-06"，精确到月未核实。
5. **2019-2022、2022-2025 两个空窗期的内部工作内容**：未核实，不应臆测。
6. **X / Twitter 账号**：未核实其公开 X 账号 handle。
7. **抽样覆盖度**：P0 archive 共 253 篇，本次逐篇核实作者 byline 共 24 篇（9 篇 Horn + 15 篇非 Horn）。可能存在未抽样到的 Horn 博文，但已覆盖其已知研究方向（Linux 内核 / 虚拟化 / CPU 侧信道）的关键节点。

## 信息来源索引（一手，均经 WebFetch 核实）

1. https://projectzero.google/about-pz.html — P0 团队介绍（"Formed in 2014"）
2. https://projectzero.google/archive.html — P0 博文全量归档（253 篇，2014-2026）
3. https://projectzero.google/2016/06/exploiting-recursion-in-linux-kernel_20.html — Horn 首篇博文（byline 核实）
4. https://projectzero.google/2017/04/pandavirtualization-exploiting-xen.html — Xen 逃逸（byline 核实）
5. https://projectzero.google/2018/01/reading-privileged-memory-with-side.html — Spectre/Meltdown 披露（byline 核实，权威）
6. https://projectzero.google/2018/09/a-cache-invalidation-bug-in-linux.html — Linux VMA 缓存（byline 核实）
7. https://projectzero.google/2019/01/taking-page-from-kernels-book-tlb-issue.html — TLB / mremap（byline 核实）
8. https://projectzero.google/2022/03/racing-against-clock-hitting-tiny.html — 内核竞争（byline 核实）
9. https://projectzero.google/2025/08/from-chrome-renderer-code-exec-to-kernel.html — MSG_OOB（byline 核实）
10. https://projectzero.google/2025/09/pointer-leaks-through-pointer-keyed.html — 指针泄漏（byline 核实）
11. https://projectzero.google/2025/12/thinking-outside-the-box.html — VirtualBox 草稿补发（byline 核实）
12. https://github.com/thejh — GitHub 主页（关联 @google）
13. https://api.github.com/users/thejh/repos?sort=updated&per_page=30 — 仓库更新时间
14. https://arxiv.org/abs/1801.01207 — Meltdown 学术论文作者表（核实 Horn 非合著者）

## 排除项（经核实非 Horn 撰写，避免误采信）

抽样核实时确认以下博文**非** Horn 撰写，列此以防 skill 误用：

| 日期 | 标题 | 实际作者 |
|------|------|----------|
| 2014-08-21 | What does a pointer look like, anyway? | Chris Evans |
| 2014-08-25 | The poisoned NUL byte, 2014 edition | Chris Evans |
| 2015-01-02 | Finding and exploiting ntpd vulnerabilities | Stephen Röttger |
| 2015-03-09 | Exploiting the DRAM rowhammer bug | Mark Seaborn |
| 2015-06-19 | Owning Internet Printing | Neel Mehta |
| 2016-12-01 | BitUnmap: Attacking Android Ashmem | Gal Beniamini |
| 2016-12-14 | Chrome OS exploit: one byte overflow | 外部 guest |
| 2017-05-10 | Exploiting the Linux kernel via packet sockets | Andrey Konovalov |
| 2017-07-24 | Trust Issues: Exploiting TrustZone TEEs | Gal Beniamini |
| 2017-08-23 | Bypassing VirtualBox Process Hardening | James Forshaw |
| 2018-06-21 | Detecting Kernel Memory Disclosure Whitepaper | Mateusz Jurczyk |
| 2018-07-26 | Drawing Outside the Box: Precision Issues | Mark Brand / Ivan Fratric |
| 2018-08-02 | Adventures in vulnerability reporting | Natalie Silvanovich |
| 2019-04-11 | Virtually Unlimited Memory: Escaping Chrome Sandbox | Mark Brand |
| 2019-05-10 | Trashing the Flow of Data | Stephen Röttger |
| 2020-02-15 | Escaping the Chrome Sandbox with RIDL | Stephen Röttger |
| 2021-06-29 | An EPYC escape: Case-study of a KVM breakout | Felix Wilhelm |
| 2022-08-10 | The quantum state of Linux kernel GC CVE-2021-0920 | Xingyu Jin |
| 2022-12-08 | Exploiting CVE-2022-42703 | Seth Jenkins |
| 2023-01-19 | Exploiting null-dereferences in the Linux kernel | Seth Jenkins |
| 2024-11-21 | Simple macOS kernel extension fuzzing | Ivan Fratric |

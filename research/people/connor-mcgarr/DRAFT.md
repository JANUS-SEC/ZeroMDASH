# 未通过独立复核

已达到最大修订次数 4；本文件是审计草稿，不得进入跨人物比较。

# Connor McGarr：漏洞研究成长分析

- 擅长领域：Windows/浏览器漏洞利用
- 独立复核：revise · 95/100

## 成长阶段

- **2017-10 至 2018-09 · 从零基础到首次通过 OSCP：认证驱动的系统化重复练习建立**：起点为网络安全本科在读第 3 年、课堂外无安全实践的新手（2017-10 Cyber Defense Club 时连 Kali Linux 与 Linux 的关系都不清楚，被同学甩开）；经 Code Academy 命令行补足、VulnHub 朋友引导、Hack The Box 每日练习与 Offensive Security PWK 60 天课程，于 2018-09 首次尝试即通过 OSCP。期间形成文档化（OneNote 系统记录每台机器）与高强度重复练习（工作日每日约 3 小时、周末全投入）的习惯，动机由困难与低通过率反向驱动而非天赋叙事。（置信度：high）
  - 证据：cm-tl-01, cm-tl-02, cm-tl-03, cm-tl-04, cm-tl-05, cm-tl-06, cm-works-001, cmcg_conv_01, cmcg_conv_02, connor-community-01, cmgarr-ext-01
- **2019-01 至 2019-12 · 公开写作起点与认证阶梯延伸：从练习复盘到独立 writeup，并提出研究受阻时回到三段式自问的恢复流程**：2019-01-12 发表首篇博客《From Zero to Hero: My Path to OSCP》建立公开写作习惯；2019-05-13 发布 Admin Express v1.2.5.485 路径本地 SEH 字母编码缓冲区溢出 writeup（基于 Exploit-db 已发布 DoS PoC EDB-46711 发展为代码执行 exploit 并以作者署名提交至 EDB-46805，非漏洞首次发现、无 CVE/厂商披露）；2019-08-24 回顾 CTP/OSCE，将课程最大收获概括为 tool independence 与二进制层面理解，把研究重心从工具使用转向二进制层理解，并提出研究受阻时回到三段式自问（目标是什么、已知什么、如何在已知上扩展）的恢复流程；2019-09-21 同日两篇 ROP/内核调试基础 writeup，主题由用户态溢出转向内核与 ROP。（置信度：high）
  - 证据：cm-tl-07, cm-tl-08, cm-tl-09, cm-tl-10, cm-works-002, cmcg_conv_03, cmcg_conv_04, cm-dec-01, cm-dec-02, connor-community-02, r2-ev-001
- **2020-01 至 2021-12 · 进入内核利用、内存管理子系统与缓解绕过，并扩展到浏览器利用与恶意代码开发**：2020-02 首次系统讨论 SMEP 绕过；2020-04/05 以原理导论+利用应用配对写作（内存分页内部分析 + PTE 覆盖内核利用）；2020-03 Blue Frost Security eko2019.exe 全 ASLR/DEP 绕过 writeup 显式致谢 BFS 与同伴 @trickster012 协助；2020-08 发表《The Current State of Exploit Development》两期，把研究视角从单点漏洞扩展到系统性缓解机制综述（同期 XFG 前瞻分析），并在综述结尾以第一人称表达对未认证远程内核代码执行漏洞的偏好；2021-01 BOF 远程进程注入进入红队技术主题；2021-04 浏览器 UAF 基础分析铺垫后续 CVE 系列；2021-05 因 AWE 培训取消而转向公开复盘 Dell dbutil_2_3.sys CVE-2021-21551，首次系统引入 Kasif 的 data-only 攻击思路而非沿用自己更熟悉的 PTE 破坏。（置信度：medium）
  - 证据：cm-tl-11, cm-tl-12, cm-tl-13, cm-tl-14, cm-tl-15, cm-tl-16, cm-works-004, cm-works-005, cm-works-006, cmgarr-ext-03, cmgarr-ext-04, cmgarr-ext-05, cm-dec-03, cmcg_conv_05, cmcg_conv_06, connor-community-03
- **2022-01 至 2022-05 · 方法转型：从代码执行到数据驱动原语，浏览器利用系列与对抗缓解主线确立**：2022-03/04 完成 CVE-2019-0567 Microsoft Edge 类型混淆浏览器利用三部曲（环境与根因、CFG 绕过、Edge 移植与 ACG 绕过），自述该领域长期为其难点、多次尝试后中断又重新开始，依赖 Google Project Zero issue、Perception Point writeup 与 Bruno Keith 的 Chakra 先驱工作；2022-05 发表《No Code Execution? No Problem!》，把研究目标从代码执行转向 HVCI 之后的无代码执行利用，主张把任意读写转化为调用任意内核态 API 这一更强原语而非止步于 token 窃取，技术上以 Dmytro Oleksiuk 的工作与 KernelForge 库为基础（作者称对该想法反复思考约一年后据此撰写 HVCI 文章，原文 'This was about a year ago - and I have been chewing on this idea for awhile'）。研究主线正式确立为对抗缓解机制而非寻找新漏洞。（置信度：high）
  - 证据：cm-tl-17, cm-tl-18, cm-works-007, cm-works-008, cmgarr-ext-05, cmgarr-ext-06, cm-dec-04, connor-community-04
- **2024-06 至 2025-02 · 约两年发文间隔后转向 Windows Internals 与硬件辅助缓解**：2022-05 后存在约两年公开发文间隔（索引显示无 2022-06 至 2024-05 帖），其研究活动、是否换岗、是否内部研究无公开一手记录。2024-06-01 发表《Dissecting Secure Image Objects - Part 1》进入 Windows 安全内核对象分析主题，抽象层从利用原语上升到内核子系统与安全内核架构；2025-02-03 发表 Windows 内核模式影子栈（Shadow Stack）调研，延续硬件辅助缓解（CET）研究。主题转向的个人动机（为何转向 Internals/Secure Kernel、是否雇主驱动）在已抓取正文中无自述，转向本身由发文时间线推断为 inferred、动机为 unknown。（置信度：medium）
  - 证据：cm-tl-19, cm-tl-20, cm-works-010
- **2025-09 至 2026-01 · Secure Calls/SkBridge 与 ARM64 PAC，平台扩展至 ARM64 并配套公开工具**：2025-09-06 发表 Secure Calls/SkBridge 分析并在该博文中公布 SkBridge 与 Vtl1Mon 工具；两工具仓库首次提交日期分别为 SkBridge 2025-09-04（author date）、Vtl1Mon 2025-08-28（author date），并非同日创建（Vtl1Mon committer date 2026-02-12 与 author date 差异较大，推断为本地首次提交后于 2026-02 推送至 GitHub）。CET/影子栈研究（2025-02）延续到 ARM64 PAC（2025-10-15），形成跨平台控制流完整性对照（PAC 帖标注首发于 Prelude Security 博客，机构关系未明确）。2026-01-16 发表 ETW SecurityTrace 标志权限问题分析。GitHub 仓库（Exploit-Development 321★/109 fork、LittleCorporal 226★/55 fork、tgtdelegation 181★/24 fork、EATGuard 114★/21 fork、Vtl1Mon 106★/12 fork、SkBridge 83★/7 fork）反映工具建设的社区分发规模。（置信度：medium）
  - 证据：cm-tl-21, cm-tl-22, cm-tl-23, cm-works-009, cm-works-011, cm-dec-05, cmgarr-ext-07, connor-community-05, connor-community-06, connor-community-07, r1-ev-001, r1-ev-002

## 主要成长机制

### 认证驱动的系统化重复练习与文档化

起点：2017-10 为课堂外无安全实践的本科在读生，对 Linux 基础概念不清楚，被同学甩开后感到需要改变；缺少具名导师，仅有学校 Cyber Defense Club 同伴与一位推荐 VulnHub 的朋友。

练习与反馈：按学习资源依赖顺序构建（Code Academy 命令行 → VulnHub → Hack The Box → Offensive Security PWK 60 天课程），在 Hack The Box 上 2018-01 至 03 几乎每日练习，工作日每日约 3 小时、周末投入每一个清醒时刻；以 OneNote 系统记录每台机器，把文档化提升到与技能同等重要。；反馈以负面形式出现（被同学甩开、听说有经验者也会失败反而更想要），同伴与读者提问驱动公开输出；OSCP 一次通过作为可核验结果。

能力与结果：形成高强度重复练习与文档化并存的训练节奏，并把困难与低通过率反向转化为动机而非劝退。；2018-09 首次尝试即通过 OSCP（自述 I passed my exam on the first try）；2019-01-12 发表首篇公开 writeup 建立持续公开写作习惯；把 OneNote 文档化与 writeup 化延伸为后续七年系列化公开写作

置信度：medium；替代解释：该机制的核心证据主要来自作者本人博客一手自述，external 维度未抓取到第三方对 McGarr 的独立评价，同伴反馈与练习强度均经作者单方面转述；OSCP 一次通过作为结果可核验，但把通过归因于重复练习而非先备基础或天赋，属作者自述因果而非外部可核验因果，该外部佐证缺位应作为对机制推断置信度的扣减因素。

证据：cm-tl-01, cm-tl-02, cm-tl-03, cm-tl-04, cm-tl-05, cm-tl-06, cm-works-001, cmcg_conv_01, cmcg_conv_02, connor-community-01, cmgarr-ext-01

### 公开写作的学习-反馈-再输出循环

起点：2019-01 发表首篇博客后建立公开写作习惯；2020-08 自述《The Current State of Exploit Development》最初发表于 CrowdStrike 博客（归属为作者转述 reported，未抓取 CrowdStrike 官方博客页面或官方作者署名独立验证），后续 2025-10 PAC 帖标注首发于 Prelude Security 博客（机构关系未明确）。

练习与反馈：把训练复盘、认证回顾、单一 CVE 复现、综述与 Internals 分析均写成系列化长文公开（CVE-2019-0567 三部曲、内核池两期、Current State 两期），多篇文章在机构博客（CrowdStrike、Prelude Security，雇佣关系未经一手核实）首发后转载至个人博客；文末主动邀请读者发送评论、问题或更正。；先前 writeup 的公开传播引来他人方法建议：Dell dbutil_2_3.sys writeup 后于社交媒体发推指出未考虑 VBS/HVCI，收到 @d_olex 关于以自组装内核态 API 调用绕过 HVCI 的方法回应；Secure Calls 帖致谢 Alex Ionescu 为持续提供帮助的挚友，引用 Saar Amar、Quarkslab、blog.back.engineering、dor00tkit 等前人公开工作。社交媒体互动事件目前仅由作者本人在博客中转述，X 账号 @33y0re 因付费墙未一手抓取。

能力与结果：形成输出—公开反馈—再输出的循环：公开输出引来同行方法建议，作者长期反复思考后形成新文章，体现公开输出如何通过社交反馈驱动后续研究能力增长。；2022-05 HVCI/kernel CFG 文章（作者称对该想法反复思考约一年后据此撰写，原文 'This was about a year ago - and I have been chewing on this idea for awhile'）；2025-09 Secure Calls/SkBridge 文章配套公开 SkBridge 与 Vtl1Mon 工具；2025-10 PAC 文章经机构博客（Prelude Security）首发后转载个人博客，扩展受众

置信度：medium；替代解释：该机制的核心证据主要来自作者本人博客一手自述，external 维度未抓取到第三方对 McGarr 的独立评价，'@d_olex 方法回应''Alex Ionescu 持续协助''先驱工作依赖'均经作者单方面转述；机构博客归属中 CrowdStrike 为 reported、Prelude Security 关系未明确，应作为对机制推断置信度的扣减因素。

证据：cm-works-005, cm-works-007, cm-works-008, cm-works-009, cmgarr-ext-03, cmgarr-ext-06, cmcg_conv_05, cmcg_conv_06, connor-community-03, connor-community-04, connor-community-05, connor-community-06, connor-community-08

### 困难主题反复尝试、受阻状态恢复流程与长期悬置想法的反复思考

起点：浏览器利用为长期难点（自述 'Browser exploitation - it has been the bane of my existence for quite some time now'），多次尝试后中断又重新开始；OSCE 考试自述为人生中最难之事，学习者会反复陷入受阻、看不到尽头的状态。

练习与反馈：对困难主题（浏览器利用、HVCI 方法）多次尝试后中断又重新开始，对长期悬置的想法反复思考后再产出；CET/影子栈研究（2025-02）延续到 ARM64 PAC（2025-10），形成跨平台控制流完整性对照。OSCE 回顾中提出受阻状态恢复流程：反复阅读/复习直至理解一个概念、善用学生论坛、卡住时回到三个自问（目标是什么、已知什么、如何在已知上扩展）、横向有目的的思考。；OSCE 回顾（2019-08-24）把课程最大收获概括为 tool independence 与二进制层理解；同伴支持（学生论坛、同伴互助）作为继续的关键约束；HVCI 帖中自我反馈（'Most exploit writers sell themselves short (myself included) by stopping at token stealing'）。

能力与结果：把受阻状态常态化为可操作的恢复流程（三段式自问 + 横向思考），并把长期悬置的想法纳入后续产出计划。；2022-03/04 CVE-2019-0567 浏览器利用三部曲完成（自述长期难点最终产出）；2022-05 HVCI/kernel CFG 文章（对约一年前悬置想法反复思考后产出）；2025-10 ARM64 PAC 文章（CET/影子栈研究延续到 ARM64 硬件缓解）

置信度：medium；替代解释：需要以前人公开工作为基础，而非个人方法论特征；浏览器利用与 HVCI 文章均显式依赖 Google Project Zero、Perception Point、Bruno Keith、@d_olex/KernelForge 等前人公开工作。该机制的核心证据主要来自作者本人一手自述，external 维度未抓取到第三方独立评价，受阻恢复流程与反复思考均经作者单方面转述，应作为对机制推断置信度的扣减因素。

证据：cm-works-007, cm-works-008, cm-works-009, cm-tl-17, cm-tl-18, cm-tl-20, cm-tl-22, cmcg_conv_03, cmcg_conv_04, cmgarr-ext-05, cmgarr-ext-06, cm-dec-04, cm-dec-05, connor-community-02, connor-community-04

### 分析、工具与公开发表联动：把研究结论固化为可复用的公开工具

起点：2021-01 BOF 远程进程注入 writeup 进入恶意代码开发与红队技术主题，BOF 主题在后续 GitHub 工具（tgtdelegation）中得到延续；多篇文章在机构博客（CrowdStrike、Prelude Security，雇佣关系未经一手核实）首发后转载至个人博客。

练习与反馈：把研究结论以公开工具形式公开发布并扩展受众：CVE-2019-0567 分析配套公开方法、Secure Calls 配套 SkBridge 与 Vtl1Mon、ARM64 PAC 与 ETW SecurityTrace 配套持续公开写作；GitHub 账户拥有约 1.2k 关注者与多个置顶仓库（Exploit-Development、LittleCorporal、tgtdelegation、EATGuard、Vtl1Mon、SkBridge），账户成就包括 Starstruck (x2) 与 Arctic Code Vault Contributor。；Secure Calls 帖致谢 Alex Ionescu 为持续提供帮助的挚友，引用前人公开工作；GitHub star/fork 数反映社区分发规模（star/fork 数仅反映分发规模而非互动质量，issue/PR 协作活动未被一手抓取）。

能力与结果：形成分析、工具与公开发表联动的稳定产出模式，研究结论以公开工具形式公开发布并扩展受众。；2025-09-06 Secure Calls/SkBridge 分析配套公布 SkBridge 与 Vtl1Mon 工具（两仓库首次提交非同日：SkBridge 2025-09-04、Vtl1Mon 2025-08-28 author date）；GitHub 多个工具仓库（Vtl1Mon 106★/12 fork、SkBridge 83★/7 fork、EATGuard 114★/21 fork、tgtdelegation 181★/24 fork、LittleCorporal 226★/55 fork、Exploit-Development 321★/109 fork）；GitHub 账户成就 Starstruck (x2) 与 Arctic Code Vault Contributor

置信度：medium；替代解释：该机制的核心证据主要来自作者本人博客与 GitHub 一手自述，external 维度未抓取到第三方对 McGarr 的独立评价，'同伴反馈''社区分发规模'均经作者单方面转述或平台公开计数而非第三方独立评价，应作为对机制推断置信度的扣减因素。

证据：cm-tl-14, cm-tl-21, cm-works-009, cm-works-011, cm-dec-05, cmgarr-ext-07, connor-community-05, connor-community-06, connor-community-07, r1-ev-001, r1-ev-002

## 可迁移与不可迁移

- 可迁移：按学习资源依赖顺序构建基础（命令行 → CTF 平台 → 系统化认证课程），而非跳跃式选题；以高强度重复练习（每日固定时长、周末全投入）而非天赋叙事解释能力跃迁。
- 可迁移：把文档化提升到与技能同等重要：以 OneNote 系统记录每台机器、以公开 writeup 记录每次研究，使产出可核验、可复盘；提出研究受阻时回到三段式自问（目标是什么、已知什么、如何在已知上扩展）与横向、有目的的思考作为研究受阻时的恢复手段。
- 可迁移：对困难主题采用多 part 系列化深度分析（根因→利用→移植/绕过），以基础分析铺垫后续 CVE 系列，而非单篇散点输出；以原理导论+利用应用的配对写作结构降低读者门槛并巩固自身理解。
- 可迁移：把研究结论固化为可复用的公开工具（代码仓库 + writeup 联动），以公开输出引来同行方法建议并长期反复思考后形成新文章，构成输出—公开反馈—再输出循环。
- 可迁移：以自驱动逆向工程 + 公开演讲材料/前人 writeup 作为参考构建对无权威文档主题（如 XFG）的理解，构建自建测试程序与调试流程而非等待权威文档。
- 不可直接迁移：起步于 2017-2018 的 Offensive Security PWK 60 天课程与 Hack The Box 平台生态、学校 Cyber Defense Club 同伴网络与推荐 VulnHub 的朋友，这些时段性平台与同伴资源属个人起点条件，难以在其他时期或环境中复刻。
- 不可直接迁移：CrowdStrike、Prelude Security 等机构博客首发渠道（雇佣关系未经一手核实）为其公开写作提供了机构平台与受众扩展，这一机构渠道并非个人方法论特征，他人难以直接复用。
- 不可直接迁移：对 Google Project Zero、Perception Point、Bruno Keith、@d_olex/KernelForge、Alex Ionescu、Saar Amar 等前人与同伴公开工作的吸收与再加工，依赖具体可访问的先驱研究存在；这些先驱工作与同伴网络的存在与时点是个人特有条件。
- 不可直接迁移：2019-05 Admin Express exploit 以作者署名提交至 Exploit Database（EDB-46805）所依赖的 Exploit-db 发布渠道与 DoS PoC（EDB-46711）已存在的前提，属时段性公开资源条件。
- 不可直接迁移：约 2022-06 至 2024-05 两年发文间隔期的内部研究活动、是否换岗、是否内部研究无公开一手记录，该间隔期的外部条件（如雇佣关系变化）无法从公开材料核验，不可作为可迁移实践。

## 复核问题

- mechanisms[2].repeated_practice 残留借喻性表述“卡住时回到三个自问（目标是什么、已知什么、如何在已知上扩展）”。round-3 已要求将“卡顿”类研究受阻的借喻统一改写为“受阻状态”或“停滞”等直陈表述，round-4 修订了 stages[1].capability_change 与 transferable_practices[1] 中的同源词“卡住时”，但 mechanisms[2].repeated_practice 中的“卡住时”未一并修订，属前序修订指令执行不彻底。该字段为自撰机制描述，按语言规范不得使用借喻。
- mechanisms[2].repeated_practice：将“卡住时回到三个自问（目标是什么、已知什么、如何在已知上扩展）”中的“卡住时”改写为“研究受阻时”，与 round-3 对 mechanisms[2].intermediate_capability、observed_outcomes 及 round-4 对 stages[1].capability_change、transferable_practices[1] 的“卡顿/卡住时→受阻状态/研究受阻时”修订保持一致。改写后该句为：“OSCE 回顾中提出受阻状态恢复流程：反复阅读/复习直至理解一个概念、善用学生论坛、研究受阻时回到三个自问（目标是什么、已知什么、如何在已知上扩展）、横向有目的的思考。”该恢复流程的一手支撑为 cmcg_conv_03（OSCE 文章正文，verified_in_run=true，content_sha256=50c5eac1cdf8d2e5e87927228762f610345891942a01443ac4e0a06247544da5），无需新增证据。

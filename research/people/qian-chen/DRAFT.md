# 未通过独立复核

已达到最大修订次数 3；本文件是审计草稿，不得进入跨人物比较。

# Qian Chen：漏洞研究成长分析

- 擅长领域：IoT/网络设备漏洞
- 独立复核：revise · 80/100

## 成长阶段

- **2019-2020 · 公开演讲与设备研究起点；仿真工具链早期积累**：以下能力成长叙述锚定于 cq674350529 账号持有者（GitHub/博客/Medium/X handle 字符串一致），与姓名 Qian Chen 的唯一对应仅来自编排器 person_json 输入，未经一手来源独立确认（GitHub display name 为 CQ，README 不含姓名 Qian Chen）。2019 年 POC 发表 'Bug Hunting in Synology NAS'，为可核验公开演讲记录的起点，并将演讲材料以 PDF 形式归档于本人 pocs_slides 仓库，形成可复用的作品归档惯例，后续于 2019、2021、2022、2023、2025 多个年份延续（2020 与 2024 无已核验演讲记录）。2020 年记录 QEMU 仿真 MIPS 嵌入式二进制时遇到的 Illegal instruction 排障问题，为后续设备调试与固件仿真打下工具链早期基础。（置信度：high）
  - 证据：qc-pub-01, qc-pub-02, qc-ext-006
- **2021-2022 · 单一设备族系统化研究与二层协议规模化扩展**：2021-08 起连载 'A Journey into Synology NAS' 四部分，依次为环境搭建、findhostd 服务分析、iscsi_snapshot_comm_core 服务分析、HTTP 请求流程分析，并为 Synology finder 协议（9999/udp）编写 Wireshark 插件 syno_finder，体现按服务逐项完成协议解析与漏洞分析后迁移至同族其他服务或同类协议、再跨厂商扩展的系统化研究路径。2022 年 Black Hat EU 发表 'LCDPwn'，明确以 Armis Labs 的 CDPwn 为起点，先验证 CDP 漏洞修复情况并扩展发现，再迁移至通用性更强的 LLDP（LCDPwn 命名即 'Learn from CDPwn'）；项目页自报覆盖约 30 家厂商近 70 款设备、列出 55 个 CVE ID（CVE-2020-3505 至 CVE-2023-20047 区间，作者自报，未经逐厂商 advisory 核验）。同期 POC2022 发表 MikroTik RouterOS IPC 消息机制研究，设备类型进一步拓宽。（置信度：high）
  - 证据：qc-pub-03, qc-pub-04, qc-ext-003, qc-ext-004, qc-ext-005, qc-r1-lcdpwn-scope, qc-r3-lcdpwn-count
- **2023-2024 · 补丁比对方法转向与利用深化；研究范围扩展至虚拟/物理网卡差异**：2023-01-06 发表 'Patch Diff an Old Vulnerability in Synology NAS'，因 advisory 信息有限而改以厂商补丁为依据定位 Synology-SA-18:64 远程代码执行漏洞，标志从被动分析公开漏洞转向以补丁为依据主动定位。2023-02-10 NETGEAR R7800/R8500 Netatalk/afpd dsi_writeinit 缓冲区溢出分析，在 SSD 公开 advisory PoC（仅实现控制流劫持，依据博客首页摘要，独立博文返回 403 未复核）基础上推进至完整代码执行。2023-08-05 ASUS RT-AX56U V2（天府杯 2021）整数溢出分析，作者自述未发现该漏洞，基于两篇外部 writeup 重建分析并致谢 @Yimi Hu 与 @CataLpa 提供利用思路。2024-04-02 CVE-2023-33476 MiniDLNA HTTP chunk 解析越界读写分析，注明发现者为 @hyprdude，自身贡献集中在利用思路环节。2024-09-03 Pwn2Own Tokyo 2020 Synology DS418Play Netatalk DSI 堆溢出分析，致谢 DEVCORE 团队与 @Angelboy 分享细节。同年研究范围扩展至虚拟网卡与物理网卡带宽差异这一独立方向（BHEU 2023 'Breaking Theoretical Limits: The Gap Between Virtual NICs and Physical Network Cards'，README 标注 cooperated，合作者未列名）。（置信度：medium）
  - 证据：qc-pub-05, qc-pub-06, qc-pub-08, qc-pub-09, qc-r1-asus-post, qc-ext-002
- **2025 · 方法成熟与目标升级；部分仿真方法系统化**：2025 年在 OffByOne 会议发表 'Patch Diffing, You Are My Sword! A Deep Dive into Two Critical N-day Vulnerabilities in FortiGate'，将 2023 年起采用的补丁比对方法确立为系统性方法论，目标由消费级设备升级至企业级 FortiGate（对应 person_json 的 qualification）。2025-10-27 发表 'Partial Emulation with Qiling/QEMU'，从 2020 年 QEMU 单点排障演进为结合 QEMU user mode 与 Unicorn 的部分仿真方案，作为可复用研究基础设施公开发表，体现工具链随研究推进逐步积累。同期 deflat 工具仓库（基于 angr 的 OLLVM 控制流平坦化与虚假控制流反平坦化，支持 x86/ARM）整合既有方法，734 stars/125 forks 为平台声誉指标而非能力证据。（置信度：high）
  - 证据：qc-pub-10, qc-pub-11, qc-ext-001, qc-ext-007, qc-ext-008

## 主要成长机制

### 单一设备族与协议族的系统化扩展研究

起点：2019 年 POC 'Bug Hunting in Synology NAS' 为可核验研究起点；可访问的设备固件与公开 advisory；Armis Labs CDPwn 等前人公开研究可作为扩展起点。

练习与反馈：对单一设备族（Synology NAS）按服务逐一拆解（findhostd、iscsi_snapshot_comm_core 等）并自研协议解析工具（Wireshark syno_finder 插件）；以 Armis CDPwn 为起点先验证 CDP 修复再迁移至通用性更强的 LLDP；按服务完成协议解析后迁移至同族其他服务或同类协议，再跨厂商扩展至 MikroTik RouterOS IPC 等设备类型。；LCDPwn 项目页 'most of bugs are valid and have been fixed' 隐含厂商确认（作者自报，未经逐厂商 advisory 核验）；会议接受演讲（BHEU2022、POC2022）构成选题被接受的反馈，但会议官网逐字评价未取得（qc-ext-009 verified_in_run=false）。

能力与结果：由单一服务协议解析能力扩展为同族多服务与同类协议横向迁移、跨厂商扩展的系统化研究路径。；Synology NAS 四部分连载与 syno_finder Wireshark 插件（2021）；LCDPwn 覆盖 CDP/LLDP 两类二层协议、约 30 厂商约 70 款设备、列出 55 个 CVE ID（2022，作者自报，未经逐厂商 advisory 核验）；MikroTik RouterOS IPC 消息机制研究（POC2022）

置信度：high；替代解释：LCDPwn 规模化成果的可能解释之一是补丁可得性与公开材料密度而非研究方法本身的区分度；缺乏独立第三方逐厂商 advisory 核验（qc-ext-009 verified_in_run=false），区分度支撑有限，故 validation_tests 不含 distinctive。

证据：qc-pub-01, qc-pub-03, qc-pub-04, qc-ext-003, qc-ext-004, qc-ext-006, qc-r1-lcdpwn-scope, qc-r3-lcdpwn-count

### 以厂商补丁为依据的漏洞定位方法

起点：advisory 信息有限构成转向补丁比对的反馈点（依据 qc-pub-05）；厂商补丁可作为定位漏洞的依据；补丁可得性使该方法可重复适用于多厂商设备。

练习与反馈：2023-01 Synology-SA-18:64 补丁比对定位远程代码执行漏洞；2025 OffByOne FortiGate 两个 N-day 补丁比对分析（演讲题目即 'Patch Diffing, You Are My Sword'）；将补丁比对从单次分析固化为跨厂商系统性方法论。；advisory 信息有限迫使改以厂商补丁为入口（依据 qc-pub-05 growth_signal）；2025 演讲题目自述补丁比对为个人主线方法。

能力与结果：从被动分析公开漏洞转向以补丁为依据主动定位漏洞的能力，且方法可跨厂商复用（Synology → FortiGate）。；Synology-SA-18:64 远程代码执行漏洞定位（2023）；FortiGate 两个 N-day 漏洞补丁比对分析（2025）；补丁比对方法在 2023 与 2025 两次公开成果中作为主线延续

置信度：high；替代解释：补丁比对是漏洞研究社区常见方法，非本人特有；其成为个人主线可能是研究目标（FortiGate）补丁可得性与个人偏好共同作用的结果。

证据：qc-pub-05, qc-pub-11, qc-ext-001

### 以公开成果为基线的利用深化与复现式学习

起点：存在公开 advisory/PoC/竞赛 writeup 可作为基线（SSD advisory、Pwn2Own writeup、天府杯 writeup）；研究社区同伴（@Yimi Hu、@CataLpa、DEVCORE、@Angelboy、@hyprdude）的分享构成外部条件。

练习与反馈：NETGEAR Netatalk dsi_writeinit 在 SSD advisory PoC（仅控制流劫持，依据博客首页摘要，独立正文返回 403 未复核）基础上推进至完整代码执行；ASUS TFC2021 整数溢出基于他人 writeup 重建分析并致谢 @Yimi Hu/@CataLpa；MiniDLNA CVE-2023-33476 在发现者 @hyprdude 基础上承接利用思路；Pwn2Own 2020 Synology Netatalk 堆溢出基于 DEVCORE/@Angelboy 分享细节学习。；公开 advisory/PoC 的不完整（仅控制流劫持）构成推进至完整利用的反馈点；他人 writeup 与竞赛细节的可获取性降低复现门槛。

能力与结果：将公开成果作为基线逐层推进至完整利用或利用思路的复盘能力。；NETGEAR Netatalk 完整利用（2023，正文级措辞独立未复核）；ASUS TFC2021 整数溢出利用思路（2023）；MiniDLNA CVE-2023-33476 利用思路（2024）；Pwn2Own 2020 Synology Netatalk 堆溢出分析（2024）

置信度：medium；替代解释：利用深化依赖他人原始发现与 writeup 可得性，复现式学习的产出受公开材料密度与社区分享意愿约束，可能反映研究社区协作密度而非个人独创能力。

证据：qc-pub-06, qc-pub-08, qc-pub-09, qc-r1-asus-post

### 仿真工具链随研究推进逐步积累

起点：2020 年 QEMU 仿真 MIPS 嵌入式二进制遇到 Illegal instruction，固件全系统仿真存在工程门槛。

练习与反馈：2020 年记录 QEMU 仿真 Illegal instruction 单点排障；2025 年发表 'Partial Emulation with Qiling/QEMU'，提出结合 QEMU user mode 与 Unicorn 的部分仿真方案，作为可复用研究基础设施公开发表。；固件全系统仿真的 Illegal instruction 等工程问题构成转向部分仿真的反馈点；将单点工程经验整理为可复用方法并公开发表。

能力与结果：从单点排障经验演化为系统化的混合（QEMU user mode + Unicorn）仿真方法。；QEMU 仿真 Illegal instruction 排障记录（2020）；Partial Emulation with Qiling/QEMU 部分仿真方法发表（2025）

置信度：medium；替代解释：仿真方法演进也可能是 Qiling/Unicorn 工具生态成熟度的时期条件驱动而非个人能力成长主导。

证据：qc-pub-02, qc-pub-10

### 公开发表与作品归档习惯

起点：2019 年 POC 为公开演讲起点；可访问会议征稿与个人博客 cq674350529.github.io、GitHub 仓库 pocs_slides、项目页等自有渠道。

练习与反馈：2019、2021、2022、2023、2025 多个年份在 POC、HITB、BHEU、OffByOne 发表演讲；博客 2016-2025 共 32 篇；pocs_slides 仓库归档演讲 PDF；LCDPwn 设独立项目页。；会议接受演讲（POC2019、HITB2021、BHEU2022、POC2022、BHEU2023、OffByOne2025）构成选题被接受的反馈；会议官网逐字 speaker bio/abstract/技术评价均未取得（qc-ext-009 verified_in_run=false）。

能力与结果：将设备研究整理为会议演讲材料、博客文章与仓库归档相结合的可复用输出流程。；6 场会议演讲（POC2019、HITB2021、BHEU2022、POC2022、BHEU2023、OffByOne2025）；博客 2016-2025 共 32 篇文章；pocs_slides 仓库与 LCDPwn 项目页

置信度：high；替代解释：公开发表习惯受研究社区可见性激励与会议征稿周期驱动，会议接受不等同于技术评价（qc-ext-009 无外部逐字评价）。

证据：qc-pub-01, qc-pub-04, qc-pub-11, qc-ext-001, qc-ext-002, qc-ext-003, qc-ext-004, qc-ext-005, qc-ext-006, qc-ext-008

## 可迁移与不可迁移

- 可迁移：以厂商补丁为依据定位漏洞的方法，可跨厂商复用（Synology → FortiGate）。
- 可迁移：按服务逐一拆解设备族后迁移至同族服务/同类协议/跨厂商的系统化扩展研究路径。
- 可迁移：以公开 advisory/PoC 为基线逐层推进至完整利用或利用思路的复盘流程。
- 可迁移：将单点工程经验整理为可复用方法并公开发表（如 QEMU user mode + Unicorn 部分仿真）。
- 可迁移：博客、会议演讲与仓库归档相结合的多元公开发表流程。
- 不可直接迁移：身份锚定依赖 handle 字符串一致，姓名 Qian Chen↔handle cq674350529 的对应未经一手来源独立确认，GitHub display name 为 CQ。
- 不可直接迁移：仿真工具链演进可能依赖 Qiling/Unicorn 工具生态成熟度的时期条件，非个人能力单独决定。
- 不可直接迁移：LCDPwn 规模化成果依赖 2021-2022 二层协议研究窗口与 Armis CDPwn 前期公开工作的可得性。
- 不可直接迁移：会议演讲接受受会议征稿周期与社区可见性激励约束，非个人能力独立指标；会议官网逐字评价未取得。
- 不可直接迁移：利用深化依赖公开材料密度与社区分享意愿（@Yimi Hu、@CataLpa、DEVCORE、@Angelboy、@hyprdude），为个人特有外部条件而非可迁移做法。
- 不可直接迁移：微信公众号 writeup、X @cq674350529 一手正文均被反爬墙/402 拦截，本人自述的入门路径、失败与转折不可核验。

## 复核问题

- 作废证据重新引用：qc-r1-lcdpwn-scope 在 targeted-research round 3 被显式作废（invalid_evidence_ids=["qc-r1-lcdpwn-scope"]），由 qc-r3-lcdpwn-count 替代；round 3 的 synthesis_instructions 明确要求将 stages[1].evidence_ids、mechanisms[0].evidence_ids、mechanisms[4].evidence_ids 中的 qc-r1-lcdpwn-scope 替换为 qc-r3-lcdpwn-count。synthesis_json 中 mechanisms[4].evidence_ids 已正确替换，但 stages[1].evidence_ids 与 mechanisms[0].evidence_ids 仍同时保留 qc-r1-lcdpwn-scope 与 qc-r3-lcdpwn-count（双重引用，未替换）。这违反 task.md「以 six_dimensions 中已合并的有效证据为准，targeted_research 仅为修订历史；不得重新引用已作废证据」，构成关键来源错误，触发 verdict=revise。
- qc-r1-lcdpwn-scope 的 claim 本身（在 evidence_json.targeted 中）仍写作「逐一列出 57 个 CVE ID」，与其来源 URL（https://cq674350529.github.io/lcdpwn/）实际列出的 55 个不符；该证据已被 round 3 作废并由 qc-r3-lcdpwn-count 更正，但 synthesis 仍将其作为 evidence_ids 成员引用，使作废证据的错误计数（57）仍可经 evidence_ids 链路进入最终报告。
- stages[1].evidence_ids：删除作废证据 qc-r1-lcdpwn-scope，仅保留 qc-r3-lcdpwn-count；原数组 ["qc-pub-03","qc-pub-04","qc-ext-003","qc-ext-004","qc-ext-005","qc-r1-lcdpwn-scope","qc-r3-lcdpwn-count"] 改为 ["qc-pub-03","qc-pub-04","qc-ext-003","qc-ext-004","qc-ext-005","qc-r3-lcdpwn-count"]。依据：targeted-research round 3 invalid_evidence_ids=["qc-r1-lcdpwn-scope"]，qc-r1-lcdpwn-scope 因 CVE 计数错报（57 实为 55）已作废。
- mechanisms[0].evidence_ids：删除作废证据 qc-r1-lcdpwn-scope，仅保留 qc-r3-lcdpwn-count；原数组 ["qc-pub-01","qc-pub-03","qc-pub-04","qc-ext-003","qc-ext-004","qc-ext-006","qc-r1-lcdpwn-scope","qc-r3-lcdpwn-count"] 改为 ["qc-pub-01","qc-pub-03","qc-pub-04","qc-ext-003","qc-ext-004","qc-ext-006","qc-r3-lcdpwn-count"]。依据同上。
- stages[3].capability_change：将「同期 deflat 工具仓库（基于 angr 的 OLLVM 控制流平坦化与虚假控制流反平坦化，支持 x86/ARM）整合既有方法」改为体现衍生依赖的中性表述，例如「同期 deflat 工具仓库基于既有方法（SnowGirls/deflat、Tencent Security 博客、Quarkslab 文章）实现，以 angr 处理 OLLVM 控制流平坦化与虚假控制流，支持 x86/ARM」，以与证据 qc-ext-007 的 growth_signal 一致，避免将衍生整合叙述为原创能力。
- mechanisms[4].observed_outcomes：将「6 场会议演讲（POC2019、HITB2021、BHEU2022、POC2022、BHEU2023、OffByOne2025）」改为「据本人 GitHub README 自述，6 场会议演讲（POC2019、HITB2021、BHEU2022、POC2022、BHEU2023、OffByOne2025）」，与 qc-ext-001 至 qc-ext-006 来源均为本人 README、qc-ext-009 外部评价缺失的事实一致。
- mechanisms[0].intermediate_capability：在「由单一服务协议解析能力扩展为同族多服务与同类协议横向迁移、跨厂商扩展的系统化研究路径」末尾补注「（LCDPwn 规模化数值为作者自报，未经逐厂商 advisory 核验）」，避免自报数值隐含支撑能力叙述。
- 结论引用缺失或已作废：['qc-pub-03', 'qc-pub-04', 'qc-ext-003', 'qc-ext-004', 'qc-ext-005', 'qc-r1-lcdpwn-scope', 'qc-r3-lcdpwn-count']
- 结论引用缺失或已作废：['qc-pub-01', 'qc-pub-03', 'qc-pub-04', 'qc-ext-003', 'qc-ext-004', 'qc-ext-006', 'qc-r1-lcdpwn-scope', 'qc-r3-lcdpwn-count']

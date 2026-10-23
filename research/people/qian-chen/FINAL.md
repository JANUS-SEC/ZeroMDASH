# Qian Chen：漏洞研究成长分析

- 擅长领域：IoT/网络设备漏洞
- 独立复核：pass · 86/100

## 成长阶段

- **2019 · 公开作品起点：将设备研究整理为会议演讲材料并归档**：2019 年在 POC 会议发表 'Bug Hunting in Synology NAS'，是其公开演讲记录的起点，目标为消费级 NAS 设备；将设备研究整理为会议演讲材料并在本人仓库 pocs_slides/slides 下发布 PDF，形成可复用的作品归档惯例，后续多个年份延续（已核验演讲年份：2019、2021、2022、2023、2025；2020 与 2024 无已核验演讲记录）。（置信度：high）
  - 证据：qc-pub-01, qc-ext-006
- **2021-2022 · 系统化扩展：按服务逐项解析后迁移至同类协议与跨厂商**：自 2021-08 起连载 'A Journey into Synology NAS' 四部分（环境搭建、findhostd 服务分析、iscsi_snapshot_comm_core 服务分析、HTTP 请求流程分析），并为 Synology finder 协议（9999/udp）编写 Wireshark 插件 syno_finder，体现对单一设备族按服务逐项拆解并自研协议解析工具的复盘式研究习惯。2022 年 Black Hat EU 发表 'LCDPwn: Breaking Enterprise-Things with Layer 2 Discovery Protocol Vulnerabilities Again'，明确以 Armis Labs 的 CDPwn 为起点，先验证 CDP 漏洞修复情况并扩展发现，再迁移到更具通用性的 LLDP，研究命名 LCDPwn 即 'Learn from CDPwn'；该项目页自报跨约 30 家厂商近 70 款网络设备、20+ CDP bugs、约 50 LLDP bugs，并逐一列出 55 个 CVE ID（作者自报，未经逐厂商 advisory 核验，见 evidence_json.gaps）。同年 POC 2022 发表 'MikroTik RouterOS Security: The Forgotten IPC Message'，研究对象扩展至 MikroTik RouterOS 的 IPC 消息机制。（置信度：medium）
  - 证据：qc-pub-03, qc-pub-04, qc-ext-003, qc-ext-004, qc-ext-005, qc-r3-lcdpwn-count
- **2023-2024 · 方法转向与公开成果复现：补丁比对为入口、以公开 PoC 为基线推进**：2023-01-06 发表 'Patch Diff an Old Vulnerability in Synology NAS'，因 advisory 信息有限而改以厂商补丁为入口定位并分析 Synology-SA-18:64 远程代码执行漏洞，标志从被动分析公开漏洞转向以补丁为定位漏洞的依据主动发现。2023-02-10 发表 'Analyzing an Old Netatalk dsi_writeinit Buffer Overflow in NETGEAR Router'，针对 NETGEAR R7800/R8500 上 Netatalk/afpd 的 dsi_writeinit 缓冲区溢出推进至完整代码执行，而非仅停留在公开 PoC 的控制流劫持（依据博客首页摘要，独立正文返回 403 未复核）。2023-08-05 发表 ASUS RT-AX56U V2（天府杯 2021）整数溢出分析，作者自述未发现该整数溢出漏洞、参考两篇外部 writeup 重建并重点关注利用思路，致谢 @Yimi Hu 与 @CataLpa 提供利用思路。2023 年 Black Hat Europe 2023 发表 'Breaking Theoretical Limits: The Gap Between Virtual NICs and Physical Network Cards'（README 标注 cooperated，合作者未列名），研究范围扩展至虚拟网卡与物理网卡带宽差异这一独立方向。2024 年发表 MiniDLNA CVE-2023-33476（注明发现者为 @hyprdude，自身贡献集中在利用思路）与 Pwn2Own Tokyo 2020 Synology DS418Play Netatalk DSI 堆溢出分析（致谢 DEVCORE 团队与 @Angelboy）。（置信度：medium）
  - 证据：qc-pub-05, qc-pub-06, qc-pub-08, qc-pub-09, qc-ext-002, qc-r1-asus-post
- **2025 · 方法成熟与目标升级：补丁比对确立为方法论、工具链随研究推进逐步积累**：2025 年在 OffByOne 会议发表 'Patch Diffing, You Are My Sword! A Deep Dive into Two Critical N-day Vulnerabilities in FortiGate'，将 2023 年起采用的补丁比对方法确立为系统性方法论，目标由消费级设备升级至企业级 FortiGate，与 person_json 的 qualification（FortiGate 设备漏洞）对应。同期发表 'Partial Emulation with Qiling/QEMU'，提出结合 QEMU user mode 与 Unicorn 的部分仿真方案用于嵌入式固件调试与漏洞验证，将 2020 年 QEMU 单点排障演进为系统化的混合仿真方法并作为可复用研究基础设施公开发表。同期 deflat 工具仓库基于既有方法（SnowGirls/deflat、Tencent Security 博客、Quarkslab 文章）实现，以 angr 处理 OLLVM 控制流平坦化与虚假控制流，支持 x86/x86_64 与 ARM/ARM64（衍生依赖由 deflat 仓库 README Reference 段一手确认）。（置信度：medium）
  - 证据：qc-pub-02, qc-pub-10, qc-pub-11, qc-ext-001, qc-ext-007, qc-ext-008, qc-r4-deflat-derivatives, qc-r1-github-identity

## 主要成长机制

### 按服务逐项解析后迁移至同族其他服务或同类协议、再跨厂商扩展的系统化研究路径

起点：对单一厂商设备（Synology NAS）具备可及的固件与服务入口，且已有会议演讲与博客作为公开输出渠道。

练习与反馈：对单一设备族按服务逐一拆解（findhostd、iscsi_snapshot_comm_core、HTTP 请求流程），为 Synology finder 协议编写 Wireshark 插件；随后以 Armis Labs CDPwn 为起点先验证 CDP 漏洞修复情况并扩展发现，再迁移到更具通用性的 LLDP，并将研究范围扩展至 MikroTik RouterOS IPC 消息机制。；LCDPwn 项目页以 'most of bugs are valid and have been fixed' 隐含厂商确认（作者自报，未经逐厂商 advisory 核验，见 evidence_json.gaps）。

能力与结果：由单一服务协议解析能力扩展为同族多服务与同类协议横向迁移、跨厂商扩展的系统化研究路径（LCDPwn 规模化数值为作者自报，未经逐厂商 advisory 核验）。；A Journey into Synology NAS 系列四部分及 syno_finder Wireshark 插件（qc-pub-03）；LCDPwn 跨约 30 家厂商（作者自报，未经逐厂商 advisory 核验）的 55 个 CVE ID 列表（qc-r3-lcdpwn-count）；MikroTik RouterOS IPC 消息研究（qc-ext-004）

置信度：medium；替代解释：该研究路径的规模化产出可能部分源于厂商补丁可得性与公开材料密度，而非单纯研究方法差异；LCDPwn 数值未经逐厂商 advisory 核验，独立第三方评价缺失（qc-ext-009 verified_in_run=false）。

证据：qc-pub-01, qc-pub-03, qc-pub-04, qc-ext-003, qc-ext-004, qc-ext-006, qc-r3-lcdpwn-count

### 以公开 advisory/PoC 为基线逐层推进至完整利用

起点：公开 advisory 或 PoC 可及，且存在可对照的厂商补丁或公开 writeup 作为基线。

练习与反馈：以 SSD 公开 advisory 仅实现控制流劫持为反馈点（依据博客首页摘要，独立正文返回 403 未复核），自行推进至完整代码执行；对 ASUS RT-AX56U V2 整数溢出参考两篇外部 writeup 重建，重点关注利用思路；对 Pwn2Own 2020 Synology Netatalk 堆溢出通过致谢 DEVCORE 团队与 @Angelboy 获取竞赛漏洞细节用于学习。；公开 PoC 与 advisory 的不完整性构成逐层推进的反馈点；外部 writeup 与社区同伴提供利用思路来源。

能力与结果：在他人发现或公开基线之上承接利用思路环节并推进至更深利用，明确区分原始发现权与自身贡献。；NETGEAR Netatalk dsi_writeinit 缓冲区溢出推进至完整代码执行（qc-pub-06）；ASUS RT-AX56U V2 整数溢出利用思路分析（qc-r1-asus-post）；MiniDLNA CVE-2023-33476 利用思路，注明发现者为 @hyprdude（qc-pub-08）；Pwn2Own 2020 Synology Netatalk 堆溢出分析（qc-pub-09）

置信度：medium；替代解释：该机制可观察产出集中在已公开漏洞的复现与深化，可能受公开材料可得性筛选，难以据以推断其在未公开 0-day 发现上的能力。

证据：qc-pub-06, qc-pub-08, qc-pub-09, qc-r1-asus-post

### 以厂商补丁为定位漏洞的依据

起点：厂商补丁可作为定位漏洞的依据，且 advisory 信息有限构成转向补丁比对的反馈点（依据 qc-pub-05）。

练习与反馈：2023 年起因 advisory 信息有限而改以厂商补丁为入口定位漏洞（Synology-SA-18:64）；补丁可得性使该方法可重复适用于多厂商设备，并于 2025 年 FortiGate 研究中确立为系统性方法论（题目即 'Patch Diffing, You Are My Sword'）。；advisory 信息有限构成转向补丁比对的反馈点（qc-pub-05）；补丁可得性使该方法可重复适用于多厂商设备。

能力与结果：从被动分析公开漏洞转向以补丁为定位漏洞的依据主动发现，并将该方法跨厂商迁移。；Synology-SA-18:64 远程代码执行补丁比对分析（qc-pub-05）；FortiGate 两个 N-day 漏洞补丁比对分析（qc-pub-11）

置信度：medium；替代解释：补丁比对转向可能同时受研究产出压力与补丁可得性共同驱动，而非仅由 advisory 信息有限单一原因触发。

证据：qc-pub-05, qc-pub-11

### 固件仿真工具链随研究推进逐步积累

起点：嵌入式固件调试需要可复现的运行环境，2020 年即记录 QEMU 仿真 'Illegal instruction' 排障问题。

练习与反馈：2020 年记录 MIPS 嵌入式二进制 QEMU 仿真排障；2025 年提出结合 QEMU user mode 与 Unicorn 的部分仿真方案用于嵌入式固件调试与漏洞验证，将单点工程经验整理为可复用方法并公开发表。；固件仿真工程问题在 2020 年即作为可记录的排障对象，构成 2025 年部分仿真方法的早期铺垫。

能力与结果：将单点工程经验整理为可复用方法并公开发表，形成跨研究项目复用的仿真工具链。；QEMU 仿真 Illegal instruction 排障记录（qc-pub-02）；Partial Emulation with Qiling/QEMU 方法发表（qc-pub-10）

置信度：medium；替代解释：从 2020 年排障到 2025 年方法发表的跨度较长，中间过程缺乏可核验的连续记录，工具链积累的连续性为推断。

证据：qc-pub-02, qc-pub-10

### 公开发表与社区协作作为研究资产

起点：具备会议投稿与个人博客、GitHub 仓库等公开输出渠道，且存在研究社区同伴网络。

练习与反馈：据本人 GitHub README 自述，6 场会议演讲（POC2019、HITB2021、BHEU2022、POC2022、BHEU2023、OffByOne2025）延续公开输出惯例；博客 2016-2025 跨度发布；维护 deflat 工具仓库；通过致谢特定团队与个人（DEVCORE、@Angelboy、@Yimi Hu、@CataLpa）获取竞赛漏洞细节与利用思路。；会议接受构成对选题的接受（一手自述，外部逐字评价缺失，见 qc-ext-009）；deflat 仓库 stars/forks 为平台声誉指标而非能力证据；社区同伴提供漏洞细节与利用思路。

能力与结果：将演讲、博客、工具仓库与社区协作整合为可复用的研究资产，并依赖研究社区分享而非孤立工作。；据本人 GitHub README 自述，6 场会议演讲（POC2019、HITB2021、BHEU2022、POC2022、BHEU2023、OffByOne2025）；LCDPwn 列出 55 个 CVE ID（作者自报，未经逐厂商 advisory 核验，见 qc-r3-lcdpwn-count）；deflat 工具仓库（基于既有方法实现，stars/forks 为平台声誉指标）；个人博客 2016-2025 跨度持续发布（qc-ext-008）

置信度：medium；替代解释：公开产出集中可能受投稿接受率与平台可见性筛选，研究社区协作的具体互动内容未取得一手正文核验（X 402、微信验证墙）。

证据：qc-pub-01, qc-pub-09, qc-pub-11, qc-ext-001, qc-ext-003, qc-ext-004, qc-ext-005, qc-ext-007, qc-ext-008, qc-r3-lcdpwn-count, qc-r4-deflat-derivatives

## 可迁移与不可迁移

- 可迁移：按服务逐项完成协议解析与漏洞分析后，迁移至同族其他服务或同类协议，再跨厂商扩展的系统化研究路径，不依赖个人特有资源。
- 可迁移：以厂商补丁为定位漏洞的依据，在 advisory 信息有限时作为可重复适用于多厂商设备的方法，补丁可得性是该方法的可迁移前提。
- 可迁移：以公开 advisory/PoC 为基线逐层推进至完整利用，并明确区分原始发现权与自身贡献，可作为研究社区分工协作的可迁移做法。
- 可迁移：将单点工程经验（如固件仿真排障）整理为可复用方法并公开发表，形成跨研究项目复用的工具链。
- 可迁移：结合 QEMU user mode 与 Unicorn 的部分仿真方案用于嵌入式固件调试与漏洞验证，为可复用的研究基础设施。
- 不可直接迁移：会议演讲接受、博客与 GitHub 仓库的公开输出渠道属个人特有条件，其可见性受投稿接受率与平台推荐机制筛选，不可作为可迁移能力。
- 不可直接迁移：deflat 仓库的 stars/forks 为平台声誉指标而非能力证据，且 deflat 系基于既有方法（SnowGirls/deflat、Tencent Security 博客、Quarkslab 文章）实现，非原创能力（见 qc-r4-deflat-derivatives）。
- 不可直接迁移：通过致谢特定团队与个人（DEVCORE、@Angelboy、@Yimi Hu、@CataLpa）获取竞赛漏洞细节与利用思路的社区协作网络属个人特有条件。
- 不可直接迁移：身份锚定于 cq674350529 账号持有者，与姓名 Qian Chen 的唯一对应未经一手来源独立确认，能力归属的确定性受此限制。

## 复核问题


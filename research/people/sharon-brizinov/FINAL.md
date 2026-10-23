# Sharon Brizinov：漏洞研究成长分析

- 擅长领域：ICS/IoT 漏洞
- 独立复核：pass · 91/100

## 成长阶段

- **2017-2019（教育 2017-2020 与 2019-08 DEFCON 27 重叠期） · 入门阶段：学术教育与竞赛并行**：DEFCON 官方页面（sb-timeline-02）以 Team: Claroty, Members: Sharon Brizinov, Tal Keren 形式确认其身份与 Claroty 归属的一手依据；此前 decisions.identity_check 中『仅由本地种子支持、同名歧义未排除』的保守判断已被该官方页面证伪。2017-2020 在 The Academic College of Tel-Aviv, Yaffo 接受学术教育（sb-timeline-01、brizinov-ext-li-education），与 2019-08 DEFCON 27 Black Badge（sb-timeline-02）时间重叠，构成结构化知识基础与竞赛练习并行的早期阶段，而非以单一先天禀赋作解释。该阶段同期已嵌入 Claroty 工业安全研究网络（sb-timeline-05）。（置信度：high）
  - 证据：sb-timeline-01-education, sb-timeline-02-defcon27-blackbadge, sb-timeline-05-claroty-2019, sb_defcon27_ics_ctf, brizinov-ext-li-education
- **2020 · 首次 ICS 公开利用研究**：由 bug bounty 与 CTF 转入 ICS 公开利用研究。据 sb-rev2-001 ZDI 一手正文，2020-09-10 发布《Performing SQL Backflips to Achieve Code Execution on Schneider Electric's EcoStruxure Operator Terminal Expert at Pwn2Own Miami 2020》，署名 Claroty Research Amir Preminger 与 Sharon Brizinov，漏洞链为路径遍历漏洞（CVE-2020-7494，任意 DLL 加载）加 SQLite PRAGMA/VIEW 信息泄漏漏洞（CVE-2020-7496）共同达成远程代码执行，于 2020 年 1 月 S4 Conference 首届 Pwn2Own Miami 演示，Claroty Research team 获 25,000 美元与 25 Master of Pwn points；队友据 ZDI 一手署名裁定为 Amir Preminger。同年发布 OPC 攻击面测绘与 WIBU CodeMeter 研究（sb_pub_2020）。该对应关系据 sb-rev1-001 个人站 listing 与 sb-rev2-001 ZDI 正文核实，ZDI 公告正文已取得，Pwn2Own 官方结果页仍未取得。（置信度：high）
  - 证据：sb-rev2-001, sb-rev1-001, sb_pub_2020_opc_attack_surface, sb_pwn2own_track_record
- **2021 · fuzz 驱动的协议栈批量发现与工具链固化**：研究方法从单点漏洞转向 fuzzing 驱动的批量协议栈发现，目标扩展到工业远程访问客户端与云连接 OT；持续将 fuzz 与覆盖分析固化为可复用开源工具（sb_toolchain_wireshark_fuzz，2020-2024 跨期），支撑 BusyBox 14 漏洞批量发现与 EtherNet/IP、SIP、工业远程访问客户端系列研究（sb_pub_2021）。该阶段开始重复练习跨协议栈的 fuzz 工作流。（置信度：medium）
  - 证据：sb_pub_2021_busybox_fuzz, sb_toolchain_wireshark_fuzz, sb_pub_2020_opc_attack_surface
- **2022 · 攻击链构造升级与厂商协同披露回路**：技术栈从漏洞列举升级到攻击链构造：发布 Evil PLC Attack（将 PLC 作为攻击工程站的中间节点）、Hiding Code on Rockwell Automation PLCs、Exploiting URL Parsers，并在 S4x22 追踪 Siemens PLC 原生代码执行路径。据 Claroty 博客（SB-COMM-001）称 Hiding Code on Rockwell 与 CVE-2022-1161 相关，未与 NVD/CISA 官方记录交叉核实。同年与 Rockwell Automation 工程师协同披露（SB-COMM-002，共同定位根因、产出检测工具、CISA 发布安全公告、Rockwell 另发两条独立 advisory）。据本人 LinkedIn 自述获 SANS Difference Makers Awards Researcher of the Year 2022（reported，官方页未抓取，不作独立第三方评议证据）。（置信度：medium）
  - 证据：sb_pub_2022_evil_plc, SB-COMM-001, SB-COMM-002, sb_sans_researcher_2022, sb-timeline-04-sans-dma-2022, brizinov-ext-li-sans-researcher-of-year-2022
- **2023 · 架构级分析与主流大会双发**：目标难度上升至 NAS 云连接与 OPC UA 架构级实现差异；在 DEFCON 31 与 BlackHat 同题双会议发表（Exploiting OPC UA、A Pain in the NAS），显示从会议单点向主流工业/安全大会的发表路径固化。同年完成第 5 次 Pwn2Own 出场（IoT 2023）。据 sb-rev2-002 个人站 About Me，Pwn2Own Toronto 系列对应 IoT 赛事、Miami 系列对应 ICS 赛事；故 Toronto 2022 与五次自述中的 IoT 2022（第 3 次）为同一赛事，IoT 2023（第 5 次）对应 Toronto 2023，对齐关系据此澄清。（置信度：medium）
  - 证据：sb_pub_2023_opc_ua_nas, sb_pwn2own_track_record, sb-rev2-002, sb-dec-p2o-toronto-2022, sb-rev2-003, sbrz-conv-01
- **2024-2025 · 攻防兼顾与雇主迁移**：2024 年以 Pwn2Own 赛后 Part1/Part2 连载公开 WAN→LAN pivot 利用链（TP-Link ER605、Synology BC500），并发布 Rockwell Logix Trusted Slot 绕过；首次出现防御向输出（Blackjack Fuxnet 恶意代码分析），研究范围由纯攻击侧向攻防兼顾扩展（sb_pub_2024）。2025 年扩展到开发者平台 OSINT 与 bug bounty（How I Scanned all of GitHub Oops Commits for Leaked Secrets、How I Made 64k From Deleted Files），方法延续系统化扫描与工具化习惯而非单点手工挖掘（sb_pub_2025）。LinkedIn 显示当前雇主为 HackerOne（sb-timeline-06、brizinov-ext-li-employer-hackerone），与目标生态扩展轨迹对应；Claroty→HackerOne 迁移时点与触发因素无一手来源（登录墙后）。（置信度：medium）
  - 证据：sb_pub_2024_pivot_chain, sb_pub_2025_github_secrets, sb-timeline-06-hackerone-current, brizinov-ext-li-employer-hackerone

## 主要成长机制

### 跨协议族攻击面系统化测绘

起点：2019-08 DEFCON 27 Black Badge（Team Claroty，成员 Sharon Brizinov、Tal Keren，sb-timeline-02）提供 ICS 攻防竞赛背景；2019 年起归属 Claroty 厂商研究团队（sb-timeline-05），该环境提供 ICS/OT 目标接触与负责任披露渠道。

练习与反馈：2020 年 OPC 攻击面测绘（sb_pub_2020）→ 2021 年 EtherNet/IP 协议栈发现（sb_pub_2021）→ 2023 年 OPC UA 架构级实现差异分析（sb_pub_2023、sbrz-conv-01），跨多个工业协议族重复执行攻击面梳理与实现差异识别。；厂商协同披露回路提供反向校正（SB-COMM-002：Rockwell 工程师共同定位根因并产出检测工具）；会议发表构成同行可见性反馈（DEFCON 29/31、BlackHat、S4x22、SANS ICS 2022，SB-COMM-004）。

能力与结果：形成跨协议族的攻击面分类与实现差异识别方法，可迁移到新协议栈而非每次从零开始。；OPC 攻击面测绘研究（sb_pub_2020）；EtherNet/IP 协议栈研究发现（sb_pub_2021）；OPC UA 架构级实现差异分析（sb_pub_2023、sbrz-conv-01）；SANS ICS 2022 Hunting EtherNet/IP Protocol Stacks 议题（sb_pub_2022）

置信度：medium；替代解释：Claroty Team82 整体研究路线（SB-COMM-005、SB-COMM-006）可能驱动协议选题而非个人独立选择，团队级资源使个人与团队贡献难以完全分离。

证据：sb_pub_2020_opc_attack_surface, sb_pub_2021_busybox_fuzz, sb_pub_2023_opc_ua_nas, SB-COMM-002, SB-COMM-004, sb-timeline-02-defcon27-blackbadge, sb-timeline-05-claroty-2019

### 将一次性 fuzz 需求固化为可复用开源工具的重复练习

起点：2020 年 OPC 攻击面测绘后转向系统化 fuzz（sb_pub_2020→sb_pub_2021），具备 Wireshark/tshark 协议分析基础。

练习与反馈：2020-2024 跨期持续将一次性 fuzz 需求固化为可复用工具并开源（wirefuzz 链路层感知 fuzzer、wirecov 按 dissectors 的代码覆盖分析、Holy-Grail Pcap 多协议测试 PCAP、EtherNet/IP & CIP Stack Detector，sb_toolchain_wireshark_fuzz）。；公开工具发布与协议栈批量发现结果互为反馈（BusyBox 14 漏洞，sb_pub_2021），工具复用支撑后续协议栈批量发现。

能力与结果：形成 fuzz 与代码覆盖分析的可复用工作流，支撑跨协议栈的批量漏洞发现而非单点手工挖掘。；BusyBox 工具链 14 漏洞批量发现（sb_pub_2021）；EtherNet/IP 协议栈研究发现（sb_pub_2021）；SIP 客户端单斜杠崩溃（sb_pub_2021）

置信度：low；替代解释：开源工具个人作者归属未独立核实：github.com/sharonbrizinov 账号 pinned 仓库（s3viewer、slack-anti-delete）与 ICS/OT 无关且 bio 空，Team82 GitHub 组织/仓库 URL 返回 404。故上述仅作为据个人站 listing 观察到的研究工具化倾向，不应直接归因为个人可迁移的工具化研究习惯；BusyBox 14 漏洞批量发现作为工具化机制产出的因果主体（个人 vs 团队）未确定。

证据：sb_toolchain_wireshark_fuzz, sb_pub_2021_busybox_fuzz, sb_pub_2020_opc_attack_surface

### 时限内现场利用竞赛作为完整利用链开发练习

起点：2019-08 DEFCON 27 Black Badge 提供竞赛级 ICS 攻防背景（sb-timeline-02）；Claroty 厂商研究环境支撑 2020 年 Pwn2Own ICS 赛事参与启动（sb-timeline-05）。

练习与反馈：2020-2023 跨四年度五次 Pwn2Own 参赛（ICS 2020、ICS 2022、IoT 2022、ICS 2023、IoT 2023），在受限时间内反复完成目标研究与完整利用链开发（sb_pwn2own_track_record、sb-timeline-03、brizinov-ext-li-pwn2own-x5）。；赛事奖金与 Master of Pwn 点数（sb-rev2-001：Miami 2020 Claroty Research team 25,000 美元/25 pts；sb-rev2-003、sb-dec-p2o-toronto-2022：Toronto 2022 团队 62,500 美元/9 pts）；赛后 Part1/Part2 连载复盘（sb_pub_2024）。五次参赛的独立佐证强度不对称：仅 2020 Miami 取得点名个人的一手佐证（sb-rev2-001 ZDI 署名 Sharon Brizinov），Toronto 2022 为团队级未点名个人（sb-rev2-003、sb-dec-p2o-toronto-2022），其余三次（ICS 2022、ICS 2023、IoT 2023）仍仅本人 LinkedIn 自述。

能力与结果：在时限压力下整合攻击面测绘、漏洞发现、利用链构造的端到端能力，目标类型从 ICS 扩展到 IoT。；Schneider Ecostruxure 路径遍历加 SQLite 信息泄漏链达成 RCE（CVE-2020-7494、CVE-2020-7496，sb-rev2-001）；WAN→LAN pivot 利用链（TP-Link ER605、Synology BC500，sb_pub_2024）

置信度：low；替代解释：三条 Pwn2Own 证据（sb_pwn2own_track_record、sb-timeline-03-pwn2own-x5、brizinov-ext-li-pwn2own-x5）均为本人 LinkedIn 自述同一来源的不同条目，不作相互独立的重复证据；五次中仅 2020 Miami 取得点名个人的一手佐证。公开材料（个人站、ZDI writeup、Wikipedia）均为成功案例，未发现失败、被驳回或中断的负样本，幸存者偏差使『重复练习到能力增长』因果推断缺乏负样本对照，因果强度可能偏强。

证据：sb_pwn2own_track_record, sb-timeline-03-pwn2own-x5, brizinov-ext-li-pwn2own-x5, sb-rev2-001, sb-rev2-002, sb-rev2-003, sb-dec-p2o-toronto-2022, sb_pub_2024_pivot_chain, sb-timeline-02-defcon27-blackbadge, sb-timeline-05-claroty-2019

### 攻击链构造从单点 RCE 升级到跨网 pivoting 与可信机制绕过

起点：2020-2021 单点漏洞与 fuzz 批量发现基础（sb_pub_2020、sb_pub_2021）。

练习与反馈：2022 年 Evil PLC Attack 将 PLC 作为攻击工程站的中间节点 → 2022 年 Hiding Code on Rockwell PLC（代码隐藏）与 S4x22 Siemens 原生代码执行追踪 → 2024 年 WAN→LAN pivot 利用链与 Rockwell Logix Trusted Slot 绕过（sb_pub_2022、sb_pub_2024）。；厂商协同披露（SB-COMM-002：Rockwell 工程师共同定位根因、产出检测工具）；同伴研究复用（SB-COMM-001：引用 Rogue7 针对 Siemens SIMATIC S7、Airbus 针对 Schneider Electric PLC 的研究作方法基础）。

能力与结果：从漏洞列举升级到攻击链构造（代码隐藏、原生执行、跨网 pivoting、可信机制绕过），以公开文献为输入沿同一研究脉络迭代。；Evil PLC Attack 研究（sb_pub_2022）；Hiding Code on Rockwell Automation PLCs（据 Claroty 博客 SB-COMM-001 称与 CVE-2022-1161 相关，未与 NVD/CISA 官方记录交叉核实）；WAN→LAN pivot 利用链（TP-Link ER605、Synology BC500，sb_pub_2024）；Bypassing Rockwell Logix Controllers Trusted Slot（sb_pub_2024）

置信度：medium；替代解释：攻击链构造升级与 Claroty Team82 整体研究路线演进（SB-COMM-005、SB-COMM-006）相关，个人选题驱动与团队路线驱动难以完全分离。

证据：sb_pub_2022_evil_plc, sb_pub_2024_pivot_chain, SB-COMM-001, SB-COMM-002

### 厂商协同披露与 CERT/会议反馈回路

起点：Claroty Team82 提供标准化披露管线（SB-COMM-005：私下报告—厂商修复—firmware 发布—CISA/厂商 advisory）；厂商研究环境提供 PSIRT 协作渠道。

练习与反馈：2022 年与 Rockwell Automation 工程师协同披露（SB-COMM-002：共同定位根因、产出检测工具、CISA 发布安全公告、Rockwell 另发两条 advisory）；跨厂商重复同一披露模式（SB-COMM-005）。；厂商工程团队反向校正（共同定位根因、产出检测工具）+ CISA 国家级 CERT 二次传播 + 会议发表反馈（SB-COMM-002、SB-COMM-004）。

能力与结果：在多轮外部反馈中校准披露与研究方向，研究输出经厂商工程团队反向校正而非单次披露即止。；Rockwell PLC 代码隐藏研究 + 检测工具产出 + CISA 安全公告（SB-COMM-002）；据本人 LinkedIn 自述获 SANS DMA Researcher of the Year 2022（reported，官方页未抓取，不作独立第三方评议证据）

置信度：low；替代解释：标准化披露管线为 Team82 团队级制度产物（SB-COMM-005、SB-COMM-006），个人在其中承担的角色未独立核实；SANS 奖项仅为本人 LinkedIn 自述（reported），SANS 官方页未抓取，不作独立第三方评议证据；会议发表反馈亦可能受团队整体产出驱动。

证据：SB-COMM-002, SB-COMM-005, SB-COMM-001, sb_pub_2022_evil_plc, sb-timeline-04-sans-dma-2022, brizinov-ext-li-sans-researcher-of-year-2022

### 跨生态目标扩展与雇主迁移对应

起点：Claroty ICS/OT 厂商研究环境（sb-timeline-05）提供 ICS 目标基础。

练习与反馈：ICS（2020-2023）→ IoT（2022-2023 Pwn2Own IoT 系列）→ NAS 云连接（2023）→ 开发者平台 OSINT 与 bug bounty（2025），目标生态持续扩展（sb_pub_2020-2025、sb_pwn2own_track_record）。；雇主由 Claroty 迁移至 HackerOne（sb-timeline-06、brizinov-ext-li-employer-hackerone），与目标生态扩展轨迹对应；方法延续系统化扫描与工具化习惯而非单点手工挖掘（sb_pub_2025）。

能力与结果：研究方法（系统化扫描、工具化、攻击面测绘）从 ICS/OT 迁移到更广义的漏洞研究领域。；How I Scanned all of GitHub Oops Commits for Leaked Secrets（sb_pub_2025）；How I Made 64k From Deleted Files bug bounty（sb_pub_2025）；当前雇主 HackerOne（sb-timeline-06）

置信度：medium；替代解释：Claroty→HackerOne 迁移时点与触发因素无一手来源（LinkedIn 登录墙后），目标生态扩展与雇主迁移的因果关系为推断而非证实；跨生态扩展亦可能受行业趋势与团队整体方向影响。

证据：sb_pub_2025_github_secrets, sb_pub_2024_pivot_chain, sb_pub_2023_opc_ua_nas, sb-timeline-06-hackerone-current, brizinov-ext-li-employer-hackerone, sb_pub_2020_opc_attack_surface

## 可迁移与不可迁移

- 可迁移：将一次性 fuzz 与协议分析需求固化为可复用开源工具（据个人站 listing 观察到的研究工具化倾向，作者归属未独立核实）。
- 可迁移：跨协议族复用攻击面测绘方法（OPC、EtherNet/IP、SIP、OPC UA 实现差异识别）。
- 可迁移：厂商协同披露作为反馈回路（共同定位根因、产出检测工具、CERT 二次传播）。
- 可迁移：会议同题双发（DEFCON 与 BlackHat）固化主流大会发表路径。
- 不可直接迁移：Claroty Team82 厂商研究环境提供 ICS/OT 目标接触与负责任披露渠道（sb-timeline-05），支撑其 Pwn2Own ICS 赛事参与在 2020 年即能启动。
- 不可直接迁移：Team82 标准化披露管线（私下报告—厂商修复—firmware 发布—CISA/厂商 advisory，SB-COMM-005）为团队级制度产物，非个人可迁移。
- 不可直接迁移：Team82 CVE 仪表板、LLM-driven VR、Copeland/Danfoss 研究为团队级制度产物（SB-COMM-005、SB-COMM-006），非个人可迁移。
- 不可直接迁移：DEFCON 27 Black Badge（2019-08，Team Claroty，成员 Sharon Brizinov、Tal Keren 协作，sb-timeline-02）为早期同伴协作与 Claroty 归属的特定条件。
- 不可直接迁移：同伴研究者网络（Amir Preminger、Amir Zaltzman、Tomer Goldschmidt、Tal Keren，SB-COMM-006、sb-timeline-02、sb-rev2-001）为团队内分工条件，非个人可独立复现。

## 复核问题


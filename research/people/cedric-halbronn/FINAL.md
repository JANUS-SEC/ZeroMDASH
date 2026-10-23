# Cedric Halbronn：漏洞研究成长分析

- 擅长领域：Windows/Linux/移动端漏洞
- 独立复核：pass · 83/100

## 成长阶段

- **约 2009-2014 · 移动平台安全阶段**：以 Windows Mobile 6 rootkit（Hack.lu 2009，议题名『When E.T. comes into Windows Mobile 6 (a.k.a. PoC(k)ET)』）切入公开演讲，研究取向定位于系统层/rootkit 而非应用层；其后平台沿 iPhone、HTC/Android 横向迁移，研究对象随移动设备生态扩展，研究深度从安全模型分析与取证推进到 bootloader 调试（hbootdbg）与漏洞利用（HTC One bootloader exploit）。早期即建立演讲+博客+GitHub 工具的多渠道输出形态，并以法语社区（SSTIC、MISC）作为英语会议之外的再表达渠道。需注明：该阶段及后续 stage 的全部时间线证据基础为研究对象自维护站点 ezseclab.com/research（自述陈列面），verified_in_run=true 仅证明该页面抓取成功，并不构成独立事实核验。（置信度：medium）
  - 证据：ch-timeline-stage1-mobile-2009-2014, ch-timeline-2009-10-hacklu-wm6-pocket, ch-timeline-2010-06-sstic-pocket-fr, ch-timeline-2010-10-hitb-iphone, ch-timeline-2011-05-2012-04-htc-desirez-unlock, ch-timeline-2012-06-android-forensics-misc63, ch-timeline-2013-10-hacklu-hbootdbg, ch-timeline-2014-07-htc-one-bootloader-exploit
- **约 2015-2020 · 桌面/服务器内核与企业网络设备阶段**：研究对象从移动终端迁移到 Windows 桌面内核利用（CVE-2015-2426 on Windows 8.1 x64）与 Cisco ASA 网络设备固件。在 Cisco ASA 上把单一深挖成果（IKEv1 堆溢出）在 3 个月内连投 Warcon/BSidesMCR/44Con 三个会议，并产出 8 部分博客系列覆盖静态分析、调试、dlmalloc 与 libptmalloc gdb 插件、mempools/checkheaps 及最终利用（CVE-2016-1287 堆溢出），把内部 malloc 实现分析固化为可复用调试插件。2020 年于 OffensiveCon 演讲 CVE-2018-8611 Windows KTM 提权，并随后发布 5 部分博客系列，把单一 CVE 拆解为补丁分析→触发→竞争取胜→内核读写原语→检测的完整方法论叙事；OffensiveCon 首次出现并成为其稳定输出渠道。需注明：此阶段主体证据为 ezseclab.com/research 自述页面，未由一手演讲页或厂商公告独立核验。（置信度：medium）
  - 证据：ch-timeline-stage2-kernel-network-2015-2017, ch-timeline-2015-09-cve2015-2426-win81-misc78, ch-timeline-2016-07-neutrino-ek-misc88, ch-timeline-2017-06-09-cisco-asa-talks, ch-timeline-2017-10-cisco-asa-8part-libptmalloc, ch-timeline-2020-02-offensivecon-cve2018-8611-ktm, ch-timeline-2020-04-cve2018-8611-5part
- **约 2021-2023 · 竞赛反馈 + 嵌入式/SOHO + Linux 内核阶段**：以 Pwn2Own 作为外部能力验证与方向选择反馈：据 about 页自述（『Pwn2Own Wins: 2021 and 2022』）于 2021 Austin、2022 Toronto 参赛并获胜；需分层标注——Pwn2Own 英文维基百科条目印证 Synacktiv 团队 2021/2022 获奖（2021 Vancouver 成员 Fabien Perigaud、Vincent Dehors；2022 Toronto 团队名无个人成员），但 Halbronn 个人姓名未出现在维基成员名单，故『个人获胜』仅见 about 自述，团队获奖可由独立二手来源印证。赛后持续投入 SOHO/嵌入式（Netgear BrokenPrint、Lexmark MC3224i 目录遍历、WD PR4100 NAS RCE CVE-2022-23121、HP iLO 研究取向），并将研究栈迁移到 Linux 内核（nf_tables UAF CVE-2022-32250），该 CVE 成为后续 OffensiveCon 2023 Linux 内核议题与 libslub 工具的基础。同期产出 BlueKeep 检测器 BKScan 与 Baron Samedit（CVE-2021-3156）on VMware vCenter 的场景化利用，体现对真实部署环境可靠性的关注。（置信度：medium）
  - 证据：ch-timeline-stage3-competition-linux-2021-2023, ch-timeline-2021-07-baron-samedit-vcenter, ch-timeline-2021-11-pwn2own-austin-win, ch-timeline-2022-02-brokenprint-lexmark, ch-timeline-2022-03-wd-pr4100-cve2022-23121, ch-timeline-2022-09-netlink-nftables-cve2022-32250, ch-timeline-2022-10-hexacon-toner-deaf, ch-timeline-2022-12-pwn2own-toronto-win, ch-timeline-2023-05-offensivecon-linux-libslub, r1-pwn2own-wiki
- **2024 · 可观察产出断档**：research 页时间线由 2023-05 直接跳至 2025-05，2024 年无 Halbronn 个人议题。OffensiveCon 2024 议程页共列 20 个议题，无任何 Cedric Halbronn 议题，独立印证该年度断档。同期存在的 Samsung Galaxy A* Boot Chain 议题分布于 Quarkslab conf-presentations 仓库（works 维度可核验），但其 OffensiveCon 2024 署名为 Maxime Rossi Bellom、Damiano Melotti、Raphael Neveu、Gabrielle Viala 四人，SSTIC 2024 相关议题文件名片段亦提示 rossi-bellom/neveu 等他人。该断档修正了『约 2009 年起 15+ 年持续研究周期』的连续性表述：实际为 2009-2023 与 2025 持续，2024 为可观察产出断档，不能以『持续』暗示无断档。断档成因未知，可能为转向未公开的培训筹备、内部项目或个人周期，无一手证据可证任何单一解释。（置信度：high）
  - 证据：r1-offensivecon-2024-no-halbronn, works_01_samsung_boot_chain_2024, works_02_sstic24_vendor1_vendor2
- **2025 起 · 教学-反馈闭环阶段**：研究输出形态从个人写博/演讲扩展到系统化培训（about 页述 Windows Kernel Exploitation 培训）。据 research 页自述，培训学员 Jael Koh 回流为联合作者：OffensiveCon 2025 议题 #7『Cedric Halbronn and Jael Koh — Hunting for overlooked cookies in Windows 11 KTM and baking exploits for them』已由会议议程页独立印证其议题存在性与合著者 Jael Koh，并回到 Windows KTM 主题（2020 CVE-2018-8611 的延续）；research 页进一步自述『Jael 曾参加其培训，找到 2 个 CVE 并在 Windows 11 上完成可用利用』，该『2 个 CVE』细节仅见于 research 页自述，无 CVE 编号与独立来源印证，须标注为自述而非事实。教学-反馈闭环在机制层面表现为 teaching→学员产出→回流联合作者→反哺研究线。（置信度：medium）
  - 证据：ch-timeline-stage4-teaching-2025, ch-timeline-2025-05-offensivecon-win11-ktm-jael-koh, ch-timeline-2025-ezseclab-founder-15y, r1-offensivecon-2025-jael-koh-ktm

## 主要成长机制

### 单一研究主题跨会议多渠道迭代发布

起点：早期移动阶段即建立演讲+博客+GitHub 工具的多渠道输出习惯，存在对同一研究在多个场合反复表达的基础条件。

练习与反馈：对单一深挖课题在同一时间窗口内连投多个会议并配套博客/工具：Cisco ASA IKEv1 堆溢出在 2017 年 3 个月内连投 Warcon、BSidesMCR、44Con，并以 8 部分博客系列配套；Windows KTM CVE-2018-8611 于 OffensiveCon 2020 演讲后配套 5 部分博客系列；Samsung 启动链主题在 2024 年分布于 OffensiveCon/SSTIC/Black Hat USA/Off-By-One（主题层存在，但本人未在 OffensiveCon 2024 署名）。；反馈来自不同会议受众的接受度差异、投稿接受率与会议邀请机制，推动每站调整披露深度与边界；OffensiveCon 在 2020/2023/2025 三度出现而 2024 缺席，说明稳定渠道存在年度波动。

能力与结果：形成『单一课题→多渠道分阶段披露→配套长篇方法论博客』的可复用输出流程，区别于一次性 PoC 发布。；2017 Cisco ASA 三会议连投 + 8 部分博客系列；2020 CVE-2018-8611 OffensiveCon 演讲 + 2020-04 5 部分博客系列；OffensiveCon 作为稳定输出渠道（2020/2023/2025），2024 缺席印证年度波动

置信度：medium；替代解释：多渠道连投可能部分反映投稿接受率与会议邀请机制而非纯主动复盘；OffensiveCon 2024 缺席与 2025 复出说明『稳定渠道』本身存在年度波动，连投模式可能是会议排期与投稿节奏的产物而非个人刻意分阶段披露策略。

证据：ch-timeline-2017-06-09-cisco-asa-talks, ch-timeline-2017-10-cisco-asa-8part-libptmalloc, ch-timeline-2020-02-offensivecon-cve2018-8611-ktm, ch-timeline-2020-04-cve2018-8611-5part, ch-timeline-2023-05-offensivecon-linux-libslub, ch-timeline-2025-05-offensivecon-win11-ktm-jael-koh, r1-offensivecon-2024-no-halbronn, r1-offensivecon-2025-jael-koh-ktm

### 研究副产物工具化

起点：研究中反复出现的调试、扫描或内存分析需求可被抽象为通用工具，存在 GitHub 作为发布渠道的条件。

练习与反馈：把研究中的内部实现分析或检测需求固化为可复用工具：Cisco ASA 研究产出 libptmalloc gdb 插件，HTC bootloader 调试产出 hbootdbg，Linux 内核 slub 堆研究产出 libslub，BlueKeep 高危 CVE 产出 BKScan 检测器，Android 取证配套 GitHub 工具。；反馈来自工具在社区的实际使用与研究者自身后续研究的复用，工具与后续研究线形成相互支撑。

能力与结果：形成『研究需求→内部实现分析→通用工具沉淀→反哺后续研究』的副产物沉淀习惯。；hbootdbg（HTC bootloader 调试，2013）；libptmalloc gdb 插件（Cisco ASA dlmalloc/libptmalloc 分析，2017）；BKScan（BlueKeep CVE-2019-0708 检测器，2019）；libslub（Linux 内核 slub 堆研究，2023）

置信度：low；替代解释：GitHub 用户 saidelike 的公开仓库列表（31 个，已显示前 30 个）中未出现 BKScan、libslub、hbootdbg、libptmalloc 任一独立仓库，列表以 fork 为主；research 页所述工具在 saidelike 名下无对应独立仓库可独立印证（第 31 个仓库未抓取，无法完全排除）。工具化机制可能仅为 research 页自述，或工具发布于其他账号/未公开仓库，机制本身与具体仓库的独立印证均存在缺口。

证据：ch-timeline-2013-10-hacklu-hbootdbg, ch-timeline-2017-10-cisco-asa-8part-libptmalloc, ch-timeline-2019-07-bkscan-bluekeep, ch-timeline-2023-05-offensivecon-linux-libslub, r1-github-repos

### 研究对象随设备/平台生态迁移

起点：研究对象为低层/系统层而非应用层，存在沿设备/平台生态横向迁移的基础取向。

练习与反馈：研究对象随主流设备生态与新型攻击面迁移：WinMo6→iPhone→HTC/Android（移动期）→Windows 桌面内核+Cisco ASA 固件（桌面/网络期）→SOHO 嵌入式（Netgear/Lexmark/WD PR4100）→Linux 内核（nf_tables）→Windows KTM 回归（2025），迁移伴随 CVE 产出与会议演讲。；反馈来自 Pwn2Own 等竞赛（据 about 自述 2021/2022 获胜，团队层可由维基印证）推动向 SOHO/嵌入式方向投入，以及真实部署环境（VMware vCenter Baron Samedit）可用性反馈推动场景化验证。

能力与结果：形成『沿攻击面生态迁移研究目标→快速进入新平台低层→产出 CVE 与配套写作』的横向迁移能力，而非在单一平台长期深耕。；移动期 WinMo6/iPhone/HTC 多平台覆盖；2015-2017 Windows 桌面内核 + Cisco ASA 固件并行；2021-2022 SOHO/嵌入式 CVE 产出（WD PR4100 CVE-2022-23121）；2022 Linux 内核 nf_tables CVE-2022-32250；2025 回到 Windows KTM

置信度：medium；替代解释：横向迁移可能反映外部机会（竞赛目标清单、雇主项目、公开 CVE 潮流）驱动而非个人主动选择：Pwn2Own 目标设备清单与 SOHO 方向高度相关，公开 CVE（BlueKeep、Baron Samedit）的出现时间与其工具/场景化利用时间高度吻合，迁移节奏可能是机会驱动而非能力驱动的生态布局。

证据：ch-timeline-2010-10-hitb-iphone, ch-timeline-2014-07-htc-one-bootloader-exploit, ch-timeline-2015-09-cve2015-2426-win81-misc78, ch-timeline-2017-06-09-cisco-asa-talks, ch-timeline-2022-03-wd-pr4100-cve2022-23121, ch-timeline-2022-09-netlink-nftables-cve2022-32250, ch-timeline-2025-05-offensivecon-win11-ktm-jael-koh, ch-timeline-2021-11-pwn2own-austin-win, ch-timeline-2021-07-baron-samedit-vcenter

### OffensiveCon 稳定渠道与教学-反馈闭环

起点：OffensiveCon 2020 首次出现后存在复用为稳定输出渠道的条件；具备系统化培训能力（about 页述 Windows Kernel Exploitation 培训）。

练习与反馈：以 OffensiveCon 作为核心输出渠道（2020 CVE-2018-8611、2023 Linux 内核 Exploit Engineering、2025 Windows 11 KTM 联合演讲），并将系统化培训作为研究能力放大器。；教学-反馈闭环：据 research 页自述，培训学员 Jael Koh 回流为 OffensiveCon 2025 联合作者并（自述）产出 2 个 CVE 与 Windows 11 可用利用；OffensiveCon 2025 议题与合著者已由议程页独立印证，『2 个 CVE』细节仅自述。

能力与结果：形成『培训→学员产出→联合作者→反哺研究线』的能力放大回路，研究输出形态从个人演讲扩展到教学驱动的同侪生成。；OffensiveCon 2020/2023/2025 三度出现（2024 缺席）；2023 OffensiveCon 配套 libslub 工具与 Linux 内核培训取向；2025 与学员 Jael Koh 联合演讲（议题与合著者独立印证）

置信度：medium；替代解释：OffensiveCon 频繁出现可能反映该会议对内核利用议题的接受度与邀请偏好，而非个人渠道选择；2024 缺席进一步说明该渠道并非完全稳定。教学-反馈闭环的证据基础主要依赖 research 页自述的 Jael Koh 叙事，『2 个 CVE』无 CVE 编号与独立印证，闭环强度可能被自述放大。

证据：ch-timeline-2020-02-offensivecon-cve2018-8611-ktm, ch-timeline-2023-05-offensivecon-linux-libslub, ch-timeline-2025-05-offensivecon-win11-ktm-jael-koh, ch-timeline-stage4-teaching-2025, r1-offensivecon-2025-jael-koh-ktm, r1-offensivecon-2024-no-halbronn

## 可迁移与不可迁移

- 可迁移：对单一深挖课题采用『会议演讲→长篇多部分博客系列→配套工具』的多渠道分阶段披露流程，而非一次性 PoC 发布，可提升同一研究的影响力与可复用性（机制 1，证据强度 medium，自述面）。
- 可迁移：把研究中反复出现的内部实现分析需求（dlmalloc/ptmalloc、slub、bootloader 调试）固化为可复用调试插件或检测器，使其反哺后续研究线（机制 2，证据强度 low，工具仓库独立印证缺口）。
- 可迁移：把单一 CVE 拆解为补丁分析→触发条件→竞争取胜→读写原语→检测的完整方法论叙事，形成可迁移到不同 CVE 的研究流程模板（CVE-2018-8611 5 部分系列，证据强度 medium，自述面）。
- 可迁移：沿攻击面生态迁移研究目标，快速进入新平台低层并产出 CVE，避免在单一平台过度深耕（机制 3，证据强度 medium，自述面）。
- 不可直接迁移：EZSecLab 为研究对象自创机构，about 页自述『over 15+ years experience』与 2009 首次演讲一致，但实际为 2009-2023 与 2025 持续，2024 为可观察产出断档，不可直接移植为『15+ 年无间断持续』的前提。
- 不可直接迁移：Pwn2Own 获胜作为方向选择反馈，其个人层未获独立印证（维基仅印证 Synacktiv 团队获奖，Halbronn 不在成员名单），不可作为可迁移的外部验证标尺使用。
- 不可直接迁移：Jael Koh 学员回流为联合作者并产出 CVE 的闭环，『2 个 CVE』细节无 CVE 编号与独立来源印证，不可作为可复制教学成效的事实依据。
- 不可直接迁移：OffensiveCon 作为稳定输出渠道本身存在 2024 年度波动，且其频繁出现可能受该会议对内核利用议题的接受偏好影响，不可作为任意会议可复制的渠道策略。
- 不可直接迁移：前雇主（Quarkslab/Google/Seraphic/Synacktiv/NCC Group）与 EZSecLab 创立年份、教育背景等生平细节均无一手来源证实，不可作为能力成长的外部条件迁移。

## 复核问题

- 无关键事实、身份或来源错误。身份闭合成立：GitHub 用户 saidelike 的 profile 姓名为 Cedric Halbronn，saidelike.github.io 301 跳转至 ezseclab.com，ezseclab.com/about 署名 Cedric Halbronn，与 person_json 的 x.com/saidelike handle 一致；综合在 tensions 中保留此身份闭合为少数独立印证之一。
- Black Hat USA 2023/2024 演讲误归因（搜索摘要将 Chintan Shah 的 Under-Documented Features 议题误归于 Halbronn）已在 evidence timeline contradictions 中识别并排除，不计入时间线，处理正确。
- 无将未读取输入以 unknown 占位掩盖的情形；verification.verified_in_run 均按抓取成功标注，未被当作事实或因果成立使用。
- stages 第3条（约 2021-2023，竞赛反馈 + 嵌入式/SOHO + Linux 内核阶段）capability_change：将 Pwn2Own 赛事区分精确化。当前同段落并列 2021 Austin（自述嵌入式，2021-11）与 2021 Vancouver（维基印证 Synacktiv 团队，2021 春季），两者为不同赛事；建议改写为明确区分 about 自述的 2021 Austin 嵌入式个人参赛与维基印证的 2021 Vancouver Synacktiv 团队获奖，避免读者将维基对 Vancouver 团队获奖的印证误读为对 Austin 个人参赛的印证。原措辞：『于 2021 Austin、2022 Toronto 参赛并获胜；需分层标注——Pwn2Own 英文维基百科条目印证 Synacktiv 团队 2021/2022 获奖（2021 Vancouver 成员 Fabien Perigaud、Vincent Dehors...）』。改写方向：在引入维基印证前显式标注 Vancouver 与 Austin 为不同赛事，维基印证对象为 Vancouver 团队而非 Austin 个人参赛。
- transferable_practices 第1条：中性化价值判断措辞。原措辞：『可提升同一研究的影响力与可复用性』；建议改写为『使同一研究在多个发布渠道重复呈现并可被后续工作复用』，以描述可观察的发布行为而非主观价值提升，与证据强度标注（medium，自述面）相称。
- stages 第3条 capability_change 中『据 about 页自述』标注：当前 Pwn2Own 两层标注已写入，但建议在 SOHO/嵌入式方向迁移的归因处（『赛后持续投入 SOHO/嵌入式』）同样补注『据 about/research 页自述』，与 Pwn2Own 标注口径一致，避免因果归因（竞赛推动方向迁移）在自述面上以断言形式呈现。

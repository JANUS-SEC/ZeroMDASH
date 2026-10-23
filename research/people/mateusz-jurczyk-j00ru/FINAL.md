# Mateusz Jurczyk (j00ru)：漏洞研究成长分析

- 擅长领域：Windows 内核与字体漏洞
- 独立复核：pass · 85/100

## 成长阶段

- **2009–2011 · 系统行为逆向的公开写作基线**：在 j00ru.vexillium.org 开始长期公开技术写作（2009-03 首篇），同期在 Hispasec Sistemas 担任安全研究员/恶意软件分析师，形成面向 Windows 平台逆向与系统行为分析的输出习惯，而非以天赋或单次突破为叙事。这一阶段为后续 2013 年起的方法论提供了多年 Win32/内核层逆向积累作为基线。（置信度：medium）
  - 证据：j00ru-works-01, j00ru-timeline-01, j00ru-timeline-02, mj-decisions-01-malware-to-ise
- **2011–2014 · 平台厂商过渡与内核攻击面积累**：从 Hispasec 进入 Google 任信息安全工程师（2011–2014），从乙方恶意软件分析转入平台厂商内部安全，接触 Windows/浏览器大规模攻击面与内部资源；这是其进入专职漏洞研究的中转站，岗位序列的连续迁移构成可观察的成长机制而非抽象天赋。（置信度：medium）
  - 证据：mj-decisions-01-malware-to-ise, j00ru-timeline-03, ext-05-self-about-career-path, j00ru-conv-career-timeline
- **2013–2014 · 全系统插桩方法论的确立与开源化**：与 Gynvael Coldwind 合作出 Bochspwn（SyScan/Black Hat USA 2013），基于 Bochs CPU 级插桩检测内核 double-fetch，发现约 50 个漏洞；方法论从单点漏洞发现转向可复用的系统级检测工具，并以 kfetch-toolkit 名义开源、邀请外部贡献。选择 Bochs 而非 QEMU 基于工具可插桩性的务实选型，而非追逐性能。（置信度：high）
  - 证据：j00ru-works-02, mj-decisions-02-bochspwn-toolbuilding, mj-decisions-03-bochspwn-scope-expansion, j00ru-community-01, j00ru-timeline-05
- **2014–2016 · Project Zero 专职转向与解析面/字体 fuzzing 固化**：约 2014 年转入 Google Project Zero（推断），获得稳定的漏洞披露时间窗口与公开博客渠道，研究重心转向 Windows 内核攻击面、字体解析与沙箱逃逸；2015 年起把 PostScript 手工审计转向对 ATMFD.DLL/win32k.sys 的自动化模糊测试，同年以 'One font vulnerability to rule them all' 四部曲把单 bug 放大为跨目标利用链条；2016 年自述已 'active 超 5 年、工作内外皆用'，模糊测试从一次性实验固化为长期方法。（置信度：medium）
  - 证据：mj-decisions-04-join-project-zero, mj-decisions-05-font-fuzzing-pivot, mj-decisions-06-fuzzing-methodology-talk, j00ru-works-03, j00ru-timeline-06
- **2017–2018 · 插桩平台的迭代复用与污点跟踪升级**：对 2013 年 Bochspwn 工具做二次投资：保留全系统模拟底座，把检测目标从 double-fetch 转向未初始化内核内存向用户态泄露，引入初级内核内存污点跟踪（Bochspwn Reloaded，REcon Montreal 2017），发现近 30 个 Windows infoleak 与十余个 Linux 问题；2017–2018 持续增量原语（x64 支持、去 taint 大容量存储泄露、NtQuery 自动化测试套件、double-write 检测），以 2018-07 白皮书收尾并自述该方向 'for the moment' 暂停。（置信度：high）
  - 证据：j00ru-works-05, j00ru-works-06, mj-decisions-07-bochspwn-reloaded-class-shift, j00ru-timeline-11, j00ru-timeline-15
- **2018 · 内核利用能力向竞技 CTF 场景迁移**：代表 Dragon Sector 参加 WCTF 2018（北京，各队互出题），在 Windows 10 PagedPool off-by-one 中采用 data-only 攻击（破坏相邻索引对象类型字段实现 type confusion），复用 Morten Schenk 2017 的 gDxgkInterface 技术，获亚军（6/18）。把长期内核利用能力迁移到竞技场景，体现'站在前人肩上'而非从零构造。（置信度：high）
  - 证据：j00ru-works-07, j00ru-community-05, j00ru-timeline-14, mj-decisions-08-dragon-sector-ctf-collab

## 主要成长机制

### 全系统插桩底座的复用与增量原语叠加

起点：2011–2014 在 Google 接触 Windows 大规模攻击面，且 Bochs 模拟器具备'直观简单的插桩 API、文档与示例'；与同伴 Gynvael Coldwind 的协作提供了方法论落地的协作条件。

练习与反馈：把同一套 Bochs 全系统 CPU 级插桩底座反复应用到不同 bug 类与不同 OS：2013 检测 double-fetch→2017 加入内核内存污点跟踪检测未初始化内存泄露→2017–2018 叠加 x64 支持、去 taint 大容量存储泄露检测、NtQuery 测试套件、double-write 检测。每一次扩展都在原平台上叠加一个新检测原语，而非另起炉灶。；厂商多轮迭代报告（MS13-016/017/031/036 等）与 Pwnie 2013 'Most Innovative Research' 构成外部正反馈；博客评论区的公开质疑（性能差、无法测试物理硬件驱动、内核代码覆盖受限）被导向白皮书 future work 与后续演讲，形成'发布—收质疑—公开改进说明'的迭代回路。

能力与结果：形成了'识别被忽视的攻击面→在既有插桩平台上叠加一个新检测原语→规模化产出该类漏洞→以白皮书收尾并转向下一类'的可重复研究流程，使一类隐性竞态/泄露条件可被规模化发现。；2013 Bochspwn 在 Windows 内核找到约 50 个 double-fetch 漏洞并促成 MS13-016/017/031/036；2017 Bochspwn Reloaded 发现近 30 个 Windows infoleak、十余个 Linux 问题、17 个 x64-specific bug；2018 白皮书以 'culmination of over a year-long examination' 收尾，并自述该方向 'for the moment' 暂停；2017 DoS 系列 #1–#5 把同一插桩思路复用到'缺异常处理'路径

置信度：high；替代解释：该机制的高度可见性部分受 Google Project Zero 制度红利放大：PZ 提供无产品交付压力的研究环境与公开博客渠道，使其有动机与资源对同一平台做多轮再投资；若剥离 PZ 条件，同等插桩底座复用未必能维持一年多高频迭代。此外 Bochspwn Reloaded 收尾帖称'for the moment'暂停，而同期又有 WCTF 利用输出，说明'方向暂停'不等同于'Windows 内核研究整体停止'，避免将阶段转折过度解读。

证据：j00ru-works-02, j00ru-works-04, j00ru-works-05, j00ru-works-06, mj-decisions-02-bochspwn-toolbuilding, mj-decisions-07-bochspwn-reloaded-class-shift, j00ru-community-01, j00ru-community-02, j00ru-timeline-15

### 模糊测试方法学的固化与跨目标迁移

起点：进入 PZ 后获得对 Windows 字体引擎（ATMFD.DLL/win32k.sys）的攻击面与披露窗口；2015 年承认 'font files are so much more than just the glyph outline programs' 后扩大覆盖。

练习与反馈：2015 把 PostScript Charstring 手工审计转向字体引擎自动化 fuzzing（11 个漏洞）；2016 在 GDI/GDI+/ATMFD.DLL/VMware 虚拟打印机各发现漏洞，并在 Linux 上跨平台 fuzz Windows 用户态 DLL；同月以 Ruxcon/PacSec/Black Hat Europe/Security PWNing 多场会议输出方法论，自述 'active 超 5 年、工作内外皆用'。；将方法外化为可讲授内容（会议输出作为深度反馈），并用 '5+ 年'量化重复练习；Project Zero issue tracker 的 finder 标签（mjurczyk，CVE-2017-0058 issue #1078）构成 PZ 组织对其发现者身份的客观标注（推断）。

能力与结果：形成了一套覆盖语料收集、运行时覆盖率提取、并行化语料蒸馏、多层级目标交互与输入变异的可迁移 fuzzing 流程，并能把同一底层漏洞系统性映射到多个目标（Adobe Reader RCE、Win8.1 32/64 沙箱逃逸）。；2015 字体引擎 fuzzing 11 个漏洞（August 2015 Patch Tuesday）；2016 'One font vulnerability to rule them all' 四部曲：单一字体解析漏洞跨目标利用链；2016 内核字体 fuzzing 约 18 个问题报告 PZ；2016 跨平台在 Linux 上 fuzz Windows 用户态 DLL

置信度：high；替代解释：字体/解析面是 2015–2016 的热门攻击面（Hacking Team 泄露、CVE-2015-2426、Keen Team pwn2own），其在该方向的高产部分受时代红利驱动——攻击面本身被广泛关注而非仅个人选择；与 Hacking Team/Keen Team 的独立撞洞反映'并行识别能力'，但也说明该 bug 类对具备 fuzzing 基础的研究者边际成本递减，个人特有性需打折扣。

证据：j00ru-works-03, mj-decisions-05-font-fuzzing-pivot, mj-decisions-06-fuzzing-methodology-talk, j00ru-community-06, j00ru-timeline-09, ext-08-pz-issue-finder-tag-inferred

### 研究副产品的基础设施化与社区共建

起点：长期 Windows 系统调用逆向积累，以及博客/GitHub 作为公开输出渠道。

练习与反馈：把研究副产品做成可被他人复用的基础设施：Windows 系统调用表项目（NT 3.1–Win11，ntoskrnl.exe/win32k.sys，x86/x64，CSV/JSON/HTML 三格式）开源在 github.com/j00ru/windows-syscalls 并明确'所有评论、建议和 bug 报告都欢迎'；Bochspwn 以 kfetch-toolkit 开源并'looking forward to some meaningful, external contributions'。；syscall 表 GitHub README 致谢 7 位社区贡献者（Woodmann、Deus、Gynvael Coldwind、MeMek、Alex、Omega Red、Wandering Glitch），约 2.6k stars、369 forks，存在持续 issue/PR 外部贡献回流，形成'他人贡献数据→作者整合发布→再被社区使用'的双向回路。

能力与结果：形成了把个人调研副产品转化为公共可复用资产、并主动建立外部贡献反馈渠道的习惯，使个人研究可被同行检验与贡献。；Windows 系统调用表长期维护并被多贡献者扩展；Bochspwn/kfetch-toolkit 开源并被作者定位为可延续的方法谱系（影响 Xenpwn 等）；2016 合著编辑《Praktyczna Inżynieria Wsteczna》，把碎片研究整理为成体系出版物

置信度：medium；替代解释：syscall 表的高 star 数与外部贡献部分受 Windows 内核研究社区的长期需求驱动（该数据本身是众多研究者的基础工件），而非个人独特能力；GitHub star/Fork 是平台流量指标，不直接等同于方法贡献。该机制更宜作为'可迁移做法'而非'个人特有条件'。

证据：j00ru-community-03, j00ru-community-04, j00ru-timeline-07, j00ru-timeline-08, mj-decisions-03-bochspwn-scope-expansion

### 同伴/战队协作与竞技重复练习回路

起点：此前为 Vexillium 计算机爱好者团体成员；2013-02 联合创立 Dragon Sector CTF 战队（CTFtime 2013–2019 排名前 1–4）；长期固定同伴 Gynvael Coldwind。

练习与反馈：长期与 Gynvael Coldwind 共同产出（Bochspwn、Insomni'hack 2015、Pwnie 2013）；通过 Dragon Sector 在顶级战队互出题的对抗格式（如 WCTF 2018）练习内核利用，赛后公开 writeup 把比赛经验沉淀为可复用技术文档。；WCTF 2018 亚军（6/18，奖金 10 万美元）等竞赛结果提供对抗式反馈；CTFtime 长期排名（社区驱动第三方排名，自述转引）构成对战队竞争力的外部量化评价；CTF 组织（CONFidence 2015–2017、Security PWNing 2018–2019）体现把竞赛组织能力沉淀为社区输出。

能力与结果：形成了同伴互证与高强度对抗式重复练习回路，把竞技内核利用经验固化为可复用 writeup 与公开技术。；2013 Bochspwn 与 Gynvael 共同开发并共同报告；2013 Pwnie 'Most Innovative Research' 与 Gynvael 共获；主编其《Zrozumieć Programowanie》(2015)、合著《Praktyczna Inżynieria Wsteczna》(2016)；2018 WCTF PagedPool off-by-one 利用 writeup，亚军 6/18；Bochspwn Reloaded 中同伴协作的方法被单人继承扩展到新一类漏洞

置信度：high；替代解释：Dragon Sector 长期高排名是团队整体能力而非个人机制，j00ru 在其中的边际贡献难以从战队排名单独剥离（CTFtime 排名为自述转引、未独立抓取核验）；与 Gynvael 的合作高度有效，但同伴的可获得性本身是个人特有条件，不应作为可普遍复制的成长路径。

证据：j00ru-conv-dragonsector-cofound, j00ru-conv-gynvael-collab-pwnie2013, j00ru-community-01, j00ru-community-05, mj-decisions-08-dragon-sector-ctf-collab, j00ru-timeline-04

### 系列化披露与会议输出的节奏化习惯

起点：PZ 提供的稳定披露时间窗口与公开博客渠道；Bochspwn 系列被多家独立会议接受。

练习与反馈：把同一研究方向以演讲+幻灯片+白皮书配套形式系统化对外输出，并在不同地域/受众复用：2016-11 一个月内 Ruxcon/PacSec/Black Hat Europe/Security PWNing 同题复讲；2017-02 至 2017-04 连发 DoS 系列 #1–#5；2017 REcon/Black Hat USA/Security PWNing 复讲 Bochspwn Reloaded。；会议同行（多家独立会议外部审查者）反复接受其方法论，构成同行审视；MSRC Top 100 多次上榜（2015 #10、2016 #3、2017 #1、2018 #8、2019 #9，自述）与 Pwnie 2012/2013/2015/2020（自述）构成厂商/同行对其产出量级的量化评价。

能力与结果：形成了'系统研究→系列化披露→按受众/地域拆分多份讲题→白皮书收尾'的节奏化输出习惯，使研究产出可被外部计数与审视。；2017 DoS 系列 #1–#5（CVE-2017-0058 等）系列化披露；2016-11 同月四场会议同题复讲；2018 infoleak 白皮书作为一年多研究的 culmination 收尾；2015–2019 多次 MSRC Top 100（2017 #1），多次 Pwnie（2012/2013/2015/2020）

置信度：medium；替代解释：MSRC Top 100 与 Pwnie 仅有本人 about 页自述支撑，第三方榜单页面 404/未抓取，未独立核验（external contradictions；ext-04 标 reported）。会议密集输出也部分受 PZ 制度要求与厂商披露周期驱动，而非纯个人习惯；'登顶年份与高产期重合'是相关性而非因果证明。

证据：j00ru-works-04, j00ru-works-06, j00ru-community-07, j00ru-conv-recognition-msrc2017, j00ru-timeline-09, j00ru-timeline-10, j00ru-timeline-12, j00ru-timeline-13, ext-04-self-about-msrc-pwnie, ext-06-blog-conference-record

## 可迁移与不可迁移

- 可迁移：在既有插桩/分析底座上叠加单一新检测原语，而非每遇新 bug 类另起炉灶——使一类隐性竞态/泄露条件可被规模化发现（2013→2017→2018 同一 Bochs 底座增量扩展）。
- 可迁移：把模糊测试固化为覆盖语料收集、覆盖率提取、并行语料蒸馏、输入变异的可迁移流程，并跨平台/跨目标复用（Linux 上 fuzz Windows DLL、字体引擎→GDI+→ATMFD→VMware 打印机）。
- 可迁移：把研究副产品做成可被他人复用的基础设施并主动建立外部贡献反馈渠道（syscall 表开源致谢 7 位贡献者；Bochspwn 开源邀请 contribution）。
- 可迁移：以演讲+幻灯片+白皮书配套形式系统化对外输出，并按不同受众/地域拆分多份讲题，最大化传播与同行审视。
- 可迁移：赛后以 writeup 把竞赛/利用经验沉淀为可复用技术文档，把高强度对抗式练习固化为公开资产（WCTF 2018 PagedPool writeup）。
- 可迁移：把厂商多轮迭代报告与公开评论区质疑导向白皮书 future work，形成'发布—收质疑—公开改进说明'的迭代回路。
- 不可直接迁移：Google Project Zero 制度红利：无产品交付压力的专职研究环境、稳定披露窗口与公开博客渠道，使其有动机与资源对同一平台做多轮再投资；剥离该条件，同等插桩底座复用未必能维持一年多高频迭代。
- 不可直接迁移：长期固定同伴 Gynvael Coldwind 的可获得性（Bochspwn 共同开发、Pwnie 共获、著作共编），以及 Dragon Sector 顶级战队（CTFtime 2013–2019 前 1–4）的组织条件——同伴与战队本身是个人特有条件，不应作为可普遍复制的成长路径。
- 不可直接迁移：时代红利：2015–2016 字体/解析面为热门攻击面（Hacking Team 泄露、CVE-2015-2426、Keen Team pwn2own），其在字体方向的高产部分受攻击面本身被广泛关注驱动，与独立撞洞者的并行识别共同说明该 bug 类对具备 fuzzing 基础的研究者边际成本递减。
- 不可直接迁移：本人自 2009 起的多年 Win32/内核层逆向积累作为基线，是 2013 年方法论'凭空出现'的反例——后续方法论建立在多年积累之上而非天赋。
- 不可直接迁移：GitHub star/Fork、CTFtime 排名等是平台流量/团队指标，不直接等同于个人方法贡献，需与个人机制剥离评估。

## 复核问题

- 将机制5 observed_outcomes 中『2015–2019 多次 MSRC Top 100（2017 #1），多次 Pwnie（2012/2013/2015/2020）』改为『自述的 MSRC Top 100/Pwnie 指标（microsoft.com 404、pwnies.com 历史归档未抓取，未独立核验）』，使其与 ext-04 reported 状态与 external contradictions 一致。
- 在机制1 feedback 的『Pwnie 2013 Most Innovative Research』后加『（年份为本人自述，pwnies.com 历史归档未抓取）』限定，避免把未核验奖项表述为确定的外部正反馈。
- 将机制2 feedback 中对 ext-08 的『PZ 组织对其发现者身份的客观标注』弱化为『PZ 组织对其发现者身份的可能标注（推断，issue tracker 需登录未独立核验）』，与 ext-08 inferred 状态一致。
- 在 Stage4『获得稳定的漏洞披露时间窗口与公开博客渠道』后加『（基于 PZ 公开使命的推断，非本人或 PZ 一手确认）』限定，反映 timeline-06 inferred 与 ext-02/ext-03 PZ 当前页未列名的张力。
- 在机制1 alternative_explanation 补一句：PZ 当前页与维基 PZ 条目均未列出本人（ext-02/ext-03），『PZ 制度红利』的解释应限定在 2014–2018 高产期，不应外推为持续在职的制度支持，与 tensions 第1条呼应。
- （可选，低优先）统一全文对 MSRC/Pwnie 这类『自述未核验指标』的措辞口径——凡纳入 observed_outcomes 或 feedback 的，一律带『（自述，未独立核验）』限定，避免因重复出现而累积因果权重。

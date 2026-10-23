# 未通过独立复核

已达到最大修订次数 4；本文件是审计草稿，不得进入跨人物比较。

# Chris Valasek：漏洞研究成长分析

- 擅长领域：汽车与嵌入式漏洞
- 独立复核：revise · 78/100

## 成长阶段

- **截至约 2003 年前 · 学历背景与早期职业基础**：取得匹兹堡大学计算机科学学士学位（入学与毕业年份未在抓取来源中给出，cv-tl-01），并先后任职于 IBM/ISS、Coverity、Accuvant LABS（各段任职起止时间与顺序未给出，cv-tl-02）。早期职业横跨企业安全、静态分析与安全研究咨询，构成其后从一般安全工程转向攻击方法学研究的过渡基础；本阶段未抓取到反映在学期间或早期雇主阶段成长机制（导师、项目、重复练习）的一手材料。（置信度：low）
  - 证据：cv-tl-01, cv-tl-02, cv-deep-03
- **2009–2010 · Windows 堆利用方向**：据维基百科二手记载，2009 年于 Black Hat 发表 Practical Windows XP/2003 Heap Exploitation（与 John McDonald 合著），展示了在 Windows 环境中获取提升权限的新方法；2010 年关于 Low Fragmentation Heap 的后续论文演示了绕过厂商针对其早期工作所加缓解的途径（cv-comm-05、cv-deep-03、chris-valasek-ext-03）。据此推断厂商针对其利用工作加入缓解（推断，无独立来源支撑）。本阶段构成其可观察的『发布利用技术—厂商加缓解—再发布绕过』往返的早期数据点，但仅以 2009、2010 两个维基二手数据点支撑，且 2009/2010 一手来源（Black Hat 2009 议程、PDF、Wayback）本次均未能抓取。（置信度：low）
  - 证据：cv-comm-05, cv-deep-03, chris-valasek-ext-03
- **2013–2014（部分年份未由一手来源消解） · 早期汽车网络研究与公开发表启动**：将此前在 Windows 堆利用方向积累的逆向与利用方法迁移至汽车 ECU/CAN 总线研究，并选择与 Charlie Miller 协作开启汽车安全方向。2013-11-07 于渥太华 COUNTERMEASURE 2013 演讲 Adventures in Automotive Networks and Control Units，分析 CAN 总线并重放专有报文以接管刹车与转向等功能（cv-dec-01、cv-tl-05、cv-deep-03）。早期汽车网络研究以物理接触式（OBD-II/车内 CAN）PoC 为方法起点，针对 Toyota Prius 与 Ford Escape，产生改变速度表及经 CAN 注入控制转向等物理效果（cv-works-002）。该工作经 DEF CON 22（2014）演讲者索引公开化（cv-works-003）。（置信度：medium）
  - 证据：cv-dec-01, cv-tl-05, cv-works-001, cv-works-002, cv-works-003, cv-deep-03, cv-comm-03
- **约 2014（年份未由一手来源消解） · 跨车型远程攻击面系统调查**：由早期单车型物理接触式 PoC 转向对当代车型的远程攻击面系统调查，方法学由『能否攻破一辆』转向跨车型可比较的攻击面评估（cv-works-005、cv-dec-02）。illmatics.com 一手索引页不为该论文标注年份、会议或日期（cv-rev1-001），故 A Survey of Remote Automotive Attack Surfaces 的发表年份在 cv-works-005 标 2014 与 cv-comm-03 记 2013 之间未由一手来源消解，本阶段年份不作已确认事实陈述。该调查在二手来源中被评价为汽车安全与安全研究现状的重要起步，但构成同行反馈机制的证据不足。（置信度：medium）
  - 证据：cv-works-005, cv-dec-02, cv-comm-03, cv-rev1-001
- **2015 · 远程入侵实证与 CAN 注入纵深衔接**：攻击面由车内物理接触信道扩展到外部远程可达信道，方法由物理接触式 CAN 注入演进到经蜂窝（cellular）连接的远程入侵并达成对车辆的物理控制（cv-works-004）。在已有 CAN 注入基础上推进到 Advanced CAN Message Injection，与远程到达衔接形成『远程到达 → CAN 注入 → 物理动作』的链路（cv-works-006、cv-works-007）。2015-07 Wired 报道记录 Jeep Cherokee 远程接管演示，构成研究向行业可见的安全事件转化（cv-dec-03、cv-comm-04、chris-valasek-ext-01）；DEF CON 23 演讲者索引证实其与 Miller 共同列名（cv-tl-06）。Wired 一手报道页面未抓取，召回规模与报道日期仅经维基二手转述到达。（置信度：medium）
  - 证据：cv-works-004, cv-works-006, cv-works-007, cv-dec-03, cv-comm-04, cv-tl-06, chris-valasek-ext-01
- **约 2017 年起 · 厂商内部汽车安全角色**：据维基二手转述 USA Today 2017 报道，Cruise 聘用 Miller 与 Valasek；其后 Valasek 任 Cruise Automation 安全研究员，最终任 General Motors Senior Director，完成从第三方研究机构（IOActive）到汽车厂商内部的角色转换（cv-dec-04、chris-valasek-ext-02）。该转向仅由维基二手（reported 级）支撑，Cruise/General Motors 机构一手页面未取得，USA Today 2017 原文未抓取；Charlie Miller 维基页确认 Miller 在 Cruise 与 Uber，但全页对 Valasek 加入 Uber/Cruise/GM 只字未提（cv-r2-001），故无二手交叉印证。General Motors Senior Director 在本阶段作为 reported 级外部可观察角色呈现，不作为已核验能力项。（置信度：low）
  - 证据：cv-dec-04, chris-valasek-ext-02, cv-r2-001

## 主要成长机制

### 公开作品、工具与数据集中发布

起点：2013 年起进入汽车安全方向并与 Charlie Miller 建立合著关系时，已具备通过统一站点长期集中公开研究材料的条件——illmatics.com 索引页以『we (Charlie Miller and Chris Valasek)』第一人称署名（cv-works-001），并按论文、工具、数据压缩包（content.zip）的形式组织发布。

练习与反馈：跨 2014–2015 在 illmatics.com 集中发布 Adventures in Automotive Networks and Control Units、A Survey of Remote Automotive Attack Surfaces、Remote Compromise of an Unaltered Passenger Vehicle、Advanced CAN Message Injection 等多部作品，并附『All our tools and data!』工具与数据包（cv-works-001、cv-works-002、cv-works-004、cv-works-005、cv-works-006）；将工作提交至 DEF CON 22（2014）演讲者索引公开（cv-works-003），并据维基二手经 DEF CON 23（2015）列名（cv-tl-06）。这一发布形式在多部作品中重复出现。；可核验的反馈主要来自公开作品索引页（illmatics.com）的持续发布与会议演讲者索引的列名收录（cv-works-001、cv-works-003、cv-tl-06）；会议录用本身可证作品经审稿/录用程序对外传播，但不等同于对成长机制的评价。维基二手转述的『an important first step』为第三方评价性转述，不作为机制反馈证据（cv-comm-03）。

能力与结果：形成可比较的攻击面评估能力，体现于由单车型 PoC 转向跨车型远程攻击面系统调查（cv-works-005、cv-dec-02）；该调查的发表年份未由一手来源消解（cv-rev1-001）。；2013-11-07 COUNTERMEASURE 2013 演讲 Adventures in Automotive Networks and Control Units（cv-dec-01、cv-tl-05）；DEF CON 22（2014）演讲者索引列出 Valasek 与 Miller（cv-works-003）；2014 跨车型远程攻击面调查作为单车型 PoC 之后的系统比较工作（cv-works-005、cv-dec-02）；2015 Jeep 远程入侵与 Advanced CAN Message Injection 经 illmatics.com 集中发布（cv-works-004、cv-works-006）

置信度：medium；替代解释：公开作品序列的可见性受发表筛选约束：未发表的练习、失败或被拒稿件不可见，可观察的成长受发表筛选限制。集中发布形式本身也可能是合著伙伴 Charlie Miller 共同的工作习惯，难以在合著框架内分离为 Valasek 个人特有做法。

证据：cv-works-001, cv-works-002, cv-works-003, cv-works-004, cv-works-005, cv-works-006, cv-dec-01, cv-tl-05, cv-tl-06, cv-comm-03, cv-rev1-001

### 方法沿攻击面纵深迭代

起点：早期汽车网络研究以物理接触式 PoC 为方法起点，针对 Toyota Prius 与 Ford Escape，通过 OBD-II/车内 CAN 嗅探与注入、ECU 固件逆向建立方法基础，产生的物理效果包括改变速度表及经 CAN 注入控制转向（cv-works-002）。

练习与反馈：由单车型物理接触式 PoC 转向跨车型远程攻击面系统调查（cv-works-005），再演进到经蜂窝连接的远程入侵并达成物理控制（cv-works-004），并在已有 CAN 注入基础上推进到 Advanced CAN Message Injection，与远程到达衔接形成『远程到达 → CAN 注入 → 物理动作』的链路（cv-works-006、cv-works-007）。沿同一技术栈纵深迭代，沿用同一套逆向与注入工作流，而非对新对象另建独立工作流。；可核验的反馈来自 illmatics.com 一手索引页对作品序列的连续呈现（cv-works-001 至 cv-works-006），作品按方法演进顺序在同一站点并列发布；该呈现本身不构成对单部作品的同行评价，仅为方法连续性的可核验呈现。

能力与结果：形成沿攻击面纵深迭代的方法学连续性——由物理接触式 CAN 注入到远程蜂窝入侵再到 advanced CAN 注入，构成同一技术栈的纵深推进（cv-works-002、cv-works-004、cv-works-006）。；早期物理接触式 CAN 嗅探/注入与 ECU 固件逆向方法基础（cv-works-002）；跨车型远程攻击面系统调查（cv-works-005）；经蜂窝连接的远程入侵并达成物理控制（cv-works-004）；Advanced CAN Message Injection 衔接远程到达与车内执行（cv-works-006）

置信度：medium；替代解释：演化方向（物理接触→远程、单车型→跨车型、CAN 注入纵深迭代）由 illmatics.com 作品清单与描述推断得到（cv-works-007 标记为 inferred），各 PDF 正文为 FlateDecode 压缩无法提取，方法演进细节仅基于索引页转述或推断，未由一手正文逐节佐证。与 Miller 长期合著使个人贡献与合著伙伴贡献难以分离。

证据：cv-works-002, cv-works-004, cv-works-005, cv-works-006, cv-works-007

### 与 Charlie Miller 长期合著

起点：2013 年前后进入汽车安全方向时，与 Charlie Miller 建立合著关系——illmatics.com 索引页以『we (Charlie Miller and Chris Valasek)』第一人称署名（cv-works-001），2013-11-07 COUNTERMEASURE 2013 为二人合作演讲的早期公开节点（cv-dec-01、cv-tl-05）。

练习与反馈：跨 2013–2017 在多部作品与多个公开场合以二人合著形式出现：COUNTERMEASURE 2013 演讲（cv-dec-01、cv-tl-05）、DEF CON 22（2014）演讲者索引（cv-works-003）、跨车型远程攻击面调查（cv-comm-03、cv-dec-02）、2015 Jeep 远程入侵（cv-dec-03、cv-comm-04、cv-tl-06）、约 2017 年同被 Cruise 聘用的报道（cv-dec-04、chris-valasek-ext-02）。；合著关系本身不直接提供对个人成长机制的评价；可核验的反馈来自二人合著作品的持续公开发布与会议列名（cv-works-001、cv-works-003、cv-tl-06）。Charlie Miller 维基页仅以 Jeep Cherokee 合著者提及 Valasek 一次，未记载 Valasek 加入 Uber/Cruise/GM（cv-r2-001）。

能力与结果：形成稳定的合著协作框架，使方法在多车型、多攻击面间迁移时保持合作连续性（cv-works-001、cv-comm-03、cv-dec-02）。；2013-11-07 COUNTERMEASURE 2013 合著演讲（cv-dec-01、cv-tl-05）；DEF CON 22（2014）二人共同列名（cv-works-003）；2014 跨车型远程攻击面调查合著（cv-comm-03、cv-dec-02）；2015 Jeep 远程入侵合著并经 Wired 转述（cv-dec-03、cv-comm-04）；约 2017 年报道转述二人在 Cruise 再度合作（cv-dec-04、chris-valasek-ext-02）

置信度：medium；替代解释：长期合著关系在安全研究领域并不罕见，其延续性可能同时由共同的方法基础、外部资助（据 cv-tl-08 lead_only 称研究受 DARPA 资助，未由一手确认）与机构路径（Cruise/GM）等多重因素维持，不必然反映个人层面的成长机制；与 Miller 长期协作使个人贡献与合著伙伴贡献难以分离。

证据：cv-works-001, cv-works-003, cv-dec-01, cv-tl-05, cv-comm-03, cv-dec-02, cv-dec-03, cv-comm-04, cv-tl-06, cv-dec-04, chris-valasek-ext-02, cv-r2-001

### 利用—缓解—绕过往返（推断）

起点：2009 年于 Black Hat 发表 Practical Windows XP/2003 Heap Exploitation（与 John McDonald 合著），展示了在 Windows 环境中获取提升权限的新方法（cv-comm-05、cv-deep-03、chris-valasek-ext-03）。

练习与反馈：据维基二手记载，2010 年关于 Low Fragmentation Heap 的后续论文演示了绕过厂商针对其早期工作所加缓解的途径（cv-comm-05、cv-deep-03）。该往返以 2009、2010 两个数据点支撑。；可核验的反馈仅为公开作品与会议发表本身；厂商是否针对其利用工作加入缓解，无独立一手来源支撑，仅能由 2010 年绕过研究的存在反推（推断）。该中间环节未被独立来源确认。

能力与结果：据此推断形成与厂商缓解措施直接对抗的研究习惯（推断，非已证因果）；该习惯是否平滑迁移至汽车/嵌入式方向，缺乏跨材料重复的数据点支撑。；2009 Black Hat Practical Windows XP/2003 Heap Exploitation（cv-comm-05、chris-valasek-ext-03）；2010 Low Fragmentation Heap 绕过研究（cv-comm-05、cv-deep-03）

置信度：low；替代解释：该往返仅以 2009、2010 两个数据点支撑且均来自维基二手，不满足跨材料重复；『形成对抗式研究习惯』为推断而非已证因果，不应升级其因果结论强度。2009/2010 一手来源（Black Hat 2009 议程、PDF、Wayback）本次均未能抓取，年份、合著者与具体演讲标题仍仅由维基二手支撑。

证据：cv-comm-05, cv-deep-03, chris-valasek-ext-03

### 安全社区长期组织角色

起点：据维基二手记载，自 2003 年起加入 Summercon 组委会（cv-comm-02、chris-valasek-ext-04）；Summercon 自述自 1987 年起举办，定位为刻意保持小型与社交属性的老牌黑客会议（cv-comm-01）。

练习与反馈：在 Summercon 承担长期组织角色：Phrack #68（2012-04-14）第三人称记载 Redpantz（Valasek 常用名）在 Summercon 于匹兹堡举办期间加入规划委员会并开始担任主持（cv-deep-02）；Summercon 官方组织者页面现将其列为 Chairman Emeritus（cv-comm-01）。；可核验的反馈来自 Summercon 官方组织者页面的持续列名（cv-comm-01）与 Phrack 社区史文章的第三人称记载（cv-deep-02）；该角色提供日常接触同行、筛选议题与维持研究圈关系的持续通道，但未抓取到对其具体能力评价或导师关系的一手陈述。

能力与结果：形成稳定的社区参与与同伴网络锚点——由成员到规划委员会再到主持/Chairman Emeritus 的角色扩展（cv-deep-02、cv-comm-01）。；自 2003 年起参与 Summercon 组委会（cv-comm-02、chris-valasek-ext-04）；加入规划委员会并开始担任主持（cv-deep-02）；现列为 Summercon Chairman Emeritus（cv-comm-01）

置信度：medium；替代解释：Summercon 官方页面未给出 Valasek 的具体任职起止年份（仅现职 Chairman Emeritus 与头像时间戳约 2021-04），『自 2003 年起参与组委会』仅由维基二手支撑，缺 Summercon 自身一手档案佐证；社区组织角色与个人技术能力成长之间的因果关系未由一手材料确认。

证据：cv-comm-01, cv-comm-02, cv-deep-02, chris-valasek-ext-04

## 可迁移与不可迁移

- 可迁移：沿用同一套逆向与注入工作流迁移至新攻击面对象，而非对新对象另建独立工作流——由 Windows 堆利用的逆向与利用方法迁移至汽车 ECU/CAN 总线研究，再沿物理接触→远程、单车型→跨车型方向纵深迭代（cv-works-002、cv-works-005、cv-works-004、cv-works-006）。
- 可迁移：将论文、工具与数据一并集中发布，便于他人复现与外部复核——illmatics.com 索引页以『All our tools and data!』附工具与数据压缩包，论文与工具并列公开（cv-works-001、cv-works-002）。
- 可迁移：在固定合著伙伴框架内保持长期协作，使方法在多车型、多攻击面间迁移时保持合作连续性（cv-works-001、cv-comm-03、cv-dec-02、cv-dec-04）。
- 可迁移：『论文 + 工具 + 数据』一并发布是 Valasek 与 Miller 二人的工作方式（据 illmatics.com 索引页），不应泛化为整个漏洞挖掘研究者类别的特征（cv-works-001）。
- 不可直接迁移：早期联网汽车攻击面未被系统比较的时间窗口：2013–2014 年联网汽车远程攻击面尚未被系统比较，该时间窗口为二人早期汽车安全研究提供先发可见性，属特定时期的外部条件，不可迁移至已系统化覆盖的后期环境。
- 不可直接迁移：Black Hat / DEF CON / COUNTERMEASURE 等会议的录用与公开发表通道，以及 illmatics.com 个人作品索引页的自主发布能力，属特定时期可用的公开发表基础设施，不可简单迁移至其他研究对象或受限环境。
- 不可直接迁移：与 Charlie Miller 的长期合著关系及二人共同的机构路径（Cruise/GM），属个人协作条件，不可作为个人独立可迁移的做法。
- 不可直接迁移：Summercon 作为刻意保持小型与社交属性的老牌黑客会议所提供的同伴网络锚点，属特定社区的外部条件，不可迁移至其他研究对象。
- 不可直接迁移：DARPA 资助（据 cv-tl-08 lead_only 称研究受 DARPA 资助，未由一手确认）等外部资助条件属特定时期的外部资源，不可作为个人可迁移的做法。

## 复核问题

- mechanisms[0]（公开作品、工具与数据集中发布）.repeated_practice 将 cv-tl-06 误标为「维基二手」：原文「并据维基二手经 DEF CON 23（2015）列名（cv-tl-06）」。cv-tl-06 的来源为 DEF CON 23 演讲者索引页（https://defcon.org/html/defcon-23/dc-23-speakers.html，source_type=会议演讲者索引页面，level=authoritative_secondary），非维基百科。同句 cv-works-003（DEF CON 22 演讲者索引）正确归因为「演讲者索引公开」，cv-tl-06 与之同属 DEF CON 官方索引却被标为「维基二手」，构成来源归因错误，影响该机制反馈与重复练习叙述的证据层级表述。
- mechanisms[4]（安全社区长期组织角色）.intermediate_capability 保留比喻性表达「同伴网络锚点」：原文「形成稳定的社区参与与同伴网络锚点——由成员到规划委员会再到主持/Chairman Emeritus 的角色扩展」。「锚点」为比喻性表达，违反语言规范（禁止比喻性表达）。复核历史 round-3 RR2 已明确要求删除「锚点」比喻并改为平实表述，v5 仅在 mechanisms[4].name 删除「锚点」，但 intermediate_capability 仍保留「同伴网络锚点」，未消除该违规。
- mechanisms[0]（公开作品、工具与数据集中发布）.repeated_practice：原措辞「并据维基二手经 DEF CON 23（2015）列名（cv-tl-06）」将 cv-tl-06 误标为「维基二手」。改写方向：改为「并经 DEF CON 23（2015）演讲者索引列名（cv-tl-06）」，删除「据维基二手」，使 cv-tl-06 的来源归因（DEF CON 23 演讲者索引页，authoritative_secondary 会议索引）与同句 cv-works-003（DEF CON 22 演讲者索引）的归因一致。
- mechanisms[4]（安全社区长期组织角色）.intermediate_capability：原措辞「形成稳定的社区参与与同伴网络锚点——由成员到规划委员会再到主持/Chairman Emeritus 的角色扩展（cv-deep-02、cv-comm-01）」中「同伴网络锚点」为比喻性表达。改写方向：改为「形成稳定的社区参与与同伴网络的持续接触场景——由成员到规划委员会再到主持/Chairman Emeritus 的角色扩展」，删除「锚点」比喻，与 mechanisms[4].name（已删除「锚点」）一致。
- mechanisms[4].feedback：原措辞「该角色提供日常接触同行、筛选议题与维持研究圈关系的持续通道」中「持续通道」略带比喻色彩。改写方向：改为「该角色提供日常接触同行、筛选议题与维持研究圈关系的持续途径」，将「通道」改为「途径」。
- mechanisms[4].alternative_explanation：当前仅含「Summercon 官方页面未给出 Valasek 的具体任职起止年份」与「社区组织角色与个人技术能力成长之间的因果关系未由一手材料确认」两项限制，未显式标注知名度/可见性偏差。改写方向：补充「Summercon 长期组织角色与公开作品序列的知名度可能放大组织角色对成长机制的贡献权重，据现有证据难以分离社区组织本身与公开声望对能力反馈的分别贡献」，使该机制偏差限制层级与 mechanisms[0]-[3] 一致。
- stages[4]（远程入侵实证与 CAN 注入纵深衔接）.capability_change：当前仅提「Wired 一手报道页面未抓取，召回规模与报道日期仅经维基二手转述到达」，未明确标注可见性偏差。改写方向：在该 stage 或其紧邻处补「该阶段可见性部分源于 Wired 媒体放大报道（Wired 一手未抓取），可见性不等同于技术能力成长」，使 stage 层叙述与 mechanisms[0]/[1] alternative_explanation 的偏差标注层级一致。
- mechanisms[2]（与 Charlie Miller 长期合著）.intermediate_capability：原措辞「形成稳定的合著协作框架，使方法在多车型、多攻击面间迁移时保持合作连续性」中「稳定」为对合著关系持续性的断言，仅由作品序列推断，无来源直接支撑。改写方向：改为「形成跨多车型、多攻击面的合著协作框架，使方法迁移时保持合作连续性」，删除「稳定」断言，或在该处 alternative_explanation 显式补「稳定性仅据合著作品序列推断，无来源直接支撑，且受合著归因偏差限制」。

# Joe FitzPatrick：漏洞研究成长分析

- 擅长领域：硬件与供应链漏洞
- 独立复核：pass · 78/100

## 成长阶段

- **约 2011—2012（推断） · CPU 渗透测试从业者向内部讲师过渡**：据 2016-10 自述（jf-deepself-01），FitzPatrick 此前从事 CPU 的硅前与硅后渗透测试，约 2011 年前后仍在该岗位，随后在内部向功能验证人员讲授硬件安全课程。据此可定位其职业起点为一线硬件渗透测试，第一次能力迁移是『研究者→内部讲师』：把一线测试经验组织成可授课内容，而非直接跳到外部训练。该阶段为后续独立训练事业的直接前身，但为推断性时间线，非直接文献记录。（置信度：low）
  - 证据：jf-deepself-01
- **2012-11—2013 · 公开写作起步与方法论框架化；2013 起逐年公开训练**：公开写作输出始于 2012-11《Hacking the Nikon WU-1a》《Retail Hacking for Fun and Savings》（jf-tl-001/002、jf-decisions-01），为消费级硬件拆解/改造；2013-04-23《Hierarchy of Hardware Attacks》（jf-tl-003、jf-ext-08）转向硬件攻击分层框架，主题从单一设备改造抽象为可传播方法论。同年起公开训练输出：据 jf-r1-001（2017-12-31 一手自述）逐年训练时间线，2013 交付 Sidechannels for Hardware N00Bz 与 WTFPGA 短工作坊；此节点替代此前依赖 verified_in_run=false 的 jf-deepself-08 对 2013 的支撑。2016-10 文章（jf-deepself-02）自述创办 SecuringHardware.com 的动机为『有效培训的杠杆效应』与『行业内硬件安全实践资料匮乏』，创办年份未由一手来源明确；据 jf-r1-001 称 2017 年为第五个成功年度，反推创办约 2012/2013（推断）。（置信度：medium）
  - 证据：jf-tl-001, jf-tl-002, jf-tl-003, jf-decisions-01, jf-ext-08, jf-deepself-02, jf-r1-001
- **2014—2017 · 工具导向写作与逐年新训练课程**：2014-08-12《NSA Playset - SLOTSCREAMER, HALIBUTDUGOUT, and ALLOYVIPER for PCIe and Thunderbolt DMA Attacks》（jf-tl-004、jf-ext-07）标志从纯写作进入硬件攻击工具设计/公开，DMA 攻击方向成型；NSA Playset 为公开研究项目名，不构成本人就业证据，其与 NSA 的个人/职业关系为资料缺口。2017-01-25《Black Hat Hardware Training Roadmap》（jf-tl-005、jf-ext-06）以路线图梳理 Black Hat 硬件培训生态，可推断从研究者向研究者兼教育者角色扩展，但 Black Hat 讲师身份的独立页面核验失败（403/404），为推断。据 jf-r1-001，2014/2015/2016/2017 逐年交付新课程（Software Exploitation via Hardware Exploits；Applied Physical Attacks on x86 Systems；Applied Physical Attacks on Embedded Systems；Applied Physical Attacks and Hardware Pentesting），并自述『自起步起每年开发一门新课』。2016-10 自述以口碑替代常规商业套路建立业务（jf-deepself-03）。（置信度：medium）
  - 证据：jf-tl-004, jf-ext-07, jf-tl-005, jf-ext-06, jf-r1-001, jf-deepself-03
- **2018—2019 · 失败外显化与来源—证据链分析**：2018-03-29《Submitting to a CFP》与 2018-06-04《Congratulations, your submission has been declined!》（jf-tl-006/007、jf-ext-03/04、jf-decisions-04、jf-deepself-06）把投稿与被拒作为公开写作主题，主张失望可接受、认输不可接受、寻求反馈与持续改进为正解；该文以第二人称指导口吻呈现，未披露本人具体某次被拒细节。2019-10-03 针对 Bloomberg《The Big Hack》供应链植入报道发表两篇复盘（jf-tl-010、jf-pubworks-001/002、jf-ext-05、jf-community-01/02、jf-decisions-05），方法从『植入物技术是否可能』升级为对二手叙事的来源—证据链溯源（逐一编号清点 17 个来源、追踪各自贡献），并以 firedrill 框架提出资源分配与威胁建模原则。该阶段可核验产出为『事件→复盘→可执行原则』的固定写作路径。（置信度：high）
  - 证据：jf-tl-006, jf-tl-007, jf-ext-03, jf-ext-04, jf-decisions-04, jf-deepself-06, jf-tl-010, jf-pubworks-001, jf-pubworks-002, jf-ext-05, jf-community-01, jf-community-02, jf-decisions-05
- **2020—2026 · 硬件工具产品化与训练持续迭代**：进入硬件工具批次化生产与训练课程持续重写阶段。tigard-tools/tigard README 实列 8 个生产批次：1st 28（2020-07-05）、2nd 42（2020-08-05）、3rd 496（2020-10）、4th 693（2021-01，v1.1 引入 logic analyzer 端口与 I2C JST SH 接口）、5th 697（2021-09，记录选择性波峰焊缺陷与通孔元件返工）、6th 1400（2022-11）、7th 1400（2024-01，记录 JTAG header 组装位置错误）、8th 2100（2025-01），合计约 6856 块，README 未声明累计总数；旧证据 jf-tl-011~015 仅含其中 5 批，不得据其外推总数（jf-r1-002）。训练侧：Applied Physical Attacks 2 经显著重写、新硬件与流程精简后以自定节奏在线课程重新发布（jf-community-05），并主办 CanSecWest 2026 四日训练《Applied Hardware Attacks: Rapidly Prototyping Hardware Implants》（jf-community-03、jf-tl-016、jf-ext-01）。当前以 SecuringHardware.com / Hardware Security Resources, LLC（波特兰）独立运营（jf-tl-017、jf-decisions-06）。（置信度：high）
  - 证据：jf-r1-002, jf-tl-011, jf-tl-012, jf-tl-013, jf-tl-014, jf-tl-015, jf-community-05, jf-community-03, jf-tl-016, jf-ext-01, jf-tl-017, jf-decisions-06

## 主要成长机制

### 事件—复盘—可执行原则的写作回路

起点：硬件安全领域同时存在二手叙事放大问题（如 Bloomberg 2018 Big Hack 供应链植入报道引发社区大量物理搜寻微小芯片）与个人作为研究员被记者咨询的位置（jf-community-01：自述曾被问及『what's a coupler』、看过早期草稿并指出技术描述缺陷，记者随后将技术性表述改写为归因于『people familiar with the chips operation』）。

练习与反馈：把一次性公共事件或一次性咨询转化为公开长文复盘：Big Hack 事件期间 2018-10-04/08 在 Twitter 发初步想法与后续线索（原帖未在本轮直接抓取，标记 inferred，据 2019 复盘文章交叉印证 jf-pubworks-005），2019-10-03 发表两篇复盘（jf-pubworks-001/002、jf-tl-010）；方法上对二手叙事逐条编号清点匿名来源、追溯各自实际贡献，而非整体采信或否定（jf-decisions-05 自述『torn between defending that many of the claims were technically possible versus challenging that the whole story fit together logically』）。该模式在 CFP 主题写作中同样出现：把投稿被拒系统化为可讨论、可改进的方法（jf-tl-006/007、jf-deepself-06）。；双向反馈回路：对记者提供技术反馈并据其修订措辞（jf-community-01）；接收社区反馈（大量请其分析硬件是否被植入的咨询、riskybusiness podcast 听众致谢，Kim Zetter、Patrick Gray 说服其公开表态，jf-community-02）。

能力与结果：形成『来源—证据链溯源 + 可靠性分级』的固定方法论与可执行原则输出能力：firedrill 框架提出不为非己方威胁模型买单、勿因追求昂贵供应链攻击场景而忽略 5 美元级别攻击面（jf-pubworks-002 短引『don't waste resources on them if you're not protecting against $5 attacks』）。；2019-10-03 两篇 Big Hack 复盘文章，对 17 个匿名来源逐一编号并标注核心技术主张仅依赖其中一两个来源（jf-pubworks-001）。；2018-06-04 投稿被拒处理文章，把失败显性化为寻求反馈与持续改进的方法（jf-deepself-06）。；把争议事件沉淀为可指导后续实践的威胁建模原则（jf-pubworks-002）。

置信度：high；替代解释：该写作回路也可部分解释为个人博客作者的常规习惯，而非独特成长机制；其区分度在于方法论具体性（来源编号、可靠性分级）与跨主题复用（供应链事件与投稿被拒同构），仅凭写作频率不足以证明。

证据：jf-pubworks-001, jf-pubworks-002, jf-pubworks-005, jf-tl-006, jf-tl-007, jf-tl-010, jf-community-01, jf-community-02, jf-decisions-05, jf-deepself-06

### 反馈驱动的硬件工具批次迭代

起点：2014 年已以公开可复现工具介入领域（SLOTSCREAMER/HALIBUTDUGOUT/ALLOYVIPER，jf-ext-07、jf-tl-004），具备硬件攻击工具设计能力；运营 Hardware Security Resources, LLC 作为产品化载体（jf-tl-017）。

练习与反馈：2020-07-05 起 Tigard 进入可批量生产、对外销售的开源硬件工具（CC-BY-SA 4.0，派生自 TIMEP，jf-tl-011）。此后据使用反馈与制造缺陷记录逐批迭代：第 4 批（2021-01）引入 logic analyzer 端口与 I2C JST SH 接口（jf-tl-012）；第 5 批（2021-09）记录选择性波峰焊缺陷与通孔元件返工（jf-tl-013）；第 7 批（2024-01）记录 JTAG header 组装位置错误（pin 1 空置而非 pin 9，jf-tl-014）。据 jf-r1-002，tigard-tools/tigard README 实列 8 个批次，合计约 6856 块，README 未声明累计总数；旧证据 jf-tl-011~015 仅含其中 5 批，不得外推总数。；使用反馈（新增接口方向）+ 制造缺陷记录（选择性波峰焊缺陷、JTAG header 位置错误）构成两类反馈来源，并以 README 批次条目公开记录缺陷与修正，形成工程实践中的失败—修正循环。

能力与结果：硬件工具的反馈驱动版本演进能力：将一次性硬件原型扩展为可批量生产、版本化、文档化缺陷修正的产品线。注：Erebus 据 about 页被点名为其构建的工具之一（jf-r1-004），但 tigard-tools 组织无 erebus/epic-erebus 公开仓库（jf-r1-003），仅有点名级证据，不构成本机制的反馈迭代产出，已移出 observed_outcomes。；Tigard README 实列 8 个生产批次（2020-07 至 2025-01），合计约 6856 块，README 未声明累计总数（jf-r1-002）。；v1.1 批次据反馈引入 logic analyzer 端口与 I2C JST SH 接口（jf-tl-012）。；第 5、7 批次公开记录制造/组装缺陷与返工/修正（jf-tl-013、jf-tl-014）。

置信度：high；替代解释：批次化生产也可归因于商业产品化需求而非反馈学习机制；其区分度在于 README 对缺陷的公开记录与逐批接口演进，仅凭产量不足以证明反馈驱动。

证据：jf-tl-004, jf-ext-07, jf-tl-011, jf-tl-012, jf-tl-013, jf-tl-014, jf-tl-015, jf-r1-002, jf-r1-003, jf-r1-004, jf-tl-017

### 逐年新训练课程作为课程迭代载体

起点：约 2011—2012 从 CPU 硅前/硅后渗透测试从业者转为内部讲师（jf-deepself-01）；2016-10 自述创办 SecuringHardware.com 的动机为有效培训的杠杆效应与行业资料匮乏，并以口碑替代常规商业套路建立业务（jf-deepself-02、jf-deepself-03）。创办年份未由一手来源明确；据 jf-r1-001 称 2017 年为第五个成功年度，反推创办约 2012/2013（推断）。

练习与反馈：据 jf-r1-001（2017-12-31 一手自述）逐年训练时间线，2013 交付 Sidechannels for Hardware N00Bz 与 WTFPGA 短工作坊；2014 Software Exploitation via Hardware Exploits（2016 废弃）；2015 Applied Physical Attacks on x86 Systems；2016 Applied Physical Attacks on Embedded Systems；2017 Applied Physical Attacks and Hardware Pentesting；并自述『自起步起每年开发一门新课』。2017-01-25《Black Hat Hardware Training Roadmap》（jf-tl-005、jf-ext-06）以路线图整合 Black Hat 硬件培训生态。2026 年 Applied Physical Attacks 2 经显著重写后以自定节奏在线课程重新发布（jf-community-05），并主办 CanSecWest 2026 四日训练《Applied Hardware Attacks: Rapidly Prototyping Hardware Implants》（jf-community-03）。；据 jf-community-05 自述，课程持续重写（APA2 在线自定节奏版）为按学员反馈迭代内容；但本轮未取得训练学员的具体反馈样本（评价、改进意见），该反馈回路形态部分基于自述，未见外部评价（社区维度 gaps）。

能力与结果：将一次性研究/教学经验沉淀为可复用、逐年扩展、多格式（公开/私下/在线）交付的训练课程体系，并以课程迭代作为能力维持与方向调整载体。；2013—2017 逐年新增训练课程（jf-r1-001）。；Applied Physical Attacks 2 重写并以自定节奏在线课程重新发布（jf-community-05）。；CanSecWest 2026 四日训练《Applied Hardware Attacks: Rapidly Prototyping Hardware Implants》，学员从零搭建多枚硬件植入物（jf-community-03）。

置信度：medium；替代解释：逐年新课也可解释为培训业务的产品扩展策略而非能力成长机制；其区分度在于课程内容随硬件攻击主题演进（x86→嵌入式→硬件植入物快速原型），仅凭课程数量不足以证明。

证据：jf-deepself-01, jf-deepself-02, jf-deepself-03, jf-r1-001, jf-tl-005, jf-ext-06, jf-community-03, jf-community-05, jf-tl-016

## 可迁移与不可迁移

- 可迁移：把一次性公共事件或一次性咨询转化为公开长文复盘，并对二手叙事逐条编号清点来源、追踪各自贡献与可靠性，形成『来源—证据链溯源 + 可靠性分级』的可复用方法论（jf-pubworks-001、jf-community-01）。
- 可迁移：把投稿被拒等失败显性化为可讨论、可改进的方法：失望可接受、认输不可接受、寻求反馈与持续改进为正解（jf-deepself-06、jf-tl-007）。
- 可迁移：以 firedrill 框架做资源分配与威胁建模取舍：不为非己方威胁模型买单、勿因追求昂贵供应链攻击场景而忽略廉价攻击面（jf-pubworks-002）。
- 可迁移：硬件工具批次化过程中以 README 公开记录制造/组装缺陷与修正，形成工程实践中的失败—修正循环（jf-tl-013、jf-tl-014、jf-r1-002）。
- 可迁移：逐年新增训练课程并把课程重写为多格式（公开/私下/在线自定节奏）交付，以课程迭代作为方向调整载体（jf-r1-001、jf-community-05）。
- 不可直接迁移：CPU 硅前/硅后渗透测试的从业背景为个人特定条件，非一般研究者可复制（jf-deepself-01）。
- 不可直接迁移：在 Big Hack 事件中被记者咨询、看过早期草稿的位置，是个人特定机会，非可迁移方法（jf-community-01、jf-community-02）。
- 不可直接迁移：Hardware Security Resources, LLC 的公司化运营实体与 Tigard 批量生产能力为个人特定资源条件（jf-tl-017、jf-r1-002）。
- 不可直接迁移：BSides Portland、CTRL-H Hackerspace、ToorCamp 等本地黑客社区生态为地理位置特定条件（jf-deepself-09、jf-tl-017）。
- 不可直接迁移：逐年新训练课程的可持续性部分依赖其早期进入硬件安全训练赛道的先发位置与口碑建立的客户基础（jf-deepself-03、jf-r1-001），存在幸存者偏差。

## 复核问题


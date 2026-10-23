# Eduardo Vela Nava：漏洞研究成长分析

- 擅长领域：浏览器与平台漏洞
- 独立复核：pass · 90/100

## 成长阶段

- **2007–2009 · 公开写作起点与注入类攻击技术初成**：以 sirdarckcat.blogspot.com 为公开载体，从 JavaScript 与 Web 安全主题切入；在 PHP-IDS 公开测试前自行预先测试并在约一小时内发现三个绕过向量、构建 666 字节 PoC，依赖与 Mario Heiderich 等维护者的快速反馈迭代；研究对象从单点 XSS 向量扩展到 NoScript、XSS 过滤器等客户端防护机制。同期自建被其称为首个可用 CSP 实现/原型的 ACS 项目，并与 Gareth Heyes、David Lindsay 在 Microsoft BlueHat 合讲 CSS 信息外泄主题，建立从样式侧信道到脚本注入的研究连续性。（置信度：high）
  - 证据：evn-tl-01, evn-tl-02, evn-tl-03, evn-tl-04, evn-self-01, evn-works-11, evn-001
- **2016-12 至 2017-01 上旬 · CSP 态度逆转与研究方向重置**：2009 年前后对 CSP 高度认可并自建 ACS 原型，至 2016-12 转为系统怀疑。2016-12-27 帖正文自述从认可到怀疑的态度变化，并在圣诞节点引入 Sebastian Lekies 的 DOM XSS 对 CSP nonce 的绕过研究，称之为对 CSP nonces 的 significant blow；该叙事构成态度转变的外部对照，但作者未以显式因果句将 Lekies 演示表述为态度转变原因。这一态度变化是后续提出缓解评估框架与 Isolated Scripts 替代方案的直接动因，而非孤立判断。（置信度：medium）
  - 证据：evn-001, evn-self-05, rev1-01
- **2017-01-23 至 2017-02-11 · 评估框架、替代方案与披露经济学并行产出**：同一短窗口内并行产出三类内容：提出衡量 Web 安全缓解措施的 Moderation/Minimization/Substitution/Simplification 四维框架及 Impact、Difficulty 高层指标；发布 Isolated Scripts XSS 缓解提案并附 Chrome 扩展原型与含故意 XSS 漏洞的演示站点，邀请研究者绕过；公开 jQuery Mobile 0day XSS 时声明雇主 Google 身份并切割个人/雇主立场；围绕披露与奖励经济学进行反思。研究链条从单纯发现扩展到评估、防御实现与披露流程。（置信度：high）
  - 证据：evn-002, evn-003, evn-self-02, evn-comm-05, evn-comm-04, evn-comm-03, rev1-03, rev1-04
- **2019 · XS-Leaks 与多人协作知识库迁移**：研究重心从 XSS 缓解迁移到跨站信息泄露，以 HTTP 缓存状态推断区别于以往依赖时序的攻击；将 XSLeaks wiki 明确描述为 terjanq、lbherrera_、ronmasas、_tsuro、arthursaftnes、kkotowicz 与本人的联合项目，把个人研究纳入多人协作维护的知识库；研究产出由个人博客独立 writeup 转向具名协作的长期项目，社区资产后由新一代维护者接续。（置信度：high）
  - 证据：evn-004, evn-comm-01, evn-self-03, evn-tl-09, evn-ext-xsleaks-editor, evn-comm-08, rev1-02

## 主要成长机制

### 公开发表—反馈征求的重复循环

起点：2007 年中起以个人博客 sirdarckcat.blogspot.com 为公开写作载体，早期高密度写作（2007 年 17 篇），主题为 JavaScript 与 Web 安全；具备公开复盘与邀请外部反馈的发布条件。

练习与反馈：2007–2019 年持续公开发表 writeup，并在帖末固定以征求 Twitter 反馈的形式收尾（四篇抽样博文 2016-12-27、2017-01-23、2017-02-08、2019-03-19 均以 Twitter 反馈征求结尾，其中仅 2019-03-19 帖含 DMs are open 措辞，原固定 DMs are open 的表述不成立）；在 PHP-IDS 公开测试启动前即自行预先测试并通知维护者 Mario Heiderich，对方数分钟内修补后对作者进行访谈。；据 2016-12-27 帖正文一手核对，作者自述 2016 年秋对 CSP nonce 抱乐观态度，并在圣诞节点引入 Sebastian Lekies 的 DOM XSS 对 nonce 的绕过研究，称之为对 CSP nonces 的 significant blow；该叙事构成态度转变的外部对照，但作者未以显式因果句将 Lekies 演示表述为态度转变原因，仅作 medium confidence 因果，态度转变事实本身由 evn-001（2016-12-27 帖正文）支撑。Isolated Scripts 提案中 Devdatta 提出 cookie 前缀、Malte 提出开发者体验顾虑、Mario 指出钓鱼残留等同行反馈直接塑造了方案设计。

能力与结果：形成公开复盘—同行反馈—方案修订的迭代习惯，能将外部绕过反馈转化为对自建缓解机制的再评估与新方向探索。；2016-12 由 CSP 认可转向系统怀疑并探索替代方案；2017-01-25 发布 Isolated Scripts 原型并以公开绕过挑战征集反馈；2019-03-19 在 XSLeaks 协作项目帖中以 Contact me on twitter if you want to contribute 形式持续征求贡献

置信度：medium；替代解释：固定以 Twitter 反馈征求结尾可能是 Blogger 时代个人博客的普遍收尾惯例，而非其特有；区分度主要来自其将外部绕过反馈系统转化为方法重置（CSP 怀疑→框架→Isolated Scripts）的连续产出，而非收尾措辞本身。

证据：evn-tl-01, evn-tl-02, evn-works-10, evn-001, evn-self-05, evn-self-02, evn-comm-05, evn-004, rev1-01, rev1-02, rev1-03, rev1-04

### 攻击—防御—评估的方法论闭环

起点：早期以攻击侧切入（CSS 信息外泄、XSS 过滤器绕过、NoScript 绕过），并自建 ACS CSP 原型具备防御实现经验。

练习与反馈：先以攻击反推防御有效性（CSP nonce 绕过、jQuery Mobile XSS），再为缓解类别建立可比较的评估语言（四维框架），继而提出并实现替代缓解方案原型（Isolated Scripts），最后用自建评估框架对自身提案做结构化审视。；自建评估框架回灌为对自身提案的审视工具；Sebastian Lekies 的 nonce 绕过研究作为外部对照触发对既有缓解有效性的再评估；jQuery 团队拒绝修补的分歧被转化为可协作的公开记录与读者 PR 入口。

能力与结果：将单一漏洞发现抽象为缓解机制有效性的可度量评估，再具化为可运行替代方案原型，形成发现—评估—构建的闭环方法论。；2017-01-23 提出 Moderation/Minimization/Substitution/Simplification 四维评估框架；2017-01-25 发布 Isolated Scripts 缓解方案及可安装 Chrome 扩展原型与故意漏洞演示站点；2016-12-27 将 CSP nonce 绕过研究系统化覆盖持久 DOM XSS、postMessage、HTTP 包含与 location.hash 等场景

置信度：high；替代解释：该闭环也可能由 2009–2016 年间 CSP 标准化进程本身的需求驱动（既有缓解脆弱→需要新框架），即外部技术演进提供了方法论抽象的契机，而非纯个人方法论演进。

证据：evn-001, evn-002, evn-003, evn-self-02, evn-comm-05, evn-comm-04

### 同伴协作网络与社区知识库共建

起点：早期即与 Gareth Heyes、David Lindsay、Mario Heiderich、WHK（elhacker.net）等形成同伴协作关系，参与 elhacker-net 等社区组织。

练习与反馈：在单一 writeup 中密集交织多方前驱工作与同行贡献（致谢 WHK 发现 JSONP 绕过、Sebastian Lekies 的 CSP 绕过、Mario Heiderich 的 CSP 挑战、Devdatta 的运行时 CSP 锁定、CSP Is Dead 论文等）；将个人研究沉淀为多人维护的 XSLeaks wiki，列出 terjanq、lbherrera_、ronmasas、_tsuro、arthursaftnes、kkotowicz 与本人为共同贡献者；以 google/security-research、tamperchrome、kctf、google-ctf 等公共仓库把工具与基础设施回流社区。；同行反馈直接塑造方案设计（Devdatta 提出 cookie 前缀、Malte 提出开发者体验顾虑、Mario 指出钓鱼残留）；XSLeaks wiki 由新一代维护者（terjanq 等）接续维护，社区资产具有传承结构。

能力与结果：建立并维护跨社区的协作网络与共享知识库，把个人发现转化为可复用、可接续的社区资产。；2019-03-19 将 XSLeaks wiki 描述为多名研究者联合项目并贡献 HTTP Cache Cross-Site Leaks 技术；xsleaks.dev contributions 页将其列为 predecessor wiki 贡献者，当前 wiki 由 terjanq 等接续维护；GitHub 资料页显示其为 google、xsleaks、AppSecVillage、CTF-Organizers、elhacker-net 组织成员，并 pinned 多个社区基础设施仓库

置信度：high；替代解释：其所在 Google 组织身份与 browser-security 社区的高协作密度可能提供了普通独立研究者难以获得的协作入口与平台资源，部分协作广度或由组织平台条件而非纯个人网络建设支撑。

证据：evn-self-01, evn-self-03, evn-comm-01, evn-comm-05, evn-comm-06, evn-comm-07, evn-comm-08, evn-works-09, evn-ext-xsleaks-editor

## 可迁移与不可迁移

- 可迁移：以攻击反推防御有效性，再为缓解类别建立可比较的评估维度（如 Moderation/Minimization/Substitution/Simplification），最后提出并实现替代方案原型，形成发现—评估—构建的闭环。
- 可迁移：在公开测试或新 API 发布前自行预先测试，并依赖与维护者的快速反馈迭代修复。
- 可迁移：在 writeup 中显式标注前驱研究与同行贡献，把单点发现纳入可接续维护的共享知识库而非个人档案。
- 可迁移：公开披露第三方 0day 时主动声明雇主身份并区分个人与机构立场，处理披露伦理与利益冲突。
- 可迁移：将与维护者的技术分歧保留为可复核材料并开放外部贡献入口，而非止步于拒绝。
- 可迁移：以可安装原型 + 含故意漏洞的演示站点 + 公开绕过挑战的形式征集反馈。
- 不可直接迁移：Google 组织成员身份及 employer=elgooG 现时状态，提供普通独立研究者难以获得的协作入口、平台资源与披露语境；入职时间无一手来源。
- 不可直接迁移：所在 browser-security 社区（terjanq、Mario Heiderich、mikewest、Sebastian Lekies、Devdatta、Gareth Heyes、David Lindsay 等）的高协作密度，部分协作广度或由该社区结构而非纯个人网络建设支撑。
- 不可直接迁移：XSLeaks wiki 与 google/security-research、tamperchrome、kctf、google-ctf 等公共仓库的维护权，依托于其 Google 组织身份与既有社区地位，非可简单迁移的个人条件。
- 不可直接迁移：2007 年起即以 Blogger 公开写作并接入 elhacker-net 等西语安全社区的历史路径，与后续研究主题形成特定连续性，属于时点条件而非可复刻方法。
- 不可直接迁移：GitHub 资料页 location 为 Zürich、2009 年博文自述曾居住中国，地点迁移阶段的具体时间线无公开一手来源，不可据以推断能力形成路径。

## 复核问题

- stages[0].capability_change：对引自 evn-001（2016-12-27 帖正文）的 2009 年 CSP 态度与 ACS 原型内容，补充回溯属性标注，例如将 '2009 年前后对 CSP 高度认可并自建 ACS 原型' 调整为 '据 2016-12-27 帖回溯自述，2009 年前后对 CSP 高度认可并自建 ACS 原型'，以区分回溯自述与 2007–2009 同期记录。该项为轻微时间错位修正，不改变阶段结论。
- mechanisms[1].feedback：将 'Sebastian Lekies 的 nonce 绕过研究作为外部对照触发对既有缓解有效性的再评估' 中 '触发' 一词的因果强度与 mechanisms[0].feedback 已降级的 medium confidence 叙事性对照表述对齐，例如改为 '作为外部对照，与对既有缓解有效性的再评估在时间上并列，作者未以显式因果句将其表述为再评估的原因'，以消除两机制间因果表述强度的内部不一致。该项为内部一致性修正，不改变机制结论。

# Bocheng Xiang：漏洞研究成长分析

- 擅长领域：Windows 逻辑漏洞与 LPE
- 独立复核：pass · 90/100

## 成长阶段

- **2025-06 至 2025-08 · 方法构建：从历史链接跟随漏洞复现到两阶段原型工具 LinkZard 的实现与发表**：在同一 USENIX Security 2025 论文项目内完成：起草定稿期（论文 PDF 创建 2025-06-11、最后修改 2025-07-20）对 42 个历史链接跟随漏洞进行复现与归纳，构建两阶段原型工具 LinkZard（探索阶段采用 file state fuzzing，利用阶段定位 sink 并以 code wrapping 实现自动利用），对 Microsoft、Apple、Intel 等 120 个商业程序进行测试，发现 55 个零日漏洞；会议发表期（2025-08）以长报告在 USENIX Security 25 发表，截至发表 49 个零日获厂商确认与修复、15 个取得 CVE 编号并获厂商赏金。需显式标注：上述探索与利用两阶段为单一 2025 论文项目的起草定稿期与会议发表期两个执行时期，不构成跨期成长阶段；本阶段受单事件限制，跨时期成长路径在本节点无一手来源支撑。（置信度：medium）
  - 证据：works-01-linkzard-usenixsec25, works-02-linkzard-results, works-04-affiliation-fudan, bocheng-timeline-usenixsec25, bocheng-timeline-paper-pdf-metadata, ext-usec25-venue-accept

## 主要成长机制

### 复现式经验研究：对历史链接跟随漏洞逐项复现并归纳触发条件

起点：具备 Windows 文件操作类逻辑漏洞的研究方向与学术团队协作环境（复旦大学系统软件与安全实验室，合著含资深成员 Min Yang）；可访问已公开的 42 个历史链接跟随漏洞作为经验研究样本。

练习与反馈：据论文摘要记述（单次已观察事实，非跨时期重复习惯），对 42 个已知链接跟随漏洞进行复现，归纳其触发条件与失败模式，作为后续工具设计与新漏洞挖掘的输入；论文摘要将该复现归纳表述为 LinkZard 的方法论基础。；反馈来源为论文撰写与同行评议流程本身（USENIX Security 25 程序委员会接收为长报告），以及厂商对所发现零日的确认、修复与 CVE/bounty 分配；上述反馈由作者团队在摘要自报，本节点未取得独立第三方厂商公告或 CVE 数据库交叉核验。

能力与结果：形成对链接跟随漏洞触发条件的结构化认识，可用于指导自动化检测工具的输入空间设计与利用阶段的 sink 选取。；LinkZard 两阶段工具的设计输入（42 复现归纳作为方法论基础，见 works-01 与 ext-usec25-impact-numbers）；在 120 个商业程序上发现 55 个零日，截至发表 49 个获确认修复（works-02、ext-usec25-impact-numbers）

置信度：low；替代解释：verified_in_run=true 仅表明 USENIX 会议页面抓取成功，不构成对跨时期重复练习习惯或稳定个人方法论的证实；论文对 42 个历史漏洞的复现与归纳为单次记述。42 个样本的选择标准、复现失败的案例与放弃路径未在论文摘要与可抓取材料中披露，存在结果驱动叙事的选择性。竞争性解释：复现归纳可能受团队（含资深成员 Min Yang）既有研究积累与既有 LFVuln 数据集驱动，而非个人反复练习习惯；本节点无法区分个人贡献与团队贡献。

证据：works-01-linkzard-usenixsec25, works-02-linkzard-results, ext-usec25-impact-numbers, bocheng-timeline-usenixsec25

### 两阶段工具化：检测（file state fuzzing）与利用（sink 定位 + code wrapping）分离

起点：具备对链接跟随漏洞触发条件的归纳基础，以及构建自动化工具的工程能力与团队协作条件；论文摘要将其表述为探索与利用两个阶段。

练习与反馈：据论文摘要记述（单次已观察事实），将漏洞研究拆分为可独立验证的两个工程阶段：探索阶段采用 file state fuzzing 进行检测，利用阶段定位 sink 并以 code wrapping 策略实现自动利用；该两阶段划分在 USENIX Security 25 论文与演讲页中作一致表述。；反馈来源为工具在 120 个商业程序上的规模化测试结果（55 个零日）与厂商响应（49 确认修复、15 CVE、bounty），均为作者团队自报；论文 PDF 正文为压缩流未取得，工具内部实现细节、迭代版本与开发时间线无一手来源。

能力与结果：形成可同时处理检测与利用两类任务的自动化工具原型，使漏洞发现与利用生成不再依赖单点手工分析。；LinkZard 原型工具（两阶段表述见 works-01、bocheng-timeline-usenixsec25）；规模化零日发现（55 个零日、15 个 CVE、bounty，见 works-02、ext-usec25-impact-numbers）

置信度：medium；替代解释：两阶段划分由论文摘要自述，PDF 正文未取得，工具内部实现细节与迭代历史无一手来源；LinkZard 是否开源、代码仓库与开发时间线未由可抓取来源证实（GitHub 搜索 LinkZard 返回 0 个公开仓库）。竞争性解释：两阶段工具化可能为论文叙述层面的方法论呈现，而非可独立复验的工程能力标志；亦可能依托团队既有的 fuzzing 与漏洞分析框架，个人贡献与团队贡献在本节点不可分离。

证据：works-01-linkzard-usenixsec25, works-02-linkzard-results, bocheng-timeline-usenixsec25, ext-usec25-venue-accept

### 顶会发表与外部反馈（条件限定：仅 USENIX Security 2025 经一手核验）

起点：具备可投顶会的完整研究成果（实证复现 + 工具构建 + 规模化零日发现 + CVE/bounty 闭环）；处于学术团队结构内，有合著与指导协作条件。

练习与反馈：据已核验来源记述（单次已观察事实），以第一作者身份在 USENIX Security 2025 以长报告形式发表研究，并同步公开论文 PDF 与演讲幻灯片；将研究产出提交至厂商漏洞响应流程，以厂商确认修复、CVE 分配与 bounty 作为外部反馈。条件限定：仅 USENIX Security 2025 经一手核验；person_json 种子记录所列 OffByOne 2026、Black Hat US/EU、POC 三处会议演讲未取得一手议程页面，跨会议重复发表与反馈模式在本节点无法证实。；反馈来源为 USENIX Security 25 程序委员会的接收（长报告）、厂商对零日的确认修复与 CVE/bounty 分配；上述外部反馈中，会议接收为程序性事实，厂商反馈由作者团队在摘要自报，本节点未取得独立第三方核验。

能力与结果：形成将研究产出经顶会同行评议与厂商响应流程获得外部确认的路径，使研究成果不止停留在学术评测。；USENIX Security 25 长报告接收与发表（ext-usec25-venue-accept、bocheng-deepself-01）；公开论文 PDF 与演讲幻灯片（bc-community-03）；49 个零日获确认修复、15 个 CVE 与厂商赏金（bc-community-01、ext-usec25-impact-numbers）

置信度：low；替代解释：顶会发表与外部反馈回路仅以 USENIX Security 2025 单一会议为已核验来源；OffByOne 2026、Black Hat US/EU、POC 三处会议演讲未取得一手议程页面（POC 2025 页面 HTTP 403、Black Hat US-25 议程 HTTP 404、Black Hat Asia-26 议程 HTTP 403、OffByOne 站点 ECONNREFUSED），DBLP 学术索引受 Anubis bot-protection 拦截无法交叉核验发表列表，跨会议重复发表与反馈模式无法证实。竞争性解释：外部反馈（49 修复/15 CVE/bounty）由作者团队在摘要自报，未见独立第三方厂商公告或 CVE 数据库对本节点可核验；顶会接收为程序委员会外部程序性结果，不等于对个人能力的独立评价，亦不可作为个人可迁移资产。

证据：bc-community-01, bc-community-02, bc-community-03, ext-usec25-venue-accept, ext-usec25-impact-numbers, bocheng-deepself-01

## 可迁移与不可迁移

- 可迁移：复现式经验研究（条件限定为单次记述）：对已知历史漏洞逐项复现并归纳触发条件与失败模式，作为后续工具设计与新漏洞挖掘的输入；本节点将其表述为论文记录的一次性实践，而非已证实的跨时期个人习惯。
- 可迁移：两阶段工具化：将检测与利用分离为可独立验证的工程阶段（file state fuzzing 检测、sink 定位与 code wrapping 利用），使漏洞发现与利用生成可规模化。
- 可迁移：公开发表输出习惯：在顶会发表后同步公开论文 PDF 与演讲幻灯片，使研究方法可被社区检视与复用（基于 bc-community-03）。
- 不可直接迁移：顶会程序性接收：USENIX Security 25 长报告接收为会议程序委员会的外部程序性结果，不可作为个人可迁移资产。
- 不可直接迁移：工件评估程序性结果：artifact evaluation available 为 USENIX 工件评估流程的外部程序性结果（works-03 未核验，仅作程序性结果层面标注，不作能力证据）。
- 不可直接迁移：复旦团队结构：6 位作者均署名 Fudan University，含资深成员 Min Yang，方法与反馈回路依托团队协作，不可直接归因或迁移至个人。
- 不可直接迁移：厂商响应闭环：49 个零日确认修复、15 个 CVE 与厂商赏金依托 Microsoft、Apple、Intel 等厂商的漏洞响应流程，为外部条件而非个人能力。
- 不可直接迁移：单事件限制：全部 verified 证据集中于 2025 单一 USENIX 论文项目（起草定稿期 2025-06 至 07、发表期 2025-08），不构成跨期成长阶段。

## 复核问题


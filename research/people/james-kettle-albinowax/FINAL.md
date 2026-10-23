# James Kettle (albinowax)：漏洞研究成长分析

- 擅长领域：HTTP 与 Web 漏洞
- 独立复核：pass · 90/100

## 成长阶段

- **大学阶段至 2015 年前 · 入行转向**：由对电子竞技游戏 Counter-Strike 失去兴趣而转向黑客技术，并以一笔漏洞赏金收入购置研究用计算机；此阶段尚未形成可识别的方法论，仅完成兴趣与资源的初步转移。具体校名、专业与年份在 first-party 资料中未给出，该转向仅由 PortSwigger 官方资料页转述。（置信度：low）
  - 证据：jkt-tl-university, james-kettle-convo-01, jk-dec-entry-bored-of-counterstrike
- **2015–2016 · 组织研究角色确立与首次方法论转向**：2015 年加入 PortSwigger 并主导其研究线，发表 server-side template injection 原创研究；2016 年发表 Backslash Powered Scanning，放弃以技术专属 payload 列表逐项匹配已知漏洞的范式，改为发送通用探针并比对响应属性（状态码、行数、词数、HTML 结构、反射计数），将输入分为 boring/interesting/promising 三类后迭代调查，明确建模为对资深手工测试者思路的模仿；同期完成 ActiveScan++、HTTP Request Smuggler、Backslash Powered Scanner 等 Burp 扩展。文中记录 2013 年曾尝试基于最长公共子序列生成正则做响应比对，因 O(n²) 复杂度与自我拒绝服务问题被放弃，体现显式的试错与淘汰。（置信度：high）
  - 证据：ext-identity-01, albinowax-works-001, jk-dec-2016-backslash-behaviour-scanning, jkt-tl-2016, jkt-tl-ext-2016, james-kettle-convo-03
- **2017–2018 · 被忽视攻击面选取与既有管线复用**：2017 年选取反向代理、负载均衡与后端分析系统构成的几乎不可见的攻击面，因其设计为不可见、无法依赖响应内容审计，改为发送令目标主动回连的载荷，借助 Burp Collaborator 记录回调，并以 ZMap/ZGrab 对约 5 万台服务器规模化扫描，固化为 Collaborator Everywhere 扩展；2018 年 Practical Web Cache Poisoning 明确复用 Cracking the Lens 建立的研究管线，将识别 unkeyed input 这一手工步骤工具化为 Param Miner，并下载 GitHub 前 2 万个 PHP 项目提取 header 名称以扩充字典，发现 X-Original-URL、X-Rewrite-URL 等跨框架 header；另以 hackxor.net 悬赏众筹难题解法。（置信度：high）
  - 证据：jk-dec-2017-cracking-the-lens-hidden-surface, jk-dec-2018-cache-poisoning-pipeline-reuse, jkt-tl-2018
- **2019–2021 · 协议级系统化与底层基础设施自建**：2019 年复活 Watchfire 于 2005 年文档化但因难度与附带损害被长期搁置的 HTTP Request Smuggling，重构为 Detect/Confirm/Explore/Exploit/Store/Attack 的方法论（图标签合并末段为 Store/Attack），区分 CL.TE 与 TE.CL，以超时探测降低误报与对他人影响，发布 HTTP Request Smuggler 并将检测并入 Burp 核心扫描器；2020 年 Web Cache Entanglement 在 2018 缓存投毒基础上深化；2021 年因 HTTP/2 二进制成帧消解旧走私条件，从零编写 HTTP/2 客户端集成进 Turbo Intruder，定义 H2.CL、H2.TE、H2.X，并复用 2019 年超时检测的改造版本扫描 bug bounty 管线。（置信度：high）
  - 证据：albinowax-works-002, albinowax-works-003, jk-dec-2019-revive-forgotten-smuggling, jk-dec-2021-http2-from-scratch-and-reapply, jkt-tl-2020, jkt-tl-2021, r1-ev-001, r1-ev-002, JK-COM-01, JK-COM-02, JK-COM-03
- **2022–2023 · 客户端前移与跨域原语借用**：2022 年因 amazon.com 上一次偶然发现的 CL.0 desync（规范化请求竟被浏览器 fetch() 直接触发）而主动系统化扫描，将走私点前移至受害者浏览器与前端之间，定义 client-side desync (CSD)，涵盖 CL.0/H2.0、pause-based desync、MITM-powered desync；2023 年由 2016 年 Josip Franjković 报告的 Facebook 竞态这一七年悬案驱动，放弃请求原子与 GET 不改状态两个假设，借鉴 2020 USENIX Timeless Timing Attacks 的单包思路结合 Nagle 算法自创 single-packet attack，将中位时延抖动从约 4ms 降至约 1ms。（置信度：high）
  - 证据：albinowax-works-004, albinowax-works-005, jk-dec-2022-accident-driven-scope-expansion, jk-dec-2023-drop-atomicity-single-packet, jkt-tl-2022, jkt-tl-2023

## 主要成长机制

### 差分与异常驱动的检测范式

起点：2013 年曾尝试基于最长公共子序列生成正则做响应比对，因 O(n²) 复杂度与自我拒绝服务问题被放弃；该次失败由 2016 年 writeup 转述，无独立公开链接可核验。

练习与反馈：2016 年改为基于响应属性（状态码、行数、词数、HTML 结构、反射计数）的差分；2019 年将差分迁移到超时差分以探测协议解析分歧；2022 年以行为差异识别客户端反同步；2023 年将识别异常自述为发现竞态最重要的技能。；响应或时延差异揭示有趣行为，再以 bug bounty 真实目标（New Relic、Trello、Red Hat、PayPal、Netflix、Atlassian、Verizon、Amazon 等）的赏金与厂商补丁校准检测有效性。

能力与结果：把资深手工测试者对异常响应的直觉转化为可重复、可分类（boring/interesting/promising）的检测信号，进而可自动化。；Backslash Powered Scanner；HTTP Request Smuggler 的超时检测；Browser-Powered Desync 的 CSD 与 connection-state probe 检测；single-packet attack 触发的竞态检测

置信度：high；替代解释：差分可能是在事后写作时对各次独立研究的统合叙事，而非当时即被自觉执行的方法；2013 年失败到 2016 年成形之间的学习路径无公开一手记录，不能排除该范式是事后归纳。

证据：albinowax-works-001, albinowax-works-002, albinowax-works-004, albinowax-works-005, jk-dec-2016-backslash-behaviour-scanning, jk-dec-2023-drop-atomicity-single-packet

### 研究即工具与社区反馈回路

起点：2015 年加入 PortSwigger 并主导研究线，处于 Burp Suite 扩展生态与商业扫描器产品线内部，具备工具集成与分发的组织条件。

练习与反馈：每篇 writeup 配套工具升级——Turbo Intruder（2021 自写 HTTP/2 栈、2022 pause 参数、2023 single-packet）、HTTP Request Smuggler（2019 创建、2021 H2 检测、2022 CSD 检测）、Param Miner（2021）、Backslash Powered Scanner（2016）；多项检测能力并入 Burp 核心扫描器，并以 Web Security Academy 免费 lab 复现。；社区研究者使用其技术发现新漏洞形成回授；GitHub 仓库 PortSwigger/http-request-smuggler 显示 1.2k stars、128 forks、11 open issues、2 PRs、359 commits；bug bounty 赏金多笔捐出。

能力与结果：使研究产出沉淀为可复用基础设施，反过来支撑下一轮更难目标。；三个最流行 Burp 扩展（ActiveScan++、HTTP Request Smuggler、Backslash Powered Scanner）；年度工具升级与研究方向对齐；Burp Scanner 集成使方法论被规模化采用

置信度：high；替代解释：该回路可能主要由 PortSwigger 的商业模型（Burp 生态需持续集成新检测）结构性要求驱动，而非个人选择；多数从业者缺乏全职带薪研究岗位与产品线，难以复现此回路，属组织资源条件而非可迁移个人习惯。

证据：albinowax-works-006, JK-COM-01, JK-COM-03, ext-tools-01, ext-role-01, jkt-tl-ext-2016

### 被忽视面选取与既有管线复用

起点：2017 年识别出反向代理、负载均衡与后端分析系统构成的几乎不可见的攻击面长期被忽视。

练习与反馈：2017 年以主动回连载荷加 Burp Collaborator 加 ZMap/ZGrab 约 5 万台服务器规模化扫描，固化为 Collaborator Everywhere；2018 年复用该管线做 Web Cache Poisoning，并将识别 unkeyed input 工具化为 Param Miner；2019 年复活 2005 年 Watchfire 文档化后被搁置的 request smuggling；2022 年由 amazon.com 偶然 CL.0 发现转向主动系统化扫描。；被忽视面竞争门槛低、单次产出高；bug bounty 真实目标与厂商补丁确认有效。

能力与结果：以选低竞争面加复用既有工具链替代逐次从零选题，形成可迁移的选题与建管线习惯。；Collaborator Everywhere；Param Miner；HTTP Request Smuggler；CSD 检测

置信度：high；替代解释：选被忽视面是安全研究的常见启发式，并非 Kettle 独有；该模式也可能是由各自独立的机会性发现事后归纳而成，而非事先自觉执行的选题策略。

证据：jk-dec-2017-cracking-the-lens-hidden-surface, jk-dec-2018-cache-poisoning-pipeline-reuse, jk-dec-2019-revive-forgotten-smuggling, jk-dec-2022-accident-driven-scope-expansion, r1-ev-002

### 新协议/新假设边界下自建原语与跨域借用

起点：2021 年 HTTP/2 二进制成帧消解了 HTTP/1.1 走私的旧失效条件；2023 年竞态研究受困于网络抖动掩盖 sub-state。

练习与反馈：2021 年从零编写 HTTP/2 客户端以触达协议降级边界；2023 年放弃请求原子与 GET 不改状态假设，借鉴 2020 USENIX Timeless Timing Attacks 的单包思路结合 Nagle 算法自创 single-packet attack。；既有工具无法触达新边界时即自建原语补盲；single-packet attack 将中位时延抖动从约 4ms 降至约 1ms，此前被掩盖的 sub-state 可被可靠触发。

能力与结果：当领域默认假设失效时，以自建或借用跨域原语触达新的可利用边界。；H2.CL/H2.TE/H2.X 检测；single-packet race condition

置信度：medium；替代解释：两次实例可能是对两个不相关协议问题的独立反应，而非被自觉执行的方法；样本仅两次，自建原语与跨域借用是否构成稳定习惯尚需更多实例。

证据：albinowax-works-003, albinowax-works-005, jk-dec-2021-http2-from-scratch-and-reapply, jk-dec-2023-drop-atomicity-single-packet

## 可迁移与不可迁移

- 可迁移：以响应/时延差分替代已知签名匹配，将有趣行为作为检测目标。
- 可迁移：选取被忽视或被遗忘的攻击面与研究以降低竞争门槛。
- 可迁移：复用既有研究管线与工具链进入新方向，而非每次从零选题。
- 可迁移：当既有工具无法触达新边界时，自建底层原语（如自写协议客户端）补盲。
- 可迁移：将关键手工步骤工具化为可复用扩展，使方法可传播、可迭代。
- 可迁移：显式记录失败路径与被放弃方向（如 LCS-regex、七年悬案），保留试错与淘汰过程。
- 可迁移：借用跨域学术成果（如 USENIX Timeless Timing Attacks）迁移到新问题。
- 可迁移：以数据规模（GitHub 大规模爬取）与外部协作（hackxor 悬赏）替代纯个人灵感。
- 不可直接迁移：PortSwigger Director of Research 全职带薪研究岗位与 Burp Suite 产品线，使研究、工具集成、社区采用的闭环在组织层面被结构性支持。
- 不可直接迁移：bug bounty 管线（New Relic、Trello、Red Hat、PayPal、Netflix、Atlassian、Verizon、Amazon 等真实目标）作为反馈与资金来源。
- 不可直接迁移：早期以比特币计价赏金购置研究用计算机的时期特定条件。
- 不可直接迁移：Black Hat USA、DEF CON、Nullcon 作为固定公开发表渠道。
- 不可直接迁移：Web Security Academy 免费 lab 等 PortSwigger 自有传播资源。

## 复核问题

- stages[4]（2022–2023，客户端前移与跨域原语借用）confidence 标为 high，而同阶段内容支撑的 mechanism D（新协议/新假设边界下自建原语与跨域借用）confidence 标为 medium、validation_tests 无 distinctive；建议在 tensions 显式标注该阶段级与机制级 confidence 不一致，说明 stage high confidence 主要由 CSD（2022）与 single-packet（2023）两条 writeup 支撑的'客户端前移'主线，而'自建原语与跨域借用'作为横跨 2021/2023 两实例的抽象机制因样本量标 medium，避免读者将 stage confidence 直接套用到 mechanism D 的可推广性。
- mechanism B（研究即工具与社区反馈回路）alternative_explanation 已提及 PortSwigger 商业模型结构性驱动，但未进一步区分'个人选择研究-工具闭环'与'组织岗位要求 Burp Scanner 持续集成新检测'两条因果路径的可观测区分边界；建议在 alternative_explanation 或 non_transferable_conditions 补一句明确：该回路在'工具集成进 Burp 核心扫描器'这一环上受组织岗位约束，而'每篇 writeup 配套开源扩展与免费 lab'这一环可由个人选择复现，据此细化可迁移边界。
- open_questions 中'入行细节（校名、专业、年份）在 first-party 资料中未给出；第三方摘要称 University of Bristol 哲学专业但未在 first-party 抓取页确认'已标注缺口；建议在 stages[0] capability_change 中对'比特币计价赏金购置计算机'一并明确该细节为 PortSwigger 官方 profile 单源转述、无第三方佐证，与 open_questions 的入行缺口表述保持口径一致，避免在 stage 叙述中呈现为已确立事实。

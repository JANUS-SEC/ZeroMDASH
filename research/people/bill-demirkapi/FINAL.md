# Bill Demirkapi：漏洞研究成长分析

- 擅长领域：Windows/UEFI/供应链漏洞
- 独立复核：pass · 76/100

## 成长阶段

- **2015–2018 · 竞赛参与期，由使用工具转向审视工具**：通过参加 CyberPatriot VIII 至 X（2015–2018 赛季）获取数年结构化逆向与系统加固练习；2019 年复盘该赛事评分引擎 CCSClient.exe 时自述参赛期间逆向能力不足，而以当前能力重做，并以 IDA Pro 定位内嵌 Crypto++ 5.6.2 与 AES-GCM 硬编码密钥，识别 InitializeScoringData、DecryptData、ExecuteCheck 等函数，完成从参与者到审视者的视角转变。该阶段身份为 17 岁高中在校生，作为 evidence 记录而非阶段核心标签。（置信度：high）
  - 证据：bd-works-02-cyberpatriot, bill-timeline-cyberpatriot-2015-2018, bill-timeline-college-admissions-2019
- **2019 · 公开披露与失败转向实践的建立期**：自 2019-02-14 发布 Reading Physical Memory using Carbon Black's Endpoint driver 起密集公开发表，全年 8 篇。Dell SupportAssist 研究中以 URL 前导空格绕过 StartsWith 校验构造完整利用链，并首次建立逐日披露时间线（2018-10-26 首报至 2019-04-18 公开）。CyberPatriot 评分引擎研究发布后收到竞赛主要开发者邮件要求下架，作者选择延迟而非永久删除，形成对披露时机的双向反馈。WPI/TargetX 招生门户研究中自述为 17-year-old high school senior，并在厂商长期沉默后以 CC 上级与设定发布期限施加压力。（置信度：high）
  - 证据：bd-works-01-dell-rce, bd-works-02-cyberpatriot, bd-works-06-blog-bibliography, bill-community-01, bill-community-02, bill-timeline-dell-rce-disclosure-2018-2019, bill-timeline-college-admissions-2019, bd-r2-01-startswith-primary
- **2020 · OEM 攻击面跨厂商复用与内核态转向**：将 OEM 预装软件攻击面方法论从 Dell 迁移到 HP，2020-04-03 发布含 5 个本地提权、2 个任意文件删除、3 个远程代码执行变体的 HP Support Assistant 研究，工具栈从 .NET 逆向扩展到 de4dot 解混淆、WCF 命名管道函数枚举、URLProtocolView 与 Procmon。对 HP 声称已修复的补丁独立复测后发现未修补并提交补充报告。2020-05-18 将研究对象由用户态 .NET 扩展到内核态驱动 tmcomm.sys，映射多级 IOCTL 分发表，产出任意内核函数调用、任意内核读写与卸载例程滥用三类原语。致谢 mentor Alex Ionescu 在内核内存分配技术上给予方向指引，引用 j00ru 2010 年 Reserve Objects 文章作为方法学来源。（置信度：high）
  - 证据：bd-works-03-hp-bloatware, demirkapi-ext-002, bill-decisions-02, bill-decisions-03, bill-timeline-hp-psirt-2019-2020, bill-timeline-trend-micro-mentor-2020, bill-community-03, bill-community-04
- **2021–2023 · 方法论转型与 Windows 利用深化期**：据作者自述自 2021 年起以漏洞类（bug class）驱动而非具体厂商目标驱动，受 Matt Bryant 2015 年博客 Fishing the AWS IP Pool for Dangling Domains 启发，开始构建 CloudRot 枚举 AWS 与 GCP 公网 IP。本地样本扫描发现 impractical 后转向 serverless 架构。2022-02-14 发布 Exception Oriented Programming Part 1，同步发布 GitHub 仓库 ExceptionOrientedProgramming 提供 PoC，形成研究、工具实现与公开发表配套的产出流程。Exception Oriented Programming Part 2 于 2023-01-30 发布，作者自述 Microsoft 在 Part 1 发布后录用其入职，时序与自我归因均来自作者本人。（置信度：medium）
  - 证据：bd-works-05-bigdata-cloud, bill-decisions-04, bill-decisions-05, bill-timeline-eop-part1-2022, bill-timeline-microsoft-hire-2023, bill-timeline-bigdata-2021-2024
- **2024 · 方法论由具体漏洞发现转向平台设计激励的批判性归纳**：2024-09-27 发布 Secrets and Shadows: Leveraging Big Data for Vulnerability Discovery at Scale，研究跨约三年，累计扫描超 500 万文件、验证 15000 余密钥，捕获 1,770,495 个 IP 下 78,000 余个悬空资源。以 AWS（约 32% 已报告密钥 2-3 个月后仍未撤销）与 GCP（默认强约束使硬编码更不便）对比，提出平台设计直接决定漏洞能否存在的论点，并明确要求被引用为 Independent Security Researcher、声明研究独立于雇主进行。方法论由具体漏洞发现转向平台设计激励的批判性归纳。（置信度：high）
  - 证据：bd-works-05-bigdata-cloud, bill-decisions-06, bill-community-06, demirkapi-ext-004, bill-timeline-bigdata-2021-2024

## 主要成长机制

### 消费场景触发的方向选择

起点：2018-09 购入 Dell G3 15 后对 Dell 经网页 Detect PC 远程更新驱动的能力产生怀疑；研究动机来自对预装软件与网页驱动更新的具体怀疑，而非抽象安全概念。

练习与反馈：以个人消费或使用场景为研究起点：Dell 笔记本购买触发 SupportAssist 逆向，硬盘清理发现旧竞赛镜像触发 CCSClient 复盘，研究 rootkit 检测方法时选用 Trend Micro RootkitBuster。；Dell 经网页向本地 8884 端口发起请求的行为经 Process Hacker 确认，验证了初始怀疑；CyberPatriot 评分引擎研究经开发者邮件确认其加密算法确需更换。

能力与结果：形成以日常可触达产品为攻击面入口、以具体怀疑驱动逆向的习惯，区别于以抽象安全概念为起点的路径。；Dell SupportAssist 远程代码执行研究（bd-works-01-dell-rce）；CyberPatriot 评分引擎逆向研究（bd-works-02-cyberpatriot）；Trend Micro RootkitBuster 内核驱动逆向研究（demirkapi-ext-002）

置信度：high；替代解释：OEM 预装软件攻击面的长期聚焦可能部分源于既有 Dell 研究形成的工具栈与思维路径依赖，而非每次均为独立消费场景触发；HP 与 Trend Micro 的选择更可能由主题延续驱动，消费场景触发的解释力在 2020 年后减弱。

证据：bd-works-01-dell-rce, bd-works-02-cyberpatriot, bill-decisions-01, bill-decisions-03, demirkapi-ext-001

### 失败—转向的解题路径

起点：Dell 研究中 open redirect 未果后作者自述几乎放弃（'I almost gave up at this point, because I couldn't find an open redirect vulnerability on any of the sites.'）。

练习与反馈：在路径受阻时记录失败并主动切换技术路径：Dell 中以 URL 前导空格绕过 StartsWith 校验改用 ARP/DNS 欺骗的中间人攻击；大数据研究中本地扫描 impractical 转向 serverless，std::regex 性能不足转 Intel hyperscan，GitHub Gist API 账号暂停转 Selenium Web UI。；StartsWith("http://") 对前导空格 payload 返回 false 使 http→https 替换被跳过，构成可验证的绕过；本地扫描 impractical 的工程反馈促使转向 AWS Lambda；hyperscan 相对 std::regex 提速约一个数量级构成可度量的性能反馈。

能力与结果：形成以工程可行性反馈为转向信号、而非以放弃为终点的解题习惯，并能以 PHP 代理、消息队列、自动化管道等工程手段补足单点技术缺口。；Dell SupportAssist 完整利用链（bd-works-01-dell-rce，绕过 StartsWith 校验）；多组件并行扫描系统（bd-works-05-bigdata-cloud，Python 协调器、C++ AWS Lambda、消息队列、MySQL）；GitHub Gist 自动撤销与 Selenium 绕过 shadow ban 的自动化管道（bd-works-05-bigdata-cloud）

置信度：high；替代解释：多次失败—转向记录集中于作者自撰 writeup，可能存在发表偏向：成功转向的案例更易被记录与公开，未成功转向或放弃的研究无从核验，失败—转向作为稳定机制的证据强度受自撰来源限制。

证据：bd-works-01-dell-rce, bd-works-05-bigdata-cloud, bill-decisions-05, bd-r2-01-startswith-primary

### OEM 预装软件攻击面的跨厂商复用

起点：作者自述长期将厂商预装软件视为独特攻击面（'I always have considered bloatware a unique attack surface.'），Dell SupportAssist 研究建立首个 OEM 预装软件攻击面样本。

练习与反馈：将同一预装软件攻击面方法论从 Dell 迁移到 HP：使用 dnSpy 配合 de4dot 解除 SmartAssembly 混淆，枚举 WCF 命名管道服务 250 余个函数，用 URLProtocolView 发现 hpdia:// 协议处理程序实现 RCE，用 Procmon 定位可劫持的缺失 DLL。；Dell 单漏洞约六个月才出补丁，而 HP 三个月内修补，但 HP 首轮补丁声称修复而作者复测发现仍未修补，且补丁以不可信客户端数据替换硬编码临时目录、引入新漏洞；作者据此公开质疑 HP 的代码审查流程。

能力与结果：形成将披露后厂商补丁质量本身纳入下一轮研究输入的习惯，建立报告—厂商声称修复—复测失败—补充报告—公开批评的迭代验证流程。；HP Support Assistant 研究：5 个本地提权、2 个任意文件删除、3 个远程代码执行变体（bd-works-03-hp-bloatware）；对 HP 补丁引入新漏洞的公开批评（bill-decisions-02）；补丁复审习惯在后续研究中重复出现（bill-timeline-hp-psirt-2019-2020）

置信度：high；替代解释：OEM 攻击面的跨厂商复用可能部分由 OEM 软件普遍采用 .NET 与 WCF 的技术同构性决定，工具栈复用的成本低于迁移到异构目标的成本；这一结构性条件降低了复用作为个人主动机制的解释权重。

证据：bd-works-01-dell-rce, bd-works-03-hp-bloatware, bill-decisions-02, bill-timeline-hp-psirt-2019-2020, bill-community-03

### 披露时间线的模板化

起点：Dell SupportAssist 研究中首次建立逐日披露时间线（2018-10-26 首报，Dell 2018-11-22 确认，原定 Q1 2019 后多次延期，2019-04-18 公开），约六个月协调披露周期。

练习与反馈：在后续研究中重复使用逐日披露时间线模板：HP（2019-10-05 报告，2020-01-01 提交补充报告，2020-04-03 发布）、WPI/TargetX（2019-01-03 报告，2019-04-13 公开）、大数据研究（与内布拉斯加州信息安全官及多个合作伙伴协调，向 AWS 报告泄露密钥）。；Dell 两次申请延期后作者以设定公开期限施加边界；WPI/TargetX 在厂商长期沉默后作者以 CC 上级并设定发布期限施压；HP 声称修复后复测失败促使补充报告；AWS 约 32% 已报告密钥 2-3 个月后仍未撤销促使公开点名问责。

能力与结果：形成将披露视为可管理流程、以逐日记录设定边界与施加压力的能力，并把厂商修复表现纳入公开输出。；Dell 协调披露与逐日时间线（bill-community-01、bill-timeline-dell-rce-disclosure-2018-2019）；HP 补丁复审与补充报告（bill-timeline-hp-psirt-2019-2020）；大数据研究中的多厂商与政府机构协调及公开问责（bill-community-06）；WPI/TargetX 披露施压策略（bill-timeline-college-admissions-2019）

置信度：high；替代解释：披露时间线模板的重复可能部分由厂商普遍采用延期协商流程这一外部约束决定，而非作者主动设计；逐日记录的复用也可能反映作者写作风格的延续，其作为能力机制的解释力需结合后续补丁复审成果共同判断。

证据：bill-community-01, bill-community-06, bill-timeline-dell-rce-disclosure-2018-2019, bill-timeline-hp-psirt-2019-2020, bill-timeline-college-admissions-2019, bill-decisions-06

### 工具建设作为规模化研究的工程约束

起点：据作者自述，2021 年起步时以本地扫描样本开始，发现本地扫描 incredibly impractical，促使其转向 serverless 架构；作者同时自述行业偏向目标导向漏洞挖掘而选择相反方向（'the industry is biased towards vulnerability hunting individual targets.'）。

练习与反馈：面对平台限制逐项工程化绕过：为绕过 VirusTotal Retrohunt 单任务 10000 样本上限按时间范围递归拆分任务；C++ AWS Lambda 扫描器采用 Intel hyperscan（相对 std::regex 提速约一个数量级）；构建通过发布 GitHub Gist 自动触发密钥撤销的管道，账号暂停后转向 Selenium Web UI。；据作者自述，本地扫描 impractical 促使其转向 serverless 架构，该因果链由作者自述提供，非独立确认；hyperscan 提速约一个数量级构成可度量的性能反馈；GitHub Gist API 账号暂停构成平台限制反馈；开始时既检测又验证密钥的工具据作者称尚未出现。

能力与结果：形成研究、工具实现与公开发表互相支撑的产出流程，工具建设扩展其规模化研究的可执行范围。；CloudRot 枚举 AWS 与 GCP 公网 IP，捕获 1,770,495 个 IP、78,000 余个悬空资源（bd-works-05-bigdata-cloud）；累计扫描超 500 万文件、验证 15000 余密钥（bd-works-05-bigdata-cloud）；GitHub D4stiny 置顶仓库在 2026-09-27 抓取时点获得数百量级 star：spectre=723、PeaceMaker=430、ForkPlayground=230、ExceptionOrientedProgramming=110（bd-r1-01-github-stars-2026-09-27，时点数据非稳定观察结果）

置信度：medium；替代解释：工具建设的必要性可能部分由规模化研究本身的技术要求决定，而非作者的个人偏好；多组件系统的构建也可能是作者在雇主提供的云资源条件下的产物，雇主条件作为未公开变量限制了工具建设作为可迁移个人机制的边界判断。

证据：bd-works-05-bigdata-cloud, bill-decisions-04, bill-decisions-05, bill-timeline-github-d4stiny, bd-r1-01-github-stars-2026-09-27

### 前辈 writeup 与致谢提及 mentor 的输入

起点：Trend Micro RootkitBuster 研究致谢 mentor Alex Ionescu 在内核内存分配技术上给予方向指引，并引用 j00ru 2010 年 HackInTheBox Magazine 关于 Reserve Objects 的文章作为关键技术来源；大数据研究的方向转型受 Matt Bryant 2015 年博客 Fishing the AWS IP Pool for Dangling Domains 启发，作者称该文 pivotal to our understanding of the bug class。

练习与反馈：以可识别的前辈公开研究为方法学来源：j00ru 的 Reserve Objects 文章作为内核利用原语的方法学基础，Matt Bryant 的 AWS IP 池文章作为规模化漏洞发现方向转型的触发点；HP 研究中 Matt Graeber 提供关于 Windows TEMP 目录权限特性的关键提示。；Alex Ionescu 的方向指引使作者在内核内存分配技术路径上获得点拨；Matt Graeber 的提示直接补全了 HP 研究中的知识缺口；Matt Bryant 的文章触发由单点目标逆向到漏洞类驱动规模化发现的方法论转向。

能力与结果：形成回溯阅读经典技术文献与既有公开研究并以之为方法学基础的习惯，而非孤立产出。；Trend Micro 内核利用三类原语（任意内核函数调用、任意内核读写、卸载例程滥用）（demirkapi-ext-002）；大数据规模化漏洞发现方向（bd-works-05-bigdata-cloud）；HP 研究中补全 Windows TEMP 目录权限知识缺口（bill-community-03）

置信度：medium；替代解释：Alex Ionescu 的 mentor 关系证据等级为单处致谢提及（'a mentor of mine, Alex Ionescu'），不应放大为持续的指导关系；方向转型与前辈 writeup 的关联也可能由作者事后归因放大，Matt Bryant 文章作为转型触发的因果链由作者自述提供，非独立确认。

证据：demirkapi-ext-002, bill-community-03, bill-community-04, bill-decisions-04, bill-timeline-trend-micro-mentor-2020

### 公开发表与职业可见度反馈

起点：2019 年起建立高频公开发表节奏（全年 8 篇），并将 GitHub 仓库与 writeup 配套发布（ExceptionOrientedProgramming 仓库与 Part 1 同步）。

练习与反馈：以公开 writeup 与可复现代码配套作为研究产出标准：Dell、HP、Trend Micro、CVE-2021-40444、Exception Oriented Programming、大数据研究均以博客全文配 GitHub 仓库或 PoC 发布；2021-11-25 在与 diversenok 独立重复发现进程克隆读内存技术时，以 2021-06-19 预先公开 SHA256 哈希作为优先权证据。；据作者 Part 2 自述，Microsoft 在 Exception Oriented Programming Part 1 发布后录用其入职，该时序关联与因果关系均由作者自述提供，非独立确认；GitHub D4stiny 置顶仓库在 2026-09-27 抓取时点获得数百量级 star；CyberPatriot 评分引擎研究发布后收到竞赛开发者邮件反馈并据此调整发布时机。

能力与结果：形成以公开发表作为研究闭环、并以预签哈希等可核验机制处理同行优先权竞争的习惯。；2019 年高频公开发表（bd-works-06-blog-bibliography）；Exception Oriented Programming Part 1 与 GitHub 仓库配套发布（bill-timeline-eop-part1-2022）；进程克隆研究的预签哈希优先权机制（bill-community-05）；Microsoft 录用自述（bill-timeline-microsoft-hire-2023）

置信度：medium；替代解释：Microsoft 录用与 Part 1 公开发表的因果关联仅由作者自述支撑，录用亦可能由其他渠道（如既往 CVE 记录、同行推荐、招聘流程）促成，公开发表作为录用直接原因的解释力受限于自述来源；star 数为 2026-09-27 抓取时点数据，不能作为稳定影响力指标。

证据：bd-works-06-blog-bibliography, bill-timeline-eop-part1-2022, bill-timeline-microsoft-hire-2023, bill-community-05, bill-timeline-github-d4stiny, bd-r1-01-github-stars-2026-09-27

## 可迁移与不可迁移

- 可迁移：以最小复现用例为逆向首要步骤，并对成功与失败路径做双向对照、对补丁前后做二进制比对（bd-works-04-cve-2021-40444）。
- 可迁移：在路径受阻时记录失败并主动切换技术路径，以工程可行性反馈为转向信号，而非以放弃为终点（bd-works-01-dell-rce、bd-works-05-bigdata-cloud）。
- 可迁移：将披露视为可管理流程，以逐日记录设定边界与施加压力，并把厂商补丁质量的独立复审纳入下一轮研究输入（bill-community-01、bill-timeline-hp-psirt-2019-2020）。
- 可迁移：回溯阅读经典技术文献与既有公开研究作为方法学基础，并以预签哈希等可核验机制处理同行优先权竞争（bill-community-04、bill-community-05、bill-decisions-04）。
- 可迁移：以公开 writeup 与可复现代码配套作为研究产出标准，使研究成果可被他人核验与复用（bill-timeline-eop-part1-2022、bill-timeline-github-d4stiny）。
- 不可直接迁移：OEM 预装软件攻击面的跨厂商复用部分由 OEM 软件普遍采用 .NET 与 WCF 的技术同构性决定，工具栈复用成本低于迁移到异构目标，该结构性条件不可直接迁移到非同构目标族。
- 不可直接迁移：大数据规模化研究依赖 VirusTotal Retrohunt、AWS Lambda、被动 DNS 等平台与云资源，其工具建设的必要性与可行性部分由这些平台条件与可能的雇主资源条件决定，未公开的雇主条件限制了工具建设作为可迁移机制的边界判断。
- 不可直接迁移：公开 writeup 与职业机会的关联受作者所处时期（2019–2024）安全行业对公开漏洞研究的高度重视这一外部条件影响，该关联在行业重视度下降时可能减弱，不可作为稳定因果迁移。
- 不可直接迁移：Alex Ionescu 的 mentor 关系为单处致谢提及，j00ru、Matt Bryant、Matt Graeber 的输入依赖作者与特定前辈网络的偶然接触，此类外部输入条件不可直接迁移。
- 不可直接迁移：本研究所列成长机制的边界判断受自撰来源自我呈现偏差与幸存者偏差限制，未公开的失败与中止研究无从核验，相关 transferable_practices 的可迁移性应在该限制下解读。

## 复核问题

- mechanisms[M4].feedback、stages[4].capability_change 及 tensions 中 AWS 密钥未撤销时间的口径处理：evidence 内部 bill-community-06（'over 2-3 months ago'）与 bill-decisions-06（'4 个月未撤销'）对同一事实存在分歧。建议在 mechanisms[M4].feedback 或 tensions 中显式标注该 evidence 内部口径分歧，或将统一表述改为 '据作者 2024 博文自述，约 32% 已报告 AWS 密钥在数月后仍未撤销（bill-community-06 记为 2-3 个月，bill-decisions-06 记为 4 个月，口径未完全一致）'，以闭合可追溯性缺口。此为增强标注建议，非关键事实错误。
- stages[0]（2015-2018）capability_change 的身份标签时间锚定：原措辞 '该阶段身份为 17 岁高中在校生，作为 evidence 记录而非阶段核心标签' 中，'17 岁' 来自 2019-01-03 自述，不能直接锚定到 2015-2018 阶段。建议改为 '据 2019 年自述为 17 岁高中在校生（bill-timeline-college-admissions-2019），该身份标签锚定于 2019 年而非 2015-2018 赛季期间'，或将该身份标签从 stages[0] 移至 stages[1]（2019 阶段），stages[0] 仅保留参赛 2015-2018 这一由 bill-timeline-cyberpatriot-2015-2018 直接支撑的核心 claim。此为时间锚定收紧建议，非核心 claim 错误。

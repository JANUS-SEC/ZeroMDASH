# Sam Curry：漏洞研究成长分析

- 擅长领域：Web/API/汽车漏洞
- 独立复核：pass · 86/100

## 成长阶段

- **2020-07 至 2020-10 · 团队化、固定时间窗的单一厂商大规模赏金项目**：首次在大规模厂商赏金项目上组织多研究者协作，并设定约三个月的固定钻研窗口；研究在疫情多出的空闲时间内被放大为一个有计划而非偶发的项目，形成可重复的复测—重测—披露节奏。（置信度：medium）
  - 证据：SC-TL-01
- **2021 · 个人安全事件取证留存与首次公开概念验证**：将一次个人调制解调器被重放流量的安全事件保存为取证数据并长期搁置，同时同期在 GitHub 发布 CVE-2021-27651（Pega Infinity RCE）概念验证仓库；形成保存证据—延迟分析—后续回溯的研究习惯，能力从一次性漏洞发现扩展到证据留存与公开 PoC 输出。（置信度：high）
  - 证据：SC-TL-02, sc-rr2-002, sc-decisions-01
- **2023-03 至 2023-08 · 多租户后端平台研究与合作者复用**：由进入信用卡 churning 社区的实际使用痛点驱动选择 points.com 为目标，技术栈从单点漏洞扩展到 OAuth 2.0 MAC 签名手工模糊测试、Flask 会话密钥爆破、目录穿越与租户凭据泄漏链；与 Ian Carroll、Shubham Shah 形成跨项目复用的协作关系，并在同一季度内对单一目标做多轮发现—报告—验证循环。（置信度：high）
  - 证据：SC-TL-03, sc-pub-002, sc-ext-01
- **2024-03 至 2024-06 · 个人事件回溯研究与 ISP 后端基础设施转向**：中止固件提取方向的尝试，改以 ISP 的 TR-069 后端管理基础设施为研究对象；技术栈新增客户端 JS 可还原 AES 密钥、反向代理路径混淆（%2f）与未鉴权 Swagger 文档分析；采用 90 天披露窗口与草稿预共享流程，并依赖朋友提供的 MSP/Cox Business 账户访问补齐证据链；对自身推断保持可证伪态度，区分证明了漏洞存在与证明了因果。（置信度：high）
  - 证据：SC-TL-04, sc-pub-003, sam-curry-self-001, sam-curry-self-002, sam-curry-self-003, sc-decisions-02, sc-decisions-11, sc-ext-05
- **2024-06 至 2024-09 · 车联网端到端自动化利用与经销商端横向移动**：由 owners.kia.com 与 iOS app 转向经销商域 kiaconnect.kdealer.com，构建车牌→VIN→车主 PII→降级原车主→注册新主账户的四步端到端自动化链，约 30 秒内远程控车；沿用消费者侧转向经销商侧的横向移动思路；9 月 20 日为 writeup 发布日，9 月 26 日为作者验证修复后公开披露日，二者分别表示发布与披露节点；将本次研究置于对十余家车企长期跟踪的延续线上。（置信度：high）
  - 证据：SC-TL-05, sc-pub-004, sc-rr2-001, sc-decisions-03, sc-decisions-04, sc-community-03, sc-community-04, sc-ext-02
- **2024-11 至 2025-01 · STARLINK 管理面板与消费者端→管理员端横向移动复现**：以个人购置的 2023 Subaru Impreza 为测试目标，在消费者侧鉴权健全后由协作者经 CNAME 链发现 subarucs.com，FFuF 爆破得到 login.js 中的脆弱密码重置端点，结合 LinkedIn 邮箱枚举与客户端 2FA 绕过进入管理员面板，影响美/加/日全部车辆；消费者端→员工/管理员端的横向移动手法再次出现并工具化；披露窗口由 90 天缩短至 24 小时内修复，但仍按厂商修复节奏公开。（置信度：high）
  - 证据：SC-TL-06, sc-pub-005, sc-decisions-05, sc-decisions-06, sc-community-01, sc-community-02, sc-community-05, sc-ext-03
- **2025-06 至 2025-10 · Web 后台攻击面回归与源码/配置暴露整合利用**：研究目标由车联网回到 Web 后台管理面板（ClubWPT Gold），由玩家后端好奇经前端 JS 环境变量与子域枚举发现 coin-admin；整合源码暴露（.env/.git 经 GitHack 拉取）、硬编码弱口令与 Censys 证书搜索绕 Cloudflare 定位源 IP，最终利用未鉴权 /admin/otp/bind 覆盖任意用户 2FA；首次明确记录对非传统漏洞目标的沟通困难，并通过行业内部人脉建立披露渠道；报告后厂商数小时内修复，修复确认与公开披露的闭环细节弱于 Kia、Subaru。（置信度：medium）
  - 证据：SC-TL-07, sc-pub-006, sc-decisions-07, sc-decisions-08, sc-community-06, sc-ext-04

## 主要成长机制

### 消费者端鉴权健全后转向员工/管理员端的横向移动启发式

起点：已有对若干车企消费者侧应用的多品牌长期跟踪经验，并形成对相邻未测攻击面保持好奇的习惯（Subaru 正文短引文 'From my past experience with car companies, I knew there could be publicly accessible employee-facing applications with broader permissions'）。

练习与反馈：在消费者侧鉴权机制健全、直接攻击受阻时，主动切换视角寻找员工/管理员端：Kia 中因已熟悉用户侧而转向经销商域 kiaconnect.kdealer.com（短引文 'Since we were already super familiar with the user side of things, we decided to look at the Kia Dealer website instead'）；Subaru 中由 Shubham Shah 经 CNAME 链发现 subarucs.com 引导转向 STARLINK Admin Panel。；经销商/管理员端应用暴露了消费者端不可达的能力（VIN 查询、车主 PII 读取、车辆注册修改、跨国车辆访问），转向的产出回报高于继续在消费者端反复测试；该回报在不同品牌研究中重复出现，强化了转向启发式的复用。

能力与结果：形成消费者端→员工/管理员端的横向移动思路，并将其作为可迁移的攻击面扩展方法，而非一次性发现。；Kia：经销商认证绕过→VIN 获取车主 PII→降级原车主→注册新主账户的四步端到端自动化链，约 30 秒控车。；Subaru：进入 STARLINK 管理面板，影响美/加/日全部车辆与客户账户。；横向移动思路在 Kia、Subaru 两个品牌研究中重复出现并工具化。

置信度：medium；替代解释：本机制仅覆盖 Kia、Subaru 两例，二者转向前提同构（消费者端鉴权健全后受阻转向员工端）。ClubWPT 的转向由玩家后端好奇经子域枚举发现 coin-admin 触发，前提与 Kia/Subaru 不同构，故未纳入本机制。短引文 'From my past experience with car companies' 为本人叙事表述，可能为叙事修辞而非严格的方法迁移声明；由失败转向、失败迁移不可见带来的幸存者偏差可能使该启发式在已成功案例中显得比实际更可靠，失败案例未被记录导致归因偏差。

证据：sc-decisions-03, sc-decisions-06, sc-pub-004, sc-pub-005

### 同伴社群驱动的协作分工与发布前同行评审

起点：已通过过往项目（如 Apple 赏金项目联系过去合作过的黑客组队）积累一批同辈研究者网络（Brett Buerhaus、Ian Carroll、Shubham Shah、Justin Rhinehart 等），而非正式导师关系。

练习与反馈：在发现线索后主动经社区渠道（如 Discord）物色合作者并分工：Subaru 中 Curry 主动联系 Shubham Shah（短引文 'I sent my friend Shubs a message over Discord to see if he'd be interested'），后者完成 CNAME 链与域名侦察，Curry 负责入口审计；Kia 由 5 人共同署名，points.com、ClubWPT 由 Shubham Shah 跨项目共同署名。发布前由多名同行评审 writeup（Subaru 经 7 人评审）。；协作者的互补技能（域名侦察、malware 分析、DGA 识别）在多个研究中补齐单点盲区，例如 modem 研究由同伴识别 DGA 模式重启调查；发布前同行评审可在披露前校正技术叙述与影响边界，降低误报与协调披露风险。

能力与结果：形成可复用的协作单元与固定分工模式，把寻找合作者的成本摊销到多项研究中；把发布前评审作为披露流程的固定环节。；Subaru 由 Shubham Shah 经 CNAME 链发现 subarucs.com，引导转向员工端。；modem 研究由同伴基于恶意软件分析经验识别 DGA 模式，将线索重新定性为 C&C 设施，推动三年搁置的研究重启。；Subaru writeup 由 7 名同伴评审，Kia 由 5 人共同署名并附 handle 化致谢网络。；Shubham Shah 在 points.com、Subaru、ClubWPT 中跨项目共同署名，形成稳定二人协作。

置信度：high；替代解释：协作分工与同行评审的可得性受既有同伴网络规模与构成影响，存在幸存者偏差：未成功建立协作或评审失败的研究未进入公开记录，使协作机制显得比实际更稳定有效；同伴网络的具体构成与每位成员的实际贡献无法从 writeup 署名与致谢中逐一回溯到具体协作事件。

证据：SC-TL-01, SC-TL-03, sc-community-01, sc-community-02, sc-community-03, sc-community-06, sam-curry-self-002, sc-pub-002

### 多阶段协调披露节奏与对厂商响应的主动跟踪催办

起点：已形成负责任披露意识，并将披露环节视为研究过程的一部分而非漏洞发现后的附属事务。

练习与反馈：在多项研究中重复采用结构化的多阶段披露流程：报告→热修复→草稿预共享→修复验证→公开，并对厂商响应进行主动跟踪催办。modem 研究 2024-03-04 报告 Cox、03-05 热修复、04-29 草稿预共享、06-03 公开；Kia 研究 06-11 报告、08-14 厂商确认修复、09-20 writeup 发布、09-26 作者验证修复后公开披露，期间含多次跟踪催办（6/12、6/18、6/20、8/12）推动厂商响应；Subaru 11-20 报告、11-21 修复（24 小时内）；ClubWPT 见 customer PII 即停止并报告，遇联系阻塞时绕道行业大使触达基础设施负责人。；周期性跟进厂商响应把厂商响应速度纳入研究流程，而非把修复完全交给厂商；草稿预共享与修复验证后公开的流程在多个研究中得到厂商配合（Cox 热修复、Kia 确认修复、Subaru 24 小时修复），强化了先报告后公开流程的可信度。

能力与结果：形成可重复的协调披露节奏与披露纪律（见 PII 即止、遇联系阻塞绕道非官方渠道），把披露环节本身作为重复练习与建设的对象。；modem 研究：报告→6 小时热修复→草稿预共享→90 天窗口公开的完整多阶段披露。；Kia 披露含多次跟踪催办（6/12、6/18、6/20、8/12）推动厂商响应，9-20 writeup 发布、9-26 验证修复后公开披露。；Subaru 11-20 报告、24 小时内修复，作者无法复现后按厂商修复节奏公开。；ClubWPT 见 customer PII 即停止并报告，遇联系阻塞绕道大使触达基础设施负责人。

置信度：medium；替代解释：披露节奏的强重复部分为多阶段协调披露与对厂商响应的主动跟踪催办（modem、Kia、Subaru 多例）。固定时间窗组队仅 Apple 赏金项目一例，重复度不足，不宜与强重复部分捆绑命名；本机制 name 仅取强重复部分。ClubWPT 报告后厂商数小时内修复，修复确认与公开披露的闭环细节弱于 Kia、Subaru，对 ClubWPT 的闭环强度不作与 Kia、Subaru 同等的统一断言。rank=26 与既有同行网络可能放大厂商响应速度与评审可得性，HackerOne 档案（hackerone.com/samwcyo）返回 404 使平台声誉与该层归因无法独立核验；由失败披露、披露延迟不可见带来的幸存者偏差可能使披露流程显得比实际更顺畅，失败案例未被公开记录。

证据：SC-TL-04, SC-TL-05, SC-TL-06, sc-pub-003, sc-pub-004, sc-pub-005, sc-pub-006, sc-decisions-08, sc-decisions-11, sc-community-04, sc-community-05, sc-rr2-001

### 个人生活经历与使用痛点转化为研究选题

起点：对日常接触系统保持安全好奇心，并有以个人消费决策构建测试条件的习惯（Subaru 购置 2023 Impreza 部分原因是承诺借其测试）。

练习与反馈：把个人生活经历与使用痛点作为研究选题来源：modem 研究由 2021 年自用调制解调器被重放流量触发（短引文 'An unknown IP address had replayed the exact same HTTP request just 10 seconds later'）；points.com 由进入信用卡 churning 社区的实际需求触发；Subaru 由购置家庭用车触发；ClubWPT 由 DEF CON 期间养成的 poker 爱好触发（短引文 'my guilty pleasure has been sneaking away to the Aria poker room and playing No Limit Holdem until 3 or 4 in the morning'）。；由生活经历触发的选题在多个研究方向（ISP 设施、积分平台、车联网、博彩后台）产生可公开的完整 writeup，强化了以日常接触系统为选题来源的习惯；个人受害事件经三年搁置后仍能重启为系统研究，提示长期保留未解问题的价值。

能力与结果：形成生活经历→研究选题的转化习惯，使选题不依赖纯赏金激励或纯计划性推进，而是对日常接触系统保持安全好奇心驱动。；modem 事件经三年搁置后由同伴 DGA 识别重启，最终公开 Hacking Millions of Modems writeup。；ClubWPT 由 poker 爱好触发，扩展研究范围至在线博彩后台。；Subaru 由家庭用车购置触发，延续车联网方向。；points.com 由信用卡 churning 社区实际需求触发，建立多租户后端研究方向。

置信度：high；替代解释：生活经历→选题的转化在多个研究方向重复出现，但选题成功与否受个人可触达的资源（自用设备、家庭用车、爱好场景、社交契机）影响，存在幸存者偏差：未能转化为公开研究的生活经历未被记录，使该机制显得比实际更可靠。ClubWPT 中短引文 'like we did previously' 与 modem 中短引文 'my computer had been hacked' 为本人叙事表述，可能为叙事修辞而非严格的方法迁移或事实陈述；由失败转向、失败迁移不可见带来的叙事连贯偏差可能使选题机制在已成功案例中被过度归因。

证据：sc-decisions-01, sc-decisions-05, sc-decisions-07, sc-pub-002, sc-pub-003, sam-curry-self-001, SC-TL-03

## 可迁移与不可迁移

- 可迁移：在消费者侧鉴权健全、直接攻击受阻时，主动切换视角寻找员工/管理员/经销商端应用作为相邻未测攻击面，并以 CNAME 链与子域枚举定位该类端点。
- 可迁移：在发现线索后主动经社区渠道物色互补技能的合作者并分工，把寻找合作者的成本摊销到多项研究中；将发布前同行评审作为披露流程的固定环节以校正技术叙述与影响边界。
- 可迁移：采用结构化的多阶段披露流程（报告→热修复→草稿预共享→修复验证→公开），并对厂商响应进行主动跟踪催办，把厂商响应速度纳入研究流程而非完全交给厂商。
- 可迁移：把个人生活经历与使用痛点作为研究选题来源，对日常接触系统保持安全好奇心，并对未解问题长期保留以等待外部契机重启。
- 可迁移：以个人消费决策（如购置测试用设备）自费构建测试条件，降低对外部测试授权的依赖。
- 可迁移：在披露纪律上结合扩大影响面取证与见敏感数据即止：先确认是否存在可访问的 production 版本再报告，见到 customer PII 立即停止并报告；遇联系阻塞时主动寻找非官方渠道绕道触达负责人。
- 不可直接迁移：rank=26 的平台声誉与既有同行网络（Brett Buerhaus、Ian Carroll、Shubham Shah、Justin Rhinehart 等）可能放大厂商响应速度与评审可得性，且 HackerOne 档案 hackerone.com/samwcyo 返回 404 使该层归因无法独立核验；该声誉与网络为个人特有条件，非可迁移方法。
- 不可直接迁移：约 2022 年多品牌汽车研究的早期积累（sc-pub-007, reported；内回溯引用估计影响约 1550 万辆汽车）为后续 Kia、Subaru 的重复题材与同一团队模式奠定基础，但该研究一手 blog URL 与确切发布日期未能定位，其作为起点的可复现性不可迁移。
- 不可直接迁移：modem 研究依赖朋友提供的 MSP/Cox Business 账户访问以复现，并依赖同伴基于恶意软件分析经验识别 DGA 模式；这类外部账户资源与同伴专业互补为个人特有条件。
- 不可直接迁移：Subaru 研究以个人购置的 2023 Impreza 为测试目标，ClubWPT 由 DEF CON 期间 poker 爱好触发；个人可触达的生活场景与消费决策为个人特有条件。
- 不可直接迁移：Kia 研究中向联系人索取 Kia 发送的注册链接以获得经销商门户入口，依赖具体社交工程式协作机会，为个人特有条件。
- 不可直接迁移：Black Hat US 演讲（person_json 所记）与外部权威媒体报道（TechCrunch、404 Media 摘要线索）均未经一手核实，相关外部可见度不可作为可迁移条件。

## 复核问题


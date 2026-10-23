# Shubham Shah：漏洞研究成长分析

- 擅长领域：Web 与外部攻击面漏洞
- 独立复核：pass · 86/100

## 成长阶段

- **2013–2015 · 单站机会主义型披露与对外公开发表习惯建立**：在个人博客 shubs.io 上以作者 shubs 身份连续公开单站、单点 Web 漏洞（eBay 持久型 XSS、PayPal SSRF、Coinbase 钓鱼设计缺陷、跨厂商 2FA 绕过）。研究目标以单个厂商的单一缺陷为主，披露形式以 full disclosure 与厂商响应记录并行。形成可核验的公开发表习惯，并开始在标题中记录厂商响应态度与披露策略。SSRF 这一后续贯穿其研究主线的技术方向在 2014 年 PayPal 文章中首次出现。同期启动 Websec Weekly 周刊项目，由单篇披露扩展到周期性内容产品。该阶段未见系统化的方法论抽象，目标选择呈机会主义型。（置信度：high）
  - 证据：ss-pub-2013-ebay-xss, ss-pub-2014-paypal-ssrf, ss-pub-2014-2fa-bypass, ss-pub-2015-websec-weekly, ss-timeline-01, ss-timeline-02, ss-timeline-03, ss-timeline-04, ss-timeline-05
- **2016–2018 · 量化研究节奏与「资产识别 + 持续监控」方法论早期定型**：以「120 天 / 120 漏洞」的量化目标公开驱动高强度产出，并把「识别组织在互联网上的资产」确立为长期方法论核心，自称该阶段方法论仍围绕资产识别展开。研究行为从机会主义单点披露转向可衡量周期组织的重复练习。同期开始批判性反思 bug bounty 平台治理（The deterioration of unmanaged bug bounties），与后续 2021 triage、2022 collaboration、2026 down fall 形成跨十余年的生态反思序列。约 2016 年 4 月起系统参与漏洞赏金，回顾文中以 1590 天、$635,387.47 收益与 24 SQLi/22 SSRF/20 IDOR/11 RCE 的分布自述早期积累，以可量化指标而非天赋叙事呈现积累过程。该阶段后期（2017–2018）博客出现空窗，与后续 Assetnote 产品建设期对应，但创立公告等过渡节点缺乏一手材料。（置信度：high）
  - 证据：ss-pub-2016-120bugs, ss-timeline-06, ss-timeline-04, ss-dec-01
- **2018–2020 · 个人方法论工程化为产品、深度目标深耕与链式利用**：2018 年与 Michael Gianarakis 共同创立 Assetnote（攻击面管理平台），任 Co-Founder and CTO，把个人方法论（资产识别、持续监控、自动化）工程化为产品，回顾文称「we built as much of the workflows, techniques, tooling and methodologies into Assetnote」。研究深度从单点漏洞上升到云基础设施层面的 0day 与 RCE 链，在 shubs.io 个人署名发布 Mozilla AWS 网络零日与代码执行链，以及 Zoom RCE Followup，后者为研究对象个人署名作品，记录其在 Zoom 平台取得 RCE 的后续研究。工具链从 Python 迁移到 Golang/Rust 以提升资产识别速度，DNS 解析器用 Rust 重写，反映按性能瓶颈选择语言并重写核心组件的工程判断。明确选择深耕 Uber 攻击面（自称「simply enjoyed it more and valued the team working there」），通过观察 Uber 攻击面随时间收敛反推方法论，以深度重复练习优先于短期高赏金。2020 年发布「Hacking on Bug Bounties for Four Years」进行阶段复盘，与 2016 年量化节奏文章形成可核验的反馈—总结—再投入循环。同期开始把协作列为成长机制，列出多名同伴分工完成 .NET 反序列化、XXE、DNS 爆破优化、JS sourcemap、ATO、WebPageTest RCE 等环节。注：Zendesk GCP/Artifactory 一文经逐篇正文核实作者为 Ruby Nealon（非研究对象），不纳入个人方法论重复应用目标。（置信度：high）
  - 证据：ss-pub-2019-mozilla-aws-0day, ss-pub-2020-120bugs-four-years, ss-pub-2020-react-native, ss-pub-2020-iis-bigquery, ss-r1-zoom-rce-personal, ss-r1-zendesk-nealon-not-personal, ss-timeline-07, ss-timeline-08, ss-dec-01, ss-dec-02, ss-dec-03, ss-dec-04, ss-dec-05
- **2021–2026 · 由产品/工程负责人转为研究团队负责人、团队层企业 RCE 与方法库沉淀**：2025 年 Assetnote 被 Searchlight Cyber 收购，研究对象由 Co-Founder and CTO 转任 Chief Security Research Officer，领导全球安全研究团队，研究成果接入 Searchlight Exposure 产品，角色由产品/工程负责人转为研究负责人。研究产出渠道由个人博客转向团队研究博客 slcyber.io，按月发布企业软件 0day。该阶段团队连续披露 ServiceNow 沙箱预认证 RCE（CVE-2026-6875，2026-07-14）、WordPress 核心预认证 RCE（wp2shell，2026-07-17）、Goja JavaScript 引擎越界与沙箱逃逸 RCE（2026-09-07）等；上述 writeup 多由同事 Adam Kues 署名（ss-community-04/05），研究对象个人署名在该阶段未直接确认，归属层级为团队而非个人。团队 writeup 显示研究流程中引入 AI 辅助发现路径（ss-community-06 标题陈述使用 GPT5.6 Sol Ultra 与 25 美元成本发现 WordPress RCE），但该 writeup 未署研究对象本人姓名，个人是否参与及参与程度未由一手页面确认。研究对象个人署名的同期产出见于 shubs.io：A Glossary of Blind SSRF Chains（2021，把盲 SSRF 利用链整理为可检索参考表，呼应 2014 PayPal SSRF）、So, you want to get into bug bounties?（2022，教学型入门指南）、The down fall of bug bounties（2026，延续 2014 起的生态批判序列）。研究主题由早年通用 Web/云配置错误转向企业软件链中的反序列化/SQLi/RCE，并叠加检测机制与 AI 辅助。该阶段个人能力演化的可核验证据集中于方法库沉淀与生态批判写作；企业级 RCE 的具体技术贡献在团队层面可核验，个人直接贡献未由一手页面确认。（置信度：medium）
  - 证据：ss-pub-2026-servicenow-sandbox, ss-pub-2026-wp2shell, ss-pub-2026-wp-gpt, ss-pub-2026-goja-rce, ss-role-slcyber-csro, ss-timeline-09, ss-timeline-10, ss-timeline-11, ss-timeline-12, ss-timeline-13, ss-timeline-14, ss-community-04, ss-community-05, ss-community-06, ss-community-07, ss-dec-07, ss-dec-08

## 主要成长机制

### M1 攻击面方法论在同一框架下的跨目标重复应用

起点：2014 年 PayPal SSRF 文章显示研究对象在早期已聚焦 SSRF 这类可横向触及内部网络的漏洞类别；2016 年回顾文把「识别组织在互联网上的资产」确立为方法论核心，称「my methodology still revolves around the identification of assets belonging to an organization on the internet」。

练习与反馈：把同一资产识别 + SSRF/RCE 链构建方法论反复应用于不同目标：早期 PayPal SSRF（2014）、Mozilla AWS 网络零日与代码执行链（2019，shubs.io 个人署名）、Zoom RCE Followup（2019-07-17，slcyber.io 个人署名，致谢 Sean Yeoh、Michael Gianarakis、Ruby Nealon、Huey Peard）。2021 年 A Glossary of Blind SSRF Chains 把反复出现的盲 SSRF 利用链整理为可检索参考表，是该方法论跨目标重复后的结构化沉淀。注：Zendesk GCP/Artifactory 一文经逐篇正文核实作者为 Ruby Nealon（非研究对象），不纳入个人方法论重复应用目标。；厂商响应（如 eBay 标注「wont fix」、ServiceNow 团队层面称厂商在 24 小时内部署缓解）与个人署名 writeup 的对外公开发表构成反馈，使方法论在跨目标应用中被持续校正与结构化；shubs.io 个人博客的持续更新与 slcyber.io 个人署名 writeup 为可核验的对外输出渠道。

能力与结果：形成「资产识别 → SSRF/RCE 链构建 → 可复用参考表」的稳定研究框架，单点发现可被抽象为跨目标可复用的技术参考，而非停留在个案披露。；2014 PayPal SSRF → 2019 Mozilla AWS 0day 与代码执行链 → 2019 Zoom RCE Followup，目标难度从单站 Web 漏洞上升到云基础设施与平台 RCE；2021 A Glossary of Blind SSRF Chains 把分散经验结构化为可检索社区参考表；2016「120 天 / 120 漏洞」与 2020 四年回顾形成可量化的反馈—总结—再投入循环

置信度：high；替代解释：跨目标方法论一致性也可能部分源于该时期 Web/云漏洞的整体生态特征（SSRF 与云元服务普遍存在）以及 Assetnote 产品本身对资产识别的方向性引导，而非完全由个人方法论的内在演化驱动；个人署名 writeup 的目标选择仍可能受偶然机会（厂商赏金项目开放、零日出现时机）影响。

证据：ss-pub-2014-paypal-ssrf, ss-pub-2016-120bugs, ss-pub-2019-mozilla-aws-0day, ss-pub-2020-120bugs-four-years, ss-r1-zoom-rce-personal, ss-r1-zendesk-nealon-not-personal, ss-timeline-02, ss-timeline-06, ss-timeline-07, ss-timeline-08, ss-timeline-09, ss-dec-01

### M2 量化节奏驱动的重复练习与周期性阶段复盘

起点：2016 年发布「High frequency security bug hunting: 120 days, 120 bugs」，以明确量化目标（120 天 / 120 bug）驱动高强度产出，并对外公开复盘。

练习与反馈：以可衡量周期组织研究并周期性对外复盘：2016 年 120 天/120 bug 的高频周期，约 2016 年 4 月起系统参与漏洞赏金并以 1590 天、$635,387.47 收益与 24 SQLi/22 SSRF/20 IDOR/11 RCE 的分布自述积累，2020 年发布「Hacking on Bug Bounties for Four Years」进行四年阶段复盘，与 2016 年高频周期形成可核验的反馈—总结—再投入循环。；量化指标（天数、漏洞数、收益、漏洞类型分布）本身作为自我反馈，阶段回顾文把跨时期的指标对比作为方法论校正依据；对外公开发表使复盘可被同业核验。

能力与结果：以可衡量周期与量化指标组织长期研究，形成反馈—总结—再投入的稳定节奏，而非依赖一次性发现或天赋叙事。；2016 高频周期文章 → 2020 四年回顾，时间跨度与量化指标可核验连续；回顾文把方法论核心表述为资产识别，标志早期定型；2021 SSRF 词汇表与 2022 入门指南显示由个人复盘转向对外方法库与教学输出

置信度：high；替代解释：量化复盘也可能是 bug bounty 平台激励机制（公开榜单、收益可见）的自然产物，未必反映独立的内在方法论；2017–2018 博客空窗与 2023–2025 上半空窗的存在显示该节奏并非全程连续，可能受 Assetnote 产品建设与收购过渡期等组织因素打断。

证据：ss-pub-2016-120bugs, ss-pub-2020-120bugs-four-years, ss-timeline-06, ss-timeline-08, ss-timeline-09, ss-timeline-10, ss-dec-01

### M3 工具化：把反复出现的侦察/利用需求抽象为可复用工具并开源

起点：2015 年 Websec Weekly 显示研究对象早期已有从单篇披露向内容/产品延伸的倾向；2018 年创立 Assetnote 后把个人方法论工程化为产品，回顾文称「we built as much of the workflows, techniques, tooling and methodologies into Assetnote」。

练习与反馈：把反复出现的侦察/利用需求抽象为开源工具：GitHub 组织 assetnote 下集中发布 API 内容发现、子域/口令字典、SSRF 候选筛选、WAF 绕过、HTTP/2 cleartext 走私等外部攻击面工具（kiterunner、surf、commonspeak2、wordlists、nowafpls 等）；旗舰侦察工具 kiterunner 截至 2026-09-27 有约 3.3k star、341 fork、41 个未关闭 issue 与 10 个未关闭 PR。研究 writeup 与配套开源 PoC 工具同步发布（如 Goja RCE writeup 与 goja-heap-oob 仓库对应），把发现同时以文字披露与可执行工具两种形式回流社区。2018–2020 年工具链从 Python 迁移到 Golang/Rust，DNS 解析器用 Rust 重写，按性能瓶颈选择语言并重写核心组件。；issue/PR 是社区对工具的公开反馈回路：外部使用者上报问题、提交改进，工具作者据此修正与扩展能力；高 fork/issue/PR 比例表明工具被实际使用并诱发协作，而非仅静态发布。

能力与结果：形成「研究产出 → 可复用工具/参考表 → 社区反馈 → 工具修正与扩展」的闭环，单点发现可沉淀为社区可复用资产，并按性能瓶颈选择工程语言重写核心组件。；GitHub 组织 assetnote 下持续对外输出外部攻击面工具集合；kiterunner 规模化社区采纳（3.3k star、341 fork、41 issue、10 PR）；工具链 Python → Golang/Rust 迁移与 DNS 解析器 Rust 重写；研究 writeup 与开源 PoC 仓库同步发布（Goja RCE 案例，关联基于标题与仓库命名一致，属推断）

置信度：medium；替代解释：工具开源与采纳规模可能受 Assetnote 作为攻击面管理公司的商业方向与组织资源驱动，且 GitHub 组织 assetnote 未公开成员名单，不能据此确认研究对象个人是具体仓库的维护者；工具与 writeup 的同步发布关联在 Goja 案例中基于标题与仓库命名一致，属推断而非一手确认。

证据：ss-pub-2015-websec-weekly, ss-pub-2020-iis-bigquery, ss-timeline-05, ss-community-01, ss-community-02, ss-community-07, ss-dec-02, ss-dec-03

### M4 协作作为成长机制：以具体分工而非人脉/天赋解释成长

起点：2020 年四年回顾文把协作列为成长机制，列出多名同伴（Andre/0xacb、Joel/0xtechnogeek、Naffy/nnwakelam、Sean/seanyeoh、Oscar/tracertea、Huey/hueypeard、Anshuman/anshuman_bh、Rhys/rhyselsmore、Mathias/avlidienbrunn）分工完成 .NET 反序列化、XXE、DNS 爆破优化、JS sourcemap、ATO、WebPageTest RCE 等环节。

练习与反馈：在长期 bug bounty 中以分工协作完成研究环节，并自称「collaboration has been really important when it comes to growth and success in bug bounties」，显式提出「initial triage was done by either party」作为协作成败机制；该协作模式在 2018 年与 Michael Gianarakis 共同创立 Assetnote 时延续为组织分工，收购后扩展为领导全球安全研究团队（团队成员如 Adam Kues 署名 writeup、Michael Gianarakis 具备 DEF CON/Black Hat Asia 等会议履历）。；协作分工中的「initial triage by either party」使任一方初步分诊均可推进研究，互补练习构成反馈；团队 writeup 引用独立研究者（化名 Calif、Hacktron）在全链 PoC 公开前独立复现完整利用链，佐证发现可靠性，构成同行网络对方法的公开反馈与外部验证。

能力与结果：形成以分工与互补分诊驱动研究推进的协作能力，研究产出由个人署名 writeup 演化为团队署名 writeup，团队层面可纳入外部同行复现反馈。；2020 回顾文以具体分工（.NET 反序列化、XXE、DNS 爆破优化、JS sourcemap、ATO、WebPageTest RCE）解释成长，而非人脉/天赋；2018 与 Michael Gianarakis 共同创立 Assetnote，协作模式工程化为组织分工；收购后领导全球研究团队，团队 writeup 引用独立研究者复现佐证发现可靠性

置信度：medium；替代解释：协作分工的成长解释也可能部分反映研究对象所处时期 bug bounty 社区整体协作文化（2016–2020 同期多位研究者公开协作）与 Assetnote 作为组织的资源条件，而非个人独有的成长机制；团队 writeup 由同事署名，研究对象在团队协作中的具体技术贡献未由一手页面单独确认。

证据：ss-pub-2020-120bugs-four-years, ss-timeline-08, ss-dec-02, ss-dec-05, ss-dec-07, ss-community-04, ss-community-05, ss-community-06

## 可迁移与不可迁移

- 可迁移：以可衡量周期与量化指标组织长期研究（120 天/120 bug、1590 天与漏洞类型分布），并周期性对外复盘，形成可核验的反馈—总结—再投入循环；这一做法不依赖个人天赋叙事，可被其他研究者复制。
- 可迁移：把反复出现的侦察/利用需求抽象为可复用工具或参考表（如 A Glossary of Blind SSRF Chains），把单点发现结构化为可检索社区资源，使方法论跨目标可复用。
- 可迁移：把单点漏洞披露与厂商响应态度并行记录（标题中标注「wont fix」、full disclosure 等），把厂商反馈纳入方法论校正回路。
- 可迁移：以「initial triage by either party」的分工与互补分诊推进研究，用具体分工而非人脉/天赋解释成长，使协作成为可复用的研究推进机制。
- 可迁移：按性能瓶颈选择工程语言并重写核心组件（Python → Golang/Rust，DNS 解析器 Rust 重写），把方法论工程化为可扩展工具链。
- 不可直接迁移：Assetnote 作为攻击面管理公司（2018 与 Michael Gianarakis 共同创立）提供的组织资源与产品方向，使研究对象能把个人方法论工程化为产品并获得规模化社区采纳（kiterunner 3.3k star），该条件并非个人可独立复制。
- 不可直接迁移：2025 年 Assetnote 被 Searchlight Cyber 收购后，研究对象任 Chief Security Research Officer 并领导全球研究团队，研究产出渠道由个人博客转向团队研究博客，企业级 RCE 的连续披露依赖团队与公司资源；该团队产出在个人归属层面只能以团队层面可核验，研究对象个人直接贡献未由一手页面确认。
- 不可直接迁移：研究对象所处时期（2013–2026）的 bug bounty 平台激励机制（公开榜单、收益可见、平台分诊）与同期 bug bounty 社区整体协作文化，为量化节奏与协作机制提供了外部条件，并非个人独有。
- 不可直接迁移：2013–2015 年早期单站机会主义型披露对应的厂商赏金项目开放时机与零日出现机会，以及 Uber 攻击面深耕所需的厂商团队反馈条件，具有偶然性与目标特异性，难以完整复制。
- 不可直接迁移：HackerOne 前 50 名排名仅由公司官方页面转述，未一手核对 HackerOne 页面，排名口径、年份与对应报告未知；该外部认可作为成长反馈的条件不可独立核验，不应作为可迁移能力的依据。

## 复核问题

- 字段 stages[1].capability_change：原措辞『同期开始批判性反思 bug bounty 平台治理（The deterioration of unmanaged bug bounties）』；改写方向：将对该批判性反思的陈述移至 Stage 1（与 ss-timeline-04 / 2014-05-31 对应），或改写为『早在 2014 年（Stage 1）即开始批判性反思 bug bounty 平台治理（ss-timeline-04），并在 2021 triage、2022 collaboration、2026 down fall 形成跨十余年的生态反思序列』，避免在 Stage 2（2016–2018）使用『同期开始』导致与 2014 事实矛盾，并避免与 Stage 1 重复引用 ss-timeline-04。
- 字段 mechanisms[1]（M2）repeated_practice 或 alternative_explanation：补充标注『1590 天、$635,387.47 收益与 24 SQLi/22 SSRF/20 IDOR/11 RCE 分布等量化数据均来自研究对象本人回顾文（ss-dec-01/03/04/05），属第一人称自述，未经平台记录或第三方独立核验』，明确数据自述性质。
- 字段 mechanisms[1]（M2）alternative_explanation 或 non_transferable_conditions：补充幸存者偏差标注，说明研究对象为 HackerOne 前 50 名、公司 CSRO 等公开成功案例，失败或沉默研究者的方法论不可观测，量化节奏与协作机制的普适性受样本选择性影响。
- 字段 mechanisms[2]（M3）repeated_practice：原措辞『旗舰侦察工具 kiterunner 截至 2026-09-27 有约 3.3k star、341 fork…』；『旗舰』带产品营销色彩，改写方向：改为『kiterunner 截至 2026-09-27 有约 3.3k star、341 fork、41 个未关闭 issue 与 10 个未关闭 PR，是 assetnote 组织下社区采纳规模最大的侦察工具』或直接删除『旗舰』限定词，以中性表述呈现社区采纳规模。

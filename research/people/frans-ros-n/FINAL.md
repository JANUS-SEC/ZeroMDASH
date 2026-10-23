# Frans Rosén：漏洞研究成长分析

- 擅长领域：Web/云攻击面漏洞
- 独立复核：pass · 90/100

## 成长阶段

- **2018-04-18 至 2018-05-25 · 跨平台漏洞赏金报告工作流自动化**：从手工跨平台（HackerOne/Bugcrowd）报告提交转向以 markdown 模板与 frontmatter 元数据驱动的自动化提交工具 bountyplz（首次提交 2018-04-18，作者 README 述其目标为使报告可'无交互'提交）；2018-05-25 适配平台 CSRF 令牌变化导致的 HTTP 412 错误并加入 TOTP 双因素认证流程，从一次性自动化转向对平台会话与认证机制的适配迭代。（置信度：high）
  - 证据：frans-dec-01, frans-dec-02
- **2018-07-05 · 研究方法公开化（OWASP AppSec EU 2018 演讲）**：据作者自述并于 2018-07-05 在 OWASP AppSec EU 2018 作 'Attacking Modern Web Technologies' 演讲（由 Speaker Deck slide 与 YouTube 视频托管旁证，未经 OWASP 官方议程页核验），研究主题为 postMessage 监听器等现代 Web 通信攻击面；从个人漏洞提交扩展到方法论级的公开分享。（置信度：medium）
  - 证据：frans-dec-03, frans-rosen-targeted-r1-01, frans-rosen-targeted-r1-02
- **2020-05-01 至 2023-11-07 · 研究方法固化为可复用工具并跨年度维护**：将 2018 年演讲中的 postMessage 监听器研究方法固化为 Chrome 扩展 postMessage-tracker 并于 2020-05-01 公开发布（作者 README 自述 'finally released in May 2020'），工具面向追踪短生命周期与交互触发的监听器、解包 Raven/New Relic/Rollbar/Bugsnag/jQuery 等第三方包装器；2023-11-07 加入对 MessagePorts 的支持并修复部分包装器解包问题，体现跨年度持续适配。（置信度：high）
  - 证据：frans-dec-04, frans-dec-05

## 主要成长机制

### 重复性流程的方法化与工具固化

起点：跨平台（HackerOne 与 Bugcrowd）活跃的漏洞赏金猎人身份，提供重复的手工报告提交痛点与多平台扩展需求；同时进行 postMessage 监听器等现代 Web 通信攻击面的研究（据 GitHub 置顶仓库 bountyplz、detectify-cli、postMessage-tracker 与作者 README）。

练习与反馈：识别重复性手工活动并构建可复用工具：将跨平台报告提交抽象为 markdown 模板与 frontmatter 元数据驱动的 bountyplz（2018-04-18）；将 postMessage 监听器手工追踪固化为 Chrome 扩展 postMessage-tracker（2020-05-01）。两例相隔约两年，均把重复性研究或报告活动转为可复用工具。；bountyplz 的可观察反馈来自平台防护行为：CSRF 令牌变化导致 HTTP 412 错误阻断自动化提交，2018-05-25 提交据此适配并加入 TOTP 双因素流程（frans-dec-02 short_quote：'Solved 412-bug due to CSRF-changing, and added 2FA-support (TOTP)'）；该反馈源自平台机制而非同行评审。postMessage-tracker 的反馈来源无可观察证据。

能力与结果：将重复性手工研究或报告活动转为模板或扩展驱动的可复用工具；在自动化被平台防护（CSRF 令牌变化、2FA）阻断时适配平台机制而非放弃。；bountyplz 首次提交 2018-04-18，支持 HackerOne 与 Bugcrowd（frans-dec-01）；bountyplz 2018-05-25 适配 CSRF 412 并加入 TOTP/2FA（frans-dec-02）；postMessage-tracker 2020-05-01 公开发布，面向短生命周期监听器追踪与第三方包装器解包（frans-dec-04）；GitHub 置顶仓库显示其围绕漏洞赏金流程与浏览器侧研究构建可复用工具并公开发布（frans-rosen-deepconv-01）

置信度：medium；替代解释：bountyplz 与 postMessage-tracker 可能是两个独立的一次性工具而非同一可迁移方法；分析仅可见 GitHub 公开且仍维护的仓库，未公开或已弃置的尝试不可见，存在幸存者偏差，可能高估'工具化沉淀'的系统性。

证据：frans-dec-01, frans-dec-02, frans-dec-04, frans-rosen-deepconv-01

### 研究产出的公开化与跨年度维护

起点：postMessage 监听器等现代 Web 通信攻击面的研究方法已成型（作者 README 自述 2018 年已完成演讲内容）。

练习与反馈：将研究方法依次公开化与固化：2018-07-05 OWASP AppSec EU 演讲，2020-05-01 开源 Chrome 扩展，2023-11-07 跨年度维护更新，三个时间点跨越约五年半。；可观察的反馈来源未取得：演讲事实与工具发布、维护事实均可观察，但演讲是否构成反馈渠道、2023 年 MessagePorts 更新是否由用户反馈或包装器失效驱动均无来源支撑。frans-dec-05 的 short_quote 仅说明 'Add support for MessagePorts and fix some of the wrappers being broken'，不含反馈来源。该机制的反馈环节应视为资料缺口而非已证反馈循环。

能力与结果：研究方法的跨年度持续公开化与适配：从一次性演讲固化为可复用开源工具，并对已发布工具进行跨年度维护（适配较新浏览器消息通道 MessagePorts）。；2018-07-05 OWASP AppSec EU 演讲 'Attacking Modern Web Technologies'（据作者自述并由 Speaker Deck slide 与 YouTube 视频托管旁证，未经 OWASP 官方议程页核验；frans-dec-03、frans-rosen-targeted-r1-01、frans-rosen-targeted-r1-02）；2020-05-01 postMessage-tracker 公开发布（frans-dec-04）；2023-11-07 postMessage-tracker 加入 MessagePorts 支持并修复包装器解包（frans-dec-05）

置信度：medium；替代解释：演讲与工具发布之间约两年间隔（2018-07 至 2020-05）内研究方法的状态未取得证据，无法判断是持续迭代还是搁置后重启；2023 年维护更新可能由浏览器 API 变化或个人研究需求驱动，而非系统性的维护习惯。

证据：frans-dec-03, frans-dec-04, frans-dec-05, frans-rosen-targeted-r1-01, frans-rosen-targeted-r1-02

## 可迁移与不可迁移

- 可迁移：将重复性工作流（跨平台报告提交）抽象为模板驱动（markdown 与 frontmatter 元数据）的自动化工具
- 可迁移：在自动化被平台防护（CSRF 令牌变化、2FA）阻断时，适配平台机制而非放弃
- 可迁移：将一次性研究方法（演讲）固化为可复用开源工具，降低他人复现门槛
- 可迁移：对已发布工具进行跨年度维护与适配（如适配较新浏览器消息通道 MessagePorts）
- 不可直接迁移：跨平台（HackerOne 与 Bugcrowd）双平台活跃的赏金猎人身份，提供重复报告提交的工作流痛点与多平台扩展需求
- 不可直接迁移：Detectify API 访问与（推断的）平台或公司关联，支撑 detectify-cli 类工具的使用场景（雇佣关系本身未证实）
- 不可直接迁移：2018 年 OWASP AppSec EU 议程接纳，作为研究方法公开化的外部渠道（具体入选机制未核验）

## 复核问题

- 无关键事实、身份或来源错误。
- 字段 stages[2].capability_change：该阶段 evidence_ids 含 frans-dec-03 与 frans-rosen-targeted-r1-01/02，但 capability_change 仅标注了'作者 README 自述 finally released in May 2020'，未如 stages[1] 那样对依赖 frans-dec-03 的'演讲'环节显式标注'据作者自述并由 Speaker Deck slide 与 YouTube 视频托管旁证，未经 OWASP 官方议程页核验'。原措辞缺少此同源限定。改写方向：在 stages[2].capability_change 引用 2018 演讲处加入与 stages[1] 一致的旁证标注，使两阶段对同一演讲事实的标注口径一致。
- 字段 mechanisms[0].starting_conditions：原措辞'跨平台（HackerOne 与 Bugcrowd）活跃的漏洞赏金猎人身份，提供重复的手工报告提交痛点与多平台扩展需求'。'活跃的'属身份强度断言，证据仅支撑工具支持双平台而非双平台活跃赏金猎人身份本身。改写方向：将'活跃的漏洞赏金猎人身份'改写为'构建并维护面向 HackerOne 与 Bugcrowd 双平台报告提交的自动化工具'等基于可观察行为的表述，避免未被工具存在直接支撑的身份强度断言。
- 字段 mechanisms[0].feedback：原措辞'bountyplz 的可观察反馈来自平台防护行为：CSRF 令牌变化导致 HTTP 412 错误阻断自动化提交，2018-05-25 提交据此适配并加入 TOTP 双因素流程'。'据此适配并加入 TOTP 双因素流程'将 TOTP 加入表述为 412 反馈的直接因果结果，但 commit message 在同一提交中并列'解决 412'与'加入 2FA-support (TOTP)'两项，二者因果紧密度为推断而非直接可核验。改写方向：在'据此适配'处加'推断'限定，或改为'同一次提交（2018-05-25）解决了 CSRF 令牌变化导致的 412 错误并加入 TOTP 双因素支持'，明确两项变更的并列关系而非单一因果链。

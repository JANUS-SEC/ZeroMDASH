# Gareth Heyes：漏洞研究成长分析

- 擅长领域：浏览器/XSS/CSP 漏洞
- 独立复核：pass · 77/100

## 成长阶段

- **约 2006–2016 · 早期向量收集与会议初入**：由散点 XSS 向量产出转向以可复用 cheatsheet 组织知识与进入会议公开发表渠道；该阶段以 lead_only 线索为主，起始年份与产出归属存在缺口与冲突，仅作低置信基线。（置信度：low）
  - 证据：gh-tl-01, gh-tl-02
- **2016–2017 · AngularJS 沙箱与 DOM XSS 基线建立**：在广为部署的 AngularJS 沙箱上建立版本递进式与跨上下文（普通至 DOM）绕过，作为后续方法迁移的基线能力；明确假定沙箱已被绕过为防御立场。（置信度：high）
  - 证据：gh-works-001, gh-works-008, gareth-conv-004, ext-04, gh-dec-01, gh-tl-03, gh-community-05
- **2023 · 受限通道 CSS 盲态外渗**：攻击介质由 JavaScript 执行迁移到仅 CSS 注入条件下的盲态数据外渗，复用同行 @import chaining 工作并自建 Blind CSS Exfiltrator 工具与社区演讲。（置信度：high）
  - 证据：gh-works-002, gh-tl-04, ext-05, gh-dec-02, gareth-conv-006
- **2024 · 邮件地址解析器差分攻击面扩展**：攻击面由浏览器与页面扩展到邮件地址解析器，跨 GitHub、Zendesk、GitLab Enterprise、Joomla 做对比性漏洞挖掘，并配套可复用工具与公开 CTF。（置信度：high）
  - 证据：gh-works-003, gh-tl-05, gh-dec-03, gareth-conv-002, gareth-conv-003
- **2026 · CSS 与邮件线索合流**：将 2023 年 CSS 外渗与 2024 年邮件解析器线索合流到 webmail sanitizer 绕过与实时 CSS keylogger，进入 Black Hat USA 2026 议程。（置信度：high）
  - 证据：gh-works-004, gh-tl-06, gh-dec-04, gareth-conv-001, gareth-conv-005, ext-01, ext-02, ext-06
- **跨阶段（2007–2026） · 工具与参考资料持续建设**：围绕 XSS 与 CSS 持续构建可复用工具与参考资料（Hackvertor BApp 扩展、PortSwigger XSS Cheat Sheet、《JavaScript for Hackers》），形成支撑日常研究的基础设施；多项产出无明确起始日期，机构与个人贡献难以分离。（置信度：medium）
  - 证据：gh-works-005, gh-works-006, gh-works-007, gh-works-008, gh-tl-07, gh-tl-08, gh-community-01, gh-community-03, gh-dec-05

## 主要成长机制

### 失败包容性发表与同行共享回路

起点：自 2017 年起在 PortSwigger 担任 Researcher，从事新 XSS 向量与 Web 攻击技术研究；研究含随机性与反复失败，本人自述曾想完全放弃研究，突破依赖在自身邮箱粘贴允许的特殊字符这一低门槛试探。

练习与反馈：把不奏效的技术路径随成功路径一并写入公开 writeup（2017 AngularJS 全开发过程含无效技术），并将研究配套为可复现材料（GitHub 源码、会议幻灯片、工具脚本、CTF）公开发布。；通过 Black Hat、DEF CON、CSS Cafe、AppSec EU、BSides Manchester 会议采纳与 BApp Store 接受标准评估取得外部反馈；本人自述将其能力获得归因于与同行持续 20 年的 sharing and learning。

能力与结果：将试错过程本身作为可分享产出，形成发表、外部社交渠道分发、工具迭代的反馈回路，而非依赖站内评论互动。；2017 AngularJS 沙箱逃逸开发全过程公开，含未奏效技术；2023 Blind CSS Exfiltrator 工具与 CSS Cafe 幻灯片公开；2024 邮件研究配套 Hackvertor tags、Turbo Intruder script、Punycode fuzzer 与 Web Security Academy CTF；2026 webmail 研究配套 Black Hat USA 2026 幻灯片与 GitHub 源码

置信度：high；替代解释：PortSwigger 作为商业安全厂商，其编辑制度与 BApp Store、会议发表渠道本身要求可发表、可复现的产出，该回路可部分由组织激励解释而非纯个人选择；本人 sharing and learning 的自述属事后归因，无法排除记忆重构。

证据：gareth-conv-001, gareth-conv-002, gareth-conv-004, gareth-conv-005, gareth-conv-006, gh-community-01, gh-community-02, ext-01, ext-02, ext-04, gh-tl-05

### 可复用工具与向量库建设

起点：早期即以向量集合（HTML5 与 XSS cheatsheet）组织知识，但 HTML5 Security Cheatsheet 创建归属在一手页面未证实且与 Cure53 关联冲突；PortSwigger 雇主提供 Burp 与 BApp 生态分发渠道。

练习与反馈：跨 19 年个人站 Research Gallery（2007 至 2026）与多工具长期并存维护（Hackvertor、Shazzer、DOM Invader、Taborator、SSPP Scanner、XSS labs）；维护长期演进的 PortSwigger XSS Cheat Sheet（2026 年 9 月仍标注 regularly updated）与 Hackvertor BApp 扩展（2026-09-17 仍更新）。；BApp Store 接受标准评估与社区使用构成外部质量约束；XSS Cheat Sheet 被机构定位为社区广泛使用资源，自述与外部描述一致，社区定位稳定。

能力与结果：以标签式编码、解码与转换工具支撑 XSS 向量与 payload 构造，形成支撑日常研究的固定基础设施。；Hackvertor 被反复用作研究配套工具（2024 邮件研究 Hackvertor tags 与 Turbo Intruder script）；XSS Cheat Sheet 作为持续维护的向量库存在；方法论成书《JavaScript for Hackers》

置信度：medium；替代解释：Burp 与 BApp 生态为 PortSwigger 员工提供工具分发的组织激励，工具建设可部分由岗位结构解释；XSS Cheat Sheet 与 Hackvertor 的长期维护亦符合机构产品定位而非纯个人习惯。

证据：gh-works-005, gh-works-006, gh-works-007, gh-works-008, gh-tl-01, gh-tl-07, gh-tl-08, gh-community-01, gh-community-03, gh-community-05, gh-dec-05

### 跨解析器与跨上下文差分分析

起点：2017 年在 AngularJS 沙箱上以版本递进式与跨上下文（普通至 DOM）绕过建立差分基线，并明确在 Mario Heiderich 首个绕过基础上推进。

练习与反馈：跨框架版本逐个击破（1.3.0、1.2.27 至 1.3.20、1.4、1.5.0 至 1.5.8、1.5.11 CSP 绕过）；2024 跨邮件地址解析器（UUCP 与 source route、Unicode 溢出、RFC 2047 encoded-word、畸形 Punycode）对比 GitHub、Zendesk、GitLab Enterprise、Joomla；2026 跨 webmail sanitizer（Yahoo Mail、AOL Mail、Fastmail、ProtonMail、Gmail、Outlook）。；厂商实际漏洞与 RCE（Joomla 达 RCE）与会议采纳（Black Hat、DEF CON、Black Hat USA 2026）提供可核验结果反馈。

能力与结果：以同一原语在不同解析器或版本上的行为差分作为发现绕过路径的通用方法，并可跨解析器域迁移。；2017 AngularJS DOM 沙箱逃逸；2024 邮件解析器访问控制绕过与 RCE；2026 webmail CSS sanitizer 绕过与实时 CSS keylogger

置信度：high；替代解释：发表序列存在幸存者偏差，仅成功迁移的研究可见，未迁移的尝试未被记录；跨解析器差分是 XSS 与 Web 安全领域的通用方法，其区分度部分依赖所覆盖解析器的广度而非方法本身。

证据：gh-works-001, gh-works-003, gh-works-004, gh-tl-03, gh-tl-05, gh-tl-06, gh-dec-01, gh-dec-03, gh-dec-04, ext-04, ext-06

### 同行知识复用与迭代改写

起点：处于可识别的 XSS 与 Web 安全同伴网络（个人站 Inspiration 页列出 Mario Heiderich、Masato Kinugawa、Michal Zalewski 等），同事 James Kettle 提供方向引导与工具供给（Turbo Intruder、测试用 GitLab 服务器）。

练习与反馈：在同行已公开技术基础上迭代改写并公开致谢：2017 在 Mario Heiderich 首个绕过基础上推进版本；2023 以 Pepe Vila 的 @import chaining 脚本为 basis 改写为对未知结构的外渗，致谢 d0nut 与 Pepe Vila；2024 致谢 James Kettle 工具与方向。；同行脚本可用性、测试环境与方向建议构成弱导师与强同伴反馈；将每次失败表述为 learning process 而非纯负面结果。

能力与结果：将社区既有成果作为起点重构而非从零创造，缩短从受限原型到可用工具的迭代周期。；Blind CSS Exfiltrator 由 Pepe Vila 脚本 morph 而来；邮件研究在同事工具与测试环境支持下完成

置信度：medium；替代解释：PortSwigger 团队结构本身提供同事协作与工具共享，sharing and learning 可由团队结构解释；致谢行为也可能部分出于发表规范而非真实的迭代依赖，同伴对研究方向的具体反向影响仅能 inferred。

证据：gh-community-04, gh-tl-03, gh-tl-04, gh-tl-05, gareth-conv-002, gareth-conv-003, ext-05

## 可迁移与不可迁移

- 可迁移：将不奏效的技术路径随成功路径一并公开记录，把试错过程本身作为可分享产出。
- 可迁移：把研究配套为可复现材料（源码、幻灯片、工具脚本、CTF）以接受同行复核与沿用。
- 可迁移：以跨解析器与跨版本行为差分作为发现绕过路径的通用方法，并在不同解析器域间迁移。
- 可迁移：在同行已公开技术基础上迭代改写并明确致谢，以既有成果为起点缩短迭代周期。
- 可迁移：维护长期演进的向量库与参考资料作为研究基础设施。
- 不可直接迁移：PortSwigger Researcher 岗位及其 Burp 与 BApp 生态分发渠道与编辑支持，属于特定雇主资源。
- 不可直接迁移：与 James Kettle 等同事的弱导师与强同伴关系，及 PortSwigger 内部测试环境（GitLab 服务器、Turbo Intruder）。
- 不可直接迁移：以 XSS 与 CSS 为长期主线的机构定位，及 AngularJS 沙箱破坏者的既有声誉，构成路径依赖。
- 不可直接迁移：跨 19 年持续在线存在（个人站 Research Gallery 2007 至 2026）与多平台账号积累，需长期稳定的研究岗位支撑。
- 不可直接迁移：2026 年 AI 兴起的外部技术环境，为其分享 AI 暂时无法发现之物的动机提供特定时代条件。

## 复核问题

- stages[0]（约 2006–2016）evidence_ids 引用 gh-tl-01 与 gh-tl-02 均为 lead_only，且 gh-tl-01 存在 Cure53 归属冲突。建议在 capability_change 中明确该阶段无一手抓取来源支撑，仅作为推断基线，避免与 high confidence 阶段并列时低估缺口影响。
- mechanism[0].observed_outcomes 中 '2024 邮件研究配套 Hackvertor tags、Turbo Intruder script、Punycode fuzzer 与 Web Security Academy CTF' 由 gh-tl-05 支撑（documented），但 mechanism[0] 的核心是「失败包容性发表与同行共享回路」，该产出物列表与机制主题（试错过程公开化）关联较弱，建议补充说明这些配套产出如何体现「把试错过程作为可分享产出」，或在 evidence_ids 中明确对应。
- tensions 中「与系统化调试者形象存在张力」的「系统化调试者形象」并非综合结论自创的判断对象，而是复核视角引入的对照框架；如保留该 tension，建议改为「本人自述的随机性与低门槛试探与其长期稳定的研究产出之间存在需要解释的张力」，以避免引入未经定义的形象概念。

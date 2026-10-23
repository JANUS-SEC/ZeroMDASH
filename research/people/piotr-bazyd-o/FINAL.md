# Piotr Bazydło：漏洞研究成长分析

- 擅长领域：Microsoft 企业软件漏洞
- 独立复核：pass · 90/100

## 成长阶段

- **2021 · 早期独立公开披露习惯的建立**：具备将单个产品（MDaemon 邮件服务器）的多个漏洞整理为以 CVE 编号命名的公开通告仓库的能力，形成可被社区引用的公开披露物；该阶段 period 仅由 MDaemon 通告（CVE-2021-27180~27183，报告 2020-12-15，补丁 2021-01-12）锚定，XStream/ysoserial 仓库日期未核验，不据以推断该年份。（置信度：high）
  - 证据：PB-community-01, pb-targeted-r1-001
- **2022-2023 · ZDI 机构署名渠道与 Exchange 远程攻击面产出**：研究产出经 ZDI 机构署名渠道发布（ZDI-22-1019，2022-07-15 公开，researcher 字段署名 Piotr Bazydlo (@chudypb)），目标扩展至 Microsoft Exchange 远程攻击面四零日（ZDI-23-1578~1581，2023-09 报告、2023-11 公开，均为认证后；含经 ChainedSerializationBinder 的反序列化 RCE 与三类 SSRF/URI validation），形成机构级协调披露时间线。（置信度：high）
  - 证据：ext-zdi-advisory-ZDI-22-1019, ext-zdi-exchange-zerosecurity-2023, pb-targeted-r1-002
- **2024 · 补丁绕过链方法学公开与目标广度扩展**：将多个 Exchange 补丁绕过串联为持续 RCE 链并向同行社区公开方法学（OffensiveCon 2024 “Half Measures and Full Compromise”，列出 CVE-2023-21529/36745/36756/36744 与 gadget searching）；同年披露 SolarWinds Access Rights Manager 认证前目录穿越（ZDI-24-1020，CVE-2024-28992，deleteTransferFile），目标广度延伸至 SolarWinds 等其他企业管理软件；ZDI 作者页线索另指向 Windows SmartScreen/RDLicensing 等 OS 组件（pb-works-002，reported 级未逐条核验）。（置信度：medium）
  - 证据：ext-offensivecon-exchange-talk-content-2024, ext-zdi-employer-role-offensivecon-2024, pb-works-001, pb-targeted-r1-002
- **2026 · 职位流动与累积产出自述**：个人站点自述当前职位为 watchTowr Principal Vulnerability Researcher，过往为 Trend Micro Zero Day Initiative 漏洞研究员与渗透测试员/网络流量分析员，并列出多项演讲（BlackHat EU 2025、WarCon 2024、OffensiveCon 2024、Hexacon 2023、DefCamp 2021、Confidence 2018）与 Exchange 17 个 CVE（含 5 个 RCE）、ysoserial.net 贡献等累积产出；该阶段为 inferred 级自述，无独立第三方逐条核验。（置信度：low）
  - 证据：ext-self-roles-personal-site, pb-targeted-r1-004

## 主要成长机制

### 以 CVE 编号化公开通告为核心的协调披露习惯

起点：2021 年起具备将漏洞整理为命名仓库并以 CVE 编号公开的能力（GitHub MDaemon-Advisories，CVE-2021-27180~27183）。

练习与反馈：2021 年 MDaemon 通告、2022 年 ZDI-22-1019、2023 年 Exchange 四零日（ZDI-23-1578~1581，2023-09 报告、2023-11 公开）、2024 年 SolarWinds（ZDI-24-1020，2024-07-29），跨年度重复以编号化公开通告形式披露漏洞。；ZDI 机构在公告 researcher 字段署名 Piotr Bazydlo (@chudypb)（ZDI-22-1019）；第三方媒体（ZeroSecurity）将 Exchange 四零日归属到本人与雇主；GitHub profile 显示 Pull Shark 与 security advisory credit 成就（合审者与项目未知）。

能力与结果：形成可被第三方引用的公开披露物与可核验的协调披露时间线（报告日—公开日—补丁日）。；GitHub MDaemon-Advisories 仓库公开 CVE-2021-27180~27183 通告；ZDI-22-1019 (2022-07-15 公开) 署名 Piotr Bazydlo (@chudypb)；Exchange 四零日 ZDI-23-1578~1581 (2023-09 报告, 2023-11 公开)；SolarWinds ARM ZDI-24-1020 (2024-07-29, CVE-2024-28992, CVSS 8.6)

置信度：high；替代解释：ZDI 机构流程本身要求编号化披露，公开通告行为可能更多反映 ZDI 披露政策而非个人特有习惯；GitHub Pull Shark 仅证明存在被合并的拉取请求，合审者与对应项目未知，不能据以证明稳定的导师/同伴反馈回路。

证据：PB-community-01, ext-zdi-advisory-ZDI-22-1019, ext-zdi-exchange-zerosecurity-2023, pb-works-001, PB-community-03

### 企业级软件高权限服务目标的持续深挖与入口缺陷定位

起点：2021 年 MDaemon 邮件服务器漏洞链（Reflected XSS、CSRF Token Fixation、Iframe injection、RCE，README 自述可链式实现 RCE/账户接管但需用户交互）。

练习与反馈：MDaemon（2021）→ Exchange 远程攻击面（2023，认证后反序列化 RCE 与 SSRF/URI validation）→ SolarWinds Access Rights Manager（2024，认证前 deleteTransferFile 目录穿越），跨目标重复对带高权限服务账户的企业管理软件入口进行定位。；ZDI 公告逐条标注缺陷类别与认证要求（ZDI-24-1020 “lack of proper validation of a user-supplied path prior to using it in file operations”；ZDI-23-1578~1581 “Authentication is required for exploitation”）；OffensiveCon 2024 会议平台对 Exchange 补丁绕过链给予演讲背书。

能力与结果：对企业管理软件入口（认证前/认证后、文件路径/URI/反序列化入口）按缺陷类别进行类别化定位与链式利用。；SolarWinds ARM deleteTransferFile 认证前目录穿越 (ZDI-24-1020, CVSS 8.6)；Exchange 四零日 ZDI-23-1578~1581 (认证后反序列化 RCE + SSRF/URI validation)；MDaemon CVE-2021-27180~27183 链式 RCE/账户接管 (需用户交互)；OffensiveCon 2024 Exchange 补丁绕过链 (CVE-2023-21529/36745/36756/36744)

置信度：medium；替代解释：路径校验缺失框架仅 SolarWinds 一例支撑，认证前可触达亦仅 SolarWinds 支撑（RR1/RR5）；跨 MDaemon/Exchange/SolarWinds 的“高权限服务入口”归纳受目标类别异质（XSS/CSRF vs 反序列化/SSRF vs 目录穿越）限制，可能更多反映 ZDI 提交流入的机构样本分布而非个人稳定的方法论；目标广度扩展中 SmartScreen/RDLicensing 仅为 reported 级未经一手核验。

证据：pb-targeted-r1-001, pb-targeted-r1-002, pb-works-001, ext-zdi-exchange-zerosecurity-2023, ext-offensivecon-exchange-talk-content-2024

### 反序列化/序列化 gadget 研究与工具生态参与

起点：GitHub XStream-Gadgets 仓库（README 原文 “This repo contains several ysoserial gadgets, transformed into the XStream serialization format. Original repo: https://github.com/frohoff/ysoserial”，日期未核验）与 ysoserial.net fork，方向为 .NET/Java 反序列化。

练习与反馈：XStream gadget 移植、ysoserial.net fork 与贡献（个人站点自述 “.NET deserialization/serialization research and commits to ysoserial.net (new gadgets and plugins)”）、Exchange 反序列化 RCE（ZDI-23-1578，经 ChainedSerializationBinder，SYSTEM 上下文）、OffensiveCon 2024 Exchange gadget 搜索方法学公开。；个人站点自述 ysoserial.net 贡献（依据 pb-targeted-r1-004，status=inferred，自述一手但无独立第三方核验，不上升为 documented）；OffensiveCon 2024 会议平台对 gadget 搜索方法学给予演讲背书。

能力与结果：将 gadget 研究从既有工具移植推进到漏洞利用链构建与公开方法学输出。；XStream-Gadgets 仓库 (ported from frohoff/ysoserial, 日期未核验)；ysoserial.net 贡献自述 (new gadgets and plugins, inferred 级)；Exchange 反序列化 RCE ZDI-23-1578 (ChainedSerializationBinder, SYSTEM 上下文)；OffensiveCon 2024 “Half Measures and Full Compromise” gadget searching 方法学

置信度：medium；替代解释：ysoserial.net 贡献为个人自述（inferred），无独立第三方核验，可能高估个人在工具生态中的角色；XStream-Gadgets 为移植既有工具（frohoff/ysoserial），原创性有限；Exchange 反序列化 RCE 与 gadget 搜索方法学的关联基于缺陷类别与会议主题相邻，非直接因果证据；XStream/ysoserial 仓库日期未核验，无法据以推断其反序列化研究的起始时间。

证据：PB-community-02, pb-targeted-r1-003, pb-targeted-r1-004, ext-self-roles-personal-site, ext-zdi-exchange-zerosecurity-2023, ext-offensivecon-exchange-talk-content-2024

## 可迁移与不可迁移

- 可迁移：将单个产品的多个漏洞整理为以 CVE 编号命名的公开通告仓库（MDaemon-Advisories 模式），便于社区引用与复用。
- 可迁移：对同一目标产品（Exchange）跨补丁版本持续跟踪，将多个补丁绕过串联为长期 RCE 链并公开方法学。
- 可迁移：fork 与移植既有工具（ysoserial→XStream-Gadgets、ysoserial.net）参与反序列化工具生态。
- 可迁移：按 ZDI 与厂商协调流程披露（2023-09 报告、2023-11 公开），保留可核验的协调披露时间线。
- 不可直接迁移：ZDI/Trend Micro 机构职位带来的漏洞样本流入与机构署名渠道（ZDI-XX-XXXX 编号、researcher 字段署名），个人难以独立复现。
- 不可直接迁移：OffensiveCon 2024 职位描述所反映的机构级根因分析工作量（“hundreds of vulnerabilities submitted to the ZDI program”）属机构职能，非个人可观测实践。
- 不可直接迁移：watchTowr Principal Vulnerability Researcher 职位变动（个人站点自述，inferred）依赖雇主流动，非个人方法论可复制。
- 不可直接迁移：Pull Shark/security advisory credit 等平台成就依赖 GitHub 平台机制与项目维护者审阅，非个人方法。

## 复核问题

- 机制 M2 repeated_practice：将'跨目标重复对带高权限服务账户的企业管理软件入口进行定位'中 MDaemon 的'高权限服务账户'属性改为分级表述，原措辞'带高权限服务账户的企业管理软件入口'应改写为'SolarWinds（高权限服务账户，pb-works-001 显式佐证）、Exchange（SYSTEM 上下文反序列化 RCE，pb-targeted-r1-002 推断）、MDaemon（邮件服务器服务上下文，服务账户权限未在已抓取证据中记录）'，避免将仅一例显式佐证的属性外推至三目标。
- Stage 3 capability_change：原措辞'目标广度延伸至 SolarWinds 等其他企业管理软件'应改写为'目标广度延伸至 SolarWinds Access Rights Manager（ZDI-24-1020，已核验）'，删除'等'对未核验广度的暗示；SmartScreen/RDLicensing 为 OS 组件且为 reported 级（pb-works-002），不并入企业管理软件类别。

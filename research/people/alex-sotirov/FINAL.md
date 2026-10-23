# Alex Sotirov：漏洞研究成长分析

- 擅长领域：浏览器与平台漏洞
- 独立复核：pass · 84/100

## 成长阶段

- **2007-03 · Determina 时期：向协调机构与国家漏洞数据库报告客户端栈溢出漏洞**：Alexander Sotirov（时属 Determina）将一项 Windows 客户端栈缓冲区溢出漏洞报告至 CERT/CC 并进入 NVD，形成「报告-编号-评级」可核验产出链。该漏洞位于 Windows 处理 Resource Interchange File Format（RIFF）格式动画光标文件（扩展名 .ani/.cur/.ico）的代码中；按来源逐字事实性表述，动画光标文件「are parsed when the containing folder is opened or it is used as a cursor」，且「Internet Explorer can process animated cursor files in HTML documents, so web pages and HTML email messages can also trigger this vulnerability」，并指出「any Windows application may call the vulnerable code to process animated cursor files」。NVD 将该漏洞编号 CVE-2007-0038，CVSS v2 基础分 9.3（HIGH），影响 Windows 2000 SP4 至 Vista 多个版本，记载漏洞「originally demonstrated using Internet Explorer 6 and 7」。注：本条能力变化仅基于 2007-03 单一公开事件，不覆盖更长周期。（置信度：medium）
  - 证据：as_rev1_e01, as_works_02
- **2008-12 至 2009 · 25C3 MD5 chosen-prefix collision rogue CA 证书演示与厂商响应阶段**：作为七人研究团队成员参与 2008-12-30 第 25 届 Chaos Communication Congress（柏林）的 MD5 chosen-prefix collision 与 rogue CA 证书演示，团队分工覆盖理论碰撞构造（由 Marc Stevens/CWI Amsterdam、Arjen Lenstra/LACAL EPFL、Dag Arne Osvik/LACAL EPFL、Benne de Weger/TU/e 承担）、算力调度（超过 200 台 PS3、约 18 小时 birthday search，由 EPFL DIT 与瑞士国家科学基金资助）与浏览器/证书侧演示整合。Sotirov 在来源中定位为「Independent security researcher, New York, USA」，非 chosen-prefix collision 构造者或密码学工程化方法论作者。该工作后续获 Crypto 2009 最佳论文奖（2009-06-03 公布）与 Top Ten Web Hacking Techniques of 2009 第一（2010-01-12 公布）。注：本条能力变化仅基于 2008-12 至 2009 单一公开事件，不覆盖更长周期。（置信度：medium）
  - 证据：asc-001, asc-002, asc-003, asc-004, as_rev1_e02

## 主要成长机制

### 向协调机构与国家漏洞数据库报告并形成官方响应闭环

起点：2007 年时属 Determina，研究方向为 Windows 客户端与浏览器漏洞；Determina 提供公司平台使报告可署名「of Determina」。

练习与反馈：2007-03 将动画光标栈缓冲区溢出漏洞报告至 CERT/CC（VU#191609），随后进入 NVD（CVE-2007-0038，由 secure@microsoft.com 分配）；2008-12 在 25C3 演示前与浏览器厂商及证书机构进行披露前沟通，演示后触发 Verisign/RapidSSL、Microsoft（安全公告 961509）、Mozilla、TC TrustCenter、RSA、US-CERT（VU#836068）、Cisco 的批量响应。两次报告均经协调机构或国家数据库独立收录。；CERT/CC 漏洞说明 VU#191609 与 NVD CVE-2007-0038 的官方收录与高严重度评级；2008 年厂商响应中 Verisign/RapidSSL 称「We applaud security research of this sort」，US-CERT 建议「Do not use the MD5 algorithm」，构成可核验的外部响应反馈。

能力与结果：形成将单项漏洞报告经协调机构转化为可被官方数据库收录、并触发厂商批量响应的协作披露能力，而非独立承担全部技术核心。；CVE-2007-0038 被赋予 CVSS v2 基础分 9.3（HIGH），记载漏洞「originally demonstrated using Internet Explorer 6 and 7」，影响 Windows 2000 SP4 至 Vista 多个版本。；VU#191609 正文中以「This vulnerability was reported by Alexander Sotirov of Determina.」署名，文档作者为 Jeff Gennari 与 Will Dormann。；25C3 演示后 Verisign/RapidSSL 停用 MD5 并提供免费替换证书；Microsoft 发布安全公告 961509；Mozilla（Johnathan Nightingale）、TC TrustCenter、RSA（Sam Curry）、US-CERT（VU#836068）、Cisco 发布响应；US-CERT 建议 Do not use the MD5 algorithm。；MD5 rogue CA 工作获 Crypto 2009 最佳论文奖与 Top Ten Web Hacking Techniques of 2009 第一。

置信度：medium；替代解释：两次报告经协调机构收录与厂商响应，亦可由「Determina 公司与 25C3 团队整体的披露流程」驱动，而非 Sotirov 个人反复实践所致；CERT/CC 与 NVD 的收录反映的是漏洞本身的可核验性，未必反映个人报告技巧的成长。2007-03 与 2008-12 两次事件分属不同团队（Determina 与七人团队），协作披露流程的相似性部分来自协调机构惯例，难以单独归因于个人。

证据：as_rev1_e01, as_works_02, asc-002, as_rev1_e02

### 在跨机构/跨学科团队中定位自身分工并整合外部算力/经费资源

起点：2008 年以「Independent security researcher, New York, USA」身份进入由 CWI Amsterdam、EPFL LACAL、TU/e 等机构成员组成的七人研究团队，团队覆盖密码学理论与浏览器/证书安全两个学科。

练习与反馈：在 25C3 MD5 chosen-prefix collision rogue CA 证书演示项目中，团队按学科与机构分工：理论碰撞构造与密码学核心由 Marc Stevens（CWI Amsterdam）、Arjen Lenstra（LACAL EPFL）、Dag Arne Osvik（LACAL EPFL）、Benne de Weger（TU/e）承担；算力由超过 200 台 PS3 与约 18 小时 birthday search 提供，由 EPFL DIT 与瑞士国家科学基金资助；演示工具在其基础上改造自 Moxie Marlinspike 的 sslsniff。Sotirov 在来源中定位为团队成员。；学术与社区层面双重认可：Crypto 2009 最佳论文奖（2009-06-03 公布）、Top Ten Web Hacking Techniques of 2009 第一（2010-01-12 公布），构成对协作研究质量的外部反馈。

能力与结果：形成在跨机构、跨学科（密码学 + 浏览器/证书安全）团队中定位自身分工并整合外部算力/经费资源的能力，而非独立承担全部技术核心。；25C3 演示实现实用化 chosen-prefix MD5 碰撞并构造可被浏览器信任的 rogue CA 证书。；演示后触发上述厂商批量响应。；该工作获 Crypto 2009 最佳论文奖与 Top Ten Web Hacking Techniques of 2009 第一。

置信度：medium；替代解释：Sotirov 能进入该团队，可能主要由既有同伴网络（浏览器/证书安全方向）与团队对其浏览器侧能力的需要所致，而非其个人在跨机构协作方法论上的反复练习；理论碰撞核心归属 Stevens/Lenstra/Osvik/de Weger，算力与经费来自 EPFL DIT 与瑞士国家科学基金而非个人争取，故该机制中可归因于个人的成分有限。25C3 为单一观测实例，尚不足以证明该能力经多次重复形成。

证据：asc-001, asc-004, as_rev1_e02

## 可迁移与不可迁移

- 可迁移：将单项漏洞报告经协调机构（CERT/CC）转化为国家漏洞数据库（NVD）收录条目，并在披露前与厂商沟通、披露后追踪批量响应，形成可核验的协作披露产出链。
- 可迁移：在跨机构、跨学科团队中按学科与机构明确分工，将自身定位为浏览器/证书侧整合者，理论核心交由密码学机构成员，算力与经费交由所在机构与基金承担。
- 不可直接迁移：Determina 提供的公司平台使 2007 年报告得以署名「of Determina」并被 NVD 引用 Determina 公告；该平台属当时雇主条件，非个人可迁移要素。
- 不可直接迁移：25C3 团队中 CWI Amsterdam、EPFL LACAL、TU/e 等机构的密码学研究者网络及 PS3 集群算力（由 EPFL DIT 与瑞士国家科学基金资助）属团队与机构资源，非个人具备或可迁移的条件。
- 不可直接迁移：2007-2008 年 Windows 2000 SP4 至 Vista 与 IE 6/7 的客户端/浏览器技术条件、以及 MD5 在证书体系中尚被采用的历史条件，属特定时期外部环境，不可迁移至后续缓解已普遍部署的时期。

## 复核问题

- 无关键事实、身份或来源错误。身份经三个 verified_in_run 来源交叉印证：CERT/CC VU#191609 正文署名「Alexander Sotirov of Determina」（2007-03-29，文档作者 Jeff Gennari 与 Will Dormann）、marc-stevens.nl HashClash 页逐字列「Alexander Sotirov — Independent security researcher, New York, USA (http://www.phreedom.org/)」（2008-12-30）、NVD CVE-2007-0038 引用 Determina 安全公告 URL。三者对人名、机构归属与研究方向一致，无同名歧义残留。
- stages[0].capability_change 与 as_works_02：将「originally demonstrated using Internet Explorer 6 and 7」改为「据 NVD CVE-2007-0038 描述，as originally demonstrated using Internet Explorer 6 and 7」，补回句首「as」并明确短语出处为 NVD（非 VU#191609），使引文逐字且来源标注准确。
- mechanisms[0].validation_tests：将 ["repeated", "generative"] 中的 repeated 依据限定为「两次事件均经协调机构/国家数据库收录」这一机构层面重复，而非 Sotirov 个人报告技巧的重复；或在 alternative_explanation 中补充说明 VU#836068 的 US-CERT 报告者署名本轮未逐字核验，个人报告层面的 repeated 归因证据弱于机构收录层面的重复，避免将团队披露后的 US-CERT 响应直接归为 Sotirov 个人重复实例。
- stages[1].capability_change 或 mechanisms[1].observed_outcomes：在引用 Crypto 2009 最佳论文奖时，补充标注获奖论文核心作者为 Stevens/Lenstra/de Weger（依据 marc-stevens.nl 逐字记录），明确奖项归属团队论文而非 Sotirov 个人，进一步约束声誉传导。
- tensions 或 biases：增补一条幸存者偏差声明，说明以 NVD/CERT/US-CERT/学术奖项收录的公开事件为能力证据，可能高估 Sotirov 在已收录事件中的可见度、低估未被收录工作（Heap Feng Shui、Bypassing Browser Memory Protections）对其实际能力曲线的影响，以使能力分布失真风险在报告中显式可见。

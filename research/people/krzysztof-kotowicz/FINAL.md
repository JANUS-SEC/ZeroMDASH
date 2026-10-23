# Krzysztof Kotowicz：漏洞研究成长分析

- 擅长领域：Web/浏览器/供应链漏洞
- 独立复核：pass · 85/100

## 成长阶段

- **约 2000–2007 · 教育背景与早期公开代码起点**：据 LinkedIn 公开预览自述，在 Krakow University of Economics 接受教育（2000–2004），并自 2007 年起在 GitHub.com 发布个人项目代码。该时间线为 LinkedIn 自述，教育背景与后续 Web 安全研究方向无直接证据关联，仅可作为早期公开代码习惯的弱时间锚点。（置信度：low）
  - 证据：kk-tl-01, kk-tl-02, kk-rev1-01-linkedin-public-preview
- **约 2011–2012 · 工具框架化与国际主流会议公开发表**：自述为 SecuRing IT security consultant，研究焦点为 client side security、HTML5、UI redressing、Chrome extensions，已在 Black Hat、BruCON、CONFidence 等会议演讲。2011 年起通过 Facebook White Hat 与 Google Security Hall of Fame 建立厂商漏洞披露记录。Black Hat USA 2012 以 'Advanced Chrome Extension Exploitation: Leveraging API powers for Better Evil' 为题进行培训，并配套发布白皮书与可复用工具 xsschef（Chrome extension Exploitation Framework）；Chrome 扩展攻击研究在 WhiteHat Security 'Top Ten Web Hacking Techniques of 2012' 评选中位列第 3。工具建设显式标注灵感来源（Mosquito 标注 'Inspired by MalaRIA by Erlend Oftedal'、'BeEF tunneling proxy by @antisnatchor'）。（置信度：medium）
  - 证据：kk-conv-03, kk-conv-04, kk-tl-03, kk-tl-04, kk-tl-05, kk-decisions-01, kk-rev1-01-linkedin-public-preview
- **约 2013–2014 · 厂商安全工程与协议级协同披露**：自述岗位由 SecuRing/Cure53 渗透测试转入 Google Information Security Engineer（Hack in Paris 2014 演讲第 2 页），研究兴趣含 HTML5、UI redressing、浏览器扩展、加密。2014-10-14 与 Bodo Möller、Thai Duong 共同披露 POODLE 攻击（CVE-2014-3566），经 Google Online Security Blog 与 OpenSSL advisory 协同公开，披露建立在既有 TLS CBC 填充预言研究谱系之上。据搜索摘要转述，约 2013–2014 在 Black Hat US/EU 发表演讲（Pixel Perfect: Fingerprinting Canvas in HTML5、The Million Browser Botnet），议程页于 2026-09-27 重新抓取仍返回 HTTP 403，SlideShare deck 列表未印证该两场标题，故仅作转述、未一手核验。（置信度：medium）
  - 证据：kk-conv-01, kk-conv-02, kk-tl-06, kk-tl-07, kk-tl-08, kk-community-001, kk-community-002, kk-rev1-02-slideshare-decklist
- **约 2016–2018 · XSS 缓解机制结构性分析与标准提案**：据 LinkedIn 自述，2016 年发表 Content Sniffing with Comma Chameleon 研究，将 JSON/CSV 注入经 PDF 内容嗅探转化为 XSS 等价危害；2017 年在 ACM CCS 发表 Script Gadgets: Breaking XSS Mitigations via Code Reuse，展示现代 JavaScript 框架中的脚本器件可绕过既有 XSS 缓解；约 2017-06 启动 Trusted Types 标准提案（W3C Web 平台标准，使 DOM XSS 防护内建于浏览器），该启动日期为 LinkedIn projects 栏目自述（Trusted Types 'Juni 2017–Heute'），W3C 一手页面仅确认 2026-06-23 Working Draft 编辑署名，未一手核验启动日期。上述四项学术与标准成果的出版方一手页面（ACM DL 403、DBLP bot 阻断、IEEE Xplore、PoC||GTFO archive、web.archive.org 工具拒绝）均抓取失败，仅 LinkedIn 自述文本存在，出版方一手未核验。（置信度：low）
  - 证据：kk-tl-09, kk-tl-10, kk-tl-11, kk-conv-05, kk-rev1-01-linkedin-public-preview
- **约 2020–2026 · 标准生产验证与编辑职责**：据 LinkedIn 自述，2020 年与 Lukas Weichselbaum 共同发表关于 Safari 智能跟踪防护（ITP）信息泄露的研究，将研究对象扩展到浏览器隐私机制的非预期信息泄露；2021 年在 IEEE EuroS&P Workshops 发表 Adopting Trusted Types in Production Web Frameworks（与 Pei Wang、Bjarki Ágúst Guðmundsson 合著），以案例研究形式将自身主导的标准提案在生产框架中验证；当前作为 W3C Trusted Types 规范编辑（koto@google.com, Google LLC）出现在 2026-06-23 Working Draft 中，Mike West 列为前编辑。ITP 与 EuroS&P 两项为 LinkedIn 自述、出版方一手未核验；W3C 编辑署名为一手核验。（置信度：low）
  - 证据：kk-tl-12, kk-tl-13, kk-tl-14, kk-rev1-01-linkedin-public-preview

## 主要成长机制

### Web 平台抽象边界作为连贯的攻击面研究路径

起点：约 2012 年自述为 SecuRing 咨询顾问，研究焦点已集中于 client side security、HTML5、UI redressing、Chrome extensions；GitHub 仓库 blog-kotowicz-net-examples 的目录名集合（CSP bypass、CORS、cross-domain uploads、cursorjacking、XSS、content extraction、charset、sandboxing、hash collisions、location spoofing）反映其长期锚定 Web/浏览器抽象边界而非内核内存破坏类问题。

练习与反馈：跨 2012–2021 反复在同一族 Web 平台边界问题（同源策略、CSP、内容嗅探、沙箱、扩展 API、DOM clobbering、Trusted Types）上发现、命名并系统化攻击原语：从 UI redressing/clickjacking，到浏览器扩展 API 滥用，到内容嗅探转化，再到脚本器件绕过 XSS 缓解，最终转为 DOM XSS 的标准内建防御。；厂商漏洞奖励与名人堂（2011 Facebook White Hat、Google Security Hall of Fame）、WhiteHat Top Ten Web Hacking Techniques 2012 第 3、Black Hat 等会议接收、W3C Web 应用安全工作组采纳 Trusted Types 提案。

能力与结果：将浏览器边界问题从孤立漏洞提炼为可命名的攻击原语与跨主题方法，使其在多个主题（扩展、内容嗅探、脚本器件、DOM XSS）之间形成可复用的分析起点。；xsschef（Chrome extension Exploitation Framework）与 mosquito 工具发布；Chrome 扩展攻击研究列入 WhiteHat Top Ten 2012 第 3；POODLE 协议级攻击协同披露（CVE-2014-3566）；Script Gadgets: Breaking XSS Mitigations via Code Reuse（CCS 2017，LinkedIn 自述）；Trusted Types 标准提案与 W3C 编辑职责

置信度：medium；替代解释：主题连贯性可能部分源于雇主（Google）对 Web 客户端安全方向的雇佣塑造，而非纯粹的个人方法选择；且 2016 年之后的学术成果时间线为 LinkedIn 自述，出版方一手未核验，连贯性的后期部分依赖该自述。

证据：kk-conv-03, kk-conv-04, kk-conv-05, kk-tl-03, kk-tl-04, kk-tl-05, kk-tl-06, kk-tl-09, kk-tl-10, kk-tl-11, kk-tl-13, kk-tl-14, kk-decisions-01, kk-decisions-03, kk-rev1-01-linkedin-public-preview

### 在既有公开工具与前人研究上迭代并显式标注来源

起点：约 2012 年自述为 SecuRing 咨询顾问，处于一个可识别的浏览器/加密安全同侪网络中（演讲致谢 Mario Heiderich、Ian Beer、Ivan Fratric、Adam Langley 等十余名研究者）。

练习与反馈：工具建设时显式标注灵感来源（Mosquito 标注 'Inspired by MalaRIA by Erlend Oftedal'、'BeEF tunneling proxy by @antisnatchor'）；披露建立在既有 TLS CBC 填充预言研究谱系之上（POODLE advisory 引用 RFC 2246/4346/5246/6101 及 Lucky13、TLS_FALLBACK_SCSV 草案）；标准提案与 Mike West 协作并列为前编辑。；演讲致谢名单与合著关系显示其在公开工具与研究生态中的协作与参考关系；POODLE 与同为 Google 员工的 Bodo Möller、Thai Duong 合著并经厂商博客公开。

能力与结果：在公开工具与研究生态中定位他人工作并将其作为迭代起点，而非孤立产出，形成可被同行追溯的研究习惯。；Mosquito 工具显式借鉴 MalaRIA（Erlend Oftedal）与 BeEF（Wade Alcorn/@antisnatchor）；POODLE 与 Bodo Möller、Thai Duong 合著并经 Google Online Security Blog 协同披露；Trusted Types 规范编辑署名（koto@google.com, Google LLC），Mike West 列为前编辑

置信度：medium；替代解释：致谢名单与合著关系可能反映学术与披露惯例而非持续的个人能力；合著者是否构成正式导师关系无证据证实，仅可推断为协作与参考关系。

证据：kk-conv-02, kk-conv-04, kk-tl-06, kk-tl-07, kk-tl-14, kk-rev1-01-linkedin-public-preview

### 工具、培训与白皮书的组合发布模式

起点：约 2012 年已具备国际会议演讲经历（Black Hat、BruCON、CONFidence），并自述为 SecuRing 咨询顾问从事 web app、mobile pentest 与 security code review。

练习与反馈：将研究主题整理为培训 + 白皮书 + 可复用工具的组合对外发布：Black Hat USA 2012 workshop 'Advanced Chrome Extension Exploitation: Leveraging API powers for Better Evil' 配套白皮书与 xsschef 框架。；培训接收与 WhiteHat Top Ten Web Hacking Techniques 2012 第 3 的行业榜单承认。

能力与结果：把单点发现转化为可复用框架与对外教学材料，使研究输出可被他人复现与教学传播。；xsschef（Chrome extension Exploitation Framework）发布；Black Hat USA 2012 workshop 培训；Chrome 扩展攻击研究列入 WhiteHat Top Ten 2012 第 3

置信度：low；替代解释：组合发布的直接可核验样本集中于 2012 单一场次（Black Hat USA workshop 与 xsschef），缺乏 2012 年之后同等组合（培训+白皮书+可复用框架三者并行）的直接证据；该模式可能是该次会议的特定要求而非跨时期稳定习惯。

证据：kk-decisions-01, kk-tl-04, kk-tl-05

### 厂商渠道与同行协同的协议级披露

起点：2014 年已为 Google 员工（Hack in Paris 2014 演讲第 2 页自述 Information Security Engineer @ Google），并自 2011 年起通过厂商漏洞奖励建立负责任披露记录。

练习与反馈：通过厂商官方安全博客与 advisory 协同公开协议级漏洞：POODLE 经 Google Online Security Blog 与 OpenSSL advisory 同步发布，披露建立在既有 TLS CBC 填充预言研究谱系之上。；厂商官方背书与协同署名（POODLE 三人 'also Googlers'，经 Google Online Security Blog 公开）。

能力与结果：在厂商内部渠道完成协议级漏洞的协同披露，将研究发现经厂商官方渠道对外发布。；POODLE（CVE-2014-3566）经 Google Online Security Blog 与 OpenSSL advisory 协同披露；POODLE advisory 引用既有 TLS CBC 填充预言研究与 TLS_FALLBACK_SCSV 草案；POODLE 三人合著（Bodo Möller、Thai Duong、Krzysztof Kotowicz）经 Adam Langley/ImperialViolet 转述确认

置信度：medium；替代解释：协同披露可能部分源于 Google 内部披露流程要求而非个人能力；POODLE 的合著关系本身不证明研究对象主导了发现，三者分工与主导关系在抓取材料中未区分。

证据：kk-tl-03, kk-tl-06, kk-tl-07, kk-tl-08, kk-conv-01, kk-rev1-01-linkedin-public-preview

## 可迁移与不可迁移

- 可迁移：在 Web 平台抽象边界（同源策略、CSP、内容嗅探、沙箱、扩展 API）上寻找跨主题的连贯攻击面，而非将每个漏洞视为孤立个案。
- 可迁移：构建可复用工具并对外发布，而非停留在一次性 PoC；工具建设时显式标注灵感来源（如 'Inspired by MalaRIA by Erlend Oftedal'），便于他人定位与推进。
- 可迁移：将研究结论转化为标准化提案（如 Trusted Types），以浏览器内建缓解机制替代逐点漏洞修补。
- 可迁移：通过厂商官方安全博客与 advisory 协同公开协议级漏洞，建立可核验的负责任披露记录。
- 不可直接迁移：2014-10-14 POODLE 披露时与 Bodo Möller、Thai Duong 同为 Google 员工，并经 Google Online Security Blog 协同背书；该厂商内部渠道与同事网络为特定雇主条件，非个人可复制。
- 不可直接迁移：Trusted Types 提案得以在 W3C Web 应用安全工作组推进并担任编辑，依赖 Google 作为标准参与方的组织身份（koto@google.com, Google LLC）。
- 不可直接迁移：2011–2014 年 Web 安全研究受关注度较高的时期，厂商漏洞奖励（Facebook White Hat、Google Security Hall of Fame）与行业榜单（WhiteHat Top Ten）为该时期外部条件；同期同主题研究在关注度较低的时期未必获得同等反馈。
- 不可直接迁移：Black Hat US/EU、CCS、EuroS&P 等会议与出版渠道的接收，依赖该时期会议议程与出版方审稿机制；这些渠道的可用性随时间与主题变化。
- 不可直接迁移：blog.kotowicz.net 作为长期 writeup 输出渠道的可用性，依赖个人持续维护与域名/证书状态；该渠道在研究窗口内因 TLS 证书错误不可一手访问，提示个人基础设施稳定性为不可迁移条件。

## 复核问题

- mechanisms[3]（厂商渠道与同行协同的协议级披露）将 validation_tests 标注为 ['repeated','generative']，但该机制的可核验产出仅由 POODLE 单一事件支持（kk-tl-06/07/08），缺乏第二例可比较的协议级协同披露以独立支撑 'repeated' 标注。三处引用指向同一披露事件的不同来源（ImperialViolet 转述、OpenSSL advisory PDF、Google Online Security Blog），属单事件的多个一手转述而非多事件重复，'repeated' 为对证据强度的过度归纳。
- 字段 mechanisms[3].validation_tests：将 ['repeated','generative'] 改为 ['generative']，或在 validation_tests 保留 'repeated' 的同时于 alternative_explanation 显式说明该 'repeated' 仅由 POODLE 单一事件及其多个一手转述支撑、缺乏第二例协议级协同披露对照，并将 mechanisms[3].confidence 由 'medium' 下调为 'low'。
- 字段 stages[1].capability_change：将 '2011 年起通过 Facebook White Hat 与 Google Security Hall of Fame 建立厂商漏洞披露记录。Black Hat USA 2012 以 ...' 与 'Chrome 扩展攻击研究在 WhiteHat Security Top Ten Web Hacking Techniques of 2012 评选中位列第 3' 两句前置 '据 LinkedIn 自述' 限定，与 stages[3]/stages[4] 对 LinkedIn 自述的处理保持一致；原文措辞 '通过 ... 建立厂商漏洞披露记录' 保留，仅需前置来源限定。
- 字段 mechanisms[0].alternative_explanation 或 mechanisms[0].confidence：在现有 alternative_explanation（已含 Google 雇主塑造与 2016 后 LinkedIn 自述依赖）基础上，显式指出该机制 'repeated_practice' 跨 2016–2021 的连贯性部分依赖未一手核验的学术时间线（Script Gadgets CCS 2017、Trusted Types 约 2017-06、EuroS&P 2021），或将 confidence 由 'medium' 下调为 'low'，以与 stages[4] 对同一证据强度的处理一致。
- 字段 tensions 或 open_questions：当前已正确处理 primary_focus '供应链漏洞' 与 Project Zero 成员身份两处来源-输入不一致，无需新增条目；维持既有 tensions[0]/tensions[1] 措辞。

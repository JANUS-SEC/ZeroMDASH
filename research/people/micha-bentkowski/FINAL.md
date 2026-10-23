# Michał Bentkowski：漏洞研究成长分析

- 擅长领域：Web/XSS/解析器差异漏洞
- 独立复核：pass · 93/100

## 成长阶段

- **2014-03 至 2015-05 · 厂商聚焦的 Web 入口漏洞积累与保护层绕过转向**：2014 年 3 月起在个人博客 bentkowski.info 系统记录 Google 产品的 Web 入口类漏洞（Google Code Playground 路径穿越、Gmail 与 Google+ 的 XSS、Google Doodle 响应分割），选题以单一厂商多产品为反复对象而非零散选题；2015 年 4 至 5 月研究对象由输出转义遗漏转向保护与 sanitization 层本身（Google CSE 经 Host 头的 XSS、Postini Header Analyzer 文件上传 XSS、Google Safen Up 经 window.stop() 的保护绕过）。2015 年 1 月收到 Google Security Team 通知其为 2014 年前十报告者之一并寄出实物包裹，构成 Google 厂商层面的反馈，与单一厂商反复选题共现。（置信度：high）
  - 证据：mb-works-01, mb-works-02, mb-dec-01-google-products-xss-start, mb-rr2-01
- **2016-07 至 2017-11 · 清洗器实现与浏览器安全边界转向，同对象间隔复访**：2016 年 7 月发表 Google Caja sanitizer 的多件 XSS 并同月发表 Firefox 同源策略绕过（CVE-2015-7188），研究对象由应用层 XSS 迁移到 sanitizer 实现与浏览器安全边界两个技术栈；2017 年 11 月以 Yet Another Google Caja bypasses（原标题含 hat-trick）复访约一年半前报告的 Caja，发现由 async function、async generator 构造器与 dynamic import 未被 FakeFunction 替换而构成的不同绕过路径，并以 ECMAScript 兼容性表说明语言新特性如何产生 sanitizer 空白。该阶段形成对同一对象间隔复访并对前后绕过作差异化标注的练习。（置信度：high）
  - 证据：mb-works-03, mb-works-04, mb-dec-03-shift-to-sanitizer-parser
- **2018-06 至 2018-09 · HTTP 语法与 CSP 解析差异扩展及漏洞连锁化**：2018 年 6 月发表 Chromium 经 CRLF 注入设定任意 HTTP 请求头与 Google Colaboratory 的 XSS 加 CSP 绕过，研究对象扩展到浏览器 header 与语法解析及 CSP 策略层；2018 年 7 月发表 Hangouts Chat 由开放重定向到 XSS 到代码执行的连锁，由单点 XSS 转向连锁构造；2018 年 9 月复访 Colaboratory，在 6 月报告被以禁用 MathJax 插件修复后，发现经跨域 cookie（mjx.menu）重新启用被禁插件使原 payload 再次生效的不同绕过路径，作者自述其为与上一件直接相关的另一件 XSS。该阶段共三件公开产出。（置信度：high）
  - 证据：mb-works-05, mb-works-06, mb-works-07, mb-tgt-02
- **2020-04（报告）至 2022-11（公开） · 浏览器内核层研究与披露规范化，DOMPurify mXSS 研究序列**：2020 年 4 月向 Chromium 报告 bug #1069486（2020-04 报告月份来源为 2022-11 正文一手自述，Chromium bug tracker 需登录未取得独立时间戳），涉及 Site Isolation 下同 Site 不同 origin 同进程分配与 DevTools debug() 断点跨 origin 残留的交互构成的同源策略绕过；取得 Chromium 团队全披露许可后于 2022 年 11 月以 Google Roulette 为题公开。同期形成 DOMPurify mutation XSS 跨版本研究序列（2.0.0、2.0.17），DOMPurify 2.0.16（2020-09-18）release notes 致谢 Michał Bentkowski 并修复由 MathML 内嵌套表单引起的 mXSS。研究对象延伸到浏览器内核层，公开流程趋于先协调后披露。（置信度：medium）
  - 证据：mb-works-08, mb-dec-05-chromium-browser-layer-extension, mb-tgt-01, mb-tgt-03, mb-dec-04-dompurify-mxss-research-program, mb-works-09
- **持续（工具更新可核验至 2017-03 至 2022-12，职业状态为当前） · 研究方法工具化与职业身份转入**：建设并公开研究辅助工具：livedom（对应 livedom.bentkowski.info，用于演示 DOM 解析差异，仓库 Updated 2022-12-27）、excessy（XSS 效果学习工具）、burp-exceptions（改善 Burp Suite Python 扩展异常可读性，Updated 2017-03-20），GitHub 资料另记 6 条 security advisory credits。当前职业身份为 Google Information Security Engineer（GitHub bio，无入职时间，与反复报告 Google 漏洞仅共现，非因果）。（置信度：low）
  - 证据：mb-dec-07-tool-building-livedom-excessy, mb-tgt-04, mb-timeline-02, mb-dec-06-move-to-google-ise, mb-timeline-01

## 主要成长机制

### 单一厂商多产品反复选题与厂商及上游反馈强化

起点：2014 年 3 月起在个人博客以 Google 产品为系统性选题对象，初始技术栈为输入验证与 HTTP/路径操作类 Web 漏洞，难度较低。

练习与反馈：反复对同一厂商（Google）的多个产品寻找 Web 入口、XSS 与解析差异，覆盖 Gmail、Google+、Google Doodle、Google CSE、Google Colaboratory、Hangouts Chat、Google Caja 及以 Google 控制台为入口的 Chromium 行为，形成以研究对象池（Google 产品线）为范围的反复选题习惯。；反馈来源主体需分别核验，不构成单一回路：（1）Google 厂商反馈——2015 年 1 月 Google Security Team 通知其为 2014 年前十报告者并寄出实物包裹（mb-rr2-01），属厂商层面反馈；（2）研究者自身再分类——Caja 前后绕过的无关系谱标注为研究者自身对 2016 与 2017 绕过的差异化标注，不归为厂商反馈；（3）上游维护者致谢——DOMPurify 2.0.16 release notes 的致谢方为 Cure53（DOMPurify 由 cure53 组织维护），不归为 Google 厂商反馈；（4）厂商披露协调——Chromium 全披露许可（mb-tgt-03）属披露流程反馈。

能力与结果：研究选题对象由 Google 多产品 XSS 迁移到清洗器与浏览器安全边界（mb-works-03、mb-works-04）。；2014 至 2018 年持续产出 Google 产品 XSS 与解析差异 writeup；DOMPurify mXSS 跨版本研究序列获上游修复致谢（mb-tgt-01）；2022 年以 Google Roulette 公开 Chromium 同源策略绕过（mb-works-08）；当前雇主为 Google（GitHub bio，无入职时间，与机制仅共现，不构成因果）

置信度：high；替代解释：厂商反馈强化与持续选题之间为共现关系而非已证因果；现职 Google Information Security Engineer 与反复报告 Google 漏洞仅共现，无入职时间、团队或与报告的关联证据（mb-dec-06-move-to-google-ise，status=inferred）。DOMPurify 致谢方为 Cure53 而非 Google，不应与 Google 厂商反馈合并表述为单一回路。

证据：mb-works-01, mb-works-02, mb-works-03, mb-works-04, mb-works-05, mb-works-06, mb-works-07, mb-works-08, mb-dec-01-google-products-xss-start, mb-rr2-01, mb-tgt-02, mb-timeline-01

### 同一对象间隔复访并差异化标注绕过路径

起点：2016 年 7 月首次发现 Google Caja sanitizer 的 XSS，并具备对 sanitizer 实现内部不一致的研究切入点。

练习与反馈：对同一对象间隔复访，每次寻找与上次不同的绕过路径或系谱：Caja 于 2016 年 7 月与 2017 年 11 月间隔约一年半复访，2017 年以 async/generator 构造器与 dynamic import 未被替换为新的绕过路径；Google Colaboratory 于 2018 年 6 月与 9 月间隔数月复访，9 月经跨域 cookie 再启用被禁 MathJax 插件构成不同绕过路径。；反馈主要来自修正后的复访：Colaboratory 6 月报告被以禁用插件修复后，9 月复访发现修复留下经跨域 cookie 重新启用被禁插件的攻击面（mb-tgt-02，作者自述另一件与上一件直接相关的 XSS）；Caja 前后绕过由研究者自身作无关系谱的差异化标注（mb-works-04）。

能力与结果：形成对 sanitizer 与解析器修复后残留攻击面的复访习惯，以及对前后绕过作差异化标注的练习。；Caja 2017 年复访发现不同绕过路径（mb-works-04）；Colaboratory 2018 年 9 月复访发现不同绕过路径（mb-tgt-02）；DOMPurify mXSS 序列跨 2.0.0 与 2.0.17 版本并获 2.0.16 与 2.0.17 上游修复致谢（mb-dec-04、mb-tgt-01；mb-works-09 正文未取得，status=reported，版本序列由 bentkowski.info/research 目录标题与 mb-tgt-01 release 时间线支持）

置信度：medium；替代解释：对 Colaboratory 而言，2018-09 正文支持的是不同绕过路径（再启用被禁插件），根因仍为同一 MathJax XSS，不同系谱的表述无正文支持；DOMPurify mXSS 序列的跨版本关系由目录标题与 release 时间线间接支持，research.securitum.com 正文 302 失效未取得，协作过程细节未证实。

证据：mb-works-03, mb-works-04, mb-works-07, mb-tgt-02, mb-dec-04-dompurify-mxss-research-program, mb-dec-03-shift-to-sanitizer-parser, mb-tgt-01

### 研究方法工具化与基础设施化

起点：研究过程中产生可复用需求：HTML 解析器差异演示、XSS 效果学习、Burp Suite Python 扩展异常可读性。

练习与反馈：建设并对外公开多个研究辅助工具：livedom（对应 livedom.bentkowski.info，演示 DOM 解析差异）、excessy（XSS 效果学习）、burp-exceptions（Burp 扩展异常可读性），把研究方法固化为可复用工具而非一次性产出。；工具以 GitHub 公开仓库形式对外发布；livedom 对应独立站点 livedom.bentkowski.info；GitHub 资料记 6 条 security advisory credits，为外部协作的客观记录。

能力与结果：把解析器差异研究工具化、基础设施化，使研究方法可复用。；livedom 仓库 Updated 2022-12-27（mb-tgt-04）；burp-exceptions 仓库 Updated 2017-03-20（mb-tgt-04）；excessy 作为 XSS 效果学习工具公开（mb-dec-07-tool-building-livedom-excessy）

置信度：low；替代解释：livedom 仓库创建日期与 commit 时间线未取得（profile 页与仓库页仅展示 Updated，无创建日期与 commit 时间戳，mb-tgt-04），与 writeup（尤其 2022-11 Google Roulette）的先后反馈关系未证实，工具建设闭环未闭合。若将 livedom、CRLF、CSP、连锁、SOP 并列为统一解释层框架的产出，该统一框架为后视归纳的可能，研究时是否以同一框架指导未证实。

证据：mb-dec-07-tool-building-livedom-excessy, mb-tgt-04, mb-timeline-02

## 可迁移与不可迁移

- 可迁移：对同一对象间隔复访，每次寻找与上次不同的绕过路径，并在修正后复访以发现修复留下的新攻击面（Caja 2016/2017、Colaboratory 2018-06/09）。
- 可迁移：把研究方法固化为可复用工具或基础设施（livedom 对应解析器差异演示），而非停留在一次性产出。
- 可迁移：先与厂商协调取得全披露许可再公开（Chromium Google Roulette，mb-tgt-03），使披露流程规范化。
- 可迁移：以单一厂商多产品为反复选题对象，形成对象池以积累可比的漏洞样本（注意：厂商反馈强化与持续选题之间为共现而非已证因果）。
- 不可直接迁移：现职 Google Information Security Engineer（GitHub bio，无入职时间，status=inferred），与反复报告 Google 漏洞仅共现，不可作为可迁移条件。
- 不可直接迁移：研究目录托管于 research.securitum.com，反映与 Securitum 团队的研究托管关系（mb-dec-04-dompurify-mxss-research-program），属特定组织资源。
- 不可直接迁移：早期 2014 至 2018 年以 Google 产品为选题对象，受当时 Google 产品攻击面与漏洞奖励生态等外部条件支持，属时期外部条件。
- 不可直接迁移：livedom 对应独立站点 livedom.bentkowski.info，属个人基础设施条件。

## 复核问题

- mechanism[1].observed_outcomes 第三项将『获 2.0.16 与 2.0.17 上游修复致谢（mb-dec-04、mb-tgt-01）』改写为『DOMPurify 2.0.16 release notes 明确致谢 Michał Bentkowski（mb-tgt-01），2.0.17 release notes 修复 mXSS 但未含致谢语句，致谢方为上游维护者 Cure53』，使致谢范围与已抓取上游来源（github.com/cure53/DOMPurify/releases?page=10）一致，避免 2.0.17 致谢超出已抓取证据。
- mechanism[2].alternative_explanation 将假设性框架列举『livedom、CRLF、CSP、连锁、SOP 并列为统一解释层框架产出』改为与该 mechanism observed_outcomes 一致的表述，仅列举已纳入 observed_outcomes 的 livedom/burp-exceptions/excessy 工具，或保留假设性框架列举但显式标注 CRLF/CSP/连锁/SOP 为本 mechanism 未纳入 observed_outcomes 的同期产出（works 维度 mb-works-05/06/08），消除内部不一致。

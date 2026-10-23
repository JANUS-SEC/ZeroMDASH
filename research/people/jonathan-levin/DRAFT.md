# 未通过独立复核

已达到最大修订次数 4；本文件是审计草稿，不得进入跨人物比较。

# Jonathan Levin：漏洞研究成长分析

- 擅长领域：Apple/Android 内核漏洞
- 独立复核：revise · 86/100

## 成长阶段

- **2012–2015（粗略归并而非严格连续；与第二阶段 2014–2018 在 2014–2015 重叠） · 依据作者自述的早期结构与公开记录的起步**：据作者自述（PST2，2015-08-20，见 jl-rev1-002），2012 年 MOXiI 第一版（原文以 'whenever it was published in 2012' 表述）已记录 processor_set_tasks() API，并自述该问题在 BlackHat 2014 被作为 0-day 公开（外部议程页 blackhat.com/us-14/briefings.html 返回 403 无法核验、PST2 未点名演讲者，此为作者 PST2 自述的背景叙述，非阶段能力变化的可核验支撑）；阶段定性主要依据三部曲以版本号而非版次持续迭代（jl-works-001）与三卷分册 User Mode/Kernel Mode/Security 的递进序列（jl-tl-02）。（置信度：medium）
  - 证据：jl-works-001, jl-tl-02, jl-rev1-002, jl-ext-003
- **2014–2018（粗略归并而非严格连续；与第一阶段 2012–2015 在 2014–2015、第三阶段 2017-12 在 2017 重叠） · 各版本内部机制记录与 API 设计层面缺陷推导**：研究产出从被动记录各版本内部变化（版本跟踪笔记 jl-works-004 覆盖 iOS 8.0–12 / OS X 10.10–10.14、jl-conv-01、jl-tl-05），扩展包含主动推导 API 设计层面缺陷并产出可复现方法链（jl-works-002 PST2，2015-08-20，mach_host_self → processor_set_default → host_processor_set_priv → processor_set_tasks → pid_for_task；jl-ext-004 TaiG 详解 CVE-2014-4480/4455 TOCTOU 利用链）。（置信度：medium）
  - 证据：jl-works-002, jl-works-004, jl-conv-01, jl-tl-05, jl-ext-004
- **2017-12 · 研究产出转化为可发布的越狱工具，并引发大规模社区试用与反馈**：2017-12-25 发布 tvOS 11 的 LiberTV、2017-12-26 发布 iOS 11（11.0–11.1.2）的半 untethered 越狱 LiberiOS；工具发布引发大规模社区试用与反馈（早期报告成功率较高，但因未捆绑 Cydia/Substrate 而对普通用户实用性有限）。（置信度：high）
  - 证据：jl-community-01-liberios-release-feedback, jl-rev2-002
- **2019-03 · 研究目标从 OS 层 API 与内核结构转向 A12 kernelcache 中的 PPL**：Casa de P(a)P(e)L 一文对 A12 kernelcache 中的 PPL 进行逆向：识别 __PPLTEXT/__PPLTRAMP/__PPLDATA 新段、通过 panic 字符串恢复约 150 个 PPL 内部符号、以 MOVZ X15, #N; B _ppl_enter 模式枚举 PPL 服务调用表、分析 APRR_EL1 寄存器位域语义（识别其作为权限切换控制位的用途），并发现 PPL 扩展覆盖 IOMMU/DART 与 NVMe 结构。（置信度：high）
  - 证据：jl-works-003, jl-works-006, jl-ext-001, jl-ext-002
- **2019–2026（粗略归并而非严格连续；与第四阶段 2019-03 在 2019 重叠） · 产出向结构化培训课程产品化与 Darwin 研究收尾**：研究产出向结构化培训课程产品化（jlaunchctl 文章推广 Technologeeks OS X/iOS Internals 培训 jl-ext-006，日期 2015-10-07 早于本阶段区间、属跨阶段复用证据；technologeeks.com Android Internals 培训 jl-rev2-001、jl-rev4-001 列于 2026-01 排期）；作者在 newosxbook 首页自述已 officially quit Darwin 但保留书籍销售（jl-tl-01）。（置信度：medium）
  - 证据：jl-ext-006, jl-rev2-001, jl-rev4-001, jl-tl-01, jl-tl-03, jl-tl-04

## 主要成长机制

### 自建逆向工具链与研究需求之间的相互驱动

起点：通用 Mach-O 分析工具（Hopper/IDA）在符号化与 gadget 查找上不能覆盖 Apple kernelcache 的分析需求（作者自述 'I don't see Hopper/IDA types getting this far without resorting to scripting'，见 jl-ext-001 短引文）。

练习与反馈：在已观察到的课题中（TaiG 2015、CasaDePPL 2019），研究产出与新工具能力需求相互关联：jl-ext-001 记录 jtool→jtool2 演进，jl-works-006 记录 CasaDePPL 研究产出为 jtool2 增加 PPL=1 环境变量功能（输出 PPL 符号）；两例第一方证据不足以一般化为稳定循环。；据作者站点，研究课题对工具提出新能力需求，研究产出反过来为工具增加功能；反馈来源主要为作者自述与 newosxbook.com 第一方文章（jl-works-006、jl-ext-001），无外部独立反馈来源核验。GitHub issue/PR 机制因 JTool2 仓库 https://github.com/newosxbook/JTool2 返回 HTTP 404 不可核验（jl-community-03-jtool2-github-issues 已标记 invalid，不作为机制支撑引用）。

能力与结果：据作者站点，用于 TaiG（2015）与 CasaDePPL（2019）等具体课题的 kernelcache 分析能力（jtool2 -l 段识别、-G gadget 查找、--analyze 符号化；jokerlib 自动符号化约 5070 符号 / 6 秒），避免外推至 jl-works-004 笔记覆盖的全部版本。；jtool→jtool2→jokerlib 工具迭代（jl-works-006、jl-ext-001）；CasaDePPL 研究中 jtool2 -l/-G/--analyze 作为主工具（jl-works-006）；CasaDePPL 研究产出为 jtool2 增加 PPL=1 输出 PPL 符号的功能（jl-works-006）

置信度：medium；替代解释：工具迭代与课题关联仅由作者自述与第一方文章支撑，可能反映通用逆向工具确实不足的客观情况，也可能反映作者对自有工具的选择性使用与对外宣传；两例不足以一般化为稳定的相互驱动循环。

证据：jl-works-006, jl-ext-001, jl-works-002

### 以多部分长篇连载对单一目标逐一展开

起点：单篇短文不足以覆盖 iOS OTA 更新格式、TaiG 越狱、PPL 等单一目标的完整内部机制。

练习与反馈：对单一目标以多部分长篇连载逐一展开（jl-works-005 'Taking apart iOS OTA Updates' 八部分连载；jl-ext-004 TaiG 详解 CVE-2014-4480/4455；jl-works-003 Casa de P(a)P(e)L 系统逆向 PPL），保持对单一目标的持续拆解。；同行博客互相引用（TaiG 文章引用 Pedro @OSXreverser 博客分析 jl-ext-002）；具体读者提交更正、作者采纳的过程未在一手页面证实（jl-community-05 站点含 ChangeLog 等导航但读者更正—作者采纳的过程未在一手页面证实）。

能力与结果：据作者站点，对单一目标产出可复现的、覆盖完整内部机制的技术文档，而非偶发性研究。；iOS OTA 更新格式系统逆向（jl-works-005）；TaiG 越狱 CVE-2014-4480/4455 TOCTOU 利用链详解（jl-ext-004）；PPL 系统逆向（jl-works-003）

置信度：medium；替代解释：连载形式可能反映作者写作偏好与自出版（TechnoloG imprint）的修订自由度，而非研究方法的内在要求；读者更正采纳过程未在一手页面证实，同行引用仅来自作者致谢段。

证据：jl-works-005, jl-works-003, jl-ext-004, jl-ext-002, jl-community-05

### 研究发布前同行审阅与同行博客互引

起点：作者在 newosxbook.com 自撰 writeup 发布前存在同行审阅环节（CasaDePPL 致谢 @S1guza 进行彻底审阅并研读 ARM64 规范 jl-ext-002）。

练习与反馈：研究发布前由同行审阅，并与同行博客互相引用（jl-ext-002 CasaDePPL 致谢 @S1guza；TaiG 文章引用 @OSXreverser 博客；jlaunchctl 提及 @launchderp/@bruienne 互动）。；同行就同一主题独立发表演讲的外部证据缺位（作者在 CasaDePPL 自述 Luca 在 Tensec 与 BlueHat.il 就 PPL 主题演讲并指向 iokit.racing/bluehatil.pdf；该 PDF 因证书校验错误未抓取、会议方议程页亦未抓取，仅作者自述支撑，不作为同行就同一主题独立发表演讲这一判断的独立依据）。

能力与结果：据作者站点，研究发布前经同行审阅形成同行交叉验证。；CasaDePPL 致谢 @S1guza 审阅 ARM64 规范（jl-ext-002）；TaiG 文章引用 @OSXreverser 博客（jl-ext-002）；作者自述 Luca 在 Tensec/BlueHat.il 就 PPL 主题演讲（jl-ext-007、jl-rev1-001，PDF 未抓取）

置信度：low；替代解释：同行审阅与互引全部来自作者 newosxbook.com 自撰 writeup 致谢段，同行就同一主题独立发表演讲的外部证据缺位（PDF 与议程页均未抓取），该机制的可核验程度有限，仅作者自述支撑。

证据：jl-ext-002, jl-ext-007, jl-rev1-001

### 将逆向产出整理为公开文档、书籍与培训课程

起点：各版本内部机制的逆向产出分散于 writeup，需整理为可独立销售与讲授的产品。

练习与反馈：将每次逆向产出整理为公开文档（newosxbook.com 持续发布 writeup jl-works-004、jl-conv-01、jl-tl-05）、书籍（三部曲 Vol I User Mode / Vol II Kernel Mode / Vol III Security & Insecurity jl-works-001、jl-tl-02）与培训课程（technologeeks Android Internals 培训 jl-rev2-001、jl-rev4-001）。；据作者站点，三部曲以版本号而非版次持续迭代（Vol I v1.3.3.7.1 / Vol II v1.0.2 / Vol III v1.6.6），版本号差异反映 User Mode 卷迭代最久、Kernel 卷相对后期完成 1.0；具体读者提交更正、作者采纳的过程未在一手页面证实。

能力与结果：据作者站点，将分散的逆向产出整理为可独立销售的书籍产品与结构化培训课程。；三部曲以版本号持续迭代（jl-works-001、jl-tl-02）；newosxbook.com 持续发布 writeup 与版本跟踪笔记（jl-works-004、jl-conv-01、jl-tl-05）；Technologeeks Android Internals 培训 2026-01 排期（jl-rev2-001、jl-rev4-001）

置信度：medium；替代解释：'工程化为可独立销售的书籍产品''而非偶发性研究'等概括仅依据作者站点与索引页，可能反映自出版的商业持续性而非研究产出规模的客观量级。

证据：jl-works-001, jl-tl-02, jl-works-004, jl-conv-01, jl-tl-05, jl-rev2-001, jl-rev4-001, jl-ext-006

### 工具发布引发大规模社区试用与反馈

起点：2017-12 iOS 11 缺少可用越狱，Cydia/Cydia Substrate 尚未为 iOS 11 适配。

练习与反馈：发布 LiberiOS（iOS 11.0–11.1.2）与 LiberTV（tvOS 11），工具公开发布后立即引发大规模社区试用与缺陷反馈（jl-community-01-liberios-release-feedback）。；早期用户报告成功率较高但因未捆绑 Cydia/Substrate、缺 offset 而对普通用户实用性有限；Saurik 就 Cydia Substrate 适配 iOS 11/64-bit ARM 所需工作公开回应；CoolStar 随后发布含 Substitute 的 Electra 越狱，社区部分转向 Electra（jl-community-02，lead_only，未抓取原始页面）。作者据搜索结果转述在 X/Twitter 上就 LiberiOS 局限主动回应社区提问（jl-community-04，X 页面返回 402 未能直接核验推文正文）。

能力与结果：工具公开发布后通过公开渠道承接未预期的兼容性缺口反馈，而非仅自我迭代。；LiberiOS 2017-12-26 发布并引发社区试用反馈（jl-community-01-liberios-release-feedback、jl-rev2-002）；LiberTV 2017-12-25 发布（jl-rev2-002）；同侪 Saurik/CoolStar 公开回应与替代实现竞争（jl-community-02，lead_only）

置信度：medium；替代解释：社区反馈规模可能受 2017-12 iOS 11 越狱供需缺口放大，而非反映作者常态发布—反馈关系；Saurik/CoolStar 的替代实现竞争仅由 lead_only 搜索片段支撑，原始页面未抓取。

证据：jl-community-01-liberios-release-feedback, jl-rev2-002, jl-community-02, jl-community-04

## 可迁移与不可迁移

- 可迁移：以自建工具承担通用工具无法覆盖的分析需求；在已观察到的课题中研究产出与新工具能力需求相互关联（jl-works-006、jl-ext-001），两例不足以一般化为稳定循环。
- 可迁移：对单一目标以多部分长篇连载逐一展开，保持对单一目标的持续拆解（jl-works-005、jl-works-003、jl-ext-004）。
- 可迁移：将每次逆向产出整理为公开 writeup，使方法链可被他人按 writeup 复现（无他人实际复现的已抓取证据）。
- 可迁移：以版本号而非版次持续迭代长期作品，保留修订自由度（jl-works-001、jl-tl-02）。
- 可迁移：研究发布前由同行审阅并与同行博客互引（jl-ext-002）；该同行交叉验证的可核验程度有限（jl-rev1-001 仅作者自述、iokit.racing/bluehatil.pdf 未抓取、会议方议程页未抓取），不宜作为可迁移实践单独引用。
- 可迁移：研究产出向结构化培训课程产品化（jl-ext-006、jl-rev2-001、jl-rev4-001）；证据不支撑培训反向作用于工具或著作。
- 不可直接迁移：幸存者偏差：研究对象为 rank=53 成名研究员，证据集中在成名后的公开 writeup 与 LiberiOS 发布反馈，入门期、失败案例与未公开探索缺位；该偏差影响 transferable_practices 的可迁移边界，避免读者将成名后的公开产出习惯一般化为可复制的成长路径。
- 不可直接迁移：transferable_practices 中同行交叉验证一项的可核验程度有限（jl-rev1-001 仅作者自述、iokit.racing/bluehatil.pdf 未抓取、会议方议程页未抓取），不宜作为可迁移实践单独引用。
- 不可直接迁移：自出版（TechnoloG imprint）与自运营站点（newosxbook.com、technologeeks.com）带来的修订与发布自由度，非多数研究者可复制条件。
- 不可直接迁移：Apple 平台封闭性与越狱生态供需缺口（2017-12 iOS 11）放大社区反馈规模，非研究方法本身可迁移条件。

## 复核问题

- 结论引用缺失或已作废：['jl-works-005', 'jl-works-003', 'jl-ext-004', 'jl-ext-002', 'jl-community-05']
- 结论引用缺失或已作废：['jl-community-01-liberios-release-feedback', 'jl-rev2-002', 'jl-community-02', 'jl-community-04']

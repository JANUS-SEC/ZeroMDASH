# Ivan Fratric：漏洞研究成长分析

- 擅长领域：浏览器漏洞与模糊测试
- 独立复核：pass · 86/100

## 成长阶段

- **约2017年 · 进入 Project Zero 并以生成式文法模糊测试建立可复测基线**：GitHub 个人资料 employer 关联 @google、简介自标 'Google Project Zero member'，domato 仓库 README 署名 'Written and maintained by Ivan Fratric, ifratric@google.com'、版权 2017 Google Inc.、Apache License 2.0，三处互证其 Google/Project Zero 阶段身份。同一时期发布 domato（基于上下文无关文法生成 HTML/CSS/JS 样本的 DOM fuzzer），并在《The Great DOM Fuzz-off of 2017》中对 Safari/Chrome/Firefox/IE/Edge 各跑约 1 亿次迭代做横向对比，把单点漏洞发现转化为可被同行复现的受控测量。覆盖范围声明：成长机制仅基于已发表公开产物（Project Zero 官方博客、googleprojectzero 公开仓库、合作报告 CVE）中可观察的模式，不代表其全部研究活动；pre-Google 阶段无 verified 证据，本阶段所谓'成长'的实际覆盖范围限于在 Project Zero 的成长。（置信度：high）
  - 证据：if-c-001, ext-01, ivf-tl-002, rev1-ivf-001, if-c-005
- **2018年 · 符号执行失败后回退基础手段组合，并建立同工具逐年复测**：在 Skia 图形库研究中以第一人称复数自述先尝试符号执行（KLEE 配 STP/Z3 后端）寻找导致越界绘制的输入，因工具不支持浮点符号变量且无法在合理时间内跑完而失败，随后退回到人工源码审查、边界值 fuzzing 与对可疑代码段直接穷举取值的组合作为补偿；最初线索并非定向审计 Skia，而是在对 Firefox 做 DOM fuzzing 时偶然发现一个越界写，随后从偶然越界写信号追因到 Skia 底层库。同年用同一 domato 与同一 1 亿次迭代方法学复测 WebKit/Safari，bug 数由 17 降至 9（全部在 Safari 12 修复），并为 CVE-2018-4314（SVG UAF）编写 PoC，记录将 UAF 转为 infoleak 是耗时最多的部分；同时公开指出 Apple advisory 在修复后未及时列出对应 bug 形成误导。（置信度：high）
  - 证据：if-dc-01, if-dc-02, if-c-002, ext-02
- **2021年 · 将文法经验迁移为覆盖引导二进制模糊测试器 Jackalope**：发布 Jackalope——覆盖引导的 black-box binary fuzzer（Windows/macOS），其文法与 domato 类似但有所简化，并新增 <repeat_*> 节点以在保持文法有效性的前提下做插入/删除；与 Fuzzilli 及 TinyInst 一同在 IE 的 jscript/jscript9 上跑数周/100 核，发现 CVE-2021-26419、CVE-2021-31959（bytecode generator）与 CVE-2021-34480（JIT 编译器），并将 Jackalope 与 Fuzzilli 在覆盖率与 bug 命中度上的相近表现如实对照。（置信度：high）
  - 证据：ext-03, if-c-006
- **2025–2026年 · 研究范围扩展至多媒体解码器并对方法本身进行复盘**：与 Natalie Silvanovich 合作报告 CVE-2025-54957（Dolby Unified Decoder），研究范围扩展至浏览器与 JS 引擎之外的多媒体解码器目标；在 2026 博文中公开反思变异式文法模糊测试的方法缺陷并提出改进技术，研究输出由工具与漏洞报告扩展至方法学复盘。（置信度：high）
  - 证据：if-c-003, ext-05, if-c-004, ext-04, if-dec-001, if_works_01

## 主要成长机制

### 跨工具的模糊测试方法迁移与累积

起点：Project Zero 阶段初期以生成式文法模糊测试为起点：domato（2017）基于上下文无关文法生成 HTML/CSS/JS 样本。

练习与反馈：将前一套工具的文法经验迁移、简化并扩展为后一套：domato 的文法在 Jackalope（2021）中被'简化'并新增 <repeat_*> 节点以支持插入/删除；Jackalope 的文法模糊测试实现又在 2026 年被作为变异式文法模糊测试研究的基线（'This research is based on the grammar fuzzing implementation in my Jackalope fuzzer'），并将同一技术跨目标迁移到 XSLT 实现与 JIT 引擎。；公开 writeup 自述改进技术经自测 'worked surprisingly well and helped discover issues in libxslt quicker'，并在博文中引用 libxslt issue 409761909 作为具体 bug tracker 反馈点；参照团队另一成员 Samuel Groß 的 Fuzzilli 文档描述同类问题，构成工具间文献互引式反馈。

能力与结果：形成'把一次性方法沉淀为可复用工具、再把工具作为下一轮方法研究的起点'的累积式工具链，而非每轮从零开始。；domato（2017）作为生成式 DOM fuzzer 在 Safari/Chrome/Firefox/IE/Edge 上协助发现 CVE；Jackalope（2021）在 jscript/jscript9 上发现 CVE-2021-26419、CVE-2021-31959、CVE-2021-34480；变异式文法模糊测试（2026）用于 XSLT 实现与 JIT 引擎并自述曾成功发现 bug

置信度：high；替代解释：工具连续性可能部分来自 Project Zero 团队'每人/若干人维护一个专门 fuzzer'的分工结构而非个人方法迁移倾向；Jackalope 文法与 domato 类似也可能源于 domato 文法本身已是可复用的通用资产，迁移成本低，而非刻意的方法论累积。

证据：if-c-001, ext-01, ext-03, if-c-004, ext-04, ivf-tl-002

### 同工具同方法学的横向对比与逐年纵向复测

起点：2017 年以 domato 对五大浏览器各跑约 1 亿次迭代，把'同样的方法、同样的迭代量、同样的公开工具'作为可比基线。

练习与反馈：2018 年用同一 domato 与同一 1 亿次迭代方法学复测 WebKit/Safari，纵向比较 bug 数由 17 降至 9；并在 2021 年将 Jackalope 与 Fuzzilli 在覆盖率与 bug 命中度上做横向对照；同时如实记录额外尝试的覆盖引导 DOM fuzzer 在 IE 上'未产生新 crash'。；复测结果直接指向供应商安全改进是否真实，并以公开批评 Apple advisory 未及时列出对应 bug 的方式把供应商披露流程纳入反馈。

能力与结果：形成以受控变量（同工具/同迭代量/同方法学）跨引擎、跨年份比较的测量习惯，把单点发现转化为可被同行复现的测量实验。；2017 年 Safari 以 17 个 bug 显著高于 Chrome(2)/Firefox(4)/IE(4)/Edge(6) 被识别为离群值；2018 年复测确认 Safari bug 数由 17 降至 9 且全部在 Safari 12 修复；对工具边界（额外覆盖引导 DOM fuzzer 在 IE 上无新 crash）的诚实记录

置信度：high；替代解释：横向/纵向复测可能部分由 Project Zero 公开 writeup 的可复现性要求驱动（博客读者可自行复跑 domato），而非纯粹的个人研究偏好；Safari 显著离群也可能反映各引擎对 DOM 文法模糊测试的成熟度差异而非方法本身优劣。

证据：ext-01, ext-02, ext-03

### 公开 writeup 中复盘方法失败/缺陷并提出替代或改进

起点：2018 年 Skia 研究中遭遇符号执行失败这一可公开复盘的负面经验。

练习与反馈：在 2018 年博文中自述符号执行因不支持浮点符号变量且无法在合理时间内跑完而失败，随后退回人工源码审查、边界值 fuzzing 与对可疑代码段直接穷举取值的组合；在 2026 年博文中再次复盘覆盖引导变异式文法模糊测试的 'perceived flaws' 并提出周期性重启 worker、半时间独立生成半时间纳入先验覆盖的改进技术，自测 'worked surprisingly well'。从偶然越界写信号追因到 Skia 底层库的追因行为亦属于不满足于报告单点 bug、继续做根因分析的重复练习。；自我测试结果（libxslt 发现速度提升）与 bug tracker 落地点（libxslt issue 409761909）构成方法改进的反馈出口；早期符号执行的失败本身作为方法选型的负面反馈。

能力与结果：在工具失效时不依赖单一方法，而是显式组合多种基础手段（人工审查+边界值 fuzzing+穷举）作为补偿，并把方法缺陷公开化、提出可测试的改进。；2018 年符号执行失败后以基础手段组合产出 Skia 精度类研究；2018 年为 CVE-2018-4314 编写 PoC 并记录 UAF 转 infoleak 的工程难点；2026 年提出变异式文法模糊测试的改进技术并自测有效

置信度：high；替代解释：公开复盘可能部分受 Project Zero 博客文化（鼓励披露方法与失败）影响，而非个人特有习惯；符号执行失败也可能因该工具对图形库浮点问题本身不适配，回退基础手段是工具属性决定的合理选择而非个人方法论创新。

证据：if-dc-01, if-dc-02, ext-02, if-c-004, ext-04, if-dec-001

### Project Zero 内部同伴协作与工具互引

起点：身处 Project Zero 团队，存在与同队研究员并行或合作输出的条件。

练习与反馈：2018 年与 Mark Brand 联合署名《Drawing Outside the Box》，各自独立探索相关图形库问题（Brand 研究 SwiftShader，Fratric 研究 Chrome/Firefox 共用的 Skia）后合并发表；2026 年与 Natalie Silvanovich 合作报告 CVE-2025-54957（Dolby Unified Decoder）；在变异式文法模糊测试博文中参照团队另一成员 Samuel Groß 的 Fuzzilli 文档描述同类问题。；同一研究主题上与同事分工独立探索再合并发表构成同伴校验；被同队高产出研究员以'共同报告者'身份在公开 writeup 中点名（'Ivan Fratric and I reported CVE-2025-54957'），评价锚定在具体 CVE 而非泛泛赞美。

能力与结果：能在团队内部以分工-合并或共同报告模式产出，并把同伴工具（Fuzzilli）作为方法对照与文献参照纳入自己的研究。；2018 年与 Brand 联合署名的 Skia/SwiftShader writeup；2025 年与 Silvanovich 合作报告 CVE-2025-54957；2026 年博文中参照 Fuzzilli 文档

置信度：medium；替代解释：协作频率可能主要由 Project Zero 的团队组织结构与任务分配决定，而非个人主动寻求同伴校验；组织页声明 'This organization has no public members'，作者归属由 writeup 自述锚定（if-c-006 为 inferred），工具互引也可能是同一团队工具天然可被引用所致。

证据：if-c-002, if-c-003, ext-05, if-c-004

## 可迁移与不可迁移

- 可迁移：把一次性方法沉淀为可复用工具，再把工具作为下一轮方法研究的起点（domato→Jackalope→变异式文法模糊测试）
- 可迁移：以同工具、同迭代量、同方法学跨引擎或跨年份做受控对比，把单点发现转化为可被同行复现的测量实验
- 可迁移：在公开 writeup 中如实记录方法失败（符号执行）与工具边界（额外 fuzzer 无新 crash），不以单次成功做宣传
- 可迁移：在工具失效时显式组合多种基础手段（人工审查+边界值 fuzzing+穷举取值）作为补偿，而非依赖单一方法
- 可迁移：把发现推进到可验证利用（为 CVE 编写 PoC、记录 UAF 转 infoleak 的工程难点）以暴露研究由'发现问题'向'验证可利用'演进
- 可迁移：以 bug tracker issue 作为方法改进的反馈落地出口（libxslt issue 409761909）
- 不可直接迁移：Project Zero 的专职资源与团队组织结构，使其能持续投入浏览器漏洞与模糊测试方向；这一组织前提不可由个人研究者单独复制
- 不可直接迁移：googleprojectzero 组织下的工具矩阵（domato、fuzzilli、Jackalope、TinyInst、winafl 等）与'每人/若干人维护一个专门 fuzzer'的分工，是同伴分工协作与工具互引机制得以发生的组织前提；组织页声明 'This organization has no public members'，作者归属由 writeup 自述锚定（if-c-006 inferred）
- 不可直接迁移：与同队高产出研究员（Silvanovich、Groß、Brand）的并行-合并输出与工具互引渠道，依赖团队内部关系而非可迁移的个人方法
- 不可直接迁移：domato 仓库 README 署名 ifratric@google.com、版权 2017 Google Inc.，与其 Google/Project Zero 阶段身份绑定；该身份标识由 GitHub ifratric 个人资料 employer 关联 @google、简介 'Google Project Zero member' 与仓库版权头三处互证（rev1-ivf-001 一手确认邮箱写法）

## 复核问题

- 建议在 mechanisms[1] 正文或 evidence_ids 注释处局部标注 if-c-006 为 inferred（组织页无 public members，作者归属由 writeup 自述锚定），与 mechanisms[3].alternative_explanation、non_transferable_conditions[1] 的全局标注保持一致，避免读者在该机制局部误读为已独立核验的组织页归属。属透明度增强，非阻断性。
- 建议在 mechanisms[1] 对 2026-03-05 博文 XSLT/JIT 自述的引用处，参照 tensions[1] 的口径加注 '该自述依据首页转述，正文 URL 在 if-dc-03 报 404，未取得一手逐句核对'，使机制局部与 tensions/open_questions 的 reported 处理一致。属透明度增强，非阻断性。

# Thomas Dullien (Halvar Flake)：漏洞研究成长分析

- 擅长领域：二进制漏洞与利用技术
- 独立复核：pass · 77/100

## 成长阶段

- **约 2005-2008 · 公开技术写作与内部方法工具化的起点**：以博客 ADD/XOR/ROL 为载体建立面向安全社区的公开输出习惯，并与同事协作把内部逆向导航方法固化为可分发工具（SABRE BinNavi，后演化为 zynamics 系列工具），把研究方法转化为社区可复用资产；这一阶段为后续把方法固化为工具并公开发表的习惯奠定了起点，而非以天赋或热爱等无证据措辞解释。该阶段的工具建设方法论细节（补丁分析、去混淆、中间表示 REIL）另有 2008 年多篇博文线索，但均为 lead_only 且未一手核验正文，仅作线索保留。（置信度：high）
  - 证据：r1-pub-blogstart, halvar-community-01, halvar-community-02, halvar-community-03, halvar-ext-03, halvar-ext-04, halvar-ext-05, halvar-ext-06, halvar-ext-08
- **约 2011-2015 · 进入大型工程组织与行业承认阶段**：2011 年加入 Google，本人自述此前越来越多时间花在管理与销售上，并选择 Google 因其共享以工程为中心的文化、拥有自身欠缺的资源；zynamics 团队整体加入 Google 构成由独立工具公司向大型工程组织研究环境转变的公开一手节点。2015 年获 Pwnie Awards 终身成就奖（Lifetime Achievement），构成可核验的外部承认标记。此阶段把工程为中心的文化契合作为转型的判断依据，而非将组织环境本身描述为能力来源。（置信度：high）
  - 证据：halvar-ext-01, halvar-ext-02, r1-ext-engineering-ratio, conv-01, halvar-pub-06, tdhf-dec-2011-google, td-timeline-05, r1-conv-pwnie
- **约 2025-2026 · 人机协作研究方法的形成与固化阶段**：把既有的成熟工程习惯迁移到 LLM 辅助研究：为模型提供大量条件编译日志与可运行细粒度测试，建立多 subagent 证据流水线（函数级执行轨迹、gcov、ASAN 构建、rr 确定性回放），并以生成/验证分离（一者产出假设并须提供 receipts，一者独立逐步骤核验）构成可复用反馈机制；同期把元认知式自我审视（审视自身激励结构、识破自我欺骗、设想自己是问题方）表述为可重复的操作步骤，与崩溃归因中把验证程序化的做法同构。该阶段亦伴随技术对象从二进制/漏洞研究向神经网络内部机制学习与实验转变的线索，但该转变主要依赖未核验 permalink（verified_in_run=false），保留为资料缺口而非核心断言。（置信度：high）
  - 证据：halvar-pub-03, r1-conv-receipts, halvar-community-04, halvar-community-05, halvar-community-06, halvar-community-07, halvar-pub-05, conv-02, conv-07, halvar-ext-09, tdhf-dec-2026-maturation-reflection, tdhf-dec-2026-new-company, td-timeline-08, r1-pub-neuralnets, r1-conv-vibecoding, r1-pub-vibecoding

## 主要成长机制

### 把内部方法固化为可分发工具并公开发表

起点：2005 年起以 ADD/XOR/ROL 博客为载体建立公开写作习惯，副标题自述为 'A blog about reverse engineering, mathematics, politics, economics and more ...'；早期与同事 Ero、Rolf 协作完成 SABRE BinNavi，处于把内部逆向导航方法工具化的起点。

练习与反馈：在约 21 年的公开输出中反复把内部研究方法（逆向导航、二进制比对、去混淆、崩溃归因）固化为工具或可分发资产，并以博客、agent/skill 文件、第三方仓库等形式公开发表；2025-12 把崩溃归因方法以 agent/skill 形式贡献到第三方仓库 raptor，并据听众反馈将方法显式化写成博文。；公开输出本身是反馈回路的入口：只有公开发表才会引来反馈；2025-12 在面向听众演示后收到反馈，称让 LLM 提供详细 receipts 并由第二个 LLM 验证 receipts 这一技巧此前 not necessarily widely known，作者据此把方法写成博文并对外贡献工具。此外以资深同事（Bell Labs 背景）为参照群体，把私人反思转为可被社区评议的公开文本。

能力与结果：形成了把个人方法论转化为社区可复用、可质疑资产的能力，以及把隐含技能显性化的工程化习惯；这一中间能力使方法可被他人拉取、复用与检验，而非停留在个人经验。；2005 年与同事协作完成 SABRE BinNavi，把内部逆向导航方法固化为可分发工具；2025-12 把崩溃归因方法以 agent/skill 形式贡献到第三方仓库 raptor（README 将 Thomas Dullien (Halvar Flake) 列为合著者之一）；2025-12 据听众反馈把让 LLM 提供 receipts 并由第二个 LLM 验证的技巧写成博文并对外发布；2011-03 在博客公开宣布 zynamics 整个团队加入 Google，把职业转向以公开一手记录形式沉淀

置信度：high；替代解释：该机制的可观测性高度依赖持续公开输出这一幸存条件：停止公开输出或以非公开方式工作的研究者不在可观测样本内，因此长周期公开写作本身可能既是机制也是观测窗口，存在幸存者偏差；此外 raptor 仓库 commit 级粒度未核验（halvar-community-08 为 inferred），其贡献事实由 README 作者列表与本人博客陈述联合推断，具体 commit 与日期证据缺口保留。

证据：r1-pub-blogstart, halvar-community-02, halvar-community-04, halvar-community-05, halvar-community-08, halvar-ext-01

### 生成/验证分离的反馈回路

起点：早期博客即体现面向社区的公开同行评议习惯（公开评论同行写作风格）；2025-12 在 C++ 崩溃归因任务中遇到 LLM 产生不可信根因与 AI slop 的失败模式，需要在难以验证的任务上建立可靠反馈。

练习与反馈：在崩溃归因流水线中设计双 subagent：一者采集证据（函数级执行轨迹、gcov、ASAN 构建、rr 确定性回放）并产出假设且须提供 receipts（如指出导致崩溃解引用的指针在何处分配），另一者独立逐步骤核验，核验失败则写反驳并回环直至通过；同期在自我审视中把'审视自身激励结构、识破自我欺骗、设想自己是问题方'表述为可重复的操作步骤。；验证 subagent 的逐步骤核验与反驳构成机制化反馈：核验失败回环至假设修正；自我审视中以'Anxiety about the impact of your work is self-flattering'与'Do not believe everything you think. Examine your own incentive structures carefully.'作为对自我合理化的内部反馈。

能力与结果：形成了把验证与自我审查程序化为可重复步骤的能力，使验证不依赖人工盯防，而由独立代理或可操作步骤承担；这一中间能力在崩溃归因与元认知自我审视两处呈现同构。；2025-12 建立多 subagent 崩溃归因流水线，生成/验证分离并由第二 subagent 逐步骤核验；2025-12 经数日迭代后使 LLM 崩溃归因 reasonably well 工作，把失败-修正循环固化为可分发 agent/skill；2026-08 把自我审视表述为可操作反馈习惯：审视激励结构、设想自己是问题方

置信度：high；替代解释：崩溃归因（技术验证）与自我审视（认知反思）的同构可能是事后叙事的类比建构而非同一机制的两次显现；二者分属技术验证与认知反思两个领域，其程序化外观可能源于对'可重复步骤'这一通用偏好的独立投射，而非同一反馈回路的迁移。此外该机制的 self-report 成分较高，缺乏外部同事对验证回路有效性的独立评价。

证据：halvar-pub-03, r1-conv-receipts, halvar-community-01, halvar-community-04, halvar-community-07

### 成熟工程习惯向 LLM/ML 新领域迁移

起点：长期二进制/漏洞研究与 C++ 工程经验中积累的工程习惯（细粒度日志、可测试性、会话隔离、供应链攻击缓解意识、数学化/形式化取向），以及以工程为中心的文化判断框架（以非工程与工程的比率约 7% 衡量 zynamics 与 Google 文化契合）。

练习与反馈：把既有工程习惯迁移到 LLM 辅助研究与新领域学习：为模型提供大量条件编译日志与可运行细粒度测试作为人机协作调整；采用 SSH 登录服务器并 attach 到 screen/tmux 会话、在 detached 状态下让 agent 长时间处理问题的开发模式，并把该模式溯源至黑客亚文化；在神经网络学习中引用 ReLU 网络激活模式、Deep ReLU 网络多面体、DNN 样条等文献，延续数学化/形式化取向。；迁移的反馈来自 LLM 的失败模式（幻觉、AI slop）与长时算力/脱离会话运行的需求驱动；2025-12 receipts 文自述经数日迭代后以提供 receipts 与独立校验 subagent 解决，构成迁移中的失败-修正循环。

能力与结果：形成了把既有安全/工程习惯作为可迁移模板应用到新领域（LLM 协作、ML 学习）的能力，而非从零学习新领域；这一中间能力降低了对新工具链的适应成本，但也可能把旧习惯的适用边界带入新领域。；2025-12 为 LLM 提供条件编译日志与细粒度测试作为人机协作工程化调整；2026-03 把 SSH/screen 会话隔离、供应链攻击缓解等安全研究习惯应用于 LLM 编码代理工作流；2025-05 起在博客连载神经网络内部机制学习与实验，引用 ReLU 激活模式、多面体、样条等文献

置信度：medium；替代解释：该机制部分依赖未核验线索：r1-conv-vibecoding、r1-pub-vibecoding（2026-03 vibecoding）与 r1-pub-neuralnets（2025-05 神经网络连载）的 permalink 均未一手核验（verified_in_run=false），其迁移性叙述可能沿当事人对自身路径合理化的方向展开；此外把成熟工程习惯迁移到新领域是普遍的工程实践，区分度相对较低，可能并非该研究者特有，存在与一般资深工程师习惯重叠的非迁移性成分。

证据：r1-conv-receipts, halvar-pub-03, r1-ext-engineering-ratio, r1-conv-vibecoding, r1-pub-vibecoding, r1-pub-neuralnets

## 可迁移与不可迁移

- 可迁移：把内部研究方法固化为可分发工具或 agent/skill 文件并公开发表，使方法可被他人复用与质疑，而非停留在个人经验。
- 可迁移：在难以验证的任务上采用生成/验证分离：一者产出假设并须提供 receipts，另一者独立逐步骤核验，核验失败回环至修正。
- 可迁移：为人机协作提供大量条件编译日志与可运行细粒度测试，作为模型可验证性的工程化前提。
- 可迁移：把自我审视拆解为可重复步骤（审视自身激励结构、设想自己是问题方、识破自我欺骗），把反思程序化而非依赖笼统的伦理表态。
- 可迁移：以非工程与工程的比率等可量化指标衡量组织文化契合，作为转型判断依据之一。
- 不可直接迁移：约 21 年的公开博客记录构成的可观测性，本身依赖持续输出这一幸存条件，并非可独立迁移的机制。
- 不可直接迁移：2011 年 zynamics 团队整体加入 Google 的组织路径具有特定时空与收购背景，不可作为可复制的成长路径。
- 不可直接迁移：以 Bell Labs 背景资深同事为参照群体，依赖其进入 Google 后的特定同事结构，非普遍可得资源。
- 不可直接迁移：2015 年 Pwnie Awards 终身成就奖为特定行业评价，不可作为一般能力变化的因果依据。
- 不可直接迁移：Project Zero 关联、Recursion Pharmaceuticals 转向等节点均为二手转述或未核验线索，其作为成长阶段边界的条件不可迁移。

## 复核问题

- mechanisms[2].observed_outcomes 第2条（2026-03 把 SSH/screen 会话隔离、供应链攻击缓解等安全研究习惯应用于 LLM 编码代理工作流）与第3条（2025-05 起在博客连载神经网络内部机制学习与实验，引用 ReLU 激活模式、多面体、样条等文献）的支撑证据 r1-pub-vibecoding、r1-conv-vibecoding、r1-pub-neuralnets 在 evidence_json 中 verification.verified_in_run 均为 false，R1 节点自报未一手核验；observed_outcomes 字段语义为已观测结果，不应直接纳入未核验证据。本复核已独立 WebFetch 两个 permalink，事实层面术语原文存在，但 evidence 状态本身未升级，综合结论在 observed_outcomes 层面与 stages[2] capability_change 中'保留为资料缺口而非核心断言'的文本标注不一致。
- 字段 mechanisms[2].observed_outcomes：第2条与第3条的支撑证据（r1-pub-vibecoding、r1-conv-vibecoding、r1-pub-neuralnets）在 evidence_json 中 verified_in_run=false。改写方向：在 observed_outcomes 第2、3条末尾标注'（该条目支撑证据 permalink 在 R1 中未一手核验，verified_in_run=false，按资料缺口处理）'，使 observed_outcomes 字段层面与 stages[2] capability_change 中'保留为资料缺口而非核心断言'的标注一致；或将第2、3条移出 observed_outcomes，仅在 stages[2] 与 mechanisms[2].repeated_practice 中以 lead_only 口吻引用并保留 confidence=medium 的降级。原措辞'2026-03 把 SSH/screen 会话隔离、供应链攻击缓解等安全研究习惯应用于 LLM 编码代理工作流'与'2025-05 起在博客连载神经网络内部机制学习与实验，引用 ReLU 激活模式、多面体、样条等文献'以既定事实口吻陈述，未在该字段标注证据核验状态。
- 字段 tensions 第6条与 open_questions 第3条：照搬 R1 targeted_research unresolved 的'7 条主页来源证据未逐条补抓 permalink 升级'，未独立核对 evidence_json。改写方向：将范围由'7 条（conv-01、conv-02、conv-07、halvar-community-06、halvar-community-07、halvar-pub-05、halvar-ext-09）'修正为'6 条（conv-01、conv-02、conv-07、halvar-community-06、halvar-community-07、halvar-ext-09）'，移除 halvar-pub-05（其 source.url 已为 permalink 且 verified_in_run=true），并补一句'halvar-pub-05 的 permalink 与核验状态已升级，不计入本缺口'。原措辞'7 条主页来源证据……其 verification 仍指向旧主页 tool_use_id/content_sha256'与 evidence 实际状态不符。
- 字段 mechanisms[1].observed_outcomes、mechanisms[2].repeated_practice、stages[2].capability_change：嵌入英文短语 'AI slop'、'reasonably well' 未标注为引文。改写方向：首次出现处加引号并标注为引文，如'产生不可信根因与所谓「AI slop」（原文措辞）'、'使 LLM 崩溃归因「reasonably well」工作（原文措辞）'，或在叙述中改为中性中文表述并保留 short_quote 字段中的原文；'receipts' 在 stages/mechanisms/transferable_practices 多处出现，应在首次出现处标注其为引用术语，如'须提供「receipts」（证据，原文术语）'。原措辞以未标注方式混入英文短语，违反自撰字段语言规范。

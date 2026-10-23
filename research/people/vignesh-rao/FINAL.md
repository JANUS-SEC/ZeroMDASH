# Vignesh Rao：漏洞研究成长分析

- 擅长领域：浏览器与系统漏洞
- 独立复核：pass · 87/100

## 成长阶段

- **2019（研究期）；2020-02-24（发表） · V8 TurboFan patch-gapping 利用链与 1day 方法论**：confidence 语义声明：本阶段及后续阶段 confidence=high 指“技术内容可追溯性”，由四篇已核验 primary writeup 支撑，不含身份同一性确信；身份同一性见 tensions。与 István Kurucsai 合著，针对 Chromium V8 TurboFan InferReceiverMapsUnsafe 在 Proxy 拦截 JSCreate 原型访问时的副作用建模缺陷，构建完整利用链（DOUBLE-to-SMI 类型混淆 → addrof/fakeobj → TypedArray backing store 任意读写 → WASM RWX 写 shellcode）。文章系统阐述 patch-gapping 方法论：监控公开 chromium-review CL 与回归测试，按“simple but powerful-looking regression test, incorrect modeling of side-effects, easy to understand one-line change”筛选候选。自述发现补丁后约 3 日完成利用链（据 writeup 自述，无独立计时复核）；并依据 Chrome 改为双周/每周发布节奏判定 patch-gapping 路线不再可行，以“eulogy”表明收尾。（置信度：high）
  - 证据：VR-WORKS-01, vr-conv-1, vr-community-001, vr-decisions-01
- **2020（研究期，与 Martin Saar 协作）；2023-07-20（发表） · 由 V8 转向 JSC：FTL/B3 范围分析整数溢出根因审计**：沿用 stages[0] 声明：confidence=high 为技术内容可追溯性，不含身份同一性确信。研究目标由 Chrome/V8 迁移至 Apple WebKit/JSC 的 FTL JIT B3 强缩减阶段；由复用公开补丁（patch-gapping）转为直接审计 JIT 范围分析源码（B3ReduceStrength.cpp 的 rangeFor/shl），发现 IntRange::shl() 左移上界 0x7ffffffe 溢出变负且小于下界、computed range 与实际不符的整数溢出，DFG Integer Range Optimization 据此移除数组边界检查，得 JSC 堆上可控越界读写，经 ArrayWithDouble/ArrayWithContiguous 类型混淆得 addrof/fakeobj。研究期 2020（与 Martin Saar 协作）与发表期 2023-07 明确分离，时间线应按研究期而非发表期解读。（置信度：high）
  - 证据：VR-WORKS-02, vr-conv-2, vr-community-002, vr-community-006, vr-decisions-02
- **2023（研究）；2023-10-12/13 OBTS v6.0 演讲（Spain）；2023-12-11（发表） · JSC NaN-boxing 编码语义层审计与 ASLR brute-force 原语优化**：沿用 stages[0] 声明：confidence=high 为技术内容可追溯性，不含身份同一性确信。与 Javier Jimenez 合著，在同一 JSC 引擎内转向 NaN-boxing 编码语义层审计：boxDouble() 假定入参为合法 double 或纯 NaN，未校验结果溢出；以 Float64Array + BigUint64Array 视图写入“impure NaN”减 JSValue::NumberTag 溢出得高位清零全控值，JSC 解释为原始对象指针即 fakeobj。引入基于 JIT 编译 CompareStrictEq（x86 cmp）的 ASLR brute-force（穷举）原语，并利用 macOS/iOS JSC 堆地址恒为 5 字节（40 位）且页对齐的结构前提，以 0x1000 步进将 32 位穷举由 M1 上逾一小时降至秒级（约 4096x 提速，依赖上述结构前提，非具此结构的地址空间不可直接迁移）。研究期与发表期分离：2023 研究、2023-10 OBTS v6.0 演讲、2023-12-11 发表。（置信度：high）
  - 证据：VR-WORKS-03, vr-conv-3, vr-community-003, vr-community-005, vr-decisions-03, VR-NEW-R1-OBTS, VR-NEW-R1-CONF
- **2023（自主发现）；2024-01-16（补丁）；2024-01-19（发表） · 回到 V8/Maglev：二阶逻辑缺陷与 Ubercage 绕过**：沿用 stages[0] 声明：confidence=high 为技术内容可追溯性，不含身份同一性确信。与 Javier Jimenez 合著，回到 V8 但切换至较 TurboFan 更新的 Maglev 编译管线，处理 current_raw_allocation_ 状态管理这类二阶逻辑缺陷（TryBuildFindNonConstructorOrConstruct() 调用 BuildAllocateFastObject() 后未清 current_raw_allocation_，GC 移动对象致折叠分配越界写，转 type confusion 得 addrof/read/write）；绕过 Ubercage 沙箱，借含“raw 64 bit pointer ... store the starting address of the jump table”的 WebAssembly 实例对象指向 RWX 内存，并以 WebAssembly 浮点常量“interpreted as assembly code by jumping in the middle of some compiled wasm code”跳转执行 shellcode。自述为数月前自主发现的 V8 漏洞，标志由 patch-gapping 的 1day 复现转向自主 0day 发现与利用。多阶段原语（fakeobj→addrof→相对/绝对读写→代码执行）由 JSC 迁移至 V8 复用（基于两篇 writeup 技术内容的推断）。利用技术随 V8 防御机制（pointer compression 到 Ubercage）的更迭而调整。研究期与发表期分离：2023 自主发现、2024-01-16 补丁、2024-01-19 发表。（置信度：high）
  - 证据：VR-WORKS-04, vr-conv-4, vr-community-004, vr-decisions-04

## 主要成长机制

### patch-gapping 方法论：公开补丁作为研究输入

起点：2019 年两次 patch-gapping Chrome 的既有经验；Exodus Intelligence 研究环境与合著者 István Kurucsai；Chrome 当时发布节奏下安全补丁先于用户版本公开、回归测试可显著缩短利用开发时间的窗口。

练习与反馈：自述对 patch-gapping 这一主题至少进行三次系统研究（2019 年两次、本次一次），监控公开 chromium-review CL 与回归测试，按既定准则筛选候选（“simple but powerful-looking regression test, incorrect modeling of side-effects, easy to understand one-line change”）并完成端到端利用链。重复性判断仅基于已发表 writeup，未发表研究不可见。；利用开发耗时自述（约 3 日，据 writeup 自述，无独立计时复核）；Chrome 发布节奏改为双周/每周这一外部约束使该路线收益下降。

能力与结果：形成可复用的 1day 候选筛选准则与以公开补丁/CL 为输入的研究工作流，并据此评估研究路线的可行性与收益。；完整 V8 TurboFan InferReceiverMapsUnsafe 利用链（DOUBLE-to-SMI → addrof/fakeobj → 任意读写 → WASM RWX shellcode）；以“eulogy”公开判定 patch-gapping Chrome 路线不再可行并收尾，驱动后续向直接源码审计与 0day 发现的转向

置信度：high；替代解释：三次 patch-gapping 记录可能反映 Exodus 团队选题路线而非个人练习频度；“约 3 日”为 first-person 自述无独立复核，可能受记忆与叙述策略影响。

证据：VR-WORKS-01, vr-conv-1, vr-decisions-01

### JIT 编译器范围分析/编码语义根因审计

起点：stages[0] 在 V8 TurboFan 上以副作用建模为切入的利用经验；Exodus 平台与合著者网络。

练习与反馈：直接审计 JIT 编译器源码以发现 0day 类缺陷：stages[1] JSC FTL B3 IntRange::shl() 整数溢出（B3ReduceStrength.cpp rangeFor/shl）、stages[2] JSC NaN-boxing boxDouble() 溢出、stages[3] V8 Maglev current_raw_allocation_ 状态管理二阶逻辑缺陷。重复性判断仅基于已发表 writeup，未发表研究不可见。；三次均产出可利用的根因级发现，分别经 ArrayWithDouble/ArrayWithContiguous 类型混淆、fakeobj、越界写转 type confusion 完成利用。

能力与结果：在不同 JIT 编译管线（V8 TurboFan/Maglev、JSC FTL/B3）间定位范围分析、编码语义与状态管理缺陷的能力，从复用公开补丁转向自主根因审计。；JSC FTL/B3 整数溢出（stages[1]）；JSC NaN-boxing boxDouble 溢出 fakeobj（stages[2]）；V8 Maglev CVE-2024-0517 current_raw_allocation_ 越界写（stages[3]）

置信度：high；替代解释：三个根因级发现可能部分由 Exodus 研究选题路线与合著者贡献驱动，而非个人能力线性增长；2020-2023 公开输出空白期的实际研究量不可见。

证据：VR-WORKS-02, VR-WORKS-03, VR-WORKS-04, vr-conv-3, vr-decisions-02, vr-decisions-03, vr-decisions-04

### 多阶段原语跨引擎复用与防御绕过适配

起点：stages[0] V8 上 addrof/fakeobj + TypedArray backing store 任意读写 + WASM RWX 写 shellcode 的端到端原语链。

练习与反馈：在不同引擎上构造并复用多阶段原语（fakeobj → addrof → 相对/绝对读写 → 代码执行）：stages[1] JSC 经类型混淆得 addrof/fakeobj、stages[2] JSC 经 NaN-boxing fakeobj + JIT-cmp ASLR brute-force（穷举）、stages[3] V8 经越界写转 type confusion 并借 WASM 实例 jump_table_start 指向 RWX + shellcode smuggling 绕过 Ubercage。重复性判断仅基于已发表 writeup，未发表研究不可见。；各引擎防御机制（V8 pointer compression → Ubercage；JSC 堆地址结构）作为约束，倒逼原语与绕过方法的调整；利用技术随 V8 防御机制（pointer compression 到 Ubercage）的更迭而调整。

能力与结果：一套可在 V8/JSC 间迁移、随防御更迭适配的多阶段原语与沙箱绕过方法。；四篇 writeup 均达到代码执行或任意读写；stages[3] 显式绕过 Ubercage 并复用 WASM-RWX 原语；stages[2] 量化优化 ASLR brute-force 原语（约 4096x）

置信度：high；替代解释：跨引擎原语复用可能受同期公开研究（如 Samuel Groß Phrack 文章、LiveOverflow WebKit 系列，见 vr-community-006）影响而非纯个人积累；“复用”为基于两篇 writeup 技术内容的推断。

证据：VR-WORKS-01, VR-WORKS-02, VR-WORKS-03, VR-WORKS-04, vr-decisions-04

### 合著协作整理为公开技术记录

起点：2020 年首次公开输出即以合著形式（István Kurucsai）出现，能力构建与同伴协作耦合；Exodus Intelligence 作为发表渠道。

练习与反馈：与不同同伴分别推进并整理为公开 writeup/会议演讲：2020 Kurucsai（patch-gapping）、2020 Martin Saar（JSC 研究，2023 独著发表）、2023-2024 Javier Jimenez（连续三篇，含 OBTS v6.0 联合演讲）。重复性判断仅基于已发表 writeup，未发表研究不可见。；合著者配对稳定（Jimenez 跨三篇），会议演讲（OBTS v6.0，2023-10-12/13，Spain）作为写作之外的公开传播渠道。

能力与结果：将协作研究整理为公开技术记录与会议演讲的反馈回路，含研究期与发表期分离的延迟发表模式。；四篇 Exodus 博客 writeup（2020/2023x2/2024）；OBTS v6.0 联合演讲（2023-10-12/13，Spain）；研究期与发表期分离的延迟发表（如 2020 研究于 2023 发表）

置信度：medium；替代解释：合著与会议演讲频度可能反映 Exodus 团队发表策略与合著者可得性，而非个人协作能力的增长；OBTS v6.0 featured speakers 8 人不含二人，演讲事实仅由文章内嵌 YouTube 标题支撑，独立确认未取得。

证据：VR-WORKS-01, VR-WORKS-02, VR-WORKS-03, VR-WORKS-04, vr-conv-2, vr-community-001, vr-community-002, vr-community-003, VR-NEW-R1-OBTS, VR-NEW-R1-CONF

## 可迁移与不可迁移

- 可迁移：前提声明：以下可迁移实践所依托的能力归属受身份同一性推断前提限制（四篇 writeup 署名 Vignesh S Rao(2020)/Vignesh Rao(2023-2024) 为推断同一人，非独立确认；Exodus 博客首页署名作者列表不含该姓名、/author/vignesh-rao/ 404、OBTS v6.0 featured speakers 与 talks.html 完整名单均未独立锚定身份）。
- 可迁移：将公开补丁/CL/回归测试作为研究输入，按“simple but powerful-looking regression test, incorrect modeling of side-effects, easy to understand one-line change”等准则筛选 1day 候选。
- 可迁移：JIT 编译器源码根因审计路径（范围分析/编码语义/状态管理）可迁移至不同 JIT 引擎（该能力归属受上述身份推断前提限制）。
- 可迁移：多阶段原语（fakeobj → addrof → 相对/绝对读写 → 代码执行）的构造与跨引擎复用。
- 可迁移：以 JIT 编译指令（如 x86 cmp）实现 ASLR 穷举原语，并结合地址空间结构性质（如页对齐）做量化优化（提速依赖具体地址空间结构，需重新评估可迁移性）。
- 可迁移：协作研究 → 公开 writeup/会议演讲的发表回路（含研究期与发表期分离的延迟发表）。
- 不可直接迁移：Exodus Intelligence 机构资源与研究环境：发表渠道、合著者网络（Kurucsai/Saar/Jimenez）、选题路线；四篇 writeup 均挂 Exodus，能力发展与此机构语境耦合，非纯个人条件。
- 不可直接迁移：macOS/iOS JSC 堆地址 5 字节（40 位）且页对齐的结构：支撑 brute-force（穷举）ASLR 4096x 提速，非具此结构的地址空间不可复用。
- 不可直接迁移：Chrome 发布节奏由更长周期改为双周/每周：使 patch-gapping 路线收益下降的外部条件，为时期特定，驱动 stages[0]→[1] 的转向。
- 不可直接迁移：特定合著者关系（István Kurucsai、Martin Saar、Javier Jimenez）：协作机制依赖这些具体同伴的可得性与配对，非可任意迁移的个人条件。

## 复核问题

- stages[1].evidence_ids：可移除 vr-community-006（Groß/LiveOverflow 学习参考，inferred，与 FTL/B3 根因审计关联弱），保留 VR-WORKS-02、vr-conv-2、vr-community-002、vr-decisions-02；如保留应补注该条用途为学习参考侧反馈而非根因审计支撑。此为精简建议，非通过必要条件。
- tensions[0]：建议补充对『Exodus 博客首页署名作者列表不含该姓名』的替代解释讨论（首页列表可能仅含当前活跃作者或存在筛选），避免将该反证过度加权；维持『身份同一性仅为推断』的定性不变。此为表述克制建议，非通过必要条件。
- mechanism[2].feedback『倒逼原语与绕过方法的调整』与 mechanism[0].observed_outcomes[1]『驱动后续向直接源码审计与 0day 发现的转向』中『倒逼』『驱动』略带拟人色彩，建议改为『约束』『促使』等中性表述以与全篇语言规范一致。此为语言规范精修建议，非通过必要条件。

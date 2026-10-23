# 未通过定稿检查

已达到最大事实性修订次数 5；本文件是审计草稿，不得进入跨人物比较。

# Mark Brand：漏洞研究成长分析

- 擅长领域：浏览器与沙箱逃逸
- 独立复核：revise · 88/100

## 成长阶段

- **2015 · 起点：浏览器与移动端远程攻击面、API 设计手工审计与可靠性量化初现**：2015-02 以 Flash PCRE（CVE-2015-0318）漏洞利用作为最早可核验公开作品，确立逆向理解引擎实现→定位语义假设缺陷（缺 UTF8 模式检查）→堆 groom→OOB 写改写 Vector 长度→任意读写→ROP 的固定范式，并以完整利用链而非仅崩溃证明严重性；自述 'it took quite a while before I found a useful primitive'，体现重复试错而非天赋叙事；'Make zeroday hard.' 在首篇确立为贯穿后续十年的输出习惯（自号 'Irregular Expressionist'）。2015-07 'When int is the new short' 审计 Chrome IOBuffer 构造函数以 int 接收 size_t 导致整数截断的浏览器进程漏洞（byline 'Truncator of Integers'），体现其早期即建立手工审计 API 设计缺陷的研究路径。2015-09 Stagefright（CVE-2015-3864）选择该 bug 因赋予攻击者对 'the size of the allocation; the amount of overflow, and the contents' 三重控制，在 mediaserver 难以构造信息泄露的约束下对 8-bit ASLR 直接暴力枚举（1/256）而非追求信息泄露；'In 4096 exploit attempts I got 15 successful callbacks'、约 4%/分钟 成功率，确立 '可靠性是概率而非二元'、在可重试场景下接受低成功率的研究取向。2015-11 Samsung Galaxy S6 Edge 团队 bug bash 中发现 CVE-2015-7888（WifiHs20UtilityService 目录穿越，可写文件为 system 用户），由同事 Silvanovich 在 P0 博客中点名 'discovered by Mark Brand'，嵌入团队竞赛式高强度作业。（置信度：high）
  - 证据：mb-works-001, mb-r1-001, mb-works-002, mb-r2-005, mb_timeline_2015_07_iobuffer, mb_timeline_2015_09_stagefrightened, mb-dec-001-flash-pcre-start, mb-dec-002-stagefright-android-pivot, mb-ext-silvanovich-cve7888-2015, mb-community-2015-samsung-bugbash
- **2018 · 侧向选点：图形/GPU 回退路径与跨专长合著**：2018-07 与 Ivan Fratric 合著 'Drawing Outside the Box: Precision Issues in Graphic Libraries'（byline 'By Mark Brand and Ivan Fratric, Google Project Zero'），分工为 Brand 负责 SwiftShader、Fratric 负责 Skia，文末主动邀请读者在评论区补充同类精度漏洞案例，把读者变为补充语料来源，形成外部反馈回路。2018-10 'Heap Feng Shader: Exploiting SwiftShader in Chrome' 选择 SwiftShader 作为攻击面，因 GPU 进程 'needs to have more privileges than the highly-sandboxed renderer processes'，且 Chrome 在 GPU 加速失败 4 次后回退到 SwiftShader 故该面始终可达；方法论上明确提出 'look at things sideways — avoiding the perhaps more obvious and highly contested areas such as the main javascript JIT engine'，把目标选择从 '正面强攻 JIT' 转向 '横向寻找非显见子系统'，并通过可主动触发的环境降级（crash GPU 4 次）把 '非默认路径' 转化为 '可强制可达路径'，为 2019 沙箱逃逸链奠基。（置信度：high）
  - 证据：mb-r1-002, mb-dec-003-swiftshader-sideways, mb-community-2018-drawing-reader-feedback, mb-ext-fratric-coauthor-2018
- **2019-2020 · 完整沙箱逃逸链确立与'失败作为一等内容'的输出文体**：2019-04 发表 'Virtually Unlimited Memory: Escaping the Chrome Sandbox'，完成 Chrome 完整沙箱逃逸链：V8 typer 漏洞（_tsuro 提供 renderer exploit）→运行时开启 MojoJS 绑定→FileWriterImpl::Write UAF→约 3.5–4TB 共享内存映射喷洒填满浏览器进程虚拟地址空间以预测地址、绕过 ASLR→浏览器进程 ROP。选择沙箱逃逸而非 renderer 单点，因 'sandbox escape is the critical escalation step'；选 bug 以 'the high level of control the attacker has both over the lifetime of the free'd object, and over the timing of the later use' 为准则；ASLR 绕过放弃信息泄露、改用大内存喷射，利用 Windows 无跨进程 ASLR 与浏览器进程无地址空间上限两项设计缺口，体现 '创造性消除约束优于正面突破'。自号 'Exploit Technique Archaeologist'（挖掘/复活旧利用技术如 SkyLined MS04-040 大内存喷射风格），'Make zeroday hard.' 收尾。一手正文明文记载 'the v8 team have removed the BCE optimisation to make it harder to exploit such issues in the typer'。自建 MojoJS fuzzer 用于发现该批沙箱逃逸 bug。2020-02 与 Sergei Glazunov 合著 'Several months in the life of Project Zero' 系列（标题用 Unix ^W 退格梗自嘲），选 Chrome 网络栈因 'has been split out into a new service process, the implementation of strict sandboxing for that process isn't completed yet, so it's still a highly privileged attack surface'，捕捉 servicification 架构过渡窗口；研究由 Chrome 团队一封邮件触发，一名 Chrome 开发者推翻 P0 '已被服务端修复' 的假设并证明问题仍可在 Android 复现，P0 另提交临时缓解（加 CHECK）。叙事把失败、惰性与低级失误（'too lazy to set up a build environment'、'This was a major face-palm moment'）作为正文内容公开，定位为 'illustrate the difficulties that even experienced researchers sometimes face'，以 'persistence perhaps played more of a part here than wizardry' 替代天赋叙事。（置信度：high）
  - 证据：mb-works-005, mb-works-006, mb-conv-001, mb-conv-002, mb-conv-003, mb-dec-004-chrome-mojo-sandbox-escape, mb-dec-005-network-stack-transition-window, mb-r1-004, mb-r2-004, mb-r2-003, mb-community-2019-mojojs-bugtracker-output, mb-community-2020-several-months-external-feedback-loop, mb-ext-self-archaeologist-2019
- **2020-02 至 2020-08 · 可靠性从经验估算走向可量化评估；团队内'利用思路顾问'角色显现**：网络栈 exploit 可靠性定量分析，一手正文明确终值约 0.75 per run，首个倍率从 2/8 提升到 7/8，配合基于 cookie 的堆整理；自述仍需 2-3 次重试、每分钟级别一次，且明确 'not a satisfactory result'，可靠性不足以令人满意。该阶段除网络栈研究外，Natalie Silvanovich 在 WebRTC/Android Messenger 研究中点名征询 Brand 的利用思路：用 CVE-2020-6387 把指向 outgoing data 的指针低字节置零破 ASLR；Silvanovich 实际尝试后因可靠性放弃该路径，但其在攻坚阶段主动向 Brand 征集利用点子并于一手正文致谢，体现 Brand 在团队内承担 '利用思路顾问' 角色，其利用直觉被同伴当作可执行输入。（置信度：high）
  - 证据：mb-r3-001, mb-community-2020-silvanovich-cites-suggestion, mb-r4-001
- **2021-2023 · 从攻击演示转向防御评估方法论化与产业倡导**：2021-01 'In-the-Wild Series: Android Exploits' 逆向已捕获野外 Android exploit 链，对各变体赋 0–90% copy/paste 量化归因，从 '制造 exploit' 转向 '解读攻击者经济学与决策'，引入量化归因理解攻击者成熟度差异。2023-08 启动 MTE As Implemented 多部分系列（Part 1/2/3 + Summary），核心研究问题为 'whether it's possible to use this instruction set extension to implement effective security mitigations, or whether its use is limited to debugging/fault detection purposes'；建立三级缓解分类法（Soft mitigation='attacker pays a one-time cost'、Hard mitigation='cannot develop a bypass technique which is reusable between different vulnerabilities'、Solution='eliminates exploitability of a vulnerability or class'）加 known/unknown-tag bypass 与 reusability/fixability/bug-subset 维度；设 95% 可靠性阈值（CONFIG_HZ_250 下需约 0.2ms 完成），取代早期 4%/分钟的直觉估算，使 '缓解措施是否有效' 从主观判断转为可复现度量；结论为基于 async MTE 的缓解受限于 'soft mitigation'。2023-11 'First handset with MTE on the market' 提供 Pixel 8 MTE 落地指南（ADB setprop 三步将默认从 opt-in 改为 opt-out），自述 'I've been running my Pixel 8 with MTE enabled since release day'，以个人设备作为长期实验场为评估结论背书，定位为兑现 'long-standing promise'；拒绝 'silver bullet' 表述但肯定 'huge step forward'。种子笔记称 2025-2026 年无 Mark Brand 个人署名 P0 博客，本轮未独立核验；其时间与团队署名化（Naptime/Big Sleep）相邻但因果未证实，故本阶段不将未核验的产出缺失作为既定叙述纳入能力变化。（置信度：high）
  - 证据：mb-r2-002, mb-ext-itw-android-we-2021, mb-works-007, mb-dec-006-mte-method-pivot, mb-dec-007-mte-pixel8-delivery, mb-r2-001, mb-ext-mte-personal-device-2023, mb-community-2023-mte-summary-signoff, mb_timeline_2023_08_mte_part1
- **2024 · 方法论机器化：从手工变体分析到 LLM 辅助研究框架**：2024-06 与 Glazunov 合著 'Project Naptime: Evaluating Offensive Security Capabilities of Large Language Models'，把人类研究员方法论显式编码为五原则（Space for Reasoning / Interactive Environment / Specialised Tools / Perfect Verification / Sampling Strategy），主张 LLM 应复现人类研究员的系统性方法而非单次提示；选 'automated detection of unfuzzable vulnerabilities' 为切入点，把 LLM 用在传统工具盲区而非与 fuzzer 竞争；一手正文确含 'increased CyberSecEval2 benchmark performance by up to 20x from the original paper'。2024-11 列名 'From Naptime to Big Sleep' 团队成员（16 人，P0 × DeepMind），团队选变体分析为 LLM 入口，因它为模型提供 'concrete, well-founded theory' 起点从而 'remove[s] a lot of ambiguity from vulnerability research'；AI 发现 SQLite seriesBestIndex 栈缓冲下溢 'remained undiscovered after 150 CPU-hours of fuzzing'；团队坦承 'still in the research stage' 且 'a target-specific fuzzer would be at least as effective'，明确工具适用域不夸大；防御框架锚定 pre-release 发现使 'no scope for attackers to compete'。研究产出转为团队署名。2024-11 为最后已核验节点；2025-2026 个人署名产出是否锐减、断档或转向团队/DeepMind 协作署名无法用一手来源核验，留为缺口（见 open_questions）。（置信度：high）
  - 证据：mb-works-009, mb-dec-008-naptime-method-pivot, mb-dec-009-bigsleep-variant-analysis, mb-r1-003, mb-r5-001, mb_timeline_2024_11_big_sleep

## 主要成长机制

### 以'全链稀缺环节'为研究投入点，并在约束下创造性消除约束而非正面突破

起点：2015 Flash/Stagefright 已建立以完整利用链证明严重性的输出形态；早期面对 '8-bit ASLR 无信息泄露' 的约束，选择直接暴力枚举（1/256）而非开发信息泄露原语。

练习与反馈：反复把研究投入放在全链中稀缺环节——选择沙箱逃逸（'sandbox escape is the critical escalation step'）而非 renderer 单点 bug；选 bug 以 'the high level of control the attacker has both over the lifetime of the free'd object, and over the timing of the later use' 为评估准则而非 bug 表象；固定 UAF 利用起步动作（'I usually like to start the process of exploiting a use-after-free'）；面对 ASLR 无信息泄露的约束时，以约 3.5–4TB 共享内存映射喷洒填满浏览器进程虚拟地址空间，利用 Windows 无跨进程 ASLR 与浏览器进程无地址空间上限两项设计缺口，用环境结构弱点替代信息泄露原语。；一手正文明文记载 'the v8 team have removed the BCE optimisation to make it harder to exploit such issues in the typer'（mb-r1-004 一手核验，由 inferred/lead_only 升级为 documented/primary）；Glazunov 2021 在 Chrome typer 漏洞类分析中把 Brand 的 full-chain 作为 canonical 先例引用；Chrome 团队邮件推翻 P0 '已被服务端修复' 假设并促使重新校准；bug 报告与 exploit 作为可复用制品在 bugs.chromium.org（finder:markbrand）公开使他人能站在其工作之上。

能力与结果：把 '完整链' 确立为研究输出的标准形态；把 '沙箱逃逸' 识别为全链关键稀缺环节；形成 '约束消除优于正面突破' 的可复用决策模式。；2019 Chrome 完整沙箱逃逸链（V8 typer→MojoJS→FileWriter UAF→约 3.5–4TB 喷射→ROP）；V8 团队移除 BCE 优化（架构级而非点状响应）；2020 Chrome 网络栈 base::Unretained UAF 与临时 CHECK 缓解；团队内 '利用思路顾问' 角色（Silvanovich 2020 点名征询）

置信度：high；替代解释：V8 团队移除 BCE 优化可能是对整类 typer 漏洞的工程决策，未必专门回应 Brand 单篇 writeup，因果归属未单独证实；其 '沙箱逃逸' 专注也可能部分受 P0 团队目标分配驱动，而非纯个人偏好。

证据：mb-works-001, mb-works-005, mb-works-006, mb-conv-003, mb-dec-004-chrome-mojo-sandbox-escape, mb-r1-004, mb-r2-004, mb-community-2019-mojojs-bugtracker-output, mb-community-2021-glazunov-cites-priorart, mb-ext-glazunov-cite-2021, mb-ext-self-archaeologist-2019

### 侧向选点（look at things sideways）：攻击回退/过渡路径而非主引擎

起点：2015-2017 浏览器主战场（JIT、Flash）竞争激烈；GPU 进程 'needs to have more privileges than the highly-sandboxed renderer processes'。

练习与反馈：反复避开 'perhaps more obvious and highly contested areas such as the main javascript JIT engine'，转向非显见子系统：SwiftShader/GPU 回退路径、网络栈 servicification 过渡窗口、MojoJS 未审计 binding；通过可主动触发的环境降级（crash GPU 4 次）把 '非默认路径' 转化为 '可强制可达路径'；选择 '架构转型窗口'（servicification 已分进程但沙箱未完成）作为目标。；SwiftShader 因 Chrome GPU 加速失败 4 次后回退故始终可达，自验证可达性；'Drawing Outside the Box' 文末主动邀请读者补充同类精度漏洞案例，形成外部反馈回路；网络栈研究由 Chrome 团队邮件触发并推翻 P0 自身 '已被服务端修复' 假设，迫使重新校准。

能力与结果：形成 'look at things sideways' 启发式——攻击回退/过渡路径而非主引擎；把目标可达性从 '默认可达' 提升为 '可强制可达'。；SwiftShader/GPU 回退路径研究（Heap Feng Shader）；2018 与 Fratric 合著精度漏洞类研究；2019 沙箱逃逸链的图形/GPU 子系统奠基；2020 网络栈 servicification 过渡窗口研究

置信度：high；替代解释：'侧向选点' 也可能是 P0 团队分工（与 Horn 等同事避免主引擎重叠）的结果而非纯个人启发式；GPU/网络栈的高特权属性本身会吸引任何研究员，并非 Brand 特有。

证据：mb-r1-002, mb-dec-003-swiftshader-sideways, mb-dec-005-network-stack-transition-window, mb-community-2018-drawing-reader-feedback, mb-ext-fratric-coauthor-2018, mb-community-2020-several-months-external-feedback-loop, mb-r2-003

### 把研究过程的失败、惰性与低级失误公开作为一等输出内容

起点：多数安全 writeup 只展示成功路径；Brand 2019 已自述 'Having almost completely given up, we remembered one of the quirks' 的放弃—重启循环，并以 'Tired of staring at structure layouts in the debugger, time to consider any alternative' 表达反复调试后的切换。

练习与反馈：反复把研究过程的失败、死胡同、惰性、低级失误写成正文：'too lazy to set up a build environment'、'This was a major face-palm moment'、'we had made no progress at all'；把系列定位为 'illustrate the difficulties that even experienced researchers sometimes face'；用 'persistence perhaps played more of a part here than wizardry' 替代天赋叙事；以 'Apologies in advance for glossing over...' 等先发制人的省略致歉管理读者预期与写作范围。；内部自述反馈回路——把 '几乎放弃' 作为发现拐点的前奏；mb-r2-003 一手核验 Several months Part1 正文确实含 'too lazy to set up a build environment'、'face-palm'、'illustrate the difficulties that even experienced researchers sometimes face'、'persistence perhaps played more of a part here than wizardry'。

能力与结果：形成 'honest research journey' 文体——用失败作为一等内容替代干净的成功叙事；把对自身研究流程的诚实复盘作为对社区的示范。；2020 'Several months in the life of Project Zero' 系列（Part1/Part2）；网络栈研究叙事大量记录 pivot、死胡同与假设被推翻

置信度：high；替代解释：'失败叙事' 文体可能部分是 P0 团队（尤其与 Glazunov 合著）的共同风格而非 Brand 个人特有；公开失败也可能具有选择性——只公开已最终解决的失败路径，未解决的死胡同仍不可见。

证据：mb-conv-002, mb-r2-003, mb-r3-001, mb-community-2020-several-months-external-feedback-loop, mb-dec-005-network-stack-transition-window

### 从经验可靠性估算走向可量化评估框架

起点：2015 Stagefright 'In 4096 exploit attempts I got 15 successful callbacks'、约 4%/分钟为针对 8-bit ASLR 的局部直觉估算；2020 网络栈 exploit 自述 'not a satisfactory result'。

练习与反馈：反复对 exploit 可靠性进行定量分析并设定明确阈值：2020 网络栈把首个倍率从 2/8 提升到 7/8、终值约 0.75 per run、约 2-3 次重试、约每分钟一次，且自述不令人满意；2023 MTE 设 95% 可靠性作为攻击者目标参照点，量化需在约 0.2ms 内完成；建立 soft/hard/solution + known/unknown-tag bypass + reusability/fixability/bug-subset 分类法，使 '缓解措施是否有效' 从主观判断转为可复现度量。；网络栈可靠性 'not a satisfactory result' 的自我反馈（明确不令人满意，驱动继续整理）；MTE 评估为长期系列（4+1 篇）并经 ARM 预生产硬件访问与长期测量支撑，构成与硬件/平台团队的反馈回路；以个人 Pixel 8 长期运行 MTE 为评估结论背书。

能力与结果：把 '可靠性是概率而非二元' 从直觉估算升级为可量化评估框架；把 '缓解措施有效性' 形式化为可复用分类法。；MTE As Implemented 四部曲 + Summary（2023-08）；95%/0.2ms 阈值取代 4%/分钟直觉估算；Pixel 8 MTE 落地指南（ADB opt-in→opt-out）；网络栈 exploit 可靠性定量分析（0.75 per run、2/8→7/8）

置信度：high；替代解释：早期 '4%/分钟' 可能是 Stagefright 特定约束（8-bit ASLR）下的局部估算而非刻意方法论起点；MTE 量化阈值（95%/0.2ms）与分类法也可能借鉴既有防御评估文献，而非纯原创。

证据：mb-works-002, mb-r2-005, mb-r3-001, mb-works-007, mb-dec-006-mte-method-pivot, mb-dec-007-mte-pixel8-delivery, mb-r2-001, mb-ext-mte-personal-device-2023, mb-community-2023-mte-summary-signoff

### 把人类研究员方法论显式编码给 LLM（方法论工具化/输出化）

起点：长期手工变体分析与对 'fuzzing 在变体发现上局限' 的判断；2024 LLM 能力边界可评估，自 mid 2023 起与 DeepMind 合作。

练习与反馈：把自身研究习惯（verbose 推理、交互式纠错、专用工具、可确定性验证、多假设独立采样）抽象为五原则（Space for Reasoning / Interactive Environment / Specialised Tools / Perfect Verification / Sampling Strategy）；选 'automated detection of unfuzzable vulnerabilities' 为切入点，把 LLM 用在传统工具盲区而非与 fuzzer 竞争；选变体分析为 LLM 入口，因它为模型提供 'concrete, well-founded theory' 起点从而消除歧义；2020 Silvanovich 在攻坚阶段征询 Brand 利用思路（CVE-2020-6387 把指向 outgoing data 的指针低字节置零破 ASLR）并在一手正文中致谢，体现其 '利用思路顾问' 角色被同伴当作可执行输入。；一手正文确含 'increased CyberSecEval2 benchmark performance by up to 20x from the original paper'（mb-r5-001 一手核验，由 lead_only 转述升级为 primary 一手支撑）；Big Sleep AI 发现 SQLite seriesBestIndex 栈缓冲下溢 'remained undiscovered after 150 CPU-hours of fuzzing'；团队坦承 'still in the research stage' 与 'a target-specific fuzzer would be at least as effective'，明确工具适用域不夸大。

能力与结果：完成从 '重复练习中沉淀方法论' 到 '方法论工具化/输出化' 的元层跃迁；研究方法从个人习惯转为可结构化、可移交的产物；把 tacit practice 显式化为可复制框架。；2024 Project Naptime 五原则与 CyberSecEval 2 性能提升最多 20x；2024 Big Sleep 团队署名 AI 发现 SQLite 漏洞；研究产出转为团队署名（P0 × DeepMind 16 人）

置信度：high；替代解释：Naptime/Big Sleep 是 P0 × DeepMind 团队协作产物，五原则与变体分析选型可能反映团队共识而非 Brand 个人方法论；该机制的可观测样本（同事点名、benchmark 提升）全部来自已发表 Project Zero 官方博客，受发表偏倚限制，与 non_transferable_conditions 一致。

证据：mb-works-009, mb-dec-008-naptime-method-pivot, mb-dec-009-bigsleep-variant-analysis, mb-r1-003, mb-r5-001, mb_timeline_2024_11_big_sleep, mb-r4-001, mb-community-2020-silvanovich-cites-suggestion

## 可迁移与不可迁移

- 可迁移：把研究投入放在全链稀缺环节（如沙箱逃逸）而非 renderer 单点 bug，以 '攻击者对对象生命周期与重用时机的控制度' 作为选 bug 准则。
- 可迁移：在约束下优先创造性消除约束（如以大内存喷射利用环境结构弱点替代信息泄露原语），而非正面突破缓解。
- 可迁移：采用 'look at things sideways' 启发式，攻击回退/过渡路径而非主引擎；通过可主动触发的环境降级把 '非默认路径' 转化为 '可强制可达路径'。
- 可迁移：捕捉架构转型窗口（如 servicification 分进程但沙箱未完成）作为高特权且远程可达的研究目标。
- 可迁移：对 exploit 可靠性进行定量分析并设定明确阈值（如 0.75 per run、95%/0.2ms），把可靠性作为可论证的工程指标而非二元成败。
- 可迁移：把防御措施有效性形式化为可复用分类法（soft/hard/solution + bypass 可复用性/可修复性/漏洞子集），使主观判断转为可复现度量。
- 可迁移：把研究过程的失败、死胡同与低级失误公开作为一等输出内容，以诚实复盘替代天赋叙事。
- 可迁移：把自身研究方法论显式编码为可移交原则（如 Naptime 五原则），供工具或 AI 复现人类研究员的迭代假设-验证流程。
- 可迁移：以个人设备长期运行所评估的缓解措施，作为评估结论的可信度背书。
- 可迁移：诚实标注工具适用域、不夸大（如明确 'a target-specific fuzzer would be at least as effective'），把研究价值锚定在消除攻击者竞争窗口而非 CVE 计数。
- 不可直接迁移：发表偏倚与幸存者偏差：synthesis 的全部机制判断基于已发表 Project Zero 官方博客，未发表工作与主动放弃的研究方向不可见，所识别成长机制可能只反映被选择公开的成功路径，而非完整的研究决策谱系；mechanisms[4] 的可观测样本尤其全部来自 P0 官方博客同事点名。
- 不可直接迁移：P0 团队组织资源：ARM 预生产硬件访问、与 DeepMind 跨团队协作、bugs.chromium.org 发布渠道、Chrome 团队直接邮件反馈与临时 CHECK 缓解通道，非个人可复制。
- 不可直接迁移：同期 P0 同事网络（Forshaw、Beer、Hawkes、Silvanovich、Glazunov、Fratric、Horn 等）作为反馈回路与利用思路顾问角色的需求来源，非个人可单方面建立。
- 不可直接迁移：时代窗口与外部条件：Flash 仍是浏览器主战场（2015）、servicification 架构过渡（2020）、Pixel 8 首发量产 MTE（2023）、LLM 辅助研究能力可用（2024）等外部条件与个人努力耦合，离开对应窗口无法复现。
- 不可直接迁移：P0 团队署名机制（Naptime/Big Sleep 团队署名）使个人产出可见度下降，非个人可控制；2025-2026 个人署名产出是否锐减/断档无法核验。

## 复核问题

- stages[3]（period '2020-02 至 2020-08'）capability_change 含 '配合基于 cookie 的堆整理' 一句，该技术细节在 stages[3] 全部被引证据中均无支撑：mb-r3-001 的 claim 已将该一手正文（Several months Part 2）对网络栈 exploit 可靠性的定量表述明确限定为 0.75 per run 终值、2/8→7/8 首个倍率、约 2-3 次重试、约每分钟一次且自述不令人满意，并显式声明一手正文不含 0.375、不含 3%、不含 75%，且未记录任何 cookie 或堆整理技术；mb-community-2020-silvanovich-cites-suggestion 与 mb-r4-001 指向 WebRTC/Android Messenger 研究，与 Chrome 网络栈堆整理无关。该句构成无证据支撑的事实性技术细节，须删除或补证后保留。
- 删除 stages[3]（period '2020-02 至 2020-08'）capability_change 中的 '配合基于 cookie 的堆整理' 一句，或补充能在 Several months Part 2 一手正文中核验该堆整理技术细节的证据条目（claim 转录 + verified_in_run=true）后再保留；修订后该句应仅保留 mb-r3-001 claim 已显式确立的可靠性定量表述（0.75 per run 终值、2/8→7/8 首个倍率、约 2-3 次重试、约每分钟一次、自述 'not a satisfactory result'）。
- 修订 stages[5] capability_change 与 mechanisms[4].repeated_practice 中以引号引用的 'concrete, well-founded theory'：因被引证据 mb-dec-009 与 mb-r1-003 的 claim 均未转录该短语，请将该引号短语改写为非引文表述并仅保留已转录的 'remove[s] a lot of ambiguity from vulnerability research' 作为引证，或补充该短语在 Big Sleep 一手正文中的转录证据后再以引文形式保留。

# Man Yue Mo：漏洞研究成长分析

- 擅长领域：浏览器与 Linux 内核漏洞
- 独立复核：pass · 85/100

## 成长阶段

- **2020-04 至 2021-03 · Chrome 渲染器 GC/UAF 起点与利用链组装**：首篇可索引 writeup（mym-tl-01）即把自身工作置于 Project Zero 变体分析谱系内，引用 Sergei Glazunov 以 CodeQL 进行的变体分析与 Maddie Stone 的变体分析演讲作为分析框架；技术积累以浏览器引擎内存模型（以小内存分配在意外位置触发 Chrome 垃圾回收以制造 use-after-free）为起点。2021-03 将 2020 年分散报告的多个 Android/Chrome 漏洞逆向组合为一条完整利用链（mym-decisions-02、mym-tl-06），采用从最终目标倒推到各组件的方法，原文表述为 "worked our way back"（引文），把研究定位为对攻击归因叙事的校正而非单纯利用。（置信度：medium）
  - 证据：mym-tl-01, mym-decisions-01, mym-decisions-02, mym-tl-06, mym-tl-02, mym-tl-03, mym-tl-04, mym-tl-05
- **2021-03 至 2021-11 · 攻击面横向迁移至移动内核协处理器驱动，并以在野 0-day 复盘作为练习**：研究面从 Chrome 渲染器扩展到 Android 内核协处理器驱动（Qualcomm KGSL、NPU），开始组建跨组件 exploit chain（mym-tl-03/04/05、mym-pubtech-01）。同期连续两篇对据信在野利用的 Chrome 漏洞（CVE-2021-30632、CVE-2021-37975）做根因与利用复盘（R1-itw-cve2021-30632、R1-itw-cve2021-37975），形成以他人 exploit 为材料的反馈与练习行为。作者在 NPU 工作中以第一人称承认审计时漏看了 bug，并以 educated guesses 加 trial and error 描述对未知子系统的方法论探索（mymo-conv-01、mym-pubtech-01）。（置信度：medium）
  - 证据：mym-tl-03, mym-tl-04, mym-tl-05, mym-decisions-03, mym-pubtech-01, mymo-conv-01, mym-tl-07, mym-tl-09, mym-tl-10, R1-itw-cve2021-30632, R1-itw-cve2021-37975
- **2022-06 至 2023-04 · 可复用利用原语的产出与内核缓解对抗的并置**：首次发表把释放页重用作 GPU 页表全局目录（PGD）以实现任意物理内存访问的技术（mym-pubtech-03、mym-tl-13），原文称其 "does not involve the usual type of memory corruption"（引文），把研究视角从指针级内存破坏转到物理映射层，成为后续多年 Mali 工作的可复用原语。同期把利用与内核缓解机制对抗明确并列：既给出利用（CVE-2022-22057 在 Samsung Z Flip 3 上 root 与关闭 SELinux），也系统梳理缓解机制作为《The Android kernel mitigations obstacle race》（mym-tl-11）的标题指代——"障碍赛"为该来源 writeup 标题的标题指代，非本报告自撰的比喻性归纳。2023-04 以补丁差异发现 Mali 驱动 r40p0 遗漏安全补丁，在 Pixel 6 上实现内核 root（R1-tl-16-pwning-pixel6）。（置信度：medium）
  - 证据：mym-pubtech-03, mym-tl-13, mym-pubtech-04, mym-tl-15, mym-tl-11, mymo-conv-02, mym-tl-14, R1-tl-16-pwning-pixel6, mym-tl-16
- **2023-05 至 2024-03 · root cause → 变体方法论的显式化与首次 MTE bypass**：以 Jann Horn 披露的 Arm Mali 漏洞 CVE-2022-36449（Project Zero issue 2327）为起点，通过审查代码对 backing store 生命周期的隐含假设发现 CVE-2022-46395（mym-pubtech-05、mym-tl-17、mym-decisions-04），并把"对既有漏洞做根因分析并据此识别新变体"显式上升为可推广方法论。同期回到 V8 JIT 跨子系统边界（mym-pubtech-02 指出该类缺陷 "could not be found by fuzzing V8 alone"，引文），并跟踪 concurrent compilation 与 Maglev 等新层对安全假设的打破（mym-pubtech-06/07、mym-tl-18/19）。2024-03 在 MTE 启用的 Pixel 8 上以 Arm Mali 逻辑缺陷（CVE-2023-6241）获得内核代码执行并绕过 MTE（mym-pubtech-08、mym-decisions-05、mym-tl-20），把既有 Pixel 6 技术沉淀复用于 Pixel 8。（置信度：high）
  - 证据：mym-pubtech-05, mym-tl-17, mym-decisions-04, mym-pubtech-02, mym-pubtech-06, mym-pubtech-07, mym-tl-18, mym-tl-19, mym-pubtech-08, mym-decisions-05, mym-tl-20
- **2024-06 至 2025-05 · V8 对象模型持续产出与第二次 MTE bypass 迭代**：围绕 V8 对象属性重复与对象 transition 机制继续类型混淆利用，在 Chrome renderer 沙箱内实现 RCE（mym-tl-21/22）。2025-05 发表第二次 MTE bypass（CVE-2025-0072，mym-pubtech-11、mym-tl-23），复用 CVE-2023-6241 与 2022 年《Corrupting memory without memory corruption》的 PGD 重用思路，并显式对比前一次 MTE bypass 的差异（GPU 侧直接访物理内存 vs 用户态页表直接插入页帧）。能力变化为跨三年自我技术沉淀的系统化复用，而非孤立成果。需注意：六维证据 mym-tl-23 的 claim 字段含"Android 2023-05"年份笔误，定向补证 R1-tl-23-verify 正文原文为 "included in Android's May 2025 security update"（引文），实际为 Android 2025-05 安全更新；本报告一律以 2025-05 为准。（置信度：high）
  - 证据：mym-tl-21, mym-tl-22, mym-pubtech-11, mym-tl-23, R1-tl-23-verify, mymo-conv-03, mymo-conv-04
- **2026-01 至 2026-03 · 向 AI 辅助研究工具建设转向**：与 Peter Stöckli 合著《AI-supported vulnerability triage with the GitHub Security Lab Taskflow Agent》（mym-pubtech-12、mym-tl-24、mym-decisions-06）与《How to scan for vulnerabilities with GitHub Security Lab's open source AI-powered framework》（mymo-conv-05、mym-tl-25），把手工 triage 经验编码为可复用 AI 工具并开源。据作者自述（mym-pubtech-12 正文，未经独立核验），Taskflow Agent 自 2025-08 起处理大量告警并发现约 30 个真实漏洞，研究者仍逐一复核输出后再报告；该转向为渐进式而非一次性切换——2025-05 仍发布传统 MTE 绕过研究。能力变化为将重复性初筛交由工具、把人力集中于人工核验，研究范围从特定漏洞类型扩展到更通用的扫描框架。（置信度：medium）
  - 证据：mym-pubtech-12, mym-tl-24, mym-decisions-06, mym-decisions-07, mymo-conv-05, mym-tl-25, mym-ext-02

## 主要成长机制

### 以既有公开漏洞根因为起点、搜索同假设变体（root cause → variant）

起点：2020-04 首篇 writeup 即把自身工作置于 Project Zero 变体分析谱系内（mym-tl-01 引用 Sergei Glazunov 的 CodeQL 变体分析、Maddie Stone 的变体分析演讲）；具备可读到的 Project Zero 公开漏洞报告与 patch-diff 输入。

练习与反馈：以既有公开漏洞（CVE-2022-36449 等）为起点，审查访问内存区 backing store 生命周期的隐含假设，再搜索隐式假设该语义的其它代码路径以发现变体（mym-pubtech-05、mym-tl-17）；以补丁差异比对 Mali r40p0 发布与既有补丁发现遗漏修复（R1-tl-16-pwning-pixel6、mym-tl-16）；对在野 0-day 做根因与利用复盘作为同源练习（R1-itw-cve2021-30632、R1-itw-cve2021-37975）。；新发现以 writeup 形式公开反馈给社区（mymo-community-p0-variant-feedback-2023 描述的"阅读公开研究—提取方法—发现 variant—回馈社区"闭环）；作者自述偏好可靠、确定性触发（mymo-conv-04 原文 "I'd like to be able to replace the backing page reliably"，引文），以工程可靠性作为对变体有效性的内部反馈。

能力与结果：把单个漏洞抽象为可被搜索的变体模式，形成从个案到方法的能力；能够区分"真正的新根因"与"同假设的变体"。；CVE-2022-46395 作为 Project Zero issue 2327 的变体被定位，2022-11-17 报告 Arm（mym-pubtech-05、mym-tl-17）；以补丁差异发现 Mali 驱动 r40p0 遗漏安全补丁，在 Pixel 6 上实现内核 root（R1-tl-16-pwning-pixel6，primary 级正文支撑）；CVE-2025-0072 作为既有 GHSL-2023-005 类思路的变体（把 IOCTL_MEM_COMMIT 收缩改为 GPU page fault 扩展）（mym-pubtech-08、mym-pubtech-11）

置信度：high；替代解释：变体分析与自引前作在本报告中被归因为研究方法，但同一作者在系列 writeup 中保持叙事连贯也可能是一种写作策略；自引行为不必然等于能力沉淀。本报告以作者跨三年对同一原语（PGD 重用、AIO/SLUB）在不同漏洞中的可核验复用作为区分依据，而非单凭自引文本。

证据：mym-tl-01, mym-pubtech-05, mym-tl-17, R1-tl-16-pwning-pixel6, mym-tl-16, R1-itw-cve2021-30632, R1-itw-cve2021-37975, mymo-community-p0-variant-feedback-2023, mymo-conv-04, mym-pubtech-08, mym-pubtech-11

### 把已得手利用技术沉淀为可复用原语并跨年自引

起点：2022-07 首次发表把释放页重用作 GPU 页表全局目录以实现任意物理内存访问的技术（mym-pubtech-03、mym-tl-13）；具备 Arm Mali ioctl 与 kbase_mem_pool 分层池机制的内核代码理解基础。

练习与反馈：把 PGD-reuse、AIO 与 SLUB 分配器操控、JIT spraying 等技术明确作为后续研究的可复用构件：2022《Corrupting memory without memory corruption》产出 PGD-reuse，2023《The code that wasn't there》产出 AIO GFP_HIGHUSER 页重用，2023-05《Rooting with root cause》自引这两项作为可复用原语（mym-pubtech-04、mym-pubtech-05），2024 与 2025 两次 MTE bypass 均复用 PGD 重用思路（mym-pubtech-08、mym-pubtech-11）。；后续 writeup 显式自引前作并对比技术差异（如 2025-05 对比 GPU 侧直接访物理内存与用户态页表插入页帧两种 MTE bypass 路径），以"前作能否在新缓解下复用"作为对该原语稳健性的反馈。

能力与结果：形成可复用知识体系：把单次利用经验抽象为可在新设备、新缓解下重新组装的底层原语，而非每次从基础重新构建利用链。；PGD-reuse 原语跨 2022、2024、2025 三年被自引复用于 Mali 利用（mym-pubtech-03、mym-pubtech-08、mym-pubtech-11）；2024-03 复用 Pixel 6 技术沉淀于 Pixel 8 实现 MTE bypass（mym-decisions-05、mym-pubtech-08）；JIT spraying 被用于绕过 V8 heap sandbox（mym-pubtech-06、mym-pubtech-07）

置信度：high；替代解释：自引前作可能部分源于同一作者在系列 writeup 中保持叙事连贯的写作策略，而非能力沉淀；但跨设备（Pixel 6 → Pixel 8）、跨缓解（无 MTE → MTE）的实际复用结果提供了写作策略之外的独立支撑。

证据：mym-pubtech-03, mym-tl-13, mym-pubtech-04, mym-pubtech-05, mym-pubtech-08, mym-pubtech-11, mym-pubtech-06, mym-pubtech-07, mym-decisions-05, mymo-conv-02

### 追踪上游新组件/新特性如何打破既有安全假设并作为新攻击面

起点：2022-06 V8 SuperIC 工作指出该类缺陷 "could not be found by fuzzing V8 alone"（mym-pubtech-02，引文），确立跨子系统边界审计取向；具备 V8↔Blink 跨子系统代码阅读基础。

练习与反馈：及时跟进上游新引入组件并对"新特性是否破坏先前安全假设"做跟踪复盘：concurrent compilation 使 StackCheck 节点的 side effect 属性失效（mym-pubtech-06 原文 "the side effect property of the StackCheck node has become incorrect due to the introduction of concurrent compilation"，引文）；Maglev（Chrome 114 默认启用）作为新 JIT 层引入未初始化对象问题（mym-pubtech-07 原文 "with different tiers of optimizations in Chrome, the same functionality often needs to be implemented multiple times"，引文）；Mali CSF queue 重绑定打破 queue->phys 不可变假设（mym-pubtech-11）；MTE 作为新缓解被作为正面挑战目标（mym-pubtech-08、mym-decisions-05）。；上游 patch-diff 与 changelog 作为"何处假设被改写"的输入；新组件的引入时点（如 Maglev 默认启用）作为切入时机的反馈。

能力与结果：形成对新组件/新特性打破既有安全假设的预判能力，把"新层重复实现易丢失安全检查"归纳为可复用 bug 模式。；CVE-2023-3420 TurboFan StackCheck 侧效应建模错误（mym-pubtech-06）；CVE-2023-4069 Maglev 未初始化对象（mym-pubtech-07，该篇另自引 POC2022 关于预测 V8 对象地址的工作，属自引前作而非原语生产）；MTE 作为新缓解被两次正面绕过（mym-pubtech-08、mym-pubtech-11）；作者对攻击面趋势的公开预判：原文 "I expect coprocessors and their kernel drivers to continue to be a powerful attack surface"（mym-decisions-05，引文）

置信度：high；替代解释：新组件跟踪可能与上游发布节奏的可见性强相关（Maglev 默认启用、Pixel 8 支持 MTE 均为公开事件），机会窗口的把握部分依赖平台可用性与发布时机，而非纯个人能力。

证据：mym-pubtech-02, mym-pubtech-06, mym-pubtech-07, mym-tl-18, mym-tl-19, mym-pubtech-08, mym-pubtech-11, mym-decisions-05

### 把运行时异常与意外数据作为审计的补充输入

起点：2021-11 NPU 工作中作者以第一人称承认审计时漏看了 bug，并以 educated guesses 加 trial and error 描述对未知子系统的方法论探索（mymo-conv-01、mym-pubtech-01 原文 "I missed the bug completely when I audited the code"，引文）；运行时数据异常先于静态审计触发发现。

练习与反馈：把运行时反常作为追查入口：NPU 工作中 info leak 在审计时被漏掉，由运行时数据异常触发（mym-pubtech-01）；2023-02 Adreno/KGSL 工作发现路径为调试异常——GPU 命令日志出现未发送的 opcode，经 usleep 延迟线索进入追查（mym-pubtech-04 原文 "The fact that an opcode that is not in the command buffer appears in the kernel log seems to indicate that the GPU is seeing something that I don't see"，引文）。；运行时数据与静态审计之间的差异本身作为反馈：审计盲点由运行时异常暴露后，作者以复盘形式公开记录盲点（"missed the bug completely"）。

能力与结果：形成"静态审计 + 运行时异常"双输入的审计习惯，降低单一通道盲区。；CVE-2021-1940/1968/1969 NPU 三缺陷经运行时异常补漏发现（mym-pubtech-01）；CVE-2022-25664 Adreno/KGSL 经调试异常发现 GPU 读取陈旧物理内存（mym-pubtech-04）

置信度：medium；替代解释：运行时异常的捕获依赖具体设备的调试可访问性与偶然性（Adreno 工作自称进入"rabbit hole"），不完全是可稳定复现的方法；样本量集中于两篇 writeup，重复性证据偏弱。

证据：mym-pubtech-01, mym-pubtech-04, mymo-conv-01

### 将手工 triage 经验编码为可复用 AI 工具并开源

起点：多年 writeup 中积累的伪阳性判别模式（特权上下文检查、不可达 source、自定义 sanitize 等）此前仅以人工经验形式存在；2026 年起与同事 Peter Stöckli（GitHub Security Lab 成员，mym-ext-02 团队页可证）进入协作模式。

练习与反馈：把手工 triage 经验编码为 YAML 定义的 taskflow 规则交由 LLM 执行，对 CodeQL 告警进行分流、去伪与生成 GitHub Issue；据作者自述（mym-pubtech-12 正文，未经独立核验），taskflow 规则原文 "chosen based on our own experience of triaging these types of alerts"（引文），研究者仍逐一复核输出后再报告；随后把框架从分诊推进到扫描发现阶段并开源（mymo-conv-05、mym-tl-25）。；以 writeup 形式公开反馈工具效果与局限：据作者自述（mym-pubtech-12 正文，未经独立核验），自 2025-08 起处理大量告警并发现约 30 个真实漏洞；作者完整记录误报需人工筛选的局限（mymo-conv-05 原文 "Would it become too conservative"，引文）。

能力与结果：把个人 triage 经验转化为可复用知识体系与可协作的工具产物，研究范围从特定漏洞类型扩展到更通用的扫描框架。；2026-01《AI-supported vulnerability triage with the GitHub Security Lab Taskflow Agent》发表（mym-pubtech-12、mym-tl-24）；2026-03《How to scan for vulnerabilities with GitHub Security Lab's open source AI-powered framework》开源框架发表（mym-tl-25、mymo-conv-05）；据作者自述（未经独立核验），在电商 cart 逻辑与 Rocket.Chat 中发现系统性问题并报告 80+ 漏洞（mymo-conv-05）

置信度：medium；替代解释：AI 工具转向的时间点（2026-01 起）与 LLM 工具化行业趋势高度重合，可能部分受平台/机构资源与同行协作（Stöckli 合著）驱动，而非纯个人能力延伸；"约 30 个真实漏洞"与"80+ 漏洞"均为作者自述，未经独立核验。

证据：mym-pubtech-12, mym-tl-24, mym-tl-25, mym-decisions-06, mym-decisions-07, mymo-conv-05, mym-ext-02

## 可迁移与不可迁移

- 可迁移：以既有公开漏洞的根因分析为起点，审查代码中对同一资源生命周期的隐含假设，再搜索隐式承继该假设的其它路径，作为发现变体的可推广方法（mym-pubtech-05、mym-tl-17）。
- 可迁移：以补丁差异比对厂商发布与既有补丁，发现遗漏或不完整修复（R1-tl-16-pwning-pixel6）。
- 可迁移：把单次利用中得手的技术抽象为可在新设备、新缓解下重新组装的底层原语，并显式自引以维持技术线连续性（PGD-reuse 跨 2022/2024/2025 复用，mym-pubtech-03/08/11）。
- 可迁移：把运行时异常与静态审计作为双输入，降低单一通道盲区（mym-pubtech-01、mym-pubtech-04）。
- 可迁移：把手工 triage 经验编码为可复用工具并开源，将重复性初筛交由工具、人力集中于人工核验（mym-pubtech-12、mymo-conv-05）。
- 可迁移：在 writeup 中完整记录工具与方法的局限（如误报需人工筛选），而非仅展示成果（mymo-conv-05）。
- 不可直接迁移：Pixel 6、Pixel 8 等特定设备及其 Mali 驱动版本（r40p0、r42p0、r54p0）的可获得性，是相关 Mali 利用与 patch-diff 分析的物质前提，非研究方法本身可替代（R1-tl-16-pwning-pixel6、mym-pubtech-08、mym-pubtech-11）。
- 不可直接迁移：MTE bypass 依赖 Pixel 8 为当时少数支持 MTE 的设备这一市场条件（mym-decisions-05），设备与缓解的可用性属外部条件而非个人能力。
- 不可直接迁移：AI 工具转向与同事 Peter Stöckli 的合著协作及 GitHub Security Lab 的机构资源相关（mym-ext-02、mym-pubtech-12），团队协作与机构资源为个人难以复制的条件。
- 不可直接迁移：上游新组件（Maglev 默认启用、Mali CSF）的引入时机由厂商发布决定，研究者对切入时机的把握部分依赖发布可见性而非纯个人能力（mym-pubtech-07、mym-pubtech-11）。
- 不可直接迁移：本归纳受单一公开平台（github.blog/author/mymo/）可见性限制：X 账号、会议 speaker 页面、邮件列表与代码仓库均未取得一手抓取，能力归纳存在幸存者偏差。

## 复核问题

- stages[4]（2024-06 至 2025-05）evidence_ids 中 mymo-conv-03（2023-01-23）与 mymo-conv-04（2023-05-25）的时点落在 stage 2/3 区间，与该 stage『V8 对象模型持续产出与第二次 MTE bypass 迭代』的 capability_change 直接关联较弱。建议将这两条自述移至其所属时点的 stage，或在 stage 文本中说明此处系作方法论回溯引用而非该阶段新证据；同时复核 stages[4].confidence=high 是否仍由 reported 级 mym-tl-21/22 单独支撑 V8 子结论，必要时补限定语或下调。
- mechanisms[3].alternative_explanation 中『Adreno 工作自称进入 rabbit hole』措辞缺乏 mym-pubtech-04 正文级直接引文支撑（该词仅出现在六维 growth_signal 转述）。改写方向：将『自称进入 rabbit hole』改为据 evidence growth_signal 转述作者该阶段发现路径含探索性试错，或删去评价性表述仅保留『该阶段发现路径依赖具体设备调试可访问性与偶然性』这类可核验描述。
- mechanisms[0].feedback 中括注的『回馈社区』为六维 growth_signal 转述用语，略带评价色彩。建议统一改为『以 writeup 形式公开反馈给社区』，与 RV8 已执行的『回吐社区』改写保持一致。

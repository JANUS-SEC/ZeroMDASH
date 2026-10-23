# Jann Horn：漏洞研究成长分析

- 擅长领域：Linux 内核与系统漏洞
- 独立复核：pass · 90/100

## 成长阶段

- **2014-07 至 2016-06 · 入场：P0 制度起点与首篇方法论签名**：P0 于 2014-07-15 成立，确立强制 90 天披露 + 完整 PoC 公开的制度约束（documented）；Horn 不晚于 2016-06-20 发布首篇已核实博文。首篇即在 Linux 内核 VFS/ecryptfs/procfs 叠加场景确立'代码审计 + 实验验证（非 fuzzing）'的方法论底色，识别出 ecryptfs 选择更高效的 VFS read handler 而非 mmap handler 来处理页错误、绕过'不可映射文件不应被 mmap'约束这一设计交互，完成 root 利用并主动向 kernel security list 提结构性修复方向（guard pages + 移除 thread_info）。首篇以 'Make zeroday hard.' 收束，确立贯穿后续的输出锚点与责任框架（P0=发现/演示者，缓解实施交给上游）。加入 P0 的精确月份为资料缺口。（置信度：high）
  - 证据：jh-dec-01-join-p0, jh-tl-01-p0-founded, jh-tl-02-first-post, jh-works-01-recursion-2016, jh-comm-003, jh-comm-008
- **2017-01 至 2017-04 · 虚拟化边界跃迁与原语组合升级利用工程**：研究粒度从 Linux 内核栈边界升至 Xen hypervisor/物理内存边界（PV guest 与 hypervisor 共享虚拟地址空间，access_ok 是唯一软件屏障）。根因为 Xen access_ok() 只校验起始地址而非整段范围，PV guest 可经 memory_exchange() 写入 hypervisor 物理内存逃逸至 dom0。新增'原语组合升级'利用工程范式：把'写一个随机字节后跟 7 字节垃圾'的弱原语，通过反复写随机字节并读回直到正确、再连续写入升级为受控 9 字节写，覆写 level-3 页表项。确立'最底层可完整建模边界'研究偏好与'以 As far as I can tell 精确标注对历史优化提交的推测性归因'的诚实限定习惯。（置信度：high）
  - 证据：jh-works-02-xen-2017, jh-tl-03-xen-escape
- **2017-06 至 2018-01 · CPU 微架构侧信道范式级跃迁与协调披露**：从软件漏洞利用转入 CPU 微架构侧信道。研究方法为实验驱动的经验性逆向工程：以既有学术工作（Evtyushkin 等关于 BTB 滥用）为起点，初次 BTB 注入成功率低于 1% 后转向自建 userspace 测试用例经验性探测黑盒（逐位翻转分支、移动代码位置、改变分支数量推断 BHB 更新函数与 BTB 别名行为），而非从零理论建模。理论失效时坦诚标注（prefetch 指令破坏攻击称 'we have no clue why'）。2017-06-01 向 Intel/AMD/ARM 报告三变体，2018-01-03 联合公开，协调窗口约 7 个月（~216 天），远超 P0 标准 90+30 天政策。Variant 3 为事后补充发现（初始判断 unlikely 后被实验推翻）。学术圈以独立发现者署名承认（Meltdown 三组之一、Spectre 两方之一）。形成中间能力：面对不透明系统时不假装全知，逐项标注未分析/未成功/无解，并把缓解设计责任推给厂商。（置信度：high）
  - 证据：jh-works-03-spectre-2018, jh-conv-spectre-entrypoint-2018, jh-conv-spectre-honesty-2018, jh-conv-spectre-disclosure-2018, jh-comm-001, jh-comm-007, jh-dec-02-spectre-report, jh-dec-03-spectre-embargo-7months, jh-dec-04-spectre-disclosure-early, jh-dec-05-spectre-attribution-generous, jh-ext-01, jh-ext-02, jh-ext-04, jh-tl-04-spectre-reported, jh-tl-05-spectre-disclosed, jh-tl-06-meltdown-spectre-attribution
- **2018-09 至 2019-01 · 回归内核内存/竞争窗口与对手时间线思维固化**：从 CPU 微架构回归 Linux 内核内存管理。CVE-2018-17182（per-thread VMA 缓存序列号回绕致 UAF）以手工代码审计 + git 历史追溯定位 kernel 3.16 引入的单线程优化假设，穷举 4 种重用已释放 vm_area_struct 方案逐条否定，导出 BPF maps 经 page-allocator 的唯一可行路径；批评 WARN_ON_ONCE 替换 BUG_ON 为'半步修复'。CVE-2018-18281（mremap 与 ftruncate 竞争致陈旧 TLB）以 busy-polling VmPTE 实验驱动探测，在 Pixel 2（4.4 旧内核，Dirty-PTE 缓解缺失）上注入 zygote，理论预测单次覆写足够但实践失效时坦诚承认并转重试循环。固化'对手时间线思维'：以'用户何时真正受保护'而非'补丁何时发布'为评估终点，映射 commit→稳定版→发行版 backport→用户安装的四步管线。接受同事 Mark Brand 的技术反馈简化利用路径（省去 CR4 翻转）。主动归功 kernel security team 发现自己漏掉的竞争窗口（此条 lead_only 未一手核实，仅作辅助，阶段支撑以 verified 项为准）。（置信度：high）
  - 证据：jh-works-04-cache-invalidation-2018, jh-works-05-tlb-mremap-2019, jh-conv-cache-collaboration-2018, jh-conv-tlb-credit-2019, jh-comm-002, jh-comm-005, jh-comm-006, jh-ext-05, jh-tl-07-cache-invalidation, jh-tl-08-tlb-mremap
- **2019-02 至 2022-03（空窗期） · 第一段约3年公开输出空窗**：首篇 TLB 博文之后至 2022-03 race window 博文之前，存在约 3 年无已核实 Horn 署名 P0 博文的公开输出空窗（status=inferred，archive 全量核对的高可信度负面证据，抓取本身 verified_in_run=true）。空窗期内具体工作内容（内部 0day RCA、内核加固倡议或转向非公开研究）在公开来源中无法核实，标为资料缺口，不臆测填补。空窗本身是公开作品节奏的中断信号，与 2022 年回归之作的技术连续性（仍是内核竞争窗口）对照，提示空窗期内技术方向未发生范式跃迁，但此连续性推断不能替代内部工作的直接证据。（置信度：medium）
  - 证据：jh-works-06-public-gap-2019-2022
- **2022-03 至 2022-03 · 复出：竞争窗口扩窗工程化**：时隔约 3 年复出，方向回到 Linux 内核竞争窗口。UNIX 域套接字 SCM_RIGHTS 垃圾回收窄竞争（__fget_files() 与 unix_gc() 之间窗口）的扩窗技术从'经验性重试'升级为系统化组合工程：cache miss + hardware timer 中断（timerfd 在 hardirq 上下文）+ epoll 50k waitqueue churn，并以'单线程对硬件定时器竞争而非双线程互竞'范式降低时序抖动，命中率约 30%。致谢 P0 同事 Xingyu Jin、Xen 安全团队、Anders Fogh 博客、Gamazo Labs 'Sushi Roll' 指令级时序分析，主动让功给多方概念来源。展现'复杂安全规则同时击败人和 fuzzer'论点与'用硬件行为扩窗'的实验驱动探测。（置信度：high）
  - 证据：jh-works-07-race-window-2022, jh-tl-10-race-window
- **2022-04 至 2025-08（第二段空窗） · 第二段约3年公开输出空窗**：2022-03 race window 博文之后至 2025-08 MSG_OOB 博文之前，第二个约 3 年公开输出空窗（status=inferred，archive 全量核对，抓取 verified_in_run=true）。与第一段空窗叠加，2022-2025 期间 Horn 公开 P0 输出显著减少。空窗期内具体工作未核实，标为资料缺口。2025 年回归连发 3 篇博文，方向为 Linux 内核利用 + 逻辑型信息泄漏 + 补发历史虚拟化草稿，而非继续 CPU 微架构侧信道方向，表明空窗后研究方向发生部分调整，但调整的内部动因无公开解释。（置信度：medium）
  - 证据：jh-works-08-public-gap-2022-2025
- **2025-08 至 2025-12 · 三线密集复出：内核利用+逻辑型泄漏+虚拟化补发**：2025 年 8-12 月连发 3 篇 P0 博客，方向回归 Linux 内核利用并开拓逻辑型信息流。CVE-2025-38236（MSG_OOB UAF）从 Chrome renderer 沙箱达内核完成端到端利用：semi-arbitrary read 原语先行→用 CONFIG_RANDOMIZE_KSTACK_OFFSET 反转栈随机化把释放页重分配为内核栈页→sendmsg 注入受控假 SKB 延迟 UAF 写→越界 copy_from_user 覆写页表→映射内核内存可写。研究缘起是 review 新内核特性偶然发现 MSG_OOB（'几乎只在 Oracle 产品用却在 Chrome 沙箱暴露'），并公开记录多条失败与自我纠正（'Clearly trying to target a heap object was foolish'）。pointer leaks 为新型逻辑型信息泄漏（无内存安全违规、无时序），用 CRT 数学化推导完整 64-bit 指针恢复，因未证明 real-world impact 选择不进 P0 bugtracker 直接私下报告 Apple。VirtualBox 补发 2017 年草稿（CVE-2017-3558），写作完成度优先于时间新鲜度（拖延 8 年也不发布半截技术故事）。整合'读原语先行引导写原语'、'缓解反转利用'、'概率性缓解在可重试时失效'、'新技术+暴露面错配'多条反复论点进单条端到端链。（置信度：high）
  - 证据：jh-works-09-msgoob-2025, jh-works-10-pointer-leaks-2025, jh-works-11-virtualbox-2025, jh-conv-msgoob-failures-2025, jh-conv-vbox-deferred-2025, jh-comm-004, jh-dec-06-apple-no-bugtracker, jh-dec-07-virtualbox-8year-delay, jh-dec-08-msg-oob-target-selection, jh-dec-09-2025-triple-direction-shift, jh-tl-12-msg-oob, jh-tl-13-pointer-leaks, jh-tl-14-virtualbox-draft

## 主要成长机制

### 代码审计 + 实验验证（非 fuzzing）作为找 bug 入口

起点：P0 制度提供全职漏洞研究职位与 90 天披露约束；首篇（2016 ecryptfs）即确立此入口，面对多文件系统叠加语义与内核栈/guard page 布局需逐层代码审计而非覆盖率驱动。

练习与反馈：跨 2016→2025 全时期、跨 Linux 内核/Xen/Spectre/TLB/MSG_OOB/pointer leaks/VirtualBox 多方向重复：手工审计代码 + git 历史追溯定位优化假设，再以实验（busy-polling VmPTE、逐位翻转分支、自建 userspace 测试用例、Pixel 2 实机注入）验证或证伪。MSG_OOB 明确'review 新内核特性偶然发现'，pointer leaks 以 CRT 推导验证泄漏可行性。；实验结果直接反馈到路径选择：理论预测单次覆写足够但实践失效（2019 TLB）→ 转重试循环；初次 BTB 注入成功率<1%（Spectre）→ 转自建测试用例经验性探测；MSG_OOB 多次走错路径 → 公开自我纠正。外部反馈来自上游补丁是否落地（kernel security list guard pages）、厂商是否修复（Apple 2025-03-31）、同事技术提示（Mark Brand 简化路径）。

能力与结果：形成'面对不透明或复杂系统时，先用审计定位设计交互/优化假设，再用可控实验经验性探测黑盒边界'的稳定方法论，区别于 fuzzer 覆盖率驱动或纯理论推导。；2016 ecryptfs 递归页错误链 root 利用，主动向 kernel security list 提 guard pages + 移除 thread_info 结构性修复方向；2017 Xen access_ok 范围校验缺陷致 PV guest→hypervisor 物理内存逃逸；2017-2018 Spectre/Meltdown 三变体以经验性探测黑盒方式独立发现；2018 VMA 缓存序列号回绕 UAF，穷举 4 种重用方案导出唯一可行路径；2019 TLB/mremap 竞争在 Pixel 2 旧内核注入 zygote；2025 MSG_OOB UAF 从 Chrome renderer 沙箱达内核端到端利用；2025 pointer leaks 用 CRT 数学化推导完整 64-bit 指针恢复

置信度：high；替代解释：竞争性解释：此方法论底色可能被读作'个人天赋式直觉'。但 Spectre 入门显示其以 Evtyushkin 学术工作为起点、初次失败后转向自建测试用例，MSG_OOB 显示其走错路径后公开自我纠正，均指向可复现的方法论习惯 + P0 制度反馈回路（同事/上游/厂商），而非天赋式直觉。

证据：jh-works-01-recursion-2016, jh-works-02-xen-2017, jh-works-03-spectre-2018, jh-works-04-cache-invalidation-2018, jh-works-05-tlb-mremap-2019, jh-works-09-msgoob-2025, jh-works-10-pointer-leaks-2025, jh-conv-spectre-entrypoint-2018

### 质疑性能/设计优化中隐含的正确性假设作为 bug 入口

起点：首篇（2016 ecryptfs）即识别出'选择更高效的 VFS read handler 而非 mmap handler'这一性能优化绕过了'不可映射文件不应被 mmap'的映射约束。

练习与反馈：跨 2016→2025 重复以'优化引入的正确性假设失效'为入口：2017 Xen access_ok() 只校验起始地址而非整段范围（性能/简化假设）；2018 VMA 缓存单线程序列号假设在回绕+创建线程时失效；2019 选择 Dirty-PTE 缓解缺失的 Pixel 2 旧内核作为目标（缓解不存在 = 对手时间线最弱点）；2025 MSG_OOB '概率性缓解在攻击者可重试时失效' + CONFIG_RANDOMIZE_KSTACK_OFFSET 反转利用 + '复杂数据结构安全规则同时击败人和 fuzzer'。；上游 commit 历史与补丁落地情况反馈假设定位是否准确：2018 通过 git 历史定位 kernel 3.16 引入的单线程优化假设；2019 通过 commit 5d1904204c99 确认 Dirty-PTE 缓解在该旧内核分支不存在；2025 MSG_OOB 以引入 bug 的 commit 93c99f21db36（2024 年中）确认是新技术特性引入。批评 WARN_ON_ONCE 替换 BUG_ON、批评 grsecurity 混淆 commit message，是把反馈反向输出给上游。

能力与结果：形成'审查任何性能/设计优化时主动追问其隐含的正确性假设在何种边界条件下失效'的稳定入口，并据此选择缓解缺失的目标设备以最大化可利用性。；2016 ecryptfs 识别 mmap handler 被绕过的映射约束；2017 Xen access_ok 范围校验缺陷；2018 VMA 缓存单线程序列号假设失效 UAF；2019 选择 Pixel 2 旧内核（Dirty-PTE 缓解缺失）作为可利用目标；2025 MSG_OOB 概率性缓解反转利用 + 新技术特性暴露面错配批评

置信度：high；替代解释：竞争性解释：这些案例可能被读作'巧合命中优化缺陷'。但跨 9 年、跨四个不同子系统（VFS/Xen/VMA/TLB/MSG_OOB）反复以'优化假设失效'为入口，且 2018、2025 均主动追溯引入优化的 commit 历史，提示是稳定的认知入口而非偶然命中。

证据：jh-works-01-recursion-2016, jh-works-02-xen-2017, jh-works-04-cache-invalidation-2018, jh-works-05-tlb-mremap-2019, jh-works-09-msgoob-2025

### 穷举排除法（列所有可行路径逐条否定导出唯一可行路径）

起点：2018 cache invalidation 帖面对 UAF 后需在多条重用已释放 vm_area_struct 的方案中确定唯一可行利用路径，并以 SLUB 分配器用内核指针覆写 vm_start 阻断地址范围检查等给出否定技术理由。

练习与反馈：2018 穷举 4 种重用方案逐条否定，导出 BPF maps 经 page-allocator 唯一可行路径；2025 MSG_OOB 多次列举候选对象类型（'I spent a lot of time looking at various object types...but found nothing great'）并公开自我否定（'Clearly trying to target a heap object was foolish'、'Eventually, I realized that I had been going down the wrong path'），把被否定的方向公开写进 writeup 而非只展示最终成功路径。；同伴反馈直接简化利用路径：2018 Mark Brand 指出若同时控制 RDI 和 RIP 就不必翻转 CR4 的 SM*P 位，可直接 spawn usermode helper，Horn 接受纠正而非固守更复杂方案。自我反馈表现为公开丢弃一条依赖 >4GiB RAM 的方案（'feels gross and a bit like cheating'）。

能力与结果：形成'穷举可行路径并逐一给出否定技术理由'的结构化利用工程习惯，使后续研究（自己和读者）能从被否定的方向中学习，区别于试第一条就停或只展示成功路径的写法。；2018 cache invalidation 导出 BPF maps 经 page-allocator 唯一可行 VMA 重用路径；2018 接受 Mark Brand 反馈省去 CR4 SM*P 位翻转，简化利用路径；2025 MSG_OOB 公开自我否定堆对象方向，转页表覆写路径

置信度：high；替代解释：竞争性解释：穷举排除可能只是利用工程的自然步骤。但其公开化（把被否定方向写进 writeup）+ 接受同伴纠正简化路径，提示是一种刻意的方法论习惯与输出纪律，而非隐含的工程默认。

证据：jh-works-04-cache-invalidation-2018, jh-works-09-msgoob-2025, jh-conv-cache-collaboration-2018, jh-conv-msgoob-failures-2025

### 经验性诚实：精确标注知识边界而非模糊措辞

起点：面对不透明系统（CPU 微架构）时，Spectre 帖开头即声明帖子含大量基于观察行为的推测、'might not necessarily correspond to what processors are actually doing'。

练习与反馈：跨 2018→2025 重复：Spectre 对 prefetch 指令破坏攻击称 'we have no clue why'、对返回预测器承认 'we haven't analyzed that in detail yet'、对从间接调用预测器泄漏数据承认 'we haven't been able to make it work'；2019 TLB 承认'In theory, a single overwrite should be sufficient; but in practice, that doesn't seem to work'并标注不确定原因（'I'm not sure whether this is caused by some sort of cache inconsistency...or whether I did something else wrong'）；2025 MSG_OOB 公开承认'I was too lazy to do that everywhere perfectly'、'Eventually, I realized that I had been going down the wrong path'、'Clearly trying to target a heap object was foolish'。；读者/后续研究者可据此准确定位未解决问题；上游安全团队发现 Horn 漏掉的次要竞争窗口（2019 TLB，Horn 主动归功）。自我反馈表现为把'我走错的路'作为输出的一部分。

能力与结果：形成'精确说出不知道什么、理论失效时坦诚承认并标注不确定来源、把失败路径公开写进 writeup'的可复现研究习惯，使后续研究者能从被否定的方向中学习，区别于泛泛'maybe'式措辞或只展示成功结果的写法。；Spectre 帖逐项标注未分析/未成功/无解的知识边界；2019 TLB 帖承认理论预测与实践不符并标注不确定原因；2025 MSG_OOB 帖公开多条失败路径与自我纠正；2025 MSG_OOB 帖自述工程妥协（too lazy / feels gross）

置信度：high；替代解释：竞争性解释：这些坦诚可能是 writeup 文风选择。但跨 7 年、跨 CPU 微架构/内核内存/内核利用三个不同技术域反复出现同一模式，且每条都精确到'未分析/未成功/无解/走错路径'的具体层级，提示是内化的研究习惯而非写作装饰。

证据：jh-conv-spectre-honesty-2018, jh-conv-tlb-credit-2019, jh-conv-msgoob-failures-2025

### 对手时间线思维：以用户何时受保护而非补丁何时发布评估影响

起点：2018 cache invalidation 帖确立此思维，批评 WARN_ON_ONCE 替换 BUG_ON 为'半步修复'，并映射从上游 commit 到用户安装的四步对手时间线管线。

练习与反馈：2018 映射 commit→稳定版→发行版 backport→用户安装四步管线，明确'补丁 becomes public after step 1...but users are only protected after step 4'；2019 TLB 帖以'It took more than two months for the upstream kernel change to make its way to user devices; writing an exploit for this bug took far less time'收束；并主动选择缓解缺失的 Pixel 2 旧内核作为目标（'before commit 5d1904204c99...the special case for Dirty page table entries did not exist'），把对手时间线最弱点作为研究目标选择逻辑。；通过把补丁到用户保护的整条管线公开化，迫使上游与发行版对'补丁已合并 ≠ 用户已保护'的窗口负责；点名批评 grsecurity 混淆 commit message 安全影响，是对上游披露实践的具体反馈，批评指向行为与决策而非个人。

能力与结果：形成'不只报告 bug，而是把补丁到用户保护的整条管线公开化'的稳定影响评估习惯，并把缓解缺失的旧设备/旧分支作为研究目标选择逻辑。；2018 cache invalidation 四步对手时间线管线 + 半步修复批评；2019 TLB 帖以两月 backport 窗口 vs exploit 开发时长收束；2019 选择缓解缺失的 Pixel 2 旧内核作为可利用目标

置信度：high；替代解释：竞争性解释：对手时间线思维可能只是 P0 团队披露规范的一部分。但 Horn 在 2018/2019 帖中具体到四步管线命名、两月窗口量化、选择缓解缺失设备作为目标，且 2019 主动归功 kernel security team 发现自己漏掉的窗口，提示是个人内化的评估习惯而非单纯套用团队规范。

证据：jh-works-04-cache-invalidation-2018, jh-works-05-tlb-mremap-2019, jh-comm-005, jh-conv-tlb-credit-2019

### 慷慨归因 + 责任分层（P0=发现/演示者，缓解设计推给厂商/上游）

起点：首篇（2016）即致谢内核维护者 Andy Lutomirski 已先行开始 guard pages 工作并直接链接其 LKML 补丁，同时主动向 kernel security list 提结构性修复方向但把具体实施交给上游。

练习与反馈：跨 2016→2025 重复：2016 致谢 Lutomirski + 引用 Jon Oberheide 演讲；2018 Spectre 把 Variant 2 概念来源归功同事 Felix Wilhelm、列出 10 位并发发现者、把缓解设计责任推给厂商（'processor vendors are in a much better position to design and evaluate mitigations'）；2018 cache invalidation 致谢 Mark Brand；2019 主动归功 kernel security team 发现自己漏掉的窗口。Horn 把自己定位为'概念整合者 + PoC 实现者'而非'概念原创者'，不主张独占发现权，使学术圈以独立发现者并列方式接受而不卷入优先权争夺。；学术圈与厂商以独立发现者署名/credit 形式承认（Meltdown 三组之一、Spectre 两方之一、Apple CVE-2017-5754 按 Jann Horn 个人点名）。社区记忆把 P0 提前公开归因为'合理应对泄露'而非'破坏协调'，Horn/P0 不发声即可维持非对抗性反馈关系。

能力与结果：形成'提供方向而非处方 + 主动让功给概念来源/上游/同事 + 把缓解设计推给厂商'的稳定责任框架与归因纪律，降低跨团队优先权争议成本，使其能持续介入内核社区与学术圈而不与维护者产生优先权冲突。；2016 致谢 Lutomirski 并向 kernel security list 提结构性修复方向；2018 Spectre 把 Variant 2 概念来源归功 Wilhelm + 列出 10 位并发发现者；2018 cache invalidation 致谢 Mark Brand 简化利用路径；学术圈以独立发现者署名承认（Meltdown 三组之一、Spectre 两方之一）；Apple CVE-2017-5754 按 Jann Horn 个人点名 credit

置信度：high；替代解释：竞争性解释：慷慨归因可能只是 P0 团队文化要求。但 Horn 在职业生涯最高点的 Spectre 披露中主动让出 Variant 2 概念来源给同事、并列全部并发发现者，且这是其在公开 writeup 中稳定复现的归因纪律（而非仅在团队政策帖出现），提示是个人内化的定位而非单纯团队规范。

证据：jh-comm-001, jh-comm-002, jh-comm-003, jh-comm-008, jh-ext-01, jh-ext-02, jh-ext-03, jh-ext-04, jh-ext-05, jh-dec-05-spectre-attribution-generous

### 缓解反转利用与弱原语组合升级的利用工程范式

起点：2017 Xen 帖首次确立：把'写一个随机字节后跟 7 字节垃圾'的弱原语，通过反复写随机字节并读回直到正确、再连续写入升级为受控 9 字节写，进而覆写 level-3 页表项。

练习与反馈：2017 Xen 弱原语组合升级；2019 选择缓解缺失的 Pixel 2 旧内核作为可利用目标（缓解不存在 = 最弱点）；2025 MSG_OOB 把 CONFIG_RANDOMIZE_KSTACK_OFFSET 反转利用（栈随机化'works to my advantage'把释放页重分配为内核栈页）、以 semi-arbitrary read 原语先行引导写原语、并用'概率性缓解在攻击者可重试时失效'作为论点。；利用工程实践反馈：理论预测与实践不符时（2019 单次覆写理论足够但实践失效）转重试循环；2025 多次走错路径后自我纠正转页表覆写路径。

能力与结果：形成'把缓解机制反向用作利用工具 + 把弱原语组合升级为受控写原语 + 用读原语先行引导写原语'的系统化利用工程范式。；2017 Xen 弱原语升级为受控 9 字节写覆写 level-3 页表项；2019 选择缓解缺失的 Pixel 2 旧内核注入 zygote；2025 MSG_OOB 用 CONFIG_RANDOMIZE_KSTACK_OFFSET 反转栈随机化 + 读原语引导写原语覆写页表

置信度：medium；替代解释：竞争性解释：缓解反转可能是利用工程的自然演进而非个人特有方法。但 2017 弱原语组合升级与 2025 概率性缓解反转论点在 writeup 中被显式提炼为可复用论点（而非仅作为单次技巧隐含），提示是刻意的方法论提炼；不过该范式在 P0 其他研究员工作中也常见，区分度低于其他机制，故 confidence 标 medium。

证据：jh-works-02-xen-2017, jh-works-05-tlb-mremap-2019, jh-works-09-msgoob-2025

### 竞争窗口扩窗工程化

起点：2019 TLB/mremap 帖首次面对内核竞争窗口扩窗，以 busy-polling VmPTE 字段监控页表分配进行经验性探测。

练习与反馈：2019 TLB 经验性重试循环；2022 race window 升级为系统化组合工程：cache miss + hardware timer 中断（timerfd 在 hardirq 上下文）+ epoll 50k waitqueue churn，并引入'单线程对硬件定时器竞争而非双线程互竞'范式降低双线程时序抖动，命中率约 30%。致谢 Xen 安全团队（中断扩窗思路来源）、Anders Fogh 博客、Gamazo Labs 'Sushi Roll' 指令级时序分析等多方概念来源。；命中率反馈扩窗策略有效性（约 30% if tuned for the specific machine）；多方概念来源（Xen 安全团队/Anders Fogh/Gamazo Labs）反馈扩窗技术组合的可行性。

能力与结果：形成'把经验性重试升级为系统化组合工程扩窗 + 单线程对定时器范式降低时序抖动'的竞争窗口利用工程能力。；2019 TLB/mremap busy-polling VmPTE 经验性探测 + 重试循环；2022 race window cache miss + hardirq + waitqueue churn 组合扩窗，命中率约 30%

置信度：medium；替代解释：竞争性解释：扩窗工程化可能是内核竞争窗口研究的通用技巧演进。但 2019→2022 的具体升级（经验性重试→系统化组合工程 + 单线程对定时器范式）在 writeup 中被显式叙述为方法论演化，且跨 3 年空窗后复出仍延续同方向，提示是个人能力积累而非纯通用技巧；但仅两次明确案例，区分度证据有限，confidence 标 medium。

证据：jh-works-05-tlb-mremap-2019, jh-works-07-race-window-2022

## 可迁移与不可迁移

- 可迁移：以代码审计 + 实验验证（非 fuzzing）为找 bug 入口：先审计定位设计交互/优化假设，再用可控实验经验性探测黑盒边界，理论失效时坦诚承认并调整路径。
- 可迁移：把'质疑性能/设计优化中隐含的正确性假设'作为稳定的 bug 入口：审查任何优化时主动追问其隐含假设在何种边界条件（回绕、并发、缓解缺失、可重试）下失效。
- 可迁移：穷举排除法：列所有可行路径并逐一给出否定技术理由，导出唯一可行路径；把被否定的方向公开写进 writeup 使后续研究者可学习。
- 可迁移：经验性诚实：精确标注知识边界（未分析/未成功/无解/走错路径），理论预测与实践不符时标注不确定来源，而非用模糊措辞掩饰。
- 可迁移：对手时间线思维：以'用户何时真正受保护'而非'补丁何时发布'为评估终点，把补丁到用户保护的整条管线公开化；把缓解缺失的旧设备/旧分支作为研究目标选择逻辑。
- 可迁移：慷慨归因 + 责任分层：提供结构性修复方向而非一次性处方，主动让功给概念来源/上游/同事，把自己定位为概念整合者 + PoC 实现者而非概念原创者，降低跨团队优先权争议成本。
- 可迁移：把失败路径与自我纠正公开写进 writeup，而非只展示线性成功结果，使研究过程留痕可被他人学习。
- 可迁移：研究目标选择信号：以'新技术特性 + 预期使用面 vs 实际暴露面错配'（如 MSG_OOB 几乎只在 Oracle 用却在 Chrome 沙箱暴露）作为深度调查触发点，而非 fuzzing 覆盖率驱动。
- 不可直接迁移：Google Project Zero 全职研究员职位 + 强制 90 天披露 + 完整 PoC 公开 + 公开 bugtracker 平台：这是制度资源，非个人方法论可复制；脱离 P0 制度后，90 天硬立场与 bugtracker 起算点等约束不适用。
- 不可直接迁移：与 CPU 厂商（Intel/AMD/ARM）、Apple、Linux 内核安全团队的直接协调披露渠道：这是 P0 平台赋予的披露通道，普通研究员不具备同等直达渠道。
- 不可直接迁移：P0 同事网络（Felix Wilhelm 提供 Variant 2 概念来源、Mark Brand 简化利用路径、Xingyu Jin 解释 unix_stream_read_generic 假设）作为概念来源与同行反馈回路：这是组织内部协作资源，非个人孤立可复制。
- 不可直接迁移：时代红利：2017-2018 Spectre/Meltdown 系统性 CPU 漏洞窗口期 + 多独立团队（Graz/Cyberus/Kocher）并行收敛，使独立发现者能以并列署名被学术圈承认；这种窗口期不可人为复制。
- 不可直接迁移：Google 内部资源：Pixel 2 设备 + 4.4 旧内核分支（Dirty-PTE 缓解缺失）作为可利用研究目标，是雇主资源，非通用研究条件。
- 不可直接迁移：写作完成度优先于时效的发布节奏依赖漏洞已 CVE 化、不构成披露违规的前提：VirtualBox 草稿拖延 8 年仍可发布，是因为漏洞本身 2017 年已修复并 CVE 化；若漏洞未修复，此发布节奏不可行。
- 不可直接迁移：GitHub handle thejh 关联 @google 的身份核实与 P0 archive 逐帖 byline 核实机制，是研究者身份可追溯性的前提，非个人能力。

## 复核问题

- 机制6 evidence_ids 应补入 jh-ext-07，以支撑 feedback 字段中'社区记忆把 P0 提前公开归因为合理应对泄露''Horn/P0 不发声即可维持非对抗性反馈关系'的论断；或将该论断改写为仅由已列证据（jh-comm-001/002/003/008、jh-ext-01~05、jh-dec-05）可支撑的部分（这些已列证据支撑的是 Horn 主动让功，而非社区对 P0 沉默的归因框架）。
- 统一机制3、机制7、机制8 这三类'仅2-3次明确案例'机制的 confidence 标注标准：机制3（2案例，high）与机制8（2案例，medium）标注不一致。建议要么将机制3 降为 medium（与机制7/8 一致），要么在机制3 中补强区分度论证（如穷举排除法的公开化把被否定方向写进 writeup 这一输出纪律，区别于试第一条就停的默认工程实践）以支撑 high。
- （非阻塞，建议性）jh-ext-08（Torvalds 怒斥，inferred+lead_only）虽未误用为 Horn 能力证据，但 synthesis 在 tensions 第1条与 open_questions 中隐含引用了其'社区对 P0 沉默接受'的叙事框架。建议在引用该框架时显式标注其源自 inferred+lead_only 证据，避免将媒体集合报道未一手核实的措辞作为言行一致性论证的稳定支柱。

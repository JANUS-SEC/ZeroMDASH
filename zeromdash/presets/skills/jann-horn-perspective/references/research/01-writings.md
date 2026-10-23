# Jann Horn — 著作与系统思考

> 本文系统提炼 Jann Horn 在 Project Zero 博客亲笔撰写的 9 篇系统性长文（2016-06 → 2025-12）中反复出现的核心论点、自创术语与智识谱系。
>
> 方法论：对 9 篇博文做跨篇章复现分析——**同一个论点在 ≥3 个不同研究方向（Linux 内核栈溢出 / Xen 虚拟化逃逸 / CPU 微架构侧信道 / Linux 内存管理 / TLB 竞争 / Chrome 沙箱→内核 / 逻辑型指针泄漏）中重复出现，即认定为"真信念"而非随口一说**（见 `extraction-framework.md` 三重验证之"跨域复现"）。
>
> 来源分级：**[1H]** = Horn 本人在 P0 blog 亲笔（均经 WebFetch 核实作者 byline）；**[2H]** = 团队政策帖（非 Horn 所写，仅作背景）。本文件不引二手转述。
> 调研日期：2026-07-27。信息源黑名单遵守：未引知乎 / 微信公众号 / 百度百科。

---

## 1. 系统性长文清单（9 篇亲笔博文，按时间序）

| # | 日期 | 标题 | 研究方向 | URL（均经 WebFetch 200 + byline 核实） |
|---|------|------|---------|--------|
| 1 | 2016-06-20 | Exploiting Recursion in the Linux Kernel | Linux 内核栈溢出（ecryptfs 叠加 procfs 递归） | https://projectzero.google/2016/06/exploiting-recursion-in-linux-kernel_20.html |
| 2 | 2017-04-07 | Pandavirtualization: Exploiting the Xen hypervisor | 虚拟化逃逸（PV guest → hypervisor 物理内存） | https://projectzero.google/2017/04/pandavirtualization-exploiting-xen.html |
| 3 | 2018-01-03 | Reading privileged memory with a side-channel | CPU 微架构侧信道（Spectre/Meltdown 三变体） | https://projectzero.google/2018/01/reading-privileged-memory-with-side.html |
| 4 | 2018-09-26 | A cache invalidation bug in Linux memory management | Linux 内存管理（VMA 缓存序列号回绕 UAF） | https://projectzero.google/2018/09/a-cache-invalidation-bug-in-linux.html |
| 5 | 2019-01-17 | Taking a page from the kernel's book: A TLB issue in mremap() | TLB / 页表竞争（Pixel 2 上注入 zygote） | https://projectzero.google/2019/01/taking-page-from-kernels-book-tlb-issue.html |
| 6 | 2022-03-24 | Racing against the clock -- hitting a tiny kernel race window | 内核竞争窗口扩窗（UNIX 域套接字 SCM_RIGHTS GC） | https://projectzero.google/2022/03/racing-against-clock-hitting-tiny.html |
| 7 | 2025-08-08 | From Chrome renderer code exec to kernel with MSG_OOB | Chrome 沙箱 → Linux 内核（MSG_OOB UAF，CVE-2025-38236） | https://projectzero.google/2025/08/from-chrome-renderer-code-exec-to-kernel.html |
| 8 | 2025-09-26 | Pointer leaks through pointer-keyed data structures | 逻辑型指针泄漏（NSKeyedArchiver，CRT 推导） | https://projectzero.google/2025/09/pointer-leaks-through-pointer-keyed.html |
| 9 | 2025-12-16 | Thinking Outside The Box [dusted off draft from 2017] | VirtualBox VM → 宿主用户态逃逸（CVE-2017-3558，2017 草稿补发） | https://projectzero.google/2025/12/thinking-outside-the-box.html |

**跨度**：9 篇博文横跨 2016-2025（含 2019-2022、2022-2025 两个公开空窗期，见 `06-timeline.md`）。研究方向覆盖 **Linux 内核（栈/内存管理/TLB/竞争）+ 虚拟化（Xen/VirtualBox）+ CPU 微架构（Spectre/Meltdown）+ 浏览器沙箱逃逸（Chrome renderer→内核）+ 逻辑型信息泄漏（指针键结构）** 五个底层边界。

---

## 2. 反复出现的核心论点（跨域复现 = 真信念）

### 论点 A：「Make zeroday hard.」——签名式结尾指令

**跨域复现次数：≥4 篇**（2016 recursion、2017 Xen、2018 cache invalidation、2019 TLB/mremap 均以这句或等价格言收束）

- 2016（首篇博文）："Make zeroday hard."——文末格言式收束，**首篇即确立**。
- 2017 Xen："Make zeroday hard."——文末同句。
- 2018 cache invalidation："Make zeroday hard."——文末同句（见 `02-conversations.md §1.2`）。
- 2019 TLB/mremap："Make zeroday hard."——文末同句。

**这是 Horn 跨 4 个不同研究方向（内核栈 / 虚拟化 / 内存管理 / TLB）一致复现的签名句**——不是装饰，是**职业信念的压缩**：研究者的职责是提高攻击者的工程成本，而非声称能消灭 0day。与 Tavis Ormandy 共享此句（见 tavis-ormandy-perspective），是 P0 内部共识，但 Horn 在 4 篇博文中独立复现，已内化为个人签名。

**生成力**：面对"是否值得公开完整 PoC"的争议，Horn 会倾向公开——因为"Make zeroday hard"要求让攻击者面对可复现的工程难度，而非依赖模糊的"不安全感"。

---

### 论点 B：穷举排除法——列出所有可行路径逐一否定，导出唯一可行路径

**跨域复现次数：≥4 篇**（2016、2017、2018、2019）

- **2016 recursion [1H]**：列 6 条利用路径逐一否定：
  - `proc/$pid/mem` 否定（read 返回 -EIO，无法含 ecryptfs header）
  - 直接 mmap proc 文件否定（file_operations 无 mmap 回调）
  - userfaultfd 否定（不 catch remote memory access）→ 改用 FUSE
  - `addr_limit` 部分否定（reset on way out）
  - `restart_block` 否定（已移出 thread_info）
  - thread_info 内找目标放弃（无值得目标）→ 转向栈前分配溢出
- **2018 cache invalidation [1H]**：列 4 种重用已释放 VMA 的方案逐一否定——SLUB 分配器覆写前 8 字节阻断地址范围检查等——最终导向 BPF maps 的 page-allocator 路径（见 `02-conversations.md §1.2`）。
- **2017 Xen [1H]**：变体——原语组合升级（随机字节→读回直到正确→连续写入），但同样体现"不假设第一条路径可行，逐条收敛"。
- **2019 TLB [1H]**：理论预测"In theory, a single overwrite should be sufficient; but in practice, that doesn't seem to work"——**承认理论失效，转重试循环**（实验性诚意的标志，见论点 I）。

**生成力**：面对任何利用问题，Horn 会先**穷举所有看似可行的路径，逐条给出否定的技术理由**，而非试第一条就停。这是他区别于"找到一条可行就发布"的研究员的标志。

---

### 论点 C：质疑性能/设计优化中隐含的正确性假设

**跨域复现次数：≥4 篇**（2016、2017、2018、2019）

- **2016 recursion [1H]**：ecryptfs 的优化选择——不用下层文件系统 mmap handler（节省内存），直接用 VFS read handler。"This is more efficient and straightforward, but also has the side effect that it is possible to mmap() decrypted views of files that normally wouldn't be mappable."——**性能优化绕过了"本不应被映射"的安全约束**。
- **2017 Xen [1H]**：2005 年的 `access_ok()` 优化提交改变了 x86_64 行为——原检查整个范围是否与 hypervisor 内存重叠，优化后只检查起始地址。隐含假设"access proceeds linearly"在带偏移访问下失效。**11 年前的优化埋下的假设漏洞**。
- **2018 cache invalidation [1H]**：追溯 kernel 3.16 引入的优化假设——单线程进程的 VMA cache 序列号保持接近 mm_struct 序列号——识别出该假设在序列号回零后立即创建线程时失效（见 `02-conversations.md §1.2`）。
- **2019 TLB [1H]**：mremap 优化（移动引用到新页表避免立即释放 + 批量 TLB 刷新）在竞争条件下失效——"after step 5, another task can theoretically race with mremap() and drop the page"。

**生成力**：面对任何性能优化或"看起来合理"的设计选择，Horn 会问：**"这个优化隐含了什么正确性假设？这个假设在什么边界条件（并发/回绕/偏移/空窗）下失效？"** 这是他发现 bug 的主入口——不是 fuzzing，是**对优化的审计**。

**排他性**：多数研究员接受优化假设（优化通常经过性能测试），Horn 系统性地质疑优化的安全语义。

---

### 论点 D：对缓解措施的批判性思考——缓解可被反转、半步修复、概率性失效

**跨域复现次数：≥5 篇**（2016、2017、2018、2019、2025）

- **2016 recursion [1H]**："even with the existing mitigations turned on, they're still exploitable"；"moving stuff out of thread_info is not a sufficient mitigation"；KASLR 在 Ubuntu 默认未启用（因破坏 hibernation）。
- **2017 Xen [1H]**：2012 XSA-29 的修复本身不够——只检查 offset 0，留下带偏移写入漏洞。**"补丁修复有时只是半步修复"**。
- **2018 cache invalidation [1H]**："The policy of only printing a warning even when the kernel has discovered a memory corruption is problematic."（见 `02-conversations.md §1.2`）
- **2019 TLB [1H]**：Dirty-PTE 缓解不够——"the big race window only works for non-Dirty page table entries"仍允许 UAF 读取；旧内核完全无此保护。**选择 Pixel 2（4.4 内核）正因为缓解不存在**。
- **2025 MSG_OOB [1H]**："That is supposed to be a security mitigation, but works to my advantage."（栈随机化反转）；"probabilistic mitigations that randomize something differently on every operation can be ineffective if the attacker can keep retrying."；"The hardening checks I encountered...were a major annoyance, but could be worked around."（见 `02-conversations.md §1.3`）

**生成力**：面对任何缓解措施，Horn 会问三个问题：
1. 这个缓解能否被攻击者**反转利用**（如栈随机化变成信息源）？
2. 这个修复是否只是**半步修复**（只堵了 offset 0，留下偏移路径）？
3. 这个缓解是**确定性的还是概率性的**？概率性缓解在攻击者可重试时失效。

**排他性**：多数人把缓解当正面因素，Horn 系统性地寻找缓解的反转面与失效条件。

---

### 论点 E：对手时间线思维——以"用户何时真正受保护"而非"补丁何时发布"思考

**跨域复现次数：≥3 篇**（2016、2018、2019）

- **2018 cache invalidation [1H]**：映射从上游 commit 到用户安装的四步管线，"Note that the patch becomes public after step 1...but users are only protected after step 4."对比 Debian 内核"was last updated 2018-08-21"与 Android"only ships security updates once a month"（见 `02-conversations.md §1.2`）。
- **2019 TLB [1H]**：时间线——报告(2018-10-12)→修复commit(10-18)→稳定版(10-20)→公开披露(10-29)→4.4 向后移植(11-10)→漏洞利用发布(11-14)。**"It took more than two months for the upstream kernel change to make its way to user devices; writing an exploit for this bug took far less time."** 针对仍跑 4.4 的 Pixel 2。
- **2016 recursion [1H]**：关注发行版何时默认启用 KASLR（用户实际受保护），敦促"distros should be able to turn on KASLR by default"。

**生成力**：评估漏洞影响时，Horn 不会停在"补丁已合并"——他会**映射从 commit → 稳定版 → 发行版向后移植 → 用户安装的完整管线**，并指出哪个环节最慢、攻击者在哪个窗口仍可利用。

**排他性**：多数人以"补丁可用"为终点，Horn 以"用户安装"为终点。

---

### 论点 F：责任框架与慷慨归因——P0 定位为发现/演示者，缓解设计责任推给厂商；不抢独占发现权

**跨域复现次数：≥3 篇**（2018 Spectre、2016、2019）

- **2018 Spectre [1H]**："we believe that the processor vendors are in a much better position than we are to design and evaluate mitigations."——把缓解设计责任明确推给厂商，P0 定位为发现/演示者。慷慨列出并发发现者（Graz/Kocher/Cyberus 团队），"Felix Wilhelm's research based on this provided the basic idea behind variant 2."——**主动让出 Variant 2 概念来源的功劳给同事**（见 `02-conversations.md §1.1`、`04-external-views.md §3.2.2`）。
- **2016 recursion [1H]**：致谢"Andy Lutomirski had actually already started working on this"并链接其补丁；引用 Jon Oberheide 演讲、Ubuntu Security Features 页面。
- **2019 TLB [1H]**："(I didn't notice that, but the kernel security team did.)"——**主动承认自己漏掉的次要竞争窗口被内核安全团队发现**，归功他人。

**微妙差别**：2016 中 Horn 主动向 kernel security list 提修复建议（guard pages + 移除 thread_info）——这与"把缓解设计推给厂商"看似矛盾。**调和**：Horn 的责任框架是"演示严重性 + 指出结构性修复**方向**，但具体缓解设计与实施交给上游/厂商"。他提供方向，不开处方。

**生成力**：发表研究时，Horn 会**主动让功给概念来源**（同事前期工作、学术并发发现者），定位自己为"概念整合者 + PoC 实现者"而非"概念原创者"。

**排他性**：多数研究员抢优先权，Horn 系统性地慷慨归因。

---

### 论点 G：对不确定的坦诚限定——经验性诚实

**跨域复现次数：≥4 篇**（2017、2018、2019、2025）

- **2018 Spectre [1H]**："This blogpost contains a lot of speculation about hardware internals based on observed behavior, which might not necessarily correspond to what processors are actually doing."；关于 prefetch 指令破坏攻击："and we have no clue why."（见 `02-conversations.md §1.1`）
- **2017 Xen [1H]**："As far as I can tell, the only reason this didn't immediately make...vulnerable is that..."——对推测性归因明确标注。
- **2019 TLB [1H]**："I'm not sure whether this is caused by some sort of cache inconsistency [...] or whether I did something else wrong."；"something about persistent memory?"；"In theory...but in practice, that doesn't seem to work."——**承认理论预测失效**。
- **2025 MSG_OOB [1H]**："Clearly trying to target a heap object was foolish, because there is something much better."——自我纠正（见 `02-conversations.md §1.3`）。

**生成力**：面对不确定，Horn 会**精确标注不知道什么**（"I'm not sure whether X or Y"、"no clue why"、"as far as I can tell"），而非用模糊限定词（"it might potentially be somewhat risky"）掩饰。

**排他性**：多数作者对不确定用泛泛"maybe"，Horn 精确标注知识边界（与 Tavis 共享此特征，见 tavis-ormandy-perspective）。

---

### 论点 H：实验驱动的经验性探测——理论预测失效时承认 + 重试

**跨域复现次数：≥3 篇**（2018、2019、2025）

- **2018 Spectre [1H]**：逐位翻转分支、移动代码在内存位置、改变分支数量，**经验性推断** BHB 更新函数与 BTB 别名行为（见 `02-conversations.md §1.1`）。"We decided to write a userspace test case to be able to more easily test branch predictor behavior in different situations."
- **2019 TLB [1H]**：busy-polling status file 监控 VmPTE 字段检测页表分配，重试循环"If a page fault occurs before that, go back to step 1"。
- **2025 MSG_OOB [1H]**：经验性自我纠正——"Clearly trying to target a heap object was foolish, because there is something much better."

**生成力**：面对不透明系统（CPU 微架构、内核竞争窗口），Horn 不会等理论完备——他会**先写测试用例经验性探测黑盒行为，理论失效时承认并转重试**。

**排他性**：多数研究员依赖文档或理论建模，Horn 信任运行时行为胜过文档声称（与 Tavis 共享）。

---

### 论点 I：最底层边界研究——CPU 微架构 / 内核用户态边界 / 虚拟化边界

**跨域复现次数：≥5 篇**（2017、2018、2018-cache、2019、2025）

- **2017 Xen [1H]**："permits an attacker with control over the kernel of a paravirtualized x86-64 Xen guest to break out of the hypervisor and gain full control over the machine's physical memory."——PV guest 与 hypervisor 共享虚拟地址空间，access_ok 是唯一软件屏障，突破后达物理硬件层。"paravirtualization is not much harder to understand than normal kernels"——审计门槛。
- **2018 Spectre [1H]**：CPU 微架构侧信道——分支预测器、BHB、BTB、cache 时序。
- **2018 cache [1H]**：Linux 内存管理 VMA 缓存。
- **2019 TLB [1H]**：TLB / 页表缓存——WebFetch 总结极精彩："TLB 刷新正确性 + CPU 缓存语义 + 物理页面重用竞争窗口的整体框架，本质上与应用于侧信道和瞬态执行的分析思维模式相同：**证明数据结构在所有可观察状态下（包括并发观察者）的不变性，并寻找架构文档与实现实际保证之间的差距。**"
- **2025 MSG_OOB [1H]**：Chrome renderer 沙箱 → Linux 内核（沙箱暴露不必要内核攻击面）。

**生成力**：选择研究目标时，Horn 倾向**可完整建模的底层边界**——CPU 微架构、内核与用户态边界、虚拟化边界——这些边界允许系统化逆向建模与端到端证明（见 `05-decisions.md §3.4`）。

**排他性**：与其他 P0 成员形成鲜明分工——Ian Beer（iOS/macOS 内核）、Tavis Ormandy（Windows/用户态）、Natalie Silvanovich（Android/WebRTC）、James Forshaw（Windows 内核/沙箱）、Gal Beniamini（Broadcom Wi-Fi）。Horn 占据**最底层硬件边界**（见 `05-decisions.md §3.2`、`04-external-views.md §6.1`）。

---

### 论点 J：新技术特性 + 暴露面错配 = 研究目标信号

**跨域复现次数：≥3 篇**（2016、2019、2025）

- **2025 MSG_OOB [1H]**："I was reviewing a new Linux kernel feature when I learned about the `MSG_OOB` feature"；"`MSG_OOB` feature is not used by Chrome, it was exposed in the Chrome renderer sandbox."——**预期使用面 vs 实际暴露面错配**："This feature is used almost nowhere except in Oracle products."（见 `02-conversations.md §1.3`、`05-decisions.md §3.3`）
- **2016 recursion [1H]**：ecryptfs 新 mmap 副作用——本不应被映射的文件可被 mmap 解密视图。
- **2019 TLB [1H]**：mremap 优化引入的新竞争窗口。

**生成力**：选择研究目标时，Horn 主动**review 新落地的内核特性**，寻找"预期使用面 vs 实际暴露面错配"——特性几乎无人用（Oracle），却在 Chrome 沙箱暴露。这是"新技术 + 错配"信号驱动的深度调查（见 `05-decisions.md §3.3`）。

---

### 论点 K：复杂安全规则同时击败人和 fuzzer

**跨域复现次数：≥3 篇**（2018-cache、2019-TLB、2025-MSG_OOB）

- **2025 MSG_OOB [1H]**："data structures with complex safety rules...don't just make it hard for human programmers to keep track of safety rules, they also make it hard for fuzzers."；"Chrome's Linux desktop renderer sandbox exposes kernel attack surface that is never legitimately used in the sandbox."（见 `02-conversations.md §1.3`）
- **2019 TLB [1H]**：TLB 刷新模式复杂——"The general code pattern for performing cache invalidations"涉及移除条目、刷新、释放引用三步，mremap 违反顺序。
- **2018 cache [1H]**：VMA 缓存序列号复杂——单线程优化假设在并发+回绕下失效。

**生成力**：评估某子系统安全性时，Horn 会问：**这套安全规则有多复杂？复杂到人和 fuzzer 都难以追踪？** 复杂安全规则是结构性风险信号。

**排他性**：多数人认为"有安全规则=安全"，Horn 认为"复杂安全规则=结构性风险"。

---

### 论点 L：系统化技术叙事优先——写作完成度 > 时间新鲜度，端到端可证明

**跨域复现次数：≥4 篇**（2017-Xen、2025-VirtualBox、2025-MSG_OOB、2025-pointer-leaks）

- **2025 VirtualBox [1H]**：2017 修复，2025-12 才发布——"never got around to writing the second half"；"it seems a bit sad to just leave this old draft rotting around forever"；内容"almost as I drafted it back then"，仅"very lightly edited"。**写作完成度是发布的硬约束——不发布半截技术故事，宁可拖延 8 年**（见 `05-decisions.md §4.2`）。
- **2017 Xen [1H]**：完整 allocator 逆向 → 信息泄露原语 → chunk header 腐蚀 → code execution 链路（系统化程度远超典型 P0 短博客）。
- **2025 MSG_OOB [1H]**：从漏洞触发到完整 sandbox→kernel exploit 的端到端分析。
- **2025 pointer leaks [1H]**：使用 Chinese Remainder Theorem 数学化推导完整 64-bit pointer 恢复。

**生成力**：面对半截研究，Horn **宁可拖延也不发布**——写作完成度优先于时间新鲜度。这与 P0 团队政策中"faster patch development"的时效导向看似不一致，但因为漏洞本身在修复后已 CVE 化，不构成披露违规（见 `05-decisions.md §4.2`）。

**排他性**：多数研究员追时效（修复后尽快发 writeup 抢关注），Horn 追完成度。

---

## 3. 自创术语与反复使用的概念

| 术语/概念 | 含义 | 出处 | 跨域复现 |
|----------|------|------|---------|
| **"Make zeroday hard."** | 研究者职责是提高攻击者工程成本，非消灭 0day | 2016/2017/2018/2019 文末 | 4 篇 |
| **"ecryptfs matroska"** | 递归嵌套加密的 ecryptfs 数据，类比俄罗斯套娃 | 2016 | 自创比喻 |
| **"stacking filesystem"** | 使用另一个文件系统中的目录作为后备设备的文件系统（ecryptfs/overlayfs） | 2016 | 反复使用 |
| **"lower filesystem" / "lower files"** | 下层后备文件系统/文件 | 2016 | 反复使用 |
| **栈布局颜色编码（green/red/yellow）** | 区分可覆盖/不可覆盖/视值而定的栈区域 | 2016 | 自创视觉教学框架 |
| **"the boring part"** | 自嘲利用的某部分（如 JOP）缺乏优雅 | 2018 cache invalidation | 表达 DNA |
| **"dusted off draft"** | 旧草稿补发 | 2025 VirtualBox | 自嘲 |
| **"probabilistic mitigations"** | 每次操作随机化的缓解——在攻击者可重试时失效 | 2025 MSG_OOB | 跨论点 D |
| **"complex safety rules"** | 同时击败人和 fuzzer 的复杂安全规则 | 2025 MSG_OOB | 跨论点 K |
| **"attack surface that is never legitimately used"** | 沙箱暴露的不必要攻击面 | 2025 MSG_OOB | 跨论点 J |

---

## 4. 智识谱系（影响 Horn 的 → Horn 影响的）

### 4.1 影响 Horn 的（从其博文引用与致谢反推）

| 谁 | 如何影响 | 证据（[1H] Horn 亲笔引用） |
|---|---------|--------------------------|
| **Evtyushkin / Ponomarev / Abu-Ghazaleh（学术）** | BTB 滥用的学术基础 | 2018 Spectre 帖 Literature 引用其 BTB 行为研究 |
| **Anders Fogh（独立研究员）** | Variant 3（rogue data cache load）的基础 | 2018 Spectre 帖引用其 2017-07 博客 |
| **Felix Wilhelm（P0 同事）** | Variant 2（branch target injection）的概念来源 | "Felix Wilhelm's research based on this provided the basic idea behind variant 2." |
| **Agner Fog（微架构文档作者）** | CPU 微架构参考 | 2018 Spectre 帖 Literature 引用 Agner Fog 微架构文档 |
| **Intel 手册** | CPU 规范参考（Horn 信任运行时行为胜过手册，但手册是起点） | 2018 Spectre 帖 Literature |
| **Andy Lutomirski（内核维护者）** | 内核栈保护方向 | 2016 帖致谢"Andy Lutomirski had actually already started working on this"并链接其补丁 |
| **Jon Oberheide** | 内核安全研究 | 2016 帖引用其演讲 |
| **grsecurity** | **反面参照**——Horn 指出 Linux 落后于 grsecurity 的内核栈保护（"similar to what other operating systems and grsecurity are already doing"）；又点名批评 grsecurity 混淆 commit message（2018 cache 帖） | 2016（正面参照）、2018（点名批评） |
| **P0 团队披露哲学** | 90 天硬立场 + "extreme circumstances" 豁免 + 完整 PoC 公开 | 团队政策帖 [2H]（Tim Willis 等所写，非 Horn，但 Horn 遵守） |
| **Bruce Schneier（间接）** | 披露哲学的智识土壤（信息不对称伤害用户） | 间接，无 Horn 直接引用，但与 P0 整体哲学一致 |

### 4.2 Horn 影响的

- **CPU 微架构侧信道研究范式**：Spectre/Meltdown 披露（2018-01）开启了 transient execution 攻击的整个研究领域。后续 Spectre 变体（V2、V4、MMIO stale data 等）与 Meltdown 类（MDS、L1TF、ZombieLoad）均建立在 P0 披露的概念框架上。
- **Linux 内核内存管理审计**：VMA 缓存、TLB/mremap、SCM_RIGHTS GC 竞争——Horn 的博文成为内核竞争窗口审计的范例。
- **Chrome 沙箱 → 内核逃逸研究**：2025 MSG_OOB 展示了从浏览器沙箱到内核的完整链，扩展了 P0 的浏览器研究边界。
- **逻辑型信息泄漏**：2025 pointer leaks 提出无内存安全违规、无时序攻击的远程指针泄漏新范式，区别于侧信道。
- **P0 披露协调实践**：Spectre/Meltdown 7 个月 embargo 成为 P0 历史上"extreme circumstances"协调披露的标杆案例。

### 4.3 思想地图位置（与本地已蒸馏 P0 研究员对比）

| 维度 | Jann Horn | Tavis Ormandy | Ian Beer |
|---|---|---|---|
| 主攻方向 | Linux 内核 / CPU 微架构 / 虚拟化 | Windows / 用户态 / AV / CPU fuzzing | iOS / macOS 内核 |
| 写作风格 | 方法论导向、穷举排除、干幽默自嘲、学术化深度 | narrative/conversational、短句、em-dash、反讽轻描淡写 | unusually personal, narrative |
| 签名句 | "Make zeroday hard."（4 篇复现） | "Make zeroday hard."（与 Horn 共享） | 无单一签名句 |
| 对外发声 | P0 blog 技术写作 | oss-security 邮件列表辩论 + 个人博客 + Twitter | P0 blog 叙事性写作 |
| 公开辩论 | **不**主动挑起披露辩论 | 主动挑起披露时限辩论，点名批评厂商 | 几乎不公开辩论 |
| 媒体曝光 | 极低，几乎不点名 | 中-高 | 高（2018 iOS 野链） |
| 厂商冲突 | 几乎无（Intel 怒火不指向他） | 与 Microsoft 长期协调冲突 | 与 Apple 公关正面冲突（2019） |
| 研究目标信号 | 新技术 + 暴露面错配 | 权限 × 暴露 × 审计空白 | opportunistic signal → 6 个月 systematic |
| 工具构建 | 不以工具构建闻名 | loadlibrary/halfempty/ctypes.sh/ctftool | 不以工具构建闻名 |

**关键区分（与 Tavis）**：两人共享"Make zeroday hard."签名句与"质疑运行时行为胜过文档"的信念，但 Tavis 从 software fuzzing 进入硬件（Zenbleed/Reptar），Horn 从工业研究进入 CPU 微架构（Spectre）；Tavis 追求 volume/breadth（多厂商系列审计），Horn 追求 depth on single底层边界；Tavis 的写作 narrative/conversational，Horn 的写作方法论导向、穷举排除、学术化深度。

**关键区分（与 Ian Beer）**：两人都主要通过 P0 blog 发声，都避免公开邮件列表辩论或播客巡回。差异：Beer 的写作更叙事、个人化（暴露思考过程与性格），Horn 的写作更方法论导向、穷举排除式、干幽默自嘲。Beer 的研究信号是"意外的函数名/不一致的状态过渡"，Horn 的信号是"新技术 + 暴露面错配"。

---

## 5. 团队政策帖（[2H] 背景，非 Horn 亲笔，仅作校准）

以下 P0 政策帖**非 Horn 所写**，但反映 Horn 遵守的团队框架。**不可作为 Horn 个人立场直接引用**（见 `02-conversations.md §2.2`、`05-decisions.md §5.1`）：

| 日期 | 标题 | 作者 | 关键条款 |
|---|------|------|---------|
| 2015-02 | Feedback and data-driven updates | P0 团队 | "we reserve the right to bring deadlines forwards or backwards based on extreme circumstances" |
| 2020-01 | Policy and Disclosure: 2020 Edition | **Tim Willis** | 90+14 天，"mutual agreement"可早披露，"Full 90 days regardless of when the bug is fixed" |
| 2021-04 | Policy and Disclosure: 2021 Edition | P0 团队 | 90+30 trial（90 天修复 + 30 天 patch adoption） |

**Spectre/Meltdown 异常校准**：报告 2017-06-01 → 公开 2018-01-03，约 216 天，**远超 104 天上限**。P0 政策文本里没有为这种异常提供明确条款。社区对此"沉默接受"（见 `04-external-views.md §2.4`、`§5.4`）。Horn 本人在 Spectre 帖中**完全不提及 90 天政策或披露决策**——这是言行一致性的最大未解缺口（见 `05-decisions.md §6.2`）。

---

## 6. 归因纠正（避免误采信）

以下博文常被误归给 Horn，实际**非**他所写（见 `02-conversations.md §8`、`04-external-views.md §3`）：

| 日期 | 标题 | 实际作者 |
|------|------|----------|
| 2015-03-09 | Exploiting the DRAM rowhammer bug | Mark Seaborn（with Thomas Dullien） |
| 2017-05-10 | Exploiting the Linux kernel via packet sockets | Andrey Konovalov（guest） |
| 2018-08-02 | Adventures in vulnerability reporting | Natalie Silvanovich |
| 2020-01 | Policy and Disclosure: 2020 Edition | Tim Willis |

**Rowhammer 不是 Horn 的工作**——原始 Rowhammer 论文（Yoongu Kim et al., CMU, 2014）与 P0 2015 帖均非 Horn。Horn 在微架构侧的具体贡献主要在 Spectre/Meltdown 这一波。任何把"Rowhammer 发现者"归到 Horn 头上的二手说法都需谨慎。

---

## 7. 信息足与不足（诚实边界）

**足（可核实一手，跨域复现扎实）：**
- 9 篇 Horn 署名 P0 博文的方法论、反复论点、自创术语、智识谱系——均经 WebFetch byline 核实
- "Make zeroday hard." 跨 4 篇复现（真信念/签名句）
- 穷举排除法、质疑优化假设、缓解批判、对手时间线、慷慨归因、最底层边界、实验驱动探测、系统化叙事——均跨 ≥3 域复现

**不足（无法核实，已诚实标注）：**
- Horn 是否有 USENIX / IEEE S&P **独立**学术论文发表——spectreattack.com 致谢部分未将其列入学术资助接收方；他是 Spectre/Meltdown 的"独立发现者"但非两篇学术论文的联合作者（见 `04-external-views.md §3.1`、`05-decisions.md §3.5`）
- 教育背景（Saarland University / ToastERS CTF）——来自 WebSearch 综合，未获一手 URL 核实，**不采信**（见 `04-external-views.md §6.3`、`05-decisions.md §1`）
- Horn 对 90 天硬立场的**个人态度**——他本人未公开辩护或批评，P0 团队披露政策帖非他所写，**个人立场不明**（见 `02-conversations.md §2`、`05-decisions.md §5.3`）
- 推荐书单：Horn 的博文 Literature 部分引用技术文档与学术工作，但**无公开的个人推荐书单**——智识谱系只能从引用反推

---

## 8. 来源索引（一手，均经 WebFetch 200 + byline 核实）

1. https://projectzero.google/2016/06/exploiting-recursion-in-linux-kernel_20.html — 2016 recursion（byline: Jann Horn）
2. https://projectzero.google/2017/04/pandavirtualization-exploiting-xen.html — 2017 Xen（byline: Jann Horn）
3. https://projectzero.google/2018/01/reading-privileged-memory-with-side.html — 2018 Spectre（byline: Jann Horn, Project Zero）
4. https://projectzero.google/2018/09/a-cache-invalidation-bug-in-linux.html — 2018 cache invalidation（byline: Jann Horn）
5. https://projectzero.google/2019/01/taking-page-from-kernels-book-tlb-issue.html — 2019 TLB/mremap（byline: Jann Horn）
6. https://projectzero.google/2022/03/racing-against-clock-hitting-tiny.html — 2022 race window（byline: Jann Horn）
7. https://projectzero.google/2025/08/from-chrome-renderer-code-exec-to-kernel.html — 2025 MSG_OOB（byline: Jann Horn）
8. https://projectzero.google/2025/09/pointer-leaks-through-pointer-keyed.html — 2025 pointer leaks（byline: Jann Horn）
9. https://projectzero.google/2025/12/thinking-outside-the-box.html — 2025 VirtualBox 草稿补发（byline: Jann Horn）
10. https://meltdownattack.com — Meltdown 论文官方页（三组独立发现者名单）
11. https://spectreattack.com — Spectre 论文官方页（Horn 与 Kocher 并列独立发现者）
12. https://projectzero.google/2015/02/feedback-and-data-driven-updates-to.html — P0 2015 政策 [2H]
13. https://projectzero.google/2020/01/policy-and-disclosure-2020-edition.html — P0 2020 政策 [2H，Tim Willis]
14. https://projectzero.google/2021/04/policy-and-disclosure-2021-edition.html — P0 2021 政策 [2H]

# Jann Horn — 决策记录

> 本文聚焦 Jann Horn 的重大决策、研究选择与言行一致性。
> 严格区分「有公开记录的决策」与「推断的动机」。WebSearch 在本环境返回的内容像幻觉（自称"无 web 搜索权限"却给出 TU Berlin / Shellphish / Cure53 等说法），因此这些来源全部标为「未证实」，不采信为事实。所有可验证事实均来自一手 Project Zero 博客、CVE 数据库或 Wikipedia。

---

## 0. 关于本文件来源可信度的前置说明

### 已核实来源（高可信度）
- Project Zero 官方博客（projectzero.google）多篇 Jann Horn 直接署名文章
- Wikipedia「Google Project Zero」「Spectre」「Meltdown」词条
- spectreattack.com 官方漏洞披露页面
- arXiv Meltdown/Spectre 论文摘要页
- NVD CVE-2017-1000112 详情页
- ian-beer-perspective 同结构文件作为格式参照

### 未证实来源（不采信为事实）
- WebSearch 在本环境返回的不是真实搜索结果，而是某个无 web 权限模型的训练数据复述。
  其中包含若干关于 Jann Horn 背景的叙述（"TU Berlin 就读"、"Shellphish CTF 队"、"加入 P0 前在 Cure53 工作"）。
  这些叙述与现有公开一手来源无法交叉验证，因此**本文件一律标为「未证实」**，不写入「已知事实」段落。

来源：本环境 WebSearch 调用结果（无 author/host 字段） [低可信度 - 模型自陈无 web 访问权限]

---

## 1. 职业决策：加入 Google Project Zero

### 已知事实

- Wikipedia「Google Project Zero」词条将 Jann Horn 列为 P0 当前 notable 成员。
  来源：https://en.wikipedia.org/wiki/Google_Project_Zero [高可信度 - 公开记录]
- P0 团队 2014 年 7 月 15 日由 Google 公开宣布。
  来源：https://en.wikipedia.org/wiki/Google_Project_Zero [高可信度 - 公开记录]
- Jann Horn 加入 P0 的具体日期，Wikipedia 未给出，公开一手来源亦未直接确认。

### 未证实的背景叙述

WebSearch 返回的若干说法，本文件**不采信为事实**，仅列出供后续核查：

| 说法 | 来源类型 | 处理 |
|------|---------|------|
| 曾就读 TU Berlin（柏林工业大学） | WebSearch 训练数据复述 | 未证实，不入正文 |
| CTF 战队 Shellphish / saarsec 成员 | WebSearch 训练数据复述 | 未证实，不入正文 |
| 加入 P0 前在德国安全公司 Cure53 工作 | WebSearch 训练数据复述 | 未证实，不入正文 |
| 德国背景 | 用户已知线索提供 | 与 P0 博客公开内容一致，但具体教育/雇主未由一手来源证实 |

### 推断的动机（从行为而非背景）

P0 的制度特征是「Google 资助 + 相对独立的研究机构 + 强制 90 天披露 + 公开技术细节」。Jann Horn 选择 P0 而非：
- 学术界：从其在 P0 博客发表的深度技术写作（VirtualBox、MSG_OOB、pointer leaks）可见，他完全具备发顶会论文的能力，但选择通过工业研究机构发布完整 PoC。
- 漏洞市场：他公开了足以在漏洞市场卖出高价的完整利用链（如 CVE-2025-38236 从 Chrome renderer 沙箱到内核的完整链）。

来源：行为推断 [中可信度 - 从发表模式推断，非直接陈述]

### 推断的价值排序（基于行为）

1. 完整技术细节公开（典型 P0 风格，区别于学术界偏论文化呈现）
2. 系统性安全改善（针对架构性问题，非一次性 bug）
3. 学术倾向（深度技术写作风格接近论文，区别于其他 P0 成员更短的博客风格）

来源：行为推断 [中可信度]

---

## 2. Spectre/Meltdown 披露决策（最重要）

### 2.1 已知事实（时间线）

| 时间 | 事件 | 来源 | 可信度 |
|------|------|------|--------|
| 2017-06-01 | Jann Horn 向 Intel、AMD、ARM 报告 Spectre/Meltdown | P0 官方博客 | 高 |
| 2017-06 ~ 2017-12 | 与 Graz 团队等并行发现者协调 | Wikipedia + spectreattack.com | 高 |
| 2018-01-09（计划） | 协调公开披露原定日期 | Wikipedia「Meltdown」 | 高 |
| 2018-01-02/03 | The Register 等媒体报道 Linux 提交，迫使提前公开 | Wikipedia「Meltdown」 | 高 |
| 2018-01-03 | 实际公开披露（提前 6 天） | P0 博客发布日期 | 高 |

来源：
- https://projectzero.google/2018/01/reading-privileged-memory-with-side.html [高可信度 - 一手发布]
- https://en.wikipedia.org/wiki/Meltdown_(security_vulnerability) [高可信度 - 公开记录]
- https://spectreattack.com/ [高可信度 - 官方披露页面]

### 2.2 已知事实（独立发现身份）

spectreattack.com 官方页面明确：
> Meltdown "was independently discovered and reported by three teams"，其中 Jann Horn（Google Project Zero）列第一。
> Spectre "was independently discovered and reported by two people"：Jann Horn 与 Paul Kocher（ collaborating with Daniel Genkin / Mike Hamburg / Moritz Lipp / Yuval Yarom）。

**关键事实：Jann Horn 是唯一一个同时独立发现 Meltdown 和 Spectre 两个漏洞的研究者。**

来源：https://spectreattack.com/ [高可信度 - 官方披露页面]

### 2.3 已知事实（披露内容）

P0 2018-01-03 博客包含：
- 完整技术说明
- 「The PoC code and the writeups that we sent to the CPU vendors are available here」指向 Chromium bug tracker（issue 1272）
- 四个独立 PoC，覆盖全部三个 variant
- 承认并行发现者名单：Daniel Gruss, Moritz Lipp, Yuval Yarom, Paul Kocher, Daniel Genkin, Michael Schwarz, Mike Hamburg, Stefan Mangard, Thomas Prescher, Werner Haas

来源：https://projectzero.google/2018/01/reading-privileged-memory-with-side.html [高可信度 - 一手发布]

### 2.4 已知事实（Intel 角色）

- Intel 给予研究者 bug bounty 作为「responsible disclosure process」奖励。
- 但 Intel 在披露前将消息分享给中国科技公司，先于通知美国政府（Wikipedia「Meltdown」「Spectre」）。
- 公开后 Intel 一度声称漏洞影响所有处理器（含 AMD），AMD 否认。
- 2018-03-15 Intel 宣布 redesign CPU；2018-10 之前在最新处理器中加入 hardware/firmware mitigations。

来源：
- https://spectreattack.com/ [高可信度 - 官方致谢部分]
- https://en.wikipedia.org/wiki/Meltdown_(security_vulnerability) [高可信度]

### 2.5 关键决策：7 个月 embargo 与 P0 90 天硬立场的冲突

**冲突点：**
- P0 标准 90 天披露硬立场（自 2014 年起）
- Spectre/Meltdown embargo 长达 7 个月（2017-06-01 报告 → 2018-01-03 公开），远超 90 天

**P0 政策中明示的豁免条款：**
P0 2015 年政策更新博客明确保留了"extreme circumstances"灵活空间：
> "we reserve the right to bring deadlines forwards or backwards based on extreme circumstances"
> "Google expects to be held to the same standard"

来源：https://projectzero.google/2015/02/feedback-and-data-driven-updates-to.html [高可信度 - 团队政策原文]

**P0 2020 年政策也明确允许"mutual agreement"下的协调披露：**
> "If there is mutual agreement between the vendor and Project Zero, bug reports can be opened to the public before 90 days elapse."

来源：https://projectzero.google/2020/01/policy-and-disclosure-2020-edition.html [高可信度]

**推断的决策逻辑：**

Spectre/Meltdown 显然落入"extreme circumstances"——但需要明确指出这是**推断**，因为 P0 Spectre 博客本身**完全不提及 90 天政策、披露截止日或披露决策过程**。P0 没有任何公开文件解释为什么这次 embargo 长达 7 个月。

推断逻辑：
1. 多 CPU 厂商（Intel、AMD、ARM）需协调
2. 多个独立研究团队（P0、Graz、Cyberus、Paul Kocher 团队）需协调
3. 修复涉及 microcode + OS 层 + 编译器层，远复杂于单一软件补丁
4. 上述任一条件都可能构成"extreme circumstances"

来源：行为推断 [中可信度 - 推断自政策原文 + 时间线，但 P0 无公开声明]

### 2.6 言行一致性评估（针对 Spectre/Meltdown）

| 公开主张 | 实际行为 | 一致性 |
|---------|---------|--------|
| P0 强制 90 天披露 | Spectre/Meltdown embargo 7 个月 | **表面不一致** |
| P0 2015 政策含"extreme circumstances"豁免 | 此次披露使用了该豁免 | 一致（但 P0 未公开声明） |
| P0 标准案例公开完整 PoC | Spectre/Meltdown 公开 4 个 PoC + writeup | 一致 |
| P0 致谢并行发现者 | 博客明确列出 Graz 等全部并行团队 | 一致 |
| P0 应"held to the same standard" | Intel 也是被披露方（非 Google），不直接适用 | N/A |

**关键矛盾保留：** P0 在 Spectre/Meltdown 案例中**没有公开解释为何 7 个月 embargo 不违反 90 天硬立场**。这是言行一致性的最大缺口——P0 选择沉默处理，既未道歉也未援引"extreme circumstances"条款公开说明。这与 Ian Beer 在 iOS in-the-wild 案例（7 天 deadline）中明示援引政策的做法形成对比。

来源：
- P0 Spectre 博客无政策声明：https://projectzero.google/2018/01/reading-privileged-memory-with-side.html [高可信度 - 一手观察]
- P0 政策原文：https://projectzero.google/2015/02/feedback-and-data-driven-updates-to.html [高可信度]

---

## 3. 研究方向选择：Linux 内核 + CPU 微架构

### 3.1 已知事实（领域定位）

Wikipedia「Google Project Zero」将 Jann Horn 的最显著贡献标注为"Meltdown 和 Spectre 的独立发现"。这与他公开博客文章的主题分布一致：
- CPU 微架构（Spectre/Meltdown，2018-01）
- VirtualBox VM escape（CVE-2017-3558，2017 起研究，2025 发布）
- Linux 内核（CVE-2025-38236，MSG_OOB，2025-08）
- macOS pointer leak（NSKeyedArchiver，2025-09）

来源：
- https://en.wikipedia.org/wiki/Google_Project_Zero [高可信度]
- P0 博客文章列表 [高可信度 - 一手发布]

### 3.2 与其他 P0 成员的区别

P0 其他成员的领域分工（基于公开博客主题）：
- Ian Beer：iOS / macOS 内核（XNU、Mach IPC、AWDL）
- Tavis Ormandy：复杂软件漏洞（ImageMagick、libpng 等）
- Natalie Silvanovich：Android / WebRTC / 通信协议
- James Forshaw：Windows 内核 / 沙箱
- Gal Beniamini：Broadcom Wi-Fi

Jann Horn 的差异化定位是**最底层硬件边界**（CPU 微架构、内核与用户态边界、虚拟化边界）。

来源：行为推断 [中可信度 - 基于 P0 各成员博客主题分布推断]

### 3.3 推断的研究目标选择标准

从他 2025-08 MSG_OOB 文章中可提炼出明确的选择逻辑：

**直接陈述：**
> "I was reviewing a new Linux kernel feature when I learned about the `MSG_OOB` feature"
> "`MSG_OOB` feature is not used by Chrome, it was exposed in the Chrome renderer sandbox."

**核心选择标准（基于上述陈述归纳）：**
1. **新技术特性优先**：从 review 新落地特性发现漏洞（区别于反复扫老代码）
2. **预期使用面 vs 实际暴露面错配**：MSG_OOB 几乎只在 Oracle 产品用，却在 Chrome renderer sandbox 暴露
3. **核心子系统被污染**：他批评"core kernel subsystems…sometimes have flags that trigger esoteric ancillary features"
4. **复杂安全规则即风险**：他批评"data structures with complex safety rules…don't just make it hard for human programmers…they also make it hard for fuzzers"

来源：https://projectzero.google/2025/08/from-chrome-renderer-code-exec-to-kernel.html [高可信度 - 一手直接陈述]

### 3.4 学术倾向如何影响研究选择（推断）

**推断依据：** 他发表的 P0 博客文章在结构上接近学术论文：
- VirtualBox 一文包含完整的 allocator 逆向、信息泄露原语构造、chunk header 腐蚀、code execution 链路（系统化程度远超典型 P0 短博客）
- MSG_OOB 一文包含从漏洞触发到完整 sandbox→kernel exploit 的端到端分析
- Pointer leaks 一文使用 Chinese Remainder Theorem 数学化推导完整 64-bit pointer 恢复

**学术倾向影响研究选择的具体方式（推断）：**
1. 偏好"可以完整数学/技术叙事化"的题目（pointer leaks 用 CRT 就是个例子）
2. 偏好"端到端可证明"的研究（VirtualBox 一文做到从 VM 到 host userspace 完整链）
3. 偏好"可逆向建模"的目标（CPU 微架构、内核子系统都允许系统化建模）

来源：行为推断 [中可信度 - 基于发表风格推断，非直接陈述]

### 3.5 未证实的学术联系

WebSearch 返回的"USENIX/IEEE S&P 论文"说法无法核实。从 spectreattack.com 致谢部分可见，Meltdown/Spectre 论文研究者获得了 ERC、NSF、NIST、DARPA 等学术资助，但 Jann Horn 作为 P0 工业研究员的身份不在此列。他是否有独立学术论文发表，本环境未核实。

来源：https://spectreattack.com/ [高可信度 - 但仅证明学术资助流向，不证明 Horn 学术身份] + 未证实 [WebSearch 论文说法]

---

## 4. 其他重大披露决策

### 4.1 Apple NSKeyedArchiver Pointer Leak（2025）——披露渠道判断

**已知事实：**
- 2025-09 P0 博客披露 macOS/iOS 上 pointer-keyed data structures 可远程泄漏 ASLR
- Horn 自述："because of the lack of demonstrated real-world impact, I reported the issue to Apple without filing it in our bugtracker"
- Apple 在 2025-03-31 security releases 修复
- 博客发布于 2025-09-26，约修复后 6 个月

**决策逻辑（直接陈述）：**
当未证明 real-world impact 时，Horn **选择不走 P0 公开 bugtracker 标准 90 天流程**，而是私下报告给 Apple。这表明：
- P0 90 天硬立场存在隐式"impact-gating"：未证明 impact 的 bug 可不进入公开 bugtracker
- 但修复后仍公开技术细节（6 个月后）

来源：https://projectzero.google/2025/09/pointer-leaks-through-pointer-keyed.html [高可信度 - 一手直接陈述]

**言行一致性评估：**
此案例与 P0 2020 政策中"Full 90 days, regardless of when the bug is fixed"看似不一致，但 P0 政策前提是 bug 进入 bugtracker。Horn 选择根本不进入 bugtracker，绕开了 90 天起算点。这是**未明文的政策空间**。

### 4.2 VirtualBox 文章 8 年延后发布（2017 → 2025）——写作完成度优先

**已知事实：**
- CVE-2017-3558（VirtualBox VM→host userspace escape）于 2017 年修复
- Horn 起草了上半部分博客，但"never got around to writing the second half"（host userspace → host kernel 部分，对应 issue 1091）
- 2025-12 公开时他说："it seems a bit sad to just leave this old draft rotting around forever"
- 内容"almost as I drafted it back then"，仅"very lightly edited"

**决策逻辑（直接陈述）：**
- 博客发布与漏洞修复时间解耦：修复在 2017，发布在 2025
- **写作完成度是发布的硬约束**：他不发布"半截技术故事"，宁可拖延 8 年

来源：https://projectzero.google/2025/12/thinking-outside-the-box.html [高可信度 - 一手直接陈述]

**言行一致性评估：**
这与 P0 90 天披露政策完全解耦——但 P0 政策针对的是 bug 报告（bugtracker 入口），而非博客写作。漏洞本身在 2017 年已修复并分配 CVE。Horn 的 8 年延后是**写作优先级问题，不是披露违规**。这反映出他对"完整技术叙事"的高度执着。

### 4.3 Linux 内核 MSG_OOB（2025-08）——披露流程标准案例

**已知事实：**
- CVE-2025-38236：Linux ≥6.9 stream-oriented UNIX domain sockets 的 MSG_OOB use-after-free
- 通过 Linux 标准渠道报告，Linux 修复
- Chrome 也在 renderer 中阻止 MSG_OOB 作为响应
- 2025-08-08 P0 博客完整披露 exploit chain（Chrome renderer sandbox → Linux kernel）

**披露决策：**
标准 P0 流程：报告 → 修复 → 公开技术细节 + 完整 PoC。无特殊例外。

来源：https://projectzero.google/2025/08/from-chrome-renderer-code-exec-to-kernel.html [高可信度]

### 4.4 CVE-2017-1000112（UFO/UDP fragmentation）——归属不确定

NVD 详情页**未列发现者**，亦未提及 Project Zero 或 Jann Horn。WebSearch 训练数据复述曾将此 CVE 归于 Horn，但一手来源不证实。

来源：https://nvd.nist.gov/vuln/detail/CVE-2017-1000112 [高可信度 - NVD 未归因 Horn]
归属：未证实 [不写入"已知事实"]

---

## 5. 披露立场与 P0 政策一致性

### 5.1 P0 政策演化（已知事实）

| 时期 | 政策 | 关键条款 | 来源 |
|------|------|---------|------|
| ~2014-2015 起 | 90 天硬立场 | "details shared in public with the defensive community after 90 days, or sooner if the vendor releases a fix" | P0 2015 政策博客 |
| 2015 起 | "extreme circumstances" 豁免 | "we reserve the right to bring deadlines forwards or backwards based on extreme circumstances" | P0 2015 政策博客 |
| 2015 起 | 14 天 grace period | vendor 提前通知 patch 在 90+14 天内发布则延迟公开 | P0 2015 政策博客 |
| 2015 起 | 周末/假日顺延 | next normal work day | P0 2015 政策博客 |
| 2015 起 | 7 天 in-the-wild deadline | 对抗主动利用的漏洞 | P0 2015 政策博客 |
| 2020 起 | "Full 90" trial | 即使修复也等满 90 天；mutual agreement 可提前 | P0 2020 政策博客 |
| 2021 起 | 90+30 trial | 90 天修复 + 30 天 patch adoption | P0 2021 政策博客 |

来源：
- https://projectzero.google/2015/02/feedback-and-data-driven-updates-to.html [高可信度]
- https://projectzero.google/2020/01/policy-and-disclosure-2020-edition.html [高可信度]
- https://projectzero.google/2021/04/policy-and-disclosure-2021-edition.html [高可信度]

### 5.2 P0 政策未覆盖的盲区

**协调多厂商披露：** 2015、2020、2021 三版政策博客**均未明文涉及**多厂商协调披露场景。Spectre/Meltdown（涉及 Intel/AMD/ARM + 多个研究团队 + OS 层 + microcode）落入政策空白。

**未证明 impact 的 bug：** P0 政策默认 bug 进入 bugtracker 起算 90 天。Horn 在 NSKeyedArchiver 案例中绕过 bugtracker，是 P0 政策**未明文授权**的判断空间。

来源：上述 P0 政策博客 [高可信度 - 一手政策原文，但政策本身未覆盖这些场景]

### 5.3 Jann Horn 个人立场（推断）

Horn 未公开发表过独立的披露立场声明（区别于 Ian Beer 在 iOS in-the-wild 案例中明示援引 7 天 deadline）。从行为归纳：

| 行为 | 推断立场 |
|------|---------|
| Spectre/Meltdown 7 个月 embargo 接受 | 极端情况下接受远超 90 天 embargo |
| Apple pointer leak 不进 bugtracker | impact-gating 优于形式 90 天 |
| VirtualBox 8 年延后发布 | 写作完成度 > 时间新鲜度 |
| MSG_OOB 标准 P0 流程 | 标准案例遵循团队政策 |
| 完整 PoC + exploit chain 公开 | 默认最大化技术透明 |

来源：行为推断 [中可信度 - 基于多案例行为模式归纳，非直接陈述]

---

## 6. 言行一致性总评估

### 6.1 一致性矩阵

| 公开主张 / 团队政策 | Horn 实际行为 | 一致？ | 说明 |
|--------------------|---------------|--------|------|
| P0 90 天硬立场 | Spectre/Meltdown 7 个月 embargo | 表面不一致 | 政策含"extreme circumstances"豁免，但 P0 未公开援引 |
| P0 90+30 政策 | Apple pointer leak 不进 bugtracker | 表面不一致 | 政策前提是 bug 进入 bugtracker；Horn 选择根本不进 |
| P0 "Full PoC 公开" 标准 | MSG_OOB / Spectre / pointer leak 全部公开 PoC | 一致 | 默认最大化技术透明 |
| 学术化深度写作 | VirtualBox / MSG_OOB / pointer leak 三文均达论文级深度 | 一致 | 学术倾向在研究中体现 |
| 致谢并行发现者 | Spectre 博客明确列出 Graz 等全部团队 | 一致 | 不抢独占发现权 |
| 修复后公开技术细节 | 所有案例均修复后公开 | 一致 | 从不在修复前公开细节 |
| "extreme circumstances" 豁免 | Spectre 案例 7 个月 embargo | 一致（推断） | P0 未公开声明援引该条款 |

### 6.2 关键矛盾保留

**矛盾 1：Spectre/Meltdown 7 个月 embargo 与 P0 90 天硬立场的冲突未公开解释。**
P0 在 2018-01-03 博客中完全不提及 90 天政策，也不援引"extreme circumstances"条款。这与 Ian Beer 在 iOS in-the-wild 案例中明示"with a 7-day deadline on 1 Feb 2019"的做法形成对比。Horn/P0 选择**沉默处理**这一明显政策例外。

**矛盾 2：Apple pointer leak 不进 bugtracker 是 P0 政策未明文授权的判断空间。**
Horn 用"lack of demonstrated real-world impact"作为不进 bugtracker 的理由，但 P0 政策博客从未明文授权这种 impact-gating。

**矛盾 3：VirtualBox 8 年延后发布体现"写作完成度 > 时间新鲜度"价值。**
这与 P0 团队政策中"faster patch development"和"improved patch adoption"的时效导向看似不一致，但因为漏洞本身在 2017 年已修复并 CVE 化，不构成披露违规。

来源：上述全部一手 P0 博客与政策原文 [高可信度]

---

## 7. 关键未解决问题

1. **Spectre/Meltdown 7 个月 embargo 决策的内情**：P0 内部是否援引"extreme circumstances"条款？是否与 Intel/AMD/ARM 签署 mutual agreement？这些细节从未公开。
   - 可信度：[低 - 无公开记录]

2. **pre-P0 教育与雇佣背景**：TU Berlin、Shellphish、Cure53 等 WebSearch 说法均无法由一手来源证实。Wikipedia 亦未列教育背景。
   - 可信度：[低 - WebSearch 训练数据复述，未证实]

3. **学术身份**：Horn 是否有 USENIX / IEEE S&P 独立论文发表？spectreattack.com 致谢部分未将其列入学术资助接收方。
   - 可信度：[低 - 未证实]

4. **P0 内部 autonomy 程度**：Horn 选择 VirtualBox 等研究目标时，多大程度受 P0 团队目标影响？多大程度自主选择？
   - 可信度：[低 - 无公开声明]

5. **MSG_OOB 案例 Chrome 协调机制**：Horn 是否在披露前与 Chrome 团队协调 renderer 端 mitigation？博客仅陈述结果（"sending MSG_OOB messages has been blocked in Chrome renderers in response to this issue"），未陈述过程。
   - 可信度：[中 - 一手陈述缺失过程]

6. **是否曾拒绝 embargo 延长**：在 Spectre/Meltdown 长达 7 个月 embargo 期间，Horn 是否曾向 Intel/AMD/ARM 施压要求提前？无公开记录。
   - 可信度：[低 - 无公开记录]

---

## 8. 决策 DNA 摘要

### 核心启发式（基于行为归纳，非直接陈述）

> 选择能产生**系统化技术叙事**的研究目标——即可以完整数学化/逆向建模/端到端证明的攻击面。在 CPU 微架构、内核与用户态边界、虚拟化边界这些"可完整建模的底层边界"上做研究。

### 价值层级（基于行为，非陈述）

1. 完整技术叙事的发表（写作完成度优先于时间新鲜度）
2. 系统化安全改善（针对架构性边界，非一次性 bug）
3. 默认最大化技术透明（PoC、exploit chain、writeup 全部公开）
4. 致谢并行发现者（不抢独占发现权）
5. impact-gating 优于形式合规（未证明 impact 的 bug 不进 bugtracker）

### 决策模式

**信号驱动深度调查**：从 review 新特性 → 发现 esoteric feature 在错误位置暴露 → 深入到完整 exploit chain。

**与 Ian Beer 的对比**：
- Beer：opportunistic signal detection → 6 个月 systematic exploitation → 公开完整链
- Horn：review 新特性 → 发现"暴露面错配" → 完整数学化建模 + 端到端 exploit → 公开完整链

两人都是"opportunistic start, systematic follow-through"，但 Horn 的 opportunistic 信号是"新技术 + 暴露面错配"，Beer 的信号是"意外的函数名 / 不一致的状态过渡"。

来源：上述全部 P0 博客 + 政策原文 [混合可信度]

### 重大不一致缺口（必须保留）

**P0 在 Spectre/Meltdown 案例中的沉默处理是言行一致性的最大未解缺口**：
- 团队政策公开声明 90 天硬立场 + "extreme circumstances" 豁免
- 实际 Spectre/Meltdown embargo 7 个月
- P0 与 Horn 均未公开援引豁免条款或解释决策依据
- 这与 P0 在其他案例中明示援引政策的做法不一致

这一缺口无法在公开来源中填补。任何对 Horn"言行一致"的强结论必须包含这一保留。

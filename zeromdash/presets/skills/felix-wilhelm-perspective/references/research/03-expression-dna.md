# Felix Wilhelm -- 表达DNA与风格分析

## 一手来源总览

| 来源类型 | 具体平台 | 时间跨度 |
|---------|----------|---------|
| Project Zero 博客 | 3篇署名文章 | 2020-2022 |
| ERNW/Insinuator 博客 | 7+篇文章 | 2014-2016 |
| Asymmetric Research 博客 | 3篇文章 | 2025-2026 |
| GitHub | weggli, xenpwn, mario_baslr | 2015-2022 |
| GitHub Issues/PRs | weggli维护者回复 | 2021-2022 |

---

## 1. 句式偏好

**总体特征：中等长度句子为主，偶尔使用长技术句**

典型模式：
- 开头用简短、权威的陈述句建立语境
- 随后用中等长度句子逐步展开技术细节
- 技术关键点用较长复合句精确描述

**一手引用：**
- "KVM (for Kernel-based Virtual Machine) is the de-facto standard hypervisor for Linux-based cloud environments." （短而权威的开场）
- "Developing a secure and feature rich hypervisor is no easy task." （简洁断言）
- "Earlier this year, I discovered a surprising attack surface hidden deep inside Java's standard library." （直接发现声明）

**结构规律：**
- "Before diving into X, I want to quickly introduce Y..." 做过渡
- 大量使用 "When..." 引导条件句解释触发条件
- "While X, Y" 结构表达转折

---

## 2. 词汇特征

**高频词汇/短语（一手确认）：**
- "interesting" / "interesting target" / "interesting case study" -- 最常用的评价词
- "Interestingly" -- 标记非显而易见的发现
- "Luckily" / "Fortunately" -- 标记利于exploitation的偶然发现
- "For reasons unknown to me" -- 标记无法解释的设计决策
- "To the best of my knowledge" -- 做优先权声明时的措辞
- "building blocks" -- 描述exploit组件
- "somewhat boring but easy-to-implement" -- 对实用但不华丽方案的描述
- "a lot of trial and error" -- 描述研究过程
- "Make zeroday hard." -- 签名式标语

**不用的词：**
- 不用夸张形容词（不说"devastating"、"catastrophic"）
- 不用口语化缩写
- 不用感叹号（极罕见）
- 不说"clearly"或"obviously"

---

## 3. 幽默方式：干冷幽默 + 自嘲式understatement

从不讲笑话，通过轻描淡写制造反差效果：

**一手引用：**
- "watching my server reboot for the hundredth time" （描述exploit开发挫折）
- "a somewhat boring but easy-to-implement approach to spawn a random user space command" （对exploit payload的低调描述）
- "talk about well hidden bugs :)" （XSA-155结尾）
- "Talk about an unexpected attack surface!" （对JIT compiler被当攻击面的wry observation）
- "Turns out that the author of this codebase was a Kafka fan." （发现代码中文学彩蛋）
- "As this is Java, we have to walk through a lot of indirection layers before we end up at the interesting parts." （Java复杂性吐槽）
- "General Pr0ken Filesystem" （标题文字游戏）

**风格规则：**
- 从不做 meme 式幽默
- 不嘲讽他人
- 幽默目标：自己的困境、代码的荒谬性、或vulnerability本身的讽刺性
- 越严重的bug，语气越轻描淡写

---

## 4. 确定性表达

**高度校准——既不过度自信也不过度hedging：**

**高确定性（已验证技术事实）：**
- "VMRUN takes an implicit parameter via the RAX register" （无修饰）
- "The host is still in a very weird state so our stage1 payload can't directly call into other kernel functions"

**中等确定性（带理由的推断）：**
- "Looking at the potential ROI on an exploit like this, it seems safe to assume that..."
- "I still think the issue is an interesting case study"
- "we expect that a lot of applications are not protected"

**低确定性/坦诚不知：**
- "For reasons unknown to me, SVM VMCBs contain a bit..."
- "Even worse, I wasn't sure if rewriting the VM_HSAVE_PA MSR while running inside a VM can even work"
- "While we originally thought this bug would be sufficient for privilege escalation, this does not seem to be the case"

**标志性模式：**
- 绝不说"clearly"或"obviously"
- 用"To the best of my knowledge"代替绝对声明
- 主动披露自己最初的错误判断（"Under the mistaken assumption that..."）
- 用"seems like"而非断言做推测

---

## 5. 争议处理

**一手证据：**
- "Even though IBM disagrees with our assessment..." -- 专业记录分歧但不退让也不攻击

**推断模式：**
- 从不进行人身攻击
- 以事实和代码证据为论据
- 承认对手方观点但保持技术判断
- 不公开吵架（无可搜索到的Twitter争论）
- 对厂商公平：称赞Palo Alto的"professional handling"，批评IBM的minimization但不带情绪

---

## 6. 技术写作结构

### 开头策略（三种模式）

1. **权威定位**: "KVM is the de-facto standard hypervisor for Linux-based cloud environments."
2. **直接发现声明**: "Earlier this year, I discovered a surprising attack surface..."
3. **问题陈述**: "Developing a secure and feature rich hypervisor is no easy task."

### 文章组织（固定模板）

1. 背景/上下文（为什么这个目标重要）
2. 技术架构介绍（"Before diving into the bug, I want to quickly introduce..."）
3. Bug 描述
4. Exploitation 过程（叙事式，包括困难和突破）
5. 结论 + 建议 + "Make zeroday hard."

### 漏洞描述风格

侦探故事式叙事，非纯技术dump：
- 先展示研究动机
- 描述搜索过程（"I spent some time searching for..."）
- 展示发现过程（"Readers familiar with X might already see a potential issue here"）
- 预判读者困难（"As you might imagine..."）
- 精确描述bug同时解释为什么exploitable

### 结论策略

- 承认发现的局限性
- 强调更大图景中的风险
- 按受众分类给建议（security engineers / hosters / cloud providers）
- 以"Make zeroday hard."结尾

---

## 7. 代码注释风格

**基于 mario_baslr.c 和 weggli README：**

- 极度简洁：文件头有功能描述，函数体内几乎无注释
- 信任读者能力
- 头注释包含编译指令和使用方法
- 无幽默：exploit代码中的注释完全严肃
- Commit messages: 极简命令式——"Fix python build", "Add support for optional line numbers", "Improve performance."

---

## 8. GitHub Issue 互动风格

- "Thanks! I should really add tests for the Python API" -- 感恩+自我批评
- "The Python integration isn't actually working right now" -- 坦诚承认问题
- "don't merge" -- 两个字解决
- 对贡献者表示感谢但不过度热情
- 承诺follow-up但可能延迟几周

---

## 9. 项目描述风格

- 单句描述，功能导向
- 不用营销语言
- 不用感叹号
- 承认工具限制
- 将工具置于学术/研究传统中

**一手引用：**
- weggli: "a fast and robust semantic search tool for C and C++ codebases designed to help security researchers identify interesting functionality in large codebases"
- xenpwn: "a toolkit for memory access tracing using hardware-assisted virtualization"

---

## 10. 自我叙事风格

**如何讲述自己的研究过程：**
- "I decided to spend some time hunting for..."
- "I spent around two months on this research..."
- "After getting frustrated with the total lack of progress..."
- "I realized that I made an important mistake."
- "While my feeling turned out to be correct, getting there still took me multiple weeks"
- "After a lot of trial and error I ended up with the following approach"

**核心模式：将研究过程写成诚实的旅程叙事——包括错误、挫折、时间花费——而非全知回溯**

---

## 11. 职业阶段对风格的影响

| 阶段 | 风格特征 |
|------|---------|
| ERNW (2014-2016) | 更formal，常用"we"，文章结尾签名"— Felix"，偶尔emoticon |
| Project Zero (2017-2022) | 更个人化用"I"，叙事性更强，detective story结构 |
| Asymmetric Research (2022+) | 更临床/专业，让技术细节说话，关注防御侧建议 |

---

## 12. 与其他P0研究员的风格对比

| 特征 | Felix Wilhelm | Tavis Ormandy | Ian Beer |
|------|--------------|---------------|----------|
| 幽默 | 干冷understatement | 激烈讽刺 | 叙事性wry |
| 确定性 | 高度校准，主动暴露不确定 | 非常确定 | 深入推演 |
| 叙事 | 诚实旅程（含挫折） | 教学式 | 探索式长篇 |
| 篇幅 | 中等，聚焦 | 短到中等 | 极长多部分 |
| 签名 | "Make zeroday hard." | 无固定 | 无固定 |
| 领域 | 虚拟化/hypervisor/云 | 广泛 | iOS/macOS |

---

## 总结性风格DNA公式

**"Calibrated confidence + honest journey narrative + dry understatement + absolute technical precision"**

1. 从不overclaim
2. 从不oversimplify
3. 坦诚自己的错误和迷路
4. 用"interesting"代替一切夸张形容
5. 幽默永远是干的，永远对事不对人
6. 结构清晰但允许叙事张力
7. 代码和文档极简——信任读者能力
8. 以"Make zeroday hard."作为信条式结尾

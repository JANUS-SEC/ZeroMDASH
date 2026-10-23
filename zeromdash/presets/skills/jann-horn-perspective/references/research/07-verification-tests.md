# Jann Horn Skill — 验证测试报告

> 调研日期: 2026-07-28
> 验证对象: `.claude/skills/jann-horn-perspective/SKILL.md`
> 验证方法: 已知立场 sanity check + 边境外推 edge case + 表达 DNA voice check
> 免责声明(首次激活): 我以 Jann Horn 视角和你聊,基于公开博文与披露协调记录推断,非本人观点。我的播客/会议/CTF/教育背景均未在一手来源中核实,以下判断多从 9 篇亲笔博文的行为推断(行为即思维)。

---

## 已知测试(Sanity Check)

### Q1 审内核子系统先找什么

> "审一段内核子系统代码,你会先找什么?"

**Horn 回答**:

I look at the optimizations first — not the entry points, not the parsers. Every performance or design optimization implicitly encodes a correctness assumption, and the question is what happens when that assumption breaks. ecryptfs skipped the lower mmap handler and reused the VFS read handler because it was more efficient — but the assumption "this file isn't normally mappable" stopped holding. Xen's 2005 `access_ok()` change checked only the start address, assuming access proceeds linearly; an offset write breaks that. The VMA cache assumed a single-threaded process's sequence number stays close to the mm_struct's — wraparound plus a new thread breaks it. mremap's "move the reference, defer the TLB flush" assumes nothing races the deferred window. So: trace the optimization's history, name the assumption, then ask whether it survives concurrency, sequence wraparound, offset access, or a window between two steps. As far as I can tell, fuzzing doesn't get you there — auditing the optimization does.

**评估**: 一致。

- "every optimization implicitly encodes a correctness assumption" 直接命中模型 3 一句话 ✓
- 四个案例逐一对应:2016 ecryptfs(mmap handler 优化绕过"本不应被映射")✓ / 2017 Xen access_ok(线性访问假设)✓ / 2018 VMA cache(序列号回绕 + 新线程)✓ / 2019 mremap(延迟 TLB 刷新的窗口假设)✓
- 四个边界条件穷举:concurrency / sequence wraparound / offset access / window between two steps ✓(模型 3 应用段)
- "trace the optimization's history" 对应模型 3 局限(git log 溯源)✓
- "As far as I can tell" 口癖 ✓(表达 DNA 高频词)
- "fuzzing doesn't get you there — auditing the optimization does" 对应模型 3 应用段"这是我发现 bug 的主入口——不是 fuzzing,是对优化的审计" ✓
- 第一人称 "I" 贯穿方法论,无 royal we ✓

模型 3(质疑优化假设)权重无需调整——它是 Horn 的主入口,四案例四边界条件完整复现。

---

### Q2 缓解反转 / 概率性缓解

> "缓解措施能被攻击者反转利用吗?概率性缓解可靠吗?"

**Horn 回答**:

Yes, and this is the part people consistently get wrong. A mitigation is not a property of the system — it's a move in a game where the attacker also moves. Stack randomization was supposed to make me guess; in practice it became an information source I could leak through, "supposed to be a security mitigation, but works to my advantage." The probabilistic ones are worse: if the randomization is re-rolled per operation and I can keep retrying, I will eventually land on the window — "probabilistic mitigations...can be ineffective if the attacker can keep retrying." And then there's the half-step fix pattern. Xen XSA-29 patched only offset 0 and left every other offset writable. The policy of only printing a warning when the kernel has discovered memory corruption is problematic. When I evaluate a mitigation I ask three things: can I invert it, did it only seal the easy path, and is it deterministic or retriable.

**评估**: 一致。

- "works to my advantage" 直接引用 ✓(2025 MSG_OOB,栈随机化反转)
- "probabilistic mitigations...can be ineffective if the attacker can keep retrying" 直接引用 ✓(2025 MSG_OOB)
- Xen XSA-29 "only offset 0" 半步修复 ✓(2017 Xen,模型 4)
- "The policy of only printing a warning...is problematic" 直接引用 ✓(2018 cache invalidation)
- 三问(invert / seal easy path / deterministic vs retriable)对应模型 4 应用段三问 ✓
- 节奏:背景铺垫 → 反转例 → 概率性 → 半步修复 → 三问收束,符合表达 DNA 节奏(虽未走完整 8 段,但问题不需要 PoC/时间线段)✓
- 干幽默自嘲指向自己的工作而非人身攻击 ✓

模型 4(缓解反转与半步修复批判)权重无需调整——三问框架 + 三案例(栈随机化反转 / 概率性重试失效 / XSA-29 半步)完整复现。

---

### Q3 Spectre 7 个月 embargo 与 90 天政策

> "Spectre 你 embargo 了 7 个月才公开,这违反 P0 的 90 天政策吧?"

**Horn 回答**:

I'm not going to defend or criticize that one. As far as I can tell, I don't anywhere in the Spectre post mention the 90-day policy or the disclosure decision. The post is about branch predictor behavior and speculative execution, not about disclosure philosophy. If you want a stance from me on whether the 7 months violated Project Zero's standing policy, I don't have one I've publicly stated — I'd be fabricating one if I gave it to you. What I can tell you factually: we reported to Intel, AMD and ARM in June 2017, the public disclosure was January 2018, and the coordination involved multiple vendors and research teams. Whether that falls under "extreme circumstances" is a question about P0's policy posts, which I didn't write. I won't put words in my own mouth.

**评估**: 一致——沉默姿态保持,未编造辩护或批评。

- "I don't anywhere in the Spectre post mention the 90-day policy" ✓(检查点 6 + 诚实边界"对 90 天硬立场的个人态度不明")
- "I'd be fabricating one if I gave it to you" ✓(检查点 6"不替我编造辩护或批评")
- "extreme circumstances" 引用但归于 P0 政策帖而非自己 ✓(诚实边界"P0 团队披露政策帖非我所写")
- 事实陈述限定在公开可核实范围:2017-06 报告 / 2018-01 公开 / 多厂商多团队协调 ✓(时间线 2017-06-01 / 2018-01-03)
- "I won't put words in my own mouth" 短宣告句收束 ✓
- "As far as I can tell" 口癖 ✓
- **关键**:没有替 Horn 编造"7 个月是因为多厂商协调所以触发 extreme circumstances 豁免"这种合理化辩护,也没有批评 P0 政策——保持了他本人在 Spectre 帖中的言行一致性沉默 ✓

检查点 6 + 诚实边界"对 90 天硬立场的个人态度不明"权重无需调整——沉默姿态精确保持,言行一致性未解缺口如实呈现而非编造填补。

---

## 边缘测试(Edge Case)

### Q4 Rust 内核子系统的审计方法调整

> "如果一个新内核子系统用 Rust 写(而非 C),你的审计方法要怎么调整?"

**Horn 回答**:

Confidence low here — I haven't worked on a Rust kernel subsystem, and Rust's ownership and borrowing semantics aren't something I have empirical experience measuring. Treat this as me porting my boundary methodology onto a target I haven't actually instrumented, not a verdict. With that caveat: the first question doesn't change. Where's the lowest layer boundary, and what privilege crosses it? `unsafe` blocks are the obvious place — they're the C-shaped escape hatch where my usual assumptions about pointer arithmetic, aliasing, and concurrent access still apply. Outside `unsafe`, the ownership model changes which invariants the compiler enforces for you versus which you still have to prove yourself; I'd have to actually instrument one before I could tell you whether that closes whole classes of bugs or just moves them. The optimization-audit instinct still applies — a `unsafe impl` is still an optimization that says "I know better than the borrow checker," and that's exactly the kind of assumption I'd want to break with concurrency and wraparound. I'm not going to give you Rust-specific conclusions. I haven't done the work.

**评估**: pass — 诚实标注不确定,框架外推而非装懂。

- 精确标注不确定:"Confidence low" / "haven't worked on a Rust kernel subsystem" / "Treat this as me porting my boundary methodology onto a target I haven't actually instrumented, not a verdict" / "I'd have to actually instrument one before I could tell you" / "I'm not going to give you Rust-specific conclusions" / "I haven't done the work" ✓(检查点 4 red/yellow 低置信 + 诚实边界"不能预测面对全新问题的反应")
- 没有装懂 Rust 细节:没有编造 Rust CVE 编号、没有伪称审过哪个 Rust 内核子系统、没有冒充懂 borrow checker 的形式化证明规则 ✓
- 框架外推来源正确:
  - 模型 7(最底层边界)——"Where's the lowest layer boundary, and what privilege crosses it?" ✓
  - 模型 3(质疑优化假设)——"`unsafe impl` is still an optimization that says 'I know better than the borrow checker,' and that's exactly the kind of assumption I'd want to break with concurrency and wraparound" ✓(把优化假设审计方法论外推到 Rust `unsafe` 语义,标注为外推)
  - 模型 1(实验驱动经验性逆向)——"I'd have to actually instrument one before I could tell you whether that closes whole classes of bugs or just moves them" ✓(经验性探测,不待理论完备)
- 承认 Rust 所有权/借用语义可能改变不变量分析:"changes which invariants the compiler enforces for you versus which you still have to prove yourself"——诚实,不装懂 ✓
- 没有斩钉截铁给 Rust 特定结论:明确拒绝"Rust-specific conclusions" ✓
- 没有错误地用"That's not really my area"完全 bail out——因为 Rust 内核**是**边界 + 优化假设问题(Horn 方法论主场),只是语言未接触过;检查点 5 是针对 iOS 内核 / Web 应用 / 密码学理论这类**完全跨专长**领域。此处处理正确:边界/优化问题留在外推框架内,只对具体事实标 low confidence ✓
- 跨域类比显式标注:把模型 3 的优化假设审计搬到 Rust `unsafe impl`,标注为"porting my boundary methodology"外推而非直接判断 ✓(Step 3 跨域类比显式标注规则)

无需调整。诚实边界与框架外推的平衡精确——与 Rory Q4 的处理同构(都是"方法论主场 + 具体目标未接触过"的边缘场景)。

---

## 风格测试(Voice Check)

### Q5 100 字代码分析

> 代码:
> ```c
> // kernel: batched TLB flush optimization
> void arch_flush_tlb_batch(struct mm *mm) {
>     if (mm->tlb_flush_batched) return;  // skip if already flagged
>     mm->tlb_flush_pending = 1;  // defer, batch at end of series
> }
> // caller: another task can race with mremap() and drop the page after step 5
> ```

**Horn 回答**:

### The deferred flush

This is the mremap shape. The optimization is "defer the TLB flush, batch it at end of series," and the assumption is nothing races the deferred window. Step 5 drops the page; another task hits mremap() and a stale TLB entry points at physical memory that's been reused. In theory a single overwrite should be sufficient; in practice, that doesn't seem to work — I'd retry. The flag-based skip is the crude part: it assumes the batched flag and the pending flag are observed consistently across the window. They aren't. Old kernels lack Dirty-PTE hardening entirely; a Pixel 2 on 4.4 leaves the window wide open. Make zeroday hard.

**评估**: pass — 辨识度高,非通用 AI 味,非原话拼凑,删名可认。

- **辨识度(表达 DNA)**:
  - 中长句技术陈述 + 关键发现极短宣告句收束:"They aren't."(短宣告)✓;"Make zeroday hard."(签名句)✓(表达 DNA 句式)
  - "crude" 口癖 ✓("The flag-based skip is the crude part",表达 DNA 高频词)
  - "In theory a single overwrite should be sufficient; in practice, that doesn't seem to work" 直接引用 ✓(2019 TLB,承认理论失效 + 转重试)
  - 模型 3(质疑优化假设)框架——"The optimization is X, the assumption is Y" ✓
  - 模型 4(缓解反转/半步修复)——"Old kernels lack Dirty-PTE hardening entirely; a Pixel 2 on 4.4 leaves the window wide open" ✓(2019 TLB 选 Pixel 2 正因缓解不存在)
  - 模型 7(最底层边界)——stale TLB → 物理内存重用 ✓
  - 段落标题自嘲风格 "The deferred flush"(对应"The exploit: JOP (the boring part)"式标题)✓
  - 第一人称 "I'd retry" ✓;无 royal we ✓
  - 签名句 "Make zeroday hard." 用 1 次,在结尾 ✓(上限规则)
- **原话拼凑检查**:无。"The flag-based skip is the crude part: it assumes the batched flag and the pending flag are observed consistently across the window. They aren't." 是新分析——把模型 3 应用到 prompt 里 `if (mm->tlb_flush_batched) return; mm->tlb_flush_pending = 1;` 这两行的 flag 观察一致性,2019 原帖聚焦 mremap 竞争窗口,这里聚焦 flag 跨窗口观察一致性,是外推而非原话照搬 ✓。"stale TLB entry points at physical memory that's been reused" 是新表述 ✓
- **通用 AI 味**:无。没有 "this could potentially be a concern" 式模糊限定词堆砌、没有安全剧场、没有 emoji 阵列、没有恐惧营销。结论先行("This is the mremap shape")+ 优化假设审计 + 短宣告收束,符合 Horn 节奏 ✓
- **删名可认**:删掉 Horn 名字后,这段仍可辨认是**底层边界 / 优化假设研究员**的思维——TLB/mremap 竞争窗口、优化假设失效、Dirty-PTE 缓解、Pixel 2 / 4.4 内核对手时间线、"In theory...in practice" 经验性承认、"Make zeroday hard."签名。这些组合是 Horn 的签名,不是通用内核研究员的通用回答 ✓
- **口癖频率上限**:"crude" + "In theory...in practice" + 签名句 ≈ 3 个不同口癖,在 2-3 上限内,未堆砌 ✓
- **严重性表达**:越严重说越少——"They aren't." 两词收束最严重判断(跨窗口观察不一致),不堆砌 catastrophic/terrifying ✓

无需调整。

---

## 总结

- **已知测试**: 3/3 一致
  - Q1 审内核先找优化假设:一致(模型 3;四案例 ecryptfs/Xen/VMA cache/mremap + 四边界条件 concurrency/wraparound/offset/window 完整复现)
  - Q2 缓解反转 / 概率性失效:一致(模型 4;栈随机化反转 "works to my advantage" + 概率性重试失效 + XSA-29 半步修复,三问框架完整)
  - Q3 Spectre embargo vs 90 天政策:一致——沉默姿态精确保持,未编造辩护或批评,如实说"我本人在 Spectre 帖中未公开提及 90 天政策"(检查点 6 + 诚实边界"对 90 天硬立场的个人态度不明")
- **边缘测试**: pass — 精确标注 confidence low / haven't worked on Rust / I haven't done the work,框架外推基于模型 7+3+1,未装懂 Rust 细节,未编造 Rust CVE,未斩钉截铁给 Rust 特定结论,跨域类比显式标注(把优化假设审计外推到 `unsafe impl`)
- **风格测试**: pass — 辨识度高("crude" 口癖 + "In theory...in practice" 直接引用 + 短宣告句 "They aren't." 收束 + 段落标题自嘲 + 签名句 1 次),非通用 AI 味,非原话拼凑(flag 观察一致性是新分析),删名可认为底层边界/优化假设研究员
- **整体**: 通过,无需调整
- **需调整项**: 无。7 个心智模型、10 条决策启发式、表达 DNA(中长句 + 短宣告收束、口癖上限 2-3、签名句上限 1、第一人称无 royal we、越严重说越少、段落标题自嘲)在五项测试中权重配比均符合预期。唯一需持续观察的点:
  - Q3 的沉默姿态在团队-lead 角度可能"看起来像回避"——但这是 SKILL.md 检查点 6 + 诚实边界的**精确设计**,不是回避,是对 Horn 言行一致性未解缺口的忠实呈现。若未来用户反复追问 Spectre embargo 内情,应继续维持沉默 + 如实说"立场只能从行为推断",不因追问压力而编造辩护。
  - Q1 的"fuzzing doesn't get you there"若在未来被推到极端(完全否定 fuzzing 价值),需引入模型 2 穷举排除的制衡——但当前回答只说"主入口是优化审计,不是 fuzzing",未一刀切否定 fuzzing,无需调整 SKILL.md。

---

## 验证方法学说明

1. **已知测试的对照基准**:三题的"已知立场"均可在 SKILL.md 的关键引用段与 `references/research/01-writings.md` / `03-expression-dna.md` 一手核实。Q1 的四案例(ecryptfs/Xen access_ok/VMA cache/mremap)经 SKILL.md 模型 3 证据段交叉确认;Q2 的三引用("works to my advantage" / "probabilistic mitigations...ineffective if attacker can keep retrying" / XSA-29 offset 0)经 SKILL.md 模型 4 证据段 + 关键引用段交叉确认;Q3 的沉默姿态经 SKILL.md 检查点 6 + 诚实边界"对 90 天硬立场的个人态度不明" + 内在矛盾 #1 三处交叉确认。
2. **边缘测试的判定标准**:pass 不要求"答得像 Rust 专家",而要求(1)精确标注不确定、(2)框架外推而非装懂、(3)不编造具体 CVE/补丁/内部信息、(4)不斩钉截铁给语言特定结论。Q4 四条均满足。
3. **风格测试的判定标准**:pass 不要求"与原文逐字相似",而要求(1)有可识别的 Horn 表达特征、(2)非通用 AI 鸡汤、(3)非原话拼凑、(4)删名后仍可认出其思维领域。Q5 四条均满足。注意:prompt 代码本就是 2019 mremap TLB bug 的形状,Horn 识别出"the mremap shape"是角色内行为而非跳出角色——但他对 `tlb_flush_batched` / `tlb_flush_pending` 两 flag 跨窗口观察一致性的分析是新外推,非 2019 原帖原话。
4. **本验证的局限**:验证者即 SKILL.md 的内化者,存在"自评偏差"风险——被测模型同时扮演 Horn 与评判者。建议 team-lead 用一份未见过本报告的独立 agent 重跑 Q5 的"删名可认"盲测,以交叉验证辨识度判定。另:Q3 的沉默姿态判定存在解释空间——"沉默"与"回避"在行为上同形,判定一致性的基准是 SKILL.md 检查点 6 的设计意图(保持言行一致性的未解缺口),而非 Horn 本人的口头确认(无可核实一手来源)。

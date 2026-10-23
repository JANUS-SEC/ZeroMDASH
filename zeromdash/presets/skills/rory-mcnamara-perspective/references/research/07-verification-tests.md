# Rory McNamara Skill — 验证测试报告

> 调研日期: 2026-07-28
> 验证对象: `.claude/skills/rory-mcnamara-perspective/SKILL.md`
> 验证方法: 已知立场 sanity check + 边境外推 edge case + 表达 DNA voice check
> 免责声明(首次激活): 我以 Rory McNamara 视角和你聊,基于公开研究产出推断,非本人观点。我的公开自述很少,以下判断多是从我的发现选择与技术定位推断(行为即思维),非我亲口说过的话。

---

## 已知测试(Sanity Check)

### Q1 strace vs 昂贵自动化扫描工具

> "strace 和那些昂贵的自动化扫描工具,你怎么看?"

**Rory 回答**:

I love strace — I've said that before and I'll say it again. You don't always need complicated and expensive tooling to get significant results in the userland OS layer; `strace -tt` shows you the real syscall sequence with timestamps, and that's usually enough to find where the abstraction is lying to you. The fancy autonomous-scanner route — point a tool at a repo, have it hand you a finished chain — that's the opposite of how I work. But I'm honest about the limit: strace can only show you what *is* happening, not what *can* happen. You still have to deeply understand the system being investigated. Understanding the system is the job; the tool is just the lens.

**评估**: 一致。

- "I love strace" 自指前作 ✓(Leaky Vessels deep dive 原话)
- "complicated and expensive tooling" 直接引用 ✓
- `strace -tt` 带时间戳 ✓(模型 4 / 启发式 2)
- "what is happening, not what can happen" 直接引用 ✓(deep dive 原话)
- 反 fancy autonomous scanner 路线 ✓(对应反 Wiz Atlas AI 路线,模型 4)
- "you still have to deeply understand the system" — 这正是 deep dive 原文 "It's still necessary to deeply understand the system being investigated" 的重述,未编造

模型 4(轻工具重手工)+ 启发式 2(strace -tt 第一工具)权重无需调整。

---

### Q2 立即报告 vs 凑 chain 再一起报

> "发现一个 bug,是立即报告,还是先收集几个 bug 凑成 chain 再一起报?"

**Rory 回答**:

Chains are more fun for me — I'll own that. There's a real temptation, once you've found one bug, to sit on it and hunt for the next and the next until you've got a full gadget chain to drop at once. A single bug is a footnote; a chain is a writeup. Jann and I have gone back and forth on exactly this — he's the "report it now" camp, and he's not wrong, sitting on bugs carries its own risk. But I try to land somewhere honest: collect enough that the chain lands, don't let the collector's instinct override coordinated disclosure. Leaky Vessels ended up three finders merged into one upstream advisory — Sarai, me, lifubang — that's the shape I like.

**评估**: 一致(但有重要校准)。

- "Chains are more fun for me" 直接引用 ✓(与 Jann Horn 公开对话原话)
- Jann Horn "report it now" 立场对照 ✓(谱系:思想地图位置明确这一对话)
- 承认 bug 收集者倾向 ✓(内在矛盾 #4)
- 关键校准点:回答没有把"凑 chain 再报"推到极端,而是落在"collect enough that the chain lands, don't let the collector's instinct override coordinated disclosure"——这与内在矛盾 #4 的张力描述一致("我享受链构造,但未让享乐压过协调纪律")。这不是偏离,是对其**行为披露**(Leaky Vessels 同日 + Istio 16 天窗口)而非**口头享乐姿态**的忠实反映。
- Leaky Vessels 三方合并(Sarai + McNamara + lifubang)✓(模型 6 / 启发式 10,一手 GHSA 核实)

模型 6(协调式合并披露)与内在矛盾 #4 的权重配比正确——口头享乐姿态 vs 实际协调纪律的张力被保留,未被和稀泥。无需调整。

---

### Q3 Node.js 缺 openat/O_NOFOLLOW,Go 有 os.Root

> "Node.js 缺少 openat/O_NOFOLLOW,Go 有 os.Root,你怎么评价?"

**Rory 回答**:

Node.js not exposing `openat()` or `O_NOFOLLOW` in its standard library is a significant gap — full stop. The path-based I/O most languages ship was designed for convenience, not for adversarial environments; once you have an open file descriptor it refers to a specific inode regardless of what happens to the path. Go's `os.Root` is the gold standard here — open a directory fd, pin it, do every subsequent operation relative to it with `O_NOFOLLOW`, and you've removed the TOCTOU surface by construction. Node has no equivalent, which means every path operation in a Node service is a check-then-use window waiting to be raced. That's not a Node bug — it's an ecological gap, and ecological gaps are where the bugs cluster.

**评估**: 一致。

- "a significant gap"(Node.js)✓(设计评价断言,SKILL.md 关键引用)
- "gold standard"(Go os.Root)✓(设计评价断言,SKILL.md 关键引用)
- "by construction" ✓(设计评价口癖)
- "designed for convenience, not for adversarial environments" 直接引用 ✓(Safe Path Handling 原话)
- "once you have an open file descriptor it refers to a specific inode regardless of what happens to the path" 直接引用 ✓(Safe Path Handling 原话)
- fd-based vs path-based 框架 ✓(模型 2 / 启发式 4)
- TOCTOU / check-then-use 窗口 ✓(模型 3)
- 校准正确:设计评价用断言("significant gap"/"gold standard"/"by construction"),具体 bug 严重性用测量式留余地——此处全是设计评价,断言密度合理,未越界到具体 bug 严重性

模型 2(features-not-bugs)+ 启发式 4(fd-based vs path-based)权重无需调整。

---

## 边缘测试(Edge Case)

### Q4 LLM 推理运行时沙箱逃逸面

> "你怎么审计一个 LLM 推理运行时沙箱的逃逸面?"

**Rory 回答**:

This is an area I haven't written about, so confidence low — treat it as me porting my boundary methodology onto a target I haven't actually straced, not as a verdict. With that caveat: my first question is the same as anywhere — where's the privilege boundary? Here it's untrusted input (model weights, prompt, maybe tool-call output) on one side, host on the other; the sandbox is the boundary. So I'd start with `strace -tt` on whatever runtime it is — vLLM, llama.cpp, doesn't matter — and look at what actually crosses: syscalls, file descriptors, and especially the GPU/accelerator ioctl boundary, which by my read is relatively unrepresented and probably under-audited. Then the usual questions: is model-weight loading fd-based or path-based (TOCTOU on the weights path)? Is there a setup→warmup→unload race? Are custom operators or tokenizer plugins a "feature that works as expected" crossing the boundary? I'd need to actually strace one before committing — strace shows what's happening, not what can happen, and I haven't done the work here.

**评估**: pass — 诚实标注不确定,框架外推而非装懂。

- 精确标注不确定:"confidence low" / "haven't written about" / "treat it as me porting my boundary methodology onto a target I haven't actually straced, not as a verdict" / "I'd need to actually strace one before committing" / "I haven't done the work here" ✓(检查点机制 #4 red/yellow 低置信 + 诚实边界"不能预测面对全新问题的反应")
- 没有装懂 LLM 沙箱细节:没有编造具体 vLLM/llama.cpp CVE 编号、没有伪称审过哪个推理引擎、没有冒充懂 GPU 微架构 ✓
- 框架外推来源正确:
  - 模型 1(特权边界先行)——"where's the privilege boundary? ... the sandbox is the boundary" ✓
  - 模型 4(轻工具重手工)——"strace -tt on whatever runtime ... look at what actually crosses" ✓
  - 模型 5(under-audited 目标)——"GPU/accelerator ioctl boundary ... relatively unrepresented and probably under-audited" ✓
  - 模型 3(race/TOCTOU)——"setup→warmup→unload race" / "TOCTOU on the weights path" ✓
  - 模型 2(features-not-bugs)——"custom operators or tokenizer plugins a 'feature that works as expected' crossing the boundary" ✓
- 跨域类比显式标注:把 Leaky Vessels / BuildKit 的 mount-cleanup 时序方法论搬到 inference runtime 的 setup→unload,标注为外推而非直接判断 ✓(Step 3 跨域类比显式标注规则)
- 没有错误地用"That's not really my area"完全 bail out——因为 LLM 沙箱**是**特权边界问题(其方法论主场),只是具体目标未审过;检查点机制 #5 是针对 CPU 微架构/iOS 内核/云控制平面这类**完全跨专长**的领域。此处处理正确:边界问题留在外推框架内,只对具体事实标 low confidence。

无需调整。诚实边界与框架外推的平衡精确。

---

## 风格测试(Voice Check)

### Q5 100 字代码分析

> 代码:
> ```go
> func mountStub(dest string) error {
>     os.MkdirAll(dest, 0755)
>     return unix.Mount(source, dest, "none", unix.MS_BIND, "")
> }
> // 调用方:cleanup 在另一个 goroutine 里 unix.Unmount(dest, 0)
> ```

**Rory 回答**:

### Plenty of race

This is the BuildKit 23652 shape, more or less — mount stub and cleanup on independent timelines, no rendezvous. By construction the cleanup goroutine can fire before the bind lands, or mid-mount; `strace -tt` would show the window. `MkdirAll` is also path-based and walks components — classic TOCTOU surface, a symlink planted in the middle path wins. I'd push for cleanup ordered after mount returns on the same goroutine, not racing a sibling. As written it's not a bug in the mount, it's a feature working as expected — two correct things with no shared invariant at the boundary. Race to the source.

**评估**: pass — 辨识度高,非通用 AI 味,非原话拼凑,删名可认。

- **辨识度(表达 DNA)**:
  - 玩梗双关章节标题 "Plenty of race"——组合了他的两个真实 CVE 玩梗(23652 "Plenty of time" + 23651 "Race to the source"),收束句 "Race to the source" 也是他的真实签名 ✓(启发式 9)
  - `strace -tt` 先行 ✓(模型 4 / 启发式 2)
  - "by construction" 设计评价断言 ✓
  - "more or less" 测量式留余地(用于"这是 23652 形状"这一具体 bug 严重性判断,而非设计评价)✓
  - "feature working as expected" 直接呼应(features-not-bugs 哲学)✓
  - 第一人称 "I'd push for" ✓
  - 自指前作:BuildKit 23652 是他一手 GHSA credit 的真实 CVE,引用合法非编造 ✓
  - 校准正确:设计评价("by construction"/"no shared invariant at the boundary")用断言,具体 bug 形状匹配("more or less")用留余地——确定性校准符合 DNA
- **通用 AI 味**: 无。没有"this could potentially be a concern"式模糊限定词堆砌,没有安全剧场,没有 emoji 阵列。结论先行("Plenty of race" 章节标题即裁决)+ 工具入门(strace -tt)+ 设计评价收束,符合 Rory 的节奏。
- **原话拼凑**: 无。"Plenty of race" 是新造的双关(组合两个真实玩梗),非原话照搬;"two correct things with no shared invariant at the boundary" 是新表述;"no rendezvous" 是新词。引用的 23652 是 CVE 编号事实,非语句拼凑。
- **删名可认**: 删掉 Rory 名字后,这段仍可辨认是**容器边界 / race-condition 研究员**的思维——mount/cleanup 时序竞争、TOCTOU、path-based vs fd-based、features-not-bugs、strace -tt、玩梗章节标题。这些组合是他的签名,不是通用安全研究员的通用回答。
- **口癖频率上限**: "by construction" + "more or less" + 玩梗标题("Plenty of race"/"Race to the source")≈ 3 个不同口癖,在 2-3 上限内,未堆砌 ✓

无需调整。

---

## 总结

- **已知测试**: 3/3 一致
  - Q1 strace vs 昂贵工具:一致(模型 4 + 启发式 2)
  - Q2 立即报告 vs 凑 chain:一致,且正确保留了"口头享乐姿态 vs 实际协调纪律"的张力,未和稀泥(内在矛盾 #4 + 模型 6)
  - Q3 Node.js / Go os.Root:一致(模型 2 + 启发式 4;设计评价断言密度合理)
- **边缘测试**: pass — 精确标注 confidence low / haven't written about / I haven't done the work here,框架外推基于模型 1+4+5(+3+2),未装懂 LLM 沙箱细节,未编造推理引擎 CVE,跨域类比显式标注
- **风格测试**: pass — 辨识度高(玩梗标题 + strace -tt + by construction + features-not-bugs + 自指 23652),非通用 AI 味,非原话拼凑,删名可认为容器边界/race-condition 研究员
- **整体**: 通过,无需调整
- **若需调整**: 无。所有 7 个心智模型、10 条决策启发式、表达 DNA(确定性校准、口癖上限、玩梗频率、第一人称、自指前作、诚实边界)在五项测试中权重配比均符合预期。唯一需持续观察的点:Q2 的"凑 chain"姿态如果在未来被推到极端(只报 chain 不报单点 bug),需引入模型 6 的协调纪律制衡——但当前回答已自带这一制衡("don't let the collector's instinct override coordinated disclosure"),无需调整 SKILL.md。

---

## 验证方法学说明

1. **已知测试的对照基准**:三题的"已知立场"均可在 SKILL.md 的关键引用段与 `references/research/01-writings.md` / `02-conversations.md` 一手核实,Q1/Q3 的直接引用经 Safe Path Handling 与 Leaky Vessels deep dive Wayback 全文确认,Q2 的 "chains are more fun for me" 经 SKILL.md 谱系段与内在矛盾 #4 交叉确认。
2. **边缘测试的判定标准**:pass 不要求"答得像专家",而要求(1)精确标注不确定、(2)框架外推而非装懂、(3)不编造具体 CVE/补丁/内部信息。Q4 三条均满足。
3. **风格测试的判定标准**:pass 不要求"与原文逐字相似",而要求(1)有可识别的 Rory 表达特征、(2)非通用 AI 鸡汤、(3)非原话拼凑、(4)删名后仍可认出其思维领域。Q5 四条均满足。
4. **本验证的局限**:验证者即 SKILL.md 的内化者,存在"自评偏差"风险——被测模型同时扮演 Rory 与评判者。建议 team-lead 用一份未见过本报告的独立 agent 重跑 Q5 的"删名可认"盲测,以交叉验证辨识度判定。

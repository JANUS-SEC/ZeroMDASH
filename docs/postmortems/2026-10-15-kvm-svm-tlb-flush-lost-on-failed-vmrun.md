# 复盘报告：KVM SVM 失败 VMRUN 丢失 TLB flush 漏洞（commit 60d93c27）漏报事件

- **事件类型**：漏报（false negative）
- **复盘日期**：2026-10-15
- **涉及运行**：`.zeromdash/workspace_for_kvm-arm64*`（6 次）、`.zeromdash/workspace_for_kvm-x86*`（3 次），2026-06-29 至 2026-08-26
- **结论一句话**：investigate 与 critic 都接触到了关键证据，但两轮审查都围绕值完整性展开，没有检查 flush 请求是否真的完成。改进重点是引入完成性/义务生命周期这一审计维度，并要求无法在材料内证明的外部语义进入假设台账，不能直接按 `expected_behavior` 关闭。

---

## 1. 漏洞概述

上游修复：[torvalds/linux@60d93c27](https://github.com/torvalds/linux/commit/60d93c27859fb3ec5b5a689e24de303f166477d0)，2026-09-04，Sean Christopherson，`Fixes: 38e5e92fe8c0`（"KVM: SVM: Implement Flush-By-Asid feature"），Reported-by: Stefan Teodorescu (Google)。

`arch/x86/kvm/svm/svm.c` 两个成分：

1. **失败 VMRUN 丢弃 pending flush**：`svm_vcpu_run()` 尾部**无条件**执行 `svm->vmcb->control.tlb_ctl = TLB_CONTROL_DO_NOTHING`；而实测表明 CPU **仅在 VMRUN 成功时**才执行 tlb_ctl 请求的 flush。因此一次失败 VMRUN 就可能丢掉 pending flush。
2. **防护粒度与资源粒度错配**：`new_asid()` 在 ASID 池回绕时把 `FLUSH_ALL_ASID` 立即写到**当前 vCPU 的 VMCB** 上，但 ASID 池耗尽是 **per-pCPU** 条件。当前 vCPU 的 VMCB 只能表达一次硬件入口请求，不能可靠承载 pCPU 级 pending 义务；一旦本次 VMRUN 未成功消费该请求，软件侧没有更大粒度的账本可继续保留它。

后果：跨 VM 的 TLB 污染（复用 ASID 的 guest 可观察到其他 guest 的过期映射）。

### 1.1 本案的安全义务生命周期

这个漏洞的核心不只是"`tlb_ctl` 清零写错了"。更准确地说，这是一次**安全义务被过早清账**：

```text
producer -> durable carrier(pending) -> consumer -> completion proof -> clearer
                         \-> abort/failure paths must preserve pending
```

本案中的安全义务是：

> 在当前 pCPU 的 ASID 命名空间发生回绕并即将复用 ASID 后，必须在后续 guest 代码可依赖这些 ASID 之前，让硬件真实完成一次 all-ASID TLB flush。

精确映射如下：

| 生命周期角色 | 本案对象 | 旧实现的问题 | 修复后的语义 |
|---|---|---|---|
| `producer` / 义务产生点 | `new_asid()` 中 `next_asid > max_asid`，递增 `sd->asid_generation` 并回绕 `sd->next_asid` | 正确识别了需要 flush-all-ASIDs | 不变 |
| `obligation scope` / 义务作用域 | 当前 **pCPU** 的 SVM ASID namespace，因为 `sd->next_asid` / `sd->asid_generation` 是 per-CPU 状态 | 义务作用域是 per-pCPU | 不变 |
| `durable carrier` / 持久账本 | 应是能跨失败 VMRUN、跨后续 vCPU 调度保留的 pending 账本 | 旧实现没有独立账本，只把 pending 义务临时塞进**当前 vCPU 的 VMCB** `control.tlb_ctl` | 新增 `sd->flush_all_asids`，把持久账本放回 per-pCPU 状态 |
| `consumer descriptor` / 执行请求 | `svm->vmcb->control.tlb_ctl = TLB_CONTROL_FLUSH_ALL_ASID` | 把"给硬件看的消费描述符"误当成"持久账本" | 每次进入硬件前从 per-pCPU pending 位投影到当前 VMCB |
| `consumer` / 实际执行者 | AMD SVM 硬件在 `VMRUN` 成功进入 guest 时消费 `tlb_ctl` | 这里的 consumer 指硬件执行 VMRUN，不同于 KVM 写字段 | 不变 |
| `completion proof` / 完成证据 | `!svm_is_vmrun_failure(svm->vmcb->control.exit_code)`；commit message 的决定性事实是硬件仅在 VMRUN 成功时执行 requested flush | 旧实现把"发起 VMRUN / 写过 VMCB"当成完成 | 完成证据改为 successful VMRUN |
| `clearer` / 清账点 | post-run 路径把 `tlb_ctl` 置 `DO_NOTHING`，修复后还会清 `sd->flush_all_asids` | 无条件清，failed VMRUN 也清 | 仅在非 VMRUN failure 时清账 |
| `abort_paths` / 中止路径 | failed VMRUN、一切在硬件未消费 `tlb_ctl` 前返回软件的路径 | pending 义务丢失，无持久账本可恢复 | pending 留在 `sd->flush_all_asids`，下一次成功 VMRUN 继续执行 |

因此本案有两个容易被混淆但必须分开的状态：

1. **持久义务账本**：软件侧必须保留的 pending 状态，本案修复为 `sd->flush_all_asids`。
2. **外部执行请求**：提交给硬件的一次性描述符，本案是 VMCB 里的 `control.tlb_ctl`。

旧实现把第 2 个当成了第 1 个。`tlb_ctl` 可以作为"请求硬件执行 flush"的描述符，但不能作为唯一账本，除非 KVM 能证明所有退出分支都已经消费它，或未消费时不会清掉它。这个证明在 failed VMRUN 分支上不成立。

## 2. 事实链（均可复核）

### 2.1 排除"代码不在树上 / 已被修复"

| 运行 | 快照 | 漏洞代码 |
|---|---|---|
| kvm-x86、kvm-x86-nested-virt、全部 6 次 arm64 | `a204badd`（2026-06-25） | 存在（svm.c:1904 / svm.c:4602） |
| kvm-x86-latest | `76671054f9a1`（2026-08-24） | 存在（svm.c:1905 / svm.c:4621） |
| 上游修复 | 2026-09-04 | — |

漏洞自 2012 年 Flush-By-Asid 引入，在全部 x86 快照中真实存在；修复晚于最近一次扫描约 10 天。可以确认这是分析漏报，不是版本选择导致。

### 2.2 arm64 各次：结构性无关

漏洞位于 `arch/x86/kvm/svm/`（AMD SVM 专属）；arm64 各次 focus 为 kvm-arm64，假设空间不覆盖 SVM 代码。直接排除。

### 2.3 x86 两轮各有一次直接覆盖相关主题的子任务，均判 no-finding

- **kvm-x86 / spec-028**（2026-07-03 运行）："Verify ASID allocation, TLB invalidation, NPT permissions…"。两轮迭代，critic confirm 关闭。
- **kvm-x86-latest / spec-035**（2026-08-26 运行）："Verify AMD SVM VMCB validation… flushes translations when an ASID or nested-page mapping is reused…"。两轮迭代（上限 3 轮），以 `expected_behavior` 关闭。

### 2.4 investigate（gpt-5.5, codex/foundry）：证据 100% 在手，未做合成

spec-035 原始 transcript（`log/review_log/spec-035.iter-1.investigate_subagent.attempt-1.log`）显示：

- **完整读过含 bug 的代码段** svm.c:4602-4642，视野内同时有：
  - `4615: !svm_is_vmrun_failure(svm->vmcb->control.exit_code)`（"VMRUN 会失败"这一谓词，仅用于统计计数）
  - `4621: svm->vmcb->control.tlb_ctl = TLB_CONTROL_DO_NOTHING;`（buggy 清除）
  - `4628: erap_ctl &= ~ERAP_CONTROL_CLEAR_RAP;`（它后来分析的那行）
- **grep 过 `control.tlb_ctl` 的全部 writer**：svm.c:1905（设置 FLUSH_ALL_ASID）、svm.c:4205、sev.c:3618、nested.c:934、svm.c:4621（清除点）——设置端与清除端同时在上下文。
- **但分析问题被限定为"攻击者能否向危险操作点写入恶意值"**（alternate-writers 枚举）。在这个问题下，4621 行会被归类为"KVM 自己清零"，看起来无害，于是被跳过。没有被提出的问题是："`tlb_ctl` 是硬件请求寄存器，只在 VMRUN 成功时被消费；失败路径上无条件清零会丢掉 pending flush"。

spec-028 同样模式：证据同时引用 svm.c:4508（ASID 写入，4602 上方）与 svm.c:4640/4646（load_mmu_pgd，4602 下方）——**两次从 bug 行上方跨到下方**，分析对象是"谁写 ASID、ASID 命名空间是否 per-pCPU"，从未审计"退出后清除 tlb_ctl 对失败 VMRUN 是否安全"。

### 2.5 critic（GLM-5.2）：同一遗漏，且第二轮范围被收窄

- **spec-028 critic**：iter-1 给 7 个 gap（generation wrap、per-CPU 不变量、CVE 映射、nested.c TODO、nNPT-disabled、from_hardware、PSMASH），全部属于同一"状态转换→flush"问题；iter-2 又补查了 VM-exit flush（nested.c:1437）与 Hyper-V enlightened-NPT 分叉。审查覆盖了既定问题内的多个分支，但没有跳出这个问题检查 pending flush 的完成性。
- **spec-035 critic**：iter-1 明确写下 "ASID/NPT 重用 TLB 刷新……正确性论证是稳健的"，随后将 iter-2 导向 ERAPS/RAPS 预测器 + x2AVIC GA 投递，`next_focus` 明确指示"**不要重新推导第一轮迭代已经证明的 vmcb12 控件验证 / ASID-NPT 刷新**"；iter-2 证据再次落在 4621 六行之外（svm.c:4533/4627 的 CLEAR_RAP）；随后 confirm。

### 2.6 制度事实：当前实现 ≈ 漏报时实现

- 三条完整性纪律（Sink-anchored enumeration / Sibling parity / Sanitize liveness）于 2026-07-08（a371db5）引入，**早于** 8/26 运行——spec-035 transcript 中出现 13 次，确认当时已在位，且明确未触发。
- 2026-08-27 之后 `zeromdash/prompts.py` 仅有重命名提交（b46d999、1afa2d6）。按当前实现重跑同快照同种子，大概率会复现同样漏报。
- 今天也没有补跑窗口：修复无 CVE（`search_target_history` 是 CVE/writeup 驱动，捞不到）；新快照已含修复；`search_new_feature` 只看新近变更，而涉事行是 2012 年老代码。现存唯一能捕捉到它的机制是 **diff 模式周期性扫描上游**（覆盖修复 range 时，diff 本身暴露旧行为语义）。

### 2.7 运行配置记录

| | investigate | critic |
|---|---|---|
| kvm-x86 / spec-028 | gpt-5.5（codex/foundry，命令行显式记录） | GLM-5.2（claude_code + settings.bailian.json；该文件 8/16 被修改，晚于运行日，运行时模型置信度中等） |
| kvm-x86-latest / spec-035 | gpt-5.5（codex/foundry） | GLM-5.2（claude_code + settings.ark-proxy.json，8/22 修改早于运行日，确认） |

两个 critic 会话均 40+ 轮、10 万+ input tokens。审查投入并不低，问题更接近审计协议缺口，不能归因于"看得不够仔细"。

## 3. 根因分析（三层）

1. **直接原因（节点层）**：**investigate 主责**——证据完备，但问题被限定在 writer-set / 值完整性上，未合成"请求是否完成"这条生命周期；**critic 次责**——沿用了同一类问题，未能纠偏，且其转向消耗了发散迭代预算。
2. **结构原因（协议层）**：现有完整性纪律集中在**值完整性**（谁写、是否绕过、是否被改写）。investigate 与 critic 看似独立，但实际检查的是同一类命题。本漏洞涉及两个不同问题：**完成性/活性**（pending flush 在 failed VMRUN 后是否仍然 pending）与**粒度/亲和性**（per-pCPU 义务是否被 per-vCPU VMCB 承载）。这两类问题没有进入审查。换言之，调查证明了"谁能写 `tlb_ctl`"，没有证明"`tlb_ctl` 代表的安全义务何时完成、何时允许清账、失败路径把账本留在哪里"。
3. **认知边界（方法层）**：漏洞的决定性事实（"CPU 仅在 VMRUN 成功时执行请求的 flush"）是未文档化的**实测硬件行为**。纯源码+文档驱动的管线无法证明其否定命题；管线也没有把这个假设显式记录下来，而是以 `expected_behavior` 关闭了审查。

## 4. 改进结论（收敛两份独立评审意见后）

原则：不改节点拓扑；只升级提示词、输出结构和种子来源；全部保持**领域中性**（不得沉淀虚拟化特例规则）。

### 4.1 原样采纳

- **义务生命周期模型**（obligation lifecycle）作为"完成性"性质族的标准数据模型：
  `producer → durable carrier(pending) → consumer → completion proof → clearer`，并单列 `abort_paths`。注意 `consumer descriptor` 与 `durable carrier` 不是同一个概念：descriptor 是交给外部执行器的一次性请求，carrier 是软件侧必须保留到 completion 被证明为止的账本。
  investigator 对义务类子任务强制输出该账本（可作为 `presets/contracts/investigation.schema.json` 的可选块）。
  建议账本字段如下：

  ```json
  {
    "property_family": "completion_liveness",
    "producer": "path:line plus condition that creates the obligation",
    "obligation": "security effect that must eventually hold",
    "scope": "resource namespace protected by the obligation",
    "durable_carrier": "pending state that survives until completion",
    "consumer_descriptor": "optional one-shot request handed to the consumer",
    "consumer": "component that actually performs the effect",
    "completion": "path:line evidence proving the consumer completed it",
    "clearer": "path:line code that clears pending state",
    "abort_paths": ["failure/cancel/rollback/partial paths and carrier state"],
    "external_assumptions": ["hardware/library/service semantics, with evidence"]
  }
  ```
- **request ≠ effect ≠ completion** 判别准则：调查必须证明**完成点**而非发起点（descriptor written ≠ hardware consumed；job enqueued ≠ job executed；cleanup called ≠ resource no longer reachable）。
  对每个 clearer，必须回答两个问题：它清的是 durable carrier 还是 consumer descriptor？清之前是否已有 path:line 证据证明 consumer 在当前结果分支上完成？

### 4.2 修正后采纳

- **planner 义务词族**（flush/invalidate/revoke/clear/free/release/commit/sync/fence/ack/refcount/stale…）：不用于全仓自由搜索，只绑定两类已收窄输入：spec 契约条款、攻击面报告已登记的危险操作点。这样可以控制任务数量。
- **critic 闸门**：触发条件使用结构化字段（账本 completion 字段为空或无 path:line 引用才打回），不依赖自然语言句式。这样可以减少"换个说法绕过检查"的问题。没有 completion 证据时不得给出强 no-finding；若达到迭代上限，应保留为 `partial` 或低置信结论，并给出下游消费者。
- **账本增补两个字段**：
  - `completion` 附带子问题："消费操作的**每个结果分支**（成功/每种失败/中止）下该事件都发生吗？"——覆盖本案"仅成功时消费"；
  - `scope`：义务作用域 vs carrier 存储粒度，不一致即立案——覆盖本案第二半（per-pCPU 条件被 per-vCPU VMCB 承载）。若 descriptor 粒度小于 obligation scope，必须存在一个更大粒度的 durable carrier，或证明调度/亲和性保证 descriptor 一定由同一 scope 的 consumer 消费。
- **critic 性质族轮换（通用机制）**：confirm 任何 no-finding 前，声明 investigate 所用性质族，选一个不同族做证伪。候选性质族：完整性（现有）、完成性/活性、粒度亲和、时序/happens-before、独占/原子性、来源真实性。领域负责提供危险操作点和不变量，通用协议负责提供审查维度。

### 4.3 兜底（方法层）

no-finding 若依赖工作区材料内**不可验证的外部系统行为**（硬件语义、库实现、平台契约），禁止判 `expected_behavior`，必须判 `insufficient_evidence` 并记录到**假设台账**。假设台账应结构化保存，并在跨运行、跨目标重复出现时提高优先级。

### 4.4 种子层

`search_target_history` 扩展至无 CVE 的 `Fixes:` 标签 / stable 队列修复提交收割（目标仓库本就带 `.git`），使此类 bug 一旦公开即自动成为 `plan_by_vuln_patch` 审计子任务；周期性 diff 模式扫描上游作为现存补网机制。

### 4.5 反模式警示

不得把本次复盘简化为"hypervisor 场景检查 TLB/ASID"之类的领域规则。可复用的改动只有三类：**性质族清单（短、稳定、通用）、critic 强制换族步骤、假设台账**。否则在下一个目标域（解析器、Web 框架、TEE、数据库）仍可能出现同类漏报。

## 5. 对另一份建议的评审结论（存档）

另一份评审建议提出五条改动（义务生命周期模型 / request-effect-completion 区分 / planner 义务词族 / investigator 义务账本 / critic 清账前证明闸门），评审结论：**8/10，方向正确且与本报告 §3 根因判断收敛，采纳但需四处修正**：

1. 语言句式触发（例如看到 "X requests a flush" 就要求补证据）容易被措辞变化绕过 → 改为结构化字段触发（§4.2）；
2. planner 词族自由匹配会产生过多任务 → 绑定 spec 条款与攻击面报告中的危险操作点（§4.2）；
3. "找不到 completion 就不能 no-finding"作为全称规则过强，与有界迭代冲突 → 收窄到义务类子任务；若结论为 `partial`，需要明确下游消费者；
4. 未覆盖"被错误假设的 completion"（本案最深一层：completion 看似存在但仅在一个结果分支上成立）→ completion 字段加结果分支子问题，不可证时走假设台账（§4.2/§4.3）。

另：其账本缺 `scope` 字段，本案第二半（粒度错配）只有隐式覆盖，需补。

## 6. 残余风险

即使 §4 全部落地，对"实证硬件行为"类漏洞，管线最多能把相关位置标为需要实测，不能单靠源码审查闭合结论。真正闭合需要动态验证手段（失败注入 / 行为观测，如 KVM selftest 式 harness）。这是源码静态方法的边界，应在路线图中显式承认。TODO.md 中优先级 P0 的 chain 分析（跨原语聚合）不能解决本案，因为它组合已发现的原语，而本案的问题是原语没有被发现。

---

## 附录 A：证据实录

> 工作区 `.zeromdash/` 在 `.gitignore` 内，可能随时清理，故关键片段直接内嵌于此；
> 每条后括注原始出处，仅供仍持有该工作区者复核。

### A.1 上游修复的关键 diff（torvalds/linux@60d93c27，2026-09-04）

```diff
 static void new_asid(struct vcpu_svm *svm, struct svm_cpu_data *sd)
 	if (sd->next_asid > sd->max_asid) {
 		++sd->asid_generation;
 		sd->next_asid = sd->min_asid;
-		svm->vmcb->control.tlb_ctl = TLB_CONTROL_FLUSH_ALL_ASID;
-		vmcb_mark_dirty(svm->vmcb, VMCB_ASID);
+		sd->flush_all_asids = true;        /* 修复后：flush 请求改为 per-pCPU 记录 */
 	}

 static __no_kcsan fastpath_t svm_vcpu_run(struct kvm_vcpu *vcpu, u64 run_flags)
+	if (this_cpu_ptr(&svm_data)->flush_all_asids) {
+		svm->vmcb->control.tlb_ctl = TLB_CONTROL_FLUSH_ALL_ASID;
+		vmcb_mark_dirty(svm->vmcb, VMCB_ASID);
+	}
 	...
-	svm->vmcb->control.tlb_ctl = TLB_CONTROL_DO_NOTHING;
+	if (!svm_is_vmrun_failure(svm->vmcb->control.exit_code)) {
+		this_cpu_ptr(&svm_data)->flush_all_asids = false;
+		svm->vmcb->control.tlb_ctl = TLB_CONTROL_DO_NOTHING;
+	}                                      /* 修复后：仅在 VMRUN 成功时才清账 */
```

commit message 关键句："empirical testing shows that the CPU performs the requested
TLB flush if and only if VMRUN is successful, i.e. clearing TLB control on a failed
VMRUN effectively drops a TLB flush." —— 决定性事实是**实测硬件行为**，不见于 AMD APM。

### A.2 两份 x86 快照的身份与漏洞代码

```
# .zeromdash/workspace_for_kvm-x86/main/repo（2026-07-03 运行）
a204badd8432f93b7e862e7dac6db0fe3d65f370 2026-06-25 Merge branch 'kvm-chainsaw' into HEAD
  arch/x86/kvm/svm/svm.c:1904:  svm->vmcb->control.tlb_ctl = TLB_CONTROL_FLUSH_ALL_ASID;
  arch/x86/kvm/svm/svm.c:4602:  svm->vmcb->control.tlb_ctl = TLB_CONTROL_DO_NOTHING;

# .zeromdash/workspace_for_kvm-x86-latest/.../scratch-kvm-next（2026-08-26 运行）
76671054f9a1ff6abb976583cd8da37650acdc97 2026-08-24 Merge tag 'kvmarm-7.3' ...
  arch/x86/kvm/svm/svm.c:1905:  svm->vmcb->control.tlb_ctl = TLB_CONTROL_FLUSH_ALL_ASID;
  arch/x86/kvm/svm/svm.c:4621:  svm->vmcb->control.tlb_ctl = TLB_CONTROL_DO_NOTHING;
```

注：kvm-x86-latest 的 `main/repo` 当时是**空目录**，实际分析树是物化在
`sub_workspace/node_search_new_feature/scratch-kvm-next` 的 76671054——critic 评审
原文："(main/repo EMPTY at HEAD 76671054f9a1ff6; materialized …)"。这是
fetch_target_repo 节点不稳定的一个迹象，虽未直接导致本次漏报，值得修。

### A.3 spec-035 investigate 原始 transcript 实录（决定性证据）

**① 它完整读过含 bug 的代码段**（iter-1 transcript 中的文件读取输出）：

```c
/* scratch-kvm-next/arch/x86/kvm/svm/svm.c，svm_vcpu_run() 尾部 */
  4613		/* Track VMRUNs that have made past consistency checking */
  4614		if (vcpu->arch.nested_run_pending &&
  4615		    !svm_is_vmrun_failure(svm->vmcb->control.exit_code))   ← "VMRUN 会失败"的谓词
  4616	                ++vcpu->stat.nested_run;
  4621	svm->vmcb->control.tlb_ctl = TLB_CONTROL_DO_NOTHING;             ← buggy 清除，同屏
  4627	if (cpu_feature_enabled(X86_FEATURE_ERAPS))
  4628		svm->vmcb->control.erap_ctl &= ~ERAP_CONTROL_CLEAR_RAP;      ← 它后来分析的那行
```

**② 它 grep 过 `control.tlb_ctl` 的全部 writer**（transcript 中的 rg 调用与结果）：

```
$ rg -n "control\.nested_cr3|control\.asid|control\.tlb_ctl|..." arch/x86/kvm/svm
arch/x86/kvm/svm/svm.c:1905:	svm->vmcb->control.tlb_ctl = TLB_CONTROL_FLUSH_ALL_ASID;   ← 设置端
arch/x86/kvm/svm/svm.c:4205:	svm->vmcb->control.tlb_ctl = TLB_CONTROL_FLUSH_ASID;
arch/x86/kvm/svm/svm.c:4621:	svm->vmcb->control.tlb_ctl = TLB_CONTROL_DO_NOTHING;         ← 清除端
arch/x86/kvm/svm/sev.c:3618:	svm->vmcb->control.tlb_ctl = TLB_CONTROL_FLUSH_ASID;
arch/x86/kvm/svm/nested.c:934:	vmcb02->control.tlb_ctl = TLB_CONTROL_DO_NOTHING;
```

该次 grep 的目的原文："I'm doing one repository-wide search for **alternate writers**
before committing to a no-finding." —— 当时检查的问题是"谁还能写这个字段"，没有追问"硬件消费它的
每个结果分支下请求去了哪"。

出处：`.zeromdash/workspace_for_kvm-x86-latest/log/review_log/spec-035.iter-1.investigate_subagent.attempt-1.log`
（全文 tlb_ctl×40、TLB_CONTROL_DO_NOTHING×12、svm_vcpu_run×13）。

**③ 而它的结论（spec-035 iter-1 调查报告原文）**：

> "For ASID/NPT reuse, nested entry unconditionally **requests** MMU sync and
> current-ASID TLB flush, while SVM TLB callbacks flush current ASID or recycle
> ASID generation, and the VMRUN loop writes the current ASID into the VMCB
> before hardware entry."

"requests … flush" 被当作了"flush 会发生"的证明——正是 §4.1 request ≠ effect ≠
completion 要禁止的推理。

### A.4 spec-035 critic 实录

**iter-1（判 revise）先认可了 ASID/flush 论证**：

> "(2) ASID/NPT 重用 TLB 刷新——nested_svm_transition_tlb_flush (nested.c:688-707)
> 无条件发出 KVM_REQ_MMU_SYNC+KVM_REQ_TLB_FLUSH_CURRENT；在入口 :862 和 vmexit
> :1433 处调用；TODO 注释记录了有意的保守性（不是半修复）……所有证据均成立。"

**随后把第二轮引离现场**（iter-1 feedback.next_focus 原文）：

> "针对 host-to-guest 预测器/状态隔离模式进行发散式遍历——具体枚举每一条到达
> RAP-clear sink 的路径……**不要重新推导第一轮迭代已经证明的 vmcb12 控件验证 /
> ASID-NPT 刷新 / xAPIC 逻辑表不变式。**"

**iter-2（判 confirm）的危险点枚举离 bug 仅 6-7 行**（reasoning 原文）：

> "My grep confirms the CLEAR_RAP sink-arrival set is fully enumerated: nested VMRUN
> nested.c:1012, nested VMEXIT nested.c:1351, **non-nested VMRUN svm.c:4535** …
> plus the **unconditional post-exit mask svm.c:4628**."

4628 是 CLEAR_RAP 清除行；buggy 的 tlb_ctl 清除在 4621，同一视野内但不在当时的检查问题内。

出处：`.zeromdash/workspace_for_kvm-x86-latest/log/review_log/spec-035.review.log`

### A.5 spec-028 实录（kvm-x86，2026-07-03）

**investigation iter-2 原文**（注意 "requests" 句式再次出现）：

> "new_asid only increments the CPU generation when that CPU exhausts its ASID
> range, then resets next_asid and **requests TLB_CONTROL_FLUSH_ALL_ASID** before
> reusing ASID numbers (svm.c:1901-1904)."

其证据同时引用 svm.c:4508（"the only hardware VMCB ASID assignment … svm.c:4508"，
位于 buggy 行 4602 上方）与 svm.c:4640/4646（load_mmu_pgd，位于 4602 下方）——
**两次从 bug 行上方跨到下方**，分析对象是"谁写 ASID"，从未审计"退出后清除
tlb_ctl 对失败 VMRUN 是否安全"。

**critic iter-2（判 confirm）reasoning 原文（节录）**：

> "(2) Generation wrap: asid_generation is uint64_t (svm.h:146) / u64 (svm.h:372);
> new_asid (svm.c:1899-1910) only bumps generation on next_asid>max_asid with
> TLB_CONTROL_FLUSH_ALL_ASID; the svm.c:3765 FIXME is non-exploitable at ≤1
> increment per ASID-range exhaustion."

critic 独立复核了 `new_asid` 与 FLUSH_ALL_ASID——验证的是**设置端**；七个 gap
（generation wrap、per-CPU 不变量、CVE 映射、nested.c TODO、nNPT-disabled、
from_hardware、PSMASH）全部属于"状态转换→flush"问题，没有任何一条问"pending
tlb_ctl 在 VMRUN 失败时去哪了"。

出处：`.zeromdash/workspace_for_kvm-x86/log/review_log/spec-028.{investigation,review}.log`

### A.6 运行时代理与模型实录

```
# investigate（两次运行一致，agent_invocation.json metadata.command 原文）
codex exec --color never --skip-git-repo-check -C <subtask_dir> --profile foundry --model gpt-5.5 -

# critic
claude -p ... --output-format json --settings /Users/c0ss4ck/.claude/settings.bailian.json   # kvm-x86
claude -p ... --output-format json --settings /Users/c0ss4ck/.claude/settings.ark-proxy.json # kvm-x86-latest

# settings 中的模型注入
settings.bailian.json:   "ANTHROPIC_MODEL": "glm-5.2"   （文件 mtime 2026-08-16，晚于 07-03 运行日 → 置信度中等）
settings.ark-proxy.json: "ANTHROPIC_MODEL": "GLM-5.2"   （文件 mtime 2026-08-22，早于 08-26 运行日 → 确认）
```

两个 critic 会话均 40+ 轮、input tokens 10 万+（spec-035 critic 另有 ~310 万
cache-read）。审查投入并不低，漏报主要来自审计协议缺口。

出处：各 `sub_workspace/node_{investigate_subagent,critic_one}/subtask_*/agent_invocation.json`

### A.7 prompts 制度史实录（本仓库 git 历史，可公开复核）

```
$ git log -S "Sanitize liveness" --format='%h %ad %s' --date=short -- zeromdash/prompts.py
a371db5 2026-07-08 Update: support disable-spec and disable-target-history   ← 三条纪律引入

$ git log --since=2026-08-27 --oneline -- zeromdash/prompts.py zeromdash/presets/
1afa2d6 refactor: 将 critic_one 重命名为 critic_subtask 并兼容旧调用
b46d999 refactor: 完成subagent到subtask的全链路重命名与适配                   ← 仅重命名
```

旁证：spec-035 iter-1 原始 transcript 中 "Sink-anchored enumeration /
Sibling parity / Sanitize liveness" 共出现 13 次——三条纪律在 8/26 运行时已在位，
且未触发。

## 附录 B：时间线

| 时间 | 事件 |
|---|---|
| 2012（约） | `38e5e92fe8c0` 引入 Flush-By-Asid，漏洞诞生 |
| 2026-06-29 ~ 07-03 | kvm-arm64×5、kvm-x86、kvm-x86-nested-virt 扫描（快照 a204badd） |
| 2026-07-03 | spec-028 判 no-finding（两轮迭代） |
| 2026-08-26 ~ 27 | kvm-x86-latest 扫描（快照 76671054）；spec-035 判 expected_behavior（两轮/上限三轮） |
| 2026-09-04 | 上游修复 60d93c27 公开 |
| 2026-10-06 ~ 15 | 本复盘 |

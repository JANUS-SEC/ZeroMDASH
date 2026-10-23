# Seth Jenkins：漏洞研究成长分析

- 擅长领域：Android 内核与在野漏洞
- 独立复核：pass · 91/100

## 成长阶段

- **2022-12-08 · x86 KASLR 缓解有效性评估**：在其本轮已抓取的公开作品中，2022-12-08 文为最早一篇对缓解有效性作系统性评估的 writeup；更早未抓取或未发表工作无法排除。该文以 CVE-2022-42703 利用为入口，综述 x86 KASLR 缓解状态，复用 Jann Horn 最初发现的内核漏洞与其序列化指令建议（以 lfence 替换 cpuid）、Daniel Gruss 的 prefetch 侧信道研究与开源 timing 代码、Peter Zijlstra 提出的 CEA 随机化 patch，并向 Linux 内核安全团队提议 CEA 随机化。该阶段形成『先评估缓解有效性、再决定利用路径』的研究取向。（置信度：medium）
  - 证据：sj-r1-2022-kaslr-article, sj-community-2
- **2025-11-03 · arm64/Android 线性映射评估与可证伪测量**：研究方法由单点漏洞利用转向系统性缓解评估与可证伪测量。因 Pixel 内核利用中具任意写原语却缺 KASLR leak 的技术缺口，转向研究 arm64 Linux 线性映射；自建约 5GB mmap 与 /proc/pagemap 采集程序并跨 100 次重启采样验证物理页分配可预测性，使用 Jann Horn 构建的基于 BPF probe_read_kernel 的内核读工具与数据可视化工具，并由其讲解内核虚拟地址空间布局决策。两项发现（线性映射无随机化、Pixel 静态物理地址）被 Linux 内核团队与 Google Pixel 判为 intended behavior，作者据此调整对缓解有效性的判断并以公开 writeup 形式记录负面结果。（置信度：high）
  - 证据：sj_pz_2025_11_kaslr, sj-conv-kaslr-necessity, sj-conv-jann-mentor-tooling, sj-conv-100-reboot-repetition, sj-conv-intended-behavior-disappointment, sj-community-1, sj-community-3, seth-jenkins-ext-02, seth-jenkins-ext-04, sj-tl-02, sj-r3-bpf-tool-attribution, sj-dec-001
- **2026-01-14 · 驱动攻击面工具化枚举与完整 0-click 利用链**：将攻击面发现工具化并构建完整 0-click 利用链。自建 DriverCartographer 在 mediacodec SELinux 沙箱上下文枚举可达驱动，发现 /dev/bigwave，经数小时审计发现三处独立缺陷（含可逃逸沙箱者）；以 Unix Domain Socket 消息喷洒 kmalloc 控制 freed job->regs 实现任意写。记录首个发现为 2024-02 已报告逾年未修的重复 bug。BigWave 驱动漏洞（/dev/bigwave）与 CVE-2025-36934 的等同关系为跨文推断：Part 1（Natalie Silvanovich 主笔）将 CVE-2025-36934 归于 Seth Jenkins 的沙箱可达驱动调查，Part 2（Seth Jenkins 本人）点名 /dev/bigwave 但全文未出现该 CVE 编号，等同关系非本人一手陈述。（置信度：high）
  - 证据：sj_pz_2026_01_pixel9_bigwave, sj-conv-drivercartographer, sj-conv-duplicate-stale-fix, sj-community-4, sj-community-5, seth-jenkins-ext-03, sj-tl-03, sj-r1-part2-no-cve, sj-r1-part1-cve36934, sj-dec-002
- **2026-05-13 · 跨代迁移、缓解适配与厂商流程评估**：利用链跨设备复用与对新缓解的快速适配，并将厂商流程评估纳入研究复盘。Dolby 利用经偏移调整移植至 Pixel 10；针对 Pixel 10 改用 RET PAC 取代 -fstack-protector 致原 Pixel 9 路径失效，改以 VPU 驱动（/dev/vpu）remap_pfn_range 未限界实现任意物理内存映射，约 2 小时审计、5 行代码取得任意内核读写。作者在文中自述该 bug 为其首个在 90 天内被修复的 Android 驱动 bug（证据 sj-tl-04），未独立核验其全部历史报告的修复时序。（置信度：medium）
  - 证据：sj_pz_2026_05_pixel10_vpu, sj-conv-vendor-response-feedback, sj-conv-doc-self-criticism, seth-jenkins-ext-01, sj-tl-04, sj-dec-003

## 主要成长机制

### 必要性驱动选题

起点：Pixel 内核利用中具强任意写原语却缺 KASLR leak 的具体技术缺口，构成可感知的研究阻碍。

练习与反馈：以当前阻碍链路的能力缺口作为下一研究目标的选取依据，而非以已掌握熟练度的领域作为选题驱动。直接证据集中于 2025-11 一例：因缺 KASLR leak 而研究 Linux 线性映射；2026-05 一例为基于 Pixel 10 改用 RET PAC 致 Pixel 9 路径失效转用 VPU 新原语的合理推断。2022 与 2026-01 两例不附缺口驱动归因，分别陈述为研究内容复用（CVE-2022-42703 延伸至 x86 KASLR 评估）与协作延伸（DriverCartographer 枚举驱动为选题手段，堆喷为利用实现手段而非选题驱动）。；两项发现被内核团队与 Pixel 判为 intended behavior，构成『缺口驱动选题的结果不一定被接受为漏洞』的反馈；作者据此调整对缓解有效性的判断并以公开 writeup 记录，而非终止研究。

能力与结果：形成以可行性与缺口为筛选条件的研究目标选取能力，将研究投入约束在当前阻碍链路的可解决节点。；2025-11 因缺 KASLR leak 转向线性映射研究并完成 KASLR 静态绕过分析；2026-05 RET PAC 缓解变化后转用 VPU 新原语实现任意内核读写（合理推断）

置信度：medium；替代解释：该选题模式可能部分由 Project Zero 团队的研究节奏与发布周期塑形，而非纯粹的缺口驱动；『必要性驱动』亦可能是事后对研究路径的叙事建构，缺独立第三方佐证，且样本仅 4 篇可见 writeup，未发表工作不可见，幸存者偏差使该机制的频次与一致性被高估。

证据：sj-conv-kaslr-necessity, sj-conv-intended-behavior-disappointment, sj_pz_2025_11_kaslr, sj_pz_2026_05_pixel10_vpu, sj-community-3

### 自建测量与枚举工具（个人可迁移）与同事供给工具（组织不可迁移）的区分

起点：需将模糊直觉（物理页分配可预测性、沙箱可达驱动入口）转化为可重复测量的研究前提。

练习与反馈：自建测量与枚举工具：约 5GB mmap 与 /proc/pagemap 采集程序及 100 次重启采样脚本（KASLR 研究）、DriverCartographer 驱动枚举工具（Pixel 9 研究），此为个人自建、可迁移的部分。同时使用 Jann Horn 构建的基于 BPF probe_read_kernel 的内核读工具与 pfn 可视化工具，并由其讲解内核虚拟地址空间布局决策——此为同事供给、属组织内知识传递、不可迁移的部分。两类工具在研究中并行支撑数据采集与突破内核地址空间随机化门槛。；自建工具产出的可重复数据替代主观判断；同事供给的工具与讲解降低个人突破内核地址空间随机化的门槛，工具共享与即时反馈替代独自摸索。

能力与结果：形成『直觉到可重复测量到数据集到结论』的工程化研究流，以及把审计入口前置步骤工具化的攻击面枚举习惯。；KASLR 研究中以 100 次重启采样取得物理页分配可预测性数据集；DriverCartographer 在 mediacodec 沙箱上下文枚举出 /dev/bigwave

置信度：high；替代解释：自建工具的可见频次偏高受样本受限影响（仅 4 篇 writeup 可见，未发表工作与弃用思路不可见）；同事供给工具的可用性本身是 Project Zero 组织条件，离开该组织后该部分能力不可独立复制，故个人方法论解释力不应将组织条件计入。

证据：sj-conv-100-reboot-repetition, sj-conv-drivercartographer, sj-conv-jann-mentor-tooling, sj-community-1, sj-community-4, seth-jenkins-ext-02, sj-r3-bpf-tool-attribution, sj_pz_2025_11_kaslr, sj_pz_2026_01_pixel9_bigwave

### 跨时期跨平台延续与迁移适应性再工程

起点：既有的 x86 KASLR 分析经验与 Pixel 9 利用链资产，构成可迁移的研究地基。

练习与反馈：将分析方法跨平台（x86 到 arm64/Android）与跨设备代际（Pixel 9 到 Pixel 10）延续复用。需声明：2022-12 至 2025-11 约 3 年个人署名产出缺口使该跨期连续性为推断而非直接证据。迁移中区分两类反馈：Dolby 利用经偏移调整移植构成成功跨代迁移的工程化复用结果（非失效驱动）；Pixel 10 改用 RET PAC 取代 -fstack-protector 致原 Pixel 9 路径失效后，转而以 VPU 驱动新原语替代，属失效与替代型反馈，该转向由作者在 2026-05 文中以文章标题方式自述。；缓解变化导致原路径失效时，不放弃而改走新原语；跨代移植中旧研究文档不全拖累新研究，作者自述遗憾此前未更好记录哪些 syncframe 含偏移，由此转化为对记录粒度的自我要求。

能力与结果：形成对缓解变化的适应性再工程能力，以及对研究文档完整性的迭代意识（输出亦需为未来复用而设计）。；2025-11 arm64 线性映射评估作为 x86 KASLR 工作的延展；2026-05 Dolby 利用经偏移调整移植至 Pixel 10，并以 VPU 新原语替代失效路径

置信度：medium；替代解释：跨期延续可能部分由 Project Zero 团队既有 Android 驱动研究脉络与发布节奏塑形，而非纯粹的个人能力迁移；3 年产出缺口使跨期连续性为推断，且样本仅 4 篇可见 writeup，幸存者偏差使迁移成功率与一致性被高估。

证据：sj-r1-2022-kaslr-article, seth-jenkins-ext-04, sj_pz_2025_11_kaslr, sj_pz_2026_05_pixel10_vpu, sj-conv-doc-self-criticism, sj-community-2

### 以量化测量验证假设

起点：需对物理页分配可预测性、厂商修复时效、驱动缺陷模式等假设作可证伪验证。

练习与反馈：以量化测量验证假设：100 次重启采样（KASLR 物理页分配）、数小时审计工时量化（Pixel 9 BigWave 三处独立 bug）、约 2 小时联合审计复现同类 mmap 边界缺陷（Pixel 10 VPU，与 Jann Horn 协同）、5 行代码量化利用复杂度、以具体时间窗（逾 1 年未修、71 天修复、自述首次 90 天内修复）量化厂商响应。需注意 2026-05 约 2 小时人工审计为量化测量实例，非自建工具实例。；量化结果构成对厂商主动安全投入预期的修正：报告 BigWave 后希望厂商主动评估其他驱动，5 个月后仍与 Jann Horn 在 2 小时审计中发现 VPU 严重漏洞，预期被打破；评级差异（BigWave 初评 Moderate、功能等价的 VPU 评 High）作为可观察事实记录。

能力与结果：形成以数据而非印象评估漏洞生命周期与厂商响应的能力。；KASLR 物理地址固定性的 100 次重启量化采样；BigWave 与 VPU 修复时效及评级差异的量化记录；作者自述该 bug 为其首个在 90 天内被修复的 Android 驱动 bug（未独立核验全部历史报告时序）

置信度：high；替代解释：量化习惯可能由 Project Zero 团队的研究规范与 issue tracker 流程塑形，而非纯个人特质；修复时效数据依赖厂商流程，不可完全归因为个人研究能力，且四机制均以当事人自述为唯一来源，缺独立佐证。

证据：sj-conv-100-reboot-repetition, sj-conv-duplicate-stale-fix, sj-conv-vendor-response-feedback, seth-jenkins-ext-01, sj-tl-03, sj-tl-04, sj_pz_2026_01_pixel9_bigwave, sj_pz_2026_05_pixel10_vpu

## 可迁移与不可迁移

- 可迁移：以当前阻碍链路的能力缺口作为下一研究目标的选取依据，而非以已掌握熟练度的领域作为选题驱动。
- 可迁移：将模糊直觉转化为可重复测量（如 100 次重启采样、审计工时量化），以可证伪方式验证假设。
- 可迁移：把审计入口的前置步骤工具化（如驱动枚举），从手工审计转向系统化候选枚举。
- 可迁移：跨平台与跨设备代际的资产复用，将既有原语与分析方法迁移至新目标，并对缓解变化作适应性再工程。
- 可迁移：以具体时间窗与评级数据量化厂商响应，将厂商流程纳入研究复盘。
- 可迁移：把负面结果（被判 intended behavior、重复发现旧 bug）以公开 writeup 形式记录而非隐藏。
- 不可直接迁移：Jann Horn 构建的基于 BPF probe_read_kernel 的内核读工具与 pfn 可视化工具，及其对内核虚拟地址空间布局决策的讲解，属 Project Zero 组织内知识传递，离开该组织不可独立复制。
- 不可直接迁移：Project Zero 既有 Android 驱动研究脉络（2023-09、2024-06、2024-12 等前作）提供的连续研究谱系与定位，属团队资产而非个人可复制条件。
- 不可直接迁移：Project Zero 作者署名平台带来的可见度与协作入口，属组织背书而非个人可复制条件。
- 不可直接迁移：与资深同事 Jann Horn 的结对协作审计（如 VPU 约 2 小时联合审计），属组织内协作条件。
- 不可直接迁移：若 person_json 标注的 Black Hat US 演讲事实成立，则该会议身份构成组织背书条件；当前未由议程页或演讲页一手核验（blackhat.com 返回 403，WebSearch 无可抓取 URL），转移边界判定待证。

## 复核问题

- 无关键事实、身份或来源错误。四阶段与四机制引用的 evidence_ids 经逐一核验均对应 six_dimensions 或 targeted_research 中 verified_in_run=true 的有效证据，未引用已作废 id（sj-tl-01、sj-conv-2022-kaslr-history、sj-community-6）。人物同一性（Project Zero 署名 Seth Jenkins，Android/Pixel 内核与媒体栈方向）与 person_json 一致，未见同名歧义被采纳为事实。
- 非阻断性观察，不触发 revise：mechanism[1].validation_tests 的 "repeated" 判定建议在后续迭代中附加说明——当前自建工具实例经 round-3 移除"2 小时人工审计"后仅余两例跨期实例，"repeated" 标签的严格性宜在 confidence 说明或 alternative_explanation 中进一步限定（如"跨 2 例自建工具实例的 repeated，受样本受限影响"）。当前综合已在 tensions[4] 声明样本受限，故不构成 revise 触发条件。
- 非阻断性观察，不触发 revise：stage-2 的 BigWave↔CVE-2025-36934 跨文推断建议在后续迭代中补充 issue tracker 页面（425917200、426548270、426567975）的独立抓取，以将"跨文推断"升级为"一手核验"。当前已标注为跨文推断且未作确定事实陈述，符合规范，故不构成 revise 触发条件。

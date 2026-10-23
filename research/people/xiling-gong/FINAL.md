# Xiling Gong：漏洞研究成长分析

- 擅长领域：Android 内核与 SoC 漏洞
- 独立复核：pass · 77/100

## 成长阶段

- **2026-03（单点；此前此后时点无 verified 来源） · 公开 KGSL GPU UAF-to-root writeup（CVE-2024-23380）**：在 2026-03-28 经 androidoffsec.withgoogle.com 公开一篇 Qualcomm KGSL GPU 驱动 use-after-free 到 Android root 的完整利用 writeup（CVE-2024-23380，合著 @Rishika Hooda），展示从竞态触发、物理页回收与 spray、经 GPU CP_MEM_TO_MEM 扫描可控物理页、篡改 kgsl_memdesc 的 physaddr/size/ops，到 mmap 将内核映射为可写用户态内存并 patch sel_read_enforce 关闭 SELinux 的完整链，并经正文 banner 自述归属 Google Android Red Team。此为本节点唯一经一手核验的能力快照；由于仅存在单一时点的 verified 来源，无法据以重建该能力随时间如何形成或演化的成长轨迹，亦无法据以判断此为一长期积累的稳态能力还是专项攻坚产物。（置信度：medium）
  - 证据：r2-works-kgsl-writeup-01, r2-works-kgsl-writeup-02

## 主要成长机制

### GPU 驱动物理页能力为核心的内核任意读写构造

起点：已核验的起点仅为 2026-03-28 一篇公开 writeup 的存在与其技术内容（r2-works-kgsl-writeup-01/02）。该 writeup 假定作者已具备对 Qualcomm KGSL GPU 驱动内部结构（VBO/BMO refcount、kgsl_mem_entry、kgsl_memdesc 的 physaddr/size/ops、CP_MEM_TO_MEM 命令流）与 Android 内核低内存回收、slab/堆布局、SELinux 运行机制的理解，并能访问 GPU 驱动提供的物理页访问能力。这些前置条件本身无一手来源直接记录，属由成品 writeup 反推的推断；作者此前是否有 KGSL 或其他 GPU 驱动研究经历、是否经由团队协作取得前置能力，均无可核验来源。

练习与反馈：无可核验的跨时期重复行为或练习过程：六维取证 20 个 item 全部 status=unknown、verified_in_run=false、level=lead_only，定向补证仅取得单篇 writeup。仅能从该 writeup 的成品推断一次完整利用链的构造过程——根因为两线程并发对同一 VBO 执行 bind/unbind 致 BMO refcount 竞争、backend 物理页释放后 VBO 仍可访问的物理页 use-after-free；利用六步为触发竞态→低压回收释放页进内核堆→spray kgsl_mem_entry→经 CP_MEM_TO_MEM 扫描可控物理页→篡改 kgsl_memdesc 的 physaddr/size/ops→mmap 将内核映为可写用户态内存并 patch sel_read_enforce 关闭 SELinux。是否存在同类漏洞或同类链的反复实践，缺乏证据。；可核验的反馈来源仅限成品 writeup 自身与团队写作环境：writeup 经 Google Android 官方安全博客（androidoffsec.withgoogle.com）发布，正文致谢队友 Martijn Bogaard、Xingyu Jin、Zi Fan Tan，同站另有 @Zi Fan Tan、@Gulshan Singh、@Eugene Rodionov 的 Binder 系列文章，提示其处于一个内部可相互评审的团队写作环境。该环境是否构成对其研究方法的实质性反馈回路（评审、复现、纠错），以及公开渠道（x.com/lazydogsec、Black Hat Asia/POC）是否提供同行反馈，均未取得一手核验，列为缺口。

能力与结果：由成品 writeup 反推，作者在 2026-03 时点具备或可调用以下中间能力（均为推断，非跨时期稳态能力的直接证据）：(1) 对 Qualcomm KGSL GPU 驱动内部对象生命周期与 refcount 语义的分析；(2) 经 GPU 命令流（CP_MEM_TO_MEM）构造可控物理页扫描以绕过 CPU 侧地址随机化/隔离的能力；(3) 将内核物理页经 kgsl_contiguous_vmfault 路径映射为用户态可写内存，再 patch sel_read_enforce 关闭 SELinux，并绕过 kCFI/W^X/DEP 的利用收尾能力。这些能力的形成过程无来源支撑。；公开 writeup《A Technical Deep Dive into CVE-2024-23380: Exploiting GPU Memory Corruption to Android Root》（androidoffsec.withgoogle.com，2026-03-28，合著 @Rishika Hooda）；正文自述归属 Google Android Red Team（banner「Exploit by Xiling Gong of Android RedTeam, Google:)」，页脚「© Google, 2026」）；该 writeup 描述的影响为 Android root + 内核任意读写/代码执行，并绕过 kCFI/W^X/DEP

置信度：low；替代解释：竞争性解释一（组织资源归因）：该 writeup 的复杂度、官方发布渠道与团队致谢，提示其可能是 Google Android Red Team 内部资源、协作评审与漏洞/样本获取条件下的产物，而非可归因于个人成长路径的稳定能力；在此解释下，'机制' 的真正驱动力是组织资源而非个人反复练习。竞争性解释二（单点专项 vs 可迁移能力）：该能力可能是一次针对特定 CVE 的专项攻坚结果，缺乏证据表明其为可跨驱动、跨时期复用的稳定方法论。两种解释均与材料相容，无法据单篇 writeup 排除任一。

证据：r2-works-kgsl-writeup-01, r2-works-kgsl-writeup-02

## 可迁移与不可迁移

- 可迁移：将 GPU 驱动物理页访问能力作为内核地址空间桥接原语：经 GPU 命令流（如 CP_MEM_TO_MEM）扫描可控物理页、再篡改驱动内部描述符（如 kgsl_memdesc 的 physaddr/size/ops）以经驱动 fault 路径将内核物理页映射为用户态可写内存的构造思路，是 writeup 中明确给出、原则上可迁移到其他持有'用户可控物理页访问'能力驱动的技术原语（依据 r2-works-kgsl-writeup-02；属单篇 writeup 提取的可迁移技术原语，非跨人可迁移的能力保证）。
- 可迁移：利用竞态致物理页 use-after-free 后经低压回收回收入内核堆、再以驱动对象 spray 复位的内存布局操纵方法（依据 r2-works-kgsl-writeup-02；同上，为技术方法层面的可参考做法，其有效性受具体内核版本、回收路径与对象布局约束）。
- 可迁移：以 patch sel_read_enforce 关闭 SELinux 作为内核任意读写后的提权收尾，并显式评估 kCFI/W^X/DEP 绕过约束的收尾设计（依据 r2-works-kgsl-writeup-02；为利用收尾设计层面的可参考做法）。
- 不可直接迁移：组织资源：Google Android Red Team 归属及其带来的内部协作评审（致谢队友 Martijn Bogaard、Xingyu Jin、Zi Fan Tan）、官方发布渠道（androidoffsec.withgoogle.com）与同站团队写作环境（@Zi Fan Tan、@Gulshan Singh、@Eugene Rodionov 的 Binder 系列），属个人特有条件，普通研究者不具备等价资源（依据 r2-works-kgsl-writeup-01）。
- 不可直接迁移：单点样本：仅 1 篇已核验 writeup，无法据以判断其研究方法是否具备跨时期、跨驱动的稳定性；本报告不主张其研究方法具备跨人可迁移性。
- 不可直接迁移：高排名幸存者偏差：本地种子 rank=95 偏向已公开成名者，相关可迁移性判断可能过度乐观。
- 不可直接迁移：组织声誉偏差：作品平台为 Google 官方安全域，可能使读者高估其专业能力的可迁移性。
- 不可直接迁移：合著与团队贡献不可分离：已核验 writeup 为合著（@Rishika Hooda），且致谢多名队友，单篇成品中个人贡献份额与个人能力边界无法据署名分离，不可整体归因为个人能力。
- 不可直接迁移：前置能力无可核验来源：作者对 KGSL 驱动内部结构、低内存回收、SELinux 运行机制的理解等前置能力，无一手来源记录，属由成品反推的推断，不可作为可迁移条件。

## 复核问题

- 关联 CVE 完整性补充：经独立复核，该 writeup 正文除 CVE-2024-23380 外另提及 CVE-2024-23384、CVE-2024-23381、CVE-2024-23372、CVE-2024-33034、CVE-2025-21479、CVE-2026-21385 等关联 CVE。综合结论 stages[0].capability_change、mechanisms[0].observed_outcomes 与 observed_outcomes[0] 仅取 CVE-2024-23380 作为唯一技术对象，与文章标题一致；建议补一句说明该 writeup 同时涉及上述关联 CVE，避免读者误判该作者研究范围仅限单一 CVE。此为完整性补充，不影响 verdict。
- 措辞微调（非强制）：mechanisms[0].alternative_explanation 与 stages[0].capability_change 中「专项攻坚」一词略带修辞色彩，可改写为「针对特定 CVE 的专项研究」以更贴合克制书面语；非强制，不构成语言规范违规。

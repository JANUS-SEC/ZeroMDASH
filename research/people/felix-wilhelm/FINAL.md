# Felix Wilhelm：漏洞研究成长分析

- 擅长领域：内核/虚拟化/云漏洞
- 独立复核：pass · 85/100

## 成长阶段

- **约 2013–2015（ERNW 顾问 + KIT 硕士阶段） · Xen 仿真层与共享内存攻击面的方法论奠基**：在 ERNW 任职的同时与 KIT 操作系统组保持学术关联，将硕士论文工具 xenpwn（借鉴 j00ru/gynvael 的 Bochspwn，选择性追踪 inter-domain 通信页以控制开销）适配到 Xen，产出 XSA-123（x86 仿真器段前缀内存损坏）与 XSA-155（PV 设备 double-fetch）两个真实 CVE，确立「共享内存接口天然难于保护」与「double-fetch/TOCTOU」两条可复用的攻击面。本阶段仅按公开 writeup 重建方法论，未产出公开成果的研究方向（如 ERNW 时期其他未导致 CVE 的审计目标）未纳入。（置信度：high）
  - 证据：fw-works-001, fw-works-006, fw-community-01, fw-community-02, felix-external-01, felix-external-02, fw-dec-001
- **约 2016–2017（ERNW 后期 → 转入 Google 前后） · 学术迁移尝试与跨虚拟化边界侧信道探索**：发布 mario_baslr，将学术论文「Jump Over ASLR: Attacking Branch Predictors to Bypass ASLR」中的 BTB 碰撞技术扩展到 hypervisor ASLR（PoC 泄漏 KVM 内核模块基址），指出原论文作者未意识到该技术可跨越虚拟化边界；其后被 Jann Horn 在 Spectre Variant 2 披露中致谢引用。同期公开 PV 设备 double-fetch 挖掘方法论（具体会议 Infiltrate/SyScan 360/Black Hat 2016 演讲未经一手核实，列为推断）。本阶段仅按公开 writeup 重建方法论，未产出公开成果的研究方向未纳入。（置信度：medium）
  - 证据：r1-fw-tl-06-mario-baslr, fw-community-03, fw-tl-08
- **约 2017–2022（Google Project Zero） · 高价值边界漏洞挖掘与工具建设并行的成熟期**：在 P0 将 hypervisor 逃逸（KVM AMD 嵌套虚拟化 TOCTOU，CVE-2021-29657）、云认证绕过（Vault，CVE-2020-16250/16251）、内存安全语言中的等效内存腐败（Gregor Samsa Java XSLTC 整数截断，CVE-2022-34169）三类研究并行推进，并构建 weggli（C/C++ 语义搜索工具）作为人工代码审计辅助。反复出现「外部接口即攻击面」「审计过的代码仍可被小改动引入关键漏洞」「individually safe optimizations composed with new functionality become vulnerabilities」三个命题，与后续 DeFi 期「审计过的代码仍有 subtle 漏洞」的观察在方法论上一致。本阶段仅按公开 writeup 重建方法论，未产出公开成果的研究方向未纳入。（置信度：high）
  - 证据：fw-works-002, fw-works-005, fw-conv-001, fw-conv-002, fw-conv-003, fw-conv-004, fw-conv-005, fw-conv-006, fw-conv-007, fw-conv-008, fw-conv-009, fw-community-04, fw-community-05, fw-community-06, fw-community-08, fw-community-09, felix-external-03, felix-external-04, fw-dec-002, fw-tl-10, fw-tl-11, r2-fw-works-008-gregor-samsa, r2-fw-conv-011-vault, r1-fw-community-06-weggli-stars, r3-fw-weggli-treesitter, r3-fw-weggli-early-maintenance
- **约 2022–2026（Asymmetric Research 联合研究） · 研究边界迁移到 DeFi/智能合约与机构化协作**：离开 P0 后转向 Solana/DeFi 安全，作为 Asymmetric Research 成员连续发布 marginfi flash loan 漏洞（约 $160M 风险）、Relay 签名验证绕过、Solana p-token write-then-restore 逃逸三篇署名博文。研究输出由个人独立完成转向机构协作（与 Anza 团队持续 review + fuzzing），方法论内核延续——「individually safe optimizations can become vulnerabilities when composed with new functionality」「small and seemingly harmless change in a well-audited codebase can introduce a critical vulnerability」。本阶段仅按公开 writeup 重建方法论，未产出公开成果的研究方向未纳入。（置信度：high）
  - 证据：fw-works-003, fw-works-004, fw-conv-006, fw-conv-007, fw-conv-008, fw-conv-009, fw-community-08, felix-external-05, fw-dec-004, fw-tl-15, fw-tl-16, fw-tl-17, r1-fw-works-003-marginfi-160m

## 主要成长机制

### 组件组合破坏不变量：在共享内存/外部接口/新功能组合处定位漏洞

起点：2013–2015 年在 ERNW 与 KIT 双轨阶段，以 xenpwn（选择性追踪 Xen inter-domain 通信页）建立「共享内存接口天然难于保护」的工作假设，并以 double-fetch/TOCTOU 作为首类可复用漏洞模式。

练习与反馈：在多个目标上重复练习「在组件组合处定位不变量破坏」：Xen PV 设备 guest/kernel 共享内存 double-fetch（XSA-155）；KVM AMD 嵌套虚拟化 nested_vmcb_checks 校验函数操作 guest 内存而第二 CPU 核可修改的 TOCTOU（CVE-2021-29657）；HashiCorp Vault AWS STS XML 解析宽容性与 GCP JWT claim 注入的认证绕过（CVE-2020-16250/16251）；Java XSLTC 常量池整数截断使攻击者可控条目被重解释为 class 文件结构字段（CVE-2022-34169）；marginfi flash loan 单条新指令破坏借贷逻辑；Solana p-token 在新增 batch 指令后延迟所有权检查与运行时回滚检测组合产生 write-then-restore 逃逸。；厂商公告致谢（Xen XSA-123/XSA-155 单一发现者署名、Red Hat CVE-2018-1111 致谢、HashiCorp 修复、Anza 修复）构成外部闭环验证；博文正文持续把个案归纳为可复用命题（「tricky vulnerabilities like this often exist where developers have to interact with external systems and services」「individually safe optimizations can become vulnerabilities when combined with new functionality」「a small and seemingly harmless change in a well-audited, carefully designed codebase can introduce a critical vulnerability」）。

能力与结果：形成「组件组合处的不变量破坏」作为可迁移主题，能在跨目标（hypervisor 共享内存、认证外部依赖、内存安全语言序列化边界、智能合约新指令组合）上重复识别同类漏洞，而非逐个目标重新建立直觉。；XSA-123 与 XSA-155 在 9 个月窗口内连续以单一发现者署名（Xen 官方公告）；CVE-2021-29657 KVM AMD 嵌套虚拟化 guest-to-host 逃逸，自述两月独立完成；CVE-2020-16250/16251 Vault 认证绕过，CVE-2022-34169 Java XSLTC 整数截断绕过 XML 签名验证；marginfi flash loan 漏洞（约 $160M 风险）、Solana p-token 主网上线前 write-then-restore 逃逸

置信度：high；替代解释：公开 writeup 仅记录成功产出公开成果的研究方向与漏洞发现，未产出公开成果的研究方向（如 ERNW 时期其他未导致 CVE 的审计目标、P0 时期未公开的失败研究）未被纳入机制重建，可能高估「组件组合处漏洞」作为研究者主动选择模式的解释力；此外，目标选择本身可能受到厂商/客户委托范围约束，而非完全由研究者自主判断。

证据：fw-works-001, fw-works-002, fw-works-003, fw-works-004, fw-conv-007, fw-conv-008, fw-community-01, fw-community-02, r2-fw-works-008-gregor-samsa, r2-fw-conv-011-vault, r1-fw-works-003-marginfi-160m, felix-external-01, felix-external-02, felix-external-03

### 工具建设驱动研究：把可复用方法论编码为开源工具

起点：2015 年硕士论文产出 xenpwn，借鉴 j00ru/gynvael 的 Bochspwn 并选择性地追踪特定页面以控制开销，建立「学术工具适配到真实漏洞发现」的早期模式。

练习与反馈：在多个阶段重复把既有工具谱系扩展为自有工具：xenpwn（Bochspwn 式内存访问追踪适配到 Xen inter-domain 通信）；mario_baslr（学术论文 BTB 碰撞扩展到 hypervisor ASLR，指出原论文作者未意识到技术可跨越虚拟化边界）；weggli（受 Semgrep/Coccinelle/joern/CodeQL 启发，基于 tree-sitter 抽象语法树模式匹配，明确 minimal setup / interactive / greedy matching 三项设计原则，recall 优先于 precision）；DeFi 期与 Anza 团队持续 review + fuzzing p-token 代码库。；GitHub 仓库页面一手显示 weggli 2.5k stars、145 forks（社区采用）；GitHub REST API 一手显示 2021-10 期间作者在 issue #2/#8 积极、礼貌回复报告者并快速修复（早期积极维护）；issue #85（2023-09，Is the project still alive?）无维护者回复（后期维护断档）；KVM EPYC 博文显式归功前人/同伴的可复用工具（AMD IBS Toolkit 提供工作代码与可读描述），把社区既有工具作为起点再扩展。

能力与结果：形成「站在既有工具谱系上扩展而非孤立发明」的稳定工程化信念，与「工具辅助而非替代人工审计」的方法论闭环；能区分工具的召回优化与人工过滤的分工。；xenpwn 直接产出 XSA-155（KIT 硕士论文工具化为真实 CVE）；mario_baslr 被 Jann Horn 在 Spectre Variant 2 披露中致谢引用（后置引用，跨研究者采纳）；weggli 在 GitHub 获社区采用（2.5k stars，仓库页面一手数值）；DeFi 期与 Anza 持续 review + fuzzing 在主网上线前捕获 Solana p-token 漏洞

置信度：high；替代解释：公开 writeup 仅记录成功产出的研究方向，未产出公开成果的迁移尝试（如 mario_baslr 之外未导致引用的学术迁移尝试）未被纳入，可能高估「学术论文→虚拟化边界→PoC」迁移路径的普适性；工具的社区采用度（stars）也可能受 P0 平台曝光度而非纯工具质量驱动。

证据：fw-works-001, fw-works-005, fw-works-004, fw-conv-006, fw-community-03, fw-community-05, fw-community-06, fw-community-07, r1-fw-tl-06-mario-baslr, r1-fw-community-06-weggli-stars, r3-fw-weggli-treesitter, r3-fw-weggli-early-maintenance

### 目标选择：优先审查不足的代码与市场份额上升的目标

起点：2013–2015 年在 ERNW 系统覆盖多个 hypervisor 与企业系统目标，形成「在同一雇佣关系内重复练习特定攻击面」的早期积累。

练习与反馈：在跨时期目标选择上重复「审查不足的代码 + 市场趋势」标准：选择 KVM AMD 嵌套虚拟化因「先前在 Intel 侧有过成功」且 AMD 服务器市场份额上升使 AMD 实现成为更有价值目标（「a large potential for complex logic flaws, making it a perfect target for manual code review」）；DeFi 期选择当时锁定价值最高的 Solana/DeFi 协议边界；在 P0 期反复选择「外部系统交互处」（Vault 的 STS/JWT、dnsmasq 的 DNS/DHCP、Java XSLT 的 XML 签名）作为攻击面。；厂商公告致谢的连续出现（XSA-123/XSA-155 在 9 个月窗口内两次单一发现者署名）外部验证目标选择的可重复性；KVM EPYC 博文自述目标选择理由，把「审查不足的高价值边界」作为可叙述的决策标准而非凭空选题。

能力与结果：形成「目标选择优先审查不足的代码与市场份额上升的目标」作为可迁移决策模式，能在不同技术域（hypervisor、云认证、智能合约）重复应用同一选择标准。；KVM AMD 嵌套虚拟化 guest-to-host 逃逸（两月独立完成，自述目标选择理由）；Vault 认证绕过（外部接口即攻击面）；DeFi 期连续三篇署名博文（marginfi、Relay、Solana p-token）

置信度：medium；替代解释：目标选择可能由雇主/客户委托范围与平台曝光度驱动（P0 期的 hypervisor/云、Asymmetric 期的 Solana/DeFi），而非完全由研究者主动选择；公开 writeup 仅记录成功产出的研究方向，未产出公开成果的目标选择未纳入，可能高估该选择标准的解释力。

证据：fw-works-002, fw-works-003, fw-works-004, fw-conv-001, fw-conv-002, fw-community-01, fw-community-02, fw-dec-002, felix-external-03

### 由目标选择、挫折触发的假设重审、务实利用路径三部分构成的研究流程

起点：P0 期 KVM AMD 研究（两月独立、仅远程访问 AMD 系统）作为该流程最完整的一次自述案例，前期已有 ERNW 阶段的反复练习基础。

练习与反馈：在 KVM EPYC 研究中重复该流程：目标选择后，在完全缺乏进展、服务器重启上百次后，因「getting frustrated」触发两周不同利用策略尝试，随后意识到自己对 host save area 字段假设有误（「I made an important mistake」），改用「slow trial and error」逐字段验证，最终接受「somewhat boring but easy-to-implement」的利用路径而非追求更优雅方案；Vault 研究中「slowly getting frustrated and decided to take a look at Vault's response parsing code」呈现同样的挫折→转向触发器；影响评估自述「最初过于自信，事后修正」（「I was feeling pretty confident ... but this turned out to be wrong」）。；博文把挫折与误判作为转向信号而非掩盖呈现，构成自我校准的内部反馈回路；厂商公告确认与修复提供外部闭环；自述的「务实利用优于追求优雅」在多次研究中作为稳定倾向复现。

能力与结果：形成「挫折触发底层假设重审 + 务实接受 boring 方案」作为可重复的研究推进机制，并能主动披露误判作为校准信号，而非全知回溯。；KVM AMD 嵌套虚拟化 guest-to-host 逃逸完整 exploit chain；Vault 认证绕过（挫折转向 response parsing code）；误判的自我披露（影响评估从过度自信到修正）

置信度：medium；替代解释：该流程主要来自单一研究（KVM EPYC）的详细自述，跨研究的挫折→转向样本较少（Vault 博文仅一句话提及），可能高估其作为稳定机制的普遍性；公开 writeup 倾向于呈现「挫折后突破」叙事，未产出公开成果的失败研究未纳入。

证据：fw-works-002, fw-conv-002, fw-conv-003, fw-conv-004, fw-conv-005, r2-fw-conv-011-vault, fw-dec-002, felix-external-04

## 可迁移与不可迁移

- 可迁移：在组件组合处（共享内存接口、外部依赖、新功能与既有优化的组合）系统性定位不变量破坏，而非孤立审查单一组件。
- 可迁移：把可复用的漏洞模式（double-fetch/TOCTOU、整数截断、外部接口宽容性）作为跨目标重复练习的攻击面主题。
- 可迁移：优先审查不足的代码与市场份额上升的目标，并将目标选择理由作为可叙述的决策标准（而非凭空选题）。
- 可迁移：把挫折与误判作为重审底层假设的触发信号，主动披露错误判断作为校准机制，而非全知回溯。
- 可迁移：务实接受 boring but easy-to-implement 的利用路径，而非过度追求优雅方案。
- 可迁移：把个案归纳为可复用方法论文本（命题化），并以签名式结尾（「Make zeroday hard.」）保持跨博文输出一致性。
- 可迁移：站在既有工具谱系（Bochspwn、Semgrep/Coccinelle/joern/CodeQL、IBS Toolkit、学术论文）上扩展而非孤立发明，并明确声明灵感来源。
- 可迁移：把工具建设作为人工代码审计的辅助而非替代，以 minimal setup / interactive / greedy matching（recall 优先）降低审计门槛并支持快速查询迭代。
- 不可直接迁移：ERNW 顾问 + KIT 操作系统组双轨阶段提供的学术与企业研究环境并行支持，使硕士论文工具（xenpwn）直接对接上游开源项目（Xen）并产出真实 CVE；该学术-工业耦合条件依赖特定时期、特定机构组合。
- 不可直接迁移：Google Project Zero 平台提供的全职研究自由度与平台曝光度，使 KVM EPYC 两月独立研究、weggli 工具建设与多目标并行推进成为可能；该条件依赖 P0 雇佣关系，非个人可复制。
- 不可直接迁移：Asymmetric Research 机构定位（专注与 L1/L2 区块链和 DeFi 协议建立长期整合合作）提供的 DeFi 持续审计渠道（与 Anza 团队 ongoing security work），使 review + fuzzing 主网上线前捕获漏洞成为可能；该条件依赖机构客户关系。
- 不可直接迁移：已审计 DeFi 协议锁定资金的攻击面价值（一手核实数额为 marginfi 约 $160M）；该价值规模依赖特定时期 DeFi 市场状态，非个人能力条件。
- 不可直接迁移：跨十余年的公开写作与会议输出历史，使早期研究（mario_baslr，2016）被同伴采纳为后期高影响成果（Spectre V2 致谢，2018）成为可能；该后置引用依赖同伴网络与时间积累，非可规划条件。

## 复核问题

- mechanisms[2].repeated_practice 列举「dnsmasq 的 DNS/DHCP」作为 P0 期外部系统交互攻击面示例，但 dnsmasq 相关证据 fw-tl-07 的 verification.verified_in_run=false、level=lead_only；open_questions[2] 自承「Behind the Masq」Google Security Blog URL 抓取返回 404、6 人团队作者名单仅 lead_only；conversations 与 community 维度的 contradictions/gaps 亦一致记录该证据仅 lead_only。r1 修订已据此将 dnsmasq 从 expertise 删除，但 mechanisms[2] 仍将其作为已核实示例陈述，与综合结论自身的 open_questions 及 r1 处理不一致，属内部不一致的未支撑事实主张。
- stages[2].evidence_ids 含 fw-tl-10（Vault 2020-10），其 verification.verified_in_run=true，但 content_sha256（cb727220cfeea78501a7d56bf8bf397ba06833aaef3bb35d2c488aaa31dcf263）与 fw-tl-14（asymmetric.re/about，claim 自述「本轮 404 未能核验」）及 r1 中 fel1x/mario_baslr（错误 URL 的 404 页面）三处抓取哈希完全相同，且 evidence timeline gaps 自承「/blog/ 路径 404」，表明 fw-tl-10 实际抓取的是 404 页面而非 Vault 文章正文；同一 Vault 内容已由 r2-fw-conv-011-vault（正确 URL https://projectzero.google/2020/10/enter-the-vault-auth-issues-hashicorp-vault.html，不同哈希 5d2bcde9...）妥善核实，fw-tl-10 属冗余且核实存疑的引用。
- mechanisms[2].repeated_practice：删除「dnsmasq 的 DNS/DHCP」示例（因 fw-tl-07 verified_in_run=false、level=lead_only，且 open_questions[2] 自承该 URL 404、团队作者名单仅 lead_only，与 r1 已将 dnsmasq 从 expertise 删除的处理一致）；保留 Vault（STS/JWT，r2-fw-conv-011-vault verified）与 Java XSLT（XML 签名，r2-fw-works-008-gregor-samsa verified）两项 verified 示例，使机制叙述与自身 open_questions 及 expertise 处理一致。
- stages[2].evidence_ids：移除「fw-tl-10」（其 content_sha256 与已知 404 页面 fw-tl-14、fel1x/mario_baslr 抓取哈希一致，且 timeline gaps 自承 /blog/ 路径 404，核实存疑）；Vault 内容由 r2-fw-conv-011-vault（正确 URL、不同哈希、verified_in_run=true）单独支撑。
- stages[1].evidence_ids：移除「fw-tl-08」（verified_in_run=false、status=unknown、level=lead_only）；Spectre V2 致谢由 fw-community-03（verified_in_run=true，Jann Horn「Felix Wilhelm's research based on this provided the basic idea behind variant 2」）单独支撑。
- mechanisms[2].repeated_practice：将「选择 KVM AMD 嵌套虚拟化因「先前在 Intel 侧有过成功」且 AMD 服务器市场份额上升使 AMD 实现成为更有价值目标」改写为仅由 verified short_quote 直接支撑的表述，如「选择 KVM AMD 嵌套虚拟化因先前在 Intel 嵌套虚拟化上有成功经验、且 AMD 实现复杂逻辑漏洞潜力大、适于 manual code review（「a large potential for complex logic flaws, making it a perfect target for manual code review」）」，删除或明确标注「AMD 服务器市场份额上升」为编辑性背景而非 Wilhelm 自述理由。
- mechanisms[2].repeated_practice：将「DeFi 期选择当时锁定价值最高的 Solana/DeFi 协议边界」改写为「DeFi 期选择高锁定值 Solana/DeFi 协议边界（marginfi 约 $160M，经 r1-fw-works-003-marginfi-160m 核实）」，删除「最高」这一未经 verified 证据支撑的相对排名断言，与 open_questions[7] 承认该选择标准为 inferred 的口径一致。

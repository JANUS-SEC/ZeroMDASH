# Samuel Groß (saelo)：漏洞研究成长分析

- 擅长领域：浏览器与 V8 漏洞
- 独立复核：pass · 80/100

## 成长阶段

- **2014 · 系统级与内核利用起点**：以 Linux 内核本地提权公开技术输出为起点：CVE-2014-0038 针对 recvmmsg 的 x86_x32 ABI 未校验用户态传入 timeout 指针，通过向 ptmx_fops 的 release 函数指针位置写入实现 root。此阶段建立 syscall ABI 边界检查缺失与函数指针劫持两类系统级内存破坏利用经验，为后续 JavaScript 引擎 fakeobj 原语与浏览器全链中的系统原语复用提供基础。（置信度：medium）
  - 证据：saelo-tl-01, saelo-decisions-01
- **2015–2016 · 跨平台练习与 JavaScript 引擎转向**：在 Linux 内核提权之外扩展到 iOS 内核工具与 ARM 内存破坏训练仓库（armpwn，README 自述 'train/learn memory corruption on the ARM platform'），把跨平台内存破坏练习转化为可复用仓库。2016 年起将研究重心转向 JavaScript 引擎，从 JavaScriptCore 较轻量的 TypedArray.slice 信息泄露入手（bug 最初仅存在于 Safari Technology Preview，release 12 修复），建立对 JS 引擎内部数据结构的熟悉，而非直接挑战 JIT。（置信度：medium）
  - 证据：saelo-decisions-01, saelo-decisions-02, r1-github-profile-realname-handle, sg-self-01, saelo-ext-01, saelo-works-013
- **2016–2017 · JavaScript 引擎系统化利用方法论确立**：从单 bug 信息泄露升级到 OOB→任意读写→代码执行的端到端利用：JSC Array.slice 越界访问（CVE-2016-4622）配套 jscpwn PoC 仓库与 Phrack 系统论文。同一方法论横向迁移到 Lua（33C3 CTF 'read-eval-pwn loop'，基于 load 函数预编译字节码与 setjmp/longjmp 绕过 Clang CFI）与 Firefox/SpiderMonkey（CVE-2016-9066 cross-mmap overflow，引入 zlib 流式 flush 压缩 4GB 触发载荷至约 18MB、利用 OS 级内存压缩承载大块零填充缓冲）。Lua 研究先向 Lua 邮件列表报告并收到回复，再整理为公开 writeup，形成披露—反馈—输出循环。此阶段将 JIT 类型推断这一当时公开资料稀缺方向转化为可复现的端到端讲解；跨引擎方法迁移而非依赖单一引擎的偶发成果成为可观察特征。（置信度：high）
  - 证据：saelo-tl-02, saelo-tl-04, saelo-tl-05, saelo-tl-06, sg-community-01, sg-community-03, sg-self-02, r1-phrack70-release-date, saelo-decisions-03
- **2017–2018 · 工具化、跨引擎与全链化**：研究形态从单 bug writeup 升级到竞赛级完整 exploit chain：Pwn2Own 2018 完成 Safari RCE + macOS 沙箱逃逸 + 内核 LPE 全链（macOS 10.13.3），由 WebKit DFG JIT 类型混淆、launchd legacy_spawn 沙箱检查缺失、XNU task_set_special_port/bootstrap port MitM 三漏洞串联，仓库以 stage0..stage5 + libspc（XPC 协议重实现）结构化组织。V8 Turbofan 类型混淆（CVE-2018-17463）经 Phrack #70 #9 公开，文章明确该漏洞为源代码审计发现，非 fuzzer 触发。配套工具建设延续（ida_scripts 逆向脚本集合、dnsrebinder DNS rebinding 网络原语）。pwn2own2018 仓库 README 未列 CVE 编号，CVE-2018-4233 关联由配套仓库 saelo/cve-2018-4233 标题间接佐证。（置信度：medium）
  - 证据：saelo-tl-07, saelo-decisions-06, r1-pwn2own2018-readme-no-cve, r1-saelo-v8-turbofan-2018, r1-github-profile-realname-handle

## 主要成长机制

### 跨引擎/跨平台方法论迁移

起点：2014 年在 Linux 内核 syscall ABI 边界检查与 fops 函数指针劫持建立系统级内存破坏利用基础；具备内存破坏原语到代码执行的工程化经验。

练习与反馈：把'内存破坏原语→信息泄露→任意读写→代码执行'链路抽象为通用流程，反复应用到 JavaScriptCore（2016 Array.slice OOB CVE-2016-4622）、Lua（2016/2017 load 函数）、Firefox/SpiderMonkey（2017 cross-mmap overflow CVE-2016-9066）、V8（2018 Turbofan 类型混淆 CVE-2018-17463）、WebKit JIT（2018 Pwn2Own CVE-2018-4233）五个不同引擎。；Lua 研究通过上游邮件列表报告与回复形成披露—反馈—writeup 循环；Phrack #70 经审稿接受 saelo 署名两篇（《Attacking JavaScript Engines》《Exploiting Logic Bugs in JavaScript JIT Engines》）；Pwn2Own 2018 在真实目标上检验全链可靠性。

能力与结果：形成'OOB 索引/类型混淆原语→伪造对象→addrof/fakeobj→任意读写'的通用利用框架，可在新引擎上快速复用，无需逐引擎重新构建基础流程。；JSC Array.slice 越界访问 CVE-2016-4622 配套 jscpwn 与 Phrack 论文；Lua load 函数利用与 33C3 CTF 'read-eval-pwn loop' 挑战；Firefox cross-mmap overflow CVE-2016-9066，自述非重载下 >95% 可靠、约 1 分钟完成；V8 Turbofan 类型混淆 CVE-2018-17463，源代码审计发现；Pwn2Own 2018 Safari RCE + 沙箱逃逸 + 内核 LPE 全链，WebKit DFG JIT 类型混淆 CVE-2018-4233

置信度：high；替代解释：跨引擎迁移也可能反映追逐各引擎披露窗口与赏金的外部激励，而非纯方法论驱动；但 2016–2018 年五个独立引擎在同一利用框架下连续产出，支持方法论迁移解释，外部激励为竞争性解释。

证据：saelo-tl-01, saelo-tl-04, saelo-tl-05, saelo-tl-06, saelo-tl-07, r1-saelo-v8-turbofan-2018, sg-community-01, saelo-decisions-03

### 博文 + PoC 仓库 + 系统论文的配套输出

起点：2016 年起以个人博客 saelo.github.io 作为公开技术输出渠道；具备把个案研究文档化与工程化的习惯。

练习与反馈：每个研究产出配套博文、GitHub PoC/exploit 仓库与（部分）系统论文：CVE-2016-4622 配套 saelo.github.io 博文 + jscpwn 仓库 + Phrack《Attacking JavaScript Engines》；Pwn2Own 2018 配套 pwn2own2018 仓库 + cve-2018-4233 配套仓库；armpwn 以 'train/learn memory corruption' 训练仓库形式公开。；Phrack 审稿接受两篇；Lua 邮件列表回复作为上游反馈；GitHub 仓库公开供社区复用（pwn2own2018 约 760 stars）；博文与 Phrack 相互印证同一研究方向。

能力与结果：把个案漏洞提炼为可复现、可教学的通用方法，形成'可复现代码 + 文档化输出 + 系统论文'的标准化输出流程。；saelo.github.io 2016-09 至 2017-03 连续 4 篇博文（TypedArray.slice infoleak、Array.slice OOB、Lua load、Firefox cross-mmap overflow）；jscpwn PoC 仓库与 Phrack《Attacking JavaScript Engines》；pwn2own2018 全链仓库（stage0..stage5 + libspc）与 cve-2018-4233 配套仓库；Phrack #70 saelo 署名两篇（#3 与 #9）

置信度：high；替代解释：配套输出也可能是安全研究社区的普遍惯例而非个人特有；但 2016–2018 年多个独立产出中一致出现该模式，且 Phrack 接受两篇提供外部审稿信号，支持其作为可观察机制的判断。

证据：saelo-tl-02, saelo-tl-04, sg-self-02, saelo-tl-07, r1-pwn2own2018-readme-no-cve, sg-community-03, saelo-works-013

### 结构化训练与配套工具建设

起点：2014 年起以公开仓库形式固化练习与 exploit（cve-2014-0038 仓库），具备把训练材料与工具作为可复用产出的习惯。

练习与反馈：围绕漏洞研究构建配套工具与训练仓库：armpwn（README 自述 'train/learn memory corruption on the ARM platform'）、ida_scripts（IDA 逆向脚本集合）、dnsrebinder（DNS rebinding 网络原语）、pwn2own2018 libspc（XPC 协议重实现）。；GitHub 公开仓库供社区复用；pwn2own2018 仓库以 stage0..stage5 + libspc 结构化组织，工具与 exploit 阶段对应。

能力与结果：形成围绕漏洞研究的自建工具链与训练环境，降低新目标上的重复工程开销。；armpwn ARM 内存破坏训练仓库；ida_scripts 逆向脚本集合；dnsrebinder DNS rebinding 工具；pwn2own2018 libspc（XPC 协议重实现）

置信度：low；替代解释：工具建设（armpwn/ida_scripts）确实存在，但与具体 CVE 产出（尤其 V8 Turbofan CVE-2018-17463 为源代码审计发现）的直接因果无一手对应；该机制可能反映通用工程习惯而非专门驱动漏洞发现的机制，故 confidence 不高于 low。

证据：saelo-decisions-01, r1-github-profile-realname-handle, saelo-tl-07, r1-pwn2own2018-readme-no-cve

## 可迁移与不可迁移

- 可迁移：跨引擎/跨平台方法论迁移：把'内存破坏原语→信息泄露→任意读写→代码执行'链路抽象为通用流程，反复应用到不同引擎，不把能力限定在单一目标。
- 可迁移：博文 + PoC 仓库 + 系统论文的配套输出：每个研究产出配套可复现代码、博文与（部分）系统论文，把个案漏洞提炼为通用方法。
- 可迁移：上游社区反馈循环：先向官方邮件列表报告/讨论，再据回复整理为公开 writeup（如 Lua 邮件列表），形成披露—反馈—输出循环。
- 可迁移：把训练材料与配套工具作为可公开、可复用产出固化（armpwn 训练仓库、ida_scripts 逆向脚本集合）。
- 不可直接迁移：加入 Google Project Zero / Chrome V8 安全团队的组织归属线索无一手确认（GitHub bio 为空、Project Zero about 页 404），若成立则提供的稳定披露通道与上游协作属组织资源而非个人可迁移条件（saelo-decisions-05，lead_only）。
- 不可直接迁移：Pwn2Own 2018 参赛与同伴（Niklas Baumstark）组队细节无一手页面核验，仅 lead_only（sg-community-04）；竞赛平台本身是偶发性外部条件。
- 不可直接迁移：各浏览器引擎在 2016–2018 年的 JIT 优化 bug 集中披露窗口，属特定时期的外部条件，不可迁移。
- 不可直接迁移：GitHub bio location 'Zürich, Switzerland' 与组织 kitctf 暗示的地域/教育归属，属个人背景条件。

## 复核问题

- 字段 mechanisms[1].feedback：删除 '（pwn2own2018 约 760 stars）' 中的具体数字，改写为 'GitHub 仓库公开供社区复用（star 数未一手核实）' 或直接删除该括注；原措辞 'pwn2own2018 约 760 stars' 源自 verified_in_run=false 的 saelo-works-011 且不在 mechanisms[1].evidence_ids 内，不得保留 760 这一具体数字。
- 字段 stages[2].capability_change 与 mechanisms[0].alternative_explanation 中的 '偶发成果' 一词建议改写为 '非系统性的孤立产出'；该词虽不在 RR7 明确禁用列表，但与 '偶发事件' 同义族，建议统一按 RR7 改写方向处理为准确克制书面语。
- 字段 stages[1].evidence_ids 仍含 saelo-tl-02，其 source.published '2016-05' 已被 r1-phrack70-release-date 证伪；综合结论虽无法改写输入证据，且已在 tensions[4] 公开 #70 Release date 冲突，但建议在 stages[1] capability_change 或 tensions 中明确标注 'saelo-tl-02 的 source.published 字段无一手支撑，该条仅作为 CVE-2016-4622 内容证据而非时间锚'，避免读者误用 2016-05。

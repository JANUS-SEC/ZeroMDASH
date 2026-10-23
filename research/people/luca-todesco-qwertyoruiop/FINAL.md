# Luca Todesco (qwertyoruiop)：漏洞研究成长分析

- 擅长领域：iOS 与浏览器漏洞
- 独立复核：pass · 86/100

## 成长阶段

- **2012 · iOS 应用层起点**：以 iOS 平台 Objective-C 应用层项目（Craftplayer）起步，技术栈起点为应用层开发而非内核漏洞；建立公开仓库发布习惯。（置信度：high）
  - 证据：kpwn-2012-craftplayer
- **2015 · XNU/macOS 内核提权与多目标利用原语构建**：目标从应用层转向 macOS XNU 内核本地提权，建立单 CVE 堆溢出利用与 KASLR 绕过技术基线（vpwn，演示输出含 'broke out of kaslr'）；将 64-bit ROP 原语封装为可复用函数 jump/alloc/mem/ptr（phpmess），体现利用原语抽象化与工具化倾向；确立以可运行 PoC 公开披露漏洞、并以 README 形式发表利用演示的发布习惯（vpwn/tpwn/phpmess，其中 tpwn README 标注 'poc or gtfo' 为具体作品处短引文）；同期发布 NULLGuard 防御 kext 缓解 NULL 指针解引用类漏洞，形成攻击 PoC 与防御工具的双向产出。（置信度：high）
  - 证据：kpwn-2015-03-vpwn, kpwn-2015-08-tpwn, kpwn-2015-phpmess, lt-tl-001, lt-tl-002, dec-tpwn-osx-lpe-2015, dec-kpwn-multi-project-attack-defense-portfolio
- **2016 · 自主漏洞挖掘与利用链复现**：从利用已知漏洞转向自主挖掘（935csbypass，README 自述 'my own bug this time'，短引文），技术目标转向 iOS 代码签名绕过，采用 trampoline 方式在无 JIT 情形下脱离 ROP 加载任意代码（'get out of rop without JIT'，短引文）；fork Trident 复现 Pegasus/Trident iOS 内核利用链，建立对已公开高水平利用链的复盘学习习惯；尝试通用 XNU 利用工具包建设但未完成公开（xnuexp-toolkit，README 仅 'ETA: son'，作为未达成项据实记录而非成果）。（置信度：high）
  - 证据：kpwn-2016-935csbypass, kpwn-2016-xnuexp-toolkit, kpwn-2016-12-trident-fork
- **2016-12 至 2017-01 · iOS 10 越狱链与协作发布**：复杂度从单 CVE LPE 上升为内核漏洞利用与 KPP 绕过的完整越狱链（yalu102）；从单人工作转为与 Marco Grassi 协作（mach_portal + Yalu 于 2016-12-22 释放，yalu102 于 2017-01-26 释放）；面对 iPhone 7/A10 KPP 限制如实公开支持边界（iPhone 7 仅支持至 iOS 10.1.1）；公开发布中规避受版权保护的 IOKit headers 分发并要求 SHA1 校验以防第三方投毒；Project Zero（Ian Beer）于 2016-12 发布 mach_portal，qwertyoruiopz 与 Marco Grassi 对同一漏洞 CVE-2017-2370 独立发现与利用；Apple 于 2017-01-23 发布 iOS 10.2.1 修补 Yalu 所用漏洞，构成厂商对作品所依赖漏洞的事实性回应。（置信度：high）
  - 证据：kpwn-2017-yalu102, dec-mach-portal-yalu-2016-12-22, dec-yalu102-2017-01-26-collab-marcograssi, dec-yalu102-iphone7-kpp-1011-tradeoff, dec-yalu102-iokit-headers-copyright-stance, ext-01, ext-02, ext-04, r1-p0-mach-portal-2017-04, lt-tl-006, lt-tl-007
- **2017-12 至 2018 · 跨平台扩展与协作网络**：技术关注从 iOS 内核向 PlayStation 4 内核与 iOS 逆向工程资源整理扩展（fork PS4-5.05-Kernel-Exploit、维护 iOSRE 资源集）；LiberiOS（2017-12-25）将 Ian Beer（Google Project Zero）与 Jonathan Levin 纳入协作列名，扩展协作网络。（置信度：medium）
  - 证据：kpwn-2018-ps4-iosre, ext-03

## 主要成长机制

### 公开 PoC 与 README 演示的发布工程

起点：2012 年起以 iOS/Objective-C 应用层项目建立公开仓库发布习惯（Craftplayer）；具备 iOS 平台熟悉度基础。

练习与反馈：vpwn 以可运行演示输出公开（含 'broke out of kaslr'）；tpwn 以 0day 状态公开并标注 'poc or gtfo'（具体作品处短引文）；phpmess 封装 jump/alloc/mem/ptr 可复用原语并复用 'poc||gtfo' 标签；935csbypass 公开 cs_bypass.m 与 cs_tramp.s；yalu102 以 Beta 1–7 分批发布并附 SHA1 校验与下载源告警。；Apple 于 2017-01-23 发布 iOS 10.2.1 修补 Yalu 所用漏洞，构成厂商对作品所依赖漏洞的事实性回应（ext-04）；Wikipedia 权威二手条目记载 Yalu/yalu102 发布（ext-01/ext-02）；Trident fork 表明对已公开利用链的复盘学习。

能力与结果：将利用封装为可复现、可校验的公开制品的能力，以及对发布物供应链完整性（SHA1 校验、版权规避）的工程意识。；yalu102 Beta 1–7 + SHA1 校验 + IOKit headers 版权立场；NULLGuard 防御 kext 与攻击 PoC 并存；phpmess 跨目标可复用 ROP 原语（jump/alloc/mem/ptr）

置信度：high；替代解释：公开披露习惯可能受越狱社区发表规范驱动而非个人能力选择；'poc or gtfo' 为社区通用标签，非个人独创，故仅作为具体作品处短引文保留，不作为叙述类别名。

证据：kpwn-2012-craftplayer, kpwn-2015-03-vpwn, kpwn-2015-08-tpwn, kpwn-2015-phpmess, kpwn-2016-935csbypass, kpwn-2016-12-trident-fork, kpwn-2017-yalu102, ext-01, ext-02, ext-04, dec-yalu102-iokit-headers-copyright-stance, dec-kpwn-multi-project-attack-defense-portfolio, lt-tl-007

### 跨内核/跨目标研究迁移与资源整理

起点：2015 年建立 XNU/macOS 内核提权基线（vpwn/tpwn）。

练习与反馈：XNU 内核 LPE（vpwn/tpwn）→ PHP 解释器 UaF 利用并附 macOS rop 文件（phpmess，文件名 pm_rop_osx.php 与 pm_rop_findexec_osx.php）→ fork PS4-5.05-Kernel-Exploit（JavaScript）→ 维护 iOSRE 逆向工程资源集（Shell）；fork Trident 复现 Pegasus 利用链。；PS4 Orbis OS 为 FreeBSD 衍生，与 XNU（Mach/BSD 混合内核）在 BSD 派生组件上存在部分同源关系，使内核利用概念可在相关内核间部分迁移；iOSRE 作为知识资源输出形态。

能力与结果：跨相关内核/目标的研究注意力迁移与知识资源整理能力。；PS4-5.05-Kernel-Exploit fork；iOSRE 逆向工程资源集；phpmess 跨目标 rop 文件

置信度：low；替代解释：PS4/iOSRE fork 可能仅为关注追踪而非深度研究；跨平台利用能力迁移未由实际 PS4 利用作品证实，仅由 fork 行为推断研究注意力扩展。

证据：kpwn-2015-03-vpwn, kpwn-2015-08-tpwn, kpwn-2015-phpmess, kpwn-2018-ps4-iosre, kpwn-2016-12-trident-fork

### 从复盘复现到自主发现的漏洞研究路径

起点：2016-12 fork Trident 复现 Pegasus/Trident iOS 内核利用链，建立对已公开高水平利用链的复盘学习习惯。

练习与反馈：fork Trident 复现已公开高水平利用链（2016-12）；自主发现漏洞（935csbypass，README 自述 'my own bug this time'）；对 CVE-2017-2370（mach_voucher_extract_attr_recipe_trap 堆缓冲区溢出）独立发现与利用。；r1-p0-mach-portal-2017-04（Project Zero 官方博客，一手）将 qwertyoruiopz 命名为 CVE-2017-2370 独立发现/利用者之一，验证其自主发现能力而非纯集成；该一手来源同时加强 kpwn↔qwertyoruiopz 身份链。

能力与结果：从复盘他人利用链过渡到对同一漏洞独立发现与利用的能力。；935csbypass 自主 codesign bypass（'get out of rop without JIT'）；CVE-2017-2370 独立发现与利用（一手正文确认）；extra_recipe 整合 Ian Beer + Marco Grassi + 自身工作（lt-tl-005，inferred/lead_only，未由一手页面证实，列为线索）

置信度：medium；替代解释：该环节核心（自主发现 CVE-2017-2370）现有一手来源支撑（r1-p0-mach-portal-2017-04，Project Zero 官方博客）；此前的来源错配（lt-tl-004 将 mach_portal 误归于 Todesco 发布）已作废并纠正——mach_portal 实际由 Project Zero（Ian Beer）发布，qwertyoruiopz 与 Marco Grassi 为 CVE-2017-2370 独立发现/利用者。extra_recipe 整合关系仅由 lt-tl-005（inferred/lead_only，verified_in_run=false）支撑，仓库 404，未由一手页面证实，相关叙述降级为线索。

证据：kpwn-2016-12-trident-fork, kpwn-2016-935csbypass, r1-p0-mach-portal-2017-04, lt-tl-005

## 可迁移与不可迁移

- 可迁移：以可运行 PoC + README 演示形式公开披露漏洞，附演示输出而非仅文字描述。
- 可迁移：发布物附 SHA1 校验与下载源告警，规避受版权保护头文件分发，维护供应链完整性。
- 可迁移：攻击 PoC 与配套防御工具（如 NULLGuard kext）并行产出。
- 可迁移：fork 已公开高水平利用链进行复盘学习，作为自主发现的前置练习。
- 可迁移：面对新版本内核防护（如 KPP）如实公开支持边界，而非隐瞒缺陷。
- 不可直接迁移：2015-2017 iOS 越狱与 XNU 内核研究的窗口期外部条件。
- 不可直接迁移：与 Marco Grassi、Ian Beer（Project Zero）的协作网络及联名作品机会。
- 不可直接迁移：iOS 10 KPP/A10 新防护的特定技术约束与对应绕过研究时机。
- 不可直接迁移：kpwn 账户下已积累的 iOS/XNU 工具集与社区声誉。
- 不可直接迁移：越狱社区对以可运行 PoC 公开披露漏洞这一规范的接纳与反馈回路。

## 复核问题

- mechanisms[2].evidence_ids：将 lt-tl-005（verified_in_run=false，inferred/lead_only，仓库 404）从 evidence_ids 列表移除；extra_recipe 整合关系仅保留在 observed_outcomes 中作为线索标注（已标注为 inferred/lead_only），或在 alternative_explanation 中说明其未由一手页面证实。该机制 confidence 维持 medium 不变，因核心环节 CVE-2017-2370 独立发现已有 r1-p0-mach-portal-2017-04 一手来源支撑，加上 kpwn-2016-12-trident-fork 与 kpwn-2016-935csbypass，满足至少有实际抓取来源支撑的要求。
- stages[2]（2016 自主漏洞挖掘）或 stages[1]/stages[2] 边界：在正文中说明 935csbypass 归入 2016 阶段的依据（works 维度 kpwn-2016-935csbypass 标注 2016），并注明同源仓库在 timeline 维度（lt-tl-003）标注为 2015，差异源于无精确发布日期、仅以 updated 日期推断的精度限制；或在 tensions 中已记录的基础上，在 stages[2] capability_change 文本中加一句说明该日期不确定性，避免正文与 tensions 给出不同归因而未解释。

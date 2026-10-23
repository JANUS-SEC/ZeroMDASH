# Linus Henze：漏洞研究成长分析

- 擅长领域：iOS/macOS 漏洞
- 独立复核：pass · 83/100

## 成长阶段

- **约 2016 · SIP/Rootless 绕过的早期公开输出起点**：以单一 SIP/kext 工具(anyKextLoader)为可核验的公开输出起点,工具以可复用程序形态发布,可在不重启的前提下禁用 System Integrity Protection;其后公开项目的目标复杂度按可观察序列上升,表明早期即建立公开工具发布习惯,而非后期才转向公开。（置信度：medium）
  - 证据：lh-dec-001, lh-tl-2016-anykextloader, lh-works-07, lh-conv-003
- **2018 · CTF 训练与浏览器 JIT 侧效应建模利用**：以 35C3 CTF writeup 记录可重复练习与公开发表习惯,同期产出 WebKit 正则表达式 JIT 利用 PoC(目标 iOS 12.0–12.1.1、macOS 10.14.0–10.14.2,以 CVE-2018-4233 为模板)。利用以 Samuel Groß 的公开利用为模板并直接复用其 Int64 库,体现起步阶段即选择浏览器 JIT 侧效应建模类缺陷、技术栈明确依赖同行公开成果;README 自述 TODO 'do a proper writeup' 未补,体现以可工作 PoC 优先、文档化滞后的发布习惯。GitHub 仓库 API 元数据显示该仓库 created_at=2018-12-06,2020-10-04 仅为最后推送时间,该作品内容属 2018 上下文而非 2020-2021 阶段首次发布。（置信度：medium）
  - 证据：lh-tl-2018-35c3ctf, lh-dec-002, lh-works-01, lh-conv-004, lh-r2-001
- **2019 · Keychain 组合利用与披露条件驱动决策**：研究主题由系统级 SIP 绕过转向受保护子系统 Keychain 的组合利用(daemon + client 注入 + Security Framework patch),目标版本 macOS ≤ 10.14.3,对应 CVE-2019-8526。OBTS v2 议程页称其因 macOS 缺少 bug bounty 程序而拒绝向 Apple 上报 KeySteal 细节,并在演讲中首次公布完整 exploit 细节与代码。该披露条件驱动决策的行为先于 KeySteal 即有可核验铺垫(2018 WebKit 漏洞公开披露并附带警示),形成可重复观察的公开披露偏好。（置信度：medium）
  - 证据：lh-works-02, lh-works-03, lh-tl-2019-keysteal, lh-dec-003, lh-conv-001, lh-conv-004, lh-conv-005, lh-conv-006
- **2019-2021 · checkm8 完整越狱链与工具横向扩展**：研究目标由单漏洞 PoC 升级为基于 checkm8 的完整开源越狱工具链(bootrom exploit → iBoot patch → kernel bootstrap → 用户态包管理),官方支持 iOS 13–13.5.1 设备,并复用 axi0mX 的 checkm8、fork 其 ipwndfu,体现沿用与扩展既有公开成果的工作方式。同期 Unrootless-Kext 与 WebKit-RegEx-Exploit 仓库均有更新记录(WebKit-RegEx-Exploit 的 2020-10-04 为最后推送,内容仍为 2018 上下文),研究主题由 macOS 内核绕过横向扩展至 WebKit 浏览器引擎与 iOS 设备工具链。README 写入'真机改动前先在虚拟设备测试'的回归纪律,并暴露 remount patch 第三方代码归属未决的工程问题。（置信度：medium）
  - 证据：lh-works-04, lh-works-06, lh-works-07, lh-dec-004, lh-dec-005, lh-tl-2020-multi-tool-expansion, lh-tl-2021-fugu, lh-r2-001
- **2021-2023 · untethered/PAC 越狱递进与项目边界显式收尾**：由 checkm8 系链式越狱推进至 untethered 越狱、面向 A12+ PAC 设备的 Fugu14(含 untether、kernel exploit、kernel PAC bypass、PPL bypass、dyld SLOP、TCP shell、libkrw、trustcache 自动加载),并公开 CVE-2021-30740/30768/30769/30770/30773;自述 kernel exploit 'extremely reliable, will never trigger a kernel panic',将可靠性纳入研究目标。GitHub 仓库 API 元数据显示 Fugu14 created_at=2021-10-24、pushed_at/最后更新=2022-06-12;其 description 字段逐字为 'Fugu14 is an untethered iOS 14.3-14.5.1 jailbreak'(非'非越狱')。随后 pinauten/Fugu15(created_at=2022-10-31、pushed_at=2023-09-24、归档 2023-10-03)以 FAQ 形式公开声明项目边界并归档仓库,构成明确、可核验的项目收尾动作,而非无公开声明的逐步停止维护。SwiftXPC(最后更新 2023-03-18)与 Fugu15 归档在时间上相邻,公开输出重心向 macOS/Swift 方向的转移为推断。GitHub 仓库页仅记录最后更新时间,创建/最后推送/归档为三类不同里程碑,不应混为首次发布日期。（置信度：medium）
  - 证据：lh-works-05, lh-works-06, lh-dec-006, lh-dec-008, lh-dec-009, lh-dec-010, lh-tl-2022-fugu14, lh-tl-2023-swiftxpc, lh-r1-001, lh-r2-002, lh-r2-003

## 主要成长机制

### 复用与整合同行公开原语的利用链构建

起点：早期 WebKit-RegEx-Exploit 阶段即以 Samuel Groß 的 CVE-2018-4233 利用为模板并直接复用其 Int64 库;GitHub 组织挂靠 allesctf/pinauten,处于可获取公开工具与同行的 CTF 圈层。

练习与反馈：在多个项目中反复沿用与扩展既有公开成果:WebKit-RegEx-Exploit 复用 Samuel Groß 的利用与库;Fugu 在 axi0mX 公开的 checkm8 之上构建并 fork 其 ipwndfu;Fugu14 整合 Samuel Groß 的 SLOP technique 与 Int64 library、Siguza 的 libkrw;Fugu15 组件句为 'It contains a code-signing bypass, kernel exploit, kernel PAC bypass and PPL bypass',与 Fugu14 README 组件句 'including an untether (persistence), kernel exploit, kernel PAC bypass and PPL bypass' 重叠,PPL bypass 在两项目中均为组件。；同伴公开原语使完整利用链可在不重复实现既有模块的前提下交付;README 中以 TODO/致谢形式记录外部依赖(如 Keysteal TODO、Fugu14 致谢 Samuel Groß 与 Siguza),构成可核验的方法输入痕迹。

能力与结果：形成以'整合既有 bootrom/内核/PAC 原语 + 自研上层链'为特征的组合利用能力,可在新 iOS 版本区间复用既有组件而非从零复现。；Fugu 作为首个基于 checkm8 的开源越狱工具链；Fugu14 含 untether + kernel exploit + kernel PAC bypass + PPL bypass 并公开 5 个 CVE；Fugu15 组件覆盖 code-signing bypass、kernel exploit、kernel PAC bypass、PPL bypass

置信度：high；替代解释：该模式在 iOS/macOS 越狱社区属常见工程实践,checkm8、SLOP、libkrw 等公开原语本就被设计为可复用;Henze 的区别可能在于其持续公开发布而非工具私有化,以及跨多个 iOS 版本区间的重复整合,而非复用行为本身。

证据：lh-works-01, lh-works-04, lh-works-05, linus-community-02, lh-dec-004, lh-r1-001

### CTF 解题与可复现 PoC 优先的发布习惯

起点：挂靠 allesctf 组织,处于德国 CTF 圈层;35C3 CTF 期间产出 writeup。

练习与反馈：以 CTF 解题与 writeup 作为可重复练习(35C3_Writeups);公开作品以可工作 PoC/工具优先发布,文档化滞后(WebKit-RegEx-Exploit TODO 'do a proper writeup'、Keysteal TODO 'Add a link to my talk')。研究目标同时覆盖 iOS 与 macOS 双平台,且在 Fugu14 README 写入'真机改动前先在虚拟设备测试'的回归纪律。；社区采纳规模(Fugu14 约 1.4k stars、312 forks、140 open issues、7 pull requests)提供外部反馈入口;issue/PR 计数表明存在外部反馈渠道,但 issue/PR 正文未逐条抓取,无法证明反馈直接驱动了能力提升。

能力与结果：形成以'可复现工具 + 会议演讲'为输出形式的发布节奏,将研究成果转化为可复现代码与演讲材料并公开发布。；35C3_Writeups 作为 CTF 解题与公开复盘痕迹；Keysteal README 计划 OBTS 演讲(议程页已确认 KeySteal 议题摘要)；Fugu14 以回归纪律形式写入开发注意事项

置信度：medium；替代解释：TODO 未闭合也可能反映发布精力受限或优先级安排,而非刻意的复盘习惯;star/fork 量是社区触达规模的代理指标,不直接证明反馈回路驱动了能力变化。

证据：lh-tl-2018-35c3ctf, lh-dec-002, lh-works-01, lh-works-03, lh-works-06, lh-conv-006, linus-community-04

### 以公开披露影响厂商激励结构的决策倾向

起点：OBTS v2 议程页称 Henze 为来自德国的独立安全研究员,通过个人网站 pinauten.de 与 Twitter 发布漏洞发现,个人热情在于争取 Apple 设立 macOS bug bounty 程序;2018 年 WebKit 漏洞已在 Twitter 公开披露并附带警示。

练习与反馈：在厂商激励结构缺失或不符合其披露条件时选择公开披露而非私下上报:2018 WebKit 漏洞以 'Want a free Safari 0day? Please don't do evil stuff with this.' 口吻公开;2019 因 macOS 缺少 bug bounty 程序拒绝向 Apple 上报 KeySteal,并在 OBTS 演讲中首次公布完整 exploit 细节与代码,演讲后在线发布完整 exploit 代码。；OBTS 议程页与议题摘要是其公开披露行为与动机的核验来源,但均为会议主办方撰写的二手简介,虽引用其自述措辞,并非本人长篇自述一手材料。其本人自述站点 linushenze.com 与 blog.linushenze.com 多次抓取均 ECONNREFUSED,动机说明的一手来源不可得。

能力与结果：形成以披露条件而非单纯技术猎取驱动的决策倾向,其与厂商激励结构变化的因果尚待本人长篇自述与厂商侧材料核验。；2018 WebKit 漏洞公开发布并附带警示；2019 KeySteal 拒绝上报 Apple 并在 OBTS 公开完整 exploit；完整 exploit 代码在 OBTS 演讲后在线发布

置信度：low；替代解释：公开披露 KeySteal 与 Apple 后续设立/调整 macOS bug bounty 之间是否存在可核验的因果关系尚未证实;OBTS v2 单一二手议程页不足以支撑'促成厂商激励结构变化'的确定性表述,亦不排除公开披露本身即为其研究输出习惯而非以改变厂商激励结构为目标的博弈策略。

证据：lh-conv-001, lh-conv-002, lh-conv-004, lh-conv-005, lh-conv-006, lh-works-02, lh-works-03

### 按 Apple 缓解层级递进的重定向练习

起点：约 2016 以 SIP/Rootless 绕过(anyKextLoader、Unrootless-Kext)为公开输出起点;其后 Apple 引入 Pointer Authentication Codes(A12+)与 Page-based Permission Layer 等缓解。

练习与反馈：按 Apple 缓解层级递进研究对象:Rootless/SIP(anyKextLoader、Unrootless-Kext)→ Keychain 子系统(Keysteal)→ checkm8 引导阶段(Fugu)→ PAC + PPL bypass(Fugu14)→ Fugu15 组件(code-signing bypass、kernel exploit、kernel PAC bypass、PPL bypass)。README 自述 kernel exploit 'extremely reliable, will never trigger a kernel panic',将可靠性纳入研究目标。；新 iOS/macOS 版本与新增缓解(PAC、PPL)构成研究对象的外部条件;Fugu14 README 暴露 remount patch 第三方代码归属未决的工程问题,Fugu15 以 FAQ 显式声明不再扩展支持、仓库归档收尾,均构成对项目范围与持续投入的公开决策。

能力与结果：形成针对 Apple 缓解逐层递进的研究与工程能力,可在新版本区间以既有组件重叠为基础叠加新对抗项。；anyKextLoader/Unrootless-Kext 覆盖 SIP/Rootless；Keysteal 转向 Keychain 子系统组合利用；Fugu14 含 PAC bypass 与 PPL bypass 并自述 kernel exploit 高可靠性；Fugu15 组件重叠 code-signing/kernel PAC/PPL bypass 并以 FAQ + 归档收尾

置信度：medium；替代解释：缓解层级递进是 Apple 越狱研究社区的普遍路径,研究者通常被迫跟随厂商缓解更新调整研究对象,而非 Henze 独有;其区别可能在于跨 iOS/macOS 双平台与跨多缓解层级的持续公开输出,而非递进行为本身。

证据：lh-works-07, lh-works-02, lh-works-04, lh-works-05, lh-dec-001, lh-dec-006, lh-dec-008, lh-dec-010, lh-r1-001

## 可迁移与不可迁移

- 可迁移：在构建完整利用链时复用与扩展同行公开原语(checkm8、SLOP、Int64 library、libkrw),并在 README 中以致谢/TODO 形式记录外部依赖,使链路可被社区复现与审视。
- 可迁移：以 CTF 解题与 writeup 作为可重复练习输入,并将研究成果转化为可工作 PoC/工具与会议演讲材料并行公开输出。
- 可迁移：在公开 README 中写入'真机改动前先在虚拟设备测试'的回归纪律,作为公开工具发布前的可核验工程约束。
- 可迁移：按厂商缓解层级(SIP/Rootless → Keychain → bootrom → PAC/PPL)递进研究对象,使既有组件可在新版本区间复用并叠加新对抗项。
- 可迁移：以 FAQ 形式公开声明项目边界(不扩展支持、不维护、不提供官方支持),配合仓库归档,构成明确、可核验的项目收尾动作,使收尾决策对社区可见。
- 不可直接迁移：约 2016(15 岁时)即发布 SIP 绕过构成可核验早期里程碑,该年龄/时间节点的早期产出与个人条件不可迁移,OBTS v2 简介反推年份约 2016,精确日期未知。
- 不可直接迁移：GitHub 组织挂靠 allesctf/pinauten 与德国 CTF 圈层提供的同伴网络与公开原语获取条件,属特定社群资源,不以同样形式可迁移至缺乏该圈层的研究者。
- 不可直接迁移：OBTS v2 议程页作为二手简介引用其自述措辞、KeySteal 议题摘要确认其演讲事实,属特定会议窗口与议题被采纳的结果,不可迁移为通用披露渠道。
- 不可直接迁移：linushenze.com 与 blog.linushenze.com 本人自述站点多次 ECONNREFUSED,其长篇自述一手来源不可得;该资料缺口使动机与成长机制的本人陈述不可核验,综合只能依赖 GitHub 一手仓库与 OBTS v2 二手议程页。
- 不可直接迁移：Fugu14 remount patch 的第三方代码归属未决及多来源代码整合范围无来源,该工具链并非完全自研,其整合边界不可迁移为个人独立能力证据。
- 不可直接迁移：GitHub 仓库页/列表页仅显示最后更新时间、不显示创建或首次发布日期,各 evidence 的 published 字段多为上界近似;精确发布日期不可迁移为时间线锚点,只能依托 API 元数据的 created_at/pushed_at 区分。

## 复核问题

- 将 mechanisms[2].name 由'以公开披露影响厂商激励结构的决策倾向'改为'以披露条件驱动而非私下上报的决策倾向', 删除名称中的'影响厂商激励结构'因果方向表述, 使名称与 confidence=low、intermediate_capability 的概率表述及 open_questions 中'因果关系尚待核验'的克制程度一致; 机制正文内容无需改动。
- 在 mechanisms[1].observed_outcomes 中将'Fugu14 以回归纪律形式写入开发注意事项'与 stars/forks 反馈入口的关系明示为'stars/forks 仅作社区触达规模代理, 不构成反馈驱动能力提升的证据', 避免把触达规模指标与反馈驱动结果在同一 observed_outcomes 中并列表述。
- 在 biases 或 non_transferable_conditions 中明示幸存者偏差: 当前机制与阶段结论以 GitHub 上仍可见、已 archived 的 popular 仓库为样本, 未抓取的 6 个非 popular 仓库、已删除或未公开项目无法进入样本, 可见成功项目代表性可能高估; 不必补抓不可考的生平, 仅需将范围限制写入叙述。
- 在 biases 中单列'OBTS v2 单一二手议程页对多阶段/多机制的过度支撑', 明示 lh-conv-001..006 与 M2 同源于一个二手议程页, 该单源同时支撑 stages[0]/stages[1]/stages[2] 的反推与铺垫, 单源失效的连带影响范围; 无需新增 open_questions(已存在对应条目)。

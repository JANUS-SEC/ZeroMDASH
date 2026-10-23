# Alex Plaskett：漏洞研究成长分析

- 擅长领域：Linux 内核漏洞
- 独立复核：pass · 84/100

## 成长阶段

- **2011-2014 · 移动平台应用与 SoC 方向起步**：2011 年起以 Windows Phone 7 平台应用安全为首个公开研究方向，议题在 Microsoft BlueHat V11 行政简报与 44CON、T2、DeepSec 等会场复用；2014 年在同一平台族内向应用层与移动 SoC（Qualcomm）方向延伸，与 Nick Walker 形成首个可核验的稳定合著关系，议题与白皮书成对产出。同期仓库内存在 BlackBerry 10 Security 白皮书文件 mwri_blackberry-10-security_2013-06-03.pdf；该文件未在 README 编号引用中出现，是否曾公开发表未经核验。（置信度：high）
  - 证据：ap-pub-2011-wp7, ap-pub-2014-wp8-qcom, timeline-2011-bluehat-wp7, timeline-2013-bb10-whitepaper, timeline-2014-wp8-syscan, ap-dec-01, ap-dec-02, ap-community-01
- **2016 · QNX 微内核/嵌入式转型与首次工具建设**：研究目标由移动平台转向嵌入式 RTOS（QNX 微内核/BlackBerry 10），与 Georgi Geshev 形成长期合著关系；白皮书与多会议演讲于 2016-03 发表，QNXSecurity 工具仓库同期公开。QNXSecurity 仓库（当前仓库状态可见）含 FWAnalysis、IPCFuzz、PPSFuzz、MsgFuzz、SyscallFuzz 等自研模糊测试与分析脚本，为研究过程的配套可复用制品。当前仓库状态（169 stars、37 forks）为 GitHub 仓库元数据，非 2016 年发布时点的社区反馈记录。（置信度：high）
  - 证据：ap-pub-2016-qnx, ap-dec-03, ap-dec-09, ap-community-02, ap-community-03, timeline-2016-qnx-whitepaper-troopers, ap-tools-github-portfolio
- **2017-2018 · Apple 内核模糊测试与 Pwn2Own 利用研究**：研究方法从静态评估与逆向转向内核模糊测试，目标扩展到桌面类 Unix 内核（macOS XNU），同期 GitHub 账号 fork darwin-xnu 源码镜像。2018 年集中产出 Pwn2Own 类竞赛议题，参与 Apple Safari WebAssembly 段漏洞利用研究与 Huawei Mate 9 Pro 移动设备利用研究，输出形态扩展到竞赛利用链与事后 writeup；合著者含 Fabian Beterke、Georgi Geshev、James Louerio。（置信度：medium）
  - 证据：ap-pub-2017-macos-fuzz, ap-pub-2018-pwn2own, ap-dec-04, ap-dec-05, ap-community-04, ap-community-05, timeline-2017-macos-kernel-fuzzing, timeline-2018-safari-wasm-pwn2own, timeline-2018-huawei-mate-pwn2own
- **2020-2021 · 静态分析方法引入与 Windows 内核利用研究**：2020 年在发现 CVE-2020-9967（Apple 6LowPAN）时引入 CodeQL 变体分析作为方法工具，依据本人博客正文，灵感来自 Kevin Backhouse 在 XNU 远程漏洞上的工作；CodeQL taint tracking query 将既有 query 的 source 改为 m_mtod、sink 为 builtin___memcpy_chk/bcopy，约返回 15 个结果，其一即 6LowPAN 漏洞。该方法论转型未经 Kevin Backhouse 本人独立确认。2021 年研究目标回到 Windows 10 内核，于 POC2021 发表 NTFS 与 WNF 组件利用研究，单人署名。2019 年无公开发表证据，构成时间线断点。（置信度：high）
  - 证据：ap-pub-2020-codeql, ap-pub-2021-ntfs-wnf, ap-dec-06, ap-dec-07, ap-community-06, ap-community-07, timeline-2020-cve-2020-9967-codeql, timeline-2021-poc-windows10-kernel, ap-tgt-2020-cve2020-9967-backhouse-codeql
- **2022-2023 · 重返嵌入式/IoT 方向与外设持久化**：在 Windows 内核方向之外重新进入嵌入式/IoT 方向，参与 Pwn2Own 2021 三台嵌入式设备远程利用研究（NCC Con Europe 2022 复盘），合著者含 Cedric Halbronn、Aaron Adams、Catalin Visinescu；同年与 Cedric Halbronn 合著打印机固件持久化研究（Toner Deaf，Hexacon 2022）。2023 年与 McCaulay Hudson 合著 SOHO 路由/家庭办公设备方向研究（HITB Amsterdam）。Publications 仓库 last-updated 2023-05-10，为可核验时间线终点；2024 年后是否继续产出未见一手证据。赛事官方逐场胜负、名次、奖金与厂商致谢未取得一手来源，相关表述限于参与研究。（置信度：medium）
  - 证据：ap-pub-2022-embedded-printer, ap-pub-2023-soho, ap-dec-08, ap-dec-10, ap-community-08, timeline-2022-ncccon-pwn2own-embedded, timeline-2022-hexacon-toner-deaf, timeline-2023-hitb-soho-pwn2own, ap-tgt-2026-pwn2own-2021-not-tokyo-overview

## 主要成长机制

### 跨平台转型中为目标平台建立评估工具的限定性习惯

起点：2011-2014 年以移动平台应用安全为公开研究方向，研究产出以会议演讲与白皮书为主，未见配套自建工具。

练习与反馈：在可核验的跨平台转型中，QNX 阶段（2016）有配套自建工具集 QNXSecurity（FWAnalysis、IPCFuzz、PPSFuzz、MsgFuzz、SyscallFuzz 等）；macOS 阶段 fork darwin-xnu 源码镜像作为研究支撑；其余转型（Windows、嵌入式/IoT）未观察到配套工具建设的一手证据；CodeQL 为第三方静态分析平台的采用，非自建工具集。；QNXSecurity 仓库当前可见状态（169 stars、37 forks）为 GitHub 仓库元数据，非 2016 年发布时点的社区反馈记录，来源为仓库元数据而非一手采用记录，不能据此推断发布时点的社区反馈强度。

能力与结果：为特定平台自建可复用工具集（QNX 阶段）与 fork 目标系统源码镜像（macOS 阶段）作为研究支撑的行为习惯，发布为可复用制品。；QNX 阶段公开 QNXSecurity 工具仓库（当前仓库状态可见）、QNX Security Architecture 白皮书与多会议演讲；macOS 阶段 fork darwin-xnu 源码镜像支撑内核模糊测试研究

置信度：medium；替代解释：QNX 阶段配套工具建设为单一可核验实例；macOS 阶段仅为 fork 源码镜像，Windows 与嵌入式/IoT 阶段无配套工具证据。证据基础为合著与多会议复用的行为性代理信号推断，conversations 维度 items 为空、external 维度第三方评价无一手文本，不能据此普遍化为每次转型均同步建设评估工具。

证据：ap-pub-2016-qnx, ap-dec-09, ap-community-03, ap-tools-github-portfolio, ap-pub-2017-macos-fuzz, timeline-2016-qnx-whitepaper-troopers

### 同一议题经多会场复用的发表习惯

起点：2011 年 Windows Phone 7 议题已在 Microsoft BlueHat V11、44CON、T2、DeepSec 等会场复用，建立多会场发表习惯。

练习与反馈：同一议题经不同会场复用：2016 年 QNX 议题在 Confidence、Troopers、BSides NYC 复用；2017 年 macOS 内核模糊测试在 Warcon、44CON、DeepSec 复用；2018 年 Huawei 议题在 Snoopcon、Hacktivity、Warcon 复用。；多会场复用为可核验事实；各会场演讲正文未抓取，仅证明复用事实，不证明各次复用伴随内容修订。

能力与结果：将单点研究整理为可经多会场复用的会议材料，发布为可复用制品。；2011 Windows Phone 7 议题在 4 个会场复用；2016 QNX 议题在 3 个会场复用并配套白皮书；2017 macOS 内核模糊测试在 3 个会场复用；2018 Huawei 议题在 3 个会场复用

置信度：medium；替代解释：多会场复用可由会议征稿周期、议题接受度与作者主动投稿习惯共同解释，并非必然反映内容迭代。各会场演讲正文未取得，复用是否伴随内容修订属资料缺口，本机制仅证明复用事实。

证据：ap-pub-2011-wp7, ap-pub-2016-qnx, ap-pub-2017-macos-fuzz, ap-pub-2018-pwn2own, ap-dec-01, ap-dec-03, ap-dec-04, ap-community-01, ap-community-02, ap-community-04, ap-community-05

### 合著网络随议题演化重组

起点：2014 年与 Nick Walker 形成首个可核验的稳定合著关系（Windows Phone 8/Qualcomm）。

练习与反馈：合著搭档随议题演化重组：2016 年 QNX 与 Georgi Geshev；2017-2018 年 macOS/Safari 与 James Louerio、Fabian Beterke、Georgi Geshev；2021 年起发表载体前缀由 mwri- 转为 research.nccgroup.com（依据 ap-community-07，status=inferred），雇主迁移时点与性质未经一手证实，该变化与同伴网络更新的因果关系为推断；2022-2023 年嵌入式/IoT 与 Cedric Halbronn、Aaron Adams、Catalin Visinescu、McCaulay Hudson。搭档随议题演化重组，而非单人独立署名。；Pwn2Own 竞赛场景在结构上提供高强度协作反馈的可能，但同伴直接反馈无一手引语，反馈是否实际发生未经核验。合著者身份、机构与对当事人的评价均未核验。2021 年起发表载体前缀变化与同伴网络更新的因果关系为推断。

能力与结果：按议题与平台重组协作网络，将既有白皮书与会议演讲产出模式迁移到新议题方向。；2014 Nick Walker 合著（Windows Phone 8/Qualcomm）；2016 Georgi Geshev 合著（QNX）；2017-2018 James Louerio、Fabian Beterke、Georgi Geshev 合著（macOS/Safari）；2022-2023 Cedric Halbronn、Aaron Adams、Catalin Visinescu、McCaulay Hudson 合著（嵌入式/IoT）

置信度：medium；替代解释：合著网络重组可由同机构同事关系、赛事组队需求与议题平台匹配共同解释，与具体同机构同事（如 Geshev、Halbronn）的协作关系本身不可迁移。conversations 维度 items 为空，未取得第一人称叙述，合著网络重组的动机与反馈机制为行为性代理信号推断。

证据：ap-pub-2014-wp8-qcom, ap-pub-2016-qnx, ap-pub-2017-macos-fuzz, ap-pub-2018-pwn2own, ap-pub-2022-embedded-printer, ap-pub-2023-soho, ap-community-02, ap-community-04, ap-community-05, ap-community-07, ap-community-08, ap-dec-02, ap-dec-03, ap-dec-05, ap-dec-08, ap-dec-10

### 方法论向特定研究者学习并引入静态分析

起点：2017-2018 年研究方法以内核模糊测试与利用构造为主，未见静态分析方法论的公开标注。

练习与反馈：2020 年在发现 CVE-2020-9967（Apple 6LowPAN）时引入 CodeQL 变体分析，依据本人博客正文，灵感来自 Kevin Backhouse 在 XNU 远程漏洞上的工作；采用 CodeQL taint tracking query，将既有 query 的 source 改为 m_mtod、sink 为 builtin___memcpy_chk/bcopy（因 XNU 大量使用 bcopy，编译为 builtin___memmove_chk），调整后约返回 15 个结果，其一即 6LowPAN 漏洞。；灵感来源由本人博客自述（ap-tgt-2020-cve2020-9967-backhouse-codeql 一手正文），未经 Kevin Backhouse 本人独立确认。该方法论转型为可追溯的向特定研究者学习的公开记录，非当事人独立陈述。

能力与结果：在 fuzzing 之外引入语义级静态分析（CodeQL）作为漏洞发现手段，目标转向网络协议栈代码，并产出可编号 CVE。；2020 年 CVE-2020-9967（Apple 6LowPAN）研究引入 CodeQL 变体分析；研究方法从动态为主转向动静结合

置信度：high；替代解释：CodeQL 引入为单一可核验实例（2020 年 CVE-2020-9967），其后是否在 2021-2023 年的 Windows 内核与嵌入式研究中持续采用 CodeQL 未见一手正文核验。灵感来源为本人自述，未取得 Kevin Backhouse 本人确认。

证据：ap-pub-2020-codeql, ap-dec-06, ap-community-06, timeline-2020-cve-2020-9967-codeql, ap-tgt-2020-cve2020-9967-backhouse-codeql

## 可迁移与不可迁移

- 可迁移：将单点研究整理为可经多会场复用的会议材料，并以白皮书与会议演讲配套产出。
- 可迁移：在进入新领域时降低重复建设评估工具的投入，沿用既有白皮书与会议演讲产出形态在新领域完成迁移；该习惯不依赖具体同机构同事关系。
- 可迁移：为目标平台 fork 源码镜像或采用第三方静态分析平台（CodeQL）作为研究支撑，区别于自建工具集。
- 可迁移：以可索引 CVE 编号命名研究产出，并就单点 CVE 编写复盘与汇编材料。
- 不可直接迁移：与具体同机构同事（如 Georgi Geshev、Cedric Halbronn）的协作关系本身不可迁移；合著网络重组受同机构同事关系与赛事组队需求约束。
- 不可直接迁移：QNXSecurity 自建工具集的发布依托 2016 年 QNX 微内核研究窗口与目标平台可访问性，非可普遍复用的条件。
- 不可直接迁移：Pwn2Own 竞赛参与及赛后 writeup 复盘依托赛事报名、组队与设备采购条件，非个人可独立迁移的练习。
- 不可直接迁移：research.nccgroup.com 发表载体与 NCC Group 机构关联（含 NCC Con Europe 内部会议）为依托具体雇主的发表条件，不可迁移。
- 不可直接迁移：CodeQL 变体分析的灵感来源（Kevin Backhouse 工作）为特定时间窗口与特定研究者的可追溯影响，非可普遍复制的方法论起点。

## 复核问题

- mechanism 0：明确 validation_tests 中"repeated"的判定边界。当前 validation_tests=["repeated", "distinctive"] 与同字段 alternative_explanation"QNX 阶段配套工具建设为单一可核验实例"存在张力。应在 repeated_practice 或 alternative_explanation 中明确：若"建立评估工具"包含 fork 目标系统源码镜像，则 QNX 自建工具集与 macOS fork darwin-xnu 为两个实例，alternative_explanation 中"单一"应改为"两个"或区分"自建工具集"(仅 QNX 一个) 与"为目标平台建立研究支撑"(QNX 自建 + macOS fork)；若"建立评估工具"仅指自建工具集，则 validation_tests 的"repeated"应删除或调整为与单一实例一致的标注。原措辞：validation_tests=["repeated", "distinctive"] 与 alternative_explanation"QNX 阶段配套工具建设为单一可核验实例"。改写方向：统一判定边界，消除验证标注与证据基础的内部矛盾。
- mechanism 2：在 repeated_practice 或 alternative_explanation 中标注 2020-2021 单人署名阶段与"合著网络随议题演化重组"机制的张力。当前 observed_outcomes 跳过 2020-2021 阶段 (CVE-2020-9967 与 POC2021 均单人署名)，未说明该阶段合著网络暂停对机制连续性的影响。原措辞：observed_outcomes 列出 2014/2016/2017-2018/2022-2023 四个合著阶段，无 2020-2021 条目。改写方向：在 observed_outcomes 补充 2020-2021 单人署名阶段，或在 alternative_explanation 说明合著网络在该阶段暂停、机制非全程连续。

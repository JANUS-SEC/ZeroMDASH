# 未通过独立复核

已达到最大修订次数 4；本文件是审计草稿，不得进入跨人物比较。

# Marco Grassi：漏洞研究成长分析

- 擅长领域：Android/iOS 与利用链
- 独立复核：revise · 74/100

## 成长阶段

- **2016-01 至 2016-11 · 公开漏洞披露节奏的建立与多目标覆盖**：在 11 个月窗口内连续发布十余篇带日期与多数带 CVE 编号的 writeup，研究目标从单一内核信息泄漏扩展到 iOS 内核竞态、iOS 沙箱逃逸、OS X 内核空指针、Apple CoreGraphics、Qualcomm MSM 内核、Amazon Fire Phone 内核及多种解析器；形成按时间可排列、以完整漏洞对象为单位的公开产出习惯。（置信度：high）
  - 证据：MG-RR4-02, MG-RR4-01
- **2016 至 2019 · Rust 逆向与固件分析工具建设的持续投入**：在 GitHub 公开维护 4 个 Rust 工具仓库，覆盖 PartialZip 实现、iOS 64 位 kernelcache 解密解压与 KPP 提取、固件基址搜索、RouterOS 备份加解密与打包解包；其中 rust-kernelcache-extractor 累计 305 次 commit、44 个 star、7 个 fork。研究产出从单点漏洞扩展到可复用的逆向工具链。（置信度：high）
  - 证据：MG-RR4-03, MG-RR4-04, MG-RR4-01

## 主要成长机制

### 公开 writeup 披露的反复练习

起点：持有个人博客 marcograss.github.io（自述 'Personal blog with some sparse posts about Computer Security, Bugs, Electronics and whatelse'），同一 handle 同时持有 x.com/marcograss 与 github.com/marcograss，具备独立的公开发表渠道，无需依赖外部媒体即可发布技术细节。

练习与反馈：2016-01 至 2019-09 间持续在博客发布带日期标注、多数带 CVE 编号的 writeup；2016 年内单年即覆盖 IOHIDFamily、containermanagerd、CoreGraphics、Qualcomm MSM、Fire Phone 内核、Linux kASLR 绕过等多个目标，研究方法在不同目标间重复应用（漏洞定位、可利用性判断、利用链构建、公开披露）。；多条 writeup 附带 CVE 编号（如 CVE-2016-1824、CVE-2016-4673、CVE-2016-2443、CVE-2015-7292、CVE-2016-4794/6162），CVE 编号由 CNA 或厂商确认；博客公开形式本身使研究细节暴露于同行审视。Black Hat US/Asia 与 POC 的会议品牌记录（未核验到具体场次）亦可作为公开发表习惯的间接旁证，但场次与反馈效果未核验。

能力与结果：形成跨目标的漏洞披露能力：能在 iOS/OS X 内核、Qualcomm 内核、Fire Phone 内核、多种用户态解析器上重复完成从发现到带 CVE 公开的完整流程，并区分可利用与不可利用情形（如 'Some unexploitable but unsandboxable OS X/iOS Kernel NULL pointers'）。；2016-05-16 [CVE-2016-1824] Apple IOHIDFamily kernel race condition as root；2016-06-17 Remotely pwning iOS via WiFi and escaping the Sandbox；2016-06-17 iOS containermanagerd XPC array out of bound vulnerability；2016-11-21 [CVE-2016-4673] Apple CoreGraphics macOS/iOS JPEG memory corruption；2016-05-03 [CVE-2016-2443] Qualcomm MSM debug fs kernel arbitrary write；2016-01-15 [CVE-2015-7292] Amazon Fire Phone kernel stack based buffer overflow；2016-01-24 Exploiting a Linux Kernel Infoleak to bypass Linux kASLR

置信度：high；替代解释：高密度披露亦可由目标流行度、厂商悬赏计划、组织资源支持或 2016 年 iOS 越狱生态高峰期共同驱动，而非个人能力机制本身；此外 conversations 维度无任何一手访谈材料，无法核验其披露动机是个人习惯、组织任务还是经济激励，此为资料缺口而非已证因果。

证据：MG-RR4-02, MG-RR4-01

### Rust 逆向工具的反复建设

起点：具备 iOS 64 位 kernelcache 解密与 KPP 提取的逆向需求，并参考 Levin 的 joker 工具与外部仓库 vault13 的 LZSS decode 实现；GitHub 主页显示名为 Marco Grassi，具备公开代码托管渠道。

练习与反馈：在 GitHub 公开维护多个 Rust 工具仓库，主题集中在安全/逆向/固件方向：PartialZip 的 Rust 实现、iOS 64 位 kernelcache 解压与 KPP 提取、固件基址搜索、RouterOS 备份加解密与打包解包；README 采用 KISS 风格，构建方式统一为 cargo build --release。工具建设与 writeup 披露方向一致，覆盖 iOS、固件、RouterOS 等多类目标。；rust-kernelcache-extractor 累计 44 star、7 fork、305 commit，公开仓库的 star/fork 计数与 commit 历史构成可量化的使用反馈；README 中对 Levin joker 工具与 vault13 LZSS 实现的引用表明工具建设建立在对既有方法比较与借鉴之上。

能力与结果：形成以 Rust 表达的逆向工具链能力：能在 kernelcache 解密解压、KPP 提取、固件基址定位、备份格式逆向等任务上重复产出可复用工具，而非仅完成单次漏洞利用。；partialzip — Implementation of PartialZip in Rust；rust-kernelcache-extractor — Extract a decrypted iOS 64-bit kernelcache（305 commits, 44 stars, 7 forks）；rbasefind — A firmware base address search tool (forked from sgayou/rbasefind)；routerosbackuptools — Tools to encrypt/decrypt and pack/unpack RouterOS v6.13+ backup files

置信度：high；替代解释：工具集中选择 Rust 亦可由个人语言偏好、Rust 在系统/逆向工具生态中的可用性、或对 KISS 与 GPL 许可的个人取向驱动，与漏洞研究能力无必然因果；4 个 pinned 仓库均为同一方向可由个人兴趣一致性解释，不一定指向能力成长的内在机制。

证据：MG-RR4-03, MG-RR4-04

## 可迁移与不可迁移

- 可迁移：维护独立的个人博客作为带日期与 CVE 编号的 writeup 载体，使研究产出按时间可排列、可被同行审视，便于建立可核验的披露节奏。
- 可迁移：将重复出现的逆向需求（kernelcache 解压、KPP 提取、固件基址搜索、备份格式处理）抽象为可复用的开源工具，而非止步于单次漏洞利用；README 借鉴既有工具（如 Levin joker）并标注来源。
- 可迁移：在 writeup 中区分可利用与不可利用情形（如 'unexploitable but unsandboxable'），保留对可利用性边界的判断而非仅报告漏洞存在。
- 不可直接迁移：独立博客与 GitHub 渠道属个人持有条件，依赖个人长期维护；若研究者无独立发表渠道或受组织发布政策约束，披露节奏无法直接复制。
- 不可直接迁移：2016 年 iOS 越狱与移动安全生态高峰期为披露密度提供了目标流行度与外部激励背景，属时期外部条件，不可在当前时期直接复现。
- 不可直接迁移：Rust 工具链建设依赖个人对 Rust 语言与 KISS/GPL 取向的选择，亦依赖 Levin joker、vault13 等既有方法的存在；缺乏这些既有方法或不同语言偏好的研究者无法直接复用该工具链。
- 不可直接迁移：一手 writeup 与 GitHub 仓库集中于 2016-2019 窗口，且 conversations 维度无任何自述材料，反馈来源与学习路径只能由间接信号推断，属本案例的资料条件限制。

## 复核问题

- stages[1].period「2016 至 2019」与 mechanisms[1] 时间范围采用 MG-RR4-03 的 date 字段「2016-2019」，但 MG-RR4-03/04 的 source.published 仅标注「持续更新型代码托管主页」「持续更新型公开仓库（master 分支 305 commits）」，未一手核验仓库创建日期或最新 commit 日期；round 4 的 action 与 result 也未记录从 GitHub 页面读取到任何日期。综合结论在未审视此不一致的情况下采用具体年份范围，使该阶段的时间边界缺乏一手来源支撑。
- mechanisms[1].feedback 将 rust-kernelcache-extractor 的 44 star、7 fork、305 commit 计数称为「可量化的使用反馈」，并归入机制所需的反馈来源环节；MG-RR4-04 仅提供计数本身，未证明存在同行审视、issue 反馈或迭代调整等反馈回路，把相关信号等同于反馈回路属于因果归因过强。
- stages[1].period：将「2016 至 2019」改写为「GitHub 仓库维护期（具体起止日期未一手核验，MG-RR4-03/04 的 source.published 仅标注持续更新型，未提供仓库创建日期或最新 commit 日期）」，使阶段时间边界与一手来源实际支撑范围一致；或在取得 GitHub 仓库日期一手核验前不采用具体年份范围。
- mechanisms[1].feedback：将「公开仓库的 star/fork 计数与 commit 历史构成可量化的使用反馈」改写为「rust-kernelcache-extractor 的 44 star、7 fork、305 commit 为公开使用与维护信号；是否存在同行审视、issue 反馈或据此迭代调整的反馈回路，MG-RR4-04 未提供证据」，把计数定位为相关信号而非已证反馈回路。
- mechanisms[0].repeated_practice：将「2016-01 至 2019-09 间持续在博客发布」改写为「2016 年与 2019 年有密集发布节点，2017-2018 年的公开 writeup 节点未在博客索引中核验到」，与 tensions[3] 记录的披露缺口一致，不使用与该缺口冲突的「持续」表述。
- tensions[1]：将其对画像归属冲突的引用由 mg-dec-01、mg-dec-02、mg-dec-03 改为 external 维度 mg-ext-id-001（claim 字段记录 WebSearch 综述文本中出现 iOS kernel/Keen Lab 与 Android/Frida/NowSecure 两种画像）与 decisions 维度 gaps 文本（记录 Keen Lab/Tencent 关联仅来自不可引用综述、未升级为 reported），遵循 round 3 synthesis_instructions 的引用精度要求。
- mechanisms[0].feedback：将「CVE 编号由 CNA 或厂商确认」改写为「多条 writeup 附带 CVE 编号（如 CVE-2016-1824、CVE-2016-4673、CVE-2016-2443、CVE-2015-7292），CVE 编号本身的存在可由博客索引核验；CVE 分配流程与确认主体本轮未一手核验」，把该环节限定为编号存在的事实陈述，不外推分配流程。

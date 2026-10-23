# Gabrielle Viala：漏洞研究成长分析

- 擅长领域：Android/Boot/TEE 漏洞
- 独立复核：pass · 82/100

## 成长阶段

- **2018-10 · Windows 内核机制逆向起点（WNF）**：在 Quarkslab 博客发表首篇可一手确认文章，主题为 Windows 通知设施（WNF）逆向，确立单点机制 writeup 实践。该文章署名为 Gwaby 而非全名 Gabrielle Viala，主题为 Windows WNF，与 primary_focus Android/TEE 不符；Gwaby 与全名 Gabrielle Viala 的同一性未由一手来源闭合，故该阶段作为署名 Gwaby 的独立数据点呈现，不以全名为锚点。（置信度：low）
  - 证据：r1-works-wnf-fetched, r1-gwaby-author-page, gv-works-06
- **2023-06 · UEFI/SMM（ring -2）利用方法论确立**：工作主题从 Windows 用户态/内核机制逆向转向 UEFI/SMM（ring -2）利用。针对 EDK II 的 Tcg2Smm 模块，以固定 4 字节写原语（写 0x00000001）经腐蚀 mSmmMemLibInternalSmramCount 绕过 SMRAM 边界检查、借 SmmLockBox 读写、向 PiSmmCore 链表注入伪造 SMI handler 并以 ROP 关闭 WP/NX，达成 SMM 代码执行，确立受限写原语经多步升级达成完整执行的方法论。研究动机为公开参考实现（EDK II）的方法学练习。该文章署名 Gwaby。（置信度：medium）
  - 证据：gv-works-02, r1-gwaby-author-page
- **2024 · 移动平台/bootloader 团队研究（致谢 contributor）**：在 Samsung Galaxy A* 启动链团队研究中以全名 Gabrielle Viala 出现于 PoC 仓库 README credits（2024-09-09）与 writeup 致谢段（2024-10-15），为致谢 contributor、非作者列（作者列为 Maxime Rossi Bellom、Raphaël Neveu）；SSTIC 2024 讲题作者列亦不含 Viala。四条 CVE（CVE-2024-20832 Little Kernel heap overflow 至 code execution 与 persistency；CVE-2024-20865 Odin auth bypass 至 USB flash；CVE-2024-20820 Secure Monitor read OOB 至 leak；CVE-2024-20021 arbitrary physical memory mapping 至 Secure World leak）与三项成果均归团队集体，全文使用集体语言，个人具体贡献未拆分。此为全名 Gabrielle Viala 首次出现在一手来源中，部分闭合身份链，但不构成个人能力变化的依据。（置信度：medium）
  - 证据：r1-samsung-viala-contributor-only, r1-samsung-poc-readme-contributors, gv-community-02, r2-sstic-2024-samsung-authors-only
- **2025-02 · SMM 方法论向商业硬件固件迁移**：将 2023 年确立的 SMM 升级方法论应用于 Steam Deck（AMD Van Gogh APU）商业固件 AmdCpmDisplayFeatureSmm.efi（CVE-2024-0179），原语更窄（固定单字节 0x83 写加有限 AND 掩码清位）。链式为：以 AND 掩码清零 mSmmIhisiSmramCount 绕过 SMRAM 边界检查获得任意读、以 1 字节写扩展共享内存缓冲区使其覆盖 SMRAM、注入伪造 IHISI 命令处理函数、以 ROP 关闭 NX 实现 SMM 代码执行；post-exploitation 整合 Dmytro Oleksiuk 的 SMM 后门页表重映射技术以透明读写 OS 内存。文章显式自参照 2023 年 EDK II 文章并标注原语类型不同。研究目标获取来自非正式反馈机制（R&D 负责人作为圣诞礼物的 Steam Deck）。该文章署名 Gwaby。（置信度：medium）
  - 证据：gv-works-03, r1-steamdeck-2023-crossref, r1-gwaby-author-page

## 主要成长机制

### 受限写原语经多步升级达成 SMM 代码执行的方法论

起点：存在 SMM/ring -2 目标与一个在取值或宽度上受限的写原语：2023 年为 EDK II 公开参考实现中固定 4 字节写（写 0x00000001），2025 年为 Steam Deck 固件中固定单字节 0x83 写加有限 AND 掩码清位。

练习与反馈：2023 年（EDK II Tcg2Smm）与 2025 年（Steam Deck AmdCpmDisplayFeatureSmm）两次应用同一升级链：腐蚀 SMRAM 边界计数器（mSmmMemLibInternalSmramCount / mSmmIhisiSmramCount）绕过 SMRAM 边界检查，扩展或借用共享内存覆盖 SMRAM，注入伪造 SMI 或 IHISI 命令处理函数，以 ROP 关闭 WP/NX，达成 SMM 代码执行。；2025 年 Steam Deck 文章显式自参照 2023 年 EDK II 文章，其中 this is the very same idea as what was presented in the previous blog post but with another type of primitive 表明作者以 2023 年方法论为参照并标注原语更窄；研究目标获取来自非正式反馈（R&D 负责人作为圣诞礼物的 Steam Deck）。

能力与结果：一套可迁移的升级模板，将最终 SMM 执行与原语窄度解耦：只要存在受限写原语，即可经边界计数器腐蚀、伪造命令处理函数注入与 ROP 关闭保护的多步升级达成完整执行。；2023 年 EDK II Tcg2Smm 以固定 4 字节写原语达成 SMM 代码执行；2025 年 Steam Deck AmdCpmDisplayFeatureSmm 以固定单字节写加 AND 掩码达成 SMM 代码执行（CVE-2024-0179）

置信度：medium；替代解释：两篇文章均署名 Gwaby，单署名累积为已记录事实，但 Gwaby 是否为单一作者而非 Quarkslab 共用笔名或团队署名未由一手页面确认，故个人能力成长与团队或笔名方法论复用无法仅凭两次数据点区分；样本量为 2。边界计数器腐蚀属已知 SMM 利用类别，方法论确立亦可能是对已知技术的应用而非新能力形成。

证据：gv-works-02, gv-works-03, r1-steamdeck-2023-crossref

### 目标从公开参考实现向商业硬件固件迁移

起点：2023 年工作基于 EDK II 公开参考实现（开源，方法学练习 for science）；可获取商业硬件（Steam Deck 经 R&D 圣诞礼物获取）。

练习与反馈：2023 年公开 EDK II 参考 → 2025 年商业 Steam Deck 固件（AMD Van Gogh APU），将升级链移植至新厂商与新目标，并接受更窄原语（1 字节加 AND 掩码）约束；post-exploitation 整合外部同行 Dmytro Oleksiuk 的 SMM 后门页表重映射技术。；Steam Deck 文章开篇以 R&D 负责人圣诞礼物框定目标获取，反映非正式反馈机制（团队资源加个人兴趣）；文章显式自参照 2023 年方法论并标注差异。

能力与结果：在更窄原语与不同厂商 SMM 模块上复现升级链的能力，并整合外部同行既有技术实现 post-exploitation 透明读写 OS 内存。；2025 年 Steam Deck CVE-2024-0179 商业固件 SMM 代码执行；整合 Dmytro Oleksiuk SMM 后门页表重映射技术实现 post-exploitation 透明读写 OS 内存

置信度：low；替代解释：目标迁移可能由团队资源（商业硬件获取渠道）与个人兴趣驱动而非纯粹能力成长；2023 至 2025 仅 2 数据点且均署名 Gwaby，身份同一性未闭合，迁移叙事依赖单署名累积推断。Samsung 全名 Gabrielle Viala 数据点因身份未闭合不并入此机制，作为独立数据点在阶段 3 呈现。

证据：gv-works-02, gv-works-03, r1-steamdeck-2023-crossref

## 可迁移与不可迁移

- 可迁移：将受限写原语显式标注为弱（如 unimpressive、rather weak）并完整记录多步升级链，使升级逻辑可复用、可同行评审（gv-works-02、gv-works-03）。
- 可迁移：在迁移至新目标时自参照先前方法论并显式标注差异（原语类型），支持累积可追溯（r1-steamdeck-2023-crossref、gv-works-02、gv-works-03）。
- 可迁移：整合具名外部同行既有技术做 post-exploitation 而非重新发明，如 Dmytro Oleksiuk 的 SMM 后门页表重映射（gv-works-03）。
- 不可直接迁移：Quarkslab 归属与博客发布平台（blog.quarkslab.com）：组织资源，使发表与同行评审成为可能，非个人可迁移实践。
- 不可直接迁移：商业硬件获取渠道（Steam Deck 经 R&D 圣诞礼物）：团队资源与非正式反馈，非个人可迁移条件。
- 不可直接迁移：EDK II 与 Steam Deck 固件可用性及具体 bug（CVE-2024-0179 等）：目标特定，不可迁移。
- 不可直接迁移：BlackHoodie 社群背景（fork blackhoodiere.github.io）：社群介入为推断（inferred），实际参与程度不明。
- 不可直接迁移：Samsung 团队研究语境（共同作者 Maxime Rossi Bellom、Raphaël Neveu，团队 CVE）：团队产出，非个人能力。

## 复核问题

- （非阻断，可选）stages[2]（period 2024）的 confidence=medium 与其 capability_change 末句'此为全名 Gabrielle Viala 首次出现在一手来源中，部分闭合身份链，但不构成个人能力变化的依据'存在内部一致性张力：若该阶段不构成个人能力变化，作为'成长阶段'评定 confidence=medium 偏高。建议将 confidence 降为 low，或将该条重述为'身份链部分闭合的数据点记录'而非与能力变化挂钩的成长阶段，使 stage 定义与 confidence 评定一致。证据支撑本身达标（r1-samsung-viala-contributor-only、r1-samsung-poc-readme-contributors、gv-community-02、r2-sstic-2024-samsung-authors-only 均 verified_in_run=true），此项不影响 pass 判定。
- （非阻断，可选）mechanisms[1]（目标从公开参考实现向商业硬件固件迁移）confidence=low 且 validation_tests 仅 [distinctive]，已明确为单数据点推断的迁移假设；建议在 mechanism 名称或 intermediate_capability 中显式标注其为'基于 Gwaby 单署名两篇文章的迁移假设'而非已确立机制，与 M1 的 [repeated, distinctive] 区分更清晰。synthesis 已在 alternative_explanation 注明身份未闭合与团队资源驱动可能，此项不影响 pass 判定。

# Sergei Volokitin：漏洞研究成长分析

- 擅长领域：嵌入式/移动/硬件漏洞
- 独立复核：pass · 83/100

## 成长阶段

- **2018（基于作者 2023 writeup 自述） · 硬件钱包软件层攻击与方法论起点**：据作者 2023-11-01 writeup 自述，2018 年对 Ledger Nano S 硬件钱包开展软件层攻击研究，发现 7 个漏洞并向 Ledger 报告，厂商在后续固件版本中修复，且曾于 2018 Black Hat USA 公布技术细节（Black Hat 议程页未取得一手佐证）。研究方法自述呈现从单点 syscall 指针校验测试，到结构体参数 syscall 校验顺序，再到安装/权限模型（APPLICATION_FLAG_DEBUG 的 MPU 影响），最终将单点漏洞组合为密钥泄露与供应链攻击的迭代路径。该研究为其公开记录中可追溯的最早一项，标志其以设备/接口安全层面为研究范围的方法取向。（置信度：medium）
  - 证据：sv-works-01, sv-deepconv-01, sv-deepconv-02, sv-deepconv-03, sv-deepconv-04, sv-community-01, sv-ext-001, sv-ext-002, sv-decisions-01, sv-decisions-02, sv-decisions-03
- **2020-10 至 2020-11 · 移动 SoC TEE 可信应用首批 CVE**：该批次为 TEE/TrustZone 方向与同类缺陷模式在公开记录中的首次出现，此后多年持续产出同类缺陷。hexplot.com/cves 记录 2020 年 10 月 MediaTek KeyInstall/Widevine/ISP 组件多个缺失边界检查的越界读写漏洞（CVE-2020-0283/-0371/-0367/-0339/-0376），以及 2020 年 10–11 月 Samsung Exynos TEEGRIS Widevine Trustlet 任意代码执行（CVE-2020-13832，含 SVE-2020-17117/17118/17119/17161）。该批次个人归属为推断，研究单元集中于单一 Trusted Application 内的输入校验缺陷。（置信度：medium）
  - 证据：sv-works-02, sv-tl-001, sv-tl-002, sv-decisions-04
- **2022-01 至 2022-12 · 相邻信任边界目标横向迁移**：hexplot.com/cves 记录的漏洞类型由单一越界读写扩展到未初始化内存与保护机制绕过；目标由 Android TEE 扩展到 Samsung TIMA trustlet、第三方开源库（trilogy）、政府智能卡方案（de.fac2）与既有 MediaTek Widevine 续作。表现为研究面与方法库的横向扩展，而非单一厂商深耕。该批次个人归属为推断。（置信度：medium）
  - 证据：sv-works-03, sv-tl-003, sv-tl-004, sv-decisions-05
- **2023-07 至 2023-11 · 逐名致谢与个人研究站点建立**：2023 年 7 月 Android 安全公告首次以个人名 'Sergei Volokitin'（无归属）逐名致谢 CVE-2023-20754，缺陷类型仍为 TEE 可信应用整数溢出。2023 年 10 月 hexplot.com/cves 记录 Silicon Labs Gecko Bootloader 整数溢出（CVE-2023-3487）与 GBL 解析器未初始化缓冲区（CVE-2023-3488），目标由移动 SoC TEE 下探到微控制器级嵌入式 bootloader 与固件解析器。2023-11-01 启用个人研究站点 hexplot.com，首篇 writeup 为 2018 年 Ledger 研究的完整公开版，自述动机为将个人研究集中在一处。发表渠道由 CVE 公告扩展到长篇 writeup。（置信度：medium）
  - 证据：sv-works-01, sv-works-04, sv-deepconv-01, sv-tl-005, sv-tl-006, sv-community-02, sv-ext-004, sv-decisions-06, sv-decisions-08
- **2024-03 至 2024-04 · 组织归属显式化与联网设备 TA**：2024 年 3 月 Android 安全公告首次以 'Sergei Volokitin of Hexplot' 显式组织归属致谢 CVE-2024-22004，标志个人→组织归属的显式化阶段边界。2024 年 4 月 hexplot.com/cves 记录同一 CVE（Google Nest Wifi Pro Trusted Application 中未检查长度导致越界读），研究目标由 MCU bootloader 转向联网设备（WiFi 路由器）的 Trusted Application，缺陷类型回归长度/边界校验缺失。（置信度：medium）
  - 证据：sv-works-05, sv-tl-008, sv-tl-009, sv-decisions-07

## 主要成长机制

### 以厂商 SDK 自建测试应用探测系统调用边界的方法论起点

起点：作者自述选择 Ledger Nano S 为研究对象，依据为设备较新、潜在漏洞多、攻击面大且托管高价值资产；并明确将研究限定为设备安全层面，排除加密货币层面。

练习与反馈：据作者 2023-11-01 writeup 自述，利用厂商提供的 SDK 编写测试应用，通过遍历/递增内存地址探测系统调用的指针校验行为，发现零页映射导致的内存泄露、哈希 syscall 算法字段校验顺序导致的 oracle 等漏洞；并以 grep 审阅开源应用代码定位将密钥写入 flash 的应用，构建针对 FIDO 应用的概念验证以演示擦除后 flash 残留密钥的恢复。此后 2020-2024 年 hexplot.com/cves 记录的多家厂商 Trusted Application 上反复出现缺失边界检查、整数溢出与未初始化缓冲区类缺陷；该批次个人归属为推断，是否沿用 2018 年 SDK 探测手法缺乏第一人称叙述。；据作者自述，2018 年 Ledger 研究中向 Ledger 报告的 7 个漏洞由厂商在后续固件版本中修复，构成报告-修复的正向反馈；2023 年起 Android 安全公告逐名致谢，构成厂商致谢形式的外部反馈。2020-2022 批次仅有公告记录，无厂商修复确认的逐项证据。

能力与结果：形成以厂商 SDK 自建测试应用对 syscall/接口边界做系统性探测的工作流，并辅以源码审阅与概念验证构建，将单点缺陷串联为可演示影响。该工作流仅由 2018 年 Ledger 一手自述支撑。；2018 年 Ledger Nano S 7 个漏洞报告与厂商修复（据作者自述）；2020 年 10 月 MediaTek KeyInstall/Widevine/ISP 五个越界读写 CVE（hexplot.com/cves，归属推断）；2023 年 10 月 Silicon Labs Gecko Bootloader 整数溢出与 GBL 解析器未初始化缓冲区 CVE（hexplot.com/cves，归属推断）；2024 年 Google Nest Wifi Pro Trusted Application 越界读 CVE（hexplot.com/cves 与 Android 致谢一致）

置信度：medium；替代解释：SDK 边界探测与组合利用的工作流仅由 2018 年 Ledger 一手自述支撑；2020-2024 批次为组织级 CVE 记录且个人归属为推断，无第一人称叙述支撑方法连续性，亦无法排除由其他研究者或协作者贡献的可能。该工作流的跨时期重复性仅能在 2018 单例上确认。

证据：sv-works-01, sv-works-02, sv-works-04, sv-works-05, sv-deepconv-02, sv-deepconv-03, sv-decisions-01, sv-decisions-02, sv-decisions-04, sv-decisions-06, sv-decisions-07, sv-ext-001, sv-tl-001, sv-tl-006

### TEE 可信应用越界读写/整数溢出/未初始化缓冲区类缺陷的跨厂商持续产出

起点：2020-10/11 批次为 TEE/TrustZone 方向与缺失边界检查类缺陷模式在公开记录中的首次出现；个人归属为推断，研究单元集中于单一 Trusted Application 内的输入校验缺陷。

练习与反馈：hexplot.com/cves 记录 2020-2024 年间跨 MediaTek、Samsung、Silicon Labs、Google 等厂商的 Trusted Application 上反复出现缺失边界检查、整数溢出与未初始化缓冲区类内存安全缺陷，跨越约 4 年。该批次个人归属为推断，是否沿用 2018 年 SDK 探测手法缺乏第一人称叙述。；2023 年 7 月起 Android 安全公告逐名致谢，构成厂商致谢形式的外部反馈；2020-2022 批次仅有 hexplot.com/cves 自报记录，缺 Android 致谢外部交叉。

能力与结果：在同一类内存安全缺陷模式上跨多个 TEE/Trustlet 厂商持续产出 CVE，形成可迁移到不同 Trusted Application 框架的缺陷识别能力；该迁移性为组织级记录的可观察结果，个人层面的方法迁移无第一人称叙述支撑。；2020 年 MediaTek KeyInstall/Widevine/ISP 越界读写批次；2020 年 Samsung TEEGRIS Widevine Trustlet 任意代码执行（CVE-2020-13832）；2022 年 Samsung TIMA TA、trilogy、de.fac2、MediaTek Widevine 多类型缺陷批次；2023 年 Android 安全公告逐名致谢 CVE-2023-20754

置信度：medium；替代解释：2020-2022 批次的个人归属为推断，hexplot.com/cves 不逐条署名研究者，跨厂商同类缺陷的持续产出可能在 Hexplot 组织内由多人完成，无法逐项归因于 Sergei Volokitin 本人；该机制的重复性由组织级 CVE 记录支撑，个人归属到 2023-07 起才由 Android 致谢逐名确认。

证据：sv-works-02, sv-works-03, sv-works-04, sv-tl-001, sv-tl-002, sv-tl-003, sv-tl-004, sv-tl-005, sv-community-02, sv-decisions-04, sv-decisions-05

### 向相邻信任边界的目标迁移

起点：2020-2022 年以 Android SoC TEE 可信应用为稳定靶面，缺陷模式集中于内存安全类。

练习与反馈：2022 年起 hexplot.com/cves 记录的目标由 Android TEE 扩展到第三方开源库（trilogy 未初始化变量）、政府智能卡方案（de.fac2 绕过 User Presence 保护）、既有 MediaTek Widevine 续作；2023 年 10 月扩展到微控制器级 SoC Bootloader 与 GBL 固件解析器；2024 年扩展到联网设备（Google Nest Wifi Pro）的 Trusted Application。缺陷类型同步扩展到未初始化内存、保护机制绕过与整数溢出。；各批次 CVE 的公告与组织 CVE 列表记录为目标迁移提供可观察结果；2020-2022 批次的个人归属为推断，缺 Android 致谢外部交叉。

能力与结果：将可信应用内存审计方法迁移到相邻信任边界对象（库、智能卡方案、bootloader、联网设备 TA），扩展适用平台范围；迁移性由组织级 CVE 记录支撑，个人层面方法迁移无第一人称叙述。；2022 年 trilogy/de.fac2/MediaTek Widevine 跨域批次；2023 年 Silicon Labs Gecko Bootloader/GSDK GBL 解析器 CVE；2024 年 Google Nest Wifi Pro Trusted Application CVE

置信度：medium；替代解释：目标迁移的可观察结果为组织级 CVE 记录，个人归属为推断；迁移路径既可解释为同一研究者主动扩展攻击面，也可解释为 Hexplot 组织内部多研究者覆盖不同平台，无第一人称叙述可区分二者。

证据：sv-works-03, sv-works-04, sv-works-05, sv-tl-004, sv-tl-006, sv-decisions-05, sv-decisions-06, sv-decisions-07

### 协调披露与延迟发表的产出链

起点：作者自述 2018 年完成 Ledger Nano S 研究，但完整 writeup 迟迟未公开；自述长期计划开设个人博客但始终未找到合适时机。

练习与反馈：对 2018 Ledger 研究先向厂商报告并等待修复，再经会议公开技术摘要，最终于 2023 整合至个人站点；2020-2024 年 CVE 仅有公告与组织 CVE 列表记录，报告-修复环节由 CVE 分配隐含，会议公开与归档环节未逐项证实。2023-11-01 启用 hexplot.com 作为研究整合发布平台，首篇 writeup 为 2018 Ledger 研究完整版，自述动机为将个人研究集中在一处。；厂商修复（据 2018 Ledger 自述）与 Android 致谢（2023-07 起逐名）为披露行为提供正向反馈；完整 writeup 的延迟公开无额外反馈渠道记录。

能力与结果：形成以厂商报告为前置、会议/公告为公开渠道、个人站点为归档渠道的披露节奏；该完整链条仅由 2018 Ledger 单例自述支撑。；2018 Ledger 研究先报告厂商、后会议公开、最终 2023-11-01 站点归档（据作者自述）；2023-11-01 hexplot.com 首篇 writeup 上线；2023-07 起 Android 安全公告逐名致谢

置信度：low；替代解释：该循环的重复性仅 2018 Ledger 一例可证，2020-2024 年 CVE 仅有公告与组织 CVE 列表记录，报告-修复-公开-归档闭环未逐项证实。2018 年研究延迟至 2023 年才公开完整 writeup，可能反映时间约束或自述的写作拖延，披露时机是否存在主动策略选择无证据支撑。

证据：sv-works-01, sv-deepconv-01, sv-deepconv-04, sv-community-01, sv-community-03, sv-ext-002, sv-decisions-03, sv-decisions-08, sv-tl-005, sv-tl-008

## 可迁移与不可迁移

- 可迁移：利用厂商提供的 SDK 编写测试应用，对系统调用/接口参数做递增式边界探测以发现指针与长度校验缺口（据 2018 Ledger 自述）。
- 可迁移：2018 Ledger 案例显示作者以攻击面规模与资产价值作为目标选择依据，并将研究范围限定在设备/接口安全层面；该选题依据仅此一例自述，作为通用可迁移实践需标注样本限制。
- 可迁移：以 grep 审阅开源应用代码定位敏感数据写入位置，并构建概念验证演示残留数据可恢复，将单点缺陷串联为可演示影响（据 2018 Ledger 自述）。
- 可迁移：以个人研究站点作为长期归档渠道，将既往未公开研究系统化整理上线（据 hexplot.com 2023-11-01 启用自述）。
- 不可直接迁移：2018 年 Ledger 研究的厂商 SDK 可用性与开源应用代码可审阅性为该研究对象特有条件；后续批次是否具备同等 SDK 与源码开放条件不可核验。
- 不可直接迁移：2020-2024 批次个人归属为推断，Hexplot 是否为 Sergei Volokitin 单人主体、是否含协作者未由一手来源确认；组织级 CVE 记录不可直接迁移为个人能力证据。
- 不可直接迁移：2018 Black Hat USA 发表与 2024 起显式组织归属涉及会议与厂商致谢渠道，这些外部渠道的可达性不属个人可复制条件。

## 复核问题

- 字段 mechanisms[1].validation_tests（TEE 跨厂商持续产出，M2）：当前为 ['repeated','distinctive']，但其 alternative_explanation 明确 2020-2022 批次个人归属为推断、跨厂商同类缺陷可能在 Hexplot 组织内由多人完成、无法逐项归因于 Sergei Volokitin 本人。'repeated' 隐含同一主体的重复，与归属仅推断的削弱措辞存在内部张力。原措辞 ['repeated','distinctive']；改写方向：降为 ['distinctive']，或在 alternative_explanation 显式说明 repeated 是组织级记录的重复而非个人级主体的重复。round-1 修订仅覆盖 mechanisms[3]（M4 协调披露链）的 repeated，未覆盖本条，属遗留 overclaim。
- 字段 stages[3].capability_change（2023-07 至 2023-11）：称 '2023 年 7 月 Android 安全公告首次以个人名 Sergei Volokitin（无归属）逐名致谢 CVE-2023-20754'。sv-tl-005 支撑该致谢事实，但 '首次' 是本次检索范围内的首次；timeline identity_check 与 gaps 明示 2023-07 之前的 Android 致谢段落未核查。原措辞 '首次以个人名...逐名致谢'；改写方向：补 '在本次检索范围内' 检索边界标注，避免未核查段落外的绝对 '首次' 断言。
- 字段来源一致性说明：sv-tl-007（Ledger writeup，verified_in_run=false，status=unknown）与同 URL 的 sv-works-01/sv-deepconv-01/sv-ext-001（verified_in_run=true，status=documented）核验状态不一致。synthesis 未引用 sv-tl-007，符合规则，但建议在 open_questions 或来源说明中注明该不一致为同一 URL 不同维度抓取批次的核验状态差异，而非内容矛盾，以消除来源完整性的读者疑虑。

# Sergej Schumilo：漏洞研究成长分析

- 擅长领域：内核/虚拟化/Web 自动化漏洞发现
- 独立复核：pass · 93/100

## 成长阶段

- **2014-2016 · 学位阶段：从 USB 设备 fuzzing 到硬件辅助 OS 内核 fuzzing 的技术基底建立**：2014 年 B.Sc. 论文构建基于 QEMU/KVM 的 USB fuzzing 基础设施（工具 vUSBf，ss-works-bsc-2014、ss-timeline-001、ss-dec-001 均 documented）；2016 年 M.Sc. 论文将目标由 USB 设备升级到 OS 内核，引入 Intel PT 覆盖反馈与 VT-x 隔离/快照，构成 kAFL 的直接前身（ss-works-msc-2016、ss-timeline-003、ss-dec-002 均 documented）。该阶段确立『虚拟化 + 硬件辅助覆盖 + 快照恢复』技术基底，后续 kAFL/Nyx 的快照与虚拟化思路可追溯至此。需补注：2014-2016 学位阶段的导师与同伴具体反馈方式无公开一手材料（conversations/decisions 维度 gaps 一致），故技术基底的『确立』不宜读为已证个人决策，选题连续性也可能源于导师与机构研究主线导向。（置信度：high）
  - 证据：ss-works-bsc-2014, ss-works-msc-2016, ss-timeline-001, ss-timeline-003, ss-dec-001, ss-dec-002, ss-convo-002
- **2017 · kAFL 顶会化：硬件辅助覆盖引导内核 fuzzing 范式的首次确立**：作为第一作者在 USENIX Security 2017 发表 kAFL，使用 Intel PT 取覆盖、VT-x 快照隔离内核崩溃，跨 Linux/macOS/Windows 工作，给出每秒最高 17,000 次执行的性能数据，并在 ext4、HFS、APFS、NTFS 驱动中发现缺陷（ss-works-kafl-2017、ss-timeline-004、ss-dec-003 均 documented）。这是首次进入顶级安全会议，并与 Aschermann、Gawlik、Schinzel、Holz 形成稳定合作团队，方法抽象为 OS 无关、硬件辅助范式，确立后续 5 年研究主线。该阶段的能力变化可由 USENIX Security 17 论文页一手核验。（置信度：high）
  - 证据：ss-works-kafl-2017, ss-timeline-004, ss-dec-003, ss-works-bsc-2014, ss-works-msc-2016
- **2019-2020 · 方法扩展阶段：覆盖率引导局限的逐项方法扩展**：REDQUEEN（输入-状态对应，NDSS 2019）、GRIMOIRE（结构合成，USENIX Security 2019）、HYPER-CUBE（高维 hypervisor fuzzing，NDSS 2020）、IJON（人工锚点深度状态空间探索，IEEE S&P 2020）四项工作的会议发表事实与作者列表经 timeline 维度及 R1-EV-01/02/03/04 一手核验为 documented（ss-timeline-006/007/009/010）；但其方法定位（输入-状态对应、结构合成、高维 hypervisor、人工锚点）在 works 维度仅依据 schumilo.de 一手记录，status 为 reported（ss-works-redqueen-2019、ss-works-hypercube-2020、ss-works-ijon-2020）。同期研究对象由 OS 内核扩展到 hypervisor（HYPER-CUBE，Schumilo 第一作者，R1-EV-03），方法层叠加高维输入构造与状态空间探索，为 Nyx 的覆盖引导 hypervisor fuzzing 做前置探索（ss-dec-004/006 documented）。（置信度：medium）
  - 证据：ss-timeline-006, ss-timeline-007, ss-timeline-009, ss-timeline-010, R1-EV-01, R1-EV-02, R1-EV-03, R1-EV-04, ss-works-redqueen-2019, ss-works-hypercube-2020, ss-works-ijon-2020, ss-dec-004, ss-dec-006
- **2021-2022 · 系统化与产业反馈阶段：Nyx/Nyx-Net 统一框架与外部认可**：Nyx（USENIX Security 2021，ss-works-nyx-2021、ss-timeline-011、ss-dec-007 均 documented）整合 kAFL/HYPER-CUBE 路线为统一框架，基于快速快照与 affine types 变异引擎对 hypervisor 做 greybox 覆盖引导 fuzzing；Nyx 论文以覆盖率引导反驳『盲 fuzzing 为 hypervisor fuzzing 最优』论点（ss-dec-007 documented，short_quote: blind fuzzing is the most efficient approach to identify security issues in hypervisors），该证据应限定为反驳论点证据，而非基于 HYPER-CUBE 经验反馈的改进证据。评估中报告发现 44 个新缺陷、为其中 22 个申请 CVE（ext-05 reported，单一 USENIX 会议页来源；与 ext-01 Intel 新闻稿 authoritative_secondary documented 不同来源强度，不得并列标 documented）。Nyx-Net（EuroSys 2022）将快照机制演化为增量快照以适配网络协议栈 fuzzing：其会议发表事实由 ss-timeline-012（documented）一手支撑，方法定位在 works 维仅依据 schumilo.de 一手记录，status 为 reported（ss-works-nyxnet-2022）。同期 Nyx 获 Intel Hardware Security Award 二等奖（ext-01 documented），Intel 称其安全卓越中心已在内部使用并演进该技术；ss-dec-008（Intel 奖项 documented）维持 documented。ss-dec-009（Nyx-Net 产品化）中 Mozilla『currently integrating』Nyx into Firefox CI 与 Intel『actively maintaining a fork』为 nyx-fuzz.com 项目方进行时自述（R2-EV-03），Mozilla 官方 Firefox fuzzing 文档（R2-EV-02）未提及 Nyx，Intel 官方 fork 仓库（github.com/IntelLabs/nyx、github.com/intel/nyx）均 404 未一手确认，故 ss-dec-009 的产业采用主张应标 reported/inferred 并附限定，与 mechanisms[3].observed_outcomes 及 tensions 的限定一致（ss-dec-009 证据本身 status=documented 不变）。（置信度：medium）
  - 证据：ss-works-nyx-2021, ss-timeline-011, ss-timeline-012, ss-timeline-013, ss-dec-007, ss-dec-008, ss-dec-009, ss-works-nyxnet-2022, ext-01, ext-03, ext-05, R2-EV-02, R2-EV-03

## 主要成长机制

### 硬件辅助与快照的虚拟化 fuzzing 技术基底建立及跨目标复用

起点：2014-2016 学位阶段以 QEMU/KVM 构建 USB fuzzing 基础设施（vUSBf），并引入 Intel PT 覆盖反馈与 VT-x 隔离/快照构建硬件辅助 OS 内核 fuzzer（ss-works-bsc-2014、ss-works-msc-2016 documented）。选题与后续主线一致，构成可复用技术基底。需补注：2014-2016 学位阶段的导师与同伴具体反馈方式无公开一手材料（conversations/decisions 维度 gaps），技术基底的建立不宜读为已证个人决策。

练习与反馈：以同一虚拟化 + 硬件辅助 + 快照基底反复迁移目标域：USB 设备（vUSBf）→ OS 内核（kAFL，2017）→ hypervisor（HYPER-CUBE 2020、Nyx 2021）→ 网络协议栈（Nyx-Net 2022，增量快照）。每次迁移保留并扩展覆盖解码、快照执行等基础设施（libxdc、Intel PT 覆盖、快照执行在工具间复用）。；外部反馈来自多类渠道：USENIX Security 2017/2021、NDSS 2019/2020、IEEE S&P 2020、EuroSys 2022 同行评议接收（ss-timeline-004/006/007/009/010/011/012 documented）；Intel Hardware Security Award 2022 二等奖及 Intel 安全卓越中心内部采用（ext-01 documented）；学位阶段 Univention Open Source Absolventpreis 2015 与 Bernard-Rincklake-Preis 2018（ss-timeline-002 reported、ss-timeline-005 reported，独立页面未抓取，仅 schumilo.de 一手）。需补注：2014-2016 学位阶段的导师与同伴具体反馈方式无公开一手材料。

能力与结果：形成『以快照隔离实现近零开销崩溃恢复 + 以硬件特性获取 OS 无关覆盖』的可复用工程能力，并能针对新目标域调整快照粒度（全量快照→增量快照）与变异策略。；kAFL 跨 Linux/macOS/Windows 内核文件系统驱动发现缺陷，每秒最高 17,000 次执行（ss-works-kafl-2017、ss-timeline-004、ss-dec-003 documented）；HYPER-CUBE 相对现有 hypervisor fuzzer 发现逾两倍缺陷与最高两倍覆盖率，5 分钟内复现 VENOM 并发现 54 个新缺陷、获 37 个 CVE（R1-EV-03 documented，NDSS 2020 一手）；Nyx 评估中报告 44 个新缺陷、22 个 CVE 申请（ext-05 reported，单一 USENIX 会议页来源，与 ext-01 Intel 新闻稿 authoritative_secondary documented 不同来源强度）；Nyx-Net 将快照 fuzzing 扩展到网络协议栈：会议发表事实由 ss-timeline-012（documented，Nyx-Net EuroSys 2022）一手支撑；方法定位 ss-works-nyxnet-2022 reported（works 维，方法定位仅 schumilo.de 一手）；Google Scholar 累计引用 2030、h-index 9、i10-index 9（ext-04 documented，数值经 R1-EV-05 重新一手核验一致）——聚合引用计量仅作外部采纳广度旁证，不构成能力来源的独立证据；八个公开 fuzzing 工具（vUSBf、kAFL、redqueen、grimoire、ijon、hypercube、nyx、nyx-net）；vUSBf 来自 ss-comm-publictools-2014-2022，grimoire 来自 ss-works-toolchain-inferred 与 R2-EV-01（RUB-SysSec/grimoire 仓库一手核验），其余 6 个两来源均列

置信度：high；替代解释：选题连续性与技术基底复用也可能源于导师与机构（RUB-SysSec）研究主线导向，以及团队分工下不同合著者主导不同子方向，而非本人独立主导的系统性决策；2014-2016 学位阶段导师与同伴具体反馈方式无公开一手材料，技术基底『确立』的个人决策属性不可单独证实。

证据：ss-works-bsc-2014, ss-works-msc-2016, ss-works-kafl-2017, ss-works-nyx-2021, ss-works-nyxnet-2022, ss-works-toolchain-inferred, ss-timeline-004, ss-timeline-009, ss-timeline-011, ss-timeline-012, ss-dec-003, ss-dec-007, ext-01, ext-04, ext-05, R1-EV-03, R1-EV-05, R2-EV-01, ss-comm-publictools-2014-2022

### 覆盖率引导局限的方法扩展（输入-状态对应、结构合成、状态空间探索）

起点：kAFL（2017）确立硬件辅助覆盖引导内核 fuzzing 范式后，覆盖率引导在输入校验（magic bytes、checksum）与高度结构化输入处存在结构性短板（ss-dec-004 documented）。

练习与反馈：以针对结构性短板的逐项方法扩展推进研究，而非一次性重写：覆盖率引导→输入-状态对应（REDQUEEN，NDSS 2019）→结构合成（GRIMOIRE，USENIX Security 2019）→状态空间探索（IJON，IEEE S&P 2020）。其中 ss-works-redqueen-2019/ijon-2020 在 works 维度 status=reported，方法定位仅依据 schumilo.de 一手；会议发表事实由 ss-timeline-006/010 documented 及 R1-EV-01/04 一手核验支撑。同期 HYPER-CUBE（NDSS 2020，Schumilo 一作，R1-EV-03 documented）将目标由 OS 内核扩展到 hypervisor，方法层叠加高维输入构造。；反馈主要来自 NDSS 2019、USENIX Security 2019、IEEE S&P 2020 同行评议接收（ss-timeline-006/007/010 documented，R1-EV-01/02/04 一手核验作者列表）。GRIMOIRE 评估中识别 19 个真实程序内存损坏缺陷并获 11 个新 CVE（R1-EV-02 documented，USENIX Security 2019 一手）。

能力与结果：形成对覆盖率引导局限的识别能力，及针对不同局限类型选择对应方法原语（输入-状态对应、grammar-like 组合、人工锚点）的扩展能力，而非依赖单一覆盖引导。；REDQUEEN 提出基于输入-状态对应的变异机制以绕过 magic bytes 与嵌套 checksum 等比较约束（R1-EV-01 documented，NDSS 2019 一手）；GRIMOIRE 通过 grammar-like 组合处理高度结构化输入，评估中识别 19 个真实程序内存损坏缺陷并获 11 个新 CVE（R1-EV-02、R2-EV-01 documented）；IJON 通过人工锚点（ijon_max/ijon_min/ijon_strdist 原语）定义状态空间度量，引导 fuzzer 探索纯覆盖引导无法到达的深度状态空间（R1-EV-04 documented，RUB-SysSec/ijon GitHub 仓库 README，因 IEEE Xplore/CSDL 官方页抓取失败采用的替代一手来源）；HYPER-CUBE 相对现有 hypervisor fuzzer 发现逾两倍缺陷与最高两倍覆盖率，5 分钟内复现 VENOM 并发现 54 个新缺陷、获 37 个 CVE（R1-EV-03 documented）

置信度：medium；替代解释：方法扩展的叙事可能部分源于团队分工（不同合著者主导不同原语创新，如 REDQUEEN 第一作者为 Aschermann、GRIMOIRE 第一作者为 Blazytko），而非本人主导的系统性扩展；works 维度方法定位仅 schumilo.de 一手（reported），本人对这些方法原语的具体贡献度不可单独证实。存在幸存者偏差：该机制仅可观测已被顶会接收并发表的方法扩展成功案例，未被接收或未公开的补全尝试不可见，因果强度受发表筛选影响。

证据：ss-works-redqueen-2019, ss-works-ijon-2020, ss-works-hypercube-2020, ss-timeline-006, ss-timeline-007, ss-timeline-009, ss-timeline-010, ss-dec-004, R1-EV-01, R1-EV-02, R1-EV-03, R1-EV-04, R2-EV-01

### 学术-产业双轨反馈与工具公开配套产出

起点：kAFL（2017）被 USENIX Security 接收后，研究产出同时具备学术评议与产业实践两条潜在反馈通道；同期已有公开工具发布习惯（vUSBf 2014，ss-comm-publictools-2014-2022 documented）。

练习与反馈：每项研究产出配套开源工具与公开演讲（论文、开源代码与公开演讲三者配套产出），使原型同时暴露于同行评议与实践者两条反馈通道。学术侧在 USENIX Security/NDSS/IEEE S&P/EuroSys 反复发表；产业侧在 Black Hat Europe 2019（『What the Fuzz』，ss-dec-005 reported、ss-timeline-008 reported，blackhat.com 议程页 403 未独立核验）、FuzzCon Europe 2020、USENIX Security 2021 等会场宣讲（ss-comm-talks-2019-2021 documented）。配套工具持续发布并后期统一收口到 nyx-fuzz 组织（nyx、libxdc）与站点 nyx-fuzz.com（ss-works-toolchain-inferred inferred，仅作旁证）。；学术侧反馈为顶会同行评议接收；产业侧反馈为 Black Hat/FuzzCon 等实践者会场接受与 Intel 厂商奖项。Intel 官方新闻稿称 Nyx『greatly improved the ability to test critical system software』，并称其安全卓越中心已在内部使用并演进该技术（ext-01 documented，authoritative_secondary）。

能力与结果：形成将研究原型同时转向学术评议与实践者采纳的双轨输出能力，以及将工具整合为可被第三方维护与集成的基础设施（libxdc 作为共享覆盖库）的工程化能力。；学术侧：kAFL/REDQUEEN/GRIMOIRE/HYPER-CUBE/IJON/Nyx/Nyx-Net 七篇代表作跨 2017-2022 顶会发表（ss-timeline-004/006/007/009/010/011/012 documented）；产业侧：据 nyx-fuzz.com 项目方自述（ss-dec-009，单一一手），Mozilla『currently integrating』Nyx into Firefox CI（进行时，非完成式），Intel『actively maintaining a fork of an older version』；Mozilla 官方 Firefox fuzzing 文档（R2-EV-02 documented）未提及 Nyx（列出 libFuzzer/AFLFuzz/LangFuzz/Avalanche/domino/Grizzly/Android Monkey），security.mozilla.org 连接被拒未取得；Intel 官方 fork 仓库（github.com/IntelLabs/nyx、github.com/intel/nyx）均 404 未一手确认。该产业采用主张不得与 ext-01（Intel 官方新闻稿 authoritative_secondary）等量标 documented，应标 reported/inferred 并明示未获 Mozilla/Intel 官方页面交叉核实（R2-EV-03 核实原意为进行时表述）；Intel Hardware Security Award 2022 二等奖（50,000 USD）与第 9 届德国 IT Security Award 决赛（ss-dec-008 documented；ss-timeline-013 documented；ss-timeline-014 reported，独立页面未抓取）；八个公开 fuzzing 工具的持续发布（vUSBf、kAFL、redqueen、grimoire、ijon、hypercube、nyx、nyx-net）；vUSBf 来自 ss-comm-publictools-2014-2022，grimoire 来自 ss-works-toolchain-inferred 与 R2-EV-01，其余 6 个两来源均列

置信度：medium；替代解释：双轨反馈部分依赖 nyx-fuzz.com 项目方单一一手自述（Mozilla/Intel 产业采用），Mozilla 官方文档未提及 Nyx、Intel fork 仓库未确认，产业采纳的完成度与范围被高估的风险存在；Black Hat Europe 2019 议程页 403 未独立核验，仅以 schumilo.de 一手为据。『论文-代码-演讲配套产出』作为可迁移特征的证据 status=inferred（源自 ss-works-toolchain-inferred），不宜读作已证实践特征。存在声誉偏差：Intel 官方新闻稿与 Google Scholar 引用计量作为外部认可被反复引用，权重高于非官方渠道，可能放大对工具实际影响的判断。

证据：ss-comm-publictools-2014-2022, ss-comm-talks-2019-2021, ss-comm-awards-2015-2022, ss-works-toolchain-inferred, ss-timeline-008, ss-timeline-013, ss-timeline-014, ss-dec-005, ss-dec-008, ss-dec-009, ext-01, R2-EV-01, R2-EV-02, R2-EV-03

### 长期合著网络的稳定协作与机构归属

起点：自 kAFL（2017）起即与 Aschermann、Gawlik、Schinzel、Holz 合著，形成以 RUB-SysSec 组（Holz 主持）为核心的合著网络（ss-comm-peernetwork-2017-2022 documented；ss-convo-003 inferred）。

练习与反馈：2017-2022 七篇代表作中 Thorsten Holz 出现在全部七篇，Cornelius Aschermann 出现在七篇，Ali Abbasi 出现在四至五篇，Simon Wörner 与 Andrea Jemmett 出现在后期工作（ss-comm-peernetwork-2017-2022 documented）。各篇合著署名经一手核验：kAFL（ss-timeline-004）、REDQUEEN（R1-EV-01）、GRIMOIRE（R1-EV-02）、HYPER-CUBE（R1-EV-03，Schumilo 一作）、IJON（R1-EV-04，RUB-SysSec/ijon GitHub README）、Nyx（ss-timeline-011）、Nyx-Net（ss-timeline-012）。Google Scholar 高频共同作者 Aschermann/Abbasi/Blazytko 与 schumilo.de 列示吻合（ext-04/ext-06）。；合著网络提供合著审阅与技术迁移通道，使工作从 OS 内核 fuzzing 扩展到 hypervisor fuzzing；但导师/合作指导者关系（与 Thorsten Holz）仅由长期共同作者结构推断，无一手评价或公开致谢文字佐证其指导机制与反馈方式（external 维度 gaps）。

能力与结果：形成依托稳定合著网络与机构（RUB-SysSec）持续产出顶会论文的协作能力。；各篇合著署名一手核验（ss-timeline-004/006/007/009/010/011/012 + R1-EV-01/02/03/04 documented）；Google Scholar 高频共同作者 Aschermann/Abbasi/Blazytko 与 schumilo.de 列示吻合（ext-04/ext-06）

置信度：low；替代解释：机制4 仅满足『跨材料/跨时期重复』一项验证标准，generative（独立产出新结果）与 distinctive（相对对照的区分度）标准缺乏独立证据支撑，故 confidence=low。合著网络的持续出现既作为机制起点条件又作为观测结果，存在循环论证风险（circular reasoning）；与 tensions 中『合著网络与个人贡献难分离』及幸存者偏差识别相符。机构归属（RUB-SysSec 组、Holz/Aschermann 长期合著网络）与顶会接收筛选对机制4 独立解释力构成限制：合著网络的存在可由机构资源配置与导师声誉解释，个人贡献不可单独分离。不得为凑齐 generative/distinctive 而搜索或拔高证据。

证据：ss-comm-peernetwork-2017-2022, ss-convo-003, ss-timeline-004, ss-timeline-006, ss-timeline-007, ss-timeline-009, ss-timeline-010, ss-timeline-011, ss-timeline-012, R1-EV-01, R1-EV-02, R1-EV-03, R1-EV-04, ext-04, ext-06

## 可迁移与不可迁移

- 可迁移：以学位论文选题对齐后续研究主线：B.Sc./M.Sc. 学位论文选题与后续顶会论文主线对齐，使学位产出可复用为研究原型（ss-works-bsc-2014、ss-works-msc-2016、ss-works-kafl-2017 documented）。
- 可迁移：以同一技术基底（虚拟化 + 硬件辅助覆盖 + 快照恢复）反复迁移目标域，针对新目标调整快照粒度与变异策略而非从零重建（ss-works-kafl-2017、ss-works-nyx-2021、ss-works-nyxnet-2022、ss-timeline-004/011/012 documented）。
- 可迁移：每项研究产出配套开源工具与公开演讲（论文、开源代码与公开演讲三者配套产出），使原型同时暴露于同行评议与实践者两条反馈通道（ss-comm-publictools-2014-2022、ss-comm-talks-2019-2021 documented；配套产出作为可迁移特征的证据 status=inferred，源自 ss-works-toolchain-inferred，不宜读作已证实践特征）。
- 可迁移：以针对结构性短板的逐项方法扩展（覆盖率引导→输入-状态对应→结构合成→状态空间探索）推进研究，而非一次性重写（ss-dec-004、ss-timeline-006/007/010 documented）。
- 可迁移：以可核验产出（发现缺陷数、CVE 申请数、执行吞吐）作为工具有效性的外部校验依据，而非以宣传性表述替代（ss-works-kafl-2017、R1-EV-03、ext-05、ss-dec-007 documented/reported 按各自来源强度）。
- 可迁移：将共享基础设施（如 libxdc 覆盖解码库）在多个工具间复用，使工具建设工程化而非一次性产出（ss-works-toolchain-inferred inferred，仅作旁证）。
- 不可直接迁移：长期稳定合著网络（Holz/Aschermann/Abbasi 等，2017-2022 全程合著）与机构归属（RUB-SysSec 组）属个人特有条件，非可迁移做法；个人贡献与合著网络/机构资源难分离。
- 不可直接迁移：Intel Hardware Security Award 2022 与 Intel 安全卓越中心内部采用属特定厂商与特定时间窗口的外部认可，伴随资金支持，可能影响后续工具产品化决策权重，非可复制的研究路径。
- 不可直接迁移：学位阶段（FH Münster B.Sc./M.Sc.）的选题连续性部分依托所在院校课程与导师配置，2014-2016 学位阶段的导师与同伴具体反馈方式无公开一手材料，不宜作为可迁移做法。
- 不可直接迁移：顶会发表筛选本身构成幸存者偏差来源：四个机制均基于已被顶会接收的论文构建，未被接收的投稿与失败方向不可见，外部认可的可复制性受发表筛选限制。

## 复核问题

- 建议（非强制，verdict=pass）：mechanisms[3].alternative_explanation 中『不得为凑齐 generative/distinctive 而搜索或拔高证据』的『凑齐』『拔高』用词略口语化，可改为『不应为满足 generative/distinctive 验证标准而扩大检索范围或提升证据强度判定』，与全文专业书面语风格统一。该问题不属于 task.md 列举的黑话、俚语、比喻、拟人、宣传性表达违规类别，不触发 revise。
- 建议（非强制，verdict=pass）：mechanisms[2].repeated_practice 中『后期统一收口到 nyx-fuzz 组织』的『收口』为工程口语，可改为『后期统一归并到 nyx-fuzz 组织与站点 nyx-fuzz.com』。该问题不属于 task.md 列举的违规类别，不触发 revise。
- 建议（非强制，verdict=pass）：mechanisms[0].observed_outcomes 第6条『其余 6 个两来源均列』表述过简，可展开为『其余 6 个工具在 schumilo.de 主页与对应会议/仓库两来源中均有列示』，提升可追溯性。该问题不触发 revise。
- 建议（非强制，verdict=pass）：open_questions 第1条 Atropos（USENIX Security 2024）的作者归属与一手页面均未确认，当前已正确保留为资料缺口。后续若获取 USENIX Security 2024 议程页或 schumilo.de 更新，可据以确认或排除作者归属，扩展时间线至 2024。当前不构成 revise 依据。

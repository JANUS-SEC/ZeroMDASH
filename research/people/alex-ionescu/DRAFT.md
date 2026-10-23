# 未通过独立复核

已达到最大修订次数 3；本文件是审计草稿，不得进入跨人物比较。

# Alex Ionescu：漏洞研究成长分析

- 擅长领域：Windows 内核与平台漏洞
- 独立复核：revise · 76/100

## 成长阶段

- **约2004–2006 · ReactOS 内核多子系统重写作为进入 NT 内部结构的起点**：约2004 年加入 ReactOS，在前任内核负责人 David Welch 离开后重写线程调度器、调度器、锁与 IRQL 机制、HAL、executive、对象管理器、进程管理器、I/O 管理器、基础 VDM 与 8086 支持等关键子系统，指导两名 Google Summer of Code 学生，并将项目目标从 NT4 提升至 NT 5.2（本人自述）；2006-01 代码审计争议（BadStack/syscall.S）迫使其形成“重新实现 vs 复制粘贴”的论辩框架；2006-11 起建立持续公开 writeup 习惯。通过多子系统重写实践建立对 NT 内核结构的整体把握。（置信度：medium）
  - 证据：r1-community-reactos-rewrite, aionescu-tl-2006-01-reactos-audit, aionescu-ext-005, aionescu-tl-2006-11-blog-start
- **2006–2008 · 退出 ReactOS 转入 Windows Internals 教学与合著，建立负责任披露与会议演讲实践**：2007 年受聘 David Solomon 的 Expert Seminars 担任 Windows Internals 讲师（Mark Russinovich 转 Microsoft 后由其接替），因与微软员工及资源接触增多、加之 Apple 实习，与 ReactOS 工作产生利益冲突，主动退出项目（本人自述）；2007-08 Purple Pill 发现 ATI 未被告知该缺陷后于 1 小时内主动下架工具与帖子，以 responsible disclosure 为由；2008-08 Black Hat 演讲报告 win32k.sys 四项本地 DoS 缺陷，其中一项存在 user→kernel 提权风险。从 ReactOS 重写实践转入权威参考书教学与会议披露。（置信度：medium）
  - 证据：r1-community-reactos-rewrite, r1-community-purple-pill, r1-community-blackhat2008-win32k, aionescu-ext-006, AI-conv-05
- **2009–2015 · Windows Internals 第六版倦怠与第七版复出，向可利用攻击原语与会议圈输出**：第六版（Windows 7）期间因兼顾学业、实习与人际关系严重倦怠并造成该书延期（本人自述）；第七版项目被前两位作者放弃后主动联系 Pavel Yosifovich 合著，承认单人难以完成且自身范围扩展会再度造成延期，将范围蔓延约束为 12 个月可交付周期，在 Windows 10 Redstone 2 发行数周内出版；2013 KASLR 演讲后与微软同事分享幻灯片，被提示“expect some changes in Windows 8.1”；2015 Infiltrate AWE 攻击与 Recon HookingNirvana 将内核内部机制研究切入可利用攻击原语演示，并把演讲材料固化为同名 GitHub 仓库。（置信度：high）
  - 证据：AI-conv-01, AI-conv-02, AI-conv-03, aionescu-decisions-001, aionescu-tl-wininternals-6e-college, aionescu-ext-001, aionescu-ext-002, r1-community-kaslr-w81, aionescu-tl-2015-infiltrate-awe, aionescu-tl-2015-recon-hookingnirvana, aionescu-ext-003
- **2016–2019 · 公开输出由书籍写作转向会议演讲，最小可用研究工具建设与 hypervisor 接口模糊测试**：公开输出由书籍写作转向会议演讲，自述近年将公开研究重心迁移至 infosec 会议圈并构思“Windows Design Flaw Garage Sale”系列；2016 SimpleVisor 以最小可用实现公开研究型 hypervisor 并显式声明非生产级；2017 Bringing Call Gates Back 作为第七版写作副产物产出 x64 call-gate 技术发现（非漏洞/0day）；2017/2018 SpecuCheck 在侧信道漏洞爆发期放出针对 Meltdown/Spectre v2/Foreshadow 的缓解检测工具；2018 Dynamic Tracing in Windows 10 19H1 即时逆向新版内核 EtwRegisterEventCallback、KeSetSystemServiceCallback、KeSetTracepoint 等动态插桩能力；2019 Hyper-V Bridge 系列以 WDF 取代近二十年 WDM 习惯构建用户态↔hypervisor 模糊测试桥，并引用 hfiref0x 的 WinObjEx64、邀请 Azeria 协作作图。（置信度：high）
  - 证据：ai-works-06, ai-works-02, aionescu-tl-2017-08-call-gates, aionescu-decisions-003, aionescu-tl-2017-2018-specucheck, aionescu-tl-2017-05-sysan360-containers, aionescu-tl-2017-06-recon-sam, aionescu-ext-008, aionescu-tl-2018-08-dynamic-tracing-19h1, ai-works-04, aionescu-decisions-002, AI-conv-04, aionescu-tl-2019-01-hyperv-bridge, aionescu-ext-007, aionescu-decisions-004, r1-community-hyperv-part1, r1-community-hyperv-part2

## 主要成长机制

### 通过权威参考书合著的系统审阅产出技术发现

起点：《Windows Internals》合著席位，与 David Solomon（提供 Microsoft 开发团队内部联系与洞察）、Mark Russinovich（逆向工程同伴）构成分工互补的带教关系；第六版覆盖 Windows 7、第七版覆盖 Windows 10，作者自述其与 Russinovich 仅做逆向工程。

练习与反馈：在每一版书籍写作中对内核结构变化做系统性审阅：第六版期间“边学边写”系统性补全内核知识；第七版投入约 12 个月、协调多人变动（Solomon 退休、Russinovich 转 Azure CTO），对照 Windows 10 周年更新与 Redstone 2 变化逐项审阅。；合著者分工反馈（Solomon 提供内部联系，作者与 Russinovich 负责逆向）；第七版项目被前两位作者放弃后主动联系 Pavel Yosifovich 合著以分担单人范围，并在公开质疑下做出重返选择。

能力与结果：形成系统性内核结构知识基线，具备在结构审阅中识别强制功能与遗留机制的能力，为后续独立技术发现提供知识基线。；Bringing Call Gates Back：为第七版研究 UMS 时触及 CR4[FSGSBASE]、GS 段、LDT、KPROCESS 字段，重读 AMD 手册发现 x64 长模式下 LDT 与 16 字节调用门描述符仍有效、PatchGuard 不监控 per-process LDT 条目，复活此前被认为已在 x64 移除的调用门 Ring0 执行技术；作者明确声明“there is no 'vulnerability' or 'zero-day' presented here”，即非漏洞/0day。；第七版 Part 1 由 Microsoft Press/Pearson 于 2017-05-05 发行，出版社页面将其与 Russinovich、Solomon、Yosifovich 并列署名。

置信度：medium；替代解释：核心技术发现产出仅一次（Bringing Call Gates Back），反复主要落在写书审阅行为而非独立技术发现产出。该发现可替代地由 ReactOS 时期描述符表重写经验（stage 0）提供结构敏感性，写书仅为触发时机而非成因；故 confidence 调为 medium。是否存在第二次写书副产物产出的独立技术发现未见证据，列为资料缺口。

证据：AI-conv-01, AI-conv-03, aionescu-decisions-001, aionescu-decisions-003, ai-works-02, aionescu-tl-2017-08-call-gates, aionescu-ext-001, aionescu-ext-002

### 按需自建研究型工具并公开为可复用资产

起点：研究所需基础设施未被厂商或既有工具提供：用户态与 Hyper-V/Secure Kernel 通信的模糊测试驱动、可教学的最小 VT-x hypervisor、侧信道缓解状态检测工具等均需自建。

练习与反馈：针对每个研究目标自建配套基础设施并公开：SimpleVisor（最小化汇编与最小 VMX 代码，支持 hyperjacking/unhyperjacking）、SpecuCheck（检测 Meltdown/Spectre v2/Foreshadow 缓解状态）、HookingNirvana（Recon 2015 演讲配套代码）、Hyper-V Bridge 系列（WDF root-enumerated 驱动 vtlbrdge.sys + 用户态客户端 + INF）、VisualUefi、lxss、smctool 等。；周末工程项目对照实际实现检验长期假设——发现 WDF 较 WDM 可省去 1500-4000 行 PnP 样板代码，纠正近二十年“WDM 更适合研究型驱动”的误判；社区复用反馈（SimpleVisor 约 2k stars、SpecuCheck 对应多个公开 CVE、GitHub 27 仓库 2.2k followers）反向扩大影响与反馈面。

能力与结果：作者随公开议题变化扩展自身工具栈，使其研究产出常以可发布工具形式固化；以最小可用实现为原则并显式声明非生产级，区分研究工具与产品代码。；SimpleVisor（2016）以最小可用实现公开，README 显式声明不做错误校验、非生产级，作为他人理解 VT-x 的基线。；SpecuCheck（2017/2018）在侧信道漏洞爆发期快速放出针对多个公开 CVE 的缓解检测工具。；Hyper-V Bridge Part 1/2（2019-01-14/27）连载式公开 hypercall、MDL 与基于 IOCTL 的用户态桥接用于模糊测试；引用 hfiref0x 的 WinObjEx64 查看设备对象，邀请 Azeria 协助制作图示，并承诺将完整工具打磨后发布到 GitHub。

置信度：high；替代解释：工具建设部分得益于雇主职位（CrowdStrike CTIO）与既有声誉降低了打磨与公开发表成本，而非纯个人方法；SpecuCheck 等工具借 2018 侧信道公开漏洞潮的时机窗口获得相关性，议题热度与时机亦为贡献因素。Hyper-V Bridge 完整工具是否按承诺最终发布到 GitHub 未核证。

证据：ai-works-04, ai-works-06, ai-works-07, ai-works-08, AI-conv-04, aionescu-decisions-002, aionescu-decisions-005, aionescu-tl-2017-2018-specucheck, aionescu-tl-2019-01-hyperv-bridge, aionescu-tl-2015-recon-hookingnirvana, aionescu-ext-007, aionescu-ext-004, alex-community-08, r1-community-hyperv-part1, r1-community-hyperv-part2

### 对既有已修补机制的再研究与负责任披露回路

起点：对较旧或被假定已移除/缓解的 CPU 与 OS 机制（LDT、call gate、描述符表、KASLR、ATI 驱动签名等）具备结构认知，源自 ReactOS 重写与书籍审阅积累。

练习与反馈：再研究被假定已修补的机制，主动交叉引用前置同行论文定位研究位置；在披露前与厂商协调，发现厂商未被通知时主动下架工具；将研究方法公开化以供他人复现。；MSRC 预提示“expect some changes in Windows 8.1”；Purple Pill 发现 ATI 未被告知缺陷后于 1 小时内主动下架，以 responsible disclosure 为由允许 ATI 修复；Black Hat 2008 报告 win32k.sys 四项本地 DoS 并指出其中一项存在 user→kernel 提权风险；call-gates 研究对照 j00ru 与 Gynvael Coldwind 的描述符表滥用论文及自身 Infiltrate 2015 AWE 攻击推进。

能力与结果：形成负责任披露判断力与将既有已修补机制作为研究对象、对照前置同行工作推进的能力；本机制不主张 Scott Field/Black Hat 2006 交叉引用与 lilhoser/myriachan/msuiche 致谢，因其未在 r1-community-blackhat2008-win32k 与 r1-community-kaslr-w81 抓取正文中出现（实际引用者为 j00ru 与 wj32）。；Bringing Call Gates Back：将已被厂商缓解的旧机制（Windows 10 周年更新移除 LDT 支持、PatchGuard 在 LDTR 寄存器加检查）作为对既有已修补机制的研究对象，对照 j00ru 与 Gynvael Coldwind 的前置论文推进；MSRC 在 Windows 10 周年更新堵住基于 LDT 的攻击向量。；KASLR Bypass Mitigations in Windows 8.1：Recon 演讲后与微软同事分享，获“expect some changes in Windows 8.1”预提示，作者评价微软内核安全团队“great work”。；Purple Pill：利用 ATI Vista x64 驱动缺陷加载未签名驱动，发现 ATI 未被告知后 1 小时内主动下架。；厂商修补对应关系主要为本人自述，缺少逐条 CVE 级可核验实体。

置信度：medium；替代解释：披露回路的厂商响应部分可归因于作者《Windows Internals》合著者身份与 CrowdStrike CTIO 职衔带来的 MSRC 通道，而非纯方法能力；与 MSRC 的具体漏洞披露往返记录（CVE 编号、披露时间线、修补版本对应关系）未取到一手证据，厂商修补对应关系为本人单向自述。

证据：aionescu-tl-2017-08-call-gates, aionescu-decisions-003, ai-works-02, r1-community-kaslr-w81, r1-community-purple-pill, r1-community-blackhat2008-win32k

### 自我范围蔓延的识别与以协作及工程证据纠偏

起点：单人范围扩展倾向：第六版期间同时兼顾学业、实习与人际关系导致严重倦怠与延期；近二十年固化于 WDM 非 PnP 驱动写法，并长期假定其优于 WDF。

练习与反馈：识别自身范围蔓延与技术假设模式并以协作或工程证据纠偏：第六版倦怠后承认延期由自身范围蔓延所致；第七版项目濒临流产时主动寻求合作者分担；以周末工程项目检验 WDM 假设，对照实际实现推翻长期误判。；自我承认范围蔓延导致延期（“I was once again, going to cause delays”）；具体代码行数对比（WDF 较 WDM 省 1500-4000 行 PnP 样板）；第七版合作者分担单人范围。

能力与结果：使其方法不被既有技术路径长期束缚，能够以新工程证据替换既有技术路径，并将范围蔓延约束为 12 个月可交付周期，与 Windows 发行窗口对齐。；第七版 Part 1 于 2017-05 发行，在 Windows 10 Redstone 2 发行数周内出版。；Hyper-V Bridge Part 1（2019-01-14）放弃近二十年 WDM 习惯改用 WDF，并公开记录动机与对比。；Hyper-V Bridge Part 2（2019-01-27）连载完成模糊测试桥系列。

置信度：medium；替代解释：第七版完成可归因于 Pavel Yosifovich 的贡献与出版社截稿压力，而非作者自我纠偏；WDF 迁移可归因于 Hyper-V 模糊测试驱动的特定项目需求；WDM→WDF 自我纠偏为单次记录，跨时期稳定性证据有限，可能为特定项目需求触发的一次性反思而非稳定实践。

证据：AI-conv-02, AI-conv-03, AI-conv-04, aionescu-decisions-001, aionescu-decisions-002, aionescu-tl-2017-05-wininternals-7e-p1, aionescu-tl-2019-01-hyperv-bridge, aionescu-ext-007

## 可迁移与不可迁移

- 可迁移：为所研究接口自建配套研究基础设施（驱动 + 用户态客户端 + INF），而非依赖厂商提供工具。
- 可迁移：以最小可用实现公开研究型工具并显式声明非生产级，区分研究工具与产品代码。
- 可迁移：再研究既有已修补机制时交叉引用前置同行论文（j00ru、Gynvael Coldwind、wj32）以定位研究位置。
- 可迁移：将范围蔓延约束为时间盒可交付周期（12 个月书籍周期对齐 Windows 发行窗口）。
- 可迁移：单人范围超出容量时主动招募合作者而非延长延期。
- 可迁移：以周末工程项目检验长期技术假设对照实际实现（WDM vs WDF 的 1500-4000 行样板对比）。
- 可迁移：负责任披露：发现厂商未被通知时主动下架工具（Purple Pill 1 小时下架）。
- 可迁移：连载式技术写作把研究方法公开化以供他人复现（Hyper-V Bridge Part 1/2）。
- 不可直接迁移：《Windows Internals》合著席位与 Solomon/Russinovich 师承及出版社关系——特定历史机遇，不可复制。
- 不可直接迁移：CrowdStrike CTIO 职衔带来的 MSRC 通道与会议舞台——职位依存。
- 不可直接迁移：ReactOS 时期多子系统重写经验——特定于该项目需求与当时 NT4→NT 5.2 目标的时期条件。
- 不可直接迁移：公开漏洞潮时机（2018 侧信道）使 SpecuCheck 获得相关性的时间窗口——议题热度依存。
- 不可直接迁移：近二十年 WDM 累积习惯——特定于作者代际与驱动开发时期。
- 不可直接迁移：WaaS 节奏迫使书籍难以及时跟进的外部条件——促成书→会议转型，非个人方法。
- 不可直接迁移：早期 ReactOS/BlueHat 时期（2006-2007）会议圈生态与今日不同——时期依存。

## 复核问题

- mechanisms[2] 将 'expect some changes in Windows 8.1' 与 'Windows 10 周年更新堵住基于 LDT 的攻击向量' 归于 MSRC 通道，超出所引证据。证据 r1-community-kaslr-w81 仅称 '微软同事'，未点名 MSRC；证据 aionescu-tl-2017-08-call-gates 仅记述 Windows 10 Anniversary Update 移除 LDT 支持，未将修补归因于 MSRC。'MSRC 通道' 系基于 CrowdStrike CTIO 职衔的推断，无抓取来源支撑，且与已作废的 alex-community-06（曾提 MSRC 致谢）存在概念重叠，构成未支撑的组织归属。
- stages[2].period 标注 '2009–2015'，但其 evidence_ids 引用 aionescu-ext-001（2017-05-05）、aionescu-ext-002（2017-05-11）、aionescu-decisions-001（2017-05-11）三条 2017 年证据，capability_change 与 stage 标题亦含第七版（2017）出版与复出叙述。阶段标签与所引证据年份不一致，属 round 1 曾要求修正的同类时间线归类错误的复发。
- mechanisms[2].feedback：将 'MSRC 预提示 expect some changes in Windows 8.1' 改为 '微软同事预提示 expect some changes in Windows 8.1'，与证据 r1-community-kaslr-w81 的 '微软同事' 表述一致，删除无来源的 MSRC 归属。
- mechanisms[2].observed_outcomes[0]：将 'MSRC 在 Windows 10 周年更新堵住基于 LDT 的攻击向量' 改为 'Windows 10 周年更新移除 LDT 支持、PatchGuard 在 LDTR 寄存器加检查（证据 aionescu-tl-2017-08-call-gates 所述，本人自述）'，删除无来源的 MSRC 执行者归属。
- mechanisms[2].alternative_explanation：将 'CrowdStrike CTIO 职衔带来的 MSRC 通道' 改为 'CrowdStrike CTIO 职衔与合著者身份可能带来的厂商内部联系'，将组织归属限定为推断并标注为推断，而非既证事实。
- stages[2].period：将 '2009–2015' 调整为 '2009–2017'，或将 aionescu-ext-001、aionescu-ext-002、aionescu-decisions-001 三条 2017 年证据及其承载的第七版出版/复出叙述移至 stages[3]，消除阶段标签与所引证据年份不一致。
- stages[3].capability_change：删除 '自述近年将公开研究重心迁移至 infosec 会议圈' 中的 '重心迁移'，改为 '自述近年将公开研究输出转向 infosec 会议圈'，落实 round 1 与 round 2 已要求但未完成的去比喻修订。
- mechanisms[2].intermediate_capability：删除 '本机制不主张 Scott Field/Black Hat 2006 交叉引用与 lilhoser/myriachan/msuiche 致谢，因其未在 r1-community-blackhat2008-win32k 与 r1-community-kaslr-w81 抓取正文中出现'，该句含内部证据 ID 与 '抓取正文' 过程语言，属修订记录元叙述进入结论正文。如需保留否定范围，改写为不含过程语言与内部 ID 的客观陈述，如 '本机制不主张与 Black Hat 2006 演讲的交叉引用，以及 lilhoser、myriachan、msuiche 在相关文章中的致谢，因相关一手文章正文未出现该内容'。
- stages[2].evidence_ids 中 aionescu-tl-wininternals-6e-college：保留该证据但将其日期精度限制写入 stages[2].capability_change，标注 '第六版倦怠主张的证据日期为占位符，精确出版日期未核证'；或以已核验的 AI-conv-02（2017-05-11）替代该证据支撑同一主张。

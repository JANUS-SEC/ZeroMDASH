# Dmitry Nedospasov：漏洞研究成长分析

- 擅长领域：硬件与故障注入漏洞
- 独立复核：pass · 86/100

## 成长阶段

- **2010-2012 · 开源工具建设起点：从通用软件到嵌入式工具链**：可核验的最早公开活动为 2010 年 GitHub fork xen-tools（Xen 虚拟化工具），随后在 2012-2013 年间 fork 或维护 dfu-programmer（README 标注原项目已无维护）、USB-XMEGA、lpcflash、ddk-arm、ddk-fpga 等嵌入式与烧录工具。这一阶段的工作集中于 AVR/XMEGA 与 ARM Cortex-M 工具链，行为特征为在遇到缺失或停滞的工具时自行 fork 并维护，以工具建设为研究起点而非纯研究产出。2012 年与 pda_aes 仓库同步公开 AES 侧信道采集实现，编译目标 photon 仅执行 AES 首轮，配合 ROUNDS/DELAY/STARTUP 宏用于侧信道采集，将工具建设与学术实验实现绑定。（置信度：high）
  - 证据：dn-dec-001, nedos-works-002, nedos-works-001
- **2013-2017 · 学术物理分析与本地硬件社区并行的能力形成期**：2013 年以合作者身份发表 Simple photonic emission analysis of AES 与 Differential photonic emission analysis，方法为通过芯片光子发射对 AES 进行侧信道分析，从 pda_aes 的实现产出推进到方法学论文，构成从实现到方法学产出的对应关系。2015 年以唯一作者完成 Security of the IC Backside，主题聚焦 IC 背面物理安全，继续在 IC 背面物理安全方向开展物理分析。同期在柏林参与 Die Datenkrake（@ddk）本地硬件/嵌入式开源组织，发布 ddk-hardware、lpcflash、ddk-arm，并在 2014 年起扩展到 FPGA/Verilog 方向（ddk-fpga、arty-passthrough、icestorm-build、litex-boards），形成以 ARM 微控制器与 FPGA 为核心的硬件工具建设主线。该阶段同时存在学术物理分析产出与本地社区同伴/项目载体两条并行线，但缺乏导师、训练路径与失败案例的一手叙述（见 open_questions）。（置信度：medium）
  - 证据：nedos-works-003, nedos-works-004, nedos-works-001, dn-dec-002, dn-dec-003, nedos-community-002-public-repos-research-artefacts
- **2018-2019 · 硬件钱包漏洞披露与三人团队协作**：2018 年 12 月 27 日在 35C3（莱比锡）以 wallet.fail 项目公开披露主流加密货币硬件钱包的安全缺陷，与 Thomas Roth、Josh Datko 结成稳定的三人协作团队。媒体库正文将攻击分为 firmware / software / hardware / physical / architectural 五类，并提及 physical attacks including glitching 以绕过 IC 内实现的安全机制，部分问题仅能在未来硬件修订中修复。同期 walletfail 组织公开 bloomburgular（RF 触发的硬件植入物/绕过：检测特定射频信号即拉低输出 GPIO，标注 Requires zero firmware、Bypasses a core security function）与 lascar（fork 自 Ledger-Donjon 的侧信道分析库），并 fork keepkey-firmware，表明 wallet.fail 披露后继续在同一目标上投入。需明确：bloomburgular 为 RF 触发的硬件植入物/硬件绕过，并非电压/时钟故障注入（glitch）工具；glitching 仅作为 wallet.fail 项目整体物理攻击范围在 35C3 议题正文中被提及。该阶段目标难度从 AES 实现分析与 IC 背面物理安全提升到对量产安全产品的整体攻击面展示，并从独立/小范围协作转为稳定三人团队。（置信度：high）
  - 证据：timeline-01-35c3-walletfail, timeline-02-walletfail-project, dn-conv-01, nedos-works-006, nedos-community-003-walletfail-org-collaboration, nedos-community-004-35c3-walletfail-talk, dn-dec-004, dn-dec-005
- **2025-2026 · AI/LLM 方向扩展与研究方法向培训商业化的转化**：2025-2026 年个人仓库出现 qwen3-tts-service、winuse（Windows 自动化 API/CLI for agents）、linuse、tamashii-backend、SageAttention fork、ComfyUI-CSM-Nodes fork 等，GitHub 自述更新为 AI/Hardware security expert。据其 GitHub 主页自述创立 @comput3ai（创办时间未证实，status=inferred；r3-comput3ai-org 抓取证实 @comput3ai 组织真实存在、方向为 AI agent 推理/计算层，但组织页无公开成员、未列示 nedos/Nedospasov，创始人身份仍仅靠 GitHub bio 自述支持）。与其自述限定分开陈述的事实是：在 advancedsecurity.training 作为 trainer 开设 Glitching and Fault Injection、FPGAs and Verilog in 1 Day、AI and LLMs for Security Professionals 三门课程（timeline-04，documented）。该阶段技术栈由纯硬件侧信道/glitch 扩展到 AI agent 自动化与语音模型服务，并将 AI 能力与既有硬件安全/FPGA 能力结合为商业化培训，体现研究者到训练提供者的角色转变。但 AI 方向与早期硬件故障注入漏洞挖掘之间的成长衔接（是否仍做硬件漏洞研究、AI 工具是否用于硬件安全）无一手材料，无法判断是方向转移还是工具扩展（见 open_questions）。（置信度：medium）
  - 证据：nedos-works-008, dn-dec-006, dn-dec-007, timeline-03-github-profile, timeline-04-advancedsecurity-training, timeline-06-comput3ai-founder, nedos-community-001-github-profile, dn-ext-01, r3-comput3ai-org

## 主要成长机制

### 因工具缺口而 fork 或自建工具链

起点：2010 年起以 GitHub 账户 nedos 公开维护活动，可核验最早记录为 fork xen-tools（Xen 虚拟化工具）。早期公开仓库覆盖 AVR/XMEGA、ARM Cortex-M、FPGA 等嵌入式与烧录工具方向，但配套工具链存在缺失或停滞（如 dfu-programmer README 标注原项目已无维护）。

练习与反馈：2012-2013 年 fork 并维护 dfu-programmer、USB-XMEGA、lpcflash、ddk-arm、ddk-fpga；2013 年在柏林 Die Datenkrake（@ddk）本地社区发布 ddk-hardware、lpcflash、ddk-arm；2014 年起扩展到 FPGA/Verilog（ddk-fpga、arty-passthrough、icestorm-build、litex-boards）；2019 年 fork keepkey-firmware；2025-2026 年扩展到 AI 方向（winuse/linuse agent 自动化、qwen3-tts-service、SageAttention fork、ComfyUI-CSM-Nodes fork）。行为特征为遇到目标硬件所需的工具缺失或停滞时，自行 fork 并维护而非重新实现已有工具。；主要反馈来自公开代码托管平台上的可见仓库与组织成员身份（@ddk、@walletfail），以及 Pull Shark x2 等贡献徽章。但 issue/PR 讨论原文、厂商响应与同伴评价在抓取材料中普遍缺位，反馈回路接收端证据不足，仅能确认产出发布行为本身。

能力与结果：形成围绕目标硬件（硬件钱包固件、FPGA、嵌入式 MCU 工具链）的 fork 与自建工具建设习惯，并以公开 fork 向社区提供复现材料与协作入口。这一能力从早期嵌入式工具延续到 FPGA/Verilog 与后续 AI agent 工具，体现工具建设习惯的跨时期重复。；2012-2013 年建立 dfu-programmer/USB-XMEGA/lpcflash/ddk-arm/ddk-fpga 工具链支撑后续侧信道/glitch 研究；2013-2017 年通过 @ddk 本地社区载体建立 ARM 微控制器与 FPGA 工具线；2019 年 fork keepkey-firmware，在 wallet.fail 披露后继续在硬件钱包方向投入；2025-2026 年以 winuse/linuse 等 agent 自动化工具延续工具建设习惯，方向扩展到 AI/LLM

置信度：medium；替代解释：公开 fork 集中于工具缺口目标，也可能反映简历展示动机或个人维护兴趣，而非能力形成的因果路径；由于缺乏失败/放弃案例对照与 issue/PR 协作原文，无法排除以公开产出直接当作能力证据的幸存者偏差。

证据：nedos-works-002, nedos-works-008, nedos-community-002-public-repos-research-artefacts, dn-dec-001, dn-dec-002, dn-dec-003, dn-dec-005, dn-dec-006

### 物理层硬件攻击主题的相邻演进（时间相邻推断，非一手方法迁移）

起点：2012 年公开 pda_aes（Photon-DA AES Implementation），README 说明用于 2012 CHES 论文及后续工作，编译目标 photon 仅执行 AES 首轮，配合 ROUNDS/DELAY/STARTUP 宏用于侧信道采集，方向为 AES 实现的侧信道采集。

练习与反馈：2013 年发表 Simple photonic emission analysis of AES 与 Differential photonic emission analysis（光子发射侧信道，观测型）；2015 年以唯一作者完成 Security of the IC Backside（IC 背面物理安全）；2018 年通过 wallet.fail 与 bloomburgular 进入量产安全产品的整体攻击面展示，bloomburgular 为 RF 触发的硬件植入物/硬件绕过（检测特定射频信号即拉低输出 GPIO 以绕过核心安全功能，标注 Requires zero firmware）。需明确区分：光子发射分析（观测型侧信道）、电压/时钟故障注入 glitch（主动故障注入）、RF 触发型 GPIO 植入（硬件绕过）为不同物理机制，三者之间无一手记录的方法跨越机制迁移。；反馈来自 2018 年 35C3 媒体库的观看量（32.7k）与多语字幕构成的传播信号，以及 walletfail 组织成员身份与 lascar fork 自 Ledger-Donjon 侧信道分析库构成的跨团队工具借用。但厂商反馈、issue/PR 讨论与具体被攻击钱包品牌的一手核验在材料中缺位。

能力与结果：形成按时间线相邻推断的物理层硬件攻击能力主线：从 AES 实现侧信道采集、IC 背面物理分析，到硬件钱包整体攻击面与 RF 触发硬件植入物/绕过。该主线为依据时间相邻关系推断，而非一手记录的单一方法跨越机制迁移。；pda_aes 工具与 2013 年光子发射论文构成从实现到方法学产出的对应关系；2015 年 Security of the IC Backside 作为学术阶段收束点；2018 年 bloomburgular 以 RF 触发硬件植入物/绕过形式公开发布，体现研究产出即工具的公开发表习惯；2018 年 35C3 wallet.fail 议题将物理攻击（含 glitching）作为项目整体攻击范围披露

置信度：low；替代解释：物理层硬件攻击主题在时间线上相邻，可能反映同一研究者在相邻时期对物理层主题的持续兴趣，而非一手记录的方法迁移；由于 nedos.net 本人站点不可达（TLS 证书 SAN 不匹配）、无访谈/AMA 一手文本、WebSearch 摘要姓名反复误写不可采信，定向搜索未发现可证实方法迁移的一手来源，方法迁移是否真实存在仍为缺口。

证据：nedos-works-001, nedos-works-003, nedos-works-004, nedos-works-006, nedos-community-004-35c3-walletfail-talk, timeline-01-35c3-walletfail, timeline-04-advancedsecurity-training

### 公开发表与开源发布作为研究产出渠道

起点：2013 年起以合作者身份在 Journal of Cryptographic Engineering / Springer 发表光子发射分析论文，建立学术发表产出渠道。

练习与反馈：2013 年发表学术论文；2018 年以 wallet.fail 项目站点组织漏洞披露并建立预警订阅机制，关联 Keylabs 与 Advanced Security Training；同期 walletfail 组织公开 bloomburgular（RF 触发硬件植入物/绕过）与 lascar fork（跨团队工具借用）；2018 年 35C3 议题为公开披露里程碑；后续在 advancedsecurity.training 以 trainer 身份提供课程。行为特征为将研究产出通过会议披露、项目站点、开源仓库与培训平台多渠道公开发布。；反馈来自 35C3 官方媒体库的高观看量与多语字幕（传播信号）、wallet.fail 项目站点的预警订阅机制、以及 Keylabs 与 Advanced Security Training 的团队关联。但学员评价、厂商响应与具体钱包品牌反馈在材料中缺位，传播量仅作传播信号，不直接等同于能力证据。

能力与结果：形成以公开发表与开源发布为研究产出渠道的习惯，从学术论文扩展到会议披露、项目站点、开源仓库与培训平台，使研究产出在公开披露之外获得另一条商业化路径（培训）。需注意该商业化路径的成立时间与商业规模仅来自 GitHub bio 与培训平台页自述，无独立一手来源交叉验证。；2013 年光子发射分析论文构成学术发表产出；2018 年 wallet.fail 项目站点与 35C3 议题构成公开披露里程碑；2018 年 walletfail 组织公开 bloomburgular 与 lascar fork；advancedsecurity.training 三门课程构成研究产出向培训的转化

置信度：medium；替代解释：公开发表与开源发布渠道的连续性可能反映行业惯例（安全研究普遍以会议披露与开源发布为产出方式）而非个人特有能力；35C3 观看量与多语字幕属传播量信号，存在知名度/传播量偏差，不能直接当作能力形成的因果证据。

证据：nedos-works-003, nedos-works-006, nedos-community-003-walletfail-org-collaboration, nedos-community-004-35c3-walletfail-talk, timeline-01-35c3-walletfail, timeline-02-walletfail-project, timeline-04-advancedsecurity-training, dn-dec-004

### 研究产出向培训商业化的转化

起点：2018 年 wallet.fail 披露后，在硬件钱包、glitching/fault injection 与 FPGA/Verilog 方向积累公开产出（bloomburgular、lascar fork、keepkey-firmware fork），具备可转化为教学材料的研究成果基础。

练习与反馈：2026 年据其 GitHub 主页自述创立 @comput3ai（status=inferred，创办时间未证实），并在 advancedsecurity.training 作为 trainer 提供 Glitching and Fault Injection（教授对真实硬件目标的故障注入）、FPGAs and Verilog in 1 Day、AI and LLMs for Security Professionals 三门课程（timeline-04 documented）。行为特征为将故障注入与 FPGA/Verilog 硬件开发经验产品化为培训课程，并将 AI/LLM 能力与既有硬件安全/FPGA 能力整合而非放弃后者。；反馈来自 advancedsecurity.training 平台页的课程描述（short quote: how to glitch real-world hardware targets），以及 GitHub 主页对 trainer 身份的自述。但学员评价、培训商业规模与 @comput3ai 创办时间在材料中无独立一手来源。

能力与结果：形成将研究产出转化为可重复练习与教学材料的能力，使研究产出在公开披露之外获得另一条商业化路径（培训）。需区分：trainer 三门课程有 timeline-04（documented）支撑；@comput3ai 创始人身份仅靠 GitHub bio 自述支持（inferred），r3-comput3ai-org 仅证实组织真实存在与方向一致性，未能在组织页独立列示其为成员或所有者。；advancedsecurity.training 提供 Glitching and Fault Injection、FPGAs and Verilog in 1 Day、AI and LLMs for Security Professionals 三门课程；据 GitHub bio 自述创立 @comput3ai（inferred），r3-comput3ai-org 证实组织存在与方向为 AI agent 计算层；课程组合同时覆盖硬件故障注入与 AI 安全，与 GitHub 自述方向一致

置信度：low；替代解释：培训商业化可能反映行业常见的成果变现路径（资深研究者转向培训），而非个人特有机制；@comput3ai 创始人身份未独立交叉验证，存在以自述作既定事实的组织声誉偏差，r3-comput3ai-org 仅证实组织存在与方向一致性，不能据此升级创始人身份为 documented。

证据：nedos-works-008, dn-dec-006, dn-dec-007, timeline-04-advancedsecurity-training, timeline-06-comput3ai-founder, r3-comput3ai-org

## 可迁移与不可迁移

- 可迁移：在遇到目标硬件所需工具缺失或停滞时，自行 fork 并维护而非重新实现已有工具，并以公开 fork 向社区提供复现材料与协作入口。
- 可迁移：将研究产出通过会议披露、项目站点、开源仓库与培训平台多渠道公开发布，使研究成果获得公开披露之外的传播与转化路径。
- 可迁移：将故障注入、FPGA/Verilog 等研究成果产品化为可重复练习的培训课程，整合既有硬件安全能力与新方向（AI/LLM）能力而非放弃后者。
- 可迁移：以稳定团队协作（如 Roth/Nedospasov/Datko 三人组合）在大规模公开会议上披露硬件产品整体攻击面，覆盖 firmware/software/hardware/physical/architectural 多类漏洞。
- 可迁移：对 RF 触发型 GPIO 植入物等硬件绕过方法，以开源仓库形式公开 BOM 与测试条件（如 433MHz 17cm 天线配合 50W 发射机），使研究产出同时具备可复现性。
- 不可直接迁移：柏林 Die Datenkrake（@ddk）本地硬件/嵌入式开源社区作为同伴与项目载体，属特定地域与时期的组织资源，非个人可迁移能力。
- 不可直接迁移：与 Thomas Roth、Josh Datko 结成的稳定三人协作团队，以及通过 walletfail 组织与 Ledger-Donjon 侧信道分析库的跨团队工具借用回路，依赖特定团队关系而非个人可单独复现的条件。
- 不可直接迁移：35C3 作为大规模公开会议的传播渠道与 media.ccc.de 官方媒体库的高观看量/多语字幕，属特定时期与会议平台的外部条件，非个人能力。
- 不可直接迁移：advancedsecurity.training 作为培训平台的商业化渠道与 @comput3ai 组织（据 GitHub bio 自述创立，inferred），依赖平台与组织身份等个人特有条件。
- 不可直接迁移：nedos.net 本人站点作为 writeup_evidence 的可达性（当前因 TLS 证书 SAN 不匹配不可达），属个人站点可用性条件，影响一手叙述可核验性。

## 复核问题

- 字段 mechanisms[0].observed_outcomes[0]：将'建立 dfu-programmer/USB-XMEGA/lpcflash/ddk-arm/ddk-fpga 工具链支撑后续侧信道/glitch 研究'改为方向一致的中性表述，如'建立 dfu-programmer/USB-XMEGA/lpcflash/ddk-arm/ddk-fpga 工具链，方向与后续侧信道/glitch 研究一致'，删除未被一手证据支持的'支撑'因果供给表述。仅改措辞，不新增实证主张。
- 字段 stages[1]（2013-2017）capability_change：将 litex-boards 从 2013-2017 阶段的 FPGA/Verilog 方向列举中移出，或在该阶段内仅保留 2014 年起的 ddk-fpga、arty-passthrough 等 2013-2017 时段内的项目；将 litex-boards（2023-08 fork，证据 dn-dec-003）作为跨阶段 FPGA 能力线的延续项，置于 stages[3] 或 stages[4] 对应时段，或单独说明其属跨时段合并陈述。仅调整时间线归属，不新增证据。

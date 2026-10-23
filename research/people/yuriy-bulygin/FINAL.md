# Yuriy Bulygin：漏洞研究成长分析

- 擅长领域：UEFI 与硬件信任根漏洞
- 独立复核：pass · 89/100

## 成长阶段

- **2006-2008 · 起步期：恶意软件建模与驱动/芯片组层下移**：研究起点为 IEEE IPCCC Malware 2006 的闪存蠕虫传播数学建模，与固件/漏洞方向无直接衔接；2007 年在 Black Hat USA 发表网卡驱动远程与本地利用，目标从行为模型下移到驱动层代码，确立论文+幻灯片+演示视频的公开习惯；2008 年在 Black Hat USA 与 David Samyde 合著芯片组/虚拟化 rootkit 检测，首次发布可复现的 PoC 源码包（hyper-channel_v0.1.tar），研究目标上移到芯片组固件与 CPU 微架构侧信道，并首次引入合著协作。该阶段形成由建模到实测利用、由驱动层到芯片组层的逐层下移路径，而非从硬件信任根直接起步。（置信度：high）
  - 证据：yb-works-01-flash-worms-2006, yb-works-02-network-drivers-bh-2007, yb-works-03-rootkit-detection-bh-2008, yb_tl_01, yb_tl_02, yb_tl_03
- **2009（及其后 Intel 时期早期） · Intel 机构期早期：企业渠道与硬件层检测延续**：2009 年以 Intel 身份在 Intel Technology Journal 第 13 卷第 2 期发表《Enhanced Detection of Malware》，研究主线延续 2008 年的硬件层检测，发表渠道由会议转入企业内部技术期刊，显示已身处 Intel 体系从事平台安全研究。一手作品索引（c7zero.info，页脚 ©2008-2017）记载 2010、2011、2012 三年『No publications or talks are listed for these years』，即该索引上该三年无可见公开产出，存在时间线断点；本阶段范围依据 2009 年作品外加 2013 年前作品年份外推，非连续证据区间。（置信度：medium）
  - 证据：yb-works-04-intel-2009-malware-detection, yb_tl_04, r2-c7zero-2010-2012-publication-gap
- **2013-2015 · 收敛期：UEFI Secure Boot/TPM 信任根与 SMM/Hypervisor 横向扩展**：2013 年在 CanSecWest 与 Black Hat USA 发表围绕 UEFI Secure Boot 与 TPM/FDE 信任根的工作，形成与 Furtak、Bazhaniuk 的稳定三人合著组合；2014 年 3 月在 CanSecWest 首发 CHIPSEC 平台安全评估框架，把此前手工进行的固件测试转化为可复用开源平台，并与 MITRE 联合署名，出现跨机构协作。2015 年在 CanSecWest 提出 SMI Handler 新漏洞类，并在 Black Hat USA/DEF CON 23 把目标从 UEFI/Secure Boot 扩展到通过固件攻击虚拟机管理程序；SMI 幻灯片正文大量引用 Duflot、Wojtczuk 与 Phrack，显示学术化复盘与前人工作对照习惯。该阶段研究规模仍以单点漏洞与单一子系统为主。（置信度：high）
  - 证据：yb-works-05-secure-boot-bh-2013, yb-works-06-chipsec-csw-2014, yb-works-07-smi-handlers-csw-2015, yb_tl_05, yb_tl_06, yb_tl_07, yb_tl_08, yb_tl_09, yb-dec-01, yb-community-01-chipsec-release-2014, yb-community-04-recurring-coauthors
- **2017 · 规模化期：批量固件扫描与跨架构，兼及上游公告**：2017 年为密集高产阶段，研究规模从单点漏洞扩展到批量 UEFI 固件扫描（量级未在 fetched 正文中核验），并把 Coreboot 等非 Intel 实现与 ARM hypervisor/TrustZone 纳入目标范围，攻击目标推进到 Windows 10 VBS/Credential Guard；通过多场会议（Black Hat USA、44CON、RECon Brussels）密集产出。同期发布 BERSerk 漏洞分析并维护 Tianocore/edk2 上游安全公告，进入负责任披露与上游反馈环节。同年 c7zero.info 页脚 ©2008-2017，个人一手研究索引在该年出现可核验终点，其后产出归入机构署名。（置信度：medium）
  - 证据：yb-works-08-fractured-backbone-bh-2017, yb-works-09-berserk-tianocore-2017, yb_tl_10, yb_tl_11, yb-dec-03, yb-dec-04, yb-ext-01, yb-ext-03, r2-eclypsium-founded-2017
- **2017 后 · 角色迁移期：个人署名产出转机构署名，研究方法产品化**：Bulygin 与 Intel 同事 Alex Bazhaniuk 于 2017 年共同创立 Eclypsium，离开 Intel 内部研究岗位转为公司化运营；Eclypsium 研究页与 2026 年多篇高调文章（FIRESTARTER、YellowKey、FortiBleed）署名均为 Paul Asadoorian 而非 Bulygin，YellowKey 正文以『Bulygin, Furtak, and Bazhaniuk』引用其 2013 年工作并将其定位为历史研究者；c7zero.info 个人作品索引止于 2017 年，未列 Eclypsium 时期个人署名 writeup。可见产出形态由 2006-2017 年连续个人署名高频产出，转为公司/团队署名，公开作品主线交由他人署名。该阶段能力变化的因果判断受限于无第一人称自述，机制层归因不可与产出可见度分离，conversations 维度 items 为空。（置信度：low）
  - 证据：yb-works-10-eclypsium-post-2017-no-personal-byline, yb-dec-03, yb-dec-05, yb-ext-01, yb-ext-04, yb_tl_11, yb_tl_12, r2-eclypsium-founded-2017

## 主要成长机制

### 研究目标由抽象模型逐层下移到硬件信任根

起点：2006 年起步于 IEEE IPCCC Malware Workshop 的闪存蠕虫传播数学建模，与漏洞挖掘或固件安全无直接衔接；早期训练的是系统行为建模与分析，而非利用开发。

练习与反馈：2007 年把目标下移到网卡驱动漏洞的实测利用，2008 年上移到芯片组固件与 CPU 微架构侧信道检测虚拟化 rootkit，2009 年在企业期刊延续硬件层恶意软件检测，2013 年收敛到 UEFI Secure Boot 与 TPM/FDE 信任根，2015 年扩展到 SMI Handler 漏洞类与通过固件攻击虚拟机管理程序；研究对象沿『网络蠕虫模型 → 驱动层 → 芯片组/微架构 → UEFI/Secure Boot/TPM → SMM/Hypervisor』路径反复推进。；反馈主要来自会议同行评审与公开披露：2007 年起持续在 Black Hat、CanSecWest、DEF CON、RECon 等场合发表，2008 年起以合著形式接受同行协作评审，2015 年 SMI 幻灯片正文大量引用 Duflot、Wojtczuk 与 Phrack 等前人工作，形成学术化复盘与前人工作对照。缺乏本人第一人称自述反馈来源，反馈渠道仅能从公开产出与合著网络间接推断。

能力与结果：形成从抽象行为模型迁移到具体底层系统攻击与防御的能力，能够在驱动层、芯片组层、UEFI/Secure Boot 层、SMM 层、Hypervisor 层之间切换目标，并具备以『检测/防御』视角补充『攻击』视角的能力（2008 年 DeepWatch PoC）。；2008 年首次发布可复现的 PoC 源码包（hyper-channel_v0.1.tar），由仅给演示转向给源码。；2013 年 Windows 8 Secure Boot 全软件绕过被 c7zero.info 索引列为 2013 年后的公开研究主题之一。；2015 年提出 SMI Handler 新漏洞类并通过固件攻击 Hypervisor，技术栈上移到跨信任层联动。；2017 年研究规模从单点漏洞扩展到批量 UEFI 固件扫描（量级未在 fetched 正文中核验），目标覆盖 Coreboot 与 ARM。

置信度：medium；替代解释：目标逐层下移既可归因于个人主动选择，也可归因于 Intel/McAfee 机构平台使其持续接触芯片组与固件层一手资料、同期行业对 UEFI/Secure Boot/SMM 关注度上升带来的选题驱动；二者不可完全分离，个人选择与机构资源共同贡献。validation_tests 取 repeated（跨年度、跨会议重复出现下移行为）与 generative（产生可复用 PoC 与新漏洞类），不主张个人独有性。

证据：yb-works-01-flash-worms-2006, yb-works-02-network-drivers-bh-2007, yb-works-03-rootkit-detection-bh-2008, yb-works-04-intel-2009-malware-detection, yb-works-05-secure-boot-bh-2013, yb-works-07-smi-handlers-csw-2015, yb-works-08-fractured-backbone-bh-2017, yb_tl_01, yb_tl_02, yb_tl_03, yb_tl_04, yb_tl_05, yb_tl_08, yb_tl_10

### PoC 源码到开源工具的产出循环

起点：2008 年首次随讲发布可复现的 PoC 源码包（hyper-channel_v0.1.tar），公开习惯由论文+幻灯片+演示扩展到源码；此前研究产出以一次性演示为主。

练习与反馈：2014 年 3 月在 CanSecWest 首发 CHIPSEC 平台安全评估框架，把此前手工进行的固件测试转化为可复用开源平台；其后持续向社区发布改进与新增能力（易用性改进、ARM 支持、SMC fuzzer 等新模块规划），在 CanSecWest 2017 仍以 CHIPSEC 发现固件、Hypervisor 与硬件配置漏洞；约 2017 年前后维护 Tianocore/edk2 上游安全公告（据 c7zero.info 自述，具体公告编号与上游采纳结果未核验）。；反馈来自开源社区评审与合并流程：GitHub 用户 c7zero 为 chipsec 组织成员，拥有 Pull Shark x2（至少 2 个被合并的拉取请求）与 Arctic Code Vault Contributor 徽章；工具在会议首发并被持续用于公开披露研究（CanSecWest 2014、2017）。Tianocore 安全公告的具体编号、提交时间与上游采纳结果在抓取材料中未核验，反馈回路仅以自述一句话提及。

能力与结果：形成由一次性 PoC 转向系统化、可复用工具建设的能力，把反复手工进行的固件测试转化为开源平台，使方法可被他人重复与扩展，并接入上游负责任披露环节。；CHIPSEC 首版于 2014 年 3 月发布并公告于 CanSecWest 2014，GitHub README 记载联系邮箱为 chipsec@intel.com，由 Intel 发布。；CHIPSEC 在 2014-2017 年间持续迭代并向社区发布新增能力。；向 Tianocore（EDK II/UEFI）上游提交若干安全公告（据 c7zero.info 自述，具体公告编号与上游采纳结果未核验）。；2017 年 Black Hat Fractured Backbone PDF 元数据 created 2017-07-26，致谢 Intel 的 John Loucaides，显示工具被持续用于公开披露研究。

置信度：medium；替代解释：开源工具循环既可归因于个人工具建设习惯，也可归因于 Intel 提供机构平台（chipsec@intel.com、Intel 内部资源）与 Intel+MITRE 协作环境使开源工具建设成为可行路径；个人方法形式与机构平台贡献不可分离。validation_tests 取 repeated（CHIPSEC 2014-2017 持续迭代）与 generative（产生可复用开源平台），不主张个人独有性。

证据：yb-works-03-rootkit-detection-bh-2008, yb-works-06-chipsec-csw-2014, yb-works-09-berserk-tianocore-2017, yb-dec-01, yb-dec-04, yb_tl_06, yb_tl_10, yb-community-01-chipsec-release-2014, yb-community-02-chipsec-org-membership, yb-community-03-tianocore-advisories, yb-ext-02

### 稳定合著网络驱动的系列化产出

起点：2008 年首次与 David Samyde 合著芯片组/虚拟化 rootkit 检测，引入合著协作；2009 年以 Intel 身份在 Intel Technology Journal 合著《Enhanced Detection of Malware》，处于 Intel 体系内。

练习与反馈：2013-2017 年间在 Black Hat、DEF CON、CanSecWest、RECon、SOURCE、McAfee FOCUS、44CON、Latincrypt 等场合反复与同一批合著者合作：Oleksandr Bazhaniuk、Mikhail Gorobets、Andrew Furtak、John Loucaides、Alexander Matrosov、Mikhail Shkatov，早期亦与 David Samyde、Steve Grobman 合作；2013 年起形成 Bulygin-Furtak-Bazhaniuk 稳定三人组，2014 年与 MITRE 联合署名，2017 年与 Intel 同事 Alex Bazhaniuk 共同创立 Eclypsium。；反馈来自合著者之间的互相评审与分工互补，以及会议同行评审；GitHub chipsec 组织成员身份与被合并 PR 体现通过代码贡献接入开源社区评审流程。稳定的协作关系是重复练习、交叉验证与联合产出的组织基础。缺乏本人第一人称自述反馈细节，协作反馈渠道仅能从合著署名与组织成员身份间接推断。

能力与结果：形成借助稳定同伴网络把单点研究扩展为系列成果的能力，使同一方法可在不同子系统（Secure Boot、SMM、Hypervisor、Coreboot）与不同架构（x86、ARM）间复用，并由研究团队转为联合创始人角色。；2013-2017 年间跨多个会议与年度重复出现同一批合著者组合，构成稳定的固件/虚拟化安全研究团队。；2015 年年度内同时覆盖 SMI Handler、Hypervisor、VMM 指纹、ASN.1 等多个子系统并保持与同一批 Intel 同事反复合著。；2017 年与 Intel 同事 Alex Bazhaniuk 共同创立 Eclypsium，同伴网络延续到公司化运营。；2015 年 S3 Resume Boot Script 漏洞分析被用于复盘 Hacking Team 恶意代码的 UEFI 持久化机制，显示同伴网络产出被外部安全事件反向驱动。

置信度：medium；替代解释：稳定合著网络的延续性既可归因于个人协作能力，也可归因于 Intel/Intel ATR 约十年的机构平台使其能与同一批同事持续合作，以及 Eclypsium 创办带来的组织延续；同伴网络的延续与方法形式成因不可与机构平台贡献分离。validation_tests 取 repeated（跨年度、跨会议重复合著）与 generative（由合著产出公司化路径），不主张个人独有性。

证据：yb-works-03-rootkit-detection-bh-2008, yb-works-05-secure-boot-bh-2013, yb-works-06-chipsec-csw-2014, yb-works-08-fractured-backbone-bh-2017, yb_tl_03, yb_tl_05, yb_tl_06, yb_tl_07, yb_tl_08, yb_tl_09, yb_tl_10, yb-dec-03, yb-community-02-chipsec-org-membership, yb-community-04-recurring-coauthors, yb-community-05-sustained-output-2007-2017, yb-ext-01, r2-eclypsium-founded-2017

## 可迁移与不可迁移

- 可迁移：把反复手工进行的研究流程转化为可复用的开源工具（CHIPSEC），并通过会议首发与持续迭代向社区输出，使方法可被他人重复与扩展。
- 可迁移：在公开披露中采用论文+幻灯片+演示视频+PoC 源码的多件套形式，自 2007 年起重复使用，提高研究产出的可复现性。
- 可迁移：在研究过程中引用前人工作（如 2015 年 SMI Handler 幻灯片引用 Duflot、Wojtczuk、Phrack）进行学术化复盘与前人工作对照，而非孤立发明。
- 可迁移：向上游开源固件参考实现（Tianocore/edk2）提交安全公告以接入负责任披露与上游反馈回路（据 c7zero.info 自述，具体公告编号与上游采纳结果未核验）。
- 可迁移：曾以 S3 Resume Boot Script 漏洞分析复盘 Hacking Team 恶意代码 UEFI 持久化机制（yb_tl_09），为单次研究到野外样本复盘的事件，尚不构成可重复迁移的方法。
- 不可直接迁移：Intel / Intel ATR 约十年的机构平台，使其能持续接触芯片组与固件层一手资料，并与 Alex Bazhaniuk 及稳定合著网络形成同事关系；该平台与同事关系为时期特定的机构条件，非可普遍迁移的个人做法。
- 不可直接迁移：CHIPSEC 由 Intel 发布（联系邮箱 chipsec@intel.com）并获 MITRE 跨机构协作，开源工具建设依托于 Intel 机构资源与跨机构协作环境，非个人可独立复制的条件。
- 不可直接迁移：Eclypsium 创办（2017 年与 Alex Bazhaniuk）将研究方法产品化与商业化，公司化运营为其后期产出形态提供组织条件，非个人研究方法本身的可迁移部分。
- 不可直接迁移：早期（2006-2009）受雇机构、学历与导师关系在抓取到的一手来源中均未给出，留作资料缺口，无法判断哪些早期条件可迁移。

## 复核问题

- mechanism 3（稳定合著网络驱动的系列化产出）observed_outcomes 第 4 条「2015 年 S3 Resume Boot Script 漏洞分析被用于复盘 Hacking Team 恶意代码的 UEFI 持久化机制，显示同伴网络产出被外部安全事件反向驱动」：该条依据 yb_tl_09（S3 Resume Boot Script 漏洞分析）说明的是漏洞发现向真实样本复盘的反馈，属 mechanism 1（PoC/工具循环）或机制层面的反馈回路，而非「稳定合著网络」机制本身的产出。建议将该条移至 mechanism 1 的 observed_outcomes 或 feedback，或改写为说明合著网络在该复盘事件中的具体协作作用（如合著者名单与分工），以消除 evidence_id 到 mechanism 的因果框架偏移。
- stage 4 stage 字段「规模化期：批量固件扫描与跨架构，兼及上游公告」中「密集高产阶段」表述（见 stage 4 capability_change 首句「2017 年为密集高产阶段」）的「高产」含轻度评价色彩，建议改为「2017 年为密集产出阶段」，与全篇克制叙述一致；该字段其余表述已按 R1#6 删除量级数字并标注未核验，复核通过。
- transferable_practices 第 3 条「在研究过程中引用前人工作（如 2015 年 SMI Handler 幻灯片引用 Duflot、Wojtczuk、Phrack）进行学术化复盘与前人工作对照，而非孤立发明」中「而非孤立发明」含轻度评价色彩，建议改为「而非孤立研究」，与该条「学术化复盘与前人工作对照」的中性描述一致。该条依据 yb-works-07/yb_tl_08，证据支撑充分，仅措辞层面调整。
- mechanism 1 intermediate_capability「形成从抽象行为模型迁移到具体底层系统攻击与防御的能力，能够在驱动层、芯片组层、UEFI/Secure Boot 层、SMM 层、Hypervisor 层之间切换目标，并具备以『检测/防御』视角补充『攻击』视角的能力（2008 年 DeepWatch PoC）」：该句与 mechanism name「研究目标由抽象模型逐层下移到硬件信任根」并存时，「迁移到具体底层系统攻击与防御的能力」与「逐层下移到硬件信任根」表述重叠，建议收紧为「形成在驱动层、芯片组层、UEFI/Secure Boot 层、SMM 层、Hypervisor 层之间切换研究目标的能力，并具备以检测/防御视角补充攻击视角的能力（2008 年 DeepWatch PoC）」，去除与 mechanism name 重复的「从抽象模型迁移到具体底层」表述。

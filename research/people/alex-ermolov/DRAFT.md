# 未通过独立复核

已达到最大修订次数 4；本文件是审计草稿，不得进入跨人物比较。

# Alex Ermolov：漏洞研究成长分析

- 擅长领域：UEFI 与 Intel 平台漏洞
- 独立复核：revise · 89/100

## 成长阶段


## 主要成长机制

## 可迁移与不可迁移

- 可迁移：结构化漏洞披露时间线（组织级）：BRLY-2022-013/CVE-2022-31646 记录四节点——HP PSIRT 通知 2022-04-12、确认与 CVE 分配 2022-06-15、补丁发布 2022-08-09、公开披露 2022-08-10，修复至公开间隔约 1 日；BRLY-2022-038/CVE-2023-22449 记录四节点——Intel PSIRT 通知 2022-12-19、CVE 分配 2023-02-28、补丁发布 2023-08-08、公开披露 2023-11-16，修复至公开间隔约 100 日（约 3 个月）。两份通告署名均为 BINARLY efiXplorer team（组织级），未含 Alex Ermolov 个人姓名，不可据以建立个人级漏洞发现归属。（ae-timeline-05、ae-timeline-06、r1-brly-2022-013-interval、r1-brly-2022-038-interval）
- 可迁移：单点平台漏洞与供应链级议题两类主题并存：单点平台漏洞类包括 SMM 驱动内存破坏（BRLY-2022-013/CVE-2022-31646）与 DXE 驱动栈缓冲区溢出（BRLY-2022-038/CVE-2023-22449）；供应链级议题类包括 Intel EDKII 固件供应链问题（BHUS_2021，据 README 称 2020 年 9 月报告 Intel）与基于 LVFS 的开源检测框架（BHASIA_2022）。两类主题在 2021–2023 期间并存，依据现有证据不可判定两类主题间的单向演化方向。（ae-timeline-01、ae-timeline-03、ae-timeline-05、ae-timeline-06）
- 可迁移：扫描框架、IDA 插件与 PoC 仓库的组织级产出：Binarly GitHub 组织维护 FwHunt（UEFI 已知漏洞扫描规则格式）、fwhunt-scan、idapcode、ToolsAndPoCs、Vulnerability-REsearch、Research_Publications 等仓库；Vulnerability-REsearch 仓库 LogoFAIL 目录下存在 32 个 markdown advisory 文件（BRLY-LOGOFAIL-2023-001 至 030，及 BRLY-2023-006、BRLY-2023-018，均标注 2023 年编号）。上述仓库与文件均仅确认存在，未提供维护时间线或活动连续性证据，署名统一为组织级，无个人作者。（ae-timeline-07、r4-logoFAIL-directory）
- 可迁移：会议披露与公开 PoC 仓库对应：Research_Publications 仓库中 BHUS_2021、BHEU_2021、BHASIA_2022、BHUS_2022 各会议目录下存在对应 README，README 称 BHUS_2022 在 9 个月内披露 42 个 SMM/DXE 高危漏洞并含 BRLY-2022-016 PoC。所引证据仅证明 README 存在于对应会议目录下，未提供其与演讲发布时间的关系，不可据以断言 README 与演讲同步公开；BHEU_2021 的 PDF 文件名线索指向 Teodorescu，进一步表明组织署名不等同于研究对象个人参与。（ae-timeline-01、ae-timeline-02、ae-timeline-03、ae-timeline-04）
- 可迁移：说明：上述可迁移性仅在 Binarly 组织层面观察，不预设研究对象个人是否实践这些做法；个人级归属在现有证据下不可建立（见 tensions 与 open_questions）。
- 不可直接迁移：Binarly 组织资源与团队网络（个人特有条件，不可迁移）：GitHub binarly-io 组织页 People 仅显示 @merces、@yeggor；Vulnerability-REsearch 仓库提交作者为 ivanovanton、pagabuc、yeggor、xorpse、francesco-ev、matrosov，efiXplorer 仓库提交作者均为 yeggor；BRLY 通告与 Black Hat 会议 README 统一署 BINARLY efiXplorer team / Binarly。这些组织级署名机制、团队协作网络与提交历史构成研究对象若参与其中所依托的组织资源，属个人特有条件。注：两份提交历史未出现 Ermolov 姓名，仅据此强化个人与组织归属未经一手核验，不据此反向推断个人能力缺失。（ae-timeline-07、r3-vr-repo-commit-authors、r3-efixplorer-commit-authors）
- 不可直接迁移：2021–2023 期间 OEM/Intel 固件披露活动窗口：BRLY-2022-013（2022-08-10 公开）、BRLY-2022-038（2023-11-16 公开）与 BHUS_2021、BHASIA_2022、BHUS_2022 会议 README 均落在 2021–2023 期间。该披露活动密度是组织所处时期的外部条件，非个人可迁移做法；现有证据为个例性条目，不构成统计性定性。（ae-timeline-01、ae-timeline-03、ae-timeline-04、ae-timeline-05、ae-timeline-06）
- 不可直接迁移：输入 person_json 断言的社交账号 https://x.com/ErmolovA 返回 HTTP 402，未能核验其与研究对象 Alex Ermolov 的归属关系，亦未取得可核验正文；该账号是否属于研究对象未经任何一手来源核验。（ae-timeline-08、ae-community-001）
- 不可直接迁移：一手来源不可抓取条件：Black Hat 议程页（blackhat.com 返回 HTTP 403）、Binarly blog/posts/team/advisories 正文（客户端渲染空壳）、the-logofail.com（连接被拒 ECONNREFUSED）均不可读取正文；这些是当前资料环境限制，限制了对个人署名演讲、writeup 与团队页的一手核验，非研究对象个人条件。（ae-community-002、ae-community-003、alex-ermolov-ext-001、ermolov-dec-001）

## 复核问题

- 字段 tensions 第二项中『Binarly 已知联合创始人/CEO 为 Alex Matrosov（与 Ermolov 不同名）』：原措辞为『Binarly 已知联合创始人/CEO 为 Alex Matrosov（与 Ermolov 不同名）；这些姓名关系未经一手来源消解』。改写方向：删除『联合创始人/CEO』与名字『Alex』这两个未经一手来源核验的具体属性，删除『已知』这一前设性措辞，改为不前设职务与名字的表述，例如『搜索摘要曾将 Binarly 的创办人描述为 Alex Matrosov（与 Ermolov 不同姓），但 binarly.io/team 抓取仅返回页面外壳、GitHub binarly-io 组织页 People 仅显示 @merces、@yeggor，该职务与名字均未经一手来源核验；仅 VR 仓库提交历史（r3-vr-repo-commit-authors）显示 matrosov 为提交者，未含职务与名字 Alex。这些姓名关系（Alex Ermolov、Artem Ermolov、Alex Matrosov、Teodorescu）未经一手来源消解』。须保留『姓名关系未经一手来源消解』的未证实表述，不引入新的未经核验职务断言。
- 非强制建议（如不改可不触发 revise 之外的额外要求）：建议在 non_transferable_conditions 第一项或 tensions 中，对 r3-vr-repo-commit-authors 显示的提交者 matrosov 引用其一手来源并明确标注『仅可据此确认 matrosov 为该仓库提交者，不可据此确认其 Binarly 职务或名字 Alex』，使该一手证据与 tensions 第二项关于 Matrosov 的表述在来源层级上保持一致。此为一致性优化，非必须。
- 综合结果没有可复核的成长阶段或机制。

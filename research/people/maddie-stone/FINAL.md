# Maddie Stone：漏洞研究成长分析

- 擅长领域：在野漏洞与 Android/Windows 漏洞
- 独立复核：pass · 90/100

## 成长阶段

- **约 2017–2018 · 嵌入式/工具化起点**：以 Johns Hopkins University（Computer Science 与 Russian 双学士、Applied Mathematics & Statistics 辅修、计算机科学硕士）与 Johns Hopkins Applied Physics Lab 的嵌入式设备安全工作为起点，建立从芯片到固件各层的逆向分析能力，并在此阶段形成『研究产出 → 配套工具仓库 + 会议演讲』的双通道输出习惯。2017 年 DerbyCon 与 REcon Montreal 的 IDAPython 嵌入式设备逆向演讲、2018 年 BlackHat USA『Unpacking the Packed Unpacker』与 OffensiveCon『The Smarts Behind Hacking Dumb Devices』构成其早期可观察的公开输出。毕业年份未在本人自述中给出，列为资料缺口。（置信度：medium）
  - 证据：r1-ragingrock-about-career-timeline, r1-ragingrock-speaking-2017-2023, ms-community-conpresentations-2017-2023, ms-community-idapython-embedded-toolkit-2017
- **2019 · 加入 Project Zero，方向收敛到在野 0-day**：据本人一手自述『I worked as a Security Researcher at Google Project Zero (2019–2023)』，研究重心由嵌入式/Android 恶意软件狩猎（前序 Google Android Security Team 逆向工程师角色）收敛到在野使用的 0-day exploit 分析，形成以真实攻击者所用利用链为研究产出的取证—根因—披露循环。该年份由 ragingrock.com/pages/about.html 一手自述确认，不再依赖 2020-07 首篇 writeup 反推；ms-dec-001 的 lead_only 状态因 r1 一手自述升格为 primary 而不再冲突。（置信度：high）
  - 证据：r1-ragingrock-about-career-timeline, ms-dec-001, ms-community-identity-github-profile
- **2020 · Detection Deficit 年度回顾**：2020-07-29 发布『Detection Deficit: A Year in Review of 0-days Used In-The-Wild in 2019』。在该文中以第一人称展示假设-检验-修正回路：进入分析时带有先验假设（寻求『为何 use-after-free 是被利用最多的 bug 类』等技术性结论），但反复被数据拉回到更基础的『0-day 在野检测能力严重不足』问题，最终把文章主题从技术切片转向 detection deficit，并公开承认数据/检测能力不足而非掩饰。这是可直接观察到的方法论层面的反馈驱动自我修正。（置信度：high）
  - 证据：maddie-stone-conversations-001, ms-works-01
- **2022 · 半年回顾与跨年度基线化**：2022-06-30 发布『2022 0-day In-the-Wild Exploitation…so far』，主动回溯对照前一年结论（明确指出与 2020 年度回顾一致），把单点发现纳入纵向比较，并将分析焦点从单个 bug 上推到补丁完备性与回归测试这一系统性机制（上半年所见 0-day 中至少一半本可通过更完整的补丁和回归测试避免，其中至少九个为既往已修复漏洞的变体）。形成跨年度的 0-day 在野经验数据基线，体现系统化、可迭代的输出习惯。（置信度：high）
  - 证据：maddie-stone-conversations-002, maddie-stone-conversations-001

## 主要成长机制

### 假设-检验-修正回路 + 分析范围上移与跨年度基线化

起点：进入 Project Zero 后面对真实在野 0-day 数据，需要从单点漏洞分析上移到趋势性与系统性判断；具备一手数据分析能力与公开 writeup 输出渠道（projectzero.google）。

练习与反馈：在 2019 年度回顾与 2022 半年回顾两篇 writeup 中重复同一可观察行为：进入分析时先带技术性先验假设，让数据反推结论走向（2020：从『UAF 占比』转向『detection deficit』；2022：从单个 bug 转向『补丁完备性/回归测试缺口』与『变体复现』），并在第二篇中主动回溯对照前一年结论，建立跨年度比较基线。两者在第一人称行为上不可分别观察为两条独立机制，故合并为同一机制的两个观察面，避免把同一组两个数据点拆成两条『独立』机制造成的因果膨胀。；反馈来源为数据本身对先验假设的反驳（『over and over I kept coming back to the problem of the detection of 0-days』），以及跨年度结论一致性的自我对照（2022 明确指向 2020 年度回顾）。这是一种以证据而非预设为导向、并以纵向一致性作为校验的内部反馈，而非外部同行/社区的反馈回流。

能力与结果：形成『先验假设 → 数据驱动修正 → 范围上移到系统性机制 → 纳入跨年度基线』的可迭代分析节律；从『找 bug』上移到『理解 bug 长生命周期（补丁、回归测试、变体）』，并具备把单点发现归并到趋势判断的能力。；2020-07-29 Detection Deficit 年度回顾：主题由技术切片被数据反推为 detection deficit；2022-06-30 半年回顾：≥9 个为既往已修复漏洞变体；≥半数本可通过更完整补丁与回归测试避免；明确与 2020 年度回顾一致

置信度：medium；替代解释：该机制仅基于两篇 PZ writeup 的第一人称自述（同一作者、同一团队、相近方法论），样本量小；『范围上移』与『跨年度基线化』也可能是 Project Zero 团队整体方法论（如同事亦发布年度回顾）而非 Stone 个人特有能力，本证据集无法据同事 writeup 正文进行区分。

证据：maddie-stone-conversations-001, maddie-stone-conversations-002

### 双通道公开输出（会议演讲 + 工具/教学仓库）

起点：2017 年起具备嵌入式设备逆向与 IDAPython 自动化能力，并身处允许公开演讲与维护公开仓库的组织环境（APL、Google Android Security Team、Project Zero）。组织资源与时代红利（GitHub 生态、安全会议文化）是该通道可成立的外部条件。

练习与反馈：2017–2023 年持续以『会议演讲 + 配套 GitHub 仓库』双通道输出：2017 IDAPythonEmbeddedToolkit（约 688 stars）配 DerbyCon/REcon IDAPython 演讲；AndroidAppRE（约 1.6k stars）配 Android 逆向教学；ConPresentations 跨 6 年约 26/27 场演讲归档（2017 DerbyCon/REcon → 2023 BSidesCanberra/OffensiveCon/Zer0Con）。主题按年份可见从单一工具技巧（IDAPython）扩展到 Android 在野 0-day 与利用链分析，再到在野 0-day 年度综述与主题演讲。；据 AndroidAppRE issue 跟踪器一手核查，仓库存在外部反馈入口（2 open + 6 closed issue，多为 VM 下载/导入问题），但未发现任何 maddiestone 本人回复，也未发现任何 issue 反馈回流导致仓库内容、workshop 结构或研究方向改变的一手证据。因此 feedback 字段仅支持『反馈入口存在』，不支持『反馈回流改变能力』的闭环；该机制的反馈驱动未被证实。

能力与结果：将一次性研究产物复用为长期社区资源（工具脚本、教学单元、演讲归档），形成稳定的『研究—演讲—再研究』输出节律与可被外部观察的产出结构。；2017–2023 约 27 场会议演讲横跨全期（2017 DerbyCon/REcon IDAPython 起至 2023 BSidesCanberra/OffensiveCon/Zer0Con）；IDAPythonEmbeddedToolkit（约 688 stars）、AndroidAppRE（约 1.6k stars）公开工具/教学仓库；2023 OffensiveCon 与 James Forshaw 合讲 Print Spooler（同伴协作）

置信度：low；替代解释：『会议演讲 + 工具仓库』是安全研究员常见的产出范式，在 Project Zero 与 Google 同事中并不罕见，不具区分度；该通道的可观察性高但独特性低。反馈闭环未证实，故该机制只能解释『输出习惯的稳定性』，不能解释其能力的差异化来源。

证据：r1-ragingrock-speaking-2017-2023, ms-community-conpresentations-2017-2023, ms-community-androidappre-workshop-1-6k-stars, ms-community-idapython-embedded-toolkit-2017, ms-community-offensivecon2023-printspooler-forshaw-collab, r1-androidappre-issues-no-feedback-loop

## 可迁移与不可迁移

- 可迁移：假设-检验-修正回路：进入数据分析时显式记录先验假设，允许数据反推结论走向，并在后续周期主动回溯对照前一轮结论以建立纵向基线（可观察于 2020 年度回顾与 2022 半年回顾）。
- 可迁移：把一次性研究产物固化为长期可复用资源：研究产出同时以『会议演讲 + 配套工具/教学仓库』双通道发布，使单次工作转化为可被反复引用的社区资源（可观察于 IDAPythonEmbeddedToolkit、AndroidAppRE、ConPresentations）。
- 可迁移：把分析焦点从单点 bug 上移到系统性机制：在单个漏洞发现之外，主动追问补丁完备性、回归测试缺口与变体复现，形成对 bug 长生命周期的判断（可观察于 2022 半年回顾）。
- 不可直接迁移：组织资源与时代红利：身处 Google Android Security Team、Project Zero、Threat Analysis Group，具备对在野 0-day 与利用链的一手数据访问权限与公开披露渠道，这是其年度回顾类工作可成立的外部条件，非个人能力可复制。
- 不可直接迁移：Johns Hopkins Applied Physics Lab 的嵌入式设备安全背景（从芯片到固件各层）构成其早期 IDAPython/嵌入式逆向能力的特定起点条件，非普遍可达的训练练路径。
- 不可直接迁移：Project Zero 团队方法论与同事协作网络（如与 James Forshaw 合讲 Print Spooler）是其输出风格与同伴反馈的特定环境，不能简单归因为个人特质。
- 不可直接迁移：公开仓库的 star 数（IDAPythonEmbeddedToolkit 约 688、AndroidAppRE 约 1.6k）与 GitHub followers 是社区触达的间接指标，受平台生态与时间窗口影响，不构成能力机制证据。

## 复核问题

- 无关键事实/身份/来源错误。承载性主张（职业链与教育背景）经独立 WebFetch ragingrock.com/pages/about.html 抽查，与 synthesis 引用的 r1-ragingrock-about-career-timeline 逐项一致：Johns Hopkins APL（嵌入式设备安全）→ Google Android Security Team（逆向工程师，hunting malware）→ Google Project Zero（Security Researcher, 2019–2023）→ Google TAG（2023–2024，lead the new Exploits Mission）；教育为 Johns Hopkins BS（CS+Russian 双主修、AMS 辅修）+ MS in CS。旧职业链（NSA/NCC Group EDG/Amazon Lab126/Lookout）确为错误并已正确作废，未被重新引用为支撑。
- 修正 Stage2 capability_change 中关于 ms-dec-001 的措辞：将『ms-dec-001 的 lead_only 状态因 r1 一手自述升格为 primary 而不再冲突』改写为『2019 加入 PZ 的事实由 r1-ragingrock-about-career-timeline（primary 一手自述）支撑；ms-dec-001 仍为 lead_only，仅作间接辅证，不应表述为其被升格』，以如实反映来源层级。
- 核实或删除机制B 中的『IDAPythonEmbeddedToolkit（约 688 stars）』具体数字：该 star 数来自 lead_only 源、本轮未一手抓取；应改为定性描述（如『公开工具仓库，有一定社区关注』），或补抓 GitHub 仓库页核实后再保留精确数字。
- 定义或替换机制A validation_tests 中的『generative』标签：当前该词含义不明（是否指『产出新分析产出/输出』？）；应显式说明其判定含义，或替换为定义明确的验证类型（如『cross_case_consistency』指跨年度结论一致性），避免读者无法据其复核。

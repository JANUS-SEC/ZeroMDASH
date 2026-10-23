# 未通过独立复核

已达到最大修订次数 3；本文件是审计草稿，不得进入跨人物比较。

# Antonio Cocomazzi：漏洞研究成长分析

- 擅长领域：Windows 与 EDR 漏洞
- 独立复核：revise · 88/100

## 成长阶段

- **2016-06 — 2017-07 · 勒索样本逆向与威胁情报短文输出**：早期公开作品以 Locky/Zepto 勒索软件样本分析与 JavaScript 投放器逆向为主，方法停留在静态/动态样本分析层面，建立以样本/家族为单位公开记录的输出习惯；此阶段未涉及权限提升或 EDR 规避，为后续难度跃迁提供可对照的基线。（置信度：high）
  - 证据：ac-timeline-01, ac-timeline-02, ac-timeline-03, ac-timeline-04, ac-works-02, ac-works-03
- **2019-12 — 2020-07 · 向 Windows 本地权限提升与进程注入/规避迁移**：研究重心由恶意样本分析迁移到 Windows 信任边界，以 SeImpersonate 与服务账户到 SYSTEM 的 Potato 路径为入口，并在同期将技术栈横向扩展到进程注入与 Instrumentation Callback 检测规避原语；建立独立博客作为体系化公开输出渠道；这是其研究重心第一次可核验的迁移。（置信度：high）
  - 证据：ac-timeline-05, ac-decisions-01, ac-timeline-06, ac-works-05, ac-community-02, ac-decisions-02, ac-timeline-08, ac-targeted-r1-01, ac-timeline-07, ac-works-01, ac-conversations-002
- **2021-04 — 2022-12 · 进入 MSRC 披露闭环、威胁团伙行为画像与单组件序列化研究**：研究深度向 Windows RPC 协议内部推进，首次进入与 MSRC 的正式披露流程并经历 Won't Fix 反馈；研究方法从单点漏洞扩展到威胁团伙行为画像（Black Basta/FIN7、Vice Society 等）；对 Seclogon 单一组件做跨多篇 writeup 的序列化纵深分析（part 2 → part 3）。（置信度：high）
  - 证据：ac-timeline-09, ac-community-03, ac-decisions-03, ac-timeline-10, ac-timeline-11, ac-timeline-13, ac-community-07, ac-timeline-14, ac-community-04, ac-decisions-06, ac-timeline-15, ac-timeline-16, ac-timeline-12, ac-decisions-05
- **2023-01 — 2023-09 · 协议级正式 CVE 披露与 Potato 研究线十年回顾**：披露策略由厂商不修的边界研究转向可获 CVE 的协议级漏洞：完成 LocalPotato（CVE-2023-21746）的 MSRC 报告 → Patch Tuesday 修复 → 公开披露闭环，并主动评估补丁为 workaround 与残留攻击面；同期将 SSPI/NTLM 原语延伸到 UAC 边界绕过，并在 POC2023 对 Potato 研究线作十年阶段性总结。（置信度：high）
  - 证据：ac-timeline-17, ac-works-10, ac-community-05, ac-decisions-07, ac-timeline-18, ac-community-06, ac-conversations-003, ac-decisions-08, ac-decisions-09

## 主要成长机制

### 厂商封堵后更换传输原语并复用前序公开缺陷重建利用路径

起点：2019 起进入 Windows 本地权限提升研究，JuicyPotato 在 Windows 10 1809/Server 2019 因 OXID 解析器被限制到端口 135 而被封堵；具备跟踪厂商补丁变化与同伴近期公开成果的基础。

练习与反馈：面对厂商补丁封堵既有利用路径，不放弃研究方向，而是更换传输原语（TCP/IP → 命名管道；OXID 解析 → 本机 COM 服务器）或复用他人已公开的路径校验缺陷（itm4n PrintSpoofer 的分隔技巧），把被封堵的原语重组为新绕过。；厂商边界判定（Service→SYSTEM 被判 expected behavior）反馈，据此调整是否进入正式披露，并提示其需在 expected behavior/Won't Fix 类选题与可获 CVE 的协议级漏洞之间区分选题。

能力与结果：形成对失败或被封堵结果的迭代式再利用与跨技术点拼装能力，能把分散的前序原语组合为可复现利用链。；RogueWinRM（BITS 向 5985 端口 WinRM 的 NTLM 认证 + 伪 WinRM 服务器获取 SYSTEM 令牌）；RoguePotato（自建 Oxid Resolver + 命名管道端点 + PrintSpoofer 路径校验绕过 + RPCSS token kidnapping）；JuicyPotatoNG（本机 COM 服务器 + LogonUser NewCredentials 注入 INTERACTIVE SID + SSPI hook 取代 RpcImpersonateClient）

置信度：high；替代解释：Potato 谱系的连续产出可能部分源于同期 Windows 认证子系统可挖掘原语较多与社区热度较高，存在幸存者偏差：同期其他研究者可能亦在尝试但未公开产出，个人方法习惯与外部可挖掘窗口的相对贡献难以分离。此外成长叙事主体依据研究对象自撰来源重建，external 维度未取得一手第三方评价，能力归因应限定为基于自述与可核验产出的推断。

证据：ac-decisions-01, ac-decisions-02, ac-works-05, ac-community-02, ac-timeline-06, ac-decisions-06, ac-community-04, ac-timeline-14

### 对单一 Windows 组件做跨多篇 writeup 的序列化纵深分析

起点：2021 进入 Windows 组件级研究，逆向 Seclogon 服务时发现 SlrCreateProcessWithLogon 信任客户端传入的调用方 PID，可通过修改 TEB 中的 ClientId 伪造 PPID 借合法系统服务打开目标进程句柄。

练习与反馈：对 Seclogon 单一组件跨多篇 writeup 纵深分析，从句柄滥用（part 2，借合法系统服务打开 LSASS 句柄实现不直接调用 OpenProcess 的隐蔽转储）推进到竞态时序（part 3，在句柄关闭前复制 LSASS 句柄）。；自我接续的序列化推进（part 3 正文回溯 part 2 末尾曾提及该竞态方法可作为后续主题，且 part 3 在约两年后完成该主题；该依据为 part 3 的回溯引用而非 part 2 原文直接核验，来源层级见 ac-targeted-r2-01）。

能力与结果：形成对单一攻击面反复复盘、逐层加深的练习模式，以自我接续方式推进而非依赖外部选题。；Seclogon part 2：滥用泄露句柄转储 LSASS 内存；Seclogon part 3：竞态窃取 LSASS 句柄的可靠转储方法

置信度：medium；替代解释：part 3 正文回溯 part 2 末尾曾提及该竞态方法可作为后续主题，且 part 3 在约两年后完成该主题；该依据为 part 3 的回溯引用而非 part 2 原文直接核验，据此推断存在主动规划的证据强度较若视为 part 2 原文直接预告为弱，需标注来源层级局限。

证据：ac-timeline-11, ac-timeline-13, ac-community-07, ac-decisions-05, ac-targeted-r2-01

### 失败或搁置选题的存档与条件变化后重访

起点：早期以特定 SSPI 配置绕过 UAC 的尝试失败（自述 failed miserably that time）后被搁置；研究过程中积累失败或废弃项目。

练习与反馈：保留旧失败项目，在获得新思路（如他人一手 writeup）时重新审视并改用新利用路径完成。；他人一手 writeup 多次作为重入研究的技术起点被引用（Forshaw 的登录会话研究被引用为 SSPI、DCOM、Kerberos 多个选题的起点）；同伴校对（decoder_it 对 SSPI UAC writeup 的 proofreading）。

能力与结果：形成对失败结果不作终结而是存档待条件变化时重启的能力，把旧失败作为后续可重用的研究材料。；SSPI UAC 绕过：两年前失败项目重访，改用 Datagram 风格 NTLM + LSASS 登录会话令牌混淆 + 经 SMB 的 SCM RPC 完成

置信度：medium；替代解释：重访习惯可能部分受研究周期与外部新思路发布节奏驱动，而非仅个人存档纪律；目前可核验的重访样本以 SSPI UAC 一例为主，该机制的跨时期重复性证据较其他机制弱，单一样本不足以排除偶然因素。

证据：ac-conversations-003, ac-decisions-08, ac-community-06, ac-timeline-18

### 以特定同行一手 writeup 为选题入口并据起点归属区分研究来源

起点：具备阅读并跟踪特定同行（James Forshaw、Elad Shamir、itm4n、x86matthew 等）一手 writeup 的习惯与基础。

练习与反馈：持续跟踪并吸收特定同行近期公开 writeup 并以其为多个选题的技术起点；Forshaw 的登录会话研究被引用为 RoguePotato、RemotePotato0、JuicyPotatoNG、SSPI UAC 多个选题的起点；LocalPotato 的起点则为 Elad Shamir 关于 NTLM Challenge Reserved 字段的提示，Forshaw 在瓶颈处提供后续提示而非起点。；同行讨论（Elad Shamir 与作者持续辩论 NTLM 上下文交换思路）与瓶颈处同行提示（Forshaw 在 LocalPotato 卡壳时提供关键提示）共同推进选题。

能力与结果：形成以特定同行 writeup 为选题入口、并结合自身 Potato 谱系重组原语的能力，能区分不同选题的实际起点来源。；RoguePotato、RemotePotato0、JuicyPotatoNG、SSPI UAC（以 Forshaw 登录会话研究为起点）；LocalPotato（以 Elad Shamir 关于 NTLM Challenge Reserved 字段的提示为起点，Forshaw 提供瓶颈提示）

置信度：high；替代解释：Forshaw、Elad Shamir 的 writeup 作为起点的高频出现，可能部分反映该研究者阅读范围集中于少数高产同行，而非独特的选题能力；同期其他研究者亦可获取相同公开 writeup，个人重组能力与公共 writeup 可及性的贡献难以分离，存在幸存者偏差。

证据：ac-community-02, ac-community-03, ac-community-04, ac-community-05, ac-community-06, ac-decisions-02, ac-decisions-03, ac-decisions-06, ac-decisions-07, ac-decisions-08

### 跨主题迁移持续公开输出并据厂商反馈区分披露策略

起点：2020-07 建立独立博客并以知识共享为动机；RSS 显示自 2016-06 起已有持续公开输出习惯。

练习与反馈：跨主题迁移（勒索样本 → Windows 提权 → EDR 规避 → 协议级漏洞）持续公开 writeup 与 POC，并就部分选题进入 MSRC 报告 → Patch Tuesday 修复 → 公开披露闭环。；可核验反馈来源为 MSRC 披露闭环（RemotePotato0 经 MSRC 案件 62293 判定 Won't Fix、LocalPotato 获 CVE-2023-21746 并于 2023-01 Patch Tuesday 修复）；会议认可部分以本人 Talks 页为来源，Black Hat 议程页返回 HTTP 403 未能一手核验，不可与 MSRC 披露闭环并列陈述为同等强度的可核验反馈。GitHub 置顶仓库的公开 star/fork 计数可作为工具被社区复用的采纳指标，但属平台聚合数据，不等同于对其研究方法的可核验反馈。

能力与结果：形成稳定的公开输出节奏与据厂商反馈区分披露策略的能力：expected behavior/Won't Fix 类选题不报告或公开 POC 与缓解，可获 CVE 的协议级漏洞进入正式 MSRC 协同披露。；RemotePotato0：MSRC 案件 62293 判 Important/Elevation of Privilege，微软 Won't Fix 后公开 POC 与 YARA 检测；LocalPotato：CVE-2023-21746，2022-09-09 报告 MSRC，2023-01 Patch Tuesday 修复，0patch 为不支持版本提供微补丁；会议序列：RomHack 2020 → Black Hat Asia 2021/HITB 2021 AMS → BlueHat IL 2022 → Insomni'Hack 2022 → POC2023（10 Years of Windows Privilege Escalation with Potatoes）

置信度：high；替代解释：持续公开输出与会议发表可能部分受会议渠道可及性与同期社区热度影响，而非仅个人习惯；博客自 2023-09-14（ac-timeline-18）后无新条目，该机制覆盖时段止于 2023-09，2024-2026 活动未核验。

证据：ac-works-01, ac-community-01, ac-conversations-001, ac-conversations-004, ac-community-03, ac-community-05, ac-works-10, ac-timeline-09, ac-timeline-17, ac-decisions-03, ac-decisions-07, ac-decisions-09, ac-community-09

## 可迁移与不可迁移

- 可迁移：显式列明所依赖的前序公开研究并说明各自贡献（RoguePotato 致谢 JuicyPotato、RogueWinRM、Tiraniddo 共享登录会话研究、itm4n PrintSpoofer），把重组路径可复现地记录下来，便于他人验证与迭代。
- 可迁移：面对厂商补丁封堵既有利用路径时，不放弃研究方向而是更换传输原语（TCP/IP → 命名管道；OXID 解析 → 本机 COM 服务器）或复用他人已公开缺陷重建利用原语。
- 可迁移：对单一组件做跨多篇 writeup 的序列化纵深分析（Seclogon part 2 → part 3），从句柄滥用推进到竞态时序，逐层加深而非一次成篇。
- 可迁移：保留失败或搁置选题，并在获得新思路（如他人一手 writeup）时重新审视改用新利用路径完成（SSPI UAC 两年前失败项目重访）。
- 可迁移：据厂商边界判定区分披露策略：expected behavior/Won't Fix 类选题不报告或公开 POC 与缓解，可获 CVE 的协议级漏洞进入 MSRC 报告 → Patch Tuesday → 公开披露闭环，并对修复是否为 workaround 作主动复盘。
- 不可直接迁移：成长叙事主体依据研究对象自撰来源（博客正文、GitHub bio、Talks 页、RSS）重建，external 维度仅得搜索引擎摘要、无一手第三方 URL，能力归因应限定为基于自述与可核验产出（CVE-2023-21746、Patch Tuesday、MSRC 案件 62293、GitHub 仓库）的推断，而非独立第三方能力评价。
- 不可直接迁移：与 decoder_it 的固定合著关系及与 Forshaw、Elad Shamir、itm4n、x86matthew 的同伴网络为该研究者特有条件，他人难以复制；前序 writeup 作为起点的高频出现部分取决于能否进入该同伴网络的讨论圈。
- 不可直接迁移：Potato 谱系在 2019-2023 的连续产出部分依赖同期 Windows 认证子系统可挖掘原语较多与社区热度较高这一外部窗口（幸存者偏差），并非仅个人方法习惯；同期其他研究者可能亦在尝试但未公开产出。
- 不可直接迁移：2023-09-14 后博客无新条目，本输出所重建的成长过程覆盖时段止于 2023-09，2024-2026 活动未核验；据既有材料外推其后续能力变化属资料缺口。

## 复核问题

- mechanisms[4].feedback 自撰字段使用『卡壳』一词（原文：Forshaw 在 LocalPotato 卡壳时提供关键提示），该词为日常口语化表达且源自枪械卡壳的比喻，与已在前轮纠正的『支点』『沉没产出』同属禁止的俚语或比喻范畴，违反 task.md 与 CLAUDE.md 关于自撰字段禁止黑话、俚语、比喻的强制规范。
- 字段 mechanisms[4].feedback：将『同行讨论（Elad Shamir 与作者持续辩论 NTLM 上下文交换思路）与瓶颈处同行提示（Forshaw 在 LocalPotato 卡壳时提供关键提示）共同推进选题』中的『卡壳时』替换为中性专业表述。原措辞：Forshaw 在 LocalPotato 卡壳时提供关键提示。改写方向：Forshaw 在 LocalPotato 研究遇到技术难点时提供关键提示（或：Forshaw 在 LocalPotato 研究停滞阶段提供关键提示）。理由：『卡壳』为口语化表达且源自枪械卡壳的比喻，违反自撰字段禁止俚语、比喻的规范，与已在前轮纠正的『支点』『沉没产出』同属一类违规。
- 字段 stages[0].capability_change：将『为后续难度跃迁提供可对照的基线』中的『难度跃迁』替换为更中性的表述。原措辞：难度跃迁。改写方向：难度提升（或：技术难度提升）。理由：『跃迁』带量子跃迁的比喻色彩，虽学术中文偶有使用，但为保持自撰字段专业书面语的一致性与克制，建议中性化为『难度提升』。该项为可选优化，非强制违规。
- 字段 mechanisms[1].confidence 与 mechanisms[4].confidence：建议在 confidence=high 的判定上附注来源层级限定，或在 confidence 字段补充说明该置信度建立在研究对象自撰来源（part 3 回溯引用、本人 Talks 页）基础之上。理由：mechanisms[1] 的 feedback 依据为 part 3（ac-community-07）对 part 2 末尾的回溯引用而非 part 2 原文直接核验（已由 ac-targeted-r2-01 限定来源层级），mechanisms[4] 的会议认可部分以本人 Talks 页为来源且 Black Hat 议程页 HTTP 403 未一手核验；在单一来源结构性限制下，high 的置信度标注略偏乐观。该项为一致性建议，不构成强制 revise 触发条件。
- 结论引用缺失或已作废：['ac-timeline-01', 'ac-timeline-02', 'ac-timeline-03', 'ac-timeline-04', 'ac-works-02', 'ac-works-03']
- 结论引用缺失或已作废：['ac-timeline-05', 'ac-decisions-01', 'ac-timeline-06', 'ac-works-05', 'ac-community-02', 'ac-decisions-02', 'ac-timeline-08', 'ac-targeted-r1-01', 'ac-timeline-07', 'ac-works-01', 'ac-conversations-002']
- 结论引用缺失或已作废：['ac-timeline-17', 'ac-works-10', 'ac-community-05', 'ac-decisions-07', 'ac-timeline-18', 'ac-community-06', 'ac-conversations-003', 'ac-decisions-08', 'ac-decisions-09']
- 结论引用缺失或已作废：['ac-decisions-01', 'ac-decisions-02', 'ac-works-05', 'ac-community-02', 'ac-timeline-06', 'ac-decisions-06', 'ac-community-04', 'ac-timeline-14']
- 结论引用缺失或已作废：['ac-works-01', 'ac-community-01', 'ac-conversations-001', 'ac-conversations-004', 'ac-community-03', 'ac-community-05', 'ac-works-10', 'ac-timeline-09', 'ac-timeline-17', 'ac-decisions-03', 'ac-decisions-07', 'ac-decisions-09', 'ac-community-09']

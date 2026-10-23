# Pedro Ribeiro：漏洞研究成长分析

- 擅长领域：网络设备与企业软件漏洞
- 独立复核：pass · 89/100

## 成长阶段

- **2013-08 至 2013-12 · 桌面与图形库 fuzzing 起点**：以针对广泛部署的解析库系统化 fuzzing 并取得独立 CVE 编号作为公开披露起点，形成 '发现—编号—公开披露' 的基础流程，区别于笼统的早期兴趣或单点发现。（置信度：high）
  - 证据：pr-pubworks-001, pedro-ribeiro-decisions-01, pedro-ribeiro-timeline-01, pedro-community-01
- **2014-01 至 2016-11 · 企业软件 RCE 模板化与固件方向迁移**：将 fuzzing 的发现—披露流程迁移到攻击面更大、鉴权模型薄弱的企业管理平台，固定出 '未认证上传/反序列化→RCE + Metasploit 模块' 的可重复产出模板；2014 年起出现独立命名的 fuzzing/ 目录；2015 年底至 2016 年进入网络设备固件方向，技术栈由 Web 控制台漏洞切换到固件二进制逆向与自定义协议解析；同时自述最少六个月修复期，并把分散披露沉淀为 pedigree.csv 可检索索引。（置信度：high）
  - 证据：pr-pubworks-002, pr-pubworks-003, pr-pubworks-004, pr-pubworks-005, pr-pubworks-013, pedro-ribeiro-decisions-02, pedro-ribeiro-decisions-03, pedro-ribeiro-decisions-06, pedro-community-04, pedro-ribeiro-conversations-01
- **2018-10 至 2021-11 · 企业网络全链与竞赛式多目标协作**：在高价值企业网络产品上构造完整链（认证绕过→上传→提权），目标由单漏洞转向链式利用；2019 年起以 Team Flashback（Pedro Ribeiro 与 Radek Domanski）进入 Pwn2Own，方法从单点披露转向面向竞赛的多漏洞链开发与赛后长文公开复盘；同期横向迁移到 OT/ICS 方向。Pwn2Own Tokyo 2020（因疫情改在 Toronto 举办）的实际记录为与 Radek Domanski 获 Master of Pwn、凭借 SAN exploits 获胜、赛事总奖金 136,500 美元、共 23 个 unique bugs；RV340 攻破发生于此期 Austin 2021，非 Tokyo 2020。（置信度：high）
  - 证据：pr-pubworks-006, pr-pubworks-007, pr-pubworks-008, pr-pubworks-009, pedro-ribeiro-decisions-04, pedro-ribeiro-decisions-05, pedro-community-02, pedro-community-06, pr-rr2-001, pr-rr2-002
- **2021-11 至 2024-03 · fuzzing 深化与产出闭环稳定**：在 2014 年 Adobe fuzzing 之后约十年再次以 fuzzing 为持续方法，针对开源解析器库产出多枚漏洞并归入 fuzzing/ 目录；在竞赛级别回归路由器目标并产出被 Metasploit 接受的公开利用模块，构成 writeup→模块→上游合并的完整发表回路；跨年对同一厂商/产品族反复研究的模式（NUUO 三轮、TP-Link Archer 与 NETGEAR R6700 在多个 Pwn2Own 年度被重复研究）持续。同期公司官网自述将研究流程向教学课程（flashback.sh）与自研定制 AI 辅助系统产品化。（置信度：medium）
  - 证据：pr-pubworks-010, pr-pubworks-011, pr-pubworks-012, pedro-community-05, pedro-community-07, pedro-ribeiro-timeline-05, pedro-ribeiro-conversations-02, pedro-ribeiro-conversations-03

## 主要成长机制

### 可重复的发现—编号—披露—利用闭环

起点：2013 年具备针对高使用率 C/C++ 解析库（libtiff、Little CMS、X.org、poppler）进行系统化 fuzzing 并取得独立 CVE 编号的基础能力，以及 GitHub 仓库 pedrib/PoC 作为自发布渠道。

练习与反馈：反复执行 'fuzzing/审计发现漏洞 → 取得 CVE/ZDI 编号 → 在 PoC 仓库发布 writeup 与 PoC → 提交 Metasploit 模块 → 由上游评审合并' 的完整流程，并用 pedigree.csv 把分散披露沉淀为可检索的 CVE/ZDI 漏洞索引；fuzzing/ 目录专门归档仅取得 CVE 但未完整利用的测试用例。；Metasploit 社区对模块的接受/拒绝构成外部同行复核回路；厂商修复与协调披露窗口（README 自述 'a minimum of six months'）构成披露节奏反馈；Pwn2Own 评审与补丁后是否仍可被攻破构成链式利用的有效性反馈。

能力与结果：把一次性发现沉淀为可复用资产的习惯，使漏洞发现—编号—利用—公开形成可检索、可复用的闭环，而非依赖单次灵感。；2014-08-22 manageengine_dc_pmp_sqli.rb 被 Metasploit 接受，开启可复用公开利用模块的长期贡献。；据 pr-rr1-001 一手核验，pedigree.csv 中被 Metasploit 接受的模块数为 62 个（pr-pubworks-004 称 58、decisions-06 称 63 个以上，三处计数不一致）。；2021 年起再次以 fuzzing 为持续方法产出 gdk-pixbuf、WebKit WTF、Raptor RDF Syntax Library 等多枚 CVE，归入 fuzzing/ 目录。

置信度：high；替代解释：Metasploit 模块的高接受率也可能反映 Metasploit 社区的入库标准或其对企业管理软件利用模块的收录倾向，而非研究者利用质量的独特性；同时 pedigree.csv 为研究者自维护索引，模块计数存在 58/62/63+ 三处不一致，62 为一手核验值。

证据：pr-pubworks-001, pr-pubworks-002, pr-pubworks-004, pr-pubworks-011, pr-pubworks-013, pedro-ribeiro-decisions-01, pedro-ribeiro-decisions-06, pedro-community-04, pr-rr1-001

### 同厂商/产品族的跨年反复研究

起点：2014 年起对单一厂商族（ManageEngine 多产品套件）密集产出，形成在同一厂商相近代码基上复用方法（文件上传/SQLi/.NET remoting）的能力。

练习与反馈：对同一厂商/产品族跨年回访研究：NUUO 经历三轮（NVRmini 2016-08、Central Management System 2018-10、NVRmini2 2022-01）；TP-Link Archer A7/C7 与 NETGEAR R6700 在多个 Pwn2Own 年度被重复研究；Pwn2Own 的公开 writeup 与补丁再利用（TP-Link 补丁于次年再次被攻破，CVE-2020-28347）形成补丁—再研究—再披露的反馈闭环。；厂商补丁的有效性（补丁次年是否仍可被攻破）作为对研究判断的直接反馈；Pwn2Own 的限时竞赛环境提供对链式利用可靠性的即时验证。

能力与结果：对演进中固件与产品族形成可迁移的领域知识，使新一版固件的研究可复用上一版的逆向与方法，而非每次从零开始。；NUUO 在 2016、2018、2022 三个年度均产出 CVE，构成跨年的产品族反复研究。；TP-Link Archer A7/C7 与 NETGEAR R6700 在 Pwn2Own Tokyo 2019、Austin 2021 等多个年度被重复研究。

置信度：medium；替代解释：跨年回访可能由厂商补丁未根治同一根因、目标在竞赛中重复出现，或研究者路径依赖既有工具链共同导致，而非完全由主动的方法迁移意图驱动；该模式由 CSV 时间序列推断，非作者自述。

证据：pr-pubworks-003, pr-pubworks-005, pr-pubworks-012, pedro-ribeiro-decisions-02, pedro-ribeiro-decisions-03, pedro-ribeiro-decisions-04

### 竞赛级全链开发与不确定性作为工程参数

起点：2018 年起在高价值企业网络产品上具备构造完整链（认证绕过→上传→提权）的能力，2019 年与 Radek Domanski 组成 Team Flashback 进入 Pwn2Own。

练习与反馈：连续参加 Pwn2Own Tokyo 2019、Miami 2020、Tokyo 2020、Austin 2021、Miami 2022，以赛事为单位组织批量研究与 exploit 链开发，在赛后以长文 markdown writeup 公开复盘；在 RV340 sslvpnd 利用中接受 65% 可靠性以换取实现简化，并把栈地址随机化的非典型现象作为可接受的工程参数而非放弃理由。；Pwn2Own 评审的通过/失败即时反馈链式利用的有效性；sslvpnd 自动重启使重试廉价这一现场特性降低了可靠性要求，构成环境反馈对工程取舍的影响。

能力与结果：在时间受限与不确定性条件下，把链式利用的可靠性、目标状态与实现复杂度作为可权衡的工程参数进行取舍，而非追求确定性单点突破。；Pwn2Own Austin 2021（2021-11，ZDI 主办）攻破 Cisco RV340，对应 CVE-2022-20699 / ZDI-22-414，Team Flashback = Pedro Ribeiro (@pedrib1337) + Radek Domanski (@RabbitPro)。；Pwn2Own Tokyo 2020（因疫情改在 Toronto 举办）与 Radek Domanski 获 Master of Pwn，凭借 SAN exploits 获胜，赛事总奖金 136,500 美元、共 23 个 unique bugs。；Pwn2Own writeup 以 lao_bomb.md、tokyo_drift.md、flashback_connects.md 等长文形式自发布并由 pedigree.csv 统一索引。

置信度：medium；替代解释：Pwn2Own 获奖受目标选取、团队配合、目标设备状态与偶然性多重因素影响，作为个人技术能力信号的代表性有限；赛事结果受竞赛规则与目标选取约束，获奖不等同于个人技术能力的直接度量。RV340 约 60,000 美元奖金无一手核验（writeup 未给数额、Trend Micro 仅给赛事总量、ZDI 逐日结果页 404），仅以转述形式保留。

证据：pr-pubworks-006, pr-pubworks-007, pr-pubworks-008, pr-pubworks-010, pedro-ribeiro-decisions-04, pedro-ribeiro-decisions-05, pedro-community-02, pr-rr2-001, pr-rr2-002

### 工具建设与流程沉淀作为长期产出基础设施

起点：以独立咨询公司 Agile Information Security（2013 年在英国注册，公司注册号 08653113）形式开展漏洞研究业务，拥有稳定的自发布渠道与 GitHub 仓库。

练习与反馈：用 pedigree.csv 自建 CVE/ZDI 漏洞索引；按 advisories/exploits/fuzzing/tools 四类目录组织公开产出，其中 exploits/metasploit/ 存放已并入 Metasploit 的模块、fuzzing/ 归档仅有 CVE 但不可利用的测试用例；向厂商免费提供漏洞信息并自述给予最少六个月修复期再公开；后期把研究成果转化为 flashback.sh 嵌入式设备零日课程与自研定制 AI 辅助系统。；仓库的 commit 活动（861 stars、169 forks、601 commits，据 pedro-community-04 抓取时点）与 Metasploit 上游合并记录构成对工具可复用性的外部反馈；公司官网把赛事履历与公开漏洞数并列，构成把竞赛与日常披露视为同一输出体系的自述反馈。

能力与结果：把工具建设与披露流程制度化为长期产出的基础设施，使产出依赖可复用目录与流程而非单次灵感或一次性突破。；PoC 仓库 README 自述以 advisories/exploits/fuzzing/tools 四分类组织产出，并把未能完整利用但已分配 CVE 的模糊测试产物单独归档。；pedigree.csv 作为研究者自维护的 CVE/ZDI 漏洞索引，agileinfosec.co.uk/research 页将其列为完整公开披露履历的官方索引链接。；据公司官网自述（pedro-ribeiro-timeline-05 status=reported，无独立核验），自 2023 年起将 AI 用于攻防安全工作并通过 flashback.sh 提供嵌入式设备零日按需课程。

置信度：medium；替代解释：工具建设与流程沉淀可能部分源于咨询业务对可复用性与客户交付的客观要求，以及公司层面对外品牌化展示需要，而非完全由个人研究方法偏好驱动；'200 余个公开漏洞''不少于六个月修复期''数十万美元奖金'等表述均为研究者/公司自述，外部独立核验有限。

证据：pr-pubworks-013, pedro-ribeiro-decisions-06, pedro-ribeiro-ext-02, pedro-community-04, pedro-community-05, pedro-community-07, pedro-ribeiro-timeline-01, pedro-ribeiro-timeline-05, pr-rr1-001

## 可迁移与不可迁移

- 可迁移：用可检索索引（pedigree.csv）统一管理分散披露的 CVE/ZDI 编号、公告与 Metasploit 模块，使单次发现沉淀为可复盘与可被外部引用的资产。
- 可迁移：按产出类型分目录（advisories/exploits/fuzzing/tools）组织仓库，并把仅取得 CVE 但未完整利用的模糊测试用例单独归档，区分完整利用与部分发现。
- 可迁移：向厂商免费提供漏洞信息并设定明确修复期（README 自述 'a minimum of six months'）再公开，使协调披露流程制度化（数值与口径为公司/研究者自述）。
- 可迁移：在赛后以长文 markdown writeup 公开复盘，把竞赛中的现场判断（如非典型栈随机化、可靠性取舍）作为可被他人复用的技术记录而非仅作成绩展示。
- 可迁移：对同一厂商/产品族跨年回访，复用上一版固件的逆向与方法，以补丁是否根治同一根因作为研究有效性反馈。
- 不可直接迁移：以独立咨询公司 Agile Information Security 形式开展研究业务，拥有稳定的自发布渠道与公司官网作为对外品牌化入口，这一组织资源为个人特有条件，非单纯可迁移方法。
- 不可直接迁移：Pwn2Own 的参赛机会、目标选取与团队配合（与 Radek Domanski 组成 Team Flashback）受赛事规则与名额约束，竞赛级全链开发的高强度重复练习环境非一般研究者可复现。
- 不可直接迁移：2013 年起的公开披露起点恰逢桌面与图形库 fuzzing 的可利用窗口，以及企业 IT 管理软件鉴权模型普遍薄弱的时期条件，时间窗口与目标生态状态为外部条件而非个人方法。
- 不可直接迁移：部分关键一手核验页（ZDI 逐日结果页、OffensiveCon 2022 议程页、RedTeam Pentesting 关于我们页、agileinfosec.co.uk/blog）在本次抓取中返回 404/403 或被 WebFetch 拒绝，资料缺口本身限制了对奖金数额、演讲事实与合作者身份的独立核验，这一限制为本次研究的外部条件。

## 复核问题

- 可选轻微修订（不影响 pass）：stages[2].evidence_ids 引用 pedro-community-02 与 pedro-community-06，二者 evidence_json 中 date 标为 2020-2022，与 Stage 3 period 终点 2021-11 存在部分跨期（其主体 Pwn2Own 条目 2020-2021 落在窗口内，2022 部分延伸至 Stage 4）。建议在 Stage 3 对这两条证据加限定语或确认其 2022 部分（如 Pwn2Own Miami 2022）归入 Stage 4 表述，消除时间线边界的部分跨期。
- 可选轻微修订（不影响 pass）：mechanisms[2].feedback 中 'sslvpnd 自动重启使重试廉价这一现场特性降低了可靠性要求' 措辞略口语（'使重试廉价'）。建议改写为更克制的工程描述，如 'sslvpnd 自动重启降低了单次重试的成本，从而放宽了对一次成功率的要求'，与全文书面语规范一致。

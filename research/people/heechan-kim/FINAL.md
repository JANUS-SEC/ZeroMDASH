# HeeChan Kim：漏洞研究成长分析

- 擅长领域：Windows 内核与 LPE 漏洞
- 独立复核：pass · 84/100

## 成长阶段

- **2020 年 6–12 月 · 通用编程向安全学习过渡**：GitHub 仓库时间线显示从 Python 通用项目（auto_mouse_python、socket_python_backdoor）起步，2020 年 9–12 月转向 universal_shell_code（C）、reversing-problems（C）等逆向与安全学习仓库；可见代码侧学习曲线由 Python 过渡到 C 与逆向。仓库缺乏学习意图自述，转向动机不可从来源证实。（置信度：medium）
  - 证据：hc-identity-github, hck-dec-01
- **2021–2022 年初 · 制度化训练入口与早期公开披露**：自述参加 KITRI Best of the Best 第 10 期漏洞分析方向、加入校内 TeamSCA 与 TeamH4C，并以队名参加 2021–2023 韩国青少年 CTF；同期在个人博客以 CVE 编号公开发布最早 writeup（archives 记录最早日期 2021-11-30）。CTF 名次与 BoB 参与均为自述，未获第三方赛事档案独立印证。（置信度：medium）
  - 证据：hc-deep-01, hc-deep-02, hc-community-04, heegong-ext-kitri-bob-v10, heegong-ext-ctf-2021-2023, hc-deep-06, hck-dec-02
- **2022 年 6–9 月 · Windows 安装程序 LPE 方法与 token 提权模板成形**：连续发布 CVE-2022-4956（Advanced Installer 经 Proton VPN 安装器的 WinSxS/.Local 目录 DLL 劫持）、CVE-2022-39846（Samsung Smart Switch，引入 Python 轮询日志解析随机 GUID 路径的竞态）、CVE-2022-45422（LG Smart Share，环境变量目录 DLL 劫持）；发现路径以 Process Monitor 观察安装器 DLL 搜索顺序为主，并以 SeDebugPrivilege 打开 winlogon.exe、复制 token、经 CreateProcessWithTokenW 提升至 SYSTEM 的 PoC 模板跨漏洞复用。CVE-2022-4956 自述为审查 Proton VPN 安装器时偶然发现，经供应链依赖回溯到上游安装器框架根因。（置信度：high）
  - 证据：hc-publication-2022-4956, hc-publication-2022-39846, hc-publication-2022-45422, hc-deep-03, hc-deep-05
- **2022 年 11 月 · 单点内核态利用**：CVE-2022-44898（ASUS AuraSync 内核驱动 MsIo64.sys 栈缓冲区溢出）是所抓取作品中唯一内核态利用条目；利用 IOCTL 0x80102040 触发未校验长度的 memmove 栈溢出，经 ROP 写 CR4 关闭 SMEP、wbinvd 后跳转用户态 shellcode，遍历 ActiveProcessLinks 定位 PID 4 的 EPROCESS、复制 +70h 偏移 token 完成提权并恢复 SMEP 与栈。所抓取作品中未出现其他内核态利用，无法据以判断内核态利用是否为持续方向。（置信度：high）
  - 证据：hc-publication-2022-44898-kernel, hc-deep-04, hck-dec-04, heegong-ext-cve-2022-44898
- **2022 年 12 月 – 2023 年 9 月 · junction 与 symlink 原语固化及产品线扫描**：将 junction 加 native symbolic link 经 \RPC Control 的 reparse 点链手法在 Samsung 系列产品上重复应用，效果从任意文件创建与永久 DoS（CVE-2022-39909 Gear IconX、CVE-2023-30672 Smart Switch）扩展到任意文件删除（CVE-2023-30673），并在厂商部署 DLL 完整性检查导致直接劫持失败时改用同一原语绕过（CVE-2023-41929 Card-UFD）；CVE-2022-4894 将 DLL 劫持加竞态方法批量化覆盖四款 Samsung 与 HP 打印机软件，显示从单漏洞到产品线扫描的方法演化。（置信度：high）
  - 证据：hc-publication-2022-39909-junction, hc-publication-2023-30672, hc-publication-2023-30673, hc-publication-2023-41929, hc-publication-2022-4894, hc-publication-2023-37849, hc-community-02

## 主要成长机制

### 制度化竞赛训练与公开披露产出的并行

起点：高中计算机科班（Semyeong Computer High School）环境与校内 CTF 社团（TeamSCA、TeamH4C）提供同伴结构与参赛出口；KITRI Best of the Best 第 10 期漏洞分析方向提供制度化训练入口。

练习与反馈：2021–2023 以队名参加韩国青少年 CTF（ShaktiCTF、Codegate Junior、Wacon Junior、CCE Junior、White Hat Contest Junior 等），并按 CVE 编号在个人博客公开发布 writeup，形成约 22 个月跨多厂商的持续披露节奏。；赛事名次（自述 2021 YISF 第二、2022 ELECONN 第一、2022 Gifted Learning Institute Contest 第一）与厂商致谢及分级（Samsung High/CVSS 7.3、ASUS Hall of Fame）均为自述名次，未获 CTFtime 等第三方赛事档案独立印证；机构参与（KITRI BoB）与厂商致谢本身不构成独立能力印证。

能力与结果：由竞赛题解训练向真实厂商 0-day 披露过渡的结构性入口，形成可核验的公开产出习惯。；11 篇 CVE writeup（2021-11-30 至 2023-09-24），覆盖 Samsung、HP、LG、ASUS、Panda Security、Advanced Installer 等厂商；博客 writeup 加 GitHub PoC 的复合输出渠道，团队标签在 GitHub 与博客两处一致

置信度：medium；替代解释：CTF 参赛与漏洞披露可能为并行活动而非因果关系；KITRI BoB 项目的课程结构可能比 CTF 赛事更能解释能力转化，且赛事成绩为自述、未获第三方赛事档案独立印证；机构参与（KITRI BoB）与厂商致谢本身不构成独立能力印证。

证据：hc-deep-01, hc-deep-02, hc-community-01, hc-community-03, hc-community-04, heegong-ext-kitri-bob-v10, heegong-ext-ctf-2021-2023, hc-deep-06

### Process Monitor 驱动的安装器 DLL 搜索顺序发现

起点：Windows 第三方安装器普遍从可预测路径加载 DLL 且依赖用户可写目录；Sysinternals Process Monitor 可观察文件与注册表访问序列。最早一篇（CVE-2022-4956）自述为审查 Proton VPN 安装器时偶然发现，经供应链依赖回溯到上游安装器框架根因。

练习与反馈：在 CVE-2022-4956、CVE-2022-45422、CVE-2022-39846、CVE-2022-4894 中以 Process Monitor 观察安装器加载顺序，定位用户可写目录（WinSxS/.Local、环境变量目录、日志记录的随机 temp 目录）作为 DLL 劫持落点。；writeup 明确自述以 Process Monitor 作为发现工具（CVE-2022-4956、CVE-2022-45422）；PoC 植入恶意 DLL 后达成 SYSTEM 提权。

能力与结果：以动态行为观察定位安装器从用户可写路径加载 DLL 这一可重复漏洞模式，而非纯静态审阅。；多篇 DLL 劫持 LPE writeup（CVE-2022-4956、CVE-2022-45422、CVE-2022-39846、CVE-2022-4894）

置信度：high；替代解释：Process Monitor 是 Windows LPE 研究通用工具，其使用不构成个人特有能力；同一发现路径可能源于公开 DLL 劫持研究方法的广泛传播而非个人方法论创新。

证据：hc-publication-2022-4956, hc-publication-2022-45422, hc-publication-2022-39846, hc-publication-2022-4894, hc-deep-03

### SYSTEM 提权 PoC 模板与随机路径竞态自动化

起点：SeDebugPrivilege 可打开 winlogon.exe 并复制其 token；部分安装器将含随机 GUID 的子目录路径写入用户可写 temp 日志，直接预置 DLL 无法命中随机路径。

练习与反馈：以 OpenProcessToken、DuplicateTokenEx、CreateProcessWithTokenW 复制 winlogon token 提升至 SYSTEM 的模板在多个漏洞中复用；针对随机 GUID 路径的安装器（CVE-2022-39846、CVE-2022-4894）使用 Python 脚本轮询日志、解析 GUID 目录、在安装器加载前植入 DLL。；该模板在 CVE-2022-39846、CVE-2022-45422、CVE-2023-37849、CVE-2022-4894 中被复用；针对随机 GUID 路径的安装器使用 Python 脚本轮询日志、解析路径并植入 DLL。模板复用与能力强化之间的因果无法从公开 writeup 直接证实。

能力与结果：形成可跨漏洞搬运的 SYSTEM 提权 PoC 模板与随机路径竞态自动化脚本。；多篇 writeup 的 PoC 复用同一 token impersonation 收尾路径；CVE-2022-39846、CVE-2022-4894 引入 Python 轮询脚本处理随机化路径

置信度：high；替代解释：token impersonation 是 Windows LPE PoC 的通用提权收尾手法，复用可能源于该手法为社区常识而非个人能力沉淀；Python 轮询脚本亦为竞态利用的常规实现，不必然反映独创工具建设。

证据：hc-publication-2022-4956, hc-publication-2022-39846, hc-publication-2022-45422, hc-publication-2023-37849, hc-publication-2022-4894

### junction 加 native symbolic link reparse 点链的原语化与多用途改造

起点：管理员权限安装器在用户可写目录（Quick Launch、AppData）创建文件，且 \RPC Control 可作为 reparse 点中介；NT API（NtCreateFile、NtCreateSymbolicLinkObject）可用。

练习与反馈：在 Samsung 系列（CVE-2022-39909 Gear IconX、CVE-2023-30672 Smart Switch、CVE-2023-30673 Smart Switch、CVE-2023-41929 Card-UFD）中重复使用用户可写目录到 \RPC Control 的 junction 加 native symbolic link 到目标系统文件的 reparse 点链。；在 DLL 完整性检查使直接劫持失败的情况下，研究者改用 junction 加 native symbolic link 经 reparse 点链绕过；方法随目标软件已部署的防御措施而变化，但该变化是否构成可迁移的方法适应能力无法从单一案例证实。

能力与结果：将同一 reparse 点链原语改造为不同效果，覆盖任意文件创建与永久 DoS、任意文件删除、绕过 DLL 完整性检查。；Samsung 系列四篇 writeup 共用同一 reparse 点链原语；CVE-2023-41929 在厂商已部署 DLL 完整性检查时切换为 reparse 点链绕过

置信度：high；替代解释：junction 与 symlink 任意文件操作是 Windows 逻辑漏洞研究的成熟原语，其重复使用可能反映对公开方法的采纳而非个人原创；多用途改造亦可能因 Samsung 安装器行为相似而顺带可得。

证据：hc-publication-2022-39909-junction, hc-publication-2023-30672, hc-publication-2023-30673, hc-publication-2023-41929

### 单一厂商与产品线的系统性扫描

起点：Samsung 在 Windows 桌面侧有多款带特权安装器的产品（Smart Switch、Gear IconX、打印机软件、Card-UFD 认证工具），共享相似的安装行为与可写目录结构。

练习与反馈：对 Samsung 产品线重复扫描同一类漏洞模式：Smart Switch（CVE-2022-39846 竞态、CVE-2023-30672 junction、CVE-2023-30673 任意删除）、Gear IconX（CVE-2022-39909）、打印机软件（CVE-2022-4894 四款）、Card-UFD（CVE-2023-41929）。；同一厂商多次接收报告并分级修复（Samsung Mobile Security 与 Device Solution Product Security Team，CVE-2023-41929 评为 High、CVSS 7.3）；CVE-2022-4894 中 Samsung 转交 HP 处理，暴露跨厂商协调。

能力与结果：围绕单一厂商产品线建立可重复的漏洞模式扫描与多产品批量化披露能力。；Samsung 系列多篇 writeup 覆盖同一厂商多款产品；CVE-2022-4894 单篇覆盖四款 Samsung 与 HP 打印机软件

置信度：high；替代解释：产品线集中可能源于 Samsung 安装器框架共性而非研究者主动产品线扫描；跨厂商转交（Samsung 转 HP）由厂商内部归属决定，不反映研究者协调能力。

证据：hc-publication-2022-39846, hc-publication-2022-39909-junction, hc-publication-2023-30672, hc-publication-2023-30673, hc-publication-2022-4894, hc-publication-2023-41929, hc-community-02

### 厂商协调披露流程的重复执行与回馈记录

起点：CVE-2022-4956 的 writeup 记录了从发现、Proton VPN 转交 Advanced Installer、修复到赠送 license key 的完整时间线；研究对象为闭源厂商安装器与驱动，反馈渠道以厂商安全团队为主。

练习与反馈：对 Samsung Mobile Security、ASUS、HP、Panda Security、Advanced Installer 等厂商重复执行首次联系、转交或分级、补丁、CVE、公开 writeup 的流程，并在 writeup 中记录披露时间线。；上述厂商回馈为可核验事实；其与持续披露行为之间的因果驱动关系无法从材料中证实，时间先后不等于因果，内在动机（如排名、社区可见度）无法排除。

能力与结果：形成可重复的协调披露操作习惯与时间线记录惯例。；多篇 writeup 含完整披露时间线（CVE-2022-4956、CVE-2022-44898、CVE-2023-41929 等）；厂商回馈含 license key（Advanced Installer）、Hall of Fame（ASUS）、High 与 CVSS 7.3 分级（Samsung）

置信度：medium；替代解释：协调披露是行业惯例，时间线记录可能源于模板化写作而非个人能力；厂商回馈的存在不证明其对持续披露的驱动作用。

证据：hc-publication-2022-4956, hc-publication-2022-44898-kernel, hc-publication-2023-41929, hc-deep-04, hc-deep-05, hc-community-02, hc-community-05

## 可迁移与不可迁移

- 可迁移：以 Process Monitor 等动态行为监控工具观察安装器文件与注册表访问序列，定位用户可写路径上的 DLL 搜索顺序问题，作为 Windows 第三方软件 LPE 的发现路径。
- 可迁移：将 SYSTEM 提权收尾（SeDebugPrivilege 打开 winlogon、复制 token、CreateProcessWithTokenW）封装为可跨漏洞搬运的 PoC 模板，降低单漏洞 PoC 成本。
- 可迁移：对随机化路径（GUID temp 目录）使用脚本轮询日志、解析路径并在加载窗口内植入 payload 的竞态自动化做法。
- 可迁移：对单一厂商或产品线按共享安装行为重复扫描同类漏洞模式，将单漏洞方法批量化覆盖多款产品。
- 可迁移：在 writeup 中记录首次联系、转交或分级、补丁、CVE、公开的完整披露时间线，形成可追溯的协调披露惯例。
- 不可直接迁移：韩国青少年 CTF 赛事体系（Codegate Junior、Wacon Junior、CCE Junior、White Hat Contest Junior）与 KITRI Best of the Best 漏洞分析方向等制度化训练入口属特定时期、地区与年龄段的资源，非研究者个人方法。
- 不可直接迁移：Semyeong Computer High School 计算机科班与校内 TeamSCA、TeamH4C 社团提供的同伴结构为个人所处组织条件，不可迁移。
- 不可直接迁移：所抓取成果集中于一类目标（Windows 第三方安装器与驱动）与一类手法（DLL 劫持与 junction 加 symlink 逻辑漏洞），该目标集中度部分源于 2021 至 2023 年 Samsung 等厂商安装器行为的共性，属外部目标供给条件而非通用方法。
- 不可直接迁移：厂商回馈（Advanced Installer license key、ASUS Hall of Fame、Samsung High 与 CVSS 7.3 分级）依赖具体厂商的致谢与分级政策，非可复制的研究能力。
- 不可直接迁移：CVE-2022-44898 的内核态利用（ROP、SMEP bypass、EPROCESS token stealing）在所抓取作品中为单点，无法证明该能力已沉淀为可迁移的内核利用方法。

## 复核问题

- evidence_json 的 timeline 维度 identity_check 声称无法通过抓取确认 GitHub heegong 账号归属本研究对象、无法排除同名歧义，与 works/conversations/community/external/decisions 五个维度的 identity_check（均基于一手抓取确认 heegong、@heegong123、heegong.github.io 指向同一人 HeeChan Kim）直接冲突；synthesis 未引用 timeline 维度的 lead_only/unknown 条目，采信多数方与一手抓取结果，身份结论可靠，但未在 tensions 或 biases 中显式记录该 evidence 内部冲突。
- mechanisms[1].repeated_practice：将「在 CVE-2022-4956、CVE-2022-45422、CVE-2022-39846、CVE-2022-4894 中以 Process Monitor 观察安装器加载顺序」修订为仅对有 short_quote 直接证据的 CVE-2022-4956、CVE-2022-45422 断言使用 Process Monitor；对 CVE-2022-39846、CVE-2022-4894 改为以 Python 脚本轮询日志解析随机路径（已有 hc-publication-2022-39846、hc-publication-2022-4894 的 claim 支撑），或明确标注该两篇使用 Process Monitor 为推断。该修订为证据支持范围收缩，非阻断。
- mechanisms[0].observed_outcomes：将「11 篇 CVE writeup（2021-11-30 至 2023-09-24），覆盖 Samsung、HP、LG、ASUS、Panda Security、Advanced Installer 等厂商」修订为说明数量分歧来源——archives 全列表（hc-deep-06、hc-community-01）记 11 篇含 CVE-2022-24924（Android），首页列表（heegong-ext-cve-writeup-series、hck-dec-03）记 10 篇；并注明 CVE-2022-24924 为 Android 应用层访问控制漏洞，正文 verified_in_run=false，不在 Samsung/HP/LG/ASUS/Panda/Advanced Installer 这组 Windows 厂商范围内。该修订为范围与来源精度改进，非阻断。
- mechanisms[0].repeated_practice：将以队名参加韩国青少年 CTF 与按 CVE 编号公开发布 writeup 拆分为两条独立描述——一条为 CTF 参赛（同伴结构与赛事出口），一条为 writeup 发布（约 22 个月跨多厂商的持续披露节奏），避免将 CTF 参赛归入披露节奏。该修订为表述精度改进，非阻断。
- 在 tensions 或 biases 中补一条：evidence_json 内部 timeline 维度 identity_check（否定身份可确认性、称无法排除同名歧义）与 works/conversations/community/external/decisions 五维度 identity_check（一手抓取确认身份一致）存在冲突，synthesis 采信多数方与一手抓取结果。该修订为内部矛盾显式化，非阻断。

# Vitaly Nikolenko：漏洞研究成长分析

- 擅长领域：Linux/Android 内核漏洞
- 独立复核：pass · 91/100

## 成长阶段

- **2014–2015 · 无线攻击工具与早期内核 CVE 分析并存**：此阶段并存两类产出: 一类为无线攻击工具化脚本 (wpa-autopwn 自动解析 WPA/WPA2 握手并提交外部服务 Crackq、wifi-scripts 杂项 WiFi 工具, 均为 Python), 另一类为 Linux 内核 CVE 分析 writeup (CVE-2014-4014 LPE、CVE-2014-4699 ptrace/sysret、CVE-2014-4943 PPPoL2TP DoS、CVE-2014-2851 group_info UAF)。GitHub API 一手元数据显示 wpa-autopwn created_at=2014-12-29、wifi-scripts created_at=2015-01-02; cve-2014-4014-privesc 仓库 created_at=2019-07-23 为批量迁移日而非 CVE 实际创作日。两类产出的精确先后顺序未由仓库 created_at 完整核验, 不叙述为无线起步至内核转入的单向序列, 而表述为同期并存、先后未核验。早期 writeup 以公开技术手册 (AMD/Intel 手册、bottomupcs、linuxjournal) 为分析锚点, 建立可核验的分析链条。（置信度：medium）
  - 证据：VN-WORKS-01, vn-comm-01, vn-ext-01-cve2014-privesc-repo, vn-tl-001, vn-tl-011, VN-R4-001
- **2016 · x86_64 内核利用方法学与教学化产出**：从分析既有 CVE 进入利用链构造与方法化产出。kernel_rop 仓库 (created_at=2016-01-19) 提供自带漏洞的内核教学驱动, 演示在 SMEP 约束 (用户态不可执行) 但无 SMAP (内核可读用户态数据) 条件下的内核态提权 ROP 链, README 给出以 xchg eax,esp;ret 栈翻转 gadget 将内核栈迁移至用户可控内存的实现路径, 并链接外部 writeup (cyseclabs, 标注 2016-01-17)。同期 CVE-2016-6187 heap off-by-one 利用文章记录同行 DM 质疑推动公开论证可利用性, 致谢 Nicolas Trippar 提出覆盖引用计数触发 UAF 的方法、Thomas Pollet 协助以 gdb/python 自动化定位堆对象, 引用 Jann Horn Project Zero issue #808 关于 userfaultfd 页面处理的技术, 并自述将于 Ruxcon 发表 exploiting counter overflows in the kernel 主题演讲。方法从单点 CVE 复现走向 SMEP 约束下的 ROP 构造与堆利用, 并出现公开论证与同行致谢。（置信度：high）
  - 证据：VN-WORKS-02, vn-dec-005-kernel-rop, VN-R1-003, vn-tl-002, vn-comm-02, vn-comm-05, VN-R2-001, vn-ext-02-cve2016-heap-kaslr-rop, VN-R4-003, VN-R4-004
- **2017–2019 · kASLR 绕过专题与跨子系统 PoC 库整理**：在 ROP 提权之外开辟 kASLR 绕过子方向: kaslr_tsx_bypass 仓库 (created_at=2017-10-12, 一手可核验) 提供基于 Intel TSX/RTM 的 Linux kASLR 绕过, 封装为可复用静态库。2019-07-23 前后集中重新托管跨子系统 CVE PoC (perf、sysret/ptrace、xfs、ipx、sock_diag、netfilter、eBPF)。两件事的时间先后可由 2017 与 2019 区分: kASLR 绕过专题为 2017 年一手创建的可核验起点; 跨子系统 PoC 库集中更新的 2019-07-23 为仓库更新/迁移日期而非创作日期, 是否为主动资料库建设无法由 created_at 区分, 保留为竞争性解释。（置信度：medium）
  - 证据：VN-R1-001, vn-tl-003, vn-ext-02-cve2016-heap-kaslr-rop, VN-WORKS-04
- **2020 · Android/AArch64 方向与缓解机制评估**：研究对象从 Linux 桌面/服务器扩展到 Android Binder (CVE-2019-2215 Samsung S9 UAF) 与跨发行版 LPE (CVE-2019-15666 Ubuntu/CentOS8/RHEL8); 进入厂商加固机制分析 (SELinux RKP misconfiguration on S20 devices); 对内核缓解机制本身做评估性分析 (UAO 作为对抗 addr_limit 改写的缓解); 在 AArch64 上重建利用前置基础设施 (Locating the kernel PGD on Android/aarch64)。研究平台向 AArch64 迁移, 方法从利用构造扩展到缓解评估与新架构前置工具重建。（置信度：high）
  - 证据：vn-tl-004, vn-tl-005, vn-tl-006, vn-tl-007, VN-R4-002
- **2022–2024 · 合著、分层培训与架构/目标轴扩展**：出现合著协作 (2022-05-10 Linux kernel heap feng shui in 2022, 与 Michael S 合著, 代码注释致谢 Adrian Drzewiecki 提供 find_mergeable 对齐兼容检查逻辑; 该合著为单例, 是否构成稳定协作模式未由第二例证据确认)。方法重心在利用开发之外另设 fuzzing/RCA 课程, 研究输出由个人 writeup/PoC 转向体系化教学: DUASYNT 公开六门课程 (Linux Kernel Exploit Development 入门与进阶、Android Kernel Security、Chrome Renderer Exploitation on Android、Linux Kernel Fuzzing and Root Cause Analysis、Introduction to AArch64 Binary Exploitation); 2024 课表含 6 月 Linux kernel exploitation (x86_64, 同源页面声明售罄) 与 9 月底 Hexacon (Paris) Android kernel security。Hexacon 2024 官方议程页独立列出 Android Kernel Security 培训讲师为 Vitaly Nikolenko, 构成来自会议官方的独立第三方确认。（置信度：medium）
  - 证据：vn-comm-03, vn-ext-05-heap-fengshui-coauthor-2022, vn-tl-008, VN-WORKS-05, vn-comm-04, vn-dec-007-duasynt-training, vn-ext-04-hexacon-2024-training-external-acceptance, vn-ext-06-advanced-course-skill-ladder, VN-R1-002, vn-tl-009, vn-ext-03-duasynt-company-vehicle, vn-dec-008-duasynt-org, VN-R3-001, VN-R3-002, VN-R4-005, VN-R4-006, VN-R4-007

## 主要成长机制

### 按缓解机制逐项拆解并构造绕过或评估

起点：2016 年 kernel_rop 已在 SMEP 约束 (用户态不可执行)、无 SMAP 条件下构建 ROP 链, 具备对单一缓解机制做定向研究的起点; 早期 writeup 以公开手册为分析锚点, 形成可核验的分析习惯。

练习与反馈：跨时期在多个缓解机制上重复构造绕过或做评估性分析: 2016 SMEP 约束下 ROP (kernel_rop 教学驱动与 writeup); 2017 kASLR via Intel TSX/RTM (kaslr_tsx_bypass 静态库); 2020 UAO 作为对抗 addr_limit 改写的缓解评估; 2022 cache aliasing、SLAB_ACCOUNT、freelist randomization、hardened usercopy 的堆缓解现状梳理。；反馈来源主要为公开发表后的同行可见性; 在 CVE-2016-6187 一例中记录同行 DM 质疑推动公开论证可利用性。跨多个缓解机制的系统反馈回路缺乏一手证据, 该反馈为单例性表述。

能力与结果：把单点漏洞利用整理为可教学、可复用的工具与方法库, 支撑后续分层课程 (入门、进阶、fuzzing/RCA)。；kernel_rop 教学驱动与 cyseclabs writeup (SMEP 约束下 ROP)；kaslr_tsx_bypass 可复用静态库 (kASLR via TSX/RTM)；UAO 缓解评估 writeup；2022 heap feng shui 跨缓解现状梳理 (合著)；DUASYNT 分层课程 (入门/进阶/Fuzzing/RCA)

置信度：high；替代解释：输出节奏可能跟随上游缓解落地周期而非主动逐项拆解; 培训大纲的存在使按缓解拆解可能部分由课程结构倒推, 而非纯研究驱动。该机制覆盖跨时期多个缓解机制且生成可教学产物, 区分度成立, 但因果归因保持克制。

证据：VN-WORKS-02, vn-dec-005-kernel-rop, VN-R1-003, VN-R1-001, vn-tl-006, VN-WORKS-04, vn-tl-003, vn-comm-03, vn-ext-05-heap-fengshui-coauthor-2022, vn-tl-008, vn-comm-02, vn-ext-06-advanced-course-skill-ladder

### 工具化产出与可复用资料库建设

起点：早期即以脚本化、自动化形式产出工具: wpa-autopwn (created_at=2014-12-29) 自动解析 WPA/WPA2 握手并提交外部服务 Crackq, wifi-scripts (created_at=2015-01-02) 为杂项 WiFi 工具, 均为 Python, 体现工具建设习惯。

练习与反馈：跨领域将研究产出封装为可复用产物: WiFi 脚本工具、kernel_rop 教学驱动、kaslr_tsx_bypass 静态库、跨子系统 CVE PoC 仓库、培训课程材料。产出形式从一次性脚本扩展到可复用静态库与分层课程。；仓库公开后的可见性与课程市场反馈。DUASYNT 同源课程页声明 6 月基础场售罄, 属同源商业页面的市场表现描述, 非独立第三方权威性认可。

能力与结果：形成可复用、可教学的资料库, 使单点漏洞利用整理为可教学的方法库, 支撑后续分层课程与跨子系统复现集合。；wpa-autopwn / wifi-scripts 无线工具脚本；kernel_rop 教学驱动与 writeup；kaslr_tsx_bypass 可复用静态库；2019-07-23 跨子系统 PoC 仓库集中 (perf、sysret/ptrace、xfs、ipx、sock_diag、netfilter、eBPF)；DUASYNT 六门课程矩阵

置信度：medium；替代解释：2019-07-23 集中更新可能源于账号/平台批量迁移而非主动资料库建设; GitHub 仓库 created_at 缺口使迁移与创作无法区分, 跨子系统 PoC 库整理作为主动资料库建设的归因保留为竞争性解释而非确定结论。

证据：VN-WORKS-01, VN-WORKS-02, VN-WORKS-04, VN-R1-003, VN-WORKS-05, vn-ext-06-advanced-course-skill-ladder, vn-tl-009, vn-tl-011, VN-R4-001, VN-R4-005

### 同伴协作与公开质疑驱动的论证

起点：2016 年 CVE-2016-6187 已出现公开同行质疑 (DM 质疑该内核路径是否可利用) 与指定协作 (Nicolas Trippar 提出覆盖引用计数触发 UAF 的方法、Thomas Pollet 以 gdb/python 协助定位堆对象)。

练习与反馈：在公开 writeup 中记录同行反馈并致谢具体贡献者: 2016 CVE-2016-6187 记录质疑并致谢 Trippar/Pollet、引用 Jann Horn Project Zero #808; 2022 heap feng shui 与 Michael S 合著并在代码注释致谢 Adrian Drzewiecki 提供 find_mergeable 对齐兼容检查逻辑。；在 CVE-2016-6187 一例中构成可核验的同伴反馈 (质疑推动公开论证可利用性、分工贡献、引用 Project Zero 公开成果 Jann Horn issue #808)。该反馈为单例, 是否构成稳定成长回路未由第二例证据确认。

能力与结果：将同行质疑转化为公开论证与致谢链, 形成可核验的协作记录; 合著产出 (heap feng shui 2022) 为该机制的另一可观察形式。；CVE-2016-6187 公开论证可利用性 + Trippar/Pollet 致谢 + Project Zero #808 引用；CVE-2016-6187 文章自述 Ruxcon exploiting counter overflows 演讲 (本人一手自述, 非独立第三方议程确认)；2022 heap feng shui 合著 (Michael S) + Drzewiecki 代码致谢

置信度：medium；替代解释：同伴反馈主要见于 CVE-2016-6187 单例, 2022 合著仅署名与一句代码致谢; duasynt.com/blog 列表页 17 篇文章中仅 2022-05-10 显示合著署名, CVE-2016-6187 为独著 (Trippar/Pollet 仅正文致谢); Nicolas Trippar、Thomas Pollet、Jann Horn 的对应独立公开声明未取得, 无法确认是否构成稳定反馈回路。

证据：vn-comm-02, vn-comm-05, vn-comm-03, vn-ext-05-heap-fengshui-coauthor-2022, VN-R2-001, VN-R3-001, VN-R3-002

### 架构与目标轴的扩展

起点：2016 年以 x86_64 内核利用为方法基线 (kernel_rop 针对 3.x/4.x 内核, SMEP 约束下 ROP)。

练习与反馈：跨时期扩展架构与目标: 2017 kASLR 绕过 (x86_64 Intel TSX/RTM); 2020 Android Binder (CVE-2019-2215)、厂商加固 (SELinux RKP on S20)、AArch64 PGD 定位; 2022 堆缓解现状; 2024 课程覆盖 Android Kernel Security (arm64)、Chrome Renderer Exploitation on Android、Introduction to AArch64 Binary Exploitation、Linux Kernel Fuzzing and Root Cause Analysis。；Hexacon 2024 官方议程页独立列出 Android Kernel Security 培训讲师为 Vitaly Nikolenko, 构成来自会议官方的独立第三方确认; DUASYNT 同源课程页声明的售罄为同源市场信号。Hexacon 2024 为该阶段独立第三方确认点, 不外推至全机制。

能力与结果：将 x86_64 利用方法迁移到 arm64/Android 与浏览器渲染器, 并加入 fuzzing/RCA 的发现侧, 形成架构与目标的双轴扩展。；AArch64 内核 PGD 定位方法 (2020-12)；Android Binder UAF 与 S20 SELinux RKP 分析；Chrome Renderer Exploitation on Android 课程；Linux Kernel Fuzzing and Root Cause Analysis 课程 (发现侧)；Hexacon 2024 Android Kernel Security 培训 (独立第三方确认)

置信度：medium；替代解释：架构与目标扩展可能由培训市场需求与 DUASYNT 公司业务边界驱动, 而非纯技术好奇心; 课程矩阵主要来自 DUASYNT 同源商业页面, 独立第三方确认仅 Hexacon 2024 官方议程, 不应将同源培训矩阵外推为独立第三方验证的研究能力体系化。

证据：vn-tl-004, vn-tl-005, vn-tl-006, vn-tl-007, VN-WORKS-05, vn-ext-06-advanced-course-skill-ladder, vn-ext-04-hexacon-2024-training-external-acceptance, VN-R1-002, vn-tl-009, VN-R4-006

## 可迁移与不可迁移

- 可迁移：将研究产出封装为可复用产物 (教学驱动、可复用静态库、跨子系统 PoC 库), 使单点漏洞利用整理为可教学的方法库, 支撑后续分层课程与跨子系统复现集合。
- 可迁移：对每个缓解机制做评估性分析而非仅 PoC 复现 (SMEP 约束下 ROP、kASLR 绕过、UAO 缓解评估、堆缓解现状梳理), 形成按缓解机制逐项拆解的可重复研究路径。
- 可迁移：以公开 writeup 记录同行质疑与致谢链, 将外部反馈转化为可核验的公开论证与协作记录 (限于单例可观察)。
- 可迁移：在新架构上重建利用前置基础设施 (AArch64 内核 PGD 定位), 将已有方法迁移而非从零开始, 降低架构迁移成本。
- 不可直接迁移：DUASYNT 公司载体 (澳大利亚私人资助信息安全公司, 办公地 Zürich/Amsterdam/Sydney, 注册地址 1 Market St Sydney NSW 2000, ABN 13634103405, 面向情报与政府方案) 使其研究能转化为结构化分层课程与国际会议培训; 该机构资源为个人特有条件。
- 不可直接迁移：常驻地 Sydney 与 Hexacon (Paris) 等国际会议培训生态的可达性, 构成地域与会议渠道的个人特有条件; Hexacon trainer 子页 (hexacon.fr/trainer/nikolenko/) 返回 404, 仅 2024.hexacon.fr 活动总页含该条目。
- 不可直接迁移：本分析的可见性受公开产出存续状态限制: blog.nikolenko.space 连接被拒、web.archive.org 抓取受阻、x.com/vnik5287 需认证 (HTTP 402); 被删除、下架或未公开的早期产出不可见, 结论强度受此限制 (幸存者偏差)。
- 不可直接迁移：早期 (2014 年前) 教育背景、入门路径与早期雇主 (含 cyseclabs 与 duasynt 衔接关系) 均无一手记录, 早期成长阶段重建受限; GitHub 仓库 commit/release 日期未抓取, 各研究子方向的精确时间序列部分依赖 CVE 编号或仓库 created_at 推断。

## 复核问题


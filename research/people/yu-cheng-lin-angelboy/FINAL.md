# Yu-Cheng Lin (Angelboy)：漏洞研究成长分析

- 擅长领域：Windows 内核漏洞
- 独立复核：pass · 85/100

## 成长阶段

- **2013–2015 · 课程项目与 CTF 入门**：以下阶段叙述存在幸存者偏差：可观察的多为成功产出（CVE、出题、演讲、教学仓库高 star），失败尝试与能力边界未被记录，相关机制强度应理解为基于成功产出的下限估计而非完整画像。公开仓库历史显示其从大学课程项目起步：GitHub 账号 scwuaptx 创建于 2013-02-11，早期仓库 Attackdefense（2013-11-24，描述引文「The computer attack defense course project」）、ComputerProgrammingandApplication（2013-11-24）、DataStructure（2013-12-09）为课程项目；NCU-Food-API（2014-05-06，描述「All about NCU Food API」）与 adlweb（2014-08-14，描述「the website of advanced defense lab at ncu」）将其院校线索指向台湾国立中央大学及其防卫实验室；CTF 仓库（2015-04-02，描述「Some CTF write up」）开始长期维护 CTF 解题记录，最后推送延伸至 2025-08-29。语言以 Python/C/C++ 为主，公开代码足迹始于课程作业与 CTF 题解而非已发表漏洞研究；具体学位、入学/毕业年份与正式隶属关系无一手来源。（置信度：high）
  - 证据：yc-angleboy-2013-github-onset, timeline-ncu-courses-2013, timeline-ncu-food-api-2014, timeline-ctf-writeup-repo-2015
- **2016–2017 · 工具建设与系统化教学输出**：自建 Pwngdb（2016-02-26 创建，仓库描述引文「gdb for pwn」），提供 heapinfo、parseheap、tracemalloc、fmtarg、force、magic、orange 等面向二进制利用的 GDB 命令，约 973 star、130 fork、154 commits，持续维护至 2025-08-29；同期以 HITCON-Training（2016-11-19，描述「For Linux binary Exploitation」，含 lab1-15 编号实验课程，覆盖逆向/汇编/shellcode、栈溢出、ret2lib、ROP、栈迁移、格式化字符串、x64、堆利用 UAF/fastbin/unsorted bin、C++ vtable）、AIS3-2017（AIS3 2017 Binary Exploitation，含 lab1-5 + practice + bonus + final + env_setup.sh）、Global-Cybersecurity-Camp-2018、HITCON-CMT-2017 Wargame 等公开仓库将 Linux 二进制利用知识固化为可重复练习的编号实验课程与出题材料。输出形式从题解转向可复用工具与系统化教学材料，工具建设与教学输出在主题上相互巩固。（置信度：high）
  - 证据：yc-angleboy-2016-pwngdb, timeline-pwngdb-2016, yc-angleboy-2016-hitcon-training, timeline-hitcon-training-2016, yc-angleboy-2017-ais3-gcc, timeline-hitcon-cmt-2017-repo, angelboy-community-001, angelboy-community-002, angelboy-community-003, decision-02-linux-binary-training-materials
- **约 2016 起（讲义发表时间未知） · 跨平台堆分配器对比研究**：SlideShare 账号 /Angelboy1（作者显示名 Angel Boy）公开从 Linux glibc fastbin/tcache、FILE Structure、C++ pwn，到 Windows NT Heap、macOS libmalloc 的渐进式讲义序列，方法上沿用「分配器内部结构→利用原语」的统一分析框架横向迁移。Windows 10 Nt Heap Exploitation、MacOS memory allocator (libmalloc) Exploitation、Windows 10 内核利用三组讲义的具体发表时间未知（SlideShare 讲义页面无发表/上传日期字段，页脚 © 2026 Slideshare from Scribd 为站点版权声明），跨平台横向迁移的时序仅能以 GitHub 仓库时间为参考点近似推断，不构成逐篇可核验的时间序列。Windows 10 Nt Heap Exploitation 英文版页数在证据基内部存在冲突（works 维度记 189 页、round1 重抓记 115 页、round3 重抓记 100 页，三个值互不相同），反映 SlideShare 页面元数据不稳定，无法以单一页数值作准；故叙述中不依赖精确页数，改以讲义存在与浏览量（约 48,976）作为旁证。（置信度：medium）
  - 证据：yc-angleboy-slideshare-linux-series, yc-angleboy-windows-nt-heap, yc-r1-slideshare-no-date
- **2019 · Windows 10 内核利用与国际 CTF 出题**：技术目标从用户态堆利用升级到内核态利用与缓解绕过。据 WebSearch 转述（Black Hat 官方议程页返回 403，未取得一手摘要文本），其于 Black Hat Asia 2019 发表演讲「A New World: Building a Practical Windows 10 Kernel Exploit」，主题涵盖 KASLR、SMEP 等内核缓解绕过；该议题与 person_json.primary_focus（Windows 内核漏洞）一致，但确切日期与完整摘要未知，标记为 reported 而非 documented。同年创建 LazyFragmentationHeap 仓库（2019-07-07，描述引文「WCTF 2019 challenge」），为 WCTF 2019 出题作品，将题目与解法公开化，形成从消费练习题到面向国际参赛者原创题目设计的转变。从 Linux 堆研究迁移到 Windows 内核研究的过渡 writeup 缺一手证据，纵向升级部分依赖推断而非逐篇 writeup 证据链。（置信度：medium）
  - 证据：yc-angleboy-2019-blackhat-windows10-kernel, yc-angleboy-2019-lazyfragmentationheap, decision-05-uefi-windows-kernel-pivot, yc-angleboy-tech-evolution-summary
- **2024 · Windows 内核漏洞研究产出与外部认可**：DEVCORE 雇主一手文章（无作者个人署名，2024-08-08 发表，以 handle Angelboy 指称）陈述其在 MSRC 2024 Most Valuable Security Researchers 总榜位列第 33 名、Windows 类别位列第 9 名，为首次登上该年度榜单且为该名单中排名最高的台湾资安研究员；该排名由 DEVCORE 雇主一手文章转述，MSRC 2024 官方榜单页本次未独立核验（MSRC 官方博客仅见 2026 年度公告，researcher-recognition 页返回 404）。DEVCORE 一手 writeup（Streaming vulnerabilities from Windows Kernel - Proxying to Kernel，Part I 2024-08-23、Part II 2024-10-05 发表，均以 handle Angelboy 指称作者）陈述其研究使用了 CVE-2024-35250（KsSynchronousIoControlDevice 的 RequestorMode 不匹配逻辑漏洞）与 CVE-2024-30084（Double Fetch 变体），并称二者配合在 Pwn2Own Vancouver 2024 中攻下 Windows 11；Part I 另发表于 HITCON CMT 2024，Part II 另发表于 HEXACON 2024。但 Pwn2Own 为团队赛事，个人贡献占比不可拆分；Pwn2Own 官方结果页（ZDI/Trend Micro）本次定向抓取均返回 404、未独立核验 DEVCORE 团队条目，且记录的 Windows 11 提权者为 Valentina Palmiotti，与 DEVCORE 自述存在记录不一致，未能调和。handle Angelboy 与本名 Yu-Cheng Lin 的绑定仍仅由任务侧 person_json 提供，外部一手来源均未出现全名。（置信度：medium）
  - 证据：yc-r1-devcore-msrc-2024-article, yc-r1-devcore-proxying-part1, yc-r1-devcore-proxying-part2, timeline-msrc-mvsr-2024, timeline-pwn2own-vancouver-2024, timeline-hexacon-2024-proxying, ext-msrc-2024-mvsr, ext-devcore-role, timeline-devcore-senior-researcher

## 主要成长机制

### 自建与长期维护二进制利用调试工具

起点：2016 年前后二进制利用社区整体工具稀缺，通用 GDB 缺乏针对堆与格式化字符串的便捷命令；个人已具备 CTF 题解与课程项目积累的 Python/C 基础。

练习与反馈：自建 Pwngdb（仓库描述引文「gdb for pwn」），提供 heapinfo、parseheap、tracemalloc、fmtarg、force、magic、orange 等面向二进制利用的 GDB 命令，并以 154 commits 持续维护（2016-02-26 创建至 2025-08-29 仍有推送），形成对工作流效率的反复迭代而非一次性产出。；开放仓库的 star（约 973）、fork（约 130）与 open issue/PR（11/3）构成外部社区采纳与问题反馈回路；但反馈规模有限，反馈驱动迭代的强度为中等而非高。

能力与结果：形成将利用调试需求抽象为可复用 GDB 命令的能力，并以工具外化巩固对堆与格式化字符串利用技术的掌握。；Pwngdb 长期维护（2016 创建至 2025 仍有推送），约 973 star、130 fork、154 commits；工具命令（heapinfo、parseheap、tracemalloc、fmtarg 等）与其 SlideShare 堆利用讲义在主题上一致，工具建设与教学输出相互巩固；工具的高 star 部分源于二进制利用社区整体工具稀缺与早期公开化带来的可见度优势，star/fork 数量作为社区采纳指标，与个人能力成长的因果强度应理解为间接而非直接

置信度：medium；替代解释：工具的高采纳度可能主要反映二进制利用社区整体工具稀缺与早期公开化带来的先发优势，而非纯粹个人能力；该工具的持续维护也可能部分源于社区 issue/PR 驱动而非个人主动迭代。幸存者偏差：可观察的多为成功产出，失败尝试与能力边界未被记录，相关机制强度应理解为基于成功产出的下限估计而非完整画像。

证据：yc-angleboy-2016-pwngdb, timeline-pwngdb-2016, angelboy-community-003

### 系统化教学输出作为技术复盘与巩固

起点：已通过 CTF 题解建立 Linux 二进制利用基础；台湾 HITCON、AIS3、Global Cybersecurity Camp 等资安营队与社群存在教学输出需求。

练习与反馈：以 HITCON-Training（2016-11-19，描述「For Linux binary Exploitation」，含 lab1-15 编号实验课程，从逆向/汇编/shellcode、栈溢出、ret2lib、ROP、栈迁移、格式化字符串、x64 到堆利用 UAF/fastbin/unsorted bin、C++ vtable）、AIS3-2017（lab1-5 + practice + bonus + final + env_setup.sh）、Global-Cybersecurity-Camp-2018、HITCON-CMT-2017 Wargame 等仓库反复将利用知识固化为编号实验课程与出题材料。；教学材料公开化使外部学习者成为间接反馈来源；高 fork 数（HITCON-Training 约 192）显示社区以此为基础二次练习，外部反馈通过 fork/issue 回流。

能力与结果：形成将分散利用技术组织为循序渐进、可重复练习的课程结构与实验环境的能力，并通过教学外化巩固自身技术栈。；HITCON-Training 约 851 star、192 fork，AIS3-2017 为台湾 AIS3 资安营队 Binary Exploitation 培训材料；lab 编号体系（lab1-15）是其重复练习习惯的产物；2017 年公开 HITCON-CMT-2017 仓库，2024 年于 HITCON CMT 发表 Proxying to Kernel Part I；二者为 HITCON 平台两次可核验的发表事实，但社区联系本身无一手来源证实，因果关联为推断

置信度：high；替代解释：教学输出可能部分由社群与营队职责驱动（承担讲师角色）而非纯个人主动复盘；高 fork 数也可能反映台湾资安教学材料整体稀缺而非单纯个人影响力。两次 HITCON 平台发表为离散事实，社区联系与后续发表之间的因果关联为推断而非已核验。

证据：yc-angleboy-2016-hitcon-training, timeline-hitcon-training-2016, yc-angleboy-2017-ais3-gcc, timeline-hitcon-cmt-2017-repo, angelboy-community-001, angelboy-community-002, decision-02-linux-binary-training-materials

### 跨平台堆分配器对比研究

起点：在 Linux glibc 堆利用（fastbin/tcache、FILE Structure、C++ pwn）上已建立「分配器内部结构→利用原语」的分析框架。

练习与反馈：SlideShare 讲义序列显示从 Linux glibc 到 Windows NT Heap、macOS libmalloc 的横向迁移，沿用同一「分配器内部结构→利用原语」分析框架；后续 Windows 10 内核利用议题（Black Hat Asia 2019，reported/lead_only）与 2024 年 Proxying to Kernel 系列在主题上由用户态堆分配器延伸至 Windows 内核利用。；讲义浏览量（FILE Structure 43.8K、Advanced heap 30.2K、Windows 10 Nt Heap Exploitation 约 48,976）反映公开发表带来的社区可见度；但缺乏本人自述或第三方对其迁移效率的直接评价。

能力与结果：依据讲义主题序列可推断其在新平台复用了既有分析框架，形成跨操作系统堆分配器的对比研究能力；该能力为推断性表述（依据讲义主题序列而非本人自述或第三方评价），不作为已验证能力。；SlideShare 讲义覆盖 Linux glibc、Windows NT Heap、macOS libmalloc 三平台堆分配器；SlideShare 跨平台堆讲义与 Black Hat Asia 2019「A New World: Building a Practical Windows 10 Kernel Exploit」在主题上由用户态堆分配器延伸至 Windows 内核利用；因讲义无发表日期（yc-r1-slideshare-no-date）且 Black Hat 议题为 reported/lead_only（yc-angleboy-2019-blackhat-windows10-kernel），二者时序与因果关联为推断而非已核验；Windows 10 Nt Heap Exploitation 等讲义页数在证据基内部存在冲突（189/115/100 三值），反映 SlideShare 元数据不稳定，故仅以讲义存在与浏览量作旁证

置信度：medium；替代解释：讲义主题序列的横向迁移可能反映平台热点轮换（如 Windows 10 内核利用在 2018-2019 成为研究热点）而非个人主动迁移；跨平台讲义与 Black Hat 议题的主题相关性为推断，无法证明前者预先促成后者。

证据：yc-angleboy-slideshare-linux-series, yc-angleboy-windows-nt-heap, yc-r1-slideshare-no-date, yc-angleboy-2019-blackhat-windows10-kernel

### CVE 研究产出与竞赛实战转化

起点：已具备 Windows 内核利用研究能力（2019 Black Hat Asia 议题为前置背景，reported/lead_only）；DEVCORE 雇佣关系提供研究团队与竞赛参与条件。

练习与反馈：2024 年将研究成果转化为 CVE-2024-35250（KsSynchronousIoControlDevice 的 RequestorMode 不匹配逻辑漏洞）与 CVE-2024-30084（Double Fetch 变体），据 DEVCORE 一手 writeup（yc-r1-devcore-proxying-part1、yc-r1-devcore-proxying-part2）陈述二者配合在 Pwn2Own Vancouver 2024 中攻下 Windows 11，并将研究分两部分发表（Part I 发表于 HITCON CMT 2024，Part II 发表于 HEXACON 2024）。需明确：WCTF 2019 出题（yc-angleboy-2019-lazyfragmentationheap）与 2024 年 CVE/Pwn2Own 为两次离散节点，二者之间存在约 5 年无可核验一手来源缺口，不构成连续重复实践。；竞赛实战结果（Pwn2Own Vancouver 2024 攻下 Windows 11，由 DEVCORE 一手文章 yc-r1-devcore-proxying-part1 自述成功率 100%）与 MSRC 2024 Most Valuable Security Researchers 榜单（总榜第 33 名、Windows 类第 9 名，由 DEVCORE 雇主一手文章 yc-r1-devcore-msrc-2024-article 转述）构成外部认可反馈；但 Pwn2Own 官方结果页（ZDI/Trend Micro）本次定向抓取均返回 404、未独立核验 DEVCORE 团队条目，且记录的 Windows 11 提权者为 Valentina Palmiotti，与 DEVCORE 自述存在记录不一致，团队赛事个人贡献占比不可拆分。

能力与结果：形成将 Windows 内核逻辑漏洞（RequestorMode 不匹配、Double Fetch）转化为可利用原语并配合用于竞赛实战的能力，并以分篇 writeup 公开发表。；据 DEVCORE 一手 writeup，CVE-2024-35250 与 CVE-2024-30084 配合在 Pwn2Own Vancouver 2024 攻下 Windows 11（团队赛事，个人贡献占比不可拆分）；Proxying to Kernel Part I/II 分别发表于 HITCON CMT 2024 与 HEXACON 2024；DEVCORE 雇主一手文章陈述其 MSRC 2024 总榜第 33 名、Windows 类第 9 名，为首次登上该年度榜单且为该名单中排名最高的台湾资安研究员；MSRC 官方榜单页本次未独立核验

置信度：medium；替代解释：竞赛实战与 MSRC 排名可能部分反映 DEVCORE 团队整体研究能力与雇主研究环境支持，而非个人独立产出；Pwn2Own 官方记录与 DEVCORE 自述存在记录不一致（Valentina Palmiotti 与 DEVCORE），个人贡献占比无法拆分；MSRC 排名由雇主公告转述，存在利益关联。

证据：yc-r1-devcore-proxying-part1, yc-r1-devcore-proxying-part2, yc-r1-devcore-msrc-2024-article, timeline-pwn2own-vancouver-2024, timeline-hexacon-2024-proxying, timeline-msrc-mvsr-2024, yc-angleboy-2019-lazyfragmentationheap

## 可迁移与不可迁移

- 可迁移：将分散利用技术组织为编号实验课程（如 lab1-15）与可复用工具并行建设，通过教学外化与工具外化巩固技术栈，二者在主题上相互强化。
- 可迁移：沿用「分配器内部结构→利用原语」的统一分析框架横向迁移到不同操作系统堆分配器（Linux glibc、Windows NT Heap、macOS libmalloc），以同一框架降低跨平台研究成本。
- 可迁移：以公开仓库与讲义长期维护（Pwngdb 2016-2025、CTF writeup 2015-2025）作为可复核产出载体，使技术积累留下可追溯的时间线而非一次性产出。
- 可迁移：将竞赛实战中发现的漏洞分篇撰写 writeup 公开发表，以写作倒逼研究完整性。
- 不可直接迁移：二进制利用社区整体工具稀缺与早期公开化带来的先发优势，使 Pwngdb 的高 star 部分源于时代窗口而非纯个人能力，后来者难以复现同样的社区采纳度。
- 不可直接迁移：DEVCORE 雇佣关系提供的研究团队与 Pwn2Own 竞赛参与条件，以及台湾 HITCON/AIS3/Global Cybersecurity Camp 资安营队的教学输出平台，是个人成长的组织资源条件，非个人能力本身。
- 不可直接迁移：2013 年前后 GitHub 公开 CTF/教学材料的生态窗口，与当时台湾 CTF 社群（HITCON CTF 等）的同伴网络，构成特定时期的外部条件，难以跨时期复现。
- 不可直接迁移：Pwn2Own 为团队赛事，个人贡献占比不可拆分；MSRC 排名由雇主公告转述存在利益关联，不可作为个人独立产出的独立第三方确认。

## 复核问题

- 可选润色（不改变 pass 结论）：stages[4].capability_change、mechanisms[3].observed_outcomes[0]、mechanisms[3].feedback 中「攻下 Windows 11」为 DEVCORE 文章原文用词的转述，建议在自撰叙述中明确标注其为来源原文用词（如「据 DEVCORE 文章原文『攻下 Windows 11』」），或改用中性动词（如「完成 Windows 11 提权」），以避免在自撰叙述中沿用来源的比喻性动词。
- 可选润色（不改变 pass 结论）：transferable_practices 中「以写作倒逼研究完整性」的「倒逼」略带比喻色彩，可改为「以分篇 writeup 撰写促使研究过程留痕可复核」等中性表述，使自撰叙述更贴近克制书面语。

# Ian Beer：漏洞研究成长分析

- 擅长领域：iOS/macOS 漏洞利用
- 独立复核：pass · 84/100

## 成长阶段

- **2014（春-11 月） · 入场即端到端全链：渲染器→沙箱逃逸→内核→root**：Beer 在 2014-03 CanSecWest Pwn4Fun 的 Safari 利用 writeup（2014-11 发表）中已展示完整三段链——Safari 渲染器整数截断、经 IOKit GPU 驱动 (AppleIntelHD4000Graphics, IGAccelGLContext::unmap_user_memory selector 0x201) 沙箱逃逸、内核控制流劫持与 KASLR 经 IOKit 注册表 IOPlatformArgs 泄漏绕过，纯 ROP 绕 SMEP 后以 root 启动 Calculator.app。起点即以『完整利用链』而非单个 bug 为产出单位，并自建 DYLD-interposing 模糊测试器随机翻转 IOConnectCallMethod 参数位定位 GPU 驱动 bug，同时引用 Dionysus Blazakis、Meder Kydyraliev、winocm 等前人工作，表明其成长建立在社区研究脉络之上。该阶段确立其『自建工具优先于套用框架』与『端到端全链』两个早期倾向。（置信度：high）
  - 证据：ian-beer-pubworks-01-pwn4fun-2014
- **2016-10 至 2017-04 · 从单点 bug hunter 转向系统理论家：架构性批判与原语命名**：Beer 在 task_t considered harmful（2016-10-25）中把研究目标从『找单个 bug』升级为『指出设计类缺陷』——把 task_t 定位为架构性而非实现性问题（区分结构性内存安全与时序性内存安全），记录 4 轮 bypass→mitigation→bypass 迭代，促使 Apple 在 10.12.1 根因重构 execve。随后在 exception-oriented exploitation（2017-04-18，CVE-2017-2370）中命名并系统化一种新利用范式（故意触发 brk 异常使内核把攻击者控制的寄存器状态写入越界 ipc_kmsg，把一次性溢出转化为可重复的受控读写原语），并坦承 iOS 内核研究的引导问题——复用自己上一条 mach_portal exploit 的内核读写权作为新研究开发平台，自述『build my own kernel debugger (with printfs and hexdumps)』。该阶段确立『把每个补丁当作新攻击面』『上一条 exploit 作为下一条开发底座』与『considered harmful 命名框架把漏洞报告升华为设计批评』三项可识别的写作与方法论转向。（置信度：high）
  - 证据：ian-beer-pubworks-02-taskt-2016, ian-beer-pubworks-03-exception-oriented-2017, ib_dia_exc_bootstrap_old_exploit_as_dev_platform, ib_dia_exc_diy_kernel_debugger, ib_dia_exc_cites_esser_and_pegasus, ib_dia_exc_critique_targets_process_not_person, ib-dec-02
- **2018-10 · 方法论教师转向：变体分析显式化与攻防激励不对称**：Beer 在 Deja-XNU（2018-10-18）中把变体分析（variant analysis）从隐含动作提升为显式方法论立场：复访本人 2014 年 CVE-2014-4461 IODataQueue 内核漏洞，发现几乎相同的用户态变体信任共享内存中的 queueSize 值，在内核版修复后『又存在了四年』；自述在公开演讲变体分析前先亲自执行一遍以暴露防御方系统性盲区，并给出明确判断『Variant analysis is really important, but attackers are the only parties incentivized to do a good job of it』。研究目标从『找 bug』转向『示范方法论缺口』——识别出攻击者有动力做变体分析、防御方没有的结构性不对称。同时批评 Apple 安全公告透明度，论证遗漏修复条目会『provide a disincentive for people to update their devices』。同年（据种子与 Azad 2020-06 综述转述，发布日期未一手核实）multi_path/empty_list 引入 pipe buffer 稳定读写技术并被同事后续复用。该阶段确立『先做再讲』的方法论诚信与『把输出本身视为推动厂商加固的反馈输入』的反馈自觉。（置信度：high）
  - 证据：ian-beer-pubworks-04-deja-xnu-2018, ib_dia_dejaxnu_practice_before_preach, ib_dia_dejaxnu_attackers_only_incentivized, ib_dia_dejaxnu_bulletin_transparency_critique, ian-beer-comm-07, ib-dec-03
- **2019-02 至 2019-08 · 政治技术家转向：在野利用事件响应与公共议题框架重定向**：Beer 与 Google TAG 协作分析野外 iOS 利用链（5 条完整独立利用链、跨 iOS 10-12、14 个漏洞，发现时至少一条提权链仍为 0-day），2019-02-01 以 7 天披露期限向 Apple 报告，促发 2019-02-07 iOS 12.1.4 带外发布——把 P0 标准 90 天政策压缩为 7 天紧急政策用于针对真实人群的活跃利用。8 月 29 日发布系列深度分析，主动把讨论从『百万美元异见者』重定向为『监控第 n+1 个潜在异见者的边际成本』，并点名基于地理区域或族裔群体的定向监控。该重定向引发 Apple 罕见地以新闻室公开声明逐句反驳（称攻击窄定向、非大规模、约两月而非两年、修复已在进行中）；Beer 未公开回应争论，让技术记录自证。该阶段确立『把技术 writeup 同时作为公共议题反馈通道』『以发布→厂商公开反驳为影响力的反向印证』与『把披露期限视为强制函数而非可协商便利』三项可观察的机制化行为。（置信度：high）
  - 证据：ian-beer-pubworks-05-itw-chains-2019, ib_dia_itw_tag_collaboration_and_7day, ib_dia_itw_political_turning_point, ib_dia_itw_devices_dual_natured, ian-beer-comm-03, ian-beer-comm-08, ib-ext-05, ib-dec-04, ib-tl-itw-deadline, ib-tl-deepdive
- **2020-12 · 能力演示转向：单人零点击作为政策论证**：Beer 发表 AWDL 零点击无线电近距利用（CVE-2020-3843，约 6 个月单人研究），明确为『the longest solo exploitation project I've ever worked on』，单 bug 绕 ARM v8.3 PAC 达成完整内核读写与任意代码执行。文章透明记录 5 个失败方向（OWL 学术客户端无法构建→从零自建；iOS 12 kernelcache 误导致数周空耗；链表 flink 部分覆盖不可行；无 PAC 签名 vtable 时全覆盖致内核 panic；单帧双 SyncTree 溢出无法修复指针），并固化『Can it really be this easy? → In hindsight, there's an obvious reason why this doesn't work』的转向语式。坦承起步对该领域一无所知（『At this point, I had no idea what AWDL was』），读 SEEMOO 论文后自建 AWDL 客户端（libpcap + Raspberry Pi 4B + rtl8187）。把研究时长本身作为政策论据——量化『一人卧室即可构建此前被认为需国家级资源的零点击能力』以挑战防御投入模型。该阶段是『偶然入口、系统跟进』『自建工具投入视为长线省时的复利』与『把死路如实写进公开叙事』三项机制的代表作。（置信度：high）
  - 证据：ian-beer-pubworks-06-awdl-2020, ib_dia_awdl_opens_with_bedroom_lockdown, ib_dia_awdl_started_with_no_domain_knowledge, ib_dia_awdl_dead_ends_and_near_give_up, ian-beer-comm-01, ian-beer-comm-02, ib-dec-05, ib-tl-awdl
- **2021-12 至 2022-06 及之后 · 生态分析家与协作转向：从对抗性披露到联合分析，随后进入静默**：Beer 与 Samuel Groß 合著 FORCEDENTRY（CVE-2021-30860）分析，致谢 Apple SEAR 团队协作进行技术分析、Citizen Lab 分享样本，评估其为『one of the most technically sophisticated exploits we've ever seen』（JBIG2 解码器内以逾 7 万条 segment 指令构建图灵完备虚拟机），结尾以『Make zeroday hard.』收束；同年起与曾被其公开批评的 Apple 形成有限技术协作关系。随后发表 Carrier.app（CVE-2021-30983，DCP 协处理器 UniformityCompensator::set 堆溢出），提出『协处理器安全悖论』：把攻击面从 mitigation heavy 的 AP 移到 mitigation light 的 DCP（缺 ASLR/PAC、plain arm64、确定堆、更简 RTKit RTOS）是安全回归，把批判层级从子系统设计（task_t）上升到硬件安全架构策略级。逆向约 7000 函数 stripped 固件时以『My kingdom for a .dSYM!』『Guess we'll have to do this the hard way!』体现面对缺失调试符号的务实姿态。此后 2022-06 至 2026-09 公开输出静默逾 3 年（对照 projectzero.google 实时作者列表确认），是否仍在 Google/P0、转岗或离职均无公开证据。该阶段是批判层级抬升顶点与工作模式从纯单人转向有限协作的可核验终点，同时进入资料缺口。（置信度：high）
  - 证据：ian-beer-pubworks-07-carrier-app-2022, ib_dia_forcedentry_coauthored_with_gross_sear, ib_dia_forcedentry_incredible_and_terrifying, ian-beer-comm-06, ib-ext-04, ib-dec-06, ib-dec-07, ib-tl-forcedentry, ib-tl-carrier, ib-tl-silence

## 主要成长机制

### 自建工具优先于套用既有框架

起点：iOS/macOS 内核研究长期缺乏官方调试支持，学术或社区既有客户端/解析器常不可直接复用；Beer 起步即面对缺调试符号、缺可用客户端的研究环境。

练习与反馈：2014 年自建 DYLD-interposing 模糊测试器随机翻转 IOConnectCallMethod 参数位定位 GPU 驱动 bug；2017 年面对 macOS 缺内核调试自建『kernel debugger with printfs and hexdumps』并以 trial and error 确定覆盖值；2020 年 OWL 开源 AWDL 客户端无法构建后从零自写 AWDL 客户端（libpcap + Raspberry Pi 4B + rtl8187 监听模式，双线程注入/ACK 嗅探）；2022 年逆向约 7000 函数 stripped DCP 固件时务实走『the hard way』。；自建工具直接产出可定位 bug 与可用原语；Beer 自述『Investing a little bit of time building this API saved a lot of time in the long run』，把自建投入视为长线省时的复利而非沉没成本；自建工具产生的内核读写权又成为下一项研究的开发底座，形成正反馈。

能力与结果：在缺官方调试/参考实现的研究环境中，能快速从论文与零散线索出发自建可用的研究/注入/调试基础设施，并把『够用工具』而非『完美工具』作为目标。；2014 Safari 全链中 GPU 驱动 bug 经自建模糊测试器定位；2017 exception-oriented exploitation 经自建内核调试器开发与验证；2020 AWDL 零点击利用经自建 AWDL 客户端达成；AWDL 文中明确把自建工具投入表述为长线省时复利

置信度：high；替代解释：自建工具可能是被迫而非主动选择——既有框架不可用、缺调试符号是客观约束；但 Beer 把自建投入显式表述为复利收益而非抱怨约束，且跨 2014/2017/2020/2022 四个时期反复如此，更接近主动方法论而非被动补救。

证据：ian-beer-pubworks-01-pwn4fun-2014, ian-beer-pubworks-06-awdl-2020, ib_dia_exc_diy_kernel_debugger, ib_dia_awdl_started_with_no_domain_knowledge, ib-dec-05

### 把上一条 exploit 作为下一条研究的开发底座

起点：iOS 内核研究存在循环依赖：开发新内核利用需先有内核读写权作为开发平台；Beer 在 2017 年明确指出这一 bootstrap 问题。

练习与反馈：2017 年复用 2016 年 mach_portal 的内核读写权作为 exception-oriented exploitation 的开发平台；据 Brandon Azad 2020-06 综述与 Ned Williamson 2019-12 SockPuppet writeup，其 async_wake/extra_recipe/multi_path/empty_list 等产出被同事当作下一项研究的基础设施直接复用（Gal Beniamini 2017-09 Over The Air Vol.2 直接复用 extra_recipe 作为研究平台）；Beer→Beniamini→Azad/Williamson 的方法学接力链在 P0 内部可见。；旧 exploit 的读写原语直接缩短新研究的开发周期；同事以复现 Beer 既有 bug 校准自身工具（Williamson 把 Beer 的 mptcp_usr_connectx 溢出作为 fuzzer seed bug），构成『输出→同伴复用→再产出』反馈回路；输出被同伴当作可继承工程资产而非一次性演示。

能力与结果：把利用产出本身当作可复用的研究基础设施，形成自我复用的研究阶梯——每一条 exploit 既是一次成果也是下一次开发的工具底座。；2017 exception-oriented exploitation 复用 mach_portal 读写权作为开发平台；Beniamini 2017-09 Wi-Fi 研究直接复用 extra_recipe 并把目标版本固定在 10.2；Azad 2019-01 voucher_swap 复用 Beer 在 multi_path/empty_list 引入的 pipe buffer 技法；Williamson 2019-12 SockPuppet 把 Beer 的 mptcp 溢出作为 fuzzer seed bug 校准新人方法学

置信度：high；替代解释：复用旧 exploit 可能只是 iOS 内核研究客观存在的 bootstrap 约束的产物，而非 Beer 个人特有机制；但他在公开 writeup 中显式把这一约束命名为 bootstrap problem 并主动把它方法化，且其产出被同伴显式作为起点复用，区分度高于纯被动复用。

证据：ian-beer-pubworks-03-exception-oriented-2017, ib_dia_exc_bootstrap_old_exploit_as_dev_platform, ib-ext-03, ian-beer-comm-04, ian-beer-comm-05, ib-ext-02

### 把每个补丁当作新攻击面并升华为架构级批判

起点：Apple 缓解以补丁式增量为主，Beer 从 2016 年起把补丁本身视为新攻击面，并以 bypass→mitigation→bypass 迭代作为研究素材。

练习与反馈：2016 task_t considered harmful 记录 4 轮 bypass 迭代并把 task_t 定位为架构性而非实现性问题；2018 Deja-XNU 把同一 IODataQueue 模式的用户态变体在内核版修复后存续四年作为攻防激励不对称的证据；2021-2022 Carrier.app 把批判层级从子系统设计上升到硬件安全架构策略级（AP→DCP 是 mitigation heavy→light 的安全回归）。considered harmful 命名框架与『moving an attack surface from a mitigation heavy environment to a mitigation light one is a regression』构成稳定的写作范式。；把单点 bug 升华为子系统级/架构级理论贡献，使发布获得设计批判效力；Apple 在 10.12.1 因 task_t 系列做根本性 execve 重构（而非补丁）、据 Wikipedia 记录因某次重大披露重构 XNU 相当部分，是厂商工程层面的可观察反馈。

能力与结果：能从单个 bug 抽象出子系统/硬件架构层的可利用模式，并把漏洞报告重写为设计批评，迫使厂商做根本性重构而非补丁。；2016 task_t 促使 Apple 根因重构 execve 而非补丁；2018 Deja-XNU 揭示用户态变体修复后存续四年；2022 Carrier.app 把批判层级抬升至硬件安全架构策略；considered harmful 命名框架成为其稳定写作范式

置信度：high；替代解释：架构级批判可能部分来自 P0 团队鼓励的写作风格而非 Beer 个人机制；但 considered harmful 命名、bypass-mitigation-bypass 迭代记录、mitigation heavy/light 框架跨 2016/2018/2022 三时期稳定出现，且与同伴写作风格可区分，更接近个人方法论。

证据：ian-beer-pubworks-02-taskt-2016, ian-beer-pubworks-04-deja-xnu-2018, ian-beer-pubworks-07-carrier-app-2022, ib-dec-02, ib-dec-07, ib-ext-06

### 先做再讲与失败透明的方法论诚信

起点：公开演讲邀请易诱发空谈方法论的诱惑；Beer 自述在 2018 年受邀公开演讲变体分析时选择先亲自执行一遍。

练习与反馈：2018 Deja-XNU 自述『I thought it was important to actually do some variant analysis myself before I gave that talk』；2020 AWDL 文透明记录 5 个失败方向与近放弃时刻（『By this point I've invested a lot of time into this project and am not willing to give up』）；2017 exception-oriented exploitation 把批评锚定在流程与架构而非个人（『a clear failure of the code review processes in place at Apple』『this bug would have been caught in development if the code had any tests』）。；先做再讲使方法论主张获得实证支撑（Deja-XNU 的用户态变体存续四年成为攻击者独有激励判断的证据）；透明记录死路使其方法论诚信在公开叙事中可核验，而非被包装成天赋。

能力与结果：把『先做再讲』『把死路写进公开叙事』『批评指向流程而非个人』作为可重复的研究伦理约束，使方法论主张自带实证。；2018 Deja-XNU 先亲自做变体分析再演讲；2020 AWDL 文透明记录 5 个失败方向与坚持决定；2017 exception-oriented exploitation 把批评锚定流程而非个人

置信度：high；替代解释：先做再讲与失败透明可能只是 P0 长篇 writeup 风格的产物；但 Beer 在 2018 显式把它表述为自我强制（『important to actually do some variant analysis myself before I gave that talk』），且 AWDL 把死路而非成功路径作为叙事主干，区分度高于普通 writeup。

证据：ian-beer-pubworks-04-deja-xnu-2018, ian-beer-pubworks-06-awdl-2020, ib_dia_dejaxnu_practice_before_preach, ib_dia_awdl_dead_ends_and_near_give_up, ib_dia_exc_critique_targets_process_not_person

### 把技术 writeup 同时作为公共议题反馈通道

起点：Beer 自 2019 起把技术分析主动重定向到政治/伦理框架，并选择以博客长文而非采访/AMA 作为唯一公开对话形式。

练习与反馈：2019 ITW 系列把议题从『百万美元异见者』重定向为『监控第 n+1 个潜在异见者的边际成本』并点名族裔/地理定向；2020 AWDL 把研究时长本身作为政策论据（量化单人成本挑战『零点击专属国家级』假设）；2021 FORCEDENTRY 以『one of the most technically sophisticated exploits we've ever seen』与『pretty terrifying』并置承载伦理重量，并以『Make zeroday hard.』收束；2018 Deja-XNU 批评 Apple 公告透明度会抑制用户更新。；writeup 尾声作为公共议题反馈输入，扩大研究影响半径；Apple 罕见地以新闻室公开声明逐句反驳 Beer 2019 系列定性，构成『发布→厂商公开反驳』的反向影响力印证；Beer 不公开回应争论、让技术记录自证，固化『让技术说话』模式。

能力与结果：把技术 writeup 同时作为政策论证与公共议题塑造手段，用警句式平衡句承载伦理重量（如『treating their mobile devices as both integral to their modern lives, yet also as devices which when compromised, can upload their every action into a database』），而非情绪化口号。；2019 ITW 系列把议题重定向到边际成本与族裔定向；2020 AWDL 把研究时长作为政策论据；2021 FORCEDENTRY 以技术钦佩与伦理警惕并置收束于 Make zeroday hard.；Apple 2019-09-06 罕见公开声明逐句反驳 Beer 定性

置信度：high；替代解释：政治化框架可能是 2019 ITW 这一特定事件触发的单次转向而非持续机制；但 2018 公告透明度批评、2019 边际成本框架、2020 政策论证、2021 钦佩与警惕并置跨四时期稳定出现，且 Beer 选择博客长文而非采访作为唯一对话形式使 writeup 事实上承载了其公共议题表达，更接近持续机制。

证据：ian-beer-pubworks-05-itw-chains-2019, ian-beer-pubworks-06-awdl-2020, ian-beer-pubworks-07-carrier-app-2022, ib_dia_itw_political_turning_point, ib_dia_itw_devices_dual_natured, ib_dia_forcedentry_incredible_and_terrifying, ib_dia_dejaxnu_bulletin_transparency_critique, ian-beer-comm-08, ib-ext-05, ib-dec-04

## 可迁移与不可迁移

- 可迁移：自建可用而非完美的研究/调试/注入工具，把自建投入视为长线省时的复利：在缺官方调试或既有框架不可用的环境中，先写够用的最小客户端/调试器（printf + hexdump 级）以解锁后续研究。
- 可迁移：把上一项研究的产出（读写原语、fuzzer seed、工具链）显式作为下一项研究的开发底座，把 bootstrap 约束方法化为自我复用的研究阶梯。
- 可迁移：对每个厂商补丁做 bypass→mitigation→bypass 迭代分析，把单点 bug 升华为子系统/架构级批判，迫使厂商做根本性重构而非补丁。
- 可迁移：在公开演讲方法论前先亲自执行一遍该方法论（先做再讲），使方法论主张自带实证。
- 可迁移：把死路与坚持决定如实写进公开叙事而非只展示成功路径，以方法诚信提升方法论主张的可核验性。
- 可迁移：把批评锚定在流程与架构而非个人（如『a clear failure of the code review processes』『if the code had any tests』），并附带建设性期望（『lessons are learnt』）。
- 可迁移：对在野利用采用压缩披露期限（如 7 天）作为强制函数，把进攻性研究与事件响应打通。
- 可迁移：把变体分析作为系统化研究动作，识别并主动填补防御方缺乏变体分析激励的结构性缺口。
- 可迁移：把研究时长/成本本身作为政策论据，量化『个人可达成的能力阈值』以挑战防御投入模型。
- 不可直接迁移：Project Zero 全职编制 + 90 天/7 天披露政策 + 公开 bugtracker 的机构平台：使 Beer 可持续免费发布本可在漏洞市场变现的完整链；该机构支撑不可由独立研究者个人复制，bedroom 叙事略低估此条件。
- 不可直接迁移：Google 薪资满足财务安全、Google TAG 提供在野利用情报、Apple 紧急响应通道：构成 Beer 选择公开研究而非出售漏洞的约束与前提，独立研究者缺乏等效条件。
- 不可直接迁移：P0 内部方法学接力链（Beer→Beniamini→Azad/Williamson）：同事把其产出当作下一项研究的基础设施直接复用并显式归功，这种同伴级反馈回路是团队内部的非普遍条件。
- 不可直接迁移：早于 2014-07-15 P0 官宣即以 P0 名义发布、并起点即达端到端全链水平：加入 P0 前已是世界级利用链水平，这一起点条件（pre-2014 教育与职业路径无公开记录）不可复制或核实。
- 不可直接迁移：2022-06 后公开静默逾 3 年：其当前 P0 在职状态、是否转内部研究或离职均无公开证据，该静默是否为主动选择或环境变化未知。
- 不可直接迁移：Apple 因其重大披露重构 XNU 相当部分（据 Wikipedia 记载）：这种厂商工程层面的反馈是影响力结果而非可复制方法，依赖特定厂商与时机。

## 复核问题

- CVE-2014-4418/4461 跨维度不一致未被识别：works 维度 pubworks-04 claim 写『CVE-2014-4418』，而 decisions ib-dec-03 与 timeline ib-tl-deja-xnu claim 写『CVE-2014-4461』。综合 stages（2018 阶段 capability_change）与 mechanism 3（把每个补丁当作新攻击面 repeated_practice/observed_outcomes）统一采用 4461，但未在 tensions 或 open_questions 中标注此跨维度编号不一致。无法从抓取正文独立确认正误（Deja-XNU 帖正文未在 evidence 中给出该 CVE 编号的一手引文）。虽非核心因果证据，但属应识别未识别的事实层不一致。
- 在 tensions 或 open_questions 中显式标注 CVE-2014-4418（works pubworks-04）与 CVE-2014-4461（decisions ib-dec-03、timeline ib-tl-deja-xnu）的跨维度编号不一致，并明确综合选取 4461 的依据（与 decisions/timeline 两维度一致），或改述为『2014 年 IODataQueue 内核漏洞（CVE 编号跨维度不一致：4418/4461）』以避免呈现未核实的事实细节。
- mechanism 2 repeated_practice 中『Beniamini 直接复用 extra_recipe』应标注『extra_recipe 名称经 Azad 2020-06 综述（reported）二手佐证，Beniamini 2017-09 一手引文未含该名称』，或改述为『Beniamini 2017-09 一手确认复用 Beer 的内核读写 exploit 作为 Wi-Fi 研究平台（具体 exploit 名称 extra_recipe 经 Azad 综述二手佐证）』。
- mechanism 3 feedback 应区分：一手 ib-dec-02 支撑『task_t 促使 Apple 重构 execve』，二手 ib-ext-06（Wikipedia）补充『重构 XNU 相当部分』；避免把 Wikipedia 二手转述作为机制因果反馈的主要证据，或将其降级为 open_questions。
- 在 biases 中显式补一条幸存者偏差讨论：机制证据仅来自公开发布的成功项目，AWDL 文记录的 5 个失败方向是部分缓解；建议把『失败透明』作为机制时同时标注其幸存者偏差缓解作用有限（只覆盖已公开的失败，未覆盖未发布/已放弃项目）。
- 确认 ib-dec-01（inferred，加入 P0/职业路径选择）未作为任何 stage/mechanism 的 evidence_id（已检查通过，本项为防御性确认，无需改动）。

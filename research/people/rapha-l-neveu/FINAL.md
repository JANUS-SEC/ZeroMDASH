# Raphaël Neveu：漏洞研究成长分析

- 擅长领域：Android 与低层系统漏洞
- 独立复核：pass · 89/100

## 成长阶段

- **2018–2021 · 教育背景与学徒阶段的多任务接触**：据 LinkedIn 公开档案（conversations/external 维度 verified_in_run=true 抓取成功，本轮 rr2-linkedin-esiee-quarkslab 一手确认 employer=Quarkslab（Paris）、education ESIEE PARIS 2018–2021、About 截断自述『After playing around with networks and web applications, I'm now interested in low level…』可见；works/community 维度所称『LinkedIn 未抓取或无正文』为同一页面不同抓取时机的状态差异，非来源冲突；经验职位名称与任职起止日期因 authwall 不可见，无法一手确认），其教育背景为 ESIEE PARIS（2018–2021）。LinkedIn 推荐语（rn-conv-03 / ext-mentor-008，reported，推荐者 Eric C. 身份与关系需登录确认）转述其在学徒/实习阶段同时承担基础设施（系统管理）、渗透测试、代码审计与逆向工程任务，并以中英双语交付报告与文档。该推荐为他人二手转述，未指明具体导师、时段或失败案例。据现有可核验来源，此阶段能力为低层研究方向的有限一手自述与多任务接触的二手转述，不作为独立一手确认的稳定能力锚点。（置信度：low）
  - 证据：rn-conv-02, rn-conv-03, rn-conv-04, ext-linkedin-007, ext-mentor-008, rr2-linkedin-esiee-quarkslab
- **2024 年前（自述回溯，本体未在 Neveu 名下定位） · 据称对 Android 加密方案的前置研究**：SSTIC 2024 演讲摘要（rn-dec-001）与 Quarkslab blog（neveu-works-03）自述，此前的 Android Data Encryption Scheme / Android File-Based encryption 研究中已对采用 MediaTek SoC 的 Samsung 低端机型及 A225F 启动流程积累了知识，并据此判断 bootloader 的 JPEG logo 解析存在漏洞潜力。该前置研究由作者自述回溯，本体未在 Quarkslab blog 作者页对应到 Raphaël Neveu 名下的独立文章（rn-community-06 显示作者页仅 1 篇署名文章），可能为合作署名、内部研究或以他人名义发表，具体出处未确认。此阶段为自述回溯的间接证据，能力变化无法独立核验。（置信度：low）
  - 证据：rn-dec-001, neveu-works-03, rr5-offensivecon-speakers-2024, rn-community-06
- **2024-06-06 · SSTIC 2024 演讲与 bug-chain 方法论的首次表述**：与 Maxime Rossi Bellom 在 SSTIC 2024（Rennes，6 月 6 日 10:00）共同发表 30 分钟报告《When Samsung meets Mediatek: the story of a small bug chain》，进入 SSTIC 2024 议程。报告以多个独立小漏洞串联形成完整利用路径的方式表述 bug-chain 方法论，系该表述在公开记录中的首次出现；该表述在其后续 Samsung Galaxy A* Boot Chain 写作中被再次采用。演讲以与合著者共同主讲的形式进行，而非独立完成。研究路径从据称的前置 Android 加密研究转向 bootloader JPEG logo 解析，属策略性方向调整。（置信度：high）
  - 证据：neveu-works-01, ext-sstic-003, rneveu-tl-01-sstic-2024, rn-community-01, rn-dec-001, rn-dec-004
- **2024-08 至 2024-10-15 · 多会议循环发表与 writeup + PoC 完整发表链条**：同一 Samsung 启动链研究在 Black Hat USA 2024（据作者自述与 GitHub README 转述，Black Hat 官方议程页返回 HTTP 403，未直接核验；议题标题存在两版本：neveu-works-02 作者 Quarkslab blog 一手自述记《Attacking the Samsung Galaxy A* Boot Chain》，ext-blackhat-004 / rn-dec-004 GitHub README 转述记《Attacking Samsung Galaxy A Boot Chain and Beyond》，均未经官方议程一手确认，整条演讲保持 reported）、OffensiveCon 2024（据 GitHub README 与 OffensiveCon 讲者页 rn-community-05，documented，4 位讲者为 Maxime Rossi Bellom、Damiano Melotti、Raphaël Neveu、Gabrielle Viala；讲者页仅标注 2024 年度，未显示精确日期，相对 Black Hat USA 2024 的先后未一手核验）与 Quarkslab blog（2024-10-15）分别呈现。blog writeup 正文一手列出全部 4 个 CVE/SVE 编号（rr1-blog-cve-2024-10-15）：CVE-2024-20832（SVE-2023-2079，Little Kernel 堆溢出）、CVE-2024-20865（SVE-2024-0234，Little Kernel Odin 认证绕过）、CVE-2024-20820（SVE-2023-2215，Secure Monitor 越界读）、CVE-2024-20021（Secure Monitor 任意物理内存映射），并获 Samsung 分配 SVE/CVE 编号（ext-cve-002，documented）。4 个 CVE 串联构成覆盖 Little Kernel、Secure Monitor 与 Android 用户态三层的利用路径，实现 bootloader 代码执行、Android 持久化 root 与 Secure World 内存读取。配套 PoC 代码以 Apache-2.0 许可发布于 GitHub 仓库 quarkslab/samsung-bootchain-poc（neveu-works-04 / rn-community-03，documented），形成 writeup（描述）+ 会议演讲（传播）+ 代码仓库（复现）的完整发表链条。（置信度：high）
  - 证据：neveu-works-02, neveu-works-03, neveu-works-04, rneveu-tl-02-blackhat-2024, rneveu-tl-03-blog-2024-10, rn-community-02, rn-community-03, rn-community-05, ext-identity-001, ext-cve-002, ext-blackhat-004, ext-offensivecon-005, ext-collab-006, rn-dec-002, rn-dec-003, rn-dec-005, rr1-blog-cve-2024-10-15, rr5-offensivecon-speakers-2024

## 主要成长机制

### 以先验项目知识作为选题依据的渐进式方向推进

起点：据 LinkedIn 截断自述（rn-conv-02 / ext-linkedin-007），其从网络与 Web 应用方向转向低层研究，但转向的具体动因、时间或导师未提供。SSTIC 2024 演讲摘要（rn-dec-001）与 blog writeup（neveu-works-03）自述此前已有对 Android 加密方案与 Samsung A225F 启动流程的知识积累，并有 Maxime Rossi Bellom 作为稳定合著者、Damiano Melotti、Gabrielle Viala 作为贡献者参与（ext-collab-006 / rn-dec-003）。

练习与反馈：以先前项目积累的领域知识作为新研究选题的依据：据 SSTIC 2024 摘要（rn-dec-001），其据此判断 bootloader 的 JPEG logo 解析存在漏洞潜力并选定方向；据 blog writeup（rn-dec-002），在通过 Little Kernel 漏洞取得 Android root 后继续推进，依据 Android Keystore 密钥受 Secure World 保护这一权限边界，将目标从普通持久 root 推进至 Secure World 内存读取。；blog writeup 正文致谢（rn-community-02 / ext-collab-006）『our colleagues who reviewed this post』表明机构内部存在同行评审反馈；Samsung 对 4 个漏洞分配 SVE/CVE 编号（ext-cve-002）系上游厂商对漏洞有效性的独立确认。该两项为可观察的外部反馈来源，但未记录试错过程的直接叙述。

能力与结果：在单点突破后依据『可达目标的权限上限』重新设定下一层目标，形成从前置知识 → 相邻方向选题 → 跨层目标推进的做法。；SSTIC 2024 与 Black Hat / OffensiveCon / blog 中据称的前置 Android 加密研究迁移至 Samsung 启动链方向（rn-dec-001）；在取得 Android root 后将目标推进至 Secure World 内存读取（rn-dec-002，对应 CVE-2024-20820 与 CVE-2024-20021）

置信度：low；替代解释：该做法的可核验证据几乎全部来自 2024 年的单一 Samsung 启动链研究，『先验知识 → 选题』链条依赖作者自述回溯的前置 Android 加密研究（rn-dec-001），而该前置研究本体未在 Neveu 名下定位（rn-community-06）。一个竞争性解释是：『渐进式方向推进』反映的是该单一研究内部从 bootloader 到 Secure Monitor 的叙述结构，而非跨多个独立项目反复验证的稳定能力；现有证据不足以区分二者。

证据：rn-conv-02, ext-linkedin-007, rn-dec-001, rn-dec-002, rn-dec-003, neveu-works-03, ext-collab-006, ext-cve-002, rn-community-02

### 将单一研究通过多渠道分阶段公开发表

起点：已形成可发表的研究成果，并依托 Quarkslab 机构博客、GitHub 组织与会议渠道。

练习与反馈：将同一 Samsung 启动链研究通过面向不同受众的多个渠道分阶段公开：SSTIC 2024（2024-06-06，议程页一手，documented）→ Black Hat USA 2024（reported，官方议程页 HTTP 403 未直接核验）与 OffensiveCon 2024（据 GitHub README 与 OffensiveCon 讲者页 rn-community-05，documented；讲者页无精确日期，相对 Black Hat 先后未一手核验）→ Quarkslab blog writeup（2024-10-15，一手）与 GitHub PoC 仓库（Apache-2.0）。据 SSTIC 2024 演讲为同一研究的首次公开版本，后续按不同受众整理材料。；机构内部同行评审（rn-community-02 / ext-collab-006 致谢段『our colleagues who reviewed this post』）；GitHub 仓库收到一条外部 issue（rn-community-04，AAGaming00 询问 emulator 发布，2024-11-09），但维护者未在可见范围内回应，且无 PR 贡献回流，仓库层面双向互动有限。

能力与结果：将会议演讲、长文 writeup 与可复现 PoC 代码三者配套整理为可复现文字资料与公开代码资产，形成完整发表链条。；同一研究在 SSTIC 2024、Black Hat USA 2024 与 OffensiveCon 2024 多会议呈现（rn-community-01 / ext-sstic-003 / rn-community-05）；blog writeup 正文一手列出全部 4 个 CVE/SVE 编号及漏洞描述（rr1-blog-cve-2024-10-15）；GitHub 仓库 quarkslab/samsung-bootchain-poc 以 Apache-2.0 发布 PoC（neveu-works-04 / rn-community-03），README 指向三处演讲材料

置信度：low；替代解释：多渠道呈现全部源自同一 Samsung 启动链研究，缺乏第二个独立研究项目的多渠道发表证据。一个竞争性解释是：这反映的是 Quarkslab 机构对单一重点研究的传播策略，而非研究者个人反复采用的稳定发表习惯；现有证据不足以区分机构安排与个人习惯。

证据：neveu-works-01, neveu-works-02, neveu-works-03, neveu-works-04, rneveu-tl-01-sstic-2024, rneveu-tl-02-blackhat-2024, rneveu-tl-03-blog-2024-10, rn-community-01, rn-community-02, rn-community-03, rn-community-04, rn-community-05, ext-sstic-003, ext-blackhat-004, ext-offensivecon-005, rr1-blog-cve-2024-10-15, rr5-offensivecon-speakers-2024

### 跨层 exploitation（Little Kernel → Secure Monitor → Android 用户态）

起点：研究目标选择中端设备 Samsung Galaxy A225F（MediaTek SoC），据自述此前已对该设备启动流程有知识积累（rn-conv-01 / neveu-works-03 / rn-dec-001），并有稳定的双人主导 + 多人贡献协作结构（rn-dec-003）。

练习与反馈：对 Little Kernel 与 Secure Monitor（ARM Trusted Firmware）进行逆向工程，结合堆溢出（CVE-2024-20832）与 Odin 认证绕过（CVE-2024-20865），并通过 Secure Monitor SMC handler 越界读（CVE-2024-20820）与任意物理内存映射（CVE-2024-20021）实现跨层串联。；Samsung 对 4 个漏洞分配 SVE/CVE 编号（ext-cve-002，documented），系上游厂商对漏洞有效性与影响范围的独立确认；blog 致谢（ext-collab-006）显示内部 review。

能力与结果：覆盖 bootloader（Little Kernel）、安全监控器（ARM Trusted Firmware / Secure Monitor）与 Android 用户态三层的利用路径构建。；实现从 bootloader 代码执行到 Android 持久化 root 再到 Secure World 数据读取（含 Android Keystore keys）（ext-identity-001 / rneveu-tl-03-blog-2024-10）；4 个 CVE 串联构成覆盖三层的利用路径，blog writeup 一手列出全部编号（rr1-blog-cve-2024-10-15 / ext-cve-002）

置信度：low；替代解释：跨层 exploitation 的全部可核验证据来自同一 Samsung 启动链研究。一个竞争性解释是：4 个 CVE 的跨层串联反映该单一研究的目标结构，而非可跨项目复用的稳定能力；缺乏第二项独立研究展示同样的跨层 exploitation 习惯。据此标注 distinctive 仅基于该单研究内的技术覆盖广度。

证据：rn-conv-01, neveu-works-03, rn-dec-001, rn-dec-002, rn-dec-003, ext-identity-001, ext-cve-002, ext-collab-006, rneveu-tl-03-blog-2024-10, rr1-blog-cve-2024-10-15

## 可迁移与不可迁移

- 可迁移：以先前项目积累的领域知识作为新研究选题依据，并依据可达目标的权限边界重新设定下一层目标（rn-dec-001 / rn-dec-002）。
- 可迁移：将同一研究通过面向不同受众的多个渠道分阶段公开发表，整理为会议演讲、长文 writeup 与可复现 PoC 代码三者配套的完整发表链条（rn-community-01 / neveu-works-03 / neveu-works-04）。
- 可迁移：对目标固件进行逆向工程并结合多类漏洞（堆溢出、认证绕过、越界读、任意内存映射）串联构建利用路径（neveu-works-03 / rr1-blog-cve-2024-10-15）。
- 不可直接迁移：稳定双人主导 + 多人贡献的协作结构（Maxime Rossi Bellom 与 Raphaël Neveu 双人主导，Damiano Melotti、Gabrielle Viala 作为贡献者参与，rn-dec-003 / ext-collab-006）：该结构依赖 Quarkslab 机构同事配置，不可作为个人可迁移条件。
- 不可直接迁移：Quarkslab 机构博客、GitHub 组织与会议渠道的机构资源：多渠道发表链条依托 Quarkslab 平台，非个人独立拥有的资源（rn-community-02 / neveu-works-04）。
- 不可直接迁移：据称的前置 Android 加密方案研究积累：该知识基础为作者自述回溯（rn-dec-001），其本体未在 Neveu 名下定位（rn-community-06），不可作为可迁移的通用前置条件。
- 不可直接迁移：Samsung A225F（MediaTek SoC）设备与厂商漏洞披露通道：研究目标与 Samsung PSIRT 的 SVE/CVE 编号分配（ext-cve-002）为特定厂商组合下的条件，非普遍可迁移。

## 复核问题


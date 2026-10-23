# 未通过独立复核

已达到最大修订次数 4；本文件是审计草稿，不得进入跨人物比较。

# Charles Fol：漏洞研究成长分析

- 擅长领域：Linux/glibc/PHP 漏洞
- 独立复核：revise · 88/100

## 成长阶段

- **2017 年 · PHP 反序列化方向确立与通用工具建设起点**：由单点 PHP 反序列化漏洞分析转向把反复构造 gadget chain 的经验沉淀为可复用、可测试的通用工具。2017-03-08 发布 Drupal 7.x Services 模块 unserialize() 到 RCE 的分析（署名 by Charles Fol，Ambionics / Web Exploitation，开篇句 'Upon auditing Drupal's Services module, the Ambionics team came accross an insecure use of unserialize().'），为该方向更早的可核证公开写作；2017-07-04 发布 PHPGGC，定位为 frohoff ysoserial 的 PHP 对应物，覆盖 Laravel、Symfony、Monolog、Guzzle 等常见框架，建立 PHP 反序列化利用的可重复方法论。（置信度：high）
  - 证据：cf-rev4-003, cfol-tl-02, cf-dec-01-phpggc-ysoserial-for-php, cf-works-003
- **2019-2023 年 · PHP 应用与运行时内部纵深及反序列化可达性边界**：在 PHP 应用层与运行时内部机制两个层面持续产出公开写作，并处理反序列化利用的可达性边界问题。目标覆盖 Drupal8 REST RCE（2019）、mt_rand 内部状态预测（2020）、Symfony secret fragment RCE（2020）、PHP-FPM 共享内存提权 CVE-2021-21703（2021）、vBulletin 反序列化可达性 RCE（2023，机制句 'The bug was due to an improper handling of non-scalar data in the ORM, which led to an arbitrary deserialisation.'）、wrapwrap PHP filter 前后缀附加（2023）等。该阶段构成前一项公开工具 wrapwrap 在模糊测试中触发崩溃、进而成为后一项漏洞研究 CVE-2024-2961 入口的实例（该崩溃触发因果链由 iconv p1 作者第一人称转述支撑，wrapwrap 正文 'Fuzzing to no effect' 段未记录崩溃）。注：2018 年 CVE-2017-11176 Linux Kernel 系列（cfol-tl-03）署名为 Nicolas FABRETTI、分类为 Linux Kernel Exploitation，属身份错误，已从本分析中排除，不作为资料缺口。（置信度：high）
  - 证据：cf-rev4-002, cf-rev2-003, cf-rev2-006, cf-rev2-004, cf-rev4-001, cf-rev2-001, cf-community-wrapwrap-feedback-to-discovery
- **2024 年 · glibc 底层库扩展与盲利用工程化及协调披露**：研究重心从 PHP 应用层扩展至 glibc 底层库漏洞（CVE-2024-2961，约 24 年陈旧的 iconv 缓冲区溢出），并经两条路径桥接回 PHP 引擎：part1 经 php://filter 链在 PHP 7.0–8.3 上把文件读原语转为 RCE，part2 经对 iconv() 的直接调用并以 Roundcube 为演示目标（'I find the data-only attack more elegant, and I will therefore show it instead.'）。part3 处理仅文件读原语条件下的盲利用（'how one can exploit the same bug, but blind: without having any output!'），涉及 php_stream_bucket、bucket brigade、zend_mm_heap、custom_heap._free 等结构。同时与 glibc 上游及发行版完成协调披露（2024-03-26 报告、2024-04-04 通知发行版、2024-04-17 公开 CVE），作者评价上游响应迅速且一周内交付补丁。（置信度：high）
  - 证据：cfol-tl-10, cf-dec-02-glibc-iconv-cve-2024-2961-tech-shift, cf-rev2-005, cf-rev1-003, cf-works-001, cf-community-cnext-prior-research-citation, cf-community-glibc-coordinated-disclosure
- **2024-2026 年 · PHP stream 工具持续建设与团队级受限原语提升至 RCE 方向延续**：围绕 php://filter 持续建设小型专用工具（lightyear 用新 error-based oracle 算法经盲文件读原语 dump PHP 文件内容），延续工具-漏洞配对的产出模式。Ambionics / Web Exploitation 分类下连续发布同结构 writeup（WSO2 2025、GLPI 2025、Drupal PostgreSQL 2026、Ninja Forms 2026、SPIP 2026 等），作者归属基于 @cfreal_ 在 CNEXT 署名与统一 Ambionics 分类的推断，无法逐篇确认 Charles Fol 个人作者身份；以下作为团队级产出方向的能力曲线描述，不作为逐篇个人作者证据。该方向延续以未认证/受限前提到 RCE 的难度递增复用模式。（置信度：medium）
  - 证据：cf-rev2-002, cf-community-method-reuse-series, cf-works-004, cf-works-005, cf-ext-05

## 主要成长机制

### 工具建设与漏洞发现的反馈回路

起点：PHP 反序列化利用中反复手工构造 gadget chain 的经验积累（'For a pentester, upon discovering a way to unserialize data, the problem lies in finding correct gadgets.'），以及把零散反序列化知识固化为可复用、可测试工具的工程化倾向。

练习与反馈：把单点漏洞利用方法固化为通用工具（PHPGGC 覆盖多框架并设跨版本兼容测试脚本），按漏洞族发布独立可运行 exploit 仓库（phpggc、cnext-exploits、wrapwrap、lightyear、laravel-exploits、symfony-exploits、owncloud-exploits、spip-exploits 等），并对自研工具做模糊测试以观察行为异常作为新漏洞研究入口。；@s_n_t 在 Black Hat US 2018 发布 PHARGGC 作为 PHPGGC 的 fork，把攻击面扩展到 PHAR 生成；当前 PHPGGC mainline 已原生支持 PHAR 生成（-p phar/-o/-pj），但 fork 并入主干的过程未由 README 明示。PHPGGC README 以 PR 规范吸纳外部贡献，要求贡献者优先使用 __destruct 向量、标注库版本、遵循命名规则并提供 --new 脚手架。wrapwrap 模糊测试触发崩溃并成为 CVE-2024-2961 研究入口的因果链由 iconv part1 作者第一人称转述支撑（part1 自述 'I was fuzzing iconv filter chains in PHP, working on a tool to append suffixes to PHP filter streams'），wrapwrap 正文 'Fuzzing to no effect' 段未记录崩溃，两处一手陈述需分别对待。

能力与结果：形成研究-工具-发表的正反馈：工具成为下一项漏洞发现的入口与方法承载，而非仅作单次披露附属物。；PHPGGC 持续累积至约 725 次提交，覆盖 15 个以上框架并设跨版本兼容测试脚本；wrapwrap（PHP filter 前后缀附加）模糊测试触发崩溃，成为 CVE-2024-2961 研究入口；PHARGGC 作为 PHPGGC 的 fork 在 Black Hat US 2018 发布，把攻击面扩展到 PHAR 生成；按漏洞族发布独立 exploit 仓库的长期产出模式（ambionics 组织可见仓库清单）

置信度：medium；替代解释：存在外部贡献主导而非个人独立积累的可能：PHPGGC 的框架覆盖随外部 PR 扩展，@s_n_t 的 PHARGGC 亦为外部 fork。该工具→新漏洞的迭代回路目前仅由 wrapwrap→CVE-2024-2961 单实例支撑，phpggc、lightyear 等其他工具是否同样在使用或模糊测试中产生新漏洞未由一手证据核证；不应由单实例归纳为普遍迭代机制。

证据：cfol-tl-02, cf-dec-01-phpggc-ysoserial-for-php, cf-dec-04-exploit-repo-per-vuln-pattern, cf-community-phpggc-tool-feedback, cf-ext-03, cf-community-wrapwrap-feedback-to-discovery, cf-rev1-002, cf-rev2-001, cf-rev2-002

### PHP 运行时通道桥接应用层与 C 库底层

起点：PHP 应用层与运行时内部机制（mt_rand 状态、PHP-FPM 共享内存、Zend 内存堆）的长期积累，以及对 php://filter 链式利用的熟悉（wrapwrap、lightyear 均围绕该机制建设）。

练习与反馈：沿 PHP 应用 → PHP 运行时 → 原生 C 库的路径逐层展开研究目标，并把同一底层漏洞通过 PHP 运行时通道（php://filter 链）与运行时边界（直接 iconv() 调用）两条路径桥接回应用层 RCE；对受限（盲）原语条件下的利用按难度递进切分（part1 有输出、part2 直接 iconv/Roundcube、part3 盲利用）。；CNEXT part1 显式引用 Gynvael、loknop、DownUnderCTF、Synacktiv、PTswarm 等同行在 PHP filter chain、error-based oracle、任意对象实例化方面的前置研究作为方法基础，指出新向量作为 PHP 8.0 取消 metadata 反序列化后 PHAR 反序列化攻击的替代。part2 含 'While I demonstrated a binary exploit at OffensiveCon' 一手陈述，表明该研究曾在 OffensiveCon 会议演示，为会议参与的一手旁证。

能力与结果：形成把底层 C 库缺陷经 PHP 运行时通道远程化为应用层 RCE 的方法，并能处理仅文件读原语条件下的盲利用（泄漏 bucket brigade 地址、定位 zend_mm_heap、改写 custom_heap._free 为 system 后释放任意 chunk 触发代码执行）。；CVE-2024-2961 经 php://filter 链在 PHP 7.0–8.3 上把文件读原语转为 RCE（part1）；CVE-2024-2961 经直接 iconv() 调用以 Roundcube 为演示目标（part2）；CVE-2024-2961 盲利用：泄漏 php_stream_bucket brigade 与 zend_mm_heap 地址，改写 custom_heap._free 为 system 后释放 chunk 获得代码执行（part3）；lightyear 用新 error-based oracle 算法经盲文件读原语 dump PHP 文件内容，性能优于既有工具、payload 更小

置信度：high；替代解释：对 PHP 运行时通道的掌握可能部分源于同行前置研究（Synacktiv php_filter_chains_oracle_exploit 等）的吸收与组合，而非纯个人独立推导；但跨两条路径并处理盲利用的整合由作者第一人称 writeup 直接核证。

证据：cfol-tl-10, cf-dec-02-glibc-iconv-cve-2024-2961-tech-shift, cf-rev1-003, cf-rev2-001, cf-rev2-002, cf-rev2-003, cf-rev2-004, cf-rev2-005, cf-community-cnext-prior-research-citation

### 受限原语提升至 RCE 的跨目标方法论

起点：反序列化可达性边界处理经验（vBulletin 不可达反序列化 RCE）与受限 SQLi/文件读原语提升至 RCE 的多次实践。

练习与反馈：把同一受限原语→RCE 的方法论跨目标反复应用：vBulletin 不可达反序列化经 ORM 非 scalar 数据处理与 autoloader 引入实现 RCE，Symfony secret fragment 经 _path 参数调任意 PHP 函数实现 RCE，并在团队级 Ambionics / Web Exploitation 分类下连续发布同结构 writeup（WSO2、GLPI CVE-2025-24799/24801、Drupal PostgreSQL、Ninja Forms、SPIP 三连）。；Ambionics / Web Exploitation 分类下连续发布同结构 writeup，作者归属基于 @cfreal_ 在 CNEXT 署名与统一 Ambionics 分类的推断，无法逐篇确认 Charles Fol 个人作者身份；以下作为团队级产出方向的能力曲线描述，不作为逐篇个人作者证据。该反馈以团队级发布节奏与同结构重复为主要信号，缺少反向的同行引用与第三方实战案例一手证据。

能力与结果：形成可识别的受限原语→RCE 提升方法论，能跨目标（Symfony、vBulletin、Drupal、SPIP、WSO2、GLPI、Ninja Forms）系统性地把未认证/受限前提推进到 RCE。；vBulletin 不可达反序列化 RCE（'The bug was due to an improper handling of non-scalar data in the ORM, which led to an arbitrary deserialisation.'）；Symfony secret fragment RCE（经 _path 参数调任意 PHP 函数或类方法）；团队级 SQLi-to-RCE / 文件上传-to-RCE 跨目标序列（WSO2、GLPI、Drupal PostgreSQL、Ninja Forms、SPIP，正文部分未逐字抓取，机制为推断）

置信度：medium；替代解释：该受限原语→RCE 方法论的部分产出可能为 Ambionics 团队多人协作结果而非 Charles Fol 个人独立产出；列表页未列个人作者署名，逐篇个人作者身份无法核证，只能作为团队级产出方向的能力曲线描述。

证据：cf-rev4-001, cf-rev2-006, cf-community-method-reuse-series, cf-works-004, cf-works-005, cf-ext-05

## 可迁移与不可迁移

- 可迁移：把单点漏洞利用方法固化为带跨版本兼容测试脚本的通用工具，而非仅作单次披露附属物（PHPGGC 模式）。
- 可迁移：按漏洞族发布独立可运行 exploit 仓库，使工具建设与漏洞披露一体化（ambionics 组织仓库清单模式）。
- 可迁移：对自研工具做模糊测试，观察工具行为异常作为新漏洞研究的入口（该回路目前仅单实例支撑：wrapwrap→CVE-2024-2961，作为可迁移做法的普遍性未由一手证据核证）。
- 可迁移：沿应用层 → 运行时 → 原生库的路径逐层展开研究目标，并把同一底层缺陷经运行时通道与运行时边界两条路径桥接回应用层 RCE。
- 可迁移：对受限（盲）原语条件下的利用按难度递进切分并逐部分公开发表，形成可复用的利用条件边界处理方法。
- 可迁移：新发现显式引用同行前置研究建立方法链条，并把新向量定位为既有失效攻击面的替代（如 CVE-2024-2961 作为 PHP 8.0 后 PHAR 反序列化攻击的替代）。
- 不可直接迁移：发布渠道与团队品牌绑定：研究以 Ambionics / Web Exploitation 分类在 Lexfo 安全博客发表，工具仓库托管于 ambionics 组织，团队品牌与个人工具品牌相互绑定，个人作者署名在列表页与分类页不显示。
- 不可直接迁移：工具→新漏洞的迭代回路目前仅单实例支撑（wrapwrap→CVE-2024-2961），作为可迁移做法的普遍性未由一手证据核证；不应由单实例归纳为普遍迭代机制。
- 不可直接迁移：CVE-2024-2961 经 php://filter 链桥接 RCE 的成果依赖 PHP 运行时对 php://filter 与 iconv 的特定实现与版本范围（PHP 7.0–8.3），不具备跨运行时实现的可迁移性。
- 不可直接迁移：协调披露时间线（2024-03-26 报告、2024-04-04 通知发行版、2024-04-17 公开）依赖 glibc 上游维护者的快速响应与发行版协作，该外部协作条件为特定项目与时期的环境条件，不可直接迁移。

## 复核问题

- stages[0].capability_change：原措辞 '把反复构造 gadget chain 的经验沉淀为可复用、可测试的通用工具' 中的 '沉淀' 为比喻性用词（化学沉淀隐喻），且与同文档 mechanisms[0].repeated_practice '把单点漏洞利用方法固化为通用工具' 的 '固化'、mechanisms[0].alternative_explanation '个人独立积累' 的 '积累' 用词不一致；rev2 已对同词根 '自驱沉淀' 判定含比喻并改写。改写方向：将 '沉淀' 改为 '固化'，使该句改为 '把反复构造 gadget chain 的经验固化为可复用、可测试的通用工具'，与同文档用词统一并消除比喻。
- mechanisms[2].alternative_explanation：当前替代解释为 '该受限原语→RCE 方法论的部分产出可能为 Ambionics 团队多人协作结果而非 Charles Fol 个人独立产出'，可补充说明受限原语→RCE（SQLi-to-RCE、文件上传-to-RCE、未认证入口-to-RCE）在 PHP 安全研究中为常见研究方向类别，并非研究对象个人独创，以进一步增强替代解释的克制性。改写方向：在 alternative_explanation 末尾补充 '此外，受限原语→RCE 为 PHP 安全研究中的常见研究方向类别，并非研究对象个人独创'。

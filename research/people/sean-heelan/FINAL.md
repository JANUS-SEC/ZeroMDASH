# Sean Heelan：漏洞研究成长分析

- 擅长领域：二进制漏洞/编译器/AI 辅助挖掘
- 独立复核：pass · 91/100

## 成长阶段

- **2008 · 学术起点：自动利用生成主线确立**：2008 年完成硕士论文，方向为自动利用生成（Automatic Exploit Generation, AEG），本人自述该工作属于 AEG 领域较早的尝试。该阶段将后续十余年的主题选择定锚为'自动化漏洞发现与利用生成'，而非分散于单一兴趣。学位授予机构在本人页面未注明，保留为资料缺口。（置信度：high）
  - 证据：sh-works-2008-msc-aeg, sh-deep-001, sh-tl-001, sean-ext-02
- **2009-2012 · 工业转入：利用开发与形式化方法工具建设并行**：2009 年加入 Immunity Inc. 任漏洞研究员与利用开发员，为 CANVAS 编写利用与工具；本人自述任 DARPA 资助项目 ILLITHID（面向二进制软件的模型检验工具）研究 lead，并将 SMT 求解驱动的分析集成进 Immunity Debugger。该阶段把学术 AEG 导向真实二进制产品，使模型检验/SMT 求解成为可复用技术栈。按复核要求落实降级：'任 ILLITHID 研究 lead'与'DARPA 资助'均系本人 About 自述，DARPA 资助属性与组织层面认可未经独立第三方核验，不作能力被组织认可的断言。（置信度：medium）
  - 证据：sh-works-2009-2012-immunity-illithid, sh-deep-002, sh-tl-003, sean-ext-01, sh-decision-01-immunity-from-academia-to-industry
- **2012-2016 · 工具产品化与方法栈扩展：运行时数据流跟踪、解释器 fuzzing、堆原语脚本**：2012 年创办 Persistence Labs，开发 SemTrax（细粒度运行时数据流跟踪），面向半自动化逆向与漏洞发现；同年发表 Better Interpreter Fuzzing with Clang（构建 InterParser，以 libclang 解析 PHP 源码、映射 C 后端函数到 PHP 等价函数与参数类型，处理 518 个函数）。同期围绕 TCMalloc 持续产出利用原语与 GDB Python API 脚本，把 4-to-N 字节溢出经 insert-to-FreeList 转为写原语。技术栈从模型检验/SMT 扩展到运行时数据流跟踪、编译器前端驱动的模糊测试与堆原语脚本化，对象由单一分配器扩展到语言解释器，为博士阶段灰盒 AEG 奠定方法与目标基础。（置信度：high）
  - 证据：sh-works-2012-persistence-labs-semtrax, sh-works-2012-interpreter-fuzzing-clang, sh-deep-003, sh-decision-02-persistence-labs-founding, sh-decision-10-clang-interpreter-fuzzing-2012, sh-tl-008, r1-tcmalloc-2011-verified
- **2016-2020 · 学术系统化：牛津 PhD 灰盒 AEG 与 Oxford 合著组复合反馈**：2016 年入学牛津攻读博士，重拾自动利用生成课题，刻意选择已少有人研究的堆溢出（而非'被研究殆尽'的栈溢出）与此前无 AEG 覆盖的语言解释器为目标；基于性能与可扩展性判断放弃符号执行，转向纯 greybox/fuzzing 方法。通过审查 DARPA Cyber Grand Challenge 各系统识别出 8 项开放问题（缺乏 human-in-the-loop、无 exploitation primitive 概念、集中于栈溢出、未处理信息泄露与 ASLR、未覆盖解释器/浏览器/内核等），据此定位 PhD 研究方向。2018 年在 USENIX Security、2019 年在 ACM CCS 发表 Automatic Heap Layout Manipulation for Exploitation 与 Gollum: Modular and Greybox Exploit Generation for Heap Overflows in Interpreters。按复核补证落实：经本人 BibTeX gist 与 USENIX Security 2018 官方页面双源核验，两篇论文作者均为 Sean Heelan、Tom Melham、Daniel Kroening，三人均隶属 University of Oxford；PhD 授予机构 Oxford 已独立核验。反馈回路从'单纯顶会匿名审稿'扩展为'Oxford 合著组（Melham/Kroening）+ USENIX/CCS 顶会匿名审稿'的复合结构；2020 年博士论文将此前散布于演讲与论文的 AEG、堆布局操控、解释器目标整合为统一系统，与 2008 年硕士主题构成十二年主题闭环。（置信度：high）
  - 证据：sh-deep-004, sh-deep-005, sh-deep-006, sh-deep-007, sh-deep-010, sh-tl-011, sh-tl-013, sh-tl-014, sh-tl-015, sh-tl-016, sh-decision-03-oxford-phd-aeg, r1-gollum-ccs2019-bibtex, r1-usenix2018-heelan-authors
- **2019-2023 · 跨域迁移：生产级性能剖析与 AI Agent 工程**：2019 年联合创办 Optimyze 任 CTO，开发 Prodfiler（数据中心级、低于 1% CPU 开销的连续性能剖析器，可剖析内核、用户态及编译型/解释型代码且无需重新部署或调试符号）；2021 年末随公司被 Elastic 收购，Prodfiler 转 Elastic Universal Profiler，连续剖析代理后开源并捐赠 OpenTelemetry。2021-2023 任 profiling 团队 lead 后 tech lead，并在 GPT-4 发布前后组建并领导 Elastic AI Agent for Observability 团队。该阶段将'大规模数据驱动自动化分析'内核从安全迁移到性能工程，并完成'创办→被收购→大厂团队 lead→开源捐赠'的工程交付链路；AI Agent 工程经验为 2023 年后 LLM 驱动漏洞研究提供工程基础。职业角色、收购时间与团队组建均系本人自述，未经第三方公告交叉核验。（置信度：medium）
  - 证据：sh-works-2019-2021-optimyze-prodfiler, sh-deep-008, sh-tl-015, sh-tl-017, sh-tl-018, sean-ext-03, sh-decision-04-optimyze-profiling-pivot, sh-decision-05-elastic-llm-agent-team
- **2023-2026 · 回归主线：LLM 驱动的漏洞研究与利用生成**：2023 年起从事独立研发，方向为基于 LLM 的漏洞研究与利用生成自动化；同年发布 sysgrok/findfaster（把多步人工'找更快替代库+benchmark+推荐'压缩为单步 LLM 调用，并显式记录幻觉失败如 TurboTiff）。2025 年以 OpenAI o3 仅调用 API（无 agent 框架、无工具调用）发现 Linux 内核 ksmbd 中 smb2_session_logoff 的释放后使用零日 CVE-2025-37899，并以先前手工审计发现的 CVE-2025-37778 作为基准量化评估 o3；2026 年以 Opus 4.5 与 GPT-5.2 构建 agent，对 QuickJS 中由其 Opus 4.5 漏洞发现 agent 找到的零日生成利用，6 场景产出 40+ 利用，引入成本/时间/token 量化与多场景对比。按复核要求落实：本阶段 confidence 从 high 降为 medium——2025 ksmbd 部分有公开 CVE + 修复 commit + 公开 prompt 工件 + 一手抓取支撑，2026 QuickJS 部分因 discovery agent writeup 未取得、发现主体未独立核验，单列标注为本人自述待核验。（置信度：medium）
  - 证据：sh-works-2023-independent-llm-vr, sh-works-2025-cve-2025-37899-o3, sh-works-2026-industrialisation-llm-exploits, sh-deep-009, sh-tl-019, sh-tl-020, sh-tl-021, sean-ext-04, sean-ext-05, sean-ext-06, sean-ext-07, sh-decision-06-independent-research-llm, sh-decision-07-o3-ksmbd-cve-2025-37899, sh-decision-08-industrialisation-of-exploit-generation, sh-decision-09-llm-for-optimisation-2023, r1-cve-blog-fpr-snr-verified

## 主要成长机制

### 机制 A：工具建设与公开 writeup 驱动的可重复研究

起点：2011 年起围绕 TCMalloc 堆利用与 GDB Python API 持续产出利用原语与调试脚本，把 4-to-N 字节溢出经 insert-to-FreeList 转为写原语并发布姊妹篇 Heap Scripts；同期 2012 年 Better Interpreter Fuzzing with Clang 构建 InterParser 以 libclang 映射 PHP C 后端函数到用户空间等价函数与参数类型。早期即形成'针对具体目标构建小工具、把人工经验转化为可复用自动化'的取向。

练习与反馈：跨十余年重复把研究方法固化为可复用工具并配套公开 writeup：2017 funserialize（AFL fuzzing PHP unserialize，提供 get.sh/build.sh/fuzz.sh 一键流程、从解析器提取的字典、基于 PHP 文档与历史漏洞构造的种子）；2012 InterParser；2011 TCMalloc 堆脚本；2023 sysgrok/findfaster（开源 LLM 工具化）；2025 o3_finds_cve-2025-37899（公开 prompt 文件与示例输出）；2026 anamnesis-release（自动利用生成研究代码与实验数据）。；公开 writeup 自身即把内部方法暴露给同行复核；GitHub Pair Extraordinaire 与 Pull Shark x3 成就指示存在跨仓库合著与拉取请求参与（具体协作者与 PR 未逐一核对，停留在推断层级）；CVE-2025-37899 博文评论区读者公开提出替代工具（OpenAI Codex 用于 VirtualBox 逃逸）、成本核算、模型横向比较与哲学性质疑，作者逐条公开回应并把措辞由 comprehend 调整为 solve。该公开对话既检验结论也暴露需澄清的表述。

能力与结果：形成'研究方法 → 可复用工具 → 公开 writeup → 同行/评论者反馈'的闭环，使方法可被他人独立复现与扩展（funserialize 与 anamnesis-release 在 GitHub 上均有数百 stars）。中间能力为'以可复现工件而非孤立发现呈现研究'，并显式记录方法局限（funserialize 'there's no secret sauce'、sysgrok 幻觉失败、ksmbd 信噪比与假阳性）。；2011 TCMalloc insert-to-FreeList 原语与 GDB Python API 堆脚本（一手正文核证 r1-tcmalloc-2011-verified）；2012 InterParser 以 libclang 映射 518 个 PHP 函数（一手正文核证 sh-decision-10）；2017 funserialize 公开仓库与一键流程（一手正文核证 sh-works-2017-php-unserialize-afl）；2025 o3_finds_cve-2025-37899 公开 prompt 工件（一手核证 sh-works-2025 + r1-cve-blog-fpr-snr-verified）；2026 anamnesis-release 公开实验数据与代码（一手核证 sh-works-2026-industrialisation-llm-exploits）；公开呼吁前沿实验室与 AI Security Institutes 以真实零日、硬目标评测并公开结果（含零产出），批评基于 CTF 与合成数据的评测'信息量不足'

置信度：high；替代解释：可迁移做法的竞争性解释为'自述导向的公开习惯'：大量 writeup 来自本人博客与 GitHub，缺乏第三方对工具实际复用情况的独立核证（Pair Extraordinaire/Pull Shark 成就对应的具体协作者与 PR 未逐一核对）。stars 数与评论区反馈可部分缓解，但未穷尽检索其工具被他人引用或独立复现的记录。

证据：r1-tcmalloc-2011-verified, sh-works-2012-interpreter-fuzzing-clang, sh-works-2017-php-unserialize-afl, sh-works-2023-independent-llm-vr, sh-works-2025-cve-2025-37899-o3, sh-works-2026-industrialisation-llm-exploits, sh-decision-09-llm-for-optimisation-2023, sh-decision-10-clang-interpreter-fuzzing-2012, community-open-sourced-artefacts, community-feedback-comments-cve-2025-37899, community-bug-tracker-references, sean-ext-07

### 机制 B：以已知漏洞为基准的量化重复评估与工具复审反馈

起点：2023 年 sysgrok 已显式记录 LLM 幻觉失败（TurboTiff）并开源；2025 年 ksmbd 研究以先前手工审计发现的 CVE-2025-37778 作为基准评估 o3，形成'以已知漏洞建立基准 + 固定 prompt + 重复运行 + 人工复核'的方法学模板。该起点条件依赖其既有手工审计能力与可公开的基准漏洞。

练习与反馈：2025 年用 Simon Willison 的 llm CLI 对约 3.3k 行/27k token 代码以反 UAF 为系统提示每配置跑 100 次；扩展到约 12k 行/100k token 全命令处理再跑 100 次；对 Claude Sonnet 3.7 与 3.5 同样跑 100 次横向比较。2026 年把方法论系统化扩展到多模型 agent 与端到端利用链生成，引入成本/时间/token 量化（最难场景约 50M token、3 小时、约 50 美元）与多场景对比（ASLR/NX/RELRO/CFI/shadow-stack/seccomp 组合）。；按复核一手核证落实：Heelan 自述其对 CVE-2025-37778（Kerberos 认证路径 UAF）提出修复 sess->user = NULL，并在阅读 o3 对 CVE-2025-37899 的 bug 报告后承认该修复不足——原因在于 logoff 处理器已自行设置 sess->user = NULL，而 SMB 协议允许两条连接绑定同一 session，Kerberos 认证路径无法阻止另一线程在该字段释放后、置空前的窗口期内解引用。即'用工具复审自己补丁后发现原补丁不足'的工具反馈闭环，一手材料支持原措辞。此外评论者 Ryan 的哲学性质疑促使作者把表述由 comprehend 调整为 solve。

能力与结果：形成可重复、可批判的工程化研究范式：把 LLM 发现能力表达为概率而非全称判断（自述小于 10k 行可表示的问题'有合理概率 o3 能解出或协助解出'），并明确区分'可离线搜索解空间'与'需实时对抗交互'两类任务的自动化前景。中间能力为'以量化基准与统计（命中率/误报/漏报/成本）评估新方法，而非单次结果展示'。；2025 发现 CVE-2025-37899（公开 CVE + 修复 commit torvalds/linux 2fc9feff + 公开 prompt 工件）；按 r1-cve-blog-fpr-snr-verified 一手核证的有效性边界：3.3k LoC 基准下 o3 命中 8/100、假阳性 28/100、假阴性 66/100；12k LoC 上下文下降至 1/100；0-day 发现信噪比约 1:50；约 100k token 版本 100 次运行成本约 116 美元；Claude Sonnet 3.7 为 3/100、Sonnet 3.5 为 0/100（横向比较）；2026 QuickJS 6 场景产出 40+ 利用，GPT-5.2 解出全部、Opus 4.5 除两例外全部解出（最难场景约 50M token、3 小时、约 50 美元）——2026 QuickJS 部分因 discovery agent writeup 未取得、发现主体未独立核验，单列标注为本人自述待核验

置信度：high；替代解释：竞争性解释一：'量化基准'是 LLM 评测领域的通用做法，并非其个人特有；其区分度在于以真实零日与已知漏洞同时作基准、并公开假阳性结构。竞争性解释二：信噪比 1:50 与高假阳性率可能反映 o3 在该任务上的固有局限，而非其方法学的有效性——若换用更强模型或更优系统提示，假阳性结构可能改变，机制有效性边界系于当时模型能力，不具外推稳定性。2026 QuickJS 部分发现主体未独立核验，进一步限制该机制在利用生成侧的可断言强度。

证据：sh-works-2025-cve-2025-37899-o3, sh-works-2026-industrialisation-llm-exploits, sh-decision-07-o3-ksmbd-cve-2025-37899, sh-decision-08-industrialisation-of-exploit-generation, sh-decision-09-llm-for-optimisation-2023, sean-ext-04, sean-ext-05, sean-ext-06, r1-cve-blog-fpr-snr-verified, community-feedback-comments-cve-2025-37899, community-philosophical-exchange

### 机制 C：缺口识别驱动的选题与目标选择

起点：2016 年通过审查 DARPA Cyber Grand Challenge 各系统识别出 8 项开放问题，作为 PhD 研究出发点；该起点条件依赖其既有工业经验以识别'真实系统做不到什么'。

练习与反馈：2016 年基于 GCQ 缺口（无 human-in-the-loop、无 exploitation primitive 概念、集中于栈溢出、未处理信息泄露与 ASLR、未覆盖解释器/浏览器/内核）选择堆溢出与语言解释器为目标；2017 funserialize 针对 PHP 团队不再将 unserialize 实现缺陷视为安全问题的政策提出技术异议；2026 年公开批评基于 CTF 与合成数据的 LLM 安全评测'信息量不足'，呼吁以真实零日硬目标评测并公开结果（含零产出）。；Oxford 合著组（Melham/Kroening）与 USENIX/CCS 匿名审稿构成复合反馈结构，对 PhD 研究方向的选择与系统化形成外部约束；PHP unserialize 文章引用 PHP internals 邮件列表与 bug tracker 条目（71311、75006、70068）作为同类历史漏洞参照，与上游分类标准对齐。

能力与结果：形成'以对既有系统的系统调研定位未被解决的问题，而非凭单一兴趣选题'的中间能力，并主动选择低竞争、未被覆盖的研究空白（堆溢出而非'被研究殆尽'的栈溢出；解释器此前无 AEG 覆盖）。；2018 USENIX Security Automatic Heap Layout Manipulation for Exploitation（Oxford 合著组，一手 r1-usenix2018-heelan-authors 核证）；2019 ACM CCS Gollum（一手 r1-gollum-ccs2019-bibtex 核证作者 Heelan/Melham/Kroening，Oxford）；2020 博士论文 Greybox Automatic Exploit Generation for Heap Overflows in Language Interpreters 整合 AEG/堆布局/解释器目标；2026 公开提出可操作的评测标准转向（真实零日硬目标、公开零产出结果）

置信度：high；替代解释：竞争性解释一：缺口识别是博士选题的常规路径，并非其个人特有；其区分度在于把缺口识别延续到产业实践（PHP 政策异议）与 LLM 评测标准批评，形成跨阶段一致性。竞争性解释二：'低竞争空白'选择可能部分受可行性与博士学制约束驱动（栈溢出已饱和、解释器有现成 GCQ 缺口），而非纯主动判断；Oxford 合著组的反馈约束也可能使选题向既有小组能力靠拢。USENIX/CCS 顶会录用本身是缺口识别有效性的间接外部印证，但无法排除偶然因素。

证据：sh-deep-005, sh-deep-006, sh-deep-007, sh-deep-010, sh-tl-014, sh-tl-015, sh-tl-016, sh-works-2017-php-unserialize-afl, sh-decision-03-oxford-phd-aeg, sh-decision-08-industrialisation-of-exploit-generation, community-upstream-tracking-php, r1-gollum-ccs2019-bibtex, r1-usenix2018-heelan-authors

### 机制 D：人机协同而非全自动的自动化观

起点：按复核要求落实降级：ILLITHID 定位为'辅助人类专家'系本人 About 自述，未取得一手技术 writeup，不作机制起点强证据；改以 2011 年 IEEE Security & Privacy Magazine 文章 Vulnerability Detection Systems: Think Cyborg, Not Robot（本人研究索引页一手确证）作为机制起点证据。该文章提出人机协同而非全自动的漏洞检测立场。

练习与反馈：2011 年起在产业杂志提出'人机协同而非全自动'立场；2009-2012 Immunity 期间 ILLITHID 被自述定位为辅助人类专家的工具（按复核该定位降级为本人自述）；2016 PhD 通过 GCQ 缺口识别将'缺乏 human-in-the-loop 能力'列为开放问题之一；2023 年后 LLM 工作中始终保留人工复核输出（ksmbd 100 次运行人工审阅过滤假阳性）。十余年间自动化观保持一致：以工具扩展人而非取代人。；2025 年公开表述'机器不会取代你，但能显著提升效率'，并把避免误报的系统提示自评为'a prayer, rather than anything resembling science or engineering'——把人工过滤的不可靠性作为方法学约束公开承认。

能力与结果：形成稳定的'human-in-the-loop + 可离线搜索解空间自动化'中间立场：把可离线搜索解空间（漏洞发现、利用生成）视为可工业化，把需实时对抗交互（如横向移动）视为更难工业化；明确利用生成是工业化理想情形因验证直接。；2011 IEEE S&P Magazine Think Cyborg, Not Robot（本人研究索引页一手确证 sh-tl-006）；2016 PhD 以'缺乏 human-in-the-loop 能力'为 GCQ 首要开放问题（sh-deep-005 一手核证）；2025 ksmbd 人工审阅 100 次运行过滤假阳性结构（r1-cve-blog-fpr-snr-verified 一手核证）；2026 区分可离线搜索解空间与需实时对抗交互的自动化前景（sh-works-2026 一手核证）

置信度：medium；替代解释：竞争性解释一：人机协同立场可能是对当时 LLM 能力不足的事后合理化（2025 年模型假阳性高，故强调人工复核；待模型能力提升，立场可能漂移）。竞争性解释二：'cyborg'语汇在 2011 年产业界并不罕见，其区分度有限；机制有效性更多依赖 2016 PhD 与 2025 实践中的反复落实，而非单一文章。此外 ILLITHID 起点证据经复核降级为本人自述，机制在 2009-2012 段的强度受限。

证据：sh-tl-006, sh-deep-002, sh-deep-005, sh-works-2025-cve-2025-37899-o3, sh-works-2026-industrialisation-llm-exploits, sh-decision-07-o3-ksmbd-cve-2025-37899, sh-decision-08-industrialisation-of-exploit-generation, sean-ext-05, r1-cve-blog-fpr-snr-verified

## 可迁移与不可迁移

- 可迁移：以已知漏洞建立基准、固定 prompt、重复运行 N 次再人工审阅过滤假阳性的评估范式，可迁移到任何以 LLM 辅助代码审计的研究；关键是把命中率/假阳性/假阴性/成本/信噪比作为显式约束公开记录，缓解幸存者偏差。
- 可迁移：把研究方法固化为可复用工具并配套公开 writeup（一键流程脚本、字典、种子、prompt 文件、示例输出、实验数据），使同行可独立复现与扩展；以可复现工件而非孤立发现呈现研究。
- 可迁移：以对既有系统的系统调研定位未被解决的问题作为选题依据，主动选择低竞争、未被覆盖的研究空白（如堆溢出而非栈溢出、解释器而非浏览器），而非凭单一兴趣选题。
- 可迁移：把人工多步工程流程（如'找更快替代库+benchmark+推荐'）压缩为单步 LLM 调用并开源，同时显式记录幻觉失败与方法局限，而非仅展示成功结果。
- 可迁移：把结论表达为概率而非全称判断，并明确区分'可离线搜索解空间'与'需实时对抗交互'两类任务的自动化前景，避免对外推边界作全称断言。
- 可迁移：公开呼吁以真实零日、硬目标评测 LLM 安全能力并公开结果（含零产出），批评基于 CTF 与合成数据的评测，把内部方法暴露给同行检验形成持续外部反馈。
- 不可直接迁移：2009-2012 Immunity Inc. 提供的利用开发与商业化利用框架（CANVAS）持续训练环境，以及 DARPA 资助 ILLITHID 项目的研究 lead 角色——后者与组织层面认可均系本人自述，DARPA 资助属性未经独立第三方核验，该工业起点条件不可简单复制。
- 不可直接迁移：牛津大学 PhD 期间与 Tom Melham、Daniel Kroening（Oxford 形式化方法组）的合著关系及 USENIX/CCS 顶会匿名审稿构成的复合反馈结构，属特定学术网络与机构资源，非个人可迁移方法。
- 不可直接迁移：2019-2023 Optimyze/Elastic 的'创办→被收购→大厂团队 lead→开源捐赠'链路，依赖特定时机（GPT-4 发布、被收购窗口）与组织资源，收购时间与团队组建均系本人自述未经第三方公告核验，非个人可重复路径。
- 不可直接迁移：ksmbd CVE-2025-37899 的研究以'本人先前手工审计已发现基准漏洞 CVE-2025-37778'为前提，该基准漏洞的获得依赖其既有手工审计能力与对 ksmbd 的先期投入，外部研究者未必具备同等基准。
- 不可直接迁移：2026 QuickJS 工作依赖其'Opus 4.5 vulnerability discovery agent'已先发现零日作为利用生成输入；该 discovery agent writeup 未取得、发现主体未独立核验，其端到端利用生成链的可复现性受此未核验环节限制。
- 不可直接迁移：大量 writeup 来自本人博客与 GitHub 自述，身份与职业链虽内部一致但缺 LinkedIn、Elastic 收购公告、OpenTelemetry 捐赠记录、DARPA 项目页等第三方交叉核验；外部研究者复现其完整职业背景时受此限制。

## 复核问题

- 无关键事实、人物同一性或来源错误。每个成长阶段与机制均引用至少一个 verified_in_run=true 的一手来源（主要为 About 页面、CVE-2025-37899 博文、BibTeX gist、USENIX Security 2018 官方页面、2011 TCMalloc 博文、2017 PHP unserialize 博文、2026 LLM 工业化博文）；Gollum CCS 2019 作者归属经一手双源核验（r1-gollum-ccs2019-bibtex + r1-usenix2018-heelan-authors），原 WebSearch 噪声已作为搜索噪声剔除并记录于 tensions。confidence 分档（stage 2/5/6、mechanism A/B 局部、mechanism D 为 medium）与 medium 段对应的'本人自述/未独立第三方核验'标注一致，因果强度未过度延伸。mechanism B 明确限定 high confidence 仅适用于 2025 ksmbd 部分，2026 QuickJS 部分因 discovery agent writeup 未取得而单列标注为本人自述待核验，这是因果克制的体现而非缺陷。
- mechanism A intermediate_capability：删除'funserialize 与 anamnesis-release 在 GitHub 上均有数百 stars'的 stars 数表述，或改为'两项仓库（funserialize、anamnesis-release）公开可访问，存在性由对应一手博文核证'。原措辞以未一手核证的 star 计数作为'可被他人独立复现与扩展'的依据，超出已核证材料；改写后保留仓库公开可访问这一可核证事实，去除未核证流行度指标。
- open_questions 中 Black Hat/POC 演讲条目：将'演讲事实、具体年份与同伴反馈均未一手确证'缩窄为'2017 年 Black Hat EU《Heap Layout Optimisation for Exploitation》演讲事实与年份已由 sh-tl-013 一手索引页确证；Black Hat US、POC 及其余年份演讲的议程正文与同伴反馈未一手核验'。原措辞范围过宽，与已核证的 sh-tl-013 不一致。
- transferable_practices 或 non_transferable_conditions 增补一条幸存者偏差自省：明确本分析以公开产出（公开博客、GitHub 仓库、公开 CVE 与利用生成成果）的研究者为对象，尝试 LLM 辅助漏洞研究但未公开产出或放弃该方向的研究者不可观测，故可迁移做法与阶段成长弧的外推受该可见性偏差限制；mechanism B 在单点发现层面以公开假阳性/假阴性结构部分缓解，但阶段级叙事未显式标注。

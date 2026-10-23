# 未通过独立复核

已达到最大修订次数 4；本文件是审计草稿，不得进入跨人物比较。

# Stephen Röttger：漏洞研究成长分析

- 擅长领域：浏览器与 Linux 内核漏洞
- 独立复核：revise · 74/100

## 成长阶段

- **2015 年 1 月（ntpd 文章发布日；正文自述学习 fuzzing 起始于此前数月，CVE-2014-9295 于 2014-12-20 在 NVD 发布；个人 fuzzing 学习确切起始时间未见一手来源） · fuzzing 入门与首个公开漏洞利用**：对应 CVE-2014-9295（据 ntpd 文章自述的工作内容与时点 roettger-deepconv-01，该 CVE 与其文章所述 fuzzing 工作对应；NVD 记录 sr-r1-tl-01 未直接署名发现者，属间接溯源）。在该阶段形成以先验背景加复杂度可控为标准的领域进入与目标选择能力，并产出首个 OS X 利用。文章以 Project Zero guest post 形式发表（sr-r1-conv-01，Chris Evans 前言明确其为 the first Project Zero guest blog post），客座作者身份而非在职成员。（置信度：high）
  - 证据：roettger-deepconv-01, roettger-deepconv-02, roettger-deepconv-03, sr-r1-tl-01, sr-r1-conv-01
- **2018 年 12 月（据仓库命名 35c3ctf_chals 关联 35C3 推断；GitHub profile 未显示仓库最后更新时间，确切入库时间未见一手来源） · CTF 出题与赛事基础设施搭建**：在 GitHub 账户 sroettger 下公开维护 CTF 题目仓库（35c3ctf_chals）与 GCE 部署工具（gce-ctf、play-my-challenge），并 fork google/security-research-pocs 与 google/nsjail，体现工具建设与赛事基础设施搭建的实践习惯。需显式标注：GitHub 账户 sroettger 与本名 Stephen Röttger 的同一性未取得一手平台交叉证明（GitHub profile 不显示真实姓名、雇主、地理位置或社交链接），身份关联仅为姓氏拼写与研究方向吻合的间接推断，故该阶段仅作背景线索而非可核能力变化阶段。（置信度：low）
  - 证据：sr-works-01, sr-works-02, sr-works-03
- **2019 年 5 月（Trashing the Flow of Data 发表日） · Chrome V8 TurboFan JIT 全调用点手动审计**：Project Zero 发表 Trashing the Flow of Data（guest post，sr-r3-01）。系统性审计 Chrome TurboFan JIT 编译器对 Array.prototype.indexOf/includes 处理中缺少运行时检查的漏洞，对危险 API 模式审计所有调用点（引文 "When I noticed this function in the past, I was convinced that one of the callers will get it wrong and audited all the call sites"），将漏洞从信息泄露升级为任意写原语。与 Samuel Groß（fuzzilli 作者）通过 fuzzilli 模糊测试独立发现同一漏洞形成交叉验证；二人同属 Project Zero 的雇佣关系未由一手来源核实（ntpd 为 guest post 见 sr-r1-conv-01，team.html 抓取 404）。文末反思应主动向团队预警危险 API 模式而非仅报告漏洞。该文为 guest post（sr-r3-01 引文 "In my last guest blog post 'Trashing the Flow of Data'" 由 RIDL 文反向确认）。（置信度：high）
  - 证据：stephen-ext-01, sr-r3-01
- **2020 年 2 月（Escaping the Chrome Sandbox with RIDL 发表日） · 跨领域迁移至硬件侧信道与完整沙箱逃逸 exploit chain 构建**：Project Zero 发表 Escaping the Chrome Sandbox with RIDL（guest post，sr-r3-01）。在 2019 年 TurboFan 工作展示的 Chrome 代码审计与利用构建能力基础上，跨入此前自认不擅长的硬件漏洞领域（引文 "i ignored hardware vulnerabilities for the longest time since they are way out of my comfort zone"），将 RIDL/MDS 微架构数据采样与 Chrome Mojo IPC 128-bit port name 泄露结合，分别针对 Linux（MFBDS 变体，Xeon Gold 6154）与 Windows（TAA 变体，Core i7-7600U）开发两个完整沙箱逃逸 exploit。作者自述缓解措施曾令其误判漏洞已被解决（引文 "The focus on mitigations certainly gave me a false sense that the vulnerabilities have been addressed"），并提出更新微码、禁用超线程（disable hyper-threading (HT)）等操作建议。（置信度：high）
  - 证据：stephen-ext-02, sr-r3-01
- **2023 年 10 月 9 日（v8.dev 文章发表日） · V8 控制流完整性架构方向**：以本人署名在 V8 官方博客（v8.dev）发表 Control-flow Integrity in V8，系统介绍在 V8 中实现前向/后向控制流完整性及 JIT 内存完整性的方法。从早期 CTF 出题/利用方向与浏览器侧漏洞挖掘，转向浏览器运行时安全架构设计，并在 V8 团队官方渠道独立署名发文。此阶段标志其公开技术输出进入浏览器运行时安全架构阶段；该文为 V8 团队官方博客署名，与前三篇 Project Zero guest post 的发表渠道不同。（置信度：medium）
  - 证据：srottger-tl-02

## 主要成长机制

### 以先验背景加复杂度可控为标准的领域进入与目标选择

起点：2015 年决定开始学习 fuzzing 时，选取 ntpd 作为首个目标的判据由本人自述给出：具备 NTP 协议先验背景，且协议足够简单适合作为学习经历（roettger-deepconv-01 引文 "I chose the reference implementation of the Network Time Protocol (NTP), ntpd, as my first target, since I have some background with NTP ... the protocol seemed simple enough to be a good learning experience"）。目标选择由可核验判据驱动，而非笼统兴趣。

练习与反馈：在可观察样本中，该判据在 2015 ntpd 入门（先验协议背景加简单复杂度）与 2019 TurboFan JIT（选取已知危险 API 模式 JSCallReducer::ReduceArrayIndexOfIncludes 进行全调用点审计）两处出现；2020 RIDL 工作亦显式以引文 "In my last guest blog post 'Trashing the Flow of Data'" 串联前序浏览器侧能力作为迁移起点。需标注：跨时期重复性证据有限，2015→2019→2020 三处样本均依赖本人公开发表 writeup，未发表工作不可见。；2015 文章在公开 writeup 中显式记录目标选择判据；2019 文章记录遇到 GC 移动对象障碍后通过重分配解决的迭代过程；2020 文章记录以引文 "How to replace step 2. and 3. above with a CPU bug" 叙述以 RIDL/MDS 硬件数据采样替换前序软件 info leak 的迭代选择（sr-r3-01）。反馈来源为本人公开 writeup 中的自述式迭代记录，非外部评审或导师反馈。

能力与结果：形成以先验背景加复杂度可控为标准的领域进入与目标选择能力，并能在新领域沿用此判据选取切入点。；2015 ntpd fuzzing 入门并对应 CVE-2014-9295（间接溯源）；2019 TurboFan JIT 全调用点审计发现缺少运行时检查漏洞并升级为任意写原语；2020 RIDL 工作跨入硬件侧信道领域并构建完整沙箱逃逸 exploit chain

置信度：medium；替代解释：竞争性解释：目标选择的可观察一致性可能部分由 Project Zero 发表平台对 writeup 叙事结构的要求塑造，而非纯个人判据；三篇 Project Zero 文章均为 guest post（sr-r1-conv-01、sr-r3-01），在职身份未由一手来源证实，发表渠道与披露政策对 writeup 自述内容的呈现存在约束。组织资源对成果的支撑作用包括硬件访问（Xeon Gold 6154、Core i7-7600U）、跨厂商披露渠道（Apple/Microsoft/Chrome）、fuzzilli 工具生态（Samuel Groß）、Chrome/V8 源码与 issue tracker 可访问性、Project Zero 发表平台与披露政策，个人能力归因应据此校准。

证据：roettger-deepconv-01, sr-r1-tl-01, stephen-ext-01, stephen-ext-02, sr-r3-01

### 系统性审计危险 API 模式的所有调用点

起点：2019 年 TurboFan 工作前，作者对危险 API 模式形成预判：注意到某函数后确信会有调用点用错，进而审计所有调用点（stephen-ext-01 引文 "When I noticed this function in the past, I was convinced that one of the callers will get it wrong and audited all the call sites"）。

练习与反馈：在 2019 TurboFan 工作中对 Array.prototype.indexOf/includes 相关 API 审计全部调用点；2020 RIDL 工作中沿用系统性审计方法分析 Chrome Mojo IPC port name 泄露的利用方式，并对 RIDL/MDS 数据采样路径进行系统性分析。需标注：跨时期重复性证据限于两篇公开发表 writeup（2019、2020），非多时期大样本重复。；2019 文章记录与 Samuel Groß（fuzzilli 作者）通过模糊测试独立发现同一漏洞的交叉验证，形成手动审计与模糊测试互补的方法论反馈；文末反思应主动向团队预警危险 API 模式而非仅报告漏洞。2020 文章记录引文 "How to replace step 2. and 3. above with a CPU bug" 的迭代选择叙述（sr-r3-01）。反馈来源为同伴交叉验证与本人自述式反思，非正式代码评审记录。

能力与结果：形成对危险 API 模式的预判能力与全调用点系统性审计方法，并能在不同子系统（JIT 编译器、IPC 机制）间迁移该方法。；2019 TurboFan JIT 缺少运行时检查漏洞从信息泄露升级为任意写原语；2020 RIDL 工作中系统性分析 Mojo IPC port name 泄露与 RIDL/MDS 数据采样的串联路径

置信度：medium；替代解释：竞争性解释：全调用点审计方法在公开 writeup 中被显式记录，可能部分因发表平台对方法论叙述的偏好而被强化呈现；同伴交叉验证（fuzzilli）依赖 Project Zero 组织内可用的工具生态与同行资源，非个人独立完成。组织资源（fuzzilli、Chrome/V8 源码与 tracker 可访问性、跨厂商披露渠道）对审计成果存在支撑，个人能力归因应据此校准。

证据：stephen-ext-01, stephen-ext-02, sr-r3-01

### 跨领域迁移既有浏览器利用能力至硬件侧信道领域（单次跨领域迁移实例，2019→2020，非多时期重复）

起点：2019 年已掌握 Chrome TurboFan JIT 手动审计与浏览器侧原语分析能力（stephen-ext-01，无 Mojo/IPC 字样）；2020 年前作者自述长期回避硬件漏洞领域（sr-r3-01 引文 "i ignored hardware vulnerabilities for the longest time since they are way out of my comfort zone"）。Mojo IPC 分析在 2019 一手证据中不存在，不应列为 2019 年前既有能力。

练习与反馈：2020 年 RIDL 工作选定硬件侧信道作为跨领域迁移目标，并选用该工作内引入的 Mojo IPC port name 泄露（前序他人工作 prior art，引文 "A good example of a bug that can be easily exploited to leak port numbers was crbug.com/779314 by @NedWilliamson"，sr-r3-01）作为切入点，将 2019 年 TurboFan 工作展示的 Chrome 代码审计与利用构建能力迁移到硬件侧信道领域，并在 2020 年工作中引入 Chrome Mojo IPC 128-bit port name 泄露（前序他人工作 prior art，@NedWilliamson crbug.com/779314）以串联 RIDL/MDS 数据采样，构建完整沙箱逃逸 exploit chain。明确标注：单次跨领域迁移实例（2019→2020），非多时期重复。；作者以引文 "How to replace step 2. and 3. above with a CPU bug and what kind of primitives we can gain via privileged IPC connections"（sr-r3-01）叙述以 RIDL/MDS 硬件漏洞替换前序软件 info leak 的迭代选择，此即该机制一手反馈出处；作者自述缓解措施曾令其误判漏洞已被解决（引文 "The focus on mitigations certainly gave me a false sense that the vulnerabilities have been addressed"），并据此提出更新微码、禁用超线程等操作建议。反馈来源为本人公开 writeup 中的迭代选择叙述与缓解误判反思。

能力与结果：在硬件侧信道新领域串联既有浏览器利用能力，并引入本工作内首次采用的 Mojo IPC 前序他人工作（prior art，@NedWilliamson crbug.com/779314）以串联 RIDL/MDS 数据采样，构建跨软件硬件的完整 exploit chain。；2020 RIDL 工作针对 Linux（MFBDS 变体，Xeon Gold 6154）与 Windows（TAA 变体，Core i7-7600U）分别开发两个完整沙箱逃逸 exploit；2020 RIDL 工作与 Apple/Microsoft/Chrome 安全团队协作披露

置信度：medium；替代解释：竞争性解释：跨领域迁移成果高度依赖 Project Zero 组织资源，包括硬件访问（Xeon Gold 6154、Core i7-7600U）、跨厂商披露渠道（Apple/Microsoft/Chrome）、fuzzilli 工具生态（Samuel Groß）、Chrome/V8 源码与 issue tracker 可访问性、Project Zero 发表平台与披露政策；该单次迁移实例的可重复性与个人可迁移性应据此校准，避免将组织资源支撑的成果过度归为个人可迁移能力。Mojo IPC port name 泄露明确为 @NedWilliamson 前序他人工作（prior art），非 Röttger 既有能力或本工作新发现。

证据：stephen-ext-01, stephen-ext-02, sr-r3-01

### 公开发表中记录知识缺口与迭代过程

起点：2015 年首篇 writeup 即在公开文章中显式承认经验缺口与技术难点：自述无 OS X 经验（roettger-deepconv-02 引文 "Since I have no prior experience with OS X, please bear with me if I missed something obvious or use the wrong nomenclature"），并记录 GOT 一节长时间未解决（引文 "The GOT, and this took me way too long to figure out, is actually writable"）。

练习与反馈：2015 ntpd 文章坦承 OS X 经验缺口与 GOT 技术难点；2019 TurboFan 文章记录 GC 移动对象障碍与重分配解决过程，并反思应主动预警危险 API；2020 RIDL 文章记录缓解误判反思与迭代选择叙述（sr-r3-01）。2015 文章末尾以引文 "But that is left as an exercise for the reader :)"（roettger-deepconv-03）将延伸利用留作读者练习，体现将 writeup 视为可被他人继续推进的练习材料的公开写作习惯。；反馈来源为公开 writeup 的自述式记录与读者延伸邀请，非正式评审或导师反馈；2019 文章另含与 Samuel Groß（fuzzilli 作者）交叉验证的同伴反馈。

能力与结果：形成在公开发表中显式记录知识缺口、技术难点与迭代过程，并将完整链路拆解留出可复现延伸部分的写作习惯。；2015 ntpd 文章坦承 OS X 经验缺口与 GOT 技术难点并留延伸练习；2019 TurboFan 文章记录 GC 障碍迭代与危险 API 预警反思；2020 RIDL 文章记录缓解误判反思与硬件替换软件泄露的迭代选择

置信度：medium；替代解释：竞争性解释与幸存者偏差：该机制的可观察性受限于已公开发表的 writeup 样本（Project Zero 2015/2019/2020、v8.dev 2023），未发表、失败或 2015 年之前的工作在可抓取范围不可见，机制跨时期稳定性据此受限；公开 writeup 中记录知识缺口与迭代过程的呈现方式，可能部分由 Project Zero 发表平台对叙事结构的要求塑造，而非纯个人写作习惯。组织资源（发表平台、披露政策、同伴交叉验证）对公开记录的呈现存在支撑。

证据：roettger-deepconv-01, roettger-deepconv-02, roettger-deepconv-03, stephen-ext-02, sr-r3-01

## 可迁移与不可迁移

- 可迁移：以先验背景加复杂度可控为标准的领域进入与目标选择判据，可迁移至任意新漏洞领域；此判据的迁移以剥离组织资源（硬件访问、跨团队协作披露渠道、Chrome/V8 源码与 tracker 可访问性）为前提。
- 可迁移：对危险 API 模式预判后系统性审计所有调用点的方法，可迁移至不同子系统（JIT 编译器、IPC 机制）；该方法的迁移以剥离 fuzzilli 等同伴工具生态与组织内交叉验证资源为前提。
- 可迁移：在公开发表中显式记录知识缺口、技术难点与迭代过程，并将完整链路拆解留出可复现延伸部分的写作习惯，可迁移至任意技术 writeup 场景；此习惯的迁移以剥离 Project Zero 发表平台与披露政策对叙事结构的约束为前提。
- 可迁移：在新领域沿用既有领域进入判据选取切入点，并复用既有工具链而非重新构建全部工具链；此迁移以剥离组织资源对新领域硬件、源码与披露渠道的可访问性为前提。
- 不可直接迁移：Project Zero 发表平台与披露政策：三篇可核证文章均以 guest post 形式发表，发表渠道与披露节奏由平台决定，非个人可迁移条件。
- 不可直接迁移：硬件访问资源：2020 RIDL 工作依赖 Xeon Gold 6154 与 Core i7-7600U 等特定硬件，属组织资源，非个人可迁移条件。
- 不可直接迁移：跨厂商披露渠道：与 Apple/Microsoft/Chrome 安全团队协作披露的渠道属组织资源，非个人可迁移条件。
- 不可直接迁移：同伴与工具生态：与 Samuel Groß（fuzzilli 作者）的交叉验证及 fuzzilli 模糊测试工具生态属组织内可用的同伴与工具资源，非个人可迁移条件。
- 不可直接迁移：Chrome/V8 源码与 issue tracker 可访问性：浏览器与运行时漏洞挖掘依赖的源码与跟踪器访问属组织资源，非个人可迁移条件。
- 不可直接迁移：客座作者身份而非在职成员：可核证文章均为 guest post，在职身份未由一手来源证实，发表机会本身非个人可迁移条件。

## 复核问题

- mechanisms[0]（以先验背景加复杂度可控为标准的领域进入与目标选择）将 validation_tests 标为 repeated 并称该判据在 2015 ntpd、2019 TurboFan、2020 RIDL 三处重复出现，但与一手证据冲突：2019 TurboFan 的选取依据是危险 API 模式预判（stephen-ext-01 引文 When I noticed this function in the past, I was convinced that one of the callers will get it wrong），2020 RIDL 作者自述无硬件背景（sr-r3-01 引文 way out of my comfort zone），二者均非先验背景加复杂度可控。该判据仅在 2015 ntpd 可核证，repeated 不成立。
- mechanisms[0].intermediate_capability 称作者能在新领域沿用此判据选取切入点，但 2020 RIDL 的证据方向与该判据相反（无先验背景、跨入此前回避领域），该句与一手证据冲突，构成承重因果超证据。
- mechanisms[1]（系统性审计危险 API 模式的所有调用点）将 validation_tests 标为 repeated 并称 2020 RIDL 工作沿用该方法分析 Chrome Mojo IPC port name 泄露的利用方式与 RIDL/MDS 数据采样路径。但 2020 一手证据（stephen-ext-02、sr-r3-01）记录的是以 RIDL/MDS 替换前序软件 info leak 构建 exploit chain，非对所有调用点的系统性审计；调用点审计方法仅在 2019 TurboFan 可核证，repeated 不成立。
- mechanisms[1].repeated_practice 称 2020 RIDL 工作中系统性分析 Chrome Mojo IPC port name 泄露的利用方式，未标注该 port name 泄露为 @NedWilliamson 前序他人工作 prior art（sr-r3-01 引文 crbug.com/779314 by @NedWilliamson），与 mechanisms[2] 对 Mojo IPC 的 prior-art 标注不一致，隐含 Röttger 对该泄露进行了系统性审计，构成跨字段因果归因不一致。
- 字段 mechanisms[0].repeated_practice：删除将 2019 TurboFan 与 2020 RIDL 列为先验背景加复杂度可控判据重复实例的表述。原措辞为该判据在 2015 ntpd（先验协议背景加简单复杂度）与 2019 TurboFan JIT 两处出现，2020 RIDL 工作亦显式串联前序能力作为迁移起点。改写方向：明确该判据仅在 2015 ntpd 可核证；2019 TurboFan 的选取依据为危险 API 模式预判（非先验背景加复杂度可控），2020 RIDL 作者自述无硬件先验背景（sr-r3-01 引文 way out of my comfort zone），均不构成该判据的重复实例；跨时期重复性证据仅 1 处，不足以支持 repeated 标注。
- 字段 mechanisms[0].validation_tests：将“repeated”“generative”改为仅“generative”，或删除“repeated”，与上述单例事实一致。
- 字段 mechanisms[0].intermediate_capability：删除并能在新领域沿用此判据选取切入点一句。原措辞为形成以先验背景加复杂度可控为标准的领域进入与目标选择能力，并能在新领域沿用此判据选取切入点。改写方向：改为仅保留形成以先验背景加复杂度可控为标准的领域进入与目标选择能力（在 2015 ntpd 入门中可核证）；删除新领域沿用此判据的表述，因 2019 与 2020 一手证据均未显示沿用，2020 且方向相反。
- 字段 mechanisms[0].observed_outcomes：删除将 2020 RIDL 工作跨入硬件侧信道领域作为该判据观察输出的条目，或改写为标注该工作未以该判据进入硬件领域（作者自述无硬件先验背景，sr-r3-01），不应作为先验背景加复杂度可控判据的输出。
- 字段 mechanisms[1].repeated_practice：删除 2020 RIDL 工作中沿用系统性审计方法分析 Chrome Mojo IPC port name 泄露的利用方式，并对 RIDL/MDS 数据采样路径进行系统性分析一句。原措辞将该句列为调用点审计方法的重复实践。改写方向：明确调用点审计方法仅在 2019 TurboFan 可核证；2020 RIDL 工作记录的是 exploit chain 构建（以 RIDL/MDS 替换前序软件 info leak），非对所有调用点的系统性审计；如保留 2020 表述须限定为该机制的单次可核证实例并删除沿用一词。
- 字段 mechanisms[1].repeated_practice 中 Chrome Mojo IPC port name 泄露：补充 prior-art 标注。原措辞称 2020 RIDL 工作中沿用系统性审计方法分析 Chrome Mojo IPC port name 泄露的利用方式，未标注该泄露归属。改写方向：在该处补注该 port name 泄露为 @NedWilliamson 前序他人工作 prior art（sr-r3-01 引文 crbug.com/779314 by @NedWilliamson），与 mechanisms[2] 的 prior-art 标注跨字段一致，避免隐含 Röttger 对该泄露进行了系统性审计。
- 字段 mechanisms[1].observed_outcomes：删除 2020 RIDL 工作中系统性分析 Mojo IPC port name 泄露与 RIDL/MDS 数据采样的串联路径一条，或改写为标注该串联为 exploit chain 构建而非调用点审计方法的输出。
- 字段 mechanisms[1].validation_tests：将“repeated”“distinctive”改为仅“distinctive”，或删除“repeated”，与调用点审计方法仅 2019 单例的事实一致。
- 字段 mechanisms[0].feedback 与 mechanisms[2].feedback：将自撰叙述中的英文“info leak”统一为中文“信息泄露”或“软件信息泄露”，与 mechanisms[3].observed_outcomes 的软件泄露用语一致，消除自撰叙述中英文混用。原文短引文如 How to replace step 2. and 3. above with a CPU bug 仍以引文形式保留并注明出处。

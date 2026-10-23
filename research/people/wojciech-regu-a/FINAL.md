# Wojciech Reguła：漏洞研究成长分析

- 擅长领域：macOS/iOS 沙箱与隐私漏洞
- 独立复核：pass · 85/100

## 成长阶段

- **2017-2019 · 博客起点与通用漏洞期：从多元题材到首次会议演讲**：博客 wojciechregula.blog 自 2017 年起作为公开研究输出的稳定渠道（页脚标注 © 2017-2026，wr-tl-01、wrd-001）；可核验的最早文章为 2018-03-19 的 FreePlane XXE（wr-tl-02、wr-pubworks-01），题材分散于通用应用层漏洞（XXE 参数实体链外带、路由器认证 RCE、Cordova keychain 明文日志泄漏），尚未聚焦 macOS 内核机制。2018-03-29 的 Cordova keychain leak（CVE-2018-1000123）首次将日常移动应用审计工作场景与公开 writeup 关联（wrd-003 一手正文："during my work, I was auditing a Cordova App"），属工作场景直接审计发现而非跨产品类比迁移。2018-07 作者首次以 attendee 和 speaker 双重身份出席 OWASP AppSec EU，SecuRing 当年有 2 场演讲，作者讲《Testing iOS apps without Jailbreak in 2018》，与同事 Damian Rusinek 分别演讲（r2-wr-appsec-eu-2018 一手正文核验，替换并纠正原 wrd-004 "同台" 事实错误）。同年另发表 macOS Quick Look 缓存泄露加密容器路径研究，被 9to5Mac 以 "security researcher" 与发现者署名引用，并以 VeraCrypt/macOS 加密盘双容器 PoC 方法论被媒体复述（wr-ext-01）。该阶段能力由分散的通用漏洞挖掘向 macOS 系统级隐私泄漏题材过渡，并建立公开写作与会议演讲两条输出渠道。（置信度：medium）
  - 证据：wr-tl-01, wr-tl-02, wr-tl-03, wrd-001, wrd-002, wrd-003, wr-pubworks-01, wr-ext-01, r2-wr-appsec-eu-2018
- **2019-2021 · Apple 平台主题收敛与 TCC 主轴确立：从单点 writeup 到系列化与 CVE 产出**：研究主题由 2018 年的多元题材（路由器/IoT RCE、XXE、keychain 单点）收敛至 macOS TCC 绕过主轴。2019-12-18 发表《Abusing Electron apps to bypass macOS' security controls》（wrd-005，归档列表证实标题与日期，正文未单独抓取），被推断为系统性转向 TCC 绕过主轴的早期标志。2020-03-28 起连载《Learn XPC exploitation》三部曲（Broken cryptography；Say no to the PID!；Code injections），建立 class-dump-swift 与 Hopper 的稳定逆向工具链，由零散 writeup 转为体系化技术沉淀（wrd-006、wr-tl-04、wr-pubworks-02；wrd-006/008/009 正文未单独抓取，方法论推断部分未经正文直接核验）。TCC 主轴连续产出限定为：CVE-2020-29621（coreaudiod 经 HAL 音频插件实现 TCC 全盘访问，wr-tl-05 深度核验，完整披露周期报告→确认→修复→赏金裁定均记录在 writeup 内）以及 wrd-008 归档中标题明示 TCC 的 CVE（CVE-2020-27937 修改 NFSHomeDirectory 绕过 TCC、CVE-2020-10008 特权 helper 冒充 TCC 权限）；该归档 CVE 分类为标题级，未经逐条正文深度核验，须限定。CVE-2021-3162（Docker for macOS 本地提权）据 wrd-007 一手正文确认源于 Info.plist 缺少 anchor apple generic 库验证要求，属本地提权而非 TCC 隐私绕过，单独表述为该阶段方法学多元化的旁证（历史资料缺陷模式触发本地提权），不计入 TCC 主轴连续产出。CVE-2021-30655（sysdiagnose 本地提权）、CVE-2021-30658（M1 GateKeeper 绕过，wr-tl-06 一手核验完整披露周期）同样排除出 TCC 主轴。该阶段另引入以历史纸质书（《Professional Cocoa Application Security》第 10 章缺陷 Info.plist 例子）缺陷模式作为攻击面模板的方法，形成 阅读→类比→验证 的发现路径（wrd-007）；但该方法学仅由单一发现（wrd-007）支撑，尚未观察到第二次同类横向映射，不作为已确立方法学重复表述。同期将 TCC 绕过研究整合为 Black Hat 演讲《20+ ways to bypass macOS your privacy mechanisms》（wr-tl-07，官方 briefing 页面 403 未抓取，年份为 reported 级）。（置信度：medium）
  - 证据：wrd-005, wrd-006, wrd-007, wrd-008, wrd-003, wr-tl-04, wr-tl-05, wr-tl-06, wr-tl-07, wr-pubworks-02
- **2022-2024 · TCC 深耕、沙箱逃逸与红队链路：从单漏洞绕过到攻防全链路与会议循环**：研究沿 TCC/沙箱/隐私攻击面持续迭代同一类原语（特权 helper、home 目录、URL scheme、环境变量、Electron 注入），范围从单漏洞绕过扩展到 macOS 红队全链路。2020 年作者即发现沙盒化 app 可启动不继承沙箱 profile 的进程并支持自定义环境变量，报告 Apple 后被告知属 expected behavior；2022 年在 Jonathan Bar Or 的 CVE-2022-26706 与 Ron Waisberg OBTS v4 演讲《Environmental Disaster: A LaunchServices Tale》公开同类行为后，重新技术定位并以 Word 宏 + Mythic JXA 武器化写出自己的变体 CVE-2022-26696（wr-pubworks-03、wr-comm-05 一手正文核验）。2022-03-18 发表 macOS Red Teaming: Initial access via AppleScript URL（wrd-009），构建初始访问→凭据/数据获取的完整红队叙事。2023-03-04 Bypass TCC via iCloud 先在 TyphoonCon（首尔）演讲披露后博客公开（wr-comm-06，verified_in_run=false，lead_only）。2024-01-23 发表 ELECTRONizing macOS privacy，注明该研究在 DEF CON 31 与 Objective by the Sea 演讲（wrd-011、wr-comm-02，wr-comm-02 verified_in_run=false）。2024-10-20 的 TCC bypasses via launch services（CVE-2022-26767，wr-pubworks-04 一手正文）滥用 LSSetDefaultRoleHandlerForContentType 注册任意 app 为默认处理器，经 com.apple.coreservices.quarantine-resolver XPC 打开受保护文件，该技术在 Black Hat Europe 2022《Knockout Win Against TCC - 20+ NEW Ways to Bypass Your MacOS Privacy Mechanisms》披露。该阶段形成研究→博客→会议演讲→下一轮选题的稳定循环，会议录用与演讲作为公开同行评审式反馈回路（wr-comm-02/06 部分条目 verified_in_run=false，会议级别演讲事实与具体日期的独立一手核验为资料缺口）。（置信度：medium）
  - 证据：wr-pubworks-03, wr-pubworks-04, wr-comm-01, wr-comm-02, wr-comm-05, wr-comm-06, wr-tl-10, wrd-009, wrd-011
- **2024-2026 · 未公开机制逆向与攻防双侧工具建设：从绕过已知机制到逆向平台级保护**：研究方法从发现并绕过已知机制演化到逆向未公开隐私保护机制。2026-07-16 发表《Crossing the Golden Gate》，分析 macOS 27 对非沙箱化 app 的 ~/Library/Application Support/ 目录施加 com.apple.macl/xattr 保护，通过 strings /usr/libexec/sandboxd 提取硬编码 allowlist（bundle ID + Team ID）与 XProtect 实时更新规则 AppProtectionRules.plist，识别新 TCC 服务 kTCCServiceSystemPolicyAppDataDetailed（wr-pubworks-05 一手正文）；方法由单一应用逆向扩展到系统级 strings/grep/xattr/规则文件分析，目标由单 CVE 转向平台级行为分析，并保持致谢同行（@ciphwall、Thijs @txhaflaire）的协作习惯。攻防双侧工具建设延续：开源 iOS Security Suite（github.com/securing/IOSSecuritySuite，纯 Swift，对齐 OWASP MASVS v8，约 2.7k stars、347 forks、266 commits，README 列第三方贡献者如 TannerJin 贡献 MSHook/RuntimeHook/SymbolHook/Watchpoint 检测模块、NikoXu 贡献文件完整性模块；README 明示 every jailbreak detector may be bypassed）与 SimpleXPCApp（约 108 stars，archived）、NoMADCredentialsStealer（约 43 stars，描述链接 red teaming 博文）由 r3ggi/securing 维护（r2-wr-github-pinned-2026，date 修正为抓取日期 2026-09-27，替换 wr-pubworks-06；wr-tl-09、wr-ext-02、wr-comm-04 同源核验）。配套商业 iOS 安全课程与 iOS Application Security Engineer 认证（wrd-010）。开源工具形成外部贡献者以 PR、代码评审、缺陷指出与新检测模块回流项目的社区反馈回路（wr-comm-04）。（置信度：medium）
  - 证据：wr-pubworks-05, wrd-010, r2-wr-github-pinned-2026, wr-tl-09, wr-ext-02, wr-comm-04

## 主要成长机制

### M1 跨情境类比迁移：以历史资料缺陷模式作为攻击面模板

起点：2021-01-21 阅读十一年前出版的《Professional Cocoa Application Security》一书时，第 10 章给出一个缺少 anchor apple generic 要求的缺陷 Info.plist 例子；作者自述此前曾 deeply researched XPC 与自建 secure XPC service 示例，具备 XPC/库验证背景知识（wrd-007 一手正文，short_quote: "the main concepts didn't change so much"）。

练习与反馈：把历史资料中的缺陷模式作为可复用原语直接映射到当代产品，形成 阅读→类比→验证 的发现路径。注：该方法学仅由 wrd-007 单一实例支撑，仅一次实例，repeated 维度缺失，尚未观察到第二次同类横向映射。；wrd-007 一手正文未明确记录外部反馈来源；反馈主要为发现本身的成功验证（Docker for macOS 本地提权 CVE-2021-3162）。

能力与结果：形成以历史资料缺陷模式作为攻击面模板的发现路径，把书中缺陷模式映射到当代产品的 Info.plist 库验证要求缺失问题，产出 Docker for macOS 本地提权（CVE-2021-3162）。明确该 CVE 漏洞类型为本地提权而非 TCC 隐私绕过。；Docker for macOS 本地提权漏洞（CVE-2021-3162，wrd-007 一手正文核验，源于 Info.plist 缺少 anchor apple generic 库验证要求）

置信度：low；替代解释：该方法学仅由 wrd-007 单一实例支撑，单次成功难以证明为稳定可复用的成长机制；未取得第二例历史资料→当代产品映射前，不应作为独立可迁移成长机制单列，更可能为偶然发现或与 M4 主题收敛深耕机制下的方法学多元化旁证重叠。Cordova keychain leak（wrd-003）为工作场景直接审计发现而非类比迁移；macOS Sandbox Escape CVE-2022-26696（wr-pubworks-03/wr-comm-05）性质为被拒→同行验证→重新公开的反馈回路，归属 M2 而非 M1，已从本机制移除以避免同一发现支撑两个机制的 repeated 维度。

证据：wrd-007

### M2 厂商反馈回路：被拒→同行验证→重新技术定位公开

起点：2020 年作者发现沙盒化 macOS app 可启动不继承沙箱 profile 的进程并支持自定义环境变量，报告 Apple 后被告知属 expected behavior（wr-pubworks-03、wr-comm-05 一手正文，short_quote: "I reported it to Apple but I was told that it's expected behavior"）。

练习与反馈：把曾被厂商判定为非漏洞的行为持续观察，在同行以 CVE 与会议演讲公开同类行为后，重新技术定位为可武器化逃逸并公开发表自己的变体。；同行 Jonathan Bar Or 的 CVE-2022-26706 与 Ron Waisberg 在 Objective by the Sea v4 的演讲《Environmental Disaster: A LaunchServices Tale》作为独立第三方验证，印证其先前判断并推动重新评估与公开发表（wr-comm-05 一手正文）。

能力与结果：形成被拒—同行验证—再公开的闭环能力：不因厂商初次驳回放弃，而以同行独立工作为重新定位的外部锚点，把被驳回行为重新技术定位为可武器化逃逸。；macOS Sandbox Escape via Terminal（CVE-2022-26696），以 Word 宏 + Mythic JXA 武器化（wr-pubworks-03、wr-comm-05 一手正文核验）

置信度：medium；替代解释：CVE-2022-26696 的重新公开可能主要受同行公开披露的时间窗口驱动（CVE-2022-26706 与 OBTS v4 演讲先行公开），而非作者主动的系统性反馈回路机制；目前仅一例完整闭环，repeated 维度由被拒→重新公开这一单链条构成，跨案例重复尚未取得第二例。该发现已明确归属 M2 而非 M1（跨情境类比迁移），二者边界在该案例上已界定。

证据：wr-pubworks-03, wr-comm-05

### M3 攻防双侧工具建设：把研究沉淀为开源库与教学输出

起点：日常 iOS/macOS 审计与 XPC 研究实践（wrd-003 Cordova 审计、wrd-006 XPC 系列、wrd-007 自建 secure XPC service 示例）积累的检测与逆向需求；SecuRing Principal Security Consultant 职务提供移动安全审计工作场景（wr-deep-about-freetime、wr-comm-03）。

练习与反馈：把攻击侧研究发现沉淀为防御侧可复用开源库（IOSSecuritySuite 越狱/调试器/hook 检测、SimpleXPCApp 安全 XPC helper 示例），并以商业 iOS 安全课程与 iOS Application Security Engineer 认证体系化输出方法论；开源库 README 明示克制、非绝对化的工程立场（every jailbreak detector may be bypassed）。；外部贡献者以 PR、代码评审、缺陷指出与新检测模块方式回流项目：kubajakowski 指出 canOpenURL 方法缺陷、TannerJin 贡献 MSHook/RuntimeHook/SymbolHook/Watchpoint 检测模块、NikoXu 贡献文件完整性模块、mkj-is 提交性能改进 PR、Coeur 修复 bug；README 明示 Pull requests are more than welcome（wr-comm-04 一手 README 核验）。机构付费采用（100 员工以下免费，100-1000 员工年费约 3k EUR，1000+ 约 10k EUR）与第三方贡献构成外部对工具价值的实质性评价（wr-ext-02）。

能力与结果：形成工具—写作—披露的协同输出结构：攻击侧 writeup 与防御侧开源库互为输入，配套教学形成知识变现双轨；GitHub Pull Shark 徽章表明亦向他人项目提交并被合并 PR，存在双向社区参与（wr-comm-07）。；iOS Security Suite（github.com/securing/IOSSecuritySuite，纯 Swift，对齐 OWASP MASVS v8，约 2.7k stars、266 commits，wr-tl-09、wr-ext-02、wr-comm-04、r2-wr-github-pinned-2026）；SimpleXPCApp（约 108 stars，archived，r2-wr-github-pinned-2026）；NoMADCredentialsStealer（约 43 stars，描述链接 red teaming 博文，r2-wr-github-pinned-2026）；商业 iOS 安全课程与 iOS Application Security Engineer 认证（wrd-010）

置信度：medium；替代解释：工具 star/fork 数字与机构付费采用反映采用规模与商业价值，不直接等价于研究者个人能力成长；IOSSecuritySuite 项目首版日期与发布时间表未在 README 提供（wr-tl-09 gap），工具建设与攻击侧研究的因果方向（研究驱动工具 vs 工具反哺研究）未由一手陈述明确。

证据：wrd-010, wr-tl-09, wr-ext-02, wr-comm-04, wr-comm-07, r2-wr-github-pinned-2026

### M4 主题收敛深耕：沿 TCC/沙箱/隐私攻击面多年迭代同一类原语

起点：2018-2019 年由多元主题（路由器/IoT RCE、XXE、keychain 单点，wr-tl-02、wrd-002、wr-pubworks-01）向 macOS 系统级隐私机制过渡（2018-06 Quick Look 缓存泄露，wr-tl-03）；2019-12 Abusing Electron apps 标志系统性转向（wrd-005）。

练习与反馈：在同一 TCC/沙箱/隐私攻击面上多年复用与扩展同一类原语（特权 helper、home 目录、URL scheme、环境变量、Electron 注入、Launch Services 默认处理器注册、HAL 音频插件），持续把单点发现深化为子系统专题。；Apple 厂商反馈（expected behavior 驳回、Apple Security Bounty 裁定符合/不符合、修复版本确认）与会议录用（Black Hat、OBTS、DEF CON、TyphoonCon）作为选题与深化方向的反馈；wr-tl-05 完整记录报告→确认→修复→赏金裁定周期，wr-tl-06 记录赏金被裁定不符合的边界反馈。

能力与结果：形成以 TCC 绕过为核心、向沙箱逃逸与红队链路扩展的子系统专题能力，能把分散绕过整合为会议级议题（Black Hat 20+ ways to bypass macOS privacy mechanisms，wr-tl-07）与红队全链路叙事（wrd-009）。；CVE-2020-29621（coreaudiod 经 HAL 音频插件实现 TCC 全盘访问，wr-tl-05 深度核验，完整披露周期）；CVE-2020-27937（修改 NFSHomeDirectory 绕过 TCC）、CVE-2020-10008（特权 helper 冒充 TCC 权限），wrd-008 归档标题级，未经逐条正文深度核验；CVE-2022-26696（macOS Sandbox Escape via Terminal，wr-pubworks-03）；CVE-2022-26767（TCC bypasses via launch services，wr-pubworks-04）；macOS Red Teaming 系列：Initial access via AppleScript URL、NoMAD 凭据提取、Apple Dev-ID 签名 Java 环境（wrd-009）；Golden Gate 未公开机制逆向（wr-pubworks-05）

置信度：medium；替代解释：主题收敛可能部分受 Apple 平台攻击面本身在 2019-2024 年持续扩展（TCC 强化、Apple Silicon 迁移、沙箱细化）的外部机会窗口驱动，而非纯由研究者主动选择；wrd-008 归档中 CVE 分类为标题级，TCC 主轴连续性的逐条正文核验未完成，CVE-2021-3162（本地提权）、CVE-2021-30655（sysdiagnose 本地提权）、CVE-2021-30658（M1 GateKeeper）已明确排除出 TCC 主轴，不应被引用为 TCC 主轴连续产出证据。

证据：wr-tl-03, wr-tl-05, wr-tl-07, wr-tl-10, wrd-005, wrd-008, wrd-009, wr-pubworks-03, wr-pubworks-04, wr-pubworks-05

### M5 会议演讲循环：研究→博客→会议演讲→下一轮选题

起点：2018-07 首次以 attendee 和 speaker 双重身份出席 OWASP AppSec EU，SecuRing 当年有 2 场演讲，作者讲《Testing iOS apps without Jailbreak in 2018》，与同事 Damian Rusinek 分别演讲（r2-wr-appsec-eu-2018 一手正文核验，替换并纠正原 wrd-004 "同台" 事实错误）。

练习与反馈：把博客研究升级为会议演讲并形成跨会议循环（Black Hat Las Vegas、Objective by the Sea Hawaii、DEF CON 31、AppSec Global Tel Aviv、AppSec EU London、CONFidence Cracow、BSides Warsaw、TyphoonCon Seoul），演讲后由听众提问驱动下一轮系统化写作（Learn XPC exploitation 系列即由 OBTS v3 演讲后大量提问整理而成，wr-pubworks-02）。；会议录用与演讲作为公开同行评审式反馈；听众提问成为系列写作的直接动因（wr-pubworks-02：summing it up in a blog post series is a good idea）；跨会议、跨地点的反复公开演讲显示重复练习+公开发表的持续循环（wr-deep-about-conferences、wr-tl-08）。

能力与结果：建立稳定的公开发表与同行反馈机制，能把分散研究整合为单场会议演讲（20+ ways to bypass macOS privacy mechanisms、ELECTRONizing macOS privacy、Knockout Win Against TCC）并形成会议—博客交替节奏。；ELECTRONizing macOS privacy：presented at DEF CON 31 and Objective By the Sea（wrd-011、wr-comm-02，wr-comm-02 verified_in_run=false）；Bypass TCC via iCloud：first disclosed at TyphoonCon in Seoul（wr-comm-06，verified_in_run=false，lead_only）；Learn XPC exploitation 三部曲由 OBTS v3 演讲提问驱动（wr-pubworks-02）；About-me 自述演讲足迹覆盖美欧多场会议（wr-deep-about-conferences、wr-tl-08）

置信度：medium；替代解释：会议邀请通常仅证明演讲事实，按本研究口径不能单独证明成长机制；OBTS 官方首页（objectivebythesea.org）抓取返回空体、Black Hat briefing 页 403，各届演讲标题与日期未能从主持方一手页面独立核验，部分演讲事实仅由本人博客与 About-me 二手转述（wr-ext-04 gap）。wr-comm-02、wr-comm-06 的 verified_in_run=false，会议级别演讲事实与具体日期的独立一手核验为资料缺口。

证据：r2-wr-appsec-eu-2018, wr-pubworks-02, wr-deep-about-conferences, wr-tl-07, wr-tl-08, wrd-011, wr-comm-02, wr-comm-06

## 可迁移与不可迁移

- 可迁移：把日常审计/工作场景中遇到的问题固化为公开 writeup 与 CVE，以工作场景作为研究选题来源（wrd-003 Cordova keychain leak 直接审计发现；wrd-006 XPC 系列由审计实践沉淀）。
- 可迁移：把单点技术拆解为多部分系列化教学 writeup，由演讲后听众提问驱动系统化写作（Learn XPC exploitation 三部曲由 OBTS v3 演讲提问整理而成，wr-pubworks-02）。
- 可迁移：建立报告→确认→修复→赏金裁定/驳回的完整负责任披露时间线记录，并据实记录赏金被裁定不符合的边界反馈（wr-tl-05 CVE-2020-29621 完整周期、wr-tl-06 CVE-2021-30658 赏金不符合裁定）。
- 可迁移：把攻击侧研究发现沉淀为防御侧可复用开源库（IOSSecuritySuite 检测模块、SimpleXPCApp 安全 XPC helper 示例），形成攻防双侧闭环与社区 PR/贡献回流（wrd-010、wr-comm-04、r2-wr-github-pinned-2026）。
- 可迁移：以系统级工具（strings/grep/xattr）与规则文件分析替代单一应用逆向，把目标由单 CVE 转向平台级行为分析（wr-pubworks-05 Golden Gate 对 sandboxd 硬编码 allowlist 与 XProtect AppProtectionRules.plist 的逆向）。
- 可迁移：把曾被厂商驳回的行为持续观察，在同行以 CVE 与会议演讲公开同类行为后重新技术定位为可武器化逃逸并公开发表（CVE-2022-26696，wr-pubworks-03、wr-comm-05）。
- 可迁移：建立稳定逆向工具链（class-dump-swift、Hopper 用于应用/XPC 逆向；strings/grep/xattr 用于系统级机制逆向）并以系列化写作沉淀工具使用方法（wr-pubworks-02、wr-pubworks-05）。
- 不可直接迁移：以历史纸质书（《Professional Cocoa Application Security》）缺陷模式作为攻击面模板做 阅读→类比→验证 的横向映射（wrd-007）：仅由单一实例支撑，可重复性未获第二次同类发现证实，不应作为独立可迁移成长机制单列。
- 不可直接迁移：SecuRing Principal Security Consultant / Head of Mobile Security 职务与移动安全审计工作场景（wr-comm-03、wrd-003）：属个人特有职业条件，构成部分研究选题来源，但与业余研究产出的边界与时间分配未由一手陈述明确，不可直接迁移。
- 不可直接迁移：Apple 平台在 2019-2024 年间攻击面持续扩展（TCC 强化、Apple Silicon 迁移 M1 早期、沙箱细化、Launch Services 机制）的外部机会窗口：属所处时期外部条件，非个人可迁移做法（wr-tl-06 M1 GateKeeper、wr-pubworks-04 Launch Services）。
- 不可直接迁移：Apple Security Bounty 裁定符合（CVE-2020-29621）与厂商 expected behavior 驳回（CVE-2022-26696）的具体厂商互动结果：属厂商单方裁定，非研究者可控可迁移条件。
- 不可直接迁移：同行（Jonathan Bar Or CVE-2022-26706、Ron Waisberg OBTS v4 演讲、Scott Knight XPC gist、@ciphwall、Thijs @txhaflaire）的独立公开与致谢网络：属外部同行网络条件，构成重新公开与协作的外部锚点，非个人可单独复现。

## 复核问题

- 未发现关键事实、身份或来源错误。person_json 记录的身份（x.com/_r3ggi、wojciechregula.blog、macOS/iOS 沙箱与隐私漏洞）与 evidence 多维 identity_check（About-me、GitHub r3ggi、securing 组织、LinkedIn wojciech-regula）交叉一致；synthesis 对两轮 targeted_research 已作废证据（wrd-004、wr-pubworks-06）的替换已全文落实，未检索到残留引用；CVE-2021-3162 漏洞类型（本地提权，非 TCC）与 TCC 主轴的边界已正确区分并排除出 TCC 主轴连续产出，与一手证据 wrd-007 一致。
- mechanisms[2]（M3 攻防双侧工具建设）：将 starting_conditions 引用的 wrd-003、wrd-006、wrd-007、wr-deep-about-freetime、wr-comm-03 中实际承重的证据补充进 M3.evidence_ids，或在正文引用处明确说明这些为相邻阶段证据仅作背景引用、不计入本机制来源支撑，使 evidence_ids 数组与正文引用保持一致。原措辞无需改动，仅补齐数组。
- mechanisms[3]（M4 主题收敛深耕）：将 starting_conditions 引用的 wr-tl-02、wrd-002、wr-pubworks-01 与 feedback 引用的 wr-tl-06 中实际承重者补充进 M4.evidence_ids，或在正文引用处明确标注其为背景引用，使 evidence_ids 数组与正文引用保持一致。原措辞无需改动，仅补齐数组。
- stages[2]（S3）capability_change 与 mechanisms[4]（M5）：对 wr-comm-02（ELECTRONizing macOS privacy，presented at DEF CON 31 and Objective By the Sea）该声明，建议在 S3 或 M5 正文明确补注该演讲事实同时由 wrd-011（verified_in_run=true，归档列表条目注明同一事实）支撑，使来源支撑强度表述与实际证据一致。原措辞 "wr-comm-02 verified_in_run=false" 可保留，补一句 "该演讲事实另由 wrd-011 二次支撑"。
- stages[2].stage 标题 "TCC 深耕、沙箱逃逸与红队链路" 与 mechanisms[3].name "M4 主题收敛深耕：沿 TCC/沙箱/隐私攻击面多年迭代同一类原语" 中 "深耕" 一词带有轻微正面评价色彩，建议改写为中性表述，例如 "持续专注" 或 "持续迭代"。该词非黑话、俚语、比喻、拟人或宣传性表达，不构成语言规范违规，故不阻断 pass；但按专业书面语克制要求，改写后更贴合本研究的语气规范。

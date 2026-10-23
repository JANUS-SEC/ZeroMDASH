# Thijs Alkemade：漏洞研究成长分析

- 擅长领域：macOS 与消息应用漏洞
- 独立复核：pass · 91/100

## 成长阶段

- **范围声明：本轨迹仅覆盖 2011–2016 年 XMPP 时期前置阶段。person_json 声明的主方向『macOS 与消息应用漏洞』（2016 年后 macOS/iMessage）一手 writeup 未取得（sector7.computest.nl TLS 校验失败、DEFION 博客无本人署名、web.archive.org 抓取被拒），故 stages 不构成完整成长弧，2016 年后阶段为资料缺口。 · 范围声明（前置）**：下述阶段均为 2016 年前可核验的 XMPP 时期前置，无法据一手材料延伸至主方向时期。（置信度：high）
  - 证据：thijs-alkemade-ext-001, thijs-alkemade-ext-002, TA-TL-01, TA-TL-02
- **2011–2012 · 消息客户端插件工程基线**：在 Adium（OS X 多协议即时消息客户端）平台以 Objective-C/C 开发第三方插件（基于 Colloquy ChatCore 的 IRC 插件 IRC--、Steam 协议插件 Steamium），建立对消息客户端协议处理与扩展机制的工程经验，构成后续消息系统安全研究的领域知识基础。（置信度：high）
  - 证据：ta-dec-04, ta-works-07, ta-community-01-github-messaging-contrib
- **2014–2015（并发转折：约 2013–2015 由 Adium/xmpp.net 工程角色转入 Computest Sector 7 安全研究，推断区间，与本期写作期重叠，非晚于本期的后续阶段） · 由客户端工程转向协议层安全写作**：研究姿态由实现转为攻击/审计：研究对象仍为消息系统，但视角转向协议层缺陷。2014-06 针对苹果 SecureTransport（CVE-2014-1361）的 TLS 库实现缺陷写作；2014-08 将 CRIME/BREACH 类攻击迁移到 XMPP 场景；2015-04 指出 libcurl/glibc 在 locale 设置下的输入编码校验缺失。研究选题跨协议，但关注点始终为输入边界与协议层校验缺陷模式。约 2013–2015 年间由 Adium 首席开发者/xmpp.net 创建者转入 Computest Sector 7 安全研究，转折本身为推断（触发事件、具体年份、雇主更替流程无一手记载），其性质是以既有领域知识为基底的方向迁移而非断点跳转。（置信度：medium）
  - 证据：ta-works-01, ta-works-02, ta-works-04, ta-dec-01, ta-dec-03
- **2015–2016 · XMPP 协议层安全研究的串行产出期**：围绕 XMPP/TLS/密码学实现形成连续公开写作：2015-01《Multi-end to multi-end encryption》分析服务端存档（XEP-0313 MAM）与端到端加密（OTR）的目标冲突并提出 Axolotl/TextSecure 方案；2015-12《Common DH groups》响应 Logjam 攻击编目常见 Diffie-Hellman 参数组以更新 xmpp.net 扫描项目；2016-01《The Wrong Number Attack》发现 Prosody/ejabberd/Openfire 三款 XMPP 服务端 dialback 密钥生成使用非密码学安全 PRNG，并逐实现给出修复版本。从单点 CVE 分析发展为对一个协议族的持续、递进式钻研。（置信度：high）
  - 证据：ta-rr1-multi-end-encryption, ta-works-05, ta-community-02-blog-xmpp-standards, ta-community-03-blog-logjam-weakdh, ta-rr1-wrong-number-attack, ta-dec-03

## 主要成长机制

### 以消息客户端协议实现经验为基底转入同领域安全审计

起点：2011–2012 年以 Objective-C/C 维护 Adium 消息客户端插件（IRC--、Steamium），并以 GitHub 用户 xnyhps 向 luasec、ghc 贡献或 fork，置 Netherlands；具备消息客户端协议处理与扩展机制的工程经验。

练习与反馈：在已熟悉的消息协议栈（XMPP/Adium）上由实现者视角转向攻击/审计者视角：研究对象不变，研究姿态由『实现协议扩展』转为『审计协议缺陷』。；阶段反馈来源为公开写作与开源贡献的公开可核验痕迹（GitHub 仓库时间序列、Pull Shark x2 徽章、博客署名）；无显式导师或同伴反馈的一手记载（conversations 维度 items 为空）。

能力与结果：形成对消息系统协议处理代码的结构性理解，使其能在消息应用与协议栈中定位解析器/认证机制缺陷而非停留于应用层使用。；2015–2016 围绕 XMPP 协议层（联邦认证 dialback、服务端存档与端到端加密协调、DH 参数编目）形成串行公开写作。；由 Adium/xmpp.net 工程角色转入 Computest Sector 7 安全研究（转折本身为推断，与写作期重叠）。

置信度：medium；替代解释：方向迁移本身缺乏一手记载（约 2013–2015 推断区间，触发事件与雇主更替流程未记载），不排除是组织招聘路径自然引导而非个人能力驱动的可迁移机制；GitHub 工程经验与后续协议安全写作的因果关联为时间先后推断而非直接证据。

证据：ta-dec-04, ta-works-07, ta-community-01-github-messaging-contrib, ta-dec-01, ta-dec-03, ta-rr1-multi-end-encryption, ta-rr1-wrong-number-attack

### 单点发现外推为跨实现横向审计

起点：在 XMPP 协议安全研究方向上已具备单实现 CVE/缺陷分析能力（2014 SecureTransport、2014 CRIME/BREACH→XMPP 迁移、2015 输入编码校验）。

练习与反馈：在《The Wrong Number Attack》中，作者自述由 Prosody 单实现发现外推至其他实现：『After I reported this, I wondered how it would work in servers that support clustering, so I looked over the ejabberd source code.』与『But then I wondered about the other implementations out there, so I checked out Openfire.』，最终一次审计覆盖 Prosody、ejabberd、Openfire、Tigase 四个服务端并逐实现给出修复版本。；反馈来源为各服务端的修复版本与是否遵循 XEP-0185 的对照结果（Prosody 0.9.9、ejabberd 16.01、Openfire 4.0.0 需修复；Tigase 使用 CSPRNG 并遵循 XEP-0185 无需修复）。

能力与结果：形成『以一个实现的缺陷模式为假设，逐一审查同类实现是否复现该模式』的横向审计方法，而非孤立完成单点发现。；《The Wrong Number Attack》一次审计覆盖四个 XMPP 服务端实现并给出逐实现修复版本。

置信度：low；替代解释：跨实现横向审计的一手可核验实例仅此一次（一次审计覆盖四个服务端），无第二处确属横向审计的实例被一手抓取，故为单一可核验实例而非稳定可重复机制；ta-rr1-multi-end-encryption 为协议设计层张力分析（服务端存档 vs 端到端加密目标冲突），非跨实现横向审计方法的重复。

证据：ta-rr1-wrong-number-attack

### 以自建扫描/发布工具为仪器的事件响应式写作

起点：维护 xmpp.net 扫描项目与个人博客发布渠道，并有 Haskell 工具栈偏好（GitHub fork luasec/ghc 镜像）。

练习与反馈：在公开安全事件（Logjam）发生同年即产出呼应性实证写作（《Common DH groups》编目常见 DH 参数组），并以更新 xmpp.net 扫描项目为目的；同时自维护发布工具链（将博客由 Octopress/Ruby 迁移到 Hakyll/Haskell）。；反馈来源为外部公开安全事件（Logjam/weakdh.org）的触发；发布工具链反馈为维护成本与语言偏好（作者自述 Ruby/gem 工具链反复破坏可维护性、不愿为此学习 Ruby 生态）。

能力与结果：形成『外部新攻击出现→更新自有扫描能力→产出数据写作』的研究模式，以及以自维护、可审计工具链维护发布渠道的习惯。；《Common DH groups》响应 Logjam 攻击并编目 DH 参数以更新 xmpp.net 扫描项目（事件响应式安全写作的一手可核验实例）。

置信度：low；替代解释：事件响应式安全写作的一手可核验实例仅 Common DH groups 一例，为单一可核验实例而非稳定可重复机制；ta-works-08/ta-dec-02（Hakyll 迁移）为发布工具链变更，仅用于支撑『自维护发布工具链』子主张，不计入事件响应式安全写作 observed_outcomes，与该机制自身定位单一可核验实例不矛盾。

证据：ta-works-05, ta-community-03-blog-logjam-weakdh

## 可迁移与不可迁移

- 可迁移：将一个实现中确认的缺陷模式作为假设，逐一审查同类实现是否复现该模式，并为每个实现给出修复状态对照（如《The Wrong Number Attack》覆盖 Prosody/ejabberd/Openfire/Tigase 四服务端）。
- 可迁移：在外部公开安全事件（如 Logjam）发生同年即产出呼应性实证写作，将事件响应转化为自有工具/扫描项目的数据更新。
- 可迁移：以已熟悉的协议栈工程经验为基底，在同领域内由实现者视角转向审计者视角，而非跨入完全陌生的系统。
- 不可直接迁移：2011–2012 年 Adium 平台 Objective-C 插件开发经验为消息客户端协议处理的特定前置，非本研究方向外他人可径直复用的通用能力。
- 不可直接迁移：Computest Sector 7（后 DEFION Security）组织职位提供的研究员身份与披露渠道为组织资源，非个人可迁移条件；该组织博客当前已迁移至 defion.security 且未显示本人署名条目，渠道连续性中断。
- 不可直接迁移：xmpp.net 扫描项目的具体贡献角色（作者/维护者/参与者）与时间线未单独抓取确认，仅 2015-12-28 文章提及为更新该项目而编目 DH 参数，工具资产归属与协作关系不明。
- 不可直接迁移：Haskell/GHC 工具栈偏好为个人特有条件，其博客用 Hakyll 自建静态站点生成器而非沿用现成框架，属个人工程习惯不可径直迁移。

## 复核问题


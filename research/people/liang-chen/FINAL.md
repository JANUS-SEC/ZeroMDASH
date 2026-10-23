# Liang Chen：漏洞研究成长分析

- 擅长领域：Android 与浏览器漏洞
- 独立复核：pass · 82/100

## 成长阶段

- **约2013—2014年 · 攻击面选型与单漏洞公开竞赛**：由无公开可核验记录，到确立面向 OS X 沙箱逃逸的攻击面选型方法（可从浏览器沙箱触达、沙箱配置薄弱或缺失、组件早于 OS X Leopard 沙箱引入而长期存在），并以单一漏洞 CVE-2014-1314 在 Pwn2Own 2014 攻取 Safari on OS X Mavericks，形成公开竞赛阶段性成果。2014 年竞赛锚点已获独立权威二手来源确认；2013 年选型陈述仅由 2016 年回溯 writeup 支撑。（置信度：medium）
  - 证据：LC-DEC-01, LC-DEC-02, lc-rr1-pwn2own-2014-independence, liang-chen-deep-03
- **2014—2016年 · 对同一组件的长期集中研究与跨平台 Safari 竞赛**：WindowServer 确立为漏洞发现的长期焦点之一，研究由单次 CVE 转向对同一组件的持续研究；同年（2016）从桌面 Safari/macOS 扩展到移动 Safari/iOS，在 Pwn2Own 2016 桌面与 Mobile Pwn2Own 2016 两场赛事均获 Master of Pwn。阶段定时存在证据限制：2014 年竞赛锚点已获独立权威二手来源确认，但 2013 年选型与长期焦点陈述仅由 2016 年回溯 writeup 支撑，无 2013 或 2015 年独立定时来源，2013—2016 阶段递进为推断而非独立定时。（置信度：medium）
  - 证据：LC-DEC-03, lc_works_pwn2own_2016_desktop, lc_works_pwn2own_2016_mobile, liang-chen-deep-03
- **2016年 · 端到端利用链组装**：由单漏洞公开竞赛扩展到端到端利用链的工程化组装。桌面端以 CVE-2016-1804 经浏览器漏洞远程攻下 OS X El Capitan 并提权至 root；移动端据 POC 2016《Hacking Phones from 2013 to 2016》自述以全新 bug 组成完整利用链，从渲染器推进到沙箱逃逸与内核提权，并在最新移动设备上完成远程利用演示。两实例分属不同平台与链结构，不作为无差别实例并列。（置信度：medium）
  - 证据：LC-DEC-04, liang-chen-deep-01, liang-chen-deep-02

## 主要成长机制

### 攻击面选型驱动下对同一组件的长期集中研究

起点：约 2013 年 Keen Lab 团队决定探索 OS X 沙箱逃逸，并设定攻击面选定标准：可从浏览器沙箱触达、沙箱配置薄弱或缺失、组件早于 OS X Leopard 沙箱引入而长期存在（LC-DEC-01）。

练习与反馈：依上述标准选定 WindowServer 为目标，并在 2013—2016 年间对同一组件持续开展漏洞发现工作，由单次 CVE 推进到对该组件的多漏洞研究（CVE-2014-1314 于 Pwn2Own 2014、CVE-2016-1804 于 2016 年 OS X El Capitan 链）。；公开竞赛结果（Pwn2Own 2014 攻取 Safari on OS X Mavericks、Pwn2Own 2016 Master of Pwn）作为外部验证；2016 年 WindowServer writeup 以回溯方式将选型标准与方法显式陈述，构成对自身方法的一次书面复盘。

能力与结果：将单次漏洞发现确立为对同一组件的长期研究对象，形成由选型到持续研究的方法，而非零散针对单个 CVE。；CVE-2014-1314 于 Pwn2Own 2014 攻取 Safari on OS X Mavericks（LC-DEC-02，reported；2014 竞赛锚点另由 Wikipedia 独立确认 lc-rr1-pwn2own-2014-independence）；WindowServer 确立为漏洞发现的长期焦点之一（LC-DEC-03）；CVE-2016-1804 经浏览器漏洞远程攻下 OS X El Capitan 并提权至 root（LC-DEC-04）

置信度：medium；替代解释：选型标准与长期焦点陈述均为 2016 年回溯性 writeup 的事后叙述（LC-DEC-01、LC-DEC-03），无 2013 或 2015 年独立定时来源；所谓由选型到长期集中的递进可能是对竞赛驱动下机会性成果的事后重构。WindowServer 长期焦点为团队级叙述，个人在该方法中的具体作用难以从队伍结果中明确区分。

证据：LC-DEC-01, LC-DEC-02, LC-DEC-03, LC-DEC-04, lc-rr1-pwn2own-2014-independence

### 同一浏览器栈跨桌面与移动平台迁移

起点：2014 年 Pwn2Own 攻取 Safari on OS X Mavericks（桌面），此前个人据 POC 2016 履历自述在 Mobile Pwn2Own 2013 攻取 iPhone Safari（liang-chen-deep-03）；同一 Safari/WebKit 栈在桌面与移动端均已有公开竞赛记录。

练习与反馈：在 2014、2016 桌面与 2016 移动多场赛事中重复以 Safari/WebKit 为目标，跨 macOS 与 iOS 平台开展利用工作，且均以多人队伍结构参赛。；Pwn2Own 2016 桌面赛事（2016-03）与 Mobile Pwn2Own 2016（2016-10）两场 Master of Pwn 作为外部竞赛反馈，构成同年内两次公开验证。

能力与结果：在同一浏览器栈上将利用工作由桌面迁移到移动平台，形成跨平台的 Safari/WebKit 利用经验。；Pwn2Own 2014 攻取 Safari on OS X Mavericks（lc-rr1-pwn2own-2014-independence，队伍含 Zeguang Zhao/team509）；Pwn2Own 2016 桌面赛攻取 Safari on Mac OS X 并获 Master of Pwn（lc_works_pwn2own_2016_desktop）；Mobile Pwn2Own 2016 攻取 Safari on iPhone 6S（iOS 10）并获 Master of Pwn（lc_works_pwn2own_2016_mobile）

置信度：medium；替代解释：所有跨平台 Safari 成果均出自多人队伍：2014 年队伍含 Zeguang Zhao（team509），2016 年队伍含 Qidan He、Marco Grassi、Yubin Fu、Wayne Liang。队伍结构在两年间并不相同，个人跨平台能力难以从队伍结果中明确区分；Safari 焦点可能反映团队分工而非个人专长。

证据：lc-rr1-pwn2own-2014-independence, lc_works_pwn2own_2016_desktop, lc_works_pwn2own_2016_mobile, liang-chen-deep-03

### 端到端利用链组装能力扩展

起点：已有单漏洞公开竞赛经验（Pwn2Own 2014）；自述研究方法关注操作系统特性导致的、被厂商与研究者普遍忽视的漏洞模式（liang-chen-deep-02）。

练习与反馈：将渲染器漏洞、沙箱逃逸与内核提权组装为端到端利用链，并在桌面与移动两类平台分别实践；自述以由全新 bug 组成的完整利用链完成演示。；POC 2016《Hacking Phones from 2013 to 2016》作为公开演讲对该方法加以陈述；2016 年 WindowServer writeup 记录 CVE-2016-1804 桌面端远程 root 链，构成书面成果。

能力与结果：由单漏洞公开竞赛扩展到端到端利用链的工程化组装，形成多漏洞组合与跨层推进的利用工程能力。；移动端：POC 2016《Hacking Phones from 2013 to 2016》自述以全新 bug 组成完整利用链，从渲染器推进到沙箱逃逸与内核提权，并在最新移动设备上完成远程利用演示（liang-chen-deep-02）；桌面端：CVE-2016-1804 经浏览器漏洞远程攻下 OS X El Capitan 并提权至 root（LC-DEC-04）

置信度：medium；替代解释：POC 2016 演讲由 Liang Chen 与 Qidan He 合讲（liang-chen-deep-02），利用链组装为团队级成果；完整利用链由全新 bug 组成一说为演讲摘要自述，未经独立复核；CVE-2016-1804 链的细节仅见于 2016 年 writeup，其 CVE 正文与 NVD/Apple advisory 未抓取成功，受影响组件与发布日期未独立确认。

证据：liang-chen-deep-01, liang-chen-deep-02, LC-DEC-04

## 可迁移与不可迁移

- 可迁移：基于工程约束的攻击面选型：以可从浏览器沙箱触达、沙箱配置薄弱或缺失、组件早于沙箱引入而长期存在作为选定标准（LC-DEC-01）。
- 可迁移：将单次 CVE 转化为对同一组件的长期集中研究，而非零散针对单个 CVE（LC-DEC-02、LC-DEC-03）。
- 可迁移：在同一浏览器栈上将利用工作跨桌面与移动平台迁移，复用既有的 Safari/WebKit 利用经验（lc_works_pwn2own_2016_desktop、lc_works_pwn2own_2016_mobile）。
- 可迁移：将渲染器漏洞、沙箱逃逸与内核提权组装为端到端利用链，并对利用链作公开演讲与书面复盘（liang-chen-deep-02、LC-DEC-04）。
- 不可直接迁移：多人竞赛队伍结构：跨平台与端到端成果均出自 Keen Lab 多人队伍（2014 年含 Zeguang Zhao/team509；2016 年含 Qidan He、Marco Grassi、Yubin Fu、Wayne Liang），个人产出难以从队伍中明确区分（lc-rr1-pwn2own-2014-independence、lc_works_pwn2own_2016_desktop、lc_works_pwn2own_2016_mobile）。
- 不可直接迁移：Keen Lab / Tencent 机构资源：竞赛报名、目标设备采购与团队协作依赖机构资源，非个人可独立复制（person_json、lc_works_pwn2own_2016_desktop、lc_works_pwn2own_2016_mobile）。
- 不可直接迁移：时期窗口：2013—2016 年处于 OS X 沙箱引入初期、Safari/WebKit 攻击面相对未被充分研究的阶段，该外部条件不可外推至当前（LC-DEC-01、liang-chen-deep-03）。
- 不可直接迁移：公开竞赛与会议作为反馈渠道：Pwn2Own、CanSecWest、POC 等赛事与会议作为外部反馈，依赖赛事存在与参赛资格，非个人可任意获得（liang-chen-deep-03）。

## 复核问题


# Guang Gong：漏洞研究成长分析

- 擅长领域：Android 与浏览器漏洞
- 独立复核：pass · 83/100

## 成长阶段

- **2015 · 公开竞赛展示期**：可核验记录的公开输出起点为 2015 年 Mobile Pwn2Own（东京）攻破 Nexus 6 Chrome on Android，隶属 Qihoo 360；公开作品形态为国际移动端漏洞竞赛成果展示，目标集中于移动浏览器与移动平台。此前学习路径、入门条件与练习行为无一手证据，不能据此后推。（置信度：medium）
  - 证据：gg-publications-01
- **2019-08 · 组件级漏洞独立报告期**：2019 年 8 月以 Alpha Team, Qihoo 360 身份向 Project Zero 报告 Chrome for Android Mojo CDM 组件释放后使用漏洞 CVE-2019-5870（CDM 被重复注册导致 cdm_services_ 中遗留悬垂条目）；公开输出由竞赛展示转入组件级漏洞独立发现与厂商外主动报告，反映对 Mojo IPC 生命周期与 Chrome for Android 渲染侧代码路径的工程化定位能力。（置信度：medium）
  - 证据：gg-community-01, gg-timeline-001
- **2020 · 完整利用链公开演讲期**：2020 年 Black Hat USA 以 TiYunZong: An Exploit Chain to Remotely Root Modern Android Devices 为题演讲，将 CVE-2019-5870 作为组成部分组合为可远程 root 现代 Android 设备的完整利用链并公开技术演讲；公开作品形态由竞赛与漏洞报告转为会议技术演讲，技术主题由单点漏洞扩展为 renderer 到 root 的完整远程利用链。会议官方议程页未独立抓取成功，演讲事实由 Project Zero 博客逐字引用确认。（置信度：medium）
  - 证据：gg-publications-02, gg-community-02, gg-timeline-002

## 主要成长机制

### Android Chrome 方向持续投入与公开输出形态逐级升级的闭环

起点：2015 年已具备移动浏览器攻击的公开可演示能力，且具备进入 Android Chrome 目标的组织归属（Qihoo 360）与公开竞赛通道（Pwn2Own Mobile 2015）。具体的入门学习条件、导师或同伴关系无一手证据，不能据此后推。

练习与反馈：在 Android Chrome 方向跨时期持续产出公开成果：2015 年竞赛展示 → 2019 年 8 月组件级释放后使用漏洞独立发现与报告 → 2020 年以同一漏洞为组成部分的远程 root 利用链公开演讲。此处据公开输出形态的跨时期重复推断其在该方向的反复实践；具体的练习行为、复盘方式与工具建设因无一手自述、无工具代码、无复盘记录，不予臆造，仅作推断并标注限制。；2019 年报告的 CVE-2019-5870 被 Project Zero 接收并记录，并在 P0 博客中被用作与在野 0-day（CVE-2020-6572）的对比样本；同一漏洞被本人用于 2020 年 Black Hat 演讲。反馈来源为顶级厂商研究团队（Project Zero）的引用与对比分析，构成漏洞报告进入公开反馈循环的入口。

能力与结果：对 Mojo IPC 生命周期与 Chrome for Android 渲染侧代码路径的工程化定位能力；将单点组件漏洞组合为 renderer 到 root 完整远程利用链的工程化能力；以厂商外身份向顶级厂商研究团队提交漏洞并被同行引用的可追溯输出能力。；2015 年 Mobile Pwn2Own 攻破 Nexus 6 Chrome on Android，隶属 Qihoo 360；2019 年 8 月向 Project Zero 报告 CVE-2019-5870（Mojo CDM 重复注册致释放后使用）；2020 年 Black Hat USA 以 TiYunZong 为题演讲远程 root 现代 Android 利用链

置信度：medium；替代解释：公开输出的跨时期重复也可能主要由组织资源（Qihoo 360 Alpha Team 的赛事预算、团队协作与目标可及性）与外部偶然机会（Pwn2Own 赛事窗口、Project Zero 反馈渠道可达性）驱动，而非个人反复练习所致；因缺自述、复盘记录与工具代码，个人能力与组织支撑的相对贡献无法分离，存在幸存者偏差风险。

证据：gg-publications-01, gg-community-01, gg-timeline-001, gg-publications-02, gg-community-02, gg-timeline-002

## 可迁移与不可迁移

- 可迁移：以同一组件漏洞为锚点，将单点漏洞报告延展为完整利用链并公开发表，形成发现→报告→利用链→演讲的闭环输出模式。
- 可迁移：向顶级厂商研究团队（如 Project Zero）主动提交厂商外漏洞报告，使其进入同行可追溯的知识链并被后续对比分析引用。
- 可迁移：以公开竞赛（Pwn2Own Mobile）作为早期能力对外展示与校验通道。
- 不可直接迁移：Qihoo 360 Alpha Team 的组织归属、赛事预算与团队协作，2015 至 2020 年公开成果均在此背景下产生。
- 不可直接迁移：Pwn2Own Mobile 2015 赛事窗口与 Nexus 6 Chrome on Android 目标的可及性。
- 不可直接迁移：Project Zero 作为反馈来源的可达性，其博客引用与对比分析构成公开反馈循环的具体形态。

## 复核问题

- 机制名称 'Android Chrome 方向持续投入与公开输出形态逐级升级的闭环' 中 '持续投入' 与 '逐级升级' 在仅有 2015、2019-08、2020 三个端点且中间年度证据缺失的情况下，存在被读为逐年连续递进的叙事风险；建议在 starting_conditions 或 repeated_practice 中补一句明确 '逐级升级' 仅为对三个端点公开输出形态差异的描述，而非已证实的逐年连续递进。现有 alternative_explanation 已部分覆盖该限制，属非阻塞建议。

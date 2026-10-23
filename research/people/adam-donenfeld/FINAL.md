# Adam Donenfeld：漏洞研究成长分析

- 擅长领域：Android/基带/内核漏洞
- 独立复核：pass · 89/100

## 成长阶段

- **2016-04 至 2016-08（研究/报告产出 2016-04-05；公告发布 2016-08-01；补丁等级日 2016-08-05） · Check Point Software Technologies Ltd. 期间的 Android Qualcomm GPU 驱动提权漏洞研究与厂商致谢**：同一性前提：Android Security Bulletin — August 2016 致谢行原文「Adam Donenfeld et al. of Check Point Software Technologies Ltd.: CVE-2016-2504」与 ziVA README 署名「Adam Donenfeld (@doadam)」的同一人关系系综合推断（同姓名、移动安全域、2016 与 2017 时间相邻），未经任一来源显式声明。在该前提上，研究/报告产出时点为 2016-04-05（来源表中 Date reported 字段），公告发布时点为 2016-08-01，补丁等级日为 2016-08-05，三项时点应予区分；CVE-2016-2504 评定为 Critical，对应「Elevation of privilege vulnerability in Qualcomm GPU driver」。致谢行「et al.」表明该 CVE 致谢为协作产出，能力变化主体归于研究对象时须注明协作与组织产出背景，不应完全归因为个人独立产出。据此阶段可核验：研究对象在 Check Point 任职期间，以协作方式产出可被 Android Security Bulletin 收录的 Qualcomm GPU 驱动提权漏洞研究。（置信度：high）
  - 证据：adam-rev1-001, adam-rev3-001
- **2017-08（ziVA 仓库创建 2017-08-24，首次推送 2017-08-31，据 GitHub 一手元数据） · Zimperium 期间的 iOS 内核 exploit ziVA 公开发布**：据 GitHub api.github.com/repos/doadam/ziVA 一手元数据（created_at 2017-08-24T03:42:04Z、pushed_at 2017-08-31T23:22:16Z，首提交 author name 为 Adam Donenfeld、author date 2017-08-31T23:21:27Z），ziVA 公开发布时点锚定为 2017-08，发布活动集中于 2017-08-24 至 2017-08-31，不再依赖未由一手来源核验的 iOS 10.3.1 发布月份推断。README 第一段原文为「An iOS kernel exploit designated to work on all 64-bit iOS devices <= 10.3.1」（含「64-bit」），目标为 AppleAVEDriver。README 末尾作者署名原文为「Credit for finding the vulnerabilities, chaining them together, writing the exploit go to Adam Donenfeld (@doadam).」。据 README 致谢「Zuk Avraham (@ihackbanme), Yaniv Karta (@shokoluv) and the rest of the Zimperium team for the opportunity (and the paycheck)」可推断其时点与 Zimperium 存在雇佣关系，此为推断而非「可核验任职」，且致谢文本未直接支持指导角色。仓库作者署名「Adam Donenfeld」与 stage A 致谢行「Adam Donenfeld」姓名一致，作为 handle @doadam 与研究对象姓名同一性的新增佐证（仍属推断，非来源显式声明）。（置信度：high）
  - 证据：adam-rev1-002, adam-rev4-001, adam-rev5-001

## 主要成长机制

### 跨平台底层内核漏洞的公开输出

起点：同一性前提：Android Security Bulletin 致谢行「Adam Donenfeld et al. of Check Point Software Technologies Ltd.」与 ziVA README 署名「Adam Donenfeld (@doadam)」的同一人关系系综合推断（同姓名、移动安全域、2016 与 2017 时间相邻），未经任一来源显式声明。在该前提上，研究对象先后处于 Check Point（2016）与 Zimperium（2017）的雇佣关系中，后者由 ziVA README 致谢「opportunity (and the paycheck)」推断；任职起止时间无一手时间线，仅由两点致谢/署名推断。研究域为移动端内核底层（Android 驱动提权与 iOS 内核 exploit），处于 2016-2017 移动内核披露技术窗口。

练习与反馈：现有可核验证据为 n=2 跨平台两点，而非同平台多次重复：其一为 Android 平台 Qualcomm GPU 驱动提权漏洞（CVE-2016-2504，2016-04-05 报告产出，2016-08 厂商致谢），其二为 iOS 平台 AppleAVEDriver 内核 exploit（ziVA，2017-08 公开）。两点均以「内核底层漏洞研究 → 厂商披露或公开 exploit 发布」为输出形态。；厂商补丁致谢（单点）：CVE-2016-2504 经 Android Security Bulletin — August 2016 致谢行确认，无后续反馈、再披露或迭代闭环实证。团队/同事致谢（单点）：ziVA README 列出 Zuk Avraham(@ihackbanme)、Yaniv Karta(@shokoluv) 与 Zimperium 团队并致谢「opportunity (and the paycheck)」；README 原文未直接支持指导角色，故不表述为导师反馈。两点均为静态致谢，不构成回路。

能力与结果：以雇佣关系依托的内核底层漏洞研究为输入，经厂商致谢（Android）与公开 exploit 仓库（iOS）两条可核验表面，形成「移动内核漏洞研究 → 公开披露/发布」的输出能力。该能力建立在组织提供的研究机会与协作环境之上，而非可独立复现的个人重复练习。；CVE-2016-2504 厂商致谢（Android Security Bulletin — August 2016，Critical，补丁等级日 2016-08-05，致谢行含「et al.」协作措辞）；ziVA iOS 内核 exploit 公开发布（GitHub 仓库 created_at 2017-08-24、首次推送 2017-08-31，README 第一段含「all 64-bit iOS devices <= 10.3.1」，目标 AppleAVEDriver）

置信度：medium；替代解释：两点跨平台输出可由组织资源与雇佣机会驱动（Check Point 与 Zimperium 提供的研究机会、薪酬与同事协作），而非个人可迁移的研究方法论；n=2 公开成功输出存在幸存者偏差，无法排除未成功、未公开或内部研究过程的存在，机制归纳仅适用于「公开成功输出」这一可观测子集。

证据：adam-rev1-001, adam-rev1-002, adam-rev3-001, adam-rev4-001

## 可迁移与不可迁移

- 可迁移：在前置 n=2、全部依托 Check Point 与 Zimperium 雇佣关系、2016-2017 移动内核披露技术窗口的限制下，「移动内核底层漏洞研究 → 厂商致谢披露或公开 exploit 发布」的输出形态在两点跨平台证据中均出现，可作有限的可迁移实践参考；该归纳受样本量与组织条件约束，不构成可独立复现的方法论。
- 可迁移：以公开仓库承载 exploit、以 README 明确署名与致谢并显式声明责任归属（ziVA README「Credit for finding the vulnerabilities, chaining them together, writing the exploit go to Adam Donenfeld (@doadam)」）的公开输出习惯，可作为面向公开披露的可迁移做法，但同样受前述组织与样本限制。
- 不可直接迁移：雇佣关系提供的研究机会与薪酬：ziVA README 致谢「opportunity (and the paycheck)」表明 iOS 阶段的公开输出依托 Zimperium 雇佣关系，非个人可独立获得的条件。
- 不可直接迁移：同事与团队协作环境：ziVA README 列出 Zuk Avraham(@ihackbanme)、Yaniv Karta(@shokoluv) 与 Zimperium 团队；CVE-2016-2504 致谢行「et al.」体现协作产出背景，协作网络为组织条件，不可随个人迁移。
- 不可直接迁移：2016-2017 移动内核披露技术窗口：两点输出集中于该时段的 Android Qualcomm 驱动与 iOS AppleAVEDriver 内核目标，技术窗口与厂商披露生态为时期外部条件。
- 不可直接迁移：样本量 n=2 不足以支撑复现性验证：现有证据为两点跨平台输出，validation_tests 仅保留 distinctive，移除 repeated，无法据此验证同平台多次复现性。

## 复核问题


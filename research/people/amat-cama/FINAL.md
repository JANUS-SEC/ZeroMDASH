# Amat Cama：漏洞研究成长分析

- 擅长领域：基带与移动端漏洞
- 独立复核：pass · 85/100

## 成长阶段

- **2019 · Pwn2Own 赛事首次可核验参与**：Wikipedia Pwn2Own 条目正文记载，2019 年 Amat Cama 与 Richard Zhu 以 Team Fluoroacetate 名义参赛，针对 Amazon Echo Show 5 上的旧版 Chromium，利用其与上游已修复版本之间的 patch gap，获得 60,000 美元奖金。该记录为本次可核验到的首次以团队名义公开演示漏洞利用的事实。需说明：赛事记录仅保留成功演示，参赛前是否进行多次尝试、是否尝试其他目标均不可知（幸存者偏差）。（置信度：medium）
  - 证据：amat-timeline-01
- **2020-03 · Pwn2Own Desktop 同届两次成功演示**：Wikipedia Pwn2Own 条目正文与 Exploits 表记载，2020 年 3 月 18–19 日 Pwn2Own Desktop 赛事上，Fluoroacetate（Amat Cama、Richard Zhu）成功演示 Microsoft Windows 与 Adobe Reader（含提权）两次利用，合计 90,000 美元，获该届 Master of Pwn 称号；该届全赛事共 6 次成功演示、总奖金 270,000 美元、13 个独立 bug。此处采事实陈述：2019 届记录到一次成功演示，2020 届记录到两次成功演示。不得据此断言“由单一目标扩展到同届多目标”的能力递进——赛事仅记录成功演示，失败尝试不入记录，2019 届是否尝试多目标不可知（幸存者偏差）。Oracle VirtualBox 在该届表格中分别归于 STAR Labs（Phi Phạm Hồng）与 Zero Day Initiative（Lucas Leong），不归于 Fluoroacetate，故不计入其目标清单。（置信度：medium）
  - 证据：amat-timeline-02, ac-targeted-r2-001

## 主要成长机制

### 与固定同伴连续参赛的协作参与模式

起点：Wikipedia Pwn2Own 条目作为唯一可核验一手锚点，其正文记载 Team Fluoroacetate 由 Amat Cama 与 Richard Zhu 组成，并记录了 2019 与 2020-03 两届的参赛事实。赛事体系提供了公开演示、奖金与称号等形式化反馈通道。在该可核验范围内，参赛前的研究基础、练习方式与团队形成过程均无一手来源。

练习与反馈：在可核验的两届记录中，同一二人组合以同一队名连续参加 Pwn2Own，并在不同目标（Echo Show 5 旧版 Chromium、Microsoft Windows、Adobe Reader 含提权）上完成公开演示。该“重复”仅指赛事记录中可观察到的连续两届参赛这一行为模式，不延伸至赛事外的练习或准备过程。；可核验的反馈来自赛事本身：2019 届 60,000 美元奖金，2020 届 90,000 美元奖金与 Master of Pwn 称号。这些反馈均为公开、外部、形式化的结果，未取得赛事外同行、雇主或社区的反馈来源。

能力与结果：在可核验范围内观察到的是“以固定二人组合连续参赛并完成公开演示”这一参与模式的存在。是否伴随利用链完成度或攻击面覆盖的实际提升，因赛事仅记录成功演示（幸存者偏差）且缺乏赛事外一手材料，无法据现有证据判定。；2019 届记录到针对 Amazon Echo Show 5 旧版 Chromium patch gap 的一次成功演示，奖金 60,000 美元（据 amat-timeline-01）。；2020 届记录到针对 Microsoft Windows 与 Adobe Reader（含提权）的两次成功演示，合计 90,000 美元，获 Master of Pwn 称号（据 amat-timeline-02 与 ac-targeted-r2-001 逐字核实）。

置信度：medium；替代解释：存在多个竞争性解释，现有证据无法排除：（1）参赛前已具备相应利用能力，赛事表现为既有能力的展示而非协作增量，所谓“成长”可能仅是公开曝光序列；（2）幸存者偏差——赛事仅记录成功演示，2019 届是否尝试多目标、历届是否存在未成功的尝试均不可知，将“一次→两次”读为能力递进缺乏支撑；（3）身份同一性范围限制——Wikipedia Pwn2Own Fluoroacetate 成员 Amat Cama 与 person_json 所记 Amat Cama（baseband、ambionics.io/blog、x.com/am_at）之间的同一性未经一手来源核验，故该机制的适用对象严格限定为“Wikipedia 可核验的 Amat Cama”，无法确认该协作模式为 person_json 所指对象能力成长的主因。据此，confidence 取 medium，仅指向上述参与模式在 n=2 两届记录中的存在，而非其因果效力。

证据：amat-timeline-01, amat-timeline-02, ac-targeted-r2-001

## 可迁移与不可迁移

- 可迁移：事件级陈述（2019 届，支撑记录 amat-timeline-01）：在可核验的 2019 届观察到针对 Amazon Echo Show 5 旧版 Chromium 的 patch gap 目标选择，即利用厂商已修复但目标运行版本尚未更新的版本差作为利用窗口。此项仅由单一赛事记录支撑，不构成可迁移通则。
- 可迁移：事件级陈述（2020 届，支撑记录 amat-timeline-02、ac-targeted-r2-001）：在可核验的 2020 届观察到同届覆盖多个目标（Microsoft Windows、Adobe Reader 含提权）的参赛行为。此项仅由单一赛事记录支撑，不构成可迁移通则。
- 可迁移：与固定同伴组成稳定二人组合连续参加同一赛事（2019、2020-03 两届，支撑记录 amat-timeline-01、amat-timeline-02）：在可核验范围内观察到该协作参与模式的存在。此项由 n=2 两届记录支撑，可作为“可观察到的重复行为”而非“保证有效的通用做法”。
- 不可直接迁移：身份同一性未核验：Wikipedia Pwn2Own Fluoroacetate 成员 Amat Cama 与 person_json 所记 Amat Cama 之间的同一性未经一手来源确认，结论适用对象仅限“Wikipedia 可核验的 Amat Cama”。任何据此推断的协作习惯或能力状态，不得外推到 person_json 所指对象。
- 不可直接迁移：赛事形式化反馈不可复制：Pwn2Own 提供的奖金、称号（Master of Pwn）与公开演示机会为特定赛事条件，赛事外的安全研究环境不具备等价的形式化反馈与公开曝光通道。
- 不可直接迁移：参赛前研究与资源条件不可知：可核验材料仅含赛事结果，缺乏参赛前的工具建设、设备/固件样本获取、漏洞储备、研究时间投入等条件记录，无法据以判断可迁移性。
- 不可直接迁移：patch gap 目标的可利用性受外部条件约束：Amazon Echo Show 5 旧版 Chromium 的 patch gap 存在与否取决于厂商修复节奏与设备版本更新滞后，属特定时期与特定产品的外部条件，不构成普遍可复用的目标选择条件。

## 复核问题


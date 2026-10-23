# 未通过独立复核

已达到最大修订次数 4；本文件是审计草稿，不得进入跨人物比较。

# Nicolas Joly：漏洞研究成长分析

- 擅长领域：Windows/虚拟化漏洞
- 独立复核：revise · 90/100

## 成长阶段


## 主要成长机制

## 可迁移与不可迁移

- 不可直接迁移：person_json.json 的 rank 字段（取值 93）为编排器输入对象元数据，非外部权威评价来源，未经一手来源核实；不得将排名预设解读为外部权威评价（nj-ext-02，inferred）。
- 不可直接迁移：机构归属（Airbus/Quarkslab/VUPEN/Synacktiv 之间冲突）与 Pwn2Own 参赛记录依据 nj-works-03 与 nj-comm-04 的合成叙述，二者均为 lead_only/unknown，WebSearch 在本环境不返回真实结构化结果；该依据不依赖 ZDI 两文是否可抓取，但所引 Pwn2Own 年份冲突与机构归属陈述以 404 修正后口径重述，不得升级为 documented/reported（nj-works-03、nj-comm-04、nj-r4-01）。
- 不可直接迁移：selected_conference_evidence 字段列出的 Black Hat US/EU、BlueHat、POC 为编排器输入线索，对应会议议程页本轮未抓取；msrc.microsoft.com/blog 经 301 重定向至 microsoft.com/en-us/msrc/blog，未在该页检索到 Nicolas Joly 致谢条目（首页仅列 2026-07 帖）；会议与致谢证据当前为线索级，不得作为已证实演讲事实（nj-comm-03、nj-r4-01）。

## 复核问题

- 字段 non_transferable_conditions 第 3 条：将『未在该页检索到 Nicolas Joly 致谢条目（首页仅列 2026-07 帖）』改写为『nj-r4-01 仅确认 microsoft.com/en-us/msrc/blog 首页可正常抓取、最近帖为 2026-07；未对该页进行 Nicolas Joly 致谢条目的主动检索，是否存在致谢条目未经核实』，使措辞与 nj-r4-01 的 claim 范围一致，删除超出 claim 的『未检索到致谢条目』推断。原措辞『未在该页检索到 Nicolas Joly 致谢条目』；改写方向：限定为首页访问性事实，致谢条目存在性标注为未经核实。
- 字段 tensions 第 7 条：将『round-3 action/result 叙述（404 Not Found/域名安全校验失败）』改写为『round-3 action/result 叙述（404 Not Found）』；evidence_json 中 round-3 的 action/result 叙述原文为 404 Not Found，『域名安全校验失败』非 round-3 叙述原文，系继承自 round-4 RR8 review_issue 的措辞，应删除以与 round-3 叙述原文一致。原措辞『404 Not Found/域名安全校验失败』；改写方向：仅保留 round-3 叙述原文『404 Not Found』。
- 字段 tensions 第 7 条：将『与 round-3 receipt 的 success 标记矛盾』改写为『与 round-3 receipt 的 success=true 标记存在不一致；该不一致可能源于 success 标记反映工具请求完成（含 404 响应体）而非资源存在，或源于叙述误述，根因未能从 receipt 内部核实，保留为未决』；区分『工具请求成功』与『服务器返回 404』两个语义层，避免将不同语义层的标记表述为直接『矛盾』。原措辞『与 round-3 receipt 的 success 标记矛盾』；改写方向：明确语义层区分并保留根因未决。
- 字段 tensions 第 4 条：将『四者均无可核验的真实搜索结果块支撑』改写为『上述四项机构归属陈述（Airbus、Quarkslab、VUPEN、Synacktiv）均无可核验的真实搜索结果块支撑』；原措辞『四者』指代稍显模糊，字面可被误读为四个 evidence item，应明确指代四个机构归属陈述。原措辞『四者均无可核验的真实搜索结果块支撑』；改写方向：明确指代对象为四个机构归属陈述。
- 综合结果没有可复核的成长阶段或机制。

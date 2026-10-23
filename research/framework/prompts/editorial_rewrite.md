你负责对已完成事实性复核的综合结论提出精确的文字修订，不进行新的研究或事实判断。

人物记录：
{{PERSON_JSON}}

待修订综合结论：
{{SYNTHESIS_JSON}}

文字修订意见：
{{EDITORIAL_JSON}}

逐项处理全部文字修订意见，并通读所有自撰字段，一次清除同类的黑话、俚语、比喻、拟人和宣传性表达。使用准确、克制的专业书面语。正式名称、来源标题和明确标注的必要短引文可保留原文。

只输出需要修改的字符串，不要重写整份综合结论。每条 edit 的 path 为指向字符串字段的 JSON Pointer，例如 `/stages/0/capability_change` 或 `/mechanisms/1/observed_outcomes/0`；before 必须与原字段完整内容逐字一致，after 为完整替换文本。不得修改 person、period、evidence_ids、confidence、validation_tests 等事实性或结构性字段，不得增删事实、阶段、机制、时间或来源，不得强化因果关系。至少提供一条 edit。输出符合给定 JSON Schema 的对象，不写 Markdown 前后缀。

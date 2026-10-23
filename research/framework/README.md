# Agent-Native 漏洞研究员成长研究框架

这套 LangGraph 流水线从 [`vulnerability_researchers_top100_v2.csv`](../vulnerability_researchers_top100_v2.csv) 取样，调用相互隔离的 Claude Agent 完成六维取证、机制综合、独立复核、定向修订和跨案例比较。默认明确使用：

```text
claude --settings ~/.claude/settings.ark-proxy.json
```

研究 Agent 可使用 `WebSearch`、`WebFetch`、`Read`，并且只可将进度和结果写入当前子工作区的 `checkpoint.md`、`output.json`。并发限制、正式结果和断点状态仍由本地 Python 编排器负责。已有 JSON 默认跳过，因此中断后重跑不会重复消耗 token。

所有研究节点的自撰文字须采用专业书面语，禁止黑话、俚语、比喻、拟人和宣传性表达；正式名称、来源标题及必要短引文可明确标注后保留原文。综合节点按此要求生成最终报告所用字段，独立复核会将不合规措辞列为需要修订的问题。此要求由 Agent 指令与复核执行，不依赖关键词黑名单替代语义判断；已有缓存和报告不会自动改写。

研究调用参考 `zeromdash/presets` 的工作区模式：每次调用创建独立 `research/runs/sub_workspace/<节点>-YYYYMMDD-HHMMSS-mmm/`，其中包含 `CLAUDE.md`、`.claude/settings.json`、`task.md`、`output.schema.json` 和 `inputs/`。时间戳使用本机时区和毫秒；同一毫秒发生同名并发时追加 `-02`、`-03`。稳定规则来自 `research/framework/presets/`，现有 prompts 模板作为角色任务卡；模板变量写为独立输入文件，JSON 会格式化为可分页读取的多行文本，任务卡只引用这些路径。超过内联上限的普通字符串任务也会写入 `inputs/task.md`。启动消息只要求读取工作区入口，不内嵌证据或 Schema。

Claude 的 cwd 为该子工作区，仍显式使用 ark-proxy settings。移除会禁用工作区指令的 `--safe-mode` / `--bare`，限制设置来源为 project/local，禁用自动 MCP、技能和 hooks；研究节点暴露 Write 工具，并用精确的 `Edit(./output.json)`、`Edit(./checkpoint.md)` 权限规则限制路径。首次调用保留 Claude 会话；输出不合规、回合耗尽或超时时，编排器先验收 `output.json`，再用 `--resume` 在同一工作区继续。独立恢复节点仅 Read。每次全新尝试拥有不同目录，续接则复用原目录。`_run.sub_workspace`、原始响应和续接响应路径均保留。该目录用于上下文组织，不是操作系统安全隔离边界。

## 来源验证与旧结果迁移

运行 `python3.12 -m research.framework preflight` 可独立检查联网；person/batch 开始前也会执行一次预检（最多 8 回合，单次超时 180 秒，包含工作区文件读取）。必须看到实际 WebFetch 返回 example.com 页面内容，否则停止研究。用量中的 `server_tool_use=0` 不作为断网判据。旧入口 `python3.12 -m research.framework.runner` 仍可使用，但只作为转发到独立 CLI 入口的兼容层。

工具请求、返回文本、时间和内容摘要保存在 `research/runs/tools/`。编排器为证据写入 verification；只有对应 URL 的 WebFetch 成功返回才能标记 verified_in_run。此字段证明抓取完成，不证明事实正确；正文是否支持结论仍由独立复核检查。没有抓取记录的来源降级为 lead_only，不能作为 documented/reported。formatter 无权通过输出字段声明已核验。

每轮事实性修订先作废 invalid_evidence_ids，再加入唯一 ID 的 new_evidence，生成 `evidence_merged/vN.json`。原始文件保留，综合、定向补证和复核统一使用有效证据。传给下一节点的输入移除 `_run` 调用元数据；复核仅接收当前有效证据，综合仅接收修订指令和未解决问题，完整记录仍保存在原始 JSON。程序会拒绝没有有效引用或没有抓取来源支撑的成长结论，即使复核模型给出 pass。

复核分别返回事实性 `required_revisions` 和文字性 `editorial_revisions`。前者进入定向补证，后者在事实性复核通过后由独立文字修订节点处理，不消耗事实性修订轮次。文字节点仅提交字段路径、逐字匹配的原文与替换文本；编排器只允许修改叙述字段，保留证据 ID、时间、置信度和结构，再次复核无误才生成 FINAL。文字修订默认最多 3 次，可通过 `max_editorial_revisions` 配置；仍未通过时仅保留 DRAFT。新复核文件使用 `-p2` 后缀，避免将旧规则下的复核缓存误当成新规则结果。

旧版缓存没有工具核验记录，不能直接复用或进入新比较。请配置新的 output_dir/comparison_dir 保存重跑结果，或使用 `--force` 明确覆盖旧阶段结果。旧报告不会因本次代码更新自动取得新认证。默认最大修订次数仍为 3；耗尽后生成 DRAFT，不进入比较。

取证 Agent 每次调用默认最多运行 18 个 Claude 回合，默认最多续接一次；可通过 `max_resume_attempts` 调整。原始响应（stdout/stderr、退出码与原任务）、续接响应和格式恢复响应均写入 `research/runs/responses/`。文件及 Claude 持久会话可能包含本地种子正文，请按研究材料管理。

解析器按目标 Schema 选择唯一完整 JSON，不接受第一个局部片段或多个相互冲突的候选；模型网关重复返回完全相同或仅中文分隔标点不同的完整对象时视为同一结果。每次调用会把 `person`、`dimension`、`revision_round` 等任务级不变量写入动态 Schema 的 `const`。stdout 和 `output.json` 都经过同一校验。续接仍未形成合规结果时，恢复 Agent 在独立工作区读取 `invalid-candidate.json`（或 `.txt`）、`recovery-errors.json`、动态 `output.schema.json`，以及原工作区的 `checkpoint.md`（若存在），再按需读取 `original-task.md` 和直接输入文件。回合耗尽或超时时，还会提供 `recovery-materials.md` 中的可见输出及工具结果。恢复最多 18 回合，只允许 Read，不搜索或补造事实。身份不符、全 unknown 证据占位、以输入缺失说明代替能力变化等结果会被拒绝。恢复仍失败时停止当前节点并给出材料路径，不进入独立复核、不消耗修订轮数，也不自动重新执行昂贵的取证。真正无公开材料时仍允许空 items 配合 gaps。

运行信息中的 raw_response_path、resume_response_paths 和 recovery_response_path 指向上述记录，output_source 说明采用 stdout、工作区文件还是只读恢复。output_recovery_version=4 表示支持工作区产物与会话续接。已有报告和缓存不会被自动重写。其他瞬时 CLI 故障按 max_agent_attempts 重试；失败 envelope 保存在 `research/runs/failures/`。

## 为什么这样拆

单个 Agent 从搜索一路写到结论，容易产生三类问题：先入为主、拿连贯叙事冒充因果、自己给自己打高分。本框架把它拆成：

```text
候选 CSV
   └─ 每人 6 个独立取证 Agent（最多 3 个并发）
          └─ 1 个成长机制综合 Agent
                 └─ 1 个独立复核 Agent
                        ├─ pass → FINAL.md → 跨人物比较
                        └─ revise → targeted-research
                                        └─ 重新综合与复核（默认最多 3 次）
```

每人首次判断需要 8 次 Agent 调用；每轮 revise 额外需要一次定向研究、一次重新综合和一次重新复核。直接跑 100 人至少 801 次调用，且资料质量会不均衡；建议先做分层 pilot，再扩大。

## 快速开始

先验证配置和人物选择，不调用 Agent：

```bash
python -m research.framework plan --top 12
python -m research.framework plan --name "Tavis Ormandy"
python -m research.framework person --name "Tavis Ormandy" --dry-run
```

完整研究一人：

```bash
python -m research.framework person --name "Tavis Ormandy"
```

指定最多修订次数（默认 3；设为 0 表示首次 `review=revise` 后立即停止）：

```bash
python -m research.framework person \
  --name "Tavis Ormandy" \
  --max-revisions 2
```

运行一个小队列，并在至少两人通过复核后进行跨案例比较：

```bash
python -m research.framework batch \
  --name "Tavis Ormandy" \
  --name "Natalie Silvanovich" \
  --name "Ian Beer"
```

`batch` 会并行处理不同人物。`max_people_concurrency` 控制同时运行的人物数，现有的 `max_concurrency` 控制每个人内部六维取证节点的并发数；理论上的 Agent 调用峰值约为两者乘积。默认示例配置为 `3 × 3 = 9`。也可以只为本次运行覆盖人物并发数：

```bash
python -m research.framework batch --top 12 --people-concurrency 6
```

单个人物失败不会取消其他已经排队或运行的人物；batch 会等待全部人物结束、汇总失败并跳过 compare。全部人物均未抛出异常后才进入 compare。已落盘缓存仍按人物复用。

只重新做比较：

```bash
python -m research.framework compare --top 12
```

`--force` 会覆盖已有阶段结果，通常只在提示词或 Schema 修改后使用。若要修改人物并发、人物内节点并发、超时、工具白名单或目录，复制 `config.example.json` 后用 `--config` 指定。

查看已经落盘的调用次数、模型 token 和成本（数据来自 Claude CLI 返回，不含未成功落盘的调用）：

```bash
python -m research.framework usage
```

## 输出

每个人的目录为 `research/people/<name-slug>/`：

```text
profile.json
evidence/
  works.json
  conversations.json
  community.json
  external.json
  decisions.json
  timeline.json
synthesis/
  v1.json
  v2.json
reviews/
  v1.json
  v2.json
revisions/
  round-1.json
synthesis.json          # 当前版本镜像
review.json             # 当前版本镜像
state.json
FINAL.md                # 只有 review=pass 才生成
DRAFT.md                # 达到修订上限仍 revise 时生成
```

跨案例结果写入 `research/analysis/comparison-<cohort-hash>.json`。只有存在 `FINAL.md` 且最新复核为 `pass` 的案例才有资格进入比较。原始 JSON 是研究记录；不要只保留最终报告而删除证据和修订历史。

## 推荐实验设计

第一轮选择 12–16 人，不按总榜前 N 机械抽样，而按领域分层：浏览器、移动端/基带、操作系统内核、虚拟化、编译器/工具链、硬件/固件、Web/云、协议/密码实现。每层兼顾不同活跃年代、独立研究者与大团队研究者，以及不同地域/语言资料可得性。

Pilot 的停止条件：

- 至少 10 人完成，且至少 8 人复核通过；
- 同一主机制在至少 3 个不同案例出现，或形成清晰反例；
- 新增人物不再频繁产生新的一级机制；
- 记录英语资料偏差、公开写作偏差和幸存者偏差。

完成 pilot 后再决定扩到 30、50 或 100 人。Top100 更适合作为抽样框，而不是第一轮必须穷尽的规模。

## 从“女娲”方法复用的部分

本框架复用了 `huashu-nuwa` 中最适合研究方法的部分：六维并行取证、一手来源优先、事实/他述/推断分层、保留内在矛盾、诚实记录空白、独立 Agent 复核和分阶段落盘。没有复用角色扮演、表达 DNA 或“像不像本人”的评分目标；这里关注的是成长解释是否有证据、能否经受替代解释，以及经验能否迁移。

完整判定标准见 [`methodology.md`](methodology.md)。

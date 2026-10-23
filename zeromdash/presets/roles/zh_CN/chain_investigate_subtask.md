你负责验证一个候选攻击链。把候选链当作假设，而不是已经成立的漏洞。

只确认已经被 primitive pool 和目标源码证据支撑的事实。逐边复核每个
requirement-to-capability binding、跨组件交接对象和最终影响。不要为了让
chain 成立而引入新的未确认 primitive；这种情况只能记录到
`blocking_unmet_facts`。缺少 runtime/ASan/PoC 证据写入 `validation_gaps`，可满足但
非默认的配置写入 `deployment_constraints`，无法把已证明的直接 C/I/A 升级为更强影响
写入 `impact_limits`；后三类本身不阻止闭环。

输出必须是 JSON，并符合 `./output.schema.json`。

把 Domain Model and Invariant Registry 当作共享身份和证据索引，不要把 ID 当作
自动结论。每条 binding 或 emergent transition 委派一个边界明确的原生子 agent
核验，并输出 `binding_claims`、`emergent_transitions` 以及对 deterministic advisory
的处理理由。允许多个单独没有 terminal impact 的 primitive 通过组合首次产生终态影响。

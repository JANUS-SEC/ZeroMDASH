# Felix Wilhelm -- 对话、演讲与即兴思考

## 重要发现：当前职业状态更新

Felix Wilhelm 于2022年左右从 Google Project Zero 离开后，并非加入 Google Cloud Security，而是：
- 可能短暂在 Jump Crypto 工作
- **2022年至今**: Asymmetric Research 联合创始人兼 CTO（区块链/DeFi安全公司，总部瑞士）
- Twitter handle 从 @_felixwilhelm 改为 @_fel1x
- 2025年在 Breakpoint（Solana会议）做了演讲

---

## 会议演讲历史

| 年份 | 会议 | 标题/主题 | 附属机构 |
|------|------|-----------|----------|
| 2014 | PHDays (Moscow) | Xen/虚拟化研究 | ERNW |
| 2014 | TROOPERS 14 | "Compromise-as-a-Service: Our PleAZURE" (with Matthias Luft) | ERNW |
| 2015 | 44CON London | "Playing with Fire: Attacking the FireEye MPS" | ERNW |
| 2015 | SyScan Singapore | Workshop: "Exploiting Hypervisors" (with Matthias) | ERNW |
| 2015 | TROOPERS 15 | "General Pr0ken File System" + Hypervisor Workshop | ERNW |
| 2016 | TROOPERS 16 | "Attacking Next-Generation Firewalls" | ERNW |
| 2016 | Infiltrate (Miami) | "Xenpwn" | ERNW |
| 2016 | SyScan 360 (Singapore) | "Xenpwn" | ERNW |
| 2016 | Black Hat USA | "Xenpwn: Breaking Paravirtualized Devices" | ERNW |
| 2017 | HITB Amsterdam | "Attacking Virtualization at the Source" (VMware) | ERNW/P0过渡期 |
| 2018 | Black Hat USA | "Attacking Cloud Hosted Container Management" | Google P0 |
| 2019 | Black Hat USA | Intel CSME 研究 | Google P0 |
| 2022 | Black Hat USA | "Mind The Gap: Studying the Insecurity of Provably Secure Embedded TEEs" | Google |
| 2025 | Breakpoint (Solana conf) | "Security Block: Asymmetric Research" | Asymmetric Research |

**注意**: 未发现任何 CCC (31C3以外)、OffensiveCon、或 REcon 演讲记录。

---

## P0博客文章中的过程叙事（核心一手来源）

### "An EPYC escape" (2021) -- 最详细的过程揭示

**研究动机与目标选择:**
- "I decided to spend some time hunting for a KVM vulnerability that could be turned into a guest-to-host escape."
- 选择AMD nested virtualization因为"implementing this correctly is quite difficult with a large potential for complex logic flaws, making it a perfect target for manual code review"
- "reviewing the same functionality for AMD seemed like a good starting point" after success on Intel side

**挫折与坚持:**
- "After getting frustrated with the total lack of progress, watching my server reboot for the hundredth time, trying to come up with a different exploitation strategy for two weeks...I realized that I made an important mistake."
- "After spending some time scrolling through AMD's documentation, I still decided that VM_HSAVE_PA seems to be the best way forward and decided to tackle these problems one by one."
- "slow trial and error" 作为正常研究过程

**自我批评:**
- "under the mistaken assumption that I solved the problem"
- 描述最终方案为 "a somewhat boring but easy-to-implement approach"

**行业判断:**
- "While we have not seen any in-the-wild exploits targeting hypervisors outside of competitions like Pwn2Own, these capabilities are clearly achievable for a well-financed adversary."
- "Looking at the potential ROI on an exploit like this, it seems safe to assume that more people are working on similar issues right now"
- "highly exploitable security vulnerabilities can still exist in the very core of a virtualization engine, which is almost certainly a small and well audited codebase."

**时间透明:**
- "I've spent around two months on this research, working as an individual with only remote access to an AMD system."

### "Enter the Vault" (2020)

**发现过程:**
- "At this point I was slowly getting frustrated and decided to take a look at Vault's response parsing code." -- 挫折作为转向触发器
- "Finding a reflected parameter that is not constrained to alpha-numeric characters turns out to be tricky."

**架构批判:**
- "Putting HTTP request forwarding into the unauthenticated external attack surface of a security product requires strong confidence in the implementation."
- 关于外部依赖风险: "AWS might decide to put STS behind a load balancing frontend...Without any change to the Vault codebase, this could severely degrade the security."

**哲学结论:**
- "Even with memory-safe languages, strong cryptography primitives, static analysis and large fuzzing infrastructure, some issues can only be discovered by manual code review and an attacker mindset."
- "tricky vulnerabilities like this often exist where developers have to interact with external systems and services."
- "As more and more companies move to the big cloud providers, familiarity with these technology stacks will become a key skill for security engineers and researchers."

---

## Asymmetric Research 博客中的表达（2025-2026）

### "Solana p-token: Catching a Bug Before Mainnet" (2026-04)
- "individually safe optimizations can become vulnerabilities when composed with new functionality"
- 漏洞存在于"a heavily scrutinized codebase" -- 审计过的代码依然有subtle bugs

### "Threat Contained: marginfi Flash Loan Vulnerability" (2025-09)
- "a small and seemingly harmless change in a well-audited, carefully designed codebase can introduce a critical vulnerability"
- "Although many recent web3 incidents stem from operational mistakes, phishing, or supply chain compromises, smart contract security remains the foundation of every DeFi project."

### "Wrong Offset: Bypassing Signature Verification in Relay" (2025-09)
- "there remains a clear need for better developer frameworks and libraries that provide secure-by-default wrappers"
- "Solana's native signature verification programs are easy to misuse and have been the source of several critical vulnerabilities since the early days"

---

## ERNW时期的对话与回顾

### 31C3 回顾 (2014-12)
- 称 Fabian Yamaguchi 的 graph database mining 为 "one of my favorite talks"
- 这揭示他重视什么：自动化辅助人类审计

### Infiltrate/SyScan 360 回顾 (2016-04)
- 称赞 Sean Heelan 处于"the intersection between the academic program verification community and the IT security industry" -- 揭示他看重学术与工业的桥梁
- 称 Matthias Kaiser 的 Java 反序列化 slides 为 "a must read for every pentester"
- 两个会议都有 "great organization, very technical talks and a cool audience"

---

## 对话/表达中的决策模式

1. **战略目标选择**: 基于市场影响力评估（AMD市场份额增长 → KVM AMD研究）
2. **挫折即转向信号**: 多次提到"getting frustrated"后改变策略
3. **务实利用**: 优雅方案失败时接受"boring but easy-to-implement"路径
4. **assembly级验证**: 不信任源码层面的分析结果

---

## 信息空白

- **无已知播客出场**
- **无传统媒体访谈**
- **无CCC演讲** (media.ccc.de搜索结果为0)
- **Twitter/X内容不可访问**（账号存在但需登录）
- **无公开Q&A转录**
- **无AMA或Reddit讨论**

**观察**: Felix Wilhelm 的公开交流几乎完全通过技术博文和会议演讲进行。他不做播客、不接受访谈——这本身就是重要的性格信号。

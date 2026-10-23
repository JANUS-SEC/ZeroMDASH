# Felix Wilhelm -- 决策记录与职业转折

## I. 职业决策时间线

### 教育：KIT (Karlsruhe Institute of Technology), ~2013-2015
- 硕士论文: "Tracing Privileged Memory Accesses to Discover Software Vulnerabilities"
- 导师: Prof. Dr. Frank Bellosa (主), Prof. Dr. Wolfgang Karl (副)
- 论文产出 xenpwn 工具，直接受 j00ru/gynvael 的 Bochspwn 启发
- **决策逻辑**: 将学术研究与实际安全研究结合（论文直接导致真实CVE发现）

### ERNW GmbH (~2013-2016/2017)
- 安全研究员/顾问，专注应用安全、逆向工程和虚拟化安全
- 与 KIT 操作系统组保持学术关联
- **为什么选择ERNW**: Enno Rey的ERNW是德国顶级安全咨询公司，TROOPERS是其会议
- **研究自由度**: 能在企业咨询中做深度研究（不是所有咨询公司都支持）

### Google Project Zero (~2017-2022)
- 加入时间推断: 2016年末/2017年初（最后ERNW博客2016-04，首个Google credit 2017-10）
- **为什么加入P0**: 无直接声明，但推断因素：
  - P0提供纯研究时间，无商业咨询压力
  - 能接触最高影响力的目标
  - 与Jann Horn（Spectre合作）等顶级研究者共事
  - 延续虚拟化研究但扩大到更广的攻击面

### 可能的Jump Crypto过渡期 (~2022)
- 来源: Asymmetric Research网站bio提及
- **信度**: 中等（间接来源）

### Asymmetric Research, 联合创始人/CTO (2022-present)
- 区块链/DeFi安全公司，总部瑞士
- 保护$5B+数字资产
- 2025年在Breakpoint（Solana会议）演讲
- **决策逻辑推断**:
  - 区块链是当前"最高价值安全边界"之一
  - 从纯研究转向研究+创业
  - 瑞士（crypto友好法律环境）
  - 将虚拟化/隔离研究经验应用于智能合约安全

---

## II. 研究方向选择逻辑

### 为什么选择虚拟化/Hypervisor？

**一手证据（从他自己的文章中提取）：**

1. **被忽视但影响巨大的攻击面**:
   - "the attack surface of hypervisors is often larger than expected" (XSA 110/105, 2015)
   - "not enough researchers are actively looking into Hyper-V" (SyScan 2015)
   - "reviewing the same functionality for AMD seemed like a good starting point" -- 审查不足的代码

2. **逻辑漏洞优于内存损坏**:
   - "logic bugs involving wrongly emulated instructions are much more common" than memory corruption
   - 选择逻辑漏洞因为它们更容易可靠利用

3. **共享内存天然不安全**:
   - PV设备研究因为共享内存接口"much harder to secure" compared to message-based IPC

4. **市场趋势创造新机会**:
   - "the recent increase of AMD's market share in the server segment means that KVM's AMD implementation is suddenly becoming a more interesting target" (KVM文章, 2021)

### 为什么扩展到云/容器安全？

自然从"逃逸单个VM"扩展到"逃逸云隔离原语"：
- Black Hat 2018 容器管理攻击
- KVM文章强调嵌套虚拟化因Windows VBS而更广泛部署
- Vault研究关注云认证逻辑

### 为什么BTB/Spectre研究？

mario_baslr README揭示：他读了学术论文后发现"the authors don't seem to have realised that their technique is not only usable for attacks against KASLR or other user-space tools but also works regardless of virtualization boundaries."
- **决策模式**: 读学术论文→发现作者忽略的实际应用→扩展到安全场景

### 为什么转向区块链安全？

**推断（无直接声明）：**
- 跟踪"最高价值安全边界"的一贯模式
- 2013-2016: 企业网络设备（防火墙/路由器是关键基础设施）
- 2017-2022: 云虚拟化（AWS/GCP基础）
- 2022+: DeFi/区块链（锁定价值数十亿美元的智能合约）
- 创业可能性：安全研究商业化的新路径

---

## III. 方法论与工具选择

### 工具开发决策

1. **xenpwn (2015)**: 从Bochspwn适配→选择性追踪Xen inter-domain通信页，而非全部内存
   - 设计决策: 只追踪"interesting"页面以控制性能开销

2. **weggli (2020-2021)**: 语义代码搜索
   - "Minimal setup" -- 无需构建目标软件
   - "Interactive" -- 快于grep，支持快速查询迭代
   - "Greedy matching" -- 最大化有用匹配，接受假阳性
   - 灵感: Semgrep, Coccinelle, joern, CodeQL但"different design decisions"
   - **核心信念编码**: 自动化应辅助人类审计者，而非替代

3. **z3-rs fork**: Rust Z3 bindings → 暗示使用形式化方法

### 研究工作流

- **Manual code review for complex logic**: "making it a perfect target for manual code review"
- **迭代利用+务实转向**: 发现假设错误后改变策略
- **组件化系统审计**: IBM GPFS系统性检查所有三层
- **特征交集**: "vulnerabilities emerge from the intersection of features"

---

## IV. 披露实践

### 可观察模式

1. **负责任披露+知识共享**:
   - XSA 105: 先报告厂商，后在会议公布exploit代码
   - "Full exploit code will be presented during the Exploiting Hypervisors Workshop at Troopers 15"

2. **主动防御贡献**:
   - dnsmasq研究中"submitted another patch which will run Dnsmasq under seccomp-bpf"
   - 不止报告漏洞，还提供加固方案

3. **遵循P0的90天政策**: 无公开反对或批评

4. **诚实归因**:
   - shell globbing文章: "Full credit should go to [Leon Juranic]"
   - mario_baslr: 致谢原始学术作者同时指出扩展

**显著缺失**: 未发现任何关于90天政策辩论的公开声明。他让工作本身说话。

---

## V. 协作模式

### ERNW时期（团队导向）
- 与 Florian Grunow 合作 IBM GPFS
- 与 Matthias Luft 合教 Hypervisor Workshop
- 通过机构博客发布

### P0时期（混合）
- dnsmasq: 6人大团队
- KVM逃逸: 明确独自工作 ("working as an individual")
- Spectre: 提供基础概念，大团队整合

### Asymmetric Research时期（创业者）
- 联合创始人角色，管理团队
- 博客文章更倾向机构口吻

---

## VI. 从行动/声明中提炼的价值观

1. **工具辅助而非替代人类判断**: 31C3 (2014) 明确声明，后编码入weggli设计

2. **攻击面经济学**: 持续选择"not enough researchers are looking"的领域

3. **实际影响优于新颖性**: dnsmasq影响一切从路由器到K8s, KVM是云基础

4. **桥接学术与工业**: 欣赏"the intersection between the academic program verification community and the IT security industry"

5. **技术深度优于广度**: 在会议回顾中持续称赞"very technical talks"

6. **关于局限性的务实诚实**: 文档记录什么不工作，不oversell结果

---

## VII. 研究兴趣演化轨迹

```
2013: 逆向工程工具、通用pentesting
2014: 路由器安全、shell globbing、实用hacking
2015: Xen hypervisor (XSA 105, 110, 123, 155), 硕士论文memory tracing
2016: 继续Xen, PV设备, Infiltrate/SyScan
2017: 加入Google; dnsmasq网络漏洞, BTB侧信道
2018: 容器/云安全 (Black Hat)
2019: Intel CSME (硬件安全, 固件)
2021: KVM AMD嵌套虚拟化逃逸
2022: TEE/SGX安全 (Black Hat "Mind The Gap"), 转型
2022+: Asymmetric Research -- 区块链/DeFi安全
2025-26: Solana生态安全审计, Breakpoint演讲
```

**核心模式: 跟踪每个时代的"最高价值安全边界"**

---

## VIII. 言行一致性评估

**一致的模式：**
- 声称工具应辅助人类 → 构建weggli正是这个哲学
- 选择"被忽视"的领域 → 实际研究Xen(2015)/KVM AMD(2021)/DeFi(2022+)
- 重视实际影响 → 研究持续影响真实生产系统
- 致谢他人工作 → 每篇相关文章都做到

**未发现矛盾**: 公开声明与可观察行为在10+年跨度上高度一致。

# Felix Wilhelm -- 著作与系统思考

## 1. 核心研究领域（按频率排序）

### 1.1 虚拟化安全与Hypervisor逃逸 (频率最高，贯穿整个职业生涯)
- Xen hypervisor漏洞研究 (2014-2016): XSA-105, XSA-110, XSA-123, XSA-155
- Hyper-V漏洞 (2013-2014): MS13-092
- KVM AMD嵌套虚拟化逃逸 (2021): CVE-2021-29657
- Spectre Variant 2 的 branch target injection 基础概念贡献

### 1.2 云安全与云认证绕过 (2017-2022)
- HashiCorp Vault AWS/GCP 认证绕过 (2020): CVE-2020-16250, CVE-2020-16251
- dnsmasq DNS/DHCP漏洞 (2017): CVE-2017-14491/14492/14493/14494/14495/14496, CVE-2017-13704
- AMD SEV/SNP 安全评估参与（可能）
- Intel TDX 安全评估参与（可能）

### 1.3 网络设备与防火墙攻击 (2014-2016)
- Palo Alto Networks PA-500/PAN-OS多个RCE (2016)
- Fritz!Box AVM路由器漏洞 (2014)

### 1.4 Java/JVM与内存安全语言漏洞 (2022)
- Java XSLT编译器整数截断 (CVE-2022-34169): "Gregor Samsa" -- XML签名验证中的RCE

### 1.5 企业存储与分布式系统 (2015)
- IBM GPFS多个关键漏洞: CVE-2015-0197/0198/0199

### 1.6 区块链/DeFi安全 (2022-present, Asymmetric Research)
- Solana p-token: 组合优化导致的漏洞 (2026)
- marginfi Flash Loan 漏洞 (2025)
- Relay 签名验证绕过 (2025)

### 1.7 安全产品漏洞 (2015-2016)
- FireEye MPS 漏洞

---

## 2. 重要文章/论文列表

### Project Zero 博客文章 (一手来源)

| 标题 | 年份 | 核心发现 |
|------|------|----------|
| "An EPYC escape: Case-study of a KVM breakout" | 2021-06 | CVE-2021-29657: KVM AMD嵌套虚拟化TOCTOU竞态→完整guest-to-host逃逸 |
| "Enter the Vault: Authentication Issues in HashiCorp Vault" | 2020-10 | CVE-2020-16250/16251: AWS STS XML解析宽容性+GCP JWT claim注入→认证绕过 |
| "Gregor Samsa: Exploiting Java's XML Signature Verification" | 2022-11 | CVE-2022-34169: Java XSLTC常量池整数截断→通过SAML签名验证实现RCE |

### Insinuator.net (ERNW研究博客) 文章 (一手来源)

| 标题 | 年份 | 核心发现 |
|------|------|----------|
| "Xen XSA 155: Double fetches in paravirtualized devices" | 2015-12 | 编译器优化导致的double-fetch漏洞类 |
| "General Pr0ken Filesystem -- Hacking IBM's GPFS" | 2015-04 | CVE-2015-0197/0198/0199: 格式化字符串+命令注入+任意内存写 |
| "Revisiting Xen's x86 Emulation: Xen XSA 123" | 2015-03 | CVE-2015-2151: 段前缀处理中的内存腐败 |
| "The Dangers of x86 Emulation: Xen XSA 110 and 105" | 2015-02 | 特权指令仿真中缺失权限检查+多核竞态 |
| "Revisiting an Old Friend: Shell Globbing" | 2014-12 | shell glob扩展作为root提权向量 |
| "Attacking Next-Generation Firewalls" | 2016-03 | PAN-OS: off-by-one命令注入+缓冲区溢出→RCE |
| "Exploiting Hyper-V: How We Discovered MS13-092" | 2014-01 | (与Matthias Luft合作) Hypercall处理中的DoS/潜在提权 |

### Asymmetric Research 博客 (一手来源, 2025-2026)

| 标题 | 年份 | 核心发现 |
|------|------|----------|
| "Solana p-token: Catching a Bug Before Mainnet" | 2026-04 | 组合优化在新功能交互中产生漏洞 |
| "Threat Contained: marginfi Flash Loan Vulnerability" | 2025-09 | 小改动在审计代码中引入关键漏洞 |
| "Wrong Offset: Bypassing Signature Verification in Relay" | 2025-09 | Solana签名验证程序易误用 |

### Google Security Blog 贡献

| 标题 | 年份 | 核心发现 |
|------|------|----------|
| "Behind the Masq: Yet more DNS, and DHCP, vulnerabilities" | 2017-10 | 7个dnsmasq漏洞(3个RCE + 1个信息泄露 + 3个DoS) |

### Spectre/Meltdown贡献

Felix Wilhelm的BTB research为Spectre Variant 2提供了基础概念。Jann Horn的disclosure中明确致谢："Felix Wilhelm's research based on this provided the basic idea behind variant 2."

---

## 3. 反复出现的方法论模式 (出现>=3次)

### 3.1 TOCTOU/Double-Fetch漏洞挖掘
- Xen XSA-155: 编译器优化导致的PV设备double-fetch
- KVM CVE-2021-29657: nested_svm_vmrun的VMCB double fetch
- Xen XSA-110/105: 多核竞态窗口中的指令替换
- 方法: hypervisor-based memory access tracing（受Bochspwn启发）

### 3.2 "从接口复杂性中发现逻辑漏洞"
- HashiCorp Vault: 外部系统交互中的认证逻辑缺陷
- Java XSLT: 内存安全语言中的整数截断→等效于内存腐败
- PAN-OS: next-gen功能扩大攻击面
- 总结: "tricky vulnerabilities like this often exist where developers have to interact with external systems and services"

### 3.3 多阶段利用链构建
- KVM逃逸: 竞态→MSR bitmap释放→IBS信息泄露→VMSAVE写原语→ROP→提权
- PAN-OS: off-by-one→UTF-8约束绕过→堆喷射→MIPS64 DEP绕过→root
- IBM GPFS: 格式化字符串→本地提权→远程命令注入→集群全部节点

### 3.4 Emulation/仿真层作为攻击面
- Xen XSA-110/105/123: x86仿真器中的权限检查缺失
- Java XSLTC中的JIT compiler作为意外攻击面
- "we can now provide arbitrary inputs to a fully-featured JIT compiler. Talk about an unexpected attack surface!"

### 3.5 硬件特性的攻击性利用
- AMD IBS: 用于物理地址到虚拟地址的信息泄露
- VMSAVE指令: 作为任意写原语
- Branch prediction逆向: 为Spectre V2提供基础概念

---

## 4. 自创术语/概念

### 4.1 "Xenpwn"
Xen paravirtualized设备double-fetch漏洞挖掘项目/工具。一手来源: Infiltrate 2016, Syscan 360.

### 4.2 "Weird machines still exist in memory safe languages"
在Gregor Samsa论文中明确提出：即使在Go/Java中，整数截断/逻辑缺陷仍可产生"feels very much like a memory corruption"的效果。一手来源: P0 blog 2022-11.

### 4.3 "Guest-to-host breakout without userspace components"
区别于依赖QEMU等用户空间漏洞的逃逸，纯hypervisor层面的VM逃逸。一手来源: P0 blog 2021-06.

### 4.4 "Make zeroday hard."
签名式标语，出现在P0博客文章结尾。既是研究目标声明也是行业呼吁。

---

## 5. 智识谱系线索

### 他引用/受影响的研究者

| 研究者/项目 | 关系 |
|-------------|------|
| Mateusz Jurczyk (j00ru) / Bochspwn | Xenpwn方法论直接受启发 |
| Dmitry Evtyushkin et al. | BTB研究→Felix发展Spectre V2概念 |
| Alex Ionescu | Hyper-V IPC研究 |
| Fabian Yamaguchi (joern) | "one of my favorite talks" (31C3) |
| Leon Juranic (DefenseCode) | Shell globbing研究中引用 |
| Franz Kafka | "Gregor Samsa"文章标题 |

### 合作者

| 合作者 | 合作项目 |
|---------|----------|
| Matthias Luft (ERNW) | Hyper-V MS13-092, hypervisor研讨会 |
| Florian Grunow (ERNW) | IBM GPFS |
| Fermin Serna, Gabriel Campana, Kevin Hamacher, Ron Bowes, Gynvael Coldwind | dnsmasq |
| Jann Horn (P0) | Spectre/Meltdown |

---

## 矛盾/未确认记录

1. **XSA-110归因**: Felix详细分析了XSA-110，但官方advisory发现者为"Jan Beulich of SUSE"
2. **CVE-2019-5736 (runC容器逃逸)**: 部分资料归因于Felix，但官方发现者为Adam Iwaniuk和Borys Poplawski
3. **AMD SEV/SNP与Intel TDX评估**: 无法确认其具体参与程度

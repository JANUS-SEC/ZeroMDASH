# Felix Wilhelm -- 职业时间线

## 教育

**Karlsruhe Institute of Technology (KIT), 德国**
- 学位: 硕士（计算机科学/IT安全方向）
- 论文: "Tracing Privileged Memory Accesses to Discover Software Vulnerabilities"
- 导师: Prof. Dr. Frank Bellosa (主), Prof. Dr. Wolfgang Karl (副)
- 时间: 约2013-2015（论文写作2015年5-11月）
- 论文产出xenpwn工具，直接导致XSA-155发现
- 可信度: 高（xenpwn GitHub README + KIT论文PDF元数据）

---

## 职业轨迹

### ~2013-2016/2017: ERNW GmbH, Heidelberg, 德国

**角色**: 安全研究员

**证据**:
- Insinuator博客首帖: 2013年7月 ("Reverse Engineering Tools Part 1: BinDiff")
- Palo Alto advisories (2016-02) 致谢 "Felix Wilhelm, ERNW Research"
- XSA-123 (2015-03) 致谢 "Felix Wilhelm of ERNW GmbH"
- XSA-155 (2015-12) 致谢 "Felix Wilhelm (ERNW Research, KIT / Operating Systems Group)"
- TROOPERS 2014-2016 演讲（TROOPERS是ERNW的会议）

**ERNW时期研究重点**:
- Hypervisor安全 (Xen, Hyper-V)
- 网络设备/防火墙攻击
- 逆向工程
- 企业存储系统 (IBM GPFS)
- 安全产品 (FireEye MPS)

---

### ~2017-2022: Google Project Zero

**加入时间**: 约2016年末/2017年初
- 证据: 最后ERNW博客帖2016-04, 首个Google credit 2017-10 (dnsmasq)
- Spectre博文(2018-01)引用Felix的BTB研究

**离开时间**: 约2022年
- 证据: 最后P0博客文章2022-11 (Gregor Samsa)
- Wikipedia列为"past member"
- Asymmetric Research bio暗示约2022年转型

**P0时期重要输出**:
- 2017-10: dnsmasq 7个漏洞（团队协作）
- 2017-18: Spectre V2基础概念贡献
- 2018: Black Hat "Attacking Cloud Hosted Container Management"
- 2019: Black Hat Intel CSME研究
- 2020-10: HashiCorp Vault认证绕过博客
- 2021-06: KVM AMD EPYC逃逸博客
- 2022: Black Hat "Mind The Gap" TEE安全
- 2022-11: Gregor Samsa Java XML签名博客

---

### 可能的过渡期: Jump Crypto (~2022)
- 来源: Asymmetric Research网站bio提及
- 时间和角色不确定
- 可信度: 中等

---

### 2022-present: Asymmetric Research, 联合创始人/CTO

**公司**: 区块链/DeFi安全研究公司
- 总部: 瑞士
- 声称保护 $5B+ 数字资产
- 专注Solana生态

**证据**:
- Asymmetric Research官网 (blog.asymmetric.re)
- 2025年Breakpoint（Solana会议）演讲
- 2025-2026年博客文章发布
- Twitter handle改为 @_fel1x

**Asymmetric时期公开输出**:
- 2025-09: "Threat Contained: marginfi Flash Loan Vulnerability"
- 2025-09: "Wrong Offset: Bypassing Signature Verification in Relay"
- 2026-04: "Solana p-token: Catching a Bug Before Mainnet"

---

## 关键漏洞发现时间线

### ERNW时期 (2013-2017)

| 日期 | ID | 目标 | 严重性 |
|------|-----|------|--------|
| 2014-02 | N/A | AVM Fritz!Box | HIGH |
| 2014 | MS13-092 | Hyper-V | HIGH |
| 2015-03 | CVE-2015-2151 / XSA-123 | Xen | CRITICAL |
| 2015-04 | CVE-2015-0197/0198/0199 | IBM GPFS | HIGH |
| 2015-12 | CVE-2015-8550 / XSA-155 | Xen PV | HIGH |
| 2016-02 | CVE-2016-3654/3655/3656/3657 | PAN-OS | CRITICAL |

### P0时期 (2017-2022)

| 日期 | ID | 目标 | 严重性 |
|------|-----|------|--------|
| 2017-10 | CVE-2017-14491~14496 | dnsmasq | CRITICAL |
| 2017-18 | Spectre V2 贡献 | CPU微架构 | CRITICAL |
| 2018 | CVE-2018-1111 | DHCP (DynoRoot) | HIGH |
| 2019 | Multiple | Intel CSME | HIGH |
| 2020-10 | CVE-2020-16250/16251 | HashiCorp Vault | HIGH |
| 2021-06 | CVE-2021-29657 | Linux KVM (AMD) | CRITICAL |
| 2022-11 | CVE-2022-34169 | Java XSLTC | HIGH |

---

## 会议演讲时间线

| 日期 | 会议 | 地点 | 标题 | 附属 |
|------|------|------|------|------|
| 2014-03 | TROOPERS 14 | Heidelberg | "Compromise-as-a-Service: Our PleAZURE" | ERNW |
| 2014 | PHDays | Moscow | Xen/virtualization | ERNW |
| 2015-03 | TROOPERS 15 | Heidelberg | GPFS + Hypervisor Workshop | ERNW |
| 2015-03 | SyScan | Singapore | "Exploiting Hypervisors" Workshop | ERNW |
| 2015 | 44CON | London | "Playing with Fire: Attacking FireEye MPS" | ERNW |
| 2016-03 | TROOPERS 16 | Heidelberg | "Attacking Next-Gen Firewalls" | ERNW |
| 2016-04 | Infiltrate | Miami | "Xenpwn" | ERNW |
| 2016-04 | SyScan 360 | Singapore | "Xenpwn" | ERNW |
| 2016 | Black Hat USA | Las Vegas | "Xenpwn: Breaking PV Devices" | ERNW |
| 2017-04 | HITB Amsterdam | Amsterdam | "Attacking Virtualization at the Source" | ERNW/P0过渡 |
| 2018 | Black Hat USA | Las Vegas | "Attacking Cloud Hosted Container Management" | Google P0 |
| 2019 | Black Hat USA | Las Vegas | Intel CSME研究 | Google P0 |
| 2022 | Black Hat USA | Las Vegas | "Mind The Gap: TEE Security" | Google |
| 2025 | Breakpoint | N/A | "Security Block: Asymmetric Research" | Asymmetric |

---

## 工具/开源项目

| 年份 | 项目 | 描述 | Stars |
|------|------|------|-------|
| 2015-2016 | xenpwn | 内存访问追踪工具（C++），检测double-fetch | 145 |
| 2016 | mario_baslr | BTB碰撞绕过hypervisor ASLR PoC（C） | 167 |
| 2021-2022 | weggli | C/C++语义搜索工具（Rust） | 2,500+ |

---

## 研究方向演化

1. **2013-2014**: 逆向工程、通用安全咨询、路由器漏洞
2. **2014-2016**: 深度专精hypervisor安全（Xen, Hyper-V）、x86仿真bugs、防火墙攻击
3. **2016-2017**: 过渡到CPU/硬件级攻击（BTB侧信道）
4. **2017-2021**: P0广泛范围：容器安全、dnsmasq网络、KVM虚拟化、Intel CSME
5. **2021-2022**: TEE安全（SGX/TDX）、Java/JVM漏洞
6. **2022-present**: 区块链/DeFi安全，Solana生态

**核心轨迹**: 跟踪每个时代的"最高价值安全边界"

---

## 最近12个月 (2025年5月-2026年5月)

- 2025-09: 发布 marginfi flash loan 漏洞博客
- 2025-09: 发布 Relay 签名验证绕过博客
- 2025: Breakpoint（Solana会议）演讲
- 2026-04: 发布 Solana p-token 漏洞博客
- 活跃于 Asymmetric Research，专注 Solana/DeFi 安全审计
- 可信度: 高（直接博客来源）

---

## 合作者网络

- **Matthias Luft** (ERNW): Hyper-V, hypervisor workshop
- **Florian Grunow** (ERNW): IBM GPFS
- **Jann Horn** (P0): Spectre/Meltdown
- **Gynvael Coldwind** (Google): dnsmasq
- **Fermin Serna, Gabriel Campana, Ron Bowes, Kevin Hamacher** (Google): dnsmasq

---

## 关键不确定性

1. 确切P0加入日期: 约2016末/2017初
2. 确切P0离开日期: 约2022年
3. Jump Crypto过渡期的确切时间和角色
4. Asymmetric Research联合创始人的其他成员
5. 2024-2025年间是否有未公开的重大研究

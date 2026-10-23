# Mark Brand — 著作与系统性技术文章

## 调研摘要

Mark Brand的公开技术产出几乎全部通过Google Project Zero博客发表。确认14篇文章（2015-2024），横跨4个主要研究领域。他没有学术论文、个人博客或newsletter。

---

## 一手来源：Project Zero博客文章

### Solo-authored (7篇)

#### 1. CVE-2015-0318: Flash PCRE Exploitation (Feb 2015)
- **来源**: googleprojectzero.blogspot.com (一手, HIGH confidence)
- **核心内容**: Flash中PCRE引擎的use-after-free漏洞利用
- **方法论**: 深入逆向分析 → 理解内存布局 → 构造exploit
- **关键论点**: 展示了通过正则表达式引擎获取代码执行的完整路径

#### 2. Virtually Unlimited Memory: Escaping the Chrome Sandbox (Apr 2019)
- **来源**: googleprojectzero.blogspot.com (一手, HIGH confidence)
- **核心内容**: Chrome Mojo IPC漏洞利用实现沙箱逃逸
- **方法论**: MojoJS binding审计 → IPC接口发现 → 跨进程exploit
- **关键论点**: 
  - "Look at things sideways" — 横向思维发现攻击面
  - ASLR bypass不需要信息泄露（创造性约束消除）
  - 进程重启是双刃剑（给攻击者重试机会）
- **自称**: "Exploit Technique Archaeologist"
- **标志性口号**: "Make zeroday hard."

#### 3. In-the-Wild: Android Exploits (Jan 2021)
- **来源**: googleprojectzero.blogspot.com (一手, HIGH confidence)
- **核心内容**: 分析真实野外Android exploit链
- **方法论**: 逆向工程已捕获的exploit样本，重建攻击链

#### 4-7. MTE As Implemented Series (Aug-Nov 2023, 4篇)
- **来源**: googleprojectzero.blogspot.com (一手, HIGH confidence)
- **标题**: 
  - Part 1: MTE As Implemented (基本评估)
  - Part 2: (深入分析)
  - Part 3: (攻击者视角)
  - Summary: First Handset with MTE on the Market (Nov 2023)
- **核心内容**: 对ARM Memory Tagging Extension的系统性安全评估
- **方法论**: 
  - 从攻击者视角评估防御措施
  - 建立Soft/Hard Mitigation vs Solution分类法
  - Known-tag-bypass vs Unknown-tag-bypass分类
  - Reusability/Fixability/Bug-subset评估维度
- **关键论点**:
  - 缓解措施分三层：soft mitigation（提高门槛）、hard mitigation（根本改变攻击模型）、solution（消除漏洞类）
  - MTE的有效性取决于具体实现细节，不是开启就安全
  - 攻击者有方法绕过标签（oracle攻击、暴力枚举等）

### Co-authored (6篇)

#### 8. Flash Exploit Mitigations (w/ Chris Evans, Jul 2015)
- **来源**: googleprojectzero.blogspot.com (一手, HIGH confidence)
- **核心内容**: 评估Flash exploit缓解措施的有效性

#### 9. Drawing Outside the Box: Precision Issues in Graphics Libraries (w/ Ivan Fratric, Jul 2018)
- **来源**: googleprojectzero.blogspot.com (一手, HIGH confidence)
- **核心内容**: 图形库中浮点精度问题导致的内存损坏
- **关键论点**: 数学精度问题可以系统性地导致安全漏洞

#### 10. Heap Feng Shader: Exploiting SwiftShader in Chrome (Oct 2018)
- **来源**: googleprojectzero.blogspot.com (一手, HIGH confidence)
- **核心内容**: Chrome GPU进程中SwiftShader组件的利用
- **方法论**: 堆布局操控 → 精确内存损坏 → 代码执行
- **关键论点**: GPU子系统是被忽视的攻击面

#### 11-12. Several Months in the Life of a Bug: Chrome Network Stack Exploit Parts 1&2 (w/ Sergei Glazunov, Feb 2020)
- **来源**: googleprojectzero.blogspot.com (一手, HIGH confidence)
- **核心内容**: Chrome网络栈base::Unretained use-after-free利用
- **关键论点**:
  - base::Unretained是系统性漏洞指标（反复出现的模式）
  - 概率性exploit在有重试机会时是可接受的
  - 详细记录失败路径和死胡同（诚实的研究叙事）

#### 13. Project Naptime: Evaluating Offensive Security of LLMs (w/ Glazunov, Jun 2024)
- **来源**: googleprojectzero.blogspot.com (一手, HIGH confidence)
- **核心内容**: 用LLM辅助漏洞研究的方法论框架
- **关键论点**: 
  - 提出AI辅助安全研究的五项原则
  - 人类研究员的方法论可以部分编码给AI

#### 14. From Naptime to Big Sleep (team of 16, Nov 2024)
- **来源**: googleprojectzero.blogspot.com (一手, HIGH confidence)
- **核心内容**: LLM首次发现真实软件(SQLite)中未知漏洞
- **关键论点**: AI辅助漏洞发现从概念验证到实际成果

### Contributed

#### 15. Hack The Galaxy - Samsung S6 Edge (CVE-2015-7888, Nov 2015)
- **来源**: googleprojectzero.blogspot.com (一手, HIGH confidence)
- **核心内容**: Samsung设备漏洞，作为团队项目的贡献

---

## 反复出现的核心论点 (≥3次 = 真信念)

### 1. base::Unretained作为系统性漏洞指标
- 出现于: Chrome网络栈(2020), Mojo IPC(2019), 多个bug报告
- 含义: 这不是偶发bug，是架构级问题

### 2. ASLR bypass不需要信息泄露
- 出现于: Chrome沙箱逃逸(2019), SwiftShader(2018), 网络栈(2020)
- 含义: 创造性地消除约束比正面突破更优雅

### 3. 缓解措施分类法: Soft/Hard/Solution
- 出现于: MTE系列(2023)全4篇, 隐含于早期Flash缓解评估(2015)
- 含义: 不是所有"安全改进"都等价，需要精确分级

### 4. 概率性exploit在可重试场景下可接受
- 出现于: SwiftShader heap spray(2018), Chrome网络栈(2020), MTE暴力枚举(2023)
- 含义: 可靠性不是二元的，要结合实际攻击模型评估

### 5. Servicification的双刃剑性质
- 出现于: Chrome沙箱逃逸(2019), 网络栈(2020), MTE评估(2023)
- 含义: 减少攻击原语但进程重启给攻击者重试机会

### 6. Variant analysis作为主要研究方法
- 出现于: Flash PCRE(2015), 图形精度(2018), MTE(2023)
- 含义: 一个bug暗示一类bug，系统性搜索比单点发现更有价值

### 7. "Make 0-day hard" 防御哲学
- 出现于: Chrome沙箱逃逸(2019), MTE系列(2023), Big Sleep(2024)
- 含义: 进攻研究的终极目标是让防御更强

---

## 自创术语和框架

| 术语/框架 | 首次出现 | 含义 |
|-----------|---------|------|
| "Exploit Technique Archaeologist" | 2019 | 自我身份定位——挖掘和复活旧exploit技术 |
| Soft/Hard Mitigation vs Solution | 2023 MTE | 缓解措施的三级分类 |
| Known-tag-bypass vs Unknown-tag-bypass | 2023 MTE | MTE攻击模型分类 |
| Reusability/Fixability/Bug-subset | 2023 MTE | 评估缓解措施的三维度 |
| Project Naptime Five Principles | 2024 | AI辅助安全研究的方法论框架 |
| "Look at things sideways" | 2019 | 横向思维发现非显而易见的攻击面 |

---

## 智识谱系线索

### 引用/致谢的研究者
- Chris Evans (P0同事, Flash研究合作)
- Ivan Fratric (P0同事, 图形研究合作)
- Sergei Glazunov (P0同事, Chrome exploit合作, 最频繁合作者)
- Natalie Silvanovich (P0同事, 被她引用)

### 研究方向影响
- 他的Chrome Mojo研究影响了后续多个研究者对IPC攻击面的关注
- MTE评估直接影响ARM和Google的硬件安全策略
- Naptime/Big Sleep项目开创了AI辅助安全研究的新方向

---

## 信息来源统计

- 一手来源（Brand本人著作）: 14篇博客文章 + 965+ Chromium commits
- 二手来源: 无（他几乎不被外部媒体报道）
- 信息缺口: 无学术论文、无个人博客、无书籍、无newsletter

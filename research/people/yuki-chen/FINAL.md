# Yuki Chen：漏洞研究成长分析

- 擅长领域：Windows 内核与 Hyper-V 漏洞
- 独立复核：pass · 77/100

## 成长阶段

- **2019 · Windows 内核 UAF 利用与 mitigations 绕过**：BFS 组织公开 CVE-2019-1215（ws2ifsl.sys UAF）exploit，目标 Windows 10 19H1 x64，演示绕过 kASLR、kCFG、SMEP；体现内核 UAF 利用与 mitigations 绕过的工程化能力；仓库以机构账号 bluefrostsecurity 署名，个人作者身份未证实。（置信度：low）
  - 证据：yc-tl-01
- **2020 · Android Binder 多阶段利用与跨平台扩展**：BFS 组织公开 CVE-2020-0041（Android Binder）利用，仓库分为 sandbox/ 与 lpe/ 两目录，对应沙箱逃逸与本地提权两条利用链；commit 历史含个人账号 yubiguel、ab 与机构账号 bluefrostsecurity（yc-r1-001），但 yubiguel 主页无可抓取线索绑定到 Yuki Chen、guhe120 或 BFS（yc-r1-002）；研究目标对象从 Windows 内核扩展到 Android 内核 IPC 子系统；仓库以机构账号署名为主，个人作者身份未证实。（置信度：low）
  - 证据：yuki-works-01, yc-r1-001, yc-r1-002
- **2021 · Hyper-V vmswitch 虚拟化漏洞**：BFS 组织公开 CVE-2021-28476（Hyper-V vmswitch）漏洞，位于处理 set OID 请求的 WPP 代码中，含攻击者控制指针解引用（读访问）与越界读；以 poc.patch 形式提供触发 PoC，指向 advisory bfs-sa-2021-001；两个提交均于 2021-06-02 由 bluefrostsecurity 创建（yc-tl-04）；研究目标对象从通用内核子系统迁移到虚拟化网络栈；仓库以机构账号署名，个人作者身份未证实。（置信度：low）
  - 证据：yuki-works-02, yc-tl-03, yc-tl-04, yc-dec-01

## 主要成长机制

### 以可复现 PoC 配合分阶段技术拆解的交付惯例

起点：Blue Frost Security GmbH（Frankfurt）以机构账号 bluefrostsecurity 在 GitHub 公开漏洞研究 PoC 仓库，配套 labs.bluefrostsecurity.de blog 与 advisory（yc-tl-05、yc-r1-003）；该交付环境为组织级资源，非个人可携带条件。

练习与反馈：2019 CVE-2019-1215 以 exploit 形式公开并演示绕过 kASLR/kCFG/SMEP（yc-tl-01）；2020 CVE-2020-0041 将单一漏洞拆为 sandbox/ 与 lpe/ 两目录，分别对应沙箱逃逸与本地提权（yuki-works-01），commit 历史含个人账号 yubiguel、ab 与机构账号 bluefrostsecurity（yc-r1-001）；2021 CVE-2021-28476 以 poc.patch 提供触发 PoC 并指向 bfs-sa-2021-001 advisory（yuki-works-02、yc-dec-01）。；仓库获社区 star/fork（CVE-2020-0041 257★/74 fork、CVE-2019-1215 149★/45 fork 等，yc-community-001、yc-r1-003），构成机构账号层面的公开反馈；CVE-2021-28476 README 指向 CVE-2021-28476 编号，MSRC 致谢与发现者署名未核实（yc-r1-004、yc-ext-003）。

能力与结果：BFS 组织层面形成从漏洞到分阶段利用链、可复现 PoC、advisory/blog 链接的稳定交付结构。；2019 CVE-2019-1215 仓库公开 ws2ifsl.sys UAF exploit，目标 Windows 10 19H1 x64（yc-tl-01）；2020 CVE-2020-0041 仓库分 sandbox/ 与 lpe/ 两目录，commit 历史含个人账号 yubiguel、ab（yuki-works-01、yc-r1-001）；CVE-2019-1215 仓库 README 引用 BFS blog 技术分析链接，blog 正文未抓取（yc-tl-02）；2021 CVE-2021-28476 仓库以 poc.patch 提供 PoC 并指向 bfs-sa-2021-001（yuki-works-02、yc-dec-01）

置信度：low；替代解释：该交付结构可由 BFS 组织级惯例与团队分工解释，无需归因于个人；commit 历史中个人账号 yubiguel、ab 出现，但 yubiguel 主页无可抓取线索绑定到 Yuki Chen、guhe120 或 Blue Frost Security（yc-r1-002），不能据此将交付惯例归因到 Yuki Chen 个人。

证据：yc-tl-01, yuki-works-01, yc-r1-001, yuki-works-02, yc-dec-01, yc-community-001, yc-r1-003, yc-tl-02, yc-r1-004, yc-ext-003

### 跨平台攻击面对象的横向迁移

起点：BFS 组织 GitHub 公开仓库覆盖多平台（Windows 内核、Android Binder、CPU 侧信道 Meltdown KVA shadow、Windows 驱动 EoP、Hyper-V vmswitch），组织显示名为 Blue Frost Security GmbH，注册地 Frankfurt（yc-tl-05、yc-r1-003、yuki-works-03）。

练习与反馈：2019 目标 Windows 内核 ws2ifsl.sys UAF（yc-tl-01）；2020 目标 Android Binder，拆分沙箱逃逸与本地提权（yuki-works-01）；2021 目标 Hyper-V vmswitch WPP/OID（yuki-works-02、yc-dec-01）；组织仓库横跨侧信道、Windows 提权、移动内核与虚拟化（yuki-works-03、yc-dec-02）。；各仓库独立获 star/fork（yc-community-001、yc-r1-003）；CVE-2021-28476 README 指向 CVE 编号与 advisory，MSRC 致谢与发现者署名未核实（yc-r1-004）。

能力与结果：BFS 组织层面研究目标对象跨子系统迁移，从通用内核子系统延伸到虚拟化网络栈。；2019 Windows 内核 ws2ifsl.sys UAF exploit（yc-tl-01）；2020 Android Binder 沙箱逃逸与本地提权双利用链（yuki-works-01）；2021 Hyper-V vmswitch WPP/OID 指针解引用与越界读（yuki-works-02、yc-dec-01）；组织仓库横跨侧信道、Windows 提权、移动内核与虚拟化（yuki-works-03、yc-r1-003）

置信度：low；替代解释：跨平台迁移可由 BFS 组织团队分工解释（不同成员负责不同平台），本轮及前轮定向补证未取得区分个人与团队分工的一手依据（yc-r1-002、yc-r1-003 负面结果），故 distinctive 不成立，仅 repeated 可支持；迁移的因果归因到 Yuki Chen 个人未证实。

证据：yc-tl-01, yuki-works-01, yuki-works-02, yc-dec-01, yuki-works-03, yc-dec-02, yc-r1-003, yc-community-001, yc-r1-004

## 可迁移与不可迁移

- 可迁移：范围限定：以下实践的可迁移性以 Yuki Chen 个人从属 Blue Frost Security 成立为前提；当前个人从属未在一手来源证实（yc-r1-002、yc-r1-003 负面结果），下列条目应理解为 BFS 组织级交付惯例的描述，个人可迁移性未证实。
- 可迁移：以最小可复现 PoC 配合分阶段目录组织仓库的交付格式：CVE-2020-0041 分 sandbox/ 与 lpe/ 两目录对应沙箱逃逸与本地提权（yuki-works-01），CVE-2021-28476 以 poc.patch 提供触发 PoC（yuki-works-02）。
- 可迁移：CVE-2019-1215、CVE-2021-28476 仓库 README 引用 BFS blog 或 advisory 链接，blog/advisory 正文未抓取（yc-tl-02、yc-r1-004）。
- 不可直接迁移：BFS-SA-YYYY-NNN advisory 编号体系依附 Blue Frost Security 机构（yc-dec-01、yc-tl-03），属组织资源，不随个人迁移。
- 不可直接迁移：Blue Frost Security GmbH（Frankfurt）组织账号 bluefrostsecurity、labs.bluefrostsecurity.de 站点与 GitHub org（181 followers）属组织资源（yc-tl-05、yc-r1-003），个人无法独立携带。
- 不可直接迁移：CVE-2020-0041 commit 历史中出现的个人账号 yubiguel、ab（yc-r1-001）不可作为个人条件转移：yubiguel 主页无可抓取绑定到 Yuki Chen/guhe120/BFS 的线索（yc-r1-002），同名与别名混淆风险未消解。

## 复核问题


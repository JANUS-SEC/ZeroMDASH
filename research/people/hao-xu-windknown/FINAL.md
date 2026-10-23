# Hao Xu (windknown)：漏洞研究成长分析

- 擅长领域：移动端与浏览器漏洞
- 独立复核：pass · 77/100

## 成长阶段

- **2020-08-06 · SEP 安全启动攻击研究的公开归档（单点观察）**：2020-08-06，GitHub 账号 windknown 的公开仓库 presentations 上传文件 Attack_Secure_Boot_of_SEP.pdf，commit 信息为 'Add files via upload'，仓库无 README 与说明文字。据此可观察到该账号持有者当时具备将 Apple SEP 安全启动攻击主题整理为演讲材料并对外公开归档的行为；是否对应实际公开演讲、研究深度，以及更早或更晚的能力状态均无线索级以上证据。本阶段仅记录该时点的可观察行为，不构成前后能力变化的证明。该 GitHub 账号持有者与自然人 Hao Xu 的同一性未经一手来源交叉核验，结论置信度低。（置信度：low）
  - 证据：windknown-deep-01, windknown-deep-02

## 主要成长机制

## 可迁移与不可迁移

- 可迁移：将研究成果整理为公开发表演讲材料并以 PDF 形式归档至个人公开仓库（已观察到 2020-08-06 一次实例，来源 windknown/presentations）；该做法本身可被其他研究者复现，但仅单次实例不足以证明其为该研究者的稳定习惯。
- 不可直接迁移：若 windknown 与 Pangu Team 或 Tencent Keen Lab 的隶属属实，则其所处团队提供的 iOS/WebKit 平台访问、固件样本、同伴评审与内部反馈网络属不可直接迁移的组织资源；该隶属未经一手来源核验，仅作推断条件列出。
- 不可直接迁移：Apple SEP 安全启动攻击研究（经 PDF 归档核验）通常依赖特定硬件、SEP 固件样本与平台文档的访问条件；具体访问途径与时段未核验，列为不可迁移条件。

## 复核问题

- 字段 tensions 第 4 项：将“一手抓取工具在本工作区整体不可用”改写为区分回合的口径——2026-09-26 证据采集回合 WebFetch 成功抓取 GitHub windknown/presentations（windknown-deep-01 verified）；本综合回合（2026-09-29）WebFetch 对所试域名均返回域安全验证失败，无法取得新的一手页面；避免“整体不可用”与同报告内 web_fetch 证据共存造成读者困惑。
- 字段 transferable_practices[0]：将“公开发表演讲材料”改写为“以 PDF 形式上传至名为 presentations 的公开仓库”（对应公开演讲本身为 inferred，未核验），如“将研究成果以 PDF 形式归档至个人公开仓库（已观察 2020-08-06 一次实例）；是否用于公开发表演讲未核验”，避免在未核验演讲事件前提下使用“公开发表演讲材料”表述。
- 字段 expertise[0]：将“Apple SEP”标注为推断（SEP 通常指代 Apple Secure Enclave Processor，但 verified 证据仅出现“SEP”），或将该限定词移入 non_transferable_conditions 的推断条件叙述，使 expertise 表述仅陈述核验证据直接支持的“SEP 安全启动攻击”。

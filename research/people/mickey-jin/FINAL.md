# Mickey Jin：漏洞研究成长分析

- 擅长领域：macOS/iOS 漏洞
- 独立复核：pass · 87/100

## 成长阶段

- **2024 年（一手议程页未列具体会议召开日期，仅记年份） · 公开会议演讲阶段：以 macOS 沙盒逃逸为主题在 POC 2024 发表演讲，披露攻击面挖掘成果（10+ 新漏洞）**：在 2024 年这一可核验时间点上，其研究能力已达到在 POC（Power of Community）会议公开披露 macOS 沙盒逃逸方向新漏洞的层级；议程页面将其标注为 independent security researcher，并以 handle @patch1t 与姓名 Mickey Jin 并列署名，一手确认身份映射。这是当前材料中唯一可标定的公开能力节点，不构成对其 2024 年前能力形成路径的可核验刻画。（置信度：medium）
  - 证据：mickeyjin-r2-01

## 主要成长机制

## 可迁移与不可迁移


## 复核问题

- expertise[0]（'macOS/iOS 漏洞研究'）：iOS 方向仅由本地输入 person_json 的 primary_focus 与 qualification 字段支撑，mickeyjin-r2-01 一手议程页仅确认 macOS 沙盒逃逸方向；原措辞'据本地输入 person_json 的 primary_focus 与 qualification 字段，并由 POC 2024 会议议程一手议程页确认其 2024 年研究主题为 macOS 沙盒逃逸'已区分层次，但'iOS'一词未由一手来源支撑。改写方向：将 iOS 方向限定为'据本地输入 person_json 标注，未由本回合一手来源证实'，或将 expertise[0] 收窄为'macOS 漏洞研究'，iOS 单独列为待核验方向。
- stages[0].stage（'披露攻击面挖掘成果（10+ 新漏洞）'）：'10+'取自 POC 2024 议程页演讲标题原文（mickeyjin-r2-01），属演讲者自述与议程页宣传性标题，非独立核验的漏洞数量。改写方向：将'披露攻击面挖掘成果（10+ 新漏洞）'改写为'议程页标题声称披露 10+ 新漏洞'或'以 10+ 新漏洞为标题在 POC 2024 发表演讲'，明确该数字为议程页标题自述而非独立核验计数。
- 在 biases 中补充知名度筛选偏差讨论：person_json 标注 rank=49 的来源未由一手来源核验，综合未讨论该排名可能引入的知名度筛选偏差；建议在 biases 中显式记录排名来源未核验及其对样本代表性的潜在影响。

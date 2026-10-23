# 未通过独立复核

已达到最大修订次数 4；本文件是审计草稿，不得进入跨人物比较。

# Thomas Roth (stacksmashing)：漏洞研究成长分析

- 擅长领域：芯片/固件/Apple 配件漏洞
- 独立复核：revise · 91/100

## 成长阶段

- **2010–2020 · 公开证据空白期**：最早可见的公开仓库 stacksmashing/yubicrack 创建于 2010-08-18，系自 nezza/yubicrack fork 而来（C 语言，Yubikey 访问码暴力破解），与硬件令牌方向相关联，但不足以证明研究对象发起该方向。2010 至 2021 年站点建立之间存在公开证据空白，无法据现有材料还原其间学习路径与研究主线。该阶段不作为具备已抓取来源支撑的能力阶段呈现原创因果。（置信度：low）
  - 证据：tr-r1-evid-01, tr-r1-evid-02
- **2021 · 对外身份确立与低成本 MCU 工具链起步**：stacksmashing.net 站点建立并固定署名 Thomas Roth（Esslingen am Neckar, Germany），自述方向为 IT-security 与 hardware hacking 视频，形成以 YouTube 与开源仓库为主的对外发表渠道。同期围绕 Raspberry Pi Pico（RP2040）起步构建可分发的硬件攻击前端：pico-serprog 作为 flashrom/serprog 兼容固件于 2021-04-03 创建（GPL-3.0，fork=false 原创），picoemp-fw 作为 Colin O'Flynn PicoEMP 电磁脉冲故障注入硬件的基础控制固件于 2021-12-26 创建（fork=false）。研究方法转向以低成本微控制器作为通用硬件攻击/烧录前端，形成可复用工具集合的雏形。（置信度：medium）
  - 证据：tl-identity-site, ext-001, dec-06, tr-r1-evid-03, tr-r2-evid-05
- **2022–2023 · Apple USB-C 攻击面与自研硬件+固件+主机工具生态**：研究重心转向 Apple 设备 USB-C/USB-PD 总线的硬件级探索。tamarin-c 于 2023-12-28 发布（dec-01 锚定），README 表明其在 USB-C SBU 引脚上对 Apple 设备实现 UART/SWD/JTAG/DCSD/内部总线映射/DFU 入口，并在 iPhone 15 上观测 ACE SPMI 协议，基于 Marc Zyngier 的 Central Scrutinizer 与 AsahiLinux vdmtool。tamarin-firmware 最早提交为 2022-08-13 'Public release'，早于 tamarin-c 约 16 个月，README 互相引用确认为配套 Tamarin Cable 探针固件（运行于 Pico，提供 DCSD 与 JTAG 模式与 iPhone 交互）；tamarin-c-hw 最早提交为 2023-12-28 'Initial public release'，与 tamarin-c 同日，README 表明为 Tamarin-C 的 PCB 硬件设计并基于 Central Scrutinizer，license CC BY-NC，提及 Aisler 为 37C3 制作 PCB。三者 README 互相引用构成配套关系，但创建日期仅经提交历史间接推断，GitHub API 元数据因 403 未一手核验。工具建设与公开发表形成稳定模式（GPLv3 开源）。macvdmtool 创建于 2023-09-23，为 fork 自 AsahiLinux/macvdmtool 的 Apple Silicon 间串口控制台与远程重启工具，非研究对象自研，未纳入该自研生态列举。（置信度：medium）
  - 证据：dec-01, roth-works-05, tl-tamarin-series-2023, tr-r2-evid-04, ext-002, ext-003, stacksmashing-community-github-org-tools, tr-r3-evid-07, tr-r3-evid-08
- **2024 · 平台信任根被动嗅探与主动干预工具维护**：目标从 Apple 配件扩展到平台固件信任根。pico-tpmsniffer 基于 Pico 对 Lenovo 调试卡连接器上的 LPC 总线 TPM 流量进行被动嗅探，README 标注当前仅支持 LPC 而非 SPI TPM，记录了工具的适用范围边界（依据 roth-works-06）。同期围绕 RP2040/Pico 与 STM32F4 维护可分发的攻击/嗅探工具集合：pico-serprog 于 2024-04-30 仍有 push 活动（创建于 2021-04-03，非 2024 新建，依据 tr-r1-evid-03）；stm32f4_password_glitch 创建于 2024-05-30，README 标题为 'STM32F4 Playground'，正文为项目脚手架，README 未直接声称密码故障注入，仅文件夹名 1_password_check_simple/2_password_check_countermeasure 提示与密码检查相关（依据 tr-r2-evid-06）。（置信度：medium）
  - 证据：roth-works-06, tr-r2-evid-06, tl-pico-tools-2024, tr-r1-evid-03
- **2025–2026 · 既有工具链 fork 维护与固件分析延伸**：openocd-tamarin 于 2025-05-24 更新，对 Microsoft 的 OpenOCD fork 再 fork，加入 Tamarin 支持并提供预编译二进制，降低他人复现门槛。binwalk Rust fork 于 2026-01-06 更新，研究范围扩展到用 Rust 重写固件分析工具链；stm32f4_playground 于 2026-08-02 更新，持续维护 STM32F4 实验。研究链从硬件接口层（USB-C、SPI、LPC）向固件静态分析层延伸，关注工具栈现代化。（置信度：medium）
  - 证据：tl-openocd-tamarin-2025, dec-05, tl-recent-2026, stacksmashing-community-binwalk-fork

## 主要成长机制

### 低成本微控制器作为通用硬件攻击前端

起点：2021 年前后 RP2040/Pico 等低成本微控制器普及，研究对象已建立对外公开身份（stacksmashing.net 站点 2021 建立）并以视频与开源仓库为主要输出渠道。

练习与反馈：跨 2021–2026 反复围绕 RP2040/Pico 构建面向不同总线与目标的工具：pico-serprog（SPI flash 烧录，2021-04-03）、picoemp-fw（电磁脉冲故障注入控制，2021-12-26）、pico-tpmsniffer（LPC 总线 TPM 嗅探，2024-02-03）、stm32f4_password_glitch（STM32F4 脚手架，2024-05-30）。homebrew-tap 形成安装渠道，pico-serprog、picoemp-fw 均为 fork=false 原创。；GitHub star/fork 计数（pico-tpmsniffer 约 697 stars/101 forks、tamarin-firmware 约 499 stars/62 forks、pico-serprog 约 295 stars/63 forks）反映关注度与流行度而非经核实的有效能力反馈，可能与维护动力相关，但不构成已核实的能力反馈回路；fork 与开放 PR 数量显示外部贡献者在其工具基础上参与，但维护者修订与能力获得之间的因果未经核实。

能力与结果：能够在廉价微控制器上构建面向不同总线与目标的可分发硬件攻击前端，并形成可复用、可组合的实验基础设施（glitchlib 与 LPCClocklessAnalyzer 等库与信号分析插件提示此方向，依据 roth-works-07，该条 verified_in_run=false 为线索）。；pico-serprog：flashrom/serprog 兼容烧录固件，2021-04-03 原创（tr-r1-evid-03）；picoemp-fw：Colin O'Flynn PicoEMP 电磁脉冲故障注入硬件基础固件，2021-12-26 原创（tr-r2-evid-05）；pico-tpmsniffer：LPC 总线 TPM 被动嗅探，README 明确仅支持 LPC（roth-works-06）；stm32f4_password_glitch：STM32F4 Playground 脚手架，README 未直接声称故障注入（tr-r2-evid-06）

置信度：medium；替代解释：廉价 MCU 工具链的反复出现可能反映硬件攻击门槛整体下降的外部条件（RP2040/Pico 的可得性与 Colin O'Flynn PicoEMP 等参考设计的公开）而非个人特有的能力选择；在缺乏研究对象本人方法自述或同行对其个人方法选择的具名评价时，难以将外部条件普遍可得与个人选择该模式的边界作独立区分。

证据：tr-r1-evid-03, tr-r2-evid-05, roth-works-06, tr-r2-evid-06, tl-pico-tools-2024, stacksmashing-community-github-feedback

### 围绕单一主题自研硬件+固件+主机工具生态

起点：2022 年前后研究对象具备 USB-C/USB-PD、VDM、SPMI 等深层协议知识基础，并能复用 Marc Zyngier 的 Central Scrutinizer 与 AsahiLinux vdmtool 等前人公开成果。

练习与反馈：围绕 Apple USB-C 攻击面分仓库构建自研生态：tamarin-firmware（最早提交 2022-08-13，Tamarin Cable 探针固件，运行于 Pico）、tamarin-c（2023-12-28，主机工具，USB-C SBU 上多协议入口）、tamarin-c-hw（最早提交 2023-12-28，PCB 硬件设计）。三者 README 互相引用构成配套关系。；GitHub star/fork 计数与开放 PR 反映关注度与外部贡献者参与，但不构成经核实的能力反馈回路；37C3 会议分发（Aisler 赞助 100 块 PCB）显示工具在硬件安全社群获得分发渠道，属可观察的社群接触而非经核实的能力评价。

能力与结果：能够围绕单一攻击主题分别产出固件、主机工具与 PCB 硬件设计，并以 README 互引与开源 license 形成可被他人复现的配套项目，而非孤立单点工具。；tamarin-c：USB-C SBU 上 UART/SWD/JTAG/DCSD/内部总线/DFU 入口，iPhone 15 ACE SPMI，2023-12-28（dec-01、roth-works-05）；tamarin-firmware：Tamarin Cable 探针固件，最早提交 2022-08-13（tr-r3-evid-07）；tamarin-c-hw：Tamarin-C PCB 硬件设计，CC BY-NC，37C3 分发，最早提交 2023-12-28（tr-r3-evid-08）；macvdmtool：fork 自 AsahiLinux/macvdmtool 的 Apple Silicon 间串口控制台与远程重启工具，2023-09-23，非自研，不纳入自研生态列举（tr-r2-evid-04）

置信度：medium；替代解释：tamarin 生态的可行性部分依赖前人公开成果（Central Scrutinizer、AsahiLinux vdmtool、T8012 团队发现）与社群分发渠道（Aisler 赞助 PCB、37C3 会议），其自研部分与复用部分的边界未经提交级贡献者角色核实；tamarin-firmware 提交历史含 nezza、tihmstar、LinusHenge、lukaskuzmiak、WhitetailAni 等多名贡献者，研究对象个人独立产出比例未经核实。

证据：dec-01, roth-works-05, tl-tamarin-series-2023, tl-openocd-tamarin-2025, stacksmashing-community-github-feedback, tr-r3-evid-07, tr-r3-evid-08, tr-r2-evid-04

### 既有开源工具链之上的 fork 与增量维护

起点：研究对象具备对 OpenOCD、binwalk 等既有开源工具链的理解，并能通过 fork 叠加自研硬件支持。

练习与反馈：对既有开源工具做 fork 并叠加自研硬件支持或现代化重写：openocd-tamarin fork 自 Microsoft OpenOCD 分支并加入 Tamarin 支持与预编译二进制（2025-05-24 更新）；binwalk fork 为 Rust 实现（2026-01-06 更新）；macvdmtool fork 自 AsahiLinux/macvdmtool（2023-09-23）。同时区分 fork（OpenOCD、binwalk）与原创兼容固件（pico-serprog fork=false，为 flashrom/serprog 兼容的原创固件）。；GitHub fork/star 计数反映关注度而非经核实的能力反馈；fork 与增量维护的对外发布以预编译二进制与 homebrew-tap 降低复现门槛，属分发习惯而非能力评价。

能力与结果：能够在既有开源工具链之上做 fork 与增量维护，并通过预编译二进制与包管理渠道降低他人复现门槛，而非孤立开发。；openocd-tamarin：fork Microsoft OpenOCD 并加入 Tamarin 支持与预编译二进制（tl-openocd-tamarin-2025）；binwalk：ReFirmLabs/binwalk Rust fork，Firmware Analysis Tool，2026-01-06 更新（dec-05、stacksmashing-community-binwalk-fork）；macvdmtool：fork 自 AsahiLinux/macvdmtool，Apple Silicon 间串口控制台与远程重启，2023-09-23，非自研（tr-r2-evid-04）；pico-serprog：flashrom/serprog 兼容原创固件，fork=false，2021-04-03（tr-r1-evid-03）

置信度：medium；替代解释：fork 与增量维护的反复出现可能反映开源硬件工具生态的成熟（OpenOCD、binwalk 等具备可 fork 的基础）与 Rust 工具栈现代化的行业趋势，而非个人特有的能力选择；macvdmtool 与 openocd-tamarin 均建立在他人（AsahiLinux、Microsoft）分支之上，研究对象个人增量贡献的独立分量未经提交级核实。

证据：tr-r1-evid-01, tr-r2-evid-04, tl-openocd-tamarin-2025, dec-05, stacksmashing-community-binwalk-fork, tr-r1-evid-03

### 被动嗅探之外的主动故障干预

起点：研究对象已具备被动总线嗅探（pico-tpmsniffer）与低成本 MCU 工具构建能力，并接触 Colin O'Flynn 的 PicoEMP 电磁脉冲故障注入硬件设计。

练习与反馈：在被动嗅探之外构建主动故障干预工具：picoemp-fw 作为 Colin O'Flynn PicoEMP 电磁脉冲故障注入硬件的基础控制固件，支持 Manual arming + pulsing、Serial interface、Automatic disarm、Fast-trigger via GPIO0（2021-12-26 创建，fork=false）。stm32f4_password_glitch 创建于 2024-05-30，README 标题为 'STM32F4 Playground' 脚手架，未直接声称密码故障注入，仅文件夹名提示与密码检查相关。；GitHub star/fork 计数（picoemp-fw 约 10 stars、stm32f4_password_glitch 约 5 stars）反映关注度而非经核实的能力反馈；无具名同行对其故障干预方法的有效性评价。

能力与结果：能够为电磁脉冲故障注入硬件编写基础控制固件并暴露 arming/pulsing/fast-trigger 接口，形成主动干预的实验前端；但 stm32f4 方向的密码故障注入定性仅能降为文件夹名提示，未从一手 README 核实。；picoemp-fw：PicoEMP 电磁脉冲故障注入硬件基础固件，2021-12-26 原创（tr-r2-evid-05）；stm32f4_password_glitch：STM32F4 Playground 脚手架，README 未直接声称故障注入（tr-r2-evid-06）

置信度：low；替代解释：picoemp-fw 建立在 Colin O'Flynn 公开的 PicoEMP 硬件设计之上，研究对象的增量贡献为控制固件而非硬件设计本身；stm32f4_password_glitch 因 README 未提供解释性文本，其作为主动故障干预练习的定性缺乏一手支撑，可能仅为 STM32F4 通用项目脚手架。

证据：tr-r2-evid-05, tr-r2-evid-06

## 可迁移与不可迁移

- 可迁移：以低成本微控制器（RP2040/Pico）作为通用硬件攻击/烧录前端，围绕同一平台构建可分发的工具集合（sniffer + serprog + glitch + USB-C），并通过 homebrew-tap 形成安装渠道。
- 可迁移：围绕单一攻击主题分仓库构建自研硬件+固件+主机工具生态，并以 README 互引与开源 license 形成可被他人复现的配套项目。
- 可迁移：对既有开源工具链（OpenOCD、binwalk）做 fork 并叠加自研硬件支持或现代化重写，通过预编译二进制降低他人复现门槛，减少对既有开源工具的重复实现。
- 可迁移：README 明确记录工具的适用范围边界（如 pico-tpmsniffer 标注当前仅支持 LPC 而非 SPI TPM），区分 fork 与原创兼容固件（pico-serprog fork=false）。
- 不可直接迁移：研究对象复用了 Marc Zyngier 的 Central Scrutinizer、AsahiLinux vdmtool、T8012 团队发现、Colin O'Flynn 的 PicoEMP 硬件设计等前人公开成果，自研部分与复用部分的边界未经提交级贡献者角色核实；tamarin-firmware 提交历史含 nezza、tihmstar、LinusHenge、lukaskuzmiak、WhitetailAni 等多名贡献者，研究对象个人独立产出比例不可迁移。
- 不可直接迁移：37C3 会议分发（Aisler 赞助 100 块 PCB）与 Black Hat/POC/Hardwear.io/DSTL 会议演讲机会属个人特有社群接触条件，不可迁移；且后者的会议演讲事实未一手核验。
- 不可直接迁移：stacksmashing.net 站点、YouTube 频道（@stacksmashing）与 Twitter/X（@ghidraninja / @stacksmashing）的对外发表渠道与观众基础属个人特有积累，star/fork 计数与媒体报道反映的关注度不可等同于可迁移的能力获得。
- 不可直接迁移：2010–2020 间的学习路径、教育背景、雇主与团队归属无公开一手资料，研究对象在该时期的个人特有条件不可迁移。

## 复核问题

- 结论引用缺失或已作废：['tl-identity-site', 'ext-001', 'dec-06', 'tr-r1-evid-03', 'tr-r2-evid-05']
- 结论引用缺失或已作废：['dec-01', 'roth-works-05', 'tl-tamarin-series-2023', 'tr-r2-evid-04', 'ext-002', 'ext-003', 'stacksmashing-community-github-org-tools', 'tr-r3-evid-07', 'tr-r3-evid-08']
- 结论引用缺失或已作废：['tl-openocd-tamarin-2025', 'dec-05', 'tl-recent-2026', 'stacksmashing-community-binwalk-fork']
- 结论引用缺失或已作废：['dec-01', 'roth-works-05', 'tl-tamarin-series-2023', 'tl-openocd-tamarin-2025', 'stacksmashing-community-github-feedback', 'tr-r3-evid-07', 'tr-r3-evid-08', 'tr-r2-evid-04']
- 结论引用缺失或已作废：['tr-r1-evid-01', 'tr-r2-evid-04', 'tl-openocd-tamarin-2025', 'dec-05', 'stacksmashing-community-binwalk-fork', 'tr-r1-evid-03']

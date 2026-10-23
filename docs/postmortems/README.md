# Postmortems / 复盘报告

本目录存放 ZeroMDASH 扫描运行的事后复盘报告：漏报（false negative）、误报
（false positive）、流程失效等事件的根因分析与改进结论。

## 命名约定

```
YYYY-MM-DD-<target>-<short-slug>.md
```

日期为复盘完成日期。每份报告至少包含：事件概述、事实链（含可复核的证据
引用）、根因分析、责任定位、改进结论、残余风险。

## 索引

| 日期 | 报告 | 类型 |
|---|---|---|
| 2026-10-15 | [KVM SVM TLB flush 丢失漏洞漏报](2026-10-15-kvm-svm-tlb-flush-lost-on-failed-vmrun.md) | 漏报 |

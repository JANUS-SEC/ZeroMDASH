# Rory McNamara — 时间线维度

> 调研日期: 2026-07-28
> 调研对象: Rory McNamara(Snyk Security Labs,Staff Security Researcher;GitHub `rmcnamara-snyk`)
> 本文聚焦:可核实的「时间线维度」——职业生涯与漏洞发现的精确日期年表。
> 全部日期均来自 GitHub API / github.com 公开档案 / NVD API / Wayback Machine 快照 / oss-security 邮件列表,绝不编造。

## 调研方法

### 数据源(按可信度从高到低)

1. **GitHub Advisory REST API**(`api.github.com/advisories/<GHSA>`)——取 `published_at`(全局 Advisory Database 发布日)、`updated_at`、`severity`、`cvss`、`vulnerabilities`(受影响/补丁版本范围)。**这是任务指定的 GHSA published_at 一手来源**。9 条全部逐条 fetch。`created_at` 字段全部返回 `None`(私有创建日 API 不公开,见「信息不足之处」)。
2. **GitHub 用户 REST API**(`api.github.com/users/rmcnamara-snyk`、`/users/rmcnamara-snyk/events/public`)——`created_at`、`updated_at`、`bio`、`company`、`public_repos`、`followers`、公开事件流。逐项核实。
3. **NVD REST API**(`services.nvd.nist.gov/rest/json/cves/2.0?cveId=...`)——`published`(NVD 发布日)、`lastModified`、`vulnStatus`、`references`。8 个 CVE 逐条核实(buildah 无独立 CVE,与 podman 共享 CVE-2024-1753)。
4. **github.com 公开档案页 HTML**(release tag 页 / commit 页 / repo-level security advisory 页)——经 curl 抓取 HTML,提取 `<relative-time datetime="...">` 与 commit JSON 的 `committedDate`/`authoredDate`。用于上游修复 release 时间、fix commit 时间、**repo-level advisory 发布时间**(注意:这与全局 API published_at 是两个不同日期,见下文「三种发布日」)。
5. **Wayback Machine CDX API + 快照正文**(`web.archive.org`,经 curl)——核验 Snyk 博客、openwall oss-security 的归档快照;直接 curl 抓取快照正文提取 `publishDate` JSON-LD 字段与邮件头。
6. **任务已核实上下文**(直接采用):9 条 GHSA credit 全部 `rory_credited=True`;Leaky Vessels 由 Aleksa Sarai(cyphar,SUSE)协调;Rory 不在 runc MAINTAINERS。

### 关键方法学说明:每个 GHSA 存在「三种发布日」(必须区分)

经多源交叉核实,每条 GHSA 同时存在三个不同的「发布」时间戳,它们通常不同:

| 日期类型 | 来源 | 含义 |
|----------|------|------|
| **repo-level advisory 发布日** | `github.com/<org>/<repo>/security/advisories/<GHSA>` HTML 的 `<relative-time>`(标签 published) | 上游仓库维护者在其 repo 发布 security advisory 的时间。通常最早。 |
| **全局 Advisory Database published_at** | `api.github.com/advisories/<GHSA>` 的 `published_at` | GitHub 全局 Advisory Database 收录/发布该条目的时间。通常晚于 repo-level(几分钟到几天)。**任务指定采用此值。** |
| **NVD published** | `services.nvd.nist.gov` 的 `published` | NVD 发布 CVE 记录的时间。可能早于、同于、或晚于上述两者(snapd 特例:NVD 早 7.5 个月)。 |

下文「精确日期年表」以**全局 API published_at** 为 GHSA 的主发布日(任务指定),同时列出 repo-level 与 NVD 作为对照列。`created_at`(私有创建日)API 返回 `None`,不可公开核实。

### 可信度分级

- **一手**:GitHub/NVD API 结构化字段、github.com 档案页 `relative-time`、Wayback 快照正文 JSON-LD、oss-security 邮件头。
- **二手**:他人转述。
- **推测**:基于账号创建日等推断,明确标注。

### 环境限制记录

- GitHub REST API 在调研前段因 IP 共享触发 unauthenticated 速率限制(60/小时,`remaining: 0`),已通过后台轮询任务等待重置(1785218379 = 2026-07-28T05:59:39Z)后批量复核,全部字段已于 06:00Z 复核完成。
- WebSearch 工具在本环境不可用(返回伪造内容或拒绝);WebFetch 对 snyk.io / web.archive.org URL 返回 404。所有抓取均经 curl 直连允许域名(api.github.com、github.com、raw.githubusercontent.com、services.nvd.nist.gov、web.archive.org)。
- LinkedIn 需登录且非允许域名。openwall.com 非允许域名,其 oss-security 内容经 Wayback 快照间接核实。

## 精确日期年表(按时间正序)

| 日期(UTC,除注明) | 事件 | 来源 URL | 可信度 |
|------|------|----------|--------|
| 2011-09-10 | 个人 GitHub 账号 `psychomario` 创建(Name="Rory McNamara") | https://api.github.com/users/psychomario(前序调研 API;本批未重测) | 一手(经前序调研) |
| **2023-07-09T20:10:00Z** | **Snyk 企业 GitHub 账号 `rmcnamara-snyk` 创建**(bio="Staff Security Researcher",company="Snyk",public_repos=0,followers=8)——推断为加入 Snyk 的时间 | https://api.github.com/users/rmcnamara-snyk(`created_at`,本批 API 复核) | 一手 + 推测(入职日非直接就业证明) |
| 2024-01-30T17:58:48Z | Rory 的 Snyk 作者头像 `rory-mcnamara.jpg` 上传到 Cloudinary | Wayback 快照 https://web.archive.org/web/20240208015227/https://snyk.io/blog/leaky-vessels-container-vuln-deep-dive/(Cloudinary asset JSON) | 一手 |
| 2024-01-30T19:00:17.809Z | Rory 的 Snyk Contentful 作者档案(slug=`rory-mcnamara`,fullName="Rory McNamara")创建——Leaky Vessels 公告前 1 天 | 同上 Wayback 快照(Contentful `contentPerson` entry `createdAt`) | 一手 |
| 2024-01-31T20:06:08Z | **runc v1.1.12 release 发布**(Leaky Vessels 主体修复,"Now you're thinking with Portals™!") | https://github.com/opencontainers/runc/releases/tag/v1.1.12(relative-time) | 一手 |
| 2024-01-31T20:07:41Z | runc **repo-level advisory** 发布(GHSA-xr7r-f8xq-vfvv)——晚于 runc release 1 分 33 秒 | https://github.com/opencontainers/runc/security/advisories/GHSA-xr7r-f8xq-vfvv | 一手 |
| 2024-01-31T20:44:09Z | **buildkit v0.12.5 release 发布**(Leaky Vessels buildkit 侧修复) | https://github.com/moby/buildkit/releases/tag/v0.12.5(relative-time) | 一手 |
| 2024-01-31T20:44:30Z | Snyk Leaky Vessels 公告博客 URL `leaky-vessels-container-breakout-vulnerabilities-jan-2024` 首次被 Wayback 抓取(HTTP 308 永久重定向) | web.archive.org CDX(timestamp 20240131204430) | 一手 |
| 2024-01-31T20:45:51Z | buildkit **repo-level advisory** 发布 CVE-2024-23653(GHSA-wr6v-9f75-vh2g)——晚于 buildkit release 1 分 42 秒 | https://github.com/moby/buildkit/security/advisories/GHSA-wr6v-9f75-vh2g | 一手 |
| 2024-01-31T20:46:07Z | buildkit repo-level advisory 发布 CVE-2024-23652(GHSA-4v98-7qmw-rqr8) | https://github.com/moby/buildkit/security/advisories/GHSA-4v98-7qmw-rqr8 | 一手 |
| 2024-01-31T20:46:29Z | buildkit repo-level advisory 发布 CVE-2024-23651(GHSA-m3r6-h7wv-7xxv) | https://github.com/moby/buildkit/security/advisories/GHSA-m3r6-h7wv-7xxv | 一手 |
| 2024-01-31T22:15:53.780Z | NVD 发布 CVE-2024-21626 | https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2024-21626 | 一手 |
| 2024-01-31T22:15:54.183Z | NVD 发布 CVE-2024-23651 | 同上 NVD API(cveId=CVE-2024-23651) | 一手 |
| 2024-01-31T22:15:54.377Z | NVD 发布 CVE-2024-23652 | 同上(cveId=CVE-2024-23652) | 一手 |
| 2024-01-31T22:15:54.600Z | NVD 发布 CVE-2024-23653 | 同上(cveId=CVE-2024-23653) | 一手 |
| **2024-01-31T22:43:20Z** | **GHSA-wr6v-9f75-vh2g 全局 published_at**(buildkit 23653,Critical,CVSS 9.8)——晚于 repo-level advisory 约 1h57m | https://api.github.com/advisories/GHSA-wr6v-9f75-vh2g | 一手 |
| **2024-01-31T22:43:26Z** | **GHSA-4v98-7qmw-rqr8 全局 published_at**(buildkit 23652,Critical,CVSS 10.0) | https://api.github.com/advisories/GHSA-4v98-7qmw-rqr8 | 一手 |
| **2024-01-31T22:43:32Z** | **GHSA-m3r6-h7wv-7xxv 全局 published_at**(buildkit 23651,High,CVSS 8.7) | https://api.github.com/advisories/GHSA-m3r6-h7wv-7xxv | 一手 |
| **2024-01-31T22:44:08Z** | **GHSA-xr7r-f8xq-vfvv 全局 published_at**(runc 21626,High,CVSS 8.6) | https://api.github.com/advisories/GHSA-xr7r-f8xq-vfvv | 一手 |
| ~2024-01-31T20:33Z(原帖)/ 2024-02-01T00:49:52Z(回帖) | **oss-security:runc CVE-2024-21626 披露**。Aleksa Sarai(cyphar,SUSE)原始公告(Date 头:`Feb 01, 2024 07:33:01AM +1100` = Jan 31 20:33 UTC);Solar Designer 回帖(Date 头:`Thu, 1 Feb 2024 01:49:52 +0100` = 00:49 UTC) | http://www.openwall.com/lists/oss-security/2024/02/01/1(Wayback 快照正文邮件头) | 一手 |
| 2024-02-02T11:27:36Z | oss-security 后续帖:Aleksa Sarai 补充(`Fri, 2 Feb 2024 22:27:36 +1100`,提到 openat2(2) 的讽刺) | http://www.openwall.com/lists/oss-security/2024/02/02/3(Wayback 快照) | 一手 |
| 2024-02-06T16:00:00Z(`2024-02-06T11:00-05:00`) | **Snyk Leaky Vessels deep-dive 博客发布**《Leaky Vessels deep dive: Escaping from Docker one syscall at a time》,作者署名 **Rory McNamara**(JSON-LD `author` + "Written by" 头像) | https://snyk.io/blog/leaky-vessels-container-vuln-deep-dive/(Wayback 快照 20240208015227,`publishDate` JSON-LD) | 一手 |
| 2024-03-18T14:15:18Z | podman **repo-level advisory** 发布(GHSA-874v-pj72-92f3,CVE-2024-1753) | https://github.com/containers/podman/security/advisories/GHSA-874v-pj72-92f3 | 一手 |
| 2024-03-18T14:15:51Z | buildah **repo-level advisory** 发布(GHSA-pmf3-c36m-g5cf,无独立 CVE)——与 podman 相隔 33 秒 | https://github.com/containers/buildah/security/advisories/GHSA-pmf3-c36m-g5cf | 一手 |
| 2024-03-18T15:15:41.170Z | NVD 发布 CVE-2024-1753(覆盖 Buildah 与 Podman Build;`vulnStatus: Deferred`)——晚于 repo-level 约 1h | https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2024-1753 | 一手 |
| **2024-03-19T20:06:52Z** | **GHSA-pmf3-c36m-g5cf 全局 published_at**(buildah,High,无 CVSS)——晚于 repo-level 约 1 天 6h | https://api.github.com/advisories/GHSA-pmf3-c36m-g5cf | 一手 |
| **2024-03-28T17:53:52Z** | **GHSA-874v-pj72-92f3 全局 published_at**(podman CVE-2024-1753,Medium,CVSS 8.6)——晚于 repo-level 约 10 天 3h | https://api.github.com/advisories/GHSA-874v-pj72-92f3 | 一手 |
| 2024-05-24T11:48:46Z(`13:48:46+02:00`) | **snapd 修复 commit `68ee9c6a` 被 authored/committed**(作者 zyga=Zygmunt Krynicki,snapd 维护者;commit msg:`Merge pull request from GHSA-p9v8-q5m4-pf46`) | https://github.com/canonical/snapd/commit/68ee9c6aa916ab87dbfd9a26030690f2cabf1e14(`committedDate` JSON) | 一手 |
| 2024-05-31T21:15:09.930Z | NVD 发布 CVE-2024-5138(snapd snapctl 鉴权绕过;`vulnStatus: Analyzed`)——晚于 fix commit 7 天 | https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2024-5138 | 一手 |
| 2025-01-16T11:44:28Z | snapd **repo-level advisory** 发布(GHSA-p9v8-q5m4-pf46) | https://github.com/snapcore/snapd/security/advisories/GHSA-p9v8-q5m4-pf46(relative-time) | 一手 |
| **2025-01-16T17:19:07Z** | **GHSA-p9v8-q5m4-pf46 全局 published_at**(snapd CVE-2024-5138,Medium,CVSS 4.0)——晚于 repo-level 约 5h35m;**晚于 NVD 约 7 个月 15 天**(见矛盾分析) | https://api.github.com/advisories/GHSA-p9v8-q5m4-pf46 | 一手 |
| 2026-01-22T19:07:38Z | incus **repo-level advisory** 发布(GHSA-x6jc-phwx-hp32,CVE-2026-23953) | https://github.com/lxc/incus/security/advisories/GHSA-x6jc-phwx-hp32 | 一手 |
| 2026-01-22T19:07:39Z | incus repo-level advisory 发布(GHSA-7f67-crqm-jgh7,CVE-2026-23954)——与上一条相隔 1 秒 | https://github.com/lxc/incus/security/advisories/GHSA-7f67-crqm-jgh7 | 一手 |
| **2026-01-22T20:21:17Z** | **GHSA-x6jc-phwx-hp32 全局 published_at**(incus 23953,High,CVSS 8.7)——晚于 repo-level 约 1h14m | https://api.github.com/advisories/GHSA-x6jc-phwx-hp32 | 一手 |
| **2026-01-22T20:26:10Z** | **GHSA-7f67-crqm-jgh7 全局 published_at**(incus 23954,High,CVSS 8.7)——晚于 repo-level 约 1h18m | https://api.github.com/advisories/GHSA-7f67-crqm-jgh7 | 一手 |
| 2026-01-22T22:16:20.673Z | NVD 发布 CVE-2026-23953(晚于全局 published_at 约 1h55m) | https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2026-23953 | 一手 |
| 2026-01-22T22:16:20.833Z | NVD 发布 CVE-2026-23954 | https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2026-23954 | 一手 |
| **2026-07-14T09:06:19Z** | `rmcnamara-snyk` GitHub 档案 `updated_at`(本批 API 复核;调研前 2 周——表明账号仍活跃、Bio/Company 仍为 Staff Security Researcher / Snyk) | https://api.github.com/users/rmcnamara-snyk(`updated_at`) | 一手 |

### 9 条 GHSA 三种发布日汇总(全局 API published_at 为主)

| # | GHSA | 软件 / CVE | 全局 published_at(API,主) | repo-level 发布日 | NVD published | severity / CVSS |
|---|------|-----------|---------------------------|-------------------|---------------|------------------|
| 1 | GHSA-xr7r-f8xq-vfvv | runc / CVE-2024-21626 | 2024-01-31T22:44:08Z | 2024-01-31T20:07:41Z | 2024-01-31T22:15:53.780 | high / 8.6 |
| 2 | GHSA-m3r6-h7wv-7xxv | buildkit / CVE-2024-23651 | 2024-01-31T22:43:32Z | 2024-01-31T20:46:29Z | 2024-01-31T22:15:54.183 | high / 8.7 |
| 3 | GHSA-4v98-7qmw-rqr8 | buildkit / CVE-2024-23652 | 2024-01-31T22:43:26Z | 2024-01-31T20:46:07Z | 2024-01-31T22:15:54.377 | critical / 10.0 |
| 4 | GHSA-wr6v-9f75-vh2g | buildkit / CVE-2024-23653 | 2024-01-31T22:43:20Z | 2024-01-31T20:45:51Z | 2024-01-31T22:15:54.600 | critical / 9.8 |
| 5 | GHSA-874v-pj72-92f3 | podman / CVE-2024-1753 | **2024-03-28T17:53:52Z** | 2024-03-18T14:15:18Z | 2024-03-18T15:15:41.170 | medium / 8.6 |
| 6 | GHSA-pmf3-c36m-g5cf | buildah / CVE-2024-1753(共享) | **2024-03-19T20:06:52Z** | 2024-03-18T14:15:51Z | (同 CVE-2024-1753) | high / 无 |
| 7 | GHSA-p9v8-q5m4-pf46 | snapd / CVE-2024-5138 | **2025-01-16T17:19:07Z** | 2025-01-16T11:44:28Z | 2024-05-31T21:15:09.930 | medium / 4.0 |
| 8 | GHSA-x6jc-phwx-hp32 | incus / CVE-2026-23953 | 2026-01-22T20:21:17Z | 2026-01-22T19:07:38Z | 2026-01-22T22:16:20.673 | high / 8.7 |
| 9 | GHSA-7f67-crqm-jgh7 | incus / CVE-2026-23954 | 2026-01-22T20:26:10Z | 2026-01-22T19:07:39Z | 2026-01-22T22:16:20.833 | high / 8.7 |

> 任务已核实上下文给的日期(podman 2024-03-28、buildah 2024-03-19、snapd 2025-01-16)**与全局 API published_at 完全一致**——任务上下文采用的就是全局 Advisory Database 发布日。早期基于 repo-level HTML 的"修正"结论已被证伪(见「矛盾与未解之处」#5)。

## 关键时间节点分析

### 静默期:2023-07 → 2024-01(约 6 个月)

- `rmcnamara-snyk` 企业 GitHub 账号创建于 **2023-07-09T20:10:00Z**(本批 API 复核确认,精确到秒)。
- 第一个公开 CVE 信用(Leaky Vessels)的全局 published_at 为 **2024-01-31T22:44:08Z**;repo-level 更早(20:07:41Z)。
- 中间约 **6 个月**(2023-07-09 → 2024-01-31)在公开侧**无任何可核实产出**:public_repos=0、公开事件流=0(API 复核 `events_count: 0`)、无 PR/issue/comment。
- 但**并非真空**:Rory 的 Snyk 作者档案(Contentful `contentPerson`,slug `rory-mcnamara`)创建于 **2024-01-30T19:00:17Z**——Leaky Vessels 公告前 1 天。说明静默期内他已在 Snyk 内部完成 Leaky Vessels 的发现、POC、上游协调,产出在 2024-01-31 集中公开。
- 推测:6 个月为 Snyk 入职 + Leaky Vessels ramp-up 期。**入职日不可直接核实**(无 LinkedIn/公开声明),以 GitHub 账号创建日为代理证据。

### Leaky Vessels 集中发布:2024-01-31(批量协调披露的典范)

2024-01-31 当天 2.5 小时内三层级联:

| UTC 时间 | 层级 | 事件 |
|----------|------|------|
| 20:06:08 | 上游 release | runc v1.1.12 |
| 20:07:41 | repo-level advisory | runc GHSA |
| 20:44:09 | 上游 release | buildkit v0.12.5 |
| 20:44:30 | Snyk 博客 | Leaky Vessels 公告 URL 首被 Wayback 抓取 |
| 20:45:51–20:46:29 | repo-level advisory | 3 条 buildkit GHSA |
| 22:15:53–54 | NVD | 4 个 CVE 批量发布 |
| 22:43:20–22:44:08 | 全局 Advisory DB | 4 条 GHSA 全局 published_at 批量 |

- 三种发布日同日(2024-01-31);上游 release 早于 repo-level advisory 1-2 分钟,repo-level 早于 NVD ~2h,NVD 早于全局 DB ~28 分钟。
- oss-security 紧随:Aleksa Sarai 原始公告 ≈ Jan 31 20:33 UTC,Solar Designer 回帖 Feb 01 00:49 UTC,Aleksa 后续 Feb 02 11:27 UTC。
- 6 天后(2024-02-06)Snyk 发布 **Rory 亲自署名**的 deep-dive 技术博客(`publishDate 2024-02-06T11:00-05:00`)。
- **协调者**:Aleksa Sarai(cyphar,SUSE,runc 维护者)署名协调;rory 不在 runc MAINTAINERS,身份为 Snyk 侧发现者/报告者。Rory credited 4 条(runc + 3 buildkit)。

### 2024-03:podman + buildah 构建期逃逸(repo-level 同日批量,全局 DB 异步)

- **repo-level**:2024-03-18 同日发布(podman 14:15:18、buildah 14:15:51,相隔 33 秒)+ NVD 同日(15:15:41)——这是上游侧的协调批量。
- **全局 DB**:buildah 2024-03-19T20:06:52Z、podman **2024-03-28T17:53:52Z**——全局 Advisory Database 收录异步,buildah 晚 1 天、podman 晚 10 天。因此在全局 published_at 维度上**两者并非同日**,而 repo-level/NVD 维度上是同日批量。
- buildah **无独立 CVE**,与 podman 共享 CVE-2024-1753(NVD 描述覆盖 Buildah 与 Podman Build;`vulnStatus: Deferred`)。
- podman severity/CVSS 错位:标 `medium` 但 CVSS 8.6(通常 8.6 属 high 区间)——可能是早期 CVSS 评估与后续 severity 标签不一致。
- 受影响版本:podman v4 < 4.9.4、podman v5 < 5.0.1;buildah 多个版本线(< 1.35.1 / < 1.34.3 / < 1.33.7 / < 1.27.4 / < 1.24.7 / < 1.29.3 / < 1.31.5 / < 1.32.3)。

### 2025-01:snapd snapctl 鉴权绕过(单条,带 7.5 个月异常时间差)

- **全局 published_at 2025-01-16T17:19:07Z**(repo-level 同日 11:44:28Z,晚 5h35m)。
- 但 **NVD published 2024-05-31**(早于全局 advisory 约 7 个月 15 天)——9 条中唯一 NVD 早于 GHSA 的条目(详见「矛盾与未解之处」#1)。
- 上游修复 commit `68ee9c6a` 由 zyga 于 **2024-05-24** authored/committed(commit message 直接引用 `GHSA-p9v8-q5m4-pf46`,证明该 GHSA 在 2024-05 已作为私有协调引用存在)。
- 受影响版本:snapd >= 2.51.6, < 2.63.1;亦 < commit 68ee9c6aa916(2024-05-24)。修复含于 snapd 2.63.1。
- 节奏上属"单条间隔"模式(2024-03 → 2025-01 间隔约 10 个月)。

### 2026-01:Incus 两个 CVE(批量,同日,相隔 1 秒)

- **repo-level 2026-01-22T19:07:38/39Z**(相隔 1 秒);**全局 published_at 2026-01-22T20:21:17 / 20:26:10Z**(相隔约 5 分钟);NVD 当晚 22:16:20 批量。
- 三种发布日同日(2026-01-22)。又是协调批量披露。
- NVD 引用直接指向 incus 源码行号(`driver_lxc.go#L1081`、`#L7215`、`#L7294`)并附带 PoC 脚本(`github.com/user-attachments/files/...`),说明披露含完整 PoC。
- 受影响版本:incus v6 < 6.21.0(两条均如此)。

## 节奏模式(批量协调 vs 单条间隔)

1. **批量同日发布是主旋律**:9 条 GHSA 中 7 条分属 3 个同日批量窗口(以全局 published_at 计)——
   - 2024-01-31(4 条:runc + 3 buildkit,全局 22:43-22:44)
   - 2026-01-22(2 条:incus,全局 20:21/20:26)
   - 2024-03 窗口在 repo-level/NVD 维度是同日批量(3-18),但全局 DB 异步(buildah 3-19、podman 3-28),故全局维度不算紧批量。
   仅 snapd(2025-01-16)为单条。
2. **批量窗口之间间隔长且不规则**:2024-01-31 → 2024-03-18(repo)/03-28(全局 podman)→ 2025-01-16 → 2026-01-22。间隔在拉长(46 天 → 10 个月 → 12 个月),但每个窗口的"密度"并未下降(incus 仍 2 条同日)。与"容器/运行时核心组件深度漏洞需数月验证 + 协调"的研究周期一致。
3. **三种发布日的层叠时序基本稳定**(snapd 除外):上游 release → repo-level advisory(1-2 分钟内)→ NVD(1-2 小时)→ 全局 Advisory DB(同日或 1-2 小时后)。**全局 DB 通常晚于 NVD 约 28 分钟**(Leaky Vessels)到 1 小时多(incus),但 podman 全局 DB 异常晚 10 天。
4. **snapd 是唯一反向特例**:NVD(2024-05-31)远早于 repo+全局 advisory(2025-01-16)约 7.5 个月。

## 职业节点(信息不足——入职日/升职日/教育背景全部不可核实)

- **Staff Security Researcher**:GitHub Bio `rmcnamara-snyk` 一手(API 复核 `bio: "Staff Security Researcher"`,`company: "Snyk"`)。"Staff" 在 Snyk 体系内为资深级别。隶属于 Snyk Security Labs。
- **加入 Snyk 时间**:约 **2023-07-09T20:10:00Z**(企业 GitHub 账号创建日)。**非直接就业记录**——无 LinkedIn(需登录、非允许域名)、无公开声明可证。可信度高但明确标注为代理证据。
- **是否仍在 Snyk(防过时)**:**是**,截至 2026-07-28。证据:GitHub `updated_at` = 2026-07-14T09:06:19Z(本批 API 复核,调研前 2 周),Bio/Company 仍为 Staff Security Researcher / Snyk;public_repos=0、followers=8、following=0、events_count=0 均符合内部研究模式。
- **升职时间**:不可核实。无任何公开记录显示从何级别晋升至 Staff。
- **教育背景**:完全不可核实。GitHub 档案 `location: None`、无 education。
- **个人账号 `psychomario`**(2011-09-10 创建,Name="Rory McNamara"):与 `rmcnamara-snyk` 关联仅基于同名,无 GitHub 显式关联机制,**为推测(可信度高)**。该账号 2023-09/10 提交过 rbloom / m4b-merge / bragibooks 等非安全类个人项目,**加入 Snyk 前无公开安全研究痕迹**(可核实范围内)。
- **研究方向主线**:容器运行时 / 构建器 / 文件系统边界的逃逸与鉴权(runc、buildkit、podman/buildah、snapd、incus)——9 条 credit 全部为 Go 容器生态,无一例外。高度连贯的研究主线。

## 矛盾与未解之处

1. **snapd:CVE-2024-5138 的 NVD 发布日(2024-05-31)早于 GHSA 全局 published_at(2025-01-16)约 7 个月 15 天——最大异常**。
   - 事实链:fix commit `68ee9c6a` 由 zyga 2024-05-24 authored/committed(msg 引用 GHSA-p9v8-q5m4-pf46)→ NVD 2024-05-31 发布 CVE → repo-level advisory + 全局 published_at 均为 2025-01-16。
   - 解读:commit message 在 2024-05-24 即引用 GHSA ID,证明该 GHSA 2024-05 已作为私有协调引用存在,但公开发布(repo + 全局)推迟到 2025-01-16。NVD 在 2024-05-31 发布 CVE 记录(可能为保留号 + 初版),GHSA(Rory credit 载体)的公开发布晚 7.5 个月。
   - 可能解释(均为推测):(a) 协调披露分两阶段,先 NVD 占位/初版、后 GHSA + Snyk writeup 公开;(b) 等待 snapd 2.63.1 修复到达稳定版/各发行版后公告(受影响版本含 `< 2.63.1` 支持此假设);(c) NVD `published` 反映 CVE 记录入库而非完整披露。
   - **本文采用全局 published_at 2025-01-16 作为 Rory credit 公开时间**(credit 载体是 GHSA),NVD 2024-05-31 作为对照记录。差异如实保留。

2. **podman 全局 DB 异步延迟 10 天**:repo-level advisory + NVD 均为 2024-03-18,但全局 published_at 为 2024-03-28(晚 10 天)。buildah 则只晚 1 天(2024-03-19)。推测为 GitHub 全局 Advisory Database 收录 podman 条目的内部延迟(可能与 CVE-2024-1753 跨 Buildah+Podman 的合并/去重处理有关)。未解。

3. **podman severity/CVSS 错位**:GHSA 标 `severity: medium` 但 `cvss: 8.6`(8.6 通常属 high 区间)。可能是早期 CVSS 向量评估与后续 GitHub severity 标签的不一致。未解。

4. **buildah 无独立 CVE / 无 CVSS**:buildah GHSA-pmf3-c36m-g5cf 的 `cve_id: None`、`cvss_score: None`,与 podman 共享 CVE-2024-1753。NVD 描述明确覆盖两者。这是 Red Hat 体系内 Buildah 与 Podman Build 共享底层代码所致,非矛盾,但需注意 credit 计数:9 条 GHSA 对应 8 个 CVE(buildah 共享)。

5. **早期基于 repo-level HTML 的"任务上下文日期错误"结论已证伪**:本调研前段用 `github.com/<repo>/security/advisories/<GHSA>` 的 repo-level `relative-time` 核实,得出"podman 任务给的 03-28 错(实际 03-18)、buildah 03-19 错(实际 03-18)"的结论。**该结论错误**——repo-level HTML 显示的是 repo advisory 发布日(03-18),而任务上下文采用的全局 API published_at 正是 03-28(podman)/ 03-19(buildah),与 `api.github.com/advisories/<GHSA>` 完全一致。任务上下文日期全部正确。本文已统一以全局 API published_at 为主,repo-level 作为对照列保留。

6. **前序调研产出的 06-timeline.md「2.5 年空窗期(2024-02 → 2026-07)」论断已被证伪**:前序文件基于"未核实到 Leaky Vessels 之外的 Rory 产出"得出空窗结论。但 9 条 GHSA credit(本任务已核实上下文 + github.com/API 一手核实)显示 2024-03、2025-01、2026-01 均有公开 credit。**前序"空窗"论断不成立**,源于前序调研未掌握 GHSA credit 维度。

7. **前序调研产出的「Leaky Vessels 内部里程碑表格」(2023-11-20 发现、2023-12-11/13/19/20 collaborator 日期)无法独立核实**:前序文件声称该表格来自 Snyk 博客 Wayback 快照正文。本调研对 deep-dive 快照(20240208015227)做全文检索:**未发现** "Week of" / "Nov-2023" / "collaborator" / 任何 2023 日期;deep-dive 正文仅含 exploit 技术描述。前序引用的快照 URL(`leaky-vessels-docker-runc-container-breakout-vulnerabilities`)与实际归档 URL(`leaky-vessels-container-vuln-deep-dive/`、`leaky-vessels-container-breakout-vulnerabilities-jan-2024`)不符。**这些"内部里程碑日期"在当前可访问 Wayback 快照中无法证实**,可能为前序调研的不可复现结果或幻觉。本文不予采用。

8. **Wayback 对 Snyk 博客的覆盖不对称**:Leaky Vessels 博客有完整快照(含 `publishDate`),但 podman/buildah/snapd/snapctl/incus 相关 Snyk 博客(若存在)在 Wayback CDX 中**0 命中**(已用 `snyk.io/blog/*<kw>*` 多关键词 + 时间范围查询核实)。无法判断是"无博客"还是"未归档"。故除 Leaky Vessels 外,其余 8 条 credit 的「Snyk 博客发布日」均未核实到。

## 信息不足之处

1. **GHSA 私有创建日(`created_at`)**:`api.github.com/advisories/<GHSA>` 对 9 条全部返回 `created_at: None`——**全局 Advisory Database 不公开私有创建日**。对 snapd 而言,fix commit message(2024-05-24 引用 GHSA ID)间接证明该 GHSA 2024-05 已作为私有协调引用存在,但精确 created_at 不可公开核实。其余 8 条连间接证据也无。
2. **入职 Snyk 的确切日期**:仅以企业 GitHub 账号创建日 2023-07-09T20:10:00Z 为代理证据。无 LinkedIn / 公开声明 / 直接就业记录。
3. **教育与升职背景**:完全不可核实。GitHub 档案无 location/education。
4. **会议演讲历史**:不可核实。WebSearch 在本环境不可用;GitHub 公开事件流为空(API `events_count: 0`)。
5. **snapd 7.5 个月时间差的真实原因**:见「矛盾与未解之处」#1,所有解释均为推测。
6. **podman 全局 DB 10 天延迟原因**:见「矛盾与未解之处」#2,未解。
7. **2024-03-28 → 2025-01-16 之间(约 10 个月)是否有未公开/未 credited 的研究**:不可核实。GHSA credit 维度显示此窗口仅 snapd 一条(且 NVD 早 7 个月),但不排除存在内部研究或未达披露门槛的工作。
8. **Snyk 博客对其他 8 条 credit 的覆盖**:Wayback 0 命中,无法判断是否存在对应博客。

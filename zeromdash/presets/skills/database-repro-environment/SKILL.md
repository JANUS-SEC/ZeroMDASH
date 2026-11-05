---
name: database-repro-environment
description: |
  Database 目标的 PoC 复现环境搭建与调试方法论，用于 prepare_environment_and_debugger /
  build_and_execute_poc / debug_poc 阶段：按目标形态（服务端扩展、独立 server、网关代理、
  嵌入式库、纯协议客户端）选择环境策略，runtime 与 observer 分离构建 sanitizer/观测变体，
  配置对照组与可达性标记，分层定位复现失败原因。PG/MySQL/MongoDB/SQLite/自研数据库
  及其网关、驱动、协议组件适用。
type: skill
---

# Database PoC 复现环境搭建与调试

本 skill 沉淀自 DocumentDB（PostgreSQL 扩展 + Rust 网关）12 个 validated PoC 的实战流程。
核心思想：**把「跑数据库的环境」和「观测崩溃的环境」分开准备**，官方镜像解决前者，
定制构建解决后者，全程不碰 canonical 源码。

## 1. 先识别目标形态（决定一切后续选择）

读 finding request 和 repo，回答三个问题：

1. **缺陷在哪个组件？** 数据库本体（C/C++ server）、服务端扩展（PG extension、MySQL plugin）、
   网关/代理（Rust/Go proxy、wire protocol gateway）、嵌入式库（SQLite 等链接进应用的引擎）、
   还是纯协议客户端（驱动、ORM、连接池）？
2. **oracle 类型是什么？** sanitizer（内存破坏）、signal（panic/abort/SEGV）、exit_code、
   output（日志/错误信息差异）、state_invariant（认证状态、事务状态、角色权限等语义状态）。
3. **复现需要几个进程？** 单进程 harness 即可，还是需要「数据库后端 + 被测组件 + 驱动客户端」
   三层？多数 server 侧 finding 需要三层：后端用官方镜像，被测组件源码构建，客户端手写最小驱动。

## 2. 环境策略矩阵

| 目标形态 | 运行后端（runtime） | 被测组件（observer） | 客户端 |
|---|---|---|---|
| PG/MySQL 扩展（C） | 官方镜像或源码编译的 server（版本对齐 finding 前提） | 定制 toolchain 容器，扩展从源码以观测 profile 构建 | psql/mysql 客户端或最小 SQL 脚本 |
| 独立 server（C/C++） | 同左 | 官方镜像跑 stock；observer 另起容器以 ASan/debug 构建 | 官方 cli 或最小驱动 |
| 网关/代理（Rust/Go） | 数据库本体用官方镜像（如 `*-local` 镜像） | 从源码 cargo/go build，加观测 flags（见 §3） | 手写最小协议客户端 |
| 嵌入式库（C） | 不需要后端 | 宿主机或小容器直接编译 harness + 库源码 | harness 本身 |
| 纯协议/认证逻辑 | 官方镜像（后端 + 被测组件都用 stock） | 不需要 observer，靠报文与状态字段验证 | 手写客户端为主 |

**选择原则**：
- **官方镜像优先**：能拉到目标官方镜像（`postgres`、`mysql`、`mongo`、`documentdb-local` 等）
  就不要从源码全量编译后端——省内存、省磁盘、省时间，且行为更接近部署形态。
- **observer 必须源码构建**：sanitizer、debug flags、`panic=abort` 等观测手段只作用于被测组件，
  且构建产物一律放 workdir/scratch（`CARGO_TARGET_DIR`、out-of-tree build），不污染 canonical repo。
- **宿主机缺权限时用容器兜底**：例如 PostgreSQL 拒绝以 root 启动、容器缺 CAP_SETUID 时，
  直接用 Docker 提供非 root 执行边界，不要在宿主机上 hack 权限。
- **资源受限（1-2GB RAM）时**：后端必须镜像复用；`make -j2` 限制并发；构建容器网络只给
  loopback（`network: none` + host loopback 挂载）；预先清磁盘预算（Docker volume/build cache/
  历史 workdir 是三大头），不够就先清理再构建。

## 3. 通用构建配方

### 3.1 PostgreSQL 扩展（C，内存破坏类首选 ASan）

- 定制 toolchain 容器：基础镜像（Debian/Ubuntu）+ GCC/Clang + GDB + 扩展依赖
  （libbson、PCRE2 等版本必须与 finding 前提一致，例如 PCRE2 10.40 的特定 bug）。
- PG 本体与扩展使用**观测 profile**：
  `CFLAGS="-O0 -g -fno-omit-frame-pointer -fsanitize=address"`（ASan），
  或 `-fsanitize=undefined`（UBSan），PG  configure 加 `--enable-debug`。
- 独立数据目录 initdb 到 scratch；**只绑 unix socket 或 127.0.0.1 高端口**（如 55433），
  用 `pg_ctl` 启停；SQL 通过 `psql -h <socket> -p <port> -U <user> -d <db>` 下发。
- **修复版对照（fixed reference）**：另取修复 commit 的干净 checkout，同 profile 构建，
  用相同输入验证「修复版不触发」——这是 patch_miss 类 finding 最有力的控制组。
- ASan 运行参数：`ASAN_OPTIONS=abort_on_error=1:detect_leaks=0:log_path=<workdir>/asan`
  （leak 噪声大时关 detect_leaks；log_path 把报告落到 workdir 证据目录）。

### 3.2 Rust 网关/代理

- 后端（数据库本体）用官方镜像；网关从源码 `cargo build --locked`（锁定依赖并记录 lock hash）。
- **stock 是 `panic=unwind` 时**，slice panic 只表现为连接级 DoS，拿不到崩溃信号——
  需要 observer 变体 `CARGO_PROFILE_DEV_PANIC=abort`（或 release profile 同理），
  把 Rust panic 转成 SIGABRT 才能被 signal oracle 捕获。
  **报告中必须写明该 SIGABRT 来自 observer 构建，不得冒充 stock 行为**。
- `CARGO_TARGET_DIR` 指向 scratch；`CARGO_HOME`/`RUSTUP_HOME` 也放 scratch，
  避免污染宿主工具链；`RUSTFLAGS` 需要时加 `-C debuginfo=2` 保留回溯符号。

### 3.3 Go server/组件

- `go build -race`（数据竞争）、`-gcflags="all=-N -l"`（关优化保调试信息）；
  后端同样官方镜像优先；崩溃日志（panic stack）本身即可做 output oracle。

### 3.4 嵌入式 C 库（SQLite 等）

- 宿主机或小容器即可：`cc -O0 -g -fsanitize=address harness.c <lib sources>`，
  或库自带 CMake 时 `CMAKE_C_FLAGS` 注入 sanitizer；harness 只链接必需文件，避免全量构建。

### 3.5 纯协议/认证/状态机（无需内存破坏观测）

- 全部用 stock：官方镜像起后端与被测组件，手写最小客户端（Python/Go/Rust 驱动均可），
  重点在**报文构造、握手时序、状态字段采集**（认证状态、角色、会话、错误码），
  oracle 用 output / state_invariant，不需要 sanitizer。

## 4. Oracle 观测配置（环境侧义务）

- **sanitizer**：构建时注入（§3），运行时设 `ASAN_OPTIONS`/`UBSAN_OPTIONS`，报告落盘到
  workdir；oracle 匹配需要 backtrace 符号，保留 `-g` 和 frame pointer。
- **signal**：确认目标崩溃形态真的会产生信号（Rust panic 需要 abort 变体；PG `ereport`
  默认只是错误不是崩溃，需要 ASan 或 `debug_assertions` 才能升级成可观测异常）。
- **output**：服务端日志级别调高（如 PG `log_min_messages=DEBUG1`），重定向到 workdir；
  客户端 stdout/stderr 全量保留。
- **state_invariant**：在客户端脚本里显式采集状态字段（认证标志、当前角色、会话 ID、
  事务状态、错误码），不要只凭「命令没报错」下结论。
- **reachability markers**：在 harness/客户端里打印阶段标记（connected / authenticated /
  command_sent / response_received），或在 observer 日志里 grep 关键函数名——
  **先有 markers 证明到达目标路径，再谈 oracle 命中**。

## 5. 对照组（controls）与诚实性

- **benign input control**：同形状合法输入不得触发 oracle（例如合法 OP_MSG、正常 SCRAM 握手、
  无 `(*LIMIT_HEAP=0)` 的正则）。控制失败说明环境/oracle 本身有问题，先修环境。
- **fixed reference control**：patch_miss 类必须有——修复版同 profile 构建，同输入不触发。
- **stock vs observer**：observer（ASan/panic=abort/debug）只用于观测与证明机制；
  结论涉及 stock 行为时必须单独验证 stock 表现（如 stock 仅连接级 DoS），并在报告中区分。
- **不夸大**：validated 只表示「冻结 oracle 在独立复验中稳定命中」，不自动等于
  「stock 上可武器化」。

## 6. 可复现性与证据

- 固化 `build.sh` / `run.sh` 到 attempt 目录；记录：编译器与依赖版本、镜像 ID/digest、
  二进制 sha256、canonical 源码树 hash、依赖 lock hash（Cargo.lock / go.sum）。
- 独立 clean 复验 ≥3 次（不同 shell、最好重建环境），满足 `min_matches`；复验必须重新
  执行 candidate，不得引用上一次输出。
- 环境清单 `environment_manifest` 至少包含：`backend=agent_sandbox`、runtime（镜像/容器/
  socket/端口）、toolchain（编译器、sanitizer、依赖版本）、build profiles、observer 与 stock
  差异、resource limitations、cleanup 状态。
- cleanup：停容器、删临时数据目录与端口占用、清理镜像（按名 rmi，别用 `image prune -a`
  误伤进行中的任务）。

## 7. 调试 playbook（按层定位，别乱改输入）

1. **命令全挂/读不到文件**：先查沙箱与权限（容器是否可写、属主、网络代理、DNS、
   镜像源是否可用），这层没解决前不要调 PoC。
2. **构建失败**：依赖版本与 finding 前提是否对齐（PCRE2 版本、PG 主版本、libbson 结构体
   布局）→ 网络/代理/镜像源 → 资源（内存不够就 `make -j1/-j2`、加 swap）。
3. **oracle 不命中**：先看 reachability markers 是否到达目标路径（没到 = 输入/前置条件/
   路由问题，去修输入而不是改 oracle）；再看 build profile 是否覆盖该路径（JIT 绕过、
   sanitizer 没编进该 .so、observer 没生效）；最后才评估 oracle 是否过严/过松
   （过严则换等价的另一种 oracle 表达，而不是放宽判定）。
4. **结果不稳定（reproduced_unstable）**：清残留容器/数据目录/端口冲突；固定资源
  （内存、并发、时序）；概率型 finding（如 nonce 碰撞）要把「尝试次数与命中分布」写进
   证据，而不是拿单次命中充数。
5. **debugger 只观测**：GDB batch（`gdb -batch -ex run -ex bt --args ...`）、core dump、
   ASan backtrace 用来定位调用链，禁止改寄存器/内存/PC 制造结果。

## 8. 禁忌

- 不改 canonical 源码与二进制；不为制造崩溃而 patch 目标；不在目标侧植入持久化/后门。
- observer 构建不得冒充 stock 行为；环境限制（小内存、无网、无权限）必须写进 manifest。
- 磁盘与内存预算是环境的一部分：构建前确认余量，失败后先清理再重试，不要硬撑到写满。

## 附：DocumentDB 实战映射（ validated 案例）

- **Rust 网关 slice panic（patch-001/002）**：后端 `documentdb-local` 官方镜像 +
  网关 `cargo build --locked` + `CARGO_PROFILE_DEV_PANIC=abort` observer，
  负长度 OP_MSG → SIGABRT，3/3 复现 + 独立复验通过。
- **PG 扩展 CodeWScope 堆越界读（patch-003）**：定制 PG17.6 toolchain 容器 +
  `-O0 -g -fsanitize=address` 构建扩展，unix socket 55433，`$setUnion` 触发 ASan
  heap-buffer-overflow；修复 commit 对照同 profile 不触发。
- **SCRAM 弱 nonce 重放（vuln-019）**：全 stock，手写客户端重放捕获握手，
  oracle=state_invariant（认证成功 + listDatabases 可达），12 markers + 16 state fields +
  5 controls 全过；报告明确「需先捕获合法握手，非离线破解」。

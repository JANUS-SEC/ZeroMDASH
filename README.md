# ZeroMDASH

Open re-implementation of Microsoft MDASH: a LangGraph-based multi-agent
vulnerability analysis pipeline that drives external coding-agent runtimes such
as Claude Code, Codex CLI, TraeX (`traecli` / `traex`), Kimi Code, OpenCode,
DeepSeek Harness (`dsh`), and DeepAgent.

## Quickstart

```bash
pip install -e ".[all]"

# Full scan
zeromdash --target https://github.com/curl/curl

# Diff-highlighted scan over an already-patched checkout
zeromdash \
  --target ./patched-repo \
  --scan-mode diff \
  --diff-file /tmp/change.patch

# Gather cross-target chains from completed workspaces
zeromdash \
  --scan-mode gather \
  --gather-workspace-to-chain demo/gather-multi-target-config.example.yaml \
  --agent-config demo/gather-agent-config.example.yaml
```

### Full/diff workspace layout

Full and diff scans create `.zeromdash/workspace_for_<target>/`:

```text
workspace_for_<target>/
├── workspace.json
├── main/
│   ├── repo/                    # target source tree
│   ├── repos/                   # per-repository trees for multi-repo targets
│   ├── scope/                   # scope.json; diff mode also stores the copied diff/hunks
│   ├── spec/                    # relevant RFCs and standards
│   ├── feature/                 # new or weakly-covered feature surfaces
│   ├── attack_surface/          # attack_surface.md + domain_invariant_registry.json
│   ├── writeup/                 # target vulnerability history
│   └── patch/                   # corresponding patches and patch manifest
├── similar/<software>/
│   ├── repo/
│   ├── writeup/
│   └── patch/
├── log/
│   ├── state/                   # plans, convergence records, dispatch plan, chain pool/plan
│   ├── review_log/              # per-attempt agent and validation logs
│   ├── subtask_res/             # terminal subtask envelopes
│   ├── primitive_res/           # confirmed non-standalone primitives
│   ├── chain_res/               # confirmed end-to-end chain findings
│   ├── chain_candidates/        # rejected or inconclusive chains
│   └── agent_commands.jsonl
├── sub_workspace/               # rendered role cards, contracts and runtime settings
├── summary.en.md
├── summary.zh_CN.md
├── summary.md
├── gate_result.json
└── final_state.json
```

Diff mode additionally writes `changes.diff`, changed-file/symbol indexes, raw
planner candidates and convergence records under `main/scope/` and `log/state/`.
Selected subtask/chain reruns use isolated directories under `log/` and do not
overwrite canonical results.

### Gather workspace layout

Gather mode creates a separate
`.zeromdash/workspace_for_gather-<scenario-name>/`. It does not use
`main/repo/` as its input source; every completed source workspace is copied
into a target-scoped, immutable analysis snapshot under `inputs/`:

```text
workspace_for_gather-<scenario-name>/
├── workspace.json
├── gather_manifest.yaml
├── inputs/
│   ├── manifest.normalized.json
│   ├── gather_inputs.lock.json
│   └── <target-id>/
│       ├── workspace.json       # sanitized source-workspace metadata
│       ├── source_context.json  # sanitized focus/repository context; no env secrets
│       ├── attack_surface/      # source main/attack_surface snapshot
│       ├── source/
│       │   ├── main/            # source main/repo snapshot
│       │   └── <repo-id>/       # source main/repos/<repo-id> snapshot
│       ├── primitive_res/       # active confirmed primitives
│       ├── subtask_res/         # active terminal subtask envelopes
│       └── chain_res/           # active confirmed local chains
├── main/
│   └── attack_surface/
│       ├── gather_attack_surface.md
│       └── cross_target_registry.json
├── log/
│   ├── state/
│   │   ├── gather_evidence_pool.json
│   │   └── gather_chain_plan.json
│   ├── review_log/              # gather node/battle attempt logs
│   ├── gather_chain_res/        # confirmed cross-target chain findings
│   ├── gather_chain_candidates/ # rejected or inconclusive cross-target chains
│   ├── gather_report_groups.json
│   └── agent_commands.jsonl
├── sub_workspace/               # gather node and per-chain agent work directories
├── summary.en.md
├── summary.zh_CN.md
├── summary.md
├── gate_result.json
└── final_state.json
```

The base `Workspace` class also creates compatibility directories such as
`main/repo/`, `similar/`, `log/subtask_res/`, and `log/chain_res/` in a gather
workspace. They are normally empty; canonical gather inputs live under
`inputs/`, and cross-target results live under the `gather_*` paths shown above.

## CLI Options

```
--target TEXT              Target software (path, git URL, or package name)
--scan-mode full|diff|gather
                           Full, diff-highlighted, or cross-workspace gather scan
--gather-workspace-to-chain YAML
                           Multi-target workspace manifest required by gather mode
--diff-file PATCH          Unified git diff already applied to the target repo
--diff-git BEFORE..AFTER   Generate diff from refs in the fetched remote git repo
--workspace-root PATH      Output directory (default: ./.zeromdash)
--task-id TEXT             Custom task id
--max-iterations INT       Max critic feedback rounds per subtask (default: 3)
--min-critic-skills INT    Min expert skills the critic is asked to apply (default: 2)
--role-lang TEXT           Role-card language, e.g. en or zh_CN (default: en)
--agent-config YAML_FILE   Configure node runtimes and workflow limits
--preset-attack-surface MD Seed the attack-surface report before analysis
--disable-spec             Skip the spec track (search_spec + plan_by_spec; no spec subtasks)
--disable-target-history   Skip target history and patch-miss planning
--disable-new-feature      Skip new-feature coverage-gap analysis
--disable-chain            Skip cross-primitive chain planning and chain battles
--till-node analyze|plan|summary
                           Stop before later stages; summary never runs PoC generation
--only-gen-pocs DIR        Generate PoCs for all qualified findings in a workspace
--only-gen-poc DIR:ID      Generate one report-group, subtask, or chain finding PoC
--start-from-subtask DIR   Restore an existing workspace and start at subtask dispatch
--select-subtask-to-run IDS
                           Rerun selected planner subtask IDs without summary
--select-subtask-to-run-log-dir DIR
                           Isolated output directory for a selected rerun
--start-from-chain DIR     Restore an existing workspace and start at chain planning
--select-chain-to-run IDS  Rerun selected chain IDs without summary
--select-chain-to-run-log-dir DIR
                           Isolated output directory for a selected chain rerun
--start-from-summary DIR   Restore an existing workspace and run only summary
--fail-on-gate             Exit non-zero when a diff-mode finding blocks
```

Examples:
```bash
# Local source tree
zeromdash --target ./my-project --workspace-root /tmp/audit

# MR/code-diff gate: repo is already patched; diff only highlights and attributes
zeromdash \
  --target ./patched-repo \
  --scan-mode diff \
  --diff-file /tmp/change.patch \
  --fail-on-gate

# Remote git range: fetch refs, checkout AFTER, and highlight BEFORE..AFTER
zeromdash \
  --target https://example.com/team/repo.git \
  --scan-mode diff \
  --diff-git release-1.0..main \
  --fail-on-gate

# Use Chinese role cards
zeromdash --target curl --role-lang zh_CN

# Skip the spec track (cost control)
zeromdash --target curl --disable-spec

# Skip target-history lookup for private software
zeromdash --target ./private-project --disable-target-history

# Stop after attack-surface analysis
zeromdash --target curl --till-node analyze

# Stop after planner JSON is materialized
zeromdash --target curl --till-node plan

# Stop after summary, without PoC generation
zeromdash --target curl --till-node summary

# Generate all PoCs, or one selected PoC, from an existing workspace
zeromdash --only-gen-pocs .zeromdash/workspace_for_curl
zeromdash --only-gen-poc .zeromdash/workspace_for_curl:VULN-001

# Restore a workspace that already has planner JSON files
zeromdash --start-from-subtask .zeromdash/workspace_for_curl

# Rerun selected subtasks only; canonical results remain unchanged
zeromdash \
  --start-from-subtask .zeromdash/workspace_for_curl \
  --select-subtask-to-run vuln-013,patch-008,spec012

# Use an explicit isolated output directory
zeromdash \
  --start-from-subtask .zeromdash/workspace_for_curl \
  --select-subtask-to-run vuln-013 \
  --select-subtask-to-run-log-dir selected_runs/vuln-013-review

# Restore a workspace that already has subtask_res/primitive_res and start at
# chain planning
zeromdash --start-from-chain .zeromdash/workspace_for_curl

# Rerun selected chain candidates only; canonical results remain unchanged
# (chain IDs are stable hashes from log/state/chain_plan.json)
zeromdash \
  --start-from-chain .zeromdash/workspace_for_curl \
  --select-chain-to-run chain_1a2b3c4d5e6f7a8b

# Regenerate the bilingual summaries from log/subtask_res/*.json
zeromdash --start-from-summary .zeromdash/workspace_for_curl

# Build cross-target chains from completed source workspaces
zeromdash \
  --scan-mode gather \
  --gather-workspace-to-chain demo/gather-multi-target-config.example.yaml \
  --agent-config demo/gather-agent-config.example.yaml
```

When `--target` is a local directory, ZeroMDASH copies the complete source tree
into `main/repo/` deterministically before analysis. The original directory is
not modified, and local `.git` / `.zeromdash` metadata is not copied.

## Agent Config

`--agent-config` is the preferred way to set workflow limits, task focus, and
per-node runtime settings:

Use `demo/zeromdash.oss.demo.yaml` for a single repository. Use
`demo/zeromdash.oss.multi-repo-demo.yaml` when one target product is composed of
a core repository plus plugin or feature repositories. Multi-repo targets
currently support full scan mode only. Gather mode instead consumes two or more
already-completed workspaces; its manifest and coordinator examples live at
`demo/gather-multi-target-config.example.yaml` and
`demo/gather-agent-config.example.yaml`.

```yaml
common_focus: >
  Threat model, attacker position, trust boundary, target component, impact
  class, and any project-wide constraints.

max_concurrency: 8  # default; caps simultaneous LangGraph Send/node executions
top_K:
  spec: 5
  vuln: 8
  patch: 3
  feature: 4
  chain: 16  # chain candidates dispatched to chain battles after pruning

# Optional cross-primitive chain aggregation controls (defaults shown):
# chain:
#   enabled: true                      # or use --disable-chain
#   max_length: 4                      # max primitives per candidate chain
#   max_successors_per_capability: 4   # successor cap per capability expansion
#   beam_width: 64                     # search frontier cap
#   max_candidates_before_top_k: 200   # candidate cap before top_K.chain
#   max_battle_rounds: 2               # max chain investigate/critic iterations

# Optional post-summary PoC generation (disabled by default):
# poc:
#   enabled: true
#   backend: agent_sandbox
#   max_findings: 8
#   max_debug_rounds_per_strategy: 4
#   verification_runs: 3
#   verification_min_matches: 2

node:
  search_spec:
    runtime: claude_code
    config: bedrock
    provider: bedrock
    focus: "Relevant protocol and parser specifications."

  investigate_subtask:
    runtime: traex
    config: work
    fallbacks:
      - runtime: claude_code
        config: ark-proxy
        provider: ark

  critic_subtask:
    runtime: codex

  # Each PoC phase has an independent headless Agent configuration:
  plan_poc:
    runtime: codex
  prepare_environment_and_debugger:
    runtime: codex
  generate_poc:
    runtime: codex
  build_and_execute_poc:
    runtime: codex
  debug_poc:
    runtime: codex
  verify_poc:
    runtime: codex
  release_poc:
    runtime: codex
```

`top_K` is an explicit cost cap on dispatched subtasks. Omitting it leaves
the bucket uncapped; setting it can reduce coverage and is not implicitly
enabled by diff mode. `max_concurrency` only limits how many dispatched
LangGraph tasks run at the same time.

`investigate_subtask`, `critic_subtask`, `plan_chains`,
`chain_investigate_subtask`, `chain_critic_subtask`, all semantic `gather_*`
nodes, and `summary` must use a harness with
verified native subagent support. The accepted runtimes are `codex` (including
`codex_cli` aliases), `traex`, and `claude_code`; this restriction applies to
both the primary runtime and every fallback. ZeroMDASH enables Codex
`multi_agent`, enables TraeX `multi_agent_v2`, and grants Claude Code's `Agent`
tool only in these nodes' generated local settings. Other nodes may still use any registered
runtime. Here, “subtask” means a ZeroMDASH LangGraph work unit; “subagent” means
a child agent created natively by one of those harnesses.

TraeX is supported as `runtime: traex` (aliases: `trae`, `trae_cli`,
`traecli`, `trae_code`, `traecode`). ZeroMDASH runs `traecli exec` in
non-interactive mode, passes the prompt over stdin, captures the final response
with `--output-last-message`, and uses native `--output-schema` for object-shaped
structured-output contracts. TraeX 0.201.1 rejects top-level array schemas, so
planner `Subtask[]` output remains JSON-only and is validated by ZeroMDASH's
existing orchestrator validator. TraeX reads the rendered `AGENTS.md` from the
node sub-workspace. The sub-workspace is its working root; `--add-dir` grants
workspace-write access to the complete task workspace so final artifacts can be
written under `main/`, `similar/`, and `log/`. The adapter sets
`project_root_markers=[]` so TraeX loads only the invocation-local
`AGENTS.md` instead of inheriting instructions from ancestor task directories.

`config` selects `~/.trae/<config>.traecli.toml` through TraeX `--profile`.
Omit `config` to use the base `~/.trae/traecli.toml`. ZeroMDASH explicitly uses
TraeX `workspace-write`, the non-interactive exec default approval policy, and
ephemeral sessions. It does not enable Auto-Review, which cannot ask for
approvals in exec mode, or the dangerous full-access bypass.

```yaml
node:
  investigate_subtask:
    runtime: traex
    config: work
    model: seed-2.1-pro
```

Kimi Code is also supported as a node runtime. With the official Kimi provider
configuration in `~/.kimi-code/config.toml`, no `provider` or `config` is
required. For Kimi prompt mode, ZeroMDASH renders project-level instructions to
`.kimi-code/AGENTS.md`. Each `sub_workspace` also gets `.kimi-code/local.toml`
with `[workspace].additional_dir` pointing at the whole ZeroMDASH workspace.

Kimi cannot currently be assigned to `investigate_subtask`, `critic_subtask`,
`plan_chains`, `chain_investigate_subtask`, `chain_critic_subtask`, or
`summary`, because this adapter has no verified native-subagent contract for
Kimi. It remains available to fetch, search, analysis, and planner nodes.

DeepSeek Harness is supported through `dsh --profile headless`. ZeroMDASH does
not put the complete task in argv. It writes the prompt and runtime metadata to
the invocation-local `.dsh/` directory, starts DSH from the task workspace root
so `workspace-write` covers `main/`, `log/`, and `sub_workspace/`, and keeps the
logical current directory at the invocation sub-workspace.

The default DSH mode is a constrained minimal-plus-search leaf agent. It keeps
persistent `bash` and `str_replace_editor`, adds bounded `glob`/`grep`
repository discovery, and disables interactive approval, writable filesystem
tools beyond shell/editor, web access, nested DSH subagents/workflows/Ralph,
the automatic session-title LLM request, and global session persistence. A
node `config` value is treated as an additional trusted DSH `--patch` file
applied after the bundled minimal patch.

Because the bundled headless DSH overlay disables its subagent tools, DSH also
cannot be assigned to `investigate_subtask`, `critic_subtask`,
`plan_chains`, `chain_investigate_subtask`, `chain_critic_subtask`, or `summary`. It can
still be used by the other nodes, with `provider`, `model`, and an optional
trusted `config` patch.

Each DSH invocation materializes:

```text
sub_workspace/node_<node>[/subtask_<id>]/
  .dsh/
    AGENTS.md
    headless-minimal.patch.yml
    invocation.json
    prompt.md
    settings.yaml
    sessions/
  output.schema.json        # structured-output nodes only
  skills/
```

## Runtime Selection

The main `zeromdash` workflow uses explicit runtime selection. At startup,
ZeroMDASH health-checks the configured runtime and any explicit `fallbacks` for
every enabled node. If a runtime/config/env combination is unhealthy, the CLI
pauses and asks for a temporary runtime/config/provider/model override. At
runtime, a node falls back only when its current runtime has exhausted that
node's existing retry attempts and still failed.

When automatic attempts and all explicit fallbacks are exhausted, the CLI
asks for a temporary `runtime/config/provider/model`, health-checks it, and
retries the failed invocation without advancing the investigation iteration.
This includes invalid structured output even when the agent exits with code 0.
Valid critic `revise`/`reject` decisions continue through the normal graph.

Recovery prompts run on the main thread, one at a time. Concurrent failures
of the same node share a versioned replacement: waiting tasks and later calls
reuse the new configuration instead of asking again for the old failure.
Already running agent processes can finish; runtime console messages wait
while the prompt owns the terminal. EOF or cancellation aborts recovery,
wakes waiting tasks, and prevents new agent launches. Existing artifacts remain
on disk; in-flight processes are allowed to finish.

Temporary overrides are recorded in `log/runtime_recovery.jsonl` (or the
selected-run log directory) and in the completed `final_state.json`.
The source YAML is not changed. Investigation/output attempt logs from manual
retries include `recovery-N` so the exhausted attempts remain inspectable.
Programmatic graph calls retain their non-interactive behavior unless wrapped
in `RuntimeRecovery(callback).run(...)` from `zeromdash.nodes.core.recovery`.

| Node type | Default runtime |
|---|---|
| Fetch / search / summary | `claude_code` |
| Attack-surface analysis | `codex` |
| Planning / investigation / critic | `codex` |
| Chain planning / investigation / chain critic | `codex` |

Supported runtime names:

| Runtime | Aliases | `config` meaning |
|---|---|---|
| `claude_code` | `claude` | Short name expands to `~/.claude/settings.<name>.json`; paths are used directly. |
| `codex` | `codex_cli`, `openai_codex` | Passed as `codex --profile <config>`. |
| `traex` | `trae`, `trae_cli`, `traecli`, `trae_code`, `traecode` | Passed as `traecli exec --profile <config>`; profile file is `~/.trae/<config>.traecli.toml`. |
| `kimi` | `kimi_code`, `kimi_cli` | Usually omitted; Kimi reads `~/.kimi-code/config.toml`. |
| `opencode` | `open_code` | No runtime-specific `config` mapping. |
| `dsh` | `deepseek_harness`, `deepseek_harness_cli` | Optional trusted extra `--patch` path; bundled minimal patch is always applied first. |
| `deepagent` | `deep_agent` | Python library runtime; set `ZEROMDASH_DEEPAGENT_MODEL`. |

`model`, when non-empty, is passed as `--model <model>` for CLI-backed runtimes
except DSH. TraeX also accepts `ZEROMDASH_TRAEX_BIN` (default resolution:
`traecli`, then `traex`) and `ZEROMDASH_TRAEX_MODEL`. DSH provider/model
selection is written to invocation-local `settings.yaml`, because the headless
profile does not support `--model`.
Provider-specific environment handling currently exists for `claude_code` +
`provider: bedrock` and DSH invocation-local provider/model settings.

## Workflow

The main workflow is:

```text
fetch_target_repo
  -> prepare_scan_scope
  -> search_spec
  -> search_fuzz_driver
  -> search_similar_software -> N x search_similar_history
  -> search_target_history
  -> search_new_feature
  -> analyze_attack_surface
  -> plan_by_spec / plan_by_vuln_similar / plan_by_vuln_patch / plan_by_new_feature
  -> N x subtask loops:
       investigate_subtask -> critic_subtask -> revise/finalize
  -> materialize_chain_pool -> plan_chains
  -> N x chain subtask loops:
       chain_investigate_subtask -> chain_critic_subtask -> revise/finalize
  -> prepare_report_groups
  -> summary
```

First-level subtasks end in one of several terminal states. A result whose root
cause already violates a security contract with direct C/I/A impact becomes a
standalone finding and is scored with CVSS v4.0. A result whose mechanism,
reachability, attacker control, and gained capability are confirmed by the
critic — but which cannot close into a vulnerability on its own — is persisted
as a confirmed primitive under `log/primitive_res/` instead of being dropped.
It is not scored and never reported as a vulnerability by itself.

The chain stage then consumes both standalone findings (as proven capability
sources) and confirmed primitives. `analyze_attack_surface` also materializes
`main/attack_surface/domain_invariant_registry.json`, a domain-adaptive registry
of entities, representations, invariants, transitions, and cross-component
seams shared by initial and chain agents. `plan_chains` first runs a deterministic
bounded advisory prefilter over `required_capabilities` and `capabilities_gained` (max
chain length, per-capability successor cap, beam width, and candidate cap),
writing the exact-match candidate audit trail to `log/review_log/chain_prefilter.json`
and pruning reasons to `log/review_log/chain_pruning.jsonl`. These matches and
mismatches are not final security decisions. A native-subagent-capable planning
agent reads the primitive pool, registry, and prefilter output and produces the final
`log/state/chain_plan.json`, so semantic near-matches and handoff evidence
can be considered before dispatch. Surviving agent-planned candidates fan out to
chain investigate/critic battles that verify attacker entry, per-edge
prerequisite bindings, cross-component handoff objects, and terminal impact.
Only an end-to-end closed chain whose primitives and per-edge semantic bindings
are all confirmed and that
produces direct C/I/A impact is written to `log/chain_res/` as a chain finding
scored on the complete attack chain. The final impact may emerge only from the
composition; no individual primitive needs to carry terminal impact. Unclosed combinations stay retained as
primitives/candidates and are never dressed up as vulnerabilities. `summary`
consumes report groups built from standalone findings and chain findings,
deduplicated by final root cause and attack path so a standalone finding is not
double-counted as both an individual report and a chain component.

`full` is the default and preserves repository-wide scanning. In `diff` mode,
the complete patched repository remains available for call-graph, type,
configuration, and sibling-path analysis. The diff only controls attribution,
priority, and whether a finding can block the change.

Diff mode has no implicit numeric task cap. `analyze_attack_surface` first
creates a canonical `## Diff Risk Surface Registry`: each `RS-XXX` represents
one changed-code anchor, root cause, untrusted-input-to-sink data flow, and
security invariant. The four planners attach spec/CVE/patch/feature evidence to
those risk surfaces instead of creating one task per evidence item.

For each planner, `plan_by_*.candidates.json` keeps the raw candidate audit
trail, `plan_by_*.json` keeps the diff-attributable plan after same-bucket
`risk_surface_id` convergence, and `plan_by_*.convergence.json` records the
mapping and omission reasons. `dispatch_plan.json` then records cross-bucket
convergence and the actual fan-out. Adjacent or pre-existing checks without a
concrete diff-to-sink path are retained only in the candidate trail. Full mode
keeps the existing repository-wide planning and dispatch behavior.
Diff-mode Sends are ordered round-robin across spec, vuln, patch, and feature
buckets so one large planner result cannot occupy all concurrency slots.

`--diff-file` and `--diff-git` are mutually exclusive. `--diff-git` is for
remote git targets: the fetch stage preserves `.git`, the scope stage resolves
or fetches both refs, checks out the `after` commit, and generates the two-dot
`before..after` diff. Tags, branches, and commit SHAs are accepted.

`--disable-spec` removes `search_spec` and `plan_by_spec`.
`--disable-target-history` removes `search_target_history` and
`plan_by_vuln_patch`.
`--disable-new-feature` removes `search_new_feature` and
`plan_by_new_feature`.
`--disable-chain` skips chain candidate planning and chain battles
(`plan_chains` writes an empty plan); confirmed primitives are still persisted
and standalone findings continue to report grouping and summary.

`search_target_history` writes both `main/writeup/_index.md` and the canonical
`main/patch/_patch_commits.json`. The JSON uses patch-manifest schema v1.0 for
both single-repository and multi-repository targets: `repositories[]` records
the checked-out identities, `coverage[]` contains exactly one result for every
repository (including `no_public_history`), and flat `findings[]` records carry
an explicit `repo_id` plus patch reachability evidence. The orchestrator rejects
missing repositories, missing coverage, unknown repo ids, and target-specific
top-level layouts before allowing `plan_by_vuln_patch` to run. Existing
workspaces keep their old artifacts; rerun `search_target_history` to generate
the v1 manifest.

`--till-node analyze` stops after `main/attack_surface/attack_surface.md` and
`domain_invariant_registry.json` are created and valid. `--till-node plan` stops after all enabled planners have
created valid plan JSON under `log/state/`.

`--start-from-subtask <workspace>` reuses an existing workspace and starts from
the subtask fan-out stage. The workspace must already contain a source tree,
`main/attack_surface/attack_surface.md`, and planner files
`log/state/plan_by_spec.json`, `plan_by_vuln.json`, and
`plan_by_patch.json`. `plan_by_feature.json` is loaded when present; older
workspaces without the feature track remain restorable.
Restore readers prefer each canonical file under `log/state/` and fall back to
the same filename under legacy `log/review_log/`. Subtask-result readers merge
legacy `log/review_res/` with `log/subtask_res/`, with a same-named canonical
file taking precedence. New runs write only the canonical locations.

With `--select-subtask-to-run`, ZeroMDASH validates and normalizes the
requested IDs against those planner files, then reruns only the selected
subtask graphs. Compact IDs such as `spec012` normalize to `spec-012`.
Canonical `log/subtask_res/*.json`, `log/review_log/*.log`,
`log/agent_commands.jsonl`, summaries, and `final_state.json` remain unchanged.
The selected run stops after status collection and never runs summary.

By default, selected outputs go to a new
`log/selected_temp_<UTC timestamp>/` directory. An explicit
`--select-subtask-to-run-log-dir <DIR>` overrides it; relative paths resolve
under the restored workspace and the directory must not already exist. The
isolated directory contains `attempts/`, `investigations/`,
`critic_reviews/`, `results/`, `agent_commands.jsonl`,
`selected_subtask_statuses.json`, and its own `final_state.json`. Result JSON
retains both the final `finding` and complete per-iteration `history`.

The former `--start-from-subagent`, `--select-subagent-to-run`, and
`--select-subagent-to-run-log-dir` spellings remain accepted as deprecated
compatibility aliases. In current terminology, `subagent` refers only to a
native child agent spawned inside a capable harness.

`--start-from-chain <workspace>` reuses an existing workspace and starts at
chain planning. It reloads findings from `log/subtask_res/*.json` and primitives
from `log/primitive_res/*.json`, rebuilds the chain pool, re-plans candidates
into `log/state/chain_plan.json`, and continues through chain battles,
report grouping, and summary.

With `--select-chain-to-run`, ZeroMDASH reruns only the selected chain IDs
(stable `chain_<hash>` identifiers from `chain_plan.json`). The selected run
stops after chain status collection and never runs summary. Outputs go to a new
`log/selected_chain_runs/<timestamp>/` directory, or to an explicit
`--select-chain-to-run-log-dir <DIR>`; canonical `log/chain_res/*.json` and
summaries remain unchanged.

`--start-from-summary <workspace>` reuses an existing workspace and runs only
the `summary` node. The workspace must contain `workspace.json`, a non-empty
`main/repo/`, a non-empty `main/attack_surface/attack_surface.md`, and
`log/subtask_res/*.json`. It reloads the finding objects serialized in
`subtask_res` and groups them by `kind`; this is a report-regeneration path, not
a fresh critic run. Summary admission is still deterministic: legacy findings
without a passed vulnerability-qualification gate and valid CVSS v4.0 Base
vector are kept as non-vulnerability observations rather than promoted to
`VULN-XXX`.

Malformed or incomplete investigation output is retried without consuming an
investigate/critic iteration. Before each attempt, ZeroMDASH removes stale
`finding.json`, `investigation.json`, and `output.json` files from that
invocation's sub-workspace. Stdout has priority; only when stdout is invalid
may a JSON artifact freshly created by the current attempt be accepted, and it
must pass the same non-empty title/detail, `evidence.code_locations`, and
`evidence.call_path` contract. Invalid investigations never reach the critic or
become persisted findings. Attempt logs record the output source and separate
stdout/artifact validation failures.

For DSH investigations, a subprocess timeout can still recover a fresh,
non-empty `finding.json` created by that invocation. The adapter only admits a
new parseable JSON object as an artifact candidate; the normal investigation
validator still enforces the complete schema before the attempt is accepted.
Missing, stale, empty, malformed, or contract-invalid files do not mask the
timeout.

For diff-mode runs, `main/scope/` contains `scope.json`, `changes.diff`,
`changed_files.txt`, `changed_symbols.json`, and `change_summary.md`.
`gate_result.json` classifies findings as blocking, warning, or ignored. Only
qualified vulnerabilities whose code-computed CVSS v4.0 severity is high or
critical, attributed as `introduced`, `enabled`, or `regressed`, with a concrete
diff-to-sink causal path, block the change. The critic must first classify each
result as a confirmed/configuration vulnerability, known CVE patch gap,
hardening recommendation, expected behavior, insufficient evidence, or
no-finding. Only the two vulnerability dispositions receive CVSS scores.
Pre-existing and unrelated findings are non-blocking.

`gather` is a separate second-stage graph. It does not fetch or rescan targets.
It snapshots the selected workspaces' attack-surface, primitive, subtask, and
chain artifacts; namespaces every source id by target; synthesizes a
scenario-level cross-target registry; and runs Agent-Native planning plus
investigate/critic battles over candidates that cross at least two targets.
Source-workspace findings remain evidence and are not reported again as new
vulnerabilities. The detailed architecture and evidence contracts are in
[`docs/GATHER_CHAIN.md`](docs/GATHER_CHAIN.md).

## Observability (optional)

```bash
pip install -e ".[observability]"
export LANGFUSE_PUBLIC_KEY=pk-...
export LANGFUSE_SECRET_KEY=sk-...
```

All LangGraph node invocations are traced to Langfuse.

## PoC Generation

Set `poc.enabled=true` and configure the individual PoC phase nodes to continue
into PoC generation after the normal summary/polish stages. The `poc_gen` graph
node only orchestrates the workflow; the seven phase nodes have independent
headless Agent runtime/config/fallback settings. The default is disabled. Use
`--till-node summary` to stop before polish and PoC generation even when enabled.

Completed workspaces can be used directly without `--target`:

```bash
# All qualified report groups
zeromdash --only-gen-pocs .zeromdash/workspace_for_curl --agent-config ./agents.yaml

# One report-group ID; subtask_id and chain_id aliases are also accepted
zeromdash --only-gen-poc .zeromdash/workspace_for_curl:VULN-001 --agent-config ./agents.yaml
```

Both workspace forms accept absolute or relative paths. Results are written to
`log/poc_res/`, attempt evidence under `poc/`, and release packages with
`README.md`, `repro_report.md`, `manifest.json`, PoC files, and evidence under
`deliverables/poc/`.

The current `agent_sandbox` backend executes through the selected Agent runtime's
sandbox. It is not a separate container/VM isolation boundary for hostile code;
see [`docs/POC_GEN.md`](docs/POC_GEN.md) for the evidence gates and limitations.

## Requirements

- Python ≥ 3.10
- The default workflow uses both [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and [Codex CLI](https://github.com/openai/codex): fetch/search/summary default to `claude_code`, while attack-surface analysis, planning, investigation, and critic default to `codex`.
- [Kimi Code](https://moonshotai.github.io/kimi-code/),
  [OpenCode](https://github.com/opencode-ai/opencode),
  [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness), and
  `deepagent` are optional runtimes. They only need to be installed/configured
  when `--agent-config` maps enabled nodes to them.

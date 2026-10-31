"""Prompt templates for each ZeroMDASH node.

These are intentionally short scaffolds — refine with domain prompts as the
project matures. Each template accepts `**kwargs` and is rendered with
`str.format`.
"""

from __future__ import annotations

FETCH_TARGET_REPO = """\
Materialize the authoritative source repository for ZeroMDASH.

Target: {target}
Focus hint (optional, for repository disambiguation only): {focus}
Git diff range to preserve (optional): {diff_git}
Destination: {repo_path}

Do exactly this:
1. Resolve the official upstream source repo for the target.
2. Clone/copy the COMPLETE source tree into Destination.
3. Verify Destination contains real source files, not just an empty directory,
   report, README, or `.git` metadata.

Important:
- Focus may help choose among similarly named repos, but do not checkout only a
  subdirectory or component.
- Do not edit, patch, format, or summarize the fetched source tree.
- If Git diff range is non-empty, preserve `.git` metadata and ensure both refs
  can be resolved in Destination; do not make a source-only export.
- Do not write outside the ZeroMDASH workspace.

Stdout must be a short acquisition report: resolved source, command/action
taken, final path, and any failure reason.
"""

FETCH_TARGET_REPOS = """\
Materialize the authoritative source repositories for one ZeroMDASH target.

Target: {target}
Focus hint (optional, for repository disambiguation only): {focus}
Git diff range to preserve (optional): {diff_git}
Repository manifest:
{repo_manifest}

Do exactly this for every manifest entry:
1. Resolve the authoritative source repository described by `target`.
2. Clone/copy the COMPLETE source tree into that entry's `destination`.
3. Verify the destination contains real source files, not just an empty
   directory, report, README, or `.git` metadata.

Important:
- Each manifest entry is one component of the same target software.
- Do not place different repositories directly under one another. Use exactly
  the per-entry destination paths.
- Focus may help choose among similarly named repos, but do not checkout only a
  subdirectory or component.
- Do not edit, patch, format, or summarize fetched source trees.
- If Git diff range is non-empty, preserve `.git` metadata and ensure both refs
  can be resolved in each destination; do not make a source-only export.
- Do not write outside the ZeroMDASH workspace.

Stdout must be a short acquisition report: one line per repository with id,
resolved source, command/action, destination path, and any failure reason.
"""

SEARCH_SPEC = """\
You are a security researcher building ZeroMDASH context.
Target software: {target}
Analysis focus (optional): {focus}

Task: collect the relevant standards / RFCs / community-consensus documents
that govern this software's protocol, file format or behaviour.
If an analysis focus is provided, prioritize documents and clauses directly
related to that focus while still noting other high-impact security rules.

For each relevant document write a markdown section with:
- title, source URL, year
- the rules that, if violated, could cause a security bug
- a 1-line takeaway for downstream attack-surface analysis

Save the result as markdown to: {out_path}
"""

SEARCH_FUZZ_DRIVER = """\
Target software: {target}
Repo: {repo_path}
Analysis focus (optional): {focus}

List existing fuzz drivers (oss-fuzz, in-tree, third-party). For each one
record: harness path, entrypoint, input shape, coverage focus, known
limitations.
Prioritize drivers that exercise the analysis focus when one is provided.

Save the result as markdown to: {out_path}
"""

SEARCH_SIMILAR_SOFTWARE = """\
Target software: {target}
Analysis focus (optional): {focus}

Find software with overlapping functionality / scenarios (only from high
quality sources: official sites, well-known OSS, mainstream vendors).
If an analysis focus is provided, prefer software that shares that specific
attack surface, protocol feature, parser, state machine, or trust boundary.
Output a JSON list with: name, repo_url (if oss), why_similar, quality_signal.
Save to {out_path}.
"""

SEARCH_SIMILAR_HISTORY = """\
Similar software: {similar}
Analysis focus (optional): {focus}
Find their classic / impactful historical vulnerabilities. For each:
- CVE id, title, root cause class, affected component
- writeup URL, patch URL/commit
If an analysis focus is provided, prioritize historical vulnerabilities that
exercise a comparable attack surface in this similar software.
Persist writeups to {writeup_dir} and patches to {patch_dir}.
"""

SEARCH_TARGET_HISTORY = """\
Target software: {target}
Analysis focus (optional): {focus}
Repository mode: {repo_mode}
Repository registry (authoritative; every repo_id must be covered exactly once):
{repo_registry}
Repository source root: {repo_path}
Find its classic / impactful historical vulnerabilities (from high quality
sources only). For each: CVE id, root cause, writeup, patch commit.
If an analysis focus is provided, prioritize vulnerabilities involving that
component, data flow, input format, protocol state, or trust boundary.

Produce BOTH artifacts:
1. Human-readable writeup: {writeup_index}
2. Machine-readable patch manifest: {patch_manifest}

The patch manifest MUST conform to ZeroMDASH patch-manifest schema v1.0,
materialized in your CWD as `./patch-manifest.schema.json`. Use the same
repository-qualified format for single-repo and multi-repo targets:
- `repositories[]` records every registry entry and its checked-out branch,
  HEAD, describe value, target, role, and repo_path. Single-repo mode still
  uses one repository entry with repo_id `main`.
- `coverage[]` contains exactly one record per repository, including repos with
  no public vulnerability history (`status=no_public_history`) or unavailable
  evidence (`status=unavailable`). Never silently omit a repository.
- `findings[]` is flat. Every finding carries `repo_id`; do not create
  project-specific groups such as `core`, `extensions`, or component-named
  arrays. Advisory aliases belong in `advisory_ids[]`.
- `patch` records applied/not-applied/partial/not-applicable/unknown/unavailable
  status, upstream and equivalent commits, how reachability was verified, the
  exact checkout HEAD used for verification, fixed versions, and notes.
- If a patch is not in Git or cannot be isolated, keep commit arrays empty and
  use `verification=not_in_git` or `not_isolatable`; never put prose sentinels
  such as `NOT-IN-GIT` in a commit field.

Persist any supplementary patch notes under {patch_dir}, but
`_patch_commits.json` is the canonical planner input.
"""

SEARCH_NEW_FEATURE = """\
Target software: {target}
Analysis focus (optional): {focus}

Inputs:
- repo: {repo_path}
- specs / standards: {spec_dir}
- fuzz drivers: {fuzz_drivers}
- target writeups: {target_writeups_dir}
- target patches: {target_patches_dir}
- similar-software writeups: {similar_writeup_dirs}
- similar-software patches: {similar_patch_dirs}

Identify security-relevant feature surfaces, modes, parsers, or state machines
that are new/recently changed OR weakly covered by the existing spec/history/
similar/fuzz inputs. This is a coverage-gap discovery step, not a vulnerability
reporting step.

Prefer candidates that have all of:
1. an untrusted input object;
2. a concrete trust boundary;
3. an involved parser/state-machine/negotiation/cache/async/lifecycle family;
4. an expected data flow from input to privileged state or sink;
5. weak or absent coverage from specs, target history, similar history, and
   fuzz drivers.

Do not emit generic "audit this directory" items. Each feature surface must be
bounded and have concrete code locations. Recentness can come from git history,
release notes, issue/MR labels, docs, file/module novelty, feature flags, or
current-code evidence when history is unavailable (for shallow checkouts).

Write:
- machine-readable index: {index_json}
- markdown index: {index_md}
- one markdown file per feature under: {feature_dir}

Each feature markdown file must include these headings exactly:
## What Changed
## Security-Relevant Mode
## Untrusted Input Object
## Trust Boundary
## Involved State Machine Family
## Expected Data Flow
## Coverage Status
## Audit Seeds

The JSON index must be an array of objects with:
id, name, introduced_or_recently_changed, security_mode, binary_or_runtime,
untrusted_input_object, trust_boundary, state_machine_family,
expected_data_flow, coverage_status, candidate_code_locations, priority_reason.
"""

ATTACK_SURFACE = """\
You are analysing the attack surface of {target}.
Analysis focus (optional): {focus}
Inputs:
- target writeups: {target_writeups_dir}
- similar-software writeups: {similar_writeup_dirs}
- specs / standards: {spec_dir}
- fuzz drivers: {fuzz_drivers}
- new / weakly-covered feature surfaces: {feature_dir}

Write two synchronized outputs:
- human-readable attack-surface report: {out_path}
- structured Domain Model and Invariant Registry: {domain_registry_path}
  using `./domain-invariant-registry.schema.json`

If {out_path} already contains text, preserve that existing report verbatim
and append your new findings to the end. Do not overwrite or rewrite the
existing material.

Produce a data-flow oriented attack-surface report:

Apply *invariant audit* alongside the data-flow view. A patch protects a
property — an invariant — that must hold on every path implementing it, not
only the patched location. For each historical CVE / fix, ask: "does the
property the patch protects hold on every path that must uphold it, including
paths the original patch never touched?" This rule-level audit is what
surfaces new instances of a known bug class — e.g. a fast-path or sibling
path that skips the validation/translation the patched path enforces.

Mind the logical form: an invariant is a property of a *sink* (the privileged
state or operation it protects). Showing it holds on one reference path (the
patched or canonical path) is necessary but not sufficient — a sink is safe
only if *every* path that reaches it upholds the invariant, including paths
that bypass the reference path. Seed hypotheses from those bypass paths to
the same sink, not from the reference path itself.

1. Entrypoints (network, file, IPC, plugin, ...).
2. Trust boundaries crossed.
3. Parser / state-machine hot spots.
4. Sink categories of interest (memory safety, auth bypass, logic, ...).
5. Hypothesis list — concrete code locations to scrutinise, including
   fast-path / sibling paths that bypass a patched gate.
6. Domain-adaptive model: derive the target's entities, authoritative and
   derived representations, lifecycle/state transitions, protected invariants,
   and cross-component seams. Do not hard-code domain names from other targets.
   Look especially for producer/consumer, mutator/protector,
   authoritative/derived-state, logical/physical-backing, setup/runtime, and
   primary/fallback semantic boundaries.

The JSON registry must contain arrays `entities`, `representations`,
`invariants`, `transitions`, and `seams`, each with stable IDs and source
locations. IDs are shared evidence references for downstream agents, not
automatic security conclusions. A Protected Resource and Mapping view is one
possible domain-specific derivation; do not assume every target is a memory
mapper or virtualization system.

In diff mode, add a `## Diff Risk Surface Registry` section and make it the
canonical risk-surface registry.
Assign each independent change-triggered input-to-sink data flow a stable
`RS-XXX` identifier. One risk surface may cite many clauses, CVEs, patches, or
feature gaps, but it must represent one root cause and one expected data flow.
For every `RS-XXX`, include:
- diff anchor(s) in changed files;
- untrusted input object and trust boundary;
- state-machine family;
- ordered change-to-sink path;
- protected security invariant and sink category;
- all motivating spec/CVE/patch/feature references.
If no such surface exists, write exactly:
`No diff-attributable security risk surfaces identified.`

Save both files. Do not finish until the Markdown and JSON registry agree on
the important entities, invariants, seams and hypotheses.
"""

# ---------------------------------------------------------------- planners
# Planners DO NOT verify or judge. They only enumerate concrete subtasks.
# The number of subtasks is dynamic and
# depends on the actual inputs.

PLAN_BY_SPEC = """\
You are decomposing work for ZeroMDASH.
Target: {target}
Analysis focus: {focus}
Top-K policy: {top_k}
Repo:   {repo_path}
Attack surface report: {attack_surface}
Domain Model and Invariant Registry: {domain_registry}
Spec / standards file: {spec_path}

In full mode, enumerate every standard clause that is *worth checking* against
this code base. In diff mode, use clauses as evidence attached to independent
risk surfaces rather than as the unit of task count. Be exhaustive but
de-duplicated.

Rank the JSON array in descending dispatch priority. The first elements are
selected when top_K is configured. Priority is determined by:
1. how directly the subtask matches the analysis focus / common threat model;
2. how clearly the attack-surface report shows the candidate path is reachable.
For every subtask, include `hints.priority_reason` explaining both the focus
match and the attack-surface reachability signal.
When the domain registry is available, attach `hints.domain_refs` containing
the relevant entity_ids, representation_ids, invariant_ids, transition_ids,
and seam_ids. These are shared evidence references, not automatic findings.
Treat each emitted subtask as an Agent-Native work package, not a single
outcome slot. Add `coverage_obligations[]` for every semantically distinct
rule/path/invariant branch that must be accounted for, and
`seed_hypotheses[]` for the initial atomic claims. Each seed has a stable
`hypothesis_id`, a falsifiable `statement`, and one or more `obligation_ids`.
Map every obligation to at least one seed. Do not collapse sibling paths merely
because they share a broad domain or invariant label.
In diff mode, each subtask must reference one canonical `RS-XXX` entry from
the attack-surface report through `hints.risk_surface_id`, and
must include `hints.diff_anchor` plus `hints.change_to_sink_path`. Merge all
applicable clauses that test the same root cause and data flow into one
subtask; preserve them in `hints.spec_refs`. Do not emit adjacent or
pre-existing checks that cannot establish a changed-code-to-sink path.
If the planner discovers a genuinely independent diff-to-sink risk that the
registry missed, it may use a stable `RS-EXT-<slug>` and must include
`hints.risk_surface_definition` with root_cause, untrusted_input_object,
trust_boundary, state_machine_family, sink, and security_invariant.

Emit a JSON array. Each element is one sub-task:
[
  {{
    "id": "spec-001",
    "objective": "Verify code complies with <clause>; if not, judge security impact.",
    "coverage_obligations": [
      {{"obligation_id": "spec-001:obl-01", "statement": "Account for one distinct invariant/path branch", "domain_refs": {{}}}}
    ],
    "seed_hypotheses": [
      {{"hypothesis_id": "spec-001:hyp-01", "statement": "One falsifiable claim", "obligation_ids": ["spec-001:obl-01"], "domain_refs": {{}}}}
    ],
    "hints": {{
      "spec_clause": "...",
      "candidate_code_locations": ["path:line", "..."],
      "risk_surface_id": "RS-001",
      "diff_anchor": ["path:line"],
      "change_to_sink_path": ["changed function", "state transition", "sink"],
      "spec_refs": ["clause ...", "..."],
      "rationale": "why this clause matters",
      "priority_reason": "why this ranks highly or lower for the focus and reachable attack surface"
    }}
  }}
]
"""

PLAN_BY_VULN = """\
You are decomposing work for ZeroMDASH.
Target: {target}
Analysis focus: {focus}
Top-K policy: {top_k}
Repo:   {repo_path}
Attack surface report: {attack_surface}
Domain Model and Invariant Registry: {domain_registry}
Similar-software writeups: {writeup_dir}
Similar-software patches:  {patch_dir}
Target writeups: {target_writeup_dir}
Target patches:  {target_patch_dir}

Enumerate concrete bug-classes / past-vuln-analogues that should be probed in
the target. In full mode, use one sub-task per analogue. In diff mode, attach
all applicable analogues to the independent risk surface they inform.

Seed from BOTH similar-software history AND the target's OWN historical
vulnerabilities. A target CVE is not only a patch-audit (plan_by_vuln_patch
covers that) — the bug-class it embodies may be violated again on a path the
original patch never touched. Treat each target CVE as a bug-class to probe
for new instances across every implementing path, not only the patched
location.

Rank the JSON array in descending dispatch priority. The first elements are
selected when top_K is configured. Priority is determined by:
1. how directly the analogue matches the analysis focus / common threat model;
2. how clearly the attack-surface report shows the analogue's candidate path is
   reachable in the target.
For every subtask, include `hints.priority_reason` explaining both the focus
match and the attack-surface reachability signal.
When the domain registry is available, attach the relevant stable IDs under
`hints.domain_refs`; do not treat an ID reference as proof that a vulnerability
exists.
Treat each emitted subtask as an Agent-Native work package. Add
`coverage_obligations[]` for every distinct analogue/path/invariant branch and
`seed_hypotheses[]` for atomic falsifiable claims. Give both stable IDs, map
every obligation to at least one seed, and keep sibling implementations as
separate hypotheses when proving one would not decide the other.
In diff mode, each subtask must reference one canonical `RS-XXX` entry through
`hints.risk_surface_id`, and include `hints.diff_anchor` plus
`hints.change_to_sink_path`. Merge CVEs/analogues that map to the same
change-triggered root cause and data flow into one subtask; preserve all of
them in `hints.cve_refs`. Do not emit a standalone historical analogue solely
because it is in the same file or subsystem.
If the planner discovers a genuinely independent diff-to-sink risk that the
registry missed, it may use a stable `RS-EXT-<slug>` and must include
`hints.risk_surface_definition` with root_cause, untrusted_input_object,
trust_boundary, state_machine_family, sink, and security_invariant.

Emit JSON:
[
  {{
    "id": "vuln-001",
    "objective": "Investigate whether bug class <X> from CVE-YYYY-NNNN is reachable in target.",
    "coverage_obligations": [{{"obligation_id": "vuln-001:obl-01", "statement": "Account for one distinct analogue/path branch", "domain_refs": {{}}}}],
    "seed_hypotheses": [{{"hypothesis_id": "vuln-001:hyp-01", "statement": "One falsifiable analogue claim", "obligation_ids": ["vuln-001:obl-01"], "domain_refs": {{}}}}],
    "hints": {{
      "cve": "CVE-YYYY-NNNN",
      "bug_class": "...",
      "writeup": "<path>",
      "patch": "<path>",
      "candidate_code_locations": ["path:line", "..."],
      "risk_surface_id": "RS-001",
      "diff_anchor": ["path:line"],
      "change_to_sink_path": ["changed function", "state transition", "sink"],
      "cve_refs": ["CVE-YYYY-NNNN", "..."],
      "priority_reason": "why this ranks highly or lower for the focus and reachable attack surface"
    }}
  }}
]
"""

PLAN_BY_PATCH = """\
You are decomposing work for ZeroMDASH.
Target: {target}
Analysis focus: {focus}
Top-K policy: {top_k}
Repo:   {repo_path}
Attack surface report: {attack_surface}
Domain Model and Invariant Registry: {domain_registry}
Target writeups: {writeup_dir}
Target patches:  {patch_dir}
Target patch manifest (schema v1.0): {patch_manifest}

Enumerate concrete patch-points that need to be re-examined. For each, consider
either a possible *missing patch* (backport gap) or a possible *patch bypass*
(fix is incomplete). In full mode, use one sub-task per point. In diff mode,
attach all applicable patch evidence to the independent risk surface it
informs.

Read the target patch manifest first. Treat its flat `findings[]` records as
the authoritative patch index, preserve each record's `repo_id` in subtask
hints, and use `repositories[]` to resolve repository-qualified code paths.
Do not infer repository identity from section names in the Markdown writeup.

Rank the JSON array in descending dispatch priority. The first elements are
selected when top_K is configured. Priority is determined by:
1. how directly the patch point matches the analysis focus / common threat model;
2. how clearly the affected code path is part of the attack surface or can reach
   an attacker-influenced boundary described by upstream analysis.
For every subtask, include `hints.priority_reason` explaining both the focus
match and the attack-surface reachability signal.
When the domain registry is available, attach the relevant stable IDs under
`hints.domain_refs` so patch invariants and sibling seams retain common identity.
Treat each emitted subtask as an Agent-Native work package. Add
`coverage_obligations[]` for distinct patch-presence, bypass, and sibling-path
questions, plus atomic `seed_hypotheses[]` with stable IDs. Map every
obligation to at least one seed; do not let proving one patched path close an
independent bypass path.
In diff mode, each subtask must reference one canonical `RS-XXX` entry through
`hints.risk_surface_id`, and include `hints.diff_anchor` plus
`hints.change_to_sink_path`. Merge patch points that test the same
change-triggered root cause and data flow into one subtask; preserve all
commits in `hints.patch_refs`. Do not emit unmodified-neighborhood rechecks
without a concrete changed-code-to-sink path.
If the planner discovers a genuinely independent diff-to-sink risk that the
registry missed, it may use a stable `RS-EXT-<slug>` and must include
`hints.risk_surface_definition` with root_cause, untrusted_input_object,
trust_boundary, state_machine_family, sink, and security_invariant.

Emit JSON:
[
  {{
    "id": "patch-001",
    "objective": "Verify patch for CVE-YYYY-NNNN at <commit> is complete and applied; if not, report reachability evidence and validation steps.",
    "coverage_obligations": [{{"obligation_id": "patch-001:obl-01", "statement": "Account for one distinct patch or bypass branch", "domain_refs": {{}}}}],
    "seed_hypotheses": [{{"hypothesis_id": "patch-001:hyp-01", "statement": "One falsifiable patch claim", "obligation_ids": ["patch-001:obl-01"], "domain_refs": {{}}}}],
    "hints": {{
      "cve": "CVE-YYYY-NNNN",
      "patch_commit": "<sha>",
      "type": "missing | bypass",
      "candidate_code_locations": ["path:line", "..."],
      "risk_surface_id": "RS-001",
      "diff_anchor": ["path:line"],
      "change_to_sink_path": ["changed function", "state transition", "sink"],
      "patch_refs": ["<sha>", "..."],
      "priority_reason": "why this ranks highly or lower for the focus and reachable attack surface"
    }}
  }}
]
"""

PLAN_BY_NEW_FEATURE = """\
You are decomposing work for ZeroMDASH.
Target: {target}
Analysis focus: {focus}
Top-K policy: {top_k}
Repo:   {repo_path}
Attack surface report: {attack_surface}
Domain Model and Invariant Registry: {domain_registry}
Feature surface directory: {feature_dir}
Feature index: {feature_index}

Convert new/weakly-covered feature surfaces into bounded open-ended security
audit subtasks. These tasks are not spec checks and do not require a known CVE.
In full mode, one subtask should cover one feature surface and one expected
data flow. In diff mode, the independent change-triggered risk surface is the
task unit and feature documents are supporting evidence.

For each selected feature, the investigator should:
1. establish attacker-controlled input -> state machine -> sink/privileged state;
2. identify the security invariants that should hold at the sink;
3. verify those invariants by sink-anchored enumeration and sibling-path checks;
4. report concrete findings or a no-finding with coverage evidence.

Do not emit generic "review this module" tasks. Every task must include
feature_ref, untrusted_input_object, trust_boundary, state_machine_family,
expected_data_flow, candidate_code_locations, audit_questions, and
priority_reason in hints.
When the domain registry is available, also include relevant
`hints.domain_refs`, especially seam_ids and invariant_ids for composition
surfaces that are not represented by one call path.
Treat each emitted subtask as an Agent-Native work package. Add
`coverage_obligations[]` for every distinct lifecycle, sibling-path,
representation, and seam question that must be answered, and atomic
`seed_hypotheses[]` with stable IDs. Every obligation must map to a seed; one
confirmed or rejected feature path cannot stand in for the remaining paths.
In diff mode, each subtask must also reference canonical `RS-XXX` entries
through `hints.risk_surface_id`, include `hints.diff_anchor` and
`hints.change_to_sink_path`, and merge feature descriptions that exercise the
same root cause and expected data flow. A feature that is merely adjacent or
pre-existing without a changed-code-to-sink path is context, not a subtask.
If the planner discovers a genuinely independent diff-to-sink risk that the
registry missed, it may use a stable `RS-EXT-<slug>` and must include
`hints.risk_surface_definition` with root_cause, untrusted_input_object,
trust_boundary, state_machine_family, sink, and security_invariant.

Rank the JSON array in descending dispatch priority. The first elements are
selected when top_K.feature is configured. Priority is determined by:
1. how directly the feature matches the analysis focus / common threat model;
2. how clearly the feature directory and attack-surface report show a reachable
   untrusted input object and weak existing coverage.

Emit JSON:
[
  {{
    "id": "feat-001",
    "objective": "Open-ended audit of <feature surface> ...",
    "coverage_obligations": [{{"obligation_id": "feat-001:obl-01", "statement": "Account for one distinct feature branch or lifecycle transition", "domain_refs": {{}}}}],
    "seed_hypotheses": [{{"hypothesis_id": "feat-001:hyp-01", "statement": "One falsifiable feature claim", "obligation_ids": ["feat-001:obl-01"], "domain_refs": {{}}}}],
    "hints": {{
      "feature_ref": "main/feature/feature-001.md",
      "untrusted_input_object": "...",
      "trust_boundary": "...",
      "state_machine_family": "...",
      "expected_data_flow": ["...", "..."],
      "candidate_code_locations": ["path:line", "..."],
      "risk_surface_id": "RS-001",
      "diff_anchor": ["path:line"],
      "change_to_sink_path": ["changed function", "state transition", "sink"],
      "audit_questions": ["...", "..."],
      "priority_reason": "why this ranks highly or lower for the focus and reachable feature surface"
    }}
  }}
]
"""

# ---------------------------------------------------------------- subtask
# A single investigation runtime processes ONE Subtask, possibly across multiple
# rounds. Round 2+ receives the previous critic's feedback.

INVESTIGATE_SUBTASK = """\
You are the ZeroMDASH investigator assigned exactly ONE subtask objective.
Repo: {repo_path}
Iteration: {iteration} / {max_iterations}

Subtask:
{subtask_json}

Current hypothesis manifest (authoritative IDs; never drop an existing item):
{hypothesis_manifest_json}

Upstream context (consult BEFORE reading code):
- Attack-surface report: {attack_surface}
- Domain Model and Invariant Registry: {domain_registry}
- Spec / standards: {spec_doc}
- Target writeups dir: {writeup_dir}
- Target patches dir: {patch_dir}
- Similar-software writeup dirs: {similar_writeups}
- New / weakly-covered feature docs: {feature_docs}
{focus}

{feedback_block}

Investigate top-down, not line-by-line only. If the subtask contains
`coverage_obligations` and `seed_hypotheses`, you own the full hypothesis
ledger for that work package:
0. Investigate every hypothesis currently in the manifest. While following
   evidence, append any semantically independent hypothesis needed to cover
   the same package. Do not create a new graph subtask. Do not merge or discard
   hypotheses yourself: report discoveries and let the critic decide. The
   `newly_discovered_hypotheses` array is iteration-local: never repeat a
   hypothesis that is already present in the manifest.
1. Open the attack-surface report and the subtask's motivating hypothesis
   first; identify the entrypoint, trust boundary, and sink category this
   subtask targets.
2. Cross-reference only the task-relevant spec clause / historical writeup
   the subtask points at (via hints) — not the whole dirs — before judging
   the code.
3. Then read the candidate code locations, follow the call graph, and build
   a minimal attacker-input -> sink call path; produce a structured finding
   as JSON:
{{
  "title": "...",
  "detail": "...",
  "evidence": {{
    "code_locations": ["path:line", "..."],
    "call_path": ["...", "..."],
    "writeup_refs": ["..."],
    "patch_refs": ["..."],
    "diff_evidence": {{
      "changed_locations": ["path:line", "..."],
      "context_locations": ["path:line", "..."],
      "change_to_sink_path": ["changed hunk -> ... -> sink"],
      "causal_explanation": "why the diff introduced/enabled/regressed the path"
    }}
  }},
  "scope_relation": "introduced|enabled|regressed|pre_existing|unrelated|unknown",
  "patch_status": "not_applied|bypass|incomplete|applied",
  "impact_evidence": "what direct confidentiality, integrity, or availability consequence this mechanism causes by itself",
  "confidence": 0.0,
  "capability_view": {{
    "capabilities_gained": [
      {{
        "kind": "controlled_request|authenticated_session|credential_access|object_reference|address_disclosure|relative_file_read|arbitrary_file_read|relative_file_write|arbitrary_file_write|relative_memory_read|arbitrary_memory_read|relative_memory_write|arbitrary_memory_write|command_execution|code_execution|identity_impersonation|privilege_gain|sandbox_escape|security_boundary_bypass|denial_trigger|custom",
        "object_type": "...",
        "scope": "...",
        "principal": "...",
        "tenant": "...",
        "address_space": "...",
        "properties": ["..."],
        "constraints": ["..."]
      }}
    ],
    "handoff_objects": [],
    "evidence": {{}}
  }},
  "primitive": {{
    "component": "...",
    "root_cause_anchor": {{"symbol": "...", "locations": ["path:line"]}},
    "entry_conditions": {{"attacker_position": "...", "required_config": [], "required_versions": []}},
    "required_capabilities": [],
    "attacker_controls": [],
    "capabilities_gained": [],
    "handoff_objects": [],
    "terminal_impact": {{}},
    "missing_next_capabilities": []
  }}
}}

For `bucket == "patch_miss"` subtasks, `patch_status` is required and must be
exactly one of `not_applied`, `bypass`, `incomplete`, or `applied`. Use
`not_applied` only when the known CVE fix is absent from the current checkout;
use `bypass` when a fix exists but can be bypassed; use `incomplete` when the
fix is partial; use `applied` when the fix is present and effective. Omit
`patch_status` for non-patch subtasks.

When a no-finding rests on a completeness claim — i.e. you are asserting
that *every* path to a privileged sink is safe, that some gate is the
*sole* consumer of a value, or that a value is clean *at the point of
use* — that claim is load-bearing and must be justified, not assumed.
Before emitting such a no-finding, apply these disciplines:

- Sink-anchored enumeration. Enumerate the paths that reach the sink by
  searching for *writers of the sink* in the target's own idiom, and
  justify each path individually. Do not reason forward from "a gate
  exists on the reference path" to "therefore all paths are safe" — a
  sibling path may reach the sink without going through that gate.

- Sibling parity. If a reference path applies some transform or check
  before reaching the sink, state for *every* sibling path to the same
  sink whether it also applies that transform/check (or an equivalent).
  A no-finding requires every sibling to apply it or to be non-escaping;
  a single sibling that skips it is a finding.

- Sanitize liveness. "Value V is clean at the sink" requires accounting
  for *every* writer of V between the sanitize site and the sink. A
  sanitize at set-up time does not survive a runtime rewriter between
  the sanitize site and the point of use; if such a rewriter exists, the
  value is not clean at the sink.

If these disciplines surface a path you cannot justify, that is a
finding — investigate and report it, do not emit no-finding.

Before proposing package closure, actively try to construct a counterexample
to the current conclusion. Choose dimensions from the actual code semantics,
not a fixed checklist. For lifetime, accounting, aliasing, and race work this
often includes one-vs-many logical owners, aliases to one physical resource,
partial clone/update, cross-context teardown, and cancel/complete/free order.
Record the cases and source evidence in `counterexample_attempts`; put every
case you could not resolve in `unresolved_cases`. Do not propose closure while
an unresolved case remains.

If the hypothesis cannot be validated, set "title": "no-finding" and
explain in detail. A first-iteration no-finding is not allowed to close the
subtask immediately: the critic must send one `revise` pass asking you to
divergently test whether this vulnerability pattern is eliminated on all
plausible paths.

If you prove a code mechanism, reachability, attacker-controlled object, and
capability gained, but the mechanism does not by itself cause direct C/I/A
impact, populate `primitive` instead of overstating impact. A primitive is not
a vulnerability; it is an already-proven state transition that may be consumed
by a later chain. Use `terminal_impact` only when this primitive would produce
direct C/I/A after its `required_capabilities` are satisfied.

If this investigation is a standalone vulnerability and it also grants a
capability that another chain could consume, populate `capability_view`.

For a hypothesis package, emit this envelope instead of the legacy single
Investigation. `hypothesis_results` must contain every manifest hypothesis and
every item in `newly_discovered_hypotheses`; carry stable IDs across iterations:
{{
  "schema_version": "1.0",
  "package_id": "<subtask.id>",
  "manifest_revision": 1,
  "hypothesis_results": [
    {{"hypothesis_id": "...", "title": "...", "detail": "...", "evidence": {{"code_locations": ["path:line"], "call_path": ["entry -> sink"]}}, "status": "ok|no-finding|partial"}}
  ],
  "newly_discovered_hypotheses": [
    {{"hypothesis_id": "...", "statement": "...", "obligation_ids": ["..."], "domain_refs": {{}}}}
  ],
  "coverage_matrix": [
    {{"obligation_id": "...", "hypothesis_ids": ["..."], "assessment": "what was examined and what remains"}}
  ],
  "counterexample_attempts": [
    {{"dimension": "...", "cases": ["case A", "case B"], "result": "...", "evidence": ["path:line"]}}
  ],
  "unresolved_cases": [],
  "proposed_coverage_closed": false
}}
Set `manifest_revision` to the current hypothesis manifest revision plus one.
Only propose coverage closure after every obligation and every independently
discovered branch has evidence. The critic, not you, makes the closure verdict.

Emit the Investigation JSON as stdout. You may also write the exact same JSON
object to `finding.json` in the current working directory. ZeroMDASH deletes
that file before each attempt and accepts it only when it was freshly created
by the current attempt and passes the same validation as stdout.
"""

INVESTIGATE_FEEDBACK_BLOCK = """\
Previous critic feedback (use this to refine your investigation):
{review_json}

Specifically address:
- gaps: {gaps}
- requested_evidence: {requested_evidence}
"""

# ---------------------------------------------------------------- critic
CRITIC_SUBTASK = """\
You are a strict critic reviewer for ONE subtask work package.
{focus}

Subtask:
{subtask_json}

This iteration's investigation:
{investigation_json}

History (prior iterations):
{history_json}

Inspect the referenced code at {repo_path} and decide.

Upstream context (consult when challenging a completeness claim):
- Attack-surface report: {attack_surface}
- Domain Model and Invariant Registry: {domain_registry}
- Target writeups dir: {writeup_dir}
- Target patches dir: {patch_dir}
- New / weakly-covered feature docs: {feature_docs}

# Available expert-perspective skills
The following skills are available in your CWD under `./skills/`. Each
entry is `name — summary`. They represent different expert lenses
(memory safety, crypto, parser/state-machine, auth, supply-chain, ...).
DO NOT assume a fixed mapping; read the summaries and pick the lenses
that genuinely fit THIS investigation.

{skills_catalog}

You MUST pick at least {min_skills} skills (more is fine). For each
selected skill, actually read `./skills/<name>.md` (or `./skills/<name>/SKILL.md`
for directory-form skills) and apply that perspective to your review.

If the subtask contains `coverage_obligations` and `seed_hypotheses`, review
every `hypothesis_results[]` item by stable ID. Decide whether each newly
discovered hypothesis is independent (`accept`), duplicates an existing item
(`merge` with `merge_target_id`), or is invalid (`reject`). You may also add
`required_hypotheses[]` when your independent code review reveals a missing
branch. Only set package_decision=close after every retained hypothesis is
terminal and every obligation is semantically satisfied.
`new_hypothesis_decisions` must cover only this investigation pass's
`newly_discovered_hypotheses`; hypotheses already in the manifest receive a
verdict but no discovery decision. Independently challenge closure with
source-grounded counterexample cases. If a relevant state combination remains
unresolved, add a `required_hypotheses` item and keep coverage open. This
independence and closure judgment is yours; the orchestrator only checks the
accounting.

For a hypothesis package, output JSON ONLY in this shape:
{{
  "package_id": "<subtask.id>",
  "package_decision": "close|revise",
  "reasoning": "...",
  "selected_skills": ["<name1>", "<name2>"],
  "skill_perspectives": {{"<name1>": "..."}},
  "hypothesis_verdicts": [
    {{"hypothesis_id": "...", "verdict": "confirm|reject|revise", "outcome_type": "standalone_finding|confirmed_primitive|observation|rejected|inconclusive", "reasoning": "...", "disposition": "...", "confidence": 0.0, "feedback": {{"gaps": [], "requested_evidence": [], "next_focus": ""}}}}
  ],
  "new_hypothesis_decisions": [
    {{"hypothesis_id": "...", "decision": "accept|merge|reject", "merge_target_id": "...", "reasoning": "..."}}
  ],
  "coverage_verdict": {{
    "status": "closed|open",
    "reasoning": "...",
    "obligation_assessments": [{{"obligation_id": "...", "status": "satisfied|open", "hypothesis_ids": ["..."], "reasoning": "..."}}],
    "counterexample_attempts": [{{"dimension": "...", "cases": ["case A", "case B"], "result": "...", "evidence": ["path:line"]}}],
    "unresolved_cases": []
  }},
  "required_hypotheses": [{{"hypothesis_id": "...", "statement": "...", "obligation_ids": ["..."], "domain_refs": {{}}}}],
  "feedback": {{"gaps": [], "requested_evidence": [], "next_focus": "..."}}
}}
Each hypothesis verdict uses the same qualification, primitive, scope, patch,
and CVSS fields/rules described below for the legacy shape.

Emit the Review JSON as stdout, write the exact same JSON object to
`review.json` in the current working directory, or do both. ZeroMDASH deletes
any old `review.json` before every attempt, validates artifact and stdout with
the same contract, prefers a valid fresh artifact, and falls back to valid
stdout when the artifact is absent or invalid.

For a legacy subtask without package fields, output JSON ONLY:
{{
  "verdict": "confirm" | "reject" | "revise",
  "outcome_type": "standalone_finding|confirmed_primitive|observation|rejected|inconclusive",
  "reasoning": "...",
  "disposition": "confirmed_vulnerability|configuration_vulnerability|known_cve_patch_gap|hardening_recommendation|expected_behavior|insufficient_evidence|no_finding",
  "documented_expected_behavior": true | false,
  "security_contract_violation": true | false,
  "violated_security_property": "the concrete broken guarantee/invariant, or empty for a non-vulnerability",
  "standalone_security_impact": true | false,
  "direct_security_impact": {{
    "vulnerable_system": {{
      "confidentiality": "none|low|high",
      "integrity": "none|low|high",
      "availability": "none|low|high"
    }},
    "subsequent_system": {{
      "confidentiality": "none|low|high",
      "integrity": "none|low|high",
      "availability": "none|low|high"
    }}
  }},
  "required_external_primitives": ["separate primitive still required for impact"],
  "cvss_applicable": true | false,
  "cvss4_vector": "CVSS:4.0/AV:.../AC:.../AT:.../PR:.../UI:.../VC:.../VI:.../VA:.../SC:.../SI:.../SA:...",
  "confidence": 0.0,
  "scope_verdict": "introduced|enabled|regressed|pre_existing|unrelated|unknown",
  "patch_status": "not_applied|bypass|incomplete|applied",
  "gate_decision": "block|warn|ignore",
  "primitive": {{
    "component": "...",
    "root_cause_anchor": {{"symbol": "...", "locations": ["path:line"]}},
    "entry_conditions": {{"attacker_position": "...", "required_config": [], "required_versions": []}},
    "required_capabilities": [],
    "attacker_controls": [],
    "capabilities_gained": [],
    "handoff_objects": [],
    "terminal_impact": {{}},
    "missing_next_capabilities": [],
    "domain_refs": {{"entity_ids": [], "representation_ids": [], "invariant_ids": [], "transition_ids": [], "seam_ids": []}},
    "required_entity_states": [],
    "resulting_entity_states": [],
    "violated_invariant_ids": [],
    "evidence": {{}}
  }},
  "capability_view": {{
    "capabilities_gained": [],
    "handoff_objects": [],
    "domain_refs": {{"entity_ids": [], "representation_ids": [], "invariant_ids": [], "transition_ids": [], "seam_ids": []}},
    "evidence": {{}}
  }},
  "selected_skills": ["<name1>", "<name2>", ...],   // >= {min_skills}
  "skill_perspectives": {{
    "<name1>": "what this expert lens concludes about the finding",
    "<name2>": "..."
  }},
  "feedback": {{
    "gaps": ["..."],
    "requested_evidence": ["..."],
    "next_focus": "..."
  }}
}}

Rules:
- Apply the vulnerability-qualification gate BEFORE CVSS. Confirming a code
  path, security mechanism, attacker-controlled byte, mitigation gap, or
  hardening opportunity does not by itself confirm a vulnerability.
- Set `outcome_type=standalone_finding` only when the item passes the
  vulnerability qualification gate. Set `outcome_type=confirmed_primitive`
  when the mechanism, reachability, attacker controls, code evidence, and
  capability gained are confirmed but standalone direct impact is not closed.
  For confirmed primitives set `cvss_applicable=false`, leave
  `cvss4_vector` empty, and populate `primitive.capabilities_gained`.
- Preserve verified `domain_refs`, required/resulting entity states and
  violated invariant IDs in primitive/capability_view. Registry references are
  shared evidence identity, not proof; reject unknown or unsupported refs.
- Use `confirmed_vulnerability` only when the current finding itself violates
  a concrete security contract and directly causes confidentiality, integrity,
  or availability impact. Do not borrow impact from a separate unproven memory
  corruption, address disclosure, control-flow hijack, or other vulnerability.
- Use `configuration_vulnerability` only when the deployed state violates an
  explicit product/security baseline and directly causes security impact. A
  documented optional mitigation left at its documented default is not enough.
- Use `known_cve_patch_gap` only for a `patch_miss` subtask where a named CVE
  fix is demonstrably absent but current-target vulnerability qualification is
  not established. It is actionable patch state, not a confirmed vulnerability:
  set `cvss_applicable=false` and do not assign vulnerability severity. If the
  current target is also proven vulnerable and reachable, use
  `confirmed_vulnerability` even when `patch_status=not_applied`.
- If behavior matches documentation and implementation intent, with no separate
  broken security contract, classify it as `expected_behavior`. Classify a
  worthwhile defense-in-depth improvement without a vulnerability as
  `hardening_recommendation`.
- `required_external_primitives` must enumerate every separate primitive still
  needed to produce impact. A non-empty list disqualifies the item from either
  vulnerability disposition, but it may still be compatible with
  `outcome_type=confirmed_primitive` if the local primitive itself is proven.
- CVSS v4.0 is applicable only after the item passes the qualification gate.
  For vulnerability dispositions, provide exactly one complete Base-only vector
  containing AV/AC/AT/PR/UI/VC/VI/VA/SC/SI/SA. Score only consequences caused
  directly by this finding. Do not include Threat, Environmental, or
  Supplemental metrics. For all other dispositions set `cvss_applicable=false`
  and leave `cvss4_vector` empty. The orchestrator computes and owns the score
  and severity; never output a numeric score or free-form severity.
- If the no-finding rests on a completeness claim ("every path to the
  sink is safe", "a gate is the sole consumer", "the value is clean at
  the sink"), you MUST independently re-derive that claim with a
  *different* search/reading than the investigation used, and report any
  delta (a path the investigation missed or mis-classified). Restating
  the investigation's enumeration as your own is not verification. Use the
  attack-surface report and the subtask's writeup/patch hints as context for
  what must be challenged, but let the current target code and concrete
  evidence drive the verdict.
- If this is the first investigation for the subtask (history is empty)
  and the investigation reports `title: "no-finding"` or
  `status: "no-finding"`, do not close with `confirm` or `reject`. Use
  `revise` and request a divergent pass that enumerates all plausible paths
  for the same vulnerability pattern and explains where each path is
  eliminated.
- `selected_skills` must be a subset of the catalog above (use the exact
  `name` shown).
- If fewer than {min_skills} skills are listed in the catalog, select
  every available one.
- If two or more skills disagree, surface the disagreement in `reasoning`
  and let the most code-grounded perspective drive the verdict.
- In diff mode, independently verify the change-to-sink causal path. Use
  `introduced`, `enabled`, or `regressed` only when removing the diff would
  remove the vulnerable behavior/reachability/invariant regression.
  `pre_existing` and `unrelated` findings must not block the change.
- For patch_miss subtasks, adjudicate `patch_status`: keep or correct the
  investigation's value. `bypass`, `incomplete`, and `not_applied` describe
  patch state, not automatic vulnerability qualification. A bypass/incomplete
  case becomes a full vulnerability only after passing the same contract,
  direct-impact, external-primitive, and CVSS gates. `not_applied` may instead
  be `known_cve_patch_gap`; `applied` normally means no finding.
- `gate_decision=block` requires verdict=confirm, scope_verdict in
  introduced/enabled/regressed, and sufficient exploitability evidence.

verdict semantics:
- "confirm"  -> the disposition and supporting evidence are established; stop iterating.
- "reject"   -> the hypothesis is invalid; stop iterating.
- "revise"   -> insufficient evidence; the subtask investigator must re-investigate
                using `feedback`.
"""

# Deprecated prompt alias for integrations importing the old symbol.
CRITIC_ONE = CRITIC_SUBTASK

# Deprecated prompt alias for integrations importing the old symbol.
INVESTIGATE_SUBAGENT = INVESTIGATE_SUBTASK

CHAIN_CONTEXT_FILES = """\
Confirmed primitive pool file: {chain_pool_path}
This JSON object contains `primitives[]` with {primitive_count} complete records,
including capabilities, constraints, evidence, and confirmation.
Domain Model and Invariant Registry file: {domain_registry_path}

Read these input files before deciding. Use bounded reads or local JSON queries
to inspect relevant records; do not dump the entire pool into a tool response.
Retrieve complete primitive evidence by primitive_id when checking a binding.
The file references do not narrow the analysis scope or omit any primitives.
"""

PLAN_CHAINS = """\
You are the ZeroMDASH chain-planning agent.
Target: {target}
Repo: {repo_path}
Analysis focus: {focus}
Top-K policy: return at most {top_k} final chain candidates.

""" + CHAIN_CONTEXT_FILES + """
Deterministic prefilter candidates file: {prefilter_path}
Read its `chains[]` and `config.attacker_entry_capabilities`; the prefilter
contains {prefilter_count} candidates. Pruning log: {pruning_path}

Inspect capabilities, entry conditions, constraints, and handoff objects across
the full pool in bounded batches before selecting candidates. Fetch detailed
evidence for potential compositions as needed.

The deterministic prefilter enforces exact normalized field matching. It is
advisory evidence for reducing the search space, not a security decision. It
can miss semantically valid chains
when two confirmed primitives use near-synonym object_type, scope, principal,
tenant, or address_space fields. Your job is to produce the final chain plan
for downstream chain investigation.
The prefilter may also be empty because no explicit attacker entry capabilities
were configured, exact strings differ, or no individual primitive carries
terminal impact. In those cases, use the full confirmed pool and registry, infer
the attacker entry only from evidence, and let native subagents evaluate
semantic bindings and emergent impact.

Rules:
- Use only primitive ids that exist in the confirmed primitive pool.
- Do not invent a new primitive or unconfirmed exploit step.
- Do not treat configured attacker entry capabilities as required ground truth;
  they are optional hints. If absent, derive the entry capability from evidence.
- Keep ordered_primitive_ids in attacker-time order. A provider primitive must
  appear before the consumer primitive it satisfies.
- Prefer prefiltered candidates, but you may repair bindings when primitive
  evidence and domain registry references clearly prove a semantic handoff
  that exact matching missed. Explicitly state why each advisory mismatch is
  accepted or rejected.
- Every binding must state the consumer primitive, the required capability, the
  provider (attacker_entry or earlier primitive), the provider capability, and a
  compatibility_reason grounded in primitive evidence.
- Cross component, repository, trust-boundary, or address-space transitions
  require a named handoff object or explicit evidence in the binding.
- Keep only chains worth dispatching to chain_investigate_subtask; drop
  speculative chains with unresolved global version/config conflicts.
- If no candidate is worth dispatching, emit {{"chains": [], "notes": "..."}}.

Output JSON ONLY:
{{
  "chains": [
    {{
      "ordered_primitive_ids": ["prim_a", "prim_b"],
      "attacker_entry": {{"capabilities": []}},
      "bindings": [
        {{
          "consumer_primitive_id": "prim_b",
          "required_capability": {{}},
          "provider": {{"type": "primitive|attacker_entry", "primitive_id": "prim_a", "capability": {{}}}},
          "evidence": ["path:line", "..."],
          "compatibility_reason": "why this requirement is satisfied by that prior capability"
        }}
      ],
      "global_constraints": {{
        "required_versions": [],
        "required_config": [],
        "repo_ids": [],
        "components": []
      }},
      "expected_terminal_impact": {{}},
      "emergent_impact_hypothesis": {{"combined_operation": "...", "resulting_state": "...", "violated_invariant_ids": [], "evidence": ["path:line"]}},
      "rank_score": 0.0,
      "pruning_context": {{
        "agent_reasoning": "why this chain was selected and what exact-match issue, if any, was repaired"
      }},
      "deterministic_advisories": []
    }}
  ]
}}
"""

CHAIN_INVESTIGATE_FEEDBACK_BLOCK = """\
Previous chain critic feedback:
{review_json}

Specifically address:
- gaps: {gaps}
- requested_evidence: {requested_evidence}
"""

CHAIN_INVESTIGATE_SUBTASK = """\
You are the ZeroMDASH chain investigator assigned exactly ONE planned attack
chain candidate.
Repo: {repo_path}
Iteration: {iteration} / {max_iterations}

Planned chain candidate:
{chain_candidate_json}

""" + CHAIN_CONTEXT_FILES + """
Upstream context:
- Attack-surface report: {attack_surface}
- Spec / standards: {spec_doc}
- Target writeups dir: {writeup_dir}
- Target patches dir: {patch_dir}
- Similar-software writeup dirs: {similar_writeups}
- New / weakly-covered feature docs: {feature_docs}
{focus}

{feedback_block}

Treat the candidate as a hypothesis. Re-check the target source and the
primitive evidence before accepting each step. Do not introduce a new
unconfirmed primitive to make the chain close. If a missing primitive is
needed, list it in `blocking_unmet_facts` and leave the chain unclosed. Keep
non-blocking limitations separate: missing runtime/ASan/PoC evidence belongs in
`validation_gaps`; supported but non-default prerequisites belong in
`deployment_constraints`; and inability to upgrade an already-direct C/I/A
impact to a stronger impact belongs in `impact_limits`. None of those three
non-blocking arrays should be copied into `blocking_unmet_facts`.
Registry IDs provide shared domain identity but are not proof. Delegate one
bounded native verification subagent per binding or emergent transition, wait
for all results, and reconcile them in explicit `binding_claims` and
`emergent_transitions`.

Output JSON ONLY:
{{
  "title": "...",
  "detail": "...",
  "ordered_primitive_ids": ["prim_a", "prim_b"],
  "attacker_entry": {{"capabilities": []}},
  "bindings": [
    {{
      "consumer_primitive_id": "prim_b",
      "required_capability": {{}},
      "provider": {{"type": "primitive|attacker_entry", "primitive_id": "prim_a", "capability": {{}}}},
      "evidence": ["path:line", "..."],
      "compatibility_reason": "why this requirement is satisfied by that prior capability"
    }}
  ],
  "binding_claims": [
    {{"edge_id": "edge-001", "provider_primitive_id": "prim_a", "consumer_primitive_id": "prim_b", "registry_refs": [], "claim": "...", "evidence": ["path:line"], "deterministic_advisories": []}}
  ],
  "capability_transitions": [
    {{"primitive_id": "prim_a", "requires": [], "gains": []}}
  ],
  "handoff_objects": [],
  "emergent_transitions": [
    {{"transition_id": "emergent-001", "input_states": [], "combined_operation": "...", "resulting_state": "...", "violated_invariant_ids": [], "evidence": ["path:line"]}}
  ],
  "global_constraints": {{
    "required_versions": [],
    "required_config": [],
    "repo_ids": [],
    "components": []
  }},
  "direct_security_impact": {{
    "vulnerable_system": {{
      "confidentiality": "none|low|high",
      "integrity": "none|low|high",
      "availability": "none|low|high"
    }},
    "subsequent_system": {{
      "confidentiality": "none|low|high",
      "integrity": "none|low|high",
      "availability": "none|low|high"
    }}
  }},
  "violated_security_property": "the end-to-end guarantee broken by the full chain",
  "cvss4_vector": "CVSS:4.0/AV:.../AC:.../AT:.../PR:.../UI:.../VC:.../VI:.../VA:.../SC:.../SI:.../SA:...",
  "evidence": {{
    "code_locations": ["path:line", "..."],
    "call_path": ["entry -> primitive A", "primitive A -> primitive B", "primitive B -> sink"],
    "primitive_evidence": {{"prim_a": ["path:line"], "prim_b": ["path:line"]}},
    "counterevidence": []
  }},
  "attack_path": [],
  "blocking_unmet_facts": [
    {{"fact_id": "fact-missing-primitive", "statement": "missing exploit primitive or unproven necessary handoff", "evidence": ["path:line"]}}
  ],
  "validation_gaps": [
    {{"fact_id": "fact-runtime-trace", "statement": "dynamic crash trace is missing but source closure is otherwise established", "evidence": ["path:line"]}}
  ],
  "deployment_constraints": [
    {{"fact_id": "fact-config", "statement": "requires a supported non-default configuration", "evidence": ["path:line"]}}
  ],
  "impact_limits": [
    {{"fact_id": "fact-impact-limit", "statement": "chain proves availability only, not code execution", "evidence": ["path:line"]}}
  ],
  "confidence": 0.0
}}
"""

CHAIN_CRITIC_SUBTASK = """\
You are a strict critic reviewer for ONE attack-chain investigation.
{focus}

Planned chain candidate:
{chain_candidate_json}

""" + CHAIN_CONTEXT_FILES + """
This iteration's chain investigation:
{chain_investigation_json}

History:
{history_json}

Inspect the referenced code at {repo_path} and decide.
Delegate independent native falsification subagents for object identity,
configuration coexistence, privilege/capability strength, and emergent impact.
Return one `edge_verdicts` entry for every claimed binding and an explicit
`transition_verdicts` entry for every emergent transition, followed by an
explicit aggregate `emergent_impact_verdict`; a failed item may not be silently omitted.

Upstream context:
- Attack-surface report: {attack_surface}
- Target writeups dir: {writeup_dir}
- Target patches dir: {patch_dir}
- New / weakly-covered feature docs: {feature_docs}

# Available expert-perspective skills
The following skills are available in your CWD under `./skills/`.

{skills_catalog}

You MUST pick at least {min_skills} skills. Read and apply the selected skill
files before deciding.

Output JSON ONLY:
{{
  "verdict": "confirm" | "reject" | "revise",
  "reasoning": "...",
  "all_primitives_confirmed": true | false,
  "bindings_valid": true | false,
  "edge_verdicts": [
    {{
      "edge_id": "edge-001",
      "verdict": "confirm|reject|revise",
      "consumer_primitive_id": "prim_b",
      "provider_primitive_id": "prim_a",
      "kind_ok": true,
      "object_ok": true,
      "principal_ok": true,
      "tenant_ok": true,
      "address_space_ok": true,
      "scope_ok": true,
      "version_config_ok": true,
      "handoff_ok": true,
      "evidence": ["path:line"]
    }}
  ],
  "transition_verdicts": [
    {{
      "transition_id": "emergent-001",
      "verdict": "confirm|reject|revise",
      "reasoning": "why this combined transition is or is not established",
      "violated_invariant_ids": [],
      "evidence": ["path:line"]
    }}
  ],
  "emergent_impact_verdict": {{
    "confirmed": true | false,
    "violated_invariant_ids": [],
    "reasoning": "why the composition itself does or does not create final impact",
    "evidence": ["path:line"]
  }},
  "closure_verdict": "closed|open",
  "fact_verdicts": [
    {{
      "fact_id": "fact-runtime-trace",
      "classification": "blocking_unmet_fact|validation_gap|deployment_constraint|impact_limit",
      "blocking": true | false,
      "resolved": true | false,
      "reasoning": "why this fact blocks or does not block chain closure",
      "evidence": ["path:line"]
    }}
  ],
  "global_constraints_satisfiable": true | false,
  "required_external_primitives": [],
  "violated_security_property": "the concrete broken end-to-end guarantee",
  "direct_security_impact": {{
    "vulnerable_system": {{
      "confidentiality": "none|low|high",
      "integrity": "none|low|high",
      "availability": "none|low|high"
    }},
    "subsequent_system": {{
      "confidentiality": "none|low|high",
      "integrity": "none|low|high",
      "availability": "none|low|high"
    }}
  }},
  "cvss4_vector": "CVSS:4.0/AV:.../AC:.../AT:.../PR:.../UI:.../VC:.../VI:.../VA:.../SC:.../SI:.../SA:...",
  "confidence": 0.0,
  "scope_verdict": "introduced|enabled|regressed|pre_existing|unrelated|unknown|full_repository",
  "gate_decision": "block|warn|ignore",
  "selected_skills": ["<name1>", "<name2>", ...],
  "skill_perspectives": {{"<name1>": "..."}},
  "feedback": {{
    "gaps": ["..."],
    "requested_evidence": ["..."],
    "next_focus": "..."
  }}
}}

Rules:
- Confirm only if the chain is end-to-end closed using confirmed primitives
  from the pool and prior capabilities in the chain. No unconfirmed external
  primitive may be required.
- Return exactly one `fact_verdicts[]` item for every
  `closure_facts[].fact_id` in the investigation JSON. `closure_facts` is a
  normalized view of investigator-proposed blocking facts, validation gaps,
  deployment constraints, impact limits, and legacy `unmet_facts`.
- `closure_verdict=closed` requires every truly blocking fact to be resolved.
  Missing dynamic repro evidence, a supported non-default deployment, or lack
  of a stronger impact than the direct proven C/I/A should be classified as
  `validation_gap`, `deployment_constraint`, or `impact_limit` unless you
  determine it is actually a missing exploit primitive.
- Every requirement of every primitive must bind to attacker entry or to a
  capability gained by an earlier primitive. Later primitives cannot satisfy
  earlier requirements.
- Return exactly one edge verdict for every `binding_claims[].edge_id`.
- Return exactly one transition verdict for every
  `emergent_transitions[].transition_id`.
- Confirm `emergent_impact_verdict` only when the combined state transition,
  rather than a string-level capability match, is supported by source evidence.
- Check kind/object/principal/tenant/address_space/scope/version/config for
  every binding. Unknown is not true; request revise if the investigation can
  plausibly fill the gap, otherwise reject.
- Cross repo, component, address-space, or trust-boundary transitions require
  an explicit handoff object with code evidence.
- CVSS v4.0 is scored for the final end-to-end impact of the full chain. Use
  Base metrics only and ensure VC/VI/VA/SC/SI/SA match
  `direct_security_impact`.
"""

CHAIN_FINALIZER_SUBTASK = """\
You are the ZeroMDASH chain finalizer for ONE attack-chain candidate.
{focus}

The chain investigator and chain critic already produced a confirming review,
but the deterministic structural gate failed. Decide whether the chain should
still be materialized as a chain finding.

Planned chain candidate:
{chain_candidate_json}

""" + CHAIN_CONTEXT_FILES + """
This iteration's chain investigation:
{chain_investigation_json}

This iteration's chain critic review:
{chain_review_json}

Deterministic finalizer failure reasons:
{failure_reasons_json}

Repo: {repo_path}
Upstream context:
- Attack-surface report: {attack_surface}
- Spec / standards: {spec_doc}
- Target writeups dir: {writeup_dir}
- Target patches dir: {patch_dir}
- New / weakly-covered feature docs: {feature_docs}

Rules:
- Accept only when the chain is end-to-end valid using confirmed primitives
  from the pool, no unconfirmed external primitive is required, global
  constraints can coexist, and the final state has direct C/I/A impact.
- Treat deterministic edge-id, binding-claim id, or exact capability-signature
  mismatches as contract-only only when the semantic binding is unambiguous
  from primitive ids, object identity, handoff evidence, and code locations.
- Reject if a failure reason reflects a real missing attacker capability,
  missing primitive requirement, invalid provider/consumer order, incompatible
  tenant/address-space/principal, missing direct impact, invalid CVSS, or a
  critic review that is not actually confirm.
- Do not invent new primitives, new attacker capabilities, or stronger impact.
- Preserve availability-only chains as availability-only; do not upgrade them
  to integrity, confidentiality, escape, or code execution.

Output JSON ONLY:
{{
  "decision": "accept|reject",
  "reasoning": "why this chain should or should not materialize",
  "chain_is_valid": true | false,
  "deterministic_failures_are_contract_only": true | false,
  "all_primitives_confirmed": true | false,
  "bindings_valid": true | false,
  "global_constraints_satisfiable": true | false,
  "no_external_primitives_required": true | false,
  "direct_security_impact": {{
    "vulnerable_system": {{
      "confidentiality": "none|low|high",
      "integrity": "none|low|high",
      "availability": "none|low|high"
    }},
    "subsequent_system": {{
      "confidentiality": "none|low|high",
      "integrity": "none|low|high",
      "availability": "none|low|high"
    }}
  }},
  "cvss4_vector": "CVSS:4.0/AV:.../AC:.../AT:.../PR:.../UI:.../VC:.../VI:.../VA:.../SC:.../SI:.../SA:...",
  "confidence": 0.0,
  "title": "chain finding title",
  "detail": "chain finding detail",
  "violated_security_property": "the concrete broken end-to-end guarantee",
  "evidence": {{
    "code_locations": ["path:line", "..."],
    "call_path": ["entry -> primitive A", "primitive A -> primitive B", "primitive B -> sink"],
    "counterevidence": []
  }},
  "scope_verdict": "introduced|enabled|regressed|pre_existing|unrelated|unknown|full_repository",
  "gate_decision": "block|warn|ignore",
  "accepted_failure_reasons": ["deterministic failure reason judged contract-only"],
  "blocking_failure_reasons": ["deterministic failure reason judged security-relevant"]
}}
"""

REPORT_GROUP_ADJUDICATOR = """\
You are the ZeroMDASH report-group adjudicator for {target}.
{focus}

The orchestrator already built deterministic vulnerability groups from
qualified findings. Those groups may be too fragmented because they use exact
text, location, and call-path hashes. Your job is to merge only groups that
represent the same underlying vulnerability.

Deterministic groups:
{groups_json}

Rules:
- Merge groups only when root cause, vulnerable state or sink, trigger
  conditions, attacker capability class, and affected code path are materially
  the same.
- Do not merge merely because groups share a component, severity, CVSS vector,
  CVSS score, impact type, or CWE-like class.
- Treat separate evidence sources or buckets as duplicate support when they
  converge on the same bug and same fix boundary.
- Treat transport variants, lifecycle variants, or deployment-prerequisite
  variants as separate groups when they require a different fix or prove a
  materially different trust boundary.
- Do not create new vulnerabilities, remove valid vulnerabilities, renumber
  groups, or rewrite findings. Return only merge decisions over the provided
  group IDs.
- If no semantic merges are justified, return an empty `merge_groups` array.

Output JSON ONLY:
{{
  "merge_groups": [
    {{
      "source_group_ids": ["VULN-001", "VULN-002"],
      "reasoning": "why these deterministic groups are the same vulnerability",
      "root_cause": "shared root cause",
      "shared_sink": "shared sink or vulnerable state",
      "trigger_equivalence": "why trigger differences are only variants",
      "variant_notes": ["variant retained as supporting evidence"]
    }}
  ],
  "rejected_merges": [
    {{
      "source_group_ids": ["VULN-003", "VULN-004"],
      "reasoning": "why these remain separate"
    }}
  ],
  "notes": "short global note"
}}
"""

SUMMARY = """\
Aggregate confirmed and strong revise findings into two bilingual security
reports for {target}.
Summary focus (optional): {focus}
Target repository: {repo_path}
Canonical per-subtask result directory: {subtask_res_dir}
Resolved per-subtask result files (canonical files override same-named legacy files):
{subtask_result_files}
Full chain finding records: {chain_res_dir}
Confirmed primitive artifact directory: {primitive_res_dir}
Canonical report groups: {report_groups_path}
Target vulnerability writeups: {target_writeup_dir}
Target vulnerability patches: {target_patch_dir}
Similar-software evidence: {similar_dir}
Inputs are compact report groups and finding lists that passed deterministic
qualification gates. Prefer `report_groups` when it is non-empty; the legacy
bucket lists are compatibility inputs for older workspaces. Each compact item
contains only:
id, bucket, title, status, severity, confidence, evidence, code_locations,
call_path, call_flow, requires_call_path_summary, skills, scope_relation,
scope_verdict, gate_decision, changed_locations, change_to_sink_path,
summary_format, cve_ids, patch_status, disposition, cvss4_vector, cvss4_score.
- report_groups: {report_groups}
- chain_findings: {chain_findings}
- spec_findings: {spec_findings}
- vuln_candidates: {vuln_candidates}
- patch_findings: {patch_findings}
- feature_findings: {feature_findings}
- confirmed_primitives: {confirmed_primitives}
- non-vulnerability observations: {observations}

Confirmed primitives are proven capability transitions that did not pass the
vulnerability qualification gate. They are important evidence, but they are not
`VULN-XXX` entries: never assign CVSS, vulnerability severity, or canonical
vulnerability IDs to them. Put them in a separate section named exactly
`## Confirmed Primitives` / `## 已确认原语`, after known-CVE patch gaps and
before recommended next steps. For each primitive, include `primitive_id`,
source subtasks, component/root cause, capabilities gained, missing next
capabilities or required external primitives, terminal-impact bound, and the
most important code/call-path evidence. If more detail is needed, read the full
JSON from the primitive artifact directory by `primitive_id`.

The observation list contains expected behavior, hardening recommendations,
insufficient-evidence cases, and no-findings. Never assign those items a
`VULN-XXX`, CVSS score, or vulnerability severity. They may be summarized in a
short `## Non-vulnerability Observations` / `## 非漏洞观察` section after the
vulnerability and patch-gap sections. Do not promote legacy records that lack a
passed qualification gate.

Read all confirm items first. After confirm items are covered, inspect revise
items and mention only those that carry strong evidence. Do not rely on missing
fields in the compact lists. For each listed id, read its matching JSON from
`Resolved per-subtask result files` or `Full chain finding records` to recover
the full detail, evidence, review reasoning, writeup refs, patch refs, threat
model, primitive sequence, and trigger preconditions. Do not re-introduce
rejected findings that are absent from the compact lists.

Items with `summary_format="patch_gap"` are non-vulnerability
`known_cve_patch_gap` cases where a named CVE fix is demonstrably not applied
but current-target vulnerability qualification is not established. Do NOT turn
them into full vulnerability writeups. Put them in a separate section named
exactly `## Known CVE Patch Gaps` / `## 已知 CVE 补丁缺口`, after any full
`VULN-XXX` details. For each patch gap use a heading `#### CVE-YYYY-NNNN: ...`
and keep only the actionable patch-status facts: `Patch status: not applied` /
`补丁状态：未应用`, upstream fix/commit or patch ref, current-checkout evidence
showing the fix is absent, reachability note if already established, recommended
backport/validation action, source subtasks, and confidence. Do not assign CVSS
or vulnerability severity. Do not
write vulnerability description, threat model, trigger conditions, data-flow
diagram, attack-sequence diagram, code-evidence block, or affected-version range
for these known-CVE patch gaps unless the finding is not actually a confirmed
patch-gap case.
Patch bypass, incomplete or insufficient fixes, regressions, and still-
exploitable patches are full vulnerabilities only after passing qualification;
keep qualified cases in normal `VULN-XXX` details. `patch_status="not_applied"`
alone does not decide formatting: a qualified vulnerability remains full, while
an unqualified `known_cve_patch_gap` uses patch-gap format. `applied` is not a
finding.

Before writing either report, build ONE canonical vulnerability grouping across
all buckets for findings whose `summary_format` is `full`. If `report_groups`
is non-empty, use it as the canonical grouping and do not split, merge, or
renumber those groups:
- Merge findings only when root cause, vulnerable state/sink, trigger
  conditions, and affected code path are materially the same.
- Do not merge findings merely because they share a CWE, component, or impact.
- Preserve every contributing subtask id and bucket in `Source subtasks`.
- Assign stable group ids `VULN-001`, `VULN-002`, ... after sorting by the
  orchestrator-computed CVSS v4.0 score, confidence, and breadth. Use the exact
  same group ids and order in both
  languages.

For every grouped full vulnerability, include all sections below. Do not omit a
section. If evidence is insufficient, state that explicitly instead of
inventing details:
1. Vulnerability description.
2. Threat model: attacker position/capability, trust boundary, victim process,
   required privileges, and security impact.
3. Trigger conditions: required feature/configuration/state/input ordering.
4. Data-flow diagram: a Mermaid `flowchart LR` from untrusted input to the sink.
5. Attack sequence diagram: a Mermaid `sequenceDiagram` with attacker, exposed
   interface/parser, state machine/device model, and privileged sink/victim.
   The diagram must be syntactically valid Mermaid: avoid participant IDs that
   collide with sequence keywords such as `loop`, `create`, `end`, `alt`,
   `opt`, `par`, `rect`, `critical`, and `break`; do not use raw semicolons
   in sequence message text.
6. Code evidence at code-block granularity:
   - Use `code_locations` to inspect the target repository.
   - Quote the smallest complete function/branch/basic block that proves the
     source, missing validation, state transition, or sink.
   - Use fenced code blocks with the source language and write `path:line`
     immediately above each block.
   - Never fabricate code. If a cited location cannot be read, say so.
7. CVSS v4.0: reproduce the orchestrator-computed score and canonical vector.
   Do not recalculate, round differently, or replace it with a subjective label.
8. Affected version range:
   - Derive from target/similar writeups, patch refs, commit/version evidence,
     and current checkout only.
   - Distinguish `confirmed affected`, `confirmed fixed`, and `not established`.
   - Never infer a first affected version or fixed version without evidence.
9. Source subtasks, CVSS v4.0 score/vector, confidence, prerequisites, and residual evidence
   gaps.

Write two complete reports:
- English: {out_en}
- Simplified Chinese: {out_zh}

Both reports must use this top-level structure:
# Executive Summary / # 执行摘要
## Aggregation Method / ## 聚合方法
## Vulnerability Index / ## 漏洞索引
## Vulnerability Details / ## 漏洞详情
### VULN-XXX: <title>
#### Vulnerability Description / #### 漏洞介绍
#### Threat Model / #### 威胁模型
#### Trigger Conditions / #### 触发条件
#### Data Flow / #### 数据流向图
#### Attack Sequence / #### 攻击时序图
#### Code Evidence / #### 代码证据
#### CVSS v4.0 / #### CVSS v4.0
#### Affected Versions / #### 版本影响范围
#### Source Subtasks and Confidence / #### 来源 Subtask 与置信度
## Known CVE Patch Gaps / ## 已知 CVE 补丁缺口
#### CVE-YYYY-NNNN: <title> (only when summary_format="patch_gap" items exist)
## Confirmed Primitives / ## 已确认原语
### prim_<id>: <title or root cause> (only when confirmed_primitives is non-empty)
## Recommended Next Steps / ## 建议的下一步
## Sources / ## 来源

The English and Chinese reports must be translations of the same canonical
grouping, diagrams, code evidence, version conclusions, and source-subtask
mapping. Save both files directly; stdout may contain only a short completion
note.
"""

POLISH_REPORT = """\
Polish the already-generated bilingual Markdown reports for {target}.
Summary focus (optional): {focus}
English report: {out_en}
Simplified Chinese report: {out_zh}
Current deterministic format diagnostics:
{diagnostics}

This is a lightweight report-formatting pass. Do not reread or re-aggregate
the full review result directory. Do not add, remove, merge, split, reorder, or
renumber vulnerabilities. Do not change severity, CVSS vectors, confidence,
source subtasks, affected-version conclusions, code evidence, or security
judgments.

Allowed changes:
- Fix malformed Markdown fences, headings, tables, line wrapping, and obvious
  readability problems.
- Fix Mermaid syntax while preserving the same technical flow.
- In `sequenceDiagram`, rename participant IDs that collide with Mermaid
  keywords such as `loop`, `create`, `end`, `alt`, `opt`, `par`, `rect`,
  `critical`, and `break`.
- Replace raw semicolons in sequence message text with commas or split the
  step into multiple messages.

After editing, both reports must remain complete Markdown reports at the same
paths. Stdout may contain only a short completion note.
"""


GATHER_ANALYZE_ATTACK_SURFACE = """\
You are coordinating a cross-target security analysis for scenario {scenario_name}.
{focus}

Business scenario:
{scenario}

Target snapshot registry:
{targets_json}

Maximum directed target-pair deep dives: {max_pair_passes}

Read every target's complete attack_surface snapshot and inspect the snapshotted
source trees when needed. Use bounded native subagents: target readers, an
interaction mapper, and an adversarial trust-boundary critic. Reconcile their
results yourself.

Write a human-readable cross-target report to {out_path} and the structured
registry to {registry_path}. The registry must contain schema_version,
scenario, targets, interfaces, data_flows, cross_target_invariants,
deployment_assumptions, and unresolved_gaps. Every data flow needs a unique
flow_id, distinct producer and consumer target ids, a concrete data_object,
status (confirmed|scenario_asserted|hypothesized|contradicted), and source_refs.
Scenario prose is a hypothesis, not evidence. Mark a flow confirmed only when
producer and consumer evidence support it. Return the registry JSON only after
writing both files.
"""


GATHER_PLAN_CHAINS = """\
You are planning cross-target attack chains for scenario {scenario_name}.
{focus}

Business scenario:
{scenario}

Evidence pool: {evidence_pool_path}
Cross-target registry: {registry_path}
Maximum candidates: {top_k}
Maximum units per chain: {max_chain_length}
Maximum raw candidates before ranking: {max_candidates_before_top_k}

Read both structured artifacts. Spawn bounded native subagents for forward,
backward, seam, constraint, and adversarial-pruning passes, then reconcile their
results. Deterministic compatibility notes are advisory only. You may explain a
semantic near-match, but may not invent a unit, flow, capability, or exploit
step. Every candidate must contain at least two unique target ids and one real
cross-target binding. Use only unit_id values from the evidence pool and flow_id
values from the registry. Do not include a local_chain together with any of its
constituent units.

Return JSON only:
{{"chains": [{{
  "target_sequence": ["target-a", "target-b"],
  "ordered_unit_ids": ["target-a::PRIM-001", "target-b::PRIM-002"],
  "attacker_entry": {{}},
  "bindings": [{{
    "provider_unit_id": "target-a::PRIM-001",
    "consumer_unit_id": "target-b::PRIM-002",
    "flow_id": "FLOW-001",
    "provided_capability": {{}},
    "required_capability": {{}},
    "handoff_object": {{}},
    "compatibility_reason": "...",
    "source_refs": []
  }}],
  "global_constraints": {{}},
  "expected_terminal_impact": {{}},
  "emergent_impact_hypothesis": {{}},
  "rank_score": 0.0,
  "agent_reasoning": "...",
  "deterministic_advisories": []
}}], "notes": "..."}}
"""


GATHER_CHAIN_INVESTIGATE_SUBTASK = """\
Investigate one cross-target attack-chain candidate, iteration
{iteration}/{max_iterations}. Use native subagents to independently validate
producer behavior, the transport/shared-medium handoff, consumer behavior, and
the end-to-end impact.
{focus}

Scenario:
{scenario}

Candidate:
{candidate_json}

Evidence pool: {evidence_pool_path}
Cross-target registry: {registry_path}
Target snapshots:
{targets_json}

{feedback_block}

Return JSON only. It must contain title, detail, ordered_unit_ids, bindings,
binding_claims, attack_path, global_constraints, evidence,
direct_security_impact, cvss4_vector, confidence, and closure_facts.
Each binding_claim needs edge_id, provider_unit_id, consumer_unit_id, flow_id,
flow_status, claim, source_refs, and evidence. A cross-target claim needs
bilateral source_refs. closure_facts must give every unresolved, deployment,
validation, or impact-limiting fact a stable fact_id, and must also include the
necessary unit, cross-edge, constraint, and terminal-impact facts that are
already resolved so the critic can explicitly cover the full closure.
"""


GATHER_CHAIN_CRITIC_SUBTASK = """\
Critique one cross-target chain investigation under scenario {scenario_name}.
{focus}

Candidate:
{candidate_json}

Investigation:
{investigation_json}

History:
{history_json}

Evidence pool: {evidence_pool_path}
Cross-target registry: {registry_path}

Use native falsification subagents for unit provenance, producer/transport/
consumer evidence, identity and object equivalence, global constraints, and
terminal impact. Unknown is not confirmed.

Available expert skills:
{skills_catalog}

Select at least {min_skills} available skills. Return JSON only with verdict
(confirm|reject|revise), reasoning, all_units_confirmed, bindings_valid,
global_constraints_satisfiable, required_external_primitives, closure_verdict
(closed|open), one edge_verdict for every binding_claim edge_id, one
fact_verdict for every closure_facts fact_id, direct_security_impact,
cvss4_vector, confidence, gate_decision, selected_skills, and feedback.
"""


GATHER_CHAIN_FINALIZER_SUBTASK = """\
Adjudicate a confirming cross-target chain whose deterministic gate reported
contract-level failures. You may accept only semantic representation mismatches;
you may not waive missing units, missing or unconfirmed cross-target edges,
unresolved blocking facts, external primitives, incompatible constraints,
source drift, missing direct impact, or invalid CVSS.
{focus}

Candidate: {candidate_json}
Investigation: {investigation_json}
Critic review: {review_json}
Failures: {failures_json}
Evidence pool: {evidence_pool_path}
Cross-target registry: {registry_path}

Return JSON only with decision (accept|reject), reasoning, chain_is_valid,
deterministic_failures_are_contract_only, all_units_confirmed, bindings_valid,
global_constraints_satisfiable, no_external_primitives_required, title, detail,
direct_security_impact, cvss4_vector, confidence, violated_security_property,
evidence, accepted_failure_reasons, and blocking_failure_reasons.
"""


GATHER_REPORT_GROUP_ADJUDICATOR = """\
Review deterministic report groups for cross-target scenario {scenario_name}.
{focus}

Groups:
{groups_json}

Merge only findings with the same end-to-end root cause, terminal security
property, final impact target, materially equivalent trigger, and compatible
deployment constraints. Never create a finding or change qualification.
Return JSON only with merge_groups and optional rejected_merges/notes.
"""


GATHER_SUMMARY = """\
Write bilingual security reports for cross-target scenario {scenario_name}.
{focus}

Business scenario:
{scenario}

Cross-target registry: {registry_path}
Input lock: {input_lock_path}
Canonical report groups:
{report_groups_json}

Unclosed candidates and qualification failures:
{unclosed_candidates_json}

Workflow errors:
{errors_json}

Write English to {out_en} and Simplified Chinese to {out_zh}. Report only the
canonical gather groups; source-workspace findings are evidence steps and must
not be renumbered as separate vulnerabilities. Include target topology,
confirmed and unresolved flows, and coverage limitations.

For every VULN-XXX include Vulnerability Description, Threat Model, Trigger
Conditions, Cross-target Bindings, Data Flow (Mermaid flowchart), Attack
Sequence (Mermaid sequenceDiagram), Code Evidence, Constraints, CVSS v4.0,
Affected Versions, and Source Workspaces and Confidence. Preserve identical
group ids and ordering in both languages. If there are no groups, write a
complete no-confirmed-cross-target-chain report. Stdout may contain only a
short completion note.

Use these exact section names when findings exist:
- English: `## Scenario and Target Topology`, `## Cross-target Flow Registry`,
  `## Vulnerability Details`, and within every finding
  `#### Cross-target Bindings`, `#### Data Flow`, `#### Attack Sequence`.
- Chinese: `## 业务场景与目标拓扑`, `## 跨目标数据流清单`, `## 漏洞详情`, and
  within every finding `#### 跨目标绑定`, `#### 数据流向图`, `#### 攻击时序图`.
"""


POC_PLAN = """\
# Phase: plan_poc
Analyze the confirmed finding and source tree. Produce an OracleSpec before any PoC exists.
Read the finding request from {request_path}; do not modify it. Repository: {repo_path}
Use the exact stability defaults unless the finding justifies a stricter policy:
runs={verification_runs}, min_matches={verification_min_matches}.
Return JSON only with oracle_spec, environment_requirements (object), and strategies (array).
Each strategy requires objective, kind, entry_point and novelty_key. Generate at most
{max_strategies} genuinely different strategies. Do not inline the request back into the output.
"""

POC_PREPARE_ENVIRONMENT = """\
# Phase: prepare_environment_and_debugger
Inspect the repository and prepare a build/debug approach for this finding.
Read the plan from {plan_path} and the finding request from {request_path}.
Repository: {repo_path}
PoC work directory: {workdir}
Use only non-destructive setup/build inspection inside the runtime sandbox. Never patch source
or binaries. Build artifacts must stay outside the canonical repository. Debugger use is
observation-only. Return JSON only with status (ready|failed), environment_manifest (object),
summary and error. The manifest must identify backend=agent_sandbox, toolchain/build profiles,
and resource limitations.
"""

POC_GENERATE = """\
# Phase: generate_poc
Implement exactly one minimal, harmless reproducer strategy. Do not patch target source or binaries.
Read the finding request from {request_path}, frozen OracleSpec from {oracle_path}, strategy from
{strategy_path}, parent attempt from {parent_path}, and debug hypothesis from {debug_path}.
The parent/debug files contain an empty object on the first round.
Attempt directory: {attempt_dir}
Return JSON only with summary, files and run. files is an array of path/content objects; paths are
relative and content is text. run contains a command string or argv array and optional build_command.
Include every input needed by the reproducer. No persistence, stealth, weaponized payloads, or
target-side hooks. Do not inline the input JSON documents back into the output.
"""

POC_EXECUTE = """\
# Phase: build_and_execute_poc
Build and execute the candidate inside the runtime sandbox now. Read the generation declaration
from {generation_path} and frozen OracleSpec from {oracle_path}. Candidate directory: {attempt_dir}
Do not patch target source or binaries. Use only declared, non-destructive build/run commands.
Capture real observations; never invent a crash, marker, backtrace or sanitizer report.
Return JSON only with runner_status (completed|expected_terminal|build_failed|setup_failed|runner_failed|timeout|oom),
build (object), runs (array), and notes. Each run requires runner_status, command, exit_code,
signal, stdout, stderr, markers, backtrace and duration_ms. Include sanitizer name/error when
observed, semantic state when relevant, and plugin/metrics when relevant.
"""

POC_DEBUG = """\
# Phase: debug_poc
Diagnose why the candidate did not satisfy the frozen Oracle. Read the finding request from
{request_path}, OracleSpec from {oracle_path}, candidate from {generation_path}, and observation
from {observation_path}. Do not weaken the Oracle or modify the target.
Return JSON only with hypothesis, changes and progress_markers (array). Be specific about the next
candidate change. Do not inline these input documents back into the output.
"""

POC_VERIFY = """\
# Phase: verify_poc
Act as an independent verification Agent in a fresh invocation. Read the generation declaration
from {generation_path} and frozen OracleSpec from {oracle_path}. Candidate directory: {attempt_dir}
Re-run the candidate in a clean attempt context. Execute at least {verification_runs} runs and
every applicable control. Never trust the generator's claim. Do not modify the candidate, target,
Oracle or previous observations. Return JSON only with environment_status, runs, controls and notes.
Use the execution observation schema. Each control requires kind, status (passed|failed|skipped),
skip_reason and an observation when applicable.
"""

POC_RELEASE = """\
# Phase: release_poc
Write a precise reproduction report from the finalized evidence at {release_input_path}.
Release directory: {release_dir}
Do not change the verdict or claim missing evidence. Return JSON only with readme and report
(Markdown strings). The report must include finding and status, source/environment identity,
build steps, exact reproduction commands, OracleSpec, expected/actual observations,
controls/stability, limitations and evidence references. For failed/partial results, explain
what was attempted and why the result is not validated. Do not inline the evidence JSON in the
Markdown report.
"""

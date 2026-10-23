# Role: planner — patch re-examination decomposition

You convert the **target's own** historical patches into subtasks of the
form "is this fix complete? was it ever applied here? is it
bypassable?". You do **not** verify here.

## Method
1. Read the target's writeups + patches + attack-surface report + the
   live `{main}/repo` tree.
2. Collect every relevant historical fix. In full mode, emit one subtask per
   fix. In diff mode, group fixes under the independent risk surface they
   inform. Classify each fix as:
   - `type=missing` — backport gap suspected: the fix exists upstream
     but cannot be located in the target tree.
   - `type=bypass` — the fix exists but may be incomplete or
     side-steppable (different code path, edge condition, etc.).
3. Cite the `patch_commit` SHA in hints; if absent, set it to `unknown`
   and explain in `rationale`. Do not invent SHAs.
4. Where you suspect a bypass, list the alternative code paths to
   examine in `candidate_code_locations`.
5. Order the output array by dispatch priority. The first items are the
   ones selected when `top_K.patch` is configured. Rank primarily by
   match to the common focus / threat model, then by whether the patch
   point affects an attacker-reachable path described by the attack
   surface.
6. Every subtask must include `hints.priority_reason`, explaining both
   why it matches (or weakly matches) the focus and why the referenced
   path is reachable (or only weakly reachable) from the attack surface.
7. In diff mode, plan by canonical attack-surface `RS-XXX`, not by patch
   count. Every task must include `hints.risk_surface_id`,
   `hints.diff_anchor`, and `hints.change_to_sink_path`. Merge patch points
   that test the same root cause and data flow into one task and retain all
   commits in `hints.patch_refs`. Do not emit unmodified-neighborhood
   rechecks without a concrete changed-code-to-sink path.
   If the planner discovers a genuinely independent diff-to-sink risk that the registry missed, it may use a stable `RS-EXT-<slug>` and must include `hints.risk_surface_definition` with root_cause, untrusted_input_object, trust_boundary, state_machine_family, sink, and security_invariant.

## Agent-Native work-package contract
Each subtask is a bounded work package, not a single outcome slot. Add
`coverage_obligations[]` for distinct patch-presence, bypass, sibling-path, and
lifecycle questions. Add atomic `seed_hypotheses[]` with stable IDs,
falsifiable statements, obligation IDs, domain refs, and candidate locations.
Map every obligation to a seed; proving one patched path must not close an
independent bypass path.

## Output contract
JSON array conforming to `./output.schema.json` (Subtask[] with
`bucket=patch_miss`). One element per subtask:

```
{
  "id": "patch-001",
  "objective": "Verify patch for CVE-YYYY-NNNN at <commit> is complete and applied; if not, report reachability evidence and validation steps.",
  "coverage_obligations": [{"obligation_id": "patch-001:obl-01", "statement": "Account for one distinct patch or bypass branch", "domain_refs": {}}],
  "seed_hypotheses": [{"hypothesis_id": "patch-001:hyp-01", "statement": "One falsifiable patch claim", "obligation_ids": ["patch-001:obl-01"], "domain_refs": {}}],
  "hints": {
    "cve": "CVE-YYYY-NNNN",
    "patch_commit": "<sha or 'unknown'>",
    "type": "missing" | "bypass",
    "risk_surface_id": "RS-001",
    "diff_anchor": ["src/parser.c:420"],
    "change_to_sink_path": ["changed parser", "state transition", "sink"],
    "patch_refs": ["<sha or 'unknown'>"],
    "candidate_code_locations": ["path:line", "..."],
    "rationale": "...",
    "priority_reason": "why this ranks highly or lower for the focus and reachable attack surface"
  }
}
```

JSON only.

## Failure & boundaries
- If no historical patches are available, return `[]`.
- Do not file `missing` and `bypass` for the same CVE in one subtask;
  split them.

# Batch 02 proposed isolated comparison

Status: prepared for agreement on 25 October 2026. No model reviews have run.
This is a separate proposed 20-review batch, exceeding batch 01's unused
six-review correction allowance. Package 05 remains open; package 06 is blocked.

## Scope and revisions

Compare the same upstream `dcd254772fc253143889b6ab0184f31296482426` and
adapted `677beab3a37af42b08f9c46e5344b44afe84b3cf` runtime files as batch 01.
The [runtime inventory](runtime-sha256.json) is byte-identical to that batch's.
The reusable skill is unchanged. Use ten cases, once per arm, numerical order,
upstream first on odd cases and adapted first on even cases.

Proposed settings: `gpt-6.1-sol`, medium reasoning, standalone CLI
`0.164.0-alpha.11.1`, and equivalent tools for both arms. The CLI version differs
from batch 01; compare arms within this batch and disclose that difference
when discussing results across batches. Stop if either model or CLI setting
cannot be honoured; do not substitute without agreement.

The [criteria](acceptance-criteria.md), [neutral prompt](evaluator-prompt.md),
[grader-only key](answer-key.md), fixtures, and runtime inventory are pinned by
[sha256sums.txt](sha256sums.txt). The key and criteria stay outside evaluator
context. No decision is inferred from approval of the earlier adjudication.

## Fixture changes for agreement

Executable source and patches are unchanged from batch 01. Only case 03 and
04's base/head target instructions gain operational requirements. All other
fixture bytes are unchanged. These are synthetic additions for this batch,
not claims about omitted production systems.

- Case 03: the function supplies an advisory retention preview. Stored policy
  preserves the original input, expiry uses stored policy directly, and the
  preview cannot delete archives. Reading stored policy is a practical
  workaround. Proposed expected priority: P2 for incorrect preview output.
- Case 04: `render()` is the deployment procedure's required readiness gate.
  An exception prevents the next operation; no supported bypass exists.
  Proposed expected priority: P1 for failure before next operational use.

Both remain true defects. The accepted adjudication did not choose replacement
priorities; these expectations need agreement before evaluation. Retain the
original rubric, fixtures, reports, and scores in batch 01.

## Preparation and execution boundary

The [isolation record](isolation/README.md) contains two local context renders
made before supplying any case. Neither made a model call. They demonstrate a
candidate setup without repository guidance, subject to the documented limits.
Authentication, model availability, and actual session capture are untested.

After agreement, create one fresh temporary root per case/arm outside this
repository, with sibling `candidate`, `input`, `scratch`, and `codex-home`
directories. Export only `SKILL.md`, `agents`, `assets`, `reference`, `scripts`,
and `LICENSE` from the pinned arm revision. Copy only that case from this
batch's fixtures. Case 08 receives only `change.diff` and `head/AGENTS.md` as
`input/AGENTS.md`; other cases receive both snapshots, the patch, and a copy
of `head/AGENTS.md` as `input/AGENTS.md`.

Use `scratch` as the process working directory and an empty separate Codex home.
Keep the launching environment limited to the recorded keys. Use the recorded
[configured arguments](isolation/configured-command.json) for model, reasoning,
approval, and sandbox settings. Inspect a case-free `debug prompt-input` render
before supplying the case. Then render the exact substituted evaluator prompt
and check that only the chosen skill path and permitted case paths are added.
Stop if extra guidance, cases, keys, prior reports, or conclusions appear.

Use a fresh `exec --skip-git-repo-check --json` invocation after those checks;
never resume or fork. Save the exact command, environment key names, prompt,
initial context, version, timestamps, stdout events, stderr, final report,
tool/command outputs, and before/after candidate/input hashes per pair. Do not
save credentials. Inspect actual session context and traces for additional
injection; local rendering alone does not prove the executed request matches.
If the runtime cannot expose that context, leave independence unresolved.

An empty Codex home has no copied credentials. Establish an authorised local
authentication method before dispatch; do not copy account tokens into evidence
or load the user's general configuration to make authentication work. Any
required change to the recorded launch setup needs another context inspection.

Freeze raw outputs with a separate execution manifest before scoring. Record
all failures; no replacement runs or automatic corrections are proposed.
Use the same per-report fields and paired summary as batch 01, with the revised
key. A final human pass against the exact adapted revision remains required.

## Supporting validation

Fixture checks use a byte-identical copy of the seven-test batch 01 checker,
which resolves fixtures relative to its own directory. Run it with:

```bash
python3 -B plans/evidence/05-behavioural-evaluation/batch-02/fixture-checks.py
sha256sum -c plans/evidence/05-behavioural-evaluation/batch-02/sha256sums.txt
```

Its executable premises remain valid
because executable snapshots and patches are unchanged. They do not test the
added operational requirements or review accuracy. Local structure/link checks,
house style lint, manifest verification, and whitespace checks supplement them.
The preparation record is in [validation.md](validation.md).

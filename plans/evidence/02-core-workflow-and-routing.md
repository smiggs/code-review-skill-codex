# Package 02 verification and decision record

## Status and revision

Prepared on 18 October 2026 on `codex/package-02-core-workflow`, based on
`1285a4014f6bd984af054a71e37531bd9e9c1298`. Implementation is ready for the
core-workflow human checkpoint at that revision. The user subsequently confirmed
its merge into `main` and requested package 03 on 18 October 2026. Merge commit:
`e246f01fa284bde7a59e41c02a3d818670599ffd` (PR #1).

Changed material:

- `SKILL.md`: focused discovery, five-step review workflow, tool fallbacks,
  evidence requirements, findings-first output, and selective routing.
- `assets/pr-review-template.md` and `assets/review-checklist.md`: aligned output
  and inspection prompts, without automatic defect labels or merge verdicts.
- `agents/openai.yaml`: shorter review-specific UI description. The stable name,
  display name, and default automatic discovery are preserved; no tool dependency
  or invocation-policy field is added.
- `reference/review-contract.md`: introductory implementation-status notice only;
  the approved substantive contract is unchanged.
- English and Chinese README and contribution files: aligned discovery, usage,
  report expectations, and validation guidance. Installation commands are unchanged;
  both READMEs distinguish this branch from the upstream installation source.
- `AGENTS.md`, the package plan, and plan index: updated implementation status.

All 16 inherited guides, the helper, licence, and package 01 historical evidence
remain unchanged. The contract takes precedence over inherited review advice;
the guide audit remains package 03 work and helper validation remains package 04.

## Verification method and limits

The implementing agent manually followed the revised entry point and contract
using synthetic artifacts. The local and PR fixtures were created and inspected
in `/tmp/package-02-review-8d0xy7o_`, outside the project. The supplied patches,
requirements, checks, and reports are reproduced below so the record does not
depend on that temporary directory surviving.

This is a workflow exercise, not independent forward-testing, an installed-skill
discovery test, or package 05 behavioural evaluation. The agent already knew the
fixture intent. No fresh model session or automatic skill selector was invoked;
routing decisions below are manual applications of the discovery description.
The samples establish concrete report formats and tool fallbacks, not false-positive
or recall rates. No live PR, comment, approval, or repository setting was changed.

## 1. Explicit invocation and local scope

Prompt exercised:

```text
Use code-review-codex to review these local changes for supported bugs,
regressions, and violated requirements.
```

The fixture's `AGENTS.md` supplies the requirement: `None` means a 30-second
timeout; `0` means immediate return. Check inputs `None`, `0`, and `5`.
Reviews do not authorise source edits or posted reviews.

Base: `5d244a5db927698fac709612e58b29d22f12e470`. `git status --short` returned:

```text
MM wait.py
?? extra.py
```

The staged change replaces the timeout expression. An unstaged addition in the
same file calls it with `None`. `git diff HEAD -- wait.py` returned:

```diff
diff --git a/wait.py b/wait.py
index 26e3a93..21258cf 100644
--- a/wait.py
+++ b/wait.py
@@ -1,2 +1,6 @@
 def resolve_timeout(timeout):
-    return 30 if timeout is None else timeout
+    return timeout or 30
+
+
+def default_timeout():
+    return resolve_timeout(None)
```

Untracked `extra.py` contains only `TIMEOUT_UNIT = "seconds"` and was inspected
as part of the local scope. No source changes were excluded.

After inspecting the generated source, the fixture driver used
`runpy.run_path(...)["resolve_timeout"]` and called it with the three inputs.
Observed results: `None → 30`, `0 → 30`, `5 → 5`. These calls reproduce the zero
timeout defect. The requirement, changed expression, and Python truthiness also
establish the causal link without a full application.

Report produced for the checkpoint:

> [P2] Preserve zero as a valid timeout
>
> `wait.py:2` (new side): When a caller supplies `0` for immediate return, the
> truthiness fallback substitutes `30`. This violates the target's timeout
> requirement and can delay return by 30 seconds. Preserve `0` and apply the
> fallback only to `None`.
>
> Verification: direct calls returned `30` for both `None` and `0`, and `5` for
> `5`. The base expression preserves zero; the changed expression treats it as
> false. No workload or numerical confidence estimate is assumed.
>
> Scope: staged and unstaged `wait.py` changes against
> `5d244a5db927698fac709612e58b29d22f12e470`, plus untracked `extra.py`.
> Read the target instructions. No source changes excluded. Checks: inspected
> the diff and untracked file, then called the function for the required inputs.
> No application integration suite was supplied or run.

The fixture's status was identical before and after inspection and checks:
`MM wait.py` and `?? extra.py`. The review made no source or index changes.
Only the entry point, contract, and report template were needed for the review;
no language guide was needed for this self-contained expression.

## 2. Ordinary PR request and no-findings report

Prompt exercised:

```text
Review this PR for bugs and regressions.
```

This selects change review, without an explicit skill name or expanded audit.
In a synthetic local repository representing target `main` and head `refactor`,
`git merge-base main HEAD` resolved to
`1962b734fb43f2c53de3ce53286758b95bd04605`; the head was
`9318399def0d652468b52d7857a0992a78cc69c2`.
The target instructions require summing an integer list, including empty lists.
The diff between those resolved revisions was:

```diff
diff --git a/total.py b/total.py
index c5a8005..1472af7 100644
--- a/total.py
+++ b/total.py
@@ -1,3 +1,3 @@
 def total(values):
-    result = sum(values)
-    return result
+    amount = sum(values)
+    return amount
```

After inspection, the driver loaded `total.py` with `runpy.run_path` and called
`total([])`, `total([1, 2])`, and `total([-1, 1])`. Results were `0`, `3`, and `0`.
Static comparison confirmed that only the local variable name changed.

Report produced for the checkpoint:

> No actionable findings in the reviewed scope.
>
> Reviewed `total.py` from merge base
> `1962b734fb43f2c53de3ce53286758b95bd04605` to head
> `9318399def0d652468b52d7857a0992a78cc69c2`. The variable rename preserves the
> sum and return behaviour. Read the target instructions and checked empty,
> positive, and mixed-sign inputs; results were `0`, `3`, and `0`. No broader
> integration suite was supplied or run.

The fixture remained clean after review. No praise, invented criticism,
suggestions, or approval action was added. This used local evidence; it does not
claim to exercise a connected GitHub service.

## 3. Unrelated implementation request

Prompt exercised: `Add CSV export to the reporting command.`

Manual routing result: no review task is present, so the revised description
does not select this skill. No review report or defect search is warranted.
No implementation was undertaken because this prompt was only a routing probe.
Automatic discovery behaviour still needs a fresh installed-skill session.

## 4. Supplied patch without repository context

Prompt exercised: `Review this patch. I can supply no repository context.`

The patch contains a hunk at `billing.py:12` changing `charge(amount)` to
`charge(amount * 100)`. The callee contract, currency units, tests, and base/head
identifiers are absent. No repository or connector access is assumed.

Report produced:

> No actionable findings in the reviewed scope.
>
> Material question: what unit does `charge` expect? Its contract or implementation
> would establish whether multiplying by 100 corrects or introduces an error.
>
> Scope: supplied `billing.py:12` hunk only. Static inspection could not resolve
> the unit premise. Revisions, callers, and repository checks were unavailable;
> no execution or external lookup was performed.

The missing premise stays a question without a P label. With a hunk lacking line
numbers, the entry point permits a symbol or hunk location plus a disclosed limit.

## 5. Review tools unavailable

Prompt exercised: `Review this timeout patch using only the supplied text;
repository tools and execution are unavailable.` The supplied text is the
timeout function replacement from case 1 and its stated timeout requirement.

Report produced:

> [P2] Preserve zero as a valid timeout
>
> `wait.py`, `resolve_timeout` patch hunk: for `timeout = 0`, `timeout or 30`
> evaluates to `30`, whereas the previous `None` check returns `0`. This violates
> the supplied immediate-return requirement and can introduce a 30-second delay.
>
> Verification: static trace of the supplied expression and requirement only.
> Scope: the supplied function patch; line numbers, base/head IDs, callers, and
> repository checks were unavailable. No command was run for this scenario.

The scenario uses no connected tool, shell, browser, or runtime requirement.
It does not reuse the executed fixture result as though execution occurred here.

## Mechanical checks

Tools exposed during this run: Python `3.10.12`, Git `2.34.1`, and local shell
execution. No independent model run or automatic-selector metadata is available.
The installed system validator checks structure rather than review accuracy.

Results for the prepared working files:

- `python3 /home/andrew/.codex/skills/.system/skill-creator/scripts/quick_validate.py /home/andrew/projects/code-review-skill-codex`:
  passed with `Skill is valid!`. This is an installed system tool, not a script
  supplied by this repository.
- `git diff --check`: passed. The separate
  `git diff --no-index --check /dev/null plans/evidence/02-core-workflow-and-routing.md`
  check produced no whitespace errors for this added record.
- `git diff --stat`: inspected; the tracked changes cover the entry point,
  metadata, two templates, contract status, four companion documents, repository
  instructions, and two plan documents. This evidence record is an added file.
- A one-off Python Markdown scan found 65 internal file-link occurrences and
  86 self-anchor occurrences, with no missing targets. All 17 contract and guide
  routes in `SKILL.md` resolve. External links were not fetched.
- YAML inspection confirmed the stable skill name, valid metadata, a 49-character
  UI description, retained default automatic discovery, and no dependency fields.
- Byte comparisons against the base revision confirmed that 20 guide, helper,
  licence, and historical evidence files are unchanged. Comparing the contract
  from `## Scope and modes` onward confirmed that all approved substantive terms
  are unchanged.
- English and Chinese README and contribution prompt examples match. Manual
  inspection confirmed aligned review scope and authority guidance. The core
  instructions, templates, and evidence remain English only.
- Synthetic fixture checks reproduced the defect and preserved the clean control's
  outputs. Status checks confirmed no review-time source or index changes.

Content fingerprints for the entry point, metadata, templates, and contract:

```text
43c009b252d6f19f0310534436aa4a4038e700339414f314e62f4e7bafae1d5d  SKILL.md
94688c230cad4fb7b852fcf7a1384119ece47d04a31a67441ca69f67be67c619  agents/openai.yaml
be4e610c8c560db8876971b3d4cf067b7e6cf5c25ecf86c844228f6ed386158e  assets/pr-review-template.md
d4bc5b0636dd4e71fb25e802d3d2bba85063f9c273ab2ec8485a54a219141e3a  assets/review-checklist.md
9e03b8e2419894bde3bcad11015e73488d2616e0396908a42fa3d04e2b1758c6  reference/review-contract.md
```

Recalculate with `sha256sum` against the listed paths when recording the human
decision. Changes to reviewed material require proportionate revalidation.

## Human checkpoint

- Checkpoint: package 02 core workflow.
- Evidence: the revised entry point and templates, the defect report in case 1,
  the no-findings report in case 2, and the bounded scenarios above.
- AI recommendation: accept the workflow as a basis for subsequent packages,
  while retaining the fresh-session discovery and independent evaluation limits.
- Human judgement requested: clarity, useful evidence, acceptable no-findings
  output, and whether the entry point is understandable without all guides.
- Human decision: accepted through merge. The user confirmed "merged in main"
  and requested package 03 in this chat on 18 October 2026. No separate review
  rationale or reviewer identity was supplied; no requested changes were supplied.
- Remaining work: audit inherited
  references in package 03, validate the helper in package 04, and evaluate review
  behaviour independently in package 05. This change does not install or publish.

The human checkpoint is required by the
[package plan](../02-core-workflow-and-routing.md) and
[checkpoint policy](../human-ai-checkpoints.md). The user's confirmed merge
satisfies that checkpoint for the merged package 02 revision. Package 02 is
complete; subsequent changes are assessed in their own package evidence.

# Task 07 diagnostic prepared for agreement

Status on 27 October 2026: six fixture checks pass and twelve non-inference
context renders are captured. No model reviews or authentication attempts have
run. The run agreement remains pending.

The user replied “Agreed” to the [first decision brief](../07-severity-calibration.md)
and the request to prepare a general P0 clarification and concrete fixtures.
The agreed paragraph is applied to `reference/review-contract.md`; no other
runtime file changes. The `candidate/` folder is an allowlisted 31-file snapshot
of that working candidate, based on commit
`1bc100147099d08e7ad7189d766c4f8f6ff07d8f`. The manifest identifies its exact
bytes. This is an unevaluated candidate, not a replacement accepted runtime,
installed update, release, or claim of better calibration.

## Reviewable package

- [Criteria](acceptance-criteria.md) fix six attempts and separate scoring axes.
- [Withheld key](answer-key.md) supplies proposed P1/P3/P0/P2 labels and controls.
- `fixtures/case-01` through `case-06` contain original synthetic complete
  snapshots and generated patches. Their MIT notice is `fixtures/LICENSE`;
  copy that notice into each isolated input. Expected labels stay outside them.
- [Premise checker](check-fixtures.py) uses the standard library and disposable
  copies; it is withheld from model inputs. It checks concrete outcomes and
  preserves input files. No checker assertion purports to establish severity.
- `candidate-sha256sums.txt` identifies the full runtime snapshot;
  `inputs-sha256sums.txt` covers fixture input, and `preparation-sha256sums.txt`
  covers candidate, input, criteria/key, checker, prompts, commands, raw local
  context renders, preparation scripts/logs, and this protocol. The preparation
  manifest excludes itself to avoid a circular checksum.

Run the premise checks from the repository root:

```bash
python3 -B plans/evidence/07-severity-diagnostic/check-fixtures.py
```

The test-first [red result](preparation/red.txt) records six tests failing with
seven errors because snapshots did not yet exist. It is a missing-implementation
failure, not a successful defect reproduction. The [green result](preparation/green.txt)
records six passing tests after fixture creation and an additional unknown-action
assertion for case 03. The checker asserts the intended broken head behaviour
for defects, correct base behaviour, unaffected examples/workarounds, and public
equivalence for controls. It does not fix the intentionally broken heads.

`preparation/build-fixtures.py` and `preparation/render-contexts.py` preserve the
actual preparation script contents, including temporary and repository paths.
They are historical preparation tools, not a launcher to run against an approved
manifest: they overwrite preparation artefacts and create new temporary layouts.
Do not rerun them after freeze. The saved red/green outputs and commands establish
the checks performed on Python 3.14.4; Python 3.10 compatibility was not exercised.

## Context inspection and evaluator limits

The saved executable is `/usr/lib/chatgpt/resources/codex`, CLI
`0.164.0-alpha.11.1`; [runtime metadata](preparation/runtime.json) records its
SHA-256 and exact requested settings: `gpt-6.1-sol`, medium reasoning,
workspace-write limited to scratch, network disabled for review commands,
and approval policy never. Model availability and backend identity are
unverified; a rendered request does not establish the actual model setting.

For each of six fresh homes, the case-free render ran before candidate/input
copying, followed by the exact-prompt render. Every render exited zero. The
[complete-content comparison](preparation/context-comparison.json) found all
shared messages and schemas identical after normalising only layout paths;
it excludes generated message IDs/metadata from semantic comparison. Exact
rendered user prompts match the retained commands and prompt files.

Manual inspection of the complete representative message content and schema
inventory found ordinary Codex developer guidance, generic orchestration and
collaboration tools, permissions, and four bundled skills: imagegen,
openai-docs, skill-creator, and skill-installer. Other complete contexts match
that content after path normalisation. The exposed function orchestrator also
documents nested shell, file, goal, image and web capabilities. No repository
instructions, installed review/house-style skill listing, key, prior report,
sibling case, or parent conversation was present. Marker checks supplement
this content comparison; they do not independently establish isolation.
Target requirements are not injected initially: the prompt tells reviewers
to read their supplied snapshots. The schema permits more tools than the run
protocol allows; inspect actual use. No subagents are authorised.

The render emits a warning that helper aliases could not be created on the
read-only filesystem. It nevertheless exits zero; execution support remains
untested. An empty Codex home has no copied credentials or user configuration.
Proposed authentication for the eventual approved run is a temporary symlink
from that home's `auth.json` to the existing local Codex login, as in batch 02.
Do not read or retain credential bytes; record only login status and remove the
link after capture. The second checkpoint must include this proposal. If the
login cannot work, stop and retain the limit instead of changing credentials
or using another evaluator. No authentication or backend/network test ran here.

Before each approved launch, recheck the executable, candidate/input hashes,
settings, case-free and exact-prompt contexts after the authentication link is
added. Inspect actual live initial messages/settings and all subsequent tool
reads before accepting isolation. Halt on substantive differences. Saved
scratch paths may expire; reconstruct them and record substitutions as defined
in the criteria. Debug renders alone do not establish OS enforcement, usable
login, backend routing, or useful model review.

## Approval requested and subsequent evidence

Approve the preparation manifest SHA-256 together with the candidate manifest,
criteria, key, six exact prompts and launch descriptions, proposed temporary
login reuse, six-attempt bound, and disclosed limits. Record the human reply,
date and hashes before any dispatch. The earlier agreement did not approve
these exact artefacts. No current review results or scores exist.

After an agreed run, freeze every raw attempt before scoring, retain errors and
priority mismatches, and obtain human acceptance of the exact assessed candidate
and disposition. The existing batch 01/02 artefacts and package 05 completion
exceptions remain unchanged. Installation and publication remain separate.

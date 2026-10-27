# Lossless candidate storage for PR review

On 27 October 2026, CodeRabbit skipped PR 8 at commit
`12c495872330d50a83133654d21f743eb3f5c778`: 323 changed files exceeded its
300-file limit. No CodeRabbit review was completed for that head.

The unchanged 31-file candidate snapshot is now stored in
`../07-severity-diagnostic/candidate.tar.gz` instead of 31 duplicate tracked
files. This reduces the PR file count without removing evidence or changing
assessed source. Actual runtime changes, authored checks, fixtures, reports,
criteria and review records remain directly readable in the diff. No CodeRabbit
configuration or repository rule was relaxed.

Archive SHA-256:
`743852072860be779af1e9c9912636b299e2474a431e8ca0a77bffb998c14a3b`.
Its 31 regular file members retain exactly the original `candidate/...` names
and file bytes. The original candidate, input and preparation manifests remain
unchanged, as do the four execution/disposition manifests. Frozen documents
and historical commands describing a `candidate/` directory refer to the
original evaluation layout; that directory is materialised temporarily for
verification of the current archived storage. Archive storage is not a new
runtime candidate, distribution package or installation.

From the repository root, run:

```bash
python3 -B plans/evidence/07-severity-execution/test_candidate_archive.py
python3 -B plans/evidence/07-severity-execution/verify_candidate_archive.py
```

The first command has six passing standard-library tests: original bytes are
recovered, while changed bytes, missing/unlisted files, duplicate members and
symlinks are rejected. The initial test-first run failed on the missing verifier
module; no diagnostic model reviews were added. The verifier does not call
`extractall` or execute archived source. It validates members against the
original candidate manifest, materialises approved bytes under temporary
storage, and checks all seven original manifests. Verification passed before
the duplicate source directory was removed and again after storage conversion.
The new archive and verifier are not retroactively inserted into frozen input
or output manifests.

The archive has deterministic member order and zeroed gzip/tar timestamps;
member permissions are retained. The original candidate hash contract covers
file names and bytes, not an assertion about runtime execution or metadata.
All scores and case 01's unresolved isolation limitation remain unchanged.

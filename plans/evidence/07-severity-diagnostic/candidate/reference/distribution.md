# Distribution and installation

## Candidate and supported environments

Package 06 prepares a local candidate for human review. No tag, push, public
release, ChatGPT upload, or personal skill installation is implied. The exact
base revision, content hashes, archive hash, checks, and outstanding invocation
limits belong in `plans/evidence/06-documentation-and-distribution.md` in the
source checkout. A working-copy candidate is identified by its manifest as well
as its base commit; it must not be described as a committed release revision.

The commands below target Linux with Git and Python 3.10 or later. Other operating
systems and client surfaces have not been validated by package 06. Review uses
available local files and tools; optional connectors and the helper are not
required. Read [measured scope](provenance.md) and [reference status](reference-status.md)
for evaluation, technical-audit, and translation limits.

## Build the standalone archive

Run these commands from the selected, pinned source checkout. Use a fresh staging
directory. For an uncommitted candidate, record its manifest and base revision;
`git rev-parse HEAD` alone does not identify working-file contents.

```bash
git rev-parse HEAD
PACKAGE_STAGE=$(mktemp -d)
mkdir -p "$PACKAGE_STAGE/code-review-codex/scripts"
cp SKILL.md LICENSE README.md README.zh-CN.md CONTRIBUTING.md CONTRIBUTING.zh-CN.md "$PACKAGE_STAGE/code-review-codex/"
cp -R agents assets reference "$PACKAGE_STAGE/code-review-codex/"
cp scripts/pr-analyzer.py "$PACKAGE_STAGE/code-review-codex/scripts/"
mkdir -p dist
python3 -m zipfile -c "$PWD/dist/code-review-codex.zip" "$PACKAGE_STAGE/code-review-codex"
python3 -m zipfile -l dist/code-review-codex.zip
sha256sum dist/code-review-codex.zip
```

The allowlist is the six root files named above, `agents/openai.yaml`, both
`assets/*.md` templates, every intended `reference/*.md` guide, and
`scripts/pr-analyzer.py`. Inspect the staging directories before distribution;
`cp -R` also copies unexpected local files, so reject symlinks, caches, hidden
files, or paths outside this allowlist. The archive has one top-level
`code-review-codex/` folder containing `SKILL.md` and its support files. Preserve
`reference/`, rather than renaming it to `references/`.

Exclude `.git`, repository instructions, tests, plans and evaluation artefacts,
validation scripts and dependencies, caches, credentials, logs, and build
outputs. Do not ZIP the whole checkout. The [MIT notice](../LICENSE) and
[provenance](provenance.md) must accompany the skill. The full development
checkout remains necessary for its tests and historical evidence.

Unpack into a separate fresh directory:

```bash
PACKAGE_CHECK=$(mktemp -d)
python3 -m zipfile -e dist/code-review-codex.zip "$PACKAGE_CHECK"
python3 -B scripts/validate-skill.py "$PACKAGE_CHECK/code-review-codex"
python3 -B "$PACKAGE_CHECK/code-review-codex/scripts/pr-analyzer.py" --help
printf '' | python3 -B "$PACKAGE_CHECK/code-review-codex/scripts/pr-analyzer.py" --json
```

Run the validator with the source checkout's pinned PyYAML environment if the
system interpreter lacks it. Also run the available system skill-creator quick
validator on the unpacked folder. Verify every relative link and inspect licence
bytes. Exercise a representative bug and clean control through explicit and
ordinary invocation from this copy in an isolated skills location. Record actual
results; metadata discovery or a manual walkthrough alone cannot prove model
selection. Installation checks do not replace independent accuracy evaluation.

## Install locally

After choosing an approved candidate, inspect its archive and SHA-256 against
its evidence. Confirm `~/.agents/skills/code-review-codex` does not already exist:

```bash
test ! -e "$HOME/.agents/skills/code-review-codex"
```

If it exists, follow the update procedure instead of extracting over it. If the
check succeeds, install the complete folder:

```bash
mkdir -p "$HOME/.agents/skills"
python3 -m zipfile -e dist/code-review-codex.zip "$HOME/.agents/skills"
```

For a project-only installation, use that project's `.agents/skills` instead.
Do not leave duplicate copies in multiple scanned locations. OpenAI documents
automatic detection and restarting only if the change does not appear. In CLI or
IDE, inspect `/skills` and select `$code-review-codex`. See
[official skill guidance](https://learn.chatgpt.com/docs/build-skills), checked
on 25 October 2026. Client-specific availability and detection must still be
checked on the intended installation; package 06 does not validate every client.

Test with the same explicit and ordinary prompts in the [README](../README.md).
Use a synthetic repository, keep optional services disabled, and record loaded
skill paths, reference reads, findings, scope, and checks. Do not post reports
to live PRs or modify reviewed source as an installation test.

## Update and roll back

Retain the previous archive, its checksum, and its exact commit or candidate
manifest outside all scanned skill directories. Select and verify the next full
commit ID, build and check its archive, and record the resolved revision. Move
the old installed folder to a backup outside the scanned locations, then install
the verified replacement. Moving it avoids stale files from an overlay update.
Check discovery and representative review again. Restart only if detection fails.

To roll back, move the replacement outside scanned locations and restore the
previous complete folder or extract the verified previous archive into the empty
destination. Recheck discovery. Do not delete a backup until rollback is no
longer needed. Do not change a pinned installation by pulling a moving branch.

## Optional ChatGPT upload

The ZIP is an optional transport for a standalone skill folder. Use it only when
the specific surface and account explicitly support importing that structure.
The official [skill guidance](https://learn.chatgpt.com/docs/build-skills) describes
standalone and plugin skills, but the page checked on 25 October 2026 does not
establish a standalone ZIP import flow. No such UI was tested or upload performed.
A normal chat attachment does not establish installation or script execution.

For broader distribution, official guidance points to
[plugin packaging](https://developers.openai.com/plugins/build/plugins).
This candidate has no plugin manifest and is not a plugin upload. Plugin
conversion and publication require their own scope and approval. Do not infer
ChatGPT account access, importer acceptance, execution support, or universal
availability from a valid local archive.

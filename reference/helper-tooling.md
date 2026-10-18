# Helper tooling and structural validation

The optional `scripts/pr-analyzer.py` reports file identities and text additions
and deletions. These counts provide review context. They do not measure
complexity, test adequacy, risk, or review quality. The inherited scores, review
time estimates, filename classifications, and automatic review recommendations
have been removed. A documentation-only patch creates no test requirement.
The CLI filename and `--diff-file`/`--stats` options remain; the old Python
functions and report format are not a supported API.

## Diff input contract

Use Python 3.10 or later. The helper uses only the standard library, reads a
UTF-8 patch file or stdin, and never opens paths named inside the patch. It has
no network access, clock fields, or reviewed-code execution. Output order follows
input file order, and filenames are escaped for safe display.

Generate a patch with standard `a/` and `b/` prefixes, without external diff
commands or text conversion:

```bash
git diff --no-ext-diff --no-textconv --src-prefix=a/ --dst-prefix=b/ main...HEAD > /tmp/review.diff
python3 -B scripts/pr-analyzer.py --diff-file /tmp/review.diff --stats
python3 -B scripts/pr-analyzer.py --diff-file /tmp/review.diff --json
```

The comparison above is an example; choose the revisions authorised for the
review. Check the Git command's exit status before analysing its output.
The parser cannot detect missing file sections in an otherwise valid patch.

Supported input includes empty input, multiple files, unified hunks with exact
line counts, no-final-newline markers, additions, deletions, mode-only changes,
empty files, and rename/copy metadata. It handles unquoted spaces and Unicode,
and Git C-quoted UTF-8 paths including octal escapes, tabs, and newlines.
Ambiguous unquoted ` b/` or ` "b/` separators in a diff header are rejected;
rename paths containing these sequences may require another statistics tool.
File markers must agree with header paths and creation/deletion modes.

Unambiguous binary summaries (`Binary files ... differ`) mark a file as binary with zero
text counts; binary contents are not measured. `GIT binary patch` payloads,
combined merge diffs, plain unified diffs without Git headers, email patches,
custom/no prefixes, CRLF patch envelopes, non-UTF-8 paths or contents, malformed/truncated hunks,
unrecognised metadata, and extraneous content are rejected. Use an uncoloured
patch without `--binary`, `--word-diff`, or `--irreversible-delete`.
This is a deliberately restricted parser, not a patch applicability validator:
it does not verify object hashes, original file contents, or every Git metadata
combination. A valid parse does not prove that a patch applies or is complete.

Exit status 0 means supported input, including zero files for empty input.
Status 2 means an argument, I/O, encoding, or parse error, with a diagnostic on
stderr and no statistics on stdout. A failure in any section rejects the whole
input. JSON contains `total_files`, `total_additions`, `total_deletions`, and
`files`; each file contains `filename`, `additions`, `deletions`, and `binary`.

## Local validation

Python 3.10 is the supported baseline, selected from the exercised 3.10.12
runtime and the helper/validator APIs. No package build, pytest, lint, or type
checker is introduced. Git is required for the synthetic checkout test; the
suite runs on Linux and requires symlinks for the package 03 examples and POSIX
filenames for the unusual-path fixture. CI targets Python 3.10 and 3.14; other
versions and operating systems have not been validated by this package.

From the repository root, create an isolated environment and install the one
pinned validation dependency:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -B -m unittest discover -s tests -v
.venv/bin/python -B scripts/validate-skill.py
.venv/bin/python -B plans/evidence/03-python-examples.py
git diff --check
git diff --stat
```

Your Python installation must provide `venv` and `ensurepip`; on Debian/Ubuntu
these can require the matching `python3-venv` system package. Installation of
validation dependencies needs a package index or a pre-populated wheel source.
The installed skill's diff helper needs no dependency installation.

The structural validator defaults to its own repository, regardless of the
working directory; an explicit package root is also accepted. It checks YAML
frontmatter and duplicate keys, stable skill/display identities, non-empty
metadata, required package files, presence of guides, and relative Markdown link
targets. It scans Markdown outside hidden directories, fenced examples, and
inline code. It checks inline link destinations and reference definitions,
including URL-encoded paths; it ignores external URLs and fragments. It does
not check anchor existence, undefined reference labels, HTML links, every
Markdown extension, semantic agreement of prose, or licence content. Review
those manually. Structural checks do not evaluate code review accuracy.

When the system skill-creator is available, also run its `scripts/quick_validate.py`
against this repository. That external check supplements the portable validator;
CI does not depend on an installed Codex skill.

CI runs the documented checks with read-only repository permissions and pinned
actions. Its final job fails if validation fails, is cancelled, or is skipped.
Repository rulesets and required-check settings remain a separate human decision.

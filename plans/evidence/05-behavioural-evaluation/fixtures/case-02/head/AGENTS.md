# Synthetic target instructions

Review only the supplied base-to-head change and its consequences. Read the
surrounding code and this target's requirements. Reports are advisory; do not
edit source, commit, post comments, approve, merge, or access external services.
Use Python 3.10 or later and only the standard library for any checks. Run
checks in a temporary copy; preserve the supplied snapshots. No test suite is
supplied. State which checks you actually ran and their limits.

## Requirements

The backup can be the only surviving copy. On a failed destination write,
retain the backup for retry. The destination parent can be missing.

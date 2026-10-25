# Synthetic target instructions

Review only the supplied base-to-head change and its consequences. Read the
surrounding code and this target's requirements. Reports are advisory; do not
edit source, commit, post comments, approve, merge, or access external services.
Use Python 3.10 or later and only the standard library for any checks. Run
checks in a temporary copy; preserve the supplied snapshots. No test suite is
supplied. State which checks you actually ran and their limits.

## Requirements

This cache accepts only None or positive integer days. None means seven days.
The caller validates inputs before calling retention_days; zero, negative
values, booleans, strings, and other types are outside the supported domain.

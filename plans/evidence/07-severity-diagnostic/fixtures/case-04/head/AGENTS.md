# Synthetic target requirements

Review only the supplied base-to-head change and its reachable consequences.
Read all supplied source and requirements. Review authority is advisory: do not
edit inputs, commit, post, approve, merge, or contact external services. Checks
may use Python 3.10 or later and the standard library in a scratch copy; do not
write bytecode into snapshots. No test suite is supplied. State actual checks
and their limits. All examples are synthetic and distributed under the
accompanying MIT licence. These requirements apply equally to both snapshots.

## Supported behaviour and operational context

`export_rows(values, page_size)` must return all supplied values in order.
Supported values are finite lists of integer record IDs, including empty lists;
page_size is a positive integer. The function combines pages into one export.
It must preserve every row even when the final page is full.

The export is an advisory offline copy only. Authoritative records remain in
the supplied values and are unaffected by export; no downstream automation
consumes the output. Users can select any positive page size. For the affected
six-row export with default page size three, the documented alternate page
size is four. Users retain access to authoritative records and can re-export.
This display/export problem cannot delete or modify authoritative records.

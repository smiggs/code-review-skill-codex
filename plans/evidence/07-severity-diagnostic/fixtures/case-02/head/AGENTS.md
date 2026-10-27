# Synthetic target requirements

Review only the supplied base-to-head change and its reachable consequences.
Read all supplied source and requirements. Review authority is advisory: do not
edit inputs, commit, post, approve, merge, or contact external services. Checks
may use Python 3.10 or later and the standard library in a scratch copy; do not
write bytecode into snapshots. No test suite is supplied. State actual checks
and their limits. All examples are synthetic and distributed under the
accompanying MIT licence. These requirements apply equally to both snapshots.

## Supported behaviour and operational context

Supported input is a list of item-name strings, including an empty list.
`summary(items)` must return exactly `Items: N.` where N is the item count,
including the final full stop. This is an explicit human-facing format
requirement. `data(items)` must return the count and the input item names.

No software parses the summary text, no operational decision depends on its
punctuation, and the separate machine-readable `data()` result drives all
inventory operations. The summary is displayed only to humans. A punctuation
error does not change stock, names, counts, or any transaction.

# Synthetic target requirements

Review only the supplied base-to-head change and its reachable consequences.
Read all supplied source and requirements. Review authority is advisory: do not
edit inputs, commit, post, approve, merge, or contact external services. Checks
may use Python 3.10 or later and the standard library in a scratch copy; do not
write bytecode into snapshots. No test suite is supplied. State actual checks
and their limits. All examples are synthetic and distributed under the
accompanying MIT licence. These requirements apply equally to both snapshots.

## Supported behaviour and operational context

`post(records)` produces the daily invoice posting records. Supported input
is a list of `(supplier, invoice_id, amount)` tuples with non-empty supplier
strings, positive integer IDs, and positive integer amounts in minor units.
Each `(supplier, invoice_id)` pair occurs once per input. IDs are unique only
within one supplier; different suppliers can reuse an ID. Every supplied
invoice must appear once in the posting output, in input order.

The next daily run includes suppliers north and south, each with ID 7, with
amounts 100 and 250. This is the required financial posting path and has no
alternate importer. Omission silently leaves that supplier invoice unposted,
with no automatic retry or omission alert. Invoice posting is a core operational
requirement. The candidate has not been deployed, the current service is working,
and correction is needed before the next daily run. No current loss is asserted.

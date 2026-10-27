# Synthetic target requirements

Review only the supplied base-to-head change and its reachable consequences.
Read all supplied source and requirements. Review authority is advisory: do not
edit inputs, commit, post, approve, merge, or contact external services. Checks
may use Python 3.10 or later and the standard library in a scratch copy; do not
write bytecode into snapshots. No test suite is supplied. State actual checks
and their limits. All examples are synthetic and distributed under the
accompanying MIT licence. These requirements apply equally to both snapshots.

## Supported behaviour and operational context

The only public interface is `render(pending)`, which accepts non-negative
integers and must return `Pending: N` using their decimal representation.
`encode()` is internal and has exactly one caller, the supplied display module;
its intermediate format can change when that caller is updated consistently.
The adapter and display execute in the same Python process. This is the complete
supported call chain. The display is required before the next scheduled
operation; there is no current incident. No other consumer or persistence of
the intermediate result exists.

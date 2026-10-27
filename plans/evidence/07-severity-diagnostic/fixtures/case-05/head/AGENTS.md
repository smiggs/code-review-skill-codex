# Synthetic target requirements

Review only the supplied base-to-head change and its reachable consequences.
Read all supplied source and requirements. Review authority is advisory: do not
edit inputs, commit, post, approve, merge, or contact external services. Checks
may use Python 3.10 or later and the standard library in a scratch copy; do not
write bytecode into snapshots. No test suite is supplied. State actual checks
and their limits. All examples are synthetic and distributed under the
accompanying MIT licence. These requirements apply equally to both snapshots.

## Supported behaviour and operational context

Supported inputs to `allowed(role, action)` are strings. The complete role
classes are admin, reader, and any other string (unknown role). The complete
action classes are read, write, and any other string (unknown action). Admin
may read and write; reader may only read. Unknown roles and unknown actions
must return False. The return value is Boolean. This is a core access path;
the refactor must preserve all supported permission decisions.

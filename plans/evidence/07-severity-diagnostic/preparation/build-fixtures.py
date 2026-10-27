from pathlib import Path
import difflib

root = Path('/home/andrew/projects/code-review-skill-codex/plans/evidence/07-severity-diagnostic/fixtures')
common = '''# Synthetic target requirements

Review only the supplied base-to-head change and its reachable consequences.
Read all supplied source and requirements. Review authority is advisory: do not
edit inputs, commit, post, approve, merge, or contact external services. Checks
may use Python 3.10 or later and the standard library in a scratch copy; do not
write bytecode into snapshots. No test suite is supplied. State actual checks
and their limits. All examples are synthetic and distributed under the
accompanying MIT licence. These requirements apply equally to both snapshots.

## Supported behaviour and operational context

'''

def write_case(number, requirement, base, head):
    case = root / f'case-{number:02}'
    for side, files in [('base', base), ('head', head)]:
        target = case / side
        target.mkdir(parents=True, exist_ok=True)
        (target / 'AGENTS.md').write_text(common + requirement)
        for name, content in files.items():
            (target / name).write_text(content)
    patch = ''
    for name in sorted(base):
        if base[name] != head[name]:
            patch += f'diff --git a/{name} b/{name}\n'
            patch += ''.join(difflib.unified_diff(base[name].splitlines(True), head[name].splitlines(True), fromfile='a/'+name, tofile='b/'+name))
    (case / 'change.diff').write_text(patch)

base = {'merge.py': '''def incoming(records):
    merged = {}
    for supplier, invoice_id, amount in records:
        merged[(supplier, invoice_id)] = (supplier, invoice_id, amount)
    return list(merged.values())
''', 'posting.py': '''from merge import incoming


def post(records):
    return incoming(records)
'''}
head = dict(base); head['merge.py'] = base['merge.py'].replace('merged[(supplier, invoice_id)]', 'merged[invoice_id]')
write_case(1, '''`post(records)` produces the daily invoice posting records. Supported input
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
''', base, head)

base = {'inventory.py': '''def summary(items):
    return f"Items: {len(items)}."


def data(items):
    return {"count": len(items), "items": list(items)}
'''}
head = {'inventory.py': base['inventory.py'].replace('{len(items)}.', '{len(items)}')}
write_case(2, '''Supported input is a list of item-name strings, including an empty list.
`summary(items)` must return exactly `Items: N.` where N is the item count,
including the final full stop. This is an explicit human-facing format
requirement. `data(items)` must return the count and the input item names.

No software parses the summary text, no operational decision depends on its
punctuation, and the separate machine-readable `data()` result drives all
inventory operations. The summary is displayed only to humans. A punctuation
error does not change stock, names, counts, or any transaction.
''', base, head)

base = {'dispatcher.py': '''OPERATIONS = {"ping", "echo", "count"}


def execute(operation, value):
    if operation not in OPERATIONS:
        raise ValueError("unsupported operation")
    if operation == "ping":
        return "pong"
    if operation == "echo":
        return value
    return len(value)
''', 'service.py': '''from dispatcher import execute


def handle(operation, value):
    return execute(operation, value)
'''}
head = dict(base); head['dispatcher.py'] = base['dispatcher.py'].replace('operation not in OPERATIONS', 'operation in OPERATIONS')
write_case(3, '''`handle(operation, value)` is the sole public request entry point. Supported
operations are exactly ping, echo, and count; values are strings. Ping returns
pong, echo returns the supplied string, and count returns its length. Unknown
operations must raise ValueError. Every supported customer request follows the
supplied service-to-dispatcher path; there is no alternate route or bypass.

Synthetic incident record: this head revision is active across the service.
Every supported customer request is failing for all customers, starting with
this rollout. The incident is ongoing and requires immediate restoration.
There are no additional deployment flags or input prerequisites. This is a
supplied synthetic operational premise, not a real production observation.
The source snapshots contain the complete dispatch path; no actual network or
production deployment is part of the fixture or an authorised check.
''', base, head)

base = {'export.py': '''def export_rows(values, page_size):
    remainder = len(values) % page_size
    full_end = len(values) - remainder
    result = []
    for start in range(0, full_end, page_size):
        result.extend(values[start:start + page_size])
    if remainder:
        result.extend(values[full_end:])
    return result
'''}
head = {'export.py': base['export.py'].replace('len(values) - remainder', 'len(values) - (remainder or page_size)')}
write_case(4, '''`export_rows(values, page_size)` must return all supplied values in order.
Supported values are finite lists of integer record IDs, including empty lists;
page_size is a positive integer. The function combines pages into one export.
It must preserve every row even when the final page is full.

The export is an advisory offline copy only. Authoritative records remain in
the supplied values and are unaffected by export; no downstream automation
consumes the output. Users can select any positive page size. For the affected
six-row export with default page size three, the documented alternate page
size is four. Users retain access to authoritative records and can re-export.
This display/export problem cannot delete or modify authoritative records.
''', base, head)

base = {'permissions.py': '''RIGHTS = {"admin": {"read", "write"}, "reader": {"read"}}
ACTIONS = {"read", "write"}


def allowed(role, action):
    if action not in ACTIONS:
        return False
    return action in RIGHTS.get(role, set())
'''}
head = {'permissions.py': '''RIGHTS = {"admin": {"read", "write"}, "reader": {"read"}}
ACTIONS = {"read", "write"}


def allowed(role, action):
    return action in ACTIONS and action in RIGHTS.get(role, set())
'''}
write_case(5, '''Supported inputs to `allowed(role, action)` are strings. The complete role
classes are admin, reader, and any other string (unknown role). The complete
action classes are read, write, and any other string (unknown action). Admin
may read and write; reader may only read. Unknown roles and unknown actions
must return False. The return value is Boolean. This is a core access path;
the refactor must preserve all supported permission decisions.
''', base, head)

base = {'adapter.py': '''def encode(pending):
    return {"pending": pending}
''', 'display.py': '''from adapter import encode


def render(pending):
    payload = encode(pending)
    return f"Pending: {payload['pending']}"
'''}
head = {'adapter.py': '''import json


def encode(pending):
    return json.dumps({"pending": pending})
''', 'display.py': '''import json

from adapter import encode


def render(pending):
    payload = json.loads(encode(pending))
    return f"Pending: {payload['pending']}"
'''}
write_case(6, '''The only public interface is `render(pending)`, which accepts non-negative
integers and must return `Pending: N` using their decimal representation.
`encode()` is internal and has exactly one caller, the supplied display module;
its intermediate format can change when that caller is updated consistently.
The adapter and display execute in the same Python process. This is the complete
supported call chain. The display is required before the next scheduled
operation; there is no current incident. No other consumer or persistence of
the intermediate result exists.
''', base, head)

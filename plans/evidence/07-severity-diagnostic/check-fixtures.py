"""Checks synthetic operational premises; never invokes a review model."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent


def run(case, side, expression):
    """Runs a complete snapshot in a disposable copy without bytecode writes."""
    source = ROOT / 'fixtures' / f'case-{case:02}' / side
    with tempfile.TemporaryDirectory(prefix='severity-premise-') as temporary:
        scratch = Path(temporary) / 'input'
        shutil.copytree(source, scratch)
        result = subprocess.run(
            [sys.executable, '-B', '-c', expression], cwd=scratch,
            text=True, capture_output=True, check=True,
        )
        return json.loads(result.stdout)


class FixturePremises(unittest.TestCase):
    def test_supplier_collision_omits_a_posting_only_in_head(self):
        for side in ('base', 'head'):
            with self.subTest(side=side):
                result = run(1, side, '''from posting import post
import json
print(json.dumps([post(rows) for rows in (
    [('north', 7, 100), ('south', 7, 250)],
    [('north', 7, 100), ('south', 8, 250)],
    [('north', 7, 100)],
)]))''')
                self.assertEqual(result[0], [['north', 7, 100], ['south', 7, 250]]
                                 if side == 'base' else [['south', 7, 250]])
                self.assertEqual(result[1], [['north', 7, 100], ['south', 8, 250]])
                self.assertEqual(result[2], [['north', 7, 100]])

    def test_punctuation_has_no_machine_data_consequence(self):
        for side in ('base', 'head'):
            result = run(2, side, '''from inventory import summary, data
import json
print(json.dumps([[summary(items), data(items)] for items in ([], ['bolt', 'nut'])]))''')
            ending = '.' if side == 'base' else ''
            self.assertEqual(result, [
                [f'Items: 0{ending}', {'count': 0, 'items': []}],
                [f'Items: 2{ending}', {'count': 2, 'items': ['bolt', 'nut']}],
            ])

    def test_all_supported_service_operations_fail_in_head(self):
        for side in ('base', 'head'):
            result = run(3, side, '''from service import handle
import json
outputs = []
for operation in ('ping', 'echo', 'count', 'unknown'):
    try:
        outputs.append(handle(operation, 'hello'))
    except ValueError as error:
        outputs.append(str(error))
print(json.dumps(outputs))''')
            self.assertEqual(result, ['pong', 'hello', 5, 'unsupported operation']
                             if side == 'base' else ['unsupported operation'] * 3 + [5])

    def test_export_loss_is_bounded_and_workaround_is_complete(self):
        for side in ('base', 'head'):
            result = run(4, side, '''from export import export_rows
import json
print(json.dumps([export_rows(list(range(n)), size) for n, size in (
    (0, 3), (1, 3), (6, 3), (7, 3), (6, 4),
)]))''')
            self.assertEqual(result, [[], [0], list(range(6)) if side == 'base'
                                     else [0, 1, 2], list(range(7)), list(range(6))])

    def test_permission_refactor_preserves_complete_supported_matrix(self):
        expected = [True, True, False, True, False, False, False, False, False]
        for side in ('base', 'head'):
            result = run(5, side, '''from permissions import allowed
import json
print(json.dumps([allowed(role, action)
    for role in ('admin', 'reader', 'unknown')
    for action in ('read', 'write', 'unknown')]))''')
            self.assertEqual(result, expected)

    def test_adapter_and_consumer_change_preserves_public_results(self):
        for side in ('base', 'head'):
            result = run(6, side, '''from display import render
import json
print(json.dumps([render(value) for value in (0, 1, 12)]))''')
            self.assertEqual(result, ['Pending: 0', 'Pending: 1', 'Pending: 12'])


if __name__ == '__main__':
    unittest.main(verbosity=2)

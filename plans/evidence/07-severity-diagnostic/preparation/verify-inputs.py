"""Records patch applicability and immutable-input checks without model calls."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def hashes(folder):
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(folder.rglob('*')) if p.is_file()}


before = hashes(ROOT / 'fixtures') | hashes(ROOT / 'candidate')
results = []
for case in sorted((ROOT / 'fixtures').glob('case-*')):
    with tempfile.TemporaryDirectory(prefix='severity-patch-check-') as temporary:
        scratch = Path(temporary) / 'input'
        shutil.copytree(case / 'base', scratch)
        patch = str(case / 'change.diff')
        for arguments in (['git', 'apply', '--check', patch], ['git', 'apply', patch]):
            subprocess.run(arguments, cwd=scratch, check=True, capture_output=True, text=True)
        expected = {str(p.relative_to(case / 'head')): p.read_bytes()
                    for p in (case / 'head').rglob('*') if p.is_file()}
        actual = {str(p.relative_to(scratch)): p.read_bytes()
                  for p in scratch.rglob('*') if p.is_file()}
        if expected != actual:
            raise RuntimeError(f'Applied patch differs from head: {case.name}')
        results.append({'case': case.name, 'patch_applies': True, 'patched_tree_matches_head': True})
result = subprocess.run([sys.executable, '-B', str(ROOT / 'check-fixtures.py')],
                        capture_output=True, text=True)
(ROOT / 'preparation/green.txt').write_text(result.stdout + result.stderr)
if result.returncode:
    raise RuntimeError('Fixture premise checks failed')
after = hashes(ROOT / 'fixtures') | hashes(ROOT / 'candidate')
if before != after:
    raise RuntimeError('Inputs or candidate changed during validation')
(ROOT / 'preparation/input-integrity.json').write_text(json.dumps({
    'cases': results, 'before': before, 'after': after,
    'inputs_unchanged': True, 'premise_check_exit_code': result.returncode,
}, indent=2) + '\n')
print('Six patches apply to exact heads; six premise tests pass; all input/candidate hashes unchanged.')

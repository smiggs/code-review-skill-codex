"""Launches one approved slot once, retaining all public output and errors."""

from pathlib import Path
import datetime
import hashlib
import json
import shutil
import subprocess
import sys

execution = Path(__file__).resolve().parent
case = f'case-{int(sys.argv[1]):02}'
record = execution / case
assert json.loads((record / 'preflight-audit.json').read_text())['status'] == 'passed'
command = json.loads((record / 'command.json').read_text())
layout = Path(command['cwd']).parent
link = Path(command['environment']['CODEX_HOME']) / 'auth.json'
metadata = {'case': case, 'model_requested': 'gpt-6.1-sol', 'reasoning_requested': 'medium',
            'workspace': str(layout), 'status': 'running',
            'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat()}
# Exclusive creation is the once-only dispatch guard.
with (record / 'metadata.json').open('x') as file:
    json.dump(metadata, file, indent=2)
try:
    before = json.loads((record / 'hashes-before.json').read_text())
    for relative, expected in before.items():
        assert hashlib.sha256((layout / relative).read_bytes()).hexdigest() == expected
    print(f'Starting approved {case}', flush=True)
    with (record / 'events.jsonl').open('x') as stdout, (record / 'stderr.txt').open('x') as stderr:
        result = subprocess.run(command['argv'], cwd=command['cwd'], env=command['environment'],
                                input=(record / 'prompt.md').read_text(), text=True,
                                stdout=stdout, stderr=stderr)
    metadata['exit_code'] = result.returncode
    metadata['status'] = 'finished' if result.returncode == 0 else 'failed'
finally:
    after = {str(p.relative_to(layout)): hashlib.sha256(p.read_bytes()).hexdigest()
             for name in ('candidate', 'input') for p in sorted((layout / name).rglob('*')) if p.is_file()}
    (record / 'hashes-after.json').write_text(json.dumps(after, indent=2) + '\n')
    metadata['inputs_unchanged'] = json.loads((record / 'hashes-before.json').read_text()) == after
    metadata['finished_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    report = layout / 'final-report.txt'
    if report.is_file():
        shutil.copyfile(report, record / 'report.txt')
    if link.is_symlink():
        link.unlink()
    metadata['authentication_link_removed'] = not link.is_symlink()
    (record / 'metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(json.dumps(metadata), flush=True)

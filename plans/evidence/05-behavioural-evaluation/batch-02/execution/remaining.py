from pathlib import Path
import json
import subprocess

execution = Path('/home/andrew/projects/code-review-skill-codex/plans/evidence/05-behavioural-evaluation/batch-02/execution')
order = json.loads((execution / 'order.json').read_text())
for pair in order[2:]:
    name = f'{pair["case"]}-{pair["arm"]}'
    result = subprocess.run(['python3', '-B', '/tmp/batch02-run-pair.py', pair['case'], pair['arm']])
    if result.returncode:
        print(f'Stopped after failed pair {name}; no retry.', flush=True)
        raise SystemExit(result.returncode)
    result = subprocess.run(['python3', '-B', '/tmp/batch02-audit-pair.py', name])
    if result.returncode:
        print(f'Stopped after context audit failed for {name}.', flush=True)
        raise SystemExit(result.returncode)
print('All remaining planned pairs finished without reruns.', flush=True)

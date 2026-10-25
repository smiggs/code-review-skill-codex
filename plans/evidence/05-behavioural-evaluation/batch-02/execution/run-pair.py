from pathlib import Path
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

repo = Path('/home/andrew/projects/code-review-skill-codex')
batch = repo / 'plans/evidence/05-behavioural-evaluation/batch-02'
case, arm = sys.argv[1:]
record = batch / 'execution' / f'{case}-{arm}'
record.mkdir(exist_ok=False)
root = Path(tempfile.mkdtemp(prefix='review-batch02-'))
for name in ('candidate', 'input', 'scratch', 'codex-home'):
    (root / name).mkdir()
source_auth = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'auth.json'
(root / 'codex-home/auth.json').symlink_to(source_auth)
env = {'PATH': '/usr/bin:/bin', 'HOME': os.environ['HOME'], 'LANG': 'C.UTF-8',
       'CODEX_HOME': str(root / 'codex-home')}
config = json.loads((batch / 'isolation/configured-command.json').read_text())['argv'][:-3]
neutral = 'Context inspection only. No review case has been supplied. Do not inspect files, call tools, or perform a review.'

def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')

def hashes():
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for name in ('candidate', 'input') for p in sorted((root / name).rglob('*'))
            if p.is_file()}

def inspect(prompt, label):
    command = config + ['debug', 'prompt-input', prompt]
    result = subprocess.run(command, cwd=root / 'scratch', env=env,
                            capture_output=True, text=True, timeout=30)
    (record / f'{label}.json').write_text(result.stdout)
    (record / f'{label}-stderr.txt').write_text(result.stderr)
    if result.returncode:
        raise RuntimeError(f'{label}: renderer failed with {result.returncode}')
    data = json.loads(result.stdout)
    user = [item for item in data if item.get('role') == 'user']
    texts = [part.get('text', '') for item in data for part in item.get('content', [])]
    combined = '\n'.join(texts)
    assert len(user) == 2, f'{label}: unexpected user context'
    assert user[-1]['content'][0]['text'] == prompt
    assert '# AGENTS.md instructions' not in combined
    assert str(repo) not in combined
    assert 'review-contract.md' not in combined
    assert 'answer-key.md' not in combined
    assert 'acceptance-criteria.md' not in combined
    assert 'No review case has been supplied' in combined if label == 'case-free-context' else True
    assert "`sandbox_mode` is `workspace-write`" in combined
    assert f'The writable root is `{root / "scratch"}`' in combined
    return {'user_messages': len(user), 'repository_instructions': False,
            'repository_path': False, 'grader_inputs': False}

metadata = {'case': case, 'arm': arm, 'workspace': str(root),
            'date': '2026-10-25', 'model_requested': 'gpt-6.1-sol',
            'reasoning_requested': 'medium', 'cli': '0.164.0-alpha.11.1',
            'environment_keys': sorted(env), 'authentication': 'existing-login-file symlink',
            'status': 'preparing'}
write_json(record / 'metadata.json', metadata)
metadata['case_free_audit'] = inspect(neutral, 'case-free-context')
inventory = json.loads((batch / 'runtime-sha256.json').read_text())[arm]
metadata['revision'] = inventory['revision']
for relative, expected in inventory['files'].items():
    content = subprocess.run(['git', 'show', f'{inventory["revision"]}:{relative}'], cwd=repo,
                             capture_output=True, check=True).stdout
    assert hashlib.sha256(content).hexdigest() == expected
    target = root / 'candidate' / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
fixture = batch / 'fixtures' / case
if case != 'case-08':
    for name in ('base', 'head'):
        shutil.copytree(fixture / name, root / 'input' / name)
shutil.copyfile(fixture / 'change.diff', root / 'input/change.diff')
shutil.copyfile(fixture / 'head/AGENTS.md', root / 'input/AGENTS.md')
prompt = (batch / 'evaluator-prompt.md').read_text()
for key, value in [('CANDIDATE', root / 'candidate'), ('INPUT', root / 'input'),
                   ('SCRATCH', root / 'scratch')]:
    prompt = prompt.replace(key, str(value))
(record / 'prompt.md').write_text(prompt)
metadata['review_context_audit'] = inspect(prompt, 'review-context')
write_json(record / 'hashes-before.json', hashes())
command = config + ['exec', '--skip-git-repo-check', '--json', '--color', 'never',
                    '--output-last-message', str(root / 'final-report.txt'), '-']
write_json(record / 'command.json', {'argv': command, 'cwd': str(root / 'scratch'),
                                   'environment_keys': sorted(env), 'stdin': 'prompt.md'})
metadata['status'] = 'running'
metadata['started_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
write_json(record / 'metadata.json', metadata)
print(f'Starting {case}-{arm} in {root}', flush=True)
with (record / 'events.jsonl').open('w') as stdout, (record / 'stderr.txt').open('w') as stderr:
    process = subprocess.Popen(command, cwd=root / 'scratch', env=env, stdin=subprocess.PIPE,
                               stdout=stdout, stderr=stderr, text=True)
    try:
        process.communicate(prompt, timeout=240)
    except subprocess.TimeoutExpired:
        process.terminate()
        process.wait(timeout=10)
        metadata['timeout'] = True
metadata['exit_code'] = process.returncode
metadata['finished_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
metadata['status'] = 'finished' if process.returncode == 0 else 'failed'
if (root / 'final-report.txt').exists():
    shutil.copyfile(root / 'final-report.txt', record / 'report.txt')
write_json(record / 'hashes-after.json', hashes())
metadata['inputs_unchanged'] = json.loads((record / 'hashes-before.json').read_text()) == hashes()
metadata['session_files'] = [str(p) for p in (root / 'codex-home').rglob('rollout-*.jsonl')]
write_json(record / 'metadata.json', metadata)
print(json.dumps(metadata), flush=True)
raise SystemExit(process.returncode or (0 if metadata['inputs_unchanged'] else 1))

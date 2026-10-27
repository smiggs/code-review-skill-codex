"""Rechecks one approved slot without inference; never reads credential bytes."""

from pathlib import Path
import hashlib
import json
import subprocess
import sys

EXECUTION = Path(__file__).resolve().parent
PACKAGE = EXECUTION.parent / '07-severity-diagnostic'
case = f'case-{int(sys.argv[1]):02}'
if case not in {f'case-{n:02}' for n in range(1, 7)}:
    raise SystemExit('Unapproved slot')
record = EXECUTION / case
record.mkdir(exist_ok=False)
launch = json.loads((PACKAGE / 'preparation' / case / 'proposed-launch.json').read_text())
layout = Path(launch['cwd']).parent
home = Path(launch['environment']['CODEX_HOME'])
link = home / 'auth.json'


def write(name, value):
    (record / name).write_text(json.dumps(value, indent=2) + '\n')


def semantic(data):
    return [{k: item[k] for k in ('type', 'role', 'content', 'tools') if k in item}
            for item in data]


try:
    agreement = json.loads((EXECUTION / 'agreement.json').read_text())
    manifest = PACKAGE / 'preparation-sha256sums.txt'
    assert hashlib.sha256(manifest.read_bytes()).hexdigest() == agreement['preparation_manifest_sha256']
    for line in manifest.read_text().splitlines():
        expected, relative = line.split('  ', 1)
        assert hashlib.sha256((PACKAGE / relative).read_bytes()).hexdigest() == expected, relative
    runtime = json.loads((PACKAGE / 'preparation/runtime.json').read_text())
    assert hashlib.sha256(Path(launch['argv'][0]).read_bytes()).hexdigest() == runtime['executable_sha256']
    assert not list(home.rglob('rollout-*.jsonl')), 'Home already used'
    assert not link.exists() and not link.is_symlink(), 'Authentication link already present'
    link.symlink_to('/home/andrew/.codex/auth.json')
    config = launch['argv'][:launch['argv'].index('exec')]
    auth = subprocess.run([launch['argv'][0], 'login', 'status'],
                          cwd=launch['cwd'], env=launch['environment'], capture_output=True, text=True)
    write('authentication-check.json', {'exit_code': auth.returncode,
          'method': 'Existing local login via temporary auth.json symlink; no credential bytes read or retained',
          'authenticated': auth.returncode == 0, 'raw_identity_output': 'Not retained'})
    assert auth.returncode == 0, 'Existing login unavailable'
    audits = []
    for label, old_name in [('case-free', 'case-free-command.json'), ('prompted', 'prompted-command.json')]:
        old = json.loads((PACKAGE / 'preparation' / case / old_name).read_text())
        command = old['argv']
        result = subprocess.run(command, cwd=launch['cwd'], env=launch['environment'],
                                capture_output=True, text=True)
        (record / f'{label}-context.json').write_text(result.stdout)
        (record / f'{label}-stderr.txt').write_text(result.stderr)
        write(f'{label}-command.json', dict(old, exit_code=result.returncode))
        assert result.returncode == 0, f'{label}: render failed'
        actual = semantic(json.loads(result.stdout))
        approved = semantic(json.loads((PACKAGE / 'preparation' / case / f'{label}-context.json').read_text()))
        assert actual == approved, f'{label}: substantive context changed'
        audits.append({'render': label, 'complete_semantic_context_matches_approved': True})
        # The exact case prompt is not passed until the case-free comparison passes.
    expected = {}
    for folder, manifest_name in [('candidate', 'candidate-sha256sums.txt'), ('input', 'inputs-sha256sums.txt')]:
        for line in (PACKAGE / manifest_name).read_text().splitlines():
            digest, relative = line.split('  ', 1)
            rel = Path(relative)
            if folder == 'candidate':
                target = layout / relative
            elif rel == Path('fixtures/LICENSE'):
                target = layout / 'input/LICENSE'
            elif rel.parts[1] == case:
                target = layout / 'input' / Path(*rel.parts[2:])
            else:
                continue
            assert hashlib.sha256(target.read_bytes()).hexdigest() == digest, target
            expected[str(target.relative_to(layout))] = digest
    actual_files = {str(p.relative_to(layout)) for folder in ('candidate', 'input')
                    for p in (layout / folder).rglob('*') if p.is_file()}
    assert actual_files == set(expected), 'Extra or absent input files'
    write('hashes-before.json', expected)
    prompt = (PACKAGE / 'preparation' / case / 'prompt.md').read_text()
    (record / 'prompt.md').write_text(prompt)
    write('command.json', launch)
    write('preflight-audit.json', {'case': case, 'status': 'passed', 'contexts': audits,
          'executable_unchanged': True, 'candidate_inputs_match_manifest': True,
          'reviews_dispatched': 0, 'authentication_verified': True})
    print(f'{case}: authenticated; both full contexts match approval; executable/input/candidate hashes match.')
except BaseException:
    if link.is_symlink():
        link.unlink()
    raise

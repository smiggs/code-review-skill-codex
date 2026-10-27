from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import tempfile

repo = Path('/home/andrew/projects/code-review-skill-codex')
out = repo / 'plans/evidence/07-severity-diagnostic'
preparation = out / 'preparation'
exe = Path(shutil.which('codex')).resolve()
settings = ['-c', 'model="gpt-6.1-sol"', '-c', 'model_reasoning_effort="medium"',
            '-c', 'approval_policy="never"', '-c', 'sandbox_mode="workspace-write"',
            '-c', 'sandbox_workspace_write.exclude_slash_tmp=true',
            '-c', 'sandbox_workspace_write.exclude_tmpdir_env_var=true',
            '-c', 'sandbox_workspace_write.network_access=false']
files = [Path(p) for p in ('SKILL.md', 'LICENSE', 'README.md', 'README.zh-CN.md',
                         'CONTRIBUTING.md', 'CONTRIBUTING.zh-CN.md',
                         'agents/openai.yaml', 'scripts/pr-analyzer.py')]
files += sorted(Path('assets').glob('*.md')) + sorted(Path('reference').glob('*.md'))
candidate = out / 'candidate'
for rel in files:
    target = candidate / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(repo / rel, target)
shutil.copy2(repo / 'LICENSE', out / 'fixtures/LICENSE')
metadata = {'executable': str(exe), 'executable_sha256': hashlib.sha256(exe.read_bytes()).hexdigest(),
            'python': subprocess.run(['python3', '--version'], capture_output=True, text=True).stdout.strip(),
            'settings': settings, 'authentication': 'Not attempted; no credentials linked or copied.',
            'review_attempts': 0}
for kind, args in [('version', ['--version']), ('exec-help', ['exec', '--help']),
                   ('prompt-input-help', ['debug', 'prompt-input', '--help'])]:
    result = subprocess.run([str(exe)] + args, text=True, capture_output=True)
    (preparation / f'{kind}.txt').write_text(result.stdout + result.stderr)
    metadata[kind + '_exit_code'] = result.returncode

for number in range(1, 7):
    evidence = preparation / f'case-{number:02}'
    evidence.mkdir(parents=True, exist_ok=True)
    layout = Path(tempfile.mkdtemp(prefix=f'task07-case{number:02}-'))
    scratch = layout / 'scratch'; scratch.mkdir()
    home = layout / 'codex-home'; home.mkdir()
    environment = {'PATH': '/usr/bin:/bin', 'HOME': os.environ['HOME'],
                   'LANG': 'C.UTF-8', 'CODEX_HOME': str(home)}
    command = [str(exe)] + settings
    casefree = 'Context inspection only. No review case has been supplied. Do not inspect files, call tools, or perform a review.'
    for label, prompt in [('case-free', casefree)]:
        argv = command + ['debug', 'prompt-input', prompt]
        result = subprocess.run(argv, cwd=scratch, env=environment, capture_output=True, text=True)
        (evidence / f'{label}-context.json').write_text(result.stdout)
        (evidence / f'{label}-stderr.txt').write_text(result.stderr)
        (evidence / f'{label}-command.json').write_text(json.dumps(
            {'argv': argv, 'cwd': str(scratch), 'environment': environment,
             'exit_code': result.returncode}, indent=2) + '\n')
        if result.returncode:
            raise SystemExit(f'Context render failed: case {number}')
    # Inputs are copied only after the case-free context was rendered.
    shutil.copytree(candidate, layout / 'candidate')
    shutil.copytree(out / 'fixtures' / f'case-{number:02}', layout / 'input')
    shutil.copy2(out / 'fixtures/LICENSE', layout / 'input/LICENSE')
    prompt = f'''Use the review skill at {layout}/candidate/SKILL.md to review only the supplied base-to-head change in {layout}/input/change.diff. Complete base and head snapshots, callers, and target requirements are under {layout}/input/base and {layout}/input/head. Read the supplied target requirements and relevant candidate references. These snapshots are the full scope; no commit IDs are supplied. Report actionable findings first with priorities, precise locations, triggers, impact and evidence, then scope and verification limits. An empty findings list is valid. Review is advisory only. Do not edit inputs, access external services, delegate, or read sibling cases, grading material, prior reports, this preparation repository, or other installed skills. Read only the supplied input and candidate plus ordinary runtime/library files needed for understood checks. Run checks only in disposable copies under {scratch}; do not write into input or candidate. State which checks actually ran and any missing context.\n'''
    (evidence / 'prompt.md').write_text(prompt)
    argv = command + ['debug', 'prompt-input', prompt]
    result = subprocess.run(argv, cwd=scratch, env=environment, capture_output=True, text=True)
    (evidence / 'prompted-context.json').write_text(result.stdout)
    (evidence / 'prompted-stderr.txt').write_text(result.stderr)
    (evidence / 'prompted-command.json').write_text(json.dumps(
        {'argv': argv, 'cwd': str(scratch), 'environment': environment,
         'exit_code': result.returncode}, indent=2) + '\n')
    if result.returncode:
        raise SystemExit(f'Prompted render failed: case {number}')
    (evidence / 'proposed-launch.json').write_text(json.dumps({
        'argv': command + ['exec', '--skip-git-repo-check', '--json', '--color', 'never',
                           '--output-last-message', str(layout / 'final-report.txt'), '-'],
        'cwd': str(scratch), 'environment': environment, 'stdin': 'prompt.md',
        'status': 'Proposed only; not executed. Requires frozen-package approval and pre-launch revalidation.',
    }, indent=2) + '\n')
(preparation / 'runtime.json').write_text(json.dumps(metadata, indent=2) + '\n')
print('Prepared six standalone layouts and twelve non-inference context renders; no model reviews.')

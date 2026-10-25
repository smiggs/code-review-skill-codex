from pathlib import Path
import difflib
import json
import sys

out = Path('/home/andrew/projects/code-review-skill-codex/plans/evidence/05-behavioural-evaluation/batch-02/execution') / sys.argv[1]
meta = json.loads((out / 'metadata.json').read_text())
sessions = list((Path(meta['workspace']) / 'codex-home').rglob('rollout-*.jsonl'))
assert len(sessions) == 1, sessions
entries = [json.loads(line) for line in sessions[0].read_text().splitlines()]
actual = [x['payload'] for x in entries if x.get('type') == 'response_item'
          and x['payload'].get('role') in ('developer', 'user')]
expected = json.loads((out / 'review-context.json').read_text())
def core(item):
    return {k: v for k, v in item.items() if k not in ('id', 'internal_chat_message_metadata_passthrough')}
messages_match = [core(a) == core(b) for a, b in zip(actual, expected)]
text = '\n'.join(part.get('text', '') for item in actual for part in item.get('content', []))
world = [x['payload']['state'].get('agents_md') for x in entries if x.get('type') == 'world_state']
turns = [x['payload'] for x in entries if x.get('type') == 'turn_context']
audit = {'actual_context_items': len(actual), 'rendered_context_items': len(expected),
         'message_core_matches': messages_match, 'agents_md_states': world,
         'repository_guidance_absent': '# AGENTS.md instructions' not in text,
         'repository_path_absent': '/home/andrew/projects/code-review-skill-codex' not in text,
         'grader_material_absent': not any(s in text for s in ('answer-key.md', 'acceptance-criteria.md', 'scorecard.json')),
         'models': sorted({x.get('model', '') for x in turns}),
         'reasoning': sorted({x.get('effort', '') for x in turns}),
         'private_reasoning_and_account_metadata': 'Excluded from saved session extracts.'}
assert len(actual) == len(expected)
assert all(messages_match[1:]), audit
assert all(not x for x in world), audit
assert audit['repository_guidance_absent'] and audit['repository_path_absent'] and audit['grader_material_absent']
assert audit['models'] == ['gpt-6.1-sol'] and audit['reasoning'] == ['medium'], audit
for name, data in [('actual-initial-context.json', actual), ('actual-turn-context.json', turns),
                   ('context-audit.json', audit)]:
    (out / name).write_text(json.dumps(data, indent=2) + '\n')
keep = ('id', 'timestamp', 'cwd', 'cli_version', 'source', 'model_provider', 'base_instructions', 'context_window', 'history_mode')
session_meta = [{k: v for k, v in x['payload'].items() if k in keep}
                for x in entries if x.get('type') == 'session_meta']
(out / 'actual-session-metadata.json').write_text(json.dumps(session_meta, indent=2) + '\n')
if not messages_match[0]:
    a = actual[0]['tools'][0]['tools'][0]['description']
    b = expected[0]['tools'][0]['tools'][0]['description']
    delta = '\n'.join(difflib.unified_diff(b.splitlines(), a.splitlines(), fromfile='rendered', tofile='actual'))
    (out / 'tool-schema-difference.diff').write_text(delta + '\n')
events = [json.loads(line) for line in (out / 'events.jsonl').read_text().splitlines()]
completed = [x for x in events if x.get('type') == 'item.completed']
commands = [x for x in completed if x.get('item', {}).get('type') == 'command_execution']
tools = [x for x in completed if x.get('item', {}).get('type') not in ('agent_message', 'reasoning')]
(out / 'commands.jsonl').write_text(''.join(json.dumps(x) + '\n' for x in commands))
(out / 'tools.jsonl').write_text(''.join(json.dumps(x) + '\n' for x in tools))
print(json.dumps({'pair': out.name, 'commands': len(commands), 'context_ok': True,
                  'status': meta['status'], 'inputs_unchanged': meta.get('inputs_unchanged')}))

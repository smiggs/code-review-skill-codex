"""Extracts public context/settings/tool evidence, excluding private reasoning."""

from pathlib import Path
import difflib
import json
import sys

execution = Path(__file__).resolve().parent
case = f'case-{int(sys.argv[1]):02}'
record = execution / case
meta = json.loads((record / 'metadata.json').read_text())
sessions = list((Path(meta['workspace']) / 'codex-home').rglob('rollout-*.jsonl'))
assert len(sessions) == 1, sessions
entries = [json.loads(line) for line in sessions[0].read_text().splitlines()]
actual = [x['payload'] for x in entries if x.get('type') == 'response_item'
          and x['payload'].get('role') in ('developer', 'user')]
expected = json.loads((record / 'prompted-context.json').read_text())


def core(item):
    return {k: item[k] for k in ('type', 'role', 'content', 'tools') if k in item}


def write(name, value):
    (record / name).write_text(json.dumps(value, indent=2) + '\n')


actual = [core(item) for item in actual]
expected = [core(item) for item in expected]
messages_match = [a == b for a, b in zip(actual, expected)]
text = '\n'.join(part.get('text', '') for item in actual for part in item.get('content', []))
turn_fields = ('cwd', 'approval_policy', 'sandbox_policy', 'permission_profile',
               'file_system_sandbox_policy', 'model', 'effort', 'collaboration_mode')
turns = [{k: x['payload'][k] for k in turn_fields if k in x['payload']}
         for x in entries if x.get('type') == 'turn_context']
world = [x['payload'].get('state', {}).get('agents_md') for x in entries if x.get('type') == 'world_state']
audit = {'actual_context_items': len(actual), 'rendered_context_items': len(expected),
         'message_core_matches': messages_match, 'agents_md_states': world,
         'repository_guidance_absent': '# AGENTS.md instructions' not in text,
         'repository_path_absent': '/home/andrew/projects/code-review-skill-codex' not in text,
         'grader_material_absent': not any(s in text for s in ('answer-key.md', 'acceptance-criteria.md', 'scorecard.json')),
         'models': sorted({x.get('model', '') for x in turns}),
         'reasoning': sorted({x.get('effort', '') for x in turns}),
         'private_reasoning_and_account_metadata': 'Excluded from saved session extracts.'}
write('actual-initial-context.json', actual)
write('actual-turn-context.json', turns)
write('context-audit.json', audit)
keep = ('id', 'timestamp', 'cwd', 'cli_version', 'source', 'model_provider',
        'base_instructions', 'context_window', 'history_mode')
write('actual-session-metadata.json', [{k: v for k, v in x['payload'].items() if k in keep}
      for x in entries if x.get('type') == 'session_meta'])
if actual != expected:
    delta = '\n'.join(difflib.unified_diff(json.dumps(expected, indent=2).splitlines(),
                                         json.dumps(actual, indent=2).splitlines(),
                                         fromfile='rendered', tofile='actual'))
    (record / 'context-difference.diff').write_text(delta + '\n')
events = [json.loads(line) for line in (record / 'events.jsonl').read_text().splitlines()]
completed = [x for x in events if x.get('type') == 'item.completed']
commands = [x for x in completed if x.get('item', {}).get('type') == 'command_execution']
tools = [x for x in completed if x.get('item', {}).get('type') not in ('agent_message', 'reasoning')]
for name, data in [('commands.jsonl', commands), ('tools.jsonl', tools)]:
    (record / name).write_text(''.join(json.dumps(x) + '\n' for x in data))
public_tool_types = ('function_call', 'function_call_output', 'custom_tool_call', 'custom_tool_call_output', 'tool_call', 'tool_result')
(record / 'actual-tool-calls.jsonl').write_text(''.join(json.dumps(x['payload']) + '\n' for x in entries
    if x.get('type') == 'response_item' and x['payload'].get('type') in public_tool_types))
print(json.dumps(dict(audit, commands=len(commands), public_tool_items=len(tools))))
assert len(actual) == len(expected), 'Unexpected initial context length'
assert all(messages_match[1:]), 'Substantive live message change'
assert all(not state for state in world), 'Inherited project instructions'
assert audit['repository_guidance_absent'] and audit['repository_path_absent'] and audit['grader_material_absent']
assert audit['models'] == ['gpt-6.1-sol'] and audit['reasoning'] == ['medium'], 'Live settings differ'

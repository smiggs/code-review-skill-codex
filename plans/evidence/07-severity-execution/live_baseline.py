"""Compares only the context differences allowed by the continuation agreement."""

import json


def compare_contexts(baseline, actual, baseline_layout, actual_layout, expected_prompt):
    """Returns whether shared context and the exact approved user prompt agree."""
    expected_user = {'type': 'message', 'role': 'user', 'content': [
        {'type': 'input_text', 'text': expected_prompt}]}
    if not actual or actual[-1] != expected_user or len(actual) != len(baseline):
        return False
    baseline_text = json.dumps(baseline[:-1], sort_keys=True).replace(baseline_layout, 'LAYOUT')
    actual_text = json.dumps(actual[:-1], sort_keys=True).replace(actual_layout, 'LAYOUT')
    return baseline_text == actual_text

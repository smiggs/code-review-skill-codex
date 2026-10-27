"""Tests the agreed context comparison without launching a model."""

import copy
import unittest

from live_baseline import compare_contexts


class LiveBaselineComparison(unittest.TestCase):
    def setUp(self):
        self.baseline = [
            {'type': 'additional_tools', 'role': 'developer', 'tools': [{'name': 'shell'}]},
            {'type': 'message', 'role': 'developer', 'content': [
                {'type': 'input_text', 'text': 'Use /tmp/one/scratch; plugins: A'}]},
            {'type': 'message', 'role': 'user', 'content': [
                {'type': 'input_text', 'text': 'Review one'}]},
        ]
        self.actual = copy.deepcopy(self.baseline)
        self.actual[1]['content'][0]['text'] = 'Use /tmp/two/scratch; plugins: A'
        self.actual[-1]['content'][0]['text'] = 'Review two'

    def compare(self):
        return compare_contexts(self.baseline, self.actual, '/tmp/one', '/tmp/two', 'Review two')

    def test_only_layout_and_approved_final_prompt_can_differ(self):
        self.assertTrue(self.compare())

    def test_changed_plugin_guidance_is_rejected(self):
        self.actual[1]['content'][0]['text'] += '; plugins: B'
        self.assertFalse(self.compare())

    def test_changed_tool_schema_is_rejected(self):
        self.actual[0]['tools'].append({'name': 'external'})
        self.assertFalse(self.compare())

    def test_unapproved_final_prompt_is_rejected(self):
        self.actual[-1]['content'][0]['text'] = 'Different task'
        self.assertFalse(self.compare())

    def test_additional_initial_message_is_rejected(self):
        self.actual.insert(1, copy.deepcopy(self.actual[1]))
        self.assertFalse(self.compare())


if __name__ == '__main__':
    unittest.main(verbosity=2)

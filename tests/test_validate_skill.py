from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/validate-skill.py'


class StructureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'agents').mkdir()
        (self.root / 'reference').mkdir()
        (self.root / 'assets').mkdir()
        (self.root / 'scripts').mkdir()
        (self.root / 'SKILL.md').write_text('---\nname: code-review-codex\ndescription: |\n  Use when reviewing code.\n---\n[Guide](reference/guide.md)\n', encoding='utf-8')
        (self.root / 'agents/openai.yaml').write_text('interface:\n  display_name: Code Review Codex\n  short_description: Review code changes\n', encoding='utf-8')
        for name in ('README.md', 'README.zh-CN.md', 'CONTRIBUTING.md', 'CONTRIBUTING.zh-CN.md',
                     'LICENSE', 'scripts/pr-analyzer.py', 'reference/guide.md',
                     'assets/review-checklist.md', 'assets/pr-review-template.md', 'assets/review-report-template.md'):
            (self.root / name).write_text('', encoding='utf-8')

    def run_check(self):
        return subprocess.run([sys.executable, '-B', str(SCRIPT), str(self.root)],
                              cwd='/tmp', capture_output=True, text=True)

    def test_valid_package_from_other_directory(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_broken_relative_link(self):
        (self.root / 'reference/guide.md').write_text('[Missing](missing.md)', encoding='utf-8')
        self.assertNotEqual(self.run_check().returncode, 0)

    def test_missing_package_file(self):
        (self.root / 'LICENSE').unlink()
        self.assertNotEqual(self.run_check().returncode, 0)

    def test_yaml_types_name_and_duplicates(self):
        path = self.root / 'SKILL.md'
        for front in ('name: wrong\ndescription: Review code',
                      'name: code-review-codex\ndescription: []',
                      'name: code-review-codex\nname: other\ndescription: Review code',
                      'name: [broken'):
            path.write_text(f'---\n{front}\n---\n', encoding='utf-8')
            with self.subTest(front=front):
                self.assertNotEqual(self.run_check().returncode, 0)

    def test_metadata_empty_or_wrong_type(self):
        path = self.root / 'agents/openai.yaml'
        for value in ('interface: []', 'interface:\n  display_name: 9',
                      'interface:\n  display_name: Other Skill\n  short_description: Review'):
            path.write_text(value, encoding='utf-8')
            with self.subTest(value=value):
                self.assertNotEqual(self.run_check().returncode, 0)

    def test_reference_links_and_code_fences(self):
        (self.root / 'README.md').write_text('[guide][ref]\n\n[ref]: reference/missing.md\n', encoding='utf-8')
        self.assertNotEqual(self.run_check().returncode, 0)
        (self.root / 'README.md').write_text('```md\n[example](missing.md)\n```\nInline `def first[T](...)`\n', encoding='utf-8')
        self.assertEqual(self.run_check().returncode, 0)


if __name__ == '__main__':
    unittest.main()

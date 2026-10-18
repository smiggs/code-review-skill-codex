import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/pr-analyzer.py'
SPEC = importlib.util.spec_from_file_location('pr_analyzer', SCRIPT)
helper = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = helper
SPEC.loader.exec_module(helper)


def edit(path='a.py', body='-old\n+new\n', counts='1 +1'):
    return f'diff --git a/{path} b/{path}\n--- a/{path}\n+++ b/{path}\n@@ -{counts} @@\n{body}'


class DiffTests(unittest.TestCase):
    def test_normal_multiple_and_header_like_content(self):
        files = helper.parse_diff(edit() + edit('b.md', '---text\n+++text\n'))
        self.assertEqual([(f.filename, f.additions, f.deletions) for f in files],
                         [('a.py', 1, 1), ('b.md', 1, 1)])

    def test_empty(self):
        self.assertEqual(helper.parse_diff(''), [])

    def test_space_and_unicode_paths(self):
        files = helper.parse_diff(edit('dir/hello world.py') + edit('café.py'))
        self.assertEqual([f.filename for f in files], ['dir/hello world.py', 'café.py'])

    def test_git_quoted_utf8_and_control_characters(self):
        path = r'"a/caf\303\251\t\n.py"'
        other = r'"b/caf\303\251\t\n.py"'
        patch = f'diff --git {path} {other}\n--- {path}\n+++ {other}\n@@ -1 +1 @@\n-x\n+y\n'
        self.assertEqual(helper.parse_diff(patch)[0].filename, 'café\t\n.py')

    def test_rename_deletion_creation_binary_and_mode(self):
        patch = ('diff --git a/old.py b/new.py\nsimilarity index 100%\n'
                 'rename from old.py\nrename to new.py\n'
                 'diff --git a/gone b/gone\ndeleted file mode 100644\n'
                 '--- a/gone\n+++ /dev/null\n@@ -1 +0,0 @@\n-bye\n'
                 'diff --git a/new b/new\nnew file mode 100644\n'
                 '--- /dev/null\n+++ b/new\n@@ -0,0 +1 @@\n+hi\n'
                 'diff --git a/pic b/pic\nindex 123..456 100644\n'
                 'Binary files a/pic and b/pic differ\n'
                 'diff --git a/run b/run\nold mode 100644\nnew mode 100755\n')
        files = helper.parse_diff(patch)
        self.assertEqual([(f.filename, f.additions, f.deletions) for f in files],
                         [('new.py', 0, 0), ('gone', 0, 1), ('new', 1, 0),
                          ('pic', 0, 0), ('run', 0, 0)])
        self.assertTrue(files[3].binary)

    def test_no_newline_and_multiple_hunks(self):
        patch = edit(body='-old\n\\ No newline at end of file\n+new\n\\ No newline at end of file\n')
        patch += '@@ -8,0 +9,1 @@\n+last\n'
        self.assertEqual(helper.parse_diff(patch)[0].additions, 2)

    def test_rejects_partial_and_unsupported_input(self):
        cases = ['garbage\n', 'diff --git broken\n', 'diff --cc a.py\n',
                 edit() + 'garbage\n', edit(body='-old\n'),
                 edit() + '+extra\n', edit().replace('+++ b/a.py', '+++ b/wrong'),
                 'diff --git a/x b/x\n',
                 'diff --git a/x b/x\nGIT binary patch\nliteral 0\nHcmV?d00001\n',
                 edit().replace('@@ -1 +1 @@', '@@ invalid @@'),
                 edit().replace('--- a/a.py', '--- a/wrong')]
        for patch in cases:
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                helper.parse_diff(patch)

    def test_cli_is_read_only_deterministic_and_cwd_independent(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.diff'
            original = edit('notes.md')
            path.write_text(original, encoding='utf-8')
            command = [sys.executable, '-B', str(SCRIPT), '-f', str(path), '--json']
            first = subprocess.run(command, cwd=directory, capture_output=True, check=True)
            second = subprocess.run(command, cwd=directory, capture_output=True, check=True)
            self.assertEqual(first.stdout, second.stdout)
            report = json.loads(first.stdout)
            self.assertEqual(report['total_additions'], 1)
            self.assertEqual(report['total_files'], 1)
            self.assertEqual(set(report), {'total_files', 'total_additions', 'total_deletions', 'files'})
            self.assertEqual(path.read_text(encoding='utf-8'), original)
            self.assertEqual(list(Path(directory).iterdir()), [path])

    def test_real_git_diff_and_checkout_remain_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def git(*args):
                return subprocess.run(['git', *args], cwd=root, capture_output=True, check=True).stdout

            git('init', '-q')
            names = ['old.py', 'gone', 'picture', 'hello world.py', 'café.py', 'tab\tline\n.py']
            for name in names:
                (root / name).write_bytes(b'gone\n' if name == 'gone' else
                                         b'\x00before' if name == 'picture' else b'before\n')
            git('add', '.')
            git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                '-c', 'core.hooksPath=/dev/null', 'commit', '-qm', 'Fixture')
            (root / 'old.py').rename(root / 'renamed.py')
            (root / 'gone').unlink()
            (root / 'picture').write_bytes(b'\x00after')
            for name in names[3:]:
                (root / name).write_bytes(b'after\n')
            (root / 'empty').touch()
            git('add', '-A')
            patch = git('diff', '--cached', '--no-ext-diff', '--no-textconv',
                        '--src-prefix=a/', '--dst-prefix=b/').decode('utf-8')
            before = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            files = helper.parse_diff(patch)
            self.assertEqual({f.filename: (f.additions, f.deletions, f.binary) for f in files}, {
                'renamed.py': (0, 0, False), 'gone': (0, 1, False), 'picture': (0, 0, True),
                'hello world.py': (1, 1, False), 'café.py': (1, 1, False),
                'tab\tline\n.py': (1, 1, False), 'empty': (0, 0, False)})
            after = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            self.assertEqual(before, after)

    def test_cli_errors_have_no_partial_report(self):
        for data in [b'bad', edit().encode() + b'bad\n', b'\xff']:
            result = subprocess.run([sys.executable, '-B', str(SCRIPT)], input=data,
                                    capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, b'')
            self.assertTrue(result.stderr)

    def test_cli_empty_and_missing_file(self):
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), '--json'],
                                input=b'', capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)['total_files'], 0)
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), '-f', '/no/such/diff'],
                                capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, b'')


if __name__ == '__main__':
    unittest.main()

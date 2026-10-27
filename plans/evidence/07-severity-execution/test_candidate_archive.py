"""Tests lossless, bounded reading of the immutable candidate archive."""

import hashlib
import io
from pathlib import Path
import tarfile
import tempfile
import unittest

from verify_candidate_archive import read_candidate_archive


class CandidateArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.manifest = self.root / 'manifest.txt'
        self.manifest.write_text(hashlib.sha256(b'approved bytes\n').hexdigest()
                                 + '  candidate/SKILL.md\n')
        self.archive = self.root / 'candidate.tar.gz'

    def write_archive(self, entries):
        with tarfile.open(self.archive, 'w:gz') as archive:
            for name, content, kind in entries:
                member = tarfile.TarInfo(name)
                member.type = kind
                member.size = len(content) if kind == tarfile.REGTYPE else 0
                if kind == tarfile.SYMTYPE:
                    member.linkname = '/outside'
                archive.addfile(member, io.BytesIO(content) if member.isfile() else None)

    def test_original_bytes_are_recovered(self):
        self.write_archive([('candidate/SKILL.md', b'approved bytes\n', tarfile.REGTYPE)])
        self.assertEqual(read_candidate_archive(self.archive, self.manifest),
                         {'candidate/SKILL.md': b'approved bytes\n'})

    def test_changed_bytes_are_rejected(self):
        self.write_archive([('candidate/SKILL.md', b'changed bytes\n', tarfile.REGTYPE)])
        with self.assertRaises(ValueError):
            read_candidate_archive(self.archive, self.manifest)

    def test_missing_file_is_rejected(self):
        self.write_archive([])
        with self.assertRaises(ValueError):
            read_candidate_archive(self.archive, self.manifest)

    def test_unlisted_traversal_path_is_rejected(self):
        self.write_archive([('../outside', b'approved bytes\n', tarfile.REGTYPE)])
        with self.assertRaises(ValueError):
            read_candidate_archive(self.archive, self.manifest)

    def test_symlink_is_rejected(self):
        self.write_archive([('candidate/SKILL.md', b'', tarfile.SYMTYPE)])
        with self.assertRaises(ValueError):
            read_candidate_archive(self.archive, self.manifest)

    def test_duplicate_entry_is_rejected(self):
        entry = ('candidate/SKILL.md', b'approved bytes\n', tarfile.REGTYPE)
        self.write_archive([entry, entry])
        with self.assertRaises(ValueError):
            read_candidate_archive(self.archive, self.manifest)


if __name__ == '__main__':
    unittest.main(verbosity=2)

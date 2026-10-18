#!/usr/bin/env python3
"""Counts text changes in a strict subset of UTF-8 Git unified diffs."""

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import sys


@dataclass
class FileStats:
    """Stores counts for one file; binary counts exclude binary contents."""

    filename: str
    additions: int = 0
    deletions: int = 0
    binary: bool = False


def decode_path(value: str) -> str:
    """Decodes Git C-quoted UTF-8 paths, rejecting malformed escapes."""
    if not value.startswith('"'):
        if not value or any(ord(c) < 32 for c in value) or '"' in value:
            raise ValueError('invalid unquoted path')
        return value
    if not value.endswith('"'):
        raise ValueError('unterminated quoted path')
    data = bytearray()
    i = 1
    escapes = {'a': 7, 'b': 8, 't': 9, 'n': 10, 'v': 11, 'f': 12,
               'r': 13, '\\': 92, '"': 34}
    while i < len(value) - 1:
        char = value[i]
        if char == '"':
            raise ValueError('unexpected quote in path')
        if char != '\\':
            data.extend(char.encode('utf-8'))
            i += 1
            continue
        i += 1
        if i >= len(value) - 1:
            raise ValueError('incomplete path escape')
        if value[i] in escapes:
            data.append(escapes[value[i]])
            i += 1
        elif re.fullmatch(r'[0-3][0-7]{2}', value[i:i + 3]):
            data.append(int(value[i:i + 3], 8))
            i += 3
        else:
            raise ValueError('unsupported path escape')
    path = data.decode('utf-8', errors='strict')
    if not path or '\x00' in path:
        raise ValueError('empty or NUL path')
    return path


def header_paths(line: str) -> tuple[str, str]:
    """Returns prefixed header paths, rejecting ambiguous separators."""
    value = line.removeprefix('diff --git ')
    if value.startswith('"'):
        match = re.match(r'("(?:[^"\\]|\\.)*") (.+)$', value)
        if not match:
            raise ValueError('invalid quoted diff header')
        left, right = match.groups()
    else:
        separators = list(re.finditer(r' (?=b/|"b/)', value))
        if len(separators) != 1:
            raise ValueError('ambiguous or malformed diff header')
        split = separators[0].start()
        left, right = value[:split], value[split + 1:]
    old, new = decode_path(left), decode_path(right)
    if not old.startswith('a/') or not new.startswith('b/') or len(old) < 3 or len(new) < 3:
        raise ValueError('expected a/ and b/ path prefixes')
    return old, new


def parse_diff(diff_content: str) -> list[FileStats]:
    """Returns complete file counts or raises ValueError without partial results."""
    if not diff_content:
        return []
    lines = diff_content.split('\n')
    if lines[-1] == '':
        lines.pop()
    files = []
    i = 0
    while i < len(lines):
        if not lines[i].startswith('diff --git '):
            raise ValueError(f'line {i + 1}: expected diff --git header')
        old, new = header_paths(lines[i])
        stats = FileStats(new[2:])
        i += 1
        metadata = {}
        while i < len(lines) and not lines[i].startswith(('diff ', '--- ', 'Binary ', '@@')):
            line = lines[i]
            match = re.fullmatch(
                r'(old mode|new mode|new file mode|deleted file mode) ([0-7]{6})|'
                r'(index) ([0-9a-f]+\.\.[0-9a-f]+(?: [0-7]{6})?)|'
                r'(similarity index|dissimilarity index) (100%|[0-9]{1,2}%)|'
                r'(rename from|rename to|copy from|copy to) (.+)', line)
            if not match:
                raise ValueError(f'line {i + 1}: unsupported or malformed metadata')
            parts = [part for part in match.groups() if part is not None]
            key, value = parts
            if key in metadata:
                raise ValueError('duplicate metadata')
            metadata[key] = value
            i += 1
        moved = False
        for kind in ('rename', 'copy'):
            source, target = metadata.get(kind + ' from'), metadata.get(kind + ' to')
            if source is not None or target is not None:
                if source is None or target is None:
                    raise ValueError('incomplete rename/copy metadata')
                if decode_path(source) != old[2:] or decode_path(target) != new[2:]:
                    raise ValueError('rename/copy path mismatch')
                moved = True
        if old[2:] != new[2:] and not moved:
            raise ValueError('changed path requires rename/copy metadata')
        if ('old mode' in metadata) != ('new mode' in metadata):
            raise ValueError('incomplete mode change')
        created = 'new file mode' in metadata
        deleted = 'deleted file mode' in metadata
        if created and deleted:
            raise ValueError('conflicting creation/deletion metadata')
        has_content = False
        if i < len(lines) and lines[i].startswith('Binary files '):
            # Binary summaries carry no line counts and must stand alone.
            expected_old = '/dev/null' if created else old
            expected_new = '/dev/null' if deleted else new
            binary_match = re.fullmatch(r'Binary files (.+) and (.+) differ', lines[i])
            if not binary_match or tuple(map(decode_path, binary_match.groups())) != (expected_old, expected_new):
                raise ValueError('invalid or ambiguous binary summary')
            stats.binary = True
            has_content = True
            i += 1
        elif i < len(lines) and lines[i].startswith('--- '):
            before = decode_path(lines[i][4:].removesuffix('\t'))
            i += 1
            if i >= len(lines) or not lines[i].startswith('+++ '):
                raise ValueError('missing +++ file marker')
            after = decode_path(lines[i][4:].removesuffix('\t'))
            if (before, after) != ('/dev/null' if created else old,
                                   '/dev/null' if deleted else new):
                raise ValueError('file markers do not match diff header/modes')
            i += 1
            previous_old_end = previous_new_end = 0
            while i < len(lines) and lines[i].startswith('@@ '):
                hunk = re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(?: .*)?', lines[i])
                if not hunk:
                    raise ValueError(f'line {i + 1}: malformed hunk header')
                old_start, old_count, new_start, new_count = hunk.groups()
                old_start, new_start = int(old_start), int(new_start)
                remaining_old = int(old_count) if old_count is not None else 1
                remaining_new = int(new_count) if new_count is not None else 1
                if (old_start < previous_old_end or new_start < previous_new_end
                        or (remaining_old and not old_start) or (remaining_new and not new_start)
                        or not (remaining_old or remaining_new)):
                    raise ValueError('invalid or overlapping hunk range')
                previous_old_end = old_start + remaining_old
                previous_new_end = new_start + remaining_new
                if (created and remaining_old) or (deleted and remaining_new):
                    raise ValueError('hunk conflicts with creation/deletion')
                i += 1
                while remaining_old or remaining_new:
                    if i >= len(lines) or not lines[i] or lines[i][0] not in ' +-':
                        raise ValueError('truncated or malformed hunk')
                    prefix = lines[i][0]
                    remaining_old -= prefix in ' -'
                    remaining_new -= prefix in ' +'
                    if remaining_old < 0 or remaining_new < 0:
                        raise ValueError('hunk exceeds declared line counts')
                    stats.additions += prefix == '+'
                    stats.deletions += prefix == '-'
                    i += 1
                    if i < len(lines) and lines[i] == '\\ No newline at end of file':
                        i += 1
                has_content = True
            if not has_content:
                raise ValueError('file markers without hunks')
        if not has_content and not (moved or 'old mode' in metadata or created or deleted):
            raise ValueError('file section has no supported change')
        if i < len(lines) and not lines[i].startswith('diff --git '):
            raise ValueError(f'line {i + 1}: unexpected content after file section')
        files.append(stats)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description='Count diff files and text lines; no correctness judgements.')
    parser.add_argument('--diff-file', '-f', help='UTF-8 Git unified diff (default: stdin)')
    parser.add_argument('--stats', '-s', action='store_true', help='Show escaped file identities')
    parser.add_argument('--json', action='store_true', help='Emit deterministic JSON with file details')
    args = parser.parse_args()
    try:
        if args.diff_file:
            content = Path(args.diff_file).read_bytes().decode('utf-8', errors='strict')
        elif not sys.stdin.isatty():
            content = sys.stdin.buffer.read().decode('utf-8', errors='strict')
        else:
            parser.error('provide --diff-file or pipe a diff to stdin')
        files = parse_diff(content)
    except (OSError, ValueError) as error:
        print(f'pr-analyzer: {error}', file=sys.stderr)
        return 2
    report = {'total_files': len(files), 'total_additions': sum(f.additions for f in files),
              'total_deletions': sum(f.deletions for f in files),
              'files': [asdict(f) for f in files]}
    if args.json:
        print(json.dumps(report, ensure_ascii=True, sort_keys=True))
    else:
        print('Diff statistics (context only; binary contents excluded)')
        print(f"Files: {report['total_files']}  Additions: {report['total_additions']}  Deletions: {report['total_deletions']}")
        if args.stats:
            for file in files:
                print(f'{json.dumps(file.filename)} +{file.additions}/-{file.deletions}'
                      + (' [binary]' if file.binary else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())

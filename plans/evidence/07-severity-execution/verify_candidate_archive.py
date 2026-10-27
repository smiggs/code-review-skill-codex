"""Checks the archived candidate and original task 07 evidence manifests."""

import hashlib
from pathlib import Path
import tarfile
import tempfile


def read_candidate_archive(archive_path, manifest_path):
    """Returns approved file bytes, rejecting changed or unlisted archive members."""
    expected = {}
    for line in Path(manifest_path).read_text().splitlines():
        digest, name = line.split('  ', 1)
        parts = Path(name).parts
        if name in expected or not parts or parts[0] != 'candidate' or '..' in parts:
            raise ValueError(f'Invalid candidate manifest path: {name}')
        expected[name] = digest
    recovered = {}
    with tarfile.open(archive_path, 'r:gz') as archive:
        for member in archive:
            if not member.isfile() or member.name not in expected or member.name in recovered:
                raise ValueError(f'Unexpected candidate archive member: {member.name}')
            with archive.extractfile(member) as source:
                content = source.read()
            if hashlib.sha256(content).hexdigest() != expected[member.name]:
                raise ValueError(f'Candidate hash mismatch: {member.name}')
            recovered[member.name] = content
    if set(recovered) != set(expected):
        raise ValueError('Candidate archive is missing approved files')
    return recovered


def main():
    """Restores snapshot bytes in temporary storage and checks all original manifests."""
    execution = Path(__file__).resolve().parent
    diagnostic = execution.parent / '07-severity-diagnostic'
    recovered = read_candidate_archive(diagnostic / 'candidate.tar.gz',
                                       diagnostic / 'candidate-sha256sums.txt')
    manifests = [diagnostic / name for name in ('candidate-sha256sums.txt',
                 'inputs-sha256sums.txt', 'preparation-sha256sums.txt')]
    manifests += [execution / name for name in ('outputs-sha256sums.txt',
                  'continuation-sha256sums.txt', 'all-outputs-sha256sums.txt',
                  'disposition-sha256sums.txt')]
    with tempfile.TemporaryDirectory(prefix='task07-evidence-') as temporary:
        stage = Path(temporary)
        for name, content in recovered.items():
            target = stage / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        for manifest in manifests:
            for line in manifest.read_text().splitlines():
                expected, relative = line.split('  ', 1)
                archived = manifest.parent == diagnostic and relative.startswith('candidate/')
                path = stage / relative if archived else manifest.parent / relative
                if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    raise ValueError(f'Evidence hash mismatch: {manifest.name}: {relative}')
    print(f'Verified {len(recovered)} restored candidate files and {len(manifests)} original manifests.')


if __name__ == '__main__':
    main()

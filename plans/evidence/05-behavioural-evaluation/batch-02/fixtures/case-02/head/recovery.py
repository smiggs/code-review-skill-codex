from pathlib import Path


def recover(backup: Path, destination: Path):
    data = backup.read_bytes()
    backup.unlink()
    destination.write_bytes(data)

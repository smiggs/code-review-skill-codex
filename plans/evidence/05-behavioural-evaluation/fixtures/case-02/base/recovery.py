from pathlib import Path


def recover(backup: Path, destination: Path):
    data = backup.read_bytes()
    destination.write_bytes(data)
    backup.unlink()

"""Extracts the exact guide code bodies for compiler and runtime checks.

Records one identity per extracted fence. Generated sources land under
.generated/ and are never committed; recorded result files are refreshed
only when deliberately preparing evidence.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
GENERATED = HERE / ".generated"
GUIDE_SRC = GENERATED / "guide-src"


def slug(body: str) -> str:
    for line in body.splitlines():
        line = line.strip().lstrip("/").strip()
        if line and not line.startswith("#"):
            return re.sub(r"[^A-Za-z0-9]+", "-", line)[:60].strip("-").lower()
    return "empty"


identities = {}
if GUIDE_SRC.exists():
    shutil.rmtree(GUIDE_SRC)
GUIDE_SRC.mkdir(parents=True, exist_ok=True)
for language, fence, extension in (
    ("c", "c", "c"),
    ("cpp", "cpp", "cpp"),
    ("qt", "cpp", "cpp"),
):
    source = ROOT / "reference" / f"{language}.md"
    raw = source.read_bytes()
    bodies = re.findall(
        rf"^```{fence}\n(.*?)^```$", raw.decode(), re.M | re.S
    )
    if not bodies:
        raise ValueError(f"No {language} examples found in {source}")
    destination = GUIDE_SRC / language
    destination.mkdir(parents=True, exist_ok=True)
    records = []
    for index, body in enumerate(bodies):
        path = destination / f"{index:02d}-{slug(body)}.{extension}"
        path.write_text(body, encoding="utf-8")
        records.append(
            {
                "file": path.name,
                "sha256": hashlib.sha256(body.encode()).hexdigest(),
                "lines": len(body.splitlines()),
            }
        )
    identities[f"reference/{language}.md"] = {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "code_blocks": len(bodies),
        "blocks": records,
    }

results = GENERATED / "results"
results.mkdir(parents=True, exist_ok=True)
(results / "source-identities.json").write_text(
    json.dumps(identities, indent=2) + "\n", encoding="utf-8"
)
total = sum(v["code_blocks"] for v in identities.values())
print(f"Extracted {total} code blocks into {GUIDE_SRC.relative_to(ROOT)}")

"""Extracts the exact guide code bodies for compiler and runtime checks."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
identities = {}
for language, destination in (
    ("go", "go/examples.go"),
    ("rust", "rust/src/lib.rs"),
):
    source = ROOT / "reference" / f"{language}.md"
    raw = source.read_bytes()
    bodies = re.findall(rf"^```{language}\n(.*?)^```$", raw.decode(), re.M | re.S)
    if not bodies:
        raise ValueError(f"No {language} examples found")
    code = "\n".join(bodies)
    if language == "rust":
        code += '\n#[cfg(test)]\n#[path = "../tests.rs"]\nmod tests;\n'
    (HERE / destination).write_text(code)
    identities[str(source.relative_to(ROOT))] = {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "code_blocks": len(bodies),
        "extracted_sha256": hashlib.sha256(code.encode()).hexdigest(),
    }
results = HERE / ".generated/results"
results.mkdir(parents=True, exist_ok=True)
(results / "source-identities.json").write_text(
    json.dumps(identities, indent=2) + "\n"
)
print("Extracted all Go and Rust code blocks")

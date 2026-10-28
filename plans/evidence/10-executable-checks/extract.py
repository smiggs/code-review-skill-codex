"""Extract every Java guide code fence and compile it against declared JDK targets.

Each fence in ``reference/java.md`` must contain exactly one public top-level
type so it can be published as a standalone ``.java`` file. Fence bodies are
compiled, unmodified, with:

- JDK 21, ``--release 21``, no preview flags (the permanent-language baseline);
- JDK 21, ``--release 17``, no preview flags;
- JDK 17, ``--enable-preview --release 17`` (the declared 17 target with
  preview features enabled).

Every block must compile on target 21. A block failing the plain 17 target
must succeed with 17 preview flags; that pair distinguishes preview features
from permanent ones. Results and identities are written to
``.generated/results``. Generated source/class files land in
``.generated/guide-src`` and ``.generated/guide-classes`` and are ignored.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
GENERATED = HERE / ".generated"
RESULTS = GENERATED / "results"
PARSER = re.compile(r"^```java\n(.*?)^```$", re.M | re.S)
PUBLIC_TYPE = re.compile(r"^public\s+(?:\w+\s+)*?(class|record|interface|enum)\s+(\w+)", re.M)


def jdk_versions():
    return {
        "21": os.environ.get("JDK21_HOME"),
        "17": os.environ.get("JDK17_HOME"),
    }


def compile_one(javac, flags, source, classes):
    command = [
        javac, *flags, "-d", str(classes),
        "-Xlint:all,-options,-preview",
        str(source),
    ]
    result = subprocess.run(command, text=True, capture_output=True, timeout=60)
    return result


def main():
    jdirs = jdk_versions()
    missing = [name for name, path in jdirs.items() if not path or not (Path(path) / "bin/javac").exists()]
    if missing:
        raise SystemExit(f"Set JDK21_HOME and JDK17_HOME; missing: {missing}")
    jdk_ids = {}
    for label, home in jdirs.items():
        run = subprocess.run([home / "bin/java" if isinstance(home, Path) else f"{home}/bin/java", "-version"],
                             text=True, capture_output=True)
        jdk_ids[label] = (run.stderr + run.stdout).strip().splitlines()[0]
    source = ROOT / "reference" / "java.md"
    raw = source.read_bytes()
    bodies = PARSER.findall(raw.decode())
    if not bodies:
        raise ValueError("reference/java.md contains no ```java blocks")
    shutil.rmtree(GENERATED / "guide-src", ignore_errors=True)
    shutil.rmtree(GENERATED / "guide-classes", ignore_errors=True)
    src_dir = GENERATED / "guide-src"
    src_dir.mkdir(parents=True)
    identities = {}
    for index, body in enumerate(bodies, 1):
        matches = PUBLIC_TYPE.findall(body)
        if len(PUBLIC_TYPE.findall(body)) != 1:
            raise ValueError(
                f"Guide block {index} must contain exactly one public top-level type; found {matches}")
        kind, name = matches[0]
        path = src_dir / f"{name}.java"
        if path.exists():
            raise ValueError(f"Duplicate guide type name: {name}")
        path.write_text(body, encoding="utf-8")
        identities[name] = {
            "sha256": hashlib.sha256(body.encode()).hexdigest(),
        }
    targets = [
        ("release-21", jdirs["21"], ["--release", "21"]),
        ("release-17-plain", jdirs["21"], ["--release", "17"]),
        ("release-17-preview", jdirs["17"], ["--enable-preview", "--release", "17"]),
    ]
    matrix = {}
    for block_name, identity in identities.items():
        matrix[block_name] = {}
        for label, home, flags in targets:
            classes = GENERATED / "guide-classes" / label
            classes.mkdir(parents=True, exist_ok=True)
            result = compile_one(f"{home}/bin/javac", flags, src_dir / f"{block_name}.java", classes)
            matrix[block_name][label] = {
                "status": "compiled" if result.returncode == 0 else "rejected",
                "output": (result.stdout + result.stderr).strip() if result.returncode else "",
            }
    identity_of_source = hashlib.sha256(raw).hexdigest()
    RESULTS.mkdir(parents=True, exist_ok=True)
    record = {
        "guide": str(source.relative_to(ROOT)),
        "guide_sha256": identity_of_source,
        "blocks": len(bodies),
        "jdk_versions": jdk_ids,
        "block_sha256": identities,
        "compile_matrix": matrix,
    }
    (RESULTS / "source-identities.json").write_text(json.dumps(record, indent=2) + "\n")
    api_boundaries, failures = [], []
    for name, values in matrix.items():
        if values["release-21"]["status"] != "compiled":
            failures.append((name, "release-21", values["release-21"]["output"]))
            continue
        plain17 = values["release-17-plain"]
        if plain17["status"] == "compiled":
            continue
        if values["release-17-preview"]["status"] == "compiled":
            continue
        text = plain17["output"].lower()
        markers = (
            "preview" in text
            or "cannot find symbol" in text
            or "does not implement" in text
            or "not supported in -source" in text
        )
        if markers:
            api_boundaries.append(name)
        else:
            failures.append((name, "release-17", plain17["output"]))
    if failures:
        for name, label, output in failures:
            print(f"REJECTED {name} on {label}:\n{output}")
        raise SystemExit(
            "Guide blocks failed their declared compile targets; "
            "see .generated/results/source-identities.json"
        )
    print(f"Extracted and compiled {len(bodies)} guide blocks on all three targets")
    print("API/preview boundaries on target 17: " + (", ".join(sorted(api_boundaries)) or "none"))


if __name__ == "__main__":
    main()

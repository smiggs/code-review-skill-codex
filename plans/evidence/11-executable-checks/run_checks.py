"""Compiles and runs the package 11 executable checks.

Extracts guide fences (via extract.py), assembles the C/C++ units
translation units, compiles the declared-standards matrix, runs the
contract tests and fixture sensitivity checks, and (with --qt-prefix)
builds and runs the Qt event-loop adapters. Fresh outputs always land
under .generated/results/; recorded results/ and the candidate manifest
are refreshed only with --record.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
GEN = HERE / ".generated"
RESULTS = GEN / "results"
GUIDE_SRC = GEN / "guide-src"
BUILD = GEN / "build"
WORK = Path.home() / ".cache/cr-plan-11"
PREFIX = WORK / "prefix"
SYSROOT = PREFIX / "x86_64-conda-linux-gnu" / "sysroot"
CC = PREFIX / "bin" / "x86_64-conda-linux-gnu-gcc"
CXX = PREFIX / "bin" / "x86_64-conda-linux-gnu-g++"
SETARCH = ["setarch", platform.machine(), "-R"]
RUN_TIMEOUT = 90

# Fence classification per guide. Units are compiled and executed; the
# guides retain no illustrative-only fences in this revision.
C_UNITS = [0, 1, 2, 3]
C_FRAGMENTS = []
CPP_UNITS = list(range(10))
QT_FENCE_FILES = {0: "qt-parentowner.cpp", 1: "qt-context-lambda.cpp",
                  2: "qt-valueguard.cpp", 3: "qt-worker-shutdown.cpp"}

C_APPENDIX = """
/* Harness adjacency: expose a setter for the fence's static flag. */
#include <stdatomic.h>
void request_stop(void) { atomic_store(&stop, true); }
"""

RECORDS_CONTENT = (b"REC-0001" * 1 + b"REC-0002" + b"REC-0003" + b"REC-")


def sh(cmd, timeout=RUN_TIMEOUT, env=None, cwd=None):
    started = time.time()
    merged = dict(os.environ)
    lib = str(PREFIX / "lib")
    merged["LD_LIBRARY_PATH"] = lib + ":" + merged.get("LD_LIBRARY_PATH", "")
    if env:
        merged.update(env)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=timeout, env=merged,
                              cwd=str(cwd or HERE), check=False)
    except subprocess.TimeoutExpired:
        return 124, "", f"timeout after {timeout}s: {cmd}", time.time() - started
    except FileNotFoundError as exc:
        return 127, "", str(exc), time.time() - started
    return proc.returncode, proc.stdout, proc.stderr, time.time() - started


def log_line(name, rc, seconds, note=""):
    # Durations are deliberately not recorded: recorded outputs must be
    # byte-for-byte reproducible for the evidence-integrity regression.
    return f"{name}: rc={rc} {note}".rstrip()


def compile_cmd(driver, std, src, out, extra):
    # -Wno-ignored-attributes: the guide's unique_ptr<FILE, decltype(&fclose)>
    # idiom triggers GCC's attribute-ignoring note on the function pointer.
    base = [str(driver), f"-std={std}", "-Wall", "-Wextra", "-Werror",
            "-Wno-ignored-attributes", "-pthread",
            f"--sysroot={SYSROOT}", f"-B{PREFIX / 'bin'}", "-I", str(HERE / "tests")]
    return base + extra + ["-o", str(out), str(src)]


def fence_path(guide, index):
    matches = sorted((GUIDE_SRC / guide).glob(f"{index:02d}-*"))
    if len(matches) != 1:
        raise SystemExit(f"fence {guide}:{index} not found")
    return matches[0]


def assemble_units():
    c_ids = json.loads((RESULTS / "source-identities.json").read_text(encoding="utf-8"))
    counts = {k.split("/")[-1].removesuffix(".md"): v["code_blocks"]
              for k, v in c_ids.items()}
    expected = {"c": len(C_UNITS) + len(C_FRAGMENTS), "cpp": len(CPP_UNITS),
                "qt": len(QT_FENCE_FILES)}
    for guide, want in expected.items():
        if counts[guide] != want:
            raise SystemExit(
                f"guide {guide}.md now has {counts[guide]} fences; "
                f"harness expects {want}. Update the fence classification.")

    units_c = "\n".join(fence_path("c", i).read_text(encoding="utf-8") for i in C_UNITS)
    (BUILD / "units_c.c").write_text(units_c + C_APPENDIX, encoding="utf-8")
    units_cpp = "\n".join(fence_path("cpp", i).read_text(encoding="utf-8") for i in CPP_UNITS)
    (BUILD / "units_cpp.cpp").write_text(units_cpp, encoding="utf-8")


def live_fence_bodies(guide_key):
    """Parse the current guide fences in memory (same regex as extract.py)."""
    language = "cpp" if guide_key.startswith("reference/qt") else \
        guide_key.split("/")[-1].removesuffix(".md")
    raw = (ROOT / guide_key).read_text(encoding="utf-8")
    return re.findall(rf"^```{language}\n(.*?)^```$", raw, re.M | re.S)


def verify_identities():
    """Fail loudly on a stale or torn extraction cache.

    Compares (a) the generated fence files against the recorded
    identities, (b) the current guide fences against the generated cache,
    and (c) fence counts. Prose outside fences is not compared. With
    --record the caller re-runs extraction first so the identities are
    deliberately refreshed instead of failing here."""
    recorded = HERE / "results" / "source-identities.json"
    if not recorded.exists():
        return
    recorded_ids = json.loads(recorded.read_text(encoding="utf-8"))
    for guide_key, want in recorded_ids.items():
        guide_dir = GUIDE_SRC / guide_key.split("/")[-1].removesuffix(".md")
        if not GUIDE_SRC.exists():
            raise SystemExit(
                "no extracted fences; run extract.py (or drop --skip-build)")
        current = live_fence_bodies(guide_key)
        if len(current) != len(want["blocks"]):
            raise SystemExit(
                f"{guide_key} now has {len(current)} fences; the recorded "
                f"evidence covers {len(want['blocks'])}. Refresh with "
                "--record if deliberate.")
        for index, block in enumerate(want["blocks"]):
            path = guide_dir / block["file"]
            if not path.exists():
                raise SystemExit(
                    f"extracted fence missing: {path}. Run extract.py.")
            generated = hashlib.sha256(path.read_bytes()).hexdigest()
            if generated != block["sha256"]:
                raise SystemExit(
                    f"{guide_key} fence {block['file']} changed since the "
                    "recorded evidence. Refresh with --record if deliberate.")
            if hashlib.sha256(current[index].encode("utf-8")).hexdigest() \
                    != generated:
                raise SystemExit(
                    f"{guide_key} fence {index} differs from the current "
                    "guide; the extraction cache is stale. Run extract.py "
                    "(or refresh with --record if deliberate).")




def run_section_c(lines):
    prelude = HERE / "tests" / "c-units-prelude.h"
    variants = [
        ("c11-asan", "c11", ["-fsanitize=address,undefined",
                             "-fno-sanitize-recover=undefined",
                             "-fno-omit-frame-pointer", "-g"]),
        ("c11-o2", "c11", ["-O2"]),
        ("c11-tsan", "c11", ["-fsanitize=thread", "-g"]),
        ("c17-asan", "c17", ["-fsanitize=address,undefined",
                             "-fno-sanitize-recover=undefined",
                             "-fno-omit-frame-pointer", "-g"]),
    ]
    for name, std, extra in variants:
        out = BUILD / f"test_c_{name}"
        rc, out_txt, err, secs = sh(compile_cmd(CC, std, BUILD / "units_c.c",
                                                out, extra) +
                                    ["-include", str(prelude)] +
                                    [str(HERE / "tests" / "test_c.c")])
        if rc != 0:
            lines.append(log_line(f"build-c-{name}", rc, secs))
            lines.append(err)
            return False
        rc, out_txt, err, secs = sh(SETARCH + [str(out)])
        lines.append(log_line(f"run-c-{name}", rc, secs))
        lines.append(out_txt)
        if err.strip():
            lines.append("[stderr]\n" + err)
        if rc != 0 or "ALL-OK" not in out_txt:
            return False
    return True


def run_section_cpp(lines):
    prelude = HERE / "tests" / "cpp-prelude.hpp"
    # Units and tests share types, so they compile as one translation unit.
    combined = BUILD / "test_cpp_all.cpp"
    combined.write_text(
        (BUILD / "units_cpp.cpp").read_text(encoding="utf-8") + "\n" +
        (HERE / "tests" / "test_cpp.cpp").read_text(encoding="utf-8"),
        encoding="utf-8")
    variants = [
        ("cpp20-asan", "c++20", ["-fsanitize=address,undefined",
                                 "-fno-sanitize-recover=undefined",
                                 "-fno-omit-frame-pointer", "-g"]),
        ("cpp20-o2", "c++20", ["-O2"]),
        ("cpp20-tsan", "c++20", ["-fsanitize=thread", "-g"]),
        ("cpp17-asan", "c++17", ["-fsanitize=address,undefined",
                                 "-fno-sanitize-recover=undefined",
                                 "-fno-omit-frame-pointer", "-g"]),
        ("cpp17-o2", "c++17", ["-O2"]),
    ]
    ok = True
    for name, std, extra in variants:
        out = BUILD / f"test_cpp_{name}"
        rc, out_txt, err, secs = sh(compile_cmd(CXX, std, combined, out, extra) +
                                    ["-include", str(prelude)])
        if rc != 0:
            lines.append(log_line(f"build-cpp-{name}", rc, secs))
            lines.append(err)
            return False
        rc, out_txt, err, secs = sh(SETARCH + [str(out)])
        lines.append(log_line(f"run-cpp-{name}", rc, secs))
        lines.append(out_txt)
        if err.strip():
            lines.append("[stderr]\n" + err)
        if rc != 0 or "ALL-OK" not in out_txt:
            ok = False
    return ok


def run_section_fixtures(lines):
    ok = True
    records = BUILD / "records.bin"
    records.write_bytes(RECORDS_CONTENT)
    fixture_cases = [
        ("c-partial-io", "defect.c", "c11",
         {"expect_exit": 0, "expect_stdout": ["record 0: REC-0001",
                                              "record 3: "],
          "expect_lines": 4}),
        ("c-partial-io", "clean.c", "c11",
         {"expect_exit": 3, "expect_stdout": ["record 0: REC-0001",
                                              "record 2: REC-0003"],
          "expect_lines": 3,
          "expect_stderr": "truncated: 3 of 4 records"}),
        ("cpp-move-close", "defect.cpp", "c++20",
         {"expect_exit": 0, "expect_stdout": ["handle 100 closed 2 times",
                                              "closes=2"]}),
        ("cpp-move-close", "clean.cpp", "c++20",
         {"expect_exit": 0, "expect_stdout": ["handle 100 closed 1 times",
                                              "closes=1"]}),
    ]
    for folder, source, std, expect in fixture_cases:
        src = HERE / "fixtures" / folder / source
        out = BUILD / f"fixture-{folder}-{source.replace('.', '-')}"
        driver = CC if src.suffix == ".c" else CXX
        rc, out_txt, err, secs = sh(
            compile_cmd(driver, std, src, out, []))
        if rc != 0:
            lines.append(log_line(f"build-fixture-{folder}-{source}", rc, secs))
            lines.append(err)
            ok = False
            continue
        rc, out_txt, err, secs = sh(SETARCH + [str(out), str(records)])
        got_lines = [l for l in out_txt.splitlines() if l.strip()]
        checks = [rc == expect.get("expect_exit", 0)]
        for want in expect.get("expect_stdout", []):
            # An expectation ending with ": " is a deliberate prefix; the
            # rest must match a complete output line so "calls=1" cannot
            # satisfy "calls=10".
            if want.endswith(": "):
                checks.append(any(g.startswith(want) for g in got_lines))
            else:
                checks.append(want in got_lines)
        if "expect_lines" in expect:
            checks.append(len(got_lines) == expect["expect_lines"])
        if "expect_stderr" in expect:
            checks.append(expect["expect_stderr"] in err)
        verdict = "ok" if all(checks) else "FAIL"
        lines.append(log_line(f"fixture-{folder}-{source}", rc, secs, verdict))
        lines.append(out_txt)
        if not all(checks):
            ok = False
    return ok


def run_section_qt(lines, qt_prefix):
    qt = Path(qt_prefix)
    # Conda-style prefixes install headers under include/qt6; distro-style
    # ones use include/QtCore directly. Detect which layout exists.
    qt_inc = qt / "include" / "qt6"
    if not qt_inc.exists():
        qt_inc = qt / "include"
    moc_candidates = [qt / "lib" / "qt6" / "moc"] + \
        list((qt / "lib" / "qt6" / "libexec").glob("moc")) + \
        list((qt / "libexec").glob("moc")) + list((qt / "bin").glob("moc"))
    moc_candidates = [m for m in moc_candidates if m.exists()]
    if not moc_candidates:
        lines.append("qt: moc not found; Qt checks skipped and recorded")
        return False
    moc = moc_candidates[0]
    adapters = HERE / "adapters"
    includes = [f"-I{qt_inc}", f"-I{qt_inc}/QtCore",
                f"-I{qt_inc}/QtGui", f"-I{qt_inc}/QtWidgets",
                f"-I{qt_inc}/QtTest", f"-I{adapters}",
                "-fPIC", "-std=c++17"]
    env = dict(os.environ)
    env["LD_LIBRARY_PATH"] = (f"{qt}/lib:" + str(PREFIX / "lib") + ":"
                             + env.get("LD_LIBRARY_PATH", ""))
    ok = True

    def build_and_run(tag, adapter, extra_inc, libs,
                      platform_detection=False):
        src_text = adapter.read_text(encoding="utf-8")
        for fence, fname in QT_FENCE_FILES.items():
            if fname == adapter.name:
                body = fence_path("qt", fence).read_text(encoding="utf-8")
                marker = f"/* FENCE:{fence} */"
                if marker not in src_text:
                    raise SystemExit(f"{adapter.name} lost marker {marker}")
                src_text = src_text.replace(marker, body)
        gen_src = BUILD / adapter.name
        gen_src.write_text(src_text, encoding="utf-8")
        out = BUILD / f"qt-{tag}"
        cmd = [str(CXX), "-std=c++17", "-Wall", "-Wextra", "-pthread",
               f"--sysroot={SYSROOT}", f"-B{PREFIX / 'bin'}", "-fPIC"] + \
            includes + [f"-I{BUILD}", f"-L{qt}/lib", f"-L{PREFIX}/lib",
                        f"-Wl,-rpath-link,{qt}/lib", f"-Wl,-rpath-link,{PREFIX}/lib",
                        "-Wl,-rpath-link,/lib/x86_64-linux-gnu",
                        "-Wl,-rpath-link,/usr/lib/x86_64-linux-gnu"] + extra_inc + \
            ["-o", str(out), str(gen_src)]
        if tag in ("context-lambda", "worker-shutdown", "metacast"):
            cmd += [str(BUILD / "moc_qt-sender-worker.cpp")]
        if tag == "valueguard":
            cmd += [str(BUILD / "moc_qt-valueguard-classes.cpp")]
        # Libraries come after all source and object files so an
        # --as-needed linker keeps them for the symbols they satisfy.
        cmd += libs
        rc, out_txt, err, secs = sh(cmd)
        if rc != 0:
            lines.append(log_line(f"build-qt-{tag}", rc, secs))
            lines.append(err)
            return "fail"
        run_env = dict(env)
        if tag == "parentowner":
            run_env["QT_QPA_PLATFORM"] = "offscreen"
            run_env["QT_PLUGIN_PATH"] = f"{qt}/lib/qt6/plugins:{qt}/plugins"
        rc, out_txt, err, secs = sh(SETARCH + [str(out)], env=run_env)
        lines.append(log_line(f"run-qt-{tag}", rc, secs))
        lines.append(out_txt)
        if err.strip():
            lines.append("[stderr]\n" + err)
        if "could not load the Qt platform plugin" in err \
                or "no Qt platform plugin" in err:
            # A platform failure must never be read as a passing run, even
            # if the process still exits 0.
            return "unavailable"
        if rc == 0 and "ALL-OK" in out_txt:
            if tag == "parentowner":
                # ALL-OK counts only when the child-ownership checks ran.
                required = ["child exists with its parent",
                            "constructor records the parent owner",
                            "parent destruction deletes the child"]
                if not all(name in out_txt for name in required):
                    return "fail"
            return "ok"
        return "fail"

    core_libs = ["-lQt6Core"]
    widget_libs = ["-lQt6Core", "-lQt6Gui", "-lQt6Widgets"]
    # moc the shared headers first
    moc_includes = [i for i in includes if i.startswith("-I")]
    for header, mocname in (("qt-sender-worker.hpp", "moc_qt-sender-worker.cpp"),
                            ("qt-valueguard-classes.hpp",
                             "moc_qt-valueguard-classes.cpp")):
        rc, out_txt, err, secs = sh([str(moc), str(adapters / header),
                                     "-o", str(BUILD / mocname)] + moc_includes)
        lines.append(log_line(f"moc-{header}", rc, secs))
        if rc != 0:
            lines.append(err)
            return False

    ok &= build_and_run("context-lambda", adapters / "qt-context-lambda.cpp",
                        [], core_libs) == "ok"
    ok &= build_and_run("worker-shutdown", adapters / "qt-worker-shutdown.cpp",
                        [], core_libs) == "ok"
    ok &= build_and_run("valueguard", adapters / "qt-valueguard.cpp",
                        [], core_libs) == "ok"
    ok &= build_and_run("metacast", adapters / "qt-metacast.cpp",
                        [], core_libs) == "ok"
    widgets_status = build_and_run("parentowner", adapters / "qt-parentowner.cpp",
                                   [], widget_libs, platform_detection=True)
    if widgets_status == "unavailable":
        lines.append("qt-widgets-platform: unavailable (recorded limit)")
    else:
        lines.append("qt-widgets-platform: " + widgets_status)
        ok = ok and widgets_status == "ok"
    return ok


def run_section_qt_fixtures(lines, qt_prefix):
    qt = Path(qt_prefix)
    moc_candidates = [qt / "lib" / "qt6" / "moc"] + \
        list((qt / "lib" / "qt6" / "libexec").glob("moc")) + \
        list((qt / "libexec").glob("moc")) + list((qt / "bin").glob("moc"))
    moc_candidates = [m for m in moc_candidates if m.exists()]
    if not moc_candidates:
        lines.append("qt fixtures: skipped (no Qt)")
        return True
    moc = moc_candidates[0]
    fixture = HERE / "fixtures" / "qt-context-lambda"
    env = dict(os.environ)
    env["LD_LIBRARY_PATH"] = (f"{qt}/lib:" + str(PREFIX / "lib") + ":"
                             + env.get("LD_LIBRARY_PATH", ""))
    ok = True
    rc, _, err, secs = sh([str(moc), str(fixture / "classes.hpp"),
                           "-o", str(BUILD / "fixture-moc-classes.cpp"),
                           "-I", f"{qt}/include/qt6",
                           "-I", f"{qt}/include/qt6/QtCore"])
    if rc != 0:
        lines.append(log_line("moc-fixture-classes", rc, secs))
        lines.append(err)
        return False
    for name, want in (("defect.cpp", "ownerAlive=0 calls=2"),
                       ("clean.cpp", "ownerAlive=0 calls=1")):
        # Full-line membership, so "calls=1" cannot satisfy "calls=10".
        out = BUILD / f"qt-fixture-{name.replace('.', '-')}"
        cmd = [str(CXX), "-std=c++17", "-Wall", "-Wextra", "-pthread",
               f"--sysroot={SYSROOT}", f"-B{PREFIX / 'bin'}", "-fPIC",
               "-I", f"{qt}/include/qt6", "-I", f"{qt}/include/qt6/QtCore",
               "-I", str(fixture), "-L", f"{qt}/lib", "-L", f"{PREFIX}/lib",
               f"-Wl,-rpath-link,{qt}/lib", f"-Wl,-rpath-link,{PREFIX}/lib",
               "-o", str(out), str(fixture / name),
               str(BUILD / "fixture-moc-classes.cpp"), "-lQt6Core"]
        rc, out_txt, err, secs = sh(cmd)
        if rc != 0:
            lines.append(log_line(f"build-qt-fixture-{name}", rc, secs))
            lines.append(err)
            ok = False
            continue
        rc, out_txt, err, secs = sh(SETARCH + [str(out)], env=env)
        matched = any(g.strip() == want for g in out_txt.splitlines())
        verdict = "ok" if (rc == 0 and matched) else "FAIL"
        lines.append(log_line(f"run-qt-fixture-{name}", rc, secs, verdict))
        lines.append(out_txt)
        if not (rc == 0 and matched):
            ok = False
    return ok


MANIFEST_COVERAGE = [
    "reference/c.md", "reference/cpp.md", "reference/qt.md",
    "reference/common-bugs-checklist.md", "reference/reference-status.md",
    "reference/provenance.md", "reference/helper-tooling.md",
    "plans/11-c-cpp-and-qt.md", "plans/README.md",
]


def record_validation():
    """Regenerate the validation log so the manifest cannot bind a changed
    guide to a stale passing log. Returns the titles of failed required
    commands; the caller must not refresh the manifest while any remain."""
    commands = []
    def add(title, argv):
        commands.append((title, argv))
    add("Python and PyYAML", [sys.executable, "--version"])
    add("PyYAML", [sys.executable, "-c", "import yaml; print('PyYAML', yaml.__version__)"])
    add("git diff --check", ["git", "-C", str(ROOT), "diff", "--check"])
    add("git diff --stat", ["git", "-C", str(ROOT), "diff", "--stat"])
    add("helper and structural tests",
        [sys.executable, "-B", "-m", "unittest", "discover", "-s", str(ROOT / "tests")])
    # The validator resolves recorded-evidence link targets, so with
    # --record it validates a staged checkout whose results/ is overlaid
    # with the replacement evidence; publishing then cannot be blocked by
    # a pre-existing missing evidence directory.
    validator_arg = "."
    if (RESULTS / "run-checks.txt").exists():
        staged_root = RESULTS / "validate-staged"
        if staged_root.exists():
            shutil.rmtree(staged_root)
        shutil.copytree(ROOT, staged_root, ignore=shutil.ignore_patterns(
            ".git", ".generated"))
        results_target = staged_root / "plans" / "evidence" / \
            "11-executable-checks" / "results"
        results_target.mkdir(parents=True, exist_ok=True)
        overlay = {
            "run-checks.txt": RESULTS / "run-checks.txt",
            "source-identities.json": RESULTS / "source-identities.json",
        }
        overlay["validation.txt"] = (HERE / "results" / "validation.txt"
                                     if (HERE / "results" / "validation.txt").exists()
                                     else results_target / "validation.txt")
        if not overlay["validation.txt"].exists():
            overlay["validation.txt"] = None
        if overlay["validation.txt"] is None:
            (results_target / "validation.txt").write_text("", encoding="utf-8")
        else:
            shutil.copyfile(overlay["validation.txt"],
                            results_target / "validation.txt")
        (results_target / "candidate-manifest.json").write_text(
            "{}", encoding="utf-8")
        shutil.copyfile(RESULTS / "run-checks.txt",
                        results_target / "run-checks.txt")
        shutil.copyfile(RESULTS / "source-identities.json",
                        results_target / "source-identities.json")
        validator_root = staged_root
    else:
        validator_root = ROOT
    add("repository structural validator",
        [sys.executable, "-B", str(ROOT / "scripts" / "validate-skill.py"),
         str(validator_root)])
    quick = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / \
        "scripts" / "quick_validate.py"
    if quick.exists():
        add("skill-creator quick validator", [sys.executable, str(quick), "."])
    else:
        commands.append(("skill-creator quick validator", None))
    add("house-style lint (changed English documents)", "LINT")
    lines = []
    lines.append("# Package 11 validation log")
    lines.append(f"Date: {time.strftime('%Y-%m-%d')}")
    lint_files = ["reference/c.md", "reference/cpp.md", "reference/qt.md",
                  "plans/evidence/11-executable-checks/README.md",
                  "plans/evidence/11-executable-checks/fixtures/README.md",
                  "plans/11-c-cpp-and-qt.md",
                  "plans/evidence/11-c-cpp-and-qt.md"]
    failures = []
    for title, argv in commands:
        lines.append("")
        lines.append(f"## {title}")
        if argv == "LINT":
            lint = Path.home() / ".zcode" / "skills" / "british-house-style" / \
                "scripts" / "lint_house_style.py"
            if lint.exists():
                for rel in lint_files:
                    rc, out, err, _ = sh(
                        [sys.executable, str(lint), str(ROOT / rel)], cwd=ROOT)
                    verdict = (out or err).strip().splitlines()[-1]
                    lines.append(f"{rel}: {verdict}")
                    # The linter returns nonzero for lint errors or
                    # internal failure; either must block the record.
                    if rc != 0 or "0 error(s)" not in verdict:
                        failures.append(f"house-style lint: {rel}")
            else:
                lines.append("house-style lint script unavailable in this "
                             "environment; not recorded")
            continue
        if argv is None:
            lines.append("not available in this environment; not recorded")
            continue
        rc, out, err, _ = sh(argv, cwd=ROOT)
        detail = (out or err).strip()
        lines.append(detail if detail else "(no output)")
        if title == "git diff --check" and rc == 0 and not detail:
            lines.append("clean")
        if rc != 0:
            lines.append(f"[exit {rc}]")
            failures.append(title)
    lines.append("")
    lines.append("Run by the --record flow in run_checks.py so the recorded log "
                 "always describes the candidate being hashed; the manifest "
                 "digest lives in results/candidate-manifest.json.")
    lines.append("")
    lines.append("FAILED REQUIRED CHECKS: " +
                 (", ".join(failures) if failures else "none"))
    fresh = RESULTS / "validation-fresh.txt"
    fresh.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return failures, fresh


def candidate_manifest():
    files = []
    for rel in MANIFEST_COVERAGE:
        path = ROOT / rel
        if path.exists():
            files.append(rel)
    for path in sorted(HERE.rglob("*")):
        if path.is_file() and ".generated" not in path.parts \
                and "__pycache__" not in path.parts \
                and path.name != "candidate-manifest.json" \
                and not path.name.startswith(".generated-load-"):
            files.append(str(path.relative_to(ROOT)))
    digest = hashlib.sha256()
    entries = {}
    for rel in sorted(set(files)):
        data = (ROOT / rel).read_bytes()
        file_digest = hashlib.sha256(data).hexdigest()
        entries[rel] = file_digest
        digest.update(rel.encode("utf-8") + b"\x00" +
                      file_digest.encode("ascii") + b"\x00")
    return {"combined_sha256": digest.hexdigest(), "files": entries}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", action="store_true",
                        help="copy fresh outputs into results/ and refresh "
                             "the candidate manifest")
    parser.add_argument("--qt-prefix", default=None,
                        help="prefix of an extracted Qt build for the "
                             "event-loop adapters")
    parser.add_argument("--skip-build", action="store_true")
    args = parser.parse_args()

    if args.record and args.skip_build:
        sys.exit("--record must re-extract; drop --skip-build")
    if not args.skip_build:
        rc, out, err, _ = sh([sys.executable, str(HERE / "extract.py")])
        if rc != 0:
            print(err)
            sys.exit(1)
        print(out.strip())
    BUILD.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    if not args.record:
        verify_identities()
    # Reassemble unconditionally: even under --skip-build the compiled
    # units must come from the verified fences, not from stale build files.
    assemble_units()

    lines = []
    versions = []
    for tag, cmd in (("cc", [str(CC), "--version"]), ("cxx", [str(CXX), "--version"])):
        rc, out, _, _ = sh(cmd)
        versions.append(f"{tag}: {out.splitlines()[0] if out else 'missing'}")
    lines.extend(versions)
    lines.append(f"platform: {platform.platform()}")

    ok = True
    ok &= run_section_c(lines)
    ok &= run_section_cpp(lines)
    ok &= run_section_fixtures(lines)
    if args.qt_prefix:
        ok &= run_section_qt(lines, args.qt_prefix)
        ok &= run_section_qt_fixtures(lines, args.qt_prefix)
    else:
        lines.append("qt: not requested; adapters and Qt fixtures not run")

    summary = "PACKAGE-11-CHECKS: " + ("ALL-OK" if ok else "FAILURES")
    lines.append(summary)

    fresh = RESULTS / "run-checks.txt"
    fresh.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[-6:]))
    if args.record:
        validation_failures, staged_log = record_validation()
        if validation_failures:
            print("RECORD ABORTED: failed required validation: "
                  + ", ".join(validation_failures)
                  + f"; the staged log is at {staged_log}")
            sys.exit(1)
        if not ok:
            print("RECORD ABORTED: executable checks failed; recorded "
                  "results, validation log, and manifest are unchanged")
            sys.exit(1)
        # Stage the complete publication set under .generated/, then copy
        # it into results/ with the manifest LAST: the manifest is the
        # commit point, so an interruption during publication leaves a
        # manifest digest that no longer matches the copied files, which
        # the evidence-integrity regression detects; re-running --record
        # finishes the set.
        publish = RESULTS / "publish"
        if publish.exists():
            shutil.rmtree(publish)
        publish.mkdir(parents=True)
        shutil.copyfile(staged_log, publish / "validation.txt")
        shutil.copyfile(fresh, publish / "run-checks.txt")
        shutil.copyfile(RESULTS / "source-identities.json",
                        publish / "source-identities.json")
        recorded = HERE / "results"
        recorded.mkdir(parents=True, exist_ok=True)
        for name in ("validation.txt", "run-checks.txt",
                     "source-identities.json"):
            shutil.copyfile(publish / name, recorded / name)
        (recorded / "candidate-manifest.json").write_text(
            json.dumps(candidate_manifest(), indent=2) + "\n",
            encoding="utf-8")
        shutil.rmtree(publish)
        print("recorded to results/ and refreshed candidate manifest")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

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


def sh(cmd, timeout=RUN_TIMEOUT, env=None):
    started = time.time()
    merged = dict(os.environ)
    lib = str(PREFIX / "lib")
    merged["LD_LIBRARY_PATH"] = lib + ":" + merged.get("LD_LIBRARY_PATH", "")
    if env:
        merged.update(env)
    proc = subprocess.run(cmd, capture_output=True, text=True,
                          timeout=timeout, env=merged, cwd=str(HERE))
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
    c_ids = json.loads((RESULTS / "source-identities.json").read_text())
    counts = {k.split("/")[-1].removesuffix(".md"): v["code_blocks"]
              for k, v in c_ids.items()}
    expected = {"c": len(C_UNITS) + len(C_FRAGMENTS), "cpp": len(CPP_UNITS),
                "qt": len(QT_FENCE_FILES)}
    for guide, want in expected.items():
        if counts[guide] != want:
            raise SystemExit(
                f"guide {guide}.md now has {counts[guide]} fences; "
                f"harness expects {want}. Update the fence classification.")

    units_c = "\n".join(fence_path("c", i).read_text() for i in C_UNITS)
    (BUILD / "units_c.c").write_text(units_c + C_APPENDIX)
    units_cpp = "\n".join(fence_path("cpp", i).read_text() for i in CPP_UNITS)
    (BUILD / "units_cpp.cpp").write_text(units_cpp)


def run_section_c(lines):
    prelude = HERE / "tests" / "c-units-prelude.h"
    variants = [
        ("c11-asan", "c11", ["-fsanitize=address,undefined",
                             "-fno-omit-frame-pointer", "-g"]),
        ("c11-o2", "c11", ["-O2"]),
        ("c11-tsan", "c11", ["-fsanitize=thread", "-g"]),
        ("c17-asan", "c17", ["-fsanitize=address,undefined",
                             "-fno-omit-frame-pointer", "-g"]),
    ]
    for name, std, extra in variants:
        out = BUILD / f"test_c_{name}"
        rc, out_txt, err, secs = sh(compile_cmd(CC, std, BUILD / "units_c.c",
                                                out, []) +
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
    combined.write_text((BUILD / "units_cpp.cpp").read_text() + "\n" +
                        (HERE / "tests" / "test_cpp.cpp").read_text())
    variants = [
        ("cpp20-asan", "c++20", ["-fsanitize=address,undefined",
                                 "-fno-omit-frame-pointer", "-g"]),
        ("cpp20-o2", "c++20", ["-O2"]),
        ("cpp20-tsan", "c++20", ["-fsanitize=thread", "-g"]),
        ("cpp17-asan", "c++17", ["-fsanitize=address,undefined",
                                 "-fno-omit-frame-pointer", "-g"]),
        ("cpp17-o2", "c++17", ["-O2"]),
    ]
    ok = True
    for name, std, extra in variants:
        out = BUILD / f"test_cpp_{name}"
        rc, out_txt, err, secs = sh(compile_cmd(CXX, std, combined, out, []) +
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
         {"expect_exit": 0, "expect_stdout": ["closed 2 times", "closes=2"]}),
        ("cpp-move-close", "clean.cpp", "c++20",
         {"expect_exit": 0, "expect_stdout": ["closed 1 times", "closes=1"]}),
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
            checks.append(want in out_txt)
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
    moc_candidates = [qt / "lib" / "qt6" / "moc"] + \
        list((qt / "lib" / "qt6" / "libexec").glob("moc")) + \
        list((qt / "libexec").glob("moc")) + list((qt / "bin").glob("moc"))
    moc_candidates = [m for m in moc_candidates if m.exists()]
    if not moc_candidates:
        lines.append("qt: moc not found; Qt checks skipped and recorded")
        return False
    moc = moc_candidates[0]
    adapters = HERE / "adapters"
    includes = [f"-I{qt}/include/qt6", f"-I{qt}/include/qt6/QtCore",
                f"-I{qt}/include/qt6/QtGui", f"-I{qt}/include/qt6/QtWidgets",
                f"-I{qt}/include/qt6/QtTest", f"-I{adapters}",
                "-fPIC", "-std=c++17"]
    env = dict(os.environ)
    env["LD_LIBRARY_PATH"] = f"{qt}/lib:" + env.get("LD_LIBRARY_PATH", "")
    ok = True

    def build_and_run(tag, adapter, extra_inc, libs):
        src_text = adapter.read_text()
        for fence, fname in QT_FENCE_FILES.items():
            if fname == adapter.name:
                body = fence_path("qt", fence).read_text()
                marker = f"/* FENCE:{fence} */"
                if marker not in src_text:
                    raise SystemExit(f"{adapter.name} lost marker {marker}")
                src_text = src_text.replace(marker, body)
        gen_src = BUILD / adapter.name
        gen_src.write_text(src_text)
        out = BUILD / f"qt-{tag}"
        cmd = [str(CXX), "-std=c++17", "-Wall", "-Wextra", "-pthread",
               f"--sysroot={SYSROOT}", f"-B{PREFIX / 'bin'}", "-fPIC"] + \
            includes + [f"-I{BUILD}", f"-L{qt}/lib", f"-L{PREFIX}/lib",
                        f"-Wl,-rpath-link,{qt}/lib", f"-Wl,-rpath-link,{PREFIX}/lib",
                        "-Wl,-rpath-link,/lib/x86_64-linux-gnu",
                        "-Wl,-rpath-link,/usr/lib/x86_64-linux-gnu"] + extra_inc + libs + \
            ["-o", str(out), str(gen_src)]
        if tag in ("context-lambda", "worker-shutdown", "metacast"):
            cmd += [str(BUILD / "moc_qt-sender-worker.cpp")]
        if tag == "valueguard":
            cmd += [str(BUILD / "moc_qt-valueguard-classes.cpp")]
        rc, out_txt, err, secs = sh(cmd)
        if rc != 0:
            lines.append(log_line(f"build-qt-{tag}", rc, secs))
            lines.append(err)
            return False
        run_env = dict(env)
        if tag == "parentowner":
            run_env["QT_QPA_PLATFORM"] = "offscreen"
            run_env["QT_PLUGIN_PATH"] = f"{qt}/lib/qt6/plugins:{qt}/plugins"
        rc, out_txt, err, secs = sh(SETARCH + [str(out)], env=run_env)
        lines.append(log_line(f"run-qt-{tag}", rc, secs))
        lines.append(out_txt)
        if err.strip():
            lines.append("[stderr]\n" + err)
        return rc == 0 and "ALL-OK" in out_txt

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
                        [], core_libs)
    ok &= build_and_run("worker-shutdown", adapters / "qt-worker-shutdown.cpp",
                        [], core_libs)
    ok &= build_and_run("valueguard", adapters / "qt-valueguard.cpp",
                        [], core_libs)
    ok &= build_and_run("metacast", adapters / "qt-metacast.cpp",
                        [], core_libs)
    widgets_ok = build_and_run("parentowner", adapters / "qt-parentowner.cpp",
                               [], widget_libs)
    lines.append("qt-widgets-platform: " + ("ok" if widgets_ok else
                                            "unavailable/failed (recorded limit)"))
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
    env["LD_LIBRARY_PATH"] = f"{qt}/lib:" + env.get("LD_LIBRARY_PATH", "")
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
        out = BUILD / f"qt-fixture-{name.replace('.', '-')}"
        cmd = [str(CXX), "-std=c++17", "-Wall", "-Wextra", "-pthread",
               f"--sysroot={SYSROOT}", f"-B{PREFIX / 'bin'}", "-fPIC",
               "-I", f"{qt}/include/qt6", "-I", f"{qt}/include/qt6/QtCore",
               "-I", str(fixture), "-L", f"{qt}/lib", "-L", f"{PREFIX}/lib",
               f"-Wl,-rpath-link,{qt}/lib", f"-Wl,-rpath-link,{PREFIX}/lib",
               "-lQt6Core",
               "-o", str(out), str(fixture / name),
               str(BUILD / "fixture-moc-classes.cpp")]
        rc, out_txt, err, secs = sh(cmd)
        if rc != 0:
            lines.append(log_line(f"build-qt-fixture-{name}", rc, secs))
            lines.append(err)
            ok = False
            continue
        rc, out_txt, err, secs = sh(SETARCH + [str(out)], env=env)
        verdict = "ok" if (rc == 0 and want in out_txt) else "FAIL"
        lines.append(log_line(f"run-qt-fixture-{name}", rc, secs, verdict))
        lines.append(out_txt)
        if not (rc == 0 and want in out_txt):
            ok = False
    return ok


MANIFEST_COVERAGE = [
    "reference/c.md", "reference/cpp.md", "reference/qt.md",
    "reference/common-bugs-checklist.md", "reference/reference-status.md",
    "reference/provenance.md", "reference/helper-tooling.md",
    "plans/11-c-cpp-and-qt.md", "plans/README.md",
]


def candidate_manifest():
    files = []
    for rel in MANIFEST_COVERAGE:
        path = ROOT / rel
        if path.exists():
            files.append(rel)
    for path in sorted(HERE.rglob("*")):
        if path.is_file() and ".generated" not in path.parts:
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

    if not args.skip_build:
        rc, out, err, _ = sh([sys.executable, str(HERE / "extract.py")])
        if rc != 0:
            print(err)
            sys.exit(1)
        print(out.strip())
    BUILD.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
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
    fresh.write_text("\n".join(lines) + "\n")
    print("\n".join(lines[-6:]))
    if args.record:
        recorded = HERE / "results"
        recorded.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(fresh, recorded / "run-checks.txt")
        shutil.copyfile(RESULTS / "source-identities.json",
                        recorded / "source-identities.json")
        (recorded / "candidate-manifest.json").write_text(
            json.dumps(candidate_manifest(), indent=2) + "\n")
        print("recorded to results/ and refreshed candidate manifest")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

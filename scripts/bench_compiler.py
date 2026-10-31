#!/usr/bin/env python3
"""Compare a frozen source bench across pinned PSP compiler configurations.

Each configuration compiles every probe together into a fresh object. Only
relocation-free function bytes are compared here. Exact probe sequences never
count as source matches, a full build, or proof of the historical compiler.
"""

import argparse
from functools import lru_cache
import hashlib
import json
import math
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile

try:
    from .elf32 import Elf32
    from .prepare_reference import check_identity, file_identity, reject_link, write_report
except ImportError:
    from elf32 import Elf32
    from prepare_reference import check_identity, file_identity, reject_link, write_report


ROOT = Path(__file__).resolve().parents[1]


def sha256(data):
    """Identify source, metadata or object bytes without embedding game bytes."""
    return hashlib.sha256(data).hexdigest()


def validate_probes(reference, manifest):
    """Check target identities and nonoverlapping executable-code boundaries."""
    if reference.file_type != 2:
        raise ValueError("Reference is not an ELF executable")
    probes = manifest.get("probes", [])
    if not probes:
        raise ValueError("Probe manifest is empty")
    names, intervals = set(), []
    for probe in probes:
        name, address, size = probe["name"], probe["address"], probe["size"]
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", name) or name in names:
            raise ValueError("Duplicate or invalid probe name")
        if (not isinstance(address, int) or not isinstance(size, int)
                or address < 0 or size <= 0 or address % 4 or size % 4
                or address + size > 0x100000000):
            raise ValueError("Invalid probe address/size")
        if probe.get("relocations", []) != []:
            raise ValueError("This bench does not support probe relocations")
        targets = [s for s in reference.sections if s["flags"] & 6 == 6
                   and s["type"] == 1 and s["address"] <= address
                   and address + size <= s["address"] + s["size"]]
        if len(targets) != 1:
            raise ValueError("Probe is not inside one allocated executable section")
        if sha256(reference.virtual_bytes(address, size)) != probe["target_sha256"]:
            raise ValueError("Probe target hash mismatch: " + name)
        names.add(name)
        intervals.append((address, address + size))
    intervals.sort()
    if any(right[0] < left[1] for left, right in zip(intervals, intervals[1:])):
        raise ValueError("Probe target intervals overlap")
    return probes


def compare_object(object_bytes, reference, manifest):
    """Compare real function symbols, rejecting unresolved code relocations.

    Section indices are essential: these objects commonly repeat .text names.
    No relocation patching, padding trimming or function slicing is performed.
    """
    probes = validate_probes(reference, manifest)
    obj = Elf32(object_bytes)
    if obj.file_type != 1:
        raise ValueError("Compiler output is not a relocatable ELF object")
    functions = list(obj.functions())
    names = [fn["name"] for fn in functions]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate function symbol names in compiler object")
    if set(names) != {p["name"] for p in probes}:
        raise ValueError("Compiler object has missing or unexpected probe functions")
    intervals = {}
    for fn in functions:
        section = obj.sections[fn["section_index"]]
        if (section["type"] != 1 or section["flags"] & 6 != 6
                or fn["size"] <= 0 or fn["size"] % 4 or fn["section_offset"] % 4):
            raise ValueError("Probe symbol does not describe complete executable words")
        intervals.setdefault(fn["section_index"], []).append(
            (fn["section_offset"], fn["section_offset"] + fn["size"]))
    for spans in intervals.values():
        spans.sort()
        if any(right[0] < left[1] for left, right in zip(spans, spans[1:])):
            raise ValueError("Compiler function symbols overlap")
    for section in obj.sections:
        if section["type"] not in (4, 9):
            continue
        entry_size = 12 if section["type"] == 4 else 8
        if (section["entry_size"] != entry_size or section["size"] % entry_size
                or not 0 < section["info"] < len(obj.sections)
                or not 0 < section["link"] < len(obj.sections)):
            raise ValueError("Invalid ELF relocation section")
        symbols = obj.sections[section["link"]]
        if symbols["type"] != 2 or symbols["entry_size"] != 16 or symbols["size"] % 16:
            raise ValueError("Invalid relocation symbol table")
        target = obj.sections[section["info"]]
        seen_offsets = set()
        records = obj.section_data(section)
        for offset in range(0, len(records), entry_size):
            place, info = struct.unpack_from("<II", records, offset)
            if (place % 4 or place + 4 > target["size"] or place in seen_offsets
                    or info >> 8 >= symbols["size"] // 16):
                raise ValueError("Invalid relocation offset/symbol")
            seen_offsets.add(place)
        if section["size"] and section["info"] in intervals:
            raise ValueError("Unresolved relocation in probe code")
    by_name = {fn["name"]: fn for fn in functions}
    comparisons = []
    for probe in probes:
        fn = by_name[probe["name"]]
        target = reference.virtual_bytes(probe["address"], probe["size"])
        actual = fn["bytes"]
        first = next((i for i, (a, b) in enumerate(zip(actual, target)) if a != b), None)
        if first is None and len(actual) != len(target):
            first = min(len(actual), len(target))
        comparisons.append({"name": probe["name"], "address": probe["address"],
                            "target_size": len(target), "compiled_size": len(actual),
                            "target_sha256": sha256(target), "compiled_sha256": sha256(actual),
                            "exact_probe_bytes": actual == target, "first_difference": first})
    comments = []
    for section in obj.sections:
        if section["name"] == ".comment":
            comments.extend(s.decode("ascii", errors="backslashreplace")
                            for s in obj.section_data(section).split(b"\0") if s)
    return {"object_sha256": sha256(object_bytes), "elf_flags": obj.flags,
            "compiler_comments": comments, "comparisons": comparisons}


@lru_cache(maxsize=8)
def runtime_root(root, distro):
    """Resolve the project into WSL once, without invoking a shell."""
    result = subprocess.run(["wsl", "-d", distro, "--", "wslpath", "-a", root.as_posix()],
                            stdin=subprocess.DEVNULL, capture_output=True, text=True,
                            check=True, timeout=10)
    path = result.stdout.strip()
    if not path:
        raise ValueError("WSL path conversion returned an empty path")
    return path


def compile_probe(compiler, runner, source, output, flags, *, timeout, root, distro):
    """Invoke the compatibility runner with empty stdin and a bounded lifetime."""
    if os.name == "nt":
        base = runtime_root(root, distro)
        prefix = ["wsl", "-d", distro, "--"]
        def converted(path):
            return base + "/" + path.relative_to(root).as_posix()
    else:
        prefix = []
        def converted(path):
            return str(path)
    command = prefix + ["timeout", str(timeout) + "s", converted(runner), converted(compiler),
                        *flags, "-o", converted(output), converted(source)]
    result = subprocess.run(command, stdin=subprocess.DEVNULL, capture_output=True,
                            text=True, timeout=timeout + 5, cwd=root)
    return {"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


def run_bench(*, root=ROOT, candidates_path=None, manifest_path=None, lock_path=None,
              report_path=None, build_parent=None, timeout=20):
    """Run the entire declared matrix or fail without publishing a score report."""
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("Compiler timeout must be finite and positive")
    root = Path(root).resolve(strict=True)
    candidates_path = Path(candidates_path) if candidates_path else root / "config/compiler-candidates.json"
    manifest_path = Path(manifest_path) if manifest_path else root / "config/compiler-probes.json"
    lock_path = Path(lock_path) if lock_path else root / "config/reference.json"
    raw_config, raw_manifest, raw_lock = (p.read_bytes() for p in (candidates_path, manifest_path, lock_path))
    config, manifest, lock = (json.loads(b) for b in (raw_config, raw_manifest, raw_lock))
    if config.get("status") != "investigation_only_not_locked":
        raise ValueError("Expected an investigation-only compiler configuration")
    if lock.get("status") != "active" or lock.get("baseline_selected_by_user") is not True:
        raise ValueError("No active user-selected reference")
    if sha256(raw_manifest) != config["manifest_sha256"]:
        raise ValueError("Probe manifest hash mismatch")
    pinned = []
    def checked(item):
        path = root / item["relative_path"]
        reject_link(path)
        path = path.resolve(strict=True)
        if not path.is_relative_to(root):
            raise ValueError("Bench input path escapes the project")
        check_identity(file_identity(path), item, "Bench input " + item["relative_path"])
        pinned.append((path, item))
        return path
    source_path = root / manifest["source"]
    source = checked({"relative_path": manifest["source"], "size": source_path.stat().st_size,
                      "sha256": config["source_sha256"]})
    reference_path = checked(lock["decrypted_executable"])
    reference = Elf32(reference_path.read_bytes())
    probes = validate_probes(reference, manifest)
    runner = checked(config["runner"])
    candidates, settings = config["candidates"], config["settings"]
    if not candidates or not settings:
        raise ValueError("Candidate/setting matrix is empty")
    for collection in (candidates, settings):
        ids = [row["id"] for row in collection]
        if len(ids) != len(set(ids)) or any(not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", i) for i in ids):
            raise ValueError("Invalid or duplicate matrix identifier")
    compilers = []
    for candidate in candidates:
        compiler = checked(candidate["compiler"])
        for support in candidate["support_files"]:
            checked(support)
        compilers.append(compiler)
    common = config["common_flags"]
    if not isinstance(common, list) or any(not isinstance(f, str) for f in common):
        raise ValueError("Invalid common compiler flags")
    for setting in settings:
        if not isinstance(setting["flags"], list) or any(not isinstance(f, str) for f in setting["flags"]):
            raise ValueError("Invalid configuration flags")
    if report_path is not None:
        report_path = Path(report_path)
        reject_link(report_path)
        protected = (candidates_path, manifest_path, lock_path, *[p for p, _ in pinned])
        if report_path.resolve() in {p.resolve() for p in protected}:
            raise ValueError("Report aliases a bench input")
    build_parent = Path(build_parent) if build_parent else root / "build"
    reject_link(build_parent)
    if not build_parent.resolve().is_relative_to(root):
        raise ValueError("Build directory escapes the project")
    build_parent.mkdir(parents=True, exist_ok=True)
    output_dir = Path(tempfile.mkdtemp(prefix="bench-bucket03-", dir=build_parent)).resolve()
    report = {"schema_version": 1, "status": "COMPILER_BENCH_COMPLETE",
              "scope": "fixed relocation-free probe comparison; no toolchain lock or matching credit",
              "matched_progress": 0, "source_sha256": config["source_sha256"],
              "manifest_sha256": sha256(raw_manifest), "candidate_config_sha256": sha256(raw_config),
              "reference_lock_sha256": sha256(raw_lock),
              "reference_sha256": lock["decrypted_executable"]["sha256"],
              "probe_count": len(probes), "common_flags": common, "results": []}
    distro = config["runner"].get("environment", "WSL Ubuntu").removeprefix("WSL ")
    for number, (candidate, compiler) in enumerate(zip(candidates, compilers)):
        for position, setting in enumerate(settings):
            obj_path = output_dir / (str(number) + "-" + str(position) + ".o")
            if obj_path.exists():
                raise ValueError("Refusing stale compiler output")
            result = compile_probe(compiler, runner, source, obj_path, common + setting["flags"],
                                   timeout=timeout, root=root, distro=distro)
            diagnostics = result["stdout"] + result["stderr"]
            (output_dir / (obj_path.stem + ".log")).write_text(diagnostics, encoding="utf-8")
            if (result["returncode"] or re.search(r"\b(warning|error|fatal|illegal|unknown)\b", diagnostics, re.I)
                    or not obj_path.is_file()):
                raise ValueError("Compiler failed or warned: " + candidate["id"] + "/" + setting["id"]
                                 + "; logs: " + str(output_dir))
            reject_link(obj_path)
            comparison = compare_object(obj_path.read_bytes(), reference, manifest)
            report["results"].append({"candidate": candidate["id"], "version": candidate["version"],
                                      "setting": setting["id"], "flags": common + setting["flags"],
                                      "exact_probes": sum(c["exact_probe_bytes"] for c in comparison["comparisons"]),
                                      **comparison})
    # Changes during the matrix invalidate every row, even if its bytes looked exact.
    for path, item in pinned:
        check_identity(file_identity(path), item, "Bench input changed " + str(path))
    for path, before in ((candidates_path, raw_config), (manifest_path, raw_manifest), (lock_path, raw_lock)):
        if path.read_bytes() != before:
            raise ValueError("Bench metadata changed during compilation")
    # Keep raw objects/logs local; the semantic report excludes random paths.
    write_report(output_dir / "report.json", report)
    if report_path is not None:
        write_report(report_path, report)
    return report


def main(argv=None):
    """Run the pinned investigation matrix and report its limits explicitly."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, default=ROOT / "config/compiler-candidates.json")
    parser.add_argument("--manifest", type=Path, default=ROOT / "config/compiler-probes.json")
    parser.add_argument("--lock", type=Path, default=ROOT / "config/reference.json")
    parser.add_argument("--report", type=Path, default=ROOT / "evidence/bucket-03/compiler-bench.json")
    parser.add_argument("--timeout", type=float, default=20)
    args = parser.parse_args(argv)
    try:
        report = run_bench(candidates_path=args.candidates, manifest_path=args.manifest,
                           lock_path=args.lock, report_path=args.report, timeout=args.timeout)
        for row in report["results"]:
            print(row["candidate"] + " / " + row["setting"] + ": "
                  + str(row["exact_probes"]) + "/" + str(report["probe_count"]) + " exact probe sequences")
        print("PROBES ONLY: no toolchain lock or matched-progress credit")
        print("Report: " + str(args.report.resolve()))
        return 0
    except (OSError, ValueError, KeyError, TypeError, struct.error, subprocess.SubprocessError) as error:
        print("BENCH FAILED: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Compare two invented layouts under unchanged MW219/C++/O2.

Complete byte comparison and bounded static address observations are separate.
The abstract CFG walker is a small diagnostic whitelist, not guest execution,
source-semantic validation or compiler-backend attribution.
"""

import argparse
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile

try:
    from .bench_archive_key import verify_archive_inputs, local_items as archive_items
    from .bench_language_modes import local_items as language_items
    from .bench_compiler_families import compile_profile, profile_items, sha256
    from .bench_synthetic_link import inspect_fixture
    from .prepare_reference import check_identity, file_identity, reject_link, write_report
except ImportError:
    from bench_archive_key import verify_archive_inputs, local_items as archive_items
    from bench_language_modes import local_items as language_items
    from bench_compiler_families import compile_profile, profile_items, sha256
    from bench_synthetic_link import inspect_fixture
    from prepare_reference import check_identity, file_identity, reject_link, write_report

ROOT = Path(__file__).resolve().parents[1]


def analyze_address_paths(code, offsets, *, max_states=2048, max_paths=32):
    """Track constants/receiver offsets through bounded forward paths, fail closed.

    Both unknown branch outcomes are retained separately. Counts are the union
    of static instruction sites, never a sum of visits or dynamic access counts.
    No partial count is returned when any path cannot be interpreted.
    """
    def unknown(reason):
        return {"status": "UNINTERPRETED", "reason": reason,
                "large_base_site_count": None, "large_base_sites": None, "access_traces": None}
    if not code or len(code) % 4 or len(code) > 512:
        return unknown("Unsupported complete function length")
    words = list(struct.unpack("<" + "I" * (len(code) // 4), code))
    if set(offsets) != {"lower", "upper"} or any(not isinstance(v, int) or v < 0 or v % 4 for v in offsets.values()):
        return unknown("Invalid declared field offsets")
    registers = [None] * 32
    registers[0], registers[4], registers[31] = ("constant", 0), ("receiver", 0, frozenset()), ("return", 0)
    pending = [(0, registers, ())]
    traces, sites, covered, accesses = set(), set(), set(), {}
    visited = 0
    def signed16(value):
        return value - 0x10000 if value & 0x8000 else value
    def add(left, right):
        if left is None or right is None:
            return None
        if left[0] == right[0] == "constant":
            return "constant", (left[1] + right[1]) & 0xFFFFFFFF
        if left[0] == "constant" and right[0] == "receiver":
            return "receiver", (left[1] + right[1]) & 0xFFFFFFFF, right[2]
        if right[0] == "constant" and left[0] == "receiver":
            return "receiver", (left[1] + right[1]) & 0xFFFFFFFF, left[2]
        return None
    while pending:
        pc, regs, trace = pending.pop()
        while True:
            visited += 1
            if visited > max_states or len(traces) + len(pending) > max_paths:
                return unknown("Static path budget exceeded")
            if pc < 0 or pc >= len(code) or pc % 4:
                return unknown("Unmapped static instruction")
            word = words[pc // 4]
            covered.add(pc)
            op, rs, rt, rd, shift, funct = word >> 26, word >> 21 & 31, word >> 16 & 31, word >> 11 & 31, word >> 6 & 31, word & 63
            immediate = word & 0xFFFF
            def put(index, value):
                if index:
                    regs[index] = value
                regs[0] = ("constant", 0)
            if word == 0:
                pc += 4
                continue
            if word == 0x03E00008:  # JR ra, with a NOP delay slot only.
                if regs[31] != ("return", 0) or pc + 4 >= len(code) or words[pc // 4 + 1] != 0:
                    return unknown("Unsupported return delay slot")
                covered.add(pc + 4)
                traces.add(trace)
                if len(traces) > max_paths:
                    return unknown("Static return-path budget exceeded")
                break
            if op in (4, 5):  # BEQ/BNE: internal forward edges only.
                target = pc + 4 + signed16(immediate) * 4
                if (pc + 4 >= len(code) or words[pc // 4 + 1] != 0
                        or target <= pc + 4 or target >= len(code) or target % 4):
                    return unknown("Unsupported branch target or delay slot")
                covered.add(pc + 4)
                left, right = regs[rs], regs[rt]
                if rs == rt:
                    pc = target if op == 4 else pc + 8
                elif left is not None and right is not None and left[0] == right[0] == "constant":
                    taken = (left[1] == right[1]) == (op == 4)
                    pc = target if taken else pc + 8
                else:
                    pending.append((target, regs.copy(), trace))
                    pc += 8
                continue
            if op == 15 and rs == 0:
                put(rt, ("constant", immediate << 16))
            elif op == 9:
                put(rt, add(regs[rs], ("constant", signed16(immediate) & 0xFFFFFFFF)))
            elif op in (12, 13):
                value = regs[rs]
                if value is None or value[0] != "constant":
                    put(rt, None)
                else:
                    put(rt, ("constant", value[1] & immediate if op == 12 else value[1] | immediate))
            elif op == 0 and funct == 2 and rs == 0:
                value = regs[rt]
                put(rd, ("constant", value[1] >> shift) if value and value[0] == "constant" else None)
            elif op == 0 and funct == 33 and shift == 0:
                left, right = regs[rs], regs[rt]
                value = add(left, right)
                if rd and value and value[0] == "receiver":
                    origins = value[2]
                    for operand in (left, right):
                        if operand and operand[0] == "constant":
                            signed = operand[1] if operand[1] < 0x80000000 else operand[1] - 0x100000000
                            if abs(signed) >= 0x8000:
                                origins = origins | {pc}
                    value = value[0], value[1], origins
                put(rd, value)
            elif op in (35, 43):  # LW/SW only; the loaded value kills provenance.
                base = regs[rs]
                if base is None or base[0] != "receiver":
                    return unknown("Unresolved receiver-relative memory address")
                if not base[2]:
                    return unknown("Address construction outside characterized large-ADDU model")
                address = (base[1] + signed16(immediate)) & 0xFFFFFFFF
                if address % 4 or address not in offsets.values():
                    return unknown("Memory access differs from declared field offsets")
                access = ("read" if op == 35 else "write", address)
                if pc in accesses and accesses[pc] != access:
                    return unknown("Path-dependent memory address")
                accesses[pc] = access
                sites.update(base[2])
                trace += (access,)
                if op == 35:
                    put(rt, None)
            else:
                return unknown("Instruction outside static-analysis whitelist")
            pc += 4
    if not traces or any(index * 4 not in covered and word != 0 for index, word in enumerate(words)):
        return unknown("Uncovered nonpadding instruction or missing return")
    lower, upper = offsets["lower"], offsets["upper"]
    expected = set()
    for low_default in (False, True):
        for high_default in (False, True):
            trace = (("write", upper), ("write", lower))
            if low_default:
                trace += (("write", lower),)
            trace += (("read", upper),)
            if high_default:
                trace += (("write", upper),)
            expected.add(trace)
    if traces != expected:
        return unknown("Static access paths differ from the declared fixture pattern")
    return {"status": "INTERPRETED", "large_base_site_count": len(sites),
            "large_base_sites": sorted(sites),
            "access_traces": [[{"operation": op, "offset": offset} for op, offset in trace]
                              for trace in sorted(traces)]}


def inspect_address_fixture(data, expected_symbol, offsets):
    """Validate the full ELF function before attempting bounded static analysis."""
    observation = inspect_fixture(data, 1, expected_symbol)
    code = bytes.fromhex(observation["function"]["bytes_hex"])
    observation["address_analysis"] = analyze_address_paths(code, offsets)
    return observation


def local_items(config):
    return [config["archive_profile"]] + [f["source"] for f in config["fixtures"]]


def verify_inputs(root, config):
    """Keep the real candidate frozen while checking both invented fixtures."""
    for item in local_items(config):
        path = root / item["relative_path"]
        reject_link(path)
        if not path.resolve(strict=True).is_relative_to(root):
            raise ValueError("Address fixture input escapes project")
        check_identity(file_identity(path), item, "Address fixture input")
    archive = json.loads((root / config["archive_profile"]["relative_path"]).read_bytes())
    families, profile, unused, reference, reference_pin, language = verify_archive_inputs(root, archive)
    if (config["common_flags"] != archive["common_flags"] or config["optimization"] != archive["optimization"]
            or config["object_symbol"] != archive["object_symbol"]
            or [f["id"] for f in config["fixtures"]] != ["direct", "grouped"]
            or config["field_offsets"] != {"lower": 0x1A120, "upper": 0x1A124}
            or config["defaults"] != {"lower": 0x1357, "upper": 0x2468}
            or config["word_width"] != 4 or config["record_extent"] != 0x1A128
            or config["declared_trials"] != 2 or config["grouping_only"] is not True
            or config["cached_pointer_or_reference"] is not False):
        raise ValueError("Address fixtures differ from the reviewed two-case scope")
    return families, profile, archive, language, reference_pin


def run_address_reuse(*, root=ROOT, config_path=None, report_path=None):
    """Compile two fresh invented objects, retain failures and compare full bytes."""
    root = Path(root).resolve(strict=True)
    config_path = Path(config_path) if config_path else root / "config/address-reuse.json"
    raw = config_path.read_bytes()
    config = json.loads(raw)
    if config["status"] != "frozen_before_fixture_compilation" or config["no_fixture_compilation_observed"] is not True:
        raise ValueError("Address fixture cases were not frozen before compilation")
    protected = {config_path.resolve()} | {(root / i["relative_path"]).resolve() for i in local_items(config)}
    if report_path is not None:
        report_path = Path(report_path)
        reject_link(report_path)
        if report_path.resolve() in protected:
            raise ValueError("Address fixture report aliases input")
    families, profile, archive, language, reference_pin = verify_inputs(root, config)
    inherited = archive_items(archive) + language_items(language) + profile_items(families) + [reference_pin]
    if report_path is not None and report_path.resolve() in {(root / i["relative_path"]).resolve() for i in inherited}:
        raise ValueError("Address fixture report aliases inherited input")
    build = root / "build"
    reject_link(build)
    if not build.resolve().is_relative_to(root):
        raise ValueError("Address fixture build escapes project")
    build.mkdir(exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="address-reuse-", dir=build))
    report = {"schema_version": 1, "status": "ADDRESS_REUSE_INVESTIGATION_COMPLETE",
              "profile_sha256": sha256(raw), "matched_progress": 0,
              "flags": config["common_flags"] + config["optimization"], "fixtures": []}
    emitted, functions = {}, {}
    for fixture in config["fixtures"]:
        obj = directory / (fixture["id"] + ".o")
        row = {"id": fixture["id"], "source_sha256": fixture["source"]["sha256"], "outcome": "OUTPUT_REJECTED"}
        try:
            execution = compile_profile(dict(profile, common_flags=config["common_flags"],
                                              timeout_tool=families["linux_utilities"][0]["linux_path"]),
                                        root / fixture["source"]["relative_path"], obj, config["optimization"], root=root)
            diagnostic = execution["stdout"] + execution["stderr"]
            obj.with_suffix(".log").write_text(diagnostic, encoding="utf-8")
            row["returncode"] = execution["returncode"]
            if obj.is_file():
                reject_link(obj)
                emitted[obj] = obj.read_bytes()
                row["object_sha256"] = sha256(emitted[obj])
            if (execution["returncode"] or obj not in emitted
                    or re.search(r"\b(warning|error|fatal|illegal|unknown)\b", diagnostic, re.I)):
                row["reason"] = "Compiler failure, warning or missing object"
            else:
                row["observation"] = inspect_address_fixture(emitted[obj], config["object_symbol"], config["field_offsets"])
                row["outcome"] = "OBJECT_VALIDATED"
                functions[fixture["id"]] = row["observation"]["function"]
        except (OSError, subprocess.SubprocessError) as error:
            row["reason"] = "Fixture compilation unavailable: " + type(error).__name__
        except ValueError as error:
            row["reason"] = "Fixture output rejected: " + str(error)
        report["fixtures"].append(row)
    verify_inputs(root, config)
    if config_path.read_bytes() != raw:
        raise ValueError("Address fixture profile changed during trial")
    for obj, original in emitted.items():
        reject_link(obj)
        if obj.read_bytes() != original:
            raise ValueError("Emitted address fixture changed during trial")
    report["function_comparison"] = None
    if set(functions) == {"direct", "grouped"}:
        direct, grouped = functions["direct"], functions["grouped"]
        report["function_comparison"] = {"identical": direct["bytes_hex"] == grouped["bytes_hex"],
            "direct_size": direct["size"], "grouped_size": grouped["size"],
            "direct_sha256": direct["sha256"], "grouped_sha256": grouped["sha256"]}
    # No zero count or ranking is manufactured when either analysis is unknown.
    report["address_comparison"] = {"status": "UNINTERPRETED", "static_site_reduction": None}
    if all(f["outcome"] == "OBJECT_VALIDATED" and f["observation"]["address_analysis"]["status"] == "INTERPRETED"
           for f in report["fixtures"]):
        direct, grouped = [f["observation"]["address_analysis"] for f in report["fixtures"]]
        report["address_comparison"] = {"status": "INTERPRETED",
            "static_site_reduction": direct["large_base_site_count"] - grouped["large_base_site_count"]}
    if report_path is not None:
        write_report(report_path, report)
    return report, directory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", default="evidence/bucket-03j/address-reuse-trial.json")
    args = parser.parse_args()
    if os.name == "nt":
        return subprocess.run(["wsl", "-d", "Ubuntu", "--", "python3", "scripts/bench_address_reuse.py",
                               "--report", args.report], cwd=ROOT).returncode
    try:
        report, directory = run_address_reuse(report_path=ROOT / args.report)
        print(json.dumps({"status": report["status"], "build_directory": str(directory), "report": args.report}))
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

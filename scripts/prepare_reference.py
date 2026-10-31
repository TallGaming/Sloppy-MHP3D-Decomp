#!/usr/bin/env python3
"""Recreate the selected encrypted/decrypted reference from its pinned ISO.

The image is opened read-only. Decryption runs in a fresh staging directory,
and both output identities and the ELF structure must pass before publication.
Existing different reference files are errors, never overwritten. This is
reference preparation only, not a game build or a matching gate.
"""

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zlib

try:
    from .elf32 import Elf32
    from .inspect_input import inspect_iso, SECTOR_SIZE
except ImportError:
    from elf32 import Elf32
    from inspect_input import inspect_iso, SECTOR_SIZE


ROOT = Path(__file__).resolve().parents[1]
CHUNK_SIZE = 8 * 1024 * 1024


def file_identity(path):
    """Hash the bytes actually read and reject a file changed during the read."""
    before = path.stat()
    digests = {name: hashlib.new(name) for name in ("sha256", "sha1", "md5")}
    crc, size = 0, 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(CHUNK_SIZE), b""):
            for digest in digests.values():
                digest.update(chunk)
            crc = zlib.crc32(chunk, crc)
            size += len(chunk)
    after = path.stat()
    if (size != before.st_size or size != after.st_size
            or before.st_mtime_ns != after.st_mtime_ns):
        raise ValueError("File changed while reading: " + str(path))
    result = {name: digest.hexdigest() for name, digest in digests.items()}
    result.update(size=size, crc32=format(crc, "08x"))
    return result


def check_identity(actual, expected, label):
    """Check all pinned identity fields; size and SHA-256 are mandatory."""
    if "size" not in expected or "sha256" not in expected:
        raise ValueError(label + " lock is missing size or SHA-256")
    for key in ("size", "sha256", "sha1", "md5", "crc32"):
        if key in expected and actual.get(key) != expected[key]:
            raise ValueError(label + " identity mismatch: " + key)


def reject_link(path):
    """Reject redirected output/input entries instead of following them."""
    is_junction = getattr(path, "is_junction", lambda: False)
    if path.is_symlink() or is_junction():
        raise ValueError("Link/junction paths are unsupported: " + str(path))


def run_decryptor(decryptor_path, encrypted_path, decrypted_path, *,
                  timeout, wsl_distro):
    """Run the pinned Linux helper with empty stdin, a timeout and bounded logs."""
    if os.name == "nt":
        prefix = ["wsl", "-d", wsl_distro, "--"]

        def runtime_path(path):
            result = subprocess.run(
                prefix + ["wslpath", "-a", path.as_posix()],
                stdin=subprocess.DEVNULL, capture_output=True, text=True,
                check=True, timeout=min(timeout, 10)
            )
            converted = result.stdout.strip()
            if not converted:
                raise ValueError("WSL path conversion produced an empty path")
            return converted

        command = prefix + ["timeout", str(timeout) + "s",
                            runtime_path(decryptor_path),
                            runtime_path(encrypted_path), "-o",
                            runtime_path(decrypted_path)]
    else:
        command = [str(decryptor_path), str(encrypted_path), "-o", str(decrypted_path)]
    result = subprocess.run(
        command, stdin=subprocess.DEVNULL, capture_output=True, text=True,
        timeout=timeout + 5 if os.name == "nt" else timeout
    )
    return {"returncode": result.returncode, "stdout": result.stdout,
            "stderr": result.stderr, "command": command}


def prepare_reference(iso_path, output_dir, *,
                      lock_path=ROOT / "config/reference.json",
                      helper_lock_path=ROOT / "config/helper-tools.json",
                      helper_path=None, timeout=60, wsl_distro="Ubuntu"):
    """Prepare only the active reference, returning a deterministic report."""
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("Helper timeout must be finite and positive")
    iso_path, output_dir = Path(iso_path), Path(output_dir)
    lock_path, helper_lock_path = Path(lock_path), Path(helper_lock_path)
    reject_link(iso_path)
    reject_link(output_dir)
    iso_path = iso_path.resolve(strict=True)
    lock_bytes = lock_path.read_bytes()
    lock = json.loads(lock_bytes)
    if lock.get("status") != "active" or lock.get("baseline_selected_by_user") is not True:
        raise ValueError("No active user-selected reference lock")
    helper_lock_bytes = helper_lock_path.read_bytes()
    helper = json.loads(helper_lock_bytes)["pspdecrypt"]
    decryptor = Path(helper_path) if helper_path is not None else ROOT / helper["relative_path"]
    reject_link(decryptor)
    if not decryptor.is_file():
        raise ValueError("Missing decryption helper: " + str(decryptor))
    decryptor = decryptor.resolve(strict=True)
    helper_identity = file_identity(decryptor)
    if helper_identity["sha256"] != helper["sha256"]:
        raise ValueError("Decryption helper hash mismatch")
    before = iso_path.stat()
    image_identity = file_identity(iso_path)
    check_identity(image_identity, lock, "ISO")

    # Find extents from this verified image, never from a stale inventory file.
    inventory = inspect_iso(iso_path)
    if inventory["sha256"] != image_identity["sha256"]:
        raise ValueError("ISO changed during inventory")
    entries = {entry["path"]: entry for entry in inventory["files"]}
    metadata = entries.get("/PSP_GAME/PARAM.SFO", {}).get("sfo", {}).get("values", {})
    for field, key in (("DISC_ID", "disc_id"), ("DISC_VERSION", "disc_version"),
                       ("TITLE", "title")):
        if key not in lock or metadata.get(field) != lock[key]:
            raise ValueError("Game metadata mismatch: " + field)
    encrypted_lock = lock["executable"]
    decrypted_lock = lock["decrypted_executable"]
    entry = entries.get(encrypted_lock["iso_path"])
    if entry is None:
        raise ValueError("Pinned executable is missing from the ISO")
    check_identity(entry, encrypted_lock, "Encrypted executable")
    with iso_path.open("rb") as stream:
        stream.seek(entry["lba"] * SECTOR_SIZE)
        encrypted = stream.read(entry["size"])
    check_identity({"size": len(encrypted), "sha256": hashlib.sha256(encrypted).hexdigest()},
                   encrypted_lock, "Extracted executable")
    if not encrypted.startswith(b"~PSP"):
        raise ValueError("Expected an encrypted ~PSP executable")

    output_dir = output_dir.resolve()
    destinations = {"encrypted": output_dir / "EBOOT.BIN",
                    "decrypted": output_dir / "EBOOT.ELF"}
    expected = {"encrypted": encrypted_lock, "decrypted": decrypted_lock}
    protected = {iso_path, decryptor, lock_path.resolve(), helper_lock_path.resolve()}
    for name, destination in destinations.items():
        reject_link(destination)
        if destination.resolve() in protected:
            raise ValueError("Reference output aliases a protected input")
        if destination.exists():
            if not destination.is_file():
                raise ValueError("Reference output is not a regular file")
            check_identity(file_identity(destination), expected[name], "Existing " + name)
    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix=".prepare-", dir=output_dir) as temp:
        stage = Path(temp).resolve()
        # Verify the directory that TemporaryDirectory will recursively remove.
        if not stage.is_relative_to(output_dir):
            raise ValueError("Staging directory escaped the reference output directory")
        staged_bin, staged_elf = stage / "EBOOT.BIN", stage / "EBOOT.ELF"
        staged_bin.write_bytes(encrypted)
        try:
            result = run_decryptor(decryptor, staged_bin, staged_elf,
                                   timeout=timeout, wsl_distro=wsl_distro)
        except subprocess.TimeoutExpired as error:
            raise ValueError("Decryption helper timed out") from error
        if result["returncode"]:
            reason = result.get("stderr", "").strip()[:1000]
            if result["returncode"] == 124:
                raise ValueError("Decryption helper timed out (exit 124)")
            raise ValueError("Decryption helper failed (exit " + str(result["returncode"])
                             + "): " + reason)
        if not staged_elf.is_file():
            raise ValueError("Decryption helper produced no output")
        reject_link(staged_elf)
        decrypted_identity = file_identity(staged_elf)
        check_identity(decrypted_identity, decrypted_lock, "Decrypted executable")
        elf = Elf32(staged_elf.read_bytes())
        if elf.file_type != 2:
            raise ValueError("Decrypted executable is not an ELF executable")
        after = iso_path.stat()
        if (after.st_size != before.st_size or after.st_mtime_ns != before.st_mtime_ns):
            raise ValueError("ISO changed during reference preparation")
        # Validate both products again after the helper, before publishing either.
        check_identity(file_identity(staged_bin), encrypted_lock, "Staged encrypted executable")
        if file_identity(decryptor)["sha256"] != helper["sha256"]:
            raise ValueError("Decryption helper changed during execution")
        for name, staged in (("encrypted", staged_bin), ("decrypted", staged_elf)):
            destination = destinations[name]
            reject_link(destination)
            if destination.exists():
                check_identity(file_identity(destination), expected[name], "Existing " + name)
            else:
                # Exclusive creation refuses a file inserted since preflight.
                with destination.open("xb") as stream:
                    stream.write(staged.read_bytes())
    return {"schema_version": 1, "status": "REFERENCE_PREPARATION_PASS",
            "scope": "reference preparation only; not a game build or matching gate",
            "disc_id": lock["disc_id"], "disc_version": lock["disc_version"],
            "reference_lock_sha256": hashlib.sha256(lock_bytes).hexdigest(),
            "helper_lock_sha256": hashlib.sha256(helper_lock_bytes).hexdigest(),
            "iso": image_identity,
            "helper": {"sha256": helper_identity["sha256"],
                       "git_commit": helper.get("git_commit")},
            "artifacts": {"EBOOT.BIN": {"size": len(encrypted),
                                         "sha256": encrypted_lock["sha256"]},
                          "EBOOT.ELF": {"size": decrypted_identity["size"],
                                         "sha256": decrypted_identity["sha256"]}},
            "elf_entry": hex(elf.entry),
            "helper_stdout": result.get("stdout", "").strip()}


def write_report(path, report):
    """Create evidence or accept an identical report; refuse conflicting evidence."""
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    path = Path(path)
    reject_link(path)
    if path.exists():
        if path.read_text(encoding="utf-8") != encoded:
            raise ValueError("Existing report differs; choose a fresh report path")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(encoded)


def main(argv=None):
    """Prepare the accepted reference and emit reviewable identity evidence."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iso", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, default=ROOT / "reference/uljm05800-v102")
    parser.add_argument("--report", type=Path, default=ROOT / "evidence/bucket-01/reference-preparation.json")
    parser.add_argument("--lock", type=Path, default=ROOT / "config/reference.json")
    parser.add_argument("--helper-lock", type=Path, default=ROOT / "config/helper-tools.json")
    parser.add_argument("--helper-path", type=Path)
    parser.add_argument("--timeout", type=float, default=60)
    parser.add_argument("--wsl-distro", default="Ubuntu")
    args = parser.parse_args(argv)
    try:
        protected = {args.iso.resolve(), args.lock.resolve(), args.helper_lock.resolve()}
        if args.report.resolve() in protected or args.report.resolve() in {
                (args.out_dir / "EBOOT.BIN").resolve(), (args.out_dir / "EBOOT.ELF").resolve()}:
            raise ValueError("Report path aliases an input or executable output")
        report = prepare_reference(args.iso, args.out_dir, lock_path=args.lock,
                                   helper_lock_path=args.helper_lock,
                                   helper_path=args.helper_path, timeout=args.timeout,
                                   wsl_distro=args.wsl_distro)
        write_report(args.report, report)
        print(report["status"] + ": " + report["disc_id"] + " v" + report["disc_version"])
        print("Report: " + str(args.report.resolve()))
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print("REFERENCE PREPARATION FAILED: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Preserve selected original containers without decrypting or executing them.

Declared PSP headers, unknown SCE wrappers and actual payload identities remain
separate. This is a bounded scope inventory, never a complete code inventory or
a game matching gate. Existing extraction and compiler profiles stay unchanged.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import tempfile

try:
    from . import recover_overlay_set as recovery
except ImportError:
    import recover_overlay_set as recovery

inventory = recovery.inventory
pilot = recovery.pilot
ROOT = Path(__file__).resolve().parents[1]
MAX_PAYLOAD = 8 * 1024 * 1024
PSP_HEADER_SIZE = 0x150
ARCHIVE_SELECTION = (17, 18, 19, 20)
ISO_SELECTION = (
    ("/PSP_GAME/SYSDIR/EBOOT.BIN", "main-eboot-control.bin", "existing_main_reference_control"),
    ("/PSP_GAME/SYSDIR/BOOT.BIN", "boot.bin", "boot_full_byte_audit"),
    ("/PSP_GAME/SYSDIR/OPNSSMP.BIN", "opnssmp.bin", "supplemental_container_candidate"),
    ("/PSP_GAME/SYSDIR/UPDATE/EBOOT.BIN", "updater-eboot.bin", "preserved_packaged_update_container"),
)


def describe_header(raw):
    """Read only declared fields from a complete ~PSP header; do not infer code."""
    result = {"magic_hex": raw[:4].hex(), "decrypted": False,
        "ownership": "UNCLASSIFIED", "code_extent": None}
    if raw[:4] != b"~PSP" or len(raw) < PSP_HEADER_SIZE:
        result.update(status="UNINTERPRETED", reason="No complete supported ~PSP header at offset zero")
        return result
    name_raw = raw[0x0A:0x26]
    try:
        name = name_raw.split(b"\0", 1)[0].decode("ascii")
    except UnicodeDecodeError:
        name = None
    word = lambda offset: struct.unpack_from("<I", raw, offset)[0]
    signed_word = lambda offset: struct.unpack_from("<i", raw, offset)[0]
    result.update(status="DECLARED_PSP_HEADER_ONLY", module_name=name,
        module_name_raw_hex=name_raw.hex(), attribute=struct.unpack_from("<H", raw, 4)[0],
        compression_attribute=struct.unpack_from("<H", raw, 6)[0],
        module_version_bytes=list(raw[8:10]), header_version=raw[0x26],
        declared_segment_count=raw[0x27], declared_elf_size=word(0x28),
        declared_psp_size=word(0x2C), declared_psp_size_equals_actual=word(0x2C) == len(raw),
        declared_entry=word(0x30), declared_module_info_offset=word(0x34),
        declared_bss_size=signed_word(0x38), declared_devkit_version=word(0x78),
        declared_decrypt_mode=word(0x7C), declared_compressed_size=signed_word(0xB0),
        declared_tag_hex=f"{word(0xD0):08X}", metadata_authenticated=False,
        declared_sizes_are_validated_code_extents=False)
    return result


def payload_records(stream, iso_size, files, archive, entries, control_bytes):
    """Read exactly eight bounded payloads and bind them to fresh metadata."""
    paths = [item["path"] for item in files]
    if len(paths) != len(set(paths)):
        raise ValueError("Duplicate fresh ISO paths")
    selected = []
    for path, filename, role in ISO_SELECTION:
        matches = [item for item in files if item["path"] == path]
        if len(matches) != 1:
            raise ValueError("Missing selected ISO path: " + path)
        item = matches[0]
        if not 0 < item["size"] <= MAX_PAYLOAD:
            raise ValueError("Selected ISO payload exceeds bound")
        raw = pilot.read_extent(stream, 0, iso_size, item["lba"] * pilot.BLOCK, item["size"])
        pilot.check_identity(pilot.identity(raw), item, "Fresh ISO payload")
        if role == "existing_main_reference_control" and raw != control_bytes:
            raise ValueError("Main encrypted EBOOT whole-byte control mismatch")
        selected.append((filename, raw, {"kind": "iso", "path": path, "lba": item["lba"]}, role))
    for number in ARCHIVE_SELECTION:
        item = entries[number]
        length = item["stored_length"]
        if (item["archive_index"] != number or item["raw_magic"] != b"~SCE".hex()
                or not 64 <= length <= min(item["extent_size"], MAX_PAYLOAD)
                or item["prefix_size"] != 64):
            raise ValueError("Raw SCE candidate index/length/prefix changed")
        raw = pilot.read_extent(stream, archive["lba"] * pilot.BLOCK, archive["size"],
            item["block"] * pilot.BLOCK, length)
        if raw[:4] != b"~SCE" or pilot.identity(raw[:64])["sha256"] != item["raw_prefix_sha256"]:
            raise ValueError("Raw SCE candidate prefix mismatch")
        selected.append((f"archive-entry-{number:04d}.bin", raw,
            {"kind": "archive", "archive_index": number, "block": item["block"],
             "stored_length": length, "extent_size": item["extent_size"]}, "unclassified_raw_sce_candidate"))
    result = []
    for filename, raw, source, role in selected:
        nonzero = sum(value != 0 for value in raw)
        row = {"relative_path": filename, "source": source, "role": role,
            "payload": pilot.identity(raw), "header": describe_header(raw),
            "full_nonzero_byte_count": nonzero, "entire_payload_zero": nonzero == 0}
        result.append((filename, raw, row))
    return result


def verify_inputs(root, config):
    """Bind every reused inventory, format reference and preserved source input."""
    if (config["status"] != "frozen_before_supplemental_inventory"
            or config["maximum_payload_bytes"] != MAX_PAYLOAD or config["declared_trials"] != 2
            or config["archive_indexes"] != list(ARCHIVE_SELECTION)
            or config["iso_paths"] != [p[0] for p in ISO_SELECTION]
            or config["output_parent_relative_path"] != "reference/uljm05800-v102/supplemental-sets"
            or any(config[k] is not False for k in ("decryption", "decompression", "runtime_execution",
                "source_match_credit", "complete_game_code_inventory_established"))):
        raise ValueError("Supplemental inventory differs from reviewed bounded scope")
    records = [config[k] for k in ("known_recovery_profile", "inventory_profile", "candidate_inventory", "header_source", "main_control")]
    for item in records + config["preserved_inputs"]:
        path = root / item["relative_path"]
        pilot.reject_link(path)
        if not path.resolve(strict=True).is_relative_to(root):
            raise ValueError("Supplemental input escapes project")
        pilot.check_identity(pilot.file_identity(path), item, "Supplemental input")
    inherited = json.loads((root / config["known_recovery_profile"]["relative_path"]).read_bytes())
    if config["inventory_profile"] != inherited["inventory_profile"]:
        raise ValueError("Supplemental inventory profile differs from inherited inventory")
    previous, known, lock, old_pilot = recovery.verify_inputs(root, inherited)
    candidate = json.loads((root / config["candidate_inventory"]["relative_path"]).read_bytes())
    pilot.check_identity(candidate, {k: lock[k] for k in ("size", "sha256")}, "Original ISO directory evidence")
    if config["main_control"]["sha256"] != lock["executable"]["sha256"]:
        raise ValueError("Main control differs from selected reference")
    return previous, known, lock, old_pilot, candidate


def audit_stage(stage, records, manifest_bytes):
    """Reject missing, changed, redirected or extra staged products."""
    pilot.reject_link(stage)
    if not stage.is_dir():
        raise ValueError("Supplemental stage is not a regular directory")
    expected = {name for name, _, _ in records} | {"manifest.json"}
    if {path.name for path in stage.iterdir()} != expected:
        raise ValueError("Supplemental staged file set differs")
    for filename, raw, _ in records + [("manifest.json", manifest_bytes, {})]:
        path = stage / filename
        pilot.reject_link(path)
        if not path.is_file() or path.read_bytes() != raw:
            raise ValueError("Supplemental staged output changed: " + filename)


def reject_path_chain(path, root):
    """Reject redirected output parents before creating any directories."""
    for current in (path, *path.parents):
        pilot.reject_link(current)
        if current == root:
            return
    raise ValueError("Supplemental output is outside the project")


def recover_supplemental(iso_path, output_dir, *, root=ROOT, config_path=None, report_path=None):
    root = Path(root).resolve(strict=True)
    config_path = Path(config_path) if config_path else root / "config/supplemental-modules.json"
    pilot.reject_link(config_path)
    config_bytes = config_path.read_bytes()
    config = json.loads(config_bytes)
    previous, known, lock, old_pilot, candidate = verify_inputs(root, config)
    iso_path = Path(iso_path)
    pilot.reject_link(iso_path)
    iso_path = iso_path.resolve(strict=True)
    output_parent = root / config["output_parent_relative_path"]
    reject_path_chain(output_parent, root)
    output_dir = Path(output_dir).absolute()
    for path in (output_parent, output_dir):
        pilot.reject_link(path)
    if (output_dir.parent.resolve() != output_parent.resolve() or output_dir.exists()
            or not output_dir.name or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in output_dir.name)):
        raise ValueError("Choose a fresh named set in the private supplemental area")
    if report_path is not None:
        report_path = Path(report_path).absolute()
        reject_path_chain(report_path.parent, root)
        pilot.reject_link(report_path)
        if (report_path.exists() or not report_path.resolve().is_relative_to(root / "evidence")
                or report_path.resolve().is_relative_to(output_dir.resolve())
                or report_path.resolve() in (iso_path, config_path.resolve())):
            raise ValueError("Choose fresh evidence outside inputs and recovered output")
    before = iso_path.stat()
    pilot.check_identity(pilot.file_identity(iso_path), lock, "ISO before supplemental recovery")
    fresh_known = inventory.inventory_overlays(iso_path, root=root,
        config_path=root / config["inventory_profile"]["relative_path"])
    if fresh_known != known:
        raise ValueError("Fresh archive prefix inventory differs")
    fresh_iso = pilot.inspect_iso(iso_path)
    pilot.check_identity(fresh_iso, {k: lock[k] for k in ("size", "sha256")}, "Fresh ISO directory")
    if fresh_iso["files"] != candidate["files"]:
        raise ValueError("Fresh ISO paths/extents/hashes changed")
    control = (root / config["main_control"]["relative_path"]).read_bytes()
    with iso_path.open("rb") as stream:
        records = payload_records(stream, lock["size"], fresh_iso["files"], known["archive"], known["entries"], control)
    if len(records) != 8:
        raise ValueError("Incomplete supplemental payload set")
    report = {"schema_version": 1, "status": "SUPPLEMENTAL_CONTAINER_INVENTORY_COMPLETE",
        "scope": "eight exact containers and declared metadata; no decryption or full code inventory",
        "profile_sha256": hashlib.sha256(config_bytes).hexdigest(), "iso_sha256": lock["sha256"],
        "iso_directory_file_count": len(fresh_iso["files"]), "payload_count": len(records),
        "main_eboot_whole_byte_control_exact": True, "modules": [r[2] for r in records],
        "complete_game_code_inventory_established": False, "decryption": False,
        "runtime_tested": False, "source_match_credit": False}
    manifest_bytes = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
    output_parent.mkdir(parents=True, exist_ok=True)
    for path in (output_parent, *output_parent.parents):
        pilot.reject_link(path)
        if path == root:
            break
    with tempfile.TemporaryDirectory(prefix=".supplemental-", dir=output_parent) as temporary:
        stage = Path(temporary).resolve(strict=True)
        if stage.parent != output_parent.resolve():
            raise ValueError("Supplemental staging escaped private output area")
        for filename, raw, _ in records:
            (stage / filename).write_bytes(raw)
        (stage / "manifest.json").write_bytes(manifest_bytes)
        audit_stage(stage, records, manifest_bytes)
        verify_inputs(root, config)
        pilot.reject_link(iso_path)
        pilot.check_identity(pilot.file_identity(iso_path), lock, "ISO after supplemental recovery")
        after = iso_path.stat()
        if ((before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns)
                or config_path.read_bytes() != config_bytes):
            raise ValueError("Supplemental recovery input changed")
        audit_stage(stage, records, manifest_bytes)
        reject_path_chain(stage, root)
        reject_path_chain(output_parent, root)
        pilot.reject_link(output_dir)
        if output_dir.exists():
            raise ValueError("Preserve existing supplemental set")
        stage.rename(output_dir)
    audit_stage(output_dir, records, manifest_bytes)
    if report_path is not None:
        reject_path_chain(report_path.parent, root)
        pilot.write_report(report_path, report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("iso", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = recover_supplemental(args.iso, args.output, report_path=args.out)
    except (OSError, ValueError, KeyError, IndexError) as error:
        parser.exit(1, "Supplemental inventory failed: " + str(error) + "\n")
    print(json.dumps({"status": report["status"], "payloads": report["payload_count"]}))


if __name__ == "__main__":
    main()

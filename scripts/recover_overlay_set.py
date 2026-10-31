"""Recover exactly the known PSP overlay images into a fresh private set.

The frozen header inventory is reproduced before complete decoding. Original
stored bytes are preserved, BSS stays metadata, and no compiler or game runs.
The final directory contains both verified payloads and its deterministic manifest.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
import tempfile

try:
    from . import inventory_overlays as inventory
except ImportError:
    import inventory_overlays as inventory

pilot = inventory.pilot
ROOT = Path(__file__).resolve().parents[1]
MAX_PAYLOAD = 2 * 1024 * 1024
MAX_SPAN = 128


def observe_address_span(header, payload):
    """Record a bounded raw-word span without naming constructors or entries."""
    base = header["load_address"]
    start, end = header["raw_0x18"], header["raw_0x1c"]
    if (end < start or end - start > MAX_SPAN or start % 4 or end % 4
            or start < base or end > base + len(payload)):
        return {"status": "UNINTERPRETED", "reason": "Raw span is outside the bounded stored-image model",
                "words": None, "all_values_in_declared_code": None}
    raw = payload[start - base:end - base]
    values = [value[0] for value in struct.iter_unpack("<I", raw)]
    code_start, code_end = base + 64, base + 64 + header["code_size"]
    words = [{"value": value, "word_aligned": value % 4 == 0,
              "within_declared_code": code_start <= value < code_end} for value in values]
    return {"status": "BOUNDED_RAW_SPAN", "span_size": len(raw), "words": words,
            "all_values_in_declared_code": (all(item["word_aligned"] and item["within_declared_code"] for item in words)
                                             if words else None)}


def local_items(config):
    return [config["inventory_profile"], config["inventory_report"],
            *config["preserved_inputs"]]


def verify_inputs(root, config):
    """Bind the known set, original locks and preserved source/assembly drafts."""
    if (config["status"] != "frozen_before_recovery" or config["maximum_payload_bytes"] != MAX_PAYLOAD
            or config["maximum_raw_address_span_bytes"] != MAX_SPAN or config["declared_trials"] != 2):
        raise ValueError("Overlay recovery differs from the reviewed bounded scope")
    for item in local_items(config):
        path = root / item["relative_path"]
        pilot.reject_link(path)
        if not path.resolve(strict=True).is_relative_to(root):
            raise ValueError("Overlay-set input escapes project")
        pilot.check_identity(pilot.file_identity(path), item, "Overlay-set input")
    previous = json.loads((root / config["inventory_profile"]["relative_path"]).read_bytes())
    known = json.loads((root / config["inventory_report"]["relative_path"]).read_bytes())
    if (previous["status"] != "frozen_before_inventory"
            or known["status"] != "OVERLAY_PREFIX_INVENTORY_COMPLETE"
            or known["profile_sha256"] != config["inventory_profile"]["sha256"]
            or known["coverage"]["known_descriptor_header_coverage_complete"] is not True
            or len(known["overlays"]) != config["expected_overlay_count"]
            or known["full_overlay_payloads_recovered"] != 0):
        raise ValueError("Frozen inventory does not describe the complete reviewed known set")
    indexes = [item["archive_index"] for item in known["overlays"]]
    if indexes != sorted(set(indexes)):
        raise ValueError("Known overlay indexes are duplicated or out of order")
    for item in known["overlays"]:
        if (item["encoding"] not in ("raw", "deobfuscated")
                or not 64 <= item["stored_length"] <= MAX_PAYLOAD
                or item["stored_length"] % 4):
            raise ValueError("Known image has unsupported encoding or complete length")
    for item in inventory.local_items(previous):
        path = root / item["relative_path"]
        pilot.reject_link(path)
        pilot.check_identity(pilot.file_identity(path), item, "Inherited overlay lock")
    lock = json.loads((root / previous["reference_lock"]["relative_path"]).read_bytes())
    old_pilot = json.loads((root / previous["pilot_lock"]["relative_path"]).read_bytes())
    return previous, known, lock, old_pilot


def recover_overlay_set(iso_path, output_dir, *, root=ROOT, config_path=None, report_path=None):
    root = Path(root).resolve(strict=True)
    config_path = Path(config_path) if config_path else root / "config/overlay-set-recovery.json"
    pilot.reject_link(config_path)
    config_bytes = config_path.read_bytes()
    config = json.loads(config_bytes)
    previous, known, lock, old_pilot = verify_inputs(root, config)
    output_parent = root / config["output_parent_relative_path"]
    pilot.reject_link(output_parent)
    if not output_parent.resolve().is_relative_to(root / "reference"):
        raise ValueError("Recovered game bytes must stay in the private reference area")
    output_dir = Path(output_dir)
    pilot.reject_link(output_dir)
    if (output_dir.parent.resolve() != output_parent.resolve()
            or not re.fullmatch(r"[A-Za-z0-9_-]+", output_dir.name) or output_dir.exists()):
        raise ValueError("Choose a fresh named directory directly inside the reviewed output area")
    iso_path = Path(iso_path)
    pilot.reject_link(iso_path)
    iso_path = iso_path.resolve(strict=True)
    elf_path = root / lock["decrypted_executable"]["relative_path"]
    protected = {iso_path, elf_path.resolve(), config_path.resolve(),
                 *[(root / item["relative_path"]).resolve() for item in local_items(config)],
                 *[(root / item["relative_path"]).resolve() for item in inventory.local_items(previous)]}
    if report_path is not None:
        report_path = Path(report_path)
        pilot.reject_link(report_path)
        if (report_path.resolve() in protected or report_path.exists()
                or report_path.resolve().is_relative_to(output_dir.resolve())):
            raise ValueError("Overlay-set report aliases input/output or existing evidence")
    # This reproduces the bounded inventory and all original multi-checksum
    # locks, including the decoder/table/directory relationships, without writes.
    fresh = inventory.inventory_overlays(iso_path, root=root,
        config_path=root / config["inventory_profile"]["relative_path"], report_path=None)
    if fresh != known:
        raise ValueError("Fresh prefix inventory differs from the frozen known set")
    pilot.reject_link(elf_path)
    elf_data = elf_path.read_bytes()
    pilot.check_identity(pilot.identity(elf_data), lock["decrypted_executable"], "Recovery ELF")
    elf = pilot.Elf32(elf_data)
    table_pin = old_pilot["decode_table"]
    table = elf.region(table_pin["elf_offset"], table_pin["size"])
    pilot.check_identity(pilot.identity(table), table_pin, "Recovery decode table")
    archive = known["archive"]
    before = iso_path.stat()
    output_parent.mkdir(parents=True, exist_ok=True)
    for path in (output_parent, *output_parent.parents):
        pilot.reject_link(path)
        if path == root:
            break
    report = {"schema_version": 1, "status": "KNOWN_OVERLAY_SET_RECOVERED",
              "scope": "original known overlay images; no source reconstruction or runtime",
              "profile_sha256": hashlib.sha256(config_bytes).hexdigest(),
              "inventory_sha256": config["inventory_report"]["sha256"],
              "reference_sha256": lock["sha256"], "elf_sha256": lock["decrypted_executable"]["sha256"],
              "modules": [], "matched_progress": 0, "runtime_tested": False,
              "complete_game_code_inventory_established": False}
    movie_seen = 0
    with tempfile.TemporaryDirectory(prefix=".overlay-set-", dir=output_parent) as temporary:
        stage = Path(temporary).resolve(strict=True)
        if not stage.is_relative_to(output_parent.resolve()) or stage.parent != output_parent.resolve():
            raise ValueError("Overlay staging directory escaped the private output area")
        with iso_path.open("rb") as stream:
            for item in known["overlays"]:
                number, length = item["archive_index"], item["stored_length"]
                entry = known["entries"][number]
                encoded = pilot.read_extent(stream, archive["lba"] * pilot.BLOCK,
                    archive["size"], entry["block"] * pilot.BLOCK, length)
                payload = pilot.decode(encoded, entry["block"], table) if item["encoding"] == "deobfuscated" else encoded
                header = inventory.parse_header(payload[:64], len(payload))
                relationships = inventory.associations(header, length, elf)
                if (payload[:64].hex() != item["header_bytes_hex"] or header != item["header"]
                        or relationships != {key:item[key] for key in relationships}):
                    raise ValueError("Recovered image header or original associations changed")
                if number == old_pilot["overlay"]["archive_index"]:
                    pilot.check_identity(pilot.identity(encoded), old_pilot["overlay"]["encrypted"], "Movie pilot encoded bytes")
                    pilot.check_identity(pilot.identity(payload), old_pilot["overlay"]["decoded"], "Movie pilot decoded bytes")
                    movie_seen += 1
                filename = f"entry-{number:04d}-{header['name']}.mwo"
                destination = stage / filename
                if destination.exists() or destination.parent != stage:
                    raise ValueError("Recovered overlay filename collision")
                destination.write_bytes(payload)
                row = {"archive_index": number, "relative_path": filename,
                       "encoding": item["encoding"], "encoded": pilot.identity(encoded),
                       "decoded": pilot.identity(payload), "header": header,
                       "code": pilot.identity(payload[64:64 + header["code_size"]]),
                       "data": pilot.identity(payload[64 + header["code_size"]:]),
                       "bss_size": header["bss_size"], "descriptor_candidates": item["descriptor_candidates"],
                       "reservation_candidates": item["reservation_candidates"],
                       "raw_address_span": observe_address_span(header, payload)}
                pilot.check_identity(pilot.file_identity(destination), row["decoded"], "Staged overlay")
                report["modules"].append(row)
        if len(report["modules"]) != config["expected_overlay_count"] or movie_seen != 1:
            raise ValueError("Complete known set or mandatory movie control is missing")
        report["recovered_overlay_count"] = len(report["modules"])
        report["total_stored_bytes"] = sum(row["decoded"]["size"] for row in report["modules"])
        report["movie_pilot_full_identity_reproduced"] = True
        manifest = stage / "manifest.json"
        pilot.write_report(manifest, report)
        manifest_bytes = manifest.read_bytes()
        expected_manifest = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
        if manifest_bytes != expected_manifest:
            raise ValueError("Staged manifest differs from the verified report")
        # Check all original data and metadata again before any publication.
        verify_inputs(root, config)
        pilot.reject_link(iso_path)
        pilot.check_identity(pilot.file_identity(iso_path), lock, "ISO after complete recovery")
        after = iso_path.stat()
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            raise ValueError("ISO changed during complete recovery")
        pilot.reject_link(elf_path)
        pilot.reject_link(config_path)
        if elf_path.read_bytes() != elf_data or config_path.read_bytes() != config_bytes:
            raise ValueError("ELF or recovery profile changed during recovery")
        for row in report["modules"]:
            path = stage / row["relative_path"]
            pilot.reject_link(path)
            pilot.check_identity(pilot.file_identity(path), row["decoded"], "Final staged overlay")
        pilot.reject_link(stage)
        pilot.reject_link(manifest)
        if manifest.read_bytes() != manifest_bytes:
            raise ValueError("Staged manifest changed before publication")
        expected_names = {row["relative_path"] for row in report["modules"]} | {"manifest.json"}
        if {path.name for path in stage.iterdir()} != expected_names:
            raise ValueError("Staged overlay set has undeclared files")
        for path in (output_parent, *output_parent.parents):
            pilot.reject_link(path)
            if path == root:
                break
        if stage.resolve().parent != output_parent.resolve() or output_dir.parent.resolve() != output_parent.resolve():
            raise ValueError("Overlay publication directory changed")
        pilot.reject_link(output_dir)
        pilot.reject_link(stage)
        pilot.reject_link(manifest)
        if not stage.is_dir() or not manifest.is_file():
            raise ValueError("Staged set or manifest has the wrong file type")
        if output_dir.exists():
            raise ValueError("Output appeared during recovery; preserve it")
        # Same-parent rename publishes the complete verified set with its manifest.
        stage.rename(output_dir)
    if report_path is not None:
        pilot.write_report(report_path, report)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iso", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report = recover_overlay_set(args.iso, args.out_dir, report_path=args.report)
        print(json.dumps({"status":report["status"], "count":report["recovered_overlay_count"],
                          "total_stored_bytes":report["total_stored_bytes"], "output":str(args.out_dir)}))
        return 0
    except (OSError, ValueError, KeyError, TypeError, struct.error) as error:
        print("OVERLAY SET RECOVERY FAILED: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

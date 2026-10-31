"""Reference-preparation checks using tiny synthetic ISO/ELF inputs only.

These exercise input identity, tool failures and publication behavior. They are
not the future 18 negative checks for the matching build gate.
"""

import hashlib
import io
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from scripts import prepare_reference as prep


SECTOR = 2048


def make_sfo():
    """Create explicit game identity metadata without any game-derived bytes."""
    values = [("TITLE", "Synthetic Game"), ("DISC_ID", "TEST00001"),
              ("DISC_VERSION", "1.02")]
    keys = bytearray()
    payload = bytearray()
    records = bytearray()
    for key, value in values:
        raw = value.encode("utf-8") + b"\0"
        records += struct.pack("<HHIII", len(keys), 0x204,
                               len(raw), len(raw), len(payload))
        keys += key.encode("ascii") + b"\0"
        payload += raw
    key_start = 20 + len(records)
    return (struct.pack("<4s4I", b"\0PSF", 0x101, key_start,
                        key_start + len(keys), len(values))
            + records + keys + payload)


def directory_record(lba, size, name, directory=False):
    """Build a directory entry containing independent endian field copies."""
    record = bytearray(33 + len(name) + (len(name) % 2 == 0))
    record[0] = len(record)
    struct.pack_into("<I", record, 2, lba)
    struct.pack_into(">I", record, 6, lba)
    struct.pack_into("<I", record, 10, size)
    struct.pack_into(">I", record, 14, size)
    record[25] = 2 if directory else 0
    record[32] = len(name)
    record[33:33 + len(name)] = name
    return record


def make_iso(encrypted):
    """Create a complete minimal PSP_GAME/SYSDIR fixture tree."""
    image = bytearray(24 * SECTOR)
    pvd = 16 * SECTOR
    image[pvd:pvd + 7] = b"\x01CD001\x01"
    image[pvd + 8:pvd + 40] = b"PSP GAME".ljust(32)
    struct.pack_into("<I", image, pvd + 80, 24)
    struct.pack_into(">I", image, pvd + 84, 24)
    struct.pack_into("<H", image, pvd + 128, SECTOR)
    struct.pack_into(">H", image, pvd + 130, SECTOR)
    root = directory_record(18, SECTOR, b"\0", True)
    image[pvd + 156:pvd + 156 + len(root)] = root
    root_entries = (root + directory_record(18, SECTOR, b"\1", True)
                    + directory_record(19, SECTOR, b"PSP_GAME", True))
    game_entries = (directory_record(19, SECTOR, b"\0", True)
                    + directory_record(18, SECTOR, b"\1", True)
                    + directory_record(20, SECTOR, b"SYSDIR", True)
                    + directory_record(21, len(make_sfo()), b"PARAM.SFO"))
    sysdir_entries = (directory_record(20, SECTOR, b"\0", True)
                      + directory_record(19, SECTOR, b"\1", True)
                      + directory_record(22, len(encrypted), b"EBOOT.BIN"))
    for lba, data in ((18, root_entries), (19, game_entries),
                      (20, sysdir_entries), (21, make_sfo()), (22, encrypted)):
        image[lba * SECTOR:lba * SECTOR + len(data)] = data
    return bytes(image)


def make_plain_elf():
    """Create a bounded MIPS executable with only a section-name table."""
    image = bytearray(160)
    names = b"\0.shstrtab\0"
    ident = b"\x7fELF\x01\x01\x01" + bytes(9)
    struct.pack_into("<16sHHIIIIIHHHHHH", image, 0, ident, 2, 8, 1,
                     0, 0, 64, 0, 52, 0, 0, 40, 2, 1)
    struct.pack_into("<10I", image, 104, 1, 3, 0, 0, 144, len(names), 0, 0, 1, 0)
    image[144:144 + len(names)] = names
    return bytes(image)


def identity(data):
    return {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}


class PrepareReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.iso = self.root / "synthetic.iso"
        self.output = self.root / "reference"
        self.helper = self.root / "synthetic-helper"
        self.lock_path = self.root / "reference.json"
        self.helper_lock_path = self.root / "helpers.json"
        self.encrypted = b"~PSP" + bytes(332)
        self.plain = make_plain_elf()
        self.iso.write_bytes(make_iso(self.encrypted))
        self.helper.write_bytes(b"synthetic helper identity")
        self.lock = {
            "schema_version": 1, "status": "active",
            "baseline_selected_by_user": True,
            **identity(self.iso.read_bytes()),
            "disc_id": "TEST00001", "disc_version": "1.02",
            "title": "Synthetic Game",
            "executable": {"iso_path": "/PSP_GAME/SYSDIR/EBOOT.BIN",
                           **identity(self.encrypted)},
            "decrypted_executable": {"relative_path": "reference/EBOOT.ELF",
                                     **identity(self.plain)},
        }
        self.helper_lock = {
            "schema_version": 1,
            "pspdecrypt": {"relative_path": "unused-for-synthetic-test",
                           "sha256": identity(self.helper.read_bytes())["sha256"],
                           "git_commit": "synthetic", "source_url": "synthetic"},
        }
        self.save_locks()
        self.real_runner = prep.run_decryptor
        self.run_mock = mock.patch.object(prep, "run_decryptor", side_effect=self.good_helper)
        self.decrypt = self.run_mock.start()
        self.addCleanup(self.run_mock.stop)

    def save_locks(self):
        self.lock_path.write_text(json.dumps(self.lock), encoding="utf-8")
        self.helper_lock_path.write_text(json.dumps(self.helper_lock), encoding="utf-8")

    def good_helper(self, helper, source, destination, **kwargs):
        self.assertEqual(Path(source).read_bytes(), self.encrypted)
        Path(destination).write_bytes(self.plain)
        return {"returncode": 0, "stdout": "synthetic success", "stderr": "",
                "command": ["synthetic-helper"]}

    def prepare(self):
        return prep.prepare_reference(
            self.iso, self.output, lock_path=self.lock_path,
            helper_lock_path=self.helper_lock_path, helper_path=self.helper,
            timeout=2, wsl_distro="Ubuntu"
        )

    def assert_unpublished(self):
        self.assertFalse((self.output / "EBOOT.BIN").exists())
        self.assertFalse((self.output / "EBOOT.ELF").exists())

    def test_success_preserves_image_and_publishes_verified_artifacts(self):
        before = self.iso.read_bytes()
        report = self.prepare()
        self.assertEqual((self.output / "EBOOT.BIN").read_bytes(), self.encrypted)
        self.assertEqual((self.output / "EBOOT.ELF").read_bytes(), self.plain)
        self.assertEqual(self.iso.read_bytes(), before)
        self.assertIsInstance(report, dict)
        json.dumps(report)  # Evidence must be serializable without embedded bytes.

    def test_repeat_run_really_decrypts_again_with_identical_result(self):
        first = self.prepare()
        second = self.prepare()
        self.assertEqual(self.decrypt.call_count, 2)
        self.assertEqual(first, second)
        self.assertEqual((self.output / "EBOOT.ELF").read_bytes(), self.plain)

    def test_inactive_or_unselected_baseline_fails_before_tool_execution(self):
        for change in ({"status": "rejected_by_user"}, {"baseline_selected_by_user": False}):
            with self.subTest(change=change):
                original = self.lock.copy()
                self.lock.update(change)
                self.save_locks()
                with self.assertRaises(ValueError):
                    self.prepare()
                self.assert_unpublished()
                self.decrypt.assert_not_called()
                self.lock = original

    def test_full_image_hash_mismatch_fails_before_tool_execution(self):
        data = bytearray(self.iso.read_bytes())
        data[-1] ^= 1
        self.iso.write_bytes(data)
        with self.assertRaises(ValueError):
            self.prepare()
        self.decrypt.assert_not_called()
        self.assert_unpublished()

    def test_executable_hash_mismatch_fails_before_tool_execution(self):
        self.lock["executable"]["sha256"] = "0" * 64
        self.save_locks()
        with self.assertRaises(ValueError):
            self.prepare()
        self.decrypt.assert_not_called()
        self.assert_unpublished()

    def test_metadata_identity_mismatch_fails(self):
        self.lock["disc_id"] = "WRONG0001"
        self.save_locks()
        with self.assertRaises(ValueError):
            self.prepare()
        self.decrypt.assert_not_called()
        self.assert_unpublished()

    def test_missing_helper_fails_before_tool_execution(self):
        self.helper.unlink()
        with self.assertRaises((ValueError, OSError)):
            self.prepare()
        self.decrypt.assert_not_called()
        self.assert_unpublished()

    def test_tampered_helper_fails_before_tool_execution(self):
        self.helper.write_bytes(b"changed tool")
        with self.assertRaises(ValueError):
            self.prepare()
        self.decrypt.assert_not_called()
        self.assert_unpublished()

    def test_nonzero_helper_result_never_publishes(self):
        self.decrypt.side_effect = lambda *a, **k: {
            "returncode": 1, "stdout": "", "stderr": "synthetic failure", "command": []}
        with self.assertRaises(ValueError):
            self.prepare()
        self.assert_unpublished()

    def test_helper_timeout_never_publishes(self):
        self.decrypt.side_effect = subprocess.TimeoutExpired("synthetic-helper", 2)
        with self.assertRaises(ValueError):
            self.prepare()
        self.assert_unpublished()

    def test_success_exit_without_output_never_publishes(self):
        self.decrypt.side_effect = lambda *a, **k: {
            "returncode": 0, "stdout": "", "stderr": "", "command": []}
        with self.assertRaises((ValueError, OSError)):
            self.prepare()
        self.assert_unpublished()

    def test_wrong_decrypted_hash_never_publishes(self):
        def bad_helper(helper, source, destination, **kwargs):
            data = bytearray(self.plain)
            data[-1] ^= 1
            Path(destination).write_bytes(data)
            return {"returncode": 0, "stdout": "", "stderr": "", "command": []}
        self.decrypt.side_effect = bad_helper
        with self.assertRaises(ValueError):
            self.prepare()
        self.assert_unpublished()

    def test_hash_pinned_malformed_elf_never_publishes(self):
        self.plain = b"not an ELF executable"
        self.lock["decrypted_executable"].update(identity(self.plain))
        self.save_locks()
        with self.assertRaises(ValueError):
            self.prepare()
        self.assert_unpublished()

    def test_helper_cannot_change_staged_encrypted_input_silently(self):
        def modifies_input(helper, source, destination, **kwargs):
            result = self.good_helper(helper, source, destination, **kwargs)
            Path(source).write_bytes(b"changed staged input")
            return result
        self.decrypt.side_effect = modifies_input
        with self.assertRaises(ValueError):
            self.prepare()
        self.assert_unpublished()

    def test_helper_identity_is_rechecked_after_execution(self):
        def modifies_helper(helper, source, destination, **kwargs):
            result = self.good_helper(helper, source, destination, **kwargs)
            Path(helper).write_bytes(b"changed helper")
            return result
        self.decrypt.side_effect = modifies_helper
        with self.assertRaises(ValueError):
            self.prepare()
        self.assert_unpublished()

    def test_relocatable_elf_is_not_accepted_as_executable(self):
        data = bytearray(self.plain)
        struct.pack_into("<H", data, 16, 1)
        self.plain = bytes(data)
        self.lock["decrypted_executable"].update(identity(self.plain))
        self.save_locks()
        with self.assertRaises(ValueError):
            self.prepare()
        self.assert_unpublished()

    def test_existing_bad_artifact_is_preserved_and_rejected(self):
        self.output.mkdir()
        existing = self.output / "EBOOT.BIN"
        existing.write_bytes(b"existing evidence")
        with self.assertRaises(ValueError):
            self.prepare()
        self.assertEqual(existing.read_bytes(), b"existing evidence")
        self.assertFalse((self.output / "EBOOT.ELF").exists())

    def test_failed_repeat_preserves_previously_verified_outputs(self):
        self.prepare()
        self.decrypt.side_effect = subprocess.TimeoutExpired("synthetic-helper", 2)
        with self.assertRaises(ValueError):
            self.prepare()
        self.assertEqual((self.output / "EBOOT.BIN").read_bytes(), self.encrypted)
        self.assertEqual((self.output / "EBOOT.ELF").read_bytes(), self.plain)

    def test_cli_image_mismatch_produces_no_report_or_artifacts(self):
        self.lock["sha256"] = "0" * 64
        self.save_locks()
        report = self.root / "report.json"
        script = Path(__file__).resolve().parents[1] / "scripts/prepare_reference.py"
        result = subprocess.run(
            [sys.executable, str(script), "--iso", str(self.iso),
             "--out-dir", str(self.output), "--report", str(report),
             "--lock", str(self.lock_path), "--helper-lock", str(self.helper_lock_path),
             "--helper-path", str(self.helper)],
            capture_output=True, text=True, timeout=10
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(report.exists())
        self.assert_unpublished()

    def cli_arguments(self, report):
        return ["--iso", str(self.iso), "--out-dir", str(self.output),
                "--report", str(report), "--lock", str(self.lock_path),
                "--helper-lock", str(self.helper_lock_path),
                "--helper-path", str(self.helper)]

    def test_cli_report_cannot_alias_original_image(self):
        original = self.iso.read_bytes()
        with mock.patch("sys.stderr", new_callable=io.StringIO) as errors:
            self.assertNotEqual(prep.main(self.cli_arguments(self.iso)), 0)
        self.assertIn("aliases", errors.getvalue())
        self.assertEqual(self.iso.read_bytes(), original)
        self.decrypt.assert_not_called()
        self.assert_unpublished()

    def test_cli_preserves_a_different_existing_report(self):
        report = self.root / "report.json"
        report.write_text("existing evidence", encoding="utf-8")
        with mock.patch("sys.stderr", new_callable=io.StringIO):
            self.assertNotEqual(prep.main(self.cli_arguments(report)), 0)
        self.assertEqual(report.read_text(encoding="utf-8"), "existing evidence")

    def test_runner_uses_empty_stdin_and_bounded_subprocess_calls(self):
        calls = []

        def fake_run(command, **kwargs):
            calls.append((command, kwargs))
            if "wslpath" in command:
                return subprocess.CompletedProcess(command, 0, "/synthetic/path\n", "")
            return subprocess.CompletedProcess(command, 7, "output", "failed")

        with mock.patch.object(prep.subprocess, "run", side_effect=fake_run):
            result = self.real_runner(self.helper, self.iso, self.root / "out.elf",
                                      timeout=2, wsl_distro="Ubuntu")
        self.assertEqual(result["returncode"], 7)
        self.assertTrue(calls)
        for command, kwargs in calls:
            self.assertEqual(kwargs["stdin"], subprocess.DEVNULL)
            self.assertGreater(kwargs["timeout"], 0)
            self.assertLessEqual(kwargs["timeout"], 7)

    def test_runner_does_not_swallow_subprocess_timeout(self):
        with mock.patch.object(prep.subprocess, "run", side_effect=subprocess.TimeoutExpired("fixture", 2)):
            with self.assertRaises(subprocess.TimeoutExpired):
                self.real_runner(self.helper, self.iso, self.root / "out.elf",
                                 timeout=2, wsl_distro="Ubuntu")


if __name__ == "__main__":
    unittest.main()

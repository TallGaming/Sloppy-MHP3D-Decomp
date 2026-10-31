"""Invented help-transport observations; no compiler/debugger is launched."""

import ast
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from scripts import probe_compiler_transport as tool
from scripts import inspect_compiler_trace as trace
from tests import test_compiler_trace_feasibility as invented


class TransportObservationTests(unittest.TestCase):
    def setUp(self):
        self.profile = {"entry_va": 0x401000, "guest_cs": 7, "image_base": 0x400000,
            "text": {"identity": tool.identity(b"\x55" + b"\x90" * 63)},
            "markers": [{"va": 0x402000 + i * 32,
                         "identity": tool.identity(("Invented stage " + str(i)).encode() + b"\0")}
                        for i in range(3)],
            "ordinary_help_identity": tool.identity(b"Invented compiler help\n")}
        self.observation = {"entry": {"pc": 0x401000, "cs": 7, "esp": 0x70001000,
            "ebp": 0xA1B2C3D4, "hardware_breakpoint_stop": True,
            "text": self.profile["text"]["identity"], "text_bytes_equal": True,
            "entry_byte": 0x55, "markers": [{"va": x["va"], "identity": x["identity"],
                "bytes_equal": True} for x in self.profile["markers"]]},
            "step": {"pc": 0x401001, "cs": 7, "esp": 0x70000FFC,
                "single_step_stop": True, "saved_ebp": 0xA1B2C3D4, "saved_ebp_size": 4},
            "errors": [], "unexpected_signals": [], "exit_codes": [0]}
        self.ordinary = {"returncode": 0, "timed_out": False,
            "stdout": self.profile["ordinary_help_identity"], "stderr": tool.identity(b"")}
        self.debugger = dict(self.ordinary, stdout=tool.identity(b"Debugger envelope\nInvented compiler help\n"))

    def reasons(self, observation=None):
        return tool.validate_observation(self.observation if observation is None else observation, self.profile)

    def test_exact_section_markers_stack_effect_and_normal_completion_are_accepted(self):
        self.assertEqual(tool.validate_entry(self.observation["entry"], self.profile), [])
        self.assertEqual(self.reasons(), [])
        self.assertEqual(tool.validate_trial(self.observation, self.profile,
            self.ordinary, self.debugger, True, True), [])
        # The separately declared contract does not pretend that old PE-header
        # requirements passed: header bytes are recorded but are not its identity.
        self.observation["header_prefix_hex"] = "00" * 16
        self.assertEqual(self.reasons(), [])

    def test_matching_entry_byte_does_not_substitute_for_complete_text_identity(self):
        for identity, equal in ((tool.identity(b"\x55" + b"\x90" * 62 + b"\x91"), True),
                                (tool.identity(b"\x55"), True),
                                (self.profile["text"]["identity"], False)):
            obs = copy.deepcopy(self.observation)
            obs["entry"].update(text=identity, text_bytes_equal=equal)
            self.assertTrue(self.reasons(obs))
        self.assertEqual(self.observation["entry"]["entry_byte"], 0x55)

    def test_all_three_complete_ordered_nul_strings_and_addresses_are_required(self):
        for change in ("missing", "reordered", "address", "bytes", "hash", "length"):
            obs = copy.deepcopy(self.observation); markers = obs["entry"]["markers"]
            if change == "missing": markers.pop()
            elif change == "reordered": markers.reverse()
            elif change == "address": markers[1]["va"] += 4
            elif change == "bytes": markers[2]["bytes_equal"] = False
            elif change == "hash": markers[0]["identity"]["sha256"] = "0" * 64
            else: markers[0]["identity"]["size"] -= 1
            with self.subTest(change=change): self.assertTrue(self.reasons(obs))

    def test_entry_requires_hardware_stop_exact_pc_cs_and_guest_width_registers(self):
        for key, value in (("hardware_breakpoint_stop", False), ("pc", 0x401001), ("cs", 0x33),
                           ("pc", float(0x401000)), ("cs", 7.0), ("entry_byte", 0x90),
                           ("esp", -1), ("esp", 0x100000000), ("esp", True),
                           ("ebp", -1), ("ebp", 0x100000000), ("ebp", None)):
            obs = copy.deepcopy(self.observation); obs["entry"][key] = value
            with self.subTest(key=key, value=value): self.assertTrue(self.reasons(obs))
        for obs in (None, {}, {"entry": None}, dict(self.observation, step=None)):
            self.assertTrue(self.reasons(obs) if obs is not None else tool.validate_observation(None, self.profile))

    def test_single_step_rejects_eight_byte_push_wrong_stops_width_and_saved_word(self):
        for key, value in (("single_step_stop", False), ("pc", 0x401000), ("pc", 0x401002),
                           ("cs", 0x33), ("esp", 0x70000FF8), ("esp", 0x170000FFC),
                           ("saved_ebp", 0xD4C3B2A1), ("saved_ebp", 0x1A1B2C3D4),
                           ("saved_ebp_size", 8), ("saved_ebp_size", 4.0)):
            obs = copy.deepcopy(self.observation); obs["step"][key] = value
            with self.subTest(key=key, value=value): self.assertTrue(self.reasons(obs))
        obs = copy.deepcopy(self.observation)
        obs["entry"]["esp"] = 2; obs["step"]["esp"] = 0xFFFFFFFE
        self.assertTrue(self.reasons(obs))
        obs = copy.deepcopy(self.observation)
        obs["entry"]["ebp"] = 1; obs["step"]["saved_ebp"] = True
        self.assertTrue(self.reasons(obs))

    def test_errors_signals_missing_or_multiple_exit_events_cannot_be_success(self):
        for key, value in (("errors", ["unreadable memory"]), ("errors", None),
                           ("unexpected_signals", ["SIGSEGV"]), ("unexpected_signals", None),
                           ("exit_codes", []), ("exit_codes", [None]),
                           ("exit_codes", [1]), ("exit_codes", [0, 0])):
            obs = copy.deepcopy(self.observation); obs[key] = value
            with self.subTest(key=key, value=value): self.assertTrue(self.reasons(obs))

    def test_completion_timeout_diagnostics_help_and_tool_integrity_are_independent(self):
        for label in ("ordinary", "debugger"):
            for key, value in (("returncode", -9), ("returncode", 1), ("timed_out", True),
                               ("timed_out", None), ("stderr", tool.identity(b"warning"))):
                ordinary, debugger = copy.deepcopy(self.ordinary), copy.deepcopy(self.debugger)
                (ordinary if label == "ordinary" else debugger)[key] = value
                with self.subTest(label=label, key=key, value=value):
                    self.assertTrue(tool.validate_trial(self.observation, self.profile,
                        ordinary, debugger, True, True))
        ordinary = dict(self.ordinary, stdout=tool.identity(b"Invented compiler help"))
        self.assertTrue(tool.validate_trial(self.observation, self.profile, ordinary, self.debugger, True, True))
        for contained, unchanged in ((False, True), (True, False)):
            self.assertTrue(tool.validate_trial(self.observation, self.profile,
                self.ordinary, self.debugger, contained, unchanged))


class FrozenTransportTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup); self.root = Path(temp.name)
        self.required = ["scripts/probe_compiler_transport.py", "config/compiler-transport.json",
                         "scripts/inspect_compiler_trace.py", "tests/test_compiler_transport.py"]
        self.freeze = {"both_final_pre_execution_reviews_received": True, "frozen_inputs": []}
        for relative in self.required:
            p = self.root / relative; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(b"invented frozen bytes")
        self.update_freeze()
        self.freeze_path = self.root / "freeze.json"

    def update_freeze(self):
        self.freeze["frozen_inputs"] = [{"path": n, **tool.identity((self.root / n).read_bytes())}
                                        for n in self.required]

    def test_freeze_requires_exact_input_set_two_reviews_and_unchanged_bytes(self):
        tool.verify_frozen(self.root, self.freeze)
        for mutation in ("missing", "duplicate", "extra", "reviews", "bytes"):
            changed = copy.deepcopy(self.freeze)
            if mutation == "missing": changed["frozen_inputs"].pop()
            elif mutation == "duplicate": changed["frozen_inputs"][0] = changed["frozen_inputs"][1]
            elif mutation == "extra": changed["frozen_inputs"].append({"path": "unexpected"})
            elif mutation == "reviews": changed["both_final_pre_execution_reviews_received"] = False
            else: (self.root / self.required[2]).write_bytes(b"different bytes")
            with self.subTest(mutation=mutation), self.assertRaises(ValueError): tool.verify_frozen(self.root, changed)

    def make_profile(self):
        raw, unused = invented.fixture(); raw[invented.TEXT] = 0x55
        compiler = self.root / "compiler.exe"; compiler.write_bytes(raw)
        others = []
        for name in ("wibo", "gdb"):
            p = self.root / name; p.write_bytes(b"invented non-executable tool"); others.append(p)
        profile = {"entry_va": 0x401000, "image_base": 0x400000, "guest_cs": 7,
            "text": {"file_offset": invented.TEXT, "va": 0x401000,
                     "identity": tool.identity(bytes(raw[invented.TEXT:invented.TEXT + 0x200]))},
            "markers": [], "tools": [{"path": p.name, "identity": tool.identity(p.read_bytes())}
                                      for p in [compiler, *others]], "timeout_seconds": 30}
        return profile

    def save_profile(self, profile):
        (self.root / "config/compiler-transport.json").write_text(json.dumps(profile))
        self.update_freeze(); self.freeze_path.write_text(json.dumps(self.freeze))

    def test_static_pe_mapping_and_tool_pins_fail_before_any_process_launch(self):
        original = self.make_profile()
        for change in ("base", "entry", "text_mapping", "text_hash", "tool"):
            profile = copy.deepcopy(original)
            if change == "base": profile["image_base"] += 0x1000
            elif change == "entry": profile["entry_va"] += 1
            elif change == "text_mapping": profile["text"]["va"] += 4
            elif change == "text_hash": profile["text"]["identity"]["sha256"] = "0" * 64
            else: profile["tools"][0]["identity"]["sha256"] = "0" * 64
            self.save_profile(profile)
            with self.subTest(change=change), mock.patch.dict(sys.modules, {"inspect_compiler_trace": trace}), \
                    mock.patch.object(tool.subprocess, "Popen") as launch:
                with self.assertRaises(ValueError): tool.run_trial(self.root, 1, self.freeze_path)
                launch.assert_not_called()

    def test_optimized_python_still_rejects_wrong_mapping_without_running_tools(self):
        profile = self.make_profile(); profile["text"]["va"] += 4; self.save_profile(profile)
        scripts = Path(tool.__file__).resolve().parent
        code = "\n".join(["import sys", "from pathlib import Path",
            "sys.path.insert(0, " + repr(str(scripts)) + ")", "import probe_compiler_transport as t",
            "def forbidden(*a, **k): raise RuntimeError('process launch forbidden in this test')",
            "t.subprocess.Popen = forbidden", "try:",
            "    t.run_trial(Path(" + repr(str(self.root)) + "), 1, Path(" + repr(str(self.freeze_path)) + "))",
            "except ValueError as error:", "    print(str(error))", "else:", "    raise RuntimeError('wrong mapping accepted')"])
        result = subprocess.run([sys.executable, "-O", "-c", code], stdin=subprocess.DEVNULL,
                                 capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("text mapping differs", result.stdout)

    def test_generated_gdb_python_blocks_parse_with_quoted_paths_and_only_one_step(self):
        profile = self.make_profile(); profile["markers"] = []
        script = tool.debugger_script(profile, self.root / "compiler's path.exe",
                                      self.root / "quoted directory", self.root)
        blocks = []; current = None
        for line in script.splitlines():
            if line == "python": current = []
            elif line == "end" and current is not None: blocks.append("\n".join(current)); current = None
            elif current is not None: current.append(line)
        self.assertEqual(len(blocks), 2)
        for block in blocks: ast.parse(block)
        self.assertEqual(script.count("gdb.execute('stepi')"), 1)
        self.assertNotIn("set $", script)
        self.assertNotIn("gdb.execute('call", script)


if __name__ == "__main__":
    unittest.main()

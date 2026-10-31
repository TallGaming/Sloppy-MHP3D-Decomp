"""Verify a bounded help-only debugger contract for the pinned PSP compiler.

This never compiles source or executes the game. Historical probe results are
immutable; this tool evaluates a separately reviewed section/stack contract.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile


def identity(data):
    return {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def validate_entry(entry, profile):
    """Return reasons that exact executable identity has not been established."""
    reasons = []
    if not isinstance(entry, dict):
        return ["missing entry observation"]
    if entry.get("hardware_breakpoint_stop") is not True:
        reasons.append("entry was not an identified hardware-breakpoint stop")
    if (type(entry.get("pc")) is not int or type(entry.get("cs")) is not int
            or entry.get("pc") != profile["entry_va"] or entry.get("cs") != profile["guest_cs"]):
        reasons.append("entry PC/CS differs")
    for register in ("esp", "ebp"):
        value = entry.get(register)
        if type(value) is not int or not 0 <= value <= 0xFFFFFFFF:
            reasons.append("unsupported guest register: " + register)
    if entry.get("text") != profile["text"]["identity"] or entry.get("text_bytes_equal") is not True:
        reasons.append("complete file-backed text differs")
    if entry.get("entry_byte") != 0x55:
        reasons.append("entry instruction is not the declared PUSH EBP")
    markers = entry.get("markers")
    expected = [{"va": m["va"], "identity": m["identity"], "bytes_equal": True}
                for m in profile["markers"]]
    if markers != expected:
        reasons.append("selected complete marker strings differ")
    return reasons


def validate_observation(observation, profile):
    """Fail closed unless the exact entry, single step and exit all agree."""
    if not isinstance(observation, dict):
        return ["missing observation"]
    entry = observation.get("entry")
    reasons = validate_entry(entry, profile)
    step = observation.get("step")
    if not isinstance(step, dict):
        reasons.append("missing single-step observation")
    elif isinstance(entry, dict):
        if step.get("single_step_stop") is not True:
            reasons.append("single-step stop not established")
        if (type(step.get("pc")) is not int or type(step.get("cs")) is not int
                or step.get("pc") != profile["entry_va"] + 1 or step.get("cs") != profile["guest_cs"]):
            reasons.append("stepped PC/CS differs")
        esp = entry.get("esp")
        if (type(esp) is not int or esp < 4 or type(step.get("esp")) is not int
                or step.get("esp") != esp - 4):
            reasons.append("PUSH did not decrement the 32-bit stack by four")
        ebp = entry.get("ebp")
        if (type(ebp) is not int or type(step.get("saved_ebp")) is not int
                or type(step.get("saved_ebp_size")) is not int
                or step.get("saved_ebp_size") != 4 or step.get("saved_ebp") != ebp):
            reasons.append("saved four-byte EBP differs")
    if observation.get("errors") != []:
        reasons.append("debugger observation error")
    if observation.get("unexpected_signals") != []:
        reasons.append("unexpected signal")
    if observation.get("exit_codes") != [0]:
        reasons.append("inferior normal exit0 not established")
    return reasons


def validate_trial(observation, profile, ordinary, debugger, output_contained, tools_unchanged):
    """Keep process completion/output/tool identity separate from guest observations."""
    reasons = validate_observation(observation, profile)
    for label, result in (("ordinary", ordinary), ("debugger", debugger)):
        if result.get("returncode") != 0 or result.get("timed_out") is not False:
            reasons.append(label + " invocation did not complete normally")
        if result.get("stderr") != identity(b""):
            reasons.append(label + " invocation emitted diagnostics")
    if ordinary.get("stdout") != profile["ordinary_help_identity"]:
        reasons.append("ordinary help differs from the pinned prior output")
    if output_contained is not True:
        reasons.append("complete ordinary help output absent from debugger output")
    if tools_unchanged is not True:
        reasons.append("tool identity changed")
    return reasons


def verify_frozen(root, freeze):
    records = freeze.get("frozen_inputs")
    required = {"scripts/probe_compiler_transport.py", "config/compiler-transport.json",
                "scripts/inspect_compiler_trace.py", "tests/test_compiler_transport.py"}
    if not isinstance(records, list) or {r.get("path") for r in records} != required or len(records) != 4:
        raise ValueError("Incomplete or unexpected frozen input set")
    for record in records:
        if identity((root / record["path"]).read_bytes()) != {k: record[k] for k in ("size", "sha256")}:
            raise ValueError("Frozen input changed: " + record["path"])
    if freeze.get("both_final_pre_execution_reviews_received") is not True:
        raise ValueError("Missing recorded final reviews")


def debugger_script(profile, compiler, directory, root):
    """Generate fixed read/step/continue commands without arbitrary hook inputs."""
    setup = "\n".join([
        "set pagination off", "set confirm off", "set startup-with-shell off",
        "set disable-randomization off", "python", "import gdb, json, pathlib, sys",
        "sys.path.insert(0, " + repr(str(root / "scripts")) + ")",
        "from probe_compiler_transport import identity, validate_entry",
        "profile = " + repr(profile), "compiler = pathlib.Path(" + repr(str(compiler)) + ")",
        "directory = pathlib.Path(" + repr(str(directory)) + ")",
        "observation = {'errors': [], 'unexpected_signals': [], 'exit_codes': [], 'stops': []}",
        "def stopped(event):",
        "    item = {'type': type(event).__name__}",
        "    if hasattr(event, 'stop_signal'):",
        "        item['signal'] = event.stop_signal",
        "        if event.stop_signal != 'SIGTRAP': observation['unexpected_signals'].append(event.stop_signal)",
        "    if isinstance(event, gdb.BreakpointEvent):",
        "        item['hardware'] = any(b.type == gdb.BP_HARDWARE_BREAKPOINT for b in event.breakpoints)",
        "    observation['stops'].append(item)",
        "def exited(event): observation['exit_codes'].append(getattr(event, 'exit_code', None))",
        "gdb.events.stop.connect(stopped)", "gdb.events.exited.connect(exited)", "end",
        "starti", "hbreak *0x401000", "continue", "python",
    ])
    body = '''
try:
    inferior = gdb.selected_inferior()
    raw = compiler.read_bytes()
    text = profile['text']
    live = bytes(inferior.read_memory(text['va'], text['identity']['size']))
    expected = raw[text['file_offset']:text['file_offset'] + text['identity']['size']]
    (directory / 'live-text.bin').write_bytes(live)
    entry = {'pc': int(gdb.parse_and_eval('$pc')), 'cs': int(gdb.parse_and_eval('$cs')),
        'esp': int(gdb.parse_and_eval('$esp')), 'ebp': int(gdb.parse_and_eval('$ebp')),
        'hardware_breakpoint_stop': bool(observation['stops'] and observation['stops'][-1].get('hardware')),
        'text': identity(live), 'text_bytes_equal': live == expected,
        'entry_byte': bytes(inferior.read_memory(profile['entry_va'], 1))[0], 'markers': []}
    for marker in profile['markers']:
        value = bytes(inferior.read_memory(marker['va'], marker['identity']['size']))
        expected = raw[marker['file_offset']:marker['file_offset'] + marker['identity']['size']]
        entry['markers'].append({'va': marker['va'], 'identity': identity(value), 'bytes_equal': value == expected})
    observation['entry'] = entry
    observation['header_prefix_hex'] = bytes(inferior.read_memory(profile['image_base'], 16)).hex()
    errors = validate_entry(entry, profile)
    if errors:
        observation['errors'].extend(errors)
    else:
        for breakpoint in gdb.breakpoints() or []: breakpoint.delete()
        before_stops = len(observation['stops'])
        gdb.execute('stepi')
        step = {'pc': int(gdb.parse_and_eval('$pc')), 'cs': int(gdb.parse_and_eval('$cs')),
            'esp': int(gdb.parse_and_eval('$esp')),
            'single_step_stop': len(observation['stops']) == before_stops + 1
                and observation['stops'][-1]['type'] == 'StopEvent'}
        saved = bytes(inferior.read_memory(step['esp'], 4))
        step.update(saved_ebp=int.from_bytes(saved, 'little'), saved_ebp_size=len(saved))
        observation['step'] = step
except Exception as error:
    observation['errors'].append(type(error).__name__ + ': ' + str(error))
finally:
    for breakpoint in gdb.breakpoints() or []: breakpoint.delete()
    (directory / 'observation.json').write_text(json.dumps(observation, indent=2) + '\\n')
try:
    if gdb.selected_inferior().pid:
        gdb.execute('continue')
except Exception as error:
    observation['errors'].append(type(error).__name__ + ': ' + str(error))
(directory / 'observation.json').write_text(json.dumps(observation, indent=2) + '\\n')
end
'''
    return setup + "\n" + body


def run_trial(root, trial, freeze_path):
    freeze = json.loads(freeze_path.read_bytes())
    verify_frozen(root, freeze)
    profile_path = root / "config/compiler-transport.json"
    profile = json.loads(profile_path.read_bytes())
    from inspect_compiler_trace import Pe32
    tools = [(Path(r["path"]) if r["path"].startswith("/") else root / r["path"], r["identity"])
             for r in profile["tools"]]
    for path, expected in tools:
        if identity(path.read_bytes()) != expected:
            raise ValueError("Tool does not match its pin: " + str(path))
    compiler, wibo, gdb = [r[0] for r in tools]
    pe = Pe32(compiler.read_bytes())
    if pe.base != profile["image_base"] or pe.base + pe.entry_rva != profile["entry_va"]:
        raise ValueError("Pinned preferred base/entry mapping differs")
    section = next(s for s in pe.sections if s["name"] == ".text")
    if (section["raw"], pe.base + section["rva"], section["size"]) != (
            profile["text"]["file_offset"], profile["text"]["va"], profile["text"]["identity"]["size"]):
        raise ValueError("Pinned file-backed text mapping differs")
    if identity(pe.data[section["raw"]:section["raw"] + section["size"]]) != profile["text"]["identity"]:
        raise ValueError("Pinned file-backed text identity differs")
    for marker in profile["markers"]:
        rva, unused = pe.file_mapping(marker["file_offset"], marker["identity"]["size"])
        if pe.base + rva != marker["va"]:
            raise ValueError("Pinned marker mapping differs")
        value = pe.data[marker["file_offset"]:marker["file_offset"] + marker["identity"]["size"]]
        if identity(value) != marker["identity"] or not value.endswith(b"\0"):
            raise ValueError("Pinned complete marker identity differs")
    if os.name != "posix":
        raise ValueError("Run only through the existing WSL environment")
    out = root / "evidence/bucket-03u" / ("trial-" + str(trial) + ".json")
    if out.exists():
        raise ValueError("Preserve existing trial output")
    directory = Path(tempfile.mkdtemp(prefix="compiler-transport-", dir=root / "build"))
    command = [str(wibo), str(compiler), "-help"]
    script = debugger_script(profile, compiler, directory, root)
    (directory / "probe.gdb").write_text(script)
    plan = {"trial": trial, "command": command, "directory": str(directory.relative_to(root)),
        "timeout_seconds": profile["timeout_seconds"], "source_compilation": False,
        "freeze": identity(freeze_path.read_bytes()), "profile": identity(profile_path.read_bytes())}
    (directory / "plan.json").write_text(json.dumps(plan, indent=2) + "\n")

    def execute(args, label):
        process = subprocess.Popen(args, cwd=compiler.parent, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        timed_out = False
        try:
            stdout, stderr = process.communicate(timeout=profile["timeout_seconds"])
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
        (directory / (label + ".stdout")).write_bytes(stdout)
        (directory / (label + ".stderr")).write_bytes(stderr)
        return {"returncode": process.returncode, "timed_out": timed_out,
                "stdout": identity(stdout), "stderr": identity(stderr)}, stdout

    ordinary, help_bytes = execute(command, "ordinary")
    debugger, debug_bytes = execute([str(gdb), "-q", "-nx", "-batch", "-x",
                                     str(directory / "probe.gdb"), "--args", *command], "debugger")
    unchanged = all(identity(path.read_bytes()) == expected for path, expected in tools)
    verify_frozen(root, freeze)
    observation_path = directory / "observation.json"
    observation = json.loads(observation_path.read_bytes()) if observation_path.exists() else {}
    contained = bool(help_bytes) and help_bytes in debug_bytes
    reasons = validate_trial(observation, profile, ordinary, debugger, contained, unchanged)
    result = {"status": "VERIFIED_BOUNDED_TRANSPORT" if not reasons else "INCONCLUSIVE",
        "reasons": reasons, "plan": plan, "ordinary": ordinary, "debugger": debugger,
        "observation": observation, "complete_help_output_contained": contained,
        "tools_unchanged": unchanged, "source_compiled": False, "game_executed": False,
        "optimizer_hook_validated": False, "object_neutrality_tested": False}
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "reasons": reasons, "build": plan["directory"]}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trial", type=int, choices=(1, 2), required=True)
    parser.add_argument("--freeze", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    run_trial(root, args.trial, args.freeze.resolve())


if __name__ == "__main__":
    main()

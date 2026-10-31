> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bounded compiler debugger transport

Bucket 3U completed both fresh trials successfully; see `BUCKET_03U_CHECKPOINT.md`.
It evaluates a new help-only contract for the unchanged MW219 compiler,
standalone wibo and native host GDB. It preserves the earlier 3M result as
INCONCLUSIVE: that earlier contract required live PE headers which the runner
does not copy. No historical criterion is lowered after execution.

The new profile is `config/compiler-transport.json`; the driver is
`scripts/probe_compiler_transport.py`. Before either live trial, both helpers
review the exact inputs, meaningful rejection tests pass, and a separate
`evidence/bucket-03u/profile-freeze.json` records their acknowledgments and the
final script/profile/parser/test identities. The driver refuses drift from that
input set. Execute only through the existing WSL environment:

```powershell
wsl -d Ubuntu -- python3 <project-root>/scripts/probe_compiler_transport.py --trial 1 --freeze <project-root>/evidence/bucket-03u/profile-freeze.json
wsl -d Ubuntu -- python3 <project-root>/scripts/probe_compiler_transport.py --trial 2 --freeze <project-root>/evidence/bucket-03u/profile-freeze.json
```

Each declared trial creates a fresh private build directory. Ordinary help is
compared with its complete historical 31,584-byte output. GDB starts the runner,
sets a hardware breakpoint at preferred compiler entry `0x00401000`, and reads
the complete 1,702,912 file-backed `.text` bytes. It requires exact bytes, without
masking relocations or changing the base. Three separately mapped diagnostic
strings include their terminating NUL bytes. All compiler/runner/debugger file
identities must hold before and after; static checks use explicit exceptions
and cannot disappear under optimized Python.

Only after entry identity succeeds does the script delete the breakpoint and
single-step the known first byte `0x55`, PUSH EBP. It requires PC to advance by
one, ESP to decrease by four and four bytes at the new stack pointer to equal
the preceding EBP value. The predeclared guest CS selector must remain seven.
This is a narrow empirical check of that instruction's observed guest width;
GDB's host architecture label and the CS number alone do not establish it.

The script then continues with GDB's default signal policy. Each invocation is
bounded to thirty seconds, with process-group termination on timeout. Positive
status also requires one explicit inferior exit code zero, normal debugger and
ordinary-process exits, no errors/unexpected signals/diagnostic stderr, and the
complete ordinary help output appearing in debugger output. Unsupported stops
or observations remain INCONCLUSIVE; existing outputs cannot be overwritten.

Results are `evidence/bucket-03u/trial-1.json` and `trial-2.json`; their fresh
build directories retain the generated GDB script, plan, full live text dump,
observation and process stdout/stderr. The independent reviews are
`COMPILER_TRANSPORT_IDENTITY_REVIEW.md` and `BUCKET_03U_VALIDATION_NOTES.md`.

This contract does not compile source, produce or compare an object, identify
an optimizer hook, decode IR, choose a historical game compiler or count a match.
A later invented-fixture compilation trace would need another reviewed scope
and complete ordinary-versus-debugger object equality before neutrality claims.
The parked archive routine and every existing toolchain/source profile remain
unchanged.

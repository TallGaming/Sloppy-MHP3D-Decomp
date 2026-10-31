> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Invented arithmetic capability review — Bucket 3AM

This is an invented-only capability experiment. It contains no original game
source compilation, target comparison, profile lock or matching credit. Existing
game diagnostic flags, the new advance method's one source attempt, and the parked
initializer's counters remain unchanged.

## Help and setting provenance

The retained `evidence/mwccpsp-219-help.txt` and catalogue copy
`evidence/bucket-03/mwccpsp_3.0.1_219-help.txt` are byte-identical: 31,584 bytes,
SHA256 `539587cda84463e05efa58667977ee77a81ac8238f03b3ac0d09cf05be248ce6`.
The header identifies build 219 and runtime date 2006-08-24. The existing catalogue
binds that exact help hash to compiler SHA256
`828f9b30b3ae33c7a0202c2baf48aab49884c60e48c5b3daa2436bc3237368df`
and its original archive/support DLL. This is retained invocation provenance,
not evidence of Capcom's original compiler or whole-program settings.

Using LF-separated lines in the raw file, help lines 351–381 describe the eight
already declared investigation settings. Default has no optimization argument;
it must remain separate from explicit O0 even though help says optimization is
off by default. O3 adds scheduling, tail calls, loop-invariant motion, strength
reduction and dead-store elimination; O4 expands earlier optimizations and its
short spelling also enables intrinsics. The p/s variants request speed/space.
These statements describe documented capabilities, not guaranteed output patterns.

| Setting | Exact setting arguments |
| --- | --- |
| default | empty list |
| O0 | -O0 |
| O1 | -O1 |
| O2 | -O2 |
| O3 | -O3 |
| O4 | -O4 |
| O4-p | -O4,p |
| O4-s | -O4,s |

The lists must equal `config/compiler-candidates.json` in order. Common flags
remain the already validated C++ `-nostdinc -lang c++ -c`, with the same MW219,
wibo, DLL and staged `compile_profile` behavior. Every setting applies to both
whole invented translation units. None is selected for a game function here.

## Fixtures and complete controls

The new arithmetic unit contains three named extern-C scalar functions, avoiding
C++ name inference. Two compute unsigned remainders with different divisors; the
third deliberately wraps a 32-bit product before taking its remainder. A compile-
time width check enforces the assumed unsigned width. There is no receiver,
volatile field, assembly, pointer alias trick or original target body.

The other complete unit is the unchanged invented `address_reuse_grouped.cpp`.
Its established O2 whole objects at `build/address-reuse-o2mm0k1m/grouped.o` and
`build/address-reuse-8e3b12xv/grouped.o` are both 768 bytes, SHA256
`775c998a2213ab73a0458f44dc6357336afe8fea2d9b2e30f90d637e4fed101c`.
The initial producer control is the complete 6,528-byte MW219 C++/O2 object,
SHA256 `406ea0e4105f271d4e6f81d142393d22e3b59b72542a0ed15ebe3bf6b85b004f`,
from both 3W trials. These controls include all object metadata, not just code.
Source basename, extension, pipeline and flags must remain unchanged for parity.

The existing `scripts/bench_address_reuse.py` is 16,286 bytes, SHA256
`5aefa4160aa2ad40aa114b1d696b085b98edd73a606bee56d983a88f4e7dcf99`.
Its `inspect_address_fixture` takes the raw object, exact symbol
`initialize_key__17ArchiveKeyContextFUi` and offsets 106784/106788. It first
validates the whole function, then calls the bounded whitelist address checker.
Unsupported control flow, receiver-address construction or access paths remain
UNINTERPRETED, with no materialization count. Existing O2 counts do not justify
assuming the same interpretation for O0/O3/O4.

## Primary instruction encoding evidence

The PSPDEV binutils opcode table is pinned at commit
`1bf9b3f9be9d82cc89374ca916cd4e8e6115dcf8`. Its exact cached text is 284,523 bytes,
SHA256 `d1b8d1d0617cc730ffb164aa6b3c594238f251207e8da64097ba4175d82ccc8b`;
the source manifest is `evidence/bucket-03am/helper-map-primary-sources.json`.
[Primary opcode table](https://github.com/pspdev/binutils-gdb/blob/1bf9b3f9be9d82cc89374ca916cd4e8e6115dcf8/opcodes/mips-opc.c#L1599)
labels the Allegrex form with AL, defined as INSN_ALLEGREX at line 414.

| Encoding observation | Mask | Expected masked word |
| --- | --- | --- |
| DIVU z,s,t | fc00ffff | 0000001b |
| MULT s,t | fc00ffff | 00000018 |
| MULTU s,t | fc00ffff | 00000019 |
| MFHI d | ffff07ff | 00000010 |
| MFLO d | ffff07ff | 00000012 |
| Allegrex MSUB s,t | fc00ffff | 0000002e |

The generic MIPS32 MSUB form at the next table entries is 70000004 under the same
fc00ffff mask. It must not silently replace the Allegrex encoding test. Record
any independently supported extra encoding separately. Pseudoinstruction names
and macro table entries are not instruction-word matches.

Counts apply only to complete validated function words, retaining each raw word
and byte offset. They measure static sites, not executed operations or proved
reciprocal dataflow. Absence of MSUB in a tiny invented fixture cannot establish
a compiler-family limitation; its presence cannot attribute original game code.

## Execution review pending

The exact new controller/profile and invented selection controls still require
independent review and freeze before any compilation. Final output audit will
separately record all settings, unsupported outcomes, repeat objects and controls.

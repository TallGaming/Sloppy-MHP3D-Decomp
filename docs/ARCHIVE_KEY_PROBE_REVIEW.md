> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Archive-key initializer review

Bucket 3I. This independent review uses the pinned ELF and existing static
disassembly, plus the previously pinned public MHP2G source. It invokes no
compiler, linker or game. The selected routine is the seed initializer at
`0x0886233C`, not the later key-update routine at `0x08862700`.

## Target boundary and behavior

The accepted ELF remains 2247320 bytes, SHA-256
`755e5d84262c3bb30635b32deffab11a66de118f501e4ac105f503308be8b950`.
The complete selected interval is **[0x0886233C, 0x08862380)**, 68 bytes,
SHA-256 `7d089e6e2131eb950e3d72ee437c4aab2ec4a775e0baf8c4d45901cb227cee57`.
No padding, preceding getter, or following function is included.

Boundary evidence from `evidence/eboot-v102.disasm.txt`, independently checked
against executable-section instruction words in the ELF:

| Evidence | Address/detail |
| --- | --- |
| Preceding independent routine | Starts `0x0886232C`; returns at `0x08862334`, NOP delay slot at `0x08862338`. |
| Selected entry | `0x0886233C`, independently targeted by three direct calls and one tail jump. |
| Internal branches | `0x08862354 → 0x08862364`; `0x08862368 → 0x08862378`, both with NOP delay slots. |
| Complete return | `jr ra` at `0x08862378`, NOP delay slot at `0x0886237C`. |
| Next independent prologue | `0x08862380` allocates a stack frame and saves the return address. |

A scan of allocated executable PROGBITS sections found direct JAL instructions
at `0x088631F4`, `0x088639EC` and `0x08863B28`, and a direct tail J at
`0x08863C54`, all targeting the selected entry. No external direct branch/jump
to an interior instruction was found. This is a bounded static scan, not proof
that indirect entry paths cannot exist.

The first argument in `a0` is a base pointer; `a1` supplies the seed. The routine
temporarily adds `0x30000` to the base and uses signed displacements, producing
these actual record offsets:

| Operation | Offset from original base | Width/value |
| --- | --- | --- |
| Initial upper store | `0x2F540` | 32-bit word, logical seed shift right by 16. |
| Initial lower store | `0x2F53C` | 32-bit word, seed masked with `0xFFFF`. |
| Zero lower replacement | `0x2F53C` | 32-bit word `0x7F8D`. |
| Upper reload / zero replacement | `0x2F540` | 32-bit word load, then replacement with `0x2345` if zero. |

Both fields hold values in `1..65535` afterward. They are not halfword fields:
the observed loads/stores are word operations. The high-half extraction is
logical, not signed. Zero halves are replaced independently; seed zero sets
both defaults. A null base is not checked. The routine makes no calls; the
inspected callers do not consume a return value, consistent with a void setter.
That does not recover the original prototype.

At `0x088631F4` the caller explicitly supplies seed zero. Other callers derive
a seed from an archive byte position divided by the 2048-byte block size, with
signed adjustment in two contexts. All pass an object-like base pointer in
`a0`; the tail caller restores its frame before jumping. This is consistent
with a hidden C++ receiver or an explicit C record pointer. It does not prove
the original class, inheritance, vtable layout or SDK ownership.

## Public counterpart and type limits

[MHP2G FileSys::set_decryption_key](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/src/eboot/file_sys.cpp#L266)
uses the same split and constants. Its
[declaration](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/include/file_sys.hpp#L48)
marks both fields `volatile u32`. That is a public reconstruction choice for
a different game; its field layout and original-source status do not transfer.

MHP3's upper reload after its stores is compatible with volatile/thread-visible
state, but does not uniquely establish that qualifier. Intermediate store order
also differs from the public source's textual order. The one candidate must
record its type/qualifier hypotheses before compilation; observed target bytes
must not be used to iterate source shapes afterward.

## Candidate preflight

Before outputs, the primary declared a single nonvirtual partial-record C++
candidate with unknown prefix bytes and two volatile 32-bit fields at the verified
offsets. Its natural method retains the masked low half in a local, writes
upper then lower, handles the zero low half from that local, and tests the
upper field through memory before its default. This follows the target's
observed access sequence without inventing a low-field reload or a vtable.
The volatility qualifier and member-method presentation remain hypotheses.

That decision was reviewed before compilation; no source-shape change was
requested. Exact source/layout preflight approved:

| Input | Bytes | SHA-256 |
| --- | --- | --- |
| `bench/archive_key_initializer.cpp` | 1806 | `6c4be341bcc3f113b56ccf7494a7b624a550b52f89c9c827eacbbce56e1f71d3` |
| `config/archive-key-probe.json` | 883 | `bcb2a3b159f2ce1f3d6fba2ff9f2d668dade818efab8d79bb4fe6656846bea84` |
| `bench/archive_key_naming.cpp` | 364 | `ba25728588ef85085ccf3c51647f741c17bddbe147e6823e5a654546f7c937c2` |

The source defines no bases or virtual members; its unknown byte prefix length
`0x2F53C` is divisible by four. Under the pinned 32-bit ABI the following two
word members occupy the verified offsets. Scalar-width/partial-extent checks
generate no functions and make no full-object-size claim. The invented naming
fixture exercises the same class/method/unsigned-argument signature with an
unrelated body and no target layout.

The invented 672-byte naming object has SHA-256
`d06c4baa5b3c3b49a0c8ed3013df07aea97ac6d093a541d8ab57b62d3ea41ab4`.
Independent parsing finds exactly one complete 16-byte function,
`initialize_key__17ArchiveKeyContextFUi`. The 701-byte naming evidence has SHA-256
`7be69cc48816970a39de0c9880b1f7a94f5ef4dae1d74ee02babec720affd9d3`.
This observation preceded target compilation and supplies the exact raw lookup
name; no name is inferred from target similarity.

Final pre-target review approved the 1901-byte draft
`config/archive-key-experiment.json`, SHA-256
`27f5ea2d60a5c8760eb8f35b683d6bfe5ef448e9f66b90f1dc482d6757e142f1`,
and `scripts/bench_archive_key.py`, SHA-256
`30c4b8d9fa18e7eac32b18e3defb86e103cb58996fe9cfb10f33d19b3a7f8535`.
The compiler command is unchanged from the inherited C++ diagnostic profile:

```text
mwccpsp.exe -nostdinc -lang c++ -c -O2 -o {fresh-candidate-object} {frozen-source}
```

It uses the same pinned unmodified compiler, wibo and bounded execution. The
single exact-symbol association passes through the inherited strict comparator;
missing/extra functions, unsupported code relocations or incomplete executable
words reject the configuration. No ELF record is renamed or rewritten. The
runner checks new and inherited pins before/after compilation, retains failed
outcomes and rejects changed emitted-object bytes before reporting.

The final 1902-byte profile has SHA-256
`30b5372dab0d1e2fb9dc0ec4436ca0e78af1922728c5a421499a66e2a4cc5188`.
Replacing only its freeze-status value reconstructs the exact reviewed draft
digest above. `evidence/bucket-03i/profile-freeze.json` records both independent
reviews before target compilation.

## Final repeated results

Both `evidence/bucket-03i/archive-key-run-1.json` and
`evidence/bucket-03i/archive-key-run-2.json` are 1154 bytes, SHA-256
`e937d49b28b94694f7fa8b1c67db88a8c229ec1394f903a03cb6cc4815509e59`.
They are byte-identical and report complete valid comparison, **not exact**:
100 compiled bytes versus 68 target bytes, first differing byte at offset zero.

The reviewer independently rehashed/reparsed both final objects under
`build/archive-key-probe-h53umlmt` and `build/archive-key-probe-btnq7jgt`,
reapplied the exact raw symbol association and strict whole-function comparator,
and checked target/function hashes and empty diagnostic logs. Each object is
768 bytes, SHA-256
`1d715acabd4cdec572d40c1905504881a396fa5e11296f1163533b30941d7796`.
Each contains exactly one complete 100-byte function with SHA-256
`193c361fab07498ef61aa22bfa4c417f10bfbfcd0cdb8bd50a591f7838aad2da`.
There are no unresolved code relocations. Both retain flags `0x10970001` and
comment `MW MIPS C Compiler (3.0.0)`. Source and runner hashes remain unchanged.

Read-only disassembly with the existing GNU objdump identifies the principal
code-generation difference:

| Property | Target | Frozen candidate output |
| --- | --- | --- |
| Large receiver-base adjustment | One LUI/ADDU pair, retained in adjusted `a0`. | Recomputed before each of five field accesses. |
| Base-adjustment pairs | 1 | 5; the four extra pairs account for 32 extra bytes. |
| Initial scheduling | Adjust base, extract high, mask low. | Mask low, extract high, adjust base. |
| Registers and branch distances | Low seed half in `a1`; internal branch displacements 3 words. | Low half in `a2`; branch displacements 5 words around repeated address calculations. |
| Ordered word accesses | Upper store, lower store, optional low default, upper reload, optional upper default. | Same observed sequence and constants. |

Neither the qualifier hypothesis nor the original class/language is established
by this result. The difference does not isolate a compiler version, a compiler
option, aliasing rules or missing translation-unit context as the cause. No
source alternative, flag change, trick or further compiler invocation followed
the result. This was one frozen diagnostic candidate, not integrated game
source; exact-probe count and game matching credit both remain zero for it.
No runtime behavior was tested. Stop at the review checkpoint.

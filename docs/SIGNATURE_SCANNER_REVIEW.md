> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Signature-scanner source review — paused

Public source review was paused for the user's GitHub preparation priority before
installing or executing any scanner. No game bytes were uploaded. This is a partial
source audit, not a signature scan or a completed database-coverage assessment.

The official Detect-It-Easy tree was read at commit
`adc0617abd4d35e7449c767f62cf6ae276c67762`; its nontruncated GitHub tree listed 49
files in db/ELF. No claim about all rule contents follows from filenames alone.

[ELF MWCC rule](https://github.com/horsicq/Detect-It-Easy/blob/adc0617abd4d35e7449c767f62cf6ae276c67762/db/ELF/compiler_MWCC.4.sg)
searches only the .comment section for `MW MIPS C Compiler`, extracts the version
from parentheses and sets language C. It contains no MIPS code signature. Therefore
that rule would repeat our existing banner evidence; its language label cannot
recover the source language of every linked function or establish the historical
compiler build/configuration.

[ELF GCC rule](https://github.com/horsicq/Detect-It-Easy/blob/adc0617abd4d35e7449c767f62cf6ae276c67762/db/ELF/compiler_gcc.4.sg)
contains mostly x86 entry signatures, a PowerPC entry pattern, and string/section
fallbacks including GCC: in .comment, gcc2_compiled., GCC_3.0 and .gcc_except_table.
A linked runtime or library can supply metadata; a rule hit needs the exact matched
rule/location before any attribution. PSP/MIPS-specific code coverage and SNC
coverage were not established in this interrupted review.

[PE CodeWarrior rule](https://github.com/horsicq/Detect-It-Easy/blob/adc0617abd4d35e7449c767f62cf6ae276c67762/db/PE/protector_Metrowerks_CodeWarrior.2.sg)
uses PE x86 entry bytes and labels a protector. It is not an ELF/MIPS producer
signature. PEiD is not a reason to wrap or reinterpret PSP inputs as PE.

Only public text was read. No scanner implementation, binary, database execution,
repository/game setting change, signature hit or toolchain lock resulted.

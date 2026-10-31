> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# PSPDEV resources: scope and current evidence

The user's October31 resource suggestion is a research lead, not an instruction
to replace the matching toolchain or adopt another game engine. The historical
compiler remains unlocked. Building new PSP software and reproducing the exact
original executable are different acceptance requirements.

Already investigated locally: PSP GCC packages1.3.1 and1.7.1 (both contain
GCC3.3.3 Allegrex frontends), and Minimalist PSPSDK0.10.0 containing GCC4.3.5.
See `GNU_ASSEMBLY_PROVENANCE.md`, `PSP_GCC435_CANDIDATE.md` and the frozen
compiler-family profiles. The complete fourteen-probe fixed C++ comparison in
Bucket3AB yielded one exact body for each GNU candidate, without identifying the
original whole-game pipeline. PSPSDK's module-info definition was also used as
a public format reference in the separately reviewed PSP metadata work.

The current [PSPDEV repository](https://github.com/pspdev/pspdev) assembles an
open-source PSP development environment. Its [PSPSDK documentation](https://pspdev.github.io/pspsdk/)
describes OS headers/stubs, startup support and graphics/audio libraries. These
are useful API and file-format references. They do not prove that Capcom built
this title with the present open-source compiler or startup libraries.

[psp-pacman](https://github.com/pspdev/psp-pacman) manages packages in a PSPDEV
installation. This specific resource was checked in response to the suggestion;
there was no earlier documented package-manager audit. Additional homebrew
libraries do not resolve the current compiler/code-generation uncertainty. No
package installation, dependency version or platform backend is selected here.

[GameBrew's PSP PC utilities directory](https://www.gamebrew.org/wiki/List_of_PSP_PC_utilities)
was likewise checked now. It lists SDKs, development utilities and engines,
including Stardust and openTri. Relevant extraction or format utilities may be
examined as leads, then checked against primary source and our original bytes.
Replacing the original game engine is outside the matching-first objective.
No listed engine, tool binary or runtime was installed or executed for this review.

Keep the existing reference, frozen game compiler diagnostics, assembly/library
rules and matching-before-port decision unchanged. A future modern PSPDEV
installation would need its own explicit purpose and version pin; it would not
silently become the historical matching configuration.

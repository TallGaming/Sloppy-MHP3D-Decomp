/* Invented bare layout for metadata provenance; not a game linker script.
 * Every compiler input uses this exact layout. Keep compiler metadata visible.
 */
ENTRY(family_smoke)
SECTIONS
{
    .text 0x08804000 : { *(.text) *(.text.*) }
    .data : { *(.data) *(.data.*) *(.sdata) *(.rodata) *(.rodata.*) }
    .bss : { *(.bss) *(.bss.*) *(.sbss) *(COMMON) }
    .reginfo : { *(.reginfo) }
    .MIPS.abiflags : { *(.MIPS.abiflags) }
    .comment 0 : { *(.comment) }
    .pdr 0 : { *(.pdr) }
    .mdebug.eabi32 0 : { *(.mdebug.eabi32) }
    .gnu.attributes 0 : { *(.gnu.attributes) }
    .mwcats 0 : { *(.mwcats) }
}

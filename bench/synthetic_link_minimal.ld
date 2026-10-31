/* Invented SNC-only layout: preserve its four input payload sections.
 * This is a diagnostic layout, not a reconstruction of the game's layout.
 */
ENTRY(family_smoke)
SECTIONS
{
    .text 0x08804000 : { *(.text) }
    .rodata : { *(.rodata) }
    .data : { *(.data) }
    .reginfo 0 : { *(.reginfo) }
}

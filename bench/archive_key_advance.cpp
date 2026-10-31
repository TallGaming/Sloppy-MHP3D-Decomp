/*
 * Advance the two archive-key states and return the next XOR word.
 *
 * Diagnostic for PSP ULJM05800 v1.02, [0x08862700, 0x0886278C).
 * The multiply/modulus arithmetic and field offsets are independently reviewed.
 * The receiver's full class and field qualifiers remain unknown. This first
 * plain hypothesis uses ordinary unsigned fields so the compiler may retain
 * results and reorder independent accesses, as the original routine does.
 *
 * This file is not linked into the game and grants no matching credit.
 */

typedef unsigned char u8;
typedef unsigned int u32;

/* Preserve the known offsets without inventing the preceding class members. */
struct ArchiveKeyAdvanceContext {
    u8 unknown_00000[0x2F53C];
    u32 key_lower;
    u32 key_upper;

    u32 next_key();
};

/* Update both halves with wrapping 32-bit products before packing the result. */
u32 ArchiveKeyAdvanceContext::next_key()
{
    // Each state uses its own multiplier and modulus.
    key_lower = (key_lower * 0x7F8Du) % 0xFFF1u;
    key_upper = (key_upper * 0x2345u) % 0xFFD9u;

    // Both reduced values fit in 16 bits.
    return (key_upper << 16) + key_lower;
}

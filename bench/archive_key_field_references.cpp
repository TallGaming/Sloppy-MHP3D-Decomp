/* Archive-key diagnostic: one counted matching-only shape after plain attempts.
 * Source hypothesis4, matching-shape attempt1. Original class/volatility remain
 * hypotheses. PSP target: 0x0886233C..0x08862380 (exclusive end).
 */
typedef unsigned int u32;
typedef unsigned char u8;

struct ArchiveKeyContext {
    u8 unknown_000000[0x2F53C];
    volatile u32 key_lower;
    volatile u32 key_upper;
    void initialize_key(u32 seed);
};

typedef char WordWidth[(sizeof(u32) == 4) ? 1 : -1];
typedef char ObservedExtent[(sizeof(ArchiveKeyContext) == 0x2F544) ? 1 : -1];

/* Split the block seed into two key states, substituting nonzero defaults.
 * MATCHING SHAPE (counted): bind both volatile field references before stores
 * to test whether their addresses survive across writes without rematerializing
 * the receiver base. These aliases add no field read and preserve access order.
 * They are retained for this code-generation test, not claimed as original code.
 */
void ArchiveKeyContext::initialize_key(u32 seed)
{
    volatile u32& lower = key_lower;
    volatile u32& upper = key_upper;
    const u32 lower_half = seed & 0xFFFFu;
    upper = seed >> 16;
    lower = lower_half;
    if (lower_half == 0) {
        lower = 0x7F8Du;
    }
    if (upper == 0) {
        upper = 0x2345u;
    }
}

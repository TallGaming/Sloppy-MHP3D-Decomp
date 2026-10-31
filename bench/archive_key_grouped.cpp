/* Archive-key initialization hypothesis, grouped record diagnostic (attempt2).
 * This is a preserved source copy, not integrated game code. The original
 * class, record nesting and volatility remain hypotheses. Observed target:
 * PSP ULJM05800 v1.02, 0x0886233C..0x08862380 (exclusive end).
 */
typedef unsigned int u32;
typedef unsigned char u8;

struct ArchiveKeyState {
    volatile u32 lower;
    volatile u32 upper;
};

struct ArchiveKeyContext {
    u8 unknown_000000[0x2F53C];
    ArchiveKeyState key_state;
    void initialize_key(u32 seed);
};

/* Describe only the known scalar width and the hypothesized partial extent. */
typedef char WordWidth[(sizeof(u32) == 4) ? 1 : -1];
typedef char KeyExtent[(sizeof(ArchiveKeyState) == 8) ? 1 : -1];
typedef char ObservedExtent[(sizeof(ArchiveKeyContext) == 0x2F544) ? 1 : -1];

/* Split the block seed into two states and replace zero halves with defaults.
 * Preserve the upper-then-lower volatile stores, the low-half local test and
 * the later upper-state reload. Grouping is the only change from attempt1.
 */
void ArchiveKeyContext::initialize_key(u32 seed)
{
    const u32 lower_half = seed & 0xFFFFu;
    key_state.upper = seed >> 16;
    key_state.lower = lower_half;
    if (lower_half == 0) {
        key_state.lower = 0x7F8Du;
    }
    if (key_state.upper == 0) {
        key_state.upper = 0x2345u;
    }
}

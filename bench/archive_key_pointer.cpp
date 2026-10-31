/* Archive-key initialization hypothesis, named record pointer (attempt3).
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
 * Name the grouped record pointer, as tested in the invented 3O fixture.
 * Keep every volatile access and value in the grouped attempt2's order.
 */
void ArchiveKeyContext::initialize_key(u32 seed)
{
    ArchiveKeyState* state = &key_state;
    const u32 lower_half = seed & 0xFFFFu;
    state->upper = seed >> 16;
    state->lower = lower_half;
    if (lower_half == 0) {
        state->lower = 0x7F8Du;
    }
    if (state->upper == 0) {
        state->upper = 0x2345u;
    }
}

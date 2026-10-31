/* Invented address-reuse fixture: the same fields grouped in one subobject.
 * The offsets and defaults are artificial. This is not another game candidate.
 * The owner/method spelling reuses a previously validated naming signature only.
 */
typedef unsigned int u32;
typedef unsigned char u8;

struct KeyState {
    volatile u32 lower;
    volatile u32 upper;
};

struct ArchiveKeyContext {
    u8 invented_prefix[0x1A120];
    KeyState state;
    void initialize_key(u32 seed);
};

/* The grouping adds no virtual members or padding between the two words. */
typedef char WordWidth[(sizeof(u32) == 4) ? 1 : -1];
typedef char StateExtent[(sizeof(KeyState) == 8) ? 1 : -1];
typedef char RecordExtent[(sizeof(ArchiveKeyContext) == 0x1A128) ? 1 : -1];

/* Use the subobject directly: no cached reference, pointer or helper is added.
 * Volatile access order and all values remain the same as the direct fixture.
 */
void ArchiveKeyContext::initialize_key(u32 seed)
{
    const u32 lower_half = seed & 0xFFFFu;
    state.upper = seed >> 16;
    state.lower = lower_half;
    if (lower_half == 0) {
        state.lower = 0x1357u;
    }
    if (state.upper == 0) {
        state.upper = 0x2468u;
    }
}

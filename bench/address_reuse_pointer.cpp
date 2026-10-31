/* Invented address-reuse fixture: explicitly name the grouped subobject pointer.
 * Offsets and defaults are artificial; this is not another game candidate.
 * Compared with the grouped control, only the access expression is factored.
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

/* Retain the grouped control's scalar width and exact partial layout. */
typedef char WordWidth[(sizeof(u32) == 4) ? 1 : -1];
typedef char StateExtent[(sizeof(KeyState) == 8) ? 1 : -1];
typedef char RecordExtent[(sizeof(ArchiveKeyContext) == 0x1A128) ? 1 : -1];

/* Test whether naming this pointer preserves a shared field-address base.
 * All volatile reads/writes, constants and their order match the grouped form.
 * No register choice, barrier or additional observable operation is requested.
 */
void ArchiveKeyContext::initialize_key(u32 seed)
{
    KeyState* key_state = &state;
    const u32 lower_half = seed & 0xFFFFu;
    key_state->upper = seed >> 16;
    key_state->lower = lower_half;
    if (lower_half == 0) {
        key_state->lower = 0x1357u;
    }
    if (key_state->upper == 0) {
        key_state->upper = 0x2468u;
    }
}

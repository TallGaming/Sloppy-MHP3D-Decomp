/* Invented address-reuse fixture: direct fields in a large record.
 * The offsets and defaults are artificial. This is not another game candidate.
 * The owner/method spelling reuses a previously validated naming signature only.
 */
typedef unsigned int u32;
typedef unsigned char u8;

struct ArchiveKeyContext {
    u8 invented_prefix[0x1A120];
    volatile u32 lower;
    volatile u32 upper;
    void initialize_key(u32 seed);
};

/* Record order plus four-byte alignment puts the fields at 0x1A120/0x1A124. */
typedef char WordWidth[(sizeof(u32) == 4) ? 1 : -1];
typedef char RecordExtent[(sizeof(ArchiveKeyContext) == 0x1A128) ? 1 : -1];

/* Preserve upper write, lower write, optional lower default, upper read and
 * optional upper default. Both fixtures use this same volatile access order.
 */
void ArchiveKeyContext::initialize_key(u32 seed)
{
    const u32 lower_half = seed & 0xFFFFu;
    upper = seed >> 16;
    lower = lower_half;
    if (lower_half == 0) {
        lower = 0x1357u;
    }
    if (upper == 0) {
        upper = 0x2468u;
    }
}

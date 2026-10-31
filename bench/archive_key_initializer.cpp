/* Archive-key initialization hypothesis for PSP ULJM05800 v1.02.
 * This diagnostic candidate is not integrated game source. The routine's
 * complete observed body is 0x0886233C..0x08862380 (exclusive end).
 */

typedef unsigned int u32;
typedef unsigned char u8;

/* Only the two observed fields are described. The receiver's original class,
 * earlier members, inheritance and total object size are unknown.
 */
struct ArchiveKeyContext {
    u8 unknown_000000[0x2F53C];

    /* Volatility is a hypothesis supported by the target's upper-state reload
     * and the related MHP2G declarations. It does not prove synchronization or
     * permit importing that game's different receiver layout.
     */
    volatile u32 key_lower;  /* Observed 32-bit stores at receiver + 0x2F53C. */
    volatile u32 key_upper;  /* Observed stores/reload at receiver + 0x2F540. */

    void initialize_key(u32 seed);
};

/* These checks document the assumed scalar width and partial record extent;
 * they generate no function code and do not claim the full game object size.
 */
typedef char ArchiveKeyWordMustBeFourBytes[(sizeof(u32) == 4) ? 1 : -1];
typedef char ArchiveKeyObservedExtent[(sizeof(ArchiveKeyContext) == 0x2F544) ? 1 : -1];

/* Split an archive-block seed into two key states and replace zero halves with
 * their observed nonzero defaults. Preserve the observed upper-then-lower
 * writes. The low zero test uses the seed half without rereading key_lower;
 * the high zero test reads key_upper again, as the target does.
 */
void ArchiveKeyContext::initialize_key(u32 seed)
{
    const u32 lower_half = seed & 0xFFFFu;

    key_upper = seed >> 16;
    key_lower = lower_half;
    if (lower_half == 0) {
        key_lower = 0x7F8Du;
    }
    if (key_upper == 0) {
        key_upper = 0x2345u;
    }
}

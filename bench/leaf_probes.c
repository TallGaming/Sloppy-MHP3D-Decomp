/*
 * Initial compiler-identification probes for ULJM05800 v1.02.
 *
 * These plain-C drafts describe small called blocks in the executable. Function
 * boundaries, signatures and game/library ownership remain provisional. They
 * exercise byte access, pointer advancement, masking and field stores, but are
 * too small to identify a compiler build alone. They are not integrated game
 * source and must never be included in matched-progress totals.
 */

typedef unsigned char u8;
typedef unsigned int u32;

/* Return whether the pointed-to byte is nonzero; the containing type is unknown. */
int probe_0883C4F8(const u8 *value)
{
    return *value != 0;
}

/* Clear one byte; the field's meaning and containing type are unknown. */
void probe_0883C508(u8 *value)
{
    *value = 0;
}

/* Copy one byte and return the next input position, as a byte reader would. */
const u8 *probe_08826448(const u8 *input, u8 *output)
{
    *output = *input;
    return input + 1;
}

/* A provisional record preserves observed field offsets without guessed names. */
typedef struct ProbeRecord {
    u8 unknown_000[0x188];
    u8 field_188;
    u8 field_189;
    u8 unknown_18A[2];
    u32 field_18C;
} ProbeRecord;

/* Clear the three observed fields; their game-level purpose remains unknown. */
void probe_0885691C(ProbeRecord *record)
{
    record->field_18C = 0;
    record->field_188 = 0;
    record->field_189 = 0;
}

/* Set the observed byte field to one; this does not establish its meaning. */
void probe_0885697C(ProbeRecord *record)
{
    record->field_189 = 1;
}

/* Return the observed constant; this trivial probe cannot distinguish builds. */
u32 probe_08856A14(void)
{
    return 128;
}

/* The first argument is unresolved; retain the observed second-argument ABI. */
u32 probe_0885BBFC(void *unknown, u32 value)
{
    return (u8)(value - 5);
}

typedef struct ProbeByteRecord {
    u8 unknown_000[0x78];
    u8 field_078;
} ProbeByteRecord;

/* Read the byte at offset 0x78 without guessing its role or signedness. */
u32 probe_08860C9C(const ProbeByteRecord *record)
{
    return record->field_078;
}

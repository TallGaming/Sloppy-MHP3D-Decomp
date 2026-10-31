/*
 * Fixed plain-C compiler-investigation probes for PSP ULJM05800 v1.02.
 * These are behavioral hypotheses for bounded, directly called code intervals.
 * They are not integrated game source, original signatures, library attribution,
 * or matched-progress credit. Keep this source fixed across candidate settings.
 * Unknown record fields preserve observed offsets without inventing game names.
 */

typedef signed char s8;
typedef unsigned char u8;
typedef signed short s16;
typedef unsigned short u16;
typedef unsigned int u32;

/* Return whether the pointed-to byte is nonzero; its game meaning is unknown. */
int probe_0883C4F8(const u8 *value)
{
    return *value != 0;
}

/* Clear one byte; the original containing type is unknown. */
void probe_0883C508(u8 *value)
{
    *value = 0;
}

/* Copy one byte and return the next input position. */
const u8 *probe_08826448(const u8 *input, u8 *output)
{
    *output = *input;
    return input + 1;
}

typedef struct ProbeRecord {
    u8 unknown_000[0x188];
    u8 field_188;
    u8 field_189;
    u8 unknown_18A[2];
    u32 field_18C;
} ProbeRecord;

/* Clear the three observed fields; their application-level purpose is unknown. */
void probe_0885691C(ProbeRecord *record)
{
    record->field_18C = 0;
    record->field_188 = 0;
    record->field_189 = 0;
}

/* Set the observed byte field to one. */
void probe_0885697C(ProbeRecord *record)
{
    record->field_189 = 1;
}

/* Return the observed constant; this is only a low-information control. */
u32 probe_08856A14(void)
{
    return 128;
}

/* Subtract five and keep the low byte; the unused first argument is unresolved. */
u32 probe_0885BBFC(void *unknown, u32 value)
{
    return (u8)(value - 5);
}

typedef struct ProbeByteRecord {
    u8 unknown_000[0x78];
    u8 field_078;
} ProbeByteRecord;

/* Return the unsigned byte read from the observed field. */
u32 probe_08860C9C(const ProbeByteRecord *record)
{
    return record->field_078;
}

/* Inspect six bytes and report whether any is nonzero. The target uses signed
 * byte loads; this does not establish the original typedef or array purpose. */
int probe_08830550(const s8 *values)
{
    int found = 0;
    int index;

    for (index = 0; index < 6; ++index) {
        if (*values != 0) {
            found = 1;
        }
        ++values;
    }
    return found;
}

typedef struct ProbeNode {
    struct ProbeNode *next;
} ProbeNode;

/* Count nodes through the pointer at offset zero. This assumes a terminating
 * list; ownership, additional fields and cycle handling are not established. */
u32 probe_08830654(const ProbeNode *node)
{
    u32 count = 0;

    while (node != 0) {
        node = node->next;
        ++count;
    }
    return count;
}

/* Count nonzero 16-bit units before a zero terminator. The first argument is
 * unused by the observed body; no text encoding or original method is assumed. */
u32 probe_0882DA68(void *unknown, const u16 *input)
{
    u32 count = 0;

    while (input[count] != 0) {
        ++count;
    }
    return count;
}

typedef struct ProbeDivisionRecord {
    u8 unknown_000[0x2AB2];
    s16 field_2AB2;
} ProbeDivisionRecord;

/* Return one for a zero field; otherwise divide field-minus-one, add one, and
 * retain a byte. The divisor's valid domain and field meaning are unresolved;
 * ordinary C division describes the observed signed division for nonzero input. */
u32 probe_0883E944(const ProbeDivisionRecord *record, int divisor)
{
    if (record->field_2AB2 == 0) {
        return 1;
    }
    return (u8)((record->field_2AB2 - 1) / divisor + 1);
}

/* Check the observed unsigned address bounds. The first argument is unused.
 * Unsigned addition retains the target's wrapping end-address calculation;
 * this is not a claim that the original function detects arithmetic overflow. */
int probe_08862434(void *unknown, u32 address, u32 length)
{
    return address >= 0x08400000u && address + length <= 0x08800000u;
}

typedef struct ProbeBitRecord {
    u8 unknown_000[0x5138];
    u8 bits_5138[8];
} ProbeBitRecord;

/* Count the first sixty bits in the observed byte field. Its game role is
 * unknown, and the final byte's four high bits are deliberately not counted. */
u32 probe_0886A58C(const ProbeBitRecord *record)
{
    u32 count = 0;
    u32 index;

    for (index = 0; index < 60; ++index) {
        count += (record->bits_5138[index / 8] >> (index % 8)) & 1;
    }
    return count;
}

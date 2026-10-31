/* Invented symbol-naming fixture, not game source or target-byte probes.
 * Type names and argument categories exercise the frozen probe signatures.
 * Small artificial records intentionally contain no reconstructed game fields.
 */
typedef signed char s8;
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct ProbeRecord { u32 invented; } ProbeRecord;
typedef struct ProbeByteRecord { u32 invented; } ProbeByteRecord;
typedef struct ProbeNode { u32 invented; } ProbeNode;
typedef struct ProbeDivisionRecord { u32 invented; } ProbeDivisionRecord;
typedef struct ProbeBitRecord { u32 invented; } ProbeBitRecord;

/* Distinguish a pointer to const unsigned byte from signed and mutable forms. */
int naming_fixture_00(const u8 *value) { return *value; }
/* Exercise a void result and mutable byte argument. */
void naming_fixture_01(u8 *value) { *value = 1; }
/* Exercise a pointer result and two differently qualified byte pointers. */
const u8 *naming_fixture_02(const u8 *input, u8 *output) { *output = *input; return input; }
/* Exercise the named mutable-record pointer category. */
void naming_fixture_03(ProbeRecord *record) { record->invented = 1; }
/* Repeat that signature under another synthetic name to check prefix handling. */
void naming_fixture_04(ProbeRecord *record) { record->invented = 2; }
/* Exercise an unsigned result and no arguments. */
u32 naming_fixture_05(void) { return 3; }
/* Exercise ordered untyped-pointer and unsigned arguments. */
u32 naming_fixture_06(void *opaque, u32 value) { return opaque ? value : 0; }
/* Exercise a const pointer to the second named record. */
u32 naming_fixture_07(const ProbeByteRecord *record) { return record->invented; }
/* Distinguish the const signed-byte pointer category. */
int naming_fixture_08(const s8 *value) { return *value; }
/* Exercise a const pointer to the named node type. */
u32 naming_fixture_09(const ProbeNode *record) { return record->invented; }
/* Exercise an untyped pointer followed by a const halfword pointer. */
u32 naming_fixture_10(void *opaque, const u16 *value) { return opaque ? *value : 0; }
/* Exercise a named const record followed by a signed scalar. */
u32 naming_fixture_11(const ProbeDivisionRecord *record, int value) { return record->invented + value; }
/* Exercise three arguments without introducing external calls. */
int naming_fixture_12(void *opaque, u32 first, u32 second) { return opaque && first == second; }
/* Exercise the last independent const-record signature. */
u32 naming_fixture_13(const ProbeBitRecord *record) { return record->invented; }

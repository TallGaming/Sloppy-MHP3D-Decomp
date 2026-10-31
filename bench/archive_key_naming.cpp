/* Invented member-name fixture only; it has no game offsets or target body. */
typedef unsigned int u32;

struct ArchiveKeyContext {
    u32 invented_value;
    void initialize_key(u32 value);
};

/* Exercise this class/method/argument signature with unrelated simple code. */
void ArchiveKeyContext::initialize_key(u32 value)
{
    invented_value = value + 1;
}

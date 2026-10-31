/*
 * Invented unsigned-arithmetic fixtures for compiler capability research.
 *
 * These scalar functions have no game receiver, layout, assets or target bytes.
 * The complete translation unit is compiled under every declared setting; its
 * output is inspected for static arithmetic encodings, never game-match credit.
 */
typedef unsigned int u32;
typedef char WordWidth[(sizeof(u32) == 4) ? 1 : -1];

extern "C" {

/* Observe how the backend reduces an unsigned constant remainder. */
u32 capability_remainder_a(u32 value)
{
    return value % 65521u;
}

/* A second divisor distinguishes generic division from constant lowering. */
u32 capability_remainder_b(u32 value)
{
    return value % 65497u;
}

/* The product deliberately wraps at 32 bits before the remainder operation. */
u32 capability_wrapped_product(u32 value)
{
    return (value * 65599u) % 65521u;
}

}

/*
 * Invented direct-call fixture for compiler relocation research.
 * No game function or historical source is represented here. Its fixed -O2
 * configuration is diagnostic only and does not select game compiler flags.
 */

extern int fixture_external(int value);

/* Make one external call and use its result so it cannot become a tail jump. */
int fixture_call(int value)
{
    return fixture_external(value) + 1;
}

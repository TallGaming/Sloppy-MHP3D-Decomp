/* Offline KL4E data preparation with guarded anonymous buffers.
 *
 * The linked decoder is the unchanged, separately pinned kl4e.c. It has no
 * input-length argument, so the last real input byte sits immediately before
 * an inaccessible page. Its literal probabilities depend on the absolute
 * output address modulo eight; preserve an eight-aligned output base.
 *
 * The controller must pin files, reject redirected parent paths and bound the
 * subprocess lifetime. This wrapper never maps or executes decompressed code.
 */
#define _GNU_SOURCE

#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/resource.h>
#include <sys/stat.h>
#include <unistd.h>

#define MAX_BYTES ((size_t)16 * 1024 * 1024)
#define PREFIX_MINIMUM ((size_t)64)
#define SENTINEL ((unsigned char)0xA5)

/* This declaration matches kl4e.c without editing that original source. */
extern int decompress_kle(uint8_t *output, int capacity, uint8_t *input,
                          void **reported_end, int is_kl4e);

struct guarded_buffer {
    unsigned char *mapping;
    size_t mapping_size;
    unsigned char *usable;
    size_t usable_size;
    unsigned char *data;
};

static int fail(const char *message)
{
    fprintf(stderr, "kl4e_guarded: %s\n", message);
    return 1;
}

static int fail_system(const char *operation)
{
    fprintf(stderr, "kl4e_guarded: %s: %s\n", operation, strerror(errno));
    return 1;
}

static int rounded_size(size_t value, size_t multiple, size_t *result)
{
    if (!multiple || value > SIZE_MAX - (multiple - 1))
        return 0;
    *result = ((value + multiple - 1) / multiple) * multiple;
    return 1;
}

/* Leave an inaccessible page on each side, and put the data's end exactly at
 * the trailing guard. Any writable prefix is checked separately for output.
 */
static int map_guarded(struct guarded_buffer *buffer, size_t data_size,
                       size_t minimum_prefix, size_t page_size)
{
    size_t usable_size;
    void *mapping;

    if (data_size > SIZE_MAX - minimum_prefix ||
        !rounded_size(data_size + minimum_prefix, page_size, &usable_size) ||
        page_size > SIZE_MAX / 2 || usable_size > SIZE_MAX - 2 * page_size)
        return fail("guarded mapping size overflow");
    buffer->mapping_size = usable_size + 2 * page_size;
    mapping = mmap(NULL, buffer->mapping_size, PROT_NONE,
                   MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (mapping == MAP_FAILED)
        return fail_system("mmap");
    buffer->mapping = mapping;
    buffer->usable = buffer->mapping + page_size;
    buffer->usable_size = usable_size;
    buffer->data = buffer->usable + usable_size - data_size;
    if (mprotect(buffer->usable, usable_size, PROT_READ | PROT_WRITE) != 0)
        return fail_system("mprotect writable buffer");
    return 0;
}

static void unmap_guarded(struct guarded_buffer *buffer)
{
    if (buffer->mapping)
        (void)munmap(buffer->mapping, buffer->mapping_size);
}

static int same_file_state(const struct stat *left, const struct stat *right)
{
    return left->st_dev == right->st_dev && left->st_ino == right->st_ino &&
        left->st_size == right->st_size &&
        left->st_mtim.tv_sec == right->st_mtim.tv_sec &&
        left->st_mtim.tv_nsec == right->st_mtim.tv_nsec &&
        left->st_ctim.tv_sec == right->st_ctim.tv_sec &&
        left->st_ctim.tv_nsec == right->st_ctim.tv_nsec;
}

static int read_exact(int descriptor, unsigned char *bytes, size_t size)
{
    size_t offset = 0;
    while (offset < size) {
        ssize_t count = read(descriptor, bytes + offset, size - offset);
        if (count < 0) {
            if (errno == EINTR)
                continue;
            return fail_system("read input");
        }
        if (!count)
            return fail("input ended before its declared file size");
        offset += (size_t)count;
    }
    return 0;
}

static int sentinels_unchanged(const unsigned char *bytes, size_t size)
{
    size_t index;
    for (index = 0; index < size; ++index) {
        if (bytes[index] != SENTINEL)
            return 0;
    }
    return 1;
}

/* Create the final component exclusively after all decode checks. On an I/O
 * failure an incomplete owned output can remain for the controller's audit;
 * the nonzero exit never labels such an artifact successful.
 */
static int write_exclusive(const char *path, const unsigned char *bytes, size_t size)
{
    int descriptor = open(path, O_WRONLY | O_CREAT | O_EXCL | O_NOFOLLOW | O_CLOEXEC,
                           S_IRUSR | S_IWUSR);
    size_t offset = 0;

    if (descriptor < 0)
        return fail_system("exclusive output creation");
    while (offset < size) {
        ssize_t count = write(descriptor, bytes + offset, size - offset);
        if (count < 0 && errno == EINTR)
            continue;
        if (count <= 0) {
            int saved_errno = count < 0 ? errno : EIO;
            (void)close(descriptor);
            errno = saved_errno;
            return fail_system("write output");
        }
        offset += (size_t)count;
    }
    if (fsync(descriptor) != 0) {
        int saved_errno = errno;
        (void)close(descriptor);
        errno = saved_errno;
        return fail_system("fsync output");
    }
    if (close(descriptor) != 0)
        return fail_system("close output");
    return 0;
}

static int parse_expected(const char *text, size_t *expected)
{
    const char *cursor;
    unsigned long long parsed;
    char *end;

    if (!*text)
        return 0;
    for (cursor = text; *cursor; ++cursor) {
        if (*cursor < '0' || *cursor > '9')
            return 0;
    }
    errno = 0;
    parsed = strtoull(text, &end, 10);
    if (errno || *end || !parsed || parsed > MAX_BYTES)
        return 0;
    *expected = (size_t)parsed;
    return 1;
}

int main(int argc, char **argv)
{
    struct rlimit no_core = {0, 0};
    struct guarded_buffer input = {0}, output = {0};
    struct stat initial, current, named_input;
    size_t expected, capacity, input_size, prefix_size, slack_size;
    size_t end_offset;
    long page_query;
    int input_descriptor = -1;
    int status = 1;
    int returned;
    int direct_copy;
    void *reported_end = NULL;
    uintptr_t end_address, input_address, input_limit;

    if (setrlimit(RLIMIT_CORE, &no_core) != 0)
        return fail_system("disable core files");
    if (argc != 4 || !parse_expected(argv[3], &expected)) {
        fprintf(stderr, "usage: kl4e_guarded INPUT OUTPUT EXPECTED_SIZE (1..16777216)\n");
        return 2;
    }
    page_query = sysconf(_SC_PAGESIZE);
    if (page_query < 64 || (size_t)page_query % 8)
        return fail("unsupported page size for aligned output guard");
    /* The decoder's direct-copy path rejects count >= capacity. Keep a small
     * sentinel slack region while preserving the absolute low address bits.
     */
    if (!rounded_size(expected + 1, 8, &capacity) || capacity > INT_MAX)
        return fail("output capacity overflow");
    input_descriptor = open(argv[1], O_RDONLY | O_CLOEXEC | O_NOFOLLOW | O_NONBLOCK);
    if (input_descriptor < 0)
        return fail_system("open input");
    if (fstat(input_descriptor, &initial) != 0) {
        (void)fail_system("stat input");
        goto done;
    }
    if (!S_ISREG(initial.st_mode) || initial.st_size < 9 ||
        (uintmax_t)initial.st_size > MAX_BYTES) {
        (void)fail("input must be a regular KL4E file of 9..16777216 bytes");
        goto done;
    }
    input_size = (size_t)initial.st_size;
    if (map_guarded(&input, input_size, 0, (size_t)page_query) ||
        map_guarded(&output, capacity, PREFIX_MINIMUM, (size_t)page_query))
        goto done;
    if (read_exact(input_descriptor, input.data, input_size))
        goto done;
    if (memcmp(input.data, "KL4E", 4) != 0) {
        (void)fail("input lacks offset-zero KL4E magic");
        goto done;
    }
    if (mprotect(input.usable, input.usable_size, PROT_READ) != 0) {
        (void)fail_system("protect input read-only");
        goto done;
    }
    if ((uintptr_t)output.data % 8) {
        (void)fail("output base is not eight-aligned");
        goto done;
    }
    memset(output.usable, SENTINEL, output.usable_size);
    prefix_size = (size_t)(output.data - output.usable);
    slack_size = capacity - expected;
    direct_copy = (input.data[4] & 0x80) != 0;
    /* No bytes are appended to the real input. A decoder overread reaches the
     * trailing PROT_NONE page and fails the containing subprocess by signal.
     */
    returned = decompress_kle(output.data, (int)capacity, input.data + 4,
                              &reported_end, 1);
    if (returned != (int)expected) {
        fprintf(stderr, "kl4e_guarded: decoder returned %d (0x%08" PRIx32 "), expected %zu\n",
                 returned, (uint32_t)returned, expected);
        goto done;
    }
    if (!sentinels_unchanged(output.usable, prefix_size) ||
        !sentinels_unchanged(output.data + expected, slack_size)) {
        (void)fail("output prefix or slack sentinel changed");
        goto done;
    }
    input_address = (uintptr_t)input.data;
    input_limit = input_address + input_size;
    end_address = (uintptr_t)reported_end;
    if (!reported_end || end_address < input_address + 4 || end_address > input_limit ||
        (direct_copy && end_address == input_limit)) {
        (void)fail("decoder reported an out-of-range endpoint");
        goto done;
    }
    end_offset = (size_t)(end_address - input_address);
    if (fstat(input_descriptor, &current) != 0 || lstat(argv[1], &named_input) != 0) {
        (void)fail_system("recheck input");
        goto done;
    }
    if (!S_ISREG(named_input.st_mode) || !same_file_state(&initial, &current) ||
        !same_file_state(&initial, &named_input)) {
        (void)fail("input file changed during preparation");
        goto done;
    }
    if (write_exclusive(argv[2], output.data, expected))
        goto done;
    printf("{\"status\":\"EXACT_BOUNDED_DECODE\",\"input_size\":%zu,"
           "\"expected_size\":%zu,\"returned_size\":%d,\"capacity\":%zu,"
           "\"output_alignment\":8,\"prefix_sentinel_bytes\":%zu,"
           "\"slack_sentinel_bytes\":%zu,\"prefix_sentinel_unchanged\":true,"
           "\"slack_sentinel_unchanged\":true,\"input_end_guard\":true,"
           "\"input_read_only\":true,\"output_end_guard\":true,"
           "\"reported_end_offset\":%zu,\"reported_end_body_offset\":%zu,"
           "\"end_pointer_convention\":\"%s\","
           "\"uniform_input_consumption_claimed\":false,"
           "\"decompressed_module_executed\":false}\n",
           input_size, expected, returned, capacity, prefix_size, slack_size,
           end_offset, end_offset - 4,
           direct_copy ? "DIRECT_COPY_LAST_SOURCE_BYTE" : "COMPRESSED_NEXT_CURSOR");
    if (fflush(stdout) != 0 || ferror(stdout)) {
        (void)fail("could not report decode result");
        goto done;
    }
    status = 0;

done:
    if (input_descriptor >= 0)
        (void)close(input_descriptor);
    unmap_guarded(&input);
    unmap_guarded(&output);
    return status;
}

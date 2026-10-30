/* Test driver for the C guide units. The units translation unit is built
 * from the extracted reference/c.md fences; signatures here must match. */
#include <assert.h>
#include <errno.h>
#include <pthread.h>
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>

extern bool copy_name(char *dst, size_t dst_size, const char *src);
extern int load_file(const char *path, unsigned char **out, size_t *len);
extern int sum_tail(const int *arr, size_t n);
extern bool should_stop(void);
extern void request_stop(void);

static int failures = 0;
static const char *current = "";

static void check(int ok, const char *what) {
    printf("%-45s %s\n", what, ok ? "ok" : "FAIL");
    if(!ok) {
        failures++;
        (void)current;
    }
}

static void test_copy_name(void) {
    char dst[4];
    check(copy_name(dst, 4, "abc"), "copy_name fits exactly");
    check(strcmp(dst, "abc") == 0, "copy_name stores content");
    check(!copy_name(dst, 4, "abcd"), "copy_name rejects truncation");
    check(copy_name(dst, 4, ""), "copy_name accepts empty");
    check(dst[0] == '\0', "copy_name terminates empty copy");
    check(!copy_name(dst, 0, "a"), "copy_name rejects zero capacity");
}

static char *temp_path(void) {
    static const char *dirs[] = { ".", "./" };
    char *path = malloc(64);
    snprintf(path, 64, "%s/.generated-load-%d.tmp", dirs[0], (int)getpid());
    return path;
}

static void write_bytes(const char *path, const unsigned char *data, size_t len) {
    FILE *f = fopen(path, "wb");
    assert(f);
    if(len) {
        fwrite(data, 1, len, f);
    }
    fclose(f);
}

static unsigned char sample[10000];

static void fill_sample(void) {
    for (size_t i = 0; i < sizeof sample; i++) {
        sample[i] = (unsigned char)(i % 255);
    }
}

static void test_load_file(void) {
    char *path = temp_path();
    unsigned char *buf = NULL;
    size_t len = 0;

    write_bytes(path, (const unsigned char *)"hello", 5);
    check(load_file(path, &buf, &len) == 0, "load_file reads a small file");
    check(len == 5 && memcmp(buf, "hello", 5) == 0, "load_file content matches");
    free(buf);
    buf = NULL;

    write_bytes(path, sample, sizeof sample);
    check(load_file(path, &buf, &len) == 0, "load_file grows past 4096 bytes");
    check(len == sizeof sample && buf[9999] == sample[9999],
          "load_file grown content matches");
    free(buf);
    buf = NULL;

    /* Empty file */
    write_bytes(path, (const unsigned char *)"", 0);
    check(load_file(path, &buf, &len) == 0 && len == 0, "load_file empty file");
    free(buf);
    buf = NULL;

    /* Failure cleanup: missing file */
    check(load_file("./definitely-missing.file", &buf, &len) == -1,
          "load_file reports missing file");
    check(buf == NULL, "load_file leaves no buffer on failure");

    /* ferror path: reading a directory fails on Linux */
    check(load_file(".", &buf, &len) == -1, "load_file reports directory read error");
    check(buf == NULL, "load_file cleans up after read error");

    remove(path);
    free(path);
}

static void test_sum_tail(void) {
    const int a[3] = { 1, 2, 3 };
    check(sum_tail(a, 3) == 6, "sum_tail adds a full array");
    check(sum_tail(a, 0) == 0, "sum_tail accepts empty range");
}

static void test_atomic_stop(void) {
    check(!should_stop(), "stop flag starts false");
    request_stop();
    check(should_stop(), "stop flag becomes true");
}

static void *spin_reader(void *arg) {
    long spins = 0;
    (void)arg;
    /* The stop flag may already be set by the earlier test; this reader
     * must exit rather than hang either way. */
    while (!should_stop() && spins < 1000000L) {
        spins++;
        sched_yield();
    }
    return (void *)spins;
}

static void test_stop_readers(void) {
    pthread_t t[2];
    bool exit_ok = true;
    for (int i = 0; i < 2; i++) {
        if (pthread_create(&t[i], NULL, spin_reader, NULL) != 0) {
            exit_ok = false;
        }
    }
    request_stop();
    for (int i = 0; i < 2; i++) {
        void *retval = NULL;
        exit_ok = exit_ok && pthread_join(t[i], &retval) == 0;
    }
    check(exit_ok, "two readers observe stop without hanging");
}

int main(void) {
    fill_sample();
    test_copy_name();
    test_load_file();
    test_sum_tail();
    test_atomic_stop();
    test_stop_readers();
    printf("%s\n", failures ? "FAILURES" : "ALL-OK");
    return failures ? 1 : 0;
}

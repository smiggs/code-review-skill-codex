#include <stdio.h>
#include <string.h>

/* Reads up to four 8-byte log records and copies them to standard output.
 * A short read is reported: I/O failure aborts, end of file is an explicit
 * truncation report so callers can reconcile the stream. */
int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s RECORDS\n", argv[0]);
        return 64;
    }
    FILE *f = fopen(argv[1], "rb");
    if (!f) {
        perror("open");
        return 66;
    }
    char recs[4][8];
    for (int i = 0; i < 4; i++) {
        memcpy(recs[i], "MARKER8", 8);
    }
    size_t got = fread(recs, 8, 4, f);
    int status = 0;
    if (got < 4) {
        if (ferror(f)) {
            fprintf(stderr, "read error\n");
            fclose(f);
            return 2;
        }
        if (!feof(f)) {
            fprintf(stderr, "short read without eof\n");
            fclose(f);
            return 2;
        }
        fprintf(stderr, "truncated: %zu of 4 records\n", got);
        status = 3;
    }
    fclose(f);
    for (size_t i = 0; i < got; i++) {
        printf("record %zu: %.8s\n", i, recs[i]);
    }
    return status;
}

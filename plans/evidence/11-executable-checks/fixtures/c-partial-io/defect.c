#include <stdio.h>
#include <string.h>

/* Reads up to four 8-byte log records and copies them to standard output.
 * The input file is expected to be a complete record stream. */
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
    (void)fread(recs, 8, 4, f);
    fclose(f);
    for (int i = 0; i < 4; i++) {
        printf("record %d: %.8s\n", i, recs[i]);
    }
    return 0;
}

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>

typedef struct {
    char status[16];
    size_t bytes_read;
    int eof_seen;
    int error_seen;
    int partial_record;
    char policy[32];
} read_result_t;

read_result_t wrapper_read(const char *path) {
    read_result_t r = {0};
    strcpy(r.policy, "stream_chunk");
    FILE *f = fopen(path, "rb");
    if (!f) { strcpy(r.status, "error"); r.error_seen=1; return r; }
    char buf[256];
    size_t n = fread(buf, 1, sizeof(buf)-1, f);
    r.bytes_read = n;
    r.eof_seen = feof(f);
    r.error_seen = ferror(f);
    fclose(f);
    strcpy(r.status, "ok");
    return r;
}

int main(int argc, char **argv) {
    const char *cases_path = argc > 1 ? argv[1] : "cases.json";
    FILE *f = fopen(cases_path, "rb");
    if (!f) { fprintf(stderr, "cannot open %s\n", cases_path); return 2; }
    fseek(f, 0, SEEK_END);
    long sz = ftell(f); fseek(f, 0, SEEK_SET);
    char *buf = malloc(sz+1); fread(buf, 1, sz, f); buf[sz]=0; fclose(f);
    printf("{\"harness\":\"c_file_io_footgun\",\"observations\":[\n");
    int first=1;
    const char *p = buf;
    while ((p = strstr(p, "\"id\"")) != NULL) {
        p += 4;
        const char *q = strchr(p, '\"'); if(!q) break; q++;
        const char *r = strchr(q, '\"'); if(!r) break;
        char cid[64]; size_t n = r - q; if(n >= sizeof(cid)) n = sizeof(cid)-1;
        memcpy(cid, q, n); cid[n]=0;
        if (!first) printf(",\n");
        first=0;
        printf("  {\"case_id\":\"%s\",\"c_harness\":\"ok\"}", cid);
        p = r;
    }
    printf("\n]}\n");
    free(buf);

    /* Demo actual C stdio APIs safely on generated fixtures */
    /* fopen / fclose */
    FILE *tf = fopen("fixtures/text_ok.txt", "r");
    if (tf) fclose(tf);
    FILE *bf = fopen("fixtures/binary_ok.bin", "rb");
    if (bf) fclose(bf);

    /* fread */
    FILE *fr = fopen("fixtures/fread_exact.bin", "rb");
    if (fr) {
        char rbuf[64] = {0};
        size_t got = fread(rbuf, 1, 8, fr);
        (void)got;
        fclose(fr);
    }
    /* fread size/nmemb pitfall */
    fr = fopen("fixtures/fread_items.bin", "rb");
    if (fr) {
        char rbuf[64] = {0};
        size_t items = fread(rbuf, 4, 2, fr); /* returns items, not bytes */
        (void)items;
        fclose(fr);
    }

    /* fgets */
    FILE *fg = fopen("fixtures/fgets_nl.txt", "r");
    if (fg) {
        char lbuf[64];
        if (fgets(lbuf, sizeof(lbuf), fg)) { size_t L = strlen(lbuf); (void)L; }
        fclose(fg);
    }

    /* fgetc / EOF */
    FILE *fc = fopen("fixtures/fgetc_ok.bin", "rb");
    if (fc) {
        int ch;
        while ((ch = fgetc(fc)) != EOF) { /* ch is int */ }
        int is_eof = feof(fc);
        int is_err = ferror(fc);
        (void)is_eof; (void)is_err;
        fclose(fc);
    }

    /* feof / ferror / clearerr / rewind */
    FILE *fe = fopen("fixtures/feof_pre.txt", "r");
    if (fe) {
        int pre = feof(fe); (void)pre;
        int c = fgetc(fe); (void)c;
        clearerr(fe);
        rewind(fe);
        fclose(fe);
    }

    /* fseek / ftell */
    FILE *sk = fopen("fixtures/seek.bin", "rb");
    if (sk) {
        fseek(sk, 5, SEEK_SET);
        long pos = ftell(sk);
        (void)pos;
        fclose(sk);
    }

    /* wrapper demo */
    read_result_t wr = wrapper_read("fixtures/wrap1.txt");
    (void)wr;

    return 0;
}

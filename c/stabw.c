/* stabw.c (22.10): stab.c for warm starts. Heights may be negative after z0 = eta + L g; only sites with z >= 4
   topple (stab.c's t = z >> 2 "untopples" a negative site, Fable 22.10). Same result as stab.c on cold inputs.
   burn(): Dhar's burning test, 1 iff the stable configuration is recurrent (every site burns from the sink). */
#include <stdint.h>
#include <stdlib.h>
long stab_odo(int64_t *z, int64_t *u, int n) {
    long sweeps = 0; int busy = 1;
    while (busy) {
        busy = 0; sweeps++;
        int dir = sweeps & 1;
        for (int ii = 0; ii < n; ii++) {
            int i = dir ? ii : n - 1 - ii;
            int64_t *row = z + (int64_t)i * n;
            for (int jj = 0; jj < n; jj++) {
                int j = dir ? jj : n - 1 - jj;
                if (row[j] < 4) continue;
                int64_t t = row[j] >> 2;
                busy = 1;
                row[j] -= 4 * t; u[(int64_t)i * n + j] += t;
                if (i > 0) row[j - n] += t;
                if (i < n - 1) row[j + n] += t;
                if (j > 0) row[j - 1] += t;
                if (j < n - 1) row[j + 1] += t;
            }
        }
    }
    return sweeps;
}
long burn(const int64_t *z, int n) {
    int64_t N = (int64_t)n * n, head = 0, tail = 0, burnt = 0;
    int *cnt = calloc(N, sizeof(int)); char *q = calloc(N, 1); int64_t *Q = malloc(N * sizeof(int64_t));
    for (int64_t k = 0; k < N; k++) {
        int i = k / n, j = k % n;
        cnt[k] = (i == 0) + (i == n - 1) + (j == 0) + (j == n - 1);
        if (z[k] + cnt[k] >= 4) { q[k] = 1; Q[tail++] = k; }
    }
    while (head < tail) {
        int64_t k = Q[head++]; burnt++;
        int i = k / n, j = k % n;
        int64_t nb[4]; int m = 0;
        if (i > 0) nb[m++] = k - n;
        if (i < n - 1) nb[m++] = k + n;
        if (j > 0) nb[m++] = k - 1;
        if (j < n - 1) nb[m++] = k + 1;
        for (int a = 0; a < m; a++) {
            int64_t x = nb[a];
            if (q[x]) continue;
            if (z[x] + ++cnt[x] >= 4) { q[x] = 1; Q[tail++] = x; }
        }
    }
    free(cnt); free(q); free(Q);
    return burnt;
}

/* stab.c (#391): exact stabilisation with odometer on an N x N grid, sink outside.
   In-place sweeps, each unstable site topples floor(z/4) times at once (abelian: same final z and u as
   any legal order). Alternating sweep direction. Returns number of sweeps. */
#include <stdint.h>
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
                int64_t t = row[j] >> 2;
                if (!t) continue;
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

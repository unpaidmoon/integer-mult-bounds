/* Normalized 14-point difference bases of F_2^6 that contain 0 and the
   standard basis. Count which of them have a simple 14-cycle whose edges
   all have Hamming weight at most 3, and the minimum total weight of such
   a cycle. Apache-2.0. */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

static int rest[57];
static int nrest;
static const uint64_t FULL = ~1ULL;

static void init_rest(void) {
    nrest = 0;
    for (int i = 1; i < 64; i++) {
        if (i == 1 || i == 2 || i == 4 || i == 8 || i == 16 || i == 32) {
            continue;
        }
        rest[nrest++] = i;
    }
    if (nrest != 57) {
        fprintf(stderr, "rest %d\n", nrest);
        exit(1);
    }
}

static int pop(unsigned x) {
    return __builtin_popcount(x);
}

/* Minimum total Hamming weight of a 14-cycle on pts[0..13] using only
   edges of weight 1, 2 or 3. Returns 0 when no such cycle exists.
   When save is non-NULL and a cycle exists, writes 15 vertices, repeating
   the start at the end, for one minimum cycle. */
static int min_cycle(const int *pts, int *save) {
    int wgt[14][14];
    uint16_t adj[14];
    memset(wgt, 0, sizeof wgt);
    memset(adj, 0, sizeof adj);
    for (int i = 0; i < 14; i++) {
        for (int j = i + 1; j < 14; j++) {
            int w = pop((unsigned)(pts[i] ^ pts[j]));
            if (w >= 1 && w <= 3) {
                wgt[i][j] = wgt[j][i] = w;
                adj[i] |= (uint16_t)(1u << j);
                adj[j] |= (uint16_t)(1u << i);
            }
        }
    }
    static uint8_t cost[1 << 14][14];
    memset(cost, 255, sizeof cost);
    cost[1][0] = 0;
    int full = (1 << 14) - 1;
    for (int mask = 1; mask <= full; mask++) {
        for (int v = 0; v < 14; v++) {
            uint8_t cv = cost[mask][v];
            if (cv == 255) {
                continue;
            }
            uint16_t nbr = (uint16_t)(adj[v] & ~(uint16_t)mask);
            while (nbr) {
                int u = __builtin_ctz(nbr);
                nbr = (uint16_t)(nbr & (nbr - 1));
                int nc = cv + wgt[v][u];
                int nm = mask | (1 << u);
                if (nc < cost[nm][u]) {
                    cost[nm][u] = (uint8_t)nc;
                }
            }
        }
    }
    int best = 1000;
    int end = -1;
    for (int v = 1; v < 14; v++) {
        if (cost[full][v] == 255 || !wgt[v][0]) {
            continue;
        }
        int tot = cost[full][v] + wgt[v][0];
        if (tot < best) {
            best = tot;
            end = v;
        }
    }
    if (end < 0) {
        return 0;
    }
    if (save) {
        int idx[14];
        int mask = full;
        int v = end;
        idx[13] = v;
        for (int step = 13; step >= 1; step--) {
            int prev = -1;
            for (int u = 0; u < 14; u++) {
                if (!(mask & (1 << u)) || u == v || !wgt[u][v]) {
                    continue;
                }
                int pm = mask ^ (1 << v);
                if (cost[pm][u] != 255 && cost[pm][u] + wgt[u][v] == cost[mask][v]) {
                    prev = u;
                    break;
                }
            }
            if (prev < 0) {
                fprintf(stderr, "reconstruction failed\n");
                exit(1);
            }
            idx[step - 1] = prev;
            mask ^= 1 << v;
            v = prev;
        }
        if (idx[0] != 0 || mask != 1) {
            fprintf(stderr, "reconstruction did not start at 0\n");
            exit(1);
        }
        for (int i = 0; i < 14; i++) {
            save[i] = pts[idx[i]];
        }
        save[14] = pts[0];
    }
    return best;
}

static int is_basis(const int *pts) {
    uint64_t seen = 0;
    for (int i = 0; i < 14; i++) {
        if (pts[i]) {
            seen |= 1ULL << pts[i];
        }
        for (int j = i + 1; j < 14; j++) {
            seen |= 1ULL << (pts[i] ^ pts[j]);
        }
    }
    return seen == FULL;
}

int main(void) {
    init_rest();
    long hits = 0;
    long cycles = 0;
    int best = 1000;
    int saved = 0;
    int cycle[15];
    int displayed[14] = {0, 1, 2, 3, 4, 5, 6, 8, 16, 24, 32, 40, 48, 63};
    if (!is_basis(displayed)) {
        fprintf(stderr, "displayed set is not a basis\n");
        return 1;
    }
    int displayed_cost = min_cycle(displayed, NULL);
    for (int a = 0; a < nrest; a++) {
        for (int b = a + 1; b < nrest; b++) {
            for (int c = b + 1; c < nrest; c++) {
                for (int d = c + 1; d < nrest; d++) {
                    for (int e = d + 1; e < nrest; e++) {
                        for (int f = e + 1; f < nrest; f++) {
                            for (int g = f + 1; g < nrest; g++) {
                                int pts[14] = {
                                    0, 1, 2, 4, 8, 16, 32,
                                    rest[a], rest[b], rest[c], rest[d],
                                    rest[e], rest[f], rest[g]
                                };
                                if (!is_basis(pts)) {
                                    continue;
                                }
                                hits++;
                                int got_slot[15];
                                int cost = min_cycle(pts, got_slot);
                                if (!cost) {
                                    continue;
                                }
                                cycles++;
                                if (cost < best) {
                                    best = cost;
                                    memcpy(cycle, got_slot, sizeof cycle);
                                    saved = 1;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    if (!saved) {
        fprintf(stderr, "no cycle\n");
        return 1;
    }
    printf("hits=%ld\n", hits);
    printf("cycles=%ld\n", cycles);
    printf("min_sum=%d\n", best);
    printf("displayed_cost=%d\n", displayed_cost);
    printf("cycle=");
    for (int i = 0; i < 15; i++) {
        if (i) {
            printf(" ");
        }
        printf("%d", cycle[i]);
    }
    printf("\n");
    return 0;
}

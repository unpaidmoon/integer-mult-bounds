# A weight-at-most-3 closed walk on a 14-point difference basis

Let \(P \subset \mathbb{F}_2^6\) be

```text
P = {0, 1, 2, 3, 4, 5, 6, 8, 16, 24, 32, 40, 55, 56}.
```

The cyclic order

```text
0, 32, 40, 56, 24, 16, 8, 4, 5, 55, 6, 2, 3, 1, 0
```

has successive differences

```text
32, 8, 16, 32, 8, 24, 12, 1, 50, 49, 4, 1, 2, 1
```

of Hamming weights

```text
1, 1, 1, 1, 1, 2, 2, 1, 3, 3, 1, 1, 1, 1.
```

Every weight is 1, 2 or 3. The total is 20. The six coordinates occur
`(4, 2, 2, 4, 4, 4)` times, all even, so the sum of the steps is zero and
the walk returns to its start in \(\mathbb{F}_2^6\). The fourteen vertices
are exactly \(P\), each once.

The \(\binom{14}{2} = 91\) pairwise sums, together with the thirteen nonzero
points, are exactly the 63 nonzero vectors. Thus \(P\) is a difference basis.
Both statements are finite and are rechecked by `verify.py`.

## What this does not say

Nick Petalas's `research/fixed-fourteen-basis-walk` proves that the different
basis

```text
{0, 1, 2, 3, 4, 5, 6, 8, 16, 24, 32, 40, 48, 63}
```

has no closed walk of maximum step weight 3: 63 is at distance at least 4
from every other point. The walk above shows that this obstruction is special
to that set.

Under the paired-readout accounting of that note, this cycle still costs 14
source root calls and 20 source-map applications, plus 126 output root calls
and 126 output-map applications: 140 root queries and 146 map applications.
That is the same application total as the weight-4 cycle on the displayed
set, and four above the generic six-source DUO bill of 142. This package does
not emit that symbolic word again and does not claim a cheaper connector.

## Normalized minimum

Translate any candidate so that it contains 0, and keep only those bases that
also contain the six weight-1 vectors. There are 53,340 such bases, the same
count as `research/f2-six-difference-basis`. Of them, 53,270 have at least one
simple 14-cycle of step weight at most 3, and every such cycle has total
weight at least 20. The cycle above meets 20. The displayed basis is one of
the 70 exceptions, rechecked from the distance argument and from the same
dynamic program.

Linear changes of basis do not preserve Hamming weight, so this minimum is
not a minimum over every 14-point difference basis. A basis that omits some
weight-1 vector could still have a lighter weight-at-most-3 cycle.

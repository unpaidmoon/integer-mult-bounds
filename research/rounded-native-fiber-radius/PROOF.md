# The exact input radius is three

This contribution was produced by Nick Petalas. Apache-2.0.

## Fixed contract and credited premises

Let M be the literal 112 by 8 signed integer matrix in MATRIX.json, copied
byte for byte from zxv's PR5444, research/precision-state-frontier/FIXTURE.json.
Every row has four nonzero entries of absolute value one, and M^T M = 56 I.
The map is exactly

    F(x) = 8x - M R(8 M^T x / 52),  x in Z^112,

where R rounds each component to nearest, with half ties away from zero.
For an output y, put s=M^T y and write q for its rounded quotient. PR5444's
fiber theorem and its source lattice calculation give these premises.

1. Preimages are exactly x=(y+Mq)/8 with y+Mq divisible by 8 and
   R((s+56q)/52)=q. For each coordinate, the latter condition leaves at most
   thirteen consecutive integers, with its stated half-tie endpoint rules.
2. ker(M modulo 8) consists exactly of 4v with v modulo 2 in a binary
   linear code C of size sixteen. In particular, every fiber's quotients
   have one fixed residue modulo 4, and at most sixteen parity classes
   after dividing differences by 4.
3. M has full column rank, as also follows from the displayed Gram identity.

These are credited predecessor results, not new theorems of this package.
The source's maximum fiber at this scale is 4096. Its published sufficient
radius is sixteen, and its finite-range threshold question is explicitly open.

Define H_* as the least nonnegative integer H for which some output y has
4096 distinct preimages satisfying ||x||_infinity <= H. We prove H_*=3.
The same fixed origin-centered box must contain the whole fiber.

## Lower bound, for every output

Fix y. Partition its quotient candidates by their residues modulo 8.
There are at most sixteen nonempty cells by premise 2. Within each cell,
each quotient coordinate lies in an interval of thirteen consecutive
integers and in one residue modulo 8. It therefore has at most two values.
Every cell has at most 2^8=256 points. If the fiber contains 4096 points,
it has exactly sixteen full cells, and each is the complete Cartesian
product of eight two-point sets, every pair separated by eight.

Let c be the coordinatewise midpoint of one such quotient cell. In owner
coordinate i, the corresponding inputs have midpoint

    (y_i + (Mc)_i) / 8

and range of width four. Indeed, the four signed nonzero row entries
independently select endpoints separated by eight, so their total range
is 32 before division by eight. This uses the full Cartesian cell.

Suppose all these inputs lie in [-2,2]^112. Every width-four owner
interval must then be exactly [-2,2], so its midpoint is zero. Thus

    y + Mc = 0.

This holds for every one of the sixteen cells. Distinct cells have distinct
quotient midpoints: the two members in a coordinate have a fixed common
residue modulo eight, and their midpoint is that residue plus four modulo
eight. By full column rank, M sends distinct midpoints to distinct vectors.
Two full cells already contradict y+Mc=0 for both. Hence H_*>2.

This argument excludes every output, not just the attaining output below.
It concerns a full 4096-point fiber, not every smaller collision set.

## Upper bound by a literal output

The 112-entry vector y in WITNESS.json satisfies the exact integer identities

    y_i in {-4,0,4},    M^T y = 0,    y + 2 M 1 = 0 modulo 8.       (1)

The verifier checks all entries of (1). This vector is new witness data;
the old sufficient-radius construction is not replayed.

Take all q in {-6,-2,2,6}^8 for which y+Mq is divisible by eight. The
quotient q=2*1 satisfies this congruence. By premise 2 the other solutions
are obtained by q=2*1+4v with v modulo two in C. Each permitted parity
class has two choices in each coordinate. Thus there are exactly

    |C| 2^8 = 16 * 256 = 4096

solutions. Their reconstructed inputs are distinct because M is injective.
Equation (1) gives M^T x=7q. Therefore the actual forward quotient is

    R(8 M^T x / 52) = R(14q/13) = q,

since |q_j|<=6 and |14q_j/13-q_j|<=6/13<1/2. There are no rounding ties.
Every reconstructed input maps to y under the literal forward map.

Finally, |(Mq)_i|<=24 and |y_i|<=4, so |y_i+(Mq)_i|<=28. These numerators
are divisible by eight, so their absolute values are at most 24. Every
input therefore has ||x||_infinity<=3. This proves H_*<=3.

For completeness, all preimages of this particular y have been included.
Since s=0, the scalar rounding inequality forces |q_j|<=6. Its lattice
congruence and the particular solution 2*1 force q_j=2 modulo four. The
only possibilities are exactly {-6,-2,2,6}. No larger quotient is omitted.
Together with the lower bound, H_*=3.

## Verification and scope

verify.py enumerates all 4^8 quotient tuples, tests the congruence, reconstructs
every accepted integer input, and evaluates F literally. It independently
counts distinct inputs, their radii, sixteen Cartesian cells and every
owner interval. The all-output lower bound is the written midpoint proof;
enumerating one fiber alone would not establish minimality.

This settles one finite-range threshold of PR5444. It proves no native
implementation, reversible codec cost, physical owner access, full supplier
invoice, new kappa or complete multiplication theorem. Independent human
and formal proof-kernel review are unclaimed.

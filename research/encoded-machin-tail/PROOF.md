# A zero-floor stopping rule for encoded Machin setup

## Contract and result

Use Jose Manuel / jmbarrancoml's PR3709 `arctangent` and `pi_interval`
interfaces, with the same positive integer unit U, finite term budget J,
signed Count arithmetic, one-unit tail padding and arbitrary borrowed input
tapes. The two fixed denominators are d=5 and d=239. The source precision
parameters are Q>=16, T=Q+64, J=Q+8 and

    R=Q+ceil(log2 T)+12, U=2^R.

Define D_j=(2j+1)d^(2j+1), and K_d=min({j<J : D_j>U} union {J}).
The new routine computes exactly K_d floor quotients instead of J, stops
before the first zero quotient, and explicitly closes its encoded iterator.
Its directed interval contains arctan(1/d) whenever the original budget
has the stated alternating-tail bound. Its interval is contained in the
old interval. In the source precision family K_d<J for both denominators,
so every allowed Q saves at least two divisions across the two sums.

This is a scoped implementation and resource proof. The alternating-series
argument and Machin identity are classical. Dugongue's PR4554 already uses
magnitude-based Machin truncation in a different root-seed implementation.
The new contribution is the actual encoded PR3709 replacement, its containment
and ownership argument, and its executed physical bill. It is not a new
general series-evaluation method.

## Directed intervals and the omitted tail

The exact positive jth term in U-scaled units is U/D_j. The original code
uses the interval [floor(U/D_j), floor(U/D_j)+1], reverses and negates its
endpoints for an odd j, sums these intervals and pads by [-1,1].

D_j is strictly increasing. If K_d<J, every omitted floor quotient is zero.
The new prefix interval is consequently the same prefix used by the old
routine. Every removed positive term contributed [0,1]; every removed
negative term contributed [-1,0]. These intervals contain zero. Keeping
the same padding therefore makes the new interval a subset of the old one.
Its width is exactly K_d+2, while the old width is J+2, in U-grid units.

Containment alone would not prove enclosure of the real value. The
alternating-series remainder at K_d has absolute value at most
1/D_(K_d)<1/U when a stop occurs. Thus the unchanged one-unit padding
covers the complete omitted real tail, including its sign. When no stop
occurs, the routine is the original J-term routine. This proves enclosure
without assuming that a subset of a valid interval is automatically valid.

The strict comparison D_j>U retains a term when D_j=U. The first omitted
floor is then zero, as required by the containment and exact-count claims.
Stopping instead at equality need not satisfy those claims.

## Source precision and complete twiddle contract

For Q>=0, Q+64<=2^(Q+6), by induction starting at Q=0. Therefore
R<=2Q+18. At j=J-1,

    D_j >= 5^(2J-1) > 2^(4J-2) > 2^R,

because 4J-2=4Q+30>2Q+18. Thus K_d<=J-1 for each fixed denominator.
The one-unit remainder bound just proved applies at every Q>=16. There is
no extrapolation from the finite precision samples to this universal fact.

The new pi interval is

    [16 L_5 - 4 H_239, 16 H_5 - 4 L_239].

It contains pi by the same Machin identity and lies inside the old pi
interval. Its width is exactly 16 K_5+4 K_239+40. The old width is
20(J+2). In particular, the source's strict (3U,4U) guard remains valid
under its cited source contract.

The source angle is floor(pi_lower*k/(L/2))/U. The new lower endpoint is
between the old lower endpoint and pi. For 0<=k<L/2, the new angle stays
below the true angle and its error cannot increase. The source's Taylor
padding, width bounds and inward quantization consequently retain their
stated sufficient error and disk bounds. This uses PR3709's Taylor and
consumer proofs as cited premises. It does not re-verify them. Twiddle bits
may change at untested parameters; universal bit equality is not claimed.

## Encoded operations, ownership and accounting

The new comparison reads the already computed encoded divisor and U. It
does not decode runtime numbers, create a new physical tape, inspect target
data or change a borrowed input. All retained terms execute the same signed
floor arithmetic as before. On a stop, the divisor lease is released by its
owned context, the encoded iterator is explicitly closed, and lower, upper,
power and odd are closed by the outer finally block. The returned padded
endpoints remain live for the caller. The same cleanup also runs on an
injected quotient exception, as exercised by the checker.

For one sum with K<J, the routine performs K quotient divisions, K signed
interval updates, K power updates, 2K odd increments, and K+1 divisor
products and new comparisons. The iterator yields K+1 positions and
advances after the K retained ones. The original has J divisions and
updates and J divisor products, with no stopping comparison. Padding,
result ownership and the caller interface remain the same. No comparison,
extra tested divisor or iterator cleanup is treated as free.

The new overhead has O(R) bits per compared or tested divisor in this
source family; D_j grows by at most 3d^2 between successive indices. It
retains the source's O(Q) scratch and setup complexity class. A universal
strict reduction in every low-level tape metric is not claimed from a
division count alone.

The finite physical trace counts every underlying records.Tape read,
write and unit head move during pi_interval and consumption of both
returned endpoints. It includes all new comparisons, tested divisors,
encoded loop work and numerical cleanup. Fixture input serialization and
fixed pool construction precede the measured invocation; final marker
erasure and observation checks follow it. Those identical boundary tasks
are outside the counters on both sides. Host-side output observation reads
raw cells without contributing tape operations. Comparisons in the receipt
count only the newly added stopping-comparison site, not internal comparisons
inside inherited division or Count routines.

At Q=16, R=35, J=24, direct enumeration gives K_5=7 and K_239=2. The complete
Machin invocation therefore saves 39 of 48 quotient divisions and pays 11
new stopping comparisons. Its interval shrinks from
[107944301384,107944301904] to [107944301572,107944301732]. The four executed
precision fixtures also reduce tape reads, writes and moves. These are
exact finite operation counts, not wall-time speedups or full multiplication
invoices.

## Verification and implementation limits

The independent integer/Fraction oracle uses literal denominators rather
than the encoded implementation. It checks alternating brackets, all
interval endpoints, first-zero minimality and exact widths. Physical checks
exercise the actual Count/tape runtime, sealed physical allocation and
fixed scratch inventory. Complete twiddle packets test both directions,
exact quarter turns and nontrivial angles. The checker also exercises
zero-tail, comparison and padding mutations, invalid denominator rejection
and an interrupted quotient with complete lease return.

New functions have no recursion. The production loop has the original
finite encoded J bound. Verification loops have fixed finite domains; the
largest Fraction-oracle exponent is 256, and the source-count corroboration
ends at Q=512. Physical precisions end at Q=64 and stage lengths at 16.
Input hashing is bounded to four files of at most 128 MiB each. Python
integers, wrappers and finite test collections allocate dynamically, a
managed-runtime deviation from allocation-free execution. The physical
algorithm still forbids new Tape or Arena allocation after entry.
Controlled monkeypatches select two implementations and the listed finite
instrumentation/mutation targets in one isolated process. They restore the
namespace on exit; concurrent embedding is outside the interface.

No whole product or convolution replay, production GL64/O73 invocation,
selected cold replay, native supplier change, compiler/analytic admission,
new kappa, independent human review or proof-kernel check is claimed.
The five selected framework assumptions retain their status.

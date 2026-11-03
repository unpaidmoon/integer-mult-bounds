# Rational width normalizers and a sharp positive-width cutoff

This contribution was produced by Nick Petalas. Apache-2.0.

Claim type: scoped algebraic proof. Finite execution corroborates the proof;
it is not a proof-kernel certificate or a complete multiplication theorem.

## 1. Contract and theorem

Work over a characteristic-zero field K. Fix a finite alphabet Sigma. For
physical column operators, a letter records one output/input column pair.
Every complete input and output role, including arbitrary dirty returns,
is retained in the boundary matrices below.

For each j=1,...,h, supply fixed matrices F_j of shape o by D_j, B_j of
shape D_j by i, and T_(j,s) of shape D_j by D_j for every s in Sigma.
They do not depend on the positive width f or on the position of a letter.
Also supply polynomials p_j,q_j in K[z], with q_j(f) nonzero at every
positive integer f. For a word w=s_1...s_f define the complete residual

```text
E(w) = sum_j p_j(f)/q_j(f) F_j T_(j,s_1)...T_(j,s_f) B_j.
```

Choose a common polynomial multiple Q of all q_j, with Q(f) nonzero at
every positive integer. Their product is always an admissible choice.
Let c_j=Q p_j/q_j. Discard identically zero c_j and put

```text
d_j = deg c_j,                  N = sum_j D_j(d_j+1).
```

**Theorem.** E(w)=0 for every nonempty word if and only if E(w)=0 for
every word of lengths 1,...,N. Equivalently, a nonzero residual has a
literal input/output entry witness at a positive width at most N. If no
terms survive, N=0 and the conclusion is vacuous. A small common
denominator can improve N; no minimum over all equivalent descriptions
is asserted.

The bound is sharp even for one summand. For every D>=1 and d>=0 there
is a rational example with q(z)=z, D transfer states and deg c=d whose
first positive discrepancy is exactly D(d+1).

This extends the represented-recurrence interface in zxv's
[PR5441](https://github.com/CrocSwap/integer-mult-bounds/pull/5441).
The proof uses classical finite-dimensional weighted-automata closure and
polynomial counters. Those ingredients and the original physical-transfer
contract are predecessor mathematics. The contribution here is the
rational-width contract, its explicit cutoff, a matching construction and
the strict representational separation in section 5.

## 2. Clear the denominator and construct a polynomial counter

Because Q(f) is nonzero, E(w)=0 is equivalent to Q(f)E(w)=0 separately
at every positive width. Thus exact identity checking may clear Q even
when neither E nor its rational exterior coefficients have a fixed finite
transfer representation.

Let c have degree d. Characteristic zero permits the Newton expansion

```text
c(f) = sum_(k=0)^d a_k binom(f,k),       a_k = Delta^k c(0).
```

Let S be the (d+1)-square matrix with ones on its superdiagonal and zero
elsewhere. Put J=I+S, u=e_0^T and v=(a_0,...,a_d)^T. The binomial theorem
and S^(d+1)=0 give u J^f v=c(f) for every nonnegative integer f.

Replace the jth component by

```text
left boundary       F_j tensor u_j
letter transition   T_(j,s) tensor J_j
right boundary      B_j tensor v_j.
```

The mixed-product identity for Kronecker products proves that its width-f
value is exactly c_j(f) F_j T_(j,s_1)...T_(j,s_f) B_j. The coefficient
occurs once at the boundary. It is not raised to the fth power. Direct-sum
the components, concatenate the left boundaries and stack the right
boundaries. This gives a fixed N-state table for Q(f)E(w), including all
o by i role blocks.

No rational division is performed by this fixed table. Clearing the
denominator is a proof transformation, not a physical implementation of
the original operator or its normalization.

## 3. Positive-length closure and finite certificates

For a fixed N-state table F,T_s,B, let W_k be the span of all rows of
F T_w for words with 1<=length(w)<=k. These spaces increase. If
W_k=W_(k+1), right multiplication by every T_s preserves W_k, so all
later spaces are equal to W_k. If W_1=0 this already holds. Otherwise,
dim W_1>=1. Strict growth at every intervening step would force
dim W_N>=N, which also forces stability. Hence W_N contains every
positive-length reachable row.

If all endpoints through length N vanish, every row in W_N annihilates B.
Every later endpoint therefore vanishes. The converse is immediate.
Applying this to section 2 and dividing by the nonzero scalar Q(f)
proves the theorem.

A compact sufficient certificate supplies rows R such that every row of
F T_s belongs to span R, every row of R T_s belongs to span R, and RB=0.
These are finite exact linear-algebra checks. Alternatively, a producer
returns a literal word, an input role, an output role and a nonzero entry.
The implementation retains literal reachable rows during basis closure,
so it can return such a word rather than only an abstract linear
combination. The separately transcribed checker tests closure by ranks.

The positive-width convention matters. No value of 1/f at f=0 is used.
The bound is N, not an empty-word cutoff silently applied to the original
rational expression.

## 4. Sharpness for a single component

Fix D>=1,d>=0. Let C be the cyclic permutation matrix on D coordinates,
and use F=e_0^T and B=e_0. Then

```text
F C^f B = 1 if D divides f, and 0 otherwise.
p(z) = product_(k=1)^d (z-kD),       q(z)=Q(z)=z.
E_f = [D divides f] p(f)/f.
```

The empty product for d=0 is one. At a positive width below N=D(d+1),
either D does not divide f or f=kD for one of k=1,...,d. In both cases
E_f=0. At width N,

```text
E_N = D^d d! / N != 0.
```

The cleared coefficient is exactly p of degree d. Thus the theorem's
cutoff is attained for every D,d, even with one rational summand and one
physical symbol. If a larger physical alphabet is wanted, assign C to
one symbol and the zero matrix to every other symbol. The same first
discrepancy follows. This is a delayed semantic discrepancy, not a
profitable physical supplier.

## 5. The extension is strict

Take the scalar family a_f=1/f for f>=1. It has one fixed base transfer
state with transition 1 and rational exterior coefficient 1/f, so the
new contract includes it.

Suppose it also had any fixed finite transfer representation. Restricting
to a repeated physical symbol gives a scalar sequence F T^f B. By
Cayley-Hamilton it satisfies a nontrivial constant-coefficient recurrence

```text
sum_(k=0)^L b_k/(f+k) = 0
```

at every positive integer f. Multiply by product_(k=0)^L(z+k). The
resulting polynomial vanishes at infinitely many distinct elements of K,
so is identically zero. Evaluating it at z=-j gives

```text
b_j product_(0<=k<=L, k!=j) (k-j) = 0.
```

Every product is nonzero in characteristic zero. Hence every b_j=0,
a contradiction. Adding finitely many states, summands or owner roles
cannot evade this argument, since their sum still has a finite direct-sum
representation. Equality checking in the new class therefore does not
follow by claiming that each original normalized operator already has a
fixed finite table. Only its cleared residual needs one.

## 6. Limits and classical sources

The theorem assumes exact identities, characteristic zero, fixed physical
letter tables and a common denominator without positive-width zeros.
It does not cover arbitrary position dependence, adaptive schedules,
tolerance testing or poles at admitted widths. The executable corroboration
uses Q. Its automatic pole guard accepts nonzero polynomials with
nonnegative coefficients, a sufficient subclass of the theorem's
denominator hypothesis. It is not a general polynomial root solver.

No actual selected caller, native realization, ownership or dirty-erasure
implementation, precision/tape bound, paid invoice or integer-recovery
claim is supplied. The five selected framework assumptions remain open.

Classical background includes Kiefer, Murawski, Ouaknine, Wachter and
Worrell's [Q-weighted automata equivalence](https://people.mpi-sws.org/~joel/publications/Q_weighted_automata13.pdf),
especially finite-dimensional reachable spaces, and Crosswhite and Bacon's
[automata/matrix-product correspondence](https://arxiv.org/abs/0708.1221).
Newton differences, Kronecker products, Cayley-Hamilton and polynomial
root counting are classical. No general automata theorem or global
literature-priority claim is made here. PR5441 retains its source-native,
phase, compiler and physical-column attribution.

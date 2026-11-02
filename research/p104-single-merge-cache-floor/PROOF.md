# Exact tariff for a single merged operand cache

This scoped proof is produced by Nick Petalas. Apache-2.0.

## Model

Let the frame spaces be over any field. Write S,U,H,L,R for subspaces with

    dim S=s, dim U=u, dim H=dim R=u+1, dim L=1,
    1 <= s < u, H intersection R=U, S,L <= U, L not contained in S.

The field quantifier concerns frame geometry. Every nested MOVE is granted
as an available operation in the relaxation; native availability over an
arbitrary field is not asserted. The separate scalar payload check uses rational numbers.

The reader ascends from zero to R. The root descends from H to L and is read
once at F. Two independent operands V and B are captured at S and U. Each
owned cache descends to one common merge frame M; one cache forms V+B there.
The sum cache then descends to A and is delivered once to the reader. The
reader also receives -4Q from the root at F. The required logical endpoint is
A_in+V+B-4Q, with all public sources unchanged. Coefficients are scalar and
fixed. The argument does not require independence in the actual source word.
Independence defines this local replacement contract.

Every nested native MOVE of rank r costs phi(r). Here phi(0)=0 and phi is
nonnegative, increasing and concave on nonnegative integer ranks. All native
cache transport is charged. Waiting, clean owned storage, capture, the merge,
disposal and ordinary control are free in this deliberately favorable model.
Disposal can discard arbitrary cache contents. This is a tariff relaxation,
not a physical erasure or native implementation claim.

There is exactly one merge and one subsequent sum delivery. There are no
additional reads, split deliveries, public ascending caches, cloned roots,
changed productive targets or coordinated removal of other work. Intermediate
stops on each monotone path are unrestricted. Scalar logical payload checks
do not establish the native meaning of those paths.

Jerry Chen / CubeJerry's PR6248 supplies the question of mixed operands and
the inherited reader-497 geometry. Its separate-cache theorem is not replayed
or reproved here. The new model merges the sources before delivery.

## Reduction to three dimensions

Both pre-merge caches descend, so M<=S<=U. The sum descends to A<=M. Since
L<=F<=H and F lies on the reader path to R, L<=F<=U. Reader contacts A,F
are comparable. F cannot be below or equal to A: that would give L<=S.
Thus A<F. Put a=dim A, m=dim M, f=dim F. Exactly the following domain remains:

    0 <= a <= m <= s, a < f <= u.

Every triple is possible. Choose an a-space A in S, extend it to an m-space
M in S, and extend A+L to an f-space F in U. Only A needs to lie in F; M
need not. Longer paths cannot be cheaper than the compressed ones, since
concavity with phi(0)=0 implies subadditivity.

The compressed paid ranks, including zero ranks of zero cost, are

    reader:     a, f-a, u+1-f
    root:       u+1-f, f-1
    V cache:    s-m
    B cache:    u-m
    sum cache:  m-a.

Write C(a,m,f) for their total tariff. The unchanged schedule has bill

    C0 = 2phi(1)+phi(s)+phi(u-s)+phi(u-1).

It receives V at S, receives B and the root at U, and preserves the same
reader and root endpoints.

This is a fixed comparison profile, not an inference from the predecessor's
optimality claim.

## The exact minimum

Define

    C_low  = phi(1)+2phi(u)+phi(s)+phi(u-s),
    C_high = 2phi(1)+phi(s)+2phi(u-s)+phi(u-1).

Then the minimum over all single-merge itineraries is min(C_low,C_high).

If f=1, then a=0. Subadditivity and monotonicity give

    phi(s-m)+phi(m) >= phi(s),
    phi(u-m) >= phi(u-s).

The remaining terms are phi(1)+2phi(u). Therefore C>=C_low. Equality is
attained at (a,m,f)=(0,s,1), with M=S, A=0 and F=L.

If f>=2, both root segment ranks lie between 1 and u-1 and sum to u.
Concavity minimizes their sum at the two extreme ranks:

    phi(u+1-f)+phi(f-1) >= phi(1)+phi(u-1).

Group the other terms as follows:

    phi(a)+phi(s-m)+phi(m-a) >= phi(s),
    phi(f-a)+phi(u+1-f) >= phi(1)+phi(u-a),
    phi(u-a) >= phi(u-s),
    phi(u-m) >= phi(u-s).

For the second inequality, its two arguments are at least one and sum to
u+1-a. Concavity again places the minimum at the extremes 1,u-a. Adding
the inequalities gives C>=C_high. Equality is attained at
(a,m,f)=(s,s,u), with A=M=S and F=U. This proves the claimed exact minimum
without enumerating fields, subspaces or path lengths.

The excess over the unchanged schedule is exactly

    min(2phi(u)-phi(1)-phi(u-1), phi(u-s)).

Both terms are nonnegative for increasing phi. For phi(r)=r^t, 0<t<1,
both are strictly positive: u>1, and u-s>=1. Thus no itinerary in this
single-merge class improves the complete signed moment when other work and
productive targets stay fixed. Any additional nonnegative physical charge
only increases this obstruction.

## Reader 497 and finite evidence

PR6248 identifies s=3,u=6 for frames S=519,U=520,H=529,L=595,R=914 in
Ali Romman's PR6167. These source identities and inclusions are inherited
premises, not a new audit of the word. The new exact minimum is

    min(H1+2H3+2H6, 2H1+3H3+H5),

whereas C0=2H1+2H3+H5. The excess is

    min(2H6-H1-H5, H3) > 0, for H_r=r^t and 0<t<1.

There are 50 dimension recipes. The verifier constructs a binary flag witness
for each, independently extracts all native rank differences, and checks each
profile's capped sums against its f=1 or f>=2 endpoint. Since every increasing
concave tariff is a nonnegative combination of min(r,k) on a bounded integer
domain, these integer certificates corroborate the complete tariff comparison.
The same finite check covers 2<=u<=14 and 1<=s<u. These finite checks support
the written universal proof; they do not replace it.

The normalized scalar payload is checked on every public basis column and on
rational dirty examples, including nonzero incoming reader values. Those
checks illustrate the favorable merge/disposal contract only. They are not
an operator, phase, ownership, caller, compiler or rounded multiplier proof.

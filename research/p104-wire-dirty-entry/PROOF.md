# Correlated dirt at a three-register wire meeting

This contribution was produced by Nick Petalas. Apache-2.0.

## Boundary and claim type

This is a scoped response-space proof and a finite local response construction.
It partially answers Matarener's PR6217 one-helper wire question. It neither
supplies nor excludes a complete one-helper program.

We cite PR6217's premises, without replaying its proof or census. For an A2
pair x,y the common seven-frame G has 24 retained ports. Its required rows
are proportional except at the third vertex z, where their ratio changes
sign. Every incoming six-frame contains at most 16 of these ports. The
content-in-frame rule confines incoming live coefficients to those ports.

The boundary has three incoming registers, one independent dirty scalar h,
and no further live reads, allocation, erasure or incoming registers during
the local meeting. Arbitrarily many rational linear local operations are
allowed. Two outputs must have the prescribed live responses and zero h
coefficient. Other initial public and helper columns are projected away.
This projection is necessary for a full program; sufficiency is not claimed.

## General kernel statement

Let K have characteristic different from two. Let C contain m ports with
distinguished z. Let e be a nonzero row supported only at z. Let c_z=0 and
c_t be nonzero for every t different from z. Put W=span(c,e). Suppose the
incoming registers are

    R_i = A_i X + b_i h,   i=0,1,2,

where b is nonzero, X has independent live coordinates, and each A_i has
support strictly smaller than m-1. Suppose local linear processing produces
c+e and c-e, both with zero h coefficient. Then:

1. At least two entries of b are nonzero. An isolated dirty helper with two
   h-free public inputs cannot suffice, regardless of the helper's live row.
2. If exactly two entries of b are nonzero, the sole h-free live row is a
   nonzero multiple of e. The dirty pair's live supports jointly cover all
   m-1 nonexceptional ports. If each support has size at most s, each dirty
   row contains at least m-1-s nonexceptional ports.

These are necessary conditions. They do not characterize the case where all
three inputs carry h. The support restriction is essential.

*Proof.* Every eventual register is a linear combination of the incoming
registers. Its h coefficient vanishes precisely when the combination lies
in ker(b^T), of dimension two. The rows c+e and c-e are independent because
2 is nonzero. Therefore the live-image map

    L: ker(b^T) -> K^C,   lambda -> sum_i lambda_i A_i

has image exactly W and is injective. If b_i=0, its coordinate vector lies
in the kernel. Thus A_i belongs to W and is nonzero. Every alpha*c+beta*e
with alpha nonzero has at least m-1 support positions, so such A_i must be
a nonzero multiple of e. Two h-free rows would make L noninjective. This
proves the first assertion.

For the second, let i be the clean index and j,k the dirty indices. A kernel
basis consists of the i-th coordinate vector and b_k times the j-th minus
b_j times the k-th. Their live images A_i and b_k A_j-b_j A_k span W. The
latter must have a nonzero c coefficient. At every t different from z,
at least one of A_jt,A_kt is consequently nonzero. Their union covers m-1
positions, giving each stated support lower bound. QED.

The proof even permits arbitrary linear readouts, without invertibility.
For PR6217, m=24 and s=16. Correlated dirt on at least two incoming rows is
necessary. If exactly two carry dirt, the clean row must already isolate z,
and each dirty row carries at least seven of the other 23 coordinates. This
is a concrete entry condition, not a claim that it can be prepared cheaply.

## Local response construction

The correlated-dirt escape is nonempty. Use literal port labels
x=11, y=19, z=487. Let G be the kernel of normals 11 and 19 in F2^9.
Add respectively normals 455 and 56 for six-frames H_0,H_1. Both normal
triples have rank three. Their port sections are complementary because
455 XOR 56=511 and every port has odd weight. The sections have sizes 16
and 8; z belongs to the former.

In the canonical gauge take the required rows G_x/2 and G_y/2 on these
24 ports. Here G_xy=1. Write these as c+e and c-e, where
e=(G_xz/2)e_z. Put a=c restricted to H_0 and d=c restricted to H_1.
Their support sizes are 15 and 8, and a+d=c. Supply

    R_0=eX,   R_1=aX-h,   R_2=dX+h.

Their live parts lie in the declared six-frames. Once they meet at G, use
these four scalar events:

    R_1 += R_2
    R_1 -= R_0
    R_0 *= 2
    R_0 += R_1

The exact endpoint is

    R_0=(c+e)X,   R_1=(c-e)X,   R_2=dX+h.

The scalar matrix has determinant 2. Reverse the four events, replacing
doubling by halving, to restore every incoming value. The helper may have
any h and retains its entrance value. This proves attainability of this
response projection with two dirty carriers and a singleton clean input.

The helper still contains dX at exit. This meeting preserves dX+h; it does
not restore the original h. Preparation of aX-h, dX+h and the singleton,
preservation of omitted public/dirty columns and later removal of dX are
not supplied. In particular, the scalar construction is not a complete
arbitrary-public-input endpoint or a favorable physical invoice.

## Decision and remaining obligations

Stop at this local result. Before expanding the architecture, identify the
pre-cut contact depositing -h into a public register, the singleton source,
all other dirty columns and the helper cleanup path. Preparation, native
delivery, restoration, precision, stock, compiler and caller costs are
unknown. None is treated as zero. There is no new kappa, supplier admission,
all-size theorem or selected-frontier change.

The proof holds over every field of characteristic different from two.
The P104 witness is rational and dyadic. A small F3 domain is finite
corroboration, not a formal proof-kernel certification.

## Credit

Matarener's PR6217 supplies the question, sign/capacity/two-source premises
and E8 interpretation. DreamingOfClouds's PR6170 supplies frame-contract
context. Retain the P104 carrier-code, native, helper, controller and caller
lineage credited there. Kernel dimension, support arguments and reversible
row operations are classical. The new contribution is their local
correlated-dirt consequence and explicit response construction.

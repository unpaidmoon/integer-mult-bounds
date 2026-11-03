# The exact paid period

Fix integers N>=2 and h>=0. There are two computational types and two
synchronized supplier modes. Their normalized moment matrices are

    A = diag(2, 1/2),
    B = diag(2^(-N), 2^(N-1)).

One mode is chosen for both types at each supplier layer. Every change of
mode inserts the recursive adapter G=2^h I. The schedule is a nonempty
cyclic word, repeated indefinitely. Its last-to-first change is charged.
The two computational types are required to contract simultaneously.

A supplier layer and an adapter layer are distinct recursive stages.
The period length below counts supplier layers. No adapter is omitted
from the matrix product or the integer child invoice.

## Theorem

The shortest word with a strict contraction has exactly

    L_min = (2h+1)(2N+1)

supplier layers. An attaining word is

    A^((2h+1)(2N-1)) B^(4h+2).

It has two cyclic changes and its complete product is I/2. Thus there is
no upper bound on the first profitable supplier period depending only on
the number of computational types and supplier modes, even at any fixed
nonnegative integer h. Both mode matrices individually have spectral radius
greater than one. This is a statement about this explicit rational family,
not an assertion about all switched systems or a selected supplier.

### Lower bound

Let x and y be the numbers of A and B layers, and let S be the number of
cyclic changes. All factors are diagonal, so the complete product is

    P = diag(2^(x-Ny+hS), 2^(-x+(N-1)y+hS)).                 (1)

For a positive diagonal matrix, a positive weight v with Pv<v exists
exactly when both diagonal entries are strictly below one. A pure word
fails: pure A expands the first coordinate and pure B expands the second.
Consequently x,y>=1 and S>=2. In fact S is even.

The exponents in (1) are integers. Strict contraction therefore requires

    (N-1)y+hS+1 <= x <= Ny-hS-1.

It follows that y>=2hS+2. Hence

    x+y >= Ny+hS+1
        >= N(2hS+2)+hS+1
         = (hS+1)(2N+1)
        >= (2h+1)(2N+1).

Equality at an exponent zero is insufficient. The proof uses this strict
integer gap, rather than accepting a critical cycle as a saving.

### Attainment

Put x=(2h+1)(2N-1) and y=4h+2. The displayed word has one A run and one
B run, so S=2 including its last-to-first boundary. Substitution into both
exponents in (1) gives -1. Its full product is therefore I/2, and
x+y=(2h+1)(2N+1). This proves both bounds.

## Unit forcing and every intermediate phase

The criterion is not obtained by dropping intermediate work. Let
D_0,...,D_(d-1) be the complete stage list of an attaining word, with both
adapters included. Here d=L_min+2 and every D_j is positive diagonal.
For each starting phase j define

    z_j = sum_(k=0)^(d-1) D_j D_(j+1) ... D_(j+k-1) 1,
    v_j = 2 z_j,

where the empty product is I and phase indices are cyclic. Every cyclic
product is I/2 since these factors commute. Thus

    v_j - D_j v_(j+1) = 2(1 - (I/2)1) = 1.                (2)

All reserves are finite positive rational numbers. Equation (2) gives a
strict positive-vector certificate for the phase-expanded recurrence,
including a unit forcing charge at every supplier and adapter stage.
Its finite-depth accumulated charges are bounded by these reserves, and
iteration over complete periods gives the exact infinite sum. A bounded
nonnegative forcing at each phase is covered by scaling v by the largest
forcing coordinate. Unknown or scale-dependent physical fees are not
covered by this observation.

This positive-vector method is classical and already appears in the
repository's A051, A054 and A055. The new assertion is the exact minimum
length of the stated paid family, not the certificate method.

## Integer child-rank realization of every stage

The entries can be actual moments of positive integer child lists with
proper descent. This does not construct operations computing a useful
supplier target. Fix any rational exponent s=p/q with 0<p<q. Choose an
integer t>=1 with pt>=N, and give every stage the same child size ratio

    1/M,   M=2^(qt).

A stage coefficient 2^e is represented by exactly 2^(pt+e) children of
the same computational type, each with that ratio. Its normalized moment is

    2^(pt+e) (1/M)^s = 2^e.

The exponents e used by A, B and G are 1,-1,-N,N-1,h. The smallest is -N,
so every multiplicity is a positive integer. M>1 gives proper descent.
The adapters use the same rule with e=h for both coordinates. They are
recursive work, rather than free changes of labels.

For an attaining schedule with d=L_min+2 stages, both computational types
have exactly 2^(ptd-1) descendants after a complete period, each with size
ratio 2^(-qtd). On period-aligned sizes the resulting homogeneous recurrence
has exponent

    s - 1/(qtd).

A unit toll at each stage only changes the finite macro toll. In particular,
N=2,h=1,s=1/2,t=2 gives M=16, mode child counts A=(8,2), B=(1,8), and
adapter counts G=(8,8). Its first profitable supplier word has 15 layers
and two adapters. The full macro has 2^33 descendants at ratio 2^(-68),
so its exponent is 33/68. These are abstract branching recurrences.

## Scope

The theorem assumes a synchronized mode for both types, a cyclic schedule,
and the specified diagonal recursive adapters. Allowing each type to select
its own mode removes this particular obstruction: type one can select B
and type two can select A. The theorem does not constrain that controller.
The phase-expanded type dimension grows with the period. No dimension-only
bound for a fixed full phase-expanded matrix is refuted.

The parameters N and the matrix bit lengths grow together. There is no
claim that every fixed finite input family requires an unbounded period,
or that no input-dependent search bound exists. Integer child moments do
not provide native operators, dirty-state restoration, ownership, physical
adapters, precision, storage, or an outer multiplication algorithm. A real
supplier must supply all of those costs and contracts separately.

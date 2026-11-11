# Exact heterogeneous three-source clean-row tariffs

This contribution was produced by Nick Petalas. Apache-2.0.

## Contract and theorem

Use the paid extra-row contract of Ali Romman's [PR5372](https://github.com/CrocSwap/integer-mult-bounds/pull/5372),
specialized to three immutable source rows. That contract builds on Cinna
Davis's PR1954 extension of Ross Richardson's PR943 connector. All spaces
are nonzero finite-dimensional vector spaces over F2, with compatible maps.
Allocate one owned row c, explicitly pay for zeroing it, and then allow only

```
B_j: c   += B_j x_j                  j = 0,1,2
A_m: y_m += A_m c                    m = 1,...,7.
```

The seven masks are their usual three-bit binary expansions. Each complete
call restores its private scratch and heads. The original dirty connector
is unused and preserved. Sources are never changed; outputs can be arbitrary
dirty values and are never read. No observer examines an intermediate output.
At exit require c=0 and, for every m,

```
y_m(out) = y_m(in) + A_m sum_{j: bit j of m = 1} B_j x_j.
```

The same fixed finite word must work for every choice of maps and input data.
It may depend on prices, not on special map identities or data. In particular,
the minimum below is generic, not a lower bound on a particular degenerate
assignment of maps. There is one allocation/zeroing/release lifetime. Another
zeroing operation, extra row, source update or output-to-source call changes
the alphabet and contract.

Let b_j>0 be the complete price of B_j and a_m>0 that of A_m. These ten prices
are independent real numbers. Write

```
E = {3,5,6},   O = {1,2,4,7},
beta = min_j b_j,   alpha_E = min_{m in E} a_m,
alpha_O = min_{m in O} a_m.
```

**Theorem.** The exact complete-map-call optimum over all finite legal words is

```
OPT(b,a) = 2 sum_j b_j + sum_{m=1}^7 a_m
           + min(2 beta, alpha_E + alpha_O).
```

Add the same fixed allocation, zeroing, release and admission bill to every
schedule. Any per-call charges constant for each identifier can be included
in its b_j or a_m. Word-dependent physical preparation, routing or storage
charges are outside this tariff theorem. No such charge is set to zero in
a supplier comparison, because no supplier comparison is claimed here.

More precisely, there are exactly fifteen componentwise-minimal ten-component
call-count vectors. Twelve have source counts (2,2,2) and output counts one
except for an arbitrary pair (e,o) in E x O, whose counts are two. The other
three have output counts all one and source counts (4,2,2) in any coordinate
order. Every legal vector componentwise dominates one of these fifteen.

## Lower bound for every finite word

Specialize all maps to identity on one common scalar coordinate and set all
other coordinates to zero. This is an allowed specialization of the universal
contract. If a chosen space has larger dimension, use maps that transport
just this coordinate. Track the source-coefficient mask p of c. Every source
call toggles exactly one bit of p, every output call adds the current p to that
output's formal coefficient, and the source walk starts and ends at zero.

Each source must be used: otherwise its singleton target cannot depend on it.
Restoration makes its count positive and even, hence at least two. Every
output needs at least one readout. The source length L is consequently even
and at least six. If a mask m is never visited, its output needs at least two
readouts, since one readout could only contribute a visited mask. Extra calls
cannot weaken any of these lower bounds.

If L=6, every source count is two. The closed cube walk alternates even and
odd Hamming-weight parity. Its six positions before the final repeated zero
contain three even and three odd positions, whether or not vertices repeat.
At most three of the four odd vertices are visited. At most three of the
four even vertices are visited, and zero is one of the visited even vertices.
There is therefore an unvisited e in E and an unvisited o in O. The vector
dominates the stated six-source-call profile for that pair, and its cost is
at least

```
2 sum b_j + sum a_m + a_e + a_o
    >= 2 sum b_j + sum a_m + alpha_E + alpha_O.
```

If L>=8, some source count is at least four, with the other two at least two.
All output counts are at least one. Its vector dominates the stated eight-call
profile with that source coordinate repeated four times, so its cost is at
least

```
2 sum b_j + sum a_m + 2 beta.
```

These two cases cover unbounded word lengths. No census cutoff, assumption of
a simple walk, restriction to paired readouts, or minimum-price assumption is
used in the lower bound.

## Attainment for arbitrary linear maps

For the eight-source-call family use the classical reflected Gray cycle

```
0,1,3,2,6,7,5,4,0.
```

Its source counts are (4,2,2). Permute coordinates to repeat a cheapest source
four times, and call each A_m once at vertex m. This attains the eight-call
branch. The Gray cycle is classical, and PR5372 already gives its general-n
clean-row use. This contribution does not claim that construction as new.

For the six-call family choose e minimizing the even output price and o
minimizing the odd output price. There is a six-cycle through the other six
vertices, including zero, with each source toggled twice. Coordinate
permutations reduce the twelve pairs to the following three templates:

| Omitted pair (e,o) | Cycle |
|---|---|
| (3,1) | 0,2,6,7,5,4,0 |
| (3,4) | 0,1,5,7,6,2,0 |
| (3,7) | 0,1,5,4,6,2,0 |

Indeed e has weight two. If o has weight one, it is either inside or outside
e's support, giving the first two templates. The remaining odd vertex is 7,
giving the third. This proves coverage of every pair without relying on an
executable enumeration.

Read every visited nonzero output at its matching vertex. For an omitted
mask m, the visited set V has size six in the eight-element group F2^3.
Since |V|+|V+m|=12>8, choose u,v in V with u+v=m. They are distinct. Neither
can be zero because m is omitted. Read A_m once at each of u and v. Linearity
gives A_m(c_u)+A_m(c_v)=A_m(c_u+c_v). At a source prefix p, induction on the
actual source calls gives c_p=sum_{j in p} B_j x_j. These two readouts therefore
give exactly the requested A_m sum_{j in m} B_j x_j. This uses no invertibility,
commutation of A and B maps, or equality of row dimensions. Output updates
can be scheduled at first arrival because outputs are never read.

Thus the two omitted outputs have count two; the five visited nonzero outputs
have count one. Every source has count two and the owned row returns to zero.
All original source/dirty boundaries and arbitrary incoming outputs are
preserved. This attains the six-call branch.

All fifteen profiles are attainable and no one dominates another: two six-call
profiles trade different doubled outputs; two eight-call profiles trade the
repeated source; across families, fewer source calls trade for extra readouts.
Combined with the lower bound, this proves the complete componentwise frontier.
Each profile is also the unique cheapest profile for some strictly positive
price vector. For a six-call profile, set its doubled-output prices to one,
the other output prices to four, and all source prices to ten. For an
eight-call profile, set its repeated-source price to one, the others to two,
and all output prices to four.

For uniform b_j=b and a_m=a this specializes to

```
OPT = min(6b+9a, 8b+7a).
```

Hence PR5372's b=10,a=1 example of cost 69 is optimal, and its price boundary
a=b is exact in this three-source case. This is a new optimality conclusion;
the predecessor's example and Gray cycle remain predecessor work.

## Finite corroboration and its limits

The written proof establishes the real-price and unbounded-word quantifiers.
The exact standard-library checker adds independent finite corroboration:

- Enumerate all 9841 source words of lengths zero through eight. Exactly 1350
  restore and use all three sources. An independent subset-XOR computation
  gives their optimal readout counts, producing 220 distinct vectors and
  exactly the fifteen claimed minimal vectors.
- Independently price source walks on states (current vertex, visited set).
  There are at most 8*128=1024 states. Positive edge costs justify Dijkstra;
  at most three relaxations per settled state bound heap pushes by 3073.
  For each final visited set, enumerate all at most 128 subsets of its
  nonzero vertices to minimize each output's readout count. This construction
  permits arbitrary source lengths and arbitrary readout multiplicities;
  it does not import the theorem's six/eight-call classification. Compare
  the optimum on 3456 integer price tuples and 24 exact rational tuples.
- Execute the fifteen actual words with rectangular 3-by-2 source maps and
  2-by-3 output maps, including dirty target/connector inputs and arbitrary
  pre-zeroing owned data. The stated 10320 cases count executions, not
  distinct matrices. Check all 26 input basis columns, zero and sixteen
  mixed states for each of sixteen map assignments and fifteen words.
- Reject 112 malformed-price, missing-allocation/release, lifetime, source,
  readout and semantic deletion controls. All checks remain active under -O.

The source-word enumeration does not by itself exclude longer words. The
written lower bound and the separate finite-state shortest-path reduction
explain their different coverage. No predecessor scientific suite is replayed
as the deliverable. Independent human and formal proof-kernel review are
unclaimed.

## Implementation constraints

All new code is package-local, has no recursion, writes no files, invokes no
subprocess, and uses exact integers/Fraction values. The fixed three-source
domain bounds every loop and collection. `profile` checks explicit witnesses
of at most 128 operations; this implementation guard does not limit the
mathematical theorem. All internal semantic checks use explicit exceptions.
No function exceeds sixty physical lines. The only indirect calls are bounded
standard-library ordering keys; there is no runtime code generation.

Power of Ten rule 3 deviation: CPython and its standard library allocate
objects during checking, so fixed allocation after initialization is not
available. The scope is these finite offline checks. The oracle holds at most
1024 distance states and 3073 heap pushes, source enumeration visits exactly
9841 words of length at most eight, and all other collections have the fixed
bounds above. Warning-strict normal/optimized replay and the capacity guards
check this bounded behavior. If this checker becomes a service or accepts a
variable source count, replace these fixed-domain structures with explicit
resource admission before widening the domain.

Power of Ten rule 10 deviation: no static type checker or linter is installed
in the required interpreter environment. This package changes no shared
build configuration. Warning-strict AST compilation and normal/optimized
registered replay are the available diagnostics. Add an agreed static checker
if the repository adopts one; this is not a claim of static type verification.

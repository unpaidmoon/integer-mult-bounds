# A single merged cache cannot improve reader 497

Scoped written proof with exact finite corroboration. No new kappa.

Mixing the two operands does not evade the reader-497 obstruction in the
single-merge model defined below. For H_r=r^t, 0<t<1, its exact optimistic
minimum is

    min(H1+2H3+2H6, 2H1+3H3+H5).

The unchanged bill is 2H1+2H3+H5. The exact excess is

    min(2H6-H1-H5, H3) > 0.

This closes one mixed-cache route explicitly left outside Jerry Chen /
CubeJerry's [PR6248](https://github.com/CrocSwap/integer-mult-bounds/pull/6248).
That result keeps the two caches separate. Here they descend to a common
frame, form V+B once, and deliver that sum to the ascending reader. Every
native cache MOVE is charged. This is a new representation and tariff proof,
not a replay of the predecessor's numbers.

## General result and scope

Let S,U,H,L,R have dimensions s,u,u+1,1,u+1, with 1<=s<u,
H intersection R=U, S,L<=U and L not contained in S. Operand caches start at
S and U, descend to M<=S and merge once. Their sum descends to A<=M and is
received once. The reader ascends from zero to R. The uncloned root descends
from H to L and meets the reader once at F. The public logical endpoint is
A_in+V+B-4Q, with arbitrary dirty public inputs preserved as specified.

For any nonnegative increasing concave tariff phi with phi(0)=0, the exact
minimum in this relaxation is

    min(phi(1)+2phi(u)+phi(s)+phi(u-s),
        2phi(1)+phi(s)+2phi(u-s)+phi(u-1)).

The proof covers every field, permitted subspace and finite monotone path.
Its two attaining flag recipes are (a,m,f)=(0,s,1) and (s,s,u), where a,m,f
are the dimensions of A,M,F. [PROOF.md](PROOF.md) gives the argument.

Waiting, capture, clean storage, merging, disposal and ordinary control are
optimistically free. Disposal may discard arbitrary cache values. Therefore
attainment is an attainment of this tariff relaxation, not a physical erasure
program. Extra nonnegative implementation costs cannot repair its loss.

No extra source reads, repeated merging/splitting, public ascending caches,
root clones, changed targets or coordinated deletions are allowed. More
general linear recoding is not excluded. The source geometry in PR6248 is
inherited, not independently audited; this package does not replay PR6167.
Native phases, physical delivery, owned erasure, caller, compiler, precision,
tape and analytic recovery remain unproved here. The selected frontier and
its five framework assumptions are unchanged.

## Evidence and reproduction

The standard-library verifier constructs all 50 dimension recipes for s=3,u=6.
It extracts MOVE ranks from explicit binary flag witnesses independently of
the symbolic invoice formula. All six capped sums for each recipe dominate
the appropriate attaining endpoint. This proves a finite concave-order
certificate for those recipes. Broader corroboration checks 20,839 recipes
over 91 dimension pairs with 2<=u<=14 and 1<=s<u. The all-dimension result
rests on the written proof, not extrapolation from those checks.

Four public basis columns and 81 rational dirty examples check the relaxed
scalar payload. Thirteen controls test illegal incidence, unpaid transport,
missing operands/root and lost incoming dirt or cache cleanup. These scalar
checks do not verify native operators.

From the repository root, using CPython 3.12:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/p104-single-merge-cache-floor/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/p104-single-merge-cache-floor/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/p104-single-merge-cache-floor
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/p104-single-merge-cache-floor --check-source-history
```

Both modes report `PASS_SINGLE_MERGE_CACHE_FLOOR`. An optional
`--receipt /absolute/path/outside/checkout/receipt.json` writes the generated
50-recipe certificate, interpreter version and hashes of all seven package
files. Receipts, exports and run logs are not committed.
[VALIDATION.md](VALIDATION.md) records actual checks and their limits.

## Open next questions

Can a cache representation with splitting and more than one merge change the
complete signed bill? It would escape the single-delivery reduction and could
change the useful next construction. Start with one chronological diagram
whose values, source captures, all cache MOVEs and erasure are explicit.
The blocker is a physically legal, fully charged delivery contract. No such
construction is supplied or reserved here.

## Sources, credit and coordination

This contribution was produced by Nick Petalas. Apache-2.0. Independent human
and formal proof-kernel review are unclaimed.

Jerry Chen / CubeJerry's PR6248 at
`9aaf76f43493cd2392eaae248274c651f29bc28e` supplies the mixed-source question
and source geometry. Its proof is available at the
[pinned source](https://github.com/CubeJerry/integer-mult-bounds/blob/9aaf76f43493cd2392eaae248274c651f29bc28e/research/p104-reader497-cache-floor/PROOF.md).
Ali Romman retains [PR6167](https://github.com/CrocSwap/integer-mult-bounds/pull/6167)
and the retained-operand construction at
`564a076b113621a93edc4e39968ee4e4a8c9caf0`. DreamingOfClouds retains
PR6144/PR6030/PR5907 and toolkit PR6170 credit. Matarener retains PR6214's
independent audit and handoff. The native, caller, compiler, BIT and earlier
P104 contributors retain their existing attribution. No predecessor source
files or credit lines are changed.

The scientific base is canonical main
`2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8. The selected
binding-only orientation passes at conditional kappa .003125804. The
[advance claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19291954)
defines this scope. The 316-open-PR and 5,998-Discussion-record cache, main
README and merged searches, recent account work and local reservations found
no competing single-merge result. The sparse overlap helper searches 99 of
8,722 main note records; separate Git README searches cover the omitted main
files for the distinctive terms. This is bounded overlap coverage, not a
proof of novelty. Frozen provenance is in [SOURCES.json](SOURCES.json).

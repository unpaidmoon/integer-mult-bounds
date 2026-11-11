# An exact integer dirty-fanout tariff beyond finite-ring shortening

This contribution was produced by Nick Petalas. Apache-2.0.
Independent human and formal proof-kernel review are unclaimed.

**Claim type: scoped proof with exact finite corroboration.** For two arbitrary
dirty integer rows a,b and one preserved source p, require
`A=a+5p, B=b+12p`. Permit only integer source insertions and integer scaled
row additions, at uniform positive prices mu and c respectively. All dirt
must return, with no extra row, free scale or free basis change. The exact
minimum over arbitrary finite input-independent words is

```text
OPT = min(2 mu, mu + 6 c).
```

At mu=10,c=1 the optimum is 16. Formally extending the five-term finite-ring
formula would give 14. This is a sharp obstruction to that extension; the
predecessor's finite-ring theorem remains outside the claim being proved.

[PROOF.md](PROOF.md) proves the unrestricted coefficient and word-length
statement. With one insertion, the suffix must have primitive column
plus or minus (5,12). Every two-shear integer column has a coordinate one
or has one coordinate congruent to one modulo the other. Neither target
sign passes. Dirt restoration requires the inverse prefix, giving at least
six paid row additions. The following chronological word attains that bound

```text
B -= 2A; A -= 2B; B -= 2A; A += p; B += 2A; A += 2B; B += 2A.
```

Two direct insertions attain the other branch. The proof applies to every
positive row width by exact equality of the full coefficient operators.

## Evidence and reproduction

From the repository root with CPython 3.12 and the standard library

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/integer-fanout-shortening-gap/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/integer-fanout-shortening-gap/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/integer-fanout-shortening-gap
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/integer-fanout-shortening-gap --check-source-history
```

On another host substitute its CPython 3.12 executable. The direct verifier
prints `PASS_INTEGER_FANOUT_SHORTENING_GAP` inside a generated JSON receipt
bound to all six package files. It writes no files. The registered runner
prints `PASS_REGISTERED_RESEARCH_PACKAGE`. No receipt is handwritten.

The verifier checks both complete 3-by-3 dirty/source operators and the
attaining inverse, literal integer input fixtures, rational price fixtures
and semantic mutations. A complete modulo-60 column census includes every
residue coefficient in both directions through two shears. A separate
normal-form calculation produces the same reachable sets. Both signed
columns are absent from both origins. Reduction maps every integer word
into that quotient, making this a finite certificate of the local lower-bound
step. The universal tariff still uses the written insertion-count proof.
The generated receipt supplies the exact enumerated counts.

The local replay enumerates 1,458 dirty-input executions, 729 rational
price pairs, 1,617 reachable quotient columns per origin and 14,400
quotient transitions across both searches. All sixteen semantic rejection
controls pass. Normal and optimized receipts agree exactly.

## Source, credit and overlap

Credit Ali Romman's [PR5312](https://github.com/CrocSwap/integer-mult-bounds/pull/5312)
for the finite-ring five-term tariff and its explicit infinite-ring boundary,
lee-phys's PR5139 for the finite-commutative formula, Krzysztof Wojt's PR5045
for the insertion/return classification, Ross Richardson's PR3121 for the
dirty-fanout lineage, Nick Petalas's PR4916 for the older unit-demand ring
contract, and Ali Romman's PR5310 for finite-module shortening. Their
predecessor credits remain intact. No predecessor executable or scientific
census is replayed as this contribution. Elementary matrices, Euclidean
arithmetic and Bezout identities are classical; global literature priority
is unclaimed.

Base canonical main is `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority
revision 8. [Advance claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19294861).
[SOURCES.json](SOURCES.json) pins the finite-ring README as context, not as
a mathematical dependency for the integer proof. The source PR head is
`5cbdbc8e3858e67c8bfbd160f742ef1e9ced9d38`. TASK.json explicitly changes the
connector-alphabet card to this scoped interface side result. Its first
945-pairing control and the selected source-binding orientation passed.

Live handoffs, active Discussions, current open PRs, recent account work,
local reservations and distinctive main/merged searches were checked.
No same-demand integer shortening result was found in that coverage.
Recent three-row Boolean and directed-cycle tariff results have different
row/topology contracts. Sparse local notes, arbitrary historical diffs and
unpublished work remain coverage limits. No novelty guarantee follows.

## Limits and implementation bounds

This proves an abstract exact tariff under the stated arithmetic and price
contract. It supplies no physical caller, rounded implementation, recursive
invoice gain, new kappa or complete multiplication theorem. The selected
frontier and five framework assumptions retain their status. No selected
cold replay, native suite, Lean or Docker build was run.

The checker has fixed domains: 3-by-3 matrices, words of at most eight gates,
coefficients of magnitude at most twelve, 9^3 input triples, at most 40^2
price fixtures, and two depth-two searches in a 60^2-state quotient. These
are checker capacities, not bounds on the theorem. The proof covers arbitrary
integer coefficients and word lengths. There is no recursion, subprocess,
network access, dynamic code or writable output. Every function fits below
sixty lines. Explicit guards remain enabled under optimized Python.

Power of Ten rule 3 has a managed-runtime deviation: CPython allocates
integers, fractions and bounded collections. At most 3600 quotient states
and six one-MiB file reads constrain live data. No allocation-free runtime
claim is made. A fixed-buffer port would be needed if that becomes a host
requirement. Warning-strict normal/optimized runs and available static
analysis provide the interpreted-code diagnostics.
No separate Python linter is installed; source compilation and a static
function-length inspection also pass, with a largest function of sixteen
lines.

## Open next questions

- Can one-insertion restoration require arbitrarily many row additions for
  primitive integer demands? This determines whether a finite shortening
  allowance needs an unbounded replacement. Start with signed Euclidean
  paths and include their inverse-prefix costs. A general shortest-column
  classification is not supplied here.
- Does a real helper caller enforce integer coefficients and supply complete
  coefficient-independent prices? Pin its arithmetic, source access, frames,
  precision and tape contract before using this tariff. No such caller or
  favorable complete invoice is supplied here.

These questions are recorded in TASK.json. Stop at this first exact result.

# Sharper reversible phase lifting by changing one tie rule

This contribution was produced by Nick Petalas. Apache-2.0.

**Claim type: scoped proof with exact finite corroboration.** For the rational
phase (3+4i)/5, changing the final half-integer tie direction in the standard
three-shear lifting program reduces its sharp all-grid squared error from
h² to **(4/5)h²**, where h is the grid spacing. The new map and its inverse
are exact bijections of the full grid. Both opposite-tie choices attain 4/5;
both same-tie choices attain 1. The optimum is over these four fixed tie pairs.

```text
u = x - ceil(y/2)
v = y + nearest(4u/5)
w = u - floor(v/2)
return (w,v)
```

[PROOF.md](PROOF.md) proves periodicity of the residual on 5Z × 10Z,
reducing the all-grid statement to 50 representatives per program. It gives
the full residual table, equality at (0,3), exact inverse and sharp additive
radial allowance 2h/sqrt(5). The program can move outward and does not preserve
each closed disk. For example (-5,-7) maps to (3,-9), increasing squared
radius from 74 to 90.

## Predecessor and new step

ywz65's [PR2589](https://github.com/CrocSwap/integer-mult-bounds/pull/2589)
supplies the standard reversible lifting control, a sufficient squared-error
bound 153/80, and the complete-disk obstruction. Its valid bound is cited,
not disputed. Classical three-shear lifting is not claimed as new. This
contribution changes one rounding rule and proves the correlated exact error
and fixed-family optimum. No predecessor mathematical verifier is imported
or replayed. Retain ywz65's PR2527/PR2549, Mason Hale's PR2313 quantizer,
Jose Manuel's PR2298 phase context and the source's classical lifting credit.
[SOURCES.json](SOURCES.json) binds the cited README and model as provenance.

The `uniform-transfer-audit` card is explicitly **changed** to this generic
precision interface side result. The original card asks for an actual selected
caller and is not discharged. Current main was
`2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8; the baseline
binding check passed at selected conditional kappa .003125804. The
[advance CLAIM](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19299721)
names the phase, four tie pairs and first-improvement stopping rule.

## Reproduce

From the repository root, with CPython 3.12 and the standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/reversible-phase-tie-optimum/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/reversible-phase-tie-optimum/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/reversible-phase-tie-optimum
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/reversible-phase-tie-optimum --check-source-history
```

An equivalent CPython 3.12 interpreter works elsewhere. The direct verifier
is standalone and prints a generated JSON receipt with status
`PASS_REVERSIBLE_PHASE_TIE_OPTIMUM`, all residual tables and SHA256 hashes of
the six package files. `--output NEW_PATH` exclusively writes that receipt;
normal replay leaves files unchanged. No hand-written receipt is supplied.

The replay covers all 200 fundamental cases, 26,244 signed-grid cases with
both inverse compositions and both error directions, 5,600 signed translations
with shifts through 4,096 bits, eight radial-family instances, eight semantic
controls and six invalid tie-rule rejections. A separate Fraction/divmod
nearest-rounding implementation checks all fundamental and large-translation
cases. The written periodicity proof establishes the unbounded quantifier;
the wider sweeps are implementation evidence.

## Limits and implementation discipline

Optimality is restricted to the four specified constant tie policies. It does
not cover input-dependent policies, other factorizations or all lattice
bijections. The phase is a generic rational kernel input, not an identified
selected root. No physical quotient workspace, overflow/word-width budget,
phase-generation tariff, repeated-word error accumulation, native realization,
complete signed invoice or new kappa is supplied. The five selected framework
assumptions remain. Independent human and formal proof-kernel review are unclaimed.

The verifier has no recursion or unbounded search. Each function is under
60 lines. Loop bounds are the stated finite fixture sizes, at most 26,244
grid cases and 5,600 large translations. Python integer and Fraction allocation
is a managed-runtime deviation from static allocation. The largest retained
set has at most 6,561 image pairs; large tests use integers of at most 4,120 bits
and stream each case. The eight semantic checks and six rejected calls are
fixed. The verifier-owned indirect targets are the two explicit forward/inverse
functions in the invalid-input checks. Warning-strict normal and optimized
checks supply the available diagnostics without changing shared tooling.

## Open next questions

1. Can a phase actually required by a rounded supplier use this exact residue
   analysis to reduce its complete precision allocation? First bind one literal
   phase and its allowed outward headroom. An actual selected caller, bounded
   integer storage and the physical quotient/return tariff are missing here.
2. Can a reversible rounding program outside these four fixed tie pairs attain
   a smaller all-grid error for the same phase? First formulate a finite residue
   matching problem with an explicit inverse. No optimality beyond the stated
   four-program family is proved.

The structured relevance, first steps and blockers are in [TASK.json](TASK.json).

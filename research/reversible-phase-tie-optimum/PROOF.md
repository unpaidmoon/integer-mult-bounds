# A sharp tie choice for a reversible rational phase

This contribution was produced by Nick Petalas. Apache-2.0.

## Statement

Let h>0 be the grid spacing, and let R be multiplication by (3+4i)/5.
Use integer numerators x,y for a point h(x+iy). Define

```text
u = x - ceil(y/2)
v = y + nearest(4u/5)
w = u - floor(v/2)
F(x,y) = (w,v).
```

There are no half-integer ties in nearest(4u/5). Then F is a bijection of
Z² and

    ||h F(x,y) - R h(x,y)||² <= (4/5) h².                 (1)

The constant is attained. The inverse has the same sharp error bound
relative to R inverse. Among the four programs obtained by choosing a fixed
upward or downward half-integer tie direction independently in the first
and last shear, the minimum squared error constant is exactly 4/5.
Both opposite-tie programs attain it. Each same-tie program has sharp
constant 1. This is optimality within four specified programs, not among
all reversible rounding algorithms or lattice bijections.

The standard rounded-shear factorization is predecessor work. The new step
is the correlated residue calculation and the improved tie choice, together
with its sharp all-grid guarantee. PR2589 gives the same-tie lifting control
and the valid sufficient bound 153/80. That bound is cited, not disputed.

## Exact inversion

Each update changes one integer coordinate by a function of the unchanged
coordinate. Undo the updates in reverse order, with the same rounding rules:

```text
u = w + floor(v/2)
y = v - nearest(4u/5)
x = u + ceil(y/2).
```

Thus both compositions with F are identity on the entire integer grid.
No input-dependent history, additional output or clean helper is needed
in this logical two-coordinate map. This statement does not price evaluation
or erasure of a physical quotient instruction's workspace.

## Finite quotient proves the all-grid bound

Write a,b in {0,1} for the first and last tie directions. Rounding n/2 is
floor((n+a)/2), and nearest(4u/5) is floor((8u+5)/10). Let F_ab be this
three-update program. For every integer input, direct substitution gives

    F_ab(x+5,y)  = F_ab(x,y) + (3,4),
    F_ab(x,y+10) = F_ab(x,y) + (-8,6).                  (2)

For the first relation, u increases by 5, the middle rounded increment
increases by 4, and the last rounded half increases by 2. For the second,
u decreases by 5, v increases by 6, and the last half increases by 3.
These are exact integer shifts for either tie direction, including negative
inputs. The displayed output shifts are R(5,0) and R(0,10). Consequently

    E_ab(x,y) = 5 F_ab(x,y) - (3x-4y, 4x+3y)

is periodic on the lattice 5Z × 10Z. Every integer input has one unique
representative in 0<=x<5, 0<=y<10. There are exactly 50 cases per tie pair.
This is a mathematical reduction to a finite quotient, rather than an
inference from a bounded input sweep.

For the chosen pair a=1,b=0 the complete residual table is

| Residual E | Number of representatives | Squared length |
| --- | ---: | ---: |
| (-2,-1) | 5 | 5 |
| (-1,-3) | 5 | 10 |
| (-1,2) | 5 | 5 |
| (0,0) | 10 | 0 |
| (1,-2) | 10 | 5 |
| (2,-4) | 5 | 20 |
| (2,1) | 5 | 5 |
| (3,-1) | 5 | 10 |

Each row follows by substituting the 50 representatives into the displayed
integer formulas. The verifier emits all residuals and their multiplicities
and compares each evaluation with a separate rational nearest-rounding
implementation. The maximum residual squared length is 20, proving (1).
For example, F(0,3)=(-2,1), with E=(2,-4), proves equality.

The analogous four-program calculation is

| First tie | Last tie | Maximum squared residual | Equality input | Output |
| --- | --- | ---: | --- | --- |
| Down | Down | 25 | (0,5) | (-3,3) |
| Down | Up | 20 | (0,7) | (-6,5) |
| Up | Down | 20 | (0,3) | (-2,1) |
| Up | Up | 25 | (0,3) | (-3,1) |

The error squared is h²||E||²/25. This proves sharpness and the stated
four-program minimum. For any output z=F(x), orthogonality of R gives

    ||F inverse(z) - R inverse(z)|| = ||F(x) - R(x)||.

Surjectivity of F transfers both the upper bound and its attainment to the
inverse. A separately rounded conjugate recipe is not assumed to be this
inverse.

## Outward slack and the disk boundary

The triangle inequality gives, uniformly over all inputs,

    ||h F(x,y)|| <= ||h(x,y)|| + (2/sqrt(5)) h.          (3)

This additive radial constant is also sharp over the full integer grid.
Take x_n=(-5n,3-10n), n>=1. Formula (2) and the equality input give

    F(x_n) = (5n-2,1-10n),
    ||x_n||² = 125n²-60n+9,
    ||F(x_n)||² - ||x_n||² = 20n-4.

Rationalizing the difference of norms shows that it tends to
20/(2 sqrt(125)) = 2/sqrt(5). This proves sharpness of (3) without a
numerical approximation. In particular x_1=(-5,-7) has squared norm 74
and image (3,-9) of squared norm 90. Exact return requires permitting this
outward motion. No claim is made that the same constant is minimal on the
particular disks with radius exactly 2^p in numerator units.

## Scope and credit

ywz65's
[PR2589](https://github.com/CrocSwap/integer-mult-bounds/pull/2589) and
`research/reversible-phase-disk-obstruction/model.py` supply the standard
rounded-shear control, the complete-disk return boundary and the question
of which changed interfaces can support reversible phases. Retain ywz65's
PR2527/PR2549, Mason Hale's PR2313 quantizer, Jose Manuel's PR2298 phase
context and the classical shear-lifting lineage credited there. No source
code is imported or vendored here. SOURCES.json pins the cited definitions
as provenance at the package base commit.

The written periodicity argument and exhaustive 200-case arithmetic are
the scoped proof. Wider signed-grid, large-integer and semantic mutation
checks corroborate its implementation. Independent human and formal
proof-kernel review are unclaimed. A rational phase is a valid generic
phase-kernel input; it is not identified with a selected supplier root.
This result does not resolve precision_tape at an actual selected caller,
discharge an inherited framework assumption or improve kappa.

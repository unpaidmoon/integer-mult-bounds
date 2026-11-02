# Full-column entry and the exact cleanup query at the 11/19 meeting

Prepared for @CubeJerry by coordinated OpenAI Codex research worker B,
with a separate assisted mathematical check. Apache-2.0.

## 1. Exact scope

Matarener's PR6217 studies the P104 "lives as wires" architecture. Nick
Petalas's PR6261 at `1866c2f3ee2d4cf5bf3e8f008883a6605ab10ed3` proves a
correlated-dirt entry condition and supplies a four-event **response
projection**, explicitly leaving other public columns and cleanup open.
Nothing here contradicts that qualified claim.

Keep its meeting x=11, y=19, z=487, seven-frame G=ker(11) intersect ker(19),
and six-frames H0=G intersect ker(455), H1=G intersect ker(56). Let X have
104 independent live coordinates. On the 24 ports in G the required Gram/2
rows are c+e and c-e, where e is supported only at z and every other entry
of c is nonzero. Write U=P(H0), V=P(H1), a=c restricted to U, d=c restricted
to V. Exact reconstruction gives disjoint U,V of sizes 16,8 with z in U,
a+d=c, and Gram(11,19)=1, Gram(11,487)=1, Gram(19,487)=-1. Thus 2eX=X487.

Let Y be the partner's independent original symbol and h the helper's.
The demanded responses are P=Y+(c+e)X and W=(c-e)X. This is a common-chart
linear boundary, not an identified selected-caller subword. The exact
fixture retains all 104 X columns, all 104 Y columns and h; unrelated
columns remain spectators. Componentwise validity for vector-valued fields
does not certify native frame implementations.

## 2. The sole h-free arrival has a forced ratio

Work over a field of characteristic different from two. Consider three
arrivals with exactly two nonzero h coefficients, no further reads,
allocation or erasure. Suppose linear processing produces P and W. If
the sole h-free arrival is R0=kY+A0X with support(A0)<23, necessarily

    k != 0,    A0=2k e.                                  (1)

The two dirty arrivals may also carry Y; merely copying Y into them does
not remove this condition.

**Proof.** The h-annihilating coefficient space has dimension two. Since
P,W are independent, its image is exactly span(P,W), and the image map
is injective. Thus R0 is a nonzero alpha P+beta W. Its live part is
(alpha+beta)c+(alpha-beta)e. The support bound forces beta=-alpha.
Consequently k=alpha is nonzero and A0=2k e. QED.

For the specialization with no other Y carriers and normalized h signs,

    R0=Y+A0X,    R1=A1X-h,    R2=A2X+h,

P,W are reachable if and only if

    A0=2e,    A1+A2=t(c-e),    t != 0.                    (2)

Every h-free/Y-free output is proportional to R1+R2, proving necessity;
normalize this sum by 1/t to obtain W, then add W to R0. This is an
arbitrary-readout statement. The two-ADD tariff below is for t=1 only.

At a partner following the strict minimal {0}->G path, with no imported
owned live component or pre-cut X access, the live part at G is zero.
Such an entry cannot satisfy (1). A public ADD at {0} cannot supply a
nonzero live port. Extra access or a changed meeting is required. This
does not exclude every one-helper architecture.

## 3. Full-column two-ADD attainment

Prepare R0=Y+2eX, R1=(a-e)X-h, R2=dX+h. Their live supports have sizes
1,16,8 and lie in the same two six-frames as the predecessor. Execute

    R1 += R2
    R0 += R1.

The endpoint is (P,W,dX+h). The triangular scalar matrix has determinant
one; reversing the two ADDs restores every arrival. Two writes are sharp
for these entries and these destination registers in the elementary
single-target ADD/SCALE alphabet: both demanded output registers differ
from their arrivals. This is not unrestricted circuit optimality.

The singleton preparation has a named source contact. While X487 is pure
at its initial line L=span{487}, move the partner {0}->L, perform
Y += X487, then move L->G. L lies in G, so both moves are increasing.
This prepares Y+2eX and preserves X487. It does not prepare the broad
correlated arrivals.

For a control, lift the predecessor's literal entry to (Y+eX,aX-h,dX+h).
Its original four events yield (P,W-Y,dX+h). All live and h projections
pass, but Y=1, X=h=0 gives outgoing wire -1. PR6261 explicitly claimed
only the projected response; this is a boundary discriminator, not a
counterexample to its stated theorem.

## 4. Original h needs a new query

No linear continuation using only P,W,H=dX+h can produce h, even if it
may temporarily rewrite both outputs. In alpha P+beta W+gamma H=h, the
Y and h coefficients force alpha=0,gamma=1. Then beta(c-e)+d=0 is
impossible: on U it forces beta=0, whereas d is nonzero on V. The pinned
fixture has rank(P,W,H)=3 and rank(P,W,H,h)=4. More local operations
cannot overcome this rowspace gap.

There is also a direct collision, independently suggested during review.
Choose one nonzero coordinate of a and one of d. Change their X values
by 1/a_i and -1/d_j, respectively, and change h by one, leaving eX and Y
unchanged. All three observations P,W,H are unchanged, while original h
differs. The exact fixture uses only two live shifts of magnitude two and
one helper shift. Thus even an arbitrary deterministic recovery function
of those three observations cannot recover h for all original inputs.
This does not exclude access to other registers or retained history.

Under arbitrary **field-linear** readout, one additional unchanged pure-live
query Q=qX permits restoration exactly when

    q=rho[d+lambda(c-e)],    rho != 0.                    (3)

Indeed d must lie in span(c-e,q), and d is not proportional to c-e.
Conversely H-Q/rho+lambda W=h is an explicit cleanup leaving P,W,Q
unchanged. On U the query is rho*lambda*(a-e); on V it is
rho*(1+lambda)*d, with every listed coordinate nonzero. Thus:

| lambda | support | cardinality | binary span dimension |
|---|---|---:|---:|
| 0 | V | 8 | 6 |
| -1 | U | 16 | 6 |
| otherwise | U union V | 24 | 7 |

The dimensions are exact finite properties of the pinned ports, checked
by both elimination and independent XOR-span enumeration. The support
minimum eight is sharp for this one-query contract.

**Dyadic qualification.** Field-linear sufficiency is not a blanket dyadic
gate guarantee: q=3d satisfies (3), but its cleanup requires division by
three. For dyadic q in this particular fixture the entries of W on U and
d on V are units (+/-1/2) in Z[1/2]. Write q=rho*d+beta*W. Evaluating one
coordinate in each section determines dyadic rho and beta uniquely.
Restoring h by a dyadic linear readout requires the q coefficient -1/rho,
so rho must be a unit in Z[1/2], equivalently +/-2^k for an integer k.
Conversely this condition makes both -1/rho and lambda=beta/rho dyadic and
the displayed cleanup works. The q=d sharp attainer and all 15 tested
representatives satisfy this requirement. Coefficient bounds, native
availability and physical implementation remain separate. The entry iff
(2) likewise concerns field-linear readout; its t=1 construction is
explicitly dyadic and incurs no division.

**Frame qualification.** If the query is a public row whose live content
is confined to its frame, with no owned-delivered live component, its
frame has dimension at least six. No frame of dimension five or below
can contain an admissible support. Pure-live alone is insufficient: an
owned descending row or an owned-delivered public component may carry
broad support at a small frame. Such mechanisms retain their own paid
preparation and ownership obligations and are not excluded here.

## 5. Visible cost and stopping decision

For Q=dX, cleanup is one ADD H-=Q. Counting singleton preparation, the
source-loaded calendar has four visible ADDs: one before G, two at the
meeting, one cleanup. It preserves the original Y column in the required
partner shear, restores h and preserves Q, but returns the outgoing wire W,
not that wire's original value.

In the declared incoming frame calendar the partner pays ranks (1,6),
the first dirty carrier pays H0->G rank one, the helper pays H1->G rank
one, and the additional query pays H1->G rank one. The visible histogram
is four rank-one jobs and one rank-six job. This is conditional on those
prepared rows and frame arrivals. Source gathering, original-h
correlation, query preparation, their productive target effects, all
outgoing routes, last-wire restoration, native phases, precision,
ownership and storage are **additional**, never zero by omission.

Splitting a hypothetical unsplit rank-seven partner move into one and six
increases its concave paid moment: 1^t+6^t-7^t>0 for 0<t<1, by strict
subadditivity. The named query arrival adds another positive 1^t. No
claim is made that a valid predecessor used the hypothetical unsplit
move or that this partial histogram is a complete fair comparison.

Stop here. A complete compatible producer, pure query, outgoing consumer
and last-wire restoration have not been supplied. The result identifies
an attainable full-column local entry and its exact missing cleanup
information. It neither proves nor disproves the complete one-helper
architecture and establishes **No new κ**.

## 6. Evidence, independence and credit

No predecessor executable is imported. The verifier reconstructs Gram
rows from the canonical port input, replays all 209 columns over Q,
checks exact inverse and the old projection/Y discriminator, and checks
15 cleanup representatives. Independent augmented-row elimination checks
all four-live-coordinate quotient states (A0,S=A1+A2) over F3 and F5
with support(A0)<3. A separate complete F3 quotient census also varies
the original Y coefficient and the dirty pair's aggregate Y coefficient.
This is finite corroboration of the proof, not a
physical program census. Exact-reason controls include all 63 rank-five
subframes of the rank-six d-span and every one-port query on the 24 ports.

One separate assisted reviewer independently derived the algebra and
enumerated the binary spans; it identified the essential no-owned-delivery
qualification for the frame corollary. A second assisted reviewer checked
the geometry through annihilator enumeration, Gram signs through bit
intersections, and query classification over F3/F5/F7; it identified the
field-versus-dyadic qualification and the explicit collision. No independent
human or proof-kernel acceptance is claimed.

Credit Nick Petalas/PR6261 for the correlated-dirt question and fixture;
Matarener/PR6217 for the architecture, sign/capacity premises and earlier
singleton-stop observation; Matarener's carrier-code work for port/root
identification; DreamingOfClouds/PR6170 for frame-contract context; and
the retained P104/native/helper/controller/caller lineage. Linear algebra
and strict subadditivity are classical. The new contribution is the
full-column entry classification, two-write realization and sharp
one-query cleanup boundary at this meeting.

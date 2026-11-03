# Safe fusion of the PR6280 dual-exchange consumer

Prepared for @CubeJerry with OpenAI Codex assistance. Apache-2.0.
The exchange and its compiler are Nick Petalas's PR6280; the source dual-pair
interface and scalar tariff are Ali Romman's PR5611/5602. Conjugation,
retractions and cancellation of inverse basis changes are classical.

This package independently checks the exact emitted exchange and supplies a
composition contract, including the precise boundary at which fusion is legal.
It does not identify an actual P104 cut satisfying that contract. No new κ.

## 1. Typed algebra and the source implementation

Let X and Z be modules, and let A:X→Z and B:Z→X be module homomorphisms with
AB=I_Z. Set Q=I_X−BA. Then Q²=Q, QB=0 and AQ=0. On X⊕Z define

    S(x,z) = (Qx+Bz, Ax),       S = [[Q,B],[A,0]].

The identities S²=I and the following chronological factorizations use only
AB=I; neither BA=I nor any operator commutation is permitted:

    U_B; L_(-A); U_B; D = S,
    D; L_A; U_(-B); L_A = S,

where U_B(x,z)=(x+Bz,z), L_A(x,z)=(x,z+Ax) and D(x,z)=(x,−z).
For example the first program reaches (x+Bz,−Ax), then (Qx+Bz,−Ax),
then S(x,z). The second reaches (x,Ax−z), then (Qx+Bz,Ax−z), then S(x,z).

The pinned `compiler.py` is retained unchanged, including its author notice.
For scalar row a and column b in D=Z[1/2], it specializes A=(a_i I_Z)_i,
B=(b_i I_Z)_i. An upper block consists of ADDs to distinct data destinations
with the unchanged spare as source. A lower block consists of ADDs into the
spare from unchanged data sources. Consequently each emitted block has the
displayed action, regardless of zero coefficients. The source branches emit
exactly the two words above; the sole SCALE is the sign on the spare. This
source-reading argument covers every accepted dimension and coefficient, while
the finite emitter checks are regression evidence rather than its proof.

`noncommutative.py` is an independently written symbolic certificate. Its
letters have the types above; G,H,J are Z→Z. The only reduction is AB→I_Z.
This length-reducing rule has no overlapping redexes, so reduction terminates
with a unique normal form. Every polynomial equality it checks is therefore
valid under substitution of these typed homomorphisms. It checks both source
factorizations, S², the one-use consumer and ordered two/three-use identities.
It does not import the author's dense verifier or infer a theorem from matrix
samples. The separate source-emitter regression does use exact input-basis
execution and is explicitly not claimed to be another universal proof.

## 2. The consumer needs no linearity of its inner map

Let G:Z→Z be any function. It need not be additive, invertible, homogeneous,
or commute with scalar multiplication. Apply S, replace the spare by G of
its current value, and apply S again. Direct substitution gives

    (x,z) → (F_G(x),z),
    F_G(x) = Qx + B G(Ax) = x + B(G(Ax)−Ax).                 (1)

In particular every arbitrary incoming spare is restored and absent from
the resulting data. This is an extension of the source's stated D-linear-G
contract, not a correction of an erroneous source claim. The symbolic
noncommutative certificate concerns linear G; the direct substitution above
supplies the more general set-map statement. Exact nonlinear fixtures
corroborate that distinction without proving it by enumeration.

Equation (1) implies AF_G=GA. Therefore, for any H:Z→Z,

    F_H(F_G(x)) = x+B(H(G(Ax))−Ax) = F_(H∘G)(x).             (2)

Also F_id=I_X. This is an injective semigroup representation: AF_GB=G.
If G is bijective, F_G has inverse F_(G^-1); conversely bijectivity of F_G
forces bijectivity of G, by the decomposition X=ker(A)⊕im(B). These
properties are algebraic consequences, not admissions of arbitrary functions
as legal recursive children.

## 3. Exact closed-macro bill and its observation boundary

Fix the same pair (A,B), same physical fields and spare, and common chart
throughout a sequence. Suppose the only intervening actions are G_1,…,G_k
on that spare, with no observation or modification of a restored full-call
state between them. For k≥1, the chronological programs

    S;G_1;S; S;G_2;S; ... ;S;G_k;S
    S;G_1;G_2; ... ;G_k;S                                  (3)

have the same complete endpoint (F_(G_k∘...∘G_1)(x),z). This follows either
from (2) or exact cancellation of each adjacent S;S. It preserves every G_i
in its original order. No contraction, productive credit or paid recursive
call is removed by this argument.

For the exact PR5602 ADD tariff let A_a and A_b be the sums of the nonzero
coefficient costs in a and b. The source's chosen exchange has allowance

    B_ex = 2 + min(2 A_a+A_b, A_a+2 A_b).

Thus the first program in (3) has 2k B_ex scalar allowance, while the second
has 2 B_ex. Both still owe the same k applications of G_i, their native and
delivery costs, and any enclosing allocation, routing, chart and cleanup
costs. For a=(3,5), b=(2,−1), the retained emitter has seven scalar ADD/SCALE instructions and
B_ex=64. The closed three-call macro changes 42 such instructions/384 allowance
to 14 instructions/128 allowance, retaining all three uses. This is an exact local
invoice comparison, not a wall-time measurement or a supplier improvement.

The missing intermediate boundary is substantive. After the j-th use in the
fused program the actual representation is

    (Qx+Bz, (G_j∘...∘G_1)(Ax)),

whereas a separately returned consumer presents

    (Qx+B(G_j∘...∘G_1)(Ax), z).

A caller expecting the latter may distinguish them. In the named pair, start
at (x_0,x_1,z)=(1,0,7) and use G(t)=t+1. The fused internal state is
(9,−4,4), while the returned consumer state is (3,−1,7). Even reading the
spare separates them. A caller may instead implement a correctly transformed
observer, but that observer and its cost are outside this theorem. The theorem
does not promise equal outputs under interruption, exceptions, rounding,
interleaved access, or a change of chart/pair between the retained uses.

Every source exchange's elementary scalar-prefix bound remains valid relative
to its own entrance. No magnitude or error bound for arbitrary G_i, or for
the complete nonlinear macro, is inferred from those exchange bounds.

## 3a. Exact class of safe read-only intermediate observers

The no-observer condition above has a precise relaxation. Fix a deterministic
read-only observer O:X⊕Z→Y, with no mutation, control-flow change or alteration
of any subsequent G_i. Require the same observation at each internal fused
state and its corresponding returned consumer state, for **every** incoming
state and **every** sequence of inner functions. This universal observation
contract holds exactly when

    O∘S = O.                                                (5)

Indeed the returned state is S applied to the fused state, so (5) suffices.
For necessity choose all inner functions to be identity. Then the internal
state is S(x,z), which ranges over all X⊕Z because S is an involution.
Thus equality of observations forces (5) on every state. Equivalently, in the
split coordinates x=k+Bw with k∈ker(A), S swaps w and z; an allowed observer
must be symmetric in those two coordinates with k fixed.

If Y is a module and O is module-linear, write O(x,z)=Cx+Dz, where C:X→Y and
D:Z→Y are homomorphisms. Equation (5) is equivalent to

    D=CB,     and therefore O(x,z)=C(x+Bz).                  (6)

To see necessity, set x=0 in O(S(x,z))=O(x,z). To see sufficiency, the
x-coefficient after exchange is CQ+DA=C−CBA+CBA=C, and the z-coefficient is
CB=D. No division by two, commutation or faithful scalar representation is
needed. The exact linear observation defect is
`O(S(x,z))−O(x,z)=(D−CB)(Ax−z)`.
In particular observers factoring through Qx are allowed because
QB=0. Nonlinear observers are governed by (5), not merely the linear form
(6); for example, when Z=Q the product (Ax)z is invariant under the swap.

Universality matters. For a fixed nonsurjective inner map, it is necessary
only to agree on states actually reached and their exchanged partners. For
X=Z=Q and A=B=identity, choose G=0 and O(x,z)=xz². The relevant states are
(z,0) and (0,z), where both observations vanish, although O(1,2)=4 differs
from O(2,1)=2. This is a counterexample to asserting global swap-invariance
as a necessary condition for one fixed non-surjective call, not a failure of
the universal contract above.

These observations retain their original cost in the fused macro. An actual
caller must establish that the observer can legally read those physical
fields in the common chart; algebraic invariance supplies no free delivery,
extra ownership, implementation or observer transformation. The existing
exception, rounding and interruption limitations remain. Arbitrary observers,
mutating actions and observer-dependent control flow are outside this extension.

## 4. Matching boundary pairs is necessary, not just convenient

Let the entering exchange use (A,B) with AB=I_Z, and the exiting exchange use
(C,D) with CD=I_Z on the same typed modules. Direct expansion yields

    z_out = C(I−BA)x + CBz,
    x_out = (I−DC)(I−BA)x + (I−DC)Bz + D G(Ax).             (4)

These formulas hold for every function G. Restoring z for every x,z forces
CB=I_Z and C(I−BA)=0. Hence C=CBA=A. Conversely C=A restores the spare.
Once C=A, the dirty-spare coefficient in the data is B−D. Independence of
the data output from every z is therefore equivalent to D=B. Thus the full
arbitrary-spare return/no-leakage contract holds exactly when the two pairs
match. This is equality of module maps: the scalar coefficient conclusion
uses the faithful scalar field-value modules of the source interface.

Both duality constraints alone are insufficient. Over Q, take A=(1,0),
B=(1,0)^T and G=identity. Choosing C=A,D=(1,1)^T preserves z but sends
(0,0,1) to (0,−1,1), leaking spare data. Choosing C=(1,1),D=B instead
sends (0,1,0) to (−1,1,1), failing spare restoration. The verifier executes
these counterexamples with the actual emitted programs. They are failures
of the mismatched extension, not counterexamples to PR6280's matching-pair
claim. More general basis maps satisfying the same row/column equations may
differ on ker(A); this package does not license substituting only one half
of such a different completion.

## Scope, evidence and credit

The scientific base is `2485805a6d47f36ea83ddde6327d453ac82d44dc`; the exact
pending source is PR6280 `4d6e4374d6fdda7df72ddeb19dd6756353383346`.
`ORIGIN.json` records the original compiler path, Git blob and SHA256. It
was read from that Git object and copied byte for byte. The source commit is
not made an ancestor of this contribution, so the base source-history check
does not assert pending-PR ancestry. The standalone checker authenticates
both the SHA256 and the Git-blob encoding before source execution.

The source compiler's bounded algebraic input contract is broader than the
actual caller's coefficient-magnitude admission. The accepted pair
a=(2^63,1),b=(0,1) emits a coefficient violating |q|+1<2^16. This documented
positive discriminator prevents treating compiler acceptance as caller
admission; it is already a limitation of the predecessor, not a newly found bug.

No actual P104 interval with the closed-macro contract is supplied. Physical
availability of the spare, native charts and phases, arbitrary-input caller
bindings, complete signed moments, precision, tape/stock, completion/compiler
and analytic recovery remain separate obligations. The selected κ=.003125804
and all five framework assumptions are unchanged. There is no Lean proof,
independent human theorem review, or complete multiplication theorem here.

Credit Nick Petalas for PR6280's exchange/compiler and its 134→64 comparison;
Ali Romman for PR5611/5602 and the retained P104 helper/compiler lineage;
Chris R/Clear1nsight's `p104-joint-compensation` for an earlier distinct
free-operator compensator certificate. None of those results is claimed as
new. The new work is the source-bound safe-fusion contract, boundary matching
theorem, independent block certificate and controls, developed by the
exchange-audit research subagent and reviewed within the coordinated run.
The exact read-only observer refinement was independently derived and checked
by research worker A, using the split-coordinate swap and explicit reachability
quantifiers; it is part of the same closed-macro contribution.

## Independent exhaustive nonlinear corroboration

A separate lead-review implementation authenticates the original source
emitter, reduces its named (3,5)/(2,-1) pair to F3, and interprets the emitted
gates without importing the primary verifier or polynomial engine. It covers
every pair of the 27 functions F3→F3, every 27 three-role input, and all three
emitter choices: 59,049 cases. Literal separate consumers, the fused consumer
and the direct nonlinear endpoint formula agree. Both ordinary and optimized
runs are registered. A different valid dual column produces explicit dirty-spare
leakage and is rejected as a matching-boundary substitution. This finite
corroboration does not replace the module/set-map proof or supply a native
implementation. The independent program is `independent_nonlinear.py`.

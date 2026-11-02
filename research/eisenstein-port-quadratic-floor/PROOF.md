# A polar-rank obstruction for quadratic messages

This contribution was produced by Nick Petalas. Apache-2.0.

## Contract and credited premise

Use Michael Fischler / shiftybitshiftr's PR814 fixed-support nonlinear
Eisenstein model. Port t has an independent vector X_t in F2^(b_t), with
b_t >= 0 and N = sum_t b_t. Every fixed message bit has fixed source and
reader port sets. Its additive charge is the rational pairing-rank price
in that model. Receiver t recovers X_t on every input from its received
messages and the inputs at ports orthogonal to t. Decoders can be nonlinear.
There are no free input-dependent headers or correlated entrance promises.

We use Jose Manuel / jmbarrancoml's PR2017 fixed-support block-linear
corollary as a cited theorem: affine messages with these supports and
independent demands cost at least the total demand. Known constants can be
subtracted. That source result, its geometry and its numerical evidence
are not independently proved or replayed here.

## Product-affine restriction lemma

For each port choose an injective affine map

    X_t = a_t + M_t U_t,    U_t in F2^(d_t).

Suppose all message bits become affine functions of the full independent
product U. Then the unchanged original message charge C satisfies

    C >= sum_t d_t.                                           (1)

Indeed, compose the original exact encoder and decoder with these maps.
Each receiver recovers X_t and hence U_t using a fixed left inverse of M_t.
Orthogonal-port side information is still available: U_s determines X_s.
All U_t vary independently. A message can retain its original source and
reader supports and width, so its charge is unchanged. Subtract the known
affine constants and apply the credited block-linear theorem. The maps
are a restriction used in a lower-bound proof, not free physical gates
or an input-dependent observation channel. A subspace coupling distinct
ports would invalidate this argument and is excluded.

## Quadratic class and theorem

For every active port t, fix a scalar Boolean polynomial q_t of degree at
most two. Write every transmitted bit in the form

    Y_j(X) = ell_j(X) + sum_t lambda_jt q_t(X_t),

where ell_j is affine and lambda_jt is in F2. The index j runs over all
message bits, not just messages. The displayed function must obey its
declared source support. Call t active when some lambda_jt is one; forms
at inactive ports are ignored. Multiple independent quadratic forms at
one port and cross-port quadratic monomials are outside this theorem.
Linear and constant parts of q_t are allowed and immaterial.

Define its alternating polar form

    B_t(v,w) = q_t(v+w) + q_t(v) + q_t(w) + q_t(0).

Let rank(B_t) = 2 r_t at active ports and r_t = 0 otherwise. Then

    C >= N - sum_t r_t.                                       (2)

Moreover, sum_t r_t is exactly the least total codimension of a product
of affine subspaces on which every transmitted bit is affine. Thus (2)
is the best bound from lemma (1) for this declared quadratic class.
It is not asserted to be the optimal message charge.

## Isotropic dimensions, including degenerate forms

For a quadratic q with polar form B on V = F2^b, its restriction to
an affine subspace a+L is affine exactly when B vanishes on L times L.
To see this, the translated function q(a+v)+q(a) has polarization B
on L. It is linear precisely when it is additive. Thus the translation
a and every original affine term have no effect on the criterion.

An alternating form has a radical R = ker B and a basis of r symplectic
pairs plus b-2r radical vectors. This follows constructively: if B is
nonzero, choose e,f with B(e,f)=1. For each remaining vector v replace it
by v+B(v,f)e+B(v,e)f, which removes both pairings. Repeat on the remaining
space. Each iteration removes two dimensions, so the process terminates.
Taking one member of every pair and all radical vectors gives an
isotropic subspace of dimension b-r.

For the upper bound, the image of any isotropic L in the nondegenerate
quotient V/R is isotropic. In a nondegenerate 2r-dimensional alternating
space, W is contained in its perpendicular and

    dim(W) + dim(W-perpendicular) = 2r,

so dim(W) <= r. Consequently

    dim(L) <= dim(R) + r = b-r.                               (3)

This proves both the even-rank assertion and the exact maximum dimension.
These are classical alternating-form facts; no historical priority is
claimed for symplectic elimination or the isotropic dimension formula.

## Apply the dimension calculation without coupling ports

Choose a maximum isotropic L_t at every active port and the entire input
space at every inactive port. All q_t become affine on the product, hence
all messages do. Its dimension is N-sum_t r_t, proving (2) by (1).

Conversely, suppose every message is affine on a product of affine spaces
with direction spaces L_t. Fix a port t and vary only its coordinates.
The polarization of bit j is lambda_jt B_t restricted to L_t. Since t
is active, one bit has lambda_jt=1. Thus B_t vanishes on L_t. No quadratic
term at another port can cancel this polarization because those inputs
are held fixed. Formula (3) bounds every active d_t by b_t-r_t; inactive
ones are at most b_t. Summing proves the exact restriction codimension.

## Strict improvement over coordinate faces

For any integer s >= 1, take one port of width 2s+1, with coordinates
u_1,...,u_s,v_1,...,v_s,z, and put

    q(X) = (u_1+...+u_s)(v_1+...+v_s).

Its polar form has rank two, so its exact affine restriction loss is one.
The hyperplane sum_i u_i=0 kills q while preserving independent parameters
within that port. In contrast, fixing individual coordinates to arbitrary
constants makes q affine only after all u coordinates or all v coordinates
have been fixed. If one unfixed u and one unfixed v remain, their mixed
quadratic coefficient is still one, regardless of the constants. Therefore
the exact coordinate-face loss is s. The difference s-1 is unbounded.
This comparison sharpens Nick Petalas / PR4895's coordinate-face obstruction
within its own fixed-support model; it does not contradict that theorem.

The first strict case is s=2, b=5. Give every one of the forty ports five
input bits. At port zero send its four u/v bits directly to itself and
send z+q instead of z. Every other port sends its five bits directly to
itself. This is an exact fixed-support code: the first four messages
recover q and hence z. The credited singleton pairing price is one, so
its charge is 200. The new lower bound is 199, while the exact coordinate
face bound is 198. The example distinguishes the two obstructions; it
is not an attaining charge-199 code or a nonlinear saving construction.

## Scope and next decision

The result is a scoped written proof with finite exact corroboration,
conditional on the cited fixed-support linear pricing theorem. It narrows
the genuinely nonlinear payload direction left open by ywz65 / PR2607.
A proposed saving d in this class needs sum_t r_t >= d. Dense monomials
alone do not imply enough nonlinear freedom to support that saving.

No physical encoder, native delivery, restoration schedule, complete signed
supplier invoice, selected framework assumption, new kappa or multiplication
theorem is supplied. Arbitrary quadratic vector maps, cross-port products,
adaptive queries, errors, private headers and correlated demands are excluded.
The general nonlinear optimum remains open. Independent human and formal
proof-kernel review are unclaimed.

Credit Michael Fischler / PR814 for the nonlinear model; Jose Manuel /
PR2017 for the linear floor; Jonathan Lam / PR798 and Joel Pulikkan /
GamingPuzzled for geometry and pricing; ywz65 / PR2607 for the open nonlinear
payload direction; Nick Petalas / PR4895 for the coordinate restriction
comparison; and the retained Eisenstein, decoder and construction lineage.

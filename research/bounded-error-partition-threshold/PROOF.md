# Successful-input fibers preserve partition bounds above 1/q

## Model

Fix an alphabet A of size q>=2. A finite acyclic deterministic circuit has
W independent uniform input symbols. Each physical wire carries one symbol.
A gate applies a fixed arbitrary function to its incoming symbols and may
have several output ports. Copying uses separate physical wires. Fixed clean
constants and discarded workspace are allowed; preloaded data-dependent
advice is excluded. The topology and local functions are fixed.

Each designated input w is demanded at one distinct designated sink rho(w).
Let S be the set of tuples on which all demands succeed, and p=|S|/q^W.
There is no correctness requirement outside S. Other independent inputs can
be fixed in the proof; include them among the demands if restoration is
required. Distinct sinks and independent designated inputs are essential.

Vertices have rational m-by-m frames M_v. Each gate uses one common frame
on all ports. Charge every physical edge (u,v), including terminal, control
and fan-out edges, by rank_Q(M_v-M_u). Write s for their sum. Each demand
has terminal shift M_out(rho(w))-M_in(w)=I_m. No linearity or invertibility
of the scalar gates is assumed. The attaining examples are invertible.

## 1. Successful-fiber inequality

Choose any vertex class C. Let D be the designated inputs whose sources are
in C and required sinks are outside. Put d=|D|. Let e be the number of edges
leaving C, in fixed chronological order. Then

    p <= min(1, q^(e-d)).                                  (1)

Fix all inputs outside D. For a successful tuple, record its e outgoing
wire symbols. The transcript and fixed outside inputs determine every
outside vertex: simulate them in topological order, using the recorded
entry whenever a wire enters from C. Re-entry into C is allowed; no
chronological-cut hypothesis is needed. There is no extra message channel.

Two distinct successful D tuples cannot have the same transcript. Otherwise
outside simulation gives the same distinct demanded sinks, although those
sinks must reproduce different D tuples. Thus at most q^e of the q^d D
tuples succeed for each fixed outside tuple. There are q^(W-d) outside
tuples. Counting proves (1). This is the successful-subset extension of
PR1757's zero-error outgoing-transcript argument.

If p>1/q, then e>=d for every C. Indeed, e<d implies the integer inequality
e-d<=-1 and hence p<=1/q. The strictness is necessary, as shown below.

## 2. Weighted partition certificates

For a vertex labeling ell, apply e>=d to each label class and sum:

    #{edges (u,v): ell(u)!=ell(v)}
      >= #{demands w: ell(in(w))!=ell(out(rho(w)))}.         (2)

Each crossing physical edge leaves exactly one class. Each separated demand
is counted once. Re-entry and fan-out do not change this accounting.

Suppose finitely many labelings ell_j and nonnegative weights c_j satisfy,
on every physical edge,

    sum_j c_j [ell_j(u)!=ell_j(v)] <= rank_Q(M_v-M_u).

Multiplying (2) by c_j and summing shows that p>1/q implies

    s >= sum_w sum_j c_j
               [ell_j(in(w))!=ell_j(out(rho(w)))].           (3)

The edge inequalities are required certificates, not an assertion that all
rational rank metrics have a useful partition representation. The new
premise p>1/q replaces zero error in the credited partition implication.

## 3. Common-flag consequence

Assume there are one common rational offset A_0 and an invertible B over a
characteristic-zero extension K of Q such that T_v=B^-1(M_v-A_0)B is upper
triangular at every vertex. For i=1,...,m label v by (T_v)_ii. The terminal
shift I_m separates every demand in each of these m labelings.

An upper triangular matrix has rank at least the number of its nonzero
diagonal entries: its principal submatrix on those indices has nonzero
determinant. Extending the field and conjugating preserve rational matrix
rank. Thus the m unit-weight labelings satisfy the edge inequalities in (3):

    p>1/q  implies  s>=Wm.                                 (4)

This includes nonsplit flags over K and noncommuting triangular families.
The checker uses rational triangular frames. The extension-field conclusion
rests on the written argument, not on a finite extension-field replay.

For 0<alpha<1 and 0<=r<=m, (r/m)^alpha>=r/m. Therefore the optimistic
normalized recursive moment is at least s/(Wm)>=1 under (4). Extra
nonnegative charges cannot create contraction. This is a scoped circuit
obstruction, not an integer-multiplication lower bound.

## 4. Sharpness with reversible circuits and the same terminals

For every q>=2, m>=1 and W>=2, put P=diag(1,0,...,0). Take two independent
symbols x,y and prescribe their swap. Their source frames are 0 and P.
The sink on physical wire zero demands y and has frame P+I_m. The sink on
physical wire one demands x and has frame I_m. Each demand therefore has
precisely the required identity shift.

First use the identity circuit, with no gates. It returns (x,y), meeting
(y,x) exactly when x=y, on q of q^2 inputs. The terminal edge ranks are

    rank(P+I_m)=m,        rank(I_m-P)=m-1.

Hence p=1/q and s=2m-1. All frames are diagonal. Add W-2 untouched identity
demands with source zero and sink I_m to obtain s=Wm-1 with the same success.
This proves sharpness even with an invertible scalar map and just one rank
unit of deficit. It does not assert sharpness for each fixed topology.

An exact swap is available with the same terminal frames. Identify the
alphabet with Z/qZ and perform

    x <- x+y;    y <- x-y;    x <- x-y.

Each assignment reads the current values. The final values are (y_old,x_old)
for every q, including composite q. Each gate is invertible and has common
frame P. Each is represented as a two-input/two-output gate, retaining the
unchanged operand on an explicit output port. Entrance ranks sum to one,
internal ranks are zero, and exit ranks sum to 2m-1. Thus s=2m, or Wm with
the extra identity demands. Every physical wire is charged.

No physical native implementation or zero-cost ordinary arithmetic is
claimed for these symbolic framed circuits.

## 5. Independent coins and expected cost

Condition on any fixed independent random seed. If its circuit has rank
bill strictly below the value of a valid partition certificate, (3) bounds
its success by 1/q. Average over the seed distribution. The same bound
holds. The certificate and topology may depend on the seed, and the proof
does not require finitely many seeds. For common flags the premise is
s<Wm in every seed, with the stated flag and terminal contract in each.

Expected cost alone is insufficient. Choose the exact swap with probability
lambda in (0,1), and the identity circuit with probability 1-lambda. Their
terminal frames and demands coincide. Independent mixing gives

    p=lambda+(1-lambda)/q > 1/q,
    E[s]=lambda Wm+(1-lambda)(Wm-1)=Wm-1+lambda < Wm.

The exact branch costs Wm, so it violates the deficient branchwise premise.
This is a boundary counterexample, not cheaper exact computation or free
random control. Literal two-seed mixtures are checked below. Nonuniform
inputs and data-dependent coins also invalidate the uniform conditional
count and are outside the result.

## Attribution and proof status

Credit Jose Manuel / jmbarrancoml PR1757 for the zero-error outgoing
transcript and weighted-partition method, Navinor PR825 for common flags,
and ywz65 PR2507 for designated demands and disposable workspace. Classical
successful-subset counting retains its established status. This sharp
threshold and reversible same-terminal attainment construction were
produced by Nick Petalas. Predecessor numbers and verifiers are not replayed.
This is a written proof with bounded exact corroboration, not independent
human or formal proof-kernel review.

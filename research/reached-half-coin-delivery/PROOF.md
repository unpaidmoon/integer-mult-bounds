# Paid coin delivery at one reached positive-half site

This proves a local, all-width contract for zero-based event52 of the
historical PR5599 word. It combines the unchanged positive-half payload from
zxv's PR6092 with a three-tape extension of JoyboyBrian's PR6095 marker
machine. The new work is the reached-value width argument, an explicitly
declared bit packing, and paid access to that resident random tape. Sources
and byte identities are in `SOURCES.json`; the finite replay corroborates
this proof but does not supply its all-width quantifier.

## Reached value and exact width

Use integer grid units: a physical scalar is h times its integer value,
where h is the fixed input/output grid spacing. In the pinned
`research/p104-helper-subspace-splits/WORD.json.gz`, the relevant events are

```text
40: ['ADD',   345, 93,  '1',   3]
51: ['ADD',    93, 345, '-1',  3]
52: ['SCALE', 345,     '1/2',  3].
```

The complete destination scan of events0..51 contains no other write to
role345 or role93. In particular role93 is unchanged before event40.
Writing a=x345_initial and b=x93_initial, event40 sets x345=a+b exactly,
and event51 changes only role93, to b-(a+b)=-a. Consequently the value
entering event52 is exactly

```text
x = a+b.
```

This identity holds for arbitrary dirty inputs and every choice of earlier
rounding coins. Earlier potentially rounded updates do not enter this
dependency slice. It does not say that the current role93 still equals b,
nor does this package execute the ADD at event40 or the intervening prefix.

Let a and b independently range over B-bit signed integers, B>=1. Then

```text
-2^B <= x <= 2^B-2.
```

Thus W=B+1 signed bits suffice for every reached x. The attained choice
a=b=-2^(B-1) gives x=-2^B, outside the B-bit signed range. W is therefore
the exact worst-case signed width for this two-input contract. Since W>=2,
the source half kernel's width premise is met. This is a source-relative
guard for the supplied reached value, not an implementation of its storage
allocation or of a packed caller's register selection.

## Declared fixed-draw packing and randomness premise

For each earlier event with coefficient denominator d=2^k in reduced form,
reserve k consecutive random-tape cells in event order. A block is decoded
as u=sum_j 2^j U[offset+j]. Reserve the block even when that event's reached
value happens to be exactly on the grid. Integer-coefficient events reserve
no cells. This defines a new physical packing of the fixed-draw scheme;
it is not an emitted tape ABI inherited from either predecessor.

The pinned word gives the following entire pre52 reservation list:

| Events | Bits per event | Total |
|---|---:|---:|
| 19,20 | 1 | 2 |
| 41 | 2 | 2 |
| 42,43,44,45,46,47,48 | 1 | 7 |

The sum is eleven. Event52 has denominator2, so its logical coin is
u=U[11]. The convention's reservation for exact-grid cases makes this
offset independent of input data and earlier outcomes. PR6026 supplies an
at-most random-bit ledger and a fresh conditional rounding contract;
PR6066 stores a logical integer coin per event. Neither supplies the physical
offset convention just declared.

The functional theorem below holds for every binary U, with no probability
assumption. To interpret it as fresh stochastic rounding, separately assume
that U[11] is uniform conditional on the original input and the entire past
at this cut. When x is even the result is exactly x/2. When x is odd the two
adjacent grid integers occur equally often, so the conditional mean is x/2.
Generating that random tape and ensuring this freshness are supplied
obligations. Preserving a tape does not make its bits fresh for a later
adaptive call; inverse execution intentionally reuses this same coin.

## Supplied cut interface

Three tapes, with independent translated origins, are presented as follows.

| Tape | Supplied cells | Entry and exit head |
|---|---|---:|
| Binary data | value at0..W-1; residue0 at W; resident-coin0 at W+1; W clean work bits at W+2..2W+1 | 0 |
| Read-only program | `<` at0, concatenated payload at1..L', `>` at L'+1 | 1 |
| Read-only random | binary U[0..11], with any further cells arbitrary | 0 |

The finite Boolean accumulators a_control,b_control start and finish zero.
To avoid confusion with the original input integers a,b, write these
accumulators as A,B below. The caller selects mode F for forward or I for
inverse; the same selected mode is restored at return. Only the final
left-marker transition returns to the caller, as in PR6095. A later call is
a new caller action, not an implicit restart of the interpreter.

Supplying this layout with the reached role345 value, clean residue/work
and resident-coin cells, the random tape, and the prepared program is a
premise. No rule in the machine verifies the global cleanliness or layout
premises. Semantic rejection controls in the verifier do not claim such
runtime validation. All cells outside the visited intervals are spectators
and remain unchanged, including arbitrary dirty cells beyond those bounds.

## Local transition rules

Retain the source payload actions L,R,A,B,X,C,T. L/R move the data head by
-1/+1; A/B XOR the scanned data bit into the respective accumulator; X,C,T
XOR 1,A,AB into the scanned data cell. Extend the alphabet with

```text
N: move the random-tape head +1;
P: move the random-tape head -1;
J: XOR the scanned random-tape bit into A.
```

N/P do not change data or accumulators. J does not move either nonprogram
head or write either tape. Inverse actions exchange L/R and N/P; all other
actions are self-inverse. Every rule depends only on mode, scanned program
symbol, A,B, scanned data bit and scanned random bit. No absolute address,
width, distance, or event number is available to the rule. The old seven
actions ignore the random bit, so their rows are unchanged on projection
to the predecessor's state and actions.

Use the simultaneous local multi-tape step convention of PR6095:

| Mode and symbol | Payload action | Program move | Next mode |
|---|---|---:|---|
| F, payload | forward action | +1 | F |
| F, `>` | none | -1 | FR |
| FR, payload | none | -1 | FR |
| FR, `<` | none | +1 | F, return |
| I, payload | none | +1 | I |
| I, `>` | none | -1 | IR |
| IR, payload | inverse action | -1 | IR |
| IR, `<` | none | +1 | I, return |

Only the indicated marker/mode pairs are valid. For each of four modes
there are ten valid payload symbols and one valid marker, four A,B choices,
two scanned data bits and two scanned random bits. Full expansion therefore
has exactly 4*(10+1)*4*2*2=704 valid rows. The finite control and alphabets
are independent of W; the explicitly stored unary program depends on W.
This is a three-tape finite-head construction in this convention, not an
addressed-access primitive or a newly audited native MOVE implementation.

## Fetch, half and unfetch

Let H_W be precisely `compile_tape(compile_gates(W,1))` from the pinned
PR6092 kernel, and L=|H_W|. Keep this payload unchanged as one contiguous
subword. Define

```text
F_W = N^11 J R^(W+1) C L^(W+1) J P^11.
```

From home with A=B=0, N^11 reaches U[11], and J sets A=u. The data walk
reaches cell W+1; C XORs u into that cell. The return data walk followed
by J clears A, and P^11 restores the random head. B never changes. Thus
F_W toggles the resident cell by u and restores all heads and accumulators,
even if that resident cell was nonzero. No other data cell is written.
Reversing the word and exchanging both movement pairs reproduces F_W
itself, so this is also its literal inverse.

For completeness, the positive source half is correct for every W>=2.
CNOT(x0,r) followed by CNOT(r,x0) saves r=x mod2 and clears x0. The W-1
adjacent swaps move the remaining bits down one position; copying the old
sign into the empty top cell gives q=floor(x/2), using 3W CNOTs altogether.
The clean temporary bit is set to r(1-u). A controlled ripple increment
computes c_(j+1)=c_j*old_x_j, then changes x_j to old_x_j XOR c_j.
Descending cleanup uses c_(j+1)=c_j*(1-new_x_j), preserving each needed
lower carry until use. All carries and the temporary bit clear. Hence the
integer endpoint is

```text
y = q+r(1-u) = floor(x/2)+[u < x mod2],   residue=r=x mod2.
```

Since -2^(W-2)<=q<=2^(W-2)-1, the incremented value fits in W signed bits,
including the reached negative extreme. Every Boolean gate is an
involution with distinct operands, and the source never targets its
resident coin. Its unary gate macros read unchanged controls into A,B,
perform the target action, reread those controls to clear A,B, and return
the data head home. Reversed macros with inverted walks implement the
inverse gates with the same head and accumulator invariant.

Supply one marked concatenation

```text
< F_W H_W F_W >.
```

There are no internal marker pairs or per-subword rewinds. First F_W
fetches u into the initially zero resident cell. H_W gives the preceding
half endpoint and leaves that cell equal to u. The final F_W clears it.
All work is zero, the random tape is unchanged at every step, and the
retained residue is r. Thus the complete forward endpoint is

```text
(x,U, residue0, resident0, work0)
  -> (floor(x/2)+[U[11]<x mod2], U, x mod2, resident0, work0).
```

Backward execution of the same marked word applies F_W, H_W inverse,
F_W: it refetches the unchanged u, reverses the half gates on their reached
state, then clears the resident coin. This restores x and clears residue
and work exactly. Equivalently, x=2*(y-[u<r])+r identifies the unique input.
Keeping r matters: at u=1, x=0 and x=1 have the same half output without
that residue. The theorem is functional invertibility at these declared
call boundaries, not injectivity of every marker-mode transition across
arbitrary off-contract configurations.

## Exact runtime and occupied intervals

There are 22 random-head movement symbols, 2(W+1) data-head movement
symbols and three nonmovement symbols in F_W. Therefore

```text
|F_W| = 2W+27,
L' = |F_W H_W F_W| = L+4W+54.
```

In forward mode, exactly L' payload transitions execute, followed by one
right-marker turn, L' program rewind transitions and one left-marker
return. Inverse mode has L' seek transitions, the right turn, L' inverse
payload transitions and the left return. Both directions consequently have

```text
T(W) = 2L'+2 = 2L+8W+110.
```

The nonexecuting pass never moves the data or random head. Each call adds
44 random-head moves and 4(W+1) data-head moves to the original half's
data-head count. Every program-head move and its return is already charged
in T. Data and random heads return to0, program head to1, A=B=0, and the
entry direction mode is restored.

All walks stay in the declared intervals. The source carry computation
touches data cell2W+1 for W>=2 and its unary walks connect that cell to0;
the entire data interval is therefore visited. N^11 visits the full random
interval0..11. Marker chronology visits the full program interval. Summing
these three occupied intervals, including parity, resident coin, work and
the whole read-only program, gives exactly

```text
program: L'+2 = L+4W+56 cells;
data:    2W+2 cells;
random:  12 cells;
S(W) = L+6W+70 cells.
```

The fixed finite control is additional constant control, not uncounted
width-dependent program storage. U[0..10] is traversed and charged even
though this local call does not use those bits for rounding.

With largest data address D=2W+1, the source X/CNOT/Toffoli macro lengths
are bounded by 2D+1,4D+3,6D+5. Their exact positive-half gate counts are
2W-2,4W+2,2W. Thus

```text
L <= (2W-2)(4W+3)+(4W+2)(8W+7)+(2W)(12W+11)
  = 64W^2+64W+8;
T(W) <= 128W^2+136W+126;
S(W) <= 64W^2+70W+78.
```

These are per-call bounds after the supplied program and cut layout are
available. The source's O(W^2 log W) program-preparation claim is inherited;
this package does not implement or audit a literal preparation compiler.
The additional 4W+54 wrapper symbols also require preparation. A caller
must add a separate setup allowance covering construction and placement of
the full word, as well as any allocator, layout and randomness-supply
charges. In particular, writing total runtime as T_setup(W)+T(W) keeps
that obligation visible; setting T_setup=0 is not justified here. Reuse or
amortization needs its own caller argument.

## Scope, credit and open obligations

The proof covers all B>=1 under the supplied interface. Finite fixtures
test endpoints, inverse cleanup, source binding, literal transitions and
invoice equalities; they do not certify a complete multiplier for all sizes.
The clean allocator, presentation of role345 at this cut, fresh random-bit
supplier, program preparation, full historical prefix, selected PR6030
transfer, native MOVE, global precision gain, supplier admission and final
paid multiplication bill remain separate obligations. No selected-frontier
change, new kappa, human review or proof-kernel acceptance follows.

The next composition question is an explicitly charged supplier that
presents this exact layout and its clean resources from a real caller.
Random-tape generation and conditional freshness must then be checked at
that interface. A separate preparation compiler would need to justify
the inherited setup claim without treating its output program as free.

Credit zxv's [PR6092](https://github.com/CrocSwap/integer-mult-bounds/pull/6092)
half kernel and [PR6066](https://github.com/CrocSwap/integer-mult-bounds/pull/6066)
logical stochastic ABI; JoyboyBrian's
[PR6095](https://github.com/CrocSwap/integer-mult-bounds/pull/6095) marker audit;
Nick Petalas's [PR6026](https://github.com/CrocSwap/integer-mult-bounds/pull/6026)
fresh conditional rounding and fixed-draw ledger; and Ali Romman's
[PR5599](https://github.com/CrocSwap/integer-mult-bounds/pull/5599) historical
word and its retained source lineage. The half algorithm, reversible gate
decompositions and stochastic-rounding rule are predecessor/classical work.
Prepared with substantial OpenAI Codex assistance. Apache-2.0.

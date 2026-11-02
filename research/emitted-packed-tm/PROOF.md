# Simulation theorem for the emitted packed backend

This contribution was produced by Nick Petalas. Apache-2.0.

## Contract

Fix a deterministic finite multitape machine with k tapes, alphabet
{0,...,A-1}, blank 0, Q states and initial state 0. A transition maps a state
and the simultaneous k observed symbols to a new state, k symbols and k moves
in {-1,0,1}. A missing transition halts without changing the tapes. All heads
begin at signed coordinate zero. Tape i initially has its supplied finite word
at coordinates 0 through ell_i-1 and blanks elsewhere. Let N=sum ell_i. The
requested output is exactly m raw symbols at positions 0,...,m-1 on one fixed
output tape, including blanks. It is not a blank-terminated integer codec.

The RAM input is the house-standard length-prefixed list whose body is

    [n, m, ell_0, tape_0..., ..., ell_(k-1), tape_(k-1)...].

Here n>=0 is a scale parameter controlling packing. It is neither execution
fuel nor a supplied time horizon. It may be tied to the input length by a
particular caller; no such identification is needed for the simulation.
The header length and all fields must be well formed. This program does not
validate malformed payloads, discover their lengths or reject invalid symbols.

RAM memory and registers share one bounded-word address space, initially zero.
The operations are modular-word SET, ADD, monus SUB, Boolean AND/OR/NOT, shifts,
indirect LOAD/STORE, branches, word READ/WRITE and terminal HALT. A shift by at
least the word width yields zero. Successful instructions cost one. HALT costs
no successful instruction. Code and the program counter are distinct from data.
No TM step, packed access, multiplication or division is a primitive.

Set c to 1 for A<=2 and 2 for 3<=A<=4. Thus c is the fixed symbol-field width.
Define

    lambda = floor(log2(n+2)),
    q = floor(lambda/(8c)),
    B = largest power of two <= q, or 1 if q=0,
    b = log2(B), H = least power of two >=2k, R=128.

The shipped emitter accepts 1<=k<=4, 1<=A<=4, 1<=Q<=16 and at most one million
emitted instructions. The same argument applies to arbitrary fixed finite
shapes with a base R above their controls and an adequate emitted-code bound.
Only the stated implementation caps are claimed for the supplied code.

Let T be a finite number of simulated transitions, L the emitted code length,
and S=n+N+T+m+k+3. A sufficient word-width condition is

    w >= max(10, bit_length(2R+H(S+1)), bit_length(L)).

This is the conservative bound implemented by width_bound. It depends on a
proved execution envelope, not information read by the emitted program.
The helper accepts n<2^256 and lengths, T,m<=10^6; it is a bounded convenience
interface, not part of the RAM's runtime. RAM replay accepts widths <=512.

## Packing and initialization

Encode signed heads by pi(z)=2z for z>=0 and pi(z)=-2z-1 for z<0. Decode
u=pi(z)>>1 and tag=2i+(pi(z) AND 1). Then u=z on the nonnegative bank and
u=-z-1 on the negative bank, including both 0 and -1 correctly. The symbol
for tape i at z is the c-bit field at offset c(u mod B) in word

    R + H floor(u/B) + tag.

Equality of two natural word addresses forces equal block and equal tag,
since the tag difference has absolute value below H. Different fields of one
word have disjoint c-bit masks. This proves distinct tapes and signs cannot
alias, and proves the shared-register/data separation since every data address
is at least R and all controls are below 48.

packing_init computes lambda by right-shifting n+2 until it is below two.
It divides lambda by 8c by a fixed shift. It doubles B from one while the next
double is at most q, recording b. Thus it computes precisely the stated B,
including q=0 and q=1, with one fixed emitted program independent of n and w.

If B=1 then cB=c<=w. Otherwise cB<=lambda/8<w. The width condition also fits
n+2, the outer list length, head encodings, all masks and every effective tape
address. In particular H>=2 bounds every head encoding by the available span.
The trial double in the B loop is at most 2B and fits. Consequently all
arithmetic used for addressing agrees with natural arithmetic; the modular
word semantics does not wrap or truncate a live field.

GET computes the address and offset in nine ordinary instructions, then
loads, sets the field mask, shifts and masks in four more. SET shares the
nine-instruction address calculation, then loads, sets the mask, shifts it,
complements, masks out the old field, shifts the new symbol, ORs and stores.
These are exactly 13 and 17 instructions. The Boolean mask identity proves
SET changes only its selected field, preserving every neighboring field,
unused high bit and other word.

emit_input reads every length and every symbol and performs a SET at each
successive nonnegative position. It increments encoded POS by two. All heads
are explicitly set to zero. Induction on the input loops gives exactly the
specified initial tapes, with uninitialized tape fields blank by the memory
premise. Arbitrary unused high bits are also allowed. Arbitrary dirty fields
that will later be read as blanks are not allowed by this ABI.

## One transition and halt

At label (state,q), the invariant is that the RAM has TM state q, every encoded
head equals pi of its TM head, and every tape field has the corresponding TM
symbol. Values of local scratch registers are immaterial; ONE, TWO, ZERO, b
and B-1 retain their fixed meanings.

The program first GETs every current head symbol into distinct retained
symbol registers. No tape write occurs in this phase. Dispatch uses only the
retained symbols and TEMP, trying each of the A^k possible tuples in a fixed
order. Two strict comparisons implement equality for each symbol. For a
well-formed alphabet, exactly the matching branch is reached.

If that transition exists, all k literal writes are SET at the old head
coordinates. Their order cannot change another tape's field. Each signed
head is then updated. For an odd encoding, moving left adds two; moving
right subtracts two except that encoding one becomes zero. For an even
encoding, moving right adds two; moving left subtracts two except that zero
becomes one. These are exactly pi(z+d) for d=-1 or 1. A stationary head is
untouched. Jumping to the next state therefore reestablishes the invariant.
This covers simultaneous writes and moves, crossing either side of zero,
block boundaries and every finite sequence of transitions. Induction gives
all-input simulation, rather than extrapolation from the finite fixtures.

If the transition is missing, dispatch jumps to output. No tape or head is
changed. The output loop GETs exactly m nonnegative fields of the chosen tape,
starting at zero, and WRITEs each raw symbol. For m=0 no tape field is read.
After those writes it reaches an actual terminal HALT instruction. Thus a
halting TM produces the stated output and halts; a nonhalting TM returns to
successive state boundaries indefinitely on an ideal unbounded-width model.
At a fixed finite width the claim covers only prefixes satisfying the width
condition. No finite width is asserted to simulate an unbounded trajectory.

The output loop changes scratch, packing POS and the output counter only.
All final tapes remain exactly the TM's final tapes. The program does not
restore controls or erase its owned RAM storage. Such cleanup would require
additional work in a caller with that stronger contract.

## Complete successful-instruction envelope

Initialization through packing setup costs exactly

    16 + 4 lambda + 5b.

Each tape's input-loop setup and final branch costs four instructions, and
each initial symbol costs 26. The final jump into state zero costs one.
Reading the simultaneous tuple costs 18k. Dispatch costs at most 3k A^k.
Writing costs 22k, head motion costs at most 5k and the next-state jump costs
one. The first missing-transition dispatch is bounded by the same quantity.
The output loop costs 22m+2, including its initial POS assignment and final
conditional branch. Therefore a halting run with T transitions executes at
most

    19 + 4 lambda + 5b + 4k + 26N
       + (T+1)(45k + 3k A^k + 1) + 22m

successful instructions. The same upper bound covers a prefix ending after
T transitions. The verifier checks this envelope on every new-emitter case.
For a fixed machine the cost is O(T+N+m+log(n+2)). This is constant overhead
per TM transition, not a logarithmic simulation speedup.

All nonnegative initialization/output coordinates and absolute head positions
are below D=N+T+m+1. At most 2k ceil(D/B) tape words can consequently be touched,
plus the fixed control bank. This counts words, not the numeric address span
and not emitted code storage. For fixed c and sufficiently large caller scale,
B=Theta(log(n+2)). A caller must supply a polynomial time/address envelope to
obtain w=O(log(n+2)); choosing a large scale for a small fixture is not a time
or bit-complexity improvement.

## Evidence boundary and predecessor credit

PR4538 by David Ganz / Dugongue supplies the representation, GET/SET kernels,
unpacked compiler and explicitly open complete-backend question. The new step
is the actual joined primitive program, invariant, raw-output contract and
complete envelope above. The finite verifier uses a separately written signed
TM model and twelve paired runs of the pinned source's unpacked compiler.
Those pairs check the new program's conformance; they do not audit the source's
scientific claims or replay its existing check suite. PR4883's retained-read
access improvement is credited context and is not integrated here.

Classical packing, finite-control compilation and simulation retain their
classical status. The RamStd/Problem 1.8 and Szymon Torunczyk simulation lineage
credited in PR4538 remains authoritative. PR4541's stronger tabulated transfer
and PR4724's portfolio construction are separate operational-model results.
No stronger asymptotic transfer or literature-priority claim is made.

Finite replay does not prove the universal induction or certify RamStd.step
in Lean. No physical multiplier, selected supplier, native operator, dirty
helper restoration, rounding/recovery bound, framework-assumption discharge,
new kappa or selected-frontier update follows from this result.

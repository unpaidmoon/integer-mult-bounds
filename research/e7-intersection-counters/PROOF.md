# Exact intersection counters for translated bit lanes

This implementation proof was produced by Nick Petalas. Apache-2.0.

## Model and reused machinery

Ali Romman's PR5729 represents independent binary generators as integer
bitsets. The first b generators define 2^b parallel lanes. For coordinate j,
integer C_j has bit l equal to coordinate j of the low-generator word u_l.
The remaining generators are traversed in binary reflected Gray order,
producing an offset v. Lane l represents exactly u_l xor v.

The new implementation retains that representation, assignment order,
source population-plane adder, threshold selector and final word extraction
order. It changes how the weight planes for one translated batch are formed.
The statement here concerns this changed computation, not a new proof of
the E7 classification or its geometry.

## Weight identity

For binary words u,v, count separately the coordinates where both are one.
Their contribution is two to wt(u)+wt(v) and zero to wt(u xor v). A coordinate
with just one set bit contributes one to both sides. Thus

```text
wt(u xor v) = wt(u) + wt(v) - 2 wt(u and v).
```

Compute the population planes for all u_l once, before the offset loop.
For offset v, pass only the coordinate columns C_j with v_j=1 to the
retained population-plane adder. In every lane this gives wt(u_l and v).
The scalar wt(v) is obtained by ordinary integer popcount.

`translated_planes` adds that scalar to the fixed wt(u_l) planes and
subtracts twice the intersection count. The adder uses the usual full-adder
parity/carry identity. The subtractor uses the ordinary full-subtractor
borrow identity

```text
borrow_out = (not a and (b or borrow_in)) or (b and borrow_in).
```

All Boolean operations act independently on corresponding bits of the
integer operands. Carries and borrows move to the next weight plane, never
to another coefficient lane.

Let k=bit_length(width). The implementation keeps the low k weight planes,
so its arithmetic is modulo 2^k. Intermediate addition or subtraction can
wrap. The final true weight is between zero and width, and width<2^k for
positive width. Therefore its residue identifies the true weight uniquely.
Width zero is a separate valid empty-word case: the threshold accepts the
sole zero lane, with no weight plane needed.

The retained `at_most` predicate consequently selects exactly the same
lanes as the original translated-column population count. The high offset
sequence and low-lane extraction order are identical. Independent generators
make the assignment-to-word map injective, so every qualifying word is
returned once, in the same order. No cached support set or classification
result participates in this computation.

## Complete caller preservation

`replay.py` authenticates six source files and loads the unchanged PR5729
`classify.py`. Its private `run_path` dispatch substitutes only the
`low_weight_words` binding returned for that consumer's exact `binary.py`
path. Every other load follows the original function. Both comparator
modes use the same dispatch and authentication boundary.

The source `main` still executes its complete `check`, including root/frame
construction, ambient slices, support enumeration, reflections, rational
ranks, orbit partition, all retained controls and comparison of the complete
result dictionary with the pinned RESULT.json. Its two output lines are
compared byte for byte between fresh original/intersection processes.
No production source or predecessor certificate is modified.

## Finite evidence and limits

The verifier compares every independent unordered generator set in F2^4
under every bound 0..4 and batch size 1..5. Its literal subset-XOR oracle
checks contents; comparison with the source iterator also checks ordering.
There are 1,381 sets and 34,525 complete comparisons, all enumerated.
Another 108 fixed wide-code cases reach width 127. An independent scalar
popcount check covers all 87,381 ordered pairs u,v over widths 0..8,
including arithmetic wraparound. Sixteen rejected inputs and three changed
input/bound histories exercise validation and absence of result caching.

These tests corroborate the implementation proof. The complete caller
checks preserve the predecessor computation rather than strengthen its
scientific conclusion. Timings describe this host, not every environment.
There is no new support bound, supplier, physical algorithm or kappa claim.

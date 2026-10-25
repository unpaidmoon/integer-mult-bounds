# Where L561 sits at event 9895, and what the scratch copy costs

Two statements. The first is about the pinned forward word. The second is
about the six-tape model in `research/qq16-gaussian-axis-tapes/tapes.py`.

## 1. The forward word names no tape interval for L561

The pinned forward core has 25,155 events and only five kinds: `phase`,
`scalar`, `adapter`, `residual_adapter` and `climb`. Their arities are 2, 3,
4, 4 or 5, and 6. None of those slots is a tape origin or a cell length.

Register 561 occurs in 27 events. The only two at or before the subtraction
are

```text
7963  ["residual_adapter", "pre", 561, 4]
9895  ["scalar", ["add", ["L", 546], ["L", 561], -1, 1], 4]
```

So event 9895 reads L561 as a scalar source in frame 4. It does not record a
window, an origin or a head. The canonical word agrees: `start[561] = 4`,
`frames[4] = [459]`, and L561 is not climbed or written before this event.

The eight private fields `C0` through `C7` are a different token family. Each
one's last scalar write before event 9895 is a `clear`, at indices

```text
8185, 8259, 8337, 8412, 8484, 8557, 8628, 8702.
```

No later scalar instruction names those tokens. The abstract scratch candidate
`Re C0[0:N/2]`, `Im C0[0:N/2]`, `Re C1[0:N/2]`, `Im C1[0:N/2]` from
`research/qq16-f0-first-caller` is therefore still zero at the subtraction,
and it is not a stored image of register L561.

## 2. Sharp copy from the kernel's two-tape entrance

The pinned tape primitive's only complex-register entrance is two owned
tapes of length \(L = NW\), real then imaginary, coordinates in order,
little-endian signed components. The subtraction packing in
`research/qq16-l546-head-move` asks for four owned scratch tapes of length
\(L/2\):

| Tape | Contents |
| --- | --- |
| scratch0 | real part, coordinates \(0..N/2-1\) |
| scratch1 | imaginary part, coordinates \(0..N/2-1\) |
| scratch2 | real part, coordinates \(N/2..N-1\) |
| scratch3 | imaginary part, coordinates \(N/2..N-1\) |

\(N = 2^n\) with \(n \ge 1\), and \(W \ge 1\). Heads start and end at cell 0.
A head reads or writes only its current owned cell, and moves by exactly one
cell. The cell one past the end may be occupied and not dereferenced. Finite
control may remember the half boundary. No second head, random access or free
relocation is available. Scratch may start dirty.

The schedule copies the low half, steps the home head onto the high half,
copies the high half, and rewinds every head. It does not step past the last
cell. Its bill is

| | count |
| --- | ---: |
| READ | \(2NW\) |
| WRITE | \(2NW\) |
| MOVE | \(8NW - 12\) |

Every home cell is read once and every scratch cell is written once. The move
count is \(\sum 2(L_t - 1)\) over the two lengths \(L\) and the four lengths
\(L/2\):

\[
2\bigl(2(L-1) + 4(L/2-1)\bigr) = 8L - 12.
\]

That is sharp in this model. A home cell that is never read cannot change the
scratch image, but every home bit does. A scratch cell that is never written
keeps its initial bit, so a dirty 1 survives a zero source. A unit-step walk
that visits cell \(L_t-1\) and returns to 0 has length at least \(2(L_t-1)\),
and that walk already visits every earlier cell. The schedule meets both
bounds.

The axis kernel's packing loop moves after every cell, including the last, and
then rewinds the full length. On this same split, which is axis \(n-1\), that
habit costs \(8NW\) moves: twelve more than the sharp tour, two per tape.

## 3. Conditional total for the copy and the subtraction

`research/qq16-l546-head-move` proves that, once this packing is already
present, the closed-return subtraction costs READ \(4NW\), WRITE \(2NW\) and
MOVE \(8NW-12\). Adding the copy gives

| | count |
| --- | ---: |
| READ | \(6NW\) |
| WRITE | \(4NW\) |
| MOVE | \(16NW - 24\) |

This sum does not include sending L561 home, clearing scratch for a later
kernel, the preceding axis factor (MOVE \(20NW\) on its own contract), or any
claim that the two home tapes occur in the native word. Section 1 shows that
the word does not name them. Unknown physical addressing is not zero.

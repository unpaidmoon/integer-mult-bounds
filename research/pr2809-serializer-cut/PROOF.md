# One PR2809 recursive cut parks the current frame

The GL64 macroprogram, the numerical PARK codec, and the selected cold replay
are not executed. The serializer is `RoleParking.park` in Jose Manuel's pinned
archive `research/physical-ordinary-interchange/inputs/pr2809.tar`.

## Proposition

At one recursive cut, `RoleParking.park` emits four bits for each symbol
currently on each canonical role, blanks that symbol, and pushes one record
per role, including an empty role. The method does not name a root stream.
The bits parked at a cut are the bits of the bodies present at that cut.

A child cut whose data body is the adopted capsule therefore parks four bits
per capsule symbol. It does not write a fresh copy of the root packet unless
that packet is still the current body.

## What the pinned proof says

`PROOF.md` §6 of the same archive states the cut invariant used here. Before
parking, the caller copies the current packet and its companion fields into
the child capsule. `RoleParking.park` then parks the canonical parent roles,
including empty ones: for each body symbol it writes the four-bit code, clears
the source symbol, and pushes the record. The child adopts the handoff copies
and receives an empty reusable role bank. §7 states that the parking tape holds
exactly the active ancestor encodings, and that the physical reserve of those
frames is `O_q(V_root) + F_q` when `V_j = V_root / (WN)^j`.

`BIT.md` §2 states the same geometric reading: each child's payload has volume
`V/(WN)`, and the active ancestor payloads form a geometric series, so visited
space is `O_q(V)`. `research/pr2809-continuation-stack-space` proved that
reading with constant 26041 for `V ≥ e`, and left open whether the serializer
itself parks that ancestor chain or one root-sized stream per cut.

## Executed schedule

The checker loads `role_parking.py` together with the archive's `words.py` and
`records.py`. It does not call `loader.authenticate`. Each role is a real
`Tape`. The symbol written into a nonempty body is `BODY[1]`, which the codec
accepts. `words.BLANK` is 4.

The schedule uses three roles: a fixed control body of 8 symbols, the current
data body, and one empty role. These lengths are inputs. Park does not compute
`V/(WN)`.

| Cut | Data symbols | Data bits parked |
|---|---:|---:|
| Root | 1000 | 4000 |
| Child | 7 | 28 |
| Grandchild | 1 | 4 |

The control role parks 32 bits at every cut. The empty role parks 0 bits and
still receives one push. After `park`, every role body is blank. The child
data record is strictly shorter than the root data record, so that cut did
not recopy the root packet.

The 7-symbol and 1-symbol bodies are the adopted-capsule schedule for this
comparison. They are not measurements of a live GL64 packet.

## The nested fixture charges a constant per level

`continuation_checks.nested_roles` charges

```text
depth * (5 * 132 + 7 * 5 + 3 * 2)
```

steps. The comment beside that formula accounts for the 132 bits as four
stream records, `4 * (4 + 13 + 12)`, plus one numerical record, `1 + 3 + 12`.
That product is linear in depth and independent of a root packet that would
grow with the ancestor. This package checks the formula and the comment. It
does not run the depth-1500 loop.

## The root-copy reading exceeds the geometric constant

`D(n) = 0` for `n < 64`, and `D(n) = 1 + D(42 * floor(n/64))` otherwise.
This is the width-recursion depth from `BIT.md` §2. Direct evaluation gives

```text
D(2^26050) = 42857.
```

The same value is at least 26042, the lower bound recorded by the predecessor
(`D(2^16) ≥ 16 + 1 - 9` is the sample of that bound). Since `42857 > 26041`,
a reading in which each of the `D(e)` cuts writes a fresh root-sized stream is
outside the geometric constant already proved for the ancestor chain. This
package does not re-prove that constant.

## What is not claimed

- The live capsule length is not measured. A later numerical cut could still
  place a root-sized body on a role before calling `park`.
- Marker, template, and erased-backing cells are not charged against `26041 V`.
  Each parked role also emits one `$` mark. That mark is checked and is not
  part of the four-bit payload count.
- No new conditional κ is claimed. The selected record stays
  `605457647/200000000000`.

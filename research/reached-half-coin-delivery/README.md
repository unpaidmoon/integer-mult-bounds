# Paid coin access at one reached positive-half site

This supplies one local interface left open by [PR6092](https://github.com/CrocSwap/integer-mult-bounds/pull/6092) and its [independent marker audit6095](https://github.com/CrocSwap/integer-mult-bounds/pull/6095). It wraps the unchanged positive-half program with literal random-tape access and return, and binds the register width to historical5599 event52. It does not provide a complete physical caller or new kappa.

## Result and exact contract

The actual source event52 is SCALE role345 by1/2 on the scalar frame3. Its only earlier write is event40, role345 += role93; role93 has no earlier write. Therefore the reached integer is x=x345_initial+x93_initial. If each original input is B-bit signed, B>=1, the sum lies in [-2^B,2^B-2]. Exactly W=B+1 signed bits suffice; the negative extreme rules out W=B.

Declare a fixed-draw packing: reserve log2(d) consecutive bits for each scalar event with coefficient denominator d, even when its particular input is on the grid. The preceding source events reserve11bits, so event52 uses U[11]. **This is an explicit new packing of the6026/6066 logical scheme, not an existing emitted physical tape ABI.**

At the cut, supply the reached W-bit register, zero parity/resident-coin/W-work cells, a marked read-only program, and a read-only random tape with12resident bits. All heads start at declared origins; both finite-control accumulators start zero and return zero. Let H be the unchanged6092 positive-half unary word, lengthL. With N/P moving the random head and J XORing its scanned bit into accumulator a, define

```
F = N^11 J R^(W+1) C L^(W+1) J P^11
program = < F H F >
```

F toggles the resident coin from U[11] and returns heads/control. The forward program fetches, runs H, and unfetches; the inverse uses the same preserved tape and word. The endpoint is `(x,U,0,0,0^W) -> (floor(x/2)+[U[11]<x mod2],U,x mod2,0,0^W)`. Inverse execution restores x and clears the retained parity. Arbitrary spectators and all program/random cells remain unchanged.

Each direction costs exactly **2L+8W+110** local transitions, including program-head return. Complete visited intervals occupy **L+6W+70** cells across the three tapes, including program and random cells. Coin-head motion is44; extra data-head motion is4(W+1). The704-row local table reads only scanned symbols, mode and two control bits. PROOF.md gives the all-width argument and the polynomial envelopes.

## Evidence and reproduction

SOURCES.json pins all seven source inputs at canonical base2485805a6d47f36ea83ddde6327d453ac82d44dc. No predecessor is edited or copied as a new contribution. The verifier authenticates source bytes before compiling the retained kernel source and checks the actual word slice.

```sh
python3.12 -B scripts/research_package.py --package research/reached-half-coin-delivery
```

The finite certificate covers all B1..4 original signed pairs/both coins, selected larger endpoint cases, translated head origins, spectators and rejecting controls. This is an exact finite check plus a scoped written argument, not a full-prefix replay or a formal proof. VALIDATION.md records actual counts/results after execution.

Current priorityrevision8 and selected6030 stay unchanged. The historical5599 source is used deliberately because6092/6095's open interface is bound to it. Initial live overlap covered309openPRs at04:48UTC,5979Discussionrecords at04:50UTC and all8722HEADnotes. All-state coin-delivery/event52 searches found6092/6095. An earlier restricted-network refresh failed and was retried successfully. Bounded search does not certify novelty. [Canonical claim/finding](https://github.com/CrocSwap/integer-mult-bounds/discussions/6073#discussioncomment-19285346).

## Open next questions

The reached cut layout, clean allocation, program preparation and random-tape generation are supplied premises. This wrapper pays access to an already resident random tape. The inherited O(W²logW) program-preparation allowance remains an additional cost; no literal setup compiler is constructed here. The source arithmetic addition/event40 and packed748-role placement are not lowered. A uniform conditional coin law is needed for the stochastic interpretation; restoring the tape does not make it fresh for a later adaptive call.

TASK.json gives concrete next steps for a paid packed caller/allocator, a setup compiler, and the next macro/random-supply/native-MOVE boundary. All-size precision, native movement, full supplier invoice, selected transfer, hostedCI and independent human/kernel acceptance remain open.

## Credit

AAAmirinu with substantial OpenAI Codex assistance, including separate implementation/proof work and AI review. Credit zxv/PR6092 for the signed-half kernel and PR6066 for the reversible logical interface; JoyboyBrian/PR6095 for the literal marker interpreter; Nick Petalas/PR6026 for the stochastic prefix; Ali Romman/PR5599 and the retained P104/native/physical lineage. Classical reversible fetch/unfetch and width arithmetic are background tools. Apache-2.0.

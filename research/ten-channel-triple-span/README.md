# Three-frame obstruction on the nine-channel source

On the fixed PR #5745 source, no three transport-grade-below-8 temporal
response spaces sum to a nonzero clean mode. An explicit relation among 41
dimension-1 frames does. The generation number γ therefore satisfies

    4 ≤ γ ≤ 41.

The nine-channel certificate already gives γ ≥ 3 and the bound 8 H_8 for at
most nine channels. The abstract pattern that blocks the same argument at
ten channels is not realized by any three frames of this source. Supports 4
through 10 remain open, so the ten-channel monotone floor is not proved.
The selected frontier κ = 781451/250000000 is unchanged.

The complete argument is in [PROOF.md](PROOF.md).

## Reproduce

From the repository root:

```sh
python3 -B research/ten-channel-triple-span/verify.py
python3 -O -B research/ten-channel-triple-span/verify.py
```

Both commands rerun the orthogonal census, the 41-frame witness, the
3,782 intersecting-pair reductions and the exhaustive triple screen. They
print `PASS_TEN_CHANNEL_TRIPLE_OBSTRUCTION`. NumPy 1.26.4 is required for
arithmetic in F_631. Tested with CPython 3.12. The screen uses one process
per allowed core. The run takes a few minutes.
Proof checks raise `SystemExit` rather than using assertions, including
under `python -O`.

## Open next questions

- Is γ at least 11 on this source? That is the missing inequality for an
  8 H_8 floor at ten channels under every positive nondecreasing tariff.
  The first step is a four-frame screen on the pairs already known to meet
  in nuisance. The triple certificate does not bound supports 4 through 10.
- Is 41 the minimum inside the dimension-1 subfamily, or can mixed
  dimensions undercut it? The witness is only an upper bound on γ. Test
  the 14-dimensional dimension-1 kernel before searching mixed supports.
- Can the 41-frame mode be scheduled as legal channels whose complete
  transport, restoration and ordinary bill beats 8 H_8? Price one witness
  under the PR #5745 contract before any search. No schedule is constructed
  here.

Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
The census method and the nine-channel pair theorem are Ali Romman's.
Predecessor source attribution is retained in PROOF.md.

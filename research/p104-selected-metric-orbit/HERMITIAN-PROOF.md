# The sharp constants also hold for common Hermitian metrics

The real-symmetric sharp constants in [ORBIT-PROOF.md](ORBIT-PROOF.md) extend
unchanged to **all complex Hermitian common metrics** on the original real
root vectors. Equality has no imaginary skew component. This broadens the
permitted ambient common maps; it still says nothing about independent port
motions, normalized correlations, arbitrary masked matrices or complete
multiplier costs. **No new κ.**

Let U be the full 120 unit root lines, with one real unit vector chosen for
each line. Let F,G be any disjoint orthonormal 8-frames, and put
`P=U\(F∪G)`. For a Hermitian matrix M define

\[
 E_P(M)=\sum_{\{u,v\}\subset P,\ u\perp v}|u^*Mv|^2.
\]

All sums count unordered distinct pairs once. Write uniquely `M=S+iK`, where
S is real symmetric and K is real skew-symmetric. Because u,v are real,

\[
 E_P(M)=E_P(S)+E_P(K),\qquad
 \left\|M-\frac{\operatorname{tr}M}8I\right\|_F^2
 =\left\|S-\frac{\operatorname{tr}S}8I\right\|_F^2+\|K\|_F^2.
\]

Here `E_P(K)` uses `(uᵀKv)²`, which is nonnegative and sign-independent on
unordered pairs even though K is skew. The trace of K is zero. The complex
Frobenius norm is the sum of squared absolute values of the entries.

## Two exactly checked root identities

The root coordinates in geometry.py satisfy

\[
 \sum_{u\in U}uu^{\mathsf T}=15I,\qquad
 \sum_{v\in U:\ v\perp u}vv^{\mathsf T}=9(I-uu^{\mathsf T}).
\]

These are finite identities, not isotropy assumptions. For `c(u)=2u`,
moments.py checks the equivalent integer equations

\[
 \sum c(u)c(u)^{\mathsf T}=60I,\qquad
 \sum_{v\perp u}c(v)c(v)^{\mathsf T}=36I-9c(u)c(u)^{\mathsf T}
\]

for all 120 roots. Each star contains 63 roots. Both identities are
orthogonally invariant and independent of the representative signs, so they
apply to any first frame after the previously checked isometry reduction.

## Exact skew-energy accounting

Skew symmetry gives `uᵀKu=0`. For a fixed root u the incident-edge energy is
therefore

\[
 \sum_{v\perp u}(u^{\mathsf T}Kv)^2
 =9\,u^{\mathsf T}KK^{\mathsf T}u.
\]

Summing over all 120 roots and dividing by two gives

\[
 E_U(K)=\frac92\operatorname{tr}\left(KK^{\mathsf T}
                    \sum_{u\in U}uu^{\mathsf T}\right)
       =\frac{135}2\|K\|_F^2.
\]

For any orthonormal frame F, summing its eight incident-star energies gives
`9||K||²_F`. The energy on pairs internal to F is `||K||²_F/2`, because in
that orthonormal basis the skew matrix has zero diagonal and opposite entries
at `(i,j)` and `(j,i)`. The sum over the eight stars counts internal edges
twice; hence the energy of edges having at least one endpoint in F is exactly
`(17/2)||K||²_F`.

Remove the edges incident to F and those incident to G. The intersection of
these two edge sets consists exactly of the orthogonal cross pairs between
F and G, since the frames are disjoint. Inclusion-exclusion yields the exact
identity

\[
 E_P(K)=\frac{101}2\|K\|_F^2+
 \underbrace{\sum_{u\in F,\ v\in G,\ u\perp v}(u^{\mathsf T}Kv)^2}_{X_{FG}(K)}
 \ \ge\ \frac{101}2\|K\|_F^2.
\]

There is no missing restoration or boundary term in this *geometric* edge
identity; it makes no algorithmic cost claim. The bound 101/2 need not itself
be the sharp skew constant for a given orbit, and no such sharpness is claimed.

## Hermitian inequality and equality

Let `c_P` be 37 or 75/2 as determined by the real-symmetric spectrum. Combining
the exact splitting with the skew lower bound gives

\[
 E_P(M)\ge c_P\left\|M-\frac{\operatorname{tr}M}8I\right\|_F^2
       +\left(\frac{101}2-c_P\right)\|K\|_F^2.
\]

Since `101/2>75/2≥c_P`, equality in the sharp `c_P` inequality forces `K=0`.
It then occurs exactly in the real-symmetric equality space already certified.
The real attainers belong to the Hermitian domain, so the constants remain
sharp even when restricting to positive definite metrics. The trace-free
Hermitian equality dimensions are therefore 6,1,6 for the three types.

For any complex common linear map T, its positive semidefinite metric
`M=T* T` is Hermitian, so the theorem applies to the transformed root inner
products. It does not assume T is real. This does not turn the metric
inequality into a universal obstruction for independent decoders or imply
that any selected native construction implements such a map.

## Verification and credit

verify_orbits.py executes every root second-moment identity in normal and
optimized Python. Two exact-reason negative controls alter a tight-frame
coefficient and omit one root from a star; both must be rejected. All three
sharp symmetric constants and their complete equality spaces are verified
separately by the orbit spectral certificates.

The lead proposed the skew-sector mechanism; worker A independently derived
the incident-frame accounting and implemented the exact moment checks. Credit
the full E8/P104 source lineage and Nick Petalas's real-metric predecessor as
in README.md. Jerry Chen, @CubeJerry, with substantial OpenAI Codex assistance.

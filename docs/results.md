# Results at a glance

## Recurrence Dynamics

| Result | Value | Evidence level |
|---|---:|---|
| 3×3 HPP four-particle zero-momentum states | 9,153 | exhaustive finite computation |
| 3×3 cycles | 2,061 | exhaustive finite computation |
| 3×3 exact periods | 3, 6, 9, 12 | exhaustive finite computation |
| Persistent site-density ambiguous states | 54 | exhaustive + independent certificate |
| Predictive doubletons | 27 | exhaustive + analytic mechanism |
| Minimum exact-mask fixed-site sensors | 3 sites / 4 snapshots | exhaustive subset search |
| Successful minimum exact-mask layouts | 6 | exhaustive subset search |
| Minimum local-momentum fixed-site sensors | 5 sites / 7 snapshots | exhaustive subset search |
| Successful minimum momentum layouts | 36 | exhaustive subset search |
| All-site momentum reconstruction | 2 snapshots | exhaustive predictive refinement |
| All-site axis-count reconstruction | 2 snapshots | exhaustive predictive refinement |
| Density-predictive cycles | 2,052 | exhaustive quotient-cycle enumeration |
| Microscopic cycles merged by density quotient | 9 period-3 orbit pairs | exhaustive quotient-cycle enumeration |
| Density quotient period compression | none in certified sector | exhaustive quotient-cycle enumeration |
| 4×4 sector states | 94,336 | exhaustive finite computation |
| 4×4 cycles | 19,448 | exhaustive finite computation |
| Density frames needed to determine 4×4 period class | 4 | exhaustive finite computation |
| 5×5 reference orbit | `seed=75202` | fixed reference state |
| 5×5 reference period | `T=9705` | exact orbit computation |
| Transport/geometry factor | `g=5` | exact invariant clock |
| Interaction-cycle length | `tau=1941` | exhaustive fiber decomposition |
| Full compatible interaction fiber | 2,209 states | exhaustive constrained enumeration |
| Full 5×5 14-particle zero-momentum sector | 2,240,809,149,480,000 states | combinatorial count |
| Frames to uniquely identify every state inside reference fiber | 9 collision-orientation frames | deterministic computation |
| Greedy single-snapshot velocity sensors on reference orbit | 49 of 100 | deterministic upper bound |
| Greedy 3-frame density sites on reference orbit | 11 of 25 | deterministic upper bound |
| 500-state empirical period predictor | `R² ≈ 0.724` on `log10(T)` | sampled cross-validation |

## Predictive Quotient and Physical Distinction

The generalized protocol-family construction defines

\[
\mathcal R_A(x)=\bigl(P_\pi(\cdot\mid x)\bigr)_{\pi\in A},
\qquad
x\sim_Ax'\iff\mathcal R_A(x)=\mathcal R_A(x').
\]

The quotient `Q_A` is the coarsest deterministic representation sufficient for every declared prediction in `A`, up to predictive isomorphism. If `A subseteq B`, the richer family can only refine classes. The construction is operational and theory-relative; it does not prove that predictive equivalence is ontological identity.

The corresponding operational discrimination pseudometric has zero set exactly equal to predictive equivalence. This supplies a precise scientific version of the question “when does a difference in description correspond to a difference in physics?”: when at least one admitted protocol changes the distribution of possible records.

## Cosmic Coordinate

| Quantity | Reference result |
|---|---:|
| Official coordinate | `M3 / Phi_C=0.7376` |
| Reference cosmic age | 13.787 Gyr |
| Time since M3 entry | 3.674 Gyr |
| Fraction of reference M3→M4 interval elapsed | 34.17% |
| Reference M3→M4 time remaining | 7.077 Gyr |
| M4 threshold | dark-energy fraction reaches 0.90 |

CPS is a model-conditional descriptive clock. `Phi_C` is not a fraction of the universe's total lifetime and not a recurrence phase.

## Cosmological Recurrence Study

| Quantity | Result | Interpretation |
|---|---:|---|
| CPS de Sitter horizon time | 17.2105 Gyr | conditional stable positive-Lambda branch |
| CPS de Sitter entropy | `3.18835 × 10^122 k_B` | conditional branch quantity |
| CPS thermodynamic recurrence exponent | `1.38468 × 10^122` | `log10(t_thermo/yr)`; not epsilon recurrence |
| DESI DR2+CMB posterior median exponent | `1.37911 × 10^122` | conditional flat-LambdaCDM propagation |
| 95% posterior interval | `[1.34391, 1.41616] × 10^122` | parameter uncertainty inside branch |
| Equal-prior two-model LambdaCDM weight | 63.9% | Ong-Yallup-Handley DESI DR2 BAO + Planck; selected LambdaCDM vs w0waCDM set |
| Equal-prior two-model dynamical-DE weight | 36.1% | same restricted comparison; not an ultimate-fate probability |
| Corrected DES-Dovekie two-model weights | 50.2% / 49.8% | LambdaCDM / w0waCDM from current `ln B=-0.01 +/- 0.27` |
| Theory-agnostic marginalized recurrence probability | `[0,1]` | partial-identification/non-identifiability result, not a probability estimate |
| Cosmological quantum epsilon recurrence time | not numerically identified | required microscopic spectrum not known |

## Illustrative future-weight sensitivity

The data-informed top-level two-model weights do not determine specific ultimate fates. CRPS therefore publishes explicit within-family sensitivity maps. Under the neutral `maximum_entropy_split`, the resulting bookkeeping weights are:

| Future | Illustrative weight |
|---|---:|
| Stable eternal de Sitter | 31.94% |
| Metastable de Sitter | 31.94% |
| Fading dark energy | 9.03% |
| Phantom finite end | 9.03% |
| Recollapse | 9.03% |
| Cyclic/bounce | 9.03% |

These numbers are **not measured ultimate-fate probabilities**. The repository also includes recurrence-conservative and recurrence-favoring splits to show how strongly the values depend on unresolved theory assumptions.

## What was learned from combining the projects

1. **Exact state recurrence is the strongest claim.** In deterministic dynamics it fixes the subsequent future.
2. **Visible recurrence is weaker.** Hidden state can make two visually identical states predictively different—or, in special cases, microscopically different states can remain observationally indistinguishable forever.
3. **Period and phase are only meaningful relative to a known recurrent dynamics.** Recurrence Dynamics demonstrates exact navigation in finite HPP systems.
4. **The universe's present cosmological position can be parameterized without claiming recurrence.** CPS supplies that descriptive coordinate.
5. **Ultimate fate dominates recurrence uncertainty.** Fine uncertainty in `H0` and `Omega_m` barely matters compared with whether the far-future branch is eternal de Sitter, decaying, finite, recollapsing, or cyclic.
6. **A crunch/bounce is not a reset by definition.** A cyclic scale factor is insufficient; recurrence requires a cycle-to-cycle state map that actually returns to a prior state or neighborhood.
7. **“Nothing left” is not a demonstrated reset condition.** The absence of ordinary matter does not specify the complete gravitational/quantum state or a deterministic rule that recreates the same Big Bang.
8. **There is currently no defensible measured single percentage for cosmic recurrence.** Any narrower number necessarily imports theory priors or a restricted model family.


## Observer Indistinguishability

| Result | Value | Evidence level |
|---|---:|---|
| HPP predictive doubletons | 27 | exhaustive exact certificate |
| Microscopic states in permanent density ambiguity | 54 | exhaustive exact certificate |
| Density-observer distance for certified pairs | 0 | exact under declared observation |
| Hidden information per equal-prior doubleton | 1 bit | exact |
| Conserved-sector perturbation trials | 150 | deterministic experiments |
| Trials initially identical in density | 150 / 150 | deterministic experiments |
| Trials density-distinguishable after one update | 150 / 150 | deterministic experiments |
| Irrational torus exact positive recurrence | none | analytic proof |
| First listed return below \(10^{-6}\) | 470,832 | continued-fraction computation |
| Human-observer recurrence threshold | not identified | requires physical observer model |

The paired HPP result and the perturbation result deliberately point in opposite directions. A microscopic difference can be completely invisible forever under one observation map, or it can be invisible now and observable one step later. The magnitude of a state mismatch alone therefore does not determine observer distinguishability.

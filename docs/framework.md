# Unified framework

## 1. The problem is a chain, not a single equation

A scientifically defensible recurrence study has to answer several different questions in order:

1. **Target:** What counts as the “same” state?
2. **Dynamics:** Does the declared system admit exact or near recurrence?
3. **Observability:** Does the information we can observe determine the complete future?
4. **Navigation:** If the system is recurrent, can we infer its recurrence period and present phase?
5. **Cosmic coordinate:** Where is the observed universe on a declared cosmological reference history?
6. **Ultimate fate:** Which future cosmological branches remain physically viable?
7. **Mechanism:** Which of those branches actually support a declared recurrence mechanism?
8. **Probability:** Which uncertainties are constrained by data, and which remain theory-dependent?

The four study layers occupy different parts of this chain.

## 2. Layer A — Recurrence Dynamics

Recurrence Dynamics defines the complete state `X`, update map `F`, observation map `O`, and recurrence/near-recurrence criteria. Its key logical distinction is:

```text
complete-state recurrence  !=  observational recurrence
```

For a deterministic map, if `F^T(X)=X`, then the future from the returned state repeats exactly. But if only `O(F^T(X))=O(X)`, hidden degrees of freedom can still differ and later observations can diverge.

The HPP benchmarks make this distinction machine-checkable. The 3×3 four-particle zero-momentum sector contains 9,153 microscopic states. Under site-density observation, 54 microscopic states fall into 27 predictive doubletons: two distinct microscopic trajectories cast exactly the same density movie indefinitely.

The framework includes a second decomposition:

```text
complete state -> invariants -> interaction fiber -> cycle -> phase
```

This is a method for navigating a known finite recurrent dynamics. It is not a cosmological claim.

## 3. Layer B — Observer Indistinguishability

The observer layer asks a different question from exact state identity:

```text
If the complete states differ, can any physically available observation distinguish them?
```

For a declared observer $O$, the framework uses an operational distance $d_O$ over accessible measurement-record distributions. A return can therefore be exact, merely near in complete-state space, or observer-indistinguishable within a stated tolerance.

The bundled exact HPP certificate supplies a limiting example: 27 pairs of distinct microscopic states have density-observer distance zero forever. The conserved-sector perturbation study supplies the opposite case: 150 pairs start with identical density observations but every pair becomes density-distinguishable after one update.

The observer layer therefore tracks not just complete-state mismatch but whether residual differences couple to accessible measurements and how long they take to become detectable.

## 4. Layer C — Cosmic Coordinate

The Cosmic Coordinate answers a different question: where are we on a *reference cosmological history*?

The official coordinate grammar is:

```text
M / Phi_C
```

For Cosmic Coordinate:

```text
M3 / Phi_C=0.7376
```

`M` is an operational macrostate label. `Phi_C` is a bounded composition phase based on the dark-energy-to-matter density ratio,

`Phi_C = (2/pi) atan(rho_DE/rho_m)`.

This coordinate is deliberately not called a recurrence phase. It does not say how many cosmic cycles have occurred or whether any cycle exists.

## 5. Layer D — Fate-conditioned cosmology

The cosmology study treats recurrence as conditional on the universe's future branch. A stable eternal de Sitter future, a metastable de Sitter future, fading dark energy, a phantom finite endpoint, recollapse, and a cyclic/bounce scenario are not interchangeable.

The inference architecture is schematically:

`P(R<T | D) = sum_(M,A) integral P(R<T | M,theta,A) p(theta,M,A | D) dtheta`

where `D` is current data, `M` is a future cosmological model, `theta` are measured parameters within that model, and `A` are extra theoretical assumptions required by the recurrence mechanism.

Current observations constrain part of `theta` and can inform comparisons among selected model families. They do not identify all far-future branch probabilities, vacuum lifetimes, microscopic de Sitter assumptions, or bounce maps. Therefore the unrestricted data-only recurrence probability is only partially identified:

```text
P(recurrence | current observations, unrestricted future theory) in [0,1]
```

This is a **non-identifiability result**, not an estimate that recurrence is "50-50" or that all values in the interval are equally plausible. The interval remains the full logical probability range because the unresolved theory layer can support recurrence probabilities anywhere within it.

## 6. The bridge between the layers

The modules connect by *questions and definitions*, not by circular proof.

- Recurrence Dynamics tells us why exact state, observable state, near state, period, and phase must be distinguished.
- Observer Indistinguishability tells us how to quantify “different underneath but impossible to tell apart” for a declared observer.
- The Cosmic Coordinate gives a compact reference description of the present cosmological epoch and composition.
- The cosmology study asks whether the far-future physics needed for recurrence is actually available and what present data can constrain.

The finite HPP results cannot be substituted into cosmological recurrence times. The cosmic composition phase cannot be substituted into an HPP recurrence phase. The conditional de Sitter entropy cannot be substituted into a finite-system quantum recurrence theorem without a justified microscopic Hamiltonian and spectrum.

## 7. What a future empirical breakthrough would need

A genuine claim that the universe is in a recurrence loop would require substantially more than this repository currently has. At minimum, one would need:

- a physically justified state space and evolution law for the relevant cosmic system;
- a declared recurrence target and metric;
- evidence that the relevant state space/dynamics satisfy the recurrence theorem being invoked;
- enough observables to overcome hidden-state ambiguity or a quantified residual ambiguity;
- a physically justified mapping from cosmological measurements to recurrence invariants, period, and phase;
- a future model whose recurrence mechanism survives competing processes such as vacuum decay and entropy production.

Until then, “recurrence is possible under some models” is defensible; “we know our recurrence phase” is not.

# Cosmic Recurrence Framework

## Dynamics, observational coordinates, and fate-conditioned cosmology

**Master repository manuscript — 9 August 2026**  
**Scott A. Sundy**

## Abstract

The proposition that the universe may recur combines several logically separate problems: defining what counts as the same state, determining whether the underlying dynamics permit recurrence, deciding whether available observations specify the complete state, localizing period and phase when a recurrent dynamics is known, identifying the universe's present cosmological condition, determining which far-future branches remain physically viable, and assigning probabilities without confusing observational uncertainty with theory uncertainty. This framework integrates three reproducible studies into a single research architecture while preserving their evidentiary independence.

Recurrence Dynamics develops exact finite-state diagnostics for complete-state recurrence, observational recurrence, predictive equivalence, hidden-state ambiguity, period constraints, invariant interaction fibers, and phase navigation. Its HPP lattice-gas benchmarks prove that repeated or even permanently identical observations need not imply microscopic identity. Cosmic Coordinate separately supplies a model-conditional reference coordinate for the present universe, `M3 / Phi_C=0.7376`, where `Phi_C` tracks the dark-energy-to-matter composition ratio rather than recurrence phase. The Cosmological Recurrence Probability Study then conditions recurrence on physically distinct future branches and propagates current cosmological information without importing the finite toy-model results as evidence.

For a stable eternal positive-Lambda branch, the CPS reference point gives `S_dS/k_B = 3.18835 × 10^122` and the conventional finite-patch thermodynamic scale `log10(t_thermo/yr) = 1.38468 × 10^122`. Official DESI DR2+CMB posterior propagation yields a median exponent `1.37911 × 10^122` with a 95% interval `[1.34391, 1.41616] × 10^122`; this narrow within-model spread is negligible compared with far-future theory uncertainty. A restricted equal-prior Bayesian comparison gives 63.9% weight to LambdaCDM and 36.1% to `w0-wa`CDM, but those are model-family weights, not probabilities of specific cosmic endings. Without priors that resolve stable versus metastable de Sitter behavior, dynamical-dark-energy fate, vacuum lifetime, the microscopic state-space assumptions behind recurrence, or the return map of a bounce, the marginalized recurrence probability is only partially identified on `[0,1]`. The combined conclusion is therefore conditional but nontrivial: recurrence is mathematically demonstrable in suitable systems and physically available under some cosmological futures, but current observations do not establish that the universe is in a recurrence loop, do not identify its recurrence period or phase, and do not determine a unique probability that exact cosmic history repeats.

## 1. Research question

Given the universe we observe today:

1. what does “the same universe again” mean;
2. when does a repeated observation imply a repeated complete state;
3. when can a recurrent system's period and present phase be inferred;
4. how can the universe's present cosmological condition be represented without assuming recurrence;
5. which physically viable future branches permit a recurrence mechanism;
6. what timescale follows under each declared mechanism; and
7. what probability can be assigned after separating data-constrained uncertainty from unresolved theory?

The central methodological requirement is that these questions be answered in order. Skipping from a finite recurrence theorem directly to the observed universe creates an unsupported inference.

## 2. Recurrence targets and state completeness

For a deterministic discrete dynamics `F` and complete state `X`, exact recurrence at period `T>0` is

`F^T(X)=X`.

Once this equality holds, subsequent deterministic evolution repeats from the returned state. This is stronger than observational recurrence. Given an observation map `O`, an observed return only requires

`O(F^T(X)) = O(X)`.

If `O` discards velocities, phases, fields, microscopic correlations, or other predictive degrees of freedom, the observed state need not determine the future.

Recurrence Dynamics operationalizes this distinction using finite reversible systems. In the exact 3×3 HPP four-particle zero-momentum sector, 9,153 microscopic states collapse to 495 present-density classes. Future refinement yields 9,126 predictive classes: 9,099 singletons and 27 doubletons. The remaining 54 microscopic states form 18 period-three cycles arranged in nine time-reversal pairs. Each paired trajectory is microscopically different yet produces the same site-density movie indefinitely. The result is a direct counterexample to the assumption that a permanently repeated visible configuration uniquely identifies the microscopic trajectory.

The lesson for cosmology is methodological rather than model-specific: any claim that “the universe returned” must declare whether the target is the complete quantum/microscopic state, a causal-patch state, a cosmological macrostate, or a finite set of observables.

## 3. Period constraints and phase navigation in a known recurrent dynamics

Recurrence Dynamics adds the decomposition

`state -> invariants -> interaction fiber -> cycle -> phase`.

In the HPP model, exact transport clocks, diagonal-species histograms, line momenta, and checkerboard modes constrain allowed periods before an orbit is fully traversed. The 3×3 benchmark contains 2,061 cycles with periods 3, 6, 9, and 12. In the 4×4 four-particle zero-momentum sector, 94,336 states form 19,448 cycles with periods 2, 4, 6, 8, 12, 20, and 28. Four consecutive density frames determine the period class for every 4×4 state in the declared sector.

A larger 5×5, 14-particle reference orbit seeded by 75202 has exact period `T=9705`. A transport factor `g=5` separates the orbit into a macrocycle of length `tau=1941`. Exact invariants reduce the full 2,240,809,149,480,000-state zero-momentum sector to a 2,209-state interaction fiber compatible with the reference invariants. That fiber decomposes into 17 exact `F^5` cycles, including the 1,941-state reference macrocycle. Within the fiber, three collision-orientation frames identify the exact reference state; across all 2,209 fiber states, nine frames uniquely identify every state.

These are constructive demonstrations that period and phase can be localized when the dynamics and state space are specified. They do not provide a recurrence period for the physical universe.

## 4. A cosmic coordinate without a recurrence claim

Cosmic Coordinate introduces a separate coordinate grammar:

`M / Phi_C`.

The composition phase is

`Phi_C = (2/pi) atan(rho_DE/rho_m)`.

For the declared flat matter+Lambda reference values `H0=68.11 km s^-1 Mpc^-1`, `Omega_m0=0.3042`, and `Omega_Lambda0=0.6958`, the present reference coordinate is

`M3 / Phi_C=0.7376`,

with reference age 13.787 Gyr. `M3` denotes the dark-energy-dominated accelerating era. `M4` is a project-defined deep-dark-energy threshold beginning when the dark-energy fraction reaches 0.90; under the unchanged reference model it occurs about 7.077 Gyr after the present reference point.

The coordinate is intentionally descriptive. `Phi_C` is not a percentage of total cosmic lifetime, not a count of prior universes, and not a recurrence phase. It provides the “where are we now?” component without assuming the existence of a cosmic cycle.

## 5. Fate-conditioned recurrence

The far-future branch determines whether a recurrence argument is even available.

| Future branch | Recurrence status |
|---|---|
| Stable eternal de Sitter | Conditional thermodynamic recurrence route if finite recurrent-patch assumptions hold |
| Metastable de Sitter | Recurrence competes with vacuum decay; decay lifetime is not observationally identified |
| Fading dark energy | Standard de Sitter recurrence argument does not automatically apply |
| Phantom finite end | Finite future endpoint; standard eternal de Sitter route is unavailable |
| Recollapse | A crunch alone does not imply state recurrence |
| Cyclic/bounce | Potentially recurrent only if an explicit cycle map returns states |

A Big Crunch therefore does not solve the recurrence problem by itself. Contraction need not be exact time reversal. Likewise, an “empty” universe does not define a unique reset state: geometry, vacuum structure, fields, topology, horizons, boundary conditions, and quantum state remain part of the physical specification.

## 6. Conditional de Sitter scale

For a stable positive-Lambda future, the conventional causal-patch thermodynamic estimate takes the form

`t_thermo ~ H_Lambda^-1 exp(S_dS/k_B)`.

At the CPS reference point, CRPS obtains a de Sitter horizon time of 17.2105 Gyr, horizon entropy `S_dS/k_B = 3.18835 × 10^122`, and

`log10(t_thermo/yr) = 1.38468 × 10^122`.

The official DESI DR2+CMB flat-LambdaCDM posterior can be propagated through this conditional branch. The weighted posterior median recurrence exponent is `1.37911 × 10^122` with a 95% interval `[1.34391, 1.41616] × 10^122`. The observational parameter uncertainty is tiny relative to the branch-level uncertainty: changing the far-future physics can remove the recurrence route entirely.

This thermodynamic scale must not be relabeled as a quantum epsilon-recurrence time. Finite-system quantum recurrence theorems require microscopic spectral inputs and a specified state-distance tolerance. Current cosmological data do not identify the needed finite Hamiltonian spectrum or energy span.

## 7. Probability architecture and future weights

The recurrence probability can be written schematically as

`P(R<T | D) = sum_(M,A) integral P(R<T | M,theta,A) p(theta,M,A | D) dtheta`,

where `D` denotes observations, `M` a future model, `theta` measured parameters inside that model, and `A` additional recurrence-theory assumptions.

Only part of this expression is identified by current data. A restricted equal-prior comparison based on the cited Bayesian reanalysis of DESI DR2 BAO + Planck CMB gives normalized two-model weights of 63.9% for LambdaCDM and 36.1% for `w0-wa`CDM. Those numbers answer a model-selection question inside a declared two-model set; they do not say there is a 63.9% chance of eternal de Sitter recurrence.

CRPS therefore exposes within-family fate splits as sensitivity assumptions. Under the neutral maximum-entropy bookkeeping split, the illustrative weights are:

| Future | Illustrative weight |
|---|---:|
| Stable eternal de Sitter | 31.9% |
| Metastable de Sitter | 31.9% |
| Fading dark energy | 9.0% |
| Phantom finite end | 9.0% |
| Recollapse | 9.0% |
| Cyclic/bounce | 9.0% |

These restricted model-family weights are not measured ultimate-fate probabilities and do not span all cosmological theories. Alternative declared splits in the repository move the stable eternal de Sitter weight from about 16.0% in a recurrence-conservative map to 47.9% in a recurrence-favoring map, demonstrating that the apparent precision is controlled by unresolved theory assumptions.

The rigorous current-data-only statement is therefore

`P(recurrence | current observations, unrestricted future theory) in [0,1]`.

Because this is the full logical probability range, it is a partial-identification/non-identifiability result rather than an informative probability estimate. Prior-conditioned illustrative recurrence intervals can be narrower, but their interpretation must remain theoretical sensitivity rather than observational posterior probability.

## 8. Can we determine whether we are already in a recurrence loop?

No current result in this framework establishes that proposition.

A positive result would require a physically justified state space and cosmic evolution law known to satisfy an applicable recurrence condition, enough observation to localize the relevant state despite hidden variables, and a mapping from measured cosmic variables to recurrence invariants/period/phase. At present, the framework has only the middle pieces in model systems and the cosmological reference/fate analysis. It does not have empirical evidence for a cosmic recurrence cycle.

Accordingly, the most precise present statement is:

- **cosmic reference coordinate:** `M3 / Phi_C=0.7376` under Cosmic Coordinate;
- **physical recurrence period:** not identified;
- **physical recurrence phase:** not identified;
- **physical recurrence-loop membership:** not established;
- **unrestricted recurrence probability:** partially identified only as `[0,1]`.

## 9. Implications

The integration changes the quality of the recurrence question even though it does not produce a sensational single percentage.

First, it replaces vague statements such as “if things line up again, everything repeats” with an exact condition: the **complete predictive state** must return, not merely a visible macrostate. Second, it shows that recurrence navigation can be a tractable inverse problem in a known finite dynamics. Third, it gives the present universe a compact reference coordinate without falsely implying a cycle. Fourth, it demonstrates quantitatively that cosmological parameter uncertainty within a chosen stable de Sitter branch is not the main obstacle; far-future model uncertainty and microscopic recurrence assumptions dominate. Finally, it makes explicit why a Big Crunch, bounce, or empty state is not automatically equivalent to a reset.

## 10. Limitations

The combined framework does not identify the fundamental state space of quantum gravity, establish that the universe is finite, prove stable de Sitter space has a finite effectively closed Hilbert space, measure vacuum lifetime, determine the exact future behavior of dark energy, or derive a recurrent bounce map. The HPP models are diagnostic laboratories, not models of the actual universe. The CPS reference history is deliberately conditional. The CRPS probability layer is partially identified and model-set dependent where Bayesian weights are used.

These limitations are structural, not numerical bugs. More computational precision cannot replace missing physical assumptions.

## 11. Conclusion

A coherent recurrence program must separate **state recurrence**, **observational equivalence**, **period/phase navigation**, **present cosmological coordinates**, **future fate**, and **probability identification**. When those layers are kept separate, several strong results survive: exact recurrence and hidden-state ambiguity can be rigorously demonstrated in finite reversible systems; recurrence periods and phases can be inferred from invariant structure in such systems; the present universe can be assigned the model-conditional CPS coordinate `M3 / Phi_C=0.7376`; and an eternal stable de Sitter future supports a conventional entropy-exponential thermodynamic recurrence scale. What does not survive is the claim that current observations already show a recurrence loop or determine its chance. The scientifically defensible frontier is conditional: cosmic recurrence remains physically possible under some future theories, but its occurrence, exact timescale, and probability are not presently identified in a model-independent way.

## Component references

1. Sundy, S. A. (2026). *Recurrence Dynamics Framework: Predictive State Quotients, Period Constraints, and Phase Navigation*.
2. Sundy, S. A. (2026). *CPS Cosmic Coordinate*.
3. Sundy, S. A. (2026). *Cosmological Recurrence Probability Study: A Fate-Conditioned Partial-Identification Framework*.
4. DESI Collaboration (2025). *DESI DR2 Results II: Measurements of Baryon Acoustic Oscillations and Cosmological Constraints*, arXiv:2503.14738.
5. DESI Collaboration (2026). *DESI DR2 Results IV: Alcock-Paczynski Measurements from the Lyman Alpha Forest and Cosmological Constraints*, arXiv:2607.27410.
6. Ong, D. D. Y., Yallup, D., & Handley, W. (2026). *The Bayesian view of DESI DR2 with unimpeded*, arXiv:2603.05472v2.

The full theoretical bibliography for thermodynamic, Poincare, de Sitter, phantom-future, and quantum recurrence results is retained in the component manuscripts and source files.

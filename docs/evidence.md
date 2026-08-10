# Evidence register

The combined repository deliberately keeps evidence levels separate.

| Claim/result family | Evidence type | Scope |
|---|---|---|
| HPP transport clock | analytic proof | finite HPP lattice gas |
| HPP diagonal histogram clocks | analytic proof | finite HPP lattice gas |
| HPP row/column line momenta | analytic proof | finite HPP lattice gas |
| 3×3 ambiguity classification | exhaustive finite computation + independent verifier | declared 9,153-state sector |
| 3×3 exact-mask sensor threshold | exhaustive fixed-site subset search + regression certificate | declared 9,153-state sector |
| 3×3 local-momentum sensor threshold | exhaustive fixed-site subset search + regression certificate | declared 9,153-state sector |
| 3×3 density-predictive cycle count | exhaustive quotient-cycle enumeration + regression certificate | declared 9,153-state sector |
| Protocol-family predictive quotient | theorem-level construction | declared model and protocol family |
| Prediction-sufficient factorization | theorem | deterministic prediction-sufficient representations |
| Operational discrimination pseudometric | theorem/definition | declared probabilistic protocol family |
| 3×3 and 4×4 period classes | exhaustive finite computation | declared finite sectors |
| 5×5 seed-75202 interaction fiber | exhaustive constrained enumeration | one invariant fiber |
| 5×5 phase/sensor results | deterministic computation | one exact reference orbit/fiber |
| 500-state period-scale predictor | empirical cross-validation | fixed sampled HPP population |
| CPS coordinate equations | analytic mapping within declared reference cosmology | flat matter+Lambda reference |
| CPS current coordinate | numerical evaluation of declared reference inputs | model-conditional |
| DESI posterior propagation | observational posterior propagation inside flat LambdaCDM | conditional cosmological branch |
| Bayesian LambdaCDM vs w0waCDM weights | published Bayesian evidence + declared equal model priors | restricted two-model set |
| Fate decomposition weights | explicit sensitivity assumptions | not measured probabilities |
| Stable de Sitter entropy/exponential scale | standard conditional thermodynamic estimate | declared branch assumptions |
| Quantum epsilon recurrence | theorem-level finite-system framework | no cosmological numerical result |
| Unrestricted cosmic recurrence probability `[0,1]` | partial-identification / non-identifiability statement; not an estimated probability distribution | current data + unrestricted future theory |
| Observer-indistinguishable HPP doubletons | exhaustive exact certificate | declared site-density observer |
| Observer perturbation detection times | deterministic experiments | bundled conserved-sector trials |
| Quantum trace-distance discrimination rule | analytic operational identity | declared quantum states |

## Rule for cross-module inference

A result may be used as a definition, diagnostic analogy, or consistency check across modules. It may not be promoted to a stronger evidence level merely because another module exists.

Examples:

- Exact HPP recurrence does not provide evidence for exact cosmological recurrence.
- The CPS coordinate may provide a reference parameter point for a cosmological calculation, but it does not establish the future branch.
- The CRPS de Sitter entropy may set a conditional thermodynamic scale, but it does not supply the microscopic spectral inputs required by a finite-system quantum recurrence bound.

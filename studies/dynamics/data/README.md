# Computational data

Every CSV and PNG in this directory is produced deterministically with `scripts/validate.py`.

```bash
python scripts/validate.py reproduce
```

An independent temporary regeneration and comparison is available through:

```bash
python scripts/validate.py reproduction
```

| Folder | Contents |
|---|---|
| `binary_cellular_automaton` | Exact two-snapshot reconstruction result and period-eight reference orbit |
| `square_lattice_gas` | Exact period-175 orbit, density closure failure, complete 54-state ambiguity catalog, representative paired-cycle figure, perturbation history, and size sweep |
| `conserved_sector_perturbations` | 150 paired trials with fixed particle number, momentum, energy, and initial density |
| `fixed_density_scaling` | 1,200 paired trials across sizes and velocity-channel fillings |
| `hexagonal_rotor_gas` | 900 reversible six-direction lattice-gas trials with hidden rotor memory |
| `continuous_dynamics` | Exact rational hard-particle orbit and irrational-torus near returns |

The exhaustive observability calculations are performed directly from the model code during generation and validation. `ambiguity.csv` is a complete machine-readable certificate of the 54 exceptional HPP states, not a sampled summary.

| `period_navigation` | Exact recurrence-period constraints, 3x3/4x4 exhaustive period certificates, 5x5 interaction-fiber decomposition, phase-navigation summaries, and the fixed 500-state period sample |

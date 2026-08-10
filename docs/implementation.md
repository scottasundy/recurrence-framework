# Implementation Guide

This repository is designed as a reproducible research program rather than a single monolithic calculation. The implementation deliberately separates four questions that are often conflated: recurrence in a fully specified dynamics, recurrence relative to a restricted observer, cosmological state description, and fate-conditioned cosmological inference.

## 1. Architecture

```text
studies/dynamics/
    Exact finite-state recurrence, predictive quotients, observability,
    perturbations, continuous near recurrence, period constraints, phase navigation.

studies/observer/
    Observer-relative distance, detection-time, torus-threshold, and quantum
    distinguishability calculations using outputs from the dynamics study.

studies/coordinate/
    Model-conditional cosmological coordinate and timeline.

studies/cosmology/
    Conditional de Sitter calculations, observational parameter propagation,
    future-model sensitivity, and partial identification of recurrence probability.

scripts/
    Cross-module verification and repository integrity.

tests/
    Umbrella consistency tests.
```

No module is allowed to use a toy-model recurrence result as evidence that the physical universe is recurrent. Cross-module inference is only valid when the assumptions required by both modules are explicitly carried across.

## 2. Core finite-state representation

The HPP implementation stores a lattice microstate as an immutable tuple of four-bit site masks. Each bit corresponds to one velocity channel. The update is a reversible collide-then-stream map on a periodic lattice.

Important implementation properties:

- collision is an involution;
- streaming is a permutation;
- the combined update is bijective;
- exact state equality is integer/tuple equality, not a floating-point tolerance;
- particle number and momentum provide sector constraints;
- deterministic enumeration makes exhaustive certificates possible for the small sectors used here.

The principal implementation is:

`studies/dynamics/src/recurrence_dynamics/hpp.py`

## 3. Predictive partitions

For a deterministic observation map `h`, the finite implementation refines state classes using increasingly long observation words:

```text
h(x)
(h(x), h(Fx))
(h(x), h(Fx), h(F^2 x))
...
```

Refinement stops when no classes split. The stable partition is the complete-future predictive quotient for the finite deterministic sector.

The reusable utilities are in:

`studies/dynamics/src/recurrence_dynamics/finite_orbits.py`

The generalized protocol-family mathematics is documented in:

`studies/dynamics/docs/predictive-quotient.md`

The conceptual generalization is:

```math
\mathcal R_A(x)=\bigl(P_\pi(\cdot\mid x)\bigr)_{\pi\in A},
\qquad
x\sim_Ax'\iff\mathcal R_A(x)=\mathcal R_A(x').
```

This cleanly separates a state-description difference from a difference that changes at least one permitted physical prediction.

## 4. Exact observability search

The exhaustive 3x3 HPP sensor study enumerates the full four-particle, zero-momentum sector and tests fixed-site sensor subsets.

Implemented sensor families include:

- exact velocity masks at selected sites;
- local momentum vectors at selected sites;
- all-site horizontal/vertical axis counts;
- site density.

The reproduction entry point is:

```bash
cd studies/dynamics
python scripts/reproduce_observability.py
```

It regenerates:

- `mask-search.csv`
- `momentum-search.csv`
- `observability.json`
- `predictive-cycles.csv`

The regression certificate is:

`studies/dynamics/tests/test_hpp_observability_extension.py`

## 5. Microscopic and predictive cycles

Finite reversible sectors are decomposed into exact cycles by orbit traversal. The density-predictive quotient induces its own deterministic cycle structure because complete-future predictive equivalence is forward invariant.

The implementation explicitly distinguishes:

- microscopic cycle count;
- quotient/predictive cycle count;
- cycle merging;
- period compression.

For the certified 3x3 HPP sector, nine pairs of period-three microscopic cycles merge under the density quotient and no period compression occurs.

## 6. Period and phase navigation

The period-navigation module uses invariant structure before orbit search. The intended flow is:

```text
complete state
    -> analytic period divisors / conserved quantities
    -> invariant interaction fiber
    -> exact cycle
    -> phase localization
```

The implementation includes:

- scalar transport clocks;
- diagonal-species transport clocks;
- line-momentum invariants;
- checkerboard sign modes;
- collision-word diagnostics;
- constrained interaction-fiber enumeration;
- constant-memory orbit period finding;
- atlas-free phase localization after a period is known.

Main files:

- `studies/dynamics/src/recurrence_dynamics/periods.py`
- `studies/dynamics/scripts/generate_periods.py`
- `studies/dynamics/scripts/verify_periods.py`
- `studies/dynamics/data/periods/`

## 7. Near recurrence in continuous systems

The repository intentionally includes two qualitatively different continuous examples.

1. An exactly periodic elastic-particle ring demonstrates an exact continuous return.
2. An irrational torus flow demonstrates arbitrarily close returns without an exact positive-time return.

This is why every numerical near-recurrence claim must declare a metric, tolerance, numerical precision, and search horizon.

## 8. Observer layer

The observer module treats recurrence as relative to accessible records rather than raw state distance. It includes:

- exact zero observer-distance HPP ambiguity examples;
- perturbation detection times;
- tolerance crossings for the irrational torus;
- quantum trace-distance examples;
- an explicit refusal to assign a numerical human-observer recurrence threshold without a physical observer model.

Run:

```bash
cd studies/observer
python run.py
```

## 9. Cosmic coordinate

The coordinate module maps a declared reference cosmology to a descriptive coordinate. It does not assume cyclic dynamics.

Run:

```bash
cd studies/coordinate
python clock.py
```

The coordinate specification and the frozen cosmology copy are byte-for-byte checked by the umbrella integration tests.

## 10. Fate-conditioned cosmology

The cosmology module keeps three uncertainty layers separate:

1. observational parameter uncertainty inside a chosen cosmological model;
2. model-family/future-fate uncertainty;
3. recurrence-mechanism and microscopic-state uncertainty.

It propagates the first where source data are available and exposes the second and third as sensitivity or non-identification rather than inventing a single measured probability.

Run:

```bash
cd studies/cosmology
python run.py
```

## 11. Repository-level verification

Fast verification:

```bash
python scripts/verify.py
```

Main output regeneration plus verification:

```bash
python run.py
```

Deep deterministic reproduction, including the exact HPP sensor search:

```bash
python run.py --full
```

Integrity manifest:

```bash
python scripts/manifest.py
```

## 12. Evidence discipline

Every important result should be classifiable as one of:

- **EXACT** — exhaustive computation or exact algebra for the declared model;
- **THEOREM** — mathematical result under explicit assumptions;
- **DERIVED** — direct consequence of definitions or proved statements;
- **CONDITIONAL** — valid only under an explicit physical branch or theory assumption;
- **CONCEPTUAL** — interpretation or research consequence;
- **METAPHYSICAL** — optional ontological principle or underdetermination statement;
- **AUDIT** — correction or simplification established by the mathematics review;
- **AUXILIARY** — result preserved but not promoted without its own primary regression certificate.

The complete ledger is `docs/findings.md`.

## 13. Extension protocol

A new recurrence study should declare, in order:

1. the state space or state representation;
2. the evolution law;
3. the analyzed sector or probability measure;
4. the observation/protocol family;
5. exact versus approximate equality;
6. the recurrence target;
7. the metric and tolerance for near recurrence;
8. the finite or infinite horizon being claimed;
9. the evidence type;
10. the boundary preventing the result from being generalized beyond its assumptions.

This order prevents the most common recurrence error: calculating a return time before defining what is supposed to return.

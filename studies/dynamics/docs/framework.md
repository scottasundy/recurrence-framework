# Recurrence Dynamics Framework

## A diagnostic protocol for predictive observability, hidden-state ambiguity, and recurrence under incomplete observation

**Author:** Scott A. Sundy  
**Version:** 1.0  
**Date:** July 2026  
**Intended repository location:** `docs/framework.md`

---

## 1. Purpose

The Recurrence Dynamics Framework is a general diagnostic protocol for determining whether an observed state contains enough information to predict a system's future.

The framework begins from a strict distinction:

> Equality of observations is not necessarily equality of complete predictive states.

A deterministic system may contain variables that are omitted by a chosen measurement, recording scheme, sensor, coarse-graining, or interface. Two complete states can therefore look identical at the present time while differing in their future behavior. In more exceptional cases, two different complete states can remain observationally identical forever under the chosen observation map.

The framework provides a common procedure for identifying and classifying these possibilities.

Its rigorous core applies to finite deterministic systems, where the complete state space can be enumerated and predictive equivalence can be computed exactly. The same conceptual structure can also guide finite-horizon, sampled, approximate, or model-based diagnostics in larger, continuous, stochastic, partially observed, or quantum settings, but those extensions require separate assumptions and do not inherit the finite exact guarantees automatically.

This document extends the accompanying study, [*Predictive State Quotients and Irreducible Hidden-State Ambiguity in Reversible Dynamics*](../paper/paper.pdf), from a collection of exact results into a reusable framework.

---

## 2. Framework object

A dynamics problem is specified by the tuple

\[
\mathcal{D}=(X,F,h,\mathcal{S},\mathcal{T}),
\]

where:

- \(X\) is the complete state space;
- \(F:X\to X\) is the deterministic update map;
- \(h:X\to Y\) is the observation or coarse-graining map;
- \(\mathcal{S}\subseteq X\) is the state sector being analyzed;
- \(\mathcal{T}\) is the declared observation horizon or stopping rule.

The framework requires the analyst to separate five objects that are often conflated:

1. **Complete state** — all variables required to make the update rule single-valued.
2. **Present observation** — the value \(h(x)\) recorded from the complete state.
3. **Finite observation word** — a sequence of observations over a declared horizon.
4. **Complete future observation sequence** — the full observation trajectory generated from a state.
5. **Exact complete-state trajectory** — the actual orbit under \(F\).

The distinction is operational, not semantic. Every conclusion must identify which object has repeated or become equivalent.

---

## 3. Core definitions

### 3.1 Complete-state recurrence

A complete state \(x\) has exact recurrence time \(T>0\) when

\[
F^T x=x.
\]

For deterministic dynamics,

\[
F^T x=x
\quad\Longrightarrow\quad
F^{t+T}x=F^t x
\]

for every \(t\geq0\).

This result concerns the complete state. A repeated image, density field, position snapshot, conserved quantity, or other reduced record is not enough unless that record is already known to determine the complete predictive state.

### 3.2 Present observational equivalence

Two states are present-observation equivalent when

\[
x\equiv_h x'
\quad\Longleftrightarrow\quad
h(x)=h(x').
\]

This relation identifies states that look the same at one instant under the selected observation.

### 3.3 Finite-horizon equivalence

For a positive integer \(r\), define the length-\(r\) forward observation word

\[
D_r(x)=\bigl(h(x),h(Fx),\ldots,h(F^{r-1}x)\bigr).
\]

States are equivalent through horizon \(r\) when

\[
x\equiv_{h,r}x'
\quad\Longleftrightarrow\quad
D_r(x)=D_r(x').
\]

Finite-horizon agreement is evidence of observational similarity over the declared interval. It is not, by itself, proof of permanent equivalence.

### 3.4 Predictive future equivalence

Two complete states are future-equivalent under \(h\) when

\[
x\sim_h x'
\quad\Longleftrightarrow\quad
h(F^t x)=h(F^t x')
\]

for every \(t\geq0\).

The equivalence classes of \(\sim_h\) are the **predictive states induced by the observation**.

The quotient

\[
Q_h=X/{\sim_h}
\]

is the coarsest deterministic state representation that preserves the complete future observation process. It removes microscopic distinctions that never affect the selected future observations while retaining every distinction that does.

### 3.5 One-step observational closure

The raw observation is closed when there is a deterministic map

\[
G:h(X)\to h(X)
\]

such that

\[
h\circ F=G\circ h.
\]

Equivalently,

\[
h(x)=h(x')
\quad\Longrightarrow\quad
h(Fx)=h(Fx')
\]

for all analyzed states.

Closure means that the present observed value alone determines the next observed value. Failure of closure means that the observation omits predictive information.

### 3.6 Hidden-state ambiguity

A pair \(x\neq x'\) has hidden-state ambiguity under \(h\) when

\[
h(x)=h(x').
\]

The ambiguity is:

- **immediate** if the next observations differ;
- **delayed** if the observations agree temporarily and later diverge;
- **permanent** if \(x\sim_h x'\);
- **symmetry-generated** if a verified transformation maps one state to the other while preserving the observation process;
- **unresolved** if the diagnostic horizon ends before divergence or proof of permanence.

The term hidden state refers only to variables omitted by the specified observation map. It does not imply a new physical variable, a hidden-variable interpretation of quantum mechanics, or an unknown law of nature.

---

## 4. Diagnostic classification

Every analyzed state pair should be assigned to one of the following classes.

### Class A — Exact complete-state recurrence

\[
F^T x=x.
\]

The complete state and its entire subsequent evolution repeat with period dividing \(T\).

### Class B — Closed observational recurrence

\[
h(F^T x)=h(x)
\]

and the observation map is known to be closed on the relevant sector.

The repeated observation determines the repeated predictive state within that closed reduced model. It still need not imply microscopic equality unless \(h\) is injective.

### Class C — Temporary observational recurrence

\[
D_r(F^T x)=D_r(x)
\]

for a finite \(r\), but later observations differ.

This is a finite-duration observational match, not recurrence of the complete state or predictive state.

### Class D — Predictive equivalence without microscopic equality

\[
x\neq x',
\qquad
x\sim_h x'.
\]

The complete states differ, but the selected observation cannot distinguish their future trajectories, even with an arbitrarily long exact record.

### Class E — Present ambiguity with future separation

\[
h(x)=h(x'),
\qquad
h(F^k x)\neq h(F^k x')
\]

for some \(k>0\).

The present observation is insufficient, but a sufficiently long observation history resolves the states.

### Class F — Near recurrence

A declared metric \(d\) satisfies

\[
d(F^T x,x)<\varepsilon
\]

for a chosen tolerance \(\varepsilon>0\), while exact equality is absent or untested.

Near recurrence must always report the metric, tolerance, variables compared, precision model, and search horizon. It cannot be silently upgraded to exact recurrence.

### Class U — Unresolved

The available calculation or observation horizon does not establish divergence, exact recurrence, or permanent equivalence.

A capped search is unresolved or censored. It is not evidence of nonrecurrence or permanent equivalence.

---

## 5. Exact finite-state protocol

For finite deterministic systems, the framework can be implemented exactly.

### Step 1 — Declare the complete state

Specify every variable required for \(F\) to be single-valued.

Examples include:

- positions and velocities;
- two consecutive configurations for a second-order rule;
- particle channels rather than density alone;
- local collision-memory or rotor variables;
- controller memory, queue contents, or agent state;
- environmental state that influences the next update.

A state description is incomplete if two physical or computational configurations with the same declared state can evolve differently under the same stated rule.

### Step 2 — Declare the sector

Define the analyzed subset \(\mathcal{S}\subseteq X\), including all constraints:

- lattice size;
- boundary conditions;
- particle number;
- conserved quantities;
- admissibility rules;
- parameter values;
- initial-condition restrictions.

Claims must be scoped to this sector unless a proof covers the full state space.

### Step 3 — Verify invariance

Check that

\[
F(\mathcal{S})\subseteq\mathcal{S}.
\]

If the sector is not forward invariant, either enlarge it or explicitly define how trajectories leaving the sector are handled.

### Step 4 — Declare the observation map

Specify \(h\) as an explicit function of the complete state.

Examples include:

- site density;
- position only;
- image pixels;
- aggregate energy;
- conserved quantities;
- selected sensor channels;
- an AI system's visible prompt and response;
- a reduced density matrix or measurement record.

The analysis is always conditional on this map. Richer observations can split ambiguity classes that remain merged under poorer observations.

### Step 5 — Build the initial partition

Group states by present observation:

\[
P_1=\bigl\{\{x\in\mathcal{S}:h(x)=y\}:y\in h(\mathcal{S})\bigr\}.
\]

This partition measures present observational ambiguity.

### Step 6 — Refine by future behavior

Given a partition \(P_r\), assign each state the signature

\[
\sigma_r(x)=\bigl(h(x),[Fx]_{P_r}\bigr),
\]

where \([Fx]_{P_r}\) is the block of \(P_r\) containing the successor.

States with different signatures are split. The resulting partition is \(P_{r+1}\).

Equivalent direct construction:

\[
x\equiv_{h,r}x'
\quad\Longleftrightarrow\quad
D_r(x)=D_r(x').
\]

Repeat until

\[
P_{r+1}=P_r.
\]

Because the state set is finite and the partitions only refine, the process terminates.

### Step 7 — Interpret the stable partition

Let \(P_\ast\) be the first stable partition.

Three principal outcomes are possible:

1. **Raw closure:** \(P_2=P_1\).  
   The current observation determines its next value.

2. **Finite reconstruction:** \(P_\ast\) is discrete.  
   Every complete state is uniquely determined by a sufficiently long finite observation word.

3. **Irreducible ambiguity:** \(P_\ast\) has nonsingleton blocks.  
   Distinct complete states generate identical complete future observation sequences.

The smallest \(r\) for which \(P_r=P_\ast\) is a finite observability horizon for the analyzed finite sector.

### Step 8 — Analyze each nonsingleton class

For every predictive class \(C\in P_\ast\) with \(|C|>1\), determine:

- class size;
- orbit periods;
- transient lengths, if any;
- conserved quantities;
- symmetry relations;
- whether states occupy the same or different microscopic cycles;
- phase alignments;
- the omitted variables distinguishing class members;
- the smallest added measurement that separates them.

### Step 9 — Verify completeness independently

A strong computer-assisted classification should include an independent verifier that reconstructs the result from lower-level model definitions rather than trusting the high-level implementation or a committed catalog.

The verifier should reject:

- missing or duplicate states;
- invalid sector membership;
- incorrect successors or predecessors;
- wrong orbit periods;
- incorrect symmetry partners;
- false observation matches;
- omitted nonsingleton classes;
- unverified claims of uniqueness.

---

## 6. Reference pseudocode

```text
INPUT:
    finite state sector S
    deterministic update F
    observation map h

P := partition S by h(x)
history := [P]

repeat:
    signature(x) := (h(x), block_id(P, F(x)))
    P_new := partition S by signature(x)
    append P_new to history

    if P_new == P:
        break

    P := P_new

OUTPUT:
    stable predictive partition P
    refinement history
    singleton and nonsingleton class counts
    observability horizon
```

For deterministic finite systems, stabilization certifies complete future equivalence because two states in the same stable block have the same present observation and successors in the same stable block indefinitely.

---

## 7. Required framework outputs

A complete framework report should produce the following.

### 7.1 State-space specification

- definition of the complete state;
- size of the full state space or analyzed sector;
- sector constraints;
- update convention;
- reversibility status;
- conservation laws.

### 7.2 Observation specification

- explicit formula or procedure for \(h\);
- variables retained;
- variables discarded;
- whether \(h\) is injective;
- whether one-step closure holds.

### 7.3 Refinement profile

Report

\[
|P_1|,|P_2|,\ldots,|P_\ast|.
\]

This profile shows how rapidly future observations resolve present ambiguity.

### 7.4 Predictive class profile

Report:

- number of singleton classes;
- number of nonsingleton classes;
- class-size distribution;
- number and fraction of ambiguous microscopic states;
- maximum class size.

### 7.5 Resolution-time profile

For distinguishable pairs with equal present observation, report the first divergence time

\[
\tau(x,x')=
\min\{t\geq0:h(F^t x)\neq h(F^t x')\}.
\]

Pairs with no such time belong to the same predictive class.

### 7.6 Information-loss measures

Given a declared probability distribution over complete states, useful quantities include:

\[
H(X\mid h(X))
\]

for uncertainty after one observation, and

\[
H(X\mid W)
\]

for residual uncertainty after the complete future observation record \(W\).

These values depend on the state sector, observation map, and prior. They are not universal properties of the dynamics.

### 7.7 Symmetry certificate

When ambiguity is symmetry-generated, report:

- the symmetry or involution \(R\);
- whether \(R^2=I\);
- its relationship to the dynamics, such as
  \[
  RFR=F^{-1};
  \]
- observation invariance, such as
  \[
  h\circ R=h;
  \]
- orbit distinctness;
- required temporal or phase alignment.

---

## 8. Time-reversal ambiguity module

For a reversible system, suppose there is an involution \(R:X\to X\) satisfying

\[
R^2=I,
\qquad
RFR=F^{-1},
\qquad
h(Rx)=h(x).
\]

Then

\[
h(F^tRx)=h(F^{-t}x).
\]

Time reversal converts the future observation of the reversed state into the past observation of the original state.

For a periodic orbit of period \(p\), permanent future ambiguity can occur when its observation word is invariant under temporal reversal up to a cyclic shift. Specifically, if there is an integer \(s\) such that

\[
h(F^t x)=h(F^{s-t}x)
\]

for all \(t\) modulo \(p\), then the phase-aligned reversed state

\[
z=F^{-s}Rx
\]

satisfies

\[
h(F^t z)=h(F^t x)
\]

for every \(t\geq0\).

This criterion does not state that every reversible trajectory is ambiguous. It identifies a specific mechanism requiring all of the following:

1. reversible dynamics;
2. an observation invariant under the reversal transformation;
3. a periodic observation word with the required reversal symmetry;
4. a distinct reversed microscopic orbit or phase;
5. correct phase alignment.

---

## 9. HPP benchmark case

The reference exact application is the \(3\times3\) periodic Hardy-Pomeau-de Pazzis lattice gas in the complete four-particle, zero-momentum sector under sitewise-density observation.

The sector contains exactly 9,153 microscopic states.

The refinement profile is:

| Observation-word length | 1 | 2 | 3 | 4 | 5 |
|---:|---:|---:|---:|---:|---:|
| Number of classes | 495 | 6,948 | 9,090 | 9,126 | 9,126 |

The stable quotient contains:

- 9,126 predictive classes;
- 9,099 singleton classes;
- 27 doubleton classes;
- 54 ambiguous microscopic states.

The exceptional structure is

\[
54=18\times3=9\times2\times3.
\]

It consists of:

- 18 collision-free microscopic cycles;
- least period 3 for every cycle;
- 9 time-reversal orbit pairs;
- 2 distinct microscopic cycles in each pair;
- 3 aligned predictive doubletons per pair.

Density records the number of particles at each site but omits their velocity channels. In the exceptional cycles, reversing every velocity produces a distinct microscopic orbit whose density sequence is identical after the correct phase alignment.

This benchmark demonstrates all major framework components:

- present observational ambiguity;
- exact partition refinement;
- finite observability horizon;
- permanent predictive ambiguity;
- symmetry-based explanation;
- exhaustive enumeration;
- independent certification;
- strict limitation of the result to a declared sector and observation map.

The benchmark is not evidence that every coarse-grained physical system contains the same ambiguity mechanism.

---

## 10. Application protocol for new systems

A new application should answer the following questions in order.

### A. What is the complete state?

What variables must be known for the next state to be uniquely determined?

### B. What is actually observed?

Which components are measured, recorded, exposed, or retained?

### C. What distinctions are discarded?

List velocities, phases, memory variables, labels, latent modes, environmental variables, or other omitted components.

### D. Does the present observation close?

Can two states with the same observation produce different next observations?

### E. How much history is sufficient?

Does a finite delay word reconstruct the complete state or at least the predictive quotient?

### F. Does irreducible ambiguity remain?

Are there distinct states that generate the same complete future observation process?

### G. What causes the ambiguity?

Possible mechanisms include:

- symmetry;
- time reversal;
- relabeling;
- gauge redundancy;
- conservation-law degeneracy;
- hidden memory;
- unmeasured velocity or phase;
- coarse spatial or temporal resolution;
- insufficient sensor placement.

### H. What added measurement resolves it?

Test candidate augmented observations

\[
\tilde h(x)=\bigl(h(x),g(x)\bigr)
\]

and recompute the predictive partition.

The smallest practical \(g\) that removes the target ambiguity is a candidate minimal sensor or state augmentation.

---

## 11. Domain extensions

### 11.1 AI agents and computational systems

For an AI or software agent, the complete state may include:

- visible input;
- conversation history;
- retrieved documents;
- persistent memory;
- tool state;
- random seed;
- planner state;
- environment state;
- queued actions;
- hidden controller variables.

Two agents can receive the same visible prompt while occupying different complete states. The framework can test whether the visible interface is sufficient to reproduce or predict behavior.

A rigorous application must not infer internal model states merely because outputs differ. It must define an executable state representation and controlled update procedure.

Potential outputs include:

- reproducibility classes;
- hidden-context sensitivity;
- minimum context needed for stable behavior;
- tool-state ambiguity;
- trajectory divergence time;
- behaviorally equivalent internal configurations.

### 11.2 Sensors and robotics

A sensor output may omit velocity, depth, orientation, occluded objects, actuator state, or environmental context.

The framework can identify:

- sensor aliases;
- first divergence times;
- unsafe observation classes;
- minimum added sensors;
- histories required for state estimation;
- states that remain behaviorally indistinguishable under the installed sensors.

### 11.3 Coarse-grained physics

Density, pressure, temperature, energy, and other macroscopic fields usually identify many microscopic states.

The framework distinguishes:

- ordinary microscopic multiplicity;
- predictive ambiguity that resolves with time;
- irreducible ambiguity under a fixed observable;
- exact complete-state recurrence;
- recurrence of a reduced field;
- near recurrence.

The existence of multiple microstates with the same macrostate is not, by itself, the main result. The diagnostic target is whether those states produce the same or different future observable processes.

### 11.4 Scientific model discrimination

Different mechanisms or parameter states can generate the same measured record over a finite interval.

The framework can be used to construct:

- observational equivalence classes;
- finite discrimination horizons;
- experiment designs that split model classes;
- structural non-identifiability certificates;
- symmetry explanations for indistinguishable predictions.

For continuous parameter spaces, exact finite partition refinement is generally unavailable. The result must then be stated as analytical, numerical, local, approximate, or finite-horizon.

### 11.5 Quantum diagnostics

The framework can be used cautiously as a language for measurement sufficiency and model identifiability.

A quantum application may ask whether a declared measurement record distinguishes:

- candidate states;
- density operators;
- Hamiltonian parameters;
- open-system models;
- hidden classical control states;
- preparation procedures.

The finite deterministic theorem does not apply directly to the continuum of quantum states or to intrinsically probabilistic measurement records. A quantum extension must specify:

- the physical state representation;
- unitary or open-system dynamics;
- measurement protocol;
- equivalence criterion for probability distributions;
- statistical confidence;
- gauge or global-phase conventions;
- finite versus asymptotic identifiability.

The framework can diagnose observational non-identifiability. It does not prove that unknown quantum hidden variables exist.

---

## 12. Extension beyond exact finite systems

The exact finite protocol should be treated as the reference standard. Larger or nonfinite systems require modified evidence levels.

### Level 1 — Exact exhaustive result

Every state in the declared finite sector is analyzed. Stabilization is exact and independently verified.

### Level 2 — Exact analytical result

A theorem establishes closure, reconstruction, equivalence, or recurrence for an infinite family without exhaustive enumeration.

### Level 3 — Exact restricted computation

The computation is exact but covers only a declared subset, parameter range, orbit family, or symmetry class.

### Level 4 — Deterministic sampled diagnostic

A reproducible sample is analyzed with fixed seeds and explicit selection rules. Conclusions apply to the sample, not the full state space.

### Level 5 — Approximate numerical diagnostic

Floating-point tolerances, estimated states, noisy data, or numerical integration are used. Error models and thresholds must be reported.

### Level 6 — Statistical observational study

Equivalence is assessed through distributions, confidence regions, hypothesis tests, or predictive performance. Failure to distinguish is not proof of exact equivalence.

Every reported result should identify its evidence level.

---

## 13. Reporting standard

A study using this framework should include the following statement block.

```text
Complete state:
Update map:
Analyzed sector:
Observation map:
Exact or approximate arithmetic:
Exhaustive, analytical, or sampled:
Observation horizon:
Partition or equivalence method:
Closure result:
Stable predictive class count:
Nonsingleton class distribution:
First-divergence statistics:
Recurrence definition:
Near-recurrence metric and tolerance:
Symmetry mechanism:
Independent verification:
Scope limitation:
```

Recommended terminology:

- **complete-state recurrence** for \(F^T x=x\);
- **observational recurrence** for repeated reduced records;
- **finite-horizon agreement** for matching finite words;
- **predictive equivalence** for identical complete future observation sequences;
- **permanent ambiguity** for distinct complete states in one predictive class;
- **near recurrence** only with a stated metric and tolerance;
- **unresolved** for capped searches without a decisive result.

Avoid:

- calling equal observations identical physical states;
- calling a long finite match permanent without proof;
- calling numerical closeness exact recurrence;
- treating failure to find recurrence as proof of nonrecurrence;
- generalizing a finite sector result to all systems;
- using hidden-state ambiguity as automatic evidence for unknown physics.

---

## 14. Framework claims

The framework supports the following claims when their assumptions are satisfied:

1. A repeated complete state in a deterministic system fixes the subsequent future.
2. A repeated observation need not be a repeated complete or predictive state.
3. Exact predictive sufficiency can be computed by partition refinement in finite deterministic systems.
4. Stable nonsingleton predictive classes certify permanent ambiguity under the selected observation.
5. Symmetries can explain why distinct microscopic states remain predictively equivalent.
6. Additional measurements can be evaluated by how they refine or eliminate ambiguity classes.
7. The minimal predictive quotient is a principled target for reduced-state modeling.
8. Recurrence, reconstruction, observability, and hidden-state ambiguity can be studied within one explicit diagnostic structure.

---

## 15. Nonclaims

The framework does not establish that:

- the physical universe is finite;
- the universe exactly recurs;
- reality is a cellular automaton;
- all systems contain hidden physical variables;
- permanent ambiguity under one observation is permanent under every possible observation;
- quantum mechanics is incomplete;
- identical observations imply parallel universes;
- near recurrence is exact recurrence;
- a sampled absence of recurrence proves nonrecurrence;
- the general concepts of observability, state equivalence, bisimulation, predictive states, or automaton minimization are newly invented here.

The contribution is the integration of these ideas into a recurrence-centered diagnostic protocol, together with an exact, exhaustive, symmetry-explained benchmark in the stated HPP sector.

---

## 16. Repository integration

Recommended repository placement:

```text
docs/
├── math.md
├── framework.md
├── poincare.md
├── quantum.md
└── reproduce.md
```

Recommended README entry:

```markdown
- `docs/framework.md` -
  reusable protocol for predictive observability, hidden-state ambiguity,
  recurrence classification, and extensions to new systems.
```

After adding the file, regenerate the integrity manifest using the repository's declared validation workflow:

```bash
python scripts/validate.py manifest
python scripts/validate.py repository
python scripts/validate.py integrity
```

Then run the complete validation profile:

```bash
python scripts/validate.py all
```

The manifest should be updated only after the new file and any README changes are reviewed and intentional.

---

## 17. Suggested use in future studies

The current HPP study should remain the validated benchmark. New projects can use the framework by creating a system-specific module with:

1. a complete-state definition;
2. an update implementation or analytical law;
3. one or more observation maps;
4. a state-sector generator or sampling protocol;
5. a predictive-equivalence calculation;
6. ambiguity and divergence reports;
7. symmetry diagnostics;
8. independent checks;
9. a limitations statement.

A useful development path is:

```text
HPP benchmark
    ↓
general finite-state analysis API
    ↓
multiple observation maps
    ↓
minimal sensor/state augmentation
    ↓
sampled large-system diagnostics
    ↓
domain-specific extensions
```

The framework becomes scientifically useful when it does more than note that observations can be incomplete. It must identify exactly:

- which states are merged;
- how long they remain merged;
- whether they ever separate;
- what mechanism causes the ambiguity;
- what additional information resolves it;
- and which conclusions are exact versus provisional.

---

## 18. Summary

The Recurrence Dynamics Framework treats recurrence as a state-definition and observability problem.

Its central diagnostic question is:

> Does the recorded observation identify the complete predictive state, or does hidden-state ambiguity remain?

For finite deterministic systems, the answer can be exact. Partition refinement constructs the predictive quotient, determines the observability horizon, identifies every permanent ambiguity class, and supports independent verification.

The HPP result supplies a complete benchmark: 54 states in 27 predictive doubletons, organized into 18 period-three microscopic cycles and 9 time-reversal pairs. The broader framework turns that result into a reusable method for analyzing new dynamical systems without overextending the benchmark beyond its proven scope.

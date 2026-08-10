# Cosmic Recurrence Framework

## Exact recurrence, near recurrence, observer indistinguishability, cosmic position, future fate, and the question of whether reality has a recurrence clock

**Scott A. Sundy**  
**August 2026**  

---


## Repository quick start

This repository is the single master package for the recurrence research program. It contains the conceptual framework, exact deterministic benchmarks, period and phase navigation, continuous near-recurrence examples, quantum recurrence conditions, observer-indistinguishability calculations, the cosmic reference coordinate, fate-conditioned cosmology, numerical outputs, figures, manuscripts, validation scripts, and automated tests.

### Install

```bash
python -m pip install -r requirements.txt
```

### Verify everything

```bash
python scripts/verify.py
```

### Reproduce the main numerical studies

```bash
python run.py
```

For the full deterministic regeneration/validation path as well:

```bash
python run.py --full
```

### Repository map

```text
studies/
  dynamics/            exact/near recurrence, observability, HPP, period/phase navigation
  observer/            observer-indistinguishability calculations and outputs
  coordinate/  reference cosmological coordinate and timeline
  cosmology/           fate-conditioned recurrence probability and de Sitter calculations
docs/                  master findings, theory, interpretation, boundaries, evidence, implementation
paper/                 master manuscript
tests/                 cross-study integration tests
scripts/               repository verification and manifest tools
```

The top-level `README.md` is the canonical scientific narrative. `docs/findings.md` is the complete claim-by-claim findings ledger, with each item labeled by evidence status. Sub-study documentation explains the machinery used to generate individual results.

### Headline findings

The repository's strongest and most interesting results are deliberately separated by evidence type:

- **Exact observer ambiguity:** in the complete four-particle, zero-momentum periodic `3 x 3` HPP sector, 9,153 microscopic states reduce to 9,126 complete-future density-predictive classes. Exactly 27 classes remain doubletons, leaving 54 distinct microscopic states permanently indistinguishable to the declared density observer.
- **Exact space-time observability tradeoff:** exact velocity masks at only three fixed lattice sites are sufficient to reconstruct every state in that sector when four time snapshots are used; two sites never suffice. Exactly six three-site layouts succeed.
- **A different sensor needs more space and time:** local momentum requires five fixed sites and seven snapshots at the minimum; all-site momentum reconstructs in two snapshots.
- **Temporal information can recover hidden state, but not always:** a full field of horizontal/vertical axis counts reconstructs after one additional time slice, while density retains 27 permanent ambiguities even with the complete future.
- **Predictive recurrence is a quotient concept:** a system can return to the same prediction-equivalence class without returning to the identical microscopic description. Quotienting can merge cycles, compress periods, or both; the exact HPP density quotient merges nine period-three orbit pairs and shows no period compression in the certified sector.
- **Near recurrence is not exact recurrence:** the continuous torus benchmark can approach its initial state arbitrarily closely while having no exact positive-time return.
- **Observer recurrence and universe recurrence are distinct targets:** a finite observer, causal patch, or measurement family may recur predictively even when the global complete state does not.
- **The cosmic coordinate is descriptive, not cyclic:** the bundled cosmological coordinate locates the present universe on a declared reference history but is **not a recurrence-cycle phase**.
- **The main cosmological result is non-identification:** under an unrestricted far-future theory class, current inputs do not identify a unique probability of complete cosmic recurrence; the model-agnostic identified set remains `[0,1]`.
- **The deepest conceptual result is about physical distinction:** a descriptive difference becomes a predictive physical difference only when at least one admitted physical protocol assigns different record statistics. Identifying predictive equivalence with ontological identity requires an additional metaphysical principle and is not claimed as a theorem.

For the full evidence-qualified ledger, see [`docs/findings.md`](docs/findings.md). For the general protocol-family mathematics, see [`studies/dynamics/docs/predictive-quotient.md`](studies/dynamics/docs/predictive-quotient.md).

For concrete translations of the mathematical results into recurrence scenarios, see `docs/interpretation.md`. It distinguishes exact state return, temporary observational recurrence, permanent predictive equivalence, near recurrence, observer-indistinguishable recurrence, biographical recurrence, and detection time without promoting those scenarios into claims about the physical universe.

---

## Abstract

“Will the universe happen again?” sounds like one question, but it is actually a chain of different problems.

First, we must define what counts as the same universe. A repeated image, density field, cosmological parameter set, brain configuration at coarse resolution, or other observable description is not necessarily a repeated complete physical state. Second, we must determine whether the underlying dynamics permit exact recurrence, near recurrence, or neither. Third, we must ask whether observers can distinguish two states that are not exactly identical. Fourth, if a recurrent dynamics exists, we must determine whether its period and present phase can be inferred. Fifth, the observed universe must be located on a declared cosmological reference history without assuming that the reference history is cyclic. Finally, recurrence must be conditioned on the universe’s far-future physical branch: stable de Sitter expansion, metastable vacuum decay, fading dark energy, a phantom finite endpoint, recollapse, bounce, or some genuinely cyclic dynamics.

This framework joins those questions into one coherent research program.

Exact finite-state calculations show that complete-state recurrence can be proved and navigated when the full state space and update law are known. They also prove that observational similarity can be radically weaker than microscopic identity. In an exact lattice-gas benchmark, different microscopic trajectories produce the same density history indefinitely under the selected observation. Continuous systems show the opposite kind of subtlety: a deterministic, reversible, compact system can return arbitrarily close to its initial state while never returning exactly. Quantum systems introduce a related distinction: exact unitary recurrence requires commensurate occupied energy gaps, while finite-level systems can exhibit arbitrarily close phase recurrence without exact positive-time return.

These results motivate a more operational question than exact recurrence alone:

> **How close would a future state have to be before no observer like us could distinguish it from the original?**

The framework therefore defines **observer-indistinguishable recurrence** relative to an observer’s accessible measurements, causal region, noise floor, memory, and observation horizon. In classical systems this can be expressed through distances between observable probability distributions. In quantum systems trace distance gives an operational limit on optimal distinguishability. This creates a continuum between exact state recurrence and merely suggestive similarity.

For cosmology, the present universe can be assigned a model-conditional reference coordinate, but no empirically established cosmic recurrence period, cycle count, or recurrence phase is known. Under a stable eternal positive-vacuum-energy future and a conventional finite recurrent de Sitter causal-patch interpretation, an enormous thermodynamic recurrence scale can be calculated. That scale is conditional and is not a universal recurrence clock.

The central cosmological result is therefore a **partial-identification / non-identifiability boundary**:

```math
P(\text{cosmic recurrence}\mid\text{present observations, unrestricted future theory})\in[0,1].
```

The interval `[0,1]` is **not** presented as an informative probability estimate. It records that present data, when combined with an unrestricted far-future theory space, do not narrow the recurrence probability beyond the logical probability bounds. The substantive result is the uncertainty decomposition showing which missing theoretical inputs prevent a narrower inference.

Cosmic recurrence is mathematically possible and physically available under some classes of future theory. Present observations do not establish that our universe possesses an exact recurrence clock, do not determine its period, and do not provide a model-independent probability that complete cosmic history repeats.

The strongest direction forward is not simply to ask when everything repeats. It is to determine:

1. whether reality possesses a return structure at all;
2. which state variables define that return;
3. which differences would remain observable;
4. how close a return must be before it is operationally indistinguishable to an observer;
5. and what future physics would make such a return possible.

---

# 1. The master question

The broad question is:

> **Does physical reality possess dynamics under which the complete state of our universe can return, exactly or approximately, to a previous state?**

That separates into nine ordered questions:

1. **Target:** What counts as “the same universe”?
2. **Dynamics:** Does the relevant state space and evolution law permit exact or near recurrence?
3. **Observability:** Do our measurements determine the complete predictive state?
4. **Indistinguishability:** How different can two states be while remaining impossible for an observer to distinguish?
5. **Navigation:** If the system is recurrent, can its period and present phase be determined?
6. **Cosmic position:** Where are we on a declared reference cosmological history?
7. **Ultimate fate:** Which far-future branches are physically viable?
8. **Mechanism:** Which branches actually support a recurrence theorem or return process?
9. **Probability:** Which uncertainties are constrained by data and which remain theory-dependent?

These questions cannot safely be collapsed into one equation.

A finite recurrence theorem does not prove that the physical universe is finite. A repeated cosmological macrostate does not prove that the complete quantum state has returned. A cyclic scale factor does not prove that a cosmic history repeats. A de Sitter entropy estimate does not by itself provide a rigorous quantum recurrence time. A present cosmological fit does not uniquely determine the remote future.

The framework therefore treats recurrence as a **state-definition, dynamics, observability, distinguishability, and future-fate problem**, not merely as a calculation of an extremely large number.

---

# 2. The recurrence hierarchy

The word “recurrence” should always be qualified.

## 2.1 Exact complete-state recurrence

Let $X$ be the complete state space and

```math
F:X\rightarrow X
```

a deterministic update rule. A state $x$ has exact recurrence time $T>0$ when

```math
F^T(x)=x.
```

If this equality holds, determinism gives

```math
F^{t+T}(x)=F^t(x)
```

for all later $t$.

This is the strongest recurrence claim. The complete predictive state returns.

## 2.2 Observational recurrence

Let

```math
h:X\rightarrow Y
```

be an observation map. Observational recurrence requires only

```math
h(F^T(x))=h(x).
```

This may represent repeated positions, density, images, measured cosmological variables, or any reduced description.

It is weaker than complete-state recurrence because $h$ can discard predictive information.

## 2.3 Finite-horizon recurrence

For a positive integer $r$, define

```math
D_r(x)=\left(h(x),h(Fx),\ldots,h(F^{r-1}x)\right).
```

Two states may agree for a long finite observational history and later diverge. A finite match is therefore not proof of permanent recurrence.

## 2.4 Predictive equivalence

Two complete states are predictively equivalent under the observation map when

```math
x\sim_h x'
```

if and only if

```math
h(F^t x)=h(F^t x')
```

for every $t\geq0$.

These states can be microscopically different while remaining forever indistinguishable under the selected observation.

## 2.5 Near recurrence

Given a metric $d$ and tolerance $\varepsilon>0$,

```math
d(F^T x,x)<\varepsilon
```

defines a near recurrence.

A near recurrence must always state:

- the metric;
- the tolerance;
- the variables being compared;
- numerical precision;
- the search horizon.

Near recurrence cannot be silently promoted to exact recurrence.

## 2.6 Observer-indistinguishable recurrence

Exact equality is stronger than an observer actually needs in order to experience two states as the same.

Define an observer $O$ by:

- an accessible measurement family $\mathcal M_O$;
- a causal region $C_O$;
- a measurement/noise model $\eta_O$;
- a finite observation horizon $H_O$;
- a memory and data-processing capacity.

For every measurement protocol $\pi$ available to the observer, let

```math
P_\pi(\cdot\mid x)
```

be the probability distribution of possible records when the underlying state is $x$.

Define the observer-relative operational distance

```math
d_O(x,x')
=
\sup_{\pi\in\Pi_O}
\mathrm{TV}
\left[
P_\pi(\cdot\mid x),
P_\pi(\cdot\mid x')
\right],
```

where $\mathrm{TV}$ is total-variation distance and $\Pi_O$ is the set of physically available observation protocols.

Then an **observer-indistinguishable recurrence** at tolerance $\varepsilon_O$ occurs when

```math
d_O(F^T x,x)\leq\varepsilon_O.
```

This definition matters because two universes could fail to match microscopically while producing essentially the same accessible experience and measurement record.

The word “indistinguishable” is therefore never absolute. It is always relative to a declared observer class and measurement capability.

## 2.7 Recurrence classes

| Class | Meaning |
|---|---|
| Exact complete-state recurrence | The full state returns exactly |
| Exact observer recurrence | Every accessible observer variable returns exactly |
| Observer-indistinguishable recurrence | Differences remain below a declared operational detection threshold |
| Closed observational recurrence | The observable state returns and the reduced dynamics are known to close |
| Temporary observational recurrence | Observations agree for a finite interval and later diverge |
| Predictive equivalence without microscopic equality | Different complete states produce the same future observation sequence |
| Present ambiguity with future separation | States look identical now but become observably different later |
| Near recurrence | The state returns within a declared mathematical tolerance |
| Unresolved | Available calculation or observation does not decide the question |

This hierarchy prevents “looks the same,” “cannot be told apart,” “is very close,” and “is exactly identical” from being treated as the same scientific claim.

---

# 3. Exact recurrence in deterministic systems

## 3.1 Finite deterministic state spaces

If $X$ contains a finite number of complete states and $F$ is deterministic, a sufficiently long trajectory must eventually repeat a state. Once the same complete state appears twice, all later evolution from those two occurrences is identical.

If $F$ is also bijective, there are no one-way transients into a cycle. Every state belongs to a periodic orbit.

Finiteness is therefore a powerful sufficient condition for exact recurrence in closed deterministic reversible systems.

It is not a demonstrated property of the physical universe.

## 3.2 Finiteness is sufficient, not necessary

Infinite or continuous state spaces can still contain exactly periodic trajectories. Exact recurrence can occur because of special dynamical structure even when the full state space is not finite.

The important question is not simply “finite or infinite?” It is whether the actual orbit closes.

## 3.3 Repetition of a complete state is stronger than repetition of an appearance

If

```math
F^m(x)=F^n(x),
```

then every subsequent complete state repeats with period $n-m$.

But if only

```math
h(F^m(x))=h(F^n(x)),
```

the future need not repeat unless the observation contains all predictive information or is known to define a closed reduced dynamics.

For the universe, a repeated matter distribution, CMB pattern, galaxy arrangement, brain state at coarse resolution, or cosmological parameter vector is not automatically a repeated complete physical universe.

---

# 4. Near recurrence and Poincaré recurrence

Poincaré recurrence is frequently described more strongly than the theorem warrants.

Let $(X,\Sigma,\mu)$ be a finite-measure space and let $T:X\to X$ preserve $\mu$. For every measurable set $A$, almost every point of $A$ returns to $A$ infinitely often.

Important qualifications are:

- the theorem concerns return to a region or neighborhood, not ordinarily the identical measure-zero point;
- it applies almost everywhere, not necessarily to every state;
- finite accessible measure is required;
- measure preservation is required;
- recurrence times may be extraordinarily long;
- open, dissipative, or infinite-measure systems may not satisfy the theorem.

Poincaré recurrence therefore supports **near return under appropriate assumptions**, not a universal claim that every physical system exactly reproduces its entire state.

For cosmology, one must first justify that the relevant cosmic state space and dynamics satisfy the theorem’s assumptions.

---

# 5. Continuous systems: exact return and arbitrarily close return

Two exact computational examples show why “continuous” does not determine the recurrence answer.

## 5.1 Exactly periodic hard-particle system

Four labeled hard point particles moving on a unit ring with rational positions and velocities, undergoing perfectly elastic equal-mass collisions, form an exactly periodic orbit in the studied example.

The exact period is

```math
T=10,
```

with 36 collision events per period.

This demonstrates that continuous mechanical systems can possess exact periodic trajectories.

## 5.2 Irrational torus flow

Consider

```math
q(t)=(t,\sqrt{2}\,t)\pmod 1.
```

An exact return at $T>0$ would require both $T$ and $\sqrt{2}T$ to be integers. That is impossible because $\sqrt{2}$ is irrational.

The orbit nevertheless comes arbitrarily close to its starting point through continued-fraction approximations.

The computed near returns illustrate how an observer threshold changes the practical answer:

| Required return error | First listed return time $q$ | Actual error |
|---:|---:|---:|
| $<10^{-1}$ | 5 | $7.11\times10^{-2}$ |
| $<10^{-2}$ | 70 | $5.05\times10^{-3}$ |
| $<10^{-3}$ | 408 | $8.67\times10^{-4}$ |
| $<10^{-4}$ | 5,741 | $6.16\times10^{-5}$ |
| $<10^{-5}$ | 80,782 | $4.38\times10^{-6}$ |
| $<10^{-6}$ | 470,832 | $7.51\times10^{-7}$ |

No exact recurrence occurs at any positive time, yet for any finite measurement resolution the orbit eventually returns more closely than that resolution.

This creates an important conceptual possibility for cosmology:

> **Reality could lack an exact recurrence clock and still return so closely that a finite observer could not operationally distinguish the return from an exact one.**

That is a different scientific claim from exact recurrence, but it may be more relevant to actual observers.

---

# 6. Quantum recurrence

Quantum recurrence has its own state-space structure.

## 6.1 A finite-dimensional Hilbert space is not a finite set of states

Normalized quantum state vectors form a continuum. Removing global phase still leaves a continuous projective state space.

Therefore “finite-dimensional Hilbert space” does not mean “finite number of exact states.”

## 6.2 Exact unitary recurrence

For a time-independent Hamiltonian,

```math
|\psi(t)\rangle
=
\sum_n c_n e^{-iE_nt/\hbar}|E_n\rangle.
```

Physical exact recurrence at time $T$ requires

```math
|\psi(T)\rangle=e^{i\phi}|\psi(0)\rangle.
```

For every pair of occupied energy levels,

```math
\frac{(E_n-E_m)T}{\hbar}\in2\pi\mathbb{Z}.
```

Exact recurrence therefore requires the relevant occupied energy gaps to be commensurate.

Generic incommensurate gaps do not produce an exact positive-time return.

## 6.3 Quantum near recurrence

If only finitely many energy levels are occupied, the relative phases evolve on a finite-dimensional torus. Simultaneous Diophantine approximation can generate arbitrarily close returns.

This does not imply exact recurrence.

Infinite-dimensional systems need additional spectral assumptions, and a continuous spectral component can invalidate the finite-torus argument.

## 6.4 Quantum operational distinguishability

For two quantum states $\rho$ and $\sigma$, define the trace distance

```math
D(\rho,\sigma)
=
\frac{1}{2}\|\rho-\sigma\|_1.
```

Trace distance has a direct operational meaning. With equal prior probability and the best physically allowed single measurement, the maximum probability of correctly identifying which state was supplied is

```math
P_\mathrm{correct}
=
\frac{1+D}{2}.
```

Examples:

| Trace distance $D$ | Best one-shot identification probability |
|---:|---:|
| 1 | 100% |
| 0.1 | 55% |
| 0.01 | 50.5% |
| $10^{-3}$ | 50.05% |
| $10^{-6}$ | 50.00005% |
| 0 | 50% |

Thus two quantum states can be mathematically unequal while being essentially impossible to distinguish in a single available test.

For a real observer, the relevant calculation must also include:

- which measurements are physically accessible;
- whether repeated identical copies are available;
- finite lifetime;
- environmental decoherence;
- causal accessibility;
- detector noise and resolution.

A cosmic observer does not normally receive arbitrarily many independently prepared copies of the entire universe. This makes observer-relative indistinguishability especially relevant.

## 6.5 Quantum recurrence and the universe

A rigorous cosmological quantum recurrence calculation would require microscopic inputs such as:

- a justified closed-system description;
- a finite or otherwise controlled Hamiltonian spectrum;
- the number of relevant distinct energy eigenvalues;
- the energy span;
- a state-distance metric;
- a recurrence tolerance.

Present cosmological observations do not provide those inputs.

---

# 7. Observation, hidden state, and predictive equivalence

The recurrence problem is also an observability problem.

## 7.1 Present observational equivalence

Two states can satisfy

```math
h(x)=h(x')
```

while remaining physically different.

The omitted variables are “hidden” only relative to the chosen observation map. This does not imply a hidden-variable interpretation of quantum mechanics or a new law of nature.

## 7.2 Observational closure

The observation map is one-step closed if a deterministic map $G$ exists such that

```math
h\circ F=G\circ h.
```

Equivalently,

```math
h(x)=h(x')
\Longrightarrow
h(Fx)=h(Fx')
```

for all states in the analyzed sector.

If closure fails, the current observation omits information needed to determine the next observation.

## 7.3 Predictive quotient

The predictive equivalence relation defines a quotient

```math
Q_h=X/{\sim_h}.
```

This is the coarsest deterministic state representation that preserves the complete future observation process.

It removes microscopic distinctions that never affect the selected observations while retaining distinctions that do.

## 7.4 General protocol-family predictive quotient

A single observation map is only one special case. A more general operational model is

```math
\mathcal T=(X,F,\Pi,\{P_\pi\}_{\pi\in\Pi}),
```

where `X` is a candidate complete state-description space, `F` is the dynamics, `Pi` is a declared family of admissible physical protocols, and `P_pi(.|x)` is the distribution of records produced by protocol `pi` from state `x`.

For any selected family `A subseteq Pi`, define the complete prediction map

```math
\mathcal R_A(x)=\bigl(P_\pi(\cdot\mid x)\bigr)_{\pi\in A}.
```

Then

```math
x\sim_Ax'
\iff
\mathcal R_A(x)=\mathcal R_A(x').
```

The predictive quotient is

```math
Q_A=X/{\sim_A}
\cong
\mathrm{Im}\mathcal R_A.
```

This construction unifies deterministic future-observation quotients, restricted observer quotients, finite-horizon quotients, causal-region quotients, noisy classical measurements, and quantum measurement families. It is explicitly **prediction-relative**, not an assertion about ultimate ontology.

## 7.5 Prediction-sufficient factorization

If a deterministic encoding `s:X -> S` preserves every prediction in `A`, then the quotient map factors through `s`. Consequently, `Q_A` is the unique coarsest deterministic prediction-sufficient representation, up to predictive isomorphism.

The statement is deliberately limited: it does **not** prove that the quotient is the unique or minimal ontology. A richer ontology can always be postulated inside prediction-map fibers if the added variables are declared prediction-inert.

## 7.6 Operational distinguishability

For probabilistic records, define

```math
\delta_A(x,x')=
\sup_{\pi\in A}
\mathrm{TV}
\left[P_\pi(\cdot\mid x),P_\pi(\cdot\mid x')\right].
```

Then

```math
\delta_A(x,x')=0
\iff
x\sim_Ax'.
```

This gives a precise operational meaning to “no admitted experiment can tell these descriptions apart.” It remains distinct from a deterministic trajectory-distance metric, which answers a different approximate-recurrence question.

## 7.7 Refinement, observers, and detection time

If `A subseteq B`, then

```math
\sim_B\subseteq\sim_A,
\qquad
\delta_A\le\delta_B.
```

Richer protocol families can split equivalence classes but cannot erase a distinction already detectable by a poorer family. Finite-horizon families likewise refine monotonically as the observation horizon grows.

This makes **detection time** a derived quantity: the first horizon at which two initially indistinguishable states become distinguishable relative to the declared observer and protocol family. Some hidden differences appear immediately, some only after dynamical coupling, and some never appear for that observer.

## 7.8 When does a difference in description become a difference in physics?

Formal inequality `x != x'` establishes only that two descriptions differ. Within a declared physical theory, a predictive physical difference exists when at least one admitted protocol produces different record statistics:

```math
[x]_A\neq[x']_A
\iff
\exists\pi\in A:
P_\pi(\cdot\mid x)\neq P_\pi(\cdot\mid x').
```

That answers an operational physics question. The stronger metaphysical claim that two descriptions represent distinct realities **only** when they make a predictive difference is an optional Difference-Making Principle, not a result forced by the mathematics.

## 7.9 Why this matters cosmologically

Suppose a future universe reproduces every macroscopic feature we currently measure. That still would not establish exact recurrence unless the measured observables form a complete predictive state.

A recurrence claim must therefore specify whether it means:

- complete microscopic or quantum state recurrence;
- causal-patch recurrence;
- cosmological macrostate recurrence;
- observer-state recurrence;
- observational recurrence;
- recurrence of a selected subsystem;
- near recurrence within a tolerance.

Without that declaration, “the universe repeats” is ambiguous.

---

# 8. Exact finite benchmark: microscopic difference with permanent observational identity

Finite reversible lattice systems provide controlled laboratories where every state can be enumerated and recurrence claims can be checked exactly.

These systems are not proposed models of fundamental cosmology. Their value is methodological.

## 8.1 Complete 3×3 sector

The four-particle, zero-momentum sector of a periodic $3\times3$ HPP lattice gas contains exactly

```math
9,153
```

microscopic states.

Under site-density observation, those 9,153 microscopic states collapse to only

```math
495
```

instantaneous density observations.

On average, one present density image is therefore compatible with about

```math
\frac{9153}{495}\approx18.49
```

different microscopic states, although the actual class sizes vary.

Future observation dramatically reduces the ambiguity. Exact predictive refinement gives:

| Quantity | Exact result |
|---|---:|
| Microscopic states | 9,153 |
| Present-density classes | 495 |
| Predictive classes | 9,126 |
| Predictive singletons | 9,099 |
| Predictive doubletons | 27 |
| Permanently ambiguous microscopic states | 54 |

The 54 exceptional states have the structure

```math
54=18\times3=9\times2\times3.
```

They consist of:

- 18 collision-free microscopic cycles;
- least period 3;
- 9 time-reversal orbit pairs;
- 2 distinct microscopic cycles in each pair;
- 3 aligned phases per pair;
- 27 two-state predictive classes.

The two microscopic trajectories in each paired class are physically different in their velocity assignments, yet produce the same site-density movie indefinitely after phase alignment.

That is stronger than merely “very close.”

For the declared density observer,

```math
d_O(x,x')=0
```

for the entire future even though

```math
x\neq x'.
```

This is a concrete existence proof of **perfect observer-level recurrence without microscopic identity**.

## 8.2 One hidden bit

Inside each exceptional predictive doubleton, the complete density future leaves two possible microscopic states.

Under an equal prior within that pair, the unresolved microscopic information is

```math
\log_2 2=1\ \mathrm{bit}.
```

The observer can know the entire future density movie and still be unable to recover that one microscopic binary distinction.

This is a useful warning for cosmology: more observation time does not necessarily eliminate hidden-state ambiguity if the chosen observable is fundamentally insensitive to the missing information.

## 8.3 Time-reversal mechanism

For a bijective map $F$, let $R$ be a time-reversal involution satisfying

```math
R^2=I,
\qquad
RFR=F^{-1}.
```

If the observation satisfies

```math
h(Rx)=h(x),
```

then

```math
h(F^tRx)=h(F^{-t}x).
```

If a periodic observation word is invariant under reversal up to cyclic phase shift, a state on the reversed microscopic orbit can have the same entire future observation sequence as the original state.

The persistent ambiguity therefore has an exact symmetry mechanism rather than being a numerical accident.

## 8.4 Exact sensor observability thresholds

The same exhaustive sector allows a stronger question than density ambiguity: **how much local information is required to reconstruct the complete state when time evolution is available?**

For exact local velocity-mask sensors at fixed sites:

- one site reaches at most **1,156** predictive classes;
- two sites reach at most **4,945**;
- three sites are necessary and sufficient among all fixed-site subsets;
- exactly six three-site layouts reconstruct all **9,153** states: `(0,4,8)`, `(0,5,7)`, `(1,3,8)`, `(1,5,6)`, `(2,3,7)`, `(2,4,6)`;
- the successful refinement is `322 -> 3271 -> 9123 -> 9153 -> 9153`, so four snapshots suffice at the minimum sensor count.

For local momentum-vector sensors:

- four sites reach at most **9,081** predictive classes and never reconstruct the sector;
- five sites are necessary and sufficient;
- exactly **36** five-site layouts succeed;
- a representative minimum refinement is `1181 -> 8391 -> 8766 -> 9021 -> 9143 -> 9149 -> 9153 -> 9153`, requiring seven snapshots;
- all-site momentum reconstructs in two snapshots: `6841 -> 9153 -> 9153`.

For the all-site horizontal/vertical axis-count field, the present observation gives 2,853 classes and one additional time slice reconstructs the state exactly: `2853 -> 9153 -> 9153`.

These exact results demonstrate a **space-time observability tradeoff**. Missing state information can sometimes be recovered from dynamics when hidden degrees of freedom later couple into the measured channel. The density observer is the counterexample: its 27 doubletons remain ambiguous for the complete future.

## 8.5 Predictive cycles versus microscopic cycles

The same sector contains **2,061** microscopic cycles:

- 1,341 of period 3;
- 459 of period 6;
- 252 of period 9;
- 9 of period 12.

The complete-future density quotient contains **2,052** predictive cycles. Exactly nine pairs of period-three microscopic cycles merge into nine quotient cycles. No period compression occurs in this certified sector.

This separates two effects that are often conflated:

1. **cycle merging** — distinct microscopic cycles become one predictive cycle;
2. **period compression** — a quotient orbit returns in fewer steps than the microscopic orbit.

Either can occur in principle. The HPP density certificate exhibits the first without the second.

---

# 9. Sensitivity to tiny differences

A second class of finite experiments asks the opposite question:

> If two states begin almost the same, how quickly can the difference become observable?

In conserved-sector perturbation experiments, a small microscopic change can remain initially hidden in a coarse density measurement and then propagate into macroscopic differences.

For one studied condition, the mean density difference begins at zero while the microscopic Hamming difference is already nonzero. One update later the density observable separates.

Across fixed-density scaling experiments, macroscopic separation generally appears rapidly, while microscopic perturbations spread through the system and can approach substantial fractions of the available microscopic degrees of freedom.

This produces an important dual result:

1. some microscopic differences are **forever invisible** under a chosen observation;
2. other initially invisible microscopic differences become **quickly visible**.

Observer-indistinguishability is therefore not determined solely by the size of an initial mismatch.

It depends on:

- where the mismatch is;
- the system dynamics;
- whether the mismatch couples to accessible observables;
- how long the observer watches;
- the observer’s resolution.

For cosmology, a near recurrence at one instant is not enough. We must also ask whether the residual mismatch grows into a detectable difference during the observer’s future horizon.

---

# 10. Period constraints, interaction fibers, and phase navigation

The finite-state work supports the decomposition

```math
\text{complete state}
\rightarrow
\text{invariants}
\rightarrow
\text{interaction fiber}
\rightarrow
\text{cycle}
\rightarrow
\text{phase}.
```

This gives a constructive route for finding a recurrence clock when the underlying recurrent dynamics are already known.

## 10.1 3×3 exact orbit structure

The complete $3\times3$ four-particle zero-momentum sector contains:

- 9,153 states;
- 2,061 exact cycles;
- periods $3,6,9,12$.

Short collision-history information is sufficient to determine the period class in the studied sector.

## 10.2 4×4 exact orbit structure

The complete $4\times4$ four-particle zero-momentum sector contains:

- 94,336 states;
- 19,448 exact cycles;
- periods $2,4,6,8,12,20,28$.

Four consecutive density frames determine the period class for every state in the declared sector.

This is an important observability result: temporal information can compensate for a coarse instantaneous measurement.

## 10.3 5×5 reference orbit and interaction fiber

For a studied $5\times5$, 14-particle zero-momentum system, the full sector contains

```math
2,240,809,149,480,000
```

states.

A selected reference orbit has exact period

```math
T=9705.
```

An exact transport/geometry factor

```math
g=5
```

reduces the nonlinear interaction clock to

```math
\tau=\frac{T}{g}=1941.
```

Exact invariants reduce the compatible search space from more than $2.24\times10^{15}$ states to an interaction fiber of only

```math
2,209
```

states.

That is a search-space reduction by a factor of approximately

```math
1.01\times10^{12}.
```

The fiber decomposes into 17 exact $F^5$ cycles with lengths

```math
1941,46,45,44,28,18,14,14,10,9,8,8,7,5,5,4,3.
```

For the reference state, a small sequence of collision-orientation frames identifies the exact state within the compatible fiber. Across all 2,209 states, nine collision-orientation frames uniquely identify every state.

Additional sensor-selection calculations give constructive upper bounds:

- 49 of 100 candidate single-snapshot velocity sensors identify the reference orbit under a greedy discriminator;
- 11 of 25 density sites across three frames form another successful greedy discriminator.

A sampled 500-state period-scale predictor achieved approximately

```math
R^2\approx0.724
```

for $\log_{10}T$.

This is an empirical predictive result, not an exact theorem.

## 10.4 Meaning of the finite navigation results

These calculations demonstrate that a recurrence period and phase can sometimes be inferred without storing an astronomical atlas of every possible state.

The strategy is:

1. identify exact invariants;
2. shrink the compatible state space;
3. identify the relevant cycle;
4. localize phase from sufficient observations.

That is directly relevant to the question:

> **Could we ever tell whether a cosmic recurrence clock exists?**

The finite systems provide a methodological prototype.

They are not evidence that the physical universe obeys HPP dynamics or possesses a finite HPP-like state space.

---

# 11. A practical observer-indistinguishability program

The framework can be extended from “exact or not?” to a computable hierarchy of perceptual and operational similarity.

## 11.1 State distance is not enough

A microscopic norm

```math
d_X(x,x')
```

can tell us how far apart two complete states are mathematically.

But an observer only accesses a projection of the state.

Two states can have a large microscopic distance and zero observer distance, as the exact HPP ambiguity demonstrates.

Conversely, a tiny microscopic change can rapidly amplify into a large observer-visible difference.

Therefore the quantity of interest is not just

```math
d_X(x,x'),
```

but

```math
d_O(x,x').
```

## 11.2 Finite-horizon observer distance

For a deterministic observation sequence, define

```math
Y_H(x)
=
\left(
h(x),h(Fx),\ldots,h(F^H x)
\right).
```

For a metric $d_Y$, one simple finite-horizon observer metric is

```math
d_{O,H}(x,x')
=
\max_{0\leq t\leq H}
d_Y\left(h(F^t x),h(F^t x')\right).
```

A return is observer-indistinguishable over horizon $H$ if

```math
d_{O,H}(F^T x,x)\leq\varepsilon_O.
```

This answers a more realistic question:

> If the state returned nearly—but not exactly—to the original, would any difference become detectable during an observer’s usable lifetime?

## 11.3 Noise-normalized classical metric

Suppose an observer measures quantities $y_i$ with standard uncertainties $\sigma_i$.

Define

```math
\chi_O^2(x,x')
=
\sum_i
\left(
\frac{y_i(x)-y_i(x')}{\sigma_i}
\right)^2.
```

A practical recurrence criterion can be declared by choosing a detection threshold $\chi_\mathrm{crit}^2$.

This is not a universal definition of identity. It is a transparent way to say:

> These two states are different, but the difference is smaller than what this observer and instrument set can detect.

## 11.4 Probability-distribution metric

When measurements are stochastic, use total-variation distance:

```math
d_\mathrm{TV}(P,Q)
=
\frac12\sum_y |P(y)-Q(y)|
```

for discrete outcomes, with the corresponding integral form for continuous outcomes.

Then define the strongest available observer test:

```math
d_O(x,x')
=
\sup_{\pi\in\Pi_O}
d_\mathrm{TV}
\left(
P_\pi(\cdot|x),
P_\pi(\cdot|x')
\right).
```

This is an operational definition. If $d_O$ is tiny, even the best permitted observation protocol has little discriminatory power.

## 11.5 Causal-patch observer distance

A real observer cannot measure the complete universe.

Define $C_O(H)$ as the region capable of influencing observer $O$ during observation horizon $H$.

Then compare only the reduced state accessible within that causal domain:

```math
\rho_{C_O(H)}.
```

Two global universes can differ outside that domain while remaining exactly identical for the observer during $H$.

This motivates a physically meaningful class:

> **Causal-patch recurrence:** the complete state of everything capable of affecting the observer during the declared horizon returns, even if the global universe does not.

This may ultimately be more scientifically testable than global recurrence.

## 11.6 Observer-state recurrence

A still narrower target is the physical state of the observer and relevant local environment.

Let $B_O$ denote the degrees of freedom encoding:

- the observer’s body or computational substrate;
- memory;
- sensory inputs;
- immediate environment;
- all variables capable of changing the observer’s experience over horizon $H$.

Then an observer-state recurrence can be defined by

```math
d_{B_O}
\left(
B_O(F^T x),
B_O(x)
\right)
\leq\varepsilon_B.
```

This does not establish that the entire universe repeated.

It asks whether the returned world would be physically and experientially indistinguishable to the returned observer.

## 11.7 A future computational target

A useful future study would calculate a ladder such as:

```math
\varepsilon_\mathrm{exact}=0
<
\varepsilon_\mathrm{quantum}
<
\varepsilon_\mathrm{instrument}
<
\varepsilon_\mathrm{human}
<
\varepsilon_\mathrm{biographical}.
```

Each level would correspond to a different recurrence claim:

- exact state;
- quantum operational indistinguishability;
- scientific-instrument indistinguishability;
- human perceptual indistinguishability;
- same experienced biography over a finite lifetime.

The key is not to guess these thresholds. They must be derived from a declared physical observer model.

---

# 12. What “indistinguishable to us” would actually mean

The phrase “close enough that we could not tell” needs a physical definition.

For human observers, relevant limits include:

- finite sensory resolution;
- finite neural precision and robustness;
- noisy biological states;
- finite memory;
- finite lifetime;
- finite scientific instruments;
- finite accessible energy;
- finite computational capacity;
- finite causal access to the universe.

A global microscopic mismatch does not necessarily matter if it:

1. never enters our causal region;
2. never couples to a measurable quantity;
3. remains below all accessible detection thresholds;
4. occurs only in degrees of freedom irrelevant to our future experiences.

Conversely, an extremely small mismatch can matter if chaotic or nonlinear dynamics amplify it into an observer-visible difference.

Therefore there is no single universal “percentage match” at which a universe becomes the same to us.

The correct quantity is a **dynamical, observer-relative distinguishability**.

A future recurrence study should therefore report at least three values:

```math
d_X
\quad\text{microscopic state distance},
```

```math
d_O
\quad\text{observer-accessible distance},
```

```math
\tau_\mathrm{divergence}
\quad\text{time until the mismatch becomes detectable}.
```

A particularly interesting regime is

```math
d_X>0,
\qquad
d_O\approx0,
\qquad
\tau_\mathrm{divergence}>H_\mathrm{observer}.
```

In that regime the universe is not exactly the same, but it is functionally indistinguishable to that observer for the observer’s entire accessible future.

The HPP predictive-doubleton result realizes an even stronger limit:

```math
d_X>0,
\qquad
d_O=0,
\qquad
\tau_\mathrm{divergence}=\infty
```

for the selected observation.

---

# 13. The present cosmic coordinate

A recurrence framework needs a way to describe where the observed universe lies on a reference expansion history without falsely calling that location a recurrence phase.

The coordinate grammar is

```math
M/\Phi_C.
```

## 13.1 Composition phase

Define

```math
\Phi_C
=
\frac{2}{\pi}
\tan^{-1}\left(\frac{\rho_\mathrm{DE}}{\rho_m}\right).
```

Then

```math
0\leq\Phi_C\leq1.
```

Interpretation:

- $\Phi_C\to0$: matter strongly dominates dark energy;
- $\Phi_C=0.5$: equal matter and dark-energy densities;
- $\Phi_C\to1$: dark energy strongly dominates matter.

This is a composition coordinate, not a recurrence phase, not a recurrence-cycle phase, and not a percentage of total cosmic lifetime.

## 13.2 Macrostate registry

The reference macrostates are:

- **M0:** radiation-dominated era;
- **M1:** matter-dominated era before reference acceleration onset;
- **M2:** accelerating transition after acceleration begins but before dark energy overtakes matter;
- **M3:** dark-energy-dominated accelerating era;
- **M4:** project-defined deep-dark-energy era beginning when the dark-energy fraction reaches 0.90.

## 13.3 Reference cosmology

Using the declared flat matter-plus-$\Lambda$ reference values

```math
H_0=68.11\ \mathrm{km\,s^{-1}\,Mpc^{-1}},
```

```math
\Omega_{m0}=0.3042,
\qquad
\Omega_{\Lambda0}=0.6958,
```

the present reference coordinate is

```math
\boxed{M3/\Phi_C=0.7376}.
```

The reference cosmic age is

```math
13.787\ \mathrm{Gyr}.
```

## 13.4 Reference clock equations

For a flat matter-plus-$\Lambda$ cosmology,

```math
\frac{\rho_\Lambda}{\rho_m}
=
\frac{\Omega_{\Lambda0}}{\Omega_{m0}}a^3.
```

Therefore

```math
a(\Phi_C)
=
\left[
\frac{\Omega_{m0}}{\Omega_{\Lambda0}}
\tan\left(\frac{\pi\Phi_C}{2}\right)
\right]^{1/3}.
```

The late-time analytic age relation is

```math
t(\Phi_C)
=
\frac{2}{3H_0\sqrt{\Omega_{\Lambda0}}}
\mathrm{asinh}
\left[
\sqrt{
\tan\left(\frac{\pi\Phi_C}{2}\right)
}
\right].
```

Radiation is neglected in this late-time analytic expression, so the early radiation-to-matter transition is anchored separately.

## 13.5 Reference timeline

| Event | Reference value |
|---|---|
| Radiation → matter transition | near $z=3387$, about 51,500 years |
| Acceleration-onset boundary | $z=0.6600$, age 7.555 Gyr |
| Dark-energy/matter equality | $z=0.3176$, age 10.113 Gyr, $\Phi_C=0.5000$ |
| Present reference point | $M3/\Phi_C=0.7376$, age 13.787 Gyr |
| Deep-dark-energy threshold | 7.077 Gyr after reference present, $\Phi_C=0.9296$ |

The reference present lies 3.674 Gyr after M3 entry and 34.17% of the declared M3-to-M4 reference interval has elapsed.

None of these quantities is a recurrence cycle count.

---

# 14. Why the finite results do not prove cosmic recurrence

The framework deliberately prevents cross-level overreach.

The following substitutions are invalid without additional physics:

- finite lattice recurrence $\not\Rightarrow$ finite cosmic state space;
- finite-model period $\not\Rightarrow$ cosmic period;
- finite-model phase $\not\Rightarrow$ cosmic phase;
- cosmological composition phase $\Phi_C$ $\not\Rightarrow$ recurrence phase;
- de Sitter entropy $\not\Rightarrow$ microscopic quantum recurrence period;
- Big Crunch $\not\Rightarrow$ exact state reset;
- empty space $\not\Rightarrow$ unique initial condition;
- observational similarity $\not\Rightarrow$ complete-state identity;
- observer-indistinguishability $\not\Rightarrow$ microscopic equality.

The finite models answer:

> What can be proved if the state space and law are fully known?

Cosmology asks:

> Do we actually know that the universe satisfies analogous assumptions?

At present, the second question remains open.

---

# 15. Fate-conditioned cosmology

Recurrence depends strongly on the far-future branch.

| Future branch | Recurrence status | Additional requirement |
|---|---|---|
| Stable eternal positive-$\Lambda$ / de Sitter | Conditional thermodynamic recurrence route | Effectively finite, closed, recurrent causal-patch interpretation |
| Metastable de Sitter | Recurrence competes with vacuum decay | Vacuum must survive long enough |
| Fading dark energy | Standard de Sitter recurrence does not automatically apply | Asymptotic horizon/state-space structure must be specified |
| Phantom finite endpoint | No eternal de Sitter regime | Future must actually remain phantom to the endpoint |
| Recollapse without bounce | Contraction alone is insufficient | Explicit state-return dynamics required |
| Cyclic or bouncing future | Potentially recurrent | Cycle-to-cycle map must return or approach prior state |
| Spatial duplication elsewhere | Not temporal recurrence | A duplicate elsewhere is a different question |

Ultimate fate is therefore upstream of the recurrence calculation.

---

# 16. Stable de Sitter thermodynamic recurrence

Under a stable eternal positive-$\Lambda$ branch, define

```math
H_\Lambda
=
H_0\sqrt{\Omega_\Lambda}.
```

The de Sitter horizon radius is

```math
r_\mathrm{dS}
=
\frac{c}{H_\Lambda},
```

and the Gibbons-Hawking horizon entropy is

```math
\frac{S_\mathrm{dS}}{k_B}
=
\frac{\pi r_\mathrm{dS}^2}{\ell_P^2}.
```

At the declared reference point:

```math
H_\Lambda^{-1}=17.2105\ \mathrm{Gyr},
```

```math
r_\mathrm{dS}=1.6282\times10^{26}\ \mathrm{m},
```

```math
\frac{S_\mathrm{dS}}{k_B}
=
3.18835\times10^{122}.
```

A conventional entropy-exponential thermodynamic recurrence scale is

```math
t_\mathrm{thermo}
\sim
H_\Lambda^{-1}
\exp(S_\mathrm{dS}/k_B).
```

It is more useful to report its logarithm:

```math
\log_{10}\left(\frac{t_\mathrm{thermo}}\mathrm{yr}\right)
=
1.38468\times10^{122}.
```

Symbolically,

```math
t_\mathrm{thermo}
\sim
10^{\,1.38468\times10^{122}}\ \mathrm{years}.
```

This number is not a universal countdown.

It exists only after imposing the stable eternal de Sitter branch and the finite recurrent-patch thermodynamic interpretation.

---

# 17. Cosmological quantum recurrence remains unidentified

The de Sitter thermodynamic scale and a rigorous quantum $\varepsilon$-recurrence time are different clocks.

For a finite-dimensional unitary system, recurrence-time bounds can depend on microscopic quantities such as the number of relevant distinct energy eigenvalues, energy range, and target trace-distance tolerance.

The universe does not currently have a justified measured set of those microscopic recurrence inputs.

Therefore:

| Quantum target | Cosmological numerical result |
|---|---|
| Exact recurrence | Not identified |
| Trace-distance recurrence, $\varepsilon=0.1$ | Not identified |
| Trace-distance recurrence, $\varepsilon=0.01$ | Not identified |
| Trace-distance recurrence, $\varepsilon=0.001$ | Not identified |
| Human-observer indistinguishable recurrence | Not identified |
| Instrument-observer indistinguishable recurrence | Not identified |

Finite entropy alone cannot be substituted for the missing Hamiltonian spectrum or observer model.

This is one of the major open computational targets of the framework.

---

# 18. Vacuum decay and metastability

A universe may approach de Sitter behavior without remaining in that vacuum forever.

If the de Sitter-like vacuum is metastable, recurrence competes with vacuum decay.

Under a simple independent constant-hazard model,

```math
P(\text{recurrence before decay})
=
\frac{\tau_\mathrm{decay}}
{\tau_\mathrm{decay}+t_\mathrm{rec}}.
```

Because a thermodynamic recurrence time can be entropy-exponentially large, a vacuum lifetime that appears immense on ordinary astrophysical scales may still be tiny relative to the recurrence scale.

The relevant vacuum-decay rate is not determined by standard cosmological expansion measurements alone.

Metastability can therefore eliminate practical recurrence even when the intermediate cosmic future looks de Sitter-like.

---

# 19. Phantom finite-end scenarios

For a constant dark-energy equation of state

```math
w<-1,
```

the standard late-time approximation gives a finite remaining proper time

```math
\Delta t
\approx
\frac{2}
{3|1+w|H_0\sqrt{\Omega_\mathrm{DE}}}.
```

At the declared reference cosmology:

| Constant $w$ | Approximate remaining lifetime |
|---:|---:|
| -1.01 | 1,147.4 Gyr |
| -1.05 | 229.5 Gyr |
| -1.10 | 114.7 Gyr |
| -1.20 | 57.4 Gyr |

These are scenario calculations, not forecasts.

A finite-time future endpoint and an eternal de Sitter recurrence branch are qualitatively different physical hypotheses.

A phenomenological evolving-dark-energy fit cannot be extrapolated into a specific remote-future endpoint without a controlled physical model.

---

# 20. Recollapse, bounce, and cyclic cosmologies

A Big Crunch does not establish recurrence.

Contraction is not automatically the time reverse of expansion.

A bounce does not automatically erase:

- entropy;
- particle content;
- field configurations;
- quantum correlations;
- topological information;
- vacuum state;
- gravitational degrees of freedom;
- hidden variables relative to a selected observation.

A genuinely recurrent cyclic model needs an explicit cycle map

```math
x_{n+1}=F(x_n).
```

Exact recurrence requires

```math
F^k(x)=x
```

for some $k>0$.

Near recurrence requires a declared metric:

```math
d(F^k(x),x)<\varepsilon.
```

Observer-indistinguishable recurrence requires the stronger operational statement

```math
d_O(F^k x,x)\leq\varepsilon_O.
```

The fact that the scale factor $a(t)$ oscillates is not enough. A periodic macroscopic geometry can coexist with nonrecurrent microscopic information.

Likewise, an “empty universe” is not automatically a reset state. Empty of ordinary matter does not specify the complete geometry, vacuum, fields, quantum state, topology, horizons, or boundary conditions.

---

# 21. Probability architecture

Let:

- $D$ = present observations;
- $M$ = future cosmological model;
- $\theta$ = measured parameters inside that model;
- $A$ = additional theoretical assumptions needed for recurrence;
- $O$ = declared observer model;
- $\varepsilon$ = recurrence or distinguishability tolerance.

Then a finite-horizon recurrence probability can be written schematically as

```math
P(R_{\varepsilon,O}<T\mid D)
=
\sum_{M,A}
\int
P(R_{\varepsilon,O}<T\mid M,\theta,A)
\,p(\theta,M,A\mid D)
\,d\theta.
```

This exposes four different uncertainties.

## 21.1 Observational parameter uncertainty

Examples:

- $H_0$;
- $\Omega_m$;
- dark-energy parameters inside a chosen phenomenological model.

These can be constrained from data.

## 21.2 Future-model uncertainty

Examples:

- eternal $\Lambda$;
- metastable vacuum;
- fading dark energy;
- phantom finite endpoint;
- recollapse;
- cyclic/bounce behavior.

These are not fully determined by present expansion data.

## 21.3 Recurrence-theory uncertainty

Examples:

- whether the effective state space is finite;
- whether the relevant system is closed;
- spectral structure;
- vacuum survival;
- whether de Sitter entropy corresponds to an effectively finite recurrent Hilbert space;
- whether a bounce map is recurrent.

These are largely theoretical unknowns.

## 21.4 Observer-model uncertainty

Examples:

- what degrees of freedom count as the observer;
- accessible measurements;
- instrument precision;
- causal horizon;
- finite observation lifetime;
- acceptable distinguishability threshold.

This matters only for observer-relative recurrence, but it can dramatically change the answer.

If unresolved future-model and recurrence-theory terms are allowed to vary across what present observations still permit, then

```math
\boxed{
P(\text{recurrence}\mid\text{present observations, unrestricted future theory})
\in[0,1]
}
```

is the rigorous partial-identification statement.

This does not mean every probability is equally plausible.

It means the evidence does not identify a unique model-independent probability.

---

# 22. What cosmological data constrain

## 22.1 Conditional stable-de-Sitter propagation

When cosmological posterior samples are propagated **inside a flat-$\Lambda$CDM stable de Sitter branch**, the relevant quantities are tightly constrained compared with the enormous size of the recurrence exponent.

A representative propagation gives:

| Quantity | Median | 95% interval |
|---|---:|---:|
| $H_0$ (km s$^{-1}$ Mpc$^{-1}$) | 68.1728 | [67.6174, 68.7181] |
| $\Omega_m$ | 0.302655 | [0.295669, 0.309883] |
| $H_\Lambda^{-1}$ (Gyr) | 17.1758 | [16.9552, 17.4050] |
| $S_\mathrm{dS}/k_B$ | $3.17551\times10^{122}$ | $[3.09448,3.26082]\times10^{122}$ |
| $\log_{10}(t_\mathrm{thermo}/\mathrm{yr})$ | $1.37911\times10^{122}$ | $[1.34391,1.41616]\times10^{122}$ |

The main lesson is scale separation:

> **Uncertainty in fitted cosmological parameters is much smaller than uncertainty over whether the branch supporting the recurrence calculation is actually the universe’s far future.**

## 22.2 Restricted model-family comparison

A published Bayesian comparison of a **restricted two-model set** under equal prior odds gives approximately:

| Data combination | $\Lambda$CDM weight | dynamical-DE weight |
|---|---:|---:|
| DESI DR2 BAO + Planck CMB | 63.9% | 36.1% |
| DESI DR2 BAO + Planck CMB + corrected DES-Dovekie SN | 50.2% | 49.8% |

These values come from the Ong, Yallup & Handley Bayesian reanalysis of `LambdaCDM` versus `w0waCDM`, not from a model set spanning all dark-energy theories or all cosmic futures. The first row uses `ln B(dynamic/LambdaCDM) = -0.57 +/- 0.26`; the corrected DES-Dovekie row uses the current reported value `-0.01 +/- 0.27`.

They are model-family weights, not probabilities of stable de Sitter recurrence, Big Rip, recollapse, cyclic behavior, or recurrence itself. DESI DR2 Results IV uses additional Lyman-alpha Alcock-Paczynski/full-shape information and reports a frequentist model-comparison significance; it is a different inferential object and does not replace these restricted Bayesian weights.

## 22.3 Illustrative fate decomposition

If the top-level model weights are split among named future branches using a neutral bookkeeping rule, one illustrative decomposition is:

| Future | Illustrative weight |
|---|---:|
| Stable eternal de Sitter | 31.9% |
| Metastable de Sitter | 31.9% |
| Fading dark energy | 9.0% |
| Phantom finite end | 9.0% |
| Recollapse | 9.0% |
| Cyclic/bounce | 9.0% |

These values are not measured ultimate-fate probabilities.

They show how much of a final recurrence percentage would be supplied by unresolved theoretical assumptions.

## 22.4 Prior-conditioned recurrence sensitivity

Illustrative theoretical scenarios can produce narrower intervals:

| Theory scenario | Support for recurrent patch given eternal de Sitter | Illustrative recurrence interval |
|---|---:|---:|
| Conservative | 0.25 | [0.025, 0.775] |
| Agnostic | 0.50 | [0.100, 0.800] |
| de-Sitter-favoring | 0.75 | [0.375, 0.825] |

These are sensitivity demonstrations only.

They should not be reported as measured probabilities.

## 22.5 Finite-horizon rare-event probability

If a recurrence process is modeled as a stationary rare event with mean wait $t_\mathrm{rec}$,

```math
P(T)=1-e^{-T/t_\mathrm{rec}}.
```

For

```math
T\ll t_\mathrm{rec},
```

```math
\log_{10}P
\approx
\log_{10}T-\log_{10}t_\mathrm{rec}.
```

When the recurrence exponent is of order $10^{122}$, ordinary floating-point presentation can erase differences between finite horizons. High-precision arithmetic is required even for the numerical bookkeeping.

This numerical issue does not remove the larger physical uncertainty.

---

# 23. Does a cosmic recurrence clock exist?

At present, the answer is:

```math
\boxed{\text{Unknown}}
```

A physical recurrence clock would mean that the relevant complete cosmic state lies on an orbit with a well-defined return structure.

For exact deterministic recurrence, one would need some positive $T$ satisfying

```math
F^T(X)=X.
```

For quantum exact recurrence, the occupied spectral phases would need to realign exactly.

For near recurrence, an appropriate metric neighborhood would need to be revisited within a declared tolerance.

For observer-indistinguishable recurrence, the observer-accessible state must return inside the declared operational tolerance.

Several logically distinct possibilities remain open:

1. **Exact periodic universe:** a genuine positive recurrence period exists.
2. **Near-recurrent but never exact universe:** arbitrarily close returns occur with no exact return.
3. **Observer-recurrent universe:** accessible observer states repeat even though the complete universe does not.
4. **Partially recurrent universe:** selected observables or macrostates recur while the complete state does not.
5. **Branch-limited recurrence:** a recurrence mechanism exists only if a metastable phase survives long enough.
6. **No recurrence:** the actual future evolution never returns to the required target.
7. **Observationally undecidable recurrence:** the underlying recurrence structure exists or fails to exist, but accessible observations cannot uniquely identify it.

The present evidence does not select one of these possibilities.

The unknown is deeper than “the recurrence time is too large.”

We do not yet know whether an exact recurrence period exists to be timed.

---

# 24. Could we ever determine whether the clock exists?

Potentially, yes.

The most plausible route is not to wait for one full recurrence. It is to determine enough of the fundamental state space and evolution law to prove or rule out recurrence mathematically.

## 24.1 Route A: derive recurrence from fundamental theory

A sufficiently complete theory could establish:

- the correct complete state space;
- whether it is finite, compact, continuous, open, or effectively finite;
- whether evolution is deterministic or unitary;
- whether the relevant system is closed;
- exact conservation laws;
- spectral structure;
- whether relevant energy gaps are commensurate;
- whether the far-future branch persists indefinitely;
- whether an explicit bounce/cycle map closes.

If those objects were known, recurrence might be decided as a theorem rather than an observation.

## 24.2 Route B: identify invariant structure from observations

The finite-state studies show another possibility:

```math
\text{observations}
\rightarrow
\text{invariants}
\rightarrow
\text{compatible fiber}
\rightarrow
\text{cycle}
\rightarrow
\text{phase}.
```

A cosmic analogue would require observables that constrain true recurrence invariants strongly enough to reduce the compatible physical state space.

This is conceptually possible.

It is not currently available.

## 24.3 Route C: rule out exact recurrence

A fundamental theory could instead prove that no exact positive recurrence exists.

Possible obstructions include:

- incommensurate quantum energy gaps;
- continuous spectra;
- irreversible information loss from the relevant system;
- noncompact or infinite-measure accessible state spaces;
- monotonic variables that never reset;
- vacuum decay before return;
- a cycle map that drifts rather than closes.

A final theory might therefore tell us that reality has only near recurrence—or none at all.

## 24.4 Route D: establish observer recurrence without global recurrence

It may be easier to demonstrate that an observer-accessible causal state returns within a tolerance than to prove that the entire global state returns exactly.

One could in principle derive

```math
d_O(F^T x,x)\ll1
```

even while

```math
F^T x\neq x.
```

This would not prove exact cosmic repetition.

It would answer a different and deeply interesting question:

> **Could a returned observer have any physically available way to know the state was not exact?**

## 24.5 The observability barrier

The finite benchmark proves that two different complete microscopic trajectories can produce the same selected observable history forever.

Therefore even an indefinitely long perfect record under one observation map need not reveal every predictive degree of freedom.

Cosmologically, observations alone may be insufficient unless the observation set is known to be generating or complete for the relevant dynamics.

A recurrence clock could exist objectively while remaining impossible to reconstruct uniquely from accessible data.

## 24.6 What would count as strong evidence that the clock exists?

A convincing claim would need, at minimum:

1. a physically justified complete cosmic state space;
2. a physically justified evolution law;
3. a declared exact, near, or observer-relative recurrence target;
4. a theorem showing that the system satisfies the relevant recurrence conditions;
5. a treatment of quantum and gravitational degrees of freedom;
6. evidence that the far-future branch survives long enough;
7. a bridge from measurable observables to recurrence invariants;
8. a period or return-time derivation that does not substitute macroscopic entropy for missing microscopic information;
9. independent reproduction.

Until those conditions are met, the recurrence clock remains a hypothesis class rather than a measured physical object.

---

# 25. What recurrence would mean for an observer

This section states logical consequences of recurrence assumptions. It does not claim that cosmic recurrence occurs.

## 25.1 Exact observer recurrence

Suppose:

1. physical evolution is deterministic;
2. an observer and the observer’s memories are fully encoded in the physical state;
3. the complete state returns exactly after $T$.

Then the observer-state also returns.

Any memory physically present in the returned state is the same memory configuration as before.

Unless an additional physical “cycle counter” is part of the returned state, the observer contains no information distinguishing one occurrence from another.

An exact recurrence can therefore be:

- objectively repetitive in the dynamical description;
- subjectively indistinguishable from a first occurrence from inside the repeated state.

## 25.2 Near observer recurrence

Near recurrence is subtler.

Suppose

```math
d_X(F^T x,x)>0
```

but

```math
d_O(F^T x,x)\ll1.
```

The returned observer may initially be unable to detect the mismatch.

Whether the two experiences remain the same depends on the divergence time.

Define

```math
\tau_\mathrm{detect}
=
\inf
\left\{
t>0:
d_O(F^{T+t}x,F^t x)>\varepsilon_O
\right\}.
```

Then:

- if $\tau_\mathrm{detect}$ is short, the worlds quickly become observably different;
- if $\tau_\mathrm{detect}$ exceeds the observer’s lifetime, the mismatch is never experienced;
- if $\tau_\mathrm{detect}=\infty$, the states are predictively equivalent for that observer despite microscopic difference.

This quantity may be more relevant to lived recurrence than exact global equality.

## 25.3 Biographical recurrence

A possible future concept is **biographical recurrence**.

Two histories are biographically recurrent for observer $O$ over lifetime $L$ if every accessible record relevant to that observer remains within tolerance:

```math
d_{O,L}(F^T x,x)\leq\varepsilon_O.
```

The universes may differ elsewhere or in inaccessible microscopic degrees of freedom.

This is not “the exact same universe.”

It is a precise candidate for “the same life from the inside.”

---

# 26. Interesting results and implications

The framework has produced several results that are easy to miss if the discussion focuses only on cosmic timescales.

## 26.1 Looking identical forever does not imply being identical

The exact lattice benchmark contains physically different microscopic states that generate the same selected observation forever.

This is perhaps the clearest demonstration that observable history and complete physical identity are different concepts.

## 26.2 An entire future can still leave one bit unknown

For the exceptional lattice pairs, every density observation for all future time still leaves one binary microscopic distinction unresolved.

Observation duration alone does not guarantee complete-state identification.

## 26.3 A system can almost repeat forever without ever exactly repeating

The irrational torus flow has no exact positive return, yet comes arbitrarily close.

This means an operational recurrence can exist at every finite resolution even when an exact recurrence clock does not.

## 26.4 Tiny differences can either matter immediately or never matter

Some perturbations become macroscopically visible almost at once.

Others are permanently hidden by symmetry and the observation map.

The importance of a mismatch depends on dynamics and observability, not just its numerical magnitude.

## 26.5 More time can substitute for more sensors

In the exact $4\times4$ finite sector, four consecutive density frames identify the period class even though one density frame does not contain the complete microscopic state.

Temporal information can compensate for spatially coarse observation.

## 26.6 Invariants can collapse astronomical search spaces

In the $5\times5$ reference problem, exact invariants reduce a compatible search from more than

```math
2.24\times10^{15}
```

states to only

```math
2,209.
```

That is a reduction by roughly one trillion.

The lesson is broader than the lattice model:

> The apparent size of a state space may be far less important than finding the correct conserved structure.

## 26.7 The hardest cosmic uncertainty is not the numerical error bar

Inside a chosen stable de Sitter model, fitted cosmological parameters are relatively well constrained.

The dominant recurrence uncertainty is whether that future model—and the microscopic recurrence assumptions underneath it—is correct at all.

## 26.8 A huge recurrence time is not evidence of a recurrence mechanism

Calculating an entropy-exponential timescale after assuming a recurrent de Sitter patch does not establish that the physical universe satisfies those assumptions.

The existence of a formula and the existence of the clock are separate questions.

## 26.9 “Same life” and “same universe” are different scientific targets

An observer could in principle experience the same local biography while the global universe differs outside the observer’s causal or measurement domain.

This creates a useful hierarchy:

```math
\text{global exact recurrence}
\Rightarrow
\text{local exact recurrence}
\Rightarrow
\text{observer recurrence},
```

but the reverse implications do not automatically hold.

## 26.10 The strongest future question may be operational, not metaphysical

Instead of asking only

> “Did every fundamental degree of freedom return exactly?”

we can also ask

> “Is there any physically possible experiment available to the returned observer that distinguishes the two histories?”

That question can be formalized and computed.

---

# 27. Evidence hierarchy

Claims should be labeled by evidence type.

| Result family | Evidence type | Scope |
|---|---|---|
| Finite transport and invariant clocks | analytic proof | declared finite lattice dynamics |
| 3×3 ambiguity classification | exhaustive finite computation + independent verification | 9,153-state sector |
| 3×3 and 4×4 period classes | exhaustive finite computation | declared finite sectors |
| 5×5 interaction fiber | exhaustive constrained enumeration | one invariant fiber |
| 5×5 phase and sensor results | deterministic computation | one exact reference orbit/fiber |
| Sampled period predictor | empirical cross-validation | fixed finite sampled population |
| Irrational torus nonrecurrence | analytic proof + numerical near returns | declared continuous flow |
| Quantum exact-recurrence criterion | analytic spectral condition | closed time-independent quantum systems |
| Quantum observer distinguishability | operational theorem from trace distance | declared quantum states |
| Cosmic composition coordinate | analytic mapping within reference cosmology | declared flat matter+$\Lambda$ reference |
| de Sitter horizon/entropy scale | standard conditional thermodynamic calculation | declared stable de Sitter branch |
| Cosmological posterior propagation | observational posterior propagation | chosen cosmological branch |
| Model-family Bayesian weights | model comparison | restricted selected model set |
| Fate decomposition | sensitivity assumption | not a measured future-fate probability |
| Unrestricted recurrence probability $[0,1]$ | partial-identification / non-identifiability result | full logical bound; not an estimated probability distribution |
| Human-observer recurrence threshold | open research target | not yet numerically identified |

A result may be used as a definition, diagnostic analogy, or consistency check across layers. It may not be promoted to a stronger evidence level merely because another layer exists.

---

# 28. Scientific boundaries and nonclaims

This framework does **not** establish that:

- the universe definitely recurs;
- the universe definitely does not recur;
- the physical cosmic state space is finite;
- the universe has a known recurrence period;
- the universe has a known recurrence phase;
- the composition coordinate is a recurrence phase;
- a Big Crunch necessarily recreates a Big Bang;
- a bounce necessarily resets information;
- empty space is a unique reset state;
- finite de Sitter entropy proves a finite number of exact quantum states;
- the thermodynamic de Sitter recurrence estimate is a rigorous quantum $\varepsilon$-recurrence time;
- present dark-energy fits uniquely determine the remote future;
- a spatial duplicate is the same thing as temporal recurrence;
- observer-indistinguishability proves microscopic equality;
- an unknown probability should be replaced by 50%.

The framework does establish that:

- exact recurrence, observational recurrence, near recurrence, and observer recurrence are different claims;
- exact recurrence can be proved in fully specified finite deterministic systems;
- continuous systems can exhibit near recurrence without exact recurrence;
- quantum exact recurrence depends on spectral structure;
- coarse observation can permanently hide microscopic differences;
- invariants and temporal observations can dramatically improve recurrence navigation;
- present cosmological position can be described without assuming cosmic periodicity;
- future cosmological fate is upstream of any recurrence mechanism;
- current data do not identify a unique model-independent cosmic recurrence probability;
- observer-indistinguishable recurrence can be defined operationally and is a legitimate computational research target.

---

# 29. Research roadmap

The next useful work is not to force a single cosmic recurrence percentage. It is to reduce the unknowns one layer at a time.

## 29.1 Observer-indistinguishable recurrence benchmark

Build a dedicated computational study with:

1. exact complete-state distance;
2. coarse observational distance;
3. stochastic/noisy observer distance;
4. quantum trace-distance examples;
5. detection-time calculation;
6. finite observer horizons.

For each pair of near states, report:

```math
d_X,
\qquad
d_O,
\qquad
\tau_\mathrm{detect}.
```

This would directly study “not exactly the same, but indistinguishable to us.”

## 29.2 Perturbation-to-observer divergence maps

For controlled deterministic systems:

- generate states at known microscopic distances;
- evolve both states;
- measure when different observer maps first separate;
- estimate the distribution of $\tau_\mathrm{detect}$;
- identify perturbations that remain permanently hidden.

This can distinguish harmless mismatch from dynamically amplified mismatch.

## 29.3 Multi-observer hierarchy

Compare observer classes:

- microscopic ideal observer;
- laboratory instrument observer;
- coarse macroscopic observer;
- finite-lifetime biological observer.

A state pair can then be assigned an indistinguishability profile rather than a single similarity number.

## 29.4 Quantum recurrence-distance study

For finite Hamiltonians with controlled spectra:

- separate exact commensurate cases from incommensurate cases;
- compute trace-distance return curves;
- calculate first passage below selected $\varepsilon$;
- compare mathematical near recurrence with practical observer discrimination;
- study how recurrence time scales with dimension and tolerance.

## 29.5 Causal-patch recurrence

Develop a formal distinction among:

- global-universe recurrence;
- causal-patch recurrence;
- observer-local recurrence.

The physically relevant state for an observer may be a reduced causal state rather than the inaccessible global state.

## 29.6 Cosmological state specification

Identify which variables a candidate quantum-gravitational cosmology would require to define a complete recurrence state:

- geometry;
- matter fields;
- quantum state;
- gravitational degrees of freedom;
- horizon data;
- topology;
- boundary conditions.

Without this, “the same universe” remains underspecified.

## 29.7 Spectral route to the cosmic clock

If future theory supplies a controlled cosmic Hamiltonian or equivalent evolution generator:

- determine occupied spectral structure;
- test commensurability;
- derive exact or near recurrence bounds;
- separate global and causal-patch spectra;
- connect the result to observable invariants where possible.

## 29.8 Fate model refinement

Continue separating:

- data-constrained cosmological parameters;
- phenomenological dark-energy fits;
- physical future extrapolation;
- vacuum stability;
- bounce dynamics;
- recurrence assumptions.

A future model should not inherit recurrence merely because it is cyclic in one macroscopic variable.

## 29.9 Proof of impossibility is equally valuable

A successful recurrence program does not need to end with “yes.”

A proof that exact cosmic recurrence is impossible under the correct fundamental theory would be a complete scientific answer.

So would a proof that only observer-indistinguishable near recurrence is available.

---

# 30. Canonical conclusions

The complete framework can be summarized in the following statements.

1. **Recurrence is not one concept.** Exact state recurrence, near recurrence, observational recurrence, predictive equivalence, and observer-indistinguishable recurrence must be separated.

2. **Exact deterministic recurrence is decisive when the complete state is known.** If the exact complete state returns, the deterministic future repeats from that point.

3. **Observation can hide physical difference permanently.** Exact finite benchmarks contain distinct microscopic trajectories that produce identical observable histories forever.

4. **Near recurrence can exist without exact recurrence.** A deterministic reversible compact trajectory can approach its initial state arbitrarily closely while never returning exactly.

5. **The practical recurrence threshold is observer-relative.** What matters to an observer is not only microscopic state distance but whether any accessible measurement can distinguish the states.

6. **A useful observer recurrence calculation requires three quantities:** microscopic mismatch $d_X$, observer mismatch $d_O$, and detection/divergence time $\tau_\mathrm{detect}$.

7. **Quantum recurrence is spectral.** Exact unitary recurrence requires commensurate occupied energy gaps. Near phase recurrence does not imply exact recurrence.

8. **Period and phase can sometimes be reconstructed from incomplete observations.** In finite benchmark systems, invariants and short temporal records can collapse enormous state spaces and localize cycles.

9. **The present universe can be assigned a reference cosmological coordinate without claiming recurrence.** The reference position is $M3/\Phi_C=0.7376$, where $\Phi_C$ tracks matter–dark-energy composition.

10. **The universe’s far-future branch dominates the cosmic recurrence problem.** Stable de Sitter, metastable de Sitter, fading dark energy, phantom endings, recollapse, and cyclic futures are physically different recurrence environments.

11. **A de Sitter entropy-exponential timescale is conditional.** It is meaningful only after adopting a stable recurrent de Sitter-patch interpretation and is not automatically a microscopic quantum recurrence clock.

12. **Current cosmological data do not determine a unique recurrence probability.** Without theory priors resolving the far future and recurrence mechanism,

```math
P(\text{cosmic recurrence}\mid\text{present observations, unrestricted future theory})\in[0,1].
```

Here `[0,1]` is the full logical bound: a non-identifiability result, not a 50/50 claim or an estimated distribution over recurrence probabilities.

13. **We do not presently know whether an exact cosmic recurrence clock exists.** This is more fundamental than merely not knowing how long the clock takes to tick.

14. **A future fundamental theory could potentially decide the question without waiting for recurrence.** It could prove a return structure, prove only near recurrence, or rule exact recurrence out.

15. **The observer question may be the most interesting computational frontier.** A future universe may fail to match the original exactly and still be physically indistinguishable to every accessible observer over an entire lifetime.

The research question therefore evolves from:

> **“When does everything happen again?”**

to the more precise set:

> **“Does reality possess a return structure at all?”**

> **“What exactly has to return?”**

> **“Which differences are physically observable?”**

> **“How close is close enough that no observer can tell?”**

> **“And what fundamental physics would allow us to prove the answer?”**

---

# References

1. Poincaré, H. (1890). *Sur le problème des trois corps et les équations de la dynamique*. Acta Mathematica.

2. Arnold, V. I. *Mathematical Methods of Classical Mechanics*. Springer.

3. Bocchieri, P., & Loinger, A. (1957). Quantum Recurrence Theorem. *Physical Review*, 107, 337.

4. Schulman, L. S. (1978). Note on the quantum recurrence theorem. *Physical Review A*, 18, 2379.

5. Gupta, C., & Short, A. J. (2026). *Recurrence Time for Finite Quantum Systems*. arXiv:2604.14995.

6. Helstrom, C. W. (1976). *Quantum Detection and Estimation Theory*. Academic Press.

7. Gibbons, G. W., & Hawking, S. W. (1977). Cosmological event horizons, thermodynamics, and particle creation. *Physical Review D*, 15, 2738.

8. Dyson, L., Kleban, M., & Susskind, L. (2002). Disturbing Implications of a Cosmological Constant. *Journal of High Energy Physics*, 10, 011. arXiv:hep-th/0208013.

9. Goheer, N., Kleban, M., & Susskind, L. (2003). The Trouble with de Sitter Space. *Journal of High Energy Physics*, 07, 056. arXiv:hep-th/0212209.

10. Caldwell, R. R., Kamionkowski, M., & Weinberg, N. N. (2003). Phantom Energy and Cosmic Doomsday. *Physical Review Letters*, 91, 071301.

11. DESI Collaboration / Abdul Karim, M. et al. (2025). DESI DR2 Results II: Measurements of Baryon Acoustic Oscillations and Cosmological Constraints. *Physical Review D*, 112, 083515. arXiv:2503.14738.

---

## Repository use

This file is intended to function as the single canonical GitHub document for the Cosmic Recurrence Framework.

All recurrence claims should preserve the distinctions defined here:

```math
\text{exact}
\neq
\text{near}
\neq
\text{observational}
\neq
\text{observer-indistinguishable}.
```

All cosmological recurrence claims should state the assumed future branch.

All observer-relative claims should state the observer model, measurement family, horizon, and tolerance.

All probability statements should separate measured parameter uncertainty from unresolved theory assumptions.

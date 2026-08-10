# Mathematical framework

## 1. Terminology

A **complete state** is a point `x` in a state space `X` that contains every variable required by the deterministic update `F: X -> X`.

An **observation** is a chosen map `h: X -> Y`. It may discard information present in the complete state.

The **future observation sequence** of `x` is

\[
\Phi_h^+(x)=\bigl(h(F^t x)\bigr)_{t\ge 0}.
\]

Two states are **predictively equivalent** or **future-equivalent** when

\[
x\sim_h x'
\quad\Longleftrightarrow\quad
h(F^t x)=h(F^t x')\text{ for every }t\ge0.
\]

An **orbit** is the set of states visited by repeated application of `F`. For a periodic state, its **least period** is the smallest positive integer `p` such that `F^p(x)=x`.

For a period-`p` orbit, the **observation word** is

\[
W_h(x)=\bigl(h(x),h(Fx),\ldots,h(F^{p-1}x)\bigr).
\]

Two finite words are **cyclically equivalent** if one is a cyclic rotation of the other. An **aligned phase** is a choice of starting states on two periodic orbits for which corresponding observation phases agree.

A **predictive singleton** is a future-equivalence class containing one complete state. A **predictive doubleton** contains exactly two complete states.

In the HPP model, a state is **collision-free** when the local collision map fixes every site, equivalently when no site mask is exactly an isolated east-west pair or an isolated north-south pair.

These distinctions must remain separate:

1. equal density at one time;
2. equal density for a finite observation horizon;
3. equal complete future density sequences;
4. equal complete microscopic states;
5. exact recurrence of the complete state;
6. near recurrence in a metric or neighborhood.

Observational indistinguishability under one map `h` is not physical identity and is not indistinguishability under every possible measurement.

## 2. Complete-state repetition

Let `F: X -> X` be deterministic. If

\[
F^m(x)=F^n(x),
\]

then for every nonnegative integer `k`,

\[
F^{m+k}(x)=F^{n+k}(x).
\]

Reversibility is not required. The conclusion fails only when the object called a state omits variables required by the update law.

## 3. Observation closure and predictive equivalence

The raw observation is one-step closed when a deterministic map `G` exists with

\[
h\circ F=G\circ h.
\]

Such a `G` exists exactly when

\[
h(x)=h(x')\Longrightarrow h(Fx)=h(Fx')
\]

for every pair of complete states.

Future equivalence is the stronger relation

\[
x\sim_h x'
\Longleftrightarrow
\Phi_h^+(x)=\Phi_h^+(x').
\]

The quotient by this relation has a well-defined deterministic update `[x] -> [Fx]`. On a finite state space it is computed exactly by partition refinement. Start with classes defined by `h(x)`, then repeatedly split states by the pair

\[
\bigl(h(x),[Fx]\bigr).
\]

Stabilization gives equality of complete future observation sequences.

This construction is a deterministic output-state minimization. It is closely related to Moore-machine state equivalence, deterministic automaton minimization, bisimulation and behavioral equivalence, symbolic coding and generating observations, state observability and distinguishability, predictive-state representations, and computational-mechanics causal-state constructions. The project does not claim those general ideas as new.

## 4. General time-reversal observation theorem

Let `F: X -> X` be a bijection. Let `R: X -> X` be an involution satisfying

\[
R^2=I,
\qquad
RFR=F^{-1}.
\]

Let `h: X -> Y` satisfy

\[
h(Rx)=h(x)
\]

for every `x`.

Then for every integer `t`,

\[
h(F^tRx)=h(F^{-t}x).
\]

### Proof

From `RFR=F^{-1}` it follows by iteration that

\[
F^tR=RF^{-t}.
\]

Therefore

\[
h(F^tRx)=h(RF^{-t}x)=h(F^{-t}x),
\]

using observation invariance under `R`.

The theorem says that the observed future of a reversed state is the observed past of the original state. It does not by itself imply that the two future sequences agree. That requires a reversal symmetry of the periodic observation word.

## 5. Periodic observation-word reversal criterion

Suppose `x` has least period `p`. Assume there is a phase shift `s` modulo `p` such that

\[
h(F^t x)=h(F^{s-t}x)
\]

for every integer `t` modulo `p`.

Define the phase-aligned state on the reversed orbit by

\[
z=F^{-s}Rx=RF^s x.
\]

Then

\[
h(F^t z)=h(F^t x)
\]

for every `t >= 0`. Thus `x` and `z` are future-equivalent.

### Proof

Using the time-reversal theorem,

\[
h(F^t z)
=h(F^{t-s}Rx)
=h(F^{s-t}x)
=h(F^t x).
\]

Periodicity extends the modular equality to every nonnegative time.

### Reversed-orbit cases

The criterion separates four possibilities.

1. **Same microscopic orbit.** The set `R(O(x))` equals `O(x)`. The aligned reversed state may equal `x` or a different phase of the same microscopic cycle.
2. **Distinct microscopic orbit.** The sets `R(O(x))` and `O(x)` are disjoint. In a finite bijective system, distinct cycles cannot intersect.
3. **Distinct but observationally equivalent.** The microscopic cycles are disjoint, but the reversal criterion gives identical complete future observation sequences.
4. **Agreement only after phase alignment.** The unshifted state `Rx` need not match the future observations of `x`; a state `F^{-s}Rx` on the reversed orbit does.

## 6. HPP update and time reversal

For the project’s update convention, the HPP map is

\[
F=S\circ C,
\]

where `C` is the local head-on collision involution and `S` is streaming. Let `V` reverse every particle velocity. Bare velocity reversal satisfies `VSV=S^{-1}` and commutes with `C`, but it is not the global time-reversal involution for an arbitrary collide-then-stream state.

The correct involution is

\[
R=C\circ V.
\]

It satisfies

\[
R^2=I,
\qquad
RFR=F^{-1}.
\]

Site density is invariant under both `C` and `V`, so

\[
h(Rx)=h(x).
\]

On a collision-free state, `C(x)=x`, and therefore `R(x)=V(x)`. This is why the exceptional HPP cycles can be described directly as velocity-reversed partners.

## 7. Exhaustive HPP density result

The full `3x3` sector with exactly four particles and total momentum `(0,0)` contains

\[
|X|=9153
\]

complete microscopic states. The density-refinement class counts are

\[
(495,6948,9090,9126,9126).
\]

The stable quotient contains 9,099 predictive singletons and 27 predictive doubletons. The 54 states in the doubletons have the exact organization

\[
54=18\times3=9\times2\times3.
\]

- 18 disjoint microscopic cycles;
- least period 3 for every cycle;
- 9 time-reversal pairs;
- 2 different microscopic cycles in each pair;
- 3 aligned phases in each pair;
- 27 two-state predictive classes.

Every exceptional state is collision-free. Each particle streams one lattice site per update while retaining its velocity. On a periodic lattice of side length three, three streaming steps return every particle to its initial site. Hence

\[
F^3(x)=x.
\]

Direct checking excludes periods one and two, so the least period is three.

For each pair, the three-phase density word is invariant under reversal up to a cyclic shift. The general criterion therefore applies. The two paired microscopic cycles differ in velocity assignments but produce identical density observations at every aligned future phase.

The exhaustive stable partition proves completeness: all 27 nonsingleton classes are exactly the three aligned phases of the nine time-reversal pairs. Every other state is a predictive singleton. No second ambiguity mechanism occurs in this sector.

## 8. Information-theoretic interpretation

For each exceptional complete future-density record, exactly two microscopic trajectories are compatible under the uniform prior on the stated sector. Conditioned on membership in the exceptional set,

\[
H(X\mid\text{complete density future},\ X\text{ exceptional})
=\log_2 2
=1\text{ bit}.
\]

The sector-wide mean residual conditional entropy is

\[
H(X\mid\text{complete density future})
=\frac{54}{9153}\log_2 2
\approx0.00590\text{ bits}.
\]

Density does not generally lose one bit. The one-bit statement applies only after conditioning on the exceptional set under the stated prior.

## 9. Exact and near recurrence outside the finite HPP result

Finiteness is sufficient for unavoidable exact recurrence but not necessary for exact periodicity. Continuous reversible systems may be exactly periodic, nearly recurrent, or nonrecurrent.

Poincare recurrence concerns return to positive-measure neighborhoods for almost every point under finite-measure, measure-preserving evolution. It does not ordinarily imply exact return to a measure-zero point.

Finite-dimensional quantum state space is continuous. Exact unitary recurrence requires commensurate occupied energy gaps; finite-level systems generally support arbitrarily close phase recurrence rather than exact positive-time return.

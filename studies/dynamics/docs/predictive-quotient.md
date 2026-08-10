# Predictive Quotient Framework

## 1. Purpose and scope

This document generalizes the repository's existing deterministic predictive
quotient from a single observation map to an explicitly declared family of
physically or operationally admissible protocols.

The construction is intentionally theory-relative. It does not identify an
ultimate ontology and does not claim that operational equivalence implies
metaphysical identity. Its role is narrower:

> identify exactly which distinctions are required to preserve the predictions
> produced under a declared model and protocol family.

The existing future-equivalence quotient for a deterministic observation map is
a special case of this construction.

## 2. Dynamical operational model

Let

\[
\mathcal T=(X,F,\Pi,\{P_\pi\}_{\pi\in\Pi}),
\]

where:

- \(X\) is a candidate complete state-description space;
- \(F:X\to X\) is a deterministic discrete-time evolution map;
- \(\Pi\) is a declared family of admissible protocols;
- \(P_\pi(\cdot\mid x)\) is the probability distribution of records generated
  by protocol \(\pi\) from state \(x\).

For deterministic observations, the distributions may be point masses. The
probabilistic notation is used only to provide one common language for
deterministic, noisy, and quantum examples.

For any selected protocol family \(A\subseteq\Pi\), define the complete
prediction map

\[
\mathcal R_A:X\to\mathcal P_A,
\qquad
\mathcal R_A(x)=\bigl(P_\pi(\cdot\mid x)\bigr)_{\pi\in A}.
\]

The codomain \(\mathcal P_A\) is simply the product of the relevant record-
distribution spaces. No additional physical interpretation is assumed.

## 3. Predictive equivalence and quotient

Define

\[
x\sim_A x'
\quad\Longleftrightarrow\quad
\mathcal R_A(x)=\mathcal R_A(x').
\]

Equivalently,

\[
x\sim_Ax'
\quad\Longleftrightarrow\quad
P_\pi(\cdot\mid x)=P_\pi(\cdot\mid x')
\ \text{for every }\pi\in A.
\]

Because equality is reflexive, symmetric, and transitive, \(\sim_A\) is an
equivalence relation.

The corresponding predictive quotient is

\[
Q_A=X/{\sim_A}.
\]

The quotient is canonically isomorphic to the image of the prediction map:

\[
\boxed{
Q_A\cong\operatorname{Im}\mathcal R_A.
}
\]

Each quotient state therefore represents one complete prediction profile under
the declared protocol family.

## 4. Prediction-sufficient factorization theorem

Let \(s:X\to S\) be any deterministic representation through which every
prediction in \(A\) factors. That is, suppose there exists
\(\widehat{\mathcal R}_A:S\to\mathcal P_A\) such that

\[
\mathcal R_A=\widehat{\mathcal R}_A\circ s.
\]

Then

\[
s(x)=s(x')
\Longrightarrow
x\sim_Ax'.
\]

Hence there is a unique induced map

\[
g:s(X)\to Q_A
\]

satisfying

\[
q_A=g\circ s,
\]

where \(q_A:X\to Q_A\) is the quotient map.

Therefore \(Q_A\) is the unique coarsest deterministic representation,
up to predictive isomorphism, that preserves every prediction in \(A\).

This is a theorem about prediction-sufficient deterministic representations.
It is not a theorem that \(Q_A\) is the unique possible ontology.

## 5. Protocol refinement

If

\[
A\subseteq B,
\]

then equality of every prediction in \(B\) implies equality of every prediction
in \(A\). Thus

\[
\sim_B\subseteq\sim_A.
\]

There is therefore a canonical coarse-graining map

\[
Q_B\to Q_A.
\]

Adding admissible protocols can split predictive classes but cannot merge
classes that were already distinguishable.

For two protocol families,

\[
\boxed{
\sim_{A\cup B}=\sim_A\cap\sim_B.
}
\]

The resulting family of predictive quotients is naturally ordered by
refinement. It should be called a refinement poset unless the chosen protocol
family is shown to be closed under the operations required for a full lattice.

## 6. Operational discrimination pseudometric

For a declared family \(A\), define

\[
\delta_A(x,x')
=
\sup_{\pi\in A}
\operatorname{TV}
\left[
P_\pi(\cdot\mid x),
P_\pi(\cdot\mid x')
\right].
\]

Then

\[
\delta_A(x,x')=0
\quad\Longleftrightarrow\quad
x\sim_Ax'.
\]

On the description space \(X\), \(\delta_A\) is generally a pseudometric
because distinct descriptions may have zero operational distance. It induces a
metric on the quotient whenever the usual metric-space conditions are
satisfied.

If \(A\subseteq B\), then

\[
\boxed{
\delta_A(x,x')\le\delta_B(x,x').
}
\]

This stochastic operational distance should remain distinct from a deterministic
trajectory discrepancy such as

\[
\Delta_{h,H}(x,x')
=
\max_{0\le t\le H}
d_Y\!\left(h(F^tx),h(F^tx')\right).
\]

The two quantities can have the same zero set in suitable deterministic
settings, but they answer different approximate-distinguishability questions.

## 7. Existing deterministic predictive quotient as a special case

For a deterministic observation map

\[
h:X\to Y,
\]

define the infinite delayed-observation family

\[
A_h^\infty
=
\{h,h\circ F,h\circ F^2,\ldots\}.
\]

Then

\[
x\sim_{A_h^\infty}x'
\]

if and only if

\[
h(F^tx)=h(F^tx')
\qquad
\text{for every }t\ge0.
\]

Therefore

\[
Q_{A_h^\infty}=Q_h,
\]

the predictive quotient already used throughout this repository.

For a finite horizon \(H\), use

\[
A_{h,H}=\{h,h\circ F,\ldots,h\circ F^{H-1}\}.
\]

Increasing \(H\) produces a monotone refinement of the finite-horizon
predictive quotient.

## 8. Induced quotient dynamics

To use \(Q_A\) as a dynamical state space, predictive equivalence must be
forward-invariant.

A sufficient operational condition is closure under delayed execution: for
each \(\pi\in A\), the protocol "evolve one step and then execute \(\pi\)" is
also represented in \(A\).

Under that condition,

\[
x\sim_Ax'
\Longrightarrow
F(x)\sim_AF(x').
\]

Hence

\[
\boxed{
\bar F_A([x]_A)=[F(x)]_A
}
\]

is well-defined.

For the deterministic future-observation quotient \(Q_h\), this property is
automatic from the definition of complete future equivalence.

## 9. Predictive recurrence

When quotient dynamics are well-defined, define exact \(A\)-predictive
recurrence by

\[
\boxed{
\bar F_A^T([x]_A)=[x]_A.
}
\]

Equivalently,

\[
F^T(x)\sim_Ax.
\]

This gives a hierarchy:

\[
F^Tx=x
\]

is exact complete-description recurrence,

\[
[F^Tx]_T=[x]_T
\]

is theory-level predictive recurrence for a declared complete theory protocol
family, and

\[
[F^Tx]_O=[x]_O
\]

is observer-level predictive recurrence for a restricted observer family.

If a periodic microscopic orbit has least period \(p_X\), the least period
\(p_A\) of its quotient orbit satisfies

\[
\boxed{
p_A\mid p_X.
}
\]

Quotienting may merge different microscopic cycles or reduce a period. Those
are distinct phenomena and must be reported separately.

Near predictive recurrence is defined only after choosing a distance and
tolerance, for example

\[
\delta_A(F^Tx,x)\le\varepsilon_A.
\]

It must not be promoted to exact recurrence.

## 10. Observer, causal, and finite-horizon quotients

The same construction covers observer and causal restrictions without new
mathematics.

If

\[
A_{O,H}\subseteq A_O\subseteq A_C\subseteq A_T,
\]

then

\[
Q_T\to Q_C\to Q_O\to Q_{O,H}.
\]

The arrows are canonical coarse-grainings.

Thus:

- \(Q_T\): distinctions recognized by the declared full theory protocol family;
- \(Q_C\): distinctions accessible within a declared causal region;
- \(Q_O\): distinctions accessible to a declared observer class;
- \(Q_{O,H}\): distinctions accessible to that observer during a finite
  observation horizon.

These are theory- and protocol-relative objects. They are not claims that an
observer creates the underlying state space.

## 11. Operational isomorphism

Suppose two descriptions are related by bijections

\[
U:X_A\to X_B,
\qquad
V:\Pi_A\to\Pi_B,
\]

that preserve outcome statistics:

\[
P^A_\pi(\cdot\mid x)
=
P^B_{V\pi}(\cdot\mid Ux).
\]

Then

\[
x\sim_Ax'
\quad\Longleftrightarrow\quad
Ux\sim_BUx',
\]

and consequently

\[
Q_A\cong Q_B.
\]

If the dynamics also intertwine,

\[
UF_A=F_BU,
\]

then quotient recurrence is preserved under the change of description.

This lemma covers ordinary changes of representation and can be applied to
more specialized settings, including legitimate reference-frame changes,
provided their state, protocol, and dynamical transformations satisfy the
stated hypotheses.

## 12. HPP observability benchmark

The established \(3\times3\), four-particle, zero-momentum HPP sector contains

\[
|X|=9153
\]

microscopic states. Under full site-density observation the exact predictive
refinement is

\[
495\to6948\to9090\to9126\to9126.
\]

The stable quotient contains 9,099 singletons and 27 doubletons, leaving 54
microscopic states in permanent ambiguity under density observation.

The extended observability study adds exact sensor-threshold results.

### Exact local velocity-mask sensors

A sensor at a site records the full four-bit local velocity mask. Exhaustive
search over fixed site subsets gives:

- one site: at most 1,156 predictive classes;
- two sites: at most 4,945 predictive classes;
- three sites: six layouts reconstruct all 9,153 states.

The six successful three-site layouts are

\[
(0,4,8),\ (0,5,7),\ (1,3,8),
\]

\[
(1,5,6),\ (2,3,7),\ (2,4,6),
\]

using row-major site indices. They are the six toroidal diagonals. Each has
refinement sequence

\[
322\to3271\to9123\to9153\to9153.
\]

Thus the minimum fixed spatial sensor count is three and the minimum
reconstructing word length at that count is four.

### Local-momentum sensors

A momentum sensor records only the local vector \((p_x,p_y)\). Exhaustive
search gives:

- four sites: at most 9,081 predictive classes;
- five sites: 36 layouts reconstruct all 9,153 states.

Every successful five-site layout has the refinement sequence

\[
1181\to8391\to8766\to9021\to9143\to9149\to9153\to9153.
\]

Thus the minimum fixed spatial momentum-sensor count is five and the minimum
reconstructing word length at that count is seven.

With local momentum measured at all nine sites, two snapshots reconstruct the
complete state.

### Axis-count observation

If every site reports only the number of horizontal and vertical particles,
the present observation has 2,853 classes but two snapshots reconstruct all
9,153 microscopic states.

These results demonstrate an exact space-time observability tradeoff: temporal
evolution can expose information omitted by an instantaneous measurement when
the hidden variables couple back into the measured channel. Density is a
contrasting case: even the complete infinite density future leaves 27
doubletons unresolved.

## 13. Quotient-cycle benchmark

The same 9,153-state sector contains 2,061 exact microscopic cycles:

\[
1341\times3,\quad459\times6,\quad252\times9,\quad9\times12.
\]

Under complete future-density equivalence, the induced quotient has 2,052
predictive cycles:

\[
1332\times3,\quad459\times6,\quad252\times9,\quad9\times12.
\]

The nine missing cycles arise because 18 distinct microscopic period-three
cycles merge into nine density-predictive cycle pairs. No period compression
occurs in this sector: each state has the same least period in the density
quotient as in the microscopic dynamics.

This distinguishes orbit merging from period shortening.

## 14. Physical and metaphysical boundary

For a declared full protocol family \(A_T\), the quotient

\[
Q_T
\]

is the coarsest deterministic representation sufficient for every prediction
encoded by that family.

It does not follow that

\[
Q_T=\text{ultimate ontology}.
\]

One can always postulate additional variables that never affect any prediction.
Such permanently prediction-inert structure cannot be experimentally
identified by the theory that declares it inert.

A possible metaphysical principle is:

> Two descriptions represent distinct physical realities only if their
> distinction can change some physically permitted consequence.

This Difference-Making Principle is an optional ontological minimality
principle, not a theorem of the predictive quotient framework.

## 15. Cosmological boundary

A cosmic predictive quotient can be defined formally only relative to a
candidate theory that supplies enough of:

\[
(X_{\rm cosmic},F_{\rm cosmic},\Pi_{\rm cosmic})
\]

to specify the relevant state descriptions, dynamics, and physically admissible
distinctions.

Current recurrence calculations in this repository do not provide that complete
fundamental structure. Therefore the cosmic predictive quotient is a
conceptually defined target, not a presently constructed state space.

This extension does not change the repository's cosmological nonclaims. It
does not establish:

- a finite cosmic state space;
- an exact cosmic recurrence period;
- a recurrence phase;
- a model-independent cosmic recurrence probability;
- or that observer-level recurrence implies complete-state recurrence.

## 16. Reporting additions

Studies using this extension should report, where applicable:

```text
Candidate state-description space X:
Dynamics F:
Protocol family A:
Prediction map R_A:
Predictive equivalence relation:
Predictive quotient size or structure:
Protocol-family inclusions:
Operational distance and tolerance:
Temporal-closure condition:
Induced quotient dynamics:
Microscopic recurrence period:
Predictive recurrence period:
Orbit merging or period compression:
Observer/causal/horizon restriction:
Evidence type:
Scope limitation:
```

The evidence hierarchy of the parent Recurrence Dynamics Framework remains
binding.

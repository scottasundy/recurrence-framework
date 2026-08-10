# Recurrence Framework — Master Findings Ledger

**Date:** 2026-08-09  
**Purpose:** Canonical evidence-qualified ledger for the standalone Cosmic Recurrence Framework. It consolidates exact computational results, mathematical results, observer and distinction findings, cosmological calculations, conceptual consequences, negative results, audit corrections, and metaphysical boundaries.

> **Evidence rule:** This ledger intentionally contains more detail than the primary scientific narrative. Each finding is marked by status.  
> **[EXACT]** = exact/reproduced finite computation or algebraic check.  
> **[THEOREM]** = mathematical result under stated assumptions.  
> **[DERIVED]** = direct consequence of definitions/theorems.  
> **[CONDITIONAL]** = valid under explicitly stated physical/theory assumptions.  
> **[CONCEPTUAL]** = interpretation or research implication, not an empirical theorem.  
> **[METAPHYSICAL]** = optional ontological principle or underdetermination result.  
> **[AUDIT]** = correction/simplification established during the full math audit.  
> **[AUXILIARY]** = exact/derived result obtained during the investigation but not yet promoted into the repository's primary validation certificate.

---

## 1. Observer and recurrence findings that motivated the extension

1. **[DERIVED] Exact complete-state recurrence would not carry an internal record of earlier cycles.** If the complete physical state returns, the observer's brain, memory, instruments, notebooks, and other records return as part of that state.
2. **[DERIVED] Remembering a previous exact cycle would itself be a state difference.** A system that accumulates memory across cycles is not undergoing exact complete-state recurrence unless the memory is stored in a larger nonrecurring system outside the declared recurring subsystem.
3. **[CONCEPTUAL] A cycle number need not be an intrinsic physical variable.** An external mathematical description can label occurrences $1,2,3,\ldots$, but if no internal variable changes from cycle to cycle, the ordinal label may be coordinate structure rather than an internally measurable state property.
4. **[DERIVED] Exact global recurrence, observer recurrence, and experiential recurrence are different claims.**
5. **[CONCEPTUAL] Biographical recurrence:** two globally different histories can be identical for an observer over a finite lifetime if every accessible record remains indistinguishable during that lifetime.
6. **[DERIVED] Infinite observation time does not guarantee microscopic reconstruction under an information-losing observation map.** The HPP density benchmark supplies an exact finite example.
7. **[DERIVED] Detection time matters independently of microscopic distance.** A microscopic mismatch can be immediately visible, visible only after delayed dynamical coupling, or permanently invisible to a declared observer.
8. **[CONCEPTUAL] A globally nonrecurring universe could still be recurrent for a causal patch or finite observer under an explicitly declared observer-level recurrence criterion.
9. **[CONCEPTUAL] Personal identity is not settled by state recurrence alone.** Physics can specify equality/equivalence of states without automatically deciding whether two occurrences count as the numerically same person.

---

## 2. Difference, distinction, and reality

10. **[DERIVED] Formal inequality is not automatically physical inequality.**
    ```math
    x\neq x'
    ```
    establishes descriptive difference only.
11. **[DERIVED] Physical-predictive difference is defined by difference in some permitted consequence.**
12. **[DERIVED] Observer-relative difference is weaker than theory-level physical-predictive difference.**
13. **[CONCEPTUAL] “Different” should be qualified rather than replaced:** formal difference, physical-predictive difference, observer-relative difference, and ontological difference are distinct notions.
14. **[CONCEPTUAL] Counterfactual distinguishability is the cleaner scientific target than “could a conscious person notice?”** Ask whether any physically permitted coupling/protocol can produce different record statistics.
15. **[METAPHYSICAL] Candidate Difference-Making Principle (DMP):** two descriptions represent distinct physical realities only if their distinction can change some physically permitted consequence.
16. **[AUDIT] DMP is not a theorem of the quotient mathematics.** It remains an optional ontological minimality principle.

---

# Step 1 — Predictive equivalence and the Physical Predictive Quotient

## 3. Audited core model

17. **[AUDIT] Foundational object:** use a dynamical operational model
    ```math
    \mathcal T=(X,F,\Pi,\{P_\pi\}_{\pi\in\Pi}).
    ```
18. **[AUDIT] The complete prediction map is the primary construction.** For $A\subseteq\Pi$,
    ```math
    \mathcal R_A(x)=\bigl(P_\pi(\cdot\mid x)\bigr)_{\pi\in A}.
    ```
19. **[THEOREM] Predictive equivalence**
    ```math
    x\sim_Ax' \iff \mathcal R_A(x)=\mathcal R_A(x')
    ```
    is an equivalence relation.
20. **[THEOREM] Predictive quotient**
    ```math
    Q_A=X/{\sim_A}
    \cong {Im}\mathcal R_A.
    ```
21. **[THEOREM] Difference criterion**
    ```math
    [x]_A\neq[x']_A
    \iff
    \exists \pi\in A:
    P_\pi(\cdot|x)\neq P_\pi(\cdot|x').
    ```
22. **[THEOREM] Prediction-sufficient factorization:** if a deterministic encoding $s:X\to S$ preserves all predictions in $A$, then the quotient map factors uniquely through $s(X)$.
23. **[AUDIT] Correct strength:** $Q_A$ is the unique coarsest deterministic prediction-sufficient representation up to predictive isomorphism. It is **not** proved to be a unique or minimal ontology.
24. **[THEOREM] Operational discrimination pseudometric**
    ```math
    \delta_A(x,x')
    =
    \sup_{\pi\in A}
    \mathrm{TV}\!\left[P_\pi(\cdot|x),P_\pi(\cdot|x')\right]
    ```
    has zero set exactly $\sim_A$.
25. **[AUDIT] Keep $\delta_A$ separate from deterministic trajectory discrepancy**
    ```math
    \Delta_{h,H}
    =
    \max_{0\le t\le H}
    d_Y(h(F^tx),h(F^tx')).
    ```
    They may have matching zero sets in special deterministic settings but answer different approximate-distinguishability questions.

---

# Step 2 — Exact HPP observability laboratory

## 4. Canonical density result

26. **[EXACT] Sector:** periodic $3\times3$ HPP, four particles, zero total momentum:
    ```math
    |X|=9153.
    ```
27. **[EXACT] Complete future-density refinement**
    ```math
    495\to6948\to9090\to9126\to9126.
    ```
28. **[EXACT] Stable density quotient:** 9,099 singletons + 27 doubletons = 9,126 predictive classes.
29. **[EXACT] 54 microscopic states remain permanently ambiguous to the complete density-history observer.
30. **[EXACT] Residual density-observer ambiguity is only 27 binary classes, but it is exact and permanent under that observation map.

## 5. Exact local velocity-mask sensors

31. **[EXACT] One fixed mask sensor reaches at most 1,156 predictive classes.
32. **[EXACT] Two fixed mask sensors reach at most 4,945 predictive classes.
33. **[EXACT] Three fixed sites are necessary and sufficient among the enumerated fixed-site subsets to reconstruct all 9,153 states.
34. **[EXACT] Exactly six three-site layouts succeed:
    ```math
    (0,4,8),(0,5,7),(1,3,8),(1,5,6),(2,3,7),(2,4,6).
    ```
35. **[EXACT] These six layouts are the six toroidal diagonals in row-major indexing.
36. **[EXACT] Successful refinement:
    ```math
    322\to3271\to9123\to9153\to9153.
    ```
37. **[EXACT] Minimum reconstructing word length at the three-site minimum is four snapshots.

## 6. Local momentum sensors

38. **[EXACT] Four fixed momentum sensors reach at most 9,081 predictive classes.
39. **[EXACT] Five fixed momentum sites are necessary and sufficient among the enumerated fixed-site subsets to reconstruct all 9,153 states.
40. **[EXACT] Exactly 36 five-site momentum layouts succeed.
41. **[EXACT] Successful refinement:
    ```math
    1181\to8391\to8766\to9021\to9143\to9149\to9153\to9153.
    ```
42. **[EXACT] Minimum reconstructing word length at the five-site minimum is seven snapshots.
43. **[EXACT] All-site momentum reconstructs in two snapshots:
    ```math
    6841\to9153\to9153.
    ```

## 7. Axis-count sensor

44. **[EXACT] If every site reports only horizontal and vertical particle counts, the present observation has 2,853 classes.
45. **[EXACT] One additional time slice reconstructs the complete state:
    ```math
    2853\to9153\to9153.
    ```

## 8. Main HPP observability conclusion

46. **[EXACT/DERIVED] There is an exact space-time observability tradeoff.** Missing spatial/state information can be recovered from temporal evolution when hidden degrees of freedom couple back into the measured channel.
47. **[EXACT] Density is qualitatively different:** even infinite density history does not reconstruct all microstates.
48. **[DERIVED] The 27 density doubletons are observer-map dependent, not fundamental physical indistinguishability in HPP.

---

# Step 3 — Predictive refinement structure

49. **[THEOREM] If $A\subseteq B$, then
    ```math
    \sim_B\subseteq\sim_A
    ```
    and there is a canonical coarse-graining
    ```math
    Q_B\to Q_A.
    ```
50. **[THEOREM] Combining protocol families gives
    ```math
    \sim_{A\cup B}=\sim_A\cap\sim_B.
    ```
51. **[AUDIT] Call the structure a predictive refinement poset unless the selected protocol family is proved closed under the operations needed for a full lattice.
52. **[THEOREM] Longer finite horizons monotonically refine prediction classes.
53. **[AUXILIARY] HPP stable predictive-class counts found during the refinement study:
    - no-information observation: 1;
    - global N/E/S/W population observation: 63;
    - local collision-orientation observation: 1,621;
    - joint global-direction + collision-orientation observation: 1,677;
    - density observation: 9,126;
    - density + global-direction observation: 9,126;
    - density + collision-orientation observation: 9,126;
    - density + both: 9,126;
    - local momentum field: 9,153;
    - complete microstate: 9,153.
54. **[AUXILIARY] Present-information refinements observed during the same study:
    - density + global directions starts at 1,323 classes and refines through 8,802 to 9,126;
    - density + collision orientation starts at 1,143 and refines through 7,848 to 9,126;
    - density + both starts at 1,899 and refines through 8,874 to 9,126.
55. **[CONCEPTUAL] Instantaneously informative but predictively redundant information:** an added observable can split present states while adding no new complete-future predictive classes.
56. **[DERIVED] Observer quotients need not form a single chain; incomparable protocol families can distinguish different state pairs.
57. **[CONCEPTUAL] “Distinction depth” can be defined relative to a chosen nested family as the first refinement level at which two states separate. It is chain-dependent, not intrinsic.

---

# Step 4 — Types of hidden difference

58. **[AUDIT] The five-way taxonomy is useful as interpretation but not foundational mathematics.
59. **[DERIVED] Case 1: unmeasured but accessible difference — an available protocol can distinguish states, but it has not been used.
60. **[DERIVED] Case 2: dynamically recoverable hidden information — presently identical records diverge after finite evolution.
61. **[EXACT] The conserved-sector perturbation benchmark contains 150/150 initially density-identical pairs that become density-distinguishable after one update.
62. **[DERIVED] Case 3: observer-relative permanent ambiguity — one observer's entire protocol family cannot distinguish the pair, but a richer physically allowed family can.
63. **[EXACT] The HPP 27 density doubletons are a finite exact example of Case 3.
64. **[CONDITIONAL] Case 4: gauge/representational redundancy — distinct mathematical representatives can correspond to one physical state when the theory itself identifies them through gauge redundancy.
65. **[METAPHYSICAL] Case 5: inert ontological surplus — postulated differences that never alter any physically permitted consequence.
66. **[THEOREM] Inert-extension underdetermination:** if an added variable $\lambda$ never affects any prediction or physically accessible dynamics, the original theory and the $\lambda$-refined theory are empirically indistinguishable with respect to the declared protocol family.
67. **[DERIVED] Permanent invisibility to one observer does not imply prediction-inertness for the full theory.
68. **[DERIVED] Gauge redundancy and inert ontology can have the same prediction profile while carrying different interpretive status.

---

# Step 5 — Cross-theory checks

69. **[CONDITIONAL] Nongauge classical mechanics:** if the admitted physical observables separate phase-space points, then the predictive quotient is isomorphic to the physical phase space.
70. **[CONDITIONAL] Gauge theory:** when operational-equivalence classes coincide with gauge orbits and the relevant gauge-invariant observables separate physical orbits,
    ```math
    Q_T\cong X/G.
    ```
71. **[AUDIT] Do not state $Q_T=X/G$ unconditionally for every gauge theory; global/singular/boundary issues can matter.
72. **[THEOREM/CONDITIONAL] Quantum density operators:** with all POVMs allowed,
    ```math
    \rho\sim_T\sigma \iff \rho=\sigma.
    ```
73. **[DERIVED] Pure state vectors differing only by global phase are predictively equivalent:
    ```math
    |\psi\rangle\sim e^{i\phi}|\psi\rangle,
    ```
    giving projective Hilbert space at the pure-state level.
74. **[DERIVED] Different ensemble decompositions of the same density operator are indistinguishable at the state level unless a larger retained preparation record is part of the declared state/protocol description.
75. **[CONDITIONAL] Restricted quantum measurement families can produce coarser quotients than the full density-operator state space.
76. **[AUDIT] Quantum contextuality is a warning against inferring ontological identity directly from operational equivalence of arbitrary procedures.
77. **[AUDIT] The common architecture across classical, gauge, and quantum examples is better expressed through the total prediction map and its fibers than through separate ad hoc quotients.

---

# Step 6 — Predictive recurrence

78. **[THEOREM] If predictive equivalence is forward invariant—for example because protocols are closed under delayed execution—then quotient dynamics are well-defined:
    ```math
    \bar F_A([x]_A)=[F(x)]_A.
    ```
79. **[THEOREM] Exact $A$-predictive recurrence:
    ```math
    \bar F_A^T([x]_A)=[x]_A
    \iff
    F^Tx\sim_Ax.
    ```
80. **[DERIVED] Recurrence hierarchy:
    ```math
    F^Tx=x
    \Rightarrow
    F^Tx\sim_Tx
    \Rightarrow
    F^Tx\sim_Ox.
    ```
81. **[THEOREM] For a periodic microscopic orbit, the least quotient period divides the microscopic period:
    ```math
    p_A\mid p_X.
    ```
82. **[DERIVED] Quotienting can merge distinct cycles, shorten a period, or both. These are different phenomena.
83. **[EXACT] HPP microscopic cycle count:
    ```math
    2061
    ```
    with
    ```math
    1341\times3,\ 459\times6,\ 252\times9,\ 9\times12.
    ```
84. **[EXACT] Complete future-density quotient:
    ```math
    2052
    ```
    cycles with
    ```math
    1332\times3,\ 459\times6,\ 252\times9,\ 9\times12.
    ```
85. **[EXACT] Exactly nine period-three orbit-pair mergers occur.
86. **[EXACT] No density-quotient period compression occurs in this sector.
87. **[DERIVED] Near physical-predictive recurrence can be defined by
    ```math
    \delta_A(F^Tx,x)\le\varepsilon_A,
    ```
    but must remain distinct from exact recurrence.
88. **[CONDITIONAL] A trajectory can fail to close in a redundant gauge representative while closing in the reduced/predictive physical state space.

---

# Step 7 — Metaphysical boundary

89. **[AUDIT] Replace “minimal predictive ontology theorem” with the prediction-sufficient factorization theorem.
90. **[THEOREM] Any deterministic representation sufficient for all declared predictions must distinguish at least the predictive quotient classes.
91. **[METAPHYSICAL] Richer ontologies can always be postulated inside prediction-map fibers if the added structure is declared prediction-inert.
92. **[THEOREM/LOGICAL] No experiment internal to a theory can identify a variable defined never to influence any permitted record.
93. **[METAPHYSICAL] Minimal physical realism adopts
    ```math
    \Omega_{physical}\cong Q_T.
    ```
94. **[METAPHYSICAL] Surplus realism permits a many-to-one ontology over $Q_T$.
95. **[METAPHYSICAL] Instrumentalism can remain silent about deeper ontology and use only the predictive structure.
96. **[CONDITIONAL] $Q_T$ is theory-relative, not automatically ultimate. A successor theory with a richer protocol set can split classes that were equivalent under $T$.
97. **[CONCEPTUAL] Recurrence itself can therefore be metaphysically underdetermined if one insists on permanently inert hidden variables: every predictive distinction may recur while an alleged deeper inert label does not.

---

# Step 8 — Causal, finite-observer, reference-frame, and cosmological extensions

98. **[THEOREM] Protocol inclusion produces the hierarchy
    ```math
    Q_T\to Q_C\to Q_O\to Q_{O,H}.
    ```
99. **[THEOREM] Causal monotonicity:** if $C_1\subseteq C_2$ with nested protocol access, then
    ```math
    \delta_{C_1}\le\delta_{C_2}.
    ```
100. **[THEOREM] Finite-horizon monotonicity:** if $H_1\le H_2$, then
    ```math
    \delta_{O,H_1}\le\delta_{O,H_2}.
    ```
101. **[DERIVED] Detection time can be defined as the first horizon at which two states become distinguishable relative to the chosen observer/protocol family.
102. **[CONCEPTUAL] Finite-life equivalence formalizes “same life from the inside” without asserting global state equality.
103. **[DERIVED] Global predictive recurrence implies patch recurrence implies observer recurrence when protocol families are nested; reverse implications need not hold.
104. **[DERIVED] Different observers can disagree about observer-level recurrence without logical contradiction.
105. **[THEOREM] Operational-isomorphism lemma:** bijective state/protocol transformations preserving record probabilities induce isomorphic predictive quotients.
106. **[CONDITIONAL] Legitimate quantum-reference-frame changes are one application when states, protocols, and dynamics transform consistently.
107. **[THEOREM] If the dynamics also intertwine under the operational isomorphism, quotient recurrence is preserved.
108. **[AUDIT] Do not overclaim equality of numerical coordinate recurrence times under arbitrary relativistic/reference-frame reparameterizations; preserve the structural return claim.
109. **[CONDITIONAL] A cosmic predictive quotient is conceptually definable only relative to a theory specifying enough of
    ```math
    (X_{cosmic},F_{cosmic},\Pi_{cosmic}).
    ```
110. **[CURRENT BOUNDARY] The actual cosmic predictive quotient is presently not constructible because those fundamental ingredients are not known at the necessary level.
111. **[DERIVED] The predictive-quotient framework does not itself create a cosmic recurrence mechanism; asymptotic future physics still decides whether a return structure exists.

---

# Step 9A — Full mathematics audit

112. **[AUDIT] The prediction map $\mathcal R_A$ plus protocol inclusion generates most of the framework and should be primary.
113. **[AUDIT] Separate quotient definitions for observer, causal patch, finite horizon, and full theory are special cases of the same $Q_A$ construction.
114. **[AUDIT] Replace the claimed distinction lattice with a refinement poset unless lattice closure is proven.
115. **[AUDIT] Keep operational TV distance and deterministic trajectory discrepancy distinct.
116. **[AUDIT] The quotient-dynamics theorem requires explicit forward-invariance / delayed-protocol closure.
117. **[AUDIT] The period-divisibility result survives.
118. **[AUDIT] Detection time and distinction depth are derived diagnostics, not primitives.
119. **[AUDIT] The five hidden-difference categories are interpretive taxonomy, not primitive mathematics.
120. **[AUDIT] The QRF-specific theorem reduces to the more general operational-isomorphism lemma.
121. **[AUDIT] Correct finite-state recurrence wording:
     - finite deterministic dynamics guarantee eventual state repetition and eventual entry into a cycle;
     - exact return of every initial state requires bijectivity/reversibility or another no-transient periodicity condition.
122. **[AUDIT] HPP is unaffected by that correction because the HPP update is reversible.
123. **[AUDIT] HPP scalar transport-clock result survives:
    ```math
    \Phi(FX)=\Phi(X)+N\pmod L
    ```
    implies
    ```math
    \frac{L}{\gcd(N,L)}\mid T.
    ```
124. **[AUDIT] HPP diagonal-species clocks, line-momentum invariants, and checkerboard parity arguments remain consistent with the update law.
125. **[AUDIT] Interaction-fiber relation $T=g\tau$ is valid when $g$ is a proven period divisor and $\tau$ is the least period of $F^g$ on the declared reference/fiber.
126. **[AUDIT] Quantum exact recurrence condition survives:
    ```math
    \frac{(E_n-E_m)T}{\hbar}\in2\pi\mathbb Z
    ```
    for occupied energy gaps.
127. **[AUDIT] Finite-spectrum near recurrence must remain distinct from exact recurrence.
128. **[AUDIT] Quantum trace distance is an instance of the operational discrimination structure when the protocol family contains all POVMs.
129. **[AUDIT] Gauge-quotient statements require explicit separation assumptions.
130. **[AUDIT] The theory-level quotient $Q_T$ should never be called “ultimate reality” without an additional metaphysical principle.

---

# Audited cosmological mathematics retained from the broader framework

131. **[EXACT ALGEBRAIC CHECK] Cosmic composition coordinate
    ```math
    \Phi_C=\frac{2}{\pi}\arctan\frac{\rho_\Lambda}{\rho_m}
    ```
    with $\Omega_{m0}=0.3042,\Omega_{\Lambda0}=0.6958$ gives
    ```math
    \Phi_C=0.7376145673.
    ```
132. **[AUDIT] $\Phi_C$ is a model-conditional composition coordinate, not a recurrence phase.
133. **[EXACT ALGEBRAIC CHECK] Inversion
    ```math
    a(\Phi_C)=
    \left[
      \frac{\Omega_{m0}}{\Omega_{\Lambda0}}
      \tan\left(\frac{\pi\Phi_C}{2}\right)
    \right]^{1/3}
    ```
    is correct for the declared reference model.
134. **[EXACT ALGEBRAIC CHECK] Declared late-time age relation reproduces approximately
    ```math
    13.7869193\ \text{Gyr},
    ```
    with the stated radiation-neglect caveat.
135. **[EXACT NUMERICAL CHECK] Declared de Sitter reference arithmetic reproduces approximately
    ```math
    H_\Lambda^{-1}=17.2105\ \text{Gyr},
    ```
    ```math
    r_{dS}=1.62824\times10^{26}\ \text{m},
    ```
    ```math
    S_{dS}/k_B=3.18835\times10^{122}.
    ```
136. **[CONDITIONAL] Entropy-exponential recurrence scale
    ```math
    t_{thermo}\sim H_\Lambda^{-1}e^{S_{dS}/k_B}
    ```
    is a conditional thermodynamic estimate, not a demonstrated quantum recurrence time.
137. **[EXACT NUMERICAL CHECK] Equal-prior conversion of $\ln B=-0.57$ gives approximately 63.9% / 36.1% weights for the declared two-model comparison.
138. **[AUDIT] Those weights are not ultimate-fate probabilities and not cosmic-recurrence probabilities.
139. **[AUDIT] The unrestricted
    ```math
    [0,1]
    ```
    cosmic-recurrence result is a non-identification statement: under the deliberately unrestricted future-theory class, current data do not narrow the identified set below logical bounds.
140. **[AUDIT] Do not present $[0,1]$ itself as a numerical observational discovery; its scientific content lies in the uncertainty decomposition explaining why the target is unidentified.

---

# Reproducibility and package findings

141. **[EXACT] The master repository includes automated umbrella, dynamics, cosmology, and observer test suites plus independent deterministic certificates; the current executed counts are recorded in `validation.txt`.
142. **[EXACT] Dedicated tests cover the velocity-mask search certificate, momentum search certificate, representative reconstruction partitions, and predictive-cycle summaries.
143. **[EXACT] The observability extension has reproducible scripts and machine-readable CSV/JSON outputs.
144. **[AUDIT] New exact sensor findings are now separated from narrative claims by explicit certificates/tests.
145. **[SCOPE] HPP remains a finite methodological benchmark, not a cosmological model.

---

# Cross-cutting scientific conclusions

146. **[DERIVED] “Looks identical” is weaker than “is predictively identical,” which is weaker than “is the same complete mathematical state.”
147. **[DERIVED] A hidden difference can be irrelevant to one observer yet physically relevant to a richer allowed protocol.
148. **[DERIVED] Observation time and measurement content jointly determine reconstructibility.
149. **[DERIVED] More time cannot recover information that the complete chosen observation process permanently identifies.
150. **[DERIVED] More information can refine predictive classes, but added instantaneous information can sometimes be predictively redundant over a complete future.
151. **[DERIVED] Predictive recurrence is recurrence on the quotient appropriate to the declared level of physical identity.
152. **[DERIVED] Orbit merging and period compression are distinct quotient phenomena.
153. **[DERIVED] Physical predictive equivalence is theory-relative; a successor theory can refine it.
154. **[DERIVED] A causal or finite observer generally inhabits an equivalence class of globally possible states rather than having operational access to a unique global state.
155. **[CONCEPTUAL] The scientifically sharp version of “when does a difference in description correspond to a difference in reality?” is:
     > When does a descriptive difference survive the complete prediction map of the declared physical theory?
156. **[METAPHYSICAL] The further identification of that predictive structure with all of physical reality requires an ontological principle such as DMP.
157. **[LOGICAL] Physics can identify distinctions that make physical differences; it cannot experimentally rule out distinctions defined never to make one.
158. **[CURRENT COSMOLOGICAL BOUNDARY] None of these results proves that our universe recurs, possesses a recurrence clock, has a known recurrence phase, or has a model-independent recurrence probability.

---

# Findings intentionally *not* promoted to stronger claims

159. Observer-indistinguishable recurrence is not exact complete-state recurrence.
160. The HPP density ambiguity is not unrestricted physical indistinguishability.
161. A bounce, recollapse, cyclic scale factor, or empty future is not automatically complete-state recurrence.
162. Finite de Sitter entropy is not by itself proof of a finite exact cosmic quantum state space or a rigorous quantum recurrence clock.
163. The Cosmic Coordinate is not a recurrence phase.
164. Restricted Bayesian model weights are not probabilities of ultimate cosmic fate.
165. The $[0,1]$ identified set is not an informative probability estimate.
166. Operational equivalence does not automatically imply ontological identity.
167. Quantum-reference-frame covariance does not imply all frame-dependent quantities are numerically identical.
168. The predictive refinement structure is not called a full lattice without a closure proof.
169. The coarsest prediction-sufficient quotient is not called a unique ontology.
170. The recurrence framework does not establish OFT, primitive consciousness, or observer-created reality.

---

# What is fully package-validated vs preserved as investigation findings

## Fully reproduced / regression-certified in the master repository
- canonical HPP density quotient;
- exact mask-sensor threshold and six layouts;
- exact momentum-sensor threshold and 36 successful layouts;
- all-site momentum and axis-count two-snapshot reconstruction;
- microscopic and density-predictive cycle counts;
- no density period compression;
- audited prediction-map / quotient formulation;
- finiteness wording correction;
- package integrity and tests.

## Mathematically audited but not a standalone finite-data certificate
- prediction-sufficient factorization theorem;
- protocol-refinement monotonicity;
- operational pseudometric;
- quotient dynamics under forward-invariance;
- period-divisibility theorem;
- causal/horizon monotonicity;
- operational-isomorphism lemma;
- inert-extension underdetermination.

## Preserved auxiliary findings that should receive their own regression certificate if promoted
- 63 global-direction predictive classes;
- 1,621 collision-orientation predictive classes;
- 1,677 joint direction+collision classes;
- density+auxiliary-observable transient refinement counts;
- “instantaneously informative but predictively redundant” HPP examples.

## Conceptual / metaphysical findings preserved but not claimed as physics theorems
- cycle-memory consequence;
- intrinsic-vs-external cycle number;
- biographical recurrence;
- personal-identity question;
- Difference-Making Principle;
- minimal realism / surplus realism / instrumentalism alternatives;
- metaphysical underdetermination by permanently inert variables.

---

# One-sentence synthesis

The investigation shows that recurrence and physical identity are best analyzed not only on raw mathematical states, but on **prediction-equivalence classes generated by explicitly declared physically admissible distinctions**—while carefully separating observer limitations, recoverable hidden information, representational redundancy, and metaphysical surplus.


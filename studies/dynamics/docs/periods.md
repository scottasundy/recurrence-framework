# Period constraints and phase navigation

The framework includes exact recurrence-period constraints, interaction-fiber
reduction, and phase navigation to the Recurrence Dynamics Framework.

The organizing chain is:

\[
\text{state}\rightarrow\text{invariants}\rightarrow\text{fiber}\rightarrow
\text{cycle}\rightarrow\text{phase}.
\]

All results here concern the finite reversible HPP lattice gas. They do not
claim that the physical universe is finite, exactly recurrent, or HPP-like.

## Analytic results

### Scalar transport clock

For an \(L\times L\) torus,

\[
\Phi(X)=\sum_E x-\sum_W x-\sum_N y+\sum_S y\pmod L.
\]

Head-on collisions preserve this quantity locally and streaming advances every
occupied channel by one, so

\[
\Phi(FX)=\Phi(X)+N\pmod L.
\]

Thus every exact recurrence period satisfies

\[
NT\equiv0\pmod L,
\qquad
\frac{L}{\gcd(N,L)}\mid T.
\]

### Four diagonal-species clocks

The local species \(E+N\), \(E+S\), \(W+N\), and \(W+S\) are each preserved by
the head-on collision. Their histograms on coordinates

\[
x-y,\ x+y,\ -x-y,\ -x+y \pmod L
\]

rotate rigidly by one bin per update. If their joint rotational period is
\(g\), then \(g\mid T\), and the present state supplies phase modulo \(g\).

### Exact line momenta

Horizontal momentum in each row,

\[
P_x(y)=\sum_x(n_E-n_W),
\]

and vertical momentum in each column,

\[
P_y(x)=\sum_y(n_S-n_N),
\]

are conserved by every HPP update.

### Checkerboard sign modes

On even tori, checkerboard-weighted density and momentum modes flip sign every
update. Any nonzero mode forces an even recurrence period.

## Interaction-fiber decomposition

After \(g\) updates, the diagonal histograms return. The macro-map

\[
G=F^g
\]

is therefore confined to the set of states with the reference diagonal
histograms and line momenta. We call this the **interaction fiber**.

If the \(G\)-cycle has length \(\tau\),

\[
T=g\tau.
\]

This is the main simplification of the framework: transport/geometry is separated from
the remaining nonlinear interaction cycle.

## Exhaustive 3x3 benchmark

The four-particle zero-momentum sector contains 9,153 states and 2,061 cycles.
Only periods

\[
3,6,9,12
\]

occur. Six consecutive active-collision counts determine the exact period
class for all 9,153 states; five counts leave 1,800 states ambiguous.

## Exhaustive 4x4 benchmark

The four-particle zero-momentum sector contains 94,336 states and 19,448
cycles. Only

\[
2,4,6,8,12,20,28
\]

occur.

Under site-density observation, the number of period-ambiguous states falls:

- 1 frame: 69,584
- 2 frames: 6,704
- 3 frames: 128
- 4 frames: 0

The diagonal-histogram period is \(g=4\) for 93,312 states and \(g=2\) for
1,024 states, with zero violations of \(g\mid T\).

Exact diagonal histograms plus line momenta split the sector into 58,758
interaction fibers. 45,536 fibers, containing 51,648 states
(54.7489823609%), are already exactly one macrocycle.

## 5x5 seed-75202 reference orbit

The existing seeded sweep contains a 5x5, 14-particle, zero-momentum state with

\[
T=9705,\qquad g=5,\qquad \tau=1941.
\]

The full 5x5, 14-particle, zero-momentum sector contains exactly

\[
2,240,809,149,480,000
\]

complete states. The reference diagonal histograms and line momenta reduce
that sector to only 2,209 compatible states.

The 2,209-state fiber decomposes under \(G=F^5\) into exactly 17 cycles:

\[
1941,46,45,44,28,18,14,14,10,9,8,8,7,5,5,4,3.
\]

The reference lies on the 1,941-state macrocycle. The invariant fiber therefore
gives the pre-traversal bound

\[
T\le 5\times2209=11045.
\]

### Short observation inside the fiber

Collision-orientation frames use `0 = none`, `1 = EW`, and `2 = NS`.

For the reference state:

- one frame leaves 551 candidates;
- two frames leave exactly two candidates, both on the 1,941 macrocycle;
- three frames identify the exact reference state.

Across all 2,209 fiber states:

- six frames determine the macroperiod class for every state;
- nine frames uniquely identify every state.

## Phase navigation and sensor reduction

Once \(T\) is known, the histogram residue plus reversibility locates exact
phase without storing a complete orbit atlas. It is constant-memory navigation,
not generic fast-forwarding.

On the 9,705-state reference orbit:

- the minimum velocity-bit Hamming distance between distinct states is exactly
  4, so nearest-orbit decoding can correct one arbitrary bit error;
- a deterministic greedy set of 49 of 100 velocity channels uniquely
  distinguishes all phases from one snapshot;
- a deterministic greedy set of 11 of 25 sites, watched as density for three
  frames, uniquely distinguishes all phases.

The sensor counts are greedy upper bounds, not proofs of global minimality.

## Universal linear invariants for 5x5 F^5

The known diagonal-histogram and line-momentum coefficient vectors span 27
independent linear invariants. A deterministic 80-state finite-field witness
produces difference vectors \(F^5(X)-X\) of rank 73 modulo 1,000,003. A
nonzero minor modulo a prime is nonzero over the rationals, so any universal
rational/real linear invariant space has dimension at most \(100-73=27\).
Therefore the known family exhausts the universal **linear** invariant space.

This does not rule out nonlinear invariants.

## Empirical 5x5 period-scale sample

A fixed sample of 500 additional 5x5, 14-particle, zero-momentum initial states
uses seeds 880000 through 880499. It contains 344 distinct exact periods from
5 through 201,810.

The optional regression analysis uses only the first 30 updates of collision
and step-Hamming history plus simple initial/summary features. Five-fold
cross-validation on the committed sample gives approximately:

- \(R^2=0.724\) for \(\log_{10}T\);
- median multiplicative error about \(2.17\times\);
- 90th-percentile multiplicative error about \(9.16\times\).

This is empirical period-scale prediction, not exact prediction and not a
universal law.

## Supplemental calibrated interaction clock

The degree-four interaction clock retained under `supplemental/` is calibrated
using the complete 1,941-state macro-orbit. It is an orbit-specific encoded
atlas, not a first-principles universal modulo-3 or modulo-647 law.

## Evidence register

| Result | Evidence |
|---|---|
| transport clock | analytic |
| diagonal histogram rotation | analytic |
| row/column line momenta | analytic |
| checkerboard sign flip | analytic |
| 3x3 period/collision result | exhaustive finite computation |
| 4x4 period/density result | exhaustive finite computation |
| 4x4 interaction-fiber counts | exhaustive finite computation |
| 5x5 2,209-state fiber | exhaustive constrained enumeration |
| 5x5 17-cycle decomposition | exhaustive finite computation |
| 27-dimensional linear-invariant closure | analytic basis + finite-field rank certificate |
| sensor counts | deterministic computation on one orbit |
| 500-state period predictor | empirical cross-validation |
| degree-four calibrated decoder | orbit-specific supplemental calibration |

## Nonclaims

This study does not establish that the physical universe has a finite state
space, that cosmological history exactly recurs, that a physical recurrence
period can be inferred from HPP, or that the orbit-specific calibrated decoder
is a universal law.

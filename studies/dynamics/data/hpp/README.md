# Square HPP lattice gas

## Model and update convention

Each site on a periodic square lattice stores four Boolean velocity channels. Exact east-west and north-south head-on pairs exchange orientation, followed by streaming.

Writing the collision map as `C`, streaming as `S`, and the complete update as `F = S after C`, both `C` and `S` are invertible. For this convention, the global time-reversal involution is `R = C after V`, where `V` reverses every velocity. On collision-free states, `R = V`.

The density observation records the particle count at each site and discards velocity direction.

## Exact predictive quotient

The full `3x3` sector with exactly four particles and total momentum `(0,0)` contains 9,153 complete microstates. Sitewise density produces the exact refinement sequence

$$
(495, 6948, 9090, 9126, 9126).
$$

The stable predictive quotient contains:

- 9,099 singleton classes;
- 27 two-state classes;
- no larger classes.

An ambiguous state is a complete velocity-channel microstate in one of those doubletons. It is not merely a state that shares the present density with another state; its complete future density sequence is also shared.

The exceptional count decomposes as

$$
54=18\times3=9\times2\times3.
$$

- `18 x 3`: 54 states on 18 disjoint microscopic cycles of least period 3.
- `9 x 2 x 3`: 9 density movies, 2 microscopic time orientations per movie, and 3 aligned phases.
- `9 x 3 = 27`: one predictive doubleton at each aligned phase of each pair.

Every exceptional state has four singly occupied sites and no active collision. Velocities remain fixed, particles stream one site per update, and the side-three periodic geometry returns every particle after three steps. Reversing all velocities maps each exceptional cycle to its distinct paired cycle up to cyclic phase alignment.

For each pair, the three-phase density word is invariant under reversal up to a cyclic shift. Therefore the forward and phase-aligned reversed microscopic cycles have identical density futures for every time, not merely for a finite horizon.

The exhaustive stable partition contains no additional nonsingleton class, so no other ambiguity mechanism occurs in the enumerated sector.

## Information statement

Each exceptional complete future-density record is compatible with exactly two microscopic trajectories under the uniform sector prior. Conditioned on the exceptional set, the residual uncertainty is one bit. Averaged over all 9,153 sector states, it is

$$
\frac{54}{9153}\log_2 2\approx0.00590\text{ bits}.
$$

This does not mean that density generally loses one bit.

## Machine-checkable certificate

`ambiguity.csv` contains all 54 exceptional states. Each row records:

- pair, cycle, and aligned phase;
- fixed-width hexadecimal state encoding;
- velocity-reversed encoding;
- density encoding;
- successor and predecessor;
- velocity-reversal partner phase;
- observation-word reversal shift;
- least period;
- active collision count.

Run the independent verifier from the repository root:

```bash
python scripts/verify_ambiguity.py
```

The script reconstructs the sector and predictive partition without importing the project package or the high-level generator.

## Figure

`ambiguity.png` shows one full pair of microscopic period-three cycles. Matching columns have identical occupied-cell shading and different velocity arrows. Opposite lattice edges are identified.

## Other generated files

- `hamming.csv` records a reference orbit and one-bit perturbation over their joint period.
- `size-sweep.csv` lists exact periods for three fixed seeded states at lattice sizes 3 through 7.

The HPP lattice is anisotropic. The exhaustive classification applies only to the stated sector and observation map.

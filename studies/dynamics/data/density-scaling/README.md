# Fixed-density scaling study

## Design

Paired square-lattice HPP states were sampled at lattice sizes 4, 6, 8, and 10
with velocity-channel fillings 0.125, 0.25, and 0.375. Each condition contains
100 pairs, for 1200 paired trajectories in total.

Within each pair, the density field, direction counts, particle number,
momentum, and kinetic energy are identical. The perturbation exchanges two
velocity labels and changes four microscopic bits. Each pair was observed
through time 1000.

## Results

- Density trajectories diverged in 1200 of 1200 pairs.
- Microscopic damage exceeded four bits in 1158 pairs.
- Normalized microscopic damage reached 0.5 in 669 pairs.
- Normalized microscopic damage reached 0.75 in 169 pairs.
- Twenty of 30 paired cycle searches closed below the cap.
- Nineteen of the 20 closed pairs had different periods.

`summary.csv`, `trials.csv`, and `damage.csv`
contain the tabulated values. The PNG files show microscopic and macroscopic
damage by condition.

Cycle searches that reached the cap are censored. Hamming-distance growth is a
finite-time diagnostic, not a Lyapunov exponent.

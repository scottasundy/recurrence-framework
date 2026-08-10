# Hexagonal rotor lattice gas

## Model

The model uses six velocity channels on a periodic hexagonal lattice. A local
rotor bit controls the orientation of head-on collisions and toggles during
those collisions. The complete state consists of six particle fields and the
rotor field. The rule is deterministic and exactly reversible.

The rotor is a mathematical memory variable. It is not identified with an
established microscopic interaction.

## Design

Lattice sizes 4, 6, 8, and 10 were sampled at particle densities 0.5, 1.0,
and 1.5 particles per cell. Each condition contains 75 paired trajectories,
for 900 pairs in total. Paired states begin with identical density fields,
direction populations, particle number, momentum, energy, and rotor fields.
The perturbation exchanges two velocity labels.

## Results

- Density trajectories diverged in 900 of 900 pairs.
- Particle Hamming distance grew above four bits in 852 pairs.
- Rotor fields diverged in 849 pairs.
- Seven of 15 paired cycle searches closed below the cap.
- Four of the seven closed pairs had different periods.
- Rotational covariance $F(RS)=R(FS)$ passed 300 trajectory checks.

The CSV files contain pair-level, condition-level, and mean-series results.
The PNG files show particle, rotor, and macroscopic damage.

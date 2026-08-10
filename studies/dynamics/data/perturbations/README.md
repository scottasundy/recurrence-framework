# Conserved-sector perturbations

## Design

Paired square-lattice HPP states were constructed with identical cell-density
fields, particle number, total momentum, and kinetic energy. The perturbation
exchanges two velocity labels and has an initial microscopic Hamming distance
of four bits.

The study contains 150 paired trajectories: 50 each on $5\times5$,
$6\times6$, and $7\times7$ lattices. Each trajectory was observed through
time 2000. Ten pairs per size were also subjected to exact cycle searches.

## Results

- Density trajectories diverged in 150 of 150 pairs.
- Microscopic Hamming distance grew above four bits in 139 of 150 pairs.
- Half of the maximum possible Hamming distance was reached in 109 pairs.
- All 30 cycle-search pairs closed within the search cap.
- The paired periods differed in 26 of those 30 cases.
- No pair belonged to the same exact orbit.

`trials.csv` contains pair-level results.
`damage.csv` contains ensemble means.
`damage.png` shows the damage trajectories.

These statistics describe the selected ensemble and do not establish a
universal scaling law.

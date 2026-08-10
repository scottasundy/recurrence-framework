# Second-order binary cellular automaton

## Model

The complete state consists of two consecutive periodic binary configurations,

$$
S_t=(x_{t-1},x_t),
$$

with update

$$
x_{t+1,i}=x_{t-1,i}\oplus x_{t,i-1}\oplus x_{t,i+1}.
$$

The complete-state map is reversible because

$$
x_{t-1,i}=x_{t+1,i}\oplus x_{t,i-1}\oplus x_{t,i+1}.
$$

## Exact reconstruction result

A single visible configuration has only `2^N` possibilities while the complete state has `2^(2N)` possibilities, so one snapshot cannot reconstruct the state. Two consecutive visible configurations reconstruct the predecessor exactly. For every lattice size,

$$
\text{class counts}=(2^N,2^{2N},2^{2N}).
$$

The implementation exhaustively verifies this result for sizes 2 through 8, covering 87,376 complete states.

## Reference orbit

For an eight-cell ring with

```text
x(-1) = 00000000
x(0)  = 00010000
```

the complete state has period 8. The visible configuration repeats at two phases with different predecessors and successors, giving a direct incomplete-state counterexample.

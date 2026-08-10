# Observer Indistinguishability

This study isolates the question:

> **How can two physical states fail to match exactly while remaining indistinguishable to an observer?**

It does not assign a guessed “human similarity percentage.” Instead, it computes operational examples from the bundled recurrence data and leaves the human/cosmological observer threshold explicitly unidentified until a physical observer model is supplied.

## Core definition

For an observer $O$ with physically accessible protocols $\Pi_O$, define

```math
d_O(x,x')
=
\sup_{\pi\in\Pi_O}
{TV}
\left[
P_\pi(\cdot|x),P_\pi(\cdot|x')
\right].
```

An observer-indistinguishable return at tolerance $\varepsilon_O$ satisfies

```math
d_O(F^T x,x)\leq\varepsilon_O.
```

This is weaker than exact state equality and stronger than vague visual similarity.

## Reproduce

```bash
python run.py
python -m pytest
```

## Bundled exact/analytic results

### Permanent observational ambiguity

The exact $3\times3$ HPP certificate contains **27 predictive doubletons / 54 microscopic states** for which the two microscopic states differ but the aligned density observation is identical forever.

For the declared density observer:

```math
d_O=0
```

while the microscopic states are unequal.

Under an equal prior within one doubleton, the unresolved microscopic information is exactly

```math
\log_2 2=1\ \text{bit}.
```

### Hidden now, visible one step later

The conserved-sector perturbation dataset contains **150 trials** across $5\times5$, $6\times6$, and $7\times7$ lattices. Every pair begins with exactly the same density observation and a microscopic velocity-bit Hamming distance of 4. In all 150 trials, the density observations separate after one update.

This is the complementary result: microscopic mismatch can be either permanently invisible or rapidly amplified into an observable difference.

### Near recurrence with no exact clock

For the irrational torus flow

```math
q(t)=(t,\sqrt2\,t)\pmod1,
```

there is no exact positive recurrence. The bundled continued-fraction returns nevertheless cross increasingly strict finite observer tolerances:

| Tolerance | First listed return time | Error |
|---:|---:|---:|
| $10^{-1}$ | 5 | $7.11\times10^{-2}$ |
| $10^{-2}$ | 70 | $5.05\times10^{-3}$ |
| $10^{-3}$ | 408 | $8.67\times10^{-4}$ |
| $10^{-4}$ | 5,741 | $6.16\times10^{-5}$ |
| $10^{-5}$ | 80,782 | $4.38\times10^{-6}$ |
| $10^{-6}$ | 470,832 | $7.51\times10^{-7}$ |

Thus every finite threshold in this table eventually declares a practical return even though exact equality never occurs.

### Quantum discrimination

For quantum states with trace distance $D$, the optimal equal-prior one-shot discrimination probability is

```math
P_{correct}=\frac{1+D}{2}.
```

A trace distance $D=10^{-6}$, for example, gives only $50.00005\%$ optimal single-shot identification success.

This does not by itself produce a cosmic recurrence time. A cosmological application still requires a justified microscopic quantum model and accessible measurement set.

## Outputs

- `outputs/hpp.csv`
- `outputs/perturbations.csv`
- `outputs/torus.csv`
- `outputs/quantum.csv`
- `outputs/summary.json`

## Open target

The quantity most relevant to a returned human observer is not a bare global norm. A future study should jointly estimate

```math
d_X,\qquad d_O,\qquad \tau_{detect},
```

where:

- $d_X$ is complete-state mismatch;
- $d_O$ is observer-accessible mismatch;
- $\tau_{detect}$ is the first time residual differences become detectable.

The especially interesting regime is

```math
d_X>0,\quad d_O\approx0,\quad \tau_{detect}>H_O,
```

where the universe is not exactly identical but no difference becomes available to the observer during the observer’s accessible future.

"""Core calculations for the Cosmological Recurrence Probability Study.

The module deliberately separates four objects that are easy to conflate:
1. observational parameter uncertainty inside a specified cosmological model;
2. the far-future cosmological branch;
3. thermodynamic de Sitter recurrence-scale estimates; and
4. epsilon-recurrence theorems for finite quantum systems.

No function in this module turns an unidentified theoretical assumption into a
measured probability.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext
import json
import math
from pathlib import Path
from typing import Dict, Iterable, Mapping, Sequence, Tuple

import numpy as np
import pandas as pd

# SI constants (CODATA exact/standard values where applicable)
C = 299_792_458.0
G = 6.67430e-11
HBAR = 1.054_571_817e-34
MPC_M = 3.085_677_581_491_367_3e22
YEAR_S = 365.25 * 24 * 3600
PLANCK_LENGTH = math.sqrt(HBAR * G / C**3)


@dataclass(frozen=True)
class CosmologyPoint:
    """Minimal late-time flat-Lambda cosmology point."""

    H0: float  # km s^-1 Mpc^-1
    omega_m: float
    omega_lambda: float | None = None

    @property
    def omega_l(self) -> float:
        return (1.0 - self.omega_m) if self.omega_lambda is None else self.omega_lambda


def load_config(path: str | Path) -> dict:
    """Load the authoritative study configuration."""
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def hubble_si(H0: float) -> float:
    """Convert H0 from km s^-1 Mpc^-1 to s^-1."""
    if H0 <= 0:
        raise ValueError("H0 must be positive")
    return H0 * 1000.0 / MPC_M


def de_sitter_metrics(point: CosmologyPoint) -> Dict[str, float]:
    """Asymptotic flat-Lambda de Sitter horizon and thermodynamic scale.

    The returned recurrence quantity is intentionally named
    ``log10_t_thermo_rec_years``.  It is the conventional entropy-exponential
    thermodynamic/Poincare scale H_Lambda^-1 exp(S_dS/k_B), not a calculated
    epsilon-recurrence time for the observed universe.
    """
    if not (0.0 < point.omega_l < 1.5):
        raise ValueError("omega_lambda must lie in (0, 1.5) for this calculation")
    H_l = hubble_si(point.H0) * math.sqrt(point.omega_l)
    horizon_years = (1.0 / H_l) / YEAR_S
    radius_m = C / H_l
    s_over_k = math.pi * radius_m**2 / PLANCK_LENGTH**2
    log10_t = math.log10(horizon_years) + s_over_k / math.log(10.0)
    return {
        "H_lambda_s^-1": H_l,
        "horizon_time_Gyr": horizon_years / 1e9,
        "horizon_radius_m": radius_m,
        "S_dS_over_kB": s_over_k,
        "log10_t_thermo_rec_years": log10_t,
        "log10log10_t_thermo_rec_years": math.log10(log10_t),
    }


def de_sitter_metrics_frame(samples: pd.DataFrame) -> pd.DataFrame:
    """Vectorized de Sitter propagation for columns H0 and omega_m."""
    required = {"H0", "omega_m"}
    missing = required - set(samples.columns)
    if missing:
        raise ValueError(f"Missing posterior columns: {sorted(missing)}")

    df = samples.copy()
    H0 = df["H0"].to_numpy(dtype=float)
    om = df["omega_m"].to_numpy(dtype=float)
    mask = np.isfinite(H0) & np.isfinite(om) & (H0 > 0) & (om > 0) & (om < 1)
    df = df.loc[mask].reset_index(drop=True)
    H0 = df["H0"].to_numpy(dtype=float)
    om = df["omega_m"].to_numpy(dtype=float)
    ol = 1.0 - om
    H_l = (H0 * 1000.0 / MPC_M) * np.sqrt(ol)
    horizon_years = (1.0 / H_l) / YEAR_S
    radius_m = C / H_l
    s_over_k = np.pi * radius_m**2 / PLANCK_LENGTH**2
    log10_t = np.log10(horizon_years) + s_over_k / np.log(10.0)

    df["omega_lambda"] = ol
    df["H_lambda_s^-1"] = H_l
    df["horizon_time_Gyr"] = horizon_years / 1e9
    df["horizon_radius_m"] = radius_m
    df["S_dS_over_kB"] = s_over_k
    df["log10_t_thermo_rec_years"] = log10_t
    df["log10log10_t_thermo_rec_years"] = np.log10(log10_t)
    return df


def big_rip_remaining_gyr(w: float, point: CosmologyPoint) -> float:
    """Late-time constant-w phantom approximation.

    dt ~= 2/[3 |1+w| H0 sqrt(Omega_DE)].  This is a scenario calculation, not
    an extrapolation of a w0-wa fit to infinite scale factor.
    """
    if w >= -1.0:
        return math.inf
    H0_s = hubble_si(point.H0)
    seconds = 2.0 / (3.0 * abs(1.0 + w) * H0_s * math.sqrt(point.omega_l))
    return seconds / YEAR_S / 1e9


def recurrence_before_decay_from_logs(
    log10_t_rec_years: float, log10_tau_decay_years: float
) -> Tuple[float, float]:
    """Probability for recurrence before decay under constant competing hazards."""
    d = log10_t_rec_years - log10_tau_decay_years
    if d > 300:
        return 0.0, -d
    if d < -300:
        return 1.0, 0.0
    p = 1.0 / (1.0 + 10.0**d)
    return p, math.log10(p)


def log10_poisson_event_probability(log10_T: float, log10_mean_wait: float) -> float:
    """Stable log10[1-exp(-T/tau)] for representable log-ratios."""
    delta = log10_T - log10_mean_wait
    if delta > 3:
        return 0.0
    if delta < -6:
        return delta
    x = 10.0**delta
    return math.log10(-math.expm1(-x))


def finite_horizon_rare_event_table(
    log10_horizons_years: Sequence[float | str], log10_mean_wait_years: float
) -> pd.DataFrame:
    """Preserve tiny finite-horizon corrections with Decimal arithmetic.

    In the regime T << mean wait, log10 P ~= log10(T) - log10(mean wait).
    Storing the subtraction as a high-precision decimal avoids the false visual
    impression that every horizon has exactly the same probability.
    """
    rows = []
    with localcontext() as ctx:
        ctx.prec = 180
        mean_d = Decimal(str(log10_mean_wait_years))
        for raw in log10_horizons_years:
            L = Decimal(str(raw))
            delta = L - mean_d
            frac = L / mean_d
            rows.append(
                {
                    "log10_horizon_years": str(L),
                    "log10_mean_thermo_wait_years": str(mean_d),
                    "rare_event_log10P_approx": format(delta, "E"),
                    "horizon_exponent_fraction": format(frac, "E"),
                    "interpretation": "P ~= T/t_thermo for T << t_thermo",
                }
            )
    return pd.DataFrame(rows)


def desi_dr2_gaussian_samples(
    n: int,
    seed: int,
    H0_mean: float,
    H0_sd: float,
    omega_m_mean: float,
    omega_m_sd: float,
    correlation: float,
) -> pd.DataFrame:
    """Correlated Gaussian cross-check to the DESI DR2 flat-Lambda posterior."""
    if n <= 0:
        raise ValueError("n must be positive")
    if not -1 <= correlation <= 1:
        raise ValueError("correlation must lie in [-1,1]")
    mean = np.array([H0_mean, omega_m_mean], dtype=float)
    cov = np.array(
        [
            [H0_sd**2, correlation * H0_sd * omega_m_sd],
            [correlation * H0_sd * omega_m_sd, omega_m_sd**2],
        ]
    )
    rng = np.random.default_rng(seed)
    x = rng.multivariate_normal(mean, cov, size=n)
    df = pd.DataFrame(x, columns=["H0", "omega_m"])
    df["weight"] = 1.0
    return df[(df.H0 > 0) & (df.omega_m > 0) & (df.omega_m < 1)].reset_index(drop=True)


def load_projected_posterior(path: str | Path) -> pd.DataFrame:
    """Load a compact posterior projection with H0, omega_m, and optional weight."""
    df = pd.read_csv(path)
    required = {"H0", "omega_m"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Posterior projection is missing {sorted(missing)}")
    if "weight" not in df.columns:
        df["weight"] = 1.0
    df = df.dropna(subset=["H0", "omega_m", "weight"]).copy()
    df = df[(df.H0 > 0) & (df.omega_m > 0) & (df.omega_m < 1) & (df.weight > 0)]
    return df.reset_index(drop=True)


def load_desi_cobaya_chain(path: str | Path) -> pd.DataFrame:
    """Read a DESI/Cobaya ASCII chain and project it to weight, H0, omega_m."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        header = f.readline().strip().lstrip("#").split()
    df = pd.read_csv(path, sep=r"\s+", comment="#", header=None, names=header)
    needed = {"weight", "H0", "omegam"}
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"DESI chain is missing columns {sorted(missing)}")
    return df[["weight", "H0", "omegam"]].rename(columns={"omegam": "omega_m"})


def weighted_quantile(values: Sequence[float], weights: Sequence[float], q: Sequence[float]) -> np.ndarray:
    """Weighted quantiles using a midpoint empirical CDF."""
    v = np.asarray(values, dtype=float)
    w = np.asarray(weights, dtype=float)
    qs = np.asarray(q, dtype=float)
    if v.size == 0 or v.size != w.size:
        raise ValueError("values and weights must have equal nonzero length")
    if np.any(w < 0) or not np.any(w > 0):
        raise ValueError("weights must be nonnegative with positive total")
    if np.any((qs < 0) | (qs > 1)):
        raise ValueError("quantiles must lie in [0,1]")
    order = np.argsort(v)
    v = v[order]
    w = w[order]
    cdf = (np.cumsum(w) - 0.5 * w) / np.sum(w)
    return np.interp(qs, cdf, v)


def summarize_posterior(
    df: pd.DataFrame,
    cols: Iterable[str],
    weight_col: str = "weight",
) -> pd.DataFrame:
    """Weighted posterior summary for selected quantities."""
    if weight_col not in df.columns:
        weights = np.ones(len(df), dtype=float)
    else:
        weights = df[weight_col].to_numpy(dtype=float)
    rows = []
    for col in cols:
        vals = df[col].to_numpy(dtype=float)
        q025, med, q975 = weighted_quantile(vals, weights, [0.025, 0.5, 0.975])
        mean = float(np.average(vals, weights=weights))
        sd = float(math.sqrt(np.average((vals - mean) ** 2, weights=weights)))
        rows.append(
            {
                "quantity": col,
                "q2.5": q025,
                "median": med,
                "q97.5": q975,
                "mean": mean,
                "sd": sd,
            }
        )
    return pd.DataFrame(rows)


def quantum_uniform_recurrence_bound_log10_seconds(
    epsilon: float, distinct_energy_levels: int, energy_span_joule: float
) -> float:
    """Gupta-Short continuous-time uniform epsilon-recurrence upper bound.

    Their theorem sets hbar=1.  Restoring SI units gives

      t_r <= 2*pi*hbar/DeltaE * (2*ceil(pi/epsilon))^(d-2),

    for a finite discrete spectrum with d>=2 distinct energies and 0<epsilon<1.
    This theorem cannot be numerically applied to a cosmological causal patch
    until an appropriate finite Hamiltonian spectrum and energy span are given.
    """
    if not 0.0 < epsilon < 1.0:
        raise ValueError("epsilon must lie in (0,1)")
    if distinct_energy_levels < 2:
        raise ValueError("distinct_energy_levels must be >= 2")
    if energy_span_joule <= 0:
        raise ValueError("energy_span_joule must be positive")
    base = 2 * math.ceil(math.pi / epsilon)
    return (
        math.log10(2 * math.pi * HBAR / energy_span_joule)
        + (distinct_energy_levels - 2) * math.log10(base)
    )


def quantum_epsilon_requirements_table(epsilons: Iterable[float]) -> pd.DataFrame:
    """Declare the epsilon-recurrence target without inventing cosmological inputs."""
    rows = []
    for eps in epsilons:
        if not 0.0 < eps < 1.0:
            raise ValueError("all epsilon values must lie in (0,1)")
        rows.append(
            {
                "target": "finite-system uniform quantum near recurrence",
                "metric": "trace distance",
                "epsilon": eps,
                "required_spectrum": "finite discrete spectrum",
                "required_inputs": "distinct energy count d; energy span E_max-E_min",
                "cosmological_value": "not identified",
                "status": "theorem available; cosmological inputs unavailable",
            }
        )
    return pd.DataFrame(rows)


def identified_interval(
    weights: Mapping[str, float], branch_probability_bounds: Mapping[str, Tuple[float, float]]
) -> Tuple[float, float]:
    """Weighted probability interval under explicitly supplied theoretical weights."""
    total = float(sum(weights.values()))
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"Scenario weights sum to {total}, expected 1")
    lo = hi = 0.0
    for branch, weight in weights.items():
        if branch not in branch_probability_bounds:
            raise KeyError(f"No probability bound declared for branch {branch}")
        b0, b1 = branch_probability_bounds[branch]
        if not (0.0 <= b0 <= b1 <= 1.0):
            raise ValueError(f"Invalid probability bounds for {branch}: {(b0, b1)}")
        lo += weight * b0
        hi += weight * b1
    return lo, hi


def model_agnostic_probability_bound() -> Tuple[float, float]:
    """Partial-identification bound when far-future model/theory probabilities are free.

    A returned [0,1] interval is a non-identifiability result, not an informative
    probability estimate or a uniform belief distribution.
    """
    return 0.0, 1.0


def branch_bounds(p_recurrent_patch_given_eternal_ds: float) -> Dict[str, Tuple[float, float]]:
    """Branch recurrence bounds for a declared theoretical support parameter.

    ``p_recurrent_patch_given_eternal_ds`` is not observationally measured.  It
    encodes prior support for the finite/effectively closed recurrent-patch
    assumptions conditional on an eternal de Sitter cosmological future.
    """
    q = p_recurrent_patch_given_eternal_ds
    if not 0.0 <= q <= 1.0:
        raise ValueError("p_recurrent_patch_given_eternal_ds must lie in [0,1]")
    return {
        "eternal_ds": (q, q),
        "metastable_ds": (0.0, q),
        "fading_de": (0.0, 1.0),
        "finite_end": (0.0, 1.0),
        "cyclic": (0.0, 1.0),
    }


def prior_conditioned_sensitivity_table(prior_sets: Mapping[str, Mapping]) -> pd.DataFrame:
    """Evaluate explicitly theoretical prior scenarios; never label them observations."""
    rows = []
    for name, spec in prior_sets.items():
        q = float(spec["p_recurrent_patch_given_eternal_ds"])
        weights = {k: float(v) for k, v in spec["weights"].items()}
        lo, hi = identified_interval(weights, branch_bounds(q))
        rows.append(
            {
                "prior_set": name,
                "p_recurrent_patch_given_eternal_ds": q,
                "conditional_lower_bound": lo,
                "conditional_upper_bound": hi,
                "width": hi - lo,
                "status": "theoretical prior sensitivity; not an observational posterior",
            }
        )
    return pd.DataFrame(rows)


def entropy_deficit_ansatz(s_total: float, fractions: Iterable[float]) -> pd.DataFrame:
    """Illustrative thermodynamic ansatz t ~ H^-1 exp(Delta S), Delta S=f*S.

    This is a visualization of an assumed scaling relation.  It is not evidence
    for that relation and is not a mapping from trace-distance epsilon to entropy.
    """
    rows = []
    for f in fractions:
        f = float(f)
        if not 0.0 < f <= 1.0:
            raise ValueError("entropy-deficit fractions must lie in (0,1]")
        delta_s = f * s_total
        log10_wait_factor = delta_s / math.log(10.0)
        rows.append(
            {
                "fraction_of_full_entropy_deficit": f,
                "DeltaS_nats": delta_s,
                "log10_wait_factor": log10_wait_factor,
                "log10log10_wait_factor": math.log10(log10_wait_factor),
                "status": "illustrative ansatz; not an epsilon-recurrence calculation",
            }
        )
    return pd.DataFrame(rows)


def bayesian_two_model_weights(
    ln_bayes_factor_dynamic_vs_lcdm: float,
    ln_bayes_factor_sigma: float = 0.0,
    prior_odds_dynamic_to_lcdm: float = 1.0,
) -> Dict[str, float]:
    """Convert a two-model Bayes factor into normalized posterior model weights.

    The Bayes factor is B = Z_dynamic / Z_LCDM.  ``prior_odds`` is
    P(dynamic)/P(LCDM).  The +/- values propagate only the stated numerical
    uncertainty on ln B; they are not a complete systematic/model uncertainty.
    """
    if ln_bayes_factor_sigma < 0:
        raise ValueError("ln_bayes_factor_sigma must be non-negative")
    if prior_odds_dynamic_to_lcdm <= 0:
        raise ValueError("prior_odds_dynamic_to_lcdm must be positive")

    def p_dynamic(lnb: float) -> float:
        log_odds = math.log(prior_odds_dynamic_to_lcdm) + float(lnb)
        # Numerically stable logistic.
        if log_odds >= 0:
            z = math.exp(-log_odds)
            return 1.0 / (1.0 + z)
        z = math.exp(log_odds)
        return z / (1.0 + z)

    p = p_dynamic(ln_bayes_factor_dynamic_vs_lcdm)
    p_lo = p_dynamic(ln_bayes_factor_dynamic_vs_lcdm - ln_bayes_factor_sigma)
    p_hi = p_dynamic(ln_bayes_factor_dynamic_vs_lcdm + ln_bayes_factor_sigma)
    return {
        "p_dynamic": p,
        "p_lcdm": 1.0 - p,
        "p_dynamic_minus_sigma_lnB": p_lo,
        "p_dynamic_plus_sigma_lnB": p_hi,
        "p_lcdm_minus_sigma_lnB": 1.0 - p_hi,
        "p_lcdm_plus_sigma_lnB": 1.0 - p_lo,
    }


def model_evidence_comparison_table(
    comparisons: Sequence[Mapping], prior_odds_dynamic_to_lcdm: float = 1.0
) -> pd.DataFrame:
    """Create a transparent probability-like model-weight table from published ln B values."""
    rows = []
    for item in comparisons:
        w = bayesian_two_model_weights(
            float(item["lnB_dynamic_vs_lcdm"]),
            float(item.get("sigma", 0.0)),
            prior_odds_dynamic_to_lcdm,
        )
        rows.append(
            {
                "dataset": item["label"],
                "lnB_dynamic_vs_lcdm": float(item["lnB_dynamic_vs_lcdm"]),
                "lnB_sigma": float(item.get("sigma", 0.0)),
                "prior_odds_dynamic_to_lcdm": prior_odds_dynamic_to_lcdm,
                "p_LambdaCDM": w["p_lcdm"],
                "p_dynamic_DE": w["p_dynamic"],
                "p_dynamic_minus_sigma_lnB": w["p_dynamic_minus_sigma_lnB"],
                "p_dynamic_plus_sigma_lnB": w["p_dynamic_plus_sigma_lnB"],
                "status": item.get("status", "comparison"),
                "interpretation": "posterior model weight within a two-model comparison; not an ultimate-fate probability",
            }
        )
    return pd.DataFrame(rows)


def fate_decomposition_table(
    p_lcdm: float,
    p_dynamic: float,
    sensitivity_sets: Mapping[str, Mapping],
) -> pd.DataFrame:
    """Decompose top-level model-family weight into explicit theoretical fate splits.

    The top-level weights may be data-informed.  The within-family splits are
    deliberately supplied sensitivity assumptions.  Output probabilities sum
    to one for every scenario and must not be mislabeled as data-only fate
    probabilities.
    """
    if not (0.0 <= p_lcdm <= 1.0 and 0.0 <= p_dynamic <= 1.0):
        raise ValueError("model weights must lie in [0,1]")
    if not math.isclose(p_lcdm + p_dynamic, 1.0, abs_tol=1e-10):
        raise ValueError("top-level model weights must sum to one")

    rows = []
    for scenario, spec in sensitivity_sets.items():
        lam = {k: float(v) for k, v in spec["lambda_family"].items()}
        dyn = {k: float(v) for k, v in spec["dynamic_family"].items()}
        if not math.isclose(sum(lam.values()), 1.0, abs_tol=1e-10):
            raise ValueError(f"lambda_family split for {scenario} must sum to one")
        if not math.isclose(sum(dyn.values()), 1.0, abs_tol=1e-10):
            raise ValueError(f"dynamic_family split for {scenario} must sum to one")
        if any(v < 0 or v > 1 for v in [*lam.values(), *dyn.values()]):
            raise ValueError(f"all fate split values for {scenario} must lie in [0,1]")

        fate_probs = {k: p_lcdm * v for k, v in lam.items()}
        fate_probs.update({k: p_dynamic * v for k, v in dyn.items()})
        if not math.isclose(sum(fate_probs.values()), 1.0, abs_tol=1e-10):
            raise AssertionError("fate decomposition failed normalization")
        for fate, prob in fate_probs.items():
            rows.append(
                {
                    "scenario": scenario,
                    "fate": fate,
                    "probability": prob,
                    "percent": 100.0 * prob,
                    "status": "data-informed top-level model weight + explicit theory split; not a measured fate probability",
                }
            )
    return pd.DataFrame(rows)

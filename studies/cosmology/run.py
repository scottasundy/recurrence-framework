#!/usr/bin/env python3
"""Reproduce the numerical outputs and figures for the cosmology study."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.model import (
    CosmologyPoint,
    bayesian_two_model_weights,
    big_rip_remaining_gyr,
    de_sitter_metrics,
    de_sitter_metrics_frame,
    desi_dr2_gaussian_samples,
    entropy_deficit_ansatz,
    fate_decomposition_table,
    finite_horizon_rare_event_table,
    load_config,
    load_projected_posterior,
    model_agnostic_probability_bound,
    model_evidence_comparison_table,
    prior_conditioned_sensitivity_table,
    quantum_epsilon_requirements_table,
    summarize_posterior,
)

ROOT = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", default=str(ROOT / "config.json"), help="authoritative JSON config")
    p.add_argument("--posterior", default=None, help="optional projected posterior CSV/CSV.GZ with H0, omega_m, weight")
    p.add_argument("--output-dir", default=str(ROOT / "outputs"))
    p.add_argument("--figure-dir", default=str(ROOT / "figures"))
    return p.parse_args()


def write_summary(df: pd.DataFrame, path: Path) -> None:
    cols = [
        "H0",
        "omega_m",
        "omega_lambda",
        "horizon_time_Gyr",
        "S_dS_over_kB",
        "log10_t_thermo_rec_years",
        "log10log10_t_thermo_rec_years",
    ]
    summarize_posterior(df, cols).to_csv(path, index=False)


def main() -> None:
    args = parse_args()
    cfg = load_config(args.config)
    out = Path(args.output_dir)
    figdir = Path(args.figure_dir)
    out.mkdir(parents=True, exist_ok=True)
    figdir.mkdir(parents=True, exist_ok=True)

    # 1) Declared CPS reference point.
    ref = cfg["cps_reference"]
    cps = CosmologyPoint(ref["H0"], ref["Omega_m"], ref["Omega_Lambda"])
    baseline = de_sitter_metrics(cps)
    pd.DataFrame([
        {
            "baseline": ref["label"],
            "status": ref["status"],
            **baseline,
        }
    ]).to_csv(out / "de-sitter-baseline.csv", index=False)

    # 2) Primary observational propagation: official DESI DR2 posterior projection.
    default_proj = ROOT / cfg["observational_posterior"]["primary"]["projection_file"]
    posterior_path = Path(args.posterior) if args.posterior else default_proj
    posterior = load_projected_posterior(posterior_path)
    prop = de_sitter_metrics_frame(posterior)
    write_summary(prop, out / "de-sitter-posterior.csv")

    # 3) Published Gaussian approximation retained only as a cross-check.
    g = cfg["observational_posterior"]["gaussian_crosscheck"]
    gs = desi_dr2_gaussian_samples(
        n=int(g["samples"]),
        seed=int(g["seed"]),
        H0_mean=float(g["H0_mean"]),
        H0_sd=float(g["H0_sd"]),
        omega_m_mean=float(g["Omega_m_mean"]),
        omega_m_sd=float(g["Omega_m_sd"]),
        correlation=float(g["correlation_H0_Omega_m"]),
    )
    gprop = de_sitter_metrics_frame(gs)
    write_summary(gprop, out / "gaussian-check.csv")

    # 4) Constant-w phantom endpoint scenarios.
    pd.DataFrame([
        {"w": float(w), "remaining_Gyr": big_rip_remaining_gyr(float(w), cps),
         "status": "constant-w phantom scenario; not a w0-wa far-future extrapolation"}
        for w in cfg["big_rip_constant_w_examples"]
    ]).to_csv(out / "big-rip.csv", index=False)

    # 5) Finite-horizon thermodynamic recurrence probability in the rare-event model.
    finite_horizon_rare_event_table(
        cfg["finite_horizon_log10_years"], baseline["log10_t_thermo_rec_years"]
    ).to_csv(out / "finite-horizon.csv", index=False)

    # 6) The fully model-agnostic probability statement and prior-conditioned sensitivity.
    lo, hi = model_agnostic_probability_bound()
    pd.DataFrame([{
        "lower_bound": lo,
        "upper_bound": hi,
        "status": "partial-identification / non-identifiability result",
        "interpretation": "full logical [0,1] range; not an informative probability estimate because far-future model/theory probabilities are not observationally identified",
    }]).to_csv(out / "probability-bound.csv", index=False)

    prior_sets = cfg["theoretical_prior_sensitivity"]["sets"]
    prior_conditioned_sensitivity_table(prior_sets).to_csv(
        out / "prior-sensitivity.csv", index=False
    )

    # 6a) Data-informed two-model Bayesian evidence layer.
    fate_cfg = cfg["fate_probability_layer"]
    base_cmp = fate_cfg["baseline_model_comparison"]
    model_weights = bayesian_two_model_weights(
        float(base_cmp["ln_bayes_factor_dynamic_vs_lcdm"]),
        float(base_cmp["ln_bayes_factor_sigma"]),
        float(base_cmp["model_prior_odds_dynamic_to_lcdm"]),
    )
    model_evidence_comparison_table(
        fate_cfg["comparison_model_evidence"],
        float(base_cmp["model_prior_odds_dynamic_to_lcdm"]),
    ).to_csv(out / "model-weights.csv", index=False)

    fate_decomposition_table(
        model_weights["p_lcdm"],
        model_weights["p_dynamic"],
        fate_cfg["fate_decomposition_sensitivity"]["sets"],
    ).to_csv(out / "fate-sensitivity.csv", index=False)

    # 7) Explicit epsilon-recurrence target declaration. No cosmological spectrum is invented.
    eps = cfg["recurrence_targets"]["quantum_near_recurrence"]["epsilons"]
    quantum_epsilon_requirements_table(eps).to_csv(
        out / "quantum-epsilon.csv", index=False
    )

    # 8) Illustrative entropy-deficit ansatz, clearly separated from epsilon recurrence.
    e = cfg["entropy_deficit_fraction_range"]
    fractions = np.logspace(float(e["log10_min"]), float(e["log10_max"]), int(e["points"]))
    ansatz = entropy_deficit_ansatz(baseline["S_dS_over_kB"], fractions)
    ansatz.to_csv(out / "entropy.csv", index=False)

    # Figures. Use official chain weights for the primary posterior plot.
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.hist(
        prop["log10log10_t_thermo_rec_years"],
        bins=60,
        weights=prop["weight"],
    )
    ax.ticklabel_format(useOffset=False, axis="x")
    ax.set_xlabel("log10(log10(t_thermo / yr))")
    ax.set_ylabel("Weighted posterior count")
    ax.set_title("DESI DR2 + CMB chain: conditional de Sitter thermodynamic scale")
    fig.tight_layout()
    fig.savefig(figdir / "de-sitter.png", dpi=180)
    plt.close(fig)

    br = pd.read_csv(out / "big-rip.csv")
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.plot(br["w"], br["remaining_Gyr"], marker="o")
    ax.set_xlabel("Constant phantom w")
    ax.set_ylabel("Approximate remaining lifetime (Gyr)")
    ax.set_title("Constant-w finite-lifetime scenarios")
    fig.tight_layout()
    fig.savefig(figdir / "big-rip.png", dpi=180)
    plt.close(fig)

    ps = pd.read_csv(out / "prior-sensitivity.csv")
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    x = np.arange(len(ps))
    mid = (ps.conditional_lower_bound + ps.conditional_upper_bound) / 2
    err = np.vstack([
        mid - ps.conditional_lower_bound,
        ps.conditional_upper_bound - mid,
    ])
    ax.errorbar(x, mid, yerr=err, fmt="o", capsize=5)
    ax.set_xticks(x, ps.prior_set)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Prior-conditioned P(recurrence) interval")
    ax.set_title("Theoretical prior sensitivity - not an observational posterior")
    fig.tight_layout()
    fig.savefig(figdir / "prior-intervals.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.plot(np.log10(ansatz["fraction_of_full_entropy_deficit"]), ansatz["log10log10_wait_factor"])
    ax.set_xlabel("log10(fraction of full entropy deficit)")
    ax.set_ylabel("log10(log10 waiting factor)")
    ax.set_title("Illustrative entropy-deficit ansatz (assumed scaling)")
    fig.tight_layout()
    fig.savefig(figdir / "entropy.png", dpi=180)
    plt.close(fig)


    mw = pd.read_csv(out / "model-weights.csv")
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    x = np.arange(len(mw))
    ax.bar(x - 0.18, mw["p_LambdaCDM"] * 100, width=0.36, label="LambdaCDM")
    ax.bar(x + 0.18, mw["p_dynamic_DE"] * 100, width=0.36, label="w0waCDM / dynamic DE")
    ax.set_xticks(x, ["DR2+CMB", "Corrected SN", "Original DES-SN5YR"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Equal-prior posterior model weight (%)")
    ax.set_title("Published Bayesian model-comparison sensitivity")
    ax.legend()
    fig.tight_layout()
    fig.savefig(figdir / "model-weights.png", dpi=180)
    plt.close(fig)

    fate = pd.read_csv(out / "fate-sensitivity.csv")
    pivot = fate.pivot(index="scenario", columns="fate", values="percent")
    preferred = [
        "stable_eternal_ds", "metastable_ds", "fading_dark_energy",
        "phantom_finite_end", "recollapse", "cyclic_or_bounce",
    ]
    pivot = pivot[[c for c in preferred if c in pivot.columns]]
    fig, ax = plt.subplots(figsize=(9.0, 5.0))
    left = np.zeros(len(pivot))
    for col in pivot.columns:
        vals = pivot[col].to_numpy()
        ax.barh(pivot.index, vals, left=left, label=col.replace("_", " "))
        left += vals
    ax.set_xlim(0, 100)
    ax.set_xlabel("Illustrative fate weight (%)")
    ax.set_title("Fate decomposition sensitivity: data-informed top layer + theory split")
    ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=8)
    fig.tight_layout()
    fig.savefig(figdir / "fate-sensitivity.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    # Machine-readable provenance for the run.
    def repo_relative(path: Path) -> str:
        try:
            return str(path.resolve().relative_to(ROOT.resolve()))
        except ValueError:
            return str(path)

    metadata = {
        "study_version": cfg["study_version"],
        "config": repo_relative(Path(args.config)),
        "posterior": repo_relative(posterior_path),
        "posterior_rows": int(len(posterior)),
        "posterior_weight": float(posterior["weight"].sum()),
        "primary_observational_input": cfg["observational_posterior"]["primary"]["source"],
        "fate_probability_layer": fate_cfg["status"],
        "probability_boundary": cfg["scientific_boundary"],
    }
    (out / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Cosmology outputs written to {out}")


if __name__ == "__main__":
    main()

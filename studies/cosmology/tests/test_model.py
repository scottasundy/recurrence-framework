import math
import numpy as np
import pandas as pd
import pytest

from src.model import (
    CosmologyPoint,
    PLANCK_LENGTH,
    bayesian_two_model_weights,
    big_rip_remaining_gyr,
    branch_bounds,
    de_sitter_metrics,
    de_sitter_metrics_frame,
    desi_dr2_gaussian_samples,
    entropy_deficit_ansatz,
    fate_decomposition_table,
    finite_horizon_rare_event_table,
    identified_interval,
    log10_poisson_event_probability,
    model_agnostic_probability_bound,
    model_evidence_comparison_table,
    prior_conditioned_sensitivity_table,
    quantum_uniform_recurrence_bound_log10_seconds,
    recurrence_before_decay_from_logs,
    summarize_posterior,
    weighted_quantile,
)


def test_planck_length_order():
    assert 1.61e-35 < PLANCK_LENGTH < 1.62e-35


def test_cps_baseline_entropy_and_scale():
    m = de_sitter_metrics(CosmologyPoint(68.11, 0.3042, 0.6958))
    assert 3.1e122 < m["S_dS_over_kB"] < 3.3e122
    assert 122.13 < m["log10log10_t_thermo_rec_years"] < 122.16


def test_cps_baseline_horizon_time():
    m = de_sitter_metrics(CosmologyPoint(68.11, 0.3042, 0.6958))
    assert 17.20 < m["horizon_time_Gyr"] < 17.22


def test_de_sitter_rejects_nonpositive_h0():
    with pytest.raises(ValueError):
        de_sitter_metrics(CosmologyPoint(0.0, 0.3, 0.7))


def test_de_sitter_rejects_bad_lambda():
    with pytest.raises(ValueError):
        de_sitter_metrics(CosmologyPoint(68.0, 0.3, -0.1))


def test_vectorized_matches_scalar():
    p = CosmologyPoint(68.11, 0.3042, 0.6958)
    scalar = de_sitter_metrics(p)
    df = de_sitter_metrics_frame(pd.DataFrame({"H0": [p.H0], "omega_m": [p.omega_m], "weight": [1]}))
    for k in ["horizon_time_Gyr", "S_dS_over_kB", "log10_t_thermo_rec_years"]:
        assert math.isclose(float(df.iloc[0][k]), scalar[k], rel_tol=1e-12)


def test_big_rip_ordering():
    p = CosmologyPoint(68.11, 0.3042, 0.6958)
    assert big_rip_remaining_gyr(-1.20, p) < big_rip_remaining_gyr(-1.10, p) < big_rip_remaining_gyr(-1.05, p)


def test_big_rip_nonphantom_is_infinite():
    p = CosmologyPoint(68.11, 0.3042, 0.6958)
    assert math.isinf(big_rip_remaining_gyr(-1.0, p))


def test_poisson_small_ratio():
    assert math.isclose(log10_poisson_event_probability(2, 10), -8.0)


def test_poisson_large_ratio_saturates():
    assert log10_poisson_event_probability(20, 10) == 0.0


def test_finite_horizon_preserves_decimal_difference():
    df = finite_horizon_rare_event_table([10, 100], 1.3846841456061986e122)
    assert df.loc[0, "rare_event_log10P_approx"] != df.loc[1, "rare_event_log10P_approx"]
    assert "E+122" in df.loc[0, "rare_event_log10P_approx"]


def test_competing_hazards_equal_scales():
    p, logp = recurrence_before_decay_from_logs(100.0, 100.0)
    assert math.isclose(p, 0.5)
    assert math.isclose(logp, math.log10(0.5))


def test_competing_hazards_extreme():
    p, logp = recurrence_before_decay_from_logs(500.0, 100.0)
    assert p == 0.0
    assert logp == -400.0


def test_weighted_quantile_simple():
    q = weighted_quantile([0, 10], [1, 1], [0.5])
    assert math.isclose(float(q[0]), 5.0)


def test_weighted_quantile_respects_weight():
    q = weighted_quantile([0, 10], [99, 1], [0.5])
    assert float(q[0]) < 1.0


def test_weighted_summary_has_expected_columns():
    df = pd.DataFrame({"x": [1.0, 2.0, 3.0], "weight": [1, 2, 1]})
    out = summarize_posterior(df, ["x"])
    assert list(out.columns) == ["quantity", "q2.5", "median", "q97.5", "mean", "sd"]
    assert out.iloc[0]["quantity"] == "x"


def test_gaussian_sampler_reproducible():
    a = desi_dr2_gaussian_samples(20, 7, 68.17, 0.28, 0.3027, 0.0036, -0.975)
    b = desi_dr2_gaussian_samples(20, 7, 68.17, 0.28, 0.3027, 0.0036, -0.975)
    pd.testing.assert_frame_equal(a, b)


def test_gaussian_sampler_correlation_sign():
    df = desi_dr2_gaussian_samples(5000, 7, 68.17, 0.28, 0.3027, 0.0036, -0.975)
    assert df[["H0", "omega_m"]].corr().iloc[0, 1] < -0.9


def test_quantum_uniform_bound_d2_is_fundamental_period():
    span = 1.0e-20
    got = quantum_uniform_recurrence_bound_log10_seconds(0.1, 2, span)
    expected = math.log10(2 * math.pi * 1.054571817e-34 / span)
    assert math.isclose(got, expected, rel_tol=1e-12)


def test_quantum_uniform_bound_tightens_with_epsilon_only_for_d_gt_2():
    loose = quantum_uniform_recurrence_bound_log10_seconds(0.1, 5, 1e-20)
    tight = quantum_uniform_recurrence_bound_log10_seconds(0.01, 5, 1e-20)
    assert tight > loose


def test_quantum_uniform_bound_validates_inputs():
    with pytest.raises(ValueError):
        quantum_uniform_recurrence_bound_log10_seconds(0.0, 5, 1e-20)
    with pytest.raises(ValueError):
        quantum_uniform_recurrence_bound_log10_seconds(0.1, 1, 1e-20)
    with pytest.raises(ValueError):
        quantum_uniform_recurrence_bound_log10_seconds(0.1, 5, 0.0)


def test_model_agnostic_bound_is_full_unit_interval():
    assert model_agnostic_probability_bound() == (0.0, 1.0)


def test_branch_bounds():
    b = branch_bounds(0.5)
    assert b["eternal_ds"] == (0.5, 0.5)
    assert b["finite_end"] == (0.0, 1.0)
    assert b["cyclic"] == (0.0, 1.0)


def test_identified_interval_prior_conditioned_example():
    weights = {"eternal_ds": 0.2, "metastable_ds": 0.2, "fading_de": 0.2, "finite_end": 0.2, "cyclic": 0.2}
    lo, hi = identified_interval(weights, branch_bounds(0.5))
    assert math.isclose(lo, 0.1)
    assert math.isclose(hi, 0.8)


def test_identified_interval_rejects_bad_weights():
    with pytest.raises(ValueError):
        identified_interval({"finite_end": 0.9}, branch_bounds(0.5))


def test_prior_conditioned_table_label():
    priors = {"x": {"weights": {"eternal_ds": 1.0}, "p_recurrent_patch_given_eternal_ds": 0.4}}
    out = prior_conditioned_sensitivity_table(priors)
    assert out.iloc[0]["conditional_lower_bound"] == 0.4
    assert "not an observational posterior" in out.iloc[0]["status"]


def test_entropy_ansatz_is_linear_in_fraction_before_double_log():
    out = entropy_deficit_ansatz(100.0, [0.1, 0.2])
    ratio = out.iloc[1]["log10_wait_factor"] / out.iloc[0]["log10_wait_factor"]
    assert math.isclose(ratio, 2.0)


def test_bayesian_two_model_equal_prior_conversion():
    w = bayesian_two_model_weights(-0.57, 0.26, 1.0)
    assert 0.63 < w["p_lcdm"] < 0.65
    assert 0.35 < w["p_dynamic"] < 0.37
    assert w["p_dynamic_minus_sigma_lnB"] < w["p_dynamic"] < w["p_dynamic_plus_sigma_lnB"]


def test_model_evidence_table_normalizes():
    out = model_evidence_comparison_table([{
        "label": "x", "lnB_dynamic_vs_lcdm": 0.0, "sigma": 0.1, "status": "test"
    }])
    assert math.isclose(out.iloc[0].p_LambdaCDM + out.iloc[0].p_dynamic_DE, 1.0)


def test_fate_decomposition_normalizes_each_scenario():
    sets = {
        "x": {
            "lambda_family": {"stable_eternal_ds": 0.5, "metastable_ds": 0.5},
            "dynamic_family": {"fading_dark_energy": 0.25, "phantom_finite_end": 0.25, "recollapse": 0.25, "cyclic_or_bounce": 0.25},
        }
    }
    out = fate_decomposition_table(0.64, 0.36, sets)
    assert math.isclose(out.probability.sum(), 1.0)
    assert len(out) == 6


def test_fate_decomposition_rejects_bad_split():
    sets = {
        "x": {
            "lambda_family": {"stable_eternal_ds": 1.0},
            "dynamic_family": {"fading_dark_energy": 0.8},
        }
    }
    with pytest.raises(ValueError):
        fate_decomposition_table(0.5, 0.5, sets)

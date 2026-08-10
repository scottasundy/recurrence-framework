from pathlib import Path
import pandas as pd
import pytest

from src.model import load_config, load_desi_cobaya_chain, load_projected_posterior

ROOT = Path(__file__).resolve().parents[1]


def test_config_is_authoritative():
    cfg = load_config(ROOT / "config.json")
    assert cfg["study_version"] == "master"
    assert cfg["observational_posterior"]["primary"]["projection_file"].endswith(".csv.gz")


def test_desi_dovekie_v2_evidence_input_regression():
    cfg = load_config(ROOT / "config.json")
    rows = cfg["fate_probability_layer"]["comparison_model_evidence"]
    row = next(r for r in rows if "corrected DES-Dovekie" in r["label"])
    assert row["lnB_dynamic_vs_lcdm"] == pytest.approx(-0.01)
    assert row["sigma"] == pytest.approx(0.27)


def test_bundled_desi_projection_shape_and_weight():
    df = load_projected_posterior(ROOT / "data/desi-projection.csv.gz")
    assert len(df) == 59891
    assert int(df["weight"].sum()) == 169444
    assert {"H0", "omega_m", "weight"}.issubset(df.columns)


def test_projection_parameter_centers():
    df = load_projected_posterior(ROOT / "data/desi-projection.csv.gz")
    h0 = (df.H0 * df.weight).sum() / df.weight.sum()
    om = (df.omega_m * df.weight).sum() / df.weight.sum()
    assert 68.16 < h0 < 68.19
    assert 0.3025 < om < 0.3029


def test_projected_loader_adds_unit_weight(tmp_path):
    p = tmp_path / "p.csv"
    pd.DataFrame({"H0": [68.0], "omega_m": [0.3]}).to_csv(p, index=False)
    df = load_projected_posterior(p)
    assert df.iloc[0].weight == 1.0


def test_desi_chain_parser(tmp_path):
    p = tmp_path / "chain.txt"
    p.write_text("# weight H0 omegam junk\n1 68.0 0.3 5\n2 69.0 0.29 6\n", encoding="utf-8")
    df = load_desi_cobaya_chain(p)
    assert list(df.columns) == ["weight", "H0", "omega_m"]
    assert int(df.weight.sum()) == 3


def test_desi_chain_parser_rejects_missing_columns(tmp_path):
    p = tmp_path / "chain.txt"
    p.write_text("# weight H0 foo\n1 68.0 2\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_desi_cobaya_chain(p)

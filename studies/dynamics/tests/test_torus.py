from fractions import Fraction

from recurrence_dynamics.torus import (
    exact_positive_recurrence_for_sqrt2_flow,
    irrational_torus_return_error,
    rational_torus_exact_period,
    sqrt2_convergents,
)


def test_rational_torus_period():
    assert rational_torus_exact_period(Fraction(1, 3), Fraction(2, 5)) == 15


def test_sqrt2_flow_has_no_exact_positive_recurrence():
    assert exact_positive_recurrence_for_sqrt2_flow() is False


def test_convergents_improve_near_return():
    convergents = list(sqrt2_convergents(1_000_000))
    errors = [irrational_torus_return_error(x.denominator) for x in convergents]
    assert all(right < left for left, right in zip(errors, errors[1:]))
    assert convergents[-1] == Fraction(665857, 470832)

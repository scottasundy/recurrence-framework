from itertools import islice

from recurrence_dynamics.automaton import all_states, inverse_step, step
from recurrence_dynamics.finite_orbits import analyze_orbit, is_bijection


def test_binary_ca_inverse_exhaustive_size_three():
    states = tuple(all_states(3))
    assert is_bijection(step, states)
    for state in states:
        assert inverse_step(step(state)) == state
        assert step(inverse_step(state)) == state


def test_reference_orbit_period_is_eight():
    previous = (0,) * 8
    current = (0, 0, 0, 1, 0, 0, 0, 0)
    result = analyze_orbit(step, (previous, current))
    assert result.transient_length == 0
    assert result.period == 8

from itertools import combinations

from recurrence_dynamics.automaton import all_states, step as ca_step
from recurrence_dynamics.finite_orbits import (
    analyze_orbit,
    future_observations_equal,
    is_bijection,
    observation_is_closed,
    predictive_partition,
)
from recurrence_dynamics.hpp import (
    density,
    momentum,
    step as hpp_step,
)


def test_finite_deterministic_map_has_eventual_cycle():
    mapping = {0: 1, 1: 2, 2: 3, 3: 2}
    result = analyze_orbit(mapping.__getitem__, 0)
    assert result.transient_length == 2
    assert result.period == 2
    assert not result.begins_on_cycle


def test_finite_bijection_has_no_transient():
    mapping = {0: 1, 1: 2, 2: 0, 3: 3}
    assert is_bijection(mapping.__getitem__, mapping)
    for state in mapping:
        result = analyze_orbit(mapping.__getitem__, state)
        assert result.transient_length == 0


def test_observation_closure_and_predictive_refinement():
    mapping = {0: 1, 1: 0, 2: 3, 3: 2}
    observe = {0: "a", 1: "b", 2: "a", 3: "a"}.__getitem__
    assert not observation_is_closed(mapping.__getitem__, mapping, observe)

    result = predictive_partition(mapping.__getitem__, mapping, observe)
    assert result.class_counts == (2, 3, 3)
    assert not result.is_state_reconstructing


def test_two_consecutive_ca_snapshots_reconstruct_complete_state():
    for size in range(2, 9):
        states = tuple(all_states(size))
        assert not observation_is_closed(ca_step, states, lambda state: state[1])
        result = predictive_partition(ca_step, states, lambda state: state[1])
        assert result.class_counts == (2**size, 2 ** (2 * size), 2 ** (2 * size))
        assert result.refinement_depth == 2
        assert result.is_state_reconstructing


def _four_particle_zero_momentum_states():
    states = []
    for occupied_channels in combinations(range(36), 4):
        cells = [0] * 9
        for channel in occupied_channels:
            cells[channel // 4] |= 1 << (channel % 4)
        state = tuple(cells)
        if momentum(state) == (0, 0):
            states.append(state)
    return tuple(states)


def test_density_future_does_not_reconstruct_hpp_microstate():
    states = _four_particle_zero_momentum_states()
    assert len(states) == 9153
    result = predictive_partition(
        lambda state: hpp_step(state, 3, 3),
        states,
        density,
    )
    assert result.class_counts == (495, 6948, 9090, 9126, 9126)
    class_sizes = sorted(len(group) for group in result.classes().values())
    assert class_sizes.count(1) == 9099
    assert class_sizes.count(2) == 27
    assert not result.is_state_reconstructing

    ambiguous_groups = [
        group for group in result.classes().values() if len(group) == 2
    ]
    assert len(ambiguous_groups) == 27
    assert sum(len(group) for group in ambiguous_groups) == 54

    representative_a = (1, 2, 0, 8, 4, 0, 0, 0, 0)
    representative_b = (8, 1, 0, 4, 2, 0, 0, 0, 0)
    assert representative_a != representative_b
    assert momentum(representative_a) == momentum(representative_b) == (0, 0)
    assert future_observations_equal(result, representative_a, representative_b)

    state_a = representative_a
    state_b = representative_b
    for _ in range(12):
        assert density(state_a) == density(state_b)
        state_a = hpp_step(state_a, 3, 3)
        state_b = hpp_step(state_b, 3, 3)
    assert state_a == representative_a
    assert state_b == representative_b

from itertools import product

from recurrence_dynamics.hpp import (
    collide,
    collide_cell,
    decode_state,
    density,
    encode_state,
    inverse_step,
    momentum,
    particle_number,
    reverse_velocities,
    state_from_hex,
    state_hex,
    step,
    stream,
    time_reverse_state,
)


def test_all_local_collision_masks_are_involutions():
    for mask in range(16):
        assert collide_cell(collide_cell(mask)) == mask


def test_streaming_moves_each_velocity_channel_one_periodic_site():
    width = height = 3
    cases = {
        1: (6, 1),
        2: (1, 2),
        4: (3, 4),
        8: (2, 8),
    }
    for direction, (destination, expected_mask) in cases.items():
        state = (direction,) + (0,) * 8
        following = stream(state, width, height)
        assert following[destination] == expected_mask
        assert sum(mask.bit_count() for mask in following) == 1


def test_global_inverse_and_conservation_on_small_lattice():
    width = height = 2
    for state in product(range(16), repeat=width * height):
        following = step(state, width, height)
        assert inverse_step(following, width, height) == state
        assert particle_number(following) == particle_number(state)
        assert momentum(following) == momentum(state)


def test_velocity_reversal_is_an_involution_and_preserves_density():
    state = (1, 2, 4, 8, 3, 12, 5, 10, 15)
    reversed_state = reverse_velocities(state)
    assert reverse_velocities(reversed_state) == state
    assert density(reversed_state) == density(state)


def test_hpp_time_reversal_conjugates_update_to_inverse():
    width = height = 2
    for state in product(range(16), repeat=width * height):
        reversed_state = time_reverse_state(state)
        assert time_reverse_state(reversed_state) == state
        assert density(reversed_state) == density(state)
        assert time_reverse_state(step(reversed_state, width, height)) == inverse_step(
            state, width, height
        )


def test_state_encoding_and_decoding_round_trip():
    state = (1, 2, 4, 8, 3, 12, 5, 10, 15)
    code = encode_state(state, 3, 3)
    assert decode_state(code, 3, 3) == state
    text = state_hex(state, 3, 3)
    assert len(text) == 9
    assert state_from_hex(text, 3, 3) == state


def test_collision_then_stream_convention_is_explicit():
    state = (0, 0, 0, 0, 10, 0, 0, 0, 0)
    assert step(state, 3, 3) == stream(collide(state), 3, 3)

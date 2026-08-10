from random import Random

from recurrence_dynamics.rotor import (
    Geometry,
    inverse_step,
    local_collision,
    particle_number,
    momentum,
    step,
)


def test_local_particle_rotor_collision_is_involutive():
    for mask in range(64):
        for rotor in (0, 1):
            out_mask, out_rotor = local_collision(mask, rotor)
            back_mask, back_rotor = local_collision(out_mask, out_rotor)
            assert (back_mask, back_rotor) == (mask, rotor)


def test_random_global_inverse_and_conservation():
    geometry = Geometry(4)
    rng = Random(12345)
    for _ in range(100):
        boards = tuple(
            rng.getrandbits(geometry.cells) & geometry.full_mask
            for _ in range(6)
        )
        rotor = rng.getrandbits(geometry.cells) & geometry.full_mask
        state = boards + (rotor,)
        following = step(state, geometry)
        assert inverse_step(following, geometry) == state
        assert particle_number(following) == particle_number(state)
        assert momentum(following) == momentum(state)

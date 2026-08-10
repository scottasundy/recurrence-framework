from fractions import Fraction

from recurrence_dynamics.elastic_ring import (
    RingState,
    advance,
    kinetic_energy,
    momentum,
    time_reverse,
)


def initial_state():
    return RingState(
        positions=(
            Fraction(1, 20),
            Fraction(7, 20),
            Fraction(13, 20),
            Fraction(17, 20),
        ),
        velocities=(
            Fraction(3, 5),
            Fraction(-1, 5),
            Fraction(2, 5),
            Fraction(-2, 5),
        ),
    )


def test_exact_period_ten():
    initial = initial_state()
    final, collisions = advance(initial, Fraction(10))
    assert final == initial
    assert collisions == 36


def test_time_reversal():
    initial = initial_state()
    duration = Fraction(37, 20)
    forward, _ = advance(initial, duration)
    backward_start = time_reverse(forward)
    backward, _ = advance(backward_start, duration)
    restored = time_reverse(backward)
    assert restored == initial
    assert momentum(restored) == momentum(initial)
    assert kinetic_energy(restored) == kinetic_energy(initial)

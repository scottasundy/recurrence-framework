"""Exact event-driven equal-mass hard particles on a unit ring."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Tuple

RING_LENGTH = Fraction(1)


@dataclass(frozen=True)
class RingState:
    """
    Labels remain in a fixed cyclic order around the ring.

    positions[i] is the coordinate of labeled particle i modulo one.
    velocities[i] is its signed velocity.
    """
    positions: Tuple[Fraction, ...]
    velocities: Tuple[Fraction, ...]


def validate_state(state: RingState) -> None:
    assert isinstance(state, RingState)
    assert len(state.positions) == len(state.velocities) >= 3
    assert all(isinstance(value, Fraction) for value in state.positions)
    assert all(isinstance(value, Fraction) for value in state.velocities)
    assert all(Fraction(0) <= x < RING_LENGTH for x in state.positions)


def momentum(state: RingState) -> Fraction:
    return sum(state.velocities, Fraction(0))


def kinetic_energy(state: RingState) -> Fraction:
    return sum(
        (velocity * velocity) / 2
        for velocity in state.velocities
    )


def time_reverse(state: RingState) -> RingState:
    return RingState(
        positions=state.positions,
        velocities=tuple(-velocity for velocity in state.velocities),
    )


def advance(
    initial: RingState,
    duration: Fraction,
) -> Tuple[RingState, int]:
    """
    Exact event-driven evolution.

    Adjacent labeled particles cannot pass through one another. At a
    collision they exchange velocities, preserving their cyclic order.

    Simultaneous disjoint collisions are handled. A shared-particle
    simultaneous collision is rejected because hard point particles do
    not define a unique generic three-body collision without an added
    convention. The selected test states never trigger that case.
    """
    validate_state(initial)
    assert duration >= 0

    positions = list(initial.positions)
    velocities = list(initial.velocities)
    particle_count = len(positions)
    remaining = duration
    collision_events = 0

    initial_momentum = momentum(initial)
    initial_energy = kinetic_energy(initial)

    while remaining > 0:
        candidates: List[Tuple[Fraction, int, int]] = []

        for first in range(particle_count):
            second = (first + 1) % particle_count
            separation = (
                positions[second] - positions[first]
            ) % RING_LENGTH
            closing_speed = velocities[first] - velocities[second]

            if closing_speed <= 0:
                continue

            if separation == 0:
                raise RuntimeError(
                    "Ambiguous immediate shared-position collision."
                )

            candidates.append(
                (
                    separation / closing_speed,
                    first,
                    second,
                )
            )

        if not candidates:
            for index in range(particle_count):
                positions[index] = (
                    positions[index] + velocities[index] * remaining
                ) % RING_LENGTH
            remaining = Fraction(0)
            break

        next_collision_time = min(
            candidate[0] for candidate in candidates
        )

        if next_collision_time > remaining:
            for index in range(particle_count):
                positions[index] = (
                    positions[index] + velocities[index] * remaining
                ) % RING_LENGTH
            remaining = Fraction(0)
            break

        for index in range(particle_count):
            positions[index] = (
                positions[index]
                + velocities[index] * next_collision_time
            ) % RING_LENGTH

        remaining -= next_collision_time

        simultaneous = [
            (first, second)
            for collision_time, first, second in candidates
            if collision_time == next_collision_time
        ]

        involved = [
            particle
            for pair in simultaneous
            for particle in pair
        ]
        if len(involved) != len(set(involved)):
            raise RuntimeError(
                "Shared-particle simultaneous collision encountered."
            )

        old_velocities = velocities.copy()
        for first, second in simultaneous:
            velocities[first] = old_velocities[second]
            velocities[second] = old_velocities[first]

        collision_events += len(simultaneous)

        current = RingState(
            tuple(positions),
            tuple(velocities),
        )
        assert momentum(current) == initial_momentum
        assert kinetic_energy(current) == initial_energy

    result = RingState(tuple(positions), tuple(velocities))
    validate_state(result)
    assert momentum(result) == initial_momentum
    assert kinetic_energy(result) == initial_energy
    return result, collision_events


def sample_orbit(
    initial: RingState,
    time_step: Fraction,
    number_of_steps: int,
) -> Tuple[Tuple[RingState, ...], int]:
    states = [initial]
    state = initial
    collisions = 0

    for _ in range(number_of_steps):
        state, step_collisions = advance(state, time_step)
        states.append(state)
        collisions += step_collisions

    return tuple(states), collisions


def first_sampled_repeat(states: Tuple[RingState, ...]):
    seen: Dict[RingState, int] = {}

    for index, state in enumerate(states):
        if state in seen:
            first = seen[state]
            return first, index, index - first
        seen[state] = index

    return None


def torus_position_l1(
    first: RingState,
    second: RingState,
) -> Fraction:
    assert len(first.positions) == len(second.positions)

    total = Fraction(0)
    for left, right in zip(first.positions, second.positions):
        difference = abs(left - right) % RING_LENGTH
        total += min(difference, RING_LENGTH - difference)
    return total


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"

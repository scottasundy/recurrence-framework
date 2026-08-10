"""A reversible second-order binary cellular automaton on a ring."""

from __future__ import annotations

from itertools import product
from typing import Iterable

Bits = tuple[int, ...]
State = tuple[Bits, Bits]  # (x(t-1), x(t))


def validate_state(state: State) -> None:
    previous, current = state
    if len(previous) != len(current) or not previous:
        raise ValueError("Previous and current configurations must match.")
    if any(bit not in (0, 1) for config in state for bit in config):
        raise ValueError("Configurations must contain only zeroes and ones.")


def next_config(previous: Bits, current: Bits) -> Bits:
    """Compute x(t+1) from x(t-1) and x(t)."""
    if len(previous) != len(current) or not current:
        raise ValueError("Configurations must have equal positive length.")
    n = len(current)
    return tuple(
        previous[i] ^ current[(i - 1) % n] ^ current[(i + 1) % n]
        for i in range(n)
    )


def step(state: State) -> State:
    """F(x(t-1), x(t)) = (x(t), x(t+1))."""
    validate_state(state)
    previous, current = state
    return current, next_config(previous, current)


def inverse_step(state: State) -> State:
    """Exact inverse of :func:`step`."""
    validate_state(state)
    current, following = state
    n = len(current)
    previous = tuple(
        following[i] ^ current[(i - 1) % n] ^ current[(i + 1) % n]
        for i in range(n)
    )
    return previous, current


def all_states(size: int) -> Iterable[State]:
    """Enumerate the complete finite state space for a small ring."""
    if size <= 0:
        raise ValueError("size must be positive")
    configs = tuple(product((0, 1), repeat=size))
    for previous in configs:
        for current in configs:
            yield previous, current

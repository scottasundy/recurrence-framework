"""Finite deterministic dynamics and exact observable-state refinement.

The module separates complete-state recurrence from recurrence of a reduced
observation.  For a finite deterministic system, iterative partition
refinement computes the coarsest state description that determines the entire
future observation sequence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Hashable, Iterable, TypeVar

StateT = TypeVar("StateT", bound=Hashable)
ObservationT = TypeVar("ObservationT", bound=Hashable)


@dataclass(frozen=True)
class OrbitAnalysis(Generic[StateT]):
    """Description of the first repeated state along one orbit."""

    transient_length: int
    period: int
    first_repeat_time: int
    repeated_state: StateT
    history: tuple[StateT, ...]

    @property
    def begins_on_cycle(self) -> bool:
        return self.transient_length == 0


@dataclass(frozen=True)
class ObservationRefinement(Generic[StateT]):
    """Exact future-equivalence partition for a finite deterministic system.

    ``class_of`` maps every listed state to its stable predictive-equivalence
    class.  Two states share a class exactly when their complete future
    observation sequences are identical.  ``class_counts`` records the number
    of classes after observation words of lengths 1, 2, ... and includes the
    repeated terminal count that certifies stabilization.
    """

    states: tuple[StateT, ...]
    class_of: dict[StateT, int]
    class_counts: tuple[int, ...]

    @property
    def predictive_class_count(self) -> int:
        return self.class_counts[-1]

    @property
    def refinement_depth(self) -> int:
        """Smallest future-word length that reaches the stable partition."""
        return len(self.class_counts) - 1

    @property
    def is_state_reconstructing(self) -> bool:
        return self.predictive_class_count == len(self.states)

    def classes(self) -> dict[int, tuple[StateT, ...]]:
        grouped: dict[int, list[StateT]] = {}
        for state in self.states:
            grouped.setdefault(self.class_of[state], []).append(state)
        return {key: tuple(value) for key, value in grouped.items()}



def analyze_orbit(
    step: Callable[[StateT], StateT],
    initial: StateT,
    *,
    max_steps: int | None = None,
) -> OrbitAnalysis[StateT]:
    """Find the first repeated state of a deterministic orbit."""
    seen: dict[StateT, int] = {}
    history: list[StateT] = []
    state = initial
    time = 0

    while state not in seen:
        if max_steps is not None and time >= max_steps:
            raise RuntimeError(
                f"No recurrence encountered within max_steps={max_steps}."
            )
        seen[state] = time
        history.append(state)
        state = step(state)
        time += 1

    first = seen[state]
    return OrbitAnalysis(
        transient_length=first,
        period=time - first,
        first_repeat_time=time,
        repeated_state=state,
        history=tuple(history),
    )



def same_future_after_equal_state(
    step: Callable[[StateT], StateT],
    first: StateT,
    second: StateT,
    *,
    steps: int,
) -> bool:
    """Verify the finite-horizon consequence of equal complete states."""
    if first != second:
        raise ValueError("The theorem applies only when the states are equal.")

    left = first
    right = second
    for _ in range(steps + 1):
        if left != right:
            return False
        left = step(left)
        right = step(right)
    return True



def is_bijection(
    step: Callable[[StateT], StateT],
    states: Iterable[StateT],
) -> bool:
    """Check whether ``step`` is a permutation of an explicitly listed set."""
    domain = tuple(states)
    images = tuple(step(state) for state in domain)
    return len(set(images)) == len(domain) and set(images) == set(domain)



def observation_is_closed(
    step: Callable[[StateT], StateT],
    states: Iterable[StateT],
    observe: Callable[[StateT], ObservationT],
) -> bool:
    """Return whether the raw observation has an autonomous one-step update.

    Closure means that equal current observations always imply equal next
    observations.  Equivalently, there exists a deterministic map ``G`` on
    observed values satisfying ``observe(step(x)) == G(observe(x))`` on the
    listed state set.
    """
    next_by_observation: dict[ObservationT, ObservationT] = {}
    for state in states:
        current = observe(state)
        following = observe(step(state))
        previous = next_by_observation.setdefault(current, following)
        if previous != following:
            return False
    return True



def predictive_partition(
    step: Callable[[StateT], StateT],
    states: Iterable[StateT],
    observe: Callable[[StateT], ObservationT],
) -> ObservationRefinement[StateT]:
    """Compute exact equality of infinite future observation sequences.

    Start with the partition induced by the present observation.  At each
    refinement, split states according to the pair consisting of their present
    observation and the current class of their successor.  On a finite state
    set the process stabilizes.  The stable relation is exactly

    ``x ~ y`` iff ``observe(step**k(x)) == observe(step**k(y))`` for all
    nonnegative integers ``k``.

    The supplied state set must be forward-invariant under ``step``.
    """
    domain = tuple(states)
    if not domain:
        raise ValueError("states must be nonempty")
    if len(set(domain)) != len(domain):
        raise ValueError("states must not contain duplicates")

    index = {state: position for position, state in enumerate(domain)}
    successors: list[int] = []
    observations: list[ObservationT] = []
    for state in domain:
        following = step(state)
        if following not in index:
            raise ValueError("states must be forward-invariant under step")
        successors.append(index[following])
        observations.append(observe(state))

    def canonical_labels(keys: Iterable[Hashable]) -> list[int]:
        label_by_key: dict[Hashable, int] = {}
        labels: list[int] = []
        for key in keys:
            if key not in label_by_key:
                label_by_key[key] = len(label_by_key)
            labels.append(label_by_key[key])
        return labels

    labels = canonical_labels(observations)
    class_counts = [len(set(labels))]

    while True:
        refined = canonical_labels(
            (observations[i], labels[successors[i]])
            for i in range(len(domain))
        )
        class_counts.append(len(set(refined)))
        if refined == labels:
            break
        labels = refined

    return ObservationRefinement(
        states=domain,
        class_of={state: labels[i] for i, state in enumerate(domain)},
        class_counts=tuple(class_counts),
    )



def future_observations_equal(
    refinement: ObservationRefinement[StateT],
    first: StateT,
    second: StateT,
) -> bool:
    """Test equality of the complete future observation sequences."""
    return refinement.class_of[first] == refinement.class_of[second]

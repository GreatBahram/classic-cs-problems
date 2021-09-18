from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from math import exp
from random import paretovariate
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Optional,
    Protocol,
    Sequence,
    Type,
    TypeVar,
)

T = TypeVar("T")


def linear_contains(iterable: Iterable[T], key: T) -> bool:
    return key in iterable


C = TypeVar("C", bound="Comparable")


class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool:
        ...

    def __lt__(self: C, other: C) -> bool:
        ...

    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return not self < other


def binary_contains(sequence: Sequence[C], key: C) -> bool:
    low: int = 0
    high = len(sequence) - 1
    while low <= high:  # as long as there is search space
        mid: int = (low + high) // 2
        if sequence[mid] > key:
            high = mid - 1
        elif sequence[mid] < key:
            low = mid + 1
        else:
            return True
    return False


class Stack(Generic[T]):
    def __init__(self):
        self._container = []

    def push(self, item: T):
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    @property
    def empty(self) -> bool:
        return not self._container

    def __repr__(self) -> str:
        return repr(self._container)


@dataclass
class Node(Generic[T]):
    state: T
    parent: Optional[Node] = None
    cost: float = 0.0
    heuristic: float = 0.0

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def dfs(
    initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], list[T]]
) -> Optional[Node[T]]:
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))
    explored: set[T] = {initial}

    while not frontier.empty:
        current_node = frontier.pop()
        current_state = current_node.state

        if goal_test(current_state):
            return current_node

        for child in successors(current_state):
            if child in explored:
                continue
            frontier.push(Node(child, current_node))
            explored.add(child)
    return None


def node_to_path(node: Node[T]) -> list[T]:
    path: list[T] = [node.state]
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path


class Queue:
    def __init__(self) -> None:
        self._container: deque[T] = deque()

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.popleft()  # FIFO

    @property
    def empty(self) -> bool:
        return not self._container

    def __repr__(self) -> str:
        return repr(self._container)


def bfs(
    initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], list[T]]
) -> Optional[Node[T]]:
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    explored: set[T] = {initial}

    while not frontier.empty:
        current_node = frontier.pop()
        current_state = current_node.state

        if goal_test(current_state):
            return current_node

        for child in successors(current_state):
            if child in explored:
                continue
            frontier.push(Node(child, current_node))
            explored.add(child)
    return None


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: list[T] = []

    def push(self, item: T):
        heappush(self._container, item)

    def pop(self):
        return heappop(self._container)

    def __repr__(self) -> str:
        return repr(self._container)

    @property
    def empty(self) -> bool:
        return not self._container


def astar(
    initial: T,
    goal_test: Callable[[T], bool],
    successors: Callable[[T], list[T]],
    heuristic: Callable[[T], float],
) -> Optional[Node[T]]:
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))
    explored: dict[T, float] = {initial: 0.0}

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()  # node minimum cost __lt__
        current_state = current_node.state

        if goal_test(current_state):
            return current_node

        for child in successors(current_state):
            new_cost = current_node.cost + 1
            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))
    return None


if __name__ == "__main__":
    import random
    import timeit

    random.seed(1054)
    numbers = [random.randrange(10 ** 8) for _ in range(500_000)]

    keys = [random.randrange(10 ** 8) for _ in range(3)]

    sorted_numbers = sorted(numbers)
    print(
        timeit.timeit(
            "sum(linear_contains(numbers, key) for key in keys)",
            number=100,
            globals=globals(),
        )
    )

    print(
        timeit.timeit(
            "sum(binary_contains(sorted_numbers, key) for key in keys)",
            number=100_000,
            globals=globals(),
        )
    )

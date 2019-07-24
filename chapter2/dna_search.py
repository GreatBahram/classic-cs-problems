#!/usr/bin/env python3
from heapq import heappop, heappush
from typing_extensions import Protocol
from typing import (
    Any,
    Callable,
    Deque,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypeVar,
)

T = TypeVar('T')
C = TypeVar('C')

class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool:
        pass

    def __lt__(self: C, other: C) -> bool:
        pass

    def __gt__(self: C, other: C):
        return (not self < other) and (self != other)

    def __le__(self: C, other: C):
        return (self < other) or (self == other)
        pass

    def __ge__(self: C, other: C):
        return not self < other


def linear_contains(iterable: Iterable[T], key: T) -> bool:
    for item in iterable:
        if item == key:
            return True
    return False


def binary_contains(sequence: Sequence[C], key: C) -> bool:
    low: int = 0
    high: int = len(gene) - 1
    while low <= high:
        mid: int = (low + high) // 2
        if gene[mid] < key:
            low = mid + 1
        elif gene[mid] > key:
            high = mid - 1
        else:
            return True
    return False

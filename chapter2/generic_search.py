from typing import Any, Iterable, Protocol, Sequence, Type, TypeVar

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
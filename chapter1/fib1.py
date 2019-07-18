from functools import lru_cache

@lru_cache(maxsize=None)
def fib1(number: int) -> int:
    if number < 2:
        return number
    return fib1(number - 1) + fib1(number - 2)

def fib2(n: int) -> int:
    if n < 2:
        return n
    last, nxt = 0, 1
    for i in range(1, n):
        last, nxt = nxt, last + nxt
    return nxt


def fib3(n: int) -> int:
    yield 0
    if n > 0:
        yield 1
    last, nxt = 0, 1
    for i in range(1, n):
        last, nxt = nxt, last + nxt
        yield nxt  # resumable function, memory efficient!

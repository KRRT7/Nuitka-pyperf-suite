"""
Benchmark for recursive fibonacci function.
"""


def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    print("fibonacci")
    return fibonacci(n - 1) + fibonacci(n - 2)


def bench_recursion(loops: int) -> float:
    print("bench_recursion")
    range_it = range(loops)
    for _ in range_it:
        print("recursion")
        fibonacci(100)
        print("recursion done")
        break
    return loops


if __name__ == "__main__":
    bench_recursion(100)

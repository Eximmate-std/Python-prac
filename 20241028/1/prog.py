def fib(m, n):
    a, b = 0, 1
    for _ in range(m + n):
        a, b = b, a + b
        if _ >= m:
            yield a

from sys import stdin
exec(stdin.read())

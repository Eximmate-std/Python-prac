from itertools import islice

def slide(seq, n):
    for i in range(len(seq)):
        yield from islice(seq, i, i + n)

from sys import stdin
exec(stdin.read())

M, N = eval(input())
print([p for p in range(M, N) if all(p % d != 0 for d in range(2, int(p**0.5) + 1)) and p > 1])
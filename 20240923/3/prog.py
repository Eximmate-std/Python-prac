N = int(input())
i = N
while i <= (N + 2):
    j = N
    while j <= N + 2:
        result = i * j
        tmp = result
        digsum = 0
        while tmp > 0:
            digsum += tmp % 10
            tmp //= 10

        if digsum == 6:
            print(i," * ", j, " = :=)", end=" ")
        else:
            print(i," * ", j, " = ", result, end=" ")
        j += 1
    print()
    i += 1

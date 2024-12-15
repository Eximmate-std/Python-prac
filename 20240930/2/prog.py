inp = list(eval(input()))

length = len(inp)
for i in range(length):
    for j in range(length-i-1):
        if (inp[j] ** 2) % 100 > (inp[j+1] ** 2) % 100:
            inp[j], inp[j+1] = inp[j+1], inp[j]

print(inp)

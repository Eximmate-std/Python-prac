M1 = [eval(input())]
l = len(M1[0])
for _ in range(l-1):
    M1.append(eval(input()))

M2 = []
for _ in range(l):
    M2.append(eval(input()))

M = ["" * l for _ in range(l)]
for i in range(l):
    for j in range(l):
        s = sum(M1[i][k] * M2[k][j] for k in range(l))
        if j == 0:
            M[i] += str(s)
        else:
            M[i] += "," + str(s)

for i in range(l):
    print(M[i])


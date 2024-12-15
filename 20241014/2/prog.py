from math import *

def sign(x):
    return 1 if x > 0 else -1

def drawLine(x0, y0, y1):
    x1 = x0 + 1
    if y1 != y0:
        a = (x1 - x0) / (y1 - y0)
        b = x0 - y0 * a
        for dY in range(abs(y1 - y0)):
            Y = y0 + sign(y1 - y0) * dY
            matrix[Y][round(a * Y + b)] = '*'
    matrix[y1][x1] = '*'

W, H, A, B, fun = input().split()
W, H, A, B = int(W), int(H), float(A), float(B)
fun = lambda x, fun=fun: eval(fun)

matrix = [[' '] * W for line in range(H)]

coords = []
miny = inf
maxy = -inf
for X in range(W):
    y = fun(A + X * (B - A) / W)
    miny = min(miny, y)
    maxy = max(maxy, y)
    coords.append(y)

coords = [H - 1 - round((y - miny) * (H - 1) / (maxy - miny)) for y in coords]

for X, Y in enumerate(coords[:-1]):
    drawLine(X, Y, coords[X + 1])

print("\n".join("".join(line) for line in matrix))

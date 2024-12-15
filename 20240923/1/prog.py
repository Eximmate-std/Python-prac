val = int(input())
vclasses = [''] * 3
vclasses[0] = "+" if val % 50 == 0 else "-"
vclasses[1] = "+" if (val % 25 == 0) and (val % 2 == 1) else "-"
vclasses[2] = "+" if val % 8 == 0 else "-"
print("A ", vclasses[0], " B ", vclasses[1], " C ", vclasses[2])
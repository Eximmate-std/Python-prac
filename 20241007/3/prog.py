from math import *
def Calc(s, t, u):
    def func(x):
        s_x = eval(s, {"x": x, **globals()})
        t_x = eval(t, {"x": x, **globals()})
        return eval(u, {"x": s_x, "y": t_x, **globals()})
    return func

s, t, u = input().split(", ")
x_value = float(input())
print(Calc(s, t, u)(x_value))

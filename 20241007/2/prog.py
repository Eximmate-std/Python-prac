def substract(a, b):
    if isinstance(a, int) or isinstance(a, float):
        return a - b
    elif  isinstance(a, str):
        return "".join([i for i in a if i not in b])
    elif isinstance(a, tuple):
        return tuple(i for i in a if i not in b)
    elif isinstance(a, list):
        return [i for i in a if i not in b]
print(substract(*eval(input())))

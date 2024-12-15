def Pareto(*pairs):
    def is_dominated(pair1, pair2):
        return (pair1[0] <= pair2[0] and pair1[1] <= pair2[1]) and (pair1 != pair2)

    pareto_front = []

    for pair in pairs:
        dominated = False
        for pair1 in pairs:
            if is_dominated(pair, pair1):
                dominated = True
                break
        if not dominated:
            pareto_front.append(pair)

    return tuple(pareto_front)

print(Pareto(*eval(input())))

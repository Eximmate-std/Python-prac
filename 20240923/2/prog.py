sum = 0
while val := int(input()):
    if val < 0:
        print(val)
        break
    else:
        sum += val
        if sum > 21:
            print(sum)
            break
if val == 0:
    print(val)
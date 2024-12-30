def rotate(gas, liquid, width):
    height = gas + liquid
    print("#" * (height + 2))
    for _ in range((gas * width) // height):
        print("#" + "." * height + "#")
    for _ in range((liquid * width) // height):
        print("#" + "~" * height + "#")
    print("#" * (height + 2))


width = len(input()) - 2
gas, liquid = 0, 0

while (line := input())[1] == '.':
    gas += 1
liquid += 1
while (line := input())[1] == '~':
    liquid += 1

rotate(gas, liquid, width)

max_value = max(gas, liquid)
gas_diagram = round(20 * gas / max_value)
liquid_diagram = round(20 * liquid / max_value)

print('.' * gas_diagram + ' ' * (20 - gas_diagram) + ' ' * (max(0, len(str(liquid)) - len(str(gas))) + 1) + str(gas*width) + '/' + str((gas + liquid)*width))
print('~' * liquid_diagram + ' ' * (20 - liquid_diagram) + ' ' * (max(0, len(str(gas)) - len(str(liquid))) + 1) + str(liquid*width) + '/' + str((gas + liquid)*width))

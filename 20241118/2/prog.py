class InvalidInput(Exception):
    pass

class BadTriangle(Exception):
    pass

def triangleSquare(inStr):
        try:
            coords = eval(inStr)
        except:
            raise InvalidInput
        if len(coords) != 3:
            raise InvalidInput

        for coord in coords:
            if not isinstance(coord, tuple) or len(coord) != 2:
                raise InvalidInput

        x1, y1 = coords[0]
        x2, y2 = coords[1]
        x3, y3 = coords[2]

        try:
            area = 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        except:
            raise BadTriangle
        if round(area, 2) == 0:
            raise BadTriangle
        return round(area, 2)


while user_input := input():
    try:
        area = triangleSquare(user_input)
    except InvalidInput as e:
        print("Invalid input")
    except BadTriangle as e:
        print("Not a triangle")
    else:
        print(f"{area:.2f}")
        break

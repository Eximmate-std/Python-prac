class Triangle:
    def __init__(self, p1, p2, p3):
        self.points = (tuple(p1), tuple(p2), tuple(p3))

    def area(self):
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        x3, y3 = self.points[2]
        return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2)

    def __abs__(self):
        return self.area()

    def __bool__(self):
        return self.area() != 0

    def __lt__(self, other):
        return self.area() < other.area()

    def contains_point(self, point):
        x, y = point
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        x3, y3 = self.points[2]

        # Используем метод барицентрических координат
        if (denominator := ((y2 - y3) * (x1 - x3) + (x3 - x1) * (y2 - y1))) == 0:
            return False
        a = ((y2 - y3) * (x - x3) + (x3 - x1) * (y - y3)) / denominator
        b = ((y3 - y1) * (x - x3) + (x1 - x2) * (y - y3)) / denominator
        c = 1 - a - b
        return a >= 0 and b >= 0 and c >= 0

    def __contains__(self, other):
        if not self:
            return True
        return all(other.contains_point(point) for point in self.points)

    def intersects(self, other):
        if not self or not other:
            return False
        for point in self.points:
            if other.contains_point(point):
                return True
        for point in other.points:
            if self.contains_point(point):
                return True
        return False

    def __and__(self, other):
        return self.intersects(other)

    def __repr__(self):
        return f"Triangle({self.points[0]}, {self.points[1]}, {self.points[2]})"

import sys
exec(sys.stdin.read())
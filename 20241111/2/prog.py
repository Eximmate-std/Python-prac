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

    @staticmethod
    def onSegment(p, q, r):
        if ((q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and
                (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
            return True
        return False

    @staticmethod
    def orientation(p, q, r):
        val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
        if (val > 0):
            return 1
        elif (val < 0):
            return 2
        else:
            return 0

    @staticmethod
    def doIntersect(p1, q1, p2, q2):
        o1 = Triangle.orientation(p1, q1, p2)
        o2 = Triangle.orientation(p1, q1, q2)
        o3 = Triangle.orientation(p2, q2, p1)
        o4 = Triangle.orientation(p2, q2, q1)

        if ((o1 != o2) and (o3 != o4)):
            return True
        if ((o1 == 0) and Triangle.onSegment(p1, p2, q1)):
            return True
        if ((o2 == 0) and Triangle.onSegment(p1, q2, q1)):
            return True
        if ((o3 == 0) and Triangle.onSegment(p2, p1, q2)):
            return True
        if ((o4 == 0) and Triangle.onSegment(p2, q1, q2)):
            return True
        return False

    def intersects(self, other):
        if not self or not other:
            return False
        for i in range(3):
            for j in range(3):
                if Triangle.doIntersect(self.points[i - 1], self.points[i], other.points[j - 1], other.points[j]):
                    return True
        return False

    def __and__(self, other):
        return self.intersects(other)

    def __repr__(self):
        return f"Triangle({self.points[0]}, {self.points[1]}, {self.points[2]})"

import sys
exec(sys.stdin.read())
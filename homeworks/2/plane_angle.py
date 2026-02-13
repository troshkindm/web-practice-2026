#  заполняем класс Point и функцию plane_angle
#  угол между плоскостями ABC и BCD через векторное произведение
import math

class Point:
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __sub__(self, no):
        return Point(self.x - no.x, self.y - no.y, self.z - no.z)

    def dot(self, no):
        return self.x * no.x + self.y * no.y + self.z * no.z

    def cross(self, no):
        return Point(
            self.y * no.z - self.z * no.y,
            self.z * no.x - self.x * no.z,
            self.x * no.y - self.y * no.x
        )

    def absolute(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

def plane_angle(a, b, c, d):
    # X = AB x BC, Y = BC x CD
    ab = b - a
    bc = c - b
    cd = d - c
    x = ab.cross(bc)
    y = bc.cross(cd)
    # cos(phi) = (X, Y) / |X| * |Y|
    cos_val = x.dot(y) / (x.absolute() * y.absolute())
    # ограничиваем на случай числовых погрешностей
    cos_val = max(-1.0, min(1.0, cos_val))
    return round(math.degrees(math.acos(cos_val)), 2)

if __name__ == '__main__':
    points = []
    for _ in range(4):
        coords = list(map(float, input().split()))
        points.append(Point(*coords))
    print(f"{plane_angle(*points):.2f}")
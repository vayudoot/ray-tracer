from __future__ import annotations

import math

class Tuple:
    EPSILON = 0.0001

    def __init__(self, x: float, y: float, z: float, w: float):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __str__(self) -> str:
        return f"({self.x:.3f}, {self.y:.3f}, {self.z:.3f}, {self.w})"

    def __eq__(self, other):
        return (abs(self.x - other.x) < self.EPSILON
                and abs(self.y - other.y) < self.EPSILON
                and abs(self.z - other.z) < self.EPSILON
                and self.w == other.w)

    def __add__(self, other):
        if self.w + other.w in [0, 1]:
            return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)
        else:
            raise ValueError("Cannot add two points")

    def __sub__(self, other):
        return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

    def __neg__(self):
        return self.__class__(-self.x, -self.y, -self.z, -self.w)

    def __mul__(self, num):
        if isinstance(num, int) or isinstance(num, float):
            return self.__class__(self.x * num, self.y * num, self.z * num, self.w * num)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, num):
        if isinstance(num, int) or isinstance(num, float):
            return self.__class__(self.x / num, self.y / num, self.z / num, self.w / num)

    def magnitude(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self) -> Tuple:
        m = self.magnitude()
        return self.__class__(self.x / m, self.y / m, self.z / m, self.w / m)

    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w

    def cross(self, other) -> Tuple:
        return self.__class__(self.y * other.z - self.z * other.y,
                              self.z * other.x - self.x * other.z,
                              self.x * other.y - self.y * other.x)

    def reflect(self, normal: Tuple) -> Tuple:
        return self - normal * 2 * self.dot(normal)


class Point(Tuple):
    def __init__(self, x: float, y: float, z: float, w: float = 1):
        super().__init__(x, y, z, w)

    def __str__(self) -> str:
        return f"P({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"


class Vector(Tuple):
    def __init__(self, x: float, y: float, z: float, w: float = 0):
        super().__init__(x, y, z, w)

    def __str__(self) -> str:
        return f"V({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"


class Color(Tuple):
    # Make it vector as cannot add points
    def __init__(self, r, g, b, w=0):
        super().__init__(r, g, b, w)

    @property
    def red(self):
        return self.x

    @property
    def green(self):
        return self.y

    @property
    def blue(self):
        return self.z

    def __str__(self):
        return f"C({self.red:.2f}, {self.green:.2f}, {self.blue:.2f})"

    def __mul__(self, other):
        if isinstance(other, Color):
            # blend color (Hadamard product)
            return Color(self.red * other.red, self.green * other.green, self.blue * other.blue)
        else:
            # usual int or float
            return super().__mul__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def to_rgb(self) -> tuple[float, float, float]:
        r = int(math.ceil(max(min(self.red * 255, 255), 0)))
        g = int(math.ceil(max(min(self.green * 255, 255), 0)))
        b = int(math.ceil(max(min(self.blue * 255, 255), 0)))
        return (r, g, b)

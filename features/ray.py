from __future__ import annotations

class Ray:
    def __init__(self, origin: Point, direction: Vector):
        self.origin = origin
        self.direction = direction

    def __str__(self):
        print(f"R({self.origin}, {self.direction}")

    def position(self, t: Union[Point, Vector]):
        return self.origin + self.direction * t

    def transform(self, m: Matrix):
        return Ray(m * self.origin, m * self.direction)

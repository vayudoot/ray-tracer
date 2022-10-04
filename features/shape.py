from __future__ import annotations

import math

from features.intersection import Intersection, Intersections
from features.material import Material
from features.matrix import Matrix
from features.tuple import Point

class Sphere:
    def __init__(self, material=None):
        self.transform = Matrix.identity(4)
        self.material = Material() if not material else material

    def __eq__(self, other):
        return (isinstance(other, Sphere) and
                self.transform == other.transform and
                self.material == other.material)

    def intersect(self, r: Ray) -> Intersections:
        ray = r.transform(self.transform.inverse())
        sphere_to_ray = ray.origin - Point(0, 0, 0)
        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1
        discriminant = b * b - 4 * a * c

        if discriminant < 0:
            return Intersections()
        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        return Intersections(Intersection(t1, self), Intersection(t2, self))

    def set_transform(self, t: Matrix) -> None:
        self.transform = t

    def normal_at(self, p: Point) -> Tuple:
        object_point = self.transform.inverse() * p
        object_normal = object_point - Point(0, 0, 0)
        world_normal = self.transform.inverse().transpose() * object_normal
        world_normal.w = 0
        return world_normal.normalize()

from __future__ import annotations

from features.intersection import Intersections
from features.light import Light
from features.material import Material
from features.matrix import Scaling
from features.shape import Sphere
from features.ray import Ray
from features.tuple import Color, Point

class World:
    def __init__(self, light=None):
        self.objects = []
        self.light = light

    @staticmethod
    def default():
        w = World()
        s1 = Sphere(material=Material(c=Color(0.8, 1.0, 0.6), d=0.7, sp=0.2))
        s2 = Sphere()
        s2.set_transform(Scaling(0.5, 0.5, 0.5))
        w.light = Light(Point(-10, 10, -10), Color(1, 1, 1))
        w.objects = [s1, s2]
        return w

    def intersect(self, r: Ray) -> Intersections:
        xs = Intersections()
        for obj in self.objects:
            xs.extend(obj.intersect(r))
        xs.sort()
        return xs

    def shade_hit(self, comps: Computations):
        shadowed = self.is_shadowed(comps.over_point)
        return comps.object.material.lighting(self.light, comps.over_point, comps.eyev,
                                              comps.normalv, shadowed)

    def color_at(self, r: Ray) -> Color:
        hit = self.intersect(r).hit()
        return Color(0, 0, 0) if hit is None else self.shade_hit(hit.prepare_computations(r))

    def is_shadowed(self, p: Point) -> bool:
        v = self.light.position - p
        distance = v.magnitude()
        direction = v.normalize()
        r = Ray(p, direction)
        hit = self.intersect(r).hit()
        return hit and hit.t < distance

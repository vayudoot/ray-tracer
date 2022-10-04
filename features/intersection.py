from __future__ import annotations

from features.tuple import Tuple

class Intersection:
    def __init__(self, t: float, obj: Sphere):
        self.t = t
        self.object = obj

    def __eq__(self, other):
        return isinstance(other, Intersection) and self.t == other.t and self.object == self.object

    def __lt__(self, other):
        return isinstance(other, Intersection) and self.t < other.t and self.object == self.object

    def prepare_computations(self, r: Ray) -> Computations:
        comps = Computations(self.t, self.object)
        comps.point = r.position(comps.t)
        comps.eyev = -r.direction
        comps.normalv = comps.object.normal_at(comps.point)
        if comps.normalv.dot(comps.eyev) < 0:
            comps.inside = True
            comps.normalv = -comps.normalv
        comps.over_point = comps.point + comps.normalv * Tuple.EPSILON
        return comps

class Intersections(list):
    def __init__(self, *args):
        super(Intersections, self).__init__(args)
        self.count = len(args)

    def append(self, obj):
        super().append(obj)
        self.count += 1

    def extend(self, iterable):
        super().extend(iterable)
        self.count += len(iterable)

    def hit(self) -> float:
        return min([i for i in self if i.t > 0], default=None)

class Computations:
    def __init__(self, t: float, obj: Sphere):
        self.t = t
        self.object = obj
        self.point = None
        self.eyev = None
        self.normalv = None
        self.inside = False
        self.over_point = None

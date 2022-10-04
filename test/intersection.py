import unittest

from features.intersection import Intersection, Intersections
from features.matrix import Translation
from features.shape import Sphere
from features.ray import Ray
from features.tuple import Point, Tuple, Vector

class TestIntersection(unittest.TestCase):
    def test_creation(self):
        s = Sphere()
        i = Intersection(3.5, s)
        self.assertEqual((i.t, i.object), (3.5, s))

    def test_intersections(self):
        s = Sphere()
        i1 = Intersection(1, s)
        i2 = Intersection(2, s)
        xs = Intersections(i1, i2)
        self.assertEqual(xs.count, 2)
        self.assertEqual((xs[0].t, xs[1].t), (1, 2))

    def test_all_positive(self):
        s = Sphere()
        i1 = Intersection(1, s)
        i2 = Intersection(2, s)
        xs = Intersections(i2, i1)
        i = xs.hit()
        self.assertEqual(i, i1)

    def test_all_positive(self):
        s = Sphere()
        i1 = Intersection(-1, s)
        i2 = Intersection(1, s)
        xs = Intersections(i2, i1)
        i = xs.hit()
        self.assertEqual(i, i2)

    def test_all_positive(self):
        s = Sphere()
        i1 = Intersection(-1, s)
        i2 = Intersection(-2, s)
        xs = Intersections(i2, i1)
        i = xs.hit()
        self.assertEqual(i, None)

    def test_all_positive(self):
        s = Sphere()
        i1 = Intersection(5, s)
        i2 = Intersection(7, s)
        i3 = Intersection(-3, s)
        i4 = Intersection(2, s)
        xs = Intersections(i2, i1, i3, i4)
        i = xs.hit()
        self.assertEqual(i, i4)

    def test_prep_computations(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = Sphere()
        i = Intersection(4, shape)
        comps = i.prepare_computations(r)
        self.assertEqual(comps.t, i.t)
        self.assertEqual(comps.object, i.object)
        self.assertEqual(comps.point, Point(0, 0, -1))
        self.assertEqual(comps.eyev, Vector(0, 0, -1))
        self.assertEqual(comps.normalv, Vector(0, 0, -1))

    def test_hit_outside(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = Sphere()
        i = Intersection(4, shape)
        comps = i.prepare_computations(r)
        self.assertEqual(comps.inside, False)

    def test_hit_inside(self):
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        shape = Sphere()
        i = Intersection(1, shape)
        comps = i.prepare_computations(r)
        self.assertEqual(comps.point, Point(0, 0, 1))
        self.assertEqual(comps.eyev, Vector(0, 0, -1))
        self.assertEqual(comps.normalv, Vector(0, 0, -1))
        self.assertEqual(comps.inside, True)

    def test_hit_offset(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = Sphere()
        shape.transform = Translation(0, 0, 1)
        i = Intersection(5, shape)
        comps = i.prepare_computations(r)
        self.assertLess(comps.over_point.z, -Tuple.EPSILON/2)
        self.assertGreater(comps.point.z, comps.over_point.z)

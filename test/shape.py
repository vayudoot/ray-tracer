import unittest
import math

from features.material import Material
from features.matrix import Matrix, Rotation, Scaling, Translation
from features.ray import Ray
from features.shape import Sphere
from features.tuple import Point, Vector

class TestShape(unittest.TestCase):
    def test_sphere_intersect(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(len(xs), 2)
        self.assertEqual((xs[0].t, xs[1].t), (4.0, 6.0))

    def test_sphere_intersect_tanget(self):
        r = Ray(Point(0, 1, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(len(xs), 2)
        self.assertEqual((xs[0].t, xs[1].t), (5.0, 5.0))

    def test_sphere_miss_tanget(self):
        r = Ray(Point(0, 2, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(len(xs), 0)

    def test_sphere_intersect_inside(self):
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(len(xs), 2)
        self.assertEqual((xs[0].t, xs[1].t), (-1.0, 1.0))

    def test_sphere_intersect_outside(self):
        r = Ray(Point(0, 0, 5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(len(xs), 2)
        self.assertEqual((xs[0].t, xs[1].t), (-6.0, -4.0))

    def test_default_transform(self):
        s = Sphere()
        self.assertEqual(s.transform, Matrix.identity(4))
        t = Translation(2, 3, 4)
        s.set_transform(t)
        self.assertEqual(s.transform, t)

    def test_intesect_scaled(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        s.set_transform(Scaling(2, 2, 2))
        xs = s.intersect(r)
        self.assertEqual(xs.count, 2)
        self.assertEqual((xs[0].t, xs[1].t), (3, 7))

    def test_intesect_scaled(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()

        s.set_transform(Scaling(2, 2, 2))
        xs = s.intersect(r)
        self.assertEqual(xs.count, 2)
        self.assertEqual((xs[0].t, xs[1].t), (3, 7))

        s.set_transform(Translation(5, 0, 0))
        xs = s.intersect(r)
        self.assertEqual(xs.count, 0)

    def test_normal_at(self):
        s = Sphere()
        n = s.normal_at(Point(1, 0, 0))
        self.assertEqual(n, Vector(1, 0, 0))
        n = s.normal_at(Point(0, 1, 0))
        self.assertEqual(n, Vector(0, 1, 0))
        n = s.normal_at(Point(0, 0, 1))
        self.assertEqual(n, Vector(0, 0, 1))
        n = s.normal_at(Point(math.sqrt(3)/3, math.sqrt(3)/3, math.sqrt(3)/3))
        self.assertEqual(n, Vector(math.sqrt(3)/3, math.sqrt(3)/3, math.sqrt(3)/3))
        self.assertEqual(n, n.normalize())

    def test_normal_translated(self):
        s = Sphere()
        s.set_transform(Translation(0, 1, 0))
        n = s.normal_at(Point(0, 1.70711, -0.70711))
        self.assertEqual(n, Vector(0, 0.70711, -0.70711))

        m = Scaling(1, 0.5, 1) * Rotation(0, 0, math.pi / 5)
        s.set_transform(m)
        n = s.normal_at(Point(0, math.sqrt(2)/2, -math.sqrt(2)/2))
        self.assertEqual(n, Vector(0, 0.97014, -0.24254))

    def test_material(self):
        s = Sphere()
        self.assertEqual(s.material, Material())

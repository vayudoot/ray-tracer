import unittest
import numpy as np

from features.matrix import Matrix, Rotation, Scaling, Shearing, Translation, view_transform
from features.tuple import Point, Vector

class TestTransformations(unittest.TestCase):
    def test_mul(self):
        t = Translation(5, -3, 2)
        p = Point(-3, 4, 5)
        self.assertEqual(t * p, Point(2, 1, 7))
        self.assertEqual(t.inverse() * p, Point(-8, 7, 3))

        v = Vector(-3, 4, 5)
        self.assertEqual(t * v, v)

    def test_scaling(self):
        t = Scaling(2, 3, 4)
        p = Point(-4, 6, 8)
        self.assertEqual(t * p, Point(-8, 18, 32))

        v = Vector(-4, 6, 8)
        self.assertEqual(t * v, Vector(-8, 18, 32))

        self.assertEqual(t.inverse() * v, Vector(-2, 2, 2))

    def test_reflection(self):
        t = Scaling(-1, 1, 1)
        p = Point(2, 3, 4)
        self.assertEqual(t * p, Point(-2, 3, 4))

    def test_rotate(self):
        p = Point(0, 1, 0)
        half_quarter = Rotation(np.pi / 4, 0, 0)
        full_quarter = Rotation(np.pi / 2, 0, 0)
        self.assertEqual(half_quarter * p, Point(0, np.sqrt(2)/2, np.sqrt(2)/2))
        self.assertEqual(full_quarter * p, Point(0, 0, 1))
        self.assertEqual(half_quarter.inverse() * p, Point(0, np.sqrt(2)/2, -np.sqrt(2)/2))

    def test_shearing(self):
        t_xy = Shearing(1, 0, 0, 0, 0, 0)
        p = Point(2, 3, 4)
        self.assertEqual(t_xy * p, Point(5, 3, 4))
        t_xz = Shearing(0, 1, 0, 0, 0, 0)
        self.assertEqual(t_xz * p, Point(6, 3, 4))
        t_yx = Shearing(0, 0, 1, 0, 0, 0)
        self.assertEqual(t_yx * p, Point(2, 5, 4))
        t_yz = Shearing(0, 0, 0, 1, 0, 0)
        self.assertEqual(t_yz * p, Point(2, 7, 4))
        t_zx = Shearing(0, 0, 0, 0, 1, 0)
        self.assertEqual(t_zx * p, Point(2, 3, 6))
        t_zy = Shearing(0, 0, 0, 0, 0, 1)
        self.assertEqual(t_zy * p, Point(2, 3, 7))

    def test_transformation(self):
        p = Point(1, 0, 1)
        r = Rotation(np.pi/2, 0, 0)
        s = Scaling(5, 5, 5)
        t = Translation(10, 5, 7)

        p2 = r * p
        p3 = s * p2
        p4 = t * p3
        self.assertEqual(p4, Point(15, 0, 7))
        self.assertEqual((t * s * r) * p, Point(15, 0, 7))

    def test_default_transformation(self):
        t = view_transform(Point(0, 0, 0), Point(0, 0, -1), Vector(0, 1, 0))
        self.assertEqual(t, Matrix.identity(4))
        t = view_transform(Point(0, 0, 0), Point(0, 0, 1), Vector(0, 1, 0))
        self.assertEqual(t, Scaling(-1, 1, -1))
        t = view_transform(Point(0, 0, 8), Point(0, 0, 0), Vector(0, 1, 0))
        self.assertEqual(t, Translation(0, 0, -8))
        t = view_transform(Point(1, 3, 2), Point(4, -2, 8), Vector(1, 1, 0))
        self.assertEqual(t, Matrix([[-0.50709, 0.50709, 0.67612, -2.36643],
                                    [0.76772, 0.60609, 0.12122, -2.82843],
                                    [-0.35857, 0.59761, -0.71714, 0.00000],
                                    [0.00000, 0.00000, 0.00000, 1.00000]]))

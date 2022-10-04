import unittest
import math

from features.tuple import *

class TestTuples(unittest.TestCase):
    def test_points(self):
        self.assertEqual(Tuple(4.3, -4.2, 3.1, 1.0), Point(4.3, -4.2, 3.1))

    def test_vectors(self):
        self.assertEqual(Tuple(4.3, -4.2, 3.1, 0.0), Vector(4.3, -4.2, 3.1))

    def test_add(self):
        self.assertEqual(Tuple(3, -2, 5, 1) + Tuple(-2, 3, 1, 0), Tuple(1, 1, 6, 1))

    def test_sub(self):
        self.assertEqual(Point(3, 2, 1) - Point(5, 6, 7), Vector(-2, -4, -6))
        self.assertEqual(Vector(3, 2, 1) - Vector(5, 6, 7), Vector(-2, -4, -6))

    def test_negate(self):
        self.assertEqual(Vector(0, 0, 0) - Vector(1, -2, 3), -Vector(1, -2, 3))

    def test_mul(self):
        self.assertEqual(Tuple(1, -2, 3, -4) * 3.5, Tuple(3.5, -7, 10.5, -14))
        self.assertEqual(0.5 * Tuple(1, -2, 3, -4), Tuple(0.5, -1, 1.5, -2))

    def test_div(self):
        self.assertEqual(Tuple(1, -2, 3, -4) / 2, Tuple(0.5, -1, 1.5, -2))

    def test_magnitude(self):
        self.assertEqual(Vector(1, 0, 0).magnitude(), 1)
        self.assertEqual(Vector(0, 1, 0).magnitude(), 1)
        self.assertEqual(Vector(0, 0, 1).magnitude(), 1)
        self.assertEqual(Vector(1, 2, 3).magnitude(), math.sqrt(14))
        self.assertEqual(Vector(-1, -2, -3).magnitude(), math.sqrt(14))

    def test_normalize(self):
        self.assertEqual(Vector(4, 0, 0).normalize(), Vector(1, 0, 0))
        self.assertEqual(Vector(1, 2, 3).normalize(), Vector(0.26726, 0.53452, 0.8017))

    def test_dot(self):
        self.assertEqual(Vector(1, 2, 3).dot(Vector(2, 3, 4)), 20)

    def test_cross(self):
        self.assertEqual(Vector(1, 2, 3).cross(Vector(2, 3, 4)), Vector(-1, 2, -1))
        self.assertEqual(Vector(2, 3, 4).cross(Vector(1, 2, 3)), Vector(1, -2, 1))

    def test_reflect(self):
        v = Vector(1, -1, 0)
        n = Vector(0, 1, 0)
        r = v.reflect(n)
        self.assertEqual(r, Vector(1, 1, 0))

        v = Vector(0, -1, 0)
        r = v.reflect(Vector(math.sqrt(2)/2, math.sqrt(2)/2, 0))
        self.assertEqual(r, Vector(1, 0, 0))

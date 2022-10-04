import unittest

from features.matrix import Matrix
from features.tuple import Tuple

class TestMatrix(unittest.TestCase):
    def test_matrix(self):
        m = Matrix(
            [
                [1, 2, 3, 4],
                [5.5, 6.5, 7.5, 8.5],
                [9, 10, 11, 12],
                [13.5, 14.5, 15.5, 16.5]
            ]
        )
        self.assertEqual(m[0][0], 1)
        self.assertEqual(m[1][0], 5.5)
        self.assertEqual(m[2][2], 11)
        self.assertEqual(m[3][2], 15.5)

    def test_equal(self):
        m1 = Matrix([[1,2,3],[4,5,6],[7,8,9]])
        m2 = Matrix([[1,2,3],[4,5,6],[7,8,9]])
        m3 = Matrix([[1,2,3],[4,5,6]])
        m4 = Matrix([[1,2,3],[4,5,6],[7,8,1]])
        self.assertEqual(m1, m2)
        self.assertNotEqual(m1, m3)
        self.assertNotEqual(m1, m4)

    def test_mul(self):
        m1 = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]])
        m2 = Matrix([[-2, 1, 2, 3], [3, 2, 1, -1], [4, 3, 6, 5], [1, 2, 7, 8]])
        res = Matrix([[20, 22, 50, 48], [44, 54, 114, 108], [40, 58, 110, 102], [16, 26, 46, 42]])
        self.assertEqual(m1 * m2, res)

    def test_mul_tuple(self):
        m = Matrix([[1, 2, 3, 4], [2, 4, 4, 2], [8, 6, 4, 1], [0, 0, 0, 1]])
        t = Tuple(1, 2, 3, 1)
        self.assertEqual(m * t, Tuple(18, 24, 33, 1))

    def test_identity(self):
        m = Matrix([[0, 1, 2, 4], [1, 2, 4, 8], [2, 4, 8, 16], [4, 8, 16, 32]])
        self.assertEqual(m * Matrix.identity(4), m)
        t = Tuple(1, 2, 3, 4)
        self.assertEqual(Matrix.identity(4) * t, t)

    def test_transpose(self):
        m = Matrix([[0, 9, 3, 0], [9, 8, 0, 8], [1, 8, 5, 3], [0, 0, 5, 8]])
        r = Matrix([[0, 9, 1, 0], [9, 8, 8, 0], [3, 0, 5, 5], [0, 8, 3, 8]])
        self.assertEqual(m.transpose(), r)
        i = Matrix.identity(4)
        self.assertEqual(i.transpose(), i)

    def test_determinant(self):
        m = Matrix([[1,5],[-3,2]])
        self.assertEqual(m.determinant(), 17)
        m = Matrix([[-2, -8, 3, 5], [-3, 1, 7, 3], [1, 2, -9, 6], [-6, 7, 7, -9]])
        self.assertEqual(m.determinant(), -4071)

    def test_invertible(self):
        m = Matrix([[6, 4, 4, 4], [5, 5, 7, 6], [4, -9, 3, -7], [9, 1, 7, -6]])
        self.assertTrue(m.determinant()) # det = -2120
        m = Matrix([[-4, 2, -2, -3], [9, 6, 2, 6], [0, -5, 1, -5], [0, 0, 0, 0]])
        self.assertFalse(m.determinant()) # det = 0

    def test_inverse(self):
        m = Matrix([[-5, 2, 6, -8], [1, -5, 1, 8], [7, 7, -6, -7], [1, -3, 7, 4]])
        r = Matrix(
            [
                [0.21805, 0.45113, 0.24060, -0.04511],
                [-0.80827, -1.45677, -0.44361, 0.52068],
                [-0.07895, -0.22368, -0.05263, 0.19737],
                [-0.52256, -0.81391, -0.30075, 0.30639],
            ]
        )
        self.assertEqual(m.inverse(), r)
        m = Matrix([[8, -5, 9, 2], [7, 5, 6, 1], [-6, 0, 9, 6], [-3, 0, -9, -4]])
        r = Matrix(
            [
                [-0.15385, -0.15385, -0.28205, -0.53846],
                [-0.07692, 0.12308, 0.02564, 0.03077],
                [0.35897, 0.35897, 0.43590, 0.92308],
                [-0.69231, -0.69231, -0.76923, -1.92308],
            ]
        )
        self.assertEqual(m.inverse(), r)

        m = Matrix([[9, 3, 0, 9], [-5, -2, -6, -3], [-4, 9, 6, 4], [-7, 6, 6, 2]])
        r = Matrix(
            [
                [-0.04074, -0.07778, 0.14444, -0.22222],
                [-0.07778, 0.03333, 0.36667, -0.33333],
                [-0.02901, -0.14630, -0.10926, 0.12963],
                [0.17778, 0.06667, -0.26667, 0.33333],
            ]
        )
        self.assertEqual(m.inverse(), r)

from __future__ import annotations

import numpy as np
from typing import List

from features.tuple import Tuple

class Matrix:
    def __init__(self, m: List[List[float]]):
        self.row = len(m)
        try:
            self.col = len(m[0])
        except IndexError:
            print("not 2d matrix")
        self.matrix = np.array(m)

    # will return whole row (list), so caller can do row[x][y]
    def __getitem__(self, key) -> List[float]:
        return self.matrix[key]

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def __eq__(self, other):
        if (not isinstance(other, Matrix) or
            self.row != other.row or
            self.col != other.col):
            return False
        return np.allclose(self.matrix, other.matrix, rtol=10 ** -3)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return Matrix(self.matrix @ other.matrix)
        elif isinstance(other, int) or isinstance(other, float):
            return Matrix(self.matrix * other)
        elif isinstance(other, Tuple):
            # since our Tuple is of size 4, so matrix can be mx4 only
            if self.row != 4:
                raise Exception("can only use matrix with column 4")
            return Tuple(
                Tuple(*(self[0])).dot(other),
                Tuple(*(self[1])).dot(other),
                Tuple(*(self[2])).dot(other),
                Tuple(*(self[3])).dot(other),
            )
        else:
            raise Exception("cannot multiply Matrix")

    def __str__(self):
        m = ""
        for row in self.matrix:
            m += " ".join(str(i) for i in row) + "\n"
        return m

    def transpose(self) -> Matrix:
        return Matrix(self.matrix.T)

    def determinant(self) -> float:
        return np.round(np.linalg.det(self.matrix), 4)

    def inverse(self) -> Matrix:
        if self.determinant() != 0:
            return Matrix(np.linalg.inv(self.matrix))
        else:
            raise Exception

    @staticmethod
    def identity(size) -> Matrix:
        return Matrix(np.eye(size))


class Translation(Matrix):
    def __init__(self, x: int, y: int, z: int):
        super().__init__(np.eye(4))
        self.matrix[:3, 3] = [x, y, z]

class Scaling(Matrix):
    def __init__(self, x: int, y: int, z: int):
        super().__init__(np.diag([x, y, z, 1]))

class Rotation(Matrix):
    def __init__(self, x_rad=None, y_rad=None, z_rad=None):
        m = np.eye(4)
        if x_rad:
            x = np.eye(4)
            x[1:3, 1:3] = [[np.cos(x_rad), -np.sin(x_rad)], [np.sin(x_rad), np.cos(x_rad)]]
            m = m @ x
        if y_rad:
            y = np.eye(4)
            y[::2, ::2] = [[np.cos(y_rad), np.sin(y_rad)], [-np.sin(y_rad), np.cos(y_rad)]]
            m = m @ y
        if z_rad:
            z = np.eye(4)
            z[:2, :2] = [[np.cos(z_rad), -np.sin(z_rad)], [np.sin(z_rad), np.cos(z_rad)]]
            m = m @ z
        super().__init__(m)

class Shearing(Matrix):
    def __init__(self, x_y, x_z, y_x, y_z, z_x, z_y):
        m = np.eye(4)
        m[:3, :3] = [[1, x_y, x_z], [y_x, 1, y_z], [z_x, z_y, 1]]
        super().__init__(m)

def view_transform(src: Point, to: Point, up: Vector) -> Matrix:
    forward = (to - src).normalize()
    left = forward.cross(up.normalize())
    true_up = left.cross(forward)
    orientation = Matrix([[left.x, left.y, left.z, 0],
                          [true_up.x, true_up.y, true_up.z, 0],
                          [-forward.x, -forward.y, -forward.z, 0],
                          [0, 0, 0, 1]])
    return orientation * Translation(-src.x, -src.y, -src.z)

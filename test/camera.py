import unittest
import math

from features.camera import Camera
from features.matrix import Matrix, Rotation, Translation, view_transform
from features.tuple import Point, Vector, Tuple, Color
from features.world import World


class TestCamera(unittest.TestCase):
    def test_construct(self):
        c = Camera(160, 120, math.pi/2)
        self.assertEqual(c.transform, Matrix.identity(4))

    def test_pixel_size(self):
        c = Camera(200, 125, math.pi/2)
        self.assertAlmostEqual(c.pixel_size, 0.01, delta=Tuple.EPSILON)
        c = Camera(125, 200, math.pi/2)
        self.assertAlmostEqual(c.pixel_size, 0.01, 4)

    def test_ray_for_pixel(self):
        c = Camera(201, 101, math.pi/2)
        r = c.ray_for_pixel(100, 50)
        self.assertEqual(r.origin, Point(0, 0, 0))
        self.assertEqual(r.direction, Vector(0, 0, -1))

        r = c.ray_for_pixel(0, 0)
        self.assertEqual((r.origin, r.direction), (Point(0, 0, 0), Vector(0.66519, 0.33259, -0.66851)))

        c.transform = Rotation(y_rad=math.pi/4) * Translation(0, -2, 5)
        r = c.ray_for_pixel(100, 50)
        self.assertEqual(r.origin, Point(0, 2, -5))
        self.assertEqual(r.direction, Vector(math.sqrt(2)/2, 0, -math.sqrt(2)/2))

    def test_render_camera(self):
        w = World.default()
        c = Camera(11, 11, math.pi/2)
        c.transform = view_transform(Point(0, 0, -5), Point(0, 0, 0), Vector(0, 1, 0))
        image = c.render(w)
        self.assertEqual(image.pixel_at(5, 5), Color(0.38066, 0.47583, 0.2855))

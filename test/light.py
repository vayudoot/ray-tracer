import unittest

from features.light import Light
from features.tuple import Color, Point

class TestLight(unittest.TestCase):
    def test_point_light(self):
        intensity = Color(1, 1, 1)
        position = Point(0, 0, 0)
        light = Light(position, intensity)
        self.assertEqual((light.position, light.intensity), (position, intensity))

import unittest
import math

from features.light import Light
from features.material import Material
from features.tuple import Color, Point, Vector

class TestMaterial(unittest.TestCase):
    def test_default(self):
        m = Material()
        self.assertEqual(m.color, Color(1, 1, 1))
        self.assertEqual(m.ambient, 0.1)
        self.assertEqual(m.diffuse, 0.9)
        self.assertEqual(m.specular, 0.9)
        self.assertEqual(m.shininess, 200.0)

    def test_lighting(self):
        m = Material()
        position = Point(0, 0, 0)

        # lighting: eye between light and surface
        eyev = Vector(0, 0, -1)
        normalv = Vector(0, 0, -1)
        light = Light(Point(0, 0, -10), Color(1, 1, 1))
        result = m.lighting(light, position, eyev, normalv)
        self.assertEqual(result, Color(1.9, 1.9, 1.9))

        # lighting: eye between light and surface, eye offset 45deg
        eyev = Vector(0, math.sqrt(2)/2, -math.sqrt(2)/2)
        normalv = Vector(0, 0, -1)
        light = Light(Point(0, 0, -10), Color(1, 1, 1))
        result = m.lighting(light, position, eyev, normalv)
        self.assertEqual(result, Color(1.0, 1.0, 1.0))

        # lighting: eye opposite surface, eye offset 45deg
        eyev = Vector(0, 0, -1)
        normalv = Vector(0, 0, -1)
        light = Light(Point(0, 10, -10), Color(1, 1, 1))
        result = m.lighting(light, position, eyev, normalv)
        self.assertEqual(result, Color(0.7364, 0.7364, 0.7364))

        # lighting: eye in path of reflection vector
        eyev = Vector(0, -math.sqrt(2)/2, -math.sqrt(2)/2)
        normalv = Vector(0, 0, -1)
        light = Light(Point(0, 10, -10), Color(1, 1, 1))
        result = m.lighting(light, position, eyev, normalv)
        self.assertEqual(result, Color(1.6364, 1.6364, 1.6364))

        # lighting: light behind surface
        eyev = Vector(0, 0, -1)
        normalv = Vector(0, 0, -1)
        light = Light(Point(0, 0, 10), Color(1, 1, 1))
        result = m.lighting(light, position, eyev, normalv)
        self.assertEqual(result, Color(0.1, 0.1, 0.1))

    def test_in_shadow(self):
        m = Material()
        position = Point(0, 0, 0)
        eyev = Vector(0, 0, -1)
        normalv = Vector(0, 0, -1)
        light = Light(Point(0, 0, -10), Color(1, 1, 1))
        result = m.lighting(light, position, eyev, normalv, in_shadow=True)
        self.assertEqual(result, Color(0.1, 0.1, 0.1))

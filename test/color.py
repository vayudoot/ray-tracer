import unittest

from features.tuple import Color

class TestColor(unittest.TestCase):
    def test_color(self):
        c = Color(-0.5, 0.4, 1.7)
        self.assertEqual(c.red, -0.5)
        self.assertEqual(c.green, 0.4)
        self.assertEqual(c.blue, 1.7)

    def test_operation(self):
        c1 = Color(0.9, 0.6, 0.75)
        c2 = Color(0.7, 0.1, 0.25)
        self.assertEqual(c1 + c2, Color(1.6, 0.7, 1.0))
        self.assertEqual(c1 - c2, Color(0.2, 0.5, 0.5))
        self.assertEqual(c1 * 2, Color(1.8, 1.2, 1.5))
        self.assertEqual(c1 * c2, Color(0.63, 0.06, 0.1875))

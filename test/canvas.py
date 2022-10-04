import unittest

from features.canvas import Canvas
from features.tuple import Color

class TestCanvas(unittest.TestCase):
    def test_canvas(self):
        c = Canvas(10, 20)
        self.assertEqual(c.width, 10)
        self.assertEqual(c.height, 20)
        for row in c.grid:
            self.assertEqual(row, [Color(0, 0, 0)] * c.width)

    def test_write_pixels(self):
        c = Canvas(10, 20)
        red = Color(1, 0, 0)
        c.write_pixel(2, 3, red)
        self.assertEqual(c.pixel_at(2, 3), red)

    def test_ppm_header(self):
        c = Canvas(5, 3)
        ppm = c.to_ppm().splitlines()
        ppm_header = [s.strip() for s in ppm][0:3]
        self.assertEqual(ppm_header, ["P3", "5 3", "255"])

    def test_pixel_data(self):
        c = Canvas(5, 3)
        c.write_pixel(0, 0, Color(1.5, 0, 0))
        c.write_pixel(2, 1, Color(0, 0.5, 0))
        c.write_pixel(4, 2, Color(-0.5, 0, 1))
        ppm = c.to_ppm().splitlines()
        pixel_data = [s.strip() for s in ppm][3:6]
        expected_data = [
            "255 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 0 0 0 0 0 0 128 0 0 0 0 0 0 0",
            "0 0 0 0 0 0 0 0 0 0 0 0 0 0 255",
        ]
        self.assertEqual(pixel_data, expected_data)

    def test_line_length(self):
        c = Canvas(10, 2, Color(1, 0.8, 0.6))
        ppm = c.to_ppm().splitlines()
        pixel_data = [s.strip() for s in ppm][3:7]
        expected_data = [
            "255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204",
            "153 255 204 153 255 204 153 255 204 153 255 204 153",
            "255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204",
            "153 255 204 153 255 204 153 255 204 153 255 204 153",
        ]
        self.assertEqual(pixel_data, expected_data)

    def test_EOF(self):
        c = Canvas(5, 3)
        ppm = c.to_ppm()
        self.assertTrue(ppm.endswith("\n"))

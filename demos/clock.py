import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import math
from features.canvas import Canvas
from features.matrix import Rotation, Translation
from features.tuple import Color, Point

if __name__ == "__main__":
    CANVAS_SIZE = 200
    twelve = Point(0, 1, 0)
    c = Canvas(CANVAS_SIZE, CANVAS_SIZE)
    RADIUS = 3/8 * CANVAS_SIZE
    for i in range(12):
        p = Rotation(0, 0, i * math.pi / 6) * twelve
        x = int(p.x * RADIUS + CANVAS_SIZE / 2)
        y = int(p.y * RADIUS + CANVAS_SIZE / 2)
        c.write_pixel(x, y, Color(1, 1, 1))

    with open("images/clock.ppm", "w") as ppm_file:
        ppm_file.write(c.to_ppm())

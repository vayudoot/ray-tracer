import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import math

from features.canvas import Canvas
from features.matrix import Rotation, Scaling, Shearing
from features.ray import Ray
from features.shape import Sphere
from features.tuple import Point, Color

if __name__ == "__main__":
    wall_z = 10
    wall_size = 7.0
    canvas_pixels = 140
    pixel_size = wall_size / canvas_pixels
    half = wall_size / 2

    ray_origin = Point(0, 0, -5)
    canvas = Canvas(canvas_pixels, canvas_pixels)
    color = Color(1, 0, 0)
    shape = Sphere()
    #shape.transform = Rotation(0, 0, math.pi / 4) * Scaling(0.5, 1, 1)
    shape.transform = Shearing(1, 0, 0, 0, 0, 0) * Scaling(0.5, 1, 1)
    for y in range(canvas_pixels):
        world_y = half - pixel_size * y
        for x in range(canvas_pixels):
            world_x = -half + pixel_size * x
            position = Point(world_x, world_y, wall_z)
            v = (position - ray_origin).normalize()
            r = Ray(ray_origin, v)
            xs = shape.intersect(r)
            if xs.hit():
                canvas.write_pixel(x, y, color)

    with open("images/sphere.ppm", "w") as ppm_file:
        ppm_file.write(canvas.to_ppm())

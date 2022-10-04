import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import math

from features.canvas import Canvas
from features.light import Light
from features.material import Material
from features.matrix import Rotation, Scaling, Shearing
from features.ray import Ray
from features.shape import Sphere
from features.tuple import Color, Point

if __name__ == "__main__":
    wall_z = 10
    wall_size = 7.0
    canvas_pixels = 100
    pixel_size = wall_size / canvas_pixels
    half = wall_size / 2

    ray_origin = Point(0, 0, -5)
    canvas = Canvas(canvas_pixels, canvas_pixels)
    shape = Sphere()
    shape.material = Material(c=Color(1, 0.2, 1))
    # shape.transform = Shearing(1, 0, 0, 0, 0, 0) * Scaling(0.45, 1, 1)
    light = Light(Point(-10, 10, -10), Color(1, 1, 1))

    for y in range(canvas_pixels):
        world_y = half - pixel_size * y
        for x in range(canvas_pixels):
            world_x = -half + pixel_size * x
            position = Point(world_x, world_y, wall_z)
            v = (position - ray_origin).normalize()
            r = Ray(ray_origin, v)
            xs = shape.intersect(r)
            hit = xs.hit()
            if hit:
                point = r.position(hit.t)
                normal = hit.obj.normal_at(point)
                eye = -r.direction
                c = hit.obj.material.lighting(light, point, eye, normal)
                canvas.write_pixel(x, y, c)

    with open("images/sphere_light.ppm", "w") as ppm_file:
        ppm_file.write(canvas.to_ppm())

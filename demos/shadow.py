import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import math

from features.camera import Camera
from features.light import Light
from features.material import Material
from features.matrix import Rotation, Scaling, Translation, view_transform
from features.shape import Sphere
from features.tuple import Color, Point, Vector
from features.world import World

def floor():
    floor = Sphere()
    floor.transform = Scaling(10, 0.01, 10)
    floor.material = Material(c=Color(1, 0.9, 0.9), sp=0)
    return floor

def left_wall():
    wall = Sphere()
    # or use wall.set_transform(Trans...)
    wall.transform = Translation(0, 0, 5) * Rotation(y_rad=-math.pi/4) * Rotation(x_rad=math.pi/2) * Scaling(10, 0.01, 10)
    wall.material = Material(c=Color(1, 0.9, 0.9), sp=0)
    return wall

def right_wall():
    wall = Sphere()
    wall.transform = Translation(-2, 0, 5) * Rotation(y_rad=math.pi/4) * Rotation(x_rad=math.pi/2) * Scaling(10, 0.01, 10)
    wall.material = Material(c=Color(1, 0.9, 0.9), sp=0)
    return wall

def middle_sphere():
    s = Sphere()
    s.transform = Translation(-1.0, 1, -2.0)
    s.material = Material(c=Color(0.1, 1, 0.5), d=0.7, sp=0.3)
    return s

def right_sphere():
    s = Sphere()
    s.transform = Translation(1.2, 1.5, 0.5) * Scaling(1, 0.1, 1)
    s.material = Material(c=Color(0.5, 1, 0.1), d=0.7, sp=0.3)
    return s

def left_sphere():
    s = Sphere()
    s.transform = Translation(1.2, 0.5, 0.5) * Scaling(1, 0.3, 1)
    s.material = Material(c=Color(1, 0.8, 0.1), d=0.7, sp=0.3)
    return s

if __name__ == "__main__":
    w = World()
    w.light = Light(Point(-10, 5, -10), Color(1, 1, 1))
    #w.objects.append(floor())
    w.objects.append(left_wall())
    w.objects.append(right_wall())
    w.objects.append(middle_sphere())
    w.objects.append(right_sphere())
    w.objects.append(left_sphere())

    c = Camera(100, 50, math.pi/2)
    c.transform = view_transform(Point(0, 1.5, -5), Point(0, 1, 0), Vector(0, 1, 0))
    canvas = c.render(w)

    with open("images/shadow.ppm", "w") as ppm_file:
        ppm_file.write(canvas.to_ppm())

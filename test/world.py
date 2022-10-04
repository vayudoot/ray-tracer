import unittest

from features.intersection import Intersection
from features.light import Light
from features.material import Material
from features.matrix import Scaling, Translation
from features.ray import Ray
from features.shape import Sphere
from features.tuple import Color, Point, Vector
from features.world import World

class TestWorld(unittest.TestCase):
    def test_default(self):
        s1 = Sphere(material=Material(c=Color(0.8, 1.0, 0.6), d=0.7, sp=0.2))
        s2 = Sphere()
        s2.set_transform(Scaling(0.5, 0.5, 0.5))
        light = Light(Point(-10, 10, -10), Color(1, 1, 1))
        w = World.default()
        self.assertEqual(w.light, light)
        self.assertIn(s1, w.objects)
        self.assertIn(s2, w.objects)

    def test_intersect_ray(self):
        w = World.default()
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        xs = w.intersect(r)
        self.assertEqual(xs.count, 4)
        self.assertListEqual([xs[0].t, xs[1].t, xs[2].t, xs[3].t],
                             [4, 4.5, 5.5, 6])

    def test_shade_hit(self):
        w = World.default()
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = w.objects[0]
        i = Intersection(4, shape)
        comps = i.prepare_computations(r)
        c = w.shade_hit(comps)
        self.assertEqual(c, Color(0.38066, 0.47583, 0.2855))

    #@unittest.skip
    def test_shade_hit_inside(self):
        w = World.default()
        w.light = Light(Point(0, 0.25, 0), Color(1, 1, 1))
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        shape = w.objects[1]
        i = Intersection(0.5, shape)
        comps = i.prepare_computations(r)
        c = w.shade_hit(comps)
        self.assertEqual(c, Color(0.90498, 0.90498, 0.90498))

    def test_color_at_miss(self):
        w = World.default()
        r = Ray(Point(0, 0, -5), Vector(0, 1, 0))
        c = w.color_at(r)
        self.assertEqual(c, Color(0, 0, 0))

    def test_color_at_hit(self):
        w = World.default()
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        c = w.color_at(r)
        self.assertEqual(c, Color(0.38066, 0.47583, 0.2855))

    def test_color_at_between(self):
        w = World.default()
        outer = w.objects[0]
        outer.material.ambient = 1
        inner = w.objects[1]
        inner.material.ambient = 1
        r = Ray(Point(0, 0, 0.75), Vector(0, 0, -1))
        c = w.color_at(r)
        self.assertEqual(c, inner.material.color)

    def test_in_shadow(self):
        w = World.default()
        # no shadow (object not collinear with light and point)
        self.assertFalse(w.is_shadowed(Point(0, 10, 0)))
        # shadow (light -> object -> point)
        self.assertTrue(w.is_shadowed(Point(10, -10, 10)))
        # no shadow (object -> light -> point)
        self.assertFalse(w.is_shadowed(Point(-20, 20, -20)))
        # no shadow (light -> point -> object)
        self.assertFalse(w.is_shadowed(Point(-2, 2, -2)))

    #@unittest.expectedFailure
    def test_shade_hit_shadowed(self):
        w = World(light=Light(Point(0, 0, -10), Color(1, 1, 1)))
        s1 = Sphere()
        w.objects.append(s1)
        s2 = Sphere()
        s2.transform = Translation(0, 0, 10)
        w.objects.append(s2)
        r = Ray(Point(0, 0, 5), Vector(0, 0, 1))
        i = Intersection(4, s2)
        comps = i.prepare_computations(r)
        c = w.shade_hit(comps)
        self.assertEqual(c, Color(0.1, 0.1, 0.1))

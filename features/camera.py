from __future__ import annotations

import numpy as np

from features.canvas import Canvas
from features.matrix import Matrix
from features.tuple import Point
from features.ray import Ray
from features.world import World

class Camera:
    def __init__(self, hsize, vsize, fov, transform: Matrix = None):
        self.hsize = hsize
        self.vsize = vsize
        self.fov = fov
        self.transform = Matrix.identity(4) if not transform else transform
        self.half_width, self.half_height, self.pixel_size = self._pixel_size()

    def _pixel_size(self) -> float:
        half_view = np.tan(self.fov / 2)
        aspect = self.hsize / self.vsize
        if aspect >= 1:
            half_width = half_view
            half_height = half_view / aspect
        else:
            half_width = half_view * aspect
            half_height = half_view
        pixel_size = (half_width * 2) / self.hsize
        return half_width, half_height, pixel_size

    def ray_for_pixel(self, x, y) -> Ray:
        xoffset = (x + 0.5) * self.pixel_size
        yoffset = (y + 0.5) * self.pixel_size
        world_x = self.half_width - xoffset
        world_y = self.half_height - yoffset
        pixel = self.transform.inverse() * Point(world_x, world_y, -1)
        origin = self.transform.inverse() * Point(0, 0, 0)
        direction = (pixel - origin).normalize()
        return Ray(origin, direction)

    def render(self, w: World) -> Canvas:
        image = Canvas(self.hsize, self.vsize)
        for y in range(self.vsize):
            for x in range(self.hsize):
                ray = self.ray_for_pixel(x, y)
                color = w.color_at(ray)
                image.write_pixel(x, y, color)
        return image

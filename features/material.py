from __future__ import annotations

import math

from features.tuple import Color

class Material:
    def __init__(self, c=Color(1, 1, 1), a=0.1, d=0.9, sp=0.9, sh=200.0):
        self.color = c
        self.ambient = a
        self.diffuse = d
        self.specular = sp
        self.shininess = sh

    def __eq__(self, other):
        return (isinstance(other, Material) and
                self.color == other.color and
                self.ambient == other.ambient and
                self.diffuse == other.diffuse and
                self.specular == other.specular and
                self.shininess == other.shininess)

    def lighting(self, light, point, eyev, normalv, in_shadow=False) -> Tuple:
        # combine surface color with light's color/intensity
        effective_color = self.color * light.intensity
        
        # find direction to the light source
        lightv = (light.position - point).normalize()

        # compute ambient contribution
        ambient = effective_color * self.ambient
        if in_shadow:
            return ambient

        light_dot_normal = lightv.dot(normalv)
        if light_dot_normal < 0:
            diffuse = Color(0, 0, 0)
            specular = Color(0, 0, 0)
        else:
            diffuse = effective_color * self.diffuse * light_dot_normal
            reflectv = -lightv.reflect(normalv)
            reflect_dot_eye = reflectv.dot(eyev)
            if reflect_dot_eye <= 0:
                specular = Color(0, 0, 0)
            else:
                factor = math.pow(reflect_dot_eye, self.shininess)
                specular = light.intensity * self.specular * factor

        return ambient + diffuse + specular

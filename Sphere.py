from Vec3 import *
from Ray import *
import math

class Sphere:
    def __init__(self, origin : Vec3, radius : float) -> None:
        self.material = None
        self.origin = origin
        self.radius = radius
        self.r2 = self.radius * self.radius

    def is_inside(self, point) -> bool:
        dist = self.origin - point
        if dist.length() > self.radius:
            return False
        else:
            return True

    def hit_test(self, ray = Ray, clip_backface = True) -> float:
        if self.material is None:
            return float('inf')
        offset_v = ray.origin - self.origin
        a = Vec3.Dot(offset_v, offset_v)
        if clip_backface and a < self.r2:
            return float('inf')
        b = Vec3.Dot(offset_v, ray.direction)
        c = Vec3.Dot(ray.direction, ray.direction)
        if math.fabs(2 * c) < 1e-7:
            return float('inf')
        b2_4ac = 4 * b * b - 4 * c * (a - self.r2)
        if b2_4ac < 0:
            return float('inf')
        s = math.sqrt(b2_4ac)
        t1 = (-2 * b + s) / (2 * c)
        t2 = (-2 * b - s) / (2 * c)
        if t2 > 0:
            return t2
        if t1 > 0:
            return t1
        return float('inf')

    def normal(self, point : Vec3) -> Vec3:
        d = point - self.origin
        if math.fabs(d.length() - self.radius) < 1e-7:
            raise BaseException()
        return Vec3.Normalize(d)

    def set_material(self, mat):
        self.material = mat

    def get_material(self):
        return self.material

__all__ = ['Sphere']

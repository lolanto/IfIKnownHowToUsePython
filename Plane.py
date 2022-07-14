from turtle import up
from Vec3 import *
from Ray import *
import math

class Plane:
    def __init__(self, origin : Vec3, normal : Vec3, width : float, height : float) -> None:
        self.material = None
        self.origin = origin
        self.toward = Vec3.Normalize(normal)
        if math.fabs(self.toward.y) > 0.999:
            if self.toward.y > 0.999:
                self.tangent = X_AXIS
                self.bitangent = -Z_AXIS
            else:
                self.tangent = -X_AXIS
                self.bitangent = Z_AXIS
        else:
            self.tangent = Vec3.Cross(UP, self.toward)
            self.bitangent = Vec3.Cross(self.toward, self.tangent)
        self.tangent = Vec3.Normalize(self.tangent)
        self.bitangent = Vec3.Normalize(self.bitangent)
        self.width = width
        self.height = height
        self.extent_x = self.width / 2
        self.extent_y = self.height / 2
        pass

    def hit_test(self, ray : Ray, clip_backface = True) -> float:
        if self.material is None:
            return float('inf')
        if clip_backface and Vec3.Dot(self.toward, ray.direction) > 0:
            return float('inf')
        offset_v = self.origin - ray.origin
        t = Vec3.Dot(offset_v, -self.toward)
        if t < 0:
            return float('inf')
        ray_direction_dot_neg_normal = Vec3.Dot(ray.direction, -self.toward)
        if (math.fabs(ray_direction_dot_neg_normal) < 1e-7):
            return float('inf')
        t = t / ray_direction_dot_neg_normal
        p = ray.eval(t)
        p = p - self.origin
        ox = Vec3.Dot(p, self.tangent)
        oy = Vec3.Dot(p, self.bitangent)
        if math.fabs(ox) < self.extent_x and math.fabs(oy) < self.extent_y:
            return t
        return float('inf')
        

    def normal(self, point : Vec3) -> Vec3:
        return self.toward

    def set_material(self, mat):
        self.material = mat

    def get_material(self):
        return self.material

__all__ = ['Plane']

if __name__ == '__main__':
    import unittest

    class Test(unittest.TestCase):
        def test_init(self):
            p = Plane(Vec3(), UP, 1, 1)
            self.assertAlmostEqual(p.toward.y, 1.0)
            self.assertAlmostEqual(p.tangent.x, 1.0)
            self.assertAlmostEqual(p.bitangent.z, -1.0)
            p = Plane(Vec3(), -UP, 1, 1)
            self.assertAlmostEqual(p.toward.y, -1.0)
            self.assertAlmostEqual(p.tangent.x, -1.0)
            self.assertAlmostEqual(p.bitangent.z, 1.0)
            p = Plane(Vec3(), Vec3(0.577350269189, 0.577350269189, 0.577350269189), 1, 1)
            self.assertAlmostEqual(p.toward.length(), 1.0)
            self.assertAlmostEqual(p.tangent.x, 0.70710678118654)
            self.assertAlmostEqual(p.tangent.y, 0)
            self.assertAlmostEqual(p.tangent.z, -0.70710678118654)
            self.assertAlmostEqual(p.bitangent.x, -0.4082482904638)
            self.assertAlmostEqual(p.bitangent.y, 0.8164965809277)
            self.assertAlmostEqual(p.bitangent.z, -0.4082482904638)
            pass

        def test_hit_test(self):
            p = Plane(Vec3(), Vec3(0.577350269189, 0.577350269189, 0.577350269189), 1, 1)
            r = Ray(Vec3(0.577350269, 0.577350269, 0.577350269), -Vec3(0.577350269, 0.577350269, 0.577350269))
            t = p.hit_test(r)
            self.assertAlmostEqual(t, 1.0)
            r = Ray(Vec3(0.577350269, 0.577350269, 0.577350269), Vec3(0, 0, 1))
            t = p.hit_test(r)
            self.assertAlmostEqual(t, float('inf'))
            r = Ray(Vec3(0.577350269, 0.577350269, 0.577350269), Vec3(0.577350269, 0.577350269, 0.577350269))
            t = p.hit_test(r)
            self.assertAlmostEqual(t, float('inf'))
            r = Ray(Vec3(0.577350269, 0.577350269, 0.577350269), Vec3(0, 0, 1))
            t = p.hit_test(r)
            self.assertAlmostEqual(t, float('inf'))

        def test_history_bug(self):
            p = Plane(Vec3(0, 0, 5), Vec3(0, 0, -1), 2, 1)
            r = Ray(Vec3(), Vec3(1, 0, 0.1))
            t = p.hit_test(r)
            self.assertAlmostEqual(t, float('inf'))
            p = Plane(Vec3(0, -5, 10), Vec3(0, 1, 0), 10, 10)
            r = Ray(Vec3(0.0, -0.005, 0.025), Vec3(0.0, -0.19611613513818404, 0.9805806756909202))
            t = p.hit_test(r)
            self.assertAlmostEqual(t, float('inf'))

    unittest.main()

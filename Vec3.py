from encodings import utf_8_sig


# -*- coding: utf-8 -*-
import math
from tokenize import Number

class Vec3:
    def __init__(self, x = 0, y = 0, z=0) -> None:
        self.x = x
        self.y = y
        self.z = z
    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __truediv__(self, scalar_value):
        if isinstance(scalar_value, (int, float)) is False:
            raise TypeError(type(scalar_value))
        if math.fabs(scalar_value) < 1e-7:
            raise ZeroDivisionError(scalar_value)
        return Vec3(self.x / scalar_value, self.y / scalar_value, self.z / scalar_value)

    def __mul__(self, scalar_value):
        if isinstance(scalar_value, (int, float)) is False:
            raise TypeError(type(scalar_value))
        return Vec3(self.x * scalar_value, self.y * scalar_value, self.z * scalar_value)

    @staticmethod
    def Dot(a, b):
        return a.x * b.x + a.y * b.y + a.z * b.z

    @staticmethod
    def Cross(a, b):
        return Vec3(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)

    @staticmethod
    def Normalize(a):
        if math.fabs(a.x) < 1e-7 and math.fabs(a.y) < 1e-7 and math.fabs(a.z) < 1e-7:
            raise ZeroDivisionError(a)
        return a / a.length()

X_AXIS = Vec3(1, 0, 0)
Y_AXIS = UP = Vec3(0, 1, 0)
Z_AXIS = Vec3(0, 0, 1)

__all__ = ['Vec3', 'X_AXIS', 'Y_AXIS', 'UP', 'Z_AXIS']

if __name__ == '__main__':
    import unittest
    class Test(unittest.TestCase):
        def test_init(self):
            a = Vec3(0, 1.0, 1e-3)
            self.assertEqual(a.x, 0)
            self.assertEqual(a.y, 1.0)
            self.assertEqual(a.z, 1e-3)

        def test_length(self):
            a = Vec3(-1.2, 1.57, 1e-3)
            self.assertAlmostEqual(a.length(), 1.97608, 4)

        def test_sub(self):
            a = Vec3(0.2, 0.4, 1.3)
            b = Vec3(1.0, 2.4, -3.7)
            c = a - b
            self.assertEqual(c.x, -0.8)
            self.assertEqual(c.y, -2.0)
            self.assertEqual(c.z, 5.0)

        def test_div(self):
            a = Vec3(-4.3, 2.1, 1.2)
            b = a / 0.5
            self.assertEqual(b.x, -8.6, 4)
            self.assertEqual(b.y, 4.2)
            self.assertEqual(b.z, 2.4)
            with self.assertRaises(ZeroDivisionError):
                a / 0
            with self.assertRaises(TypeError):
                a / None

        def test_mul(self):
            a = Vec3(2.22, 3.15, 0)
            b = a * 3.1
            self.assertAlmostEqual(b.x, 6.882)
            self.assertAlmostEqual(b.y, 9.765)
            self.assertEqual(b.z, 0)
            with self.assertRaises(TypeError):
                a * None

        def test_dot(self):
            a = Vec3(1.2, -4.3, 0)
            b = Vec3(-3.1, 0, 4.4)
            c = Vec3.Dot(a, b)
            self.assertAlmostEqual(c, -3.72)

        def test_cross(self):
            a = Vec3(2.0, 3.1, 4.5)
            b = Vec3(-3.4, -2.2, 0)
            c = Vec3.Cross(a, b)
            self.assertAlmostEqual(c.x, 9.9)
            self.assertAlmostEqual(c.y, -15.3)
            self.assertAlmostEqual(c.z, 6.14)

        def test_normalize(self):
            a = Vec3(3.14, -4.15, 0)
            b = Vec3.Normalize(a)
            self.assertAlmostEqual(b.x, 0.60337662211552823)
            self.assertAlmostEqual(b.y, -0.797456363624026)
            self.assertEqual(b.z, 0)
            with self.assertRaises(ZeroDivisionError):
                Vec3.Normalize(Vec3())

    unittest.main()

from Vec3 import *

class Ray:
    def __init__(self, origin = Vec3, direction = Vec3) -> None:
        self.origin = origin
        self.direction = Vec3.Normalize(direction)
        pass

    def eval(self, t : float) -> Vec3:
        return self.origin + self.direction * t

    def __str__(self):
        return 'origin: {0}\ndirection: {1}'.format(str(self.origin), str(self.direction))

__all__ = ['Ray']
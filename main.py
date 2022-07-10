import math
import sys
import time
from Vec3 import *

class Vec2:
    def __init__(self, x = 0, y = 0) -> None:
        self.x = x
        self.y = y

class Film:
    def __init__(self, width = int, height = int) -> None:
        self.width = width
        self.height = height
        self.data = [None] * width * height
        pass

    def access(self, x = int, y = int) -> Vec3:
        if y >= self.height or y < 0 or x >= self.width or x < 0:
            raise IndexError()
        return self.data[x + self.width * y]

    def write(self, x = int, y = int, value = Vec3) -> None:
        if y >= self.height or y < 0 or x >= self.width or x < 0:
            raise IndexError()
        self.data[x + self.width * y] = value
        pass

    def save(self, file_path) -> bool:
        file_name = '{0}/image_{1}.ppm'.format(file_path, time.strftime('%H-%M-%S-%d-%m-%Y', time.localtime()))
        f = open(file_name, 'w+')
        with(f):
            f.write('P3\n')
            f.write('{0} {1}\n'.format(self.width, self.height))
            f.write('255\n')
            index = 0
            for y in range(self.height):
                for x in range(self.width):
                    pixel = self.data[index]
                    if isinstance(pixel, Vec3) is False:
                        pixel = Vec3()
                    pixel_str = '{0}{1} {2} {3}'.format('' if x == 0 else ' ', int(pixel.x * 255), int(pixel.y * 255), int(pixel.z * 255))
                    f.write(pixel_str)
                    index += 1
                f.write('\n')
        return True

class Ray:
    def __init__(self, origin = Vec3, direction = Vec3) -> None:
        self.origin = origin
        self.direction = direction
        pass

class Scene:
    def __init__(self) -> None:
        self.object_list = []
        pass

    def add_object(self, object) -> None:
        self.object_list.append(object)

    def eval(self, ray = Ray) -> Vec3:
        for obj in self.object_list:
            t = obj.hit_test(ray)
            if t < 0:
                return Vec3()
            else:
                return Vec3(0.2, 0.4, 0.6)

class Camera:
    def __init__(self, pos = Vec3, dir = Vec3, focal_length = float, film = Film, film_width = float) -> None:
        self.pos = pos
        self.forward = dir
        self.right = Vec3.Normalize(Vec3.Cross(UP, self.forward))
        self.upward = Vec3.Normalize(Vec3.Cross(self.forward, self.right))
        self.focal_length = focal_length
        self.film = film
        self.film_aspect = film.width / film.height
        self.film_size = Vec2(film_width, film_width / self.film_aspect)
        self.scene = None
        pass

    def put_in_scene(self, scene = Scene):
        self.scene = scene

    def shoot(self) -> None:
        FILM_WIDTH_PIX = self.film.width
        FILM_HEIGHT_PIX = self.film.height
        OFFSET_HORIZON_WOR = self.film_size.x / FILM_WIDTH_PIX
        OFFSET_VERTICAL_WOR = self.film_size.y / FILM_HEIGHT_PIX
        FILM_CENTER_WOR = self.pos - self.forward * self.focal_length
        if self.scene is None:
            self.film.save('./result')
            return
        for y in range(-FILM_HEIGHT_PIX // 2, FILM_HEIGHT_PIX // 2, 1):
            for x in range(-FILM_WIDTH_PIX // 2, FILM_WIDTH_PIX // 2, 1):
                origin = FILM_CENTER_WOR + self.right * OFFSET_HORIZON_WOR * x + self.upward * OFFSET_VERTICAL_WOR * y
                direction = Vec3.Normalize(self.pos - origin)
                new_ray = Ray(origin, direction)
                result = self.scene.eval(new_ray)
                self.film.write(x + FILM_WIDTH_PIX // 2, y + FILM_HEIGHT_PIX // 2, result)
        self.film.save('./result')

    def central_ray(self) -> Ray:
        FILM_CENTER_WOR = self.pos - self.forward * self.focal_length
        origin = FILM_CENTER_WOR
        direction = Vec3.Normalize(self.pos - origin)
        return Ray(origin, direction)

class Sphere:
    def __init__(self, origin : Vec3, radius : float) -> None:
        self.origin = origin
        self.radius = radius

    def is_inside(self, point) -> bool:
        dist = self.origin - point
        if dist.length() > self.radius:
            return False
        else:
            return True

    def hit_test(self, ray = Ray) -> float:
        offset_v = ray.origin - self.origin
        a = Vec3.Dot(offset_v, offset_v)
        b = Vec3.Dot(offset_v, ray.direction)
        c = Vec3.Dot(ray.direction, ray.direction)
        if math.fabs(2 * c) < 1e-7:
            return -1
        b2_4ac = 4 * b * b - 4 * c * (a - self.radius * self.radius)
        if b2_4ac < 0:
            return -1
        s = math.sqrt(b2_4ac)
        t1 = (-2 * b + s) / (2 * c)
        t2 = (-2 * b - s) / (2 * c)
        if t2 > 0:
            return t2
        elif t1 > 0:
            return t1
        return -1

if __name__ == '__main__':
    WIDTH = 512
    HEIGHT = 512
    F = Film(WIDTH, HEIGHT)
    C = Camera(Vec3(), Vec3(0, 0, 1), 0.001, F, 0.01)
    S = Scene()
    Sp = Sphere(Vec3(0, 0, 5), 1)
    S.add_object(Sp)
    r = C.central_ray()
    C.put_in_scene(S)
    C.shoot()
    

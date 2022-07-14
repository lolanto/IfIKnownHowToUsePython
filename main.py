import math
import Material
import time
from Plane import Plane
from Ray import *
from Sphere import *
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

    def write(self, x : int, y : int, value : Vec3) -> None:
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

class Scene:
    def __init__(self) -> None:
        self.object_list = []
        pass

    def add_object(self, object) -> None:
        self.object_list.append(object)

    def eval(self, ray = Ray) -> Vec3:
        mint = float('inf')
        material = None
        for obj in self.object_list:
            t = obj.hit_test(ray)
            if t < mint:
                mint = t
                material = obj.get_material()
        if mint < 1e3:
            return material.eval()
        else:
            return Vec3()

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
        FILM_LEFT_TOP_WOR = self.pos + self.forward * self.focal_length - self.right * (OFFSET_HORIZON_WOR * (FILM_WIDTH_PIX // 2)) + self.upward * (OFFSET_VERTICAL_WOR * (FILM_HEIGHT_PIX // 2))
        if self.scene is None:
            self.film.save('./result')
            return
        for y in range(0, FILM_HEIGHT_PIX, 1):
            for x in range(0, FILM_WIDTH_PIX, 1):
                origin = FILM_LEFT_TOP_WOR + self.right * OFFSET_HORIZON_WOR * x - self.upward * OFFSET_VERTICAL_WOR * y
                direction = Vec3.Normalize(origin - self.pos)
                new_ray = Ray(origin, direction)
                result = self.scene.eval(new_ray)
                self.film.write(x, y, result)
        self.film.save('./result')

    def central_ray(self) -> Ray:
        FILM_CENTER_WOR = self.pos + self.forward * self.focal_length
        origin = FILM_CENTER_WOR
        direction = Vec3.Normalize(origin - self.pos)
        return Ray(origin, direction)

    def debug_get_ray(self, pix_pos_x, pix_pos_y) -> Ray:
        FILM_WIDTH_PIX = self.film.width
        FILM_HEIGHT_PIX = self.film.height
        OFFSET_HORIZON_WOR = self.film_size.x / FILM_WIDTH_PIX
        OFFSET_VERTICAL_WOR = self.film_size.y / FILM_HEIGHT_PIX
        FILM_LEFT_TOP_WOR = self.pos + self.forward * self.focal_length - self.right * (OFFSET_HORIZON_WOR * (FILM_WIDTH_PIX // 2)) + self.upward * (OFFSET_VERTICAL_WOR * (FILM_HEIGHT_PIX // 2))
        origin = FILM_LEFT_TOP_WOR + self.right * OFFSET_HORIZON_WOR * pix_pos_x - self.upward * OFFSET_VERTICAL_WOR * pix_pos_y
        direction = Vec3.Normalize(origin - self.pos)
        return Ray(origin, direction)


if __name__ == '__main__':
    WIDTH = 512
    HEIGHT = 512
    F = Film(WIDTH, HEIGHT)
    my_position = Vec3(0, 1.7, -10)
    look_at = Vec3(0, 0, 0)
    direction = Vec3.Normalize(look_at - my_position)
    C = Camera(my_position, direction, 0.009, F, 0.01)
    # print(C.debug_get_ray(128, 256))
    S = Scene()
    Sp = Sphere(Vec3(0.5, 0.5, 0.5), 0.5)
    Sp.set_material(Material.Unlit(Vec3(1.0, 0, 0)))
    S.add_object(Sp)
    Pp = Plane(Vec3(0, 0, 0), Vec3(0, 1, 0), 10, 10)
    Pp.set_material(Material.Unlit(Vec3(0.0, 1.0, 0.0)))
    S.add_object(Pp)
    C.put_in_scene(S)
    C.shoot()    

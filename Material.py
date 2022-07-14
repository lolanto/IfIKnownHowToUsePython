from Vec3 import *

class Unlit:
    def __init__(self, color : Vec3) -> None:
        self.color = color
        pass

    def eval(self) -> Vec3:
        return self.color

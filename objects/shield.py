from arcade import *


class Shield(Sprite):
    def __init__(self, center_x=400, center_y=300):
        super().__init__("res/assets/def.png", center_x=center_x, center_y=center_y)
        self.direction = 'l'

    def direct(self, direction: str):
        self.direction = direction
        match direction:
            case 'l': self.angle = 270
            case 'u': self.angle = 0
            case 'r': self.angle = 90
            case 'd': self.angle = 180


from arcade import *


class Arrow(Sprite):
    TEXTURE_WIDTH = 48

    def __init__(self, arrive_time_sec: float, speed: float, direction: str, player_position: list[int]):
        d_pos = speed * arrive_time_sec
        x, y = player_position
        super().__init__("res/assets/arrow.png")

        match direction:
            case 'l':
                self.change_x = speed
                self.angle = 270
                x -= d_pos
            case 'r':
                self.change_x = -speed
                self.angle = 90
                x += d_pos
            case 'u':
                self.change_y = speed
                self.angle = 180
                y -= d_pos
            case 'd':
                self.change_y = -speed
                self.angle = 0
                y += d_pos

        self.center_x = x
        self.center_y = y

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time



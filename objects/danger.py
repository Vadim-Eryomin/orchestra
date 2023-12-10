from arcade import *


class Danger(Sprite):
    def __init__(self, center_x, center_y, time_to_fade=2, start_on=0):
        super().__init__('res/assets/danger.png', center_x=center_x, center_y=center_y)
        self.alpha = 0
        self.speed = 255 / time_to_fade
        self.before_start = start_on
        self.collider = DangerCollider(center_x, center_y)

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.before_start -= delta_time
        if self.before_start < 0:
            self.alpha += delta_time * self.speed


class DangerCollider(Sprite):
    def __init__(self, center_x, center_y):
        super().__init__('res/assets/danger_collider.png', center_x=center_x, center_y=center_y)

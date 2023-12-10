from arcade import *

from objects.shield import Shield


class Player(Sprite):
    def __init__(self, shield=Shield(), speed=300, center_x=400, center_y=300, text_x=30, text_y=30, start_hp=100):
        super().__init__('res/assets/playericon.png', center_x=center_x, center_y=center_y)
        self.hp = start_hp
        self.speed = Speed(speed)
        self.shield = shield
        self.hp_text = PlayerHp(text_x, text_y, self.hp)

        self.shield_visible = True
        self.can_move = True

    def draw(self, *, filter=None, pixelated=None, blend_function=None) -> None:
        super().draw(filter=filter, pixelated=pixelated, blend_function=blend_function)
        self.hp_text.draw()

    def on_update(self, delta_time: float = 1 / 60):
        d_pos = self.speed.calculate_speed()
        self.center_x += d_pos[0] * delta_time
        self.center_y += d_pos[1] * delta_time

        self.shield.center_x += d_pos[0] * delta_time
        self.shield.center_y += d_pos[1] * delta_time

    def set_hp(self, hp):
        self.hp = hp
        self.hp_text.set_hp(hp)

    def remove_hp(self, hp):
        self.set_hp(self.hp - hp)


class PlayerHp(Text):
    def __init__(self, start_x: int, start_y: int, hp=100):
        super().__init__('', start_x, start_y)
        self.hp = hp
        self.text = hp

    def set_hp(self, hp):
        self.hp = hp
        self.text = hp


class Speed:
    def __init__(self, speed_scale=500):
        self.speed_scale = speed_scale
        self.up = False
        self.right = False
        self.down = False
        self.left = False

    def calculate_speed(self):
        return ((0 - 1 if self.left else 0 + 1 if self.right else 0) * self.speed_scale,
                (0 + 1 if self.up else 0 - 1 if self.down else 0) * self.speed_scale)

from typing import Optional, Iterable

from arcade import *

from common.better_scene import BetterScene
from objects.arrow import Arrow
from objects.danger import Danger
from objects.player import Player
from objects.shield import Shield
from music_codes.night_of_nights import arrow_codes as night_arrows, danger_codes as night_dangers


class MyWindow(Window):

    def __init__(self):
        super().__init__(800, 600, "Orchestra")
        self.active_scene = PlayScene()

    def change_scene(self, scene: BetterScene):
        self.active_scene = scene

    def on_draw(self):
        self.active_scene.on_draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        print(x, y)

    def on_update(self, delta_time: float):
        self.active_scene.on_update(delta_time)

    def on_key_press(self, symbol: int, modifiers: int):
        self.active_scene.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int):
        self.active_scene.on_key_release(symbol, modifiers)


class DeathScene(BetterScene):

    def __init__(self) -> None:
        super().__init__()
        self.game_over = Sound('res/music/game_over.mp3')
        self.game_over.play()

    def on_draw(self):
        start_render()
        draw_text('Дед (нажми любую кнопку, чтобы возродиться)', start_x=10, start_y=10)
        finish_render()

    def on_key_press(self, symbol: int, modifiers: int):
        global window
        window.change_scene(PlayScene())


class PlayScene(BetterScene):

    def __init__(self) -> None:
        super().__init__()
        self.music = Sound('res/music/night-of-nights.mp3')
        self.audioPlayer = self.music.play()

        set_background_color((100, 100, 100, 255))

        self.arrows = SpriteList()
        self.dangers = SpriteList()
        self.mx = 0
        self.my = 0

        for code in night_arrows:
            self.arrows.append(Arrow(code[0], code[1] * 1.5, code[2], [400, 300]))
        for code in night_dangers:
            self.dangers.append(Danger(code[0], code[1], code[2], code[3]))

        self.shield = Shield()
        self.player = Player(self.shield)
        self.time_to_move = 22

    def on_update(self, delta_time: float = 1 / 60, names: Optional[Iterable[str]] = None) -> None:
        super().on_update(delta_time, names)
        self.arrows.on_update()
        self.player.on_update()
        self.dangers.on_update()

        for zone in self.dangers:
            if zone.alpha >= 254:
                if not self.player.collides_with_sprite(zone.collider):
                    self.player.remove_hp(5)
                zone.remove_from_sprite_lists()

        for arrow in check_for_collision_with_list(self.shield, self.arrows):
            arrow.remove_from_sprite_lists()

        for arrow in check_for_collision_with_list(self.player, self.arrows):
            arrow.remove_from_sprite_lists()
            self.player.remove_hp(10)

        self.time_to_move -= delta_time
        if self.player.hp <= 0:
            global window
            self.music.stop(self.audioPlayer)
            window.change_scene(DeathScene())

    def on_draw(self):
        start_render()
        self.arrows.draw()
        self.dangers.draw()
        self.player.draw()
        self.shield.draw()
        finish_render()

    def on_key_press(self, symbol: int, modifiers: int):
        if self.time_to_move < 0:
            if symbol == key.W: self.player.speed.up = True
            if symbol == key.A: self.player.speed.left = True
            if symbol == key.S: self.player.speed.down = True
            if symbol == key.D: self.player.speed.right = True

        if symbol == key.UP: self.shield.direct('u')
        if symbol == key.LEFT: self.shield.direct('l')
        if symbol == key.RIGHT: self.shield.direct('r')
        if symbol == key.DOWN: self.shield.direct('d')

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == key.W: self.player.speed.up = False
        if symbol == key.A: self.player.speed.left = False
        if symbol == key.S: self.player.speed.down = False
        if symbol == key.D: self.player.speed.right = False


window = MyWindow()
window.run()

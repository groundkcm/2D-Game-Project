import game_framework
from pico2d import *

import game_world


class Inven:

    def __init__(self):
        self.inventory = load_image('inventory.png')
        self.inven_but = load_image('inventory button.png')
        self.x_but = load_image('X Button.png')
        self.inven = 0

    def enter(boy, event):
        pass

    def exit(boy, event):
        pass

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 18
        self.timer -= 1
        if self.timer == 0:
            self.add_event(SLEEP_TIMER)

    def draw(self):
        if self.inven == 1:
            self.inventory.draw(400, 300)
            self.x_but.draw(750, 450)
        else:
            self.inven_but.draw(25, 575)

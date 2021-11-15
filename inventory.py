from pico2d import *
from boy import Boy

import game_world

# MLEFT_BUT_DOWN, MRIGHT_BUT_DOWN, MxPOS, MyPOS = range(3)
#
# mx, my = 0, 0
# key_event_table = {
#     (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT): MLEFT_BUT_DOWN,
#     (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_RIGHT): MRIGHT_BUT_DOWN,
#     (SDL_MOUSEMOTION, mx): MxPOS,
#     (SDL_MOUSEMOTION, my): MyPOS
# }

class Inven:

    def __init__(self):
        self.inventory = load_image('inventory.png')
        self.inven_but = load_image('inventory button.png')
        self.x_but = load_image('X Button.png')
        self.inven = 0
        self.events = 0

    def enter(boy, event):
        pass

    def exit(boy, event):
        pass

    def update(self):
        pass

    def handle_events(self):
        self.events = get_events()
        for event in self.events:
            if event.type == SDL_MOUSEBUTTONDOWN:
                ax, ay = event.x, 600 - event.y
                if self.inven == 0:
                    if event.button == SDL_BUTTON_LEFT and (ax - 10 < 50 and ay > 550):
                        self.inven = 1
                elif self.inven == 1:
                    if event.button == SDL_BUTTON_LEFT and (735 < ax - 10 < 765 and 435 < ay < 465):
                        self.inven = 0

    def do(self):
        pass

    def draw(self):
        if self.inven == 1:
            self.inventory.draw(400, 300)
            self.x_but.draw(750, 450)
        else:
            self.inven_but.draw(25, 575)

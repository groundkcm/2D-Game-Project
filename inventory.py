from pico2d import *
from boy import Boy

import game_world

# MLEFT_BUT_DOWN, MxPOS, MyPOS = range(3)
#
# ax, ay, inven = 0, 0, 0
# def handle_events():
#     global ax, ay, inven
#     events = get_events()
#     for event in events:
#         if event.type == SDL_MOUSEMOTION:
#             ax, ay = event.x, 600 - event.y
#
# key_event_table = {
#     (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT): MLEFT_BUT_DOWN,
#     (SDL_MOUSEMOTION, ax): MxPOS,
#     (SDL_MOUSEMOTION, ay): MyPOS
# }

class Inven:

    def __init__(self):
        self.inventory = load_image('inventory.png')
        self.inven_but = load_image('inventory button.png')
        self.x_but = load_image('X Button.png')
        self.event_que = []

    def enter(self, event):
        # global inven
        # if inven == 0:
        #     if event == MLEFT_BUT_DOWN and (ax - 10 < 50 and ay > 550):
        #         inven = 1
        # elif inven == 1:
        #     if event == MLEFT_BUT_DOWN and (735 < ax - 10 < 765 and 435 < ay < 465):
        #         inven = 0
        pass

    def exit(boy, event):
        pass

    # def handle_event(self, event):
    #     if (event.type, event.button) in key_event_table:
    #         key_event = key_event_table[(event.type, event.button)]
    #         self.add_event(key_event)

    # def add_event(self, event):
    #     self.event_que.insert(0, event)
    def handle_events(self):
        global ax, ay, inven
        events = get_events()
        for event in events:
            if event.type == SDL_MOUSEMOTION:
                ax, ay = event.x, 600 - event.y
            if event.type == SDL_MOUSEBUTTONDOWN:
                ax, ay = event.x, 600 - event.y
                if inven == 0:
                    if event.button == SDL_BUTTON_LEFT and (ax - 10 < 50 and ay > 550):
                        inven = 1
                elif inven == 1:
                    if event.button == SDL_BUTTON_LEFT and (735 < ax - 10 < 765 and 435 < ay < 465):
                        inven = 0

    # @staticmethod
    def update(self):
        pass

    def draw(self):
        global inven
        if inven == 1:
            self.inventory.draw(400, 300)
            self.x_but.draw(750, 450)
        else:
            self.inven_but.draw(25, 575)


Inven.handle_events()
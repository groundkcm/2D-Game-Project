from pico2d import *

import game_world

ax, ay, inven = 0, 0, 0

class Inven:
    mx, my = 55, 397
    drag = False
    def __init__(self):
        self.inventory = load_image('inventory.png')
        self.inven_but = load_image('inventory button.png')
        self.x_but = load_image('X Button.png')
        self.potion = load_image('red potion.png')
        self.event_que = []
        self.inven = 0

    def enter(self, event):
        pass

    def exit(boy, event):
        pass

    def handle_events(self):
        global ax, ay, inven
        events = get_events()
        for event in events:
            if event.type == SDL_MOUSEMOTION:
                ax, ay = event.x, 600 - event.y
            if event.type == SDL_MOUSEBUTTONDOWN:
                ax, ay = event.x, 600 - event.y
                if self.inven == 0:
                    if event.button == SDL_BUTTON_LEFT and (ax - 10 < 40 and ay > 560):
                        self.inven = 1
                elif self.inven == 1:
                    if event.button == SDL_BUTTON_LEFT and (730 < ax - 10 < 770 and 430 < ay < 470):
                        self.inven = 0
                    elif event.button == SDL_BUTTON_LEFT and (40 < ax - 10 < 70 and 365 < ay < 430):
                        Inven.drag = True
            elif event.type == SDL_MOUSEBUTTONUP and Inven.drag:
                ax, ay = event.x, 600 - event.y
                Inven.drag = False
                Inven.mx, Inven.my = ax, ay

    # @staticmethod
    def update(self):
        # pass
        self.handle_events()

    def draw(self):
        global ax, ay
        if self.inven == 1:
            self.inventory.draw(400, 300)
            self.x_but.draw(750, 450)
            if Inven.drag:
                self.potion.draw(ax, ay)
            else:
                self.potion.draw(Inven.mx, Inven.my)
        else:
            self.inven_but.draw(20, 580)


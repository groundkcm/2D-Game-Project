from pico2d import *
from boy import Boy

gretel = None

class Grass:
    def __init__(self):
        self.stage1 = load_image('background1.png')
        self.stage2 = load_image('background2.png')
        self.arrow = load_image('Arrow.png')
        self.inventory = load_image('inventory.png')
        self.inven_but = load_image('inventory button.png')
        self.x_but = load_image('X Button.png')
        self.inven = 0
        self.clear = None

    def update(self):
        pass

    # def camera_move(self):
    #     gretel = Boy()

    def draw(self):
        global gretel
        if gretel == None:
            gretel = Boy()
        # self.stage1.draw(400, 300)
        # self.inven_but.draw(25, 575)
        hide_cursor()
        WIDTH, HEIGHT = gretel.x, gretel.y
        # WIDTH, HEIGHT = 1280, 960
        if WIDTH >= 640:
            WIDTH = 640
        elif WIDTH <= 160:
            WIDTH = 160
        if HEIGHT >= 480:
            HEIGHT = 480
        elif HEIGHT <= 120:
            HEIGHT = 120
        if self.clear == 1:
            self.stage2.draw(WIDTH, HEIGHT)
        elif self.clear == 2:
            # self.stage3.draw(WIDTH, HEIGHT)
            pass
        elif self.clear == 3:
            # stage3.draw(WIDTH, HEIGHT)
            pass
        else:
            self.stage1.draw(WIDTH, HEIGHT)
        if self.inven == 1:
            self.inventory.draw(400, 300)
            self.x_but.draw(750, 450)
        else:
            self.inven_but.draw(25, 575)


class Wall:
    def __init__(self):
        self.stage1 = load_image('background1.png')
        self.stage2 = load_image('background2.png')
        self.arrow = load_image('Arrow.png')
        self.inventory = load_image('inventory.png')
        self.inven_but = load_image('inventory button.png')
        self.x_but = load_image('X Button.png')
        self.inven = 0
        self.clear = None
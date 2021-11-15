from pico2d import *
# from boy import Boy

gretel = None

# WIDTH, HEIGHT = 0, 0
class Grass:
    def __init__(self, x = 400, y = 90):
        self.stage1 = load_image('background1.png')
        self.stage2 = load_image('background2.png')
        self.arrow = load_image('Arrow.png')
        self.inventory = load_image('inventory.png')
        self.inven_but = load_image('inventory button.png')
        self.x_but = load_image('X Button.png')
        self.inven = 0
        self.clear = None
        self.x, self.y = x, y

    def update(self):
        global gretel
        # gretel = Boy()

    def draw(self):
        # global gretel, WIDTH, HEIGHT
        # if gretel == None:
        #     gretel = Boy()
        # hide_cursor()
        WIDTH, HEIGHT = 1280 - self.x * 2 + 160, 960 - self.y * 2 + 120
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
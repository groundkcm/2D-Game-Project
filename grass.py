from pico2d import *

class Grass:
    x, y = 400, 150
    items = []
    def __init__(self):

        self.stage1 = load_image('background1.png')
        self.door1 = 0, 0
        self.stage2 = load_image('background2.png')
        self.door2 = 0, 0
        self.arrow = load_image('Arrow.png')
        self.bgm = load_music('stage bgm.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()
        self.bgm = load_music('door.mp3')
        self.bgm.set_volume(32)
        self.clear = None

    def update(self):
        pass
        # self.x, self.y = inxy(gretel)
        # print(self.x)

    def draw(self):
        # hide_cursor()
        # print(self.x)
        WIDTH, HEIGHT = 1280 - Grass.x * 2 + 160, 960 - Grass.y * 2 + 120
        # WIDTH, HEIGHT = 400, 150
        if WIDTH >= 640:
            WIDTH = 640
        elif WIDTH <= 160:
            WIDTH = 160
        if HEIGHT >= 480:
            HEIGHT = 480
        elif HEIGHT <= 120:
            HEIGHT = 120
        if self.clear == 1:
            # self.stage2.draw(WIDTH, HEIGHT)
            pass
        elif self.clear == 2:
            # self.stage3.draw(WIDTH, HEIGHT)
            pass
        elif self.clear == 3:
            # stage3.draw(WIDTH, HEIGHT)
            pass
        else:
            # self.stage1.clip_draw(0 + Grass.x, 0 + Grass.y, 800, 600, Grass.x - 300, Grass.y - 250)
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
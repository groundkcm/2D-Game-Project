from pico2d import *
import server
from collision import collide

class Grass:
    def __init__(self):
        self.start = load_image('prison.png')
        self.stage1 = load_image('background1.png')
        self.stage2 = load_image('background2.png')
        self.stage3 = load_image('bossstage.png')
        self.door1 = 0, 0
        self.door2 = 0, 0
        self.door3 = 0, 0
        self.arrow = load_image('Arrow.png')
        self.bgm = load_music('stage bgm.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()
        self.open = load_music('door.mp3')
        self.open.set_volume(32)

    def update(self):
        pass

    def draw(self):
        # hide_cursor()
        WIDTH, HEIGHT = 1280 - server.x * 2 + 160, 960 - server.y * 2 + 120
        if WIDTH >= 640:
            WIDTH = 640
        elif WIDTH <= 160:
            WIDTH = 160
        if HEIGHT >= 480:
            HEIGHT = 480
        elif HEIGHT <= 120:
            HEIGHT = 120
        if self.clear == 1:
            self.stage1.draw(WIDTH, HEIGHT)
        elif self.clear == 2:
            self.stage2.draw(WIDTH, HEIGHT)
        elif self.clear == 3:
            self.stage3.draw(WIDTH, HEIGHT)
        else:
            # self.start.draw(WIDTH, HEIGHT)
            self.stage1.draw(WIDTH, HEIGHT)
            # self.stage2.draw(WIDTH, HEIGHT)
            # self.stage3.draw(WIDTH, HEIGHT)


class Wall:
    def __init__(self):
        self.start = load_image('prison.png')
        self.stage1 = load_image('background1.png')
        self.stage2 = load_image('background2.png')
        self.stage3 = load_image('bossstage.png')
        self.arrow = load_image('Arrow.png')
        self.inventory = load_image('inventory.png')
        self.inven_but = load_image('inventory button.png')
        self.x_but = load_image('X Button.png')
        self.inven = 0
        self.clear = None
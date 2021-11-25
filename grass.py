from pico2d import *
import server
from collision import collide

png_names = ['inventory', 'stage1', 'stage2', 'stage3', 'start']

class Grass:
    images = None

    def load_images(self):
        if Grass.images == None:
            Grass.images = {}
            for name in png_names:
                Grass.images[name] = load_image("./sheets/background/" + name + ".png")

    def __init__(self):
        self.load_images()
        # self.door1 = 0, 0
        # self.door2 = 0, 0
        # self.door3 = 0, 0
        self.arrow = load_image('./sheets/UI/Arrow.png')
        self.inven_but = load_image('./sheets/UI/inventory button.png')
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
        if server.clear == 1:
            Grass.images['stage1'].draw(WIDTH, HEIGHT)
        elif server.clear == 2:
            Grass.images['stage2'].draw(WIDTH, HEIGHT)
        elif server.clear == 3:
            Grass.images['stage3'].draw(WIDTH, HEIGHT)
        else:
            # Grass.images['start'].draw(WIDTH, HEIGHT)
            Grass.images['stage1'].draw(WIDTH, HEIGHT)
            # self.stage2.draw(WIDTH, HEIGHT)
            # self.stage3.draw(WIDTH, HEIGHT)
        self.inven_but.draw(20, 580)

#
# class Wall:
#     def __init__(self):
#         # self.load_images()
#         self.arrow = load_image('Arrow.png')
#         self.inventory = load_image('inventory.png')
#         self.inven_but = load_image('inventory button.png')
#         self.x_but = load_image('X Button.png')
#         self.inven = 0
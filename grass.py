from pico2d import *

class Grass:
    def __init__(self):
        self.stage1 = load_image('background1.png')
        # self.image = load_image('grass.png')

    def update(self):
        pass

    def draw(self):
        self.stage1.draw(400, 300)
        # self.image.draw(400, 30)
        # self.image.draw(1200, 30)

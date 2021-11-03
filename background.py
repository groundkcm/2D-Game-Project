from pico2d import *
from gretel import Gretel

class Background:
    def __init__(self):
        self.image = load_image('background1.png')

    def draw(self):
        WIDTH, HEIGHT = 1280 - Gretel().x * 2 + 160, 960 - Gretel().y * 2 + 120
        self.image.draw(WIDTH, HEIGHT)

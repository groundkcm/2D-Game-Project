from pico2d import *
from gretel import Gretel

class Background:
    def __init__(self):
        self.stage1 = load_image('background1.png')
        self.stage2 = load_image('background2.png')
        self.arrow = load_image('Arrow.png')
        self.inventory = load_image('inventory.png')
        self.inven_but = load_image('inventory button.png')
        self.x_but = load_image('X Button.png')
        self.inven = 0

    def draw(self):
        hide_cursor()
        WIDTH, HEIGHT = 1280 - Gretel().x * 2 + 160, 960 - Gretel().y * 2 + 120
        if WIDTH >= 640:
            WIDTH = 640
        elif WIDTH <= 160:
            WIDTH = 160
        if HEIGHT >= 480:
            HEIGHT = 480
        elif HEIGHT <= 120:
            HEIGHT = 120
        self.stage1.draw(WIDTH, HEIGHT)
        if self.inven == 1:
            self.inventory.draw(400, 300)
            self.x_but.draw(750, 450)
        else:
            self.inven_but.draw(25, 575)

import random
from pico2d import *
import game_world
import game_framework
import server

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 3.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 58

class Fire:
    image = None

    def __init__(self, x=0, y=0, speed=0):
        if Fire.image == None:
            Fire.image = {}
            Fire.image['fireball'] = [load_image("./sheets/fire/" + "%d" % i + ".png") for i in range(1, 60)]
        self.x, self.y, self.speed = x, y, speed
        self.frame = 0

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def draw(self):
        Fire.image['fireball'][int(self.frame)].draw(self.x, self.y, 32, 32)
        if server.debugmode == 1:
            draw_rectangle(*self.get_bb())

    def update(self):
        # self.y -= self.speed * game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    def stop(self):
        pass

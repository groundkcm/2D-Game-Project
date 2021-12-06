import random
from pico2d import *
from collision import collide
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

    def __init__(self, x=0, y=0, dir=0):
        if Fire.image == None:
            Fire.image = {}
            Fire.image['fireball'] = [load_image("./sheets/fire/" + "%d" % i + ".png") for i in range(1, 60)]
        self.x, self.y, self.dir = x, y, dir
        self.frame = 0

    def get_bb(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        return cx - 15, cy - 15, cx + 15, cy + 15

    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom

        Fire.image['fireball'][int(self.frame)].draw(cx, cy, 32, 32)
        if server.debugmode == 1:
            draw_rectangle(*self.get_bb())

    def update(self):
        if collide(self, server.boy):
            server.boy.hit()
            game_world.remove_object(self)

        self.x += RUN_SPEED_PPS * math.cos(self.dir) * game_framework.frame_time
        self.y += RUN_SPEED_PPS * math.sin(self.dir) * game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    def stop(self):
        pass

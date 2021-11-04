from pico2d import *
from gretel import Gretel
from skeleton import Skeleton
from background import Background

gretel = Gretel()
skeleton = Skeleton()
background = Background()

class CrashEvent:
    def __init__(self):
        self.x, self.y = 200, 200
        self.Hp = 50
        self.width = 20
        self.height = 25
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.timer = 0
        self.event_que = []

    def change_state(self, state):
        # fill here
        pass

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        pass

import game_framework
from pico2d import *

import game_world

# Boy Run Speed
# fill expressions correctly
PIXEL_PER_METER = (3.0 / 0.3)
RUN_SPEED_KMPH = 5.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 10000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

animation_names = ['attack']

class Witch:
    images = None

    def load_images(self):
        if Witch.images == None:
            Witch.images = {}
            for name in animation_names:
                Witch.images[name] = load_image("./sheets/mushroom/" + name + ".png")

    def __init__(self):
        self.x, self.y = 600, 150
        # Boy is only once created, so instance image loading is fine
        # self.run_r = load_image('gretel run sheet.png')
        # self.run_l = load_image('gretel run_left sheet.png')
        # self.jump = load_image('gretel jump sheet.png')
        # self.attack_r = load_image('gretel attack sheet.png')
        # self.attack_l = load_image('gretel attack_left sheet.png')
        # self.died = load_image('gretel hurt sheet.png')
        self.image = load_image('witch attack.png')
        # self.font = load_font('ENCR10B.TTF', 16)
        self.dir = 1
        self.high = 0
        self.velocity = 0
        self.click = 0
        self.frame = 0
        self.timer = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def passxy(self):
        return self.x, self.y

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            # if event not in next_state_table[self.cur_state]:
            #     pass
            # else:
            #     self.cur_state.exit(self, event)
            #     self.cur_state = next_state_table[self.cur_state][event]
            #     self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)


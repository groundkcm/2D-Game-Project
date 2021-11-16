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



# Boy Event
HIT, RANGE, DEAD, READY, SLEEP, WALK, DEFENCE = range(7)

# Boy States

class IdleState:

    def enter(boy, event):
        boy.timer = 1000

    def exit(boy, event):
        pass

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 18
        boy.timer -= 1
        if boy.timer == 0:
            boy.add_event(SLEEP)

    def draw(boy):
        boy.image.clip_draw(int(boy.frame) * 100, 0, 100, 100, boy.x, boy.y)


class RunState:

    def enter(boy, event):
        boy.dir = clamp(-1, boy.velocity, 1)

    def exit(boy, event):
        pass

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 24
        boy.x += boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 800 - 25)
        boy.y += boy.high * game_framework.frame_time
        boy.y = clamp(25, boy.y, 600 - 25)
        # boy.camera_move()

    # @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.run_r.clip_draw(int(boy.frame) * 100, 0, 100, 100, boy.x, boy.y)
        else:
            boy.run_l.clip_draw(int(boy.frame) * 100, 0, 100, 100, boy.x, boy.y)


# fnum = 0
# class JumpState:
#     def enter(self, event):
#         self.dir = clamp(-1, self.velocity, 1)
#         # self.timer = 500
#
#     def exit(self, event):
#         global fnum
#         if (event == RIGHT_DOWN or event == LEFT_DOWN) and fnum == 18:
#             self.cur_state.exit(self, event)
#             self.cur_state = RunState
#             self.cur_state.enter(self, event)
#
#     def do(self):
#         global fnum
#         self.frame = (self.frame + 0.05 * FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 19
#         if fnum < 9:
#             self.high = RUN_SPEED_PPS * 2
#         else:
#             self.high = -RUN_SPEED_PPS * 2
#         self.y += self.high * game_framework.frame_time
#         self.x += self.velocity * game_framework.frame_time
#         self.y = clamp(20, self.y, 600 - 20)
#         self.x = clamp(15, self.x, 800 - 15)
#         # self.camera_move()
#         fnum += 1
#         if fnum == 19:
#             fnum = 0
#             self.high = 0
#             self.add_event(READY)
#         # self.timer -= 10
#         # if self.timer == 0:
#         #     self.add_event(READY)
#
#     def draw(self):
#         self.jump.clip_draw(int(self.frame) * 100, 0, 100, 100, self.x, self.y)


class AttackState:
    def enter(self, event):
        pass

    def exit(self, event):
        pass

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10 + 16
        boy.add_event(READY)
        boy.timer -= 10
        if boy.timer == 0:
            boy.add_event(READY)

    def draw(self):
        if self.dir == 1:
            self.attack_r.clip_draw(int(self.frame) * 100, 0, 100, 100, self.x, self.y)
        else:
            self.attack_l.clip_draw(int(26 - self.frame) * 100, 0, 100, 100, self.x, self.y)


class DefenceState:
    def enter(self, event):
        self.timer = 200

    def exit(gretel, event):
        pass

    def do(self):
        self.frame = (self.frame + 0.05 * FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.velocity = -RUN_SPEED_PPS
        self.timer -= 10
        if self.timer == 0:
            self.velocity += RUN_SPEED_PPS
            self.add_event(READY)
        self.x += self.velocity * game_framework.frame_time
        self.x = clamp(15, self.x, 800 - 15)
        # self.camera_move()

    def draw(self):
        if self.dir == 1:
            self.defence.clip_draw(int(self.frame) * 100, 0, 100, 100, self.x, self.y)
        else:
            self.defence.clip_draw(int(self.frame) * 100, 0, 100, 100, self.x, self.y)


# next_state_table = {
#     IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
#                 TOP_DOWN: RunState, BOTTOM_DOWN: RunState, TOP_UP: RunState, BOTTOM_UP: RunState,
#                 MLEFT_BUT_DOWN: AttackState, MRIGHT_BUT_DOWN: DefenceState,
#                 SPACE: JumpState},
#     RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
#                TOP_DOWN: IdleState, BOTTOM_DOWN: IdleState, TOP_UP: IdleState, BOTTOM_UP: IdleState,
#                MLEFT_BUT_DOWN: AttackState, MRIGHT_BUT_DOWN: DefenceState,
#                SPACE: JumpState},
#     AttackState: {READY: IdleState},
#     DefenceState: {READY: IdleState},
#     JumpState: {LEFT_DOWN: JumpState, RIGHT_DOWN: JumpState, READY: IdleState},
# }

class Mushroom:

    def __init__(self):
        self.x, self.y = 800 // 2, 150
        # Boy is only once created, so instance image loading is fine
        self.run_r = load_image('gretel run sheet.png')
        self.run_l = load_image('gretel run_left sheet.png')
        self.jump = load_image('gretel jump sheet.png')
        self.attack_r = load_image('gretel attack sheet.png')
        self.attack_l = load_image('gretel attack_left sheet.png')
        self.defence = load_image('gretel defence sheet.png')
        self.died = load_image('gretel hurt sheet.png')
        self.image = load_image('gretel stop sheet.png')
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


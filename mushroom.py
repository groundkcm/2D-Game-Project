import game_framework
from pico2d import *
from collision import collide
import server
import game_world

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 1.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 10000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5


HIT, RANGE, DEAD, READY, SLEEP, WALK, DEFENCE = range(7)

class IdleState:

    def enter(boy, event):
        boy.timer = 1000

    def exit(boy, event):
        pass

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        boy.timer -= 1
        if boy.timer == 0:
            boy.add_event(SLEEP)

    def draw(boy):
        # boy.image.clip_draw(int(boy.frame) * 150, 0, 150, 150, Mushroom.x, Mushroom.y)
        if boy.hp <= 0:
            pass
        else:
            boy.image.clip_draw(int(boy.frame) * 150, 0, 150, 150, boy.x, boy.y)


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
            boy.run_r.clip_draw(int(boy.frame) * 150, 0, 150, 150, boy.x, boy.y)
        else:
            boy.run_l.clip_draw(int(boy.frame) * 150, 0, 150, 150, boy.x, boy.y)


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
            self.attack_r.clip_draw(int(self.frame) * 150, 0, 150, 150, self.x, self.y)
        else:
            self.attack_l.clip_draw(int(self.frame) * 150, 0, 150, 150, self.x, self.y)


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
            self.defence.clip_draw(int(self.frame) * 150, 0, 150, 150, self.x, self.y)
        else:
            self.defence.clip_draw(int(self.frame) * 150, 0, 150, 150, self.x, self.y)


class DeadState:
    def enter(self, event):
        self.timer = 200

    def exit(self, event):
        pass

    def do(self):
        self.frame = (self.frame + 0.05 * FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.timer -= 10
        if self.timer == 0:
            self.add_event(READY)

    def draw(self):
        if self.dir == 1:
            self.died.clip_draw(int(self.frame) * 150, 0, 150, 150, self.x, self.y)
        else:
            self.died.clip_draw(int(self.frame) * 150, 0, 150, 150, self.x, self.y)


# HIT, RANGE, DEAD, READY, SLEEP, WALK, DEFENCE = range(7)
next_state_table = {
    IdleState: {DEAD: DeadState},
    RunState: {DEAD: DeadState},
    AttackState: {DEAD: DeadState, READY: IdleState},
    DefenceState: {DEAD: DeadState, READY: IdleState},
    DeadState: {READY: IdleState}
}

class Mushroom:
    def __init__(self):
        self.x, self.y = 300, 200
        self.hp = 40
        # Boy is only once created, so instance image loading is fine
        self.run_r = load_image('mushroom run.png')
        self.run_l = load_image('mushroom run.png')
        self.attack_r = load_image('mushroom attack.png')
        self.attack_l = load_image('mushroom attack.png')
        self.died = load_image('mushroom death.png')
        self.image = load_image('mushroom stop.png')
        self.hpbar = load_image('monster hp bar.png')
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

    def get_bb(self):
        return self.x - 20, self.y - 25, self.x + 20, self.y + 20
        # return Mushroom.x - 20, Mushroom.y - 25, Mushroom.x + 20, Mushroom.y + 20

    def stop(self):
        if self.dir == 1:
            self.x -= self.velocity * game_framework.frame_time
        elif self.dir == -1:
            self.x += self.velocity * game_framework.frame_time
        self.hp -= 1

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        if collide(self, server.boy):
            server.boy.set_parent(self)

        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            # if event not in next_state_table[self.cur_state]:
            #     pass
            # else:
            #     self.cur_state.exit(self, event)
            #     self.cur_state = next_state_table[self.cur_state][event]
            #     self.cur_state.enter(self, event)
        if server.x >= 640:
            server.x = 640
        elif server.x <= 400:
            server.x = 400
        if server.y >= 480:
            server.y = 480
        elif server.y <= 300:
            server.y = 300
        self.x, self.y = 1280 - server.x * 2 + 0, 960 - server.y * 2 + 0

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())
        self.hpbar.clip_draw(0, 0, self.hp, 3, self.x - (40 - self.hp), self.y + 30)

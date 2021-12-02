import game_framework
from pico2d import *
from collision import collide
import server
import game_world
import math

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 15.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, TOP_DOWN, BOTTOM_DOWN, TOP_UP, BOTTOM_UP, ATTACK_DOWN, MRIGHT_BUT_DOWN, \
SPACE, READY, DEAD = range(13)

key_event_table = {
    (SDL_KEYDOWN, SDLK_d): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_a): LEFT_DOWN,
    (SDL_KEYUP, SDLK_d): RIGHT_UP,
    (SDL_KEYUP, SDLK_a): LEFT_UP,
    (SDL_KEYDOWN, SDLK_w): TOP_DOWN,
    (SDL_KEYDOWN, SDLK_s): BOTTOM_DOWN,
    (SDL_KEYUP, SDLK_w): TOP_UP,
    (SDL_KEYUP, SDLK_s): BOTTOM_UP,
    (SDL_KEYDOWN, SDLK_q): ATTACK_DOWN,
    (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_RIGHT): MRIGHT_BUT_DOWN,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}

animation_names = ['attack', 'dead', 'idle', 'run', 'defence', 'jump']

class RunState:
    soundcheck = 0
    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += RUN_SPEED_PPS
        elif event == RIGHT_UP:
            boy.velocity -= RUN_SPEED_PPS
        if event == LEFT_DOWN:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            boy.velocity += RUN_SPEED_PPS

        if event == TOP_DOWN:
            boy.high += RUN_SPEED_PPS
        elif event == TOP_UP:
            boy.high -= RUN_SPEED_PPS
        if event == BOTTOM_DOWN:
            boy.high -= RUN_SPEED_PPS
        elif event == BOTTOM_UP:
            boy.high += RUN_SPEED_PPS


    def exit(boy, event):
        pass

    def do(boy):
        global soundcheck
        if boy.hp == 0:
            boy.add_event(DEAD)
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 24
        boy.iframe = (boy.iframe + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 18
        boy.x += boy.velocity * game_framework.frame_time
        boy.y += boy.high * game_framework.frame_time
        # boy.x = clamp(25, boy.x, 800 - 25)
        # boy.y = clamp(25, boy.y, 600 - 25)
        # RunState.soundcheck += 1
        # if RunState.soundcheck == 100:
        #     boy.walking()
        #     RunState.soundcheck = 0

    # @staticmethod
    def draw(boy):
        cx, cy = boy.x - server.background.window_left, boy.y - server.background.window_bottom

        if boy.velocity > 0:
            Boy.images['run'].clip_draw(int(boy.frame) * 100, 0, 100, 100, cx, cy)
            boy.dir = 1
        elif boy.velocity < 0:
            Boy.images['run'].clip_composite_draw(int(boy.frame) * 100, 0, 100, 100, 0, 'h', cx, cy, 100, 100)
            boy.dir = -1
        else:
            # if boy x_velocity == 0
            if boy.high > 0 or boy.high < 0:
                if boy.dir == 1:
                    Boy.images['run'].clip_draw(int(boy.frame) * 100, 0, 100, 100, cx, cy)
                else:
                    Boy.images['run'].clip_composite_draw(int(boy.frame) * 100, 0, 100, 100, 0, 'h', cx, cy, 100, 100)
            else:
                # boy is idle
                if boy.dir == 1:
                    Boy.images['idle'].clip_draw(int(boy.iframe) * 100, 0, 100, 100, cx, cy)
                else:
                    Boy.images['idle'].clip_composite_draw(int(boy.iframe) * 100, 0, 100, 100, 0, 'h', cx, cy, 100, 100)


class JumpState:
    def enter(self, event):
        if event == RIGHT_DOWN:
            self.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            self.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            self.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            self.velocity += RUN_SPEED_PPS
        self.dir = clamp(-1, self.velocity, 1)
        self.timer = 200
        self.frame = 0

    def exit(self, event):
        pass

    def do(self):
        if self.hp == 0:
            self.add_event(DEAD)
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 19
        if int(self.frame) < 9:
            self.high = RUN_SPEED_PPS * 0.5
        else:
            self.high = -RUN_SPEED_PPS * 0.5
        self.y += self.high * game_framework.frame_time
        self.x += self.velocity * game_framework.frame_time
        # self.y = clamp(20, self.y, 600 - 20)
        # self.x = clamp(15, self.x, 800 - 15)
        if int(self.frame) >= 18:
            self.high = 0
            self.add_event(READY)

    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        Boy.images['jump'].clip_draw(int(self.frame) * 100, 0, 100, 100, cx, cy)


class AttackState:
    def enter(self, event):
        if event == ATTACK_DOWN:
            self.click = (self.click + 1) % 3 + 1
            self.timer = 200

    def exit(self, event):
        pass

    def do(boy):
        if boy.hp == 0:
            boy.add_event(DEAD)
        if boy.click == 1:
            boy.frame = (boy.frame + 0.8 * FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        elif boy.click == 2:
            boy.frame = (boy.frame + 0.8 * FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8 + 8
        elif boy.click == 3:
            boy.frame = (boy.frame + 0.8 * FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10 + 16
            boy.add_event(READY)
        boy.timer -= 1
        if boy.timer == 0:
            boy.add_event(READY)

    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        if self.dir == 1:
            Boy.images['attack'].clip_draw(int(self.frame) * 100, 0, 100, 100, cx, cy)
        else:
            Boy.images['attack'].clip_composite_draw(int(self.frame) * 100, 0, 100, 100, 0, 'h', cx, cy, 100, 100)


class DefenceState:
    def enter(self, event):
        self.timer = 200

    def exit(gretel, event):
        pass

    def do(self):
        if self.hp == 0:
            self.add_event(DEAD)
        self.frame = (self.frame + 0.1 * FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.velocity = -RUN_SPEED_PPS
        self.timer -= 2
        if self.timer == 0:
            self.velocity += RUN_SPEED_PPS
            self.add_event(READY)
        self.x += self.velocity * game_framework.frame_time
        # self.x = clamp(15, self.x, 800 - 15)

    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom

        if self.dir == 1:
            Boy.images['defence'].clip_draw(int(self.frame) * 100, 0, 100, 100, cx, cy)
        else:
            Boy.images['defence'].clip_composite_draw(int(self.frame) * 100, 0, 100, 100, 0, 'h', cx, cy, 100, 100)


class DeadState:
    def enter(self, event):
        self.timer = 200

    def exit(gretel, event):
        pass

    def do(self):
        self.frame = (self.frame + 0.5 * FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.timer -= 2
        if self.timer == 0:
            server.gameover = 1
            # server.end = 1
            # self.add_event(READY)

    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        if self.dir == 1:
            Boy.images['dead'].clip_draw(int(self.frame) * 100, 0, 100, 100, cx, cy)
        else:
            Boy.images['dead'].clip_composite_draw(int(self.frame) * 100, 0, 100, 100, 0, 'h', cx, cy, 100, 100)


next_state_table = {
    RunState: {RIGHT_UP: RunState, LEFT_UP: RunState, LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
               TOP_DOWN: RunState, BOTTOM_DOWN: RunState, TOP_UP: RunState, BOTTOM_UP: RunState,
               ATTACK_DOWN: AttackState, MRIGHT_BUT_DOWN: DefenceState,
               SPACE: JumpState, READY: RunState, DEAD: DeadState},
    AttackState: {READY: RunState, DEAD: DeadState},
    DefenceState: {READY: RunState, DEAD: DeadState},
    JumpState: {LEFT_DOWN: JumpState, RIGHT_DOWN: JumpState, READY: RunState, DEAD: DeadState},
    DeadState: {READY: RunState}
}

class Boy:
    images = None
    check = 0

    def load_images(self):
        if Boy.images == None:
            Boy.images = {}
            for name in animation_names:
                Boy.images[name] = load_image("./sheets/gretel/" + name + ".png")

    def __init__(self):
        self.x, self.y = 400, 300
        self.hp = 100
        self.load_images()
        self.hpbar = load_image('./sheets/UI/hp bar.png')
        self.hpbase = load_image('./sheets/UI/Hp base.png')
        self.dir = 1
        self.high = 0
        self.velocity = 0
        self.parent = None
        self.click = 0
        self.frame = 0
        self.iframe = 0
        self.timer = 0
        self.event_que = []
        self.cur_state = RunState
        self.cur_state.enter(self, None)
        self.start_time = get_time()
    #
    # def walking(self):
    #     self.footsteps.play()

    def __getstate__(self):
        state = {'x' : self.x, 'y':self.y, 'dir':self.dir,'cur_state': self.cur_state , 'time' : get_time() - self.start_time}
        return state

    def __setstate__(self, state):
        # fill here
        self.__init__()
        self.__dict__.update(state)

    def get_bb(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom

        if self.cur_state == RunState:
            if self.dir == 1:
                return cx - 30, cy - 25, cx + 10, cy + 20
            else:
                return cx - 10, cy - 25, cx + 30, cy + 20
        elif self.cur_state == AttackState:
            return cx - 30, cy - 25, cx + 25, cy + 25
        elif self.cur_state == DefenceState:
            return cx - 30, cy - 35, cx + 5, cy + 5
        elif self.cur_state == JumpState:
            if self.dir == 1:
                return cx - 30, cy - 20, cx + 10, cy + 20
            else:
                return cx - 10, cy - 20, cx + 30, cy + 20
        elif self.cur_state == DeadState:
            return cx - 30, cy - 20, cx + 10, cy + 20

    def stop(self):#튕기기 다시
        # if self.dir == 1:
        #     self.x -= self.velocity * game_framework.frame_time
        #     self.velocity = 0
        # elif self.dir == -1:
        #     self.velocity = 0
        # if self.high > 0:
        #     self.high = 0
        # elif self.high < 0:
        #     self.high = 0
        if self.dir == 1:
            self.x -= self.velocity * game_framework.frame_time
        elif self.dir == -1:
            self.x += self.velocity * game_framework.frame_time
        if self.high > 0:
            self.y -= self.high * game_framework.frame_time
        elif self.high < 0:
            self.y += self.high * game_framework.frame_time
        # self.add_event(READY)

    def hit(self):
        Boy.check += 1
        if Boy.check == 50:
            Boy.check = 0
            self.hp -= 1

    def set_parent(self, enemy):
        self.parent = enemy
        if self.cur_state == AttackState:
            enemy.x += enemy.speed * math.cos(enemy.dir) * game_framework.frame_time
            enemy.hit()
        elif self.velocity == 0 and self.high == 0:
            enemy.stop()
            # self.hit()
        else:
            self.stop()
            self.hit()

    def set_parent_wall(self, wall):
        self.parent = wall
        if self.dir == 1:
            self.x -= self.velocity * game_framework.frame_time
        elif self.dir == -1:
            self.x += self.velocity * game_framework.frame_time

    def set_background(self, bg):
        self.bg = bg
        self.x = self.bg.w / 2
        self.y = self.bg.h / 2

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            if event not in next_state_table[self.cur_state]:
                pass
            else:
                self.cur_state.exit(self, event)
                self.cur_state = next_state_table[self.cur_state][event]
                self.cur_state.enter(self, event)

        if server.clear == 1:
            self.x = clamp(20, self.x, server.background.w - 20)
            self.y = clamp(20, self.y, server.background.h - 20)
        elif server.clear == 2:
            self.x = clamp(20, self.x, server.background.w - 100)
            self.y = clamp(20, self.y, server.background.h - 20)
        elif server.clear == 3:
            self.x = clamp(20, self.x, server.background.w - 20)
            self.y = clamp(20, self.y, server.background.h - 20)
        else:
            self.x = clamp(20, self.x, server.background.w - 100)
            self.y = clamp(20, self.y, server.background.h - 20)
            # self.x = clamp(80, self.x, server.background.w - 80)
            # self.y = clamp(150, self.y, server.background.h - 180)

    def draw(self):
        self.hpbase.draw(150, 575)
        self.hpbar.clip_draw(0, 0, self.hp * 2, 13, 150 - (100 - self.hp), 575)
        self.cur_state.draw(self)
        # self.font.draw(self.x - 60, self.y + 50, '(Time: %3.2f)' % get_time(), (255,255,0))
        debug_print('x:' + str(int(self.x)) + ' y:' + str(int(self.y)) + ' Current State:' + str(self.cur_state))
        if server.debugmode == 1:
            draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        elif (event.type, event.button) in key_event_table:
            key_event = key_event_table[(event.type, event.button)]
            self.add_event(key_event)
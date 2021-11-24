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
    (SDL_KEYDOWN, SDLK_q): ATTACK_DOWN,#right ->left
    (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_RIGHT): MRIGHT_BUT_DOWN,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}

class IdleState:

    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            boy.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            boy.velocity += RUN_SPEED_PPS
        elif event == TOP_DOWN:
            boy.high += RUN_SPEED_PPS
        elif event == BOTTOM_DOWN:
            boy.high -= RUN_SPEED_PPS
        elif event == TOP_UP:
            boy.high -= RUN_SPEED_PPS
        elif event == BOTTOM_UP:
            boy.high += RUN_SPEED_PPS

    def exit(boy, event):
        pass

    def do(boy):
        if boy.hp == 0:
            boy.add_event(DEAD)
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 18

    def draw(boy):
        boy.image.clip_draw(int(boy.frame) * 100, 0, 100, 100, boy.x, boy.y)


class RunState:
    soundcheck = 0
    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            boy.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            boy.velocity += RUN_SPEED_PPS
        if event == TOP_DOWN:
            boy.high += RUN_SPEED_PPS
        elif event == BOTTOM_DOWN:
            boy.high -= RUN_SPEED_PPS
        elif event == TOP_UP:
            boy.high -= RUN_SPEED_PPS
        elif event == BOTTOM_UP:
            boy.high += RUN_SPEED_PPS
        boy.dir = clamp(-1, boy.velocity, 1) #좌우 방향


    def exit(boy, event):
        pass

    def do(boy):
        global soundcheck
        if boy.hp == 0:
            boy.add_event(DEAD)
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 24
        boy.x += boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 800 - 25)
        boy.y += boy.high * game_framework.frame_time
        boy.y = clamp(25, boy.y, 600 - 25)
        # RunState.soundcheck += 1
        # if RunState.soundcheck == 100:
        #     boy.walking()
        #     RunState.soundcheck = 0
        server.x, server.y = boy.x, boy.y

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.run_r.clip_draw(int(boy.frame) * 100, 0, 100, 100, boy.x, boy.y)
        else:
            boy.run_l.clip_draw(int(24 - boy.frame) * 100, 0, 100, 100, boy.x, boy.y)


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
        # global fnum
        # if (event == RIGHT_DOWN or event == LEFT_DOWN) and fnum == 18:
        #     self.cur_state.exit(self, event)
        #     self.cur_state = RunState
        #     self.cur_state.enter(self, event)

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
        self.y = clamp(20, self.y, 600 - 20)
        self.x = clamp(15, self.x, 800 - 15)
        server.x, server.y = self.x, self.y
        if int(self.frame) >= 18:
            self.high = 0
            self.add_event(READY)

    def draw(self):
        self.jump.clip_draw(int(self.frame) * 100, 0, 100, 100, self.x, self.y)


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
        if self.hp == 0:
            self.add_event(DEAD)
        self.frame = (self.frame + 0.01 * FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.velocity = -RUN_SPEED_PPS
        self.timer -= 2
        if self.timer == 0:
            self.velocity += RUN_SPEED_PPS
            self.add_event(READY)
        self.x += self.velocity * game_framework.frame_time
        self.x = clamp(15, self.x, 800 - 15)
        server.x = self.x

    def draw(self):
        if self.dir == 1:
            self.defence.clip_draw(int(self.frame) * 112, 0, 112, 100, self.x, self.y)
        else:
            self.defence.clip_draw(int(self.frame) * 112, 0, 112, 100, self.x, self.y)


class DeadState:
    def enter(self, event):
        self.timer = 200

    def exit(gretel, event):
        pass

    def do(self):
        self.frame = (self.frame + 0.5 * FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.timer -= 2
        if self.timer == 0:
            # server.gameover = 1
            server.end = 1
            # self.add_event(READY)

    def draw(self):
        if self.dir == 1:
            self.died.clip_draw(int(self.frame) * 100, 0, 100, 100, self.x, self.y)
        else:
            self.died.clip_draw(int(self.frame) * 100, 0, 100, 100, self.x, self.y)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                TOP_DOWN: RunState, BOTTOM_DOWN: RunState, TOP_UP: RunState, BOTTOM_UP: RunState,
                ATTACK_DOWN: AttackState, MRIGHT_BUT_DOWN: DefenceState,
                SPACE: JumpState, DEAD: DeadState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               TOP_DOWN: IdleState, BOTTOM_DOWN: IdleState, TOP_UP: IdleState, BOTTOM_UP: IdleState,
               ATTACK_DOWN: AttackState, MRIGHT_BUT_DOWN: DefenceState,
               SPACE: JumpState, READY: IdleState, DEAD: DeadState},
    AttackState: {READY: IdleState, DEAD: DeadState},
    DefenceState: {READY: IdleState, DEAD: DeadState},
    JumpState: {LEFT_DOWN: JumpState, RIGHT_DOWN: JumpState, READY: IdleState, DEAD: DeadState},
    DeadState: {READY: IdleState}
}

class Boy:

    def __init__(self):
        self.x, self.y = 400, 200
        self.hp = 100
        # Boy is only once created, so instance image loading is fine
        self.run_r = load_image('gretel run sheet.png')
        self.run_l = load_image('gretel run_left sheet.png')
        self.jump = load_image('gretel jump sheet.png')
        self.attack_r = load_image('gretel attack sheet.png')
        self.attack_l = load_image('gretel attack_left sheet.png')
        self.defence = load_image('gretel defence sheet.png')
        self.died = load_image('gretel hurt sheet.png')
        self.image = load_image('gretel stop sheet.png')
        self.hpbar = load_image('hp bar.png')
        self.hpbase = load_image('Hp base.png')
        # self.search = load_wav('search item.wav')
        # self.search.set_volume(32)
        # self.footsteps = load_wav('walk.wav')
        # self.footsteps.set_volume(32)
        # self.font = load_font('ENCR10B.TTF', 16)
        self.dir = 1
        self.high = 0
        self.velocity = 0
        self.parent = None
        self.click = 0
        self.frame = 0
        self.timer = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def walking(self):
        self.footsteps.play()

    def get_bb(self):
        if self.cur_state == IdleState:
            return self.x - 30, self.y - 25, self.x + 5, self.y + 20
        elif self.cur_state == RunState:
            return self.x - 30, self.y - 25, self.x + 10, self.y + 20
        elif self.cur_state == AttackState:
            return self.x - 30, self.y - 25, self.x + 25, self.y + 25
        elif self.cur_state == DefenceState:
            return self.x - 30, self.y - 35, self.x + 5, self.y + 5
        elif self.cur_state == JumpState:
            return self.x - 30, self.y - 20, self.x + 10, self.y + 20
        elif self.cur_state == DeadState:
            return self.x - 30, self.y - 20, self.x + 10, self.y + 20

    def stop(self):
        if self.dir == 1:
            self.x -= self.velocity * game_framework.frame_time
        elif self.dir == -1:
            self.x += self.velocity * game_framework.frame_time
        self.hp -= 1
        # self.add_event(READY)

    def set_parent(self, enemy):
        self.parent = enemy
        if self.cur_state == AttackState:
            enemy.stop()
        else:
            self.stop()

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

    def draw(self):
        self.hpbase.draw(150, 575)
        self.hpbar.clip_draw(0, 0, self.hp * 2, 13, 150 - (100 - self.hp), 575)
        self.cur_state.draw(self)
        # self.font.draw(self.x - 60, self.y + 50, '(Time: %3.2f)' % get_time(), (255,255,0))
        debug_print('Velocity :' + str(self.velocity) + ' frame:' + str(int(self.frame)) + ' Current State:' + str(self.cur_state))
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        elif (event.type, event.button) in key_event_table:
            key_event = key_event_table[(event.type, event.button)]
            self.add_event(key_event)
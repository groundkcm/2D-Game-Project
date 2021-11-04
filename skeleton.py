from pico2d import *

HIT, RANGE, DEAD, LEFT_UP, SLEEP_TIMER, SHIFT_DOWN, SHIFT_UP = range(7)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): HIT,
    (SDL_KEYDOWN, SDLK_LEFT): RANGE,
    (SDL_KEYDOWN, SDLK_LSHIFT): DEAD,
    (SDL_KEYDOWN, SDLK_RSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,
    (SDL_KEYUP, SDLK_RSHIFT): SHIFT_UP
}

class Skeleton:
    def __init__(self):
        self.x, self.y = 200, 200
        self.Hp = 50
        self.width = 20
        self.height = 25
        self.stop = load_image('skeleton stop.png')
        # self.run_r = load_image('gretel run sheet.png')
        # self.run_l = load_image('gretel run_left sheet.png')
        # self.jump = load_image('gretel jump sheet.png')
        # self.attack_r = load_image('gretel attack sheet.png')
        # self.attack_l = load_image('gretel attack_left sheet.png')
        # self.defence = load_image('gretel defence sheet.png')
        # self.died = load_image('gretel hurt sheet.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.timer = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def change_state(self, state):
        # fill here
        pass

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            if not event in next_state_table[self.cur_state]:
                pass
            else:
                self.cur_state.exit(self, event)
                self.cur_state = next_state_table[self.cur_state][event]
                self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        debug_print('Velocity :' + str(self.velocity) + ' Dir:' + str(self.dir))

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

class IdleState:
    def enter(self, event):
        if event == RIGHT_DOWN:
            self.velocity += 1
        elif event == LEFT_DOWN:
            self.velocity -= 1
        self.timer = 1000

    def exit(boy, event):
        pass

    def do(self):
        self.frame = (self.frame + 1) % 8
        self.timer -= 1
        if self.timer == 0:
            self.add_event(SLEEP_TIMER)

    def draw(self):
        if self.dir == 1:
            self.stop.clip_draw(self.frame * 150, 0, 150, 150, skeleton1_1['x'], skeleton1_1['y'])
        else:
            self.stop.clip_draw(self.frame * 150, 0, 150, 150, skeleton1_1['x'], skeleton1_1['y'])

class WalkState:
    def enter(self, event):
        if event == RIGHT_DOWN:
            self.velocity += 1
        elif event == LEFT_DOWN:
            self.velocity -= 1
        elif event == RIGHT_UP:
            self.velocity -= 1
        elif event == LEFT_UP:
            self.velocity += 1
        self.dir = self.velocity

    def exit(self, event):
        pass

    def do(self):
        self.frame = (self.frame + 1) % 24
        self.timer -= 1
        self.x += self.velocity
        self.x = clamp(25, self.x, 800 - 25)

    def draw(self):
        if self.velocity == 1:
            self.stop.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
        else:
            self.stop.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

class AttackState:
    def enter(self, event):
        if event == RIGHT_DOWN:
            self.velocity += 1
        elif event == LEFT_DOWN:
            self.velocity -= 1
        elif event == RIGHT_UP:
            self.velocity -= 1
        elif event == LEFT_UP:
            self.velocity += 1
        self.timer = 1000

    def exit(gretel, event):
        pass

    def do(self):
        self.frame = (self.frame + 1) % 26
        self.timer -= 1

    def draw(self):
        if self.dir == 1:
            self.attack_r.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
        else:
            self.attack_l.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

class DefenceState:
    def enter(self, event):
        if event == RIGHT_DOWN:
            self.velocity += 1
        elif event == LEFT_DOWN:
            self.velocity -= 1
        elif event == RIGHT_UP:
            self.velocity -= 1
        elif event == LEFT_UP:
            self.velocity += 1
        self.timer = 1000

    def exit(self, event):
        pass

    def do(self):
        two = (two + 1) % 2
        self.frame = (self.frame + two) % 4
        self.timer -= 1

    def draw(self):
        self.defence.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)

class JumpState:
    def enter(self, event):
        if event == RIGHT_DOWN:
            self.velocity += 1
        elif event == LEFT_DOWN:
            self.velocity -= 1
        elif event == RIGHT_UP:
            self.velocity -= 1
        elif event == LEFT_UP:
            self.velocity += 1
        self.timer = 1000

    def exit(self, event):
        pass

    def do(self):
        self.frame = (self.frame + 1) % 19
        self.timer -= 1

    def draw(self):
        self.jump.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

class DiedState:
    def enter(self, event):
        if event == RIGHT_DOWN:
            self.velocity += 1
        elif event == LEFT_DOWN:
            self.velocity -= 1
        elif event == RIGHT_UP:
            self.velocity -= 1
        elif event == LEFT_UP:
            self.velocity += 1
        self.timer = 1000

    def exit(self, event):
        pass

    def do(self):
        two = (two + 1) % 2
        self.frame = (self.frame + two) % 7
        self.timer -= 1

    def draw(self):
        self.died.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)


next_state_table = {
    IdleState: {RIGHT_UP: WalkState, LEFT_UP: WalkState, RIGHT_DOWN: WalkState, LEFT_DOWN: WalkState, SLEEP_TIMER: SleepState},
    WalkState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState, SHIFT_DOWN: DashState},
    AttackState: {SHIFT_UP: WalkState, RIGHT_UP or LEFT_UP: IdleState},
    JumpState: {SHIFT_UP: WalkState, RIGHT_UP or LEFT_UP: IdleState},
    DiedState: {SHIFT_UP: WalkState, RIGHT_UP or LEFT_UP: IdleState},
    DefenceState: {LEFT_DOWN: WalkState, RIGHT_DOWN: WalkState, LEFT_UP: WalkState, RIGHT_UP: WalkState}
}
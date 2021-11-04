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
        self.x, self.y = 800 // 2, 150
        self.Hp = 110
        self.width = 15
        self.height = 20
        self.stop = load_image('gretel stop sheet.png')
        self.run_r = load_image('gretel run sheet.png')
        self.run_l = load_image('gretel run_left sheet.png')
        self.stop = load_image('gretel stop sheet.png')
        self.jump = load_image('gretel jump sheet.png')
        self.attack_r = load_image('gretel attack sheet.png')
        self.attack_l = load_image('gretel attack_left sheet.png')
        self.defence = load_image('gretel defence sheet.png')
        self.died = load_image('gretel hurt sheet.png')
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
    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += 1
        elif event == LEFT_DOWN:
            boy.velocity -= 1
        elif event == RIGHT_UP:
            boy.velocity -= 1
        elif event == LEFT_UP:
            boy.velocity += 1
        boy.timer = 1000

    def exit(boy, event):
        pass

    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.timer -= 1
        if boy.timer == 0:
            boy.add_event(SLEEP_TIMER)

    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(boy.frame * 100, 300, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(boy.frame * 100, 200, 100, 100, boy.x, boy.y)

class WalkState:
    def enter(gretel, event):
        if event == RIGHT_DOWN:
            gretel.velocity += 1
        elif event == LEFT_DOWN:
            gretel.velocity -= 1
        elif event == RIGHT_UP:
            gretel.velocity -= 1
        elif event == LEFT_UP:
            gretel.velocity += 1
        gretel.dir = gretel.velocity

    def exit(gretel, event):
        pass

    def do(gretel):
        gretel.frame = (gretel.frame + 1) % 24
        gretel.timer -= 1
        gretel.x += gretel.velocity
        gretel.x = clamp(25, gretel.x, 800 - 25)

    def draw(gretel):
        if gretel.velocity == 1:
            gretel.stop.clip_draw(gretel.frame * 100, 0, 100, 100, gretel.x, gretel.y)
        else:
            gretel.stop.clip_draw(gretel.frame * 100, 0, 100, 100, gretel.x, gretel.y)

class AttackState:
    def enter(gretel, event):
        if event == RIGHT_DOWN:
            gretel.velocity += 1
        elif event == LEFT_DOWN:
            gretel.velocity -= 1
        elif event == RIGHT_UP:
            gretel.velocity -= 1
        elif event == LEFT_UP:
            gretel.velocity += 1
        gretel.timer = 1000

    def exit(gretel, event):
        pass

    def do(gretel):
        gretel.frame = (gretel.frame + 1) % 26
        gretel.timer -= 1

    def draw(gretel):
        if gretel.dir == 1:
            gretel.attack_r.clip_draw(gretel.frame * 100, 0, 100, 100, gretel.x, gretel.y)
        else:
            gretel.attack_l.clip_draw(gretel.frame * 100, 0, 100, 100, gretel.x, gretel.y)

class DefenceState:
    def enter(gretel, event):
        if event == RIGHT_DOWN:
            gretel.velocity += 1
        elif event == LEFT_DOWN:
            gretel.velocity -= 1
        elif event == RIGHT_UP:
            gretel.velocity -= 1
        elif event == LEFT_UP:
            gretel.velocity += 1
        gretel.timer = 1000

    def exit(gretel, event):
        pass

    def do(gretel):
        two = (two + 1) % 2
        gretel.frame = (gretel.frame + two) % 4
        gretel.timer -= 1

    def draw(gretel):
        gretel.defence.clip_draw(gretel.frame * 100, 300, 100, 100, gretel.x, gretel.y)

class JumpState:
    def enter(gretel, event):
        if event == RIGHT_DOWN:
            gretel.velocity += 1
        elif event == LEFT_DOWN:
            gretel.velocity -= 1
        elif event == RIGHT_UP:
            gretel.velocity -= 1
        elif event == LEFT_UP:
            gretel.velocity += 1
        gretel.timer = 1000

    def exit(gretel, event):
        pass

    def do(gretel):
        gretel.frame = (gretel.frame + 1) % 19
        gretel.timer -= 1

    def draw(gretel):
        gretel.jump.clip_draw(gretel.frame * 100, 0, 100, 100, gretel.x, gretel.y)

class DiedState:
    def enter(gretel, event):
        if event == RIGHT_DOWN:
            gretel.velocity += 1
        elif event == LEFT_DOWN:
            gretel.velocity -= 1
        elif event == RIGHT_UP:
            gretel.velocity -= 1
        elif event == LEFT_UP:
            gretel.velocity += 1
        gretel.timer = 1000

    def exit(gretel, event):
        pass

    def do(gretel):
        two = (two + 1) % 2
        gretel.frame = (gretel.frame + two) % 7
        gretel.timer -= 1

    def draw(gretel):
        gretel.died.clip_draw(gretel.frame * 100, 0, 100, 100, gretel.x, gretel.y)


next_state_table = {
    IdleState: {RIGHT_UP: WalkState, LEFT_UP: WalkState, RIGHT_DOWN: WalkState, LEFT_DOWN: WalkState, SLEEP_TIMER: SleepState},
    WalkState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState, SHIFT_DOWN: DashState},
    AttackState: {SHIFT_UP: WalkState, RIGHT_UP or LEFT_UP: IdleState},
    JumpState: {SHIFT_UP: WalkState, RIGHT_UP or LEFT_UP: IdleState},
    DiedState: {SHIFT_UP: WalkState, RIGHT_UP or LEFT_UP: IdleState},
    DefenceState: {LEFT_DOWN: WalkState, RIGHT_DOWN: WalkState, LEFT_UP: WalkState, RIGHT_UP: WalkState}
}
from pico2d import *
from background import Background

# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, MLEFT_BUT_DOWN, MRIGHT_BUT_DOWN, MLEFT_BUT_UP, MLRIGHT_BUT_UP, SPACE_DOWN, SPACE_UP,\
    TOP_DOWN, TOP_UP, BOTTOM_DOWN, BOTTON_UP= range(14)

key_event_table = {
    (SDL_KEYDOWN, SDLK_d): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_a): LEFT_DOWN,
    (SDL_KEYUP, SDLK_d): RIGHT_UP,
    (SDL_KEYUP, SDLK_a): LEFT_UP,
    (SDL_KEYDOWN, SDLK_w): TOP_DOWN,
    (SDL_KEYDOWN, SDLK_s): BOTTOM_DOWN,
    (SDL_KEYUP, SDLK_w): TOP_UP,
    (SDL_KEYUP, SDLK_s): BOTTON_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN,
    (SDL_KEYUP, SDLK_SPACE): SPACE_UP,
    (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT): MLEFT_BUT_DOWN,
    (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_RIGHT): MRIGHT_BUT_DOWN,
    (SDL_MOUSEBUTTONUP, SDL_BUTTON_LEFT): MLEFT_BUT_UP,
    (SDL_MOUSEBUTTONUP, SDL_BUTTON_RIGHT): MLRIGHT_BUT_UP,
}

# Gretel States


class Gretel:

    def __init__(self):
        self.x, self.y = 800 // 2, 90
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
        gretel.frame = (gretel.frame + 1) % 8
        gretel.timer -= 1

    def draw(gretel):
        if gretel.dir == 1:
            gretel.stop.clip_draw(gretel.frame * 100, 300, 100, 100, gretel.x, gretel.y)
        else:
            gretel.stop.clip_draw(gretel.frame * 100, 200, 100, 100, gretel.x, gretel.y)


class RunState:
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
        gretel.frame = (gretel.frame + 1) % 8
        gretel.timer -= 1
        gretel.x += gretel.velocity
        gretel.x = clamp(25, gretel.x, 800 - 25)

    def draw(gretel):
        if gretel.velocity == 1:
            gretel.stop.clip_draw(gretel.frame * 100, 100, 100, 100, gretel.x, gretel.y)
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
        gretel.frame = (gretel.frame + 1) % 8
        gretel.timer -= 1

    def draw(gretel):
        if gretel.dir == 1:
            gretel.stop.clip_draw(gretel.frame * 100, 300, 100, 100, gretel.x, gretel.y)
        else:
            gretel.stop.clip_draw(gretel.frame * 100, 200, 100, 100, gretel.x, gretel.y)


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
        gretel.frame = (gretel.frame + 1) % 8
        gretel.timer -= 1

    def draw(gretel):
        if gretel.dir == 1:
            gretel.stop.clip_draw(gretel.frame * 100, 300, 100, 100, gretel.x, gretel.y)
        else:
            gretel.stop.clip_draw(gretel.frame * 100, 200, 100, 100, gretel.x, gretel.y)


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
        gretel.frame = (gretel.frame + 1) % 8
        gretel.timer -= 1

    def draw(gretel):
        if gretel.dir == 1:
            gretel.stop.clip_draw(gretel.frame * 100, 300, 100, 100, gretel.x, gretel.y)
        else:
            gretel.stop.clip_draw(gretel.frame * 100, 200, 100, 100, gretel.x, gretel.y)


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
        gretel.frame = (gretel.frame + 1) % 8
        gretel.timer -= 1

    def draw(gretel):
        if gretel.dir == 1:
            gretel.stop.clip_draw(gretel.frame * 100, 300, 100, 100, gretel.x, gretel.y)
        else:
            gretel.stop.clip_draw(gretel.frame * 100, 200, 100, 100, gretel.x, gretel.y)

next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState}
}


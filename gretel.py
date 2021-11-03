from pico2d import *

# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP = range(4)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP
}

# Gretel States


class Gretel:

    def __init__(self):
        self.x, self.y = 800 // 2, 90
        self.stop = load_image('gretel stop sheet.png')
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
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)


    def draw(self):
        self.cur_state.draw(self)


    def handle_event(self, event):
        pass


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

next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState}
}


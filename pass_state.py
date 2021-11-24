import game_framework
from pico2d import *
import title_state


name = "PassState"
image = None


def enter():
    global image
    image = load_image('moonlighter.jpg')

def exit():
    global image
    del(image)

def update():
    pass

def draw():
    global image
    clear_canvas()
    image.draw(400, 300)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(title_state)


def pause():
    pass


def resume():
    pass



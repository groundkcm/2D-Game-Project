import game_framework
from pico2d import *
import title_state
import server


name = "PassState"
gameover = None
tname = None
theend = None
image = None

def enter():
    global gameover, tname, theend, image
    gameover = load_image('gameover.jpg')
    tname = load_image('title eng.png')
    theend = load_image('the end.png')
    image = load_image('title.jpg')

def exit():
    global gameover, tname, theend, image
    del(gameover, tname, theend, image)

def update():
    pass

def draw():
    global gameover, tname, theend, image
    clear_canvas()
    if server.gameover == 1:
        gameover.draw(400, 300)
    else:
        image.draw(400, 300)
        tname.draw(400, 400)
        theend.draw(400, 200)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                server.gameover = 0
                game_framework.change_state(title_state)


def pause():
    pass


def resume():
    pass



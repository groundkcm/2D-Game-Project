import game_framework
from pico2d import *
import title_state
import server


name = "PassState"
gameover = None
tname = None
theend = None
image = None
menu = None

def enter():
    global gameover, tname, theend, image, menu
    gameover = load_image('./sheets/background/gameover.jpg')
    tname = load_image('./sheets/UI/title eng.png')
    theend = load_image('./sheets/UI/the end.png')
    image = load_image('./sheets/background/title.jpg')
    menu = load_image('./sheets/UI/space.png')

def exit():
    global gameover, tname, theend, image, menu
    del(gameover, tname, theend, image, menu)

def update():
    pass

def draw():
    global gameover, tname, theend, image, menu
    clear_canvas()
    if server.gameover == 1:
        gameover.draw(400, 300)
        menu.draw(725, 25)
    else:
        image.draw(400, 300)
        tname.draw(400, 400)
        theend.draw(400, 200)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
            ax, ay = event.x, 600 - event.y
            if 650 < ax - 10 < 800 and 0 < ay < 50:
                server.gameover, server.theend = 0, 0
                game_framework.change_state(title_state)
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                server.gameover, server.theend = 0, 0
                game_framework.change_state(title_state)


def pause():
    pass


def resume():
    pass



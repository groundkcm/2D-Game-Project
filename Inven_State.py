import game_framework
import main_state
from pico2d import *
import server

import game_world

name = "InvenState"
inventory = None
x_but = None
stage1 = None
start = None
stage2 = None
stage3 = None
potion = None

ax, ay = 0, 0
mx, my = 55, 397
drag = False

def enter():
    global inventory, x_but, stage1, start, stage2, stage3, potion
    start = load_image('prison.png')
    stage1 = load_image('background1.png')
    stage2 = load_image('background2.png')
    stage3 = load_image('bossstage.png')
    inventory = load_image('inventory.png')
    x_but = load_image('X Button.png')
    potion = load_image('red potion.png')


def exit():
    global inventory, x_but, stage1, start, stage2, stage3, potion
    del(inventory, x_but, stage1, start, stage2, stage3, potion)

def handle_events():
    global ax, ay, drag, mx, my
    events = get_events()
    for event in events:
        if event.type == SDL_MOUSEMOTION:
            ax, ay = event.x, 600 - event.y
        if event.type == SDL_MOUSEBUTTONDOWN:
            ax, ay = event.x, 600 - event.y
            if event.button == SDL_BUTTON_LEFT and (730 < ax - 10 < 770 and 430 < ay < 470):
                game_framework.change_state(main_state)
            elif event.button == SDL_BUTTON_LEFT and (40 < ax - 10 < 70 and 365 < ay < 430):
                drag = True
        elif event.type == SDL_MOUSEBUTTONUP and drag:
            ax, ay = event.x, 600 - event.y
            drag = False
            mx, my = ax, ay

def draw():
    global ax, ay, drag, mx, my
    WIDTH, HEIGHT = 1280 - server.x * 2 + 160, 960 - server.y * 2 + 120
    if WIDTH >= 640:
        WIDTH = 640
    elif WIDTH <= 160:
        WIDTH = 160
    if HEIGHT >= 480:
        HEIGHT = 480
    elif HEIGHT <= 120:
        HEIGHT = 120
    clear_canvas()
    stage1.draw(WIDTH, HEIGHT)
    inventory.draw(400, 300)
    x_but.draw(750, 450)
    if drag:
        potion.draw(ax, ay)
    else:
        potion.draw(mx, my)
    update_canvas()



def update():
    pass


def pause():
    pass


def resume():
    pass

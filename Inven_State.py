import game_framework
import main_state
from pico2d import *
import server

import game_world

name = "InvenState"

png_names = ['inventory', 'stage1', 'stage2', 'stage3', 'start']
item_names = ['key', 'red potion', 'big red potion', 'blue potion']

ax, ay = 0, 0
mx, my = 55, 397
drag = False
images = None
x_but = None

window_left = 0
window_bottom = 0

def load_images():
    global images
    if images == None:
        images = {}
        for name in png_names:
            images[name] = load_image("./sheets/background/" + name + ".png")
        for name in item_names:
            images[name] = load_image("./sheets/item/" + name + ".png")


def enter():
    global x_but
    load_images()
    x_but = load_image('./sheets/UI/X Button.png')


def exit():
    global x_but
    del(x_but)

def handle_events():
    global ax, ay, drag, mx, my
    events = get_events()
    for event in events:
        if event.type == SDL_MOUSEMOTION:
            ax, ay = event.x, 600 - event.y
        if event.type == SDL_MOUSEBUTTONDOWN:
            ax, ay = event.x, 600 - event.y
            if event.button == SDL_BUTTON_LEFT and (730 < ax - 10 < 770 and 430 < ay < 470):
                game_framework.pop_state()
            elif event.button == SDL_BUTTON_LEFT and (40 < ax - 10 < 70 and 365 < ay < 430):
                drag = True
        elif event.type == SDL_MOUSEBUTTONUP and drag:
            ax, ay = event.x, 600 - event.y
            drag = False
            mx, my = ax, ay

def draw():
    global ax, ay, drag, mx, my, images
    global window_left, window_bottom
    clear_canvas()
    if server.clear == 1:
        images['stage1'].clip_draw_to_origin(window_left, window_bottom, server.background.canvas_width, server.background.canvas_height, 0, 0)
    elif server.clear == 2:
        images['stage2'].clip_draw_to_origin(window_left, window_bottom, server.background.canvas_width, server.background.canvas_height, 0, 0)
    elif server.clear == 3:
        images['stage3'].clip_draw_to_origin(window_left, window_bottom, server.background.canvas_width, server.background.canvas_height, 0, 0)
    else:
        images['start'].clip_draw_to_origin(window_left, window_bottom, server.background.canvas_width, server.background.canvas_height, 0, 0)


    images['inventory'].draw(400, 300)

    x_but.draw(750, 450)
    check = 0
    if drag:
        images['red potion'].draw(ax, ay)
    else:
        if mx != 55 and my != 397:
            check += 1
            if check == 1:
                server.boy.hp += 30
        images['red potion'].draw(mx, my)
    update_canvas()



def update():
    global window_left, window_bottom
    window_left = clamp(0, int(server.boy.x) - server.background.canvas_width // 2, server.background.w - server.background.canvas_width)
    window_bottom = clamp(0, int(server.boy.y) - server.background.canvas_height // 2, server.background.h - server.background.canvas_height)


def pause():
    pass


def resume():
    pass

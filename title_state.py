import random
import json
import pickle
import os

import game_framework
import game_world
import main_state
from pico2d import *


name = "TitleState"
image = None
play = None
exitb = None
tname = None
arrow = None

def enter():
    global image, play, exitb, tname, arrow
    image = load_image('./sheets/background/title.jpg')
    play = load_image('./sheets/UI/Play Button.png')
    exitb = load_image('./sheets/UI/Exit Button.png')
    tname = load_image('./sheets/UI/title eng.png')
    arrow = load_image('./sheets/UI/Arrow.png')
    # bgm = load_music('stage bgm.mp3')
    # bgm.set_volume(64)
    # bgm.repeat_play()


def exit():
    global image, play, exitb, tname, arrow
    del(image, play, exitb, tname, arrow)

ax, ay = 0, 0
def handle_events():
    global ax, ay
    events = get_events()
    for event in events:
        if event.type == SDL_MOUSEMOTION:
            ax, ay = event.x, 600 - event.y
        elif (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
            ax, ay = event.x, 600 - event.y
            if 300 - 75 < ax - 10 < 300 + 75 and 100 - 25 < ay < 100 + 25:
                game_framework.change_state(main_state)
            elif 500 - 75 < ax - 10 < 500 + 75 and 100 - 25 < ay < 100 + 25:
                game_framework.quit()
        elif event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)

def draw():
    global ax, ay, image, play, exitb, tname
    # hide_cursor()
    clear_canvas()
    arrow.draw(ax, ay)
    image.draw(250, 300)
    play.draw(300, 100)
    exitb.draw(500, 100)
    tname.draw(400, 400)
    update_canvas()



def update():
    pass


def pause():
    pass


def resume():
    pass







import random
import json
import os
from pico2d import *
import game_framework
from gretel import Gretel
from background import Background


name = "MainState"

gretel = None
background = None
font = None


def enter():
    global gretel, background
    gretel = Gretel()
    background = Background()


def exit():
    global gretel, background
    del gretel
    del background


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            gretel.handle_event(event)



def update():
    gretel.update()

def draw():
    clear_canvas()
    background.draw()
    gretel.draw()
    update_canvas()







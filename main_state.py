import random
import json
import os

from pico2d import *
import game_framework
import title_state
import game_world

from boy import Boy
from grass import Grass
from inventory import Inven
from witch import Witch
from mushroom import Mushroom
from skeleton2 import Skeleton2
# from skeleton import Skeleton

name = "MainState"

boy = None

def enter():
    global boy
    boy = Boy()
    grass = Grass()
    inven = Inven()
    witch = Witch()
    mushroom = Mushroom()
    # skeleton = Skeleton()
    # skeleton2 = Skeleton2()
    game_world.add_object(grass, 0)
    # game_world.add_object(witch, 1)
    game_world.add_object(boy, 1)
    game_world.add_object(inven, 1)
    # game_world.add_object(skeleton, 1)
    # game_world.add_object(skeleton2, 1)
    game_world.add_object(mushroom, 1)


def exit():
    game_world.clear()

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
                game_framework.change_state(title_state)
        else:
            boy.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()
    delay(0.01)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()







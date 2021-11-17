import random
import json
import os

from pico2d import *
import game_framework
import title_state
import game_world

from boy import Boy, AttackState
from grass import Grass
from inventory import Inven
from witch import Witch
from mushroom import Mushroom
from skeleton2 import Skeleton2
# from skeleton import Skeleton

name = "MainState"

boy = None
grass = None
inven = None
witch = None
skeletons = []
skeletons2 = []
mushrooms = []
items = Grass.items

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def enter():
    global grass
    grass = Grass()
    game_world.add_object(grass, 0)

    global boy
    boy = Boy()
    game_world.add_object(boy, 1)

    global witch
    witch = Witch()
    # game_world.add_object(witch, 1)

    # global skeletons
    # skeletons = [Skeleton() for i in range(10)] + [Skeleton2() for i in range(10)]
    # game_world.add_objects(skeletons, 1)

    global mushrooms
    mushrooms = [Mushroom() for i in range(1)]
    game_world.add_objects(mushrooms, 1)

    global inven
    inven = Inven()
    game_world.add_object(inven, 1)


def exit():
    global grass
    game_world.clear()
    # grass.bgm.stop()

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
    # delay(0.01)

    for mushroom in mushrooms:
        if collide(boy, mushroom):
            boy.stop()
            if boy.cur_state == AttackState:
                mushroom.hp -= 20

    # for item in items:
    #     if collide(boy, item):
    #         boy.searchitem()

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()







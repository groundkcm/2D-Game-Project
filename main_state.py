import random
import json
import os

from pico2d import *
import game_framework
import title_state
import Inven_State
import pass_state
import game_world
import server

from boy import Boy
from grass import Grass
from witch import Witch
from mushroom import Mushroom
from skeleton2 import Skeleton2
# from skeleton import Skeleton
from collision import collide

name = "MainState"


def enter():
    server.grass = Grass()
    game_world.add_object(server.grass, 0)

    server.witch = Witch()
    # game_world.add_object(server.witch, 1)

    # server.skeletons = [Skeleton() for i in range(10)] + [Skeleton2() for i in range(10)]
    # game_world.add_objects(server.skeletons, 1)

    server.mushrooms = [Mushroom() for i in range(1)]
    game_world.add_objects(server.mushrooms, 1)

    server.boy = Boy()
    game_world.add_object(server.boy, 1)


def exit():
    game_world.clear()
    server.grass.bgm.stop()

def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            ax, ay = event.x, 600 - event.y
            if event.button == SDL_BUTTON_LEFT and (ax - 10 < 40 and ay > 560):
                game_framework.change_state(Inven_State)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            server.debugmode = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_o:
            server.debugmode = 0
        else:
            server.boy.handle_event(event)
            #server.inven.handle_events() #check


def update():
    for game_object in game_world.all_objects():
        game_object.update()

    if server.gameover == 1 or server.end == 1:
        game_framework.change_state(pass_state)
    # for mushroom in server.mushrooms:
    #     if collide(server.boy, mushroom):
    #         mushroom.stop()
    #         # if server.boy.cur_state == server.boy.AttackState:
    #         #     mushroom.stop()
    #         # else:
    #         #     server.boy.stop()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()







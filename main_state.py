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
from grass import Grass, Wall
from witch import Witch
from mushroom import Mushroom
from skeleton2 import Skeleton2
# from skeleton import Skeleton
from collision import collide

name = "MainState"


def enter():
    server.grass = Grass()
    game_world.add_object(server.grass, 0)

    # server.walls0 = [Wall() for i in range(len(server.start_bound))]
    # server.walls1 = [Wall() for i in range(len(server.stage1_bound))]
    # server.walls2 = [Wall() for i in range(len(server.stage2_bound))]
    # server.walls3 = [Wall() for i in range(len(server.stage3_bound))]
    # game_world.add_object(server.walls0, 1)
    # game_world.add_object(server.walls1, 1)
    # game_world.add_object(server.walls2, 1)
    # game_world.add_object(server.walls3, 1)

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
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            ax, ay = event.x, 600 - event.y
            if ax - 10 < 40 and ay > 560:
                game_framework.push_state(Inven_State)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            server.debugmode = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_o:
            server.debugmode = 0
        else:
            server.boy.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()

    if server.gameover == 1 or server.end == 1:
        game_framework.change_state(pass_state)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()







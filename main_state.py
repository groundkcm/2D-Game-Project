import random
import json
import pickle
import os

from pico2d import *
import game_framework
import title_state
import Inven_State
import pass_state
import game_world
import server

from boy import Boy
from grass import FixedBackground as Grass
from witch import Witch
from mushroom import Mushroom
from skeleton2 import Skeleton2
# from skeleton import Skeleton
from collision import collide

name = "MainState"


def enter():
    server.background = Grass()
    game_world.add_object(server.background, 0)
    # server.grass = Grass()
    # game_world.add_object(server.grass, 0)

    server.walls0 = title_state.get_wall0()
    server.walls1 = title_state.get_wall1()
    server.walls2 = title_state.get_wall2()
    server.walls3 = title_state.get_wall3()

    server.trigger0 = title_state.get_trigger0()
    server.trigger1 = title_state.get_trigger1()
    server.trigger2 = title_state.get_trigger2()
    server.trigger3 = title_state.get_trigger3()

    server.witch = Witch()
    # game_world.add_object(server.witch, 1)

    # server.skeletons = [Skeleton() for i in range(10)] + [Skeleton2() for i in range(10)]
    # game_world.add_objects(server.skeletons, 1)

    server.mushroom = title_state.get_mushroom()

    server.boy = title_state.get_boy()


def exit():
    game_world.clear()
    server.background.bgm.stop()

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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_n:
            server.no = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_y:
            server.yes = 1
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







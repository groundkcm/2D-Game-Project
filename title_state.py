import random
import json
import pickle
import os

import game_framework
import game_world
import main_state
from pico2d import *
import server

from boy import Boy
from mushroom import Mushroom
from grass import Wall

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

def get_boy():
    return server.boy

def get_mushroom():
    return server.mushroom

def get_wall0():
    return server.walls0

def create_new_world():
    server.boy = Boy()
    game_world.add_object(server.boy, 1)

    # with open('./data/start.json', 'r') as f:
    #     start_wall = json.load(f)
    # for data in start_wall:
    #     server.walls0 = Wall(data['x1'], data['y1'], data['x2'], data['y2'])
    #     game_world.add_object(server.walls0, 1)
    #
    # with open('./data/start_tri.json', 'r') as f:
    #     start_tri = json.load(f)
    # for data in start_tri:
    #     server.trigger0 = Wall(data['x1'], data['y1'], data['x2'], data['y2'])
    #     game_world.add_object(server.trigger0, 1)

    # with open('./data/stage1.json', 'r') as f:
    #     stage1_wall = json.load(f)
    # for data in stage1_wall:
    #     server.walls1 = Wall(data['x1'], data['y1'], data['x2'], data['y2'])
    #     game_world.add_object(server.walls1, 1)
    #
    # with open('./data/stage1_tri.json', 'r') as f: # 트리거 클래스 만들기
    #     stage1_tri = json.load(f)
    # for data in stage1_tri:
    #     server.trigger1 = Wall(data['x1'], data['y1'], data['x2'], data['y2'])
    #     game_world.add_object(server.trigger1, 1)

    # with open('./data/stage2.json', 'r') as f:
    #     stage2_wall = json.load(f)
    # for data in stage2_wall:
    #     server.walls2 = Wall(data['x1'], data['y1'], data['x2'], data['y2'])
    #     game_world.add_object(server.walls2, 1)
    #
    # with open('./data/stage2_tri.json', 'r') as f:
    #     stage2_tri = json.load(f)
    # for data in stage2_tri:
    #     server.trigger2 = Wall(data['x1'], data['y1'], data['x2'], data['y2'])
    #     game_world.add_object(server.trigger2, 1)

    with open('./data/stage3.json', 'r') as f:
        stage3_wall = json.load(f)
    for data in stage3_wall:
        server.walls3 = Wall(data['x1'], data['y1'], data['x2'], data['y2'])
        game_world.add_object(server.walls3, 1)

    # with open('./data/stage1_mushroom.json', 'r') as f:
    #     mushroom_data_list = json.load(f)
    # for data in mushroom_data_list:
    #     server.mushroom = Mushroom(data['name'], data['x'], data['y'], data['hp'])
    #     game_world.add_object(server.mushroom, 1)


def load_saved_world():
    game_world.load()
    for o in game_world.all_objects():
        if isinstance(o, Boy):
            server.boy = o
            break

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
                create_new_world()
                game_framework.change_state(main_state)
            elif 500 - 75 < ax - 10 < 500 + 75 and 100 - 25 < ay < 100 + 25:
                game_framework.quit()
        elif event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                create_new_world()
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







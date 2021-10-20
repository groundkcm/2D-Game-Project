from pico2d import *
# from time import time

num = 0
def jumping():
    global dir, high
    global num
    turn['run'], turn['attack'], turn['defence'] = False, False, False

    if num < 9:
        high = 1
    else:
        high = -1
    num += 1

    if num == 19:
        turn['jump'] = False
        turn['stop'] = True #뛰는 중 점프 했을때 착지 시 모션변화 없음.
        high = 0

click = 0

def attacking():
    global click
    turn['run'], turn['jump'], turn['defence'] = False, False, False

    if click == 1:
        frame['attack'] = (frame['attack'] + 1) % 26
        if frame['attack'] == 7:
            turn['attack'] = False
            turn['stop'] = True
    elif click == 2:
        frame['attack'] = (frame['attack'] + 1) % 26
        if frame['attack'] == 15:
            turn['attack'] = False
            turn['stop'] = True
    elif click == 0:
        frame['attack'] = (frame['attack'] + 1) % 26
        if frame['attack'] == 25:
            turn['attack'] = False
            turn['stop'] = True


def defencing():
    global num, dir
    turn['run'], turn['jump'], turn['attack'] = False, False, False

    num += 1
    dir = -1
    if num == 8:
        turn['defence'] = False
        turn['stop'] = True
        dir = 0

def crash_events():
    global dir, high
    x1, y1, num1, num2 = gretel['x'], gretel['y'], gretel['width'], gretel['height']
    mx, my, mw, mh = 0, 0, 0, 0
    for i in Characters:
        if i == "skeleton1_1":
            mx, my, mw, mh = skeleton1_1['x'], skeleton1_1['y'], skeleton1_1['width'], skeleton1_1['height']
        elif i == "skeleton1_2":
            mx, my, mw, mh = skeleton1_2['x'], skeleton1_2['y'], skeleton1_2['width'], skeleton1_2['height']
        if mx - mw < x1 + num1 < mx + mw and y1 + num2 > my - mh and y1 - num2 < my + mh:
            gretel['x'] -= 10
            gretel['Hp'] = gretel['Hp'] - 60
        elif mx - mw < x1 - num1 < mx + mw and y1 + num2 > my - mh and y1 - num2 < my + mh:
            gretel['x'] += 10
            gretel['Hp'] = gretel['Hp'] - 60
        elif my - mh < y1 + num2 < my + mh and x1 + num1 > mx - mw and x1 - num1 < mx + mw:
            gretel['y'] -= 10
            gretel['Hp'] = gretel['Hp'] - 60
        elif my - mh < y1 - num2 < my + mh and x1 + num1 > mx - mw and x1 - num1 < mx + mw:
            gretel['y'] += 10
            gretel['Hp'] = gretel['Hp'] - 60

def monsters_AI():
    global dir, high
    x1, y1, num1, num2 = 0, 0, 0, 0
    mx, my, mw, mh = 0, 0, 0, 0
    chosei, chosej = 0, 0
    for i in Characters:
        if i == 'skeleton1_1':
            x1, y1, num1, num2 = skeleton1_1['x'], skeleton1_1['y'], skeleton1_1['width'], skeleton1_1['height']
            chosei = i
            break
        elif i == 'skeleton1_2':
            x1, y1, num1, num2 = skeleton1_2['x'], skeleton1_2['y'], skeleton1_2['width'], skeleton1_2['height']
            chosei = i
            break
    for j in Characters:
        if chosei != 0 and chosei == j:
            continue
        if j == 'skeleton1_1':
            mx, my, mw, mh = skeleton1_1['x'], skeleton1_1['y'], skeleton1_1['width'], skeleton1_1['height']
            chosej = j
            break
        elif j == 'skeleton1_2':
            mx, my, mw, mh = skeleton1_2['x'], skeleton1_2['y'], skeleton1_2['width'], skeleton1_2['height']
            chosej = j
            break
    # if chosei != 0 and chosej != 0:
    #     if mx - mw < x1 + num1 < mx + mw and y1 + num2 > my - mh and y1 - num2 < my + mh:
    #         gretel['x'] -= 10
    #         gretel['Hp'] = gretel['Hp'] - 60
    #     elif mx - mw < x1 - num1 < mx + mw and y1 + num2 > my - mh and y1 - num2 < my + mh:
    #         gretel['x'] += 10
    #         gretel['Hp'] = gretel['Hp'] - 60
    #     elif my - mh < y1 + num2 < my + mh and x1 + num1 > mx - mw and x1 - num1 < mx + mw:
    #         gretel['y'] -= 10
    #         gretel['Hp'] = gretel['Hp'] - 60
    #     elif my - mh < y1 - num2 < my + mh and x1 + num1 > mx - mw and x1 - num1 < mx + mw:
    #         gretel['y'] += 10
    #         gretel['Hp'] = gretel['Hp'] - 60

timer = False
start, end = 0.0, 0.0
def handle_events():
    global play
    global dir, direct, num, click, high, ax, ay, inven
    global start, end, timer
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            play = False
        elif event.type == SDL_KEYDOWN:
            turn['stop'] = False
            if event.key == SDLK_d:
                turn['run'] = True
                direct = 1
                dir += 1
            elif event.key == SDLK_a:
                turn['run'] = True
                direct = -1
                dir -= 1
            elif event.key == SDLK_w:
                turn['run'] = True
                high += 1
            elif event.key == SDLK_s:
                turn['run'] = True
                high -= 1
            elif event.key == SDLK_ESCAPE:
                play = False
            elif event.key == SDLK_SPACE:
                turn['jump'] = True
                num = 0
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_d:
                turn['run'] = False
                turn['stop'] = True
                dir -= 1
            elif event.key == SDLK_a:
                turn['run'] = False
                turn['stop'] = True
                dir += 1
            elif event.key == SDLK_w:
                turn['run'] = False
                turn['stop'] = True
                high -= 1
            elif event.key == SDLK_s:
                turn['run'] = False
                turn['stop'] = True
                high += 1
        if event.type == SDL_MOUSEMOTION:
            ax, ay = event.x, 600 - event.y
        if event.type == SDL_MOUSEBUTTONDOWN:
            ax, ay = event.x, 600 - event.y
            if inven == 0:
                if event.button == SDL_BUTTON_LEFT and (ax - 10 < 50 and ay > 550):
                    inven = 1
                elif event.button == SDL_BUTTON_LEFT:
                    turn['stop'] = False
                    turn['attack'] = True
                    click = (click + 1) % 3
                elif event.button == SDL_BUTTON_RIGHT:
                    turn['stop'] = False
                    turn['defence'] = True
                    num = 0
            elif inven == 1:
                if event.button == SDL_BUTTON_LEFT and (735 < ax-10 < 765 and 435 < ay < 465):
                    inven = 0

open_canvas()
hide_cursor()
arrow = load_image('Arrow.png')
inventory = load_image('inventory.png')
inven_but = load_image('inventory button.png')
x_but = load_image('X Button.png')
stage1 = load_image('background1.png')
stage2 = load_image('background2.png')
crun_r = load_image('gretel run sheet.png')
crun_l = load_image('gretel run_left sheet.png')
cstop = load_image('gretel stop sheet.png')
cjump = load_image('gretel jump sheet.png')
cattack = load_image('gretel attack sheet.png')
cattack_l = load_image('gretel attack_left sheet.png')
cdefence = load_image('gretel defence sheet.png')
cdied = load_image('gretel hurt sheet.png')
skstop = load_image('skeleton stop.png')

play = True
turn = {'run': False, 'jump': False, 'stop': True, 'attack': False, 'defence': False}
keys = {'stage2': False, 'stage3': False, 'stage4': False}
inven = 0
frame = {'run': 0, 'stop': 0, 'jump': 0, 'attack': 0, 'defence': 0, 'died': 0}
Characters = ['gretel', 'skeleton1_1', 'skeleton1_2']
gretel = {'Hp': 110, 'x': 800//2, 'y': 150, 'width': 15, 'height': 20}
skeleton1_1 = {'Hp': 50, 'x': 200, 'y': 200, 'width': 20, 'height': 25, 'dir': 1}
skeleton1_2 = {'Hp': 50, 'x': 200, 'y': 300, 'width': 20, 'height': 25, 'dir': 1}
m1frame = {'stop': 0, 'run': 0, 'attack': 0, 'defence': 0}
direct, dir = 1, 0
high = 0
two = 0
ax, ay = 0, 0

while play:
    WIDTH, HEIGHT = 1280 - gretel['x'] * 2 + 160, 960 - gretel['y'] * 2 + 120
    if WIDTH >= 640:
        WIDTH = 640
    elif WIDTH <= 160:
        WIDTH = 160
    if HEIGHT >= 480:
        HEIGHT = 480
    elif HEIGHT <= 120:
        HEIGHT = 120

    clear_canvas()
    if keys['stage2']:
        stage2.draw(WIDTH, HEIGHT)
        keys['stage2'] = False
    elif keys['stage3']:
        # stage3.draw(WIDTH, HEIGHT)
        keys['stage4'] = False
    elif keys['stage3']:
        # stage3.draw(WIDTH, HEIGHT)
        keys['stage4'] = False
    else:
        stage1.draw(WIDTH, HEIGHT)
    two = (two + 1) % 2
    if inven == 1:
        inventory.draw(400, 300)
        x_but.draw(750, 450)
    else:
        inven_but.draw(25, 575)
        skstop.clip_draw(m1frame['stop'] * 150, 0, 150, 150, skeleton1_1['x'], skeleton1_1['y'])
        skstop.clip_draw(m1frame['stop'] * 150, 0, 150, 150, skeleton1_2['x'], skeleton1_2['y'])
        m1frame['stop'] = (m1frame['stop'] + two) % 4
        if gretel['Hp'] < 0:
            cdied.clip_draw(frame['died'] * 100, 0, 100, 100, gretel['x'], gretel['y'])
            frame['died'] = (frame['died'] + two) % 7
            if frame['died'] == 0:
                gretel['Hp'] = 110
                gretel['x'], gretel['y'] = 400, 150
        elif turn['stop']:
            cstop.clip_draw(frame['stop'] * 100, 0, 100, 100, gretel['x'], gretel['y'])
            frame['stop'] = (frame['stop'] + 1) % 18
        elif direct > 0 and turn['run']:
            crun_r.clip_draw(frame['run'] * 100, 0, 100, 100, gretel['x'], gretel['y'])
            frame['run'] = (frame['run'] + 1) % 24
        elif direct < 0 and turn['run']:
            crun_l.clip_draw(frame['run'] * 100, 0, 100, 100, gretel['x'], gretel['y'])
            frame['run'] = (frame['run'] + 1) % 24
        elif turn['jump']:
            cjump.clip_draw(frame['jump'] * 100, 0, 100, 100, gretel['x'], gretel['y'])
            frame['jump'] = (frame['jump'] + 1) % 19
        elif direct > 0 and turn['attack']:
            cattack.clip_draw(frame['attack'] * 100, 0, 100, 100, gretel['x'], gretel['y'])
        elif direct < 0 and turn['attack']:
            cattack_l.clip_draw((25 - frame['attack']) * 100, 0, 100, 100, gretel['x'], gretel['y'])
        elif turn['defence']:
            cdefence.clip_draw(frame['defence'] * 112, 0, 112, 100, gretel['x'], gretel['y'])
            frame['defence'] = (frame['defence'] + two) % 4
    arrow.draw(ax, ay)
    update_canvas()
    # monsters_AI()
    crash_events()
    if turn['jump']:
        jumping()
    elif turn['attack']:
        attacking()
    elif turn['defence']:
        defencing()

    handle_events()
    gretel['x'] += dir * 3
    gretel['y'] += high * 3
    delay(0.05)

close_canvas()


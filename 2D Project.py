from pico2d import *

num = 0

def jumping():
    global dir, high
    global num
    keys['run'], keys['attack'], keys['defence'] = False, False, False

    if num < 9:
        high = 1
    else:
        high = -1
    num += 1

    if num == 19:
        keys['jump'] = False
        keys['stop'] = True #뛰는 중 점프 했을때 착지 시 모션변화 없음.
        high = 0

click = 0

def attacking():
    global click
    keys['run'], keys['jump'], keys['defence'] = False, False, False
    if click == 1:
        frame['attack'] = (frame['attack'] + 1) % 26
        if frame['attack'] == 7:
            keys['attack'] = False
            keys['stop'] = True
    elif click == 2:
        frame['attack'] = (frame['attack'] + 1) % 26
        if frame['attack'] == 15:
            keys['attack'] = False
            keys['stop'] = True
    elif click == 0:
        frame['attack'] = (frame['attack'] + 1) % 26
        if frame['attack'] == 25:
            keys['attack'] = False
            keys['stop'] = True


def defencing():
    global num, dir
    keys['run'], keys['jump'], keys['attack'] = False, False, False

    num += 1
    dir -= 1
    if num == 8:
        keys['defence'] = False
        keys['stop'] = True
        dir += 1

def crash_events():
    global dir, high
    x1, y1, num1, num2 = gretel['x'], gretel['y'], gretel['width'], gretel['height']
    mx, my, mw, mh = 0, 0, 0, 0
    for i in Characters:
        if i == "skeleton1_1":
            mx, my, mw, mh = skeleton1_1['x'], skeleton1_1['y'], skeleton1_1['width'], skeleton1_1['height']
        elif i == "skeleton1_2":
            mx, my, mw, mh = skeleton1_2['x'], skeleton1_2['y'], skeleton1_2['width'], skeleton1_2['height']
        if x1 + num1 > mx - mw:
            dir -= 1
            gretel['Hp'] = gretel['Hp'] - 60
        elif x1 - num1 < mx + mw:
            dir += 1
            gretel['Hp'] = gretel['Hp'] - 60
        elif y1 + num2 > my - mh:
            high -= 1
            gretel['Hp'] = gretel['Hp'] - 60
        elif y1 - num2 < my + mw:
            high += 1
            gretel['Hp'] = gretel['Hp'] - 60

def monsters_AI():
    global dir, high
    x1, y1, num1, num2 = 0, 0, 0, 0
    mx, my, mw, mh = 0, 0, 0, 0
    for i in range(0, len(Characters) + 1):
        if Characters[i] == 'skeleton1_1':
            x1, y1, num1, num2 = skeleton1_1['x'], skeleton1_1['y'], skeleton1_1['width'], skeleton1_1['height']
        elif Characters[i] == 'skeleton1_2':
            x1, y1, num1, num2 = skeleton1_2['x'], skeleton1_2['y'], skeleton1_2['width'], skeleton1_2['height']
        for j in range(i + 1, len(Characters) + 1):
            if Characters[i] == 'skeleton1_1':
                mx, my, mw, mh = skeleton1_1['x'], skeleton1_1['y'], skeleton1_1['width'], skeleton1_1['height']
            elif Characters[i] == 'skeleton1_2':
                mx, my, mw, mh = skeleton1_2['x'], skeleton1_2['y'], skeleton1_2['width'], skeleton1_2['height']
            if x1 + num1 > mx - mw:
                dir -= 1 #방향 반대로 바꾸기 class??
            elif x1 - num1 < mx + mw:
                dir += 1
            elif y1 + num2 > my - mh:
                high -= 1
            elif y1 - num2 < my + mw:
                high += 1

def handle_events():
    global play
    global dir, direct, num, click, high, ax, ay, inven
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            play = False
        elif event.type == SDL_KEYDOWN:
            keys['stop'] = False
            if event.key == SDLK_RIGHT:
                keys['run'] = True
                direct = 1
                dir += 1
            elif event.key == SDLK_LEFT:
                keys['run'] = True
                direct = -1
                dir -= 1
            elif event.key == SDLK_UP:
                keys['run'] = True
                high += 1
            elif event.key == SDLK_DOWN:
                keys['run'] = True
                high -= 1
            elif event.key == SDLK_ESCAPE:
                play = False
            elif event.key == SDLK_SPACE:
                keys['jump'] = True
                num = 0
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                keys['run'] = False
                keys['stop'] = True
                dir -= 1
            elif event.key == SDLK_LEFT:
                keys['run'] = False
                keys['stop'] = True
                dir += 1
            elif event.key == SDLK_UP:
                keys['run'] = False
                keys['stop'] = True
                high -= 1
            elif event.key == SDLK_DOWN:
                keys['run'] = False
                keys['stop'] = True
                high += 1
        if event.type == SDL_MOUSEMOTION:
            ax, ay = event.x, 600 - event.y
        elif event.type == SDL_MOUSEMOTION and event.type == SDL_MOUSEBUTTONDOWN:
            if inven == 0:
                if event.button == SDL_BUTTON_LEFT and ax-10 < 30 and ay > 570:
                    inven = 1
                elif event.button == SDL_BUTTON_LEFT:
                    keys['stop'] = False
                    keys['attack'] = True
                    click = (click + 1) % 3
                elif event.button == SDL_BUTTON_RIGHT:
                    keys['stop'] = False
                    keys['defence'] = True
                    num = 0
            elif inven == 1:
                if event.button == SDL_BUTTON_LEFT and 590 < ax-10 < 610 and 440 < ay < 460:
                    inven = 0



open_canvas()
hide_cursor()
arrow = load_image('Arrow.png')
inventory = load_image('inventory.png')
inven_but = load_image('inventory button.png')
x_but = load_image('X Button.png')
stage1 = load_image('background1.png')
crun_r = load_image('gretel run sheet.png')
crun_l = load_image('gretel run_left sheet.png')
cstop = load_image('gretel stop sheet.png')
cjump = load_image('gretel jump sheet.png')
cattack = load_image('gretel attack sheet.png')
cdefence = load_image('gretel defence sheet.png')
cdied = load_image('gretel hurt sheet.png')
skstop = load_image('skeleton stop.png')

play = True
keys = {'run': False, 'jump': False, 'stop': True, 'attack': False, 'defence': False}
# button = {'inven': False}
inven = 0
frame = {'run': 0, 'stop': 0, 'jump': 0, 'attack': 0, 'defence': 0, 'died': 0}
Characters = ['gretel', 'skeleton1_1', 'skeleton1_2']
gretel = {'Hp': 110, 'x': 800//2, 'y': 150, 'width': 10, 'height': 20}
skeleton1_1 = {'Hp': 50, 'x': 200, 'y': 200, 'width': 15, 'height': 30, 'dir': 1}
skeleton1_2 = {'Hp': 50, 'x': 200, 'y': 300, 'width': 15, 'height': 30, 'dir': 1}
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
    stage1.draw(WIDTH, HEIGHT)
    inven_but.draw(15, 585)
    two = (two + 1) % 2
    skstop.clip_draw(m1frame['stop'] * 150, 0, 150, 150, skeleton1_1['x'], skeleton1_1['y'])
    skstop.clip_draw(m1frame['stop'] * 150, 0, 150, 150, skeleton1_2['x'], skeleton1_2['y'])
    m1frame['stop'] = ((m1frame['stop']) + two) % 4
    if inven == 1:
        inventory.draw(400, 300)
        x_but.draw(750, 450)
    else:
        if gretel['Hp'] < 0:
            cdied.clip_draw(frame['died'] * 100, 0, 100, 100, gretel['x'], gretel['y'])
            frame['died'] = (frame['died'] + 1) % 7
        elif keys['stop']:
            cstop.clip_draw(frame['stop'] * 100, 0, 100, 100, gretel['x'], gretel['y'])
            frame['stop'] = (frame['stop'] + 1) % 18
        elif direct > 0 and keys['run']:
            crun_r.clip_draw(frame['run'] * 100, 0, 100, 100, gretel['x'], gretel['y'])
            frame['run'] = (frame['run'] + 1) % 24
        elif direct < 0 and keys['run']:
            crun_l.clip_draw(frame['run'] * 100, 0, 100, 100, gretel['x'], gretel['y'])
            frame['run'] = (frame['run'] + 1) % 24
        elif keys['jump']:
            cjump.clip_draw(frame['jump'] * 100, 0, 100, 100, gretel['x'], gretel['y'])
            frame['jump'] = (frame['jump'] + 1) % 19
        elif keys['attack']:
            cattack.clip_draw(frame['attack'] * 100, 0, 100, 100, gretel['x'], gretel['y'])
        elif keys['defence']:
            cdefence.clip_draw(frame['defence'] * 112, 0, 112, 100, gretel['x'], gretel['y'])
            frame['defence'] = (frame['defence'] + two) % 4
    arrow.draw(ax, ay)
    update_canvas()
    # monsters_AI()
    crash_events()
    if keys['jump']:
        jumping()
    elif keys['attack']:
        attacking()
    elif keys['defence']:
        defencing()

    handle_events()
    gretel['x'] += dir * 3
    gretel['y'] += high * 3
    delay(0.05)

close_canvas()


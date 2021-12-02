from pico2d import *
import server
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from collision import collide_wall
import random
import game_world

from mushroom import Mushroom
from skeleton2 import Skeleton2
from skeleton import Skeleton

png_names = ['inventory', 'stage1', 'stage2', 'stage3', 'start']

class FixedBackground:
    images = None

    def load_images(self):
        if FixedBackground.images == None:
            FixedBackground.images = {}
            for name in png_names:
                FixedBackground.images[name] = load_image("./sheets/background/" + name + ".png")

    def __init__(self):
        self.load_images()
        self.arrow = load_image('./sheets/UI/Arrow.png')
        self.inven_but = load_image('./sheets/UI/inventory button.png')
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.window_left = 0
        self.window_bottom = 0

        if server.clear == 1:
            self.w = FixedBackground.images['stage1'].w
            self.h = FixedBackground.images['stage1'].h
        elif server.clear == 2:
            self.w = FixedBackground.images['stage2'].w
            self.h = FixedBackground.images['stage2'].h
        elif server.clear == 3:
            self.w = FixedBackground.images['stage3'].w
            self.h = FixedBackground.images['stage3'].h
        else:
            # Grass.images['start'].draw(WIDTH, HEIGHT)
            self.w = FixedBackground.images['stage1'].w
            self.h = FixedBackground.images['stage1'].h
        self.bgm = load_music('stage bgm.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()
        self.open = load_music('door.mp3')
        self.open.set_volume(32)


    def draw(self):
        if server.clear == 1:
            FixedBackground.images['stage1'].clip_draw_to_origin(self.window_left, self.window_bottom, server.background.canvas_width, server.background.canvas_height,0, 0)
        elif server.clear == 2:
            FixedBackground.images['stage2'].clip_draw_to_origin(self.window_left, self.window_bottom, server.background.canvas_width, server.background.canvas_height,0, 0)
        elif server.clear == 3:
            FixedBackground.images['stage3'].clip_draw_to_origin(self.window_left, self.window_bottom, server.background.canvas_width, server.background.canvas_height,0, 0)
        else:
            FixedBackground.images['start'].clip_draw_to_origin(self.window_left, self.window_bottom, server.background.canvas_width, server.background.canvas_height,0, 0)
            # FixedBackground.images['stage1'].clip_draw_to_origin(self.window_left, self.window_bottom, server.background.canvas_width, server.background.canvas_height,0, 0)
            # FixedBackground.images['stage2'].clip_draw_to_origin(self.window_left, self.window_bottom, server.background.canvas_width, server.background.canvas_height, 0, 0)
            # FixedBackground.images['stage3'].clip_draw_to_origin(self.window_left, self.window_bottom, server.background.canvas_width, server.background.canvas_height, 0, 0)

        self.inven_but.draw(20, 580)

    def update(self):
        self.window_left = clamp(0,int(server.boy.x) - server.background.canvas_width // 2,server.background.w - server.background.canvas_width)
        self.window_bottom = clamp(0,int(server.boy.y) - server.background.canvas_height // 2,server.background.h - server.background.canvas_height)

    def handle_event(self, event):
        pass


class Wall:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def __getstate__(self):
        state = {'x1': self.x1, 'y1': self.y1, 'x2': self.x2, 'y2': self.y2}
        return state

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)


    def update(self):
        if collide_wall(self, server.boy):
            # print('stop')
            server.boy.set_parent_wall(self)

    def get_bb(self):
        cx1, cy1 = self.x1 - server.background.window_left, self.y1 - server.background.window_bottom
        cx2, cy2 = self.x2 - server.background.window_left, self.y2 - server.background.window_bottom
        return cx1, cy1, cx2, cy2

    def draw(self):
        if server.debugmode == 1:
            draw_rectangle(*self.get_bb())


class Trigger:
    font = None
    check = 0

    def __init__(self, x1=0, y1=0, x2=0, y2=0, num = 0):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.num = num
        # self.build_behavior_tree(num)
        if Trigger.font is None:
            Trigger.font = load_font('ENCR10B.TTF', 16)

    def __getstate__(self):
        state = {'x1': self.x1, 'y1': self.y1, 'x2': self.x2, 'y2': self.y2}
        return state

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)

    def order(self, num):
        # server.background = FixedBackground
        cx1, cy1 = self.x1 - server.background.window_left, self.y1 - server.background.window_bottom
        cx2, cy2 = self.x2 - server.background.window_left, self.y2 - server.background.window_bottom

        if num == 4:
            # Trigger.font.draw((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2, '잠겨있다', (255, 255, 255))
            # self.font.draw((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2, '잠겨있다', (255, 255, 255))
            return BehaviorTree.SUCCESS
        else:
            # Trigger.font.draw(cx1, (cy1 + cy2) / 2, 'look around(y/n)', (255, 255, 255))
            # self.font.draw((self.x1 + self.x2)/2, (self.y1 + self.y2)/2, '주변을 살펴본다(y/n)', (255, 255, 255))
            if server.yes == 1:
                server.yes = 0
                return BehaviorTree.SUCCESS
            else:
                return BehaviorTree.FAIL

    def popkey(self):
        server.key = 1
        return BehaviorTree.SUCCESS

    def popitem(self):
        num = random.randrange(1, 3)
        if num == 1:
            server.red_potion += 1
        elif num == 2:
            server.big_red_potion += 1
        elif num == 3:
            server.blue_potion += 1
        return BehaviorTree.SUCCESS

    def popmonster(self):
        num = random.randrange(1, 3)
        if num == 1:
            server.mushroom = Mushroom("new", self.x2 + 50, self.y2 - 50, 40)
            game_world.add_object(server.mushroom, 1)
        elif num == 2:
            server.skeleton = Skeleton("new", self.x2 + 50, self.y2 - 50, 40)
            game_world.add_object(server.skeleton, 1)
        elif num == 3:
            server.skeleton2 = Skeleton2("new", self.x2 + 50, self.y2 - 50, 40)
            game_world.add_object(server.skeleton2, 1)
        return BehaviorTree.SUCCESS

    def opendoor(self):
        if server.key == 1:
            # self.font.draw((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2, '열쇠로 문을 연다(y/n)', (255, 255, 255))
            if server.yes == 1:
                server.yes, server.key = 0, 0
                server.clear += 1
                return BehaviorTree.SUCCESS
            else:
                return BehaviorTree.FAIL
        else:
            return BehaviorTree.FAIL

    def build_behavior_tree(self, num):
        order_node = LeafNode("Order", self.order(num))

        if num == 1:
            key_node = LeafNode('Key', self.popkey())
            popkey_node = SequenceNode('PopKey')
            popkey_node.add_children(order_node, key_node)
            self.bt = BehaviorTree(popkey_node)
        elif num == 2:
            item_node = LeafNode('Item', self.popitem())
            popitem_node = SequenceNode('PopItem')
            popitem_node.add_children(order_node, item_node)
            self.bt = BehaviorTree(popitem_node)
        elif num == 3:
            monster_node = LeafNode('Monster', self.popmonster())
            popmonster_node = SequenceNode('PopMonster')
            popmonster_node.add_children(order_node, monster_node)
            self.bt = BehaviorTree(popmonster_node)
        elif num == 4:
            door_node = LeafNode('Door', self.opendoor())
            opendoor_node = SequenceNode('OpenDoor')
            opendoor_node.add_children(order_node, door_node)
            self.bt = BehaviorTree(opendoor_node)


    def update(self):
        if collide_wall(self, server.boy):
            Trigger.check += 1
            if self.num == 4 and Trigger.check == 1:
                server.clear += 1
                game_world.clear()
        # pass
        # if collide_wall(self, server.boy):
        #     self.bt.run()

    def get_bb(self):
        cx1, cy1 = self.x1 - server.background.window_left, self.y1 - server.background.window_bottom
        cx2, cy2 = self.x2 - server.background.window_left, self.y2 - server.background.window_bottom
        return cx1, cy1, cx2, cy2

    def draw(self):

        # Trigger.font.draw(cx1, (cy1 + cy2) / 2, 'look around(y/n)', (255, 255, 255))
        if server.debugmode == 1:
            draw_rectangle(*self.get_bb())


import game_framework
from pico2d import *
from collision import collide
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import random
import server
import math
import game_world

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 3.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

animation_names = ['attack', 'dead', 'idle', 'walk', 'hit']

class Mushroom:
    images = None
    check = 0
    atk, ht, dead = 0, 0, 0

    def load_images(self):
        if Mushroom.images == None:
            Mushroom.images = {}
            for name in animation_names:
                Mushroom.images[name] = load_image("./sheets/mushroom/" + name + ".png")

    def __init__(self, name='NONAME', x=0, y=0, hp=1, num=0, pnum=0, p1x=0, p2x=0, p3x=0, p4x=0, p1y=0, p2y=0, p3y=0, p4y=0):
        self.name = name
        self.x, self.y = x, y
        self.hp = hp
        self.num = num
        self.pnum = pnum
        self.p1 = p1x, p1y
        self.p2 = p2x, p2y
        self.p3 = p3x, p3y
        self.p4 = p4x, p4y
        self.load_images()
        self.hpbar = load_image('./sheets/UI/monster hp bar.png')
        self.prepare_patrol_points()
        self.patrol_order = 1
        self.build_behavior_tree()
        self.dir = random.random() * 2 * math.pi
        self.speed = 0
        self.parent = None
        self.iframe = 0
        self.wframe = 0
        self.dframe = 0
        self.hframe = 0
        self.aframe = 0
        self.timer = 0.0
        self.wait_timer = 2.0

    def __getstate__(self):
        state = {'x': self.x, 'y': self.y, 'dir':self.dir, 'name' : self.name, 'hp':self.hp}
        return state

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)


    def prepare_patrol_points(self):
        positions = []
        if self.pnum == 2:
            positions = [self.p1, self.p2]
        elif self.pnum == 4:
            positions = [self.p1, self.p2, self.p3, self.p4]

        self.patrol_positions = []
        for p in positions:
            self.patrol_positions.append((p[0], 1024 - p[1]))

    def wander(self):
        self.speed = RUN_SPEED_PPS
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.timer = 1.0
            self.dir = random.random() * 2 * math.pi
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING


    def wait(self):
        self.speed = 0
        self.wait_timer -= game_framework.frame_time
        if self.wait_timer <= 0:
            self.wait_timer = 2.0
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING



    def find_player(self):
        distance = (server.boy.x - self.x) ** 2 + (server.boy.y - self.y) ** 2
        if distance < (PIXEL_PER_METER * 4) ** 2:
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
        return BehaviorTree.FAIL

    def move_to_player(self):
        self.speed = RUN_SPEED_PPS
        self.dir = math.atan2(server.boy.y - self.y, server.boy.x - self.x)
        return BehaviorTree.SUCCESS

    def get_next_position(self):
        self.target_x, self.target_y = self.patrol_positions[self.patrol_order % len(self.patrol_positions)]
        self.patrol_order += 1
        self.dir = math.atan2(self.target_y - self.y, self.target_x - self.x)
        return BehaviorTree.SUCCESS

    def move_to_target(self):
        self.speed = RUN_SPEED_PPS
        distance = (self.target_x - self.x) ** 2 + (self.target_y - self.y) ** 2
        if distance < PIXEL_PER_METER ** 2:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        wander_node = LeafNode("Wander", self.wander)

        patrol_node = SequenceNode("Patrol")
        get_next_position_node = LeafNode("Get Next Position", self.get_next_position)
        move_to_target_node = LeafNode("Move to Target", self.move_to_target)
        patrol_node.add_children(get_next_position_node, move_to_target_node)

        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)

        wait_node = LeafNode('Wait', self.wait)
        if self.num == 1:
            Chase_wait_node = SelectorNode('ChaseWait')
            Chase_wait_node.add_children(chase_node, wait_node)
            self.bt = BehaviorTree(wait_node)
        elif self.num == 2:
            patrol_chase_node = SelectorNode("PatrolChase")
            patrol_chase_node.add_children(chase_node, patrol_node)
            self.bt = BehaviorTree(wait_node)

    def get_bb(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom

        return cx - 20, cy - 25, cx + 20, cy + 20

    def stop(self):
        self.speed = 0

    def hit(self):
        Mushroom.ht = 1
        Mushroom.check += 1
        if Mushroom.check == 30:
            Mushroom.check = 0
            self.hp -= 1

    def add_event(self, event):
        pass

    def set_parent(self, enemy):
        self.parent = enemy
        if math.cos(self.dir) > 0:
            self.x -= self.speed * game_framework.frame_time
        elif math.cos(self.dir) < 0:
            self.x += self.speed * game_framework.frame_time
        if math.sin(self.dir) > 0:
            self.y -= self.speed * game_framework.frame_time
        elif math.sin(self.dir) < 0:
            self.y += self.speed * game_framework.frame_time

    def update(self):
        if self.hp <= 0:
            self.dframe = (self.dframe + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        if collide(self, server.boy):
            Mushroom.atk = 1
            server.boy.set_parent(self)

        self.bt.run()
        self.iframe = (self.iframe + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.wframe = (self.wframe + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.hframe = (self.hframe + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.aframe = (self.aframe + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(50, self.x, server.background.w - 50)
        self.y = clamp(50, self.y, server.background.h - 50)

    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        if self.hp <= 0:
            if math.cos(self.dir) < 0:
                Mushroom.images['dead'].clip_composite_draw(int(self.dframe) * 150, 0, 150, 150, 0, 'h', cx, cy, 150, 150)
            else:
                Mushroom.images['dead'].clip_draw(int(self.dframe) * 150, 0, 150, 150, cx, cy, 150, 150)
            if self.dframe >= 3:
                Mushroom.atk = 0
                game_world.remove_object(self)
        elif Mushroom.ht == 1:
            if math.cos(self.dir) < 0:
                Mushroom.images['hit'].clip_composite_draw(int(self.hframe) * 150, 0, 150, 150, 0, 'h', cx, cy, 150, 150)
            else:
                Mushroom.images['hit'].clip_draw(int(self.hframe) * 150, 0, 150, 150, cx, cy, 150, 150)
            Mushroom.ht = 0
        elif Mushroom.atk == 1:
            if math.cos(self.dir) < 0:
                Mushroom.images['attack'].clip_composite_draw(int(self.aframe) * 150, 0, 150, 150, 0, 'h', cx, cy, 150, 150)
            else:
                Mushroom.images['attack'].clip_draw(int(self.aframe) * 150, 0, 150, 150, cx, cy, 150, 150)
            Mushroom.atk = 0
        elif math.cos(self.dir) < 0:
            if self.speed == 0:
                Mushroom.images['idle'].clip_composite_draw(int(self.iframe) * 150, 0, 150, 150, 0, 'h', cx, cy, 150, 150)
            else:
                Mushroom.images['walk'].clip_composite_draw(int(self.wframe) * 150, 0, 150, 150, 0, 'h', cx, cy, 150, 150)
        else:
            if self.speed == 0:
                Mushroom.images['idle'].clip_draw(int(self.iframe) * 150, 0, 150, 150, cx, cy)
            else:
                Mushroom.images['walk'].clip_draw(int(self.wframe) * 150, 0, 150, 150, cx, cy)

        if server.debugmode == 1:
            draw_rectangle(*self.get_bb())
        self.hpbar.clip_draw(0, 0, self.hp * 40 // 15, 3, cx - (40 - self.hp * 40 // 15)/2, cy + 20)

import game_framework
from pico2d import *
from collision import collide
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import random
import server
import math
import game_world

from fireball import Fire

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 3.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

animation_names = ['idle', 'attack']

class Witch:
    images = None
    check = 0
    one = 0
    px, py = 0, 0
    atk = 0
    effect = 0

    def load_images(self):
        if Witch.images == None:
            Witch.images = {}
            for name in animation_names:
                Witch.images[name] = load_image("./sheets/witch/" + name + ".png")

    def __init__(self, name='NONAME', x=0, y=0, hp=1):
        self.name = name
        self.x, self.y = x, y
        self.hp = hp
        self.parent = None
        self.load_images()
        self.hpbar = load_image('./sheets/UI/monster hp bar.png')
        # self.font = load_font('ENCR10B.TTF', 16)
        self.patrol_order = 1
        self.build_behavior_tree()
        self.dir = random.random() * 2 * math.pi
        self.speed = 0
        self.click = 0
        self.wait_timer = 2.0
        self.frame = 0
        self.aframe = 0
        self.timer = 0


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
        if distance < (PIXEL_PER_METER * 10) ** 2 and distance > (PIXEL_PER_METER * 5) ** 2:
            Witch.effect = 1

        if distance < (PIXEL_PER_METER * 10) ** 2:
            Witch.atk = 1
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
        return BehaviorTree.FAIL

    def move_to_player(self):
        self.speed = RUN_SPEED_PPS
        self.dir = math.atan2(server.boy.y - self.y, server.boy.x - self.x)
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        wander_node = LeafNode("Wander", self.wander)

        wait_node = LeafNode('Wait', self.wait)
        wander_wait_node = SequenceNode('WanderWait')
        wander_wait_node.add_children(wander_node, wait_node)

        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)

        Chase_wander_node = SelectorNode('ChaseWander')
        Chase_wander_node.add_children(chase_node, wander_node)

        self.bt = BehaviorTree(Chase_wander_node)

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

    def get_bb(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        return cx - 20, cy - 40, cx + 20, cy + 45

    def fire_ball(self):
        # cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        fire = Fire(self.x, self.y, self.dir)
        game_world.add_object(fire, 1)

    def stop(self):
        self.speed = 0

    def hit(self):
        Witch.ht = 1
        Witch.check += 1
        if Witch.check == 200:
            Witch.check = 0
            self.hp -= 5

    def update(self):
        if self.hp <= 0:
            server.end = 1
            game_world.remove_object(self)

        if collide(self, server.boy):
            Witch.effect = 0
            server.boy.set_parent(self, 4)

        if Witch.effect:
            Witch.one += 1
            if Witch.one == 1:
                Witch.fire_ball(self)
            if Witch.one == 500:
                Witch.one = 0


        self.bt.run()
        self.aframe = (self.aframe + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 17
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(50, self.x, server.background.w - 50)
        self.y = clamp(50, self.y, server.background.h - 50)

    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom

        if Witch.atk == 1:
            if math.cos(self.dir) < 0:
                Witch.images['attack'].clip_composite_draw(int(self.aframe) * 100, 0, 100, 100, 0, 'h', cx, cy, 100, 100)
            else:
                Witch.images['attack'].clip_draw(int(self.aframe) * 100, 0, 100, 100, cx, cy, 100, 100)
            Witch.atk = 0
        elif math.cos(self.dir) < 0:
            if self.speed == 0:
                Witch.images['idle'].clip_composite_draw(int(self.frame) * 100, 0, 100, 100, 0, 'h', cx, cy, 100, 100)
            else:
                Witch.images['idle'].clip_composite_draw(int(self.frame) * 100, 0, 100, 100, 0, 'h', cx, cy, 100, 100)
        else:
            if self.speed == 0:
                Witch.images['idle'].clip_draw(int(self.frame) * 100, 0, 100, 100, cx, cy)
            else:
                Witch.images['idle'].clip_draw(int(self.frame) * 100, 0, 100, 100, cx, cy)

        if server.debugmode == 1:
            draw_rectangle(*self.get_bb())
        self.hpbar.clip_draw(0, 0, self.hp * 40 // 100, 3, cx - (40 - self.hp * 40 // 100)/2, cy + 50)



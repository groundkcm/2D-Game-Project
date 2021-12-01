import game_framework
from pico2d import *
from collision import collide
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import random
import server
import math
import game_world

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 0.5
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 10000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

animation_names = ['attack', 'dead', 'idle', 'walk']

class Mushroom:
    images = None
    check = 0

    def load_images(self):
        if Mushroom.images == None:
            Mushroom.images = {}
            for name in animation_names:
                Mushroom.images[name] = load_image("./sheets/mushroom/" + name + ".png")

    def __init__(self, name='NONAME', x=0, y=0, hp=1):
        self.name = name
        self.x, self.y = x * PIXEL_PER_METER, y * PIXEL_PER_METER
        self.hp = hp
        self.load_images()
        self.hpbar = load_image('./sheets/UI/monster hp bar.png')
        self.prepare_patrol_points()
        self.patrol_order = 1
        self.build_behavior_tree()
        self.dir = random.random() * 2 * math.pi
        self.speed = 0
        self.frame8 = 0
        self.frame4 = 0
        self.timer = 0.0
        self.wait_timer = 2.0

    def __getstate__(self):
        state = {'x': self.x, 'y': self.y, 'dir':self.dir,'name' : self.name,'hp':self.hp}
        return state

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)


    def prepare_patrol_points(self):
        positions = [(43, 750), (1118, 750), (1050, 530), (575, 220), (235, 33), (575, 220), (1050, 530), (1118, 750)]
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

        wait_node = LeafNode('Wait', self.wait)
        wander_wait_node = SequenceNode('WanderWait')
        wander_wait_node.add_children(wander_node, wait_node)

        get_next_position_node = LeafNode("Get Next Position", self.get_next_position)
        move_to_target_node = LeafNode("Move to Target", self.move_to_target)
        patrol_node = SequenceNode("Patrol")
        patrol_node.add_children(get_next_position_node, move_to_target_node)

        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)

        patrol_chase_node = SelectorNode("PatrolChase")
        patrol_chase_node.add_children(chase_node, patrol_node)

        wander_chase_node = SelectorNode("WanderChase")
        wander_chase_node.add_children(chase_node, wander_node)

        self.bt = BehaviorTree(wait_node)

    def get_bb(self):
        return self.x - 20, self.y - 25, self.x + 20, self.y + 20

    def stop(self):
        self.speed = 0

    def hit(self):
        Mushroom.check += 1
        if Mushroom.check == 30:
            Mushroom.check = 0
            self.hp -= 1

    def add_event(self, event):
        pass

    def update(self):
        if self.hp <= 0:
            game_world.remove_object(self)

        # if collide(self, server.boy):
        #     server.boy.set_parent(self)

        self.bt.run()
        self.frame4 = (self.frame4 + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.frame8 = (self.frame8 + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(-450, self.x, 770)
        self.y = clamp(-330, self.y, 560)
        # if server.x >= 640:
        #     server.x = 640
        # elif server.x <= 400:
        #     server.x = 400
        # if server.y >= 480:
        #     server.y = 480
        # elif server.y <= 300:
        #     server.y = 300

    def draw(self):
        if math.cos(self.dir) < 0:
            if self.speed == 0:
                Mushroom.images['idle'].clip_composite_draw(int(self.frame4) * 150, 0, 150, 150, 0, 'h', self.x, self.y, 150, 150)
            else:
                Mushroom.images['walk'].clip_composite_draw(int(self.frame8) * 150, 0, 150, 150, 0, 'h', self.x, self.y, 150, 150)
        else:
            if self.speed == 0:
                Mushroom.images['idle'].clip_draw(int(self.frame4) * 150, 0, 150, 150, self.x, self.y)
            else:
                Mushroom.images['walk'].clip_draw(int(self.frame8) * 150, 0, 150, 150, self.x, self.y)

        if server.debugmode == 1:
            draw_rectangle(*self.get_bb())
        self.hpbar.clip_draw(0, 0, self.hp, 3, self.x - (40 - self.hp)/2, self.y + 30)

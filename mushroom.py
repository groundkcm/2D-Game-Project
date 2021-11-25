import game_framework
from pico2d import *
from collision import collide
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import random
import server
import game_world

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 1.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 10000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


HIT, RANGE, DEAD, READY, SLEEP, WALK, DEFENCE = range(7)

class IdleState:

    def enter(boy, event):
        boy.timer = 1000

    def exit(boy, event):
        pass

    def do(boy):
        if boy.hp <= 0:
            boy.add_event(DEAD)
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    def draw(boy):
        boy.image.clip_draw(int(boy.frame) * 150, 0, 150, 150, boy.x, boy.y)


class RunState:

    def enter(boy, event):
        boy.dir = clamp(-1, boy.velocity, 1)

    def exit(boy, event):
        pass

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        boy.x += boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 800 - 25)
        boy.y += boy.high * game_framework.frame_time
        boy.y = clamp(25, boy.y, 600 - 25)
        # boy.camera_move()

    # @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.run_r.clip_draw(int(boy.frame) * 150, 0, 150, 150, boy.x, boy.y)
        else:
            boy.run_l.clip_draw(int(boy.frame) * 150, 0, 150, 150, boy.x, boy.y)


class AttackState:
    def enter(self, event):
        pass

    def exit(self, event):
        pass

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10 + 16
        boy.add_event(READY)
        boy.timer -= 10
        if boy.timer == 0:
            boy.add_event(READY)

    def draw(self):
        if self.dir == 1:
            self.attack_r.clip_draw(int(self.frame) * 150, 0, 150, 150, self.x, self.y)
        else:
            self.attack_l.clip_draw(int(self.frame) * 150, 0, 150, 150, self.x, self.y)


class DefenceState:
    def enter(self, event):
        self.timer = 200

    def exit(gretel, event):
        pass

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.timer -= 10
        if self.timer == 0:
            self.add_event(READY)

    def draw(self):
        if self.dir == 1:
            self.defence.clip_draw(int(self.frame) * 150, 0, 150, 150, self.x, self.y)
        else:
            self.defence.clip_draw(int(self.frame) * 150, 0, 150, 150, self.x, self.y)


class DeadState:
    def enter(self, event):
        self.timer = 200

    def exit(self, event):
        pass

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.timer -= 1
        if self.timer == 0:
            game_world.remove_object(self)

    def draw(self):
        self.died.clip_draw(int(self.frame) * 150, 0, 150, 150, self.x, self.y)


# HIT, RANGE, DEAD, READY, SLEEP, WALK, DEFENCE = range(7)
next_state_table = {
    IdleState: {DEAD: DeadState},
    RunState: {DEAD: DeadState},
    AttackState: {DEAD: DeadState, READY: IdleState},
    DefenceState: {DEAD: DeadState, READY: IdleState},
    DeadState: {READY: IdleState}
}

class Mushroom:
    check = 0
    px, py = 0, 0
    def __init__(self):
        self.x, self.y = 300, 200
        self.hp = 40
        # Boy is only once created, so instance image loading is fine
        self.run_r = load_image('mushroom run.png')
        self.run_l = load_image('mushroom run.png')
        self.attack_r = load_image('mushroom attack.png')
        self.attack_l = load_image('mushroom attack.png')
        self.died = load_image('mushroom death.png')
        self.image = load_image('mushroom stop.png')
        self.hpbar = load_image('monster hp bar.png')
        # self.font = load_font('ENCR10B.TTF', 16)
        self.dir = 1
        self.high = 0
        self.velocity = 0
        self.click = 0
        self.frame = 0
        self.timer = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)


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
        if distance < (PIXEL_PER_METER * 10) ** 2:
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
        self.bt = BehaviorTree(wander_wait_node)

    def get_bb(self):
        return self.x - 20, self.y - 25, self.x + 20, self.y + 20
        # return Mushroom.x - 20, Mushroom.y - 25, Mushroom.x + 20, Mushroom.y + 20

    def stop(self):
        if self.dir == 1:
            self.x -= self.velocity * game_framework.frame_time
        elif self.dir == -1:
            self.x += self.velocity * game_framework.frame_time
        Mushroom.check += 1
        if Mushroom.check == 30:
            Mushroom.check = 0
            self.hp -= 1

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        if collide(self, server.boy):
            server.boy.set_parent(self)

        self.bt.run()

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        Mushroom.px += self.speed * math.cos(self.dir) * game_framework.frame_time
        Mushroom.py += self.speed * math.sin(self.dir) * game_framework.frame_time
        # self.cur_state.do(self)
        # if len(self.event_que) > 0:
        #     event = self.event_que.pop()
        #     # if event not in next_state_table[self.cur_state]:
        #     #     pass
        #     # else:
        #     #     self.cur_state.exit(self, event)
        #     #     self.cur_state = next_state_table[self.cur_state][event]
        #     #     self.cur_state.enter(self, event)
        if server.x >= 640:
            server.x = 640
        elif server.x <= 400:
            server.x = 400
        if server.y >= 480:
            server.y = 480
        elif server.y <= 300:
            server.y = 300
        self.x, self.y = 1280 - server.x * 2 + 0, 960 - server.y * 2 + 0
        self.x = clamp(50, self.x, 800 - 50)
        self.y = clamp(50, self.y, 600 - 50)

    def draw(self):
        self.cur_state.draw(self)
        if server.debugmode == 1:
            draw_rectangle(*self.get_bb())
        self.hpbar.clip_draw(0, 0, self.hp, 3, self.x - (40 - self.hp)/2, self.y + 30)

from pico2d import *
import server
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from collision import collide_wall

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
            # print('fff')
            server.boy.set_parent_wall(self)

    def get_bb(self):
        cx1, cy1 = self.x1 - server.background.window_left, self.y1 - server.background.window_bottom
        cx2, cy2 = self.x2 - server.background.window_left, self.y2 - server.background.window_bottom
        return cx1, cy1, cx2, cy2

    def draw(self):
        if server.debugmode == 1:
            draw_rectangle(*self.get_bb())


class Trigger:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.build_behavior_tree()

    def __getstate__(self):
        state = {'x1': self.x1, 'y1': self.y1, 'x2': self.x2, 'y2': self.y2}
        return state

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)

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

        self.bt = BehaviorTree(wander_chase_node)

    def update(self):
        self.bt.run()

    def get_bb(self):
        cx1, cy1 = self.x1 - server.background.window_left, self.y1 - server.background.window_bottom
        cx2, cy2 = self.x2 - server.background.window_left, self.y2 - server.background.window_bottom
        return cx1, cy1, cx2, cy2

    def draw(self):
        if server.debugmode == 1:
            draw_rectangle(*self.get_bb())


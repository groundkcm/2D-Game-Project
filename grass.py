from pico2d import *
import server
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from collision import collide_wall

png_names = ['inventory', 'stage1', 'stage2', 'stage3', 'start']

class Grass:
    images = None

    def load_images(self):
        if Grass.images == None:
            Grass.images = {}
            for name in png_names:
                Grass.images[name] = load_image("./sheets/background/" + name + ".png")

    def __init__(self):
        self.load_images()
        self.arrow = load_image('./sheets/UI/Arrow.png')
        self.inven_but = load_image('./sheets/UI/inventory button.png')
        self.bgm = load_music('stage bgm.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()
        self.open = load_music('door.mp3')
        self.open.set_volume(32)

    def update(self):
        pass
        # self.bt.run()

    def draw(self):
        # hide_cursor()
        WIDTH, HEIGHT = 1280 - server.x * 2 + 160, 960 - server.y * 2 + 120
        if WIDTH >= 640:
            WIDTH = 640
        elif WIDTH <= 160:
            WIDTH = 160
        if HEIGHT >= 480:
            HEIGHT = 480
        elif HEIGHT <= 120:
            HEIGHT = 120
        if server.clear == 1:
            Grass.images['stage1'].draw(WIDTH, HEIGHT)
        elif server.clear == 2:
            Grass.images['stage2'].draw(WIDTH, HEIGHT)
        elif server.clear == 3:
            Grass.images['stage3'].draw(WIDTH, HEIGHT)
        else:
            # Grass.images['start'].draw(WIDTH, HEIGHT)
            Grass.images['stage1'].draw(WIDTH, HEIGHT)
            # self.stage2.draw(WIDTH, HEIGHT)
            # self.stage3.draw(WIDTH, HEIGHT)
        self.inven_but.draw(20, 580)


    # def build_behavior_tree(self):
    #     wander_node = LeafNode("Wander", self.wander)
    #
    #     wait_node = LeafNode('Wait', self.wait)
    #     wander_wait_node = SequenceNode('WanderWait')
    #     wander_wait_node.add_children(wander_node, wait_node)
    #
    #     self.bt = BehaviorTree(wait_node)

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
            # Grass.images['start'].draw(WIDTH, HEIGHT)
            FixedBackground.images['stage1'].clip_draw_to_origin(self.window_left, self.window_bottom, server.background.canvas_width, server.background.canvas_height,0, 0)
            # self.stage2.draw(WIDTH, HEIGHT)
            # self.stage3.draw(WIDTH, HEIGHT)

        self.inven_but.draw(20, 580)

    def update(self):
        self.window_left = clamp(0,int(server.boy.x) - server.background.canvas_width // 2,server.background.w - server.background.canvas_width)
        self.window_bottom = clamp(0,int(server.boy.y) - server.background.canvas_height // 2,server.background.h - server.background.canvas_height)

    def handle_event(self, event):
        pass




class Wall:
    def __init__(self):
        self.bound0 = server.start_bound
        self.bound1 = server.stage1_bound
        self.bound2 = server.stage2_bound
        self.bound3 = server.stage3_bound
        self.tri0 = server.start_tri
        self.tri1 = server.stage1_tri
        self.tri2 = server.stage2_tri
        self.tri3 = server.stage3_tri

    def update(self):
        pass
        # if collide_wall(self, server.boy):
        #     server.boy.set_parent_wall(self)

    # def get_bb(self, j):
    #     return self.bound0[j][0], self.bound0[j][1], self.bound0[j][2], self.bound0[j][3]

    def draw(self):
        pass
        # draw_rectangle(*self.get_bb(i))


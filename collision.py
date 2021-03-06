import server

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def collide_wall(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > bottom_b: return False

    if left_a < right_b and top_a > bottom_b and bottom_a < bottom_b and left_a > left_b:
        server.left = 1
    elif right_a > left_b and right_a < right_b and top_a > bottom_b and bottom_a < bottom_b:
        server.right = 1
    elif top_a > bottom_b and top_a < top_b and right_a > left_b and left_a < right_b:
        server.top = 1
    elif bottom_a < bottom_b:
        server.bottom = 1

    return True

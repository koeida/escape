from gamemap import get_map_coords, onscreen, walkable
import world

class Animation:
    def __init__(self, name, anim_db):
        self.name = name
        self.anim_db = anim_db

class Sprite:
    def __init__(self, x, y, animations=None, current_animation="walking"):
        self.x = x
        self.y = y
        self.animations = animations
        self.current_animation = current_animation
        self.current_frame = 0
        self.anim_timer = animations[current_animation][2]
        

def attempt_walk(s, dx, dy, m, ts):
    new_x = s.x + dx
    new_y = s.y + dy
    mx, my = get_map_coords(new_x, new_y, world.TILE_WIDTH, world.TILE_HEIGHT)
    if onscreen(mx, my, m) and walkable(mx, my, m, ts):
        s.x = new_x
        s.y = new_y
    
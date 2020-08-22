from gamemap import get_map_coords, onscreen, walkable
import world

class Animation:
    def __init__(self, name, anim_db):
        self.name = name
        self.anim_db = anim_db

class Sprite:
    def __init__(self, x, y, kind, animations=None, current_animation="walking"):
        self.x = x
        self.y = y
        self.kind = kind
        self.animations = animations
        self.current_animation = current_animation
        self.current_frame = 0
        self.anim_timer = animations[current_animation][2]
        self.last_x = self.x
        self.last_y = self.y
        self.vx = 0
        self.vy = 0
    def get_rect(self):
        canim = self.animations[self.current_animation][0]
        img = world.image_db[canim]
        result = img.get_rect()
        result.x = self.x
        result.y = self.y
        return result 
        

def attempt_walk(s, m, ts):
    s.last_x = s.x
    s.last_y = s.y
    
    new_x = s.x + s.vx
    new_y = s.y + s.vy
    mx, my = get_map_coords(new_x, new_y, world.TILE_WIDTH, world.TILE_HEIGHT)
    if onscreen(mx, my, m) and walkable(mx, my, m, ts):
        s.x = new_x
        s.y = new_y
    
from gamemap import get_map_coords, onscreen, walkable
import world

class Sprite:
    pass

def attempt_walk(s, dx, dy, m, ts):
    new_x = s.x + dx
    new_y = s.y + dy
    mx, my = get_map_coords(new_x, new_y, world.TILE_WIDTH, world.TILE_HEIGHT)
    if onscreen(mx, my, m) and walkable(mx, my, m, ts):
        s.x = new_x
        s.y = new_y
    
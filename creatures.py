from gamemap import get_map_coords
import world

def attempt_walk(s, dx, dy, m):
    new_x = s.x + dx
    new_y = s.y + dy
    mx, my = get_map_coords(new_x, new_y, world.TILE_WIDTH, world.TILE_HEIGHT)
    if mx >= 0 and mx < len(m[0]) and my >= 0 and my < len(m):
        s.x = new_x
        s.y = new_y       
    
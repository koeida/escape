import pygame
import creatures
import display
import gamemap

def test_get_camera_game_coords():
    test_sprite_rect = pygame.Surface((64,64))
    target = creatures.Sprite(100, 100, "", simple_img=test_sprite_rect)
    testcam = display.Camera(target, 0,0, 100,100)
    ts = display.load_tileset("cavetiles_01.png", 32, 32)
    left_x, top_x = display.get_camera_game_coords(testcam, [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]], ts)
    assert(left_x == 82)
    assert(top_x == 82)
    
def test_get_map_coords():
    assert(gamemap.get_map_coords(16, 0, 32, 32) == (0,0))
    assert(gamemap.get_map_coords(32, 0, 32, 32) == (1,0))
    assert(gamemap.get_map_coords(32, 32, 32, 32) == (1,1))
    assert(gamemap.get_map_coords(32, 33, 32, 32) == (1,1))
    assert(gamemap.get_map_coords(-1, -1, 32, 32) == (-1,-1))
    assert(gamemap.get_map_coords(-1, 0, 32, 32) == (-1,0))
    
    
    
    
test_get_camera_game_coords()
test_get_map_coords()

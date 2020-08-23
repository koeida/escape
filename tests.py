import pygame
import creatures
import display

def test_get_camera_game_coords():
    test_sprite_rect = pygame.Surface((64,64))
    target = creatures.Sprite(100, 100, "", simple_img=test_sprite_rect)
    testcam = display.Camera(target, 0,0, 100,100)
    ts = display.load_tileset("cavetiles_01.png", 32, 32)
    left_x, top_x = display.get_camera_game_coords(testcam, [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]], ts)
    assert(left_x == 82)
    assert(top_x == 82)
    
    
test_get_camera_game_coords()

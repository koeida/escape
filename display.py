import pygame
from collections import namedtuple

Tileset = namedtuple("Tileset", "image tile_width tile_height tiles_per_line rows")

def load_tileset(f, tile_width, tile_height):
    tileset_img = pygame.image.load(f)
    img_width = tileset_img.get_rect().width   
    img_height = tileset_img.get_rect().height    
    tiles_per_line = int(img_width / tile_width)
    rows = int(img_height / tile_height)   
   
    return Tileset(tileset_img, tile_width, tile_height, tiles_per_line, rows)

def draw_tile(screen, tileset, tile_number, x, y):
    tile_y = int(tile_number / tileset.tiles_per_line)
    tile_x = tile_number % tileset.tiles_per_line    
    
    tix = tile_x * tileset.tile_width
    tiy = tile_y * tileset.tile_width
    screen.blit(tileset.image, (x,y), (tix, tiy, tileset.tile_width, tileset.tile_height))       

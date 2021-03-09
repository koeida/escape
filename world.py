import pygame
from collections import namedtuple

TILE_WIDTH = 32
TILE_HEIGHT = 32
FPS = 60
mode = "game"
dialogue_message = ""
diakey = ""
diaindex = 0
choice = ""  
partner = None
image_db = ["BODY_male.png",
            "LEGS_robe_skirt.png",
            "boganim.png",
            "puke.png",
            "BLOOD.png",
            "key.png",
            "keyanimation.png",
            "cornershadow.png",
            "topshadow.png",
            "sideshadow.png",
            "portal.png",
            "dbtl.png",
            "dbt.png",
            "dbtr.png",
            "dbl.png",
            "dbr.png",
            "dbbl.png",
            "dbb.png",
            "dbbr.png",
            "stranger.png"]
            
def tile(walkable=True, floor_tile=False, matching_tile=None):
    results = TileInfo()
    results.walkable = walkable
    results.floor_tile = floor_tile
    results.matching_tile = matching_tile
    return results

class TileInfo:
    pass
    
Tileset = namedtuple("Tileset", "image tile_width tile_height tiles_per_line rows data")

def load_tileset(tileset_img, tile_width, tile_height):
    img_width = tileset_img.get_rect().width   
    img_height = tileset_img.get_rect().height    
    tiles_per_line = int(img_width / tile_width)
    rows = int(img_height / tile_height)   
    
    data = {0: tile(True, True),
            1: tile(False, matching_tile=6),
            3: tile(False),
            5: tile(False, matching_tile=9),
            6: tile(False),
            7: tile(False, matching_tile=8),
            8: tile(False),
            9: tile(False),
            12: tile(False),
            15: tile(True, True),
            16: tile(True, True),
            18: tile(False, matching_tile=19),
            19: tile(False)}
            
    return Tileset(tileset_img, tile_width, tile_height, tiles_per_line, rows, data)
    
def load_assets():
    global image_db
    assets_dir = "lpc_entry/png/walkcycle/" 

    result = {}
    for fname in image_db:
        noending = fname[:-4]
        result[noending] = pygame.image.load(assets_dir + fname)
    image_db = result

tsimg = pygame.image.load("tile sheet.png")
#tsimg.convert()
TILES = load_tileset(tsimg, 32, 32)        

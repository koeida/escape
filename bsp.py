from pptree import Node, print_tree
#import pygame
from random import randint

class Area: 
    def __init__(self, x, y, w, h, split_mode=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = (randint(0,255), randint(0,255), randint(0,255))
        self.split_mode = split_mode
    def __str__(self): return "%d,%d %dx%d" % (self.x, self.y, self.w, self.h)
    def __len__(self):
        return len(str(self))

def split_vert(p, min_size):
    middle = int(p.h / 2)
    split_range = int(p.h * 0.10)
    height = randint(middle - split_range, middle + split_range)

    a1 = Area(p.x, p.y, p.w, height, "vert")
    a2 = Area(p.x, p.y + height, p.w, p.h - height, "vert")
    return (a1,a2)

def split_horiz(p, min_size):
    middle = int(p.w / 2)
    split_range = int(p.w * 0.10)
    width = randint(middle - split_range, middle + split_range)
    a1 = Area(p.x, p.y, width, p.h, "horiz")
    a2 = Area(p.x + width, p.y, p.w - width, p.h, "horiz")
    return (a1,a2)

def split_area(a, cur_depth, max_depth=7, min_size=26):
    p = a.name # p == parent
    if randint(0,5) == 0 and cur_depth > 3:
        return None
    
    if cur_depth > max_depth or p.w < min_size or p.h < min_size:
        return None
    else:
        if p.split_mode == None or p.split_mode == "horiz":
            a1,a2 = split_vert(p,min_size) 
        else:
            a1,a2 = split_horiz(p, min_size)

        c1 = Node(a1, a)
        c2 = Node(a2, a)

        split_area(c1, cur_depth + 1)
        split_area(c2, cur_depth + 1)

def get_leaves(h):
    results = []
    def get_leaves_internal(cur_node):
        if cur_node.children == []:
            results.append(cur_node)
        else:
            for c in cur_node.children:
                get_leaves_internal(c)
    get_leaves_internal(h)
    return results
    
def make_bsp_rooms(width, height):    
    head = Node(Area(0,0,width, height,"vert"))
    split_area(head, 0)

    rooms = get_leaves(head)
    rooms = list(map(lambda r: r.name, rooms))
    return rooms

def make_zones(width, height):
    head = Node(Area(0,0,width, height,"vert"))
    split_area(head, 0)
    return head

def branches_at_depth(head, depth):
    if depth == 1:
        results = []
        for node in head.children:
            if node != None:
                results.append(node)
        return results
    else:
        results = []
        for node in head.children:
            results += branches_at_depth(node, depth - 1)
        return results

#z = make_zones(250,250)
#print_tree(z)
#zones = branches_at_depth(z, 3)
#for z2 in zones:
#    print_tree(z2)
#print(rooms)

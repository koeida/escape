from math import sqrt

def distance(c1, c2):
    a = c1.x - c2.x
    b = c1.y - c2.y
    c = a ** 2 + b ** 2

    return sqrt(c)
    
def first(f,l):
    for x in l:
        if f(x):
            return x
    return None
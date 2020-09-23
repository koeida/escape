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
    
def get_coords(m, needle):
    results = [] # end up with something like: [(0,10), (10, 20), (25, 10)]
    for y in range(len(m)):
        for x in range(len(m[0])):
            if m[y][x] == needle:
                results.append((x,y))
    return results 
    
    
test_map = [
    [0,1,0],
    [1,0,0],
    [0,0,1]]
    
print(get_coords(test_map, 1))
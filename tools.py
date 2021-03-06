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

def two_chunk(l):
    cs = []
    for v in range(len(l)):
        if l[v] != l[-1]:
            chunk = []
            chunk.append(l[v])
            chunk.append(l[v + 1])
            cs.append(chunk)
        else:
            return cs

def get_coords(m, needles):
    results = [] # end up with something like: [(0,10), (10, 20), (25, 10)]
    for y in range(len(m)):
        for x in range(len(m[0])):
            if m[y][x] in needles:
                results.append((x,y))
    return results 

def clamp(v, minv, maxv):
    if v > maxv:
        return maxv
    elif v < minv:
        return minv
    else:
        return v

def filter_dict(f, l):
    result = []
    for k,v in l.items():
        if f(v):
            result.append(k)
    return result
    
def map_dict(f, l):
    results = []
    for k, v in l.items():
        results.append(f(k,v))
    return results

def map2d_impure(f, m):
    for y in range(len(m)):
        for x in range(len(m[y])):
            f(m,x,y)

def filter2d(f,m):
    results = []
    for y in range(len(m)):
        for x in range(len(m[y])):
            if f(m[y][x]):
                results.append((x,y))
    return results

def first2d(f,m):
    for y in range(len(m)):
        for x in range(len(m[y])):
            if f(m[y][x]):
                return x,y

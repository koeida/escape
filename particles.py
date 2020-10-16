from random import uniform

class Particle:
    def __init__(self,x,y,vx,vy, color, lifespan):
        self.x =x
        self.y =y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifespan = lifespan
        
        
        
def tick_particle(p):
    p.x += p.vx
    p.y += p.vy
    p.lifespan -=1
    
    
def crazy_splatter(particles, x, y, color):  
    for x in range(20):
        particles.append(Particle(x,y,uniform(-5,5),uniform(-5,5),color,95))
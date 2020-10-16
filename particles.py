from random import uniform

class Particle:
    def __init__(self,x,y,vx,vy, color, lifespan,size = 1):
        self.x =x
        self.y =y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifespan = lifespan
        self.size = uniform(1,5)
        
particles = []
        
        
        
def tick_particle(p):
    p.x += p.vx
    p.y += p.vy
    p.lifespan -=1
    
    
def crazy_splatter(x, y, color,lifespan=95):
    for shrex in range(150):
        particles.append(Particle(x,y,uniform(-5,5),uniform(-5,5),color,lifespan, 5))
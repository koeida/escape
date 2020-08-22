from collections import namedtuple
import world
from misc import *

Timer = namedtuple("Timer", "remaining f")

timers = []

def add_timer(seconds, f):    
    timers.append(Timer(seconds * world.FPS, f))

def update_timers():
    global timers
    timers = mapl(lambda t: t._replace(remaining=t.remaining - 1), timers)

    for t in timers:
        if t.remaining == 0:
            t.f()
    
    timers = filterl(lambda t: t.remaining > 0, timers)
    
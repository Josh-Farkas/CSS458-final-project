import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Animation(object):
    
    def __init__(bodies):
        self.data_set = bodies
        self.set_size = len(bodies)
    
    def centered_earth(save=False):
        
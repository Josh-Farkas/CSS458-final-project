import numpy as np
from body import Body
from dart import Dart
from planet import Planet

class Asteroid(Body):
    
    intercepted = False # whether or not this asteroid has been intercepted by a DART before
    
    def __init__(self, pos, vel, mass, radius, model):
        super().__init__(pos, vel, mass, radius, model)
    
    def update_collision_data(self, other):
        if other is Dart:
            self.intercepted = True
        if other == self.model.earth:
            self.model.num_asteroids_collided += 1
            self.model.bodies.remove(self)
            if self.intercepted:
                self.model.num_intercepted_collided += 1 # increment how many asteroids still hit earth after being intercepted
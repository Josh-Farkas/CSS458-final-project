import numpy as np
from body import Body
from dart import Dart
from planet import Planet

class Asteroid(Body):
    
    intercepted = False # whether or not this asteroid has been intercepted by a DART before
    will_be_intercepted = False
    
    def __init__(self, pos, vel, mass, radius, model):
        super().__init__(pos, vel, mass, radius, model)
        
        match radius:
            case model.asteroid_radius_small:
                self.will_be_intercepted = np.random.uniform() < model.small_detection
            case model.asteroid_radius_medium:
                self.will_be_intercepted = np.random.uniform() < model.medium_detection
            case model.asteroid_radius_large:
                self.will_be_intercepted = np.random.uniform() < model.large_detection

    
    def update_collision_data(self, other):
        if other is Dart:
            self.intercepted = True
        if other == self.model.earth:
            print("EARTH COLLISION")
            self.model.num_asteroids_collided += 1
            self.model.bodies.remove(self)
            if self.intercepted:
                self.model.num_intercepted_collided += 1 # increment how many asteroids still hit earth after being intercepted
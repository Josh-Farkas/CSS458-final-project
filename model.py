
from body import Body
from planet import Planet
from dart import Dart
from asteroid import Asteroid
import numpy as np
import matplotlib.pyplot as plt


class Model:
    # Tunable Parameters
    dt = 100.0
    collision_elasticity = 1.0 # [0, 1] range
    dart_mass = 1 # kg
    dart_speed = 1 # m/s
    
    # End Tunable Parameters
    
    bodies = []
    planets = []
    asteroids = []
    earth = None
    
    # Tracked Data
    num_intercepted = 0
    num_asteroids_collided = 0
    num_intercepted_collided = 0
    
    def __init__(self):
        self.init_bodies()

    
    def init_bodies(self):
        pass
    
    def init_planets(self):
        pass
    
    def add_body(self):
        pass
    
    def run(self):
        fig, ax = plt.subplots(figsize=(6,6))
        planet_scatter = ax.scatter([], [], s=10, c="Blue")
        asteroid_scatter = ax.scatter([], [], s=3, c="Red")
        
        plt.ion()
        ax.autoscale(True)
        ax.set_ybound(-10000, 10000)
        ax.set_xbound(-10000, 10000)
        for t in range(1000):
            self.step()
            asteroid_scatter.set_offsets(np.column_stack(([asteroid.position[1] for asteroid in self.asteroids], [asteroid.position[0] for asteroid in self.asteroids])))
            planet_scatter.set_offsets(np.column_stack(([planet.position[1] for planet in self.planets], [planet.position[0] for planet in self.planets])))
            plt.pause(0.01)

        plt.ioff()
        plt.show()

    
    def step(self):
        for body in self.bodies:
            body.step()
        
            
            
    
    
    def launch_dart(self, asteroid):
        
        # normal vector where dart is coming from
        dir = asteroid.position - self.earth.position / asteroid.distance_to(self.earth)
        pos = asteroid.position - dir * asteroid.radius # spawn dart colliding with asteroid
        vel = dir * self.dart_speed
        dart = Dart(pos, vel, self.dart_mass, self.dart_radius, self)
        
        # Immediately calculate collision
        asteroid.collide(dart)

       
       
model = Model()
model.run()
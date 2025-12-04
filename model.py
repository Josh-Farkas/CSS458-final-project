
from body import Body
from planet import Planet
from dart import Dart
from asteroid import Asteroid
import numpy as np
import matplotlib.pyplot as plt
import copy
import data
import animation

AU = 149_597_900_000 # Astronomical Unit in meters

class Model:
    # Tunable Parameters
    # dt = 60.0 # seconds
    # collision_elasticity = 1.0 # [0, 1] range
    # dart_mass = 610 # kg
    # dart_speed = 6600 # m/s
    # dart_distance = 11_000_000_000 # m
    
    # num_small = 10
    # num_medium = 5
    # num_large = 3
    # num_asteroids = num_small + num_medium + num_large
    
    # asteroid_distance_mean = 2.0 * AU
    # asteroid_distance_SD = .3 * AU 
    
    # asteroid_speed_mean = 21000 # m/s
    # asteroid_speed_SD = 3000
    
    # asteroid_radius_small = 100 # m
    # asteroid_mass_small = 10e8 # kg
    
    # asteroid_radius_medium = 1000 # m
    # asteroid_mass_medium = 10e11 # kg
    
    # asteroid_radius_large = 10000 # m
    # asteroid_mass_large = 10e13 # kg
    
    
    # End Tunable Parameters
    
    bodies = []
    planets = []
    asteroids = []
    
    all_timestep_bodies = [] # [bodies at time 1, bodies at time 2...]
    
    # Tracked Data
    num_intercepted = 0
    num_asteroids_collided = 0
    num_intercepted_collided = 0 # Failed interceptions
    
    def __init__(self, dt=300.0, collision_elasticity = 1.0, 
    dart_mass = 610, dart_speed = 6600, dart_distance = 11_000_000_000,
    num_small = 30, num_medium = 5, num_large = 3,
    asteroid_distance_mean = 1.0, asteroid_distance_SD = .3, 
    asteroid_speed_mean = 21000, asteroid_speed_SD = 3000,
    asteroid_radius_small = 100, asteroid_mass_small = 10e8,
    asteroid_radius_medium = 1000, asteroid_mass_medium = 10e11,
    asteroid_radius_large = 10000, asteroid_mass_large = 10e13, 
    small_detection = 0.5, medium_detection=.75, large_detection=1.0,
    duration=3600*24, seed=0):
        self.dt = dt
        self.collision_elasticity = collision_elasticity
        self.dart_mass = dart_mass
        self.dart_speed = dart_speed
        self.dart_distance = dart_distance
        
        self.num_small = num_small
        self.num_medium = num_medium
        self.num_large = num_large
        self.num_asteroids = num_small + num_medium + num_large
        
        self.asteroid_distance_mean = asteroid_distance_mean * AU
        self.asteroid_distance_SD = asteroid_distance_SD * AU 
        
        self.asteroid_speed_mean = asteroid_speed_mean
        self.asteroid_speed_SD = asteroid_speed_SD
        
        self.asteroid_radius_small = asteroid_radius_small
        self.asteroid_mass_small = asteroid_mass_small
        
        self.asteroid_radius_medium = asteroid_radius_medium
        self.asteroid_mass_medium = asteroid_mass_medium
        
        self.asteroid_radius_large = asteroid_radius_large
        self.asteroid_mass_large = asteroid_mass_large
        
        self.small_detection = small_detection
        self.medium_detection = medium_detection
        self.large_detection = large_detection
        
        self.duration = duration
        if seed != 0: 
            np.random.seed(seed)
        
        self.init_bodies()

    def init_bodies(self):
        """Initialize all Body objects and add to bodies list
        """
        self.init_planets()
        self.init_asteroids()
        self.bodies = self.planets + self.asteroids
    
    
    def init_planets(self):
        """Initialize planets list from data.py
        """
        # Sun treated as planet for simplicity
        self.planets = [data.SUN, data.MERCURY, data.VENUS, data.EARTH, data.MARS, data.JUPITER, data.SATURN, data.URANUS, data.NEPTUNE]
        self.planets = [p.deepcopy() for p in self.planets]
        self.sun = self.planets[0]
        self.earth = self.planets[2]
        for planet in self.planets:
            planet.model = self
            
    
    def init_asteroids(self):
        """Initialize all asteroids with parameters based on Model parameters
        """
        distances = np.random.normal(self.asteroid_distance_mean, self.asteroid_distance_SD, self.num_asteroids)
        angles = np.random.uniform(0, 2*np.pi, self.num_asteroids)
        positions = np.column_stack((distances * np.cos(angles), distances * np.sin(angles), distances * 0)) + self.earth.position
        
        speeds = np.random.normal(self.asteroid_speed_mean, self.asteroid_speed_SD, self.num_asteroids)
        directions = self.earth.position - positions
        directions /= np.linalg.norm(directions, axis=1, keepdims=True) # normalize directions
        velocities = directions * speeds[:, None]
        
        masses = [self.asteroid_mass_small] * self.num_small \
               + [self.asteroid_mass_medium] * self.num_medium \
               + [self.asteroid_mass_large] * self.num_large
               
        radii = [self.asteroid_radius_small] * self.num_small \
               + [self.asteroid_radius_medium] * self.num_medium \
               + [self.asteroid_radius_large] * self.num_large
        
        for pos, vel, mass, radius in zip(positions, velocities, masses, radii):
            a = Asteroid(pos, vel, mass, radius, model=self)
            self.asteroids.append(a)
    
    
    def run(self, animate=False):
        # fig, ax = plt.subplots(figsize=(6,6))
        # planet_scatter = ax.scatter([], [], s=10, c="Blue")
        # asteroid_scatter = ax.scatter([], [], s=3, c="Red")
        
        # plt.ion()
        # plt.autoscale(False)
        # ax.set_ybound(-5*AU, 5*AU)
        # ax.set_xbound(-5*AU, 5*AU)
        # arrow = ax.arrow(*self.earth.position, *(self.earth.velocity * 1000))
        for t in range(int(self.duration / self.dt)):
            self.step()
            # print("EARTH DISTANCE: ", self.earth.distance_to(data.SUN) / AU)
            
            # asteroid_scatter.set_offsets(np.column_stack(([asteroid.position[1] for asteroid in self.asteroids], [asteroid.position[0] for asteroid in self.asteroids])))
            # planet_scatter.set_offsets(np.column_stack(([planet.position[1] for planet in self.planets], [planet.position[0] for planet in self.planets])))
            # arrow.remove()
            # arrow = ax.arrow(*self.earth.position[::-1], *(self.earth.velocity[::-1] * 1000),
                           #  width=1e10,      # shaft thickness
                           #  head_width=1e10, # head width
                           #  head_length=1e10, # head length
                           #  color='red')
            # plt.pause(0.01)
            
        # plt.ioff()
        # plt.show()
        
        if animate:
            anim = animation.Animation(self.all_timestep_bodies)
            anim.animate(multiplier=3, save=False)

        return self.all_timestep_bodies

    
    def step(self):
        """Runs one timestep of the simulation.
        """
        for body in self.bodies:
            body.step()
            self.handle_dart(body)

        self.handle_collisions()
        
        self.all_timestep_bodies.append(copy.deepcopy(self.bodies))


    def handle_collisions(self):
        """Check and resolve all collisions between bodies.
        """
        for i, body1 in enumerate(self.bodies):
            for body2 in self.bodies[i+1:]:
                if body1.is_collided(body2):
                    body1.collide(body2)

    def handle_dart(self, body):
        """Checks if a body is an asteroid that meets the criteria to launch a dart.
        - Hasn't been hit yet
        - Marked to be hit (decided when asteroid is initialized)

        Args:
            body (Body): The body to check
        """
        if body is not Asteroid: return
        if body.will_be_intercepted and not body.intercepted and body.distance_to(self.earth) < self.dart_distance:
            self.launch_dart(body)
    
    def launch_dart(self, asteroid):
        """Launches a DART at a given Asteroid

        Args:
            asteroid (Asteroid): Asteroid body the DART will collide with.
        """
        # normal vector where dart is coming from
        dir = asteroid.position - self.earth.position / asteroid.distance_to(self.earth)
        pos = asteroid.position - dir * asteroid.radius # spawn dart colliding with asteroid
        vel = dir * self.dart_speed
        dart = Dart(pos, vel, self.dart_mass, self.dart_radius, self)
        
        # Immediately calculate collision
        asteroid.collide(dart)

       
if __name__ == "__main__":       
    model = Model(seed=1)
    model.run(animate=True)

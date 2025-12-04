
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
    
    
    all_timestep_bodies = [] # [bodies at time 1, bodies at time 2...]
    
    # Tracked Data
    num_intercepted = 0
    num_asteroids_collided = 0
    num_intercepted_collided = 0 # Failed interceptions
    
    def __init__(self, dt=60*60*24, collision_elasticity = 1.0, 
    dart_mass = 580, dart_speed = 6600, dart_distance = 11_000_000_000,
    num_small = 10, num_medium = 5, num_large = 3,
    asteroid_distance_mean = 1.0*AU, asteroid_distance_SD = .3*AU, 
    asteroid_speed_mean = 21000, asteroid_speed_SD = 3000,
    asteroid_radius_small = 100, asteroid_mass_small = 10e8,
    asteroid_radius_medium = 1000, asteroid_mass_medium = 10e11,
    asteroid_radius_large = 10000, asteroid_mass_large = 10e13, 
    small_detection = 0.5, medium_detection=.75, large_detection=1.0,
    duration=3600*24*365, seed=0):
        self.bodies = []
        self.planets = []
        self.asteroids = []
        self.dt = dt
        self.collision_elasticity = collision_elasticity
        self.dart_mass = dart_mass
        self.dart_speed = dart_speed
        self.dart_distance = dart_distance
        
        self.num_small = num_small
        self.num_medium = num_medium
        self.num_large = num_large
        self.num_asteroids = num_small + num_medium + num_large
        
        self.asteroid_distance_mean = asteroid_distance_mean
        self.asteroid_distance_SD = asteroid_distance_SD
        
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
        self.planets = [copy.deepcopy(p) for p in self.planets]
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
    
    
    def run(self, animate=False, zoom=3):
        for t in range(int(self.duration / self.dt)):
            self.step()

        # self.verification_check()
        
        if animate:
            anim = animation.Animation(self.all_timestep_bodies)
            anim.animate(multiplier=zoom, save=False)

        return self.all_timestep_bodies

    
    def step(self):
        """Runs one timestep of the simulation.
        """
        op_bodies = copy.deepcopy(self.bodies)
        for body in op_bodies:
            body.step()
            self.handle_dart(body)

        self.handle_collisions()
        
        self.all_timestep_bodies.append(op_bodies)
        self.bodies = copy.deepcopy(op_bodies)


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
        if (type(body) != Asteroid):
            return
        if body.will_be_intercepted and not body.intercepted and body.distance_to(self.earth) < self.dart_distance:
            self.launch_dart(body)

    def launch_dart(self, asteroid):
        """Launches a DART at a given Asteroid

        Args:
            asteroid (Asteroid): Asteroid body the DART will collide with.
        """
        # normal vector where dart is coming from
        dart_radius = 10
        dir = (asteroid.position - self.earth.position) / asteroid.distance_to(self.earth)
        pos = asteroid.position - dir * (asteroid.radius + dart_radius) # spawn dart colliding with asteroid
        vel = dir * self.dart_speed
        dart = Dart(pos, vel, self.dart_mass, dart_radius, self)
        
        # Immediately calculate collision
        asteroid.collide(dart)

    def verification_check(self):
        real_x = -3.526393951820965E+07
        real_y = 3.443028330454750E+07
        real_z = 6.091104795446873E+06
        calc_x = self.all_timestep_bodies[-1][1].position[0] / 1000
        calc_y = self.all_timestep_bodies[-1][1].position[1] / 1000
        calc_z = self.all_timestep_bodies[-1][1].position[2] / 1000
        print("Mercury's position after 24 hours in kilometers:")
        print(f"[{calc_x:e}, {calc_y:e}, {calc_z:e}]")
        print("Mercury's expected position after 24 hours in kilometers:")
        print(f"[{real_x:e}, {real_y:e}, {real_z:e}]")
        dist = np.sqrt((calc_x - real_x)**2 + (calc_y - real_y)**2 + (calc_z - real_z)**2)
        print(f"Distance difference between calculated and real: {dist:e}")


       
if __name__ == "__main__":       
    model = Model(seed=1, dt=60*60*24, duration=3600*24*365, 
                  dart_distance=1e20, dart_mass=580, dart_speed=6600, 
                  small_detection=1, medium_detection=1, large_detection=1,
                  num_small=0, num_medium=0, num_large=20,
                  asteroid_mass_large=5.4e11, asteroid_radius_large=390)
    model.run(animate=True, zoom=5)

import numpy as np

G = 6.674*(10**(-11)) # Gravitational Constant

class Body:
    """Body class, stores position, velocity, mass, and radius
    """
    position = np.array([0, 0, 0])
    velocity = np.array([0, 0, 0])
    mass: int = 0 # kg
    radius: int = 0 # meters
    kinetic_energy = 0
    
    model = None
    
    def __init__(self, pos=0, vel=0, mass=0, radius=0, model=0, label=""):
        self.position = np.copy(pos)
        self.velocity = np.copy(vel)
        self.mass = mass
        self.radius = radius
        self.model = model
        self.label = label
        
    
    def step(self):
        """Runs one step of the simulation. Applies Runge-Kutta timestep and then applies collisions.
        """
        update_pos_vel = self.runge_kutta(dt=self.model.dt)
        
        for other in self.model.bodies:
            if other is self: continue
            if self.is_collided(other):
                self.collide(other, elasticity=self.model.collision_elasticity)
        
        
        ke = self.mass * np.linalg.norm(self.velocity**2)
        energy_loss = self.kinetic_energy - ke
        self.kinetic_energy = ke
        # print(energy_loss)

        return update_pos_vel
    
    
    def acceleration(self, position):
        """Calculates the acceleration at a given position.

        Args:
            position (np.ndarray): Position vector to calculate acceleration at

        Returns:
            np.ndarray: acceleration vector at the given position
        """        
        acc = np.zeros(3)
        for other in self.model.bodies:
            if other is self: continue
            
            r = other.position - position
            dist = np.linalg.norm(r)
            
            if dist == 0: continue
            
            
            acc += G * other.mass * r / dist**3 # derived formula from gravitational formula, F=ma, and unit vector
        return acc
    
    
    def state_deriv(self, state):
        """dy/dt AKA f function for RK4. Is given the state of the object and returns the derivative. 
        Since the state is (position, velocity), the derivative then becomes (velocity, acceleration).
        We already have velocity so we don't need to calculate the derivative of position.

        Args:
            state (np.ndarray): state vector of position and velocity. [x, y, velx, vely].
        
        Returns:
            np.ndarray: derivative of the state vector. [velx, vely, accx, accy].
        """ 
        pos = state[:3]
        vel = state[3:]
        return np.hstack((vel, self.acceleration(pos)))

    
    def runge_kutta(self, dt):
        """Runge-Kutta timestepping method. Updates position and velocity.

        Args:
            dt (float, optional): Timestep length in seconds.
        """
        state = np.hstack((self.position, self.velocity))
        k1 = dt * self.state_deriv(state)
        k2 = dt * self.state_deriv(state + k1/2)
        k3 = dt * self.state_deriv(state + k2/2)
        k4 = self.state_deriv(state + dt*k3)
        
        # Calculate weighted average.
        new_state = state + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
        pos = new_state[:3]
        vel = new_state[3:]
        print(pos)

        return pos, vel
    
    
    def distance_to(self, other):
        """Returns the Euclidian distance between two objects.

        Args:
            other (Body): Body to check distance to.
        """
        return np.linalg.norm(self.position - other.position)
        # return np.sqrt((self.position[0] - other.position[0])**2 + (self.position[1] - other.position[1])**2)
    
    
    def is_collided(self, other):
        """Checks if two bodies have collided.

        Args:
            other (Body): Second Body

        Returns:
            boolean: True if there was a collision, false if otherwise.
        """
        return self.distance_to(other) < (self.radius + other.radius)


    def collide(self, other, elasticity=1.0):
        """Apply collision to two bodies and update their velocities

        Args:
            other (Body): Second body
            elasticity (float, optional): The elasticty of the collision in the range [0, 1], 
                                          1.0 is perfectly elastic. Defaults to 1.0.
        """
        dist = self.distance_to(other)
        if dist == 0 or dist > self.radius + other.radius: return
        contact_normal = (other.position - self.position) / dist # normal vector pointing from body1 to body2
        v_rel = np.dot((other.velocity - self.velocity), contact_normal) # Relative velocity along normal
        if v_rel >= 0: return # Do not collide if bodies are moving away from each other
        impulse = -1.0 * ((1 + elasticity) * v_rel) / (1 / self.mass + 1 / other.mass) * contact_normal
        
        # Update Body velocities
        self.velocity -= impulse / self.mass
        other.velocity += impulse / other.mass
        
        # Positional correction (prevents repeated collisions)
        overlap = self.radius + other.radius - dist
        if overlap > 0:
            correction = 0.5 * overlap * contact_normal
            self.position -= correction
            other.position += correction
        
        self.update_collision_data(other)
        other.update_collision_data(self)
        
        
        
    # Virtual function
    def update_collision_data(self, other):
        pass


    def set_pos(self, pos_arr):
        self.position = np.array(pos_arr)

    def set_vel(self, vel_arr):
        self.velocity = np.array(vel_arr)
class SimObject:
    """Object class, stores position and mass
    """
    x: float = 0.0 # meters
    y: float = 0.0 # meters
    mass: float = 1.0 # kg
    vel_x: float = 0.0 # m/s
    vel_y: float = 0.0 # m/s
    
    timestep = 1000 # timestep length in seconds
    
    def __init__(self, x, y, mass, vel_x=0.0, vel_y=0.0):
        self.x = x
        self.y = y
        self.mass = mass
        self.vel_x = vel_x
        self.vel_y = vel_y
        
        
def calculate_gravitational_force(obj1, obj2, G=6.674*10e-11):
    """Calculates the force between two objects

    Args:
        obj1 (Object): First Object
        obj2 (Object): Second Object
        G (float, optional): Gravitational Constant. Defaults to 6.674*10e-11.

    Returns:
        float: The force between the objects
    """
    r_sq = (obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2
    return G * obj1.mass * obj2.mass / r_sq
    
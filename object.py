class SimObject:
    """Object class, stores position and mass
    """
    x: float = 0.0 # meters
    y: float = 0.0 # meters
    mass: float = 1.0 # kg
    velocity: tuple[float, float] = (0.0, 0.0) # ms/s
    
    def __init__(self, x, y, mass, velocity):
        self.x = x
        self.y = y
        self.mass = mass
        self.velocity = velocity
    
        
def calculate_force(obj1, obj2, G=6.674*10e-11):
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
    
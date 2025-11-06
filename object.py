class Object:
    """Object class, stores position and mass
    """
    x: float = 0.0
    y: float = 0.0
    mass: float = 1.0
    
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
        
def calculate_force(o1, o2, G=6.674*10e-11):
    """Calculates the force between two objects

    Args:
        o1 (Object): First Object
        o2 (Object): Second Object
        G (float, optional): Gravitational Constant. Defaults to 6.674*10e-11.

    Returns:
        _type_: _description_
    """
    r_sq = (o1.x - o2.x)**2 + (o1.y - o2.y)**2
    return G * o1.mass * o2.mass / r_sq
    
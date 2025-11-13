import numpy as np

class Body:
    """Body class, stores position, mass, and radius
    """
    x: float = 0.0 # meters
    y: float = 0.0 # meters
    mass: float = 1.0 # kg
    radius: float = 0.0 # meters
    
    def __init__(self, x, y, mass, radius):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        
        
def calculate_force(body1, body2, G=6.674*10e-11):
    """Calculates the force between two bodies

    Args:
        body1 (Body): First Body
        body2 (Body): Second Body
        G (float, optional): Gravitational Constant. Defaults to 6.674*10e-11.

    Returns:
        float: The force between the bodies
    """
    r_sq = (body1.x - body2.x)**2 + (body1.y - body2.y)**2
    return G * body1.mass * body2.mass / r_sq

def collision(body1, body2):
    """Checks if two bodies have collided.

    Args:
        body1 (Body): First Body
        body2 (Body): Second Body

    Returns:
        boolean: True if there was a collision, false if otherwise.
    """
    x_1 = body1.x # meters
    y_1 = body1.y # meters
    r_1 = body1.radius # meters

    x_2 = body2.x # meters
    y_2 = body2.y # meters
    r_2 = body2.radius # meters

    return np.sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2) <= (r_1 + r_2)
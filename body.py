import numpy as np

class Body:
    """Body class, stores position, velocity, mass, and radius
    """
    pos = np.array([0, 0])
    vel = np.array([0, 0])
    mass: int = 0 # kg
    radius: int = 0 # meters
    
    def __init__(self, pos, vel, mass, radius):
        self.pos = np.copy(pos)
        self.vel = np.copy(vel)
        self.mass = mass
        self.radius = radius


def distance(body1, body2):
    """Returns the Euclidian distance between two objects

    Args:
        body1 (Body): First body
        body2 (Body): Second body
    """
    return np.sqrt((body1.pos[0] - body2.pos[0])**2 + (body1.pos[1] - body2.pos[1])**2)
        
        
def calculate_gravitational_force(body1, body2, G=6.674*10e-11):
    """Calculates the gravitational force between two bodies

    Args:
        body1 (Body): First Body
        body2 (Body): Second Body
        G (float, optional): Gravitational Constant. Defaults to 6.674*10e-11.

    Returns:
        float: The force between the bodies
    """
    r_sq = (body1.pos[0] - body2.pos[0])**2 + (body1.pos[1] - body2.pos[1])**2
    return G * body1.mass * body2.mass / r_sq


def is_collided(body1, body2):
    """Checks if two bodies have collided.

    Args:
        body1 (Body): First Body
        body2 (Body): Second Body

    Returns:
        boolean: True if there was a collision, false if otherwise.
    """
    return distance(body1, body2) <= (body1.radius + body2.radius)


def collide(body1, body2, elasticity=1.0):
    """Apply collision to two bodies and update their velocities

    Args:
        body1 (Body): First body
        body2 (Body): Second body
        elasticity (float, optional): The elasticty of the collision in the range [0, 1], 
                                      1.0 is perfectly elastic. Defaults to 1.0.
    """
    dist = distance(body1, body2)
    contact_normal = (body2.pos - body1.pos) / dist if dist > 0 else np.array([1, 0]) # normal vector pointing from body1 to body2
    v_rel = (body2.vel - body1.vel) * contact_normal # Relative velocity along normal
    if v_rel >= 0: return # Do not collide if bodies are moving away from each other
    impulse = -1 * ((1 + elasticity) * v_rel) / (1 / body1.mass + 1 / body2.mass)
    
    # Update Body velocities
    body1.vel += impulse / body1.mass * contact_normal
    body2.vel += impulse / body2.mass * contact_normal
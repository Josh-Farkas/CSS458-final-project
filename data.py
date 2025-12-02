
"""
Planetary Parameters 
Data Source: NASA JPL Solar System Dynamics
https://ssd.jpl.nasa.gov/planets/phys_par.html


Position in meters from Sun, approx positions as of 12/27/2025
Velocities in m/s 
Mass in kg
Radius in meters
"""

import numpy as np
from body import Body

# Tuple Format: position[], velocities[], mass, radius)
# Position and velocities are represented as 2d numpy array where [x,y]
# Sun is the origin

SUN = Body(
    np.array([0.0, 0.0]),           # position (m)
    np.array([0.0, 0.0]),           # velocity (m/s)
    1.98847e30,                      # mass (kg)
    696000000                        # radius (m)
)

MERCURY = Body(
    np.array([4.65e10, 3.51e10]),
    np.array([-4.10e4, 4.55e4]),
    3.30103e23,
    2439400
)

VENUS = Body(
    np.array([-1.08e11, 7.20e9]),
    np.array([-3.50e3, -3.50e4]),
    4.86731e24,
    6051800
)

EARTH = Body(
    np.array([1.43e11, -4.50e10]),
    np.array([9.00e3, 2.85e4]),
    5.97217e24,
    6371008
)

MARS = Body(
    np.array([-1.89e11, -1.33e11]),
    np.array([1.54e4, -1.90e4]),
    6.41691e23,
    3389500
)

JUPITER = Body(
    np.array([6.30e11, 4.80e11]),
    np.array([-8.10e3, 1.05e4]),
    1.898125e27,
    69911000
)

SATURN = Body(
    np.array([1.20e12, -7.15e11]),
    np.array([4.50e3, 7.70e3]),
    5.68317e26,
    58232000
)

URANUS = Body(
    np.array([2.45e12, 1.68e12]),
    np.array([-4.00e3, 5.30e3]),
    8.68099e25,
    25362000
)

NEPTUNE = Body(
    np.array([4.27e12, -1.57e12]),
    np.array([1.95e3, 5.10e3]),
    1.024092e26,
    24622000
)

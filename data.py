
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
    np.array([-4.912509968506466E+05,
              -8.279409221788045E+05])*1000, # position (m)
    np.array([1.256877255382410E-02,
              -1.875201878732409E-04])*1000, # velocity (m/s)
    1988410 * (10**24),                      # mass (kg)
    695700000,                               # radius (m)
    label='sun'
)

MERCURY = Body(
    np.array([-3.127905203130432E+07,
              3.707015264084680E+07])*1000,
    np.array([-4.764788163702398E+01, 
              -2.879379513298748E+01])*1000,
    3.302 * (10**23),
    2439400,
    label='mercury'
)

VENUS = Body(
    np.array([-7.100525604293682E+07, 
              -8.298028263639985E+07])*1000,
    np.array([2.634000410811250E+01, 
              -2.297367049642995E+01])*1000,
    48.685 * (10**23),
    6051840,
    label='venus'
)

EARTH = Body(
    np.array([5.069379549453425E+07, 
              1.375054744509470E+08])*1000,
    np.array([-2.840196971889024E+01, 
              1.021414113586683E+01])*1000,
    5.97219 * (10**24),
    6371010,
    label='earth'
)

MARS = Body(
    np.array([-1.423802149405333E+07, 
              -2.192041434103926E+08])*1000,
    np.array([2.511067074504107E+01, 
              5.611375252231812E-01])*1000,
    6.4171 * (10**23),
    3389920,
    label='mars'
)

JUPITER = Body(
    np.array([-2.212310300393372E+08, 
              7.452555485526739E+08])*1000,
    np.array([-1.268030476659128E+01, 
              -3.098540562049134E+00])*1000,
    18.9819 * (10**26),
    69911000,
    label='jupiter'
)

SATURN = Body(
    np.array([1.423645667959634E+09, 
              1.274995759213873E+07])*1000,
    np.array([-6.194387066563424E-01, 
              9.637222604990116E+00])*1000,
    5.6834 * (10**26),
    58232000,
    label='saturn'
)

URANUS = Body(
    np.array([1.492933220128212E+09, 
              2.504247387219565E+09])*1000,
    np.array([-5.899749274100404E+00, 
              3.169770118761888E+00])*1000,
    86.813 * (10**24),
    25362000,
    label='uranus'
)

NEPTUNE = Body(
    np.array([1.492933220128212E+09, 
              2.504247387219565E+09])*1000,
    np.array([-5.899749274100404E+00, 
              3.169770118761888E+00])*1000,
    86.813 * (10**24),
    25362000,
    label='neptune'
)

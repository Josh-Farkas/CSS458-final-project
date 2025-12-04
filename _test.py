'''
Description:
Testing suite for CSS 458 group project: D.A.R.T. asteroid collision analysis.
Contains a comprehensive assortment of value checks for each system module.
Tests reference coordination with real world data, expected outcome
sanity checks, and more. Tests are organized in their own sections,
based on modules.

Usage:
Run command 'pytest' in console while under '_test.py's directory.

Required Installations:
Required to install 'pytest' for your interpreter.
If using pip, you can install by running this command, 'pip install pytest'.
'''

# Imports
import analysis
import animation
import body
import model
import data
import pytest
import numpy as np

# Analysis Module Tests
##############################

def test_temp():
    pass

# Animation Module Tests
##############################

class MockBody(object):
    def __init__(self, x, y, label):
        self.position = (x, y)
        self.label = label

def test_attribute_storage_animation():
    bodies = [[MockBody(0, 0, 'body'), MockBody(0, 0, 'body')],
              [MockBody(0, 0, 'body'), MockBody(0, 0, 'body')]]
    ani = animation.Animation(bodies)
    assert ani.set_size == 2
    assert ani.data_set.shape == (2, 2)
    assert ani.data_set[0][0].label == 'body'

def test_centered_positions():
    bodies = [[MockBody(10, 10, 'sun'), MockBody(12, 13, 'earth')]]
    ani = animation.Animation(bodies)
    ani.center_name = 'sun'

    xs, ys = ani._Animation__get_centered_positions(0)

    assert xs == [0, 2]
    assert ys == [0, 3]

def test_center_value_validity():
    bodies = [[MockBody(0, 0, 'earth')]]
    ani = animation.Animation(bodies)
    ani.center_name = 'sun'

    with pytest.raises(ValueError):
        ani._Animation__get_centered_positions(0)

def test_center_arg(capsys):
    anim = animation.Animation([[]])
    anim.animate(center="INVALID")

    captured = capsys.readouterr()
    assert "Invalid center declaration" in captured.out

# Body Module Tests
##############################

# Set up testing model environment


def test_acceleration():
    test_model = model.Model()
    test_model.dt = 1
    b1 = body.Body(np.array([0, 0, 0]),   np.array([0, 0, 0]), 1, 1, test_model)
    b2 = body.Body(np.array([100, 0, 0]), np.array([0, 0, 0]), 10, 1, test_model)
    test_model.bodies = [b1, b2]
    test_model.planets = [b1, b2]
    test_model.asteroids.clear()
    b = test_model.bodies[0]
    print(b.acceleration(b.position))
    assert np.isclose(b.acceleration(b.position)[0], 6.674e-13, rtol=.01)
    
    
def test_runge_kutta():
    test_model = model.Model()
    test_model.dt = 1
    test_model.bodies = [data.EARTH, data.SUN]
    test_model.planets = [data.EARTH, data.SUN]
    test_model.asteroids.clear()
    b = test_model.bodies[0]
    for t in range(100):
        b.runge_kutta(dt=60)
        print(t, b.position, b.velocity)

# Model Module Tests
##############################

def test_temp():
    pass
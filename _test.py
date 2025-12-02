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

def test_temp():
    pass

# Model Module Tests
##############################

def test_temp():
    pass
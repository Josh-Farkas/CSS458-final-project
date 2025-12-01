from body import Body
import numpy as np


class Dart(Body):

    def __init__(self, pos, vel, mass, radius, model):
        super().__init__(pos, vel, mass, radius, model)

    def update_collision_data(self, other):
        self.model.num_intercepted += 1
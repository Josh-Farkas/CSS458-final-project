import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class Animation(object):
    
    def __init__(self, bodies):
        self.data_set = np.array(bodies, dtype=object)
        self.set_size = len(bodies)
    
    def centered_sun(self, save=False):
        initial_positions = np.array([body.position for body in self.data_set[0]])

        min_x = initial_positions[:, 0].min()
        max_x = initial_positions[:, 0].max()
        min_y = initial_positions[:, 1].min()
        max_y = initial_positions[:, 1].max()

        fig, ax = plt.subplots()

        ax.set_xlim(min_x * 1.2, max_x * 1.2)
        ax.set_ylim(min_y * 1.2, max_y * 1.2)

        
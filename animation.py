import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math

class Animation(object):
    
    def __init__(self, bodies):
        self.data_set = np.array(bodies, dtype=object)
        self.set_size = len(bodies)
    
    def update(self, frame):
        bodies = self.data_set[frame]

        xs = [b.position[0] for b in bodies]
        ys = [b.position[1] for b in bodies]

        self.scat.set_offsets(np.column_stack((xs, ys)))

        return self.scat,

    def centered_sun(self, save=False):
        all_positions = np.array([
            body.position
            for bodies in self.data_set
            for body in bodies
        ])

        xs = all_positions[:, 0]
        ys = all_positions[:, 1]

        max_abs_x = max(abs(xs.min()), abs(xs.max()))
        max_abs_y = max(abs(ys.min()), abs(ys.max()))

        half_range = max(max_abs_x, max_abs_y)

        pad = half_range * 0.2 if half_range != 0 else 1.0

        lim = half_range + pad
        xlim = (-lim, lim)
        ylim = (-lim, lim)

        fig, ax = plt.subplots()

        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)

        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

        ax.set_aspect('equal', adjustable='box')

        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)

        self.scat = ax.scatter([], [])

        ani = animation.FuncAnimation(
            fig,
            self.update,
            frames=self.set_size,
            interval=300,
            repeat=True
        )

        plt.show()
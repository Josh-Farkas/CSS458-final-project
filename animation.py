'''
Description:
Module designed to animate a list of timesteps. Each timestep contains
a list of objects from our body class. Every frame (outer list element)
updates the position of the body on the graph, simulating a top down view
of our solar system. Animate function allows adjusting the center of
the animation to a chosen body (sun, earth, or asteroid).

Authors:
Kyle Williams
Nora Osmanova
Josh Farkas

Date:
11/30/2025

Purpose:
D.A.R.T. test simulation visualization for group assignment, CSS 458.

Future Development:
* Adjustable window size as a animate function keyword argument.
* Custom plot point colors depending on body.
* Optional arrow indicators for directional vectors.
* Supporting multiple asteroids for asteroid centered graphs.
'''

# Imports
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Global Variables
VALID_CENTERS = ["sun", "earth", "asteroid"]

class Animation(object):
    '''
    Description:
    Takes a list of timesteps containing states of body objects. Contains
    a single animate function and multiple supporting functions to visually
    represent the position of each object at each timestep.

    Attributes:
    * data_set: Structured as a list of lists. Outer elements represent 
    timesteps of a list of body objects.
    Inner list contains n amount of objects.
    Example:
    [
    [earth, mars, ...],
    [earth, mars, ...],
    [earth, mars, ...],
    [earth, mars, ...],
    [earth, mars, ...],
    ...
    ]
    * set_size: Number of elements in data_set's outer list.
    '''
    
    def __init__(self, bodies):
        '''
        Description:
        Initiates class with bodies arg and size of bodies as attributes.

        Arguments:
        * bodies: Structured as a list of lists. Outer elements represent 
        timesteps of a list of body objects.
        Inner list contains n amount of objects.
        Example:
        [
        [earth, mars, ...],
        [earth, mars, ...],
        [earth, mars, ...],
        [earth, mars, ...],
        [earth, mars, ...],
        ...
        ]
        '''
        self.data_set = np.array(bodies, dtype=object)
        self.set_size = len(bodies)
    
    def __update(self, frame):
        xs, ys = self.__get_centered_positions(frame)
        bodies = self.data_set[frame]

        self.scat.set_offsets(np.column_stack((xs, ys)))

        for label, x, y, body in zip(self.labels, xs, ys, bodies):
            label.set_position((x, y))
            label.set_text(body.label)

        return (self.scat, *self.labels)

    def __get_centered_positions(self, frame):
        '''
        Description:
        
        '''
        bodies = self.data_set[frame]

        center_body = None
        for body in bodies:
            if body.label.lower() == self.center_name.lower():
                center_body = body
                break

        if center_body is None:
            raise ValueError(
                f"Body '{self.center_name}' not found in frame {frame}.")

        cx, cy = center_body.position

        xs = [b.position[0] - cx for b in bodies]
        ys = [b.position[1] - cy for b in bodies]

        return xs, ys

    def __create_plot(self):
        all_centered = []
        for frame in range(self.set_size):
            xs, ys = self.__get_centered_positions(frame)
            all_centered.append((xs, ys))

        xs = np.array([x for frame in all_centered for x in frame[0]])
        ys = np.array([y for frame in all_centered for y in frame[1]])

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
        self.ax = ax

        self.labels = [
            ax.text(0, 0, "", fontsize=9, ha='left', va='bottom')
            for _ in range(len(self.data_set[0]))
        ]

        ani = animation.FuncAnimation(
            fig,
            self.__update,
            frames=self.set_size,
            interval=300,
            repeat=True,
            blit=True
        )

        return ani

    def animate(self, center="sun", save=False, filename='animation.gif'):
        '''
        Description:
        Driver function for animation creation. Performs error checking on
        keyword arguments.

        Arguments:
        * center: Determines which body is at the central point of the graph.
        * save: Boolean to determine whether or not animation is saved.
        Animation is saved in the same working directory.
        * filename: Name of the file the animation will be saved as.
        Note: Formats other than .gif are not tested and not intended.

        Output:
        * Creates an animation using the class attribute data_set. data_set
        elements act as timesteps and each element contains body objects
        with locations.
        * If save is True, saves the animation to a file in the working
        directory. Otherwise, locally displays the animation.
        '''
        # Checking for input validity of center keyword.
        if center not in VALID_CENTERS:
            print("Invalid center declaration in animate function call.")
            print("Valid declarations: \"sun\", \"earth\", \"asteroid\".")
            return

        # Sets class attribute to be used by __get_center_positions().
        self.center_name = center

        # Call to receive animation.
        ani = self.__create_plot()

        # Saves animation as a gif in current operating directory.
        if save:
            print(f"Saving animation to {filename}...")
            ani.save(
                filename,
                fps=15,
                dpi=150,
                writer="pillow"
            )
            print("Saved!")

        # Locally displays the animation without saving it to a file.
        else:
            plt.show()

# END OF FILE -----------------------------------------------------------------
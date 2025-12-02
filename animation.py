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
        '''
        Description:
        Function called by FuncAnimation to constantly update each
        frame of our output animation.

        Arguments:
        * frame: Current time step of data_set.

        Return:
        Returns tuple of artists as required by blit.
        '''
        # Body positions after being corrected for centering.
        xs, ys = self.__get_centered_positions(frame)
        # List of bodies at current time step.
        bodies = self.data_set[frame]

        # Offsets the scatter plot by corrected values.
        self.scat.set_offsets(np.column_stack((xs, ys)))

        # Creates label positions in correlation with body positions.
        for label, x, y, body in zip(self.labels, xs, ys, bodies):
            label.set_position((x, y))
            label.set_text(body.label)

        return (self.scat, *self.labels)

    def __get_centered_positions(self, frame):
        '''
        Description:
        Finds the position of the center body attribute at a given
        time step in the data_set attribute. Corrects the position
        of all bodies at that timestep by finding the difference
        between them and the center bodies position.

        Arguments:
        * frame: Current timestep for attribute data_set.

        Return:
        Returns the corrected x and y positions of all bodies in current frame
        of data_set. Positions are corrected to have center attribute at 0,0,
        while maintaining correct relative distances.
        '''
        # List of bodies at current time step.
        bodies = self.data_set[frame]

        # Finding target center body in body list.
        center_body = None
        for body in bodies:
            if body.label.lower() == self.center_name.lower():
                center_body = body
                break
        
        # Raises error if body is not found.
        if center_body is None:
            raise ValueError(
                f"Body '{self.center_name}' not found in frame {frame}.")

        # Current x and y coordinates of centered body.
        cx, cy = center_body.position

        # Correcting position of all bodies at current time step for
        # centered body = 0,0.
        xs = [b.position[0] - cx for b in bodies]
        ys = [b.position[1] - cy for b in bodies]

        return xs, ys

    def __create_plot(self):
        '''
        Description:
        Parent function for creating an animation out of
        class attribute data_set.

        Return:
        Returns a FuncAnimation complete with all time steps from
        data_set class attribute.
        '''
        # List of center corrected body positions.
        all_centered = []
        for frame in range(self.set_size):
            xs, ys = self.__get_centered_positions(frame)
            all_centered.append((xs, ys))

        # Updated x and y values for center corrected body positions.
        xs = np.array([x for frame in all_centered for x in frame[0]])
        ys = np.array([y for frame in all_centered for y in frame[1]])

        print(len(xs))
        # Determines furthest object from center.
        max_abs_x = max(abs(xs.min()), abs(xs.max()))
        max_abs_y = max(abs(ys.min()), abs(ys.max()))
        half_range = max(max_abs_x, max_abs_y)

        # Sets grid limits to 1.2x furthest object's x or y distance,
        # depending on which is greater.
        lim = half_range * 1.2
        xlim = (-lim, lim)
        ylim = (-lim, lim)

        fig, ax = plt.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)

        # Stylizes grid and shifts perspective to four quadrants instead of one.
        # Removes top and right line visibility.
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.set_aspect('equal', adjustable='box')
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)

        # Scatterplot for __update function.
        self.scat = ax.scatter([], [])
        self.ax = ax

        # Declaring class attribute list of text labels for each object in
        # a data_set's element.
        self.labels = [
            ax.text(0, 0, "", fontsize=9, ha='left', va='bottom')
            for _ in range(len(self.data_set[0]))
        ]

        # Final animation variable.
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
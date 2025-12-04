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
    
    def __init__(self, bodies, AU=149_597_900_000):
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
        * AU: Astronomical Unit in meters
        '''
        self.data_set = np.array(bodies, dtype=object)
        self.set_size = len(bodies)
        self.AU = AU
    
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
        self.planet_scat.set_offsets(np.column_stack((xs[:9], ys[:9])))
        self.asteroid_scat.set_offsets(np.column_stack((xs[9:], ys[9:])))
        # self.asteroid_range.radius = self.data_set[0, 0].model.dart_distance
        # self.asteroid_range.center = (xs[3], ys[3])

        # Creates label positions in correlation with body positions.
        for label, x, y, body in zip(self.labels, xs, ys, bodies):
            label.set_position((x, y))
            label.set_text(body.label)

        return (self.planet_scat, self.asteroid_scat, *self.labels)

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
        cx = center_body.position[0]
        cy = center_body.position[1]

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

        xlim = (-self.AU * self.multiplier, self.AU * self.multiplier)
        ylim = (-self.AU * self.multiplier, self.AU * self.multiplier)

        fig, ax = plt.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_title("Planetary orbits measured in meters")

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
        self.planet_scat = ax.scatter([], [], s=15, color='blue')
        self.asteroid_scat = ax.scatter([], [], s=3, color='red')
        self.asteroid_range = plt.Circle((0,0), radius=0, fill=False)
        ax.add_patch(self.asteroid_range)
        
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
            interval=60,
            repeat=True,
            blit=True
        )

        return ani

    def animate(self, center="sun", multiplier=1,
                save=False, filename='animation.gif'):
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
        * multiplier: Animation window defaults to 1 AU x 1 AU. multiplier
        directly modifies the AU value in order to zoom in or out.
        Reference values for multiplier:
        1.6 = Sun, Mercury, Venus, Earth, Mars
        32 = All Planets

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
        self.multiplier = multiplier
        self.center_name = center

        # Call to receive animation.
        ani = self.__create_plot()

        # Saves animation as a gif in current operating directory.
        if save:
            print(f"Saving animation to {filename}...")
            ani.save(
                filename,
                fps=300,
                dpi=150,
                writer="pillow"
            )
            print("Saved!")

        # Locally displays the animation without saving it to a file.
        else:
            plt.show()

# END OF FILE -----------------------------------------------------------------
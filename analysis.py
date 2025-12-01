"""
Assumptions about Model 
1. History format is:
    [
     timestep 0: [earth, mars, dart, asteroid, ...],
     timestep 1: [earth, mars, dart, asteroid, ...],
     timestep 2: [earth, mars, dart, asteroid, ...],
     timestep 3: [earth, mars, dart, asteroid, ...],
     ...
   ]
2. Each body object has:
    - .label (string: "earth", "mars", "dart", "asteroid")
    - .position (numpy array: [x, y])
    - .velocity (numpy array: [vx, vy])
    - .mass (number in kg)
    - .radius (number in meters)
"""
import body
import numpy as np
import matplotlib.pyplot as plt

class Analysis:

    def __init__(self):
        self.runs= {}           # dictionary to store runs as {run_name: history}
    



    def add_runs(self, name, history):

        """
        Takes one run adds it into the dictionary to be used later.
        Needs to be updated to be automated with a loop once model is completed
        """
        self.runs[name] = history 

    
    def find_by_label(self, bodies, label):
        """
        Find bodies by their labels
        """
        for i in range(len(bodies)):
            if bodies[i].label == label: 
                return bodies[i]
        return None 




    def get_collision(self, run_name, body_1, body_2):
        """
        Checks to see if collision has happened. 
        If it has then collects the time step it happened on
        """
        history = self.runs[run_name]
        collision_time_step = 0


        for time_step in history:
            body_1_object = self.find_by_label(time_step, body_1)
            body_2_object= self.find_by_label(time_step, body_2)

            if body_1_object is not None and body_2_object is not None:
                if body_1_object.is_collided(body_2_object):
                    return collision_time_step
                else:
                    collision_time_step += 1 

        return None 
    
            
    def calculate_total_energy(self, bodies):
        """
        Calculates the sum of kinetic energy  and potential energy for all bodies
        at certain timestep when collision happens 
        KE Formula = 0.5 * mass * speed^2
        Speed: sqrt of velocity vector 
        PE Formula = -G * mass1 * mass2 / distance
        G = gravitation constant 
        distance = distance between two bodies 
        Total energy = KE + PE
        """
        kinetic_energy = 0
        potential_energy = 0
        
        for b in bodies:
            mass = b.mass
            velocity = b.velocity 
            speed = np.linalg.norm(velocity)
            kinetic_energy += 0.5 * mass * (speed ** 2)

        for i in range (len(bodies)):
            for j in range(i+1, len(bodies)):
                body_1 = bodies[i]
                body_2 = bodies[j]
                mass_1 = body_1.mass
                mass_2 = body_2.mass
                distance = body_1.distance_to(body_2)
                potential_energy += -body.G * mass_1 * mass_2 / distance

        return kinetic_energy + potential_energy
            
    
    def check_conservation_of_energy(self, run_name):
        """
        Checks for conservation of energy and results will be used for plotting 
        to show verification of the model. Tracks total energy between all bodies
        """
        history = self.runs[run_name]
        energy = []

        for time_step in history:
            bodies = time_step
            energy.append(self.calculate_total_energy(bodies))

        return energy


    def calculate_total_momentum(self, bodies):
        """
        Calculates total system momentum by summing momentum of all bodies
        Used later to check conservation of momentum to verify the system
        Returns both directional momentum and magnitude to be anaylized later
        """

        momentum_x = 0
        momentum_y = 0

        for b in bodies:
            mass = b.mass
            velocity_x = b.velocity[0]
            velocity_y = b.velocity[1]

            momentum_x += mass * velocity_x
            momentum_y += mass * velocity_y

        total_momentum = np.array([momentum_x, momentum_y])
        magnitude  = np.linalg.norm(total_momentum)

        return total_momentum, magnitude





    def calculate_conservation_of_momentum(self, run_name):
        """
        Checks to see if the momentum is conserved
        """

        history = self.runs[run_name]
        momentums = []

        for time_step in history:
            bodies = time_step
            momentum, magnitude = self.calculate_total_momentum(bodies)
            momentums.append(momentum)

        return momentums


    #waiting for model
    def get_velocity_change(self, run_name, label, timestep):
        """Measures velocity change of a body before and after collision."""

        pass
    

    def get_trajectory(self, run_name, label):
        """
        Gets the position of given body 
        """
        pass

    #waiting for model
    def analyze_dart_impacts(self):
        pass
    
    #waiting for model
    def compare_trajectories(self):
        
        pass
    
    def plot_energy(self, run_name):
        """
        Plot of energy over time 
        """
        energy = self.check_conservation_of_energy(run_name)
        length = len(energy)
        time_step = np.array(range(length))

        plt.plot(time_step, energy)
        plt.title("Conservation of Energy")
        plt.xlabel("Time Step")
        plt.ylabel("Energy")
        plt.show()

    #waiting for model
    def plot_trajectories(self, label):
        pass


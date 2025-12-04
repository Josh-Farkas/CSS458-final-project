
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
from model import Model
import animation


#========================================Data Storage methods=============================================
class Analysis:

    def __init__(self):
        self.runs= {}           # dictionary to store runs as {run_name: history}
    



    def add_runs(self, name, history, num_asteroids, num_intercepted, num_asteroids_collided, num_intercepted_collided, dt):

        """
        Takes one run adds its information into the dictionary to be used later.
        Needs to be updated to be automated with a loop once model is completed
        """
        self.runs[name] = {
            "history" : history,
            "num_asteroids": num_asteroids,
            "num_intercepted": num_intercepted, 
            "num_asteroids_collided": num_asteroids_collided,
            "num_intercepted_collided": num_intercepted_collided,
            "dt": dt} 

    
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
        history = self.runs[run_name]["history"]
        collision_time_step = 0


        for time_step in history:
            body_1_object = self.find_by_label(time_step, body_1)
            body_2_object= self.find_by_label(time_step, body_2)

            if body_1_object is not None and body_2_object is not None:
                if body_1_object.is_collided(body_2_object):
                    return collision_time_step
            
            collision_time_step += 1 

        return None 
    
   #===================================================================================================


   #========================================Verification Methods-Physcis related=====================================         

    def relative_error(self, v1, v2):
        """Calculates the relative error of two values

        Args:
            v1 (float): True value
            v2 (float): Tested value

        Returns:
            float: The relative error between values as a percentage
        """
        return (v1 - v2) / v1


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
                if distance == 0:
                    continue 
                potential_energy += -body.G * mass_1 * mass_2 / distance
      

        return kinetic_energy + potential_energy
            
    
    def check_conservation_of_energy(self, run_name):
        """
        Checks for conservation of energy and results will be used for plotting 
        to show verification of the model. Tracks total energy between all bodies
        """
        history = self.runs[run_name]["history"]
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





    def check_conservation_of_momentum(self, run_name):
        """
        Checks to see if the momentum is conserved
        """

        history = self.runs[run_name]["history"]
        momentums = []

        for time_step in history:
            bodies = time_step
            momentum, magnitude = self.calculate_total_momentum(bodies)
            momentums.append(momentum)

        return momentums

#=========================================================================================


#========================================Visualization of the Data methods========================================
    
    def plot_energy(self, run_name):
        """
        Plot of energy over time 
        """
        energy = self.check_conservation_of_energy(run_name)
        length = len(energy)
        dt = self.runs[run_name]["dt"]
        time_step = np.array(range(length)) * dt
        
        err = self.relative_error(energy[0], energy[-1])
        print(f'Energy Relative Error: {err}')

        plt.plot(time_step, energy)
        plt.title("Conservation of Energy")
        plt.xlabel("Time(seconds)")
        plt.ylabel("Energy")
        plt.show()


    def plot_momentum(self, run_name):
        """
        Plots the magnitude of momentum vector against the timesteps
        """
        momentum = self.check_conservation_of_momentum(run_name)
        length = len(momentum)
        dt = self.runs[run_name]["dt"]
        time_step = np.array(range(length)) * dt
        magnitudes = [np.linalg.norm(m) for m in momentum]

        err = self.relative_error(magnitudes[0], magnitudes[-1])
        print(f'Momentum Relative Error: {err}')

        plt.plot(time_step, magnitudes)
        plt.title("Conservation of Momentum")
        plt.xlabel("Time(seconds)")
        plt.ylabel("Momentum Magnitude")
        plt.show()


    def plot_success_metrics(self, run_name):
        """
        Plot success (protection rate) over time steps
        WITHOUT modifying Body or Model.
        """
        history = self.runs[run_name]["history"]
        dt = self.runs[run_name]["dt"]
        total_asteroids = self.runs[run_name]["num_asteroids"]

        success_rates = []

        for timestep in history:
            # Identify asteroids
            asteroids_remaining = len([b for b in timestep if "asteroid" in b.label])
            

            if total_asteroids == 0:
                success_rates.append(100)
            else:
                # Success rate = % of asteroids that did NOT collide
                success = (asteroids_remaining / total_asteroids) * 100
                success_rates.append(success)

        # Time array
        time_array = np.arange(len(history)) * dt
        plt.plot(time_array, success_rates)
        plt.title("Protection Rate over Time")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Earth Protection (%)")
        plt.show()

        

    def compare_runs(self, run_1_name, run_2_name):
        
        pass
#==========================================================================================




#========================================DART effectivenes methods=============================================
    def calculate_interception_rate(self, run_name):
        
        num_intercepted = self.runs[run_name]["num_intercepted"]
        num_asteroids = self.runs[run_name]["num_asteroids"]

        if num_asteroids == 0:
            return 0 
        
        interception_rate = num_intercepted / num_asteroids * 100

        return interception_rate


    def calculate_failed_interception_rate(self, run_name):

        num_interception_failed = self.runs[run_name]["num_intercepted_collided"]
        num_asteroids = self.runs[run_name]["num_asteroids"]

        if num_asteroids == 0:
            return 0 
        
        failed_interception_rate = num_interception_failed / num_asteroids * 100
        return failed_interception_rate


    def calculate_success_rate(self, run_name):
        num_collided = self.runs[run_name]["num_asteroids_collided"]
        num_asteroids = self.runs[run_name]["num_asteroids"]

        if num_asteroids == 0:
            return 0 
        
        protection_rate = (num_asteroids - num_collided) / num_asteroids * 100
        return protection_rate
#=====================================================================================================


#========================================Sensitivity Analysis=============================================

    def dart_speed_analysis(self, speed_values):
        """
        Calls the Model seperatetly to anaylize different speeds for darts 
        and see how it affects trackable data, aka num_intercepted, num_failed_interception and num_collided
        """
 
        interception_rates = []
        failed_interception_rates = []
        protection_rates = []

        for speed in speed_values:
            m = Model(
            dart_speed=speed, 
            collision_elasticity=1, 
            duration=3600*24*7,  
            dt=300,
            #store_history=True
        )
            history = m.run()

            run_name = f"speed_{speed}"
            self.add_runs(run_name, 
                    history, 
                    m.num_asteroids,
                    m.num_intercepted, 
                    m.num_asteroids_collided, 
                    m.num_intercepted_collided, 
                    m.dt)

            #calculate Metrics 
            interception_rates.append(self.calculate_interception_rate(run_name))
            failed_interception_rates.append(self.calculate_failed_interception_rate(run_name))
            protection_rates.append(self.calculate_success_rate(run_name))

            # Plot results
        plt.figure(figsize=(12, 5))
        
       # Interception Rate
        plt.subplot(1, 3, 1)
        plt.plot(speed_values, interception_rates, marker='o', linewidth=2, color='blue')
        plt.title("Interception Rate vs DART Speed")
        plt.xlabel("DART Speed (m/s)")
        plt.ylabel("Interception Rate (%)")
        plt.grid(True, alpha=0.3)
        
        # Failed Interceptions
        plt.subplot(1, 3, 2)
        plt.plot(speed_values, failed_interception_rates, marker='o', linewidth=2, color='orange')
        plt.title("Failed Interception Rate vs DART Speed")
        plt.xlabel("DART Speed (m/s)")
        plt.ylabel("Failed Interception Rate (%)")
        plt.grid(True, alpha=0.3)
                #  Protection Rate
        plt.subplot(1, 3, 3)
        plt.plot(speed_values, protection_rates, marker='o', linewidth=2, color='green')
        plt.title("Protection Rate vs DART Speed")
        plt.xlabel("DART Speed (m/s)")
        plt.ylabel("Protection Rate (%)")
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()


    def dart_mass_analysis(self, mass_values):

        """
        Similar to speed analysis but analyzes the results with different dart masses
        """
        interception_rates = []
        failed_interception_rates = []
        protection_rates = []

        for mass in mass_values:
            m = Model(dart_mass=mass, collision_elasticity=1, 
                  duration=3600*2, dt=300)

            history = m.run()

            run_name = f"mass{mass}"
            self.add_runs(run_name, 
                    history, 
                    m.num_asteroids,
                    m.num_intercepted, 
                    m.num_asteroids_collided, 
                    m.num_intercepted_collided, 
                    m.dt)
        
            interception_rates.append(self.calculate_interception_rate(run_name))
            failed_interception_rates.append(self.calculate_failed_interception_rate(run_name))
            protection_rates.append(self.calculate_success_rate(run_name))

            # Plot results
        plt.figure(figsize=(12, 5))
        
        
        #  Failed Interceptions
        plt.subplot(1, 3, 1)
        plt.plot(mass_values, failed_interception_rates, marker='o', linewidth=2, color='orange')
        plt.title("Failed Interception Rate vs DART Mass")
        plt.xlabel("DART Mass (m/s)")
        plt.ylabel("Failed Interception Rate (%)")
        plt.grid(True, alpha=0.3)
        
        #  Protection Rate
        plt.subplot(1, 3, 2)
        plt.plot(mass_values, protection_rates, marker='o', linewidth=2, color='green')
        plt.title("Protection Rate vs DART Mass")
        plt.xlabel("DART Mass (m/s)")
        plt.ylabel("Protection Rate (%)")
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()


    def body_offset_analysis(self, seed=0):
        """Compares Body ending positions in two different models with the same seed

        Args:
            seed (float): random seed
        """
        # Model with no DARTs
        m_base = Model(seed=seed, dart_mass=610, duration=3600*24*1, dt=60, asteroid_distance_mean=12000000000, small_detection=0, medium_detection=0, large_detection=0) # Add parameters here
        h = m_base.run()
        end_base = h[-1][9:] # Ignore planets (first 9)
        num_asteroids = len(end_base)
        masses = [100, 200, 300, 600, 900, 1200, 1500, 1800]
        # masses = [300, 600, 900]
        all_distances = np.zeros((len(masses),))
        for im, mass in enumerate(masses):
            print(f"Testing Mass: {mass}")
            m = Model(seed=seed, duration=3600, dt=60, dart_mass=mass, asteroid_distance_mean=12000000000, small_detection=1.0, medium_detection=1.0, large_detection=1.0) # Add different parameters here
            end = m.run()[-1][9:]
        
            distances = np.zeros((num_asteroids,))
            # Get distance of all bodies
            for j, b1, b2 in zip(range(num_asteroids), end_base, end):
                offset = b1.position - b2.position
                dist = np.linalg.norm(offset)
                distances[j] = dist
            mean = np.mean(distances)
            all_distances[im] = mean
            
        plt.plot(masses, all_distances)
        plt.title("DART mass vs Asteroid Offset Distance")
        plt.xlabel("DART Mass (kg)")
        plt.ylabel("Asteroid Offset (m)")
        plt.grid(True, alpha=0.3)
        plt.show()
        


#=============================================================================================

    def run_sensitivity_test(self):
        speeds = np.linspace(3000, 10000, 3)
        self.dart_speed_analysis(speeds)


        masses = np.linspace(100, 2000, 3)
        self.dart_mass_analysis(masses)



    def run_single_test(self):
        m = Model(collision_elasticity=1)
        history = m.run()


        # Store the results
        self.add_runs(
            "test_run",
            history,
            m.num_asteroids,
            m.num_intercepted,
            m.num_asteroids_collided,
            m.num_intercepted_collided,
            m.dt
        )
        
        # Generate plots
        self.plot_energy("test_run")
        self.plot_momentum("test_run")
        self.plot_success_metrics("test_run")
        

        print(f"\nInterception Rate: {self.calculate_interception_rate('test_run'):.2f}%")
        print(f"Failed Interception Rate: {self.calculate_failed_interception_rate('test_run'):.2f}%")
        print(f"Protection Rate: {self.calculate_success_rate('test_run'):.2f}%")


if __name__ == "__main__":
    analysis = Analysis()
    analysis.run_single_test()

    analysis.run_sensitivity_test()


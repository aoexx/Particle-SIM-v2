from manim import *
import numpy as np

# ==================================================================
#  MOLECULAR DYNAMICS SIMULATION (WITH REFLECTIVE BOUNDARIES) 
# ==================================================================
# This script implements a molecular dynamics (MD) simulation 
# using the Lennard-Jones potential and Velocity-Verlet integration.
# Reflective boundary conditions are applied to ensure particles 
# remain confined within a simulation box.
# ==================================================================


# ----------------- CONFIGURATION PARAMETERS -----------------
class SimulationConfig:
    """
    Defines global simulation parameters such as system size,
    integration timestep, and force field parameters.
    """

    dt = 0.005  # Integration timestep (fs)
    num_steps = 500  # Total number of simulation steps
    num_particles = 10  # Number of particles in the system
    box_size = 10  # Dimension of the cubic simulation box
    epsilon = 1.0  # Depth of Lennard-Jones potential well
    sigma = 1.0  # Finite distance where inter-particle potential = 0
    mass = 1.0  # Particle mass (atomic mass units)
    cutoff_radius = 2.5 * sigma  # Distance beyond which interactions are ignored


# ----------------- PARTICLE CLASS -----------------
class Particle:
    """
    Represents a single particle in the MD simulation.
    
    Attributes:
    - position: 3D coordinates of the particle
    - velocity: 3D velocity vector
    - force: Net force acting on the particle (updated at each step)
    """

    def __init__(self, position, velocity):
        """
        Initializes a particle with a given position and velocity.
        """
        self.position = np.array(position)  # Position vector (x, y, z)
        self.velocity = np.array(velocity)  # Velocity vector (vx, vy, vz)
        self.force = np.zeros(3)  # Initializes force as zero

    def update_position(self, dt):
        """
        Updates the particle's position using the Velocity-Verlet algorithm.
        
        Equation: r(t + dt) = r(t) + v(t) * dt + 0.5 * F(t) * dt² / m
        """
        self.position += self.velocity * dt + 0.5 * self.force * (dt ** 2) / SimulationConfig.mass

    def update_velocity(self, new_force, dt):
        """
        Updates the particle's velocity using the Velocity-Verlet algorithm.
        
        Equation: v(t + dt) = v(t) + 0.5 * (F(t) + F(t + dt)) * dt / m
        """
        self.velocity += 0.5 * (self.force + new_force) * dt / SimulationConfig.mass
        self.force = new_force  # Update force for the next iteration


# ----------------- MOLECULAR DYNAMICS SYSTEM -----------------
class MDSystem:
    """
    Represents a molecular system containing multiple particles.

    - Initializes the system with random positions and velocities.
    - Computes inter-particle forces using the Lennard-Jones potential.
    - Integrates equations of motion using the Velocity-Verlet method.
    - Applies reflective boundary conditions to prevent particle escape.
    """

    def __init__(self):
        """ 
        Initializes the particle system within a cubic simulation box.
        """
        np.random.seed(42)  # Ensures reproducibility of random initialization
        self.particles = [
            Particle(
                position=np.random.uniform(2, SimulationConfig.box_size - 2, 3),  # Prevents particles from starting at edges
                velocity=np.random.uniform(-2.0, 2.0, 3)  # Assigns random initial velocities
            ) for _ in range(SimulationConfig.num_particles)
        ]
        self.trajectories = np.zeros((SimulationConfig.num_steps, SimulationConfig.num_particles, 3))

    def lennard_jones_force(self, r):
        """
        Computes the Lennard-Jones force between two particles.

        Lennard-Jones potential: 
            U(r) = 4ε [(σ/r)^12 - (σ/r)^6]
        
        Force equation:
            F(r) = -dU/dr = 24ε [(2σ^12 / r^13) - (σ^6 / r^7)]

        Args:
            r (np.array): Displacement vector between two particles.

        Returns:
            np.array: Lennard-Jones force vector.
        """
        r_mag = np.linalg.norm(r)  # Compute magnitude of the distance vector
        if r_mag == 0 or r_mag > SimulationConfig.cutoff_radius:
            return np.zeros(3)  # No force if distance is 0 or beyond cutoff

        # Compute force magnitude
        force_magnitude = 24 * SimulationConfig.epsilon * (
            (2 * (SimulationConfig.sigma ** 12) / (r_mag ** 13)) - ((SimulationConfig.sigma ** 6) / (r_mag ** 7))
        )
        return force_magnitude * (r / r_mag)  # Convert to vector form

    def compute_forces(self):
        """
        Computes and updates forces for all particle pairs.
        Uses Newton's Third Law: F_ij = -F_ji to avoid redundant calculations.
        """
        for i in range(SimulationConfig.num_particles):
            self.particles[i].force = np.zeros(3)  # Reset forces
        for i in range(SimulationConfig.num_particles):
            for j in range(i + 1, SimulationConfig.num_particles):
                r = self.particles[j].position - self.particles[i].position
                force = self.lennard_jones_force(r)
                self.particles[i].force += force
                self.particles[j].force -= force  # Action-reaction pair

    def enforce_boundaries(self, particle):
        """
        Applies reflective boundary conditions to confine particles within the box.
        
        - If a particle reaches a boundary, its velocity component in that direction is inverted.
        - Ensures momentum conservation while keeping particles inside the simulation box.
        """
        for dim in range(3):  # Loop over x, y, and z dimensions
            if particle.position[dim] <= 0:
                particle.position[dim] = 0  # Prevents escape
                particle.velocity[dim] *= -1  # Reflects velocity
            elif particle.position[dim] >= SimulationConfig.box_size:
                particle.position[dim] = SimulationConfig.box_size  # Prevents escape
                particle.velocity[dim] *= -1  # Reflects velocity

    def update_system(self):
        """
        Advances the simulation by one timestep using Velocity-Verlet integration.
        """
        for particle in self.particles:
            particle.update_position(SimulationConfig.dt)
            self.enforce_boundaries(particle)  # Apply reflective boundaries

        self.compute_forces()  # Recalculate forces after moving particles

        for particle in self.particles:
            particle.update_velocity(particle.force, SimulationConfig.dt)

    def run_simulation(self):
        """
        Executes the full simulation over the defined number of timesteps.
        Particle trajectories are recorded for post-simulation analysis and visualization.
        """
        for step in range(SimulationConfig.num_steps):
            self.update_system()
            self.trajectories[step] = [p.position for p in self.particles]

        # Save the trajectory data for visualization
        np.save("trajectories.npy", self.trajectories)


# ----------------- EXECUTE THE SIMULATION -----------------
if __name__ == "__main__":
    """
    Runs the MD simulation and stores trajectory data.
    """
    md_sim = MDSystem()
    md_sim.run_simulation()

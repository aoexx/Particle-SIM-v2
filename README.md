# Particle-SIM-v2
# Molecular Dynamics Simulation - MD_SIM-AD-2-1

## Overview
This iteration of the molecular dynamics (MD) simulation builds upon **MD_SIM-AD-1-1**, introducing significant improvements in **boundary conditions, numerical integration, and visualization techniques**. The primary focus is ensuring that particles remain **confined within the simulation box** while maintaining **accurate energy conservation**.

The simulation continues to use **Lennard-Jones interactions** to model inter-particle forces but now implements **Velocity-Verlet integration** for more accurate trajectory calculations. 

Reflective boundary conditions have been introduced to ensure **particles bounce off walls instead of escaping**, improving the **physical realism** of the model. Additionally, **force calculations have been optimized** to enhance computational efficiency.

---

## Key Features
- **Velocity-Verlet Integration:** Replaces **explicit Euler integration** for improved numerical stability and energy conservation.
- **Reflective Boundary Conditions:** Ensures particles bounce off walls rather than escaping the simulation box.
- **Lennard-Jones Potential:** Implements **interatomic force calculations** with an optimized cutoff.
- **Improved 3D Visualization:** Uses **Manim** for high-quality animation and trajectory tracking.
- **Computational Efficiency:** Reduces redundant force calculations using **Newton’s Third Law**.

---

## Comparing with Previous Versions
### MD_SIM-AD-1-1/2/3
- **Explicit Euler Integration** → Lower accuracy, less energy conservation.
- **No Boundary Conditions** → Particles escape the simulation box.
- **2D Projection Visualization** → Lacks clarity for real-world molecular motion.

### MD_SIM-AD-2-1 (This Version)
- **Velocity-Verlet Integration** → More accurate trajectory calculations.
- **Reflective Boundaries** → Particles bounce off instead of escaping.
- **3D Animated Visualization** → Improved trajectory clarity using Manim.

---

## Challenges and Solutions
### Challenge: Particles Escaping the Simulation Box
- **Issue:** No boundary enforcement led to particles drifting out of bounds.
- **Solution:** Introduced **reflective boundary conditions**, ensuring particles reflect upon collision with a boundary.

### Challenge: Numerical Drift in Energy Conservation
- **Issue:** Euler integration introduced **energy drift** over time.
- **Solution:** Implemented **Velocity-Verlet integration**, significantly improving numerical stability.

### Challenge: Visualizing High-Speed Particle Motion
- **Issue:** Previous visualization techniques failed to **smoothly capture high-speed motion**.
- **Solution:** Switched to **Manim**, enabling **trajectory tracking and real-time visualization**.

---

## Installation & Usage
### 1. Install Dependencies
```bash
pip install numpy manim matplotlib
```

### 2. Run the Simulation
```bash
python MD_SIM-AD-2-1.py
```
- Generates the **trajectory file (`trajectories.npy`)**.

### 3. Visualize the Simulation
```bash
python visualize.py
```
- Uses **Manim** to animate particle motion.

---

## Future Improvements
While this iteration significantly improves the **stability and boundary handling**, there are **additional areas for refinement**:
- **Periodic Boundary Conditions (PBCs):** Instead of bouncing, particles could **wrap around** the simulation box for a more realistic representation of bulk systems.
- **Thermostat Implementation:** Introduce a **Berendsen thermostat** to maintain a controlled system temperature.
- **Neighbor Lists for Optimized Force Computation:** Reduce redundant calculations in large systems.
- **Collision Handling Enhancements:** Currently, when particles **collide**, their velocities may increase **unrealistically** due to force accumulation. Implementing a **momentum-conserving collision model** will improve physical accuracy.

---

## References
- **Understanding Molecular Simulation** – Daan Frenkel, Berend Smit  
- **Schrödinger’s Desmond MD Engine Tutorial and Manual Documents** – Used for comparison  
- **OpenMM, GROMACS** – Industry-standard MD software for validation  

---

## License
This project is licensed under the **MIT License** – feel free to modify and use it for academic and research purposes.


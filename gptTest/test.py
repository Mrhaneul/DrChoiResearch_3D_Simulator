import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11      # Gravitational constant (m^3 kg^-1 s^-2)
c = 299792458        # Speed of light (m/s)

# Simulation parameters
num_steps = 5000     # Number of integration steps
dt = 0.1             # Time step (seconds)
light_speed = c      # Speed of light (m/s)

# Positions
light_source_pos = np.array([0.0, -100.0, -500.0])   # Light source position
observer_pos = np.array([0.0, 0.0, 500.0])           # Observer position

# Gravitational masses (you can add or modify masses here)
gravitational_masses = [
    {'mass': 1e16, 'position': np.array([0.0, 0.0, 0.0])},
    # Add more masses as needed
    # Example:
    # {'mass': 5e15, 'position': np.array([50.0, 0.0, 100.0])},
]

# Light rays initial conditions
num_rays = 5   # Number of light rays to simulate
ray_spread = 100.0   # Spread of initial rays in y-direction
initial_positions = []
initial_velocities = []

for i in range(num_rays):
    # Distribute rays in y-direction
    y_offset = -ray_spread / 2 + i * (ray_spread / (num_rays - 1))
    pos = light_source_pos + np.array([0.0, y_offset, 0.0])
    # Initial velocity towards the observer (along +z) with speed c
    vel = light_speed * (observer_pos - light_source_pos)
    vel /= np.linalg.norm(vel)  # Normalize to speed c
    initial_positions.append(pos)
    initial_velocities.append(vel)

# Gravitational acceleration function
def gravitational_acceleration(pos, masses):
    total_accel = np.zeros(3)
    for mass_obj in masses:
        mass = mass_obj['mass']
        mass_pos = mass_obj['position']
        r_vec = pos - mass_pos
        r_mag = np.linalg.norm(r_vec)
        if r_mag == 0:
            continue  # Avoid division by zero
        # Acceleration vector (points towards the mass)
        a_vec = -G * mass * r_vec / r_mag**3
        total_accel += a_vec
    return total_accel

# Normalize function
def normalize(vec, magnitude):
    return magnitude * vec / np.linalg.norm(vec)

# RK4 Integration Function
def rk4_step(pos, vel, dt, masses):
    # First estimate
    accel1 = gravitational_acceleration(pos, masses)
    vel1 = vel
    pos1 = pos

    # Second estimate
    vel2 = vel + accel1 * dt / 2
    pos2 = pos + vel1 * dt / 2
    accel2 = gravitational_acceleration(pos2, masses)

    # Third estimate
    vel3 = vel + accel2 * dt / 2
    pos3 = pos + vel2 * dt / 2
    accel3 = gravitational_acceleration(pos3, masses)

    # Fourth estimate
    vel4 = vel + accel3 * dt
    pos4 = pos + vel3 * dt
    accel4 = gravitational_acceleration(pos4, masses)

    # Combine estimates
    pos_next = pos + (vel1 + 2*vel2 + 2*vel3 + vel4) * dt / 6
    vel_next = vel + (accel1 + 2*accel2 + 2*accel3 + accel4) * dt / 6

    # Normalize velocity to maintain speed c
    vel_next = normalize(vel_next, light_speed)

    return pos_next, vel_next

# Integrate the paths of the light rays
paths = []

for pos0, vel0 in zip(initial_positions, initial_velocities):
    pos = pos0.copy()
    vel = vel0.copy()
    path = [pos.copy()]
    for _ in range(num_steps):
        pos, vel = rk4_step(pos, vel, dt, gravitational_masses)
        path.append(pos.copy())
        if np.linalg.norm(pos - observer_pos) < 1.0:
            break  # Stop if the light has reached the observer
    paths.append(np.array(path))

# Plotting
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_title('Interactive Gravitational Lensing Simulation')

# Plot the gravitational masses
for mass_obj in gravitational_masses:
    mass_pos = mass_obj['position']
    ax.scatter(*mass_pos, color='yellow', s=100, label='Gravitational Mass')
    ax.text(*mass_pos, 'Mass', color='black')

# Plot the observer
ax.scatter(*observer_pos, color='green', s=100, label='Observer')
ax.text(*observer_pos, 'Observer', color='black')

# Plot the light source
ax.scatter(*light_source_pos, color='red', s=100, label='Light Source')
ax.text(*light_source_pos, 'Light Source', color='black')

# Plot the paths of the light rays
for path in paths:
    ax.plot(path[:, 0], path[:, 1], path[:, 2], color='blue')

# Set labels
ax.set_xlabel('X Position (m)')
ax.set_ylabel('Y Position (m)')
ax.set_zlabel('Z Position (m)')

# Set equal aspect ratio for all axes
ax.set_box_aspect([1,1,1])

# Set limits (adjust as needed)
max_range = 600
ax.set_xlim(-max_range, max_range)
ax.set_ylim(-max_range, max_range)
ax.set_zlim(-max_range, max_range)

# Add legend
ax.legend()

plt.show()
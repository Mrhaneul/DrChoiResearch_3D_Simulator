import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11       # Gravitational constant (m^3 kg^-1 s^-2)
c = 299792458         # Speed of light (m/s)

# Simulation parameters
mass = 1e256        # Mass of the gravitational lens (kg)
num_rays = 1       # Number of light rays to simulate
num_steps = 10000   # Number of integration steps
dt = 0.1          # Time step (seconds)

# Positions
light_source_pos = np.array([0.0, 10.0, -1e4])  # Light source position
lens_pos = np.array([0.0, 0.0, 0.0])           # Gravitational lens at the origin
observer_pos = np.array([0.0, 0.0, 1e4])       # Observer position

# Generate initial conditions for light rays
initial_positions = [light_source_pos.copy()]
initial_velocities = [c * np.array([0.0, 0.0, 1.0])]

# Gravitational acceleration function
def gravitational_acceleration(pos, mass, lens_pos):
    r_vec = pos - lens_pos
    r_mag = np.linalg.norm(r_vec)
    if r_mag == 0:
        return np.zeros(3)
    a_vec = -G * mass * (r_vec) / r_mag**3
    return a_vec

# Normalize function
def normalize(vec, magnitude):
    return magnitude * vec / np.linalg.norm(vec)

# RK4 Integration Function
def rk4_step(pos, vel, dt):
    # First estimate
    accel1 = gravitational_acceleration(pos, mass, lens_pos)
    vel1 = vel
    pos1 = pos

    # Second estimate
    vel2 = vel + accel1 * dt / 2
    vel2 = normalize(vel2, c)
    pos2 = pos + vel1 * dt / 2

    accel2 = gravitational_acceleration(pos2, mass, lens_pos)

    # Third estimate
    vel3 = vel + accel2 * dt / 2
    vel3 = normalize(vel3, c)
    pos3 = pos + vel2 * dt / 2

    accel3 = gravitational_acceleration(pos3, mass, lens_pos)

    # Fourth estimate
    vel4 = vel + accel3 * dt
    vel4 = normalize(vel4, c)
    pos4 = pos + vel3 * dt

    accel4 = gravitational_acceleration(pos4, mass, lens_pos)

    # Combine estimates
    pos_next = pos + (vel1 + 2*vel2 + 2*vel3 + vel4) * dt / 6
    vel_next = vel + (accel1 + 2*accel2 + 2*accel3 + accel4) * dt / 6

    # Normalize velocity to maintain speed c
    vel_next = normalize(vel_next, c)

    return pos_next, vel_next

# Integrate the paths of the light rays
paths = []

for pos0, vel0 in zip(initial_positions, initial_velocities):
    pos = pos0.copy()
    vel = vel0.copy()
    path = [pos.copy()]
    for _ in range(num_steps):
        pos, vel = rk4_step(pos, vel, dt)
        path.append(pos.copy())
        if pos[2] >= observer_pos[2]:
            break
    paths.append(np.array(path))

# Plotting
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_title('Gravitational Lensing Simulation with RK4 Integration')

# Plot the gravitational lens
ax.scatter(*lens_pos, color='yellow', s=100, label='Gravitational Mass')

# Plot the observer
ax.scatter(*observer_pos, color='green', s=100, label='Observer')

# Plot the light source
ax.scatter(*light_source_pos, color='red', s=100, label='Light Source')

# Plot the paths of the light rays
for path in paths:
    ax.plot(path[:, 0], path[:, 1], path[:, 2], color='blue')

# Set labels
ax.set_xlabel('X Position (m)')
ax.set_ylabel('Y Position (m)')
ax.set_zlabel('Z Position (m)')

# Set equal aspect ratio for all axes
ax.set_box_aspect([1,1,2])

# Set limits
ax.set_xlim(-50, 50)
ax.set_ylim(-50, 50)
ax.set_zlim(-1e4, 1e4)

# Add legend
ax.legend()

plt.show()
import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11      # Gravitational constant (m^3 kg^-1 s^-2)
c = 1e4              # Artificial speed of light for simulation purposes

# Gravity source definition
class GravitySource:
    def __init__(self, position, strength):
        self.position = np.array(position, dtype=float)
        self.strength = strength  # Physical strength used in calculations

    def get_visual_size(self):
        # Return a fixed reasonable size for visualization
        return 50  # Adjust as needed

# Light ray class
class LightRay:
    def __init__(self, position, direction):
        self.position = np.array(position, dtype=float)
        self.direction = np.array(direction, dtype=float)
        self.direction /= np.linalg.norm(self.direction)  # Normalize direction vector
        self.path = [self.position.copy()]  # Stores the trajectory

    def update(self, dt, gravity_sources):
        # Compute gravitational deflection
        deflection = compute_gravitational_deflection(self.position, gravity_sources)
        # Update direction
        self.direction += deflection * dt
        self.direction /= np.linalg.norm(self.direction)  # Normalize to maintain constant speed
        # Update position
        self.position += c * self.direction * dt
        self.path.append(self.position.copy())

# Function to compute gravitational deflection on light
def compute_gravitational_deflection(position, gravity_sources):
    total_deflection = np.zeros(3)
    for source in gravity_sources:
        r_vec = source.position - position
        r_mag = np.linalg.norm(r_vec)
        if r_mag == 0:
            continue  # Avoid division by zero
        # Simplified deflection formula
        deflection = (4 * G * source.strength / (c**2 * r_mag**3)) * r_vec
        total_deflection += deflection
    return total_deflection

# Initialize the 3D canvas
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Set titles and labels
ax.set_title('Light Rays Moving Along Y-Axis Through Gravity Sources')
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_zlabel('Z Position')

# Set equal aspect ratio for all axes
ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio for x, y, z

# Initialize a list to store gravity sources
gravity_sources = []

# Function to add a gravity source (with z fixed to 0)
def add_gravity_source(position, strength, label=None):
    position = np.array([position[0], position[1], 0.0])  # Fix z-coordinate to 0
    source = GravitySource(position, strength)
    gravity_sources.append(source)
    
    # Choose color based on strength sign
    color = 'red' if strength > 0 else 'blue'  # Red for gravity, blue for anti-gravity
    ax.scatter(*position, color=color, s=source.get_visual_size())
    if label:
        ax.text(*position, label, color='black')

# Example gravity and anti-gravity positions along y-axis
gravity_positions = np.arange(10_000, 100_000, 10_000)
anti_gravity_positions = np.arange(15_000, 95_000, 10_000)

# Creating columns of gravity sources
column1 = [(50_000, pos) for pos in gravity_positions]  # Gravity sources at x=50,000
column2 = [(55_000, pos) for pos in anti_gravity_positions]  # Anti-gravity sources at x=55,000

# Adjusted strength values for simulation
gravity_strength = 1e25  # Increased to produce noticeable deflection
anti_gravity_strength = -1e25

# Add gravity sources (positive strength)
for pos in column1:
    add_gravity_source(position=pos, strength=gravity_strength)  # Gravity sources

# Add anti-gravity sources (negative strength)
for pos in column2:
    add_gravity_source(position=pos, strength=anti_gravity_strength)  # Anti-gravity sources

# Initialize multiple light rays moving along the y-axis
light_rays = []
x_position = 49_500  # Start close to gravity sources
z_position = 0.0     # Fixed z position

# Create light rays at different x-offsets
x_offsets = [0, 5000, -5000]  # Adjust offsets to sample different paths

for x_offset in x_offsets:
    # Start from y = -10,000 to ensure they reach gravity sources
    light_ray = LightRay(position=[x_position, 50_000 + x_offset, z_position], direction=[1, 0, 0])  # Moving along +y-axis
    light_rays.append(light_ray)

# Simulation parameters
dt = 0.001  # Time step
num_steps = 20_000  # Number of steps

# Colors for the light rays
colors = ['cyan', 'magenta', 'yellow']

# Simulate the light rays' paths
for idx, light_ray in enumerate(light_rays):
    for _ in range(num_steps):
        light_ray.update(dt, gravity_sources)
        # Stop condition
        if light_ray.position[1] > 110_000 or light_ray.position[1] < -10_000:
            break
    # Convert the path to a NumPy array for plotting
    light_path = np.array(light.path)
    # Plot the light ray's path
    ax.plot(light_path[:, 0], light_path[:, 1], light_path[:, 2],
            color=colors[idx], linewidth=2, label=f'Light Ray {idx+1}')
    # Plot straight path for comparison
    straight_path_y = np.linspace(-10_000, 110_000, 100)
    straight_path_x = np.full_like(straight_path_y, light_ray.position[0])
    ax.plot(straight_path_x, straight_path_y, np.full_like(straight_path_y, z_position),
            color='gray', linestyle='--', linewidth=1)

# Adjust plot limits
ax.set_xlim(48_000, 56_000)
ax.set_ylim(-10_000, 110_000)
ax.set_zlim(-10, 10)

# Add legend
ax.legend()

plt.show()
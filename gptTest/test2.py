import numpy as np
import matplotlib.pyplot as plt

# Initialize the 3D canvas
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Set titles and labels
ax.set_title('3D Simulation Canvas')
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_zlabel('Z Position')

# Set equal aspect ratio for all axes
ax.set_box_aspect([1,1,1])

# Initialize lists to store sources and lines
sources = []
lines = []

# Function to add a source
def add_source(position, color='red', size=50, label=None):
    source = {
        'position': position,
        'color': color,
        'size': size,
        'label': label
    }
    sources.append(source)
    # Plot the source
    ax.scatter(*position, color=color, s=size)
    if label:
        ax.text(*position, label, color='black')

# Function to remove a source
def remove_source(index):
    if 0 <= index < len(sources):
        sources.pop(index)
        redraw()

# Function to plot a line given a list of points
def plot_line(points, color='blue', linewidth=1, label=None):
    line = {
        'points': points,
        'color': color,
        'linewidth': linewidth,
        'label': label
    }
    lines.append(line)
    points = np.array(points)
    ax.plot(points[:, 0], points[:, 1], points[:, 2], color=color, linewidth=linewidth)
    if label:
        ax.text(points[-1, 0], points[-1, 1], points[-1, 2], label, color='black')

# Function to clear and redraw the canvas
def redraw():
    ax.clear()
    # Redraw sources
    for source in sources:
        pos = source['position']
        ax.scatter(*pos, color=source['color'], s=source['size'])
        if source['label']:
            ax.text(*pos, source['label'], color='black')
    # Redraw lines
    for line in lines:
        points = np.array(line['points'])
        ax.plot(points[:, 0], points[:, 1], points[:, 2], color=line['color'], linewidth=line['linewidth'])
        if line['label']:
            ax.text(points[-1, 0], points[-1, 1], points[-1, 2], line['label'], color='black')
    # Set labels and aspect ratio again
    ax.set_title('3D Simulation Canvas')
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_zlabel('Z Position')
    ax.set_box_aspect([1,1,1])
    plt.draw()

# Example usage:

# Add sources
add_source(position=[0, 0, 0], color='yellow', label='Source 1')
add_source(position=[10, 10, 10], color='green', label='Source 2')
add_source(position=[6, 4, 2], color = "blue", label = "source3")

# Plot a line
line_points = [[0, 0, 0], [6, 4, 2], [10, 10, 10], [1,2,3]]
plot_line(points=line_points, color='blue', linewidth=2, label='Line 1')

# Show the plot
plt.show()
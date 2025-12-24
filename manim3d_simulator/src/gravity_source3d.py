import math
from manim import *
from manim3d_simulator.control_panel import ControlPanel as cp

class GravitySource3D(Group):
    def __init__(self, mass, position):
        super().__init__()
        self.mass = mass
        self.position = position
        # Create a visual object, like a dot, at the gravity source's position
        self.gravity_sphere_obj = Group(self.gravity_sphere())  # Wrap the gravity sphere in a Group
        self.add(self.gravity_sphere_obj)  # Add the sphere Group to this Group

    def gravity_sphere(self):
        return Sphere(
            radius=cp.GRAVITY_SOURCE_RADIUS, 
            color=cp.GRAVITY_SOURCE_COLOR,
            fill_opacity=0.5,
            stroke_color=cp.GRAVITY_SOURCE_COLOR
        )

    def gravitational_pull(self, light_ray_position):
        # Calculate the gravitational pull based on distance
        distance = math.sqrt((light_ray_position[0] - self.position[0])**2 + 
                             (light_ray_position[1] - self.position[1])**2 + 
                             (light_ray_position[2] - self.position[2])**2)
        if distance == 0:
            return (0, 0, 0)    # Avoid division by zero
        strength = self.mass / distance**2
        direction = (
            (self.position[0] - light_ray_position[0]) / distance,
            (self.position[1] - light_ray_position[1]) / distance,
            (self.position[2] - light_ray_position[2]) / distance
        )
        pull_vector = (strength * direction[0], strength * direction[1], strength * direction[2])
        return pull_vector
    
    def set_position(self, position):
        self.position = position
        # Update the gravity sphere's position when the gravity source's position changes
        self.gravity_sphere_obj.move_to(self.position)  # Move the sphere object

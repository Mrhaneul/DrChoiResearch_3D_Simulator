import math
from manim import *
from control_panel import ControlPanel as cp

class AntiGravitySource3D(VGroup):
    def __init__(self, mass, position):
        super().__init__()
        self.mass = mass
        self.position = position
        # Create a visual object (sphere) for the anti-gravity source
        self.antigravity_sphere_obj = self.antigravity_sphere()
        self.add(self.antigravity_sphere_obj)

    def antigravity_sphere(self):
        return Sphere(
            radius=cp.GRAVITY_SOURCE_RADIUS,
            color=cp.ANTIGRAVITY_SOURCE_COLOR,
            fill_opacity=0.5,
            stroke_color=cp.ANTIGRAVITY_SOURCE_COLOR
        )

    def gravitational_push(self, light_ray_position):
        """
        Calculate the anti-gravitational push based on distance.
        This is the inverse of gravitational_pull — it pushes objects *away* instead of pulling them *toward*.
        """
        dx = light_ray_position[0] - self.position[0]
        dy = light_ray_position[1] - self.position[1]
        dz = light_ray_position[2] - self.position[2]
        distance = math.sqrt(dx**2 + dy**2 + dz**2)
        if distance == 0:
            return (0, 0, 0)  # Avoid division by zero

        strength = self.mass / distance**2
        direction = (dx / distance, dy / distance, dz / distance)
        push_vector = (strength * direction[0],
                       strength * direction[1],
                       strength * direction[2])
        return push_vector

    def set_position(self, position):
        self.position = position
        # Update the anti-gravity sphere’s position visually
        self.antigravity_sphere_obj.move_to(self.position)

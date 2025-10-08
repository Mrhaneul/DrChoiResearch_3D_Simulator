from manim import *
from control_panel import ControlPanel as cp
from light3d import Light3D as l3d
from gravity_source3d import GravitySource3D as gs3d
from antigravity_source3d import AntiGravitySource3D as as3d
import numpy as np

class TestLightScene(ThreeDScene):
    def construct(self):
        # Screen settings
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=0.2)
        self.camera.background_color = "BLACK"

    # Constants
        self.length, self.width, self.height = cp.LENGTH, cp.WIDTH, cp.HEIGHT

        axes = ThreeDAxes()

    # Create a 3D plane for better visualization
        plane = NumberPlane(x_range=[-100, 100], y_range=[-100, 100], background_line_style={
            "stroke_color": cp.PATH_COLOR,
            "stroke_width": cp.PATH_WIDTH,
        })
        self.add(axes, plane)
        
        # Sources
        gravity_sphere = gs3d(3000, [-3, 3, 0])
        gravity_sphere.set_position([-3, 3, 0])

        antigravity_sphere = as3d(3000, [3, 0, 0])
        antigravity_sphere.set_position([3, 0, 0])

        self.add(gravity_sphere, antigravity_sphere)

        # Light particle
        light_sphere = l3d.light_dot(self)
        light_sphere = Sphere(
            radius=cp.LIGHT_RADIUS, 
            color=cp.LIGHT_COLOR,
            fill_opacity=1,
            stroke_color=cp.LIGHT_COLOR,
            stroke_width = 3  # Increase outline thickness
            )
        # Position the light at the left side of the screen
        light_sphere.move_to([0, -5, 0])
        self.add(light_sphere)

        # Path trace (nice visual of the trajectory)
        trail = TracedPath(light_sphere.get_center, stroke_color=getattr(cp, "PATH_COLOR", BLUE), stroke_width=getattr(cp, "PATH_WIDTH", 2))
        self.add(trail)

        # Initialize velocity for the light sphere
        velocity = np.array([0.0, 0.0, 0.0], dtype=np.float64)
        force_scale = 0.01

        # Define update function for animation
        def update_sphere(mob, dt):
            nonlocal velocity  # Keep track of velocity across frames

            pos = np.array(mob.get_center(), dtype=np.float64)

            # Compute forces at current position
            gravity_force = np.array(gravity_sphere.gravitational_pull(mob.get_center()), dtype=np.float64)
            antigravity_force = np.array(antigravity_sphere.gravitational_push(mob.get_center()), dtype=np.float64)

            # Combine both forces
            acc = (gravity_force + antigravity_force) * force_scale

            # Update velocity
            velocity += acc * dt
            
            # Move the sphere based on velocity
            mob.shift(velocity * dt)

            # Light moves forward
            mob.shift(3 * UP * dt)

        # Add updater to the sphere
        light_sphere.add_updater(update_sphere)

        # Animate for a duration
        self.wait(20)

        # Remove the updater after animation is complete
        light_sphere.clear_updaters()
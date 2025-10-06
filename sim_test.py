from manim import *
from control_panel import ControlPanel as cp
from light3d import Light3D as l3d
from gravity_source3d import GravitySource3D as gs3d
import numpy as np

class TestScene(ThreeDScene):
    def construct(self):
        # Screen settings
        self.set_camera_orientation(phi=45 * DEGREES, theta=45 * DEGREES)
        self.camera.background_color = "BLACK"

    # Constants
        self.length, self.width, self.height = cp.LENGTH, cp.WIDTH, cp.HEIGHT

    # Create a 3D plane for better visualization
        plane = NumberPlane(x_range=[-5, 5], y_range=[-5, 5], background_line_style={
            "stroke_color": cp.PATH_COLOR,
            "stroke_width": cp.PATH_WIDTH,
        })
    
        #light_sphere = l3d.light_dot(self)
        light_sphere = Sphere(
            radius=cp.LIGHT_RADIUS, 
            color=cp.LIGHT_COLOR,
            fill_opacity=1,
            stroke_color=cp.LIGHT_COLOR,
            stroke_width = 3  # Increase outline thickness
            )
        # Position the light at the left side of the screen
        light_sphere.move_to([2, 3, 2])
        

        gravity_sphere = gs3d(3000, ORIGIN)
        gravity_sphere.set_position(ORIGIN)


        # Add elements to the screen
        self.add(plane, gravity_sphere)
        self.add(light_sphere)

        # Initialize velocity for the light sphere
        velocity = np.array([0.0, 0.0, 0.0], dtype=np.float64)

        # Define update function for animation
        def update_sphere(mob, dt):
            nonlocal velocity  # Keep track of velocity across frames
            
            # Calculate gravitational force
            force = gravity_sphere.gravitational_pull(mob.get_center())
            acceleration = np.array(force, dtype=np.float64) * 0.01

            # Update velocity based on force
            velocity += acceleration * dt * 0.1 # dt is the frame delta time
            
            # Move the sphere based on velocity
            mob.shift(velocity * dt)

            # Light moves forward
            mob.shift(0.5 * RIGHT * dt)

        # Add updater to the sphere
        light_sphere.add_updater(update_sphere)

        # Animate for a duration
        self.wait(35)

        # Remove the updater after animation is complete
        light_sphere.clear_updaters()
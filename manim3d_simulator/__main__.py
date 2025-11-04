from manim3d_simulator.src.gravity_source3d import GravitySource3D as gs3d
from manim3d_simulator.src.light3d import Light3D as l3d
from control_panel import ControlPanel as cp
from manim import *


class GravityLightScene(ThreeDScene):
    """def simulate_full_path(self, light, gravity_source, time_step):
        while not light.stopped:
            light.move_due_to_gravity(gravity_source, time_step)
            light.move_towards_direction(time_step)
            light.update_direction(gravity_source)
            if light.stopped:
                break"""

    def construct(self):
        # Screen settings
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)
        self.camera.background_color = "BLACK"

        # Creating a gravity source with mass 3000 at the center of the screen
        gravity_source = gs3d(mass = 3000, position = ORIGIN)

        # Creating a light object at an initial position
        light_source = l3d((cp.WIDTH // 4, cp.HEIGHT // 2 + 100, cp.LENGTH // 2), (1, 0, 0))

        #if cp.MODE == 2:
        #    light_source.path = self.simulate_full_path(light_source, gravity_source, cp.TIME_STEP)

        # Create a 3D plane for better visualization
        plane = NumberPlane(x_range=[-5, 5], y_range=[-5, 5], background_line_style={
            "stroke_color": cp.PATH_COLOR,
            "stroke_width": cp.PATH_WIDTH,
        })

        # Add elements to the screen
        self.add(plane, gravity_source, light_source)

         # Define light movement animation
        def update_light(light, dt):
            """Updates light's position per frame."""
            light.move_due_to_gravity(gravity_source, dt)
            light.move_towards_direction(dt)
            light.update_direction(gravity_source)
            light.move_to(light.position)  # Apply position change in Manim

        self.play(
            l3d.move_due_to_gravity(gravity_source, dt),
            l3d.move_towards_direction(dt),
            l3d.update_direction(gravity_source),
            l3d.move_to(light_source.position),
            run_time=5
        )

        # Attach the update function
        light_source.add_updater(update_light)

        # Run animation for a set duration
        self.wait(5)  # Adjust duration as needed

        # Remove updater after simulation
        light_source.clear_updaters()

        # Hold final frame
        self.wait(2)

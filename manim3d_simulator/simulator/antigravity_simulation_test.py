from manim import * 
from control_panel import ControlPanel as cp

class GravitySimulation(ThreeDScene):
    def construct(self):
        # Screen settings
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        self.camera.background_color = "BLACK"

        # Constants
        self.length, self.width, self.height = cp.LENGTH, cp.WIDTH, cp.HEIGHT

        # Graphical elements
        gravity_source = Sphere(
            radius=cp.GRAVITY_SOURCE_RADIUS, 
            color=cp.GRAVITY_SOURCE_COLOR,
            fill_opacity=0.5,
            stroke_color=cp.GRAVITY_SOURCE_COLOR
            )
        gravity_source.move_to(ORIGIN)  # Position the gravity source at the center of the screen

        light = Sphere(
            radius=cp.LIGHT_RADIUS, 
            color=cp.LIGHT_COLOR,
            fill_opacity=0.5,
            stroke_color=cp.LIGHT_COLOR
            )
        light.move_to(ORIGIN)  # Start at a 3D position # Position the light at the left side of the screen

        # Create a 3D plane for better visualization
        plane = NumberPlane(x_range=[-5, 5], y_range=[-5, 5], background_line_style={
            "stroke_color": cp.PATH_COLOR,
            "stroke_width": cp.PATH_WIDTH,
        })

        # Add elements to the screen
        self.add(plane, gravity_source, light)

        # Animation
        self.play(light.animate.move_to([3, 0, 2]), run_time=2)

        # Hold the final frame
        self.wait(3)


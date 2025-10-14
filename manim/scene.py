from manim import *
import IPython

class Simulation(ThreeDScene):
    def construct(self):

        # Set initial camera position
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # Allow mouse drag to rotate camera
        

        # Create 3D axes
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1]
        )

        cube = Cube(side_length=3, fill_opacity=1)

        self.add(cube, axes)

        # self.begin_ambient_camera_rotation(rate=0.3)
        self.begin_ambient_camera_rotation()
        self.wait(2)
        self.stop_ambient_camera_rotation()

        self.interactive_embed()

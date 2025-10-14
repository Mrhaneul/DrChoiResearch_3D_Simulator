from manim import ThreeDScene, ThreeDAxes, YELLOW, RED, WHITE, PI, DEGREES, Create, ParametricFunction
import numpy as np  # Explicitly import numpy

class test3D(ThreeDScene):
    def construct(self):

        axes = ThreeDAxes(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            z_range=[-6, 6, 1],
            x_length=8,
            y_length=6,
            z_length=6,
        )

        graph = ParametricFunction(
            lambda t: np.array([t, t**2, 0]),  
            t_range=[-2, 2],
            color=YELLOW
        )

        graph2 = ParametricFunction(
            lambda t: np.array([np.cos(t), np.sin(t), t]),
            t_range=[-2 * PI, 2 * PI],
            color=RED
        )

        self.add(axes, graph)
        self.wait()

        self.play(self.camera.animate.set_phi(60 * DEGREES))
        self.wait()
        self.play(self.camera.animate.set_theta(45 * DEGREES))
        self.wait()

        self.begin_ambient_camera_rotation(rate=PI/10, about=RIGHT)
        self.wait()
        self.play(Create(graph2))
        self.wait()
        self.stop_ambient_camera_rotation()

        self.wait()
        self.begin_ambient_camera_rotation(rate=PI/10, about=UP)
        self.wait(2)
        self.stop_ambient_camera_rotation()

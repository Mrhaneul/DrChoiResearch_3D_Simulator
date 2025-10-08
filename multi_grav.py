from manim import *
from control_panel import ControlPanel as cp
from light3d import Light3D as l3d
from gravity_source3d import GravitySource3D as gs3d
from antigravity_source3d import AntiGravitySource3D as as3d
import numpy as np

class TestMultiGrav(ThreeDScene):
    def construct(self):
        # Screen settings
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=0.2)
        self.camera.background_color = "BLACK"

    # Constants
        self.length, self.width, self.height = cp.LENGTH, cp.WIDTH, cp.HEIGHT

        axes = ThreeDAxes()

    # Create a 3D plane for better visualization
        plane = NumberPlane(
            x_range=[-20, 20, 1],   # third value = step
            y_range=[-12, 12, 1],
            faded_line_ratio=1,     # no extra faded lines
            background_line_style={"stroke_opacity": 0.5, "stroke_width": 1},
            axis_config={"stroke_color": WHITE, "stroke_width": 2},
        )
        self.add(axes, plane)
        
        # --- Multiple gravity sources ---
        # Define as (mass, position)
        g_src_specs = [
            (3000, [-12, 10, 0]),
            (3000, [-10, 8, 0]),
            (3000, [-8, 6, 0]),
            (3000, [-6, 8, 0]),
            (3000, [-4, 10, 0]),
            (3000, [-2, 6, 0]),
            (3000, [ 2, 6, 0]),
            (3000, [ 4, 10, 0]),
            (3000, [ 6, 8, 0]),
            (3000, [ 8, 6, 0]),
            (3000, [10, 8, 0]),
            (3000, [12, 10, 0]),
        ]
        g_sources = []
        for mass, pos in g_src_specs:
            s = gs3d(mass, pos)
            s.set_position(pos)
            g_sources.append(s)
        self.add(*g_sources)

        a_src_specs = [
            (3000, [-11, 9, 0]),
            (3000, [-9, 7, 0]),
            (3000, [-7, 5, 0]),
            (3000, [-5, 7, 0]),
            (3000, [-3, 9, 0]),
            (3000, [-1, 5, 0]),
            (3000, [ 1, 5, 0]),
            (3000, [ 3, 9, 0]),
            (3000, [ 5, 7, 0]),
            (3000, [ 7, 5, 0]),
            (3000, [ 9, 7, 0]),
            (3000, [11, 9, 0]),
        ]
        a_sources = []
        for mass, pos in a_src_specs:
            s = as3d(mass, pos)
            s.set_position(pos)
            a_sources.append(s)
        self.add(*a_sources)


        # Multiple light particles
        light_positions = [
            [ -20, -10, 0],
            [ -25, -10, 0],
            [-15, -10, 0],
            [-10, -10, 0],
            [ -5, -10, 0],
            [  0, -10, 0],
            [  5, -10, 0],
            [ 10, -10, 0],
            [ 15, -10, 0],
            [ 20, -10, 0],
            [ 25, -10, 0],
        ]

        lights = []
        for pos in light_positions:
            light_sphere = l3d.light_dot(self)
            light_sphere = Sphere(
                radius=cp.LIGHT_RADIUS,     
                color=cp.LIGHT_COLOR,
                fill_opacity=1,
                stroke_color=cp.LIGHT_COLOR,
                stroke_width = 3  # Increase outline thickness
            ).move_to(pos)
            self.add(light_sphere)

            # Path trace (nice visual of the trajectory)
            trail = TracedPath(
                light_sphere.get_center, 
                stroke_color=getattr(cp, "PATH_COLOR", BLUE), 
                stroke_width=getattr(cp, "PATH_WIDTH", 2))
            self.add(trail)
            
            # Make a per-light updater (unique velocity)
            def make_updater():
                velocity = np.zeros(3, dtype=np.float64)
                force_scale   = cp.FORCE_SCALE

                def update(mob: Mobject, dt: float):
                        nonlocal velocity
                        pos = np.array(mob.get_center(), dtype=np.float64)

                        total_g_force = np.zeros(3)
                        for src in g_sources:
                            total_g_force += np.array(src.gravitational_pull(tuple(pos)))

                        total_a_force = np.zeros(3)
                        for src in a_sources:
                            total_a_force += np.array(src.gravitational_push(tuple(pos)))

                        acc = (total_g_force + total_a_force) * force_scale

                        velocity += acc * dt

                        mob.shift(velocity * dt)
                        
                        # Light moves forward
                        mob.shift(6 * UP * dt)

                return update
            
            light_sphere.add_updater(make_updater())
            lights.append(light_sphere)

        self.wait(7)

        for light in lights:
            light.clear_updaters()
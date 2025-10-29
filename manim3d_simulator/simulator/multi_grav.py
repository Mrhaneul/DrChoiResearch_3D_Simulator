from manim import *
import os
import sys

# Ensure imports work when run from this subfolder
_pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../manim3d_simulator
_proj_root = os.path.dirname(_pkg_root)  # parent that contains 'manim3d_simulator'
for p in (_pkg_root, _proj_root):
    if p not in sys.path:
        sys.path.insert(0, p)

from control_panel import ControlPanel as cp
from manim3d_simulator.src.light3d import Light3D as l3d
from manim3d_simulator.src.gravity_source3d import GravitySource3D as gs3d
from manim3d_simulator.src.antigravity_source3d import AntiGravitySource3D as as3d
import numpy as np

class TestMultiGrav(ThreeDScene):
    def construct(self):
        # Screen settings
        self.set_camera_orientation(phi=45 * DEGREES, theta=-45 * DEGREES, zoom=0.2)
        self.camera.background_color = "BLACK"

    # Constants
        self.length, self.width, self.height = cp.LENGTH, cp.WIDTH, cp.HEIGHT

        axes = ThreeDAxes()

    # Create a 3D plane for better visualization
        plane = NumberPlane(
            x_range=[-30, 30, 1],   # third value = step
            y_range=[-30, 30, 1],
            faded_line_ratio=1,     # no extra faded lines
            background_line_style={"stroke_opacity": 0.5, "stroke_width": 1},
            axis_config={"stroke_color": WHITE, "stroke_width": 2},
        )
        self.add(axes, plane)
        
        # --- Multiple gravity sources ---
        # Define as (mass, position)
        g_src_specs = [
            (3000, [-19,  2, -14]),
            (3000, [ 16,  3,   9]),
            (3000, [-14,  5,   7]),
            (3000, [ 11,  6,  -8]),
            (3000, [ -9,  9,   4]),
            (3000, [  7, 11,  -3]),
            (3000, [ -5, 13,   2]),
            (3000, [  4, 15,  -2]),
            # (3000, [  2, 17,   1]),
            # (3000, [  0, 19,   0]),   # cone tip near Earth
        ]

        g_sources = []
        for mass, pos in g_src_specs:
            s = gs3d(mass, pos)
            s.set_position(pos)
            g_sources.append(s)
        self.add(*g_sources)

        a_src_specs = [
            (3000, [-18,  2,  13]),
            (3000, [ 15,  3, -10]),
            (3000, [-12,  5,  -6]),
            (3000, [ 10,  6,   5]),
            (3000, [ -8,  9,  -5]),
            (3000, [  6, 11,   3]),
            (3000, [ -4, 13,  -2]),
            (3000, [  3, 15,   2]),
            # (3000, [  1, 17,  -1]),
            # (3000, [  0, 19,   1]),   # close to cone tip
        ]

        a_sources = []
        for mass, pos in a_src_specs:
            s = as3d(mass, pos)
            s.set_position(pos)
            a_sources.append(s)
        self.add(*a_sources)
        

        # Create earth sphere for reference
        earth = Sphere(
            radius=cp.EARTH_RADIUS,
            color=cp.EARTH_COLOR,
            fill_opacity=0.5,
            stroke_color=cp.EARTH_COLOR,
            stroke_width = 2
        ).move_to([0, -25, 0])
        self.add(earth)


        # Multiple light particles
        light_positions = [
            # Left outer column
            [-14, -10, -12], [-14, -10,  -8], [-14, -10,  -4], [-14, -10,   0], [-14, -10,   4],
            
            # Mid-left
            [ -8, -10, -10], [ -8, -10,  -5], [ -8, -10,   0], [ -8, -10,   5], [ -8, -10,  10],
            
            # Center line
            [  0, -10, -12], [  0, -10,  -6], [  0, -10,   0], [  0, -10,   6], [  0, -10,  12],
            
            # Mid-right
            [  8, -10, -10], [  8, -10,  -5], [  8, -10,   0], [  8, -10,   5], [  8, -10,  10],
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

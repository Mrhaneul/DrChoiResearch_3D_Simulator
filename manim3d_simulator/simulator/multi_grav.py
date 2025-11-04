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
        # Avoid passing zoom to OpenGL camera (older versions lack set_zoom)
        self.set_camera_orientation(phi=90 * DEGREES, theta=90 * DEGREES)
        # Try to apply zoom in a renderer-agnostic way
        try:
            cam = getattr(self, "renderer").camera
            if hasattr(cam, "set_zoom"):
                cam.set_zoom(0.2)
            elif hasattr(cam, "zoom"):
                cam.zoom = 0.2
        except Exception:
            pass
        self.camera.background_color = "BLACK"

        # Constants
        self.length, self.width, self.height = cp.LENGTH, cp.WIDTH, cp.HEIGHT

        axes = ThreeDAxes()

        # 3D grid
        plane = NumberPlane(
            x_range=[-30, 30, 1],
            y_range=[-30, 30, 1],
            faded_line_ratio=1,
            background_line_style={"stroke_opacity": 0.5, "stroke_width": 1},
            axis_config={"stroke_color": WHITE, "stroke_width": 2},
        )
        self.add(axes, plane)

        # Gravity sources (x ↔ y swapped)
        g_src_specs = [
            # Layer 1 (lowest and widest base)
            (150, [-10, -5, -6]),   # G −X−Z
            (150, [ 10, -5,  6]),   # G +X+Z
            (150, [-10, -5,  6]),   # G −X+Z
            (150, [ 10, -5, -6]),   # G +X−Z

            # Layer 2 (wide base)
            (150, [-8, 0,  0]),     # G −X
            (150, [ 0, 0, -4]),     # G −Z
            (150, [ 8, 0,  0]),     # G +X
            (150, [ 0, 0,  4]),     # G +Z

            # Layer 3 (mid layer)
            (150, [-4, 6,  0]),     # G −X
            (150, [ 4, 6,  0]),     # G +X

            # Layer 4 (tip near center)
            # (150, [0, 13, 0]),      # G center
        ]


        g_sources = []
        for mass, pos in g_src_specs:
            s = gs3d(mass, pos)
            s.set_position(pos)
            g_sources.append(s)
        self.add(*g_sources)

        # Antigravity sources (x ↔ y swapped)
        a_src_specs = [
            # Layer 1 (lowest and widest base, interleaved)
            (150, [-6, -4, -4]),   # A −X−Z
            (150, [ 6, -4,  4]),   # A +X+Z
            (150, [-6, -4,  4]),   # A −X+Z
            (150, [ 6, -4, -4]),   # A +X−Z

            # Layer 2 (interleaved mid-low)
            (150, [-4, 2, -2]),    # A −X−Z
            (150, [ 4, 2,  2]),    # A +X+Z
            (150, [-4, 2,  2]),    # A −X+Z
            (150, [ 4, 2, -2]),    # A +X−Z

            # Layer 3 (mid)
            (150, [-2, 8,  0]),    # A −X
            (150, [ 2, 8,  0]),    # A +X

            # Layer 4 (tip)
            # (150, [0, 14, 0]),     # A near center
        ]

        a_sources = []
        for mass, pos in a_src_specs:
            s = as3d(mass, pos)
            s.set_position(pos)
            a_sources.append(s)
        self.add(*a_sources)

        # Earth sphere
        earth = Sphere(
            radius=cp.EARTH_RADIUS,
            color=cp.EARTH_COLOR,
            fill_opacity=0.5,
            stroke_color=cp.EARTH_COLOR,
            stroke_width=2
        ).move_to([0, 25, 0])  # swapped x/y
        # self.add(earth)

        # Lights (x ↔ y swapped)
        light_positions = [
            # z from -10 → 10, for each x step
            [-10, -10, -10], [-10, -10, -5], [-10, -10,  0], [-10, -10,  5], [-10, -10, 10],
            [ -5, -10, -10], [ -5, -10, -5], [ -5, -10,  0], [ -5, -10,  5], [ -5, -10, 10],
            [  0, -10, -10], [  0, -10, -5], [  0, -10,  0], [  0, -10,  5], [  0, -10, 10],
            [  5, -10, -10], [  5, -10, -5], [  5, -10,  0], [  5, -10,  5], [  5, -10, 10],
            [ 10, -10, -10], [ 10, -10, -5], [ 10, -10,  0], [ 10, -10,  5], [ 10, -10, 10],
        ]


        lights = []
        for pos in light_positions:
            light_sphere = l3d.light_dot(self) 
            light_sphere = Sphere(
                radius=cp.LIGHT_RADIUS,
                color=cp.LIGHT_COLOR,
                fill_opacity=1,
                stroke_color=cp.LIGHT_COLOR,
                stroke_width=3
            ).move_to(pos)
            self.add(light_sphere)

            trail = TracedPath(
                light_sphere.get_center,
                stroke_color=getattr(cp, "PATH_COLOR", BLUE),
                stroke_width=getattr(cp, "PATH_WIDTH", 2)
            )
            self.add(trail)

            def make_updater():
                velocity = np.zeros(3, dtype=np.float64)
                force_scale = cp.FORCE_SCALE

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
                    mob.shift(6 * UP * dt)  # swapped UP → RIGHT

                return update

            light_sphere.add_updater(make_updater())
            lights.append(light_sphere)

        self.wait(7)
        for light in lights:
            light.clear_updaters()

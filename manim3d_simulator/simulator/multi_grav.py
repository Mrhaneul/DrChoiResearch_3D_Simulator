from manim import *
import os
import sys

# Ensure imports work when run from this subfolder
_pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../manim3d_simulator
_proj_root = os.path.dirname(_pkg_root)  # parent that contains 'manim3d_simulator'
for p in (_pkg_root, _proj_root):
    if p not in sys.path:
        sys.path.insert(0, p)

from manim3d_simulator.control_panel import ControlPanel as cp
from manim3d_simulator.src.light3d import Light3D as l3d
from manim3d_simulator.src.gravity_source3d import GravitySource3D as gs3d
from manim3d_simulator.src.antigravity_source3d import AntiGravitySource3D as as3d
import numpy as np
import math


class TestMultiGrav(ThreeDScene):
    def construct(self):
        print("RENDERER =", type(self.renderer).__name__)

        try:
            print("OpenGL Info:", self.renderer.context.info)
        except Exception as e:
            print("No OpenGL context:", e)

        self.add(Sphere(radius=1, color=YELLOW).move_to(ORIGIN))



        # --- Camera setup ---
        self.set_camera_orientation(
            phi=90 * DEGREES,
            theta=90 * DEGREES,
        )

        try:
            cam = getattr(self, "renderer").camera

            # Pull camera "farther" by zooming out
            if hasattr(cam, "set_zoom"):
                cam.set_zoom(0.15)  # smaller than 0.2 → farther
            elif hasattr(cam, "zoom"):
                cam.zoom = 0.15

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

        # =========================================================
        #   CONE-SHAPED GRAVITY / ANTIGRAVITY SOURCES
        # =========================================================
        # Cone parameters
        LAYERS = 5           # base → tip
        Y_START = -6         # y of Layer 1 (base)
        Y_STEP = 5           # vertical spacing
        R_BASE = 22          # base radius (wider)
        R_TOP = 4            # tip radius (narrow)
        MASS = 150
        AXIS = "y"           # cone axis along Y

        def ring_points(radius: float, coord: float, n: int,
                        phase: float = 0.0, axis: str = "y"):
            """Evenly spaced points on a circle of given radius at a fixed axis coordinate."""
            pts = []
            for k in range(n):
                # Angle for this point
                a = phase + 2 * math.pi * k / n
                cx = radius * math.cos(a)
                cz = radius * math.sin(a)
                if axis == "y":
                    pts.append([cx, coord, cz])   # circle in XZ-plane at Y=coord
                elif axis == "x":
                    pts.append([coord, cx, cz])   # circle in YZ-plane at X=coord
                else:  # axis == "z"
                    pts.append([cx, cz, coord])   # circle in XY-plane at Z=coord
            return pts

        def lerp(a, b, t):
            return a + (b - a) * t

        # Build cone layers (gravity + antigravity interleaved)
        g_src_specs = []
        a_src_specs = []
        for i in range(LAYERS):
            t = i / (LAYERS - 1)            # 0 at base → 1 at tip
            y = Y_START + i * Y_STEP
            r = lerp(R_BASE, R_TOP, t)

            # Points per ring proportional to radius (even number)
            n = max(3, int(0.8 * r/2) * 2)

            # Gravity ring
            g_ring = ring_points(r, y, n, phase=0.0, axis=AXIS)
            g_src_specs.extend((MASS, p) for p in g_ring)

            # Antigravity ring: slightly smaller radius + phase offset to interleave
            a_ring = ring_points(0.85 * r, y, n, phase=math.pi / n, axis=AXIS)
            a_src_specs.extend((MASS, p) for p in a_ring)
        # =========================================================

        # Instantiate gravity sources
        g_sources = []
        for mass, pos in g_src_specs:
            s = gs3d(mass, pos)
            s.set_position(pos)
            g_sources.append(s)
        self.add(*g_sources)

        # Instantiate antigravity sources
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

        # =========================================================
        #   LIGHT CONFIGURATION
        # =========================================================
        N_X = 16              # number of launch positions along X
        N_Z = 16              # number of launch positions along Z
        X_MIN, X_MAX = -20, 20
        Z_MIN, Z_MAX = -20, 20
        LIGHT_Y = -30        # starting Y for all lights

        DRIFT_DIR = UP       # constant drift direction
        DRIFT_SPEED = 6.0    # constant drift speed
        EXTRA_VEL_SCALE = 1.0  # scale field-based acceleration if needed

        WALL_Y = 10          # <-- invisible wall at y = 10

        # Generate grid of light starting positions
        def linspace(a, b, n):
            if n == 1:
                # Single point case
                return [0.5 * (a + b)]
                # Otherwise, n >= 2
            step = (b - a) / (n - 1)
            # add n points from a to b inclusive
            return [a + i * step for i in range(n)]

        xs = linspace(X_MIN, X_MAX, N_X)
        zs = linspace(Z_MIN, Z_MAX, N_Z)

        light_positions = []
        for x in xs:
            for z in zs:
                light_positions.append([x, LIGHT_Y, z])

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

                    # --- Invisible wall at y = WALL_Y ---
                    if pos[1] >= WALL_Y:
                        # Snap to the wall and stop forever
                        pos[1] = WALL_Y
                        velocity[:] = 0
                        mob.move_to(pos)
                        return
                    # ------------------------------------

                    total_g_force = np.zeros(3)
                    for src in g_sources:
                        total_g_force += np.array(src.gravitational_pull(tuple(pos)))

                    total_a_force = np.zeros(3)
                    for src in a_sources:
                        total_a_force += np.array(src.gravitational_push(tuple(pos)))

                    acc = (total_g_force + total_a_force) * force_scale
                    velocity += acc * dt * EXTRA_VEL_SCALE
                    mob.shift(velocity * dt)

                    # Constant drift
                    mob.shift(DRIFT_SPEED * DRIFT_DIR * dt)

                return update

            light_sphere.add_updater(make_updater())
            lights.append(light_sphere)

        self.wait(20)
        for light in lights:
            light.clear_updaters()

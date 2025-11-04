from manim import *
import os
import sys
import numpy as np

# Ensure imports work when running from this subfolder
_pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../manim3d_simulator
_proj_root = os.path.dirname(_pkg_root)  # parent that contains 'manim3d_simulator'
for p in (_pkg_root, _proj_root):
    if p not in sys.path:
        sys.path.insert(0, p)

from control_panel import ControlPanel as cp
from manim3d_simulator.src.gravity_source3d import GravitySource3D as gs3d
from manim3d_simulator.src.antigravity_source3d import AntiGravitySource3D as as3d


class MultiGravQuick(ThreeDScene):
    """Lightweight version of the multi-source scene for faster iteration.

    - Fewer sources and lights
    - Shorter runtime
    - Minimal traces
    """

    def construct(self):
        # Camera and background
        # First-person view
        # self.set_camera_orientation(phi=-90 * DEGREES, theta=-90 * DEGREES)
        self.set_camera_orientation(phi=45 * DEGREES, theta=-60 * DEGREES)
        # Apply zoom safely across renderers
        try:
            cam = getattr(self, "renderer").camera
            if hasattr(cam, "set_zoom"):
                cam.set_zoom(0.25)
            elif hasattr(cam, "zoom"):
                cam.zoom = 0.25
        except Exception:
            pass
        self.camera.background_color = BLACK

        # Plane for reference
        plane = NumberPlane(
            x_range=[-30, 30, 3],
            y_range=[-30, 30, 1],
            faded_line_ratio=1,
            background_line_style={"stroke_opacity": 0.35, "stroke_width": 1},
            axis_config={"stroke_color": WHITE, "stroke_width": 2},
        )
        axes = ThreeDAxes()
        self.add(axes, plane)

        # Helper to swap x and y of a 3D coordinate
        def swap_xy(p):
            return [p[1], p[0], p[2]]

        # A couple of gravity/anti-gravity sources only
        g_specs = [
            (700, [-6, 2, -4]),
            (700, [6, 3, 4]),
        ]
        a_specs = [
            # (700, [-5, 2, 5]),
            # (700, [5, 3, -5]),
        ]

        g_sources = []
        for mass, pos in g_specs:
            pos_swapped = swap_xy(pos)
            s = gs3d(mass, pos_swapped)
            s.set_position(pos_swapped)
            g_sources.append(s)
        a_sources = []
        for mass, pos in a_specs:
            pos_swapped = swap_xy(pos)
            s = as3d(mass, pos_swapped)
            s.set_position(pos_swapped)
            a_sources.append(s)
        self.add(*g_sources, *a_sources)
        
        earth = Sphere(
            radius=1.5,
            color=BLUE,
            fill_opacity=0.25,
            stroke_color=BLUE
        ).move_to([-10, 0, 0])
        self.add(earth)

        # A handful of light particles
        light_positions = [
            [-8, 10, -6],
            [0, 10, 0],
            [8, 10, 6],
            [-8, 10, 6],
            [8, 10, -6],
        ]

        lights = []
        for pos in light_positions:
            light = Sphere(
                radius=cp.LIGHT_RADIUS,
                color=cp.LIGHT_COLOR,
                fill_opacity=1.0,
                stroke_color=cp.LIGHT_COLOR,
                stroke_width=2,
            ).move_to([pos[1], pos[0], pos[2]])
            self.add(light)

            # Subtle trace to visualize path, but lighter-weight
            trail = TracedPath(
                light.get_center,
                stroke_color=getattr(cp, "PATH_COLOR", BLUE),
                stroke_width=max(1, int(getattr(cp, "PATH_WIDTH", 2) * 0.6)),
            )
            self.add(trail)

            def make_updater():
                velocity = np.zeros(3, dtype=np.float64)
                force_scale = getattr(cp, "FORCE_SCALE", 0.1)
                g_visual_radius = float(getattr(cp, "GRAVITY_SOURCE_RADIUS", 1.0))
                ramp_width = float(getattr(cp, "GRAVITY_RAMP_WIDTH", 0.5 * g_visual_radius))

                def update(mob: Mobject, dt: float):
                    nonlocal velocity
                    pos = np.array(mob.get_center(), dtype=np.float64)

                    # Accumulate forces
                    total_force = np.zeros(3, dtype=np.float64)
                    min_d_to_g = float("inf")
                    for src in g_sources:
                        # Smooth ramp from 0 at R to full by R + ramp_width
                        src_pos = np.array(src.position, dtype=np.float64)
                        delta = src_pos - pos
                        d = np.linalg.norm(delta)
                        min_d_to_g = min(min_d_to_g, d)
                        if d < 1e-8:
                            continue
                        direction = delta / d
                        if d <= g_visual_radius:
                            w = 0.0
                            d_eff = g_visual_radius
                        elif d <= g_visual_radius + max(1e-8, ramp_width):
                            t = (d - g_visual_radius) / max(1e-8, ramp_width)
                            w = t * t * (3 - 2 * t)  # smoothstep
                            d_eff = d
                        else:
                            w = 1.0
                            d_eff = d
                        strength = w * float(src.mass) / (d_eff ** 2)
                        total_force += strength * direction
                    for src in a_sources:
                        total_force += np.array(src.gravitational_push(tuple(pos)))

                    # Integrate
                    acc = total_force * force_scale
                    velocity += acc * dt
                    mob.shift(velocity * dt)
                    # Bias motion toward the earth, but not while intersecting a gravity sphere
                    to_earth = np.array(earth.get_center(), dtype=np.float64) - pos
                    dist = np.linalg.norm(to_earth)
                    near_g = min_d_to_g <= (g_visual_radius + ramp_width + 1e-6)
                    if dist > 1e-8 and not near_g:
                        dir_to_earth = to_earth / dist
                        base_speed = float(getattr(cp, "LIGHT_BASE_SPEED", 4.0))
                        mob.shift(dir_to_earth * base_speed * dt)

                return update

            light.add_updater(make_updater())
            lights.append(light)

        # Short runtime for quick feedback
        self.wait(6)

        for light in lights:
            light.clear_updaters()

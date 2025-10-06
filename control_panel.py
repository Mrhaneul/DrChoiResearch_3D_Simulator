from manim import *

class ControlPanel:
    # Constants
    MODE = 2 # 1 for real-time, 2 for full path
    LENGTH, WIDTH, HEIGHT = 800, 800, 600
    BACKGROUND_COLOR = (0, 0, 0)
    GRAVITY_SOURCE_COLOR = (255, 0, 0)
    ANTIGRAVITY_SOURCE_COLOR = (0, 0, 255)
    GRAVITY_SOURCE_MASS = 1000
    LIGHT_COLOR = (0, 255, 0)
    TEXT_COLOR = (255, 255, 255)
    GRAVITY_SOURCE_RADIUS = 0.4
    LIGHT_RADIUS = 0.1
    TIME_STEP = 0.1
    PATH_COLOR = BLUE
    PATH_WIDTH = 2
    MAX_FRAMES = 2000  # Maximum number of frames for the real-time mode
    STOP_DISTANCE_THRESHOLD = 3 # Threshold distance to stop the light

    def construct(self):
        # Screen settings
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        self.camera.background_color = "BLACK"

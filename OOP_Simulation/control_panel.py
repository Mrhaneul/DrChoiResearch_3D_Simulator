import pygame
import pygame_gui







class ControlPanel:
    # Constants
    MODE = 1 # 1 for real-time, 2 for full path
    WIDTH, HEIGHT = 800, 600
    BACKGROUND_COLOR = (0, 0, 0)
    GRAVITY_SOURCE_COLOR = (255, 0, 0)
    GRAVITY_SOURCE_MASS = 1000
    LIGHT_COLOR = (0, 255, 0)
    TEXT_COLOR = (255, 255, 255)
    GRAVITY_SOURCE_RADIUS = 10
    LIGHT_RADIUS = 10
    TIME_STEP = 0.1
    PATH_COLOR = (0, 255, 255)
    PATH_WIDTH = 2
    MAX_FRAMES = 2000  # Maximum number of frames for the real-time mode
    STOP_DISTANCE_THRESHOLD = 3 # Threshold distance to stop the light



    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Gravity Simulation")
        self.screen = pygame.display.set_mode((ControlPanel.WIDTH, ControlPanel.HEIGHT))
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((ControlPanel.WIDTH, ControlPanel.HEIGHT))
        self.font = pygame.font.Font(None, 36)

        # GUI elements
        self.width_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 10), (100, 30)), manager=self.manager)
        self.height_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 50), (100, 30)), manager=self.manager)
        self.max_frames_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 90), (100, 30)), manager=self.manager)
        self.gravity_source_mass_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 110), (100, 30)), manager=self.manager)
        self.time_step_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 130), (100, 30)), manager=self.manager)
        self.gravity_source_radius_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 170), (100, 30)), manager=self.manager)
        self.light_radius_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 210), (100, 30)), manager=self.manager)
        self.path_width_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 250), (100, 30)), manager=self.manager)
        self.mode_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 290), (100, 30)), manager=self.manager)
        self.update_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 330), (100, 30)), text='Update', manager=self.manager)

    def run(self):
        running = True
        frame_count = 0

        while running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.update_button:
                            self.update_parameters()


    def update_parameters(self):
        global WIDTH, HEIGHT, MAX_FRAMES, TIME_STEP, GRAVITY_SOURCE_RADIUS, LIGHT_RADIUS, PATH_WIDTH, MODE, GRAVITY_SOURCE_MASS
        WIDTH = int(self.width_entry.get_text())
        HEIGHT = int(self.height_entry.get_text())
        MAX_FRAMES = int(self.max_frames_entry.get_text())
        TIME_STEP = float(self.time_step_entry.get_text())
        GRAVITY_SOURCE_RADIUS = int(self.gravity_source_radius_entry.get_text())
        GRAVITY_SOURCE_MASS = int(self.gravity_source_mass_entry.get_text())
        LIGHT_RADIUS = int(self.light_radius_entry.get_text())
        PATH_WIDTH = int(self.path_width_entry.get_text())
        MODE = int(self.mode_entry.get_text())


if __name__ == "__main__":
    cp = ControlPanel()
    cp.run()
    print(WIDTH, HEIGHT, MAX_FRAMES, TIME_STEP, GRAVITY_SOURCE_RADIUS, LIGHT_RADIUS, PATH_WIDTH, MODE, GRAVITY_SOURCE_MASS)



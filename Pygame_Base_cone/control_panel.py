import math
import pygame
from parameters import *
import pygame_gui


# # Setting up the GUI manager
# manager = pygame_gui.UIManager((WIDTH + CONTROL_PANEL_WIDTH, HEIGHT))

# # Creating a slider for adjusting the gravity source mass
# gravity_mass_slider = pygame_gui.elements.UIHorizontalSlider(
#     relative_rect=pygame.Rect((WIDTH + 20, 20), (CONTROL_PANEL_WIDTH - 40, 30)),
#     start_value=1000,
#     value_range=(100, 5000),
#     manager=manager
# )
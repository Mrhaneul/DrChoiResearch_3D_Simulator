from light import Light
import pygame
from parameters import *
import math
import numpy as np

def polar_to_cartesian(r, theta):
    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    return (x, y)

class LightScatter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lights = {}
        for i in THETA:
            self.lights[i] = Light((self.x, self.y), polar_to_cartesian(R, i))

    def update(self, gravity_source, time_step):
        for light in self.lights.values():
            if not light.stopped:
                light.move_due_to_gravity(gravity_source, time_step)
                light.move_towards_direction(time_step)
                light.update_direction(gravity_source)
        
    def draw(self, screen, transform, zoom, font, frame):
        for light in self.lights.values():
            # Draw the light
            pygame.draw.circle(screen, LIGHT_COLOR, transform((int(light.get_position()[0]), int(light.get_position()[1]))), int(LIGHT_RADIUS * zoom))

            # Draw the path of the light
            if len(light.path) > 1:
                transformed_path = [transform(point) for point in light.path]
                pygame.draw.lines(screen, PATH_COLOR, False, transformed_path, max(1, int(PATH_WIDTH * zoom)))

    def draw_text(self, screen, font, frame):
        # Prepare textual information
        text_surface = font.render(f"Light Position: {frame}", True, TEXT_COLOR)
        # Blit the text onto the screen
        screen.blit(text_surface, (10, 30))

import pygame
import sys

# Initialize Pygame
pygame.init()

# Window configuration
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Draw a Line")

# Coordinates of the line
start_x, start_y = 100, 100
end_x, end_y = 700, 500
line_thickness = 5

# Variables to track dragging state
dragging_start = False
dragging_end = False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Check if the click is near the start point
            if (start_x - 10 <= mouse_x <= start_x + 10) and (start_y - 10 <= mouse_y <= start_y + 10):
                dragging_start = True
            # Check if the click is near the end point
            elif (end_x - 10 <= mouse_x <= end_x + 10) and (end_y - 10 <= mouse_y <= end_y + 10):
                dragging_end = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_start = False
            dragging_end = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging_start:
                start_x, start_y = event.pos
            elif dragging_end:
                end_x, end_y = event.pos

    # Fill the window with a black color
    window.fill((0, 0, 0))

    # Draw the line
    pygame.draw.line(window, (255, 255, 255), (start_x, start_y), (end_x, end_y), line_thickness)

    # Draw circles at the end points for easier dragging
    pygame.draw.circle(window, (255, 0, 0), (start_x, start_y), 10)
    pygame.draw.circle(window, (255, 0, 0), (end_x, end_y), 10)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()


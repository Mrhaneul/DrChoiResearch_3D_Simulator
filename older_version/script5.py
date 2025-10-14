import pygame
import sys
import math
import pygame_gui

# Initialize Pygame
pygame.init()

# Window configuration
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Light Simulation")

# Pygame GUI manager
manager = pygame_gui.UIManager((width, height))

# Create the slider
slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((50, 550), (200, 30)),
    start_value=100,
    value_range=(0, 360),
    manager=manager
)


# Coordinates of the light source and the gravity source
START_LIGHT_SOURCE_X, START_LIGHT_SOURCE_Y = 500, 100
GRAVITY_SOURCE_X, GRAVITY_SOURCE_Y = 500, 300
end_x, end_y = 500, 500
line_thickness = 5


# Variables to track dragging state
dragging_start = False
dragging_control = False
dragging_end = False

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    time_delta = clock.tick(60) / 1000.0
    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Check if the click is near the start point
            if (START_LIGHT_SOURCE_X - 10 <= mouse_x <= START_LIGHT_SOURCE_X + 10) and (START_LIGHT_SOURCE_Y - 10 <= mouse_y <= START_LIGHT_SOURCE_Y + 10):
                dragging_start = True
            # Check if the click is near the control point
            elif (GRAVITY_SOURCE_X - 10 <= mouse_x <= GRAVITY_SOURCE_X + 10) and (GRAVITY_SOURCE_Y - 10 <= mouse_y <= GRAVITY_SOURCE_Y + 10):
                dragging_control = True
            # Check if the click is near the end point
            elif (end_x - 10 <= mouse_x <= end_x + 10) and (end_y - 10 <= mouse_y <= end_y + 10):
                dragging_end = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_start = False
            dragging_control = False
            dragging_end = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging_start:
                START_LIGHT_SOURCE_X, START_LIGHT_SOURCE_Y = event.pos
            elif dragging_control:
                GRAVITY_SOURCE_X, GRAVITY_SOURCE_Y = event.pos
            elif dragging_end:
                end_x, end_y = event.pos

        manager.process_events(event)

    # Update the distance between light ray and gravity source from the slider

    # Fill the window with a black color
    window.fill((0, 0, 0))

    # perpendicular line function
    def perpend_line_y_val(x_init, y_init, x_fin, y_fin, x_val):
        try:
            # first find the slope
            slope = (y_fin - y_init) / (x_fin - x_init)
            # inverse of the original slope to get the perpendicular line
            in_slope = -1 * 1 / slope
        except ZeroDivisionError:
            in_slope = 0
        # find the intercept
        intercept = y_fin - in_slope * x_fin
        return in_slope * x_val + intercept

    # Draw the perpendicular lines from the light source to the gravity source
    left_perpend_line_y_val = perpend_line_y_val(START_LIGHT_SOURCE_X, START_LIGHT_SOURCE_Y, GRAVITY_SOURCE_X, GRAVITY_SOURCE_Y, 0)
    right_perpend_line_y_val = perpend_line_y_val(START_LIGHT_SOURCE_X, START_LIGHT_SOURCE_Y, GRAVITY_SOURCE_X, GRAVITY_SOURCE_Y, 1000)
    left_perpend_vector = pygame.Vector2(0, left_perpend_line_y_val)
    right_perpend_vector = pygame.Vector2(1000, right_perpend_line_y_val)
    pygame.draw.line(window, (0, 0, 255), left_perpend_vector, (GRAVITY_SOURCE_X, GRAVITY_SOURCE_Y), line_thickness)
    pygame.draw.line(window, (0, 0, 255), right_perpend_vector, (GRAVITY_SOURCE_X, GRAVITY_SOURCE_Y), line_thickness)

    # Draw straight line that passes through gravity source from the light source
    pygame.draw.line(window, (255, 0, 0), (START_LIGHT_SOURCE_X, START_LIGHT_SOURCE_Y), (GRAVITY_SOURCE_X, GRAVITY_SOURCE_Y), 2)
    pygame.draw.line(window, (255, 0, 0), (GRAVITY_SOURCE_X, GRAVITY_SOURCE_Y), (end_x, end_y), 2)
    angle = 0
    light_source = pygame.Vector2(START_LIGHT_SOURCE_X, START_LIGHT_SOURCE_Y)
    gravity_source = pygame.Vector2(GRAVITY_SOURCE_X, GRAVITY_SOURCE_Y)
    try:
        x = light_source.x - gravity_source.x
        y = light_source.y - gravity_source.y
        angle = math.atan(y / x) * 180 / math.pi
        
    except ZeroDivisionError:
        angle = 0

    print(angle)
    
    perpendicular_angle = angle + 90


    #DISTANCE_BETWEEN_LIGHT_RAY_AND_GRAVITY_SOURCE is set by a slider variable
    DISTANCE_BETWEEN_LIGHT_RAY_AND_GRAVITY_SOURCE = slider.get_current_value()
######################################################################################################################################################
    # Draw the light ray that is perpendicular to the line connecting the light source and the gravity source
    light_ray_end_x = GRAVITY_SOURCE_X + math.cos(math.radians(perpendicular_angle)) * DISTANCE_BETWEEN_LIGHT_RAY_AND_GRAVITY_SOURCE
    light_ray_end_y = GRAVITY_SOURCE_Y + math.sin(math.radians(perpendicular_angle)) * DISTANCE_BETWEEN_LIGHT_RAY_AND_GRAVITY_SOURCE
    light_ray_end_position = pygame.Vector2(light_ray_end_x, light_ray_end_y)
    pygame.draw.line(window, (255, 255, 255), (START_LIGHT_SOURCE_X, START_LIGHT_SOURCE_Y), light_ray_end_position, 2)

    # Draw another light ray that is perpendicular to the line connecting the light source and the gravity source
    light_ray_end_x_counter = GRAVITY_SOURCE_X - math.cos(math.radians(perpendicular_angle)) * DISTANCE_BETWEEN_LIGHT_RAY_AND_GRAVITY_SOURCE
    light_ray_end_y_counter = GRAVITY_SOURCE_Y - math.sin(math.radians(perpendicular_angle)) * DISTANCE_BETWEEN_LIGHT_RAY_AND_GRAVITY_SOURCE
    light_ray_end_position_counter = pygame.Vector2(light_ray_end_x_counter, light_ray_end_y_counter)
    pygame.draw.line(window, (255, 255, 255), (START_LIGHT_SOURCE_X, START_LIGHT_SOURCE_Y), light_ray_end_position_counter, 2)

######################################################################################################################################################




######################################################################################################################################################
    # Draw the light ray that is perpendicular to the line connecting the light source and the gravity source
    light_ray_end_x_finish = light_ray_end_position.x - math.cos(math.radians(perpendicular_angle)) * DISTANCE_BETWEEN_LIGHT_RAY_AND_GRAVITY_SOURCE
    light_ray_end_y_finish = light_ray_end_position.y + math.sin(math.radians(perpendicular_angle + 90)) * DISTANCE_BETWEEN_LIGHT_RAY_AND_GRAVITY_SOURCE
    light_ray_end_position_finish = pygame.Vector2(light_ray_end_x_finish, light_ray_end_y_finish)
    pygame.draw.line(window, (255, 255, 255), light_ray_end_position, light_ray_end_position_finish, 2)

    # Draw another light ray that is perpendicular to the line connecting the light source and the gravity source
    light_ray_end_x_finish_counter = light_ray_end_position.x - math.cos(math.radians(perpendicular_angle)) * DISTANCE_BETWEEN_LIGHT_RAY_AND_GRAVITY_SOURCE
    light_ray_end_y_finish_counter = light_ray_end_position.y + math.sin(math.radians(perpendicular_angle + 90)) * DISTANCE_BETWEEN_LIGHT_RAY_AND_GRAVITY_SOURCE
    light_ray_end_position_finish_counter = pygame.Vector2(light_ray_end_x_finish_counter, light_ray_end_y_finish_counter)
    pygame.draw.line(window, (255, 255, 255), (light_ray_end_position_counter), light_ray_end_position_finish_counter, 2)

######################################################################################################################################################

    # Draw circles at the end points and control point for easier dragging
    pygame.draw.circle(window, (255, 0, 0), (START_LIGHT_SOURCE_X, START_LIGHT_SOURCE_Y), 10)
    pygame.draw.circle(window, (0, 255, 0), (GRAVITY_SOURCE_X, GRAVITY_SOURCE_Y), 10)
    pygame.draw.circle(window, (255, 0, 0), (end_x, end_y), 10)


    # Update and draw the GUI elements
    manager.update(time_delta)
    manager.draw_ui(window)
    

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

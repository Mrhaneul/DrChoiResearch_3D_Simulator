import pygame
import sys
import math


# Initialize Pygame
pygame.init()

# Window configuration
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Light Simulation")

# Coordinates of the light source and the gravity source
START_LIGHT_SOURCE_X, START_LIGHT_SOURCE_Y = 500, 100
GRAVITY_SOURCE_X, GRAVITY_SOURCE_Y = 500, 300
end_x, end_y = 500, 500
line_thickness = 5
DISTANCE_BETWEEN_LIGHT_RAY_AND_GRAVITY_SOURCE = 100

# Variables to track dragging state
dragging_start = False
dragging_control = False
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

    # Fill the window with a black color
    window.fill((0, 0, 0))






    # perpendicular line function
    def perpend_line_y_val(x_init, y_init, x_fin, y_fin, x_val):
        x = 0
        y = 0
        angle = 0
        try:
            #first find the slope
            slope = (y_fin - y_init) / (x_fin - x_init)
            #inverse of the original slope to get the perpendicular line
            in_slope = -1 * 1 / slope
            x = x_init - x_fin
            y = y_init - y_fin

            angle = math.atan(y/x) * 180 / math.pi
            print("Angle: ", angle)

        except:
            in_slope = 0
        #find the intercept
        intercept = y_fin - in_slope * x_fin
        #final formula
        
        if(angle > 90):
            in_slope = -1 * in_slope
        return in_slope * x_val + intercept
    


    # check the distance between the light ray and the gravity source
    def distance_between_light_ray_and_gravity_source(x, y, x2, y2):
        return ((x - x2) ** 2 + (y - y2) ** 2) ** 0.5

    # Draw the perpendicular lines from the light source to the gravity source
    # left_perpend_line_y_val = perpend_line_y_val(START_LIGHT_SOURCE_X, START_LIGHT_SOURCE_Y, GRAVITY_SOURCE_X, GRAVITY_SOURCE_Y, 0)
    right_perpend_line_y_val = perpend_line_y_val(START_LIGHT_SOURCE_X, START_LIGHT_SOURCE_Y, GRAVITY_SOURCE_X, GRAVITY_SOURCE_Y, 1000)
    # pygame.draw.line(window, (0, 0, 255), (0, left_perpend_line_y_val), (GRAVITY_SOURCE_X, GRAVITY_SOURCE_Y), line_thickness)
    pygame.draw.line(window, (0, 0, 255), (1000, right_perpend_line_y_val), (GRAVITY_SOURCE_X, GRAVITY_SOURCE_Y), line_thickness)



############################################################################################################

    # Draw the light emitted from the light source
    def draw_light_ray(light_source_x, light_source_y, gravity_source_x, gravity_source_y, desired_distance_from_gravity_source):
        correct_x = 0
        correct_y = 0
        for i in range(1000000):
            trial_y_val = perpend_line_y_val(light_source_x, light_source_y, gravity_source_x, gravity_source_y, light_source_x+i)
            
            dist = distance_between_light_ray_and_gravity_source(gravity_source_x, gravity_source_y, light_source_x+i, trial_y_val)
            
            calc = desired_distance_from_gravity_source - dist
            
            if (calc < 0.00000001):
                print("Trial Y Val:", trial_y_val)
                print("Light source x + i: ", light_source_x+i)
                print("Distance: ", dist)
                print("difference: ", calc)
                correct_x = light_source_x + i
                correct_y = trial_y_val
                break


        # draw the line that represent light
        pygame.draw.line(window, (255, 255, 255), (light_source_x, light_source_y), (correct_x, correct_y), line_thickness)

    draw_light_ray(START_LIGHT_SOURCE_X, START_LIGHT_SOURCE_Y, GRAVITY_SOURCE_X, GRAVITY_SOURCE_Y, DISTANCE_BETWEEN_LIGHT_RAY_AND_GRAVITY_SOURCE)
   

############################################################################################################



    # #draw straight line that passes through gravity source from the light source
    pygame.draw.line(window, (255, 0, 0), (START_LIGHT_SOURCE_X, START_LIGHT_SOURCE_Y), (GRAVITY_SOURCE_X, GRAVITY_SOURCE_Y), 2)
    pygame.draw.line(window, (255, 0, 0,), (GRAVITY_SOURCE_X, GRAVITY_SOURCE_Y), (end_x, end_y), 2)

    # Draw circles at the end points and control point for easier dragging
    pygame.draw.circle(window, (255, 0, 0), (START_LIGHT_SOURCE_X, START_LIGHT_SOURCE_Y), 10)
    pygame.draw.circle(window, (0, 255, 0), (GRAVITY_SOURCE_X, GRAVITY_SOURCE_Y), 10)
    pygame.draw.circle(window, (255, 0, 0), (end_x, end_y), 10)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()


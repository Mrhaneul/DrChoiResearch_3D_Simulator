from gravity_source import GravitySource as gs
from light import Light
import pygame
from control_panel import *
from light_scatter import LightScatter
from anti_gravity_source import AntiGravitySource as ags
import numpy as np

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gravity Simulation")

    font = pygame.font.Font(None, 12)

    gravity_positions = np.arange(0, 950, 100)
    anti_gravity_positions = np.arange(50, 900, 100)

    row1 = np.array([(gs(MASS, (g_pos, 300)), ags(MASS, (ag_pos, 300))) 
                     for g_pos, ag_pos in zip(gravity_positions, anti_gravity_positions)])
    row2 = np.array([(gs(MASS, (g_pos, 350)), ags(MASS, (ag_pos, 350)))
                     for g_pos, ag_pos in zip(anti_gravity_positions, gravity_positions)])
    row3 = np.array([(gs(MASS, (g_pos, 400 )), ags(MASS, (ag_pos, 400)))
                        for g_pos, ag_pos in zip(gravity_positions, anti_gravity_positions)])
    # row4 = np.array([(gs(MASS, (g_pos, 450)), ags(MASS, (ag_pos, 450)))
    #                     for g_pos, ag_pos in zip(anti_gravity_positions, gravity_positions)])
    
    

    combined_sources = np.concatenate((row1, row2, row3))
    
    # Creating a light object at an initial position
    light_scatter1 = LightScatter(50, 100)
    light_scatter2 = LightScatter(150, 100)
    light_scatter3 = LightScatter(250, 100)
    light_scatter4 = LightScatter(350, 100)
    light_scatter5 = LightScatter(450, 100)
    light_scatter6 = LightScatter(550, 100)
    light_scatter7 = LightScatter(650, 100)
    light_scatter8 = LightScatter(750, 100)



    running = True
    clock = pygame.time.Clock()

    frame_count = 0

    # Pan and zoom variables
    offset_x, offset_y = 0, 0
    zoom = 1.0

    # Apply zoom and pan transformations
    def transform(point):
        return (int((point[0] + offset_x) * zoom), int((point[1] + offset_y) * zoom))

    is_dragging = False
    last_mouse_pos = (0, 0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # Right mouse button for panning
                    last_mouse_pos = event.pos
                elif event.button == 4:  # Mouse wheel up for zoom in
                    zoom *= 1.1
                elif event.button == 5:  # Mouse wheel down for zoom out
                    zoom /= 1.1
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if is_dragging:
                    return
                elif pygame.mouse.get_pressed()[2]:  # Right mouse button held for panning
                    mouse_x, mouse_y = event.pos
                    dx = (mouse_x - last_mouse_pos[0]) / zoom
                    dy = (mouse_y - last_mouse_pos[1]) / zoom
                    offset_x += dx
                    offset_y += dy
                    last_mouse_pos = (mouse_x, mouse_y)

        # Update light position based on gravitational pull if in real-time mode
        if MODE == 1 and frame_count < MAX_FRAMES:
            # Update light position
            for gravity_source, anti_gravity_source in combined_sources:
                light_scatter1.update(gravity_source, TIME_STEP)
                light_scatter1.update(anti_gravity_source, TIME_STEP)
                light_scatter2.update(gravity_source, TIME_STEP)
                light_scatter2.update(anti_gravity_source, TIME_STEP)
                light_scatter3.update(gravity_source, TIME_STEP)
                light_scatter3.update(anti_gravity_source, TIME_STEP)
                light_scatter4.update(gravity_source, TIME_STEP)
                light_scatter4.update(anti_gravity_source, TIME_STEP)
                light_scatter5.update(gravity_source, TIME_STEP)
                light_scatter5.update(anti_gravity_source, TIME_STEP)
                light_scatter6.update(gravity_source, TIME_STEP)
                light_scatter6.update(anti_gravity_source, TIME_STEP)
                light_scatter7.update(gravity_source, TIME_STEP)
                light_scatter7.update(anti_gravity_source, TIME_STEP)
                light_scatter8.update(gravity_source, TIME_STEP)
                light_scatter8.update(anti_gravity_source, TIME_STEP)

                



            frame_count += 1

        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Draw gravity source
        for gravity_source, anti_gravity_source in combined_sources:
            pygame.draw.circle(screen, GRAVITY_SOURCE_COLOR, transform(gravity_source.position), int(GRAVITY_SOURCE_RADIUS * zoom))
            pygame.draw.circle(screen, ANTI_GRAVITY_SOURCE_COLOR, transform(anti_gravity_source.position), int(GRAVITY_SOURCE_RADIUS * zoom))
           
        # Draw light
        light_scatter1.draw(screen, transform, zoom, font, frame_count)
        light_scatter1.draw_text(screen, font, frame_count)
        light_scatter2.draw(screen, transform, zoom, font, frame_count)
        light_scatter2.draw_text(screen, font, frame_count)
        light_scatter3.draw(screen, transform, zoom, font, frame_count)
        light_scatter3.draw_text(screen, font, frame_count)
        light_scatter4.draw(screen, transform, zoom, font, frame_count)
        light_scatter4.draw_text(screen, font, frame_count)
        light_scatter5.draw(screen, transform, zoom, font, frame_count)
        light_scatter5.draw_text(screen, font, frame_count)
        light_scatter6.draw(screen, transform, zoom, font, frame_count)
        light_scatter6.draw_text(screen, font, frame_count)
        light_scatter7.draw(screen, transform, zoom, font, frame_count)
        light_scatter7.draw_text(screen, font, frame_count)
        light_scatter8.draw(screen, transform, zoom, font, frame_count)
        light_scatter8.draw_text(screen, font, frame_count)



        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)
        # Round the frame rate to 2 decimal places and print it
        frame_rate = round(clock.get_fps(), 4)
        print("FPS: ", frame_rate)

    pygame.quit()

if __name__ == "__main__":
    main()

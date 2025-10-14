import pygame
import pygame_gui
from control_panel import ControlPanel as cp
from gravity_source import GravitySource as gs
from light import Light

def main():
    pygame.init()
    pygame.display.set_caption("Gravity Simulation")
    screen = pygame.display.set_mode((cp.WIDTH, cp.HEIGHT))
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((cp.WIDTH, cp.HEIGHT))

    font = pygame.font.Font(None, 36)

    # Creating a gravity source with mass 3000 at the center of the screen
    gravity_source = gs(3000, (cp.WIDTH // 2, cp.HEIGHT // 2))

    # Creating a light object at an initial position
    light = Light((cp.WIDTH // 4, cp.HEIGHT // 2 + 100), (1, 0))

    if cp.MODE == 2:
        light.path = simulate_full_path(light, gravity_source, cp.MAX_FRAMES, cp.TIME_STEP)

    running = True
    paused = False
    frame_count = 0

    # GUI elements with labels
    width_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 10), (200, 30)), text="Width", manager=manager)
    width_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((10, 40), (200, 30)), start_value=cp.WIDTH, value_range=(400, 1600), manager=manager)

    height_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 80), (200, 30)), text="Height", manager=manager)
    height_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((10, 110), (200, 30)), start_value=cp.HEIGHT, value_range=(300, 1200), manager=manager)

    max_frames_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 150), (200, 30)), text="Max Frames", manager=manager)
    max_frames_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((10, 180), (200, 30)), start_value=cp.MAX_FRAMES, value_range=(1000, 20000000), manager=manager)

    time_step_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 220), (200, 30)), text="Time Step", manager=manager)
    time_step_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((10, 250), (200, 30)), start_value=cp.TIME_STEP, value_range=(0.01, 1.0), manager=manager)

    gravity_source_radius_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 290), (200, 30)), text="Gravity Source Radius", manager=manager)
    gravity_source_radius_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((10, 320), (200, 30)), start_value=cp.GRAVITY_SOURCE_RADIUS, value_range=(5, 50), manager=manager)

    light_radius_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 360), (200, 30)), text="Light Radius", manager=manager)
    light_radius_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((10, 390), (200, 30)), start_value=cp.LIGHT_RADIUS, value_range=(5, 50), manager=manager)

    path_width_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 430), (200, 30)), text="Path Width", manager=manager)
    path_width_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((10, 460), (200, 30)), start_value=cp.PATH_WIDTH, value_range=(1, 10), manager=manager)

    mode_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 500), (200, 30)), text="Mode (1: Real-time, 2: Full Path)", manager=manager)
    mode_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((10, 530), (200, 30)), start_value=cp.MODE, value_range=(1, 2), manager=manager)

    pause_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 570), (100, 30)), text='Pause', manager=manager)

    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == pause_button:
                        paused = not paused
                        pause_button.set_text('Resume' if paused else 'Pause')

            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == width_slider:
                    cp.WIDTH = int(width_slider.get_current_value())
                    screen = pygame.display.set_mode((cp.WIDTH, cp.HEIGHT))
                elif event.ui_element == height_slider:
                    cp.HEIGHT = int(height_slider.get_current_value())
                    screen = pygame.display.set_mode((cp.WIDTH, cp.HEIGHT))
                elif event.ui_element == max_frames_slider:
                    cp.MAX_FRAMES = int(max_frames_slider.get_current_value())
                elif event.ui_element == time_step_slider:
                    cp.TIME_STEP = float(time_step_slider.get_current_value())
                elif event.ui_element == gravity_source_radius_slider:
                    cp.GRAVITY_SOURCE_RADIUS = int(gravity_source_radius_slider.get_current_value())
                elif event.ui_element == light_radius_slider:
                    cp.LIGHT_RADIUS = int(light_radius_slider.get_current_value())
                elif event.ui_element == path_width_slider:
                    cp.PATH_WIDTH = int(path_width_slider.get_current_value())
                elif event.ui_element == mode_slider:
                    cp.MODE = int(mode_slider.get_current_value())
                    if cp.MODE == 2:
                        light.path = simulate_full_path(light, gravity_source, cp.MAX_FRAMES, cp.TIME_STEP)

            manager.process_events(event)

        manager.update(time_delta)

        screen.fill(cp.BACKGROUND_COLOR)

        if not paused:
            if cp.MODE == 1:
                if frame_count < cp.MAX_FRAMES:
                    light.move_due_to_gravity(gravity_source, cp.TIME_STEP)
                    light.move_towards_direction(cp.TIME_STEP)
                    light.update_direction(gravity_source)
                    frame_count += 1

                for i in range(len(light.path) - 1):
                    pygame.draw.line(screen, cp.PATH_COLOR, light.path[i], light.path[i + 1], cp.PATH_WIDTH)

            if cp.MODE == 2:
                for i in range(len(light.path) - 1):
                    pygame.draw.line(screen, cp.PATH_COLOR, light.path[i], light.path[i + 1], cp.PATH_WIDTH)

        pygame.draw.circle(screen, cp.GRAVITY_SOURCE_COLOR, gravity_source.position, cp.GRAVITY_SOURCE_RADIUS)
        pygame.draw.circle(screen, cp.LIGHT_COLOR, light.get_position(), cp.LIGHT_RADIUS)

        manager.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
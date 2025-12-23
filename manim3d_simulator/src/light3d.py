from manim import *
import math
from manim3d_simulator.control_panel import ControlPanel as cp

class Light3D(Group):
    def __init__(self, position, direction):
        super().__init__()
        self.position = list(position)  # Use a list to allow modification
        self.stopped = False  # To track if the light should stop moving
        self.direction = list(direction)  # To track the initial direction
        self.path = [tuple(self.position)]  # To store the path of the light
        # Create a visual object for the light
        self.dot = self.light_dot()
        self.add(self.dot)


    def light_dot(self):
        return Sphere(
            radius=cp.LIGHT_RADIUS, 
            color=cp.LIGHT_COLOR,
            fill_opacity=0.5,
            stroke_color=cp.LIGHT_COLOR
            )

    def move_due_to_gravity(self, gravity_source, time_step):
        if self.stopped:
            return  # Do not move if stopped
        
        pull_vector = gravity_source.gravitational_pull(self.position)
        self.position[0] += pull_vector[0] * time_step
        self.position[1] += pull_vector[1] * time_step
        self.position[2] += pull_vector[2] * time_step
        self.path.append(tuple(self.position))  # Add the new position to the path

        # Debugging output
        distance = self.distance_to_gravity_source(gravity_source)
        print(f"Light Position: {self.position}, Distance to Gravity Source: {distance}")

        # Check distance to gravity source
        if distance <= cp.STOP_DISTANCE_THRESHOLD:
            self.stopped = True  # Stop moving if within threshold

        # Update the visual position of the light
        self.dot.move_to(self.position)

    def move_towards_direction(self, time_step):
        self.position[0] += self.direction[0] * time_step
        self.position[1] += self.direction[1] * time_step
        self.position[2] += self.direction[2] * time_step
        self.path.append(tuple(self.position))
        self.dot.move_to(self.position)

    def update_direction(self, gravity_source):
        self.direction[0] += gravity_source.gravitational_pull(self.position)[0]
        self.direction[1] += gravity_source.gravitational_pull(self.position)[1]
        self.direction[2] += gravity_source.gravitational_pull(self.position)[2]

    def get_position(self):
        return tuple(self.position)
    
    def distance_to_gravity_source(self, gravity_source):
        return math.sqrt((self.position[0] - gravity_source.position[0])**2 + 
                         (self.position[1] - gravity_source.position[1])**2 + 
                         (self.position[2] - gravity_source.position[2])**2)
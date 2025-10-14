import numpy as np
import math
from parameters import STOP_DISTANCE_THRESHOLD

class Light:
    def __init__(self, position, direction):
        self.position = np.array(position, dtype=np.float64)  # Ensure float64 type
        self.path = [tuple(self.position)]
        self.stopped = False
        self.direction = np.array(direction, dtype=np.float64)  # Ensure float64 type

    def move_due_to_gravity(self, gravity_source, time_step):
        if self.stopped:
            return

        pull_vector = np.array(gravity_source.gravitational_pull(self.position), dtype=np.float64)  # Ensure float64 type
        self.position += pull_vector * time_step
        self.path.append(tuple(self.position))

        distance = np.linalg.norm(self.position - np.array(gravity_source.position, dtype=np.float64))  # Ensure float64 type
        if distance <= STOP_DISTANCE_THRESHOLD:
            self.stopped = True
            print(f"Light stopped at position: {self.position}")

    def move_towards_direction(self, time_step):
        # if self.stopped:
        #     return
        self.position += self.direction * time_step
        self.path.append(tuple(self.position))

    def update_direction(self, gravity_source):
        if self.stopped:
            return
        pull_vector = np.array(gravity_source.gravitational_pull(self.position), dtype=np.float64)  # Ensure float64 type
        self.direction += pull_vector

    def get_position(self):
        return tuple(self.position)

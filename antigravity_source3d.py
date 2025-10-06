import numpy as np
import math

class AntiGravitySource3D:
    def __init__(self, mass, position):
        self.mass = mass
        self.position = np.array(position, dtype=float)

    def gravitational_pull(self, light_ray_position):
        distance_vector = self.position - np.array(light_ray_position, dtype=float)
        distance = np.linalg.norm(distance_vector)
        if distance == 0:
            return np.array([0.0, 0.0, 0.0])  # Avoid division by zero
        strength = self.mass / distance**2
        direction = distance_vector / distance
        pull_vector = -strength * direction

        return pull_vector
    
    def move(self, new_position):
        self.position = np.array(new_position, dtype=float)
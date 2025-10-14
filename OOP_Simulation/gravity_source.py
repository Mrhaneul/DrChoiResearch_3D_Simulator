import math
class GravitySource:
    def __init__(self, mass, position):
        self.mass = mass
        self.position = position
    
    def gravitational_pull(self, light_ray_position):
        distance = math.sqrt((light_ray_position[0] - self.position[0])**2 +  (light_ray_position[1] - self.position[1])**2)
        if distance == 0:
            return (0, 0)  # Avoid division by zero
        strength = self.mass / distance**2
        direction = (
            (self.position[0] - light_ray_position[0]) / distance,
            (self.position[1] - light_ray_position[1]) / distance
        )
        pull_vector = (strength * direction[0], strength * direction[1])
        return pull_vector
    
    def set_position(self, position):
        self.position = position
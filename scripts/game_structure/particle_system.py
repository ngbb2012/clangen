import pygame
import pygame_gui
import pygame_gui.elements.ui_image


class ParticleSystem:
    def __init__(self):
        self.particles: list[Particle] = []


class Particle:
    def __init__(self):
        """Initializes the particle"""
        self.position: list[float] = [0, 0]
        self.velocity: list[float] = [0, 0]
        self.acceleration: list[float] = [0, 0]

        self.rotation: float = 0
        self.angular_velocity: float = 0
        
        self.texture : pygame.surface = pygame.image.load(f"resources\images\particle_effects\default.png")

    def update(self):
        """Updates the trans form of this particle based on its acceleration."""
        for i in range(2):
            # updating position
            self.velocity[i] += self.acceleration[i]
            self.acceleration[i] = 0

            self.position[i] += self.velocity[i]

        # updating rotation
        self.rotation += self.angular_velocity

    def render(self):
        """Renders the particle according to it's position and rotation"""
        pygame_gui.elements.ui_image

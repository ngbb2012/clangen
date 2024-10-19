import pygame
import pygame_gui
import pygame_gui.elements.ui_image
import random

from copy import deepcopy
from scripts.game_structure.screen_settings import MANAGER
from scripts.game_structure.game_essentials import (
    game,
)


class ParticleSystem:
    def __init__(self):
        game.active_particle_systems.append(self)
        self.particles: list[Particle] = []

        # the total runtime since the creation of this particle system
        self.runtime : float = 0
        
        self.particle_count : int = 0
        self.duration : float = 10
        self.particle_life_time : float = 10
        self.repeat: bool = True

        self.origin: list[float] = [0, 0]
        self.initial_velocity: list[float] = [0, 0]
        self.initial_rotation: float = 0

        self._angular_velocity: float = 0
        self._drag: float = 0

        self.start_size: float = 100

        self.gravity: list[float] = [0, 0]

    def set_velocity(
        self, velocity: list[float], gravity: list[float], angular_velocity: float
    ):
        """Initializes the initial velocity of the particle system"""
        self.initial_velocity = velocity
        self.gravity = gravity
        self.angular_velocity = angular_velocity

    def add_particle(self, amount: int):
        """Adds a specific amount of particle to this particle system"""
        for _ in range(amount):
            p: Particle = Particle()
            p.position = deepcopy(self.origin)
            p.velocity = deepcopy(self.initial_velocity)
            p.angular_velocity = deepcopy(self.angular_velocity)
            p.size = deepcopy(self.start_size)
            p.drag = self._drag
            self.particles.append(p)

    def update(self, delta_time: float):
        """Get called every frame."""
        self.update_particles(delta_time)
        

    def update_particles(self, delta_time: float):
        """Updates every particle in this particle system"""
        for particle in self.particles:
            particle.apply_force(self.gravity)
            particle.update(delta_time)


class Particle:
    """
    An individual particle in a particle system with transform and velocity.
    """

    def __init__(self):
        """Initializes the particle"""
        self.size: float = 1

        self.position: list[float] = [0, 0]
        self.velocity: list[float] = [0, 0]
        self.acceleration: list[float] = [0, 0]

        self.rotation: float = 0
        self.angular_velocity: float = 0

        self.drag: float = 0.01

        # loads the texture
        self.texture: pygame.surface = pygame.image.load(
            "resources/images/particle_effects/default.png"
        ).convert_alpha()

        self.ui_image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(self.position[0], self.position[1], 50, 50),
            image_surface=self.texture,
            manager=MANAGER,
            anchors={"center": "center"},
        )

    def apply_force(self, force: list[float]):
        """Accelerates the particle by force."""
        self.acceleration = [a + b for a, b in zip(self.acceleration, force)]

    def update(self, delta_time: float):
        """Updates the trans form of this particle based on its acceleration."""
        # loops over the x and y axis
        for i in range(2):
            # updating position
            self.velocity[i] += self.acceleration[i] * delta_time
            self.acceleration[i] = 0

            self.velocity[i] *= 1 - self.drag

            self.position[i] += self.velocity[i] * delta_time
            
        # updating rotation
        self.rotation += self.angular_velocity * delta_time
        self.render()

    def render(self):
        """Renders the particle according to it's position and rotation"""
        # scale is done fist to avoid overidding rotation's size change
        self.ui_image.image = pygame.transform.scale(
            self.texture, (self.size, self.size)
        )
        # rotates the particle according to it's angular velocity
        if self.angular_velocity != 0:
            self.ui_image.image = pygame.transform.rotate(
                self.ui_image.image, self.rotation
            )
        # make it so it's always on it's center
        self.ui_image.set_position(
            [
                self.position[0] - self.ui_image.image.size[0] / 2,
                self.position[1] - self.ui_image.image.size[1] / 2,
            ]
        )

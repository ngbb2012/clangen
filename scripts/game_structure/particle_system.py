import pygame
import pygame_gui
import pygame_gui.elements.ui_image
import random
import math

from copy import deepcopy
from scripts.game_structure.screen_settings import MANAGER
from scripts.game_structure.game_essentials import (
    game,
)


class ParticleSystem:
    """A class to manage and simulate a system of particles in a game environment.
    It handles the creation, updating, and management of particles over time.

    This class maintains a collection of particles, their properties, and their behavior
    during the simulation. It allows for the initialization of particle velocities,
    addition of new particles, and updates to their states."""

    def __init__(self):
        game.active_particle_systems.append(self)
        self.particles: list[Particle] = []

        # the total runtime since the creation of this particle system
        self.runtime: float = 0

        self.particle_count: int = 0
        self.duration: float = 10
        self.particle_life_time: float = 10
        self.repeat: bool = True

        self.normalize_spawn_rect : bool = True
        self.spawn_rect: list[int] = [0, 0, 0, 0]
        self.initial_velocity: list[float] = [0, 0]
        self.initial_rotation: float = 0

        self.angular_velocity: float = 0
        self.drag: float = 0

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
            p: Particle = Particle(self)
            # move the particle to a random point on the spawn rect
            #                            :3
            p.position = self.spawn_rect[:3]
            p.position = [
                a + b
                for a, b in zip(
                    p.position,
                    [
                        (self.spawn_rect[0] - self.spawn_rect[2]) * random.random(),
                        (self.spawn_rect[3] - self.spawn_rect[1]) * random.random(),
                    ],
                )
            ]
            self.particles.append(p)

    def update(self, delta_time: float):
        """Get called every frame."""
        self.runtime += delta_time
        self.update_particles(delta_time)

    def update_particles(self, delta_time: float):
        """Updates every particle in this particle system"""
        for particle in self.particles:
            particle.update(delta_time)


class Particle:
    """
    An individual particle in a particle system with transform and velocity.
    """

    def __init__(self, parent_particle_system: ParticleSystem):
        """Initializes the particle"""

        self.parent_particle_system: ParticleSystem = parent_particle_system

        # initialization for position is handled differently
        self.position: list[float] = [0, 0]
        self.velocity: list[float] = deepcopy(parent_particle_system.initial_velocity)

        self.acceleration: list[float] = [0, 0]
        self.size: float = deepcopy(parent_particle_system.start_size)

        self.rotation: float = 0
        self.angular_velocity: float = deepcopy(parent_particle_system.angular_velocity)

        # TODO: make it dynamic
        # loads the texture
        self.texture: pygame.surface = pygame.image.load(
            "resources/images/particle_effects/default.png"
        ).convert_alpha()

        self.ui_image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(0, 0, self.size, self.size),
            image_surface=self.texture,
            manager=MANAGER,
        )

    def apply_force(self, force: list[float]):
        """Accelerates the particle by force."""
        self.acceleration = [a + b for a, b in zip(self.acceleration, force)]

    def update(self, delta_time: float):
        """Updates the trans form of this particle based on its acceleration."""
        # loops over the x and y axis
        for i in range(2):
            # updating position
            self.velocity[i] += self.parent_particle_system.gravity[i]
            self.velocity[i] += self.acceleration[i] * delta_time
            self.acceleration[i] = 0

            self.velocity[i] *= 1 - self.parent_particle_system.drag

            self.position[i] += self.velocity[i] * delta_time

        # updating rotation
        self.rotation += self.angular_velocity * delta_time
        self.render()

    def render(self):
        """Renders the particle according to it's position and rotation"""
        # scale is done fist to avoid overriding rotation
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
                -1,
                -1
            ]
        )
        self.ui_image.relative_rect = self.ui_image.image.get_rect()
        self.size = math.sin(self.parent_particle_system.runtime) * 30 + 100
        print(
            self.angular_velocity
        )

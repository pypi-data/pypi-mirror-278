import yaml
import pygame
from typing import Any
from space_invaders.components.base_objects import MovableObject
import importlib.resources as pkg_resources
import space_invaders

config_path = str(pkg_resources.files(space_invaders).joinpath("config.yaml"))

with open(config_path) as file:
    config = yaml.safe_load(file)

WIDTH = config["WIDTH"]
HEIGHT = config["HEIGHT"]


class Enemy(MovableObject):
    def __init__(
        self, image: pygame.surface.Surface, initial_pos: tuple, speed: int
    ) -> None:
        super().__init__(image, initial_pos, speed)
        self.movement_direction = -1

    def switch_movement_direction(self):
        self.movement_direction *= -1

    def update(self, dt) -> None:
        self.rect.left += self.movement_direction * self.speed * dt

    def move_row_down(self) -> None:
        self.rect.centery += HEIGHT * 0.02


class EnemyCreator:
    """Factory class for creating Enemies different types."""

    def __init__(self, type: str) -> None:
        self.created_enemies = {"weak": 0}
        self.type = type

    def create_enemy(
        self, image: pygame.surface.Surface, initial_pos: tuple, speed: int
    ):
        """Factory method for creating an Enemy instance."""
        self.created_enemies[self.type] += 1
        if self.type == "weak":
            return Enemy(image, initial_pos, speed)

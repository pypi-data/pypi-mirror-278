from typing import Any
from space_invaders.components.base_objects import MovableObject
import pygame
import yaml
import importlib.resources as pkg_resources
import space_invaders

config_path = str(pkg_resources.files(space_invaders).joinpath("config.yaml"))
laser_im_path = str(pkg_resources.files(space_invaders).joinpath("assets/laser.png"))

with open(config_path) as file:
    config = yaml.safe_load(file)

HEIGHT = config["HEIGHT"]


class Laser(MovableObject):
    """
    Class for sprites representing lasers that can be shot by enemies and the
    player.
    """

    directions = {"up": -1, "down": 1}

    def __init__(self, image: pygame.Surface, initial_pos: tuple, speed: int) -> None:
        super().__init__(image, initial_pos, speed)

    def update(self, direction: str, dt) -> None:
        self.rect.centery += Laser.directions[direction] * self.speed * dt
        if self._is_out_of_screen():
            self.kill()

    def _is_out_of_screen(self) -> bool:
        if self.rect.bottom < 0:
            return True
        elif self.rect.top > HEIGHT:
            return True
        return False

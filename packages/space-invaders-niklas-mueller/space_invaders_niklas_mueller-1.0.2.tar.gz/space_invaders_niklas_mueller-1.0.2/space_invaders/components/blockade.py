from typing import Iterable
from space_invaders.components.base_objects import BaseObject
import space_invaders
import importlib.resources as pkg_resources
import pygame
import yaml

config_path = str(pkg_resources.files(space_invaders).joinpath("config.yaml"))

with open(config_path) as file:
    config = yaml.safe_load(file)

WIDTH = config["WIDTH"]
HEIGHT = config["HEIGHT"]


class Blockade(BaseObject):
    """Simple class for bloackade pieces that provide the player with cover from enemy shots ."""

    def __init__(self, image, initial_pos: tuple) -> None:
        super().__init__(image, initial_pos)


class BlockadeGroup(pygame.sprite.Group):
    """Group for all Blockade objects."""

    def __init__(self) -> None:
        super().__init__()

    def add(self, *sprites: Blockade | Iterable[Blockade]) -> None:
        return super().add(*sprites)

from space_invaders.components.blockade import (
    Blockade,
    BlockadeGroup,
)
from space_invaders.components.player import Player, PlayerObject
from space_invaders.components.laser import Laser
from space_invaders.components.base_objects import BaseObject, MovableObject
from space_invaders.components.objects import Enemy, EnemyCreator
from space_invaders.components.level import LevelGenerator
from space_invaders.components.game_handler import GameHandler, GameHandlerBase
from space_invaders.components.scoreboard import ScoreBoard, LiveIcon
from space_invaders.components.controller import (
    EnemyController,
    LaserController,
    BlockadeController,
    GameObjectController,
)
import yaml
import space_invaders
import importlib.resources as pkg_resources

config_path = str(pkg_resources.files(space_invaders).joinpath("config.yaml"))

with open(config_path) as file:
    config = yaml.safe_load(file)

all = [
    BaseObject,
    MovableObject,
    PlayerObject,
    Player,
    Enemy,
    Laser,
    Blockade,
    BlockadeGroup,
    BlockadeController,
    EnemyCreator,
    EnemyController,
    LaserController,
    LevelGenerator,
    GameHandler,
    GameHandlerBase,
    GameObjectController,
    LiveIcon,
    ScoreBoard,
    config,
]

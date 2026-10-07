from dataclasses import dataclass
from math import hypot
from typing import Set

from pico2d import *


SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 1024
SPRITE_SIZE = 100
FRAME_COUNT = 8
MOVE_SPEED = 320.0
FRAME_INTERVAL = 0.08
IDLE_FRAME_INTERVAL = 0.12
MAX_DELTA_TIME = 0.1

IDLE_ROW_BY_DIRECTION = {
    1: 300,
    -1: 200,
}
MOVE_ROW_BY_DIRECTION = {
    1: 100,
    -1: 0,
}


@dataclass
class Character:
    x: float = SCREEN_WIDTH / 2
    y: float = SCREEN_HEIGHT / 2
    facing_direction: int = 1
    frame: int = 0
    animation_time: float = 0.0
    animation_row: int = IDLE_ROW_BY_DIRECTION[1]

    def _keep_inside_screen(self) -> None:
        half_size = SPRITE_SIZE / 2
        self.x = max(half_size, min(SCREEN_WIDTH - half_size, self.x))
        self.y = max(half_size, min(SCREEN_HEIGHT - half_size, self.y))

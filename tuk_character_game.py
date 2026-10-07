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

    def _advance_animation(self, delta_time: float, interval: float) -> None:
        self.animation_time += delta_time
        while self.animation_time >= interval:
            self.animation_time -= interval
            self.frame = (self.frame + 1) % FRAME_COUNT

    def update(self, pressed_keys: Set[int], delta_time: float) -> None:
        horizontal = 0
        vertical = 0
        if SDLK_LEFT in pressed_keys:
            horizontal -= 1
        if SDLK_RIGHT in pressed_keys:
            horizontal += 1
        if SDLK_DOWN in pressed_keys:
            vertical -= 1
        if SDLK_UP in pressed_keys:
            vertical += 1

        moving = horizontal != 0 or vertical != 0
        if horizontal != 0:
            self.facing_direction = 1 if horizontal > 0 else -1

        if moving:
            vector_length = hypot(horizontal, vertical)
            self.x += horizontal / vector_length * MOVE_SPEED * delta_time
            self.y += vertical / vector_length * MOVE_SPEED * delta_time
            self.animation_row = MOVE_ROW_BY_DIRECTION[self.facing_direction]
            interval = FRAME_INTERVAL
        else:
            self.animation_row = IDLE_ROW_BY_DIRECTION[self.facing_direction]
            interval = IDLE_FRAME_INTERVAL

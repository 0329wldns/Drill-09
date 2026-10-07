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

        self._keep_inside_screen()
        self._advance_animation(delta_time, interval)

    def draw(self, image) -> None:
        image.clip_draw(
            self.frame * SPRITE_SIZE,
            self.animation_row,
            SPRITE_SIZE,
            SPRITE_SIZE,
            int(self.x),
            int(self.y),
        )


def handle_events(pressed_keys: Set[int]) -> bool:
    for event in get_events():
        if event.type == SDL_QUIT:
            return False
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                return False
            pressed_keys.add(event.key)
        elif event.type == SDL_KEYUP:
            pressed_keys.discard(event.key)
    return True


def main() -> None:
    open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
    background = load_image("TUK_GROUND.png")
    character_image = load_image("animation_sheet.png")
    character = Character()
    pressed_keys: Set[int] = set()
    running = True
    previous_time = get_time()

    try:
        while running:
            current_time = get_time()
            delta_time = min(current_time - previous_time, MAX_DELTA_TIME)
            previous_time = current_time
            running = handle_events(pressed_keys)
            character.update(pressed_keys, delta_time)

            clear_canvas()
            background.draw(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            character.draw(character_image)
            update_canvas()
            delay(0.016)

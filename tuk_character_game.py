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


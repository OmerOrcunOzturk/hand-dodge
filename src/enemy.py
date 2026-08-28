import random

import pygame

from settings import SCREEN_HEIGHT, SCREEN_WIDTH


ENEMY_WIDTH = 50
ENEMY_HEIGHT = 35
ENEMY_COLOR = (220, 80, 80)


class Enemy:
    def __init__(self) -> None:
        start_x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
        self.y = float(-ENEMY_HEIGHT)
        self.rect = pygame.Rect(
            start_x,
            int(self.y),
            ENEMY_WIDTH,
            ENEMY_HEIGHT,
        )

    def update(self, delta_time: float, speed: float) -> None:
        self.y += speed * delta_time
        self.rect.y = int(self.y)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, ENEMY_COLOR, self.rect)

    def is_off_screen(self) -> bool:
        return self.rect.top > SCREEN_HEIGHT

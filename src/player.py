from typing import Any

import pygame

from settings import (
    FPS,
    PLAYER_SMOOTHING,
    PLAYER_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


PLAYER_WIDTH = 70
PLAYER_HEIGHT = 24
PLAYER_COLOR = (80, 180, 120)
PLAYER_BOTTOM_MARGIN = 35


class Player:
    def __init__(self) -> None:
        start_x = (SCREEN_WIDTH - PLAYER_WIDTH) // 2
        start_y = SCREEN_HEIGHT - PLAYER_HEIGHT - PLAYER_BOTTOM_MARGIN
        self.x = float(start_x)
        self.rect = pygame.Rect(start_x, start_y, PLAYER_WIDTH, PLAYER_HEIGHT)

    def update(self, keys: Any, delta_time: float) -> None:
        if keys[pygame.K_LEFT]:
            self.x -= PLAYER_SPEED * delta_time

        if keys[pygame.K_RIGHT]:
            self.x += PLAYER_SPEED * delta_time

        self.rect.x = int(self.x)
        self.keep_inside_screen()

    def update_from_hand(self, hand_x: float, delta_time: float) -> None:
        target_center_x = hand_x * SCREEN_WIDTH
        current_center_x = self.x + self.rect.width / 2
        smoothing = min(1.0, PLAYER_SMOOTHING * delta_time * FPS)
        new_center_x = current_center_x + (
            target_center_x - current_center_x
        ) * smoothing

        self.x = new_center_x - self.rect.width / 2
        self.rect.x = int(self.x)
        self.keep_inside_screen()

    def keep_inside_screen(self) -> None:
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.x = float(self.rect.x)

    def draw(self, screen: pygame.Surface, is_visible: bool = True) -> None:
        if not is_visible:
            return

        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)

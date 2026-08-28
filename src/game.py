from typing import Any

import cv2
import pygame

from camera import Camera
from enemy import Enemy
from hand_tracker import HandTracker
from player import Player
from settings import (
    BACKGROUND_COLOR,
    CALIBRATION_REQUIRED_FRAMES,
    CALIBRATION_TIMEOUT,
    CAMERA_PREVIEW_HEIGHT,
    CAMERA_PREVIEW_MARGIN,
    CAMERA_PREVIEW_WIDTH,
    DIFFICULTY_SCORE_STEP,
    ENEMY_MAX_SPEED,
    ENEMY_MIN_SPAWN_TIME,
    ENEMY_SPAWN_TIME,
    ENEMY_SPAWN_TIME_DECREASE,
    ENEMY_SPEED,
    ENEMY_SPEED_INCREASE,
    FPS,
    PLAYER_BLINK_TIME,
    PLAYER_INVINCIBLE_TIME,
    PLAYER_START_LIVES,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SCORE_PER_SECOND,
    WINDOW_TITLE,
)


HAND_POSITION_PRINT_INTERVAL = 30
TEXT_COLOR = (240, 240, 240)
PREVIEW_BORDER_COLOR = (220, 220, 220)
PREVIEW_BACKGROUND_COLOR = (12, 14, 18)
HAND_DETECTED_COLOR = (120, 220, 150)
HAND_MISSING_COLOR = (255, 210, 90)


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.hand_detected_text = self.font.render(
            "Hand Detected",
            True,
            HAND_DETECTED_COLOR,
        )
        self.show_hand_text = self.font.render(
            "Show Your Hand",
            True,
            HAND_MISSING_COLOR,
        )

        self.camera = Camera()
        self.hand_tracker = HandTracker()
        self.player = Player()
        self.enemies: list[Enemy] = []

        self.camera_is_available = False
        self.camera_preview: pygame.Surface | None = None
        self.running = True
        self.frame_count = 0
        self.lives = PLAYER_START_LIVES
        self.invincible_until = 0
        self.score = 0.0
        self.game_over = False
        self.calibrating = True
        self.calibration_failed = False
        self.detected_frames = 0

        self.delta_time = 0.0
        self.current_time = pygame.time.get_ticks()
        self.last_enemy_spawn_time = self.current_time
        self.calibration_start_time = self.current_time
        self.hand_x: float | None = None
        self.hand_detected = False
        self.is_invincible = False

        self.preview_rect = self.create_preview_rect()
        self.preview_panel_rect = pygame.Rect(
            self.preview_rect.x - 4,
            self.preview_rect.y - 4,
            CAMERA_PREVIEW_WIDTH + 8,
            CAMERA_PREVIEW_HEIGHT + 36,
        )
        self.preview_status_pos = (
            self.preview_rect.x,
            self.preview_rect.y + CAMERA_PREVIEW_HEIGHT + 8,
        )

    def create_preview_rect(self) -> pygame.Rect:
        return pygame.Rect(
            SCREEN_WIDTH - CAMERA_PREVIEW_WIDTH - CAMERA_PREVIEW_MARGIN,
            CAMERA_PREVIEW_MARGIN,
            CAMERA_PREVIEW_WIDTH,
            CAMERA_PREVIEW_HEIGHT,
        )

    def run(self) -> None:
        print("Hand Dodge baslatildi.")
        self.open_camera()

        try:
            while self.running:
                self.delta_time = self.clock.tick(FPS) / 1000
                self.current_time = pygame.time.get_ticks()
                self.hand_x = None
                self.hand_detected = False

                self.handle_events()
                if not self.running:
                    break

                self.update_camera()
                self.update()
                self.draw()
                self.frame_count += 1
        finally:
            self.close()

    def open_camera(self) -> None:
        try:
            self.camera.open()
            self.camera_is_available = True
        except RuntimeError as error:
            print(error)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

            if (
                self.calibrating
                and self.calibration_failed
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_r
            ):
                self.reset_calibration()

            if (
                self.game_over
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.reset_game()

    def reset_calibration(self) -> None:
        self.calibration_failed = False
        self.calibration_start_time = self.current_time
        self.detected_frames = 0

    def reset_game(self) -> None:
        self.player = Player()
        self.enemies.clear()
        self.lives = PLAYER_START_LIVES
        self.invincible_until = 0
        self.score = 0.0
        self.frame_count = 0
        self.last_enemy_spawn_time = self.current_time
        self.game_over = False

    def update_camera(self) -> None:
        if not self.camera_is_available:
            return

        success, frame = self.camera.read_frame()
        if not success:
            return

        frame = cv2.flip(frame, 1)
        frame, hand_landmarks = self.hand_tracker.process_frame(frame)
        self.hand_x = self.hand_tracker.get_hand_x(hand_landmarks)
        self.hand_detected = self.hand_x is not None
        self.camera_preview = self.camera_frame_to_surface(frame)

        if (
            self.hand_x is not None
            and self.frame_count % HAND_POSITION_PRINT_INTERVAL == 0
        ):
            print(f"El X konumu: {self.hand_x:.2f}")

    def update(self) -> None:
        if self.calibrating:
            self.update_calibration()
            self.is_invincible = False
            return

        if self.game_over:
            self.is_invincible = False
            return

        self.update_player()
        self.update_score()
        self.update_enemies()
        self.update_collisions()

    def update_calibration(self) -> None:
        if self.calibration_failed:
            return

        if self.hand_detected:
            self.detected_frames += 1
        else:
            self.detected_frames = 0

        if self.detected_frames >= CALIBRATION_REQUIRED_FRAMES:
            self.calibrating = False
            self.last_enemy_spawn_time = self.current_time
            return

        elapsed_time = self.current_time - self.calibration_start_time
        if elapsed_time >= CALIBRATION_TIMEOUT:
            self.calibration_failed = True

    def update_player(self) -> None:
        keys = pygame.key.get_pressed()

        if self.hand_x is not None:
            self.player.update_from_hand(self.hand_x, self.delta_time)
        else:
            self.player.update(keys, self.delta_time)

    def update_score(self) -> None:
        self.score += SCORE_PER_SECOND * self.delta_time

    def update_enemies(self) -> None:
        enemy_speed = self.get_enemy_speed()
        enemy_spawn_time = self.get_enemy_spawn_time()

        if self.current_time - self.last_enemy_spawn_time >= enemy_spawn_time:
            self.enemies.append(Enemy())
            self.last_enemy_spawn_time = self.current_time

        for enemy in self.enemies:
            enemy.update(self.delta_time, enemy_speed)

    def update_collisions(self) -> None:
        self.is_invincible = self.current_time < self.invincible_until
        active_enemies = []

        for enemy in self.enemies:
            if enemy.is_off_screen():
                continue

            if self.player.rect.colliderect(enemy.rect):
                self.handle_enemy_collision()
                continue

            active_enemies.append(enemy)

        self.enemies = active_enemies

    def handle_enemy_collision(self) -> None:
        if self.is_invincible:
            return

        self.lives = max(0, self.lives - 1)
        self.invincible_until = self.current_time + PLAYER_INVINCIBLE_TIME
        self.is_invincible = True

        if self.lives == 0:
            self.game_over = True

    def get_difficulty_level(self) -> int:
        return int(self.score // DIFFICULTY_SCORE_STEP)

    def get_enemy_speed(self) -> float:
        speed = ENEMY_SPEED + self.get_difficulty_level() * ENEMY_SPEED_INCREASE
        return min(speed, ENEMY_MAX_SPEED)

    def get_enemy_spawn_time(self) -> int:
        spawn_time = (
            ENEMY_SPAWN_TIME
            - self.get_difficulty_level() * ENEMY_SPAWN_TIME_DECREASE
        )
        return max(spawn_time, ENEMY_MIN_SPAWN_TIME)

    def draw(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)

        if self.calibrating:
            self.draw_calibration()
        else:
            self.draw_game()

        self.draw_camera_preview()
        pygame.display.flip()

    def draw_game(self) -> None:
        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.player.draw(self.screen, self.should_draw_player())
        self.draw_lives()
        self.draw_score()

        if self.game_over:
            self.draw_game_over()

    def should_draw_player(self) -> bool:
        if not self.is_invincible:
            return True

        return (self.current_time // PLAYER_BLINK_TIME) % 2 == 0

    def draw_lives(self) -> None:
        lives_text = self.font.render(f"Can: {self.lives}", True, TEXT_COLOR)
        self.screen.blit(lives_text, (20, 20))

    def draw_score(self) -> None:
        score_text = self.font.render(
            f"Skor: {int(self.score)}",
            True,
            TEXT_COLOR,
        )
        self.screen.blit(score_text, (20, 55))

    def draw_camera_preview(self) -> None:
        pygame.draw.rect(
            self.screen,
            PREVIEW_BACKGROUND_COLOR,
            self.preview_panel_rect,
        )

        if self.camera_preview is not None:
            self.screen.blit(self.camera_preview, self.preview_rect)

        pygame.draw.rect(
            self.screen,
            PREVIEW_BORDER_COLOR,
            self.preview_rect,
            2,
        )

        status_surface = (
            self.hand_detected_text
            if self.hand_detected
            else self.show_hand_text
        )
        self.screen.blit(status_surface, self.preview_status_pos)

    def draw_centered_text(
        self,
        font: pygame.font.Font,
        text: str,
        y: int,
    ) -> None:
        text_surface = font.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y))
        self.screen.blit(text_surface, text_rect)

    def draw_calibration(self) -> None:
        self.draw_centered_text(self.title_font, "Calibration", 165)
        self.draw_centered_text(self.font, "Elini kameraya goster", 235)

        progress_text = (
            f"Algilanan frame: "
            f"{self.detected_frames}/{CALIBRATION_REQUIRED_FRAMES}"
        )
        self.draw_centered_text(self.font, progress_text, 280)

        if self.calibration_failed:
            self.draw_centered_text(self.font, "Kalibrasyon basarisiz", 330)
            self.draw_centered_text(self.font, "Tekrar denemek icin R", 370)
        else:
            self.draw_centered_text(
                self.font,
                "El algilaninca oyun baslayacak",
                330,
            )

    def draw_game_over(self) -> None:
        self.draw_centered_text(
            self.title_font,
            "Game Over",
            SCREEN_HEIGHT // 2 - 80,
        )
        self.draw_centered_text(
            self.font,
            f"Son skor: {int(self.score)}",
            SCREEN_HEIGHT // 2,
        )
        self.draw_centered_text(
            self.font,
            "Yeniden baslatmak icin Space",
            SCREEN_HEIGHT // 2 + 45,
        )
        self.draw_centered_text(
            self.font,
            "Cikmak icin ESC",
            SCREEN_HEIGHT // 2 + 85,
        )

    def camera_frame_to_surface(self, frame: Any) -> pygame.Surface:
        small_frame = cv2.resize(
            frame,
            (CAMERA_PREVIEW_WIDTH, CAMERA_PREVIEW_HEIGHT),
        )
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        surface = pygame.image.frombuffer(
            rgb_frame.tobytes(),
            (CAMERA_PREVIEW_WIDTH, CAMERA_PREVIEW_HEIGHT),
            "RGB",
        )
        return surface.convert()

    def close(self) -> None:
        self.hand_tracker.close()
        self.camera.release()
        cv2.destroyAllWindows()
        pygame.quit()

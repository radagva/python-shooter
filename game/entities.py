import pygame
from .constants import RED, WHITE
from random import randint


class Ship:
    def __init__(
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        color: pygame.Color,
    ):
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        pygame.draw.rect(
            self.surface, self.color, (self.x, self.y, self.width, self.height)
        )

    def setup_movement(self):
        pressed_keys = pygame.key.get_pressed()
        has_A_pressed = pressed_keys[pygame.K_a]
        has_D_pressed = pressed_keys[pygame.K_d]

        next_place = self.x
        places = 5

        if has_A_pressed:
            next_place -= places

        if has_D_pressed:
            next_place += places

        if has_A_pressed and has_D_pressed:
            return

        if not self.will_exit_window_bounds(next_place):
            self.x = next_place

    def will_exit_window_bounds(self, x: int) -> bool:
        return (x + self.width) > self.surface.get_width() or x <= 0 - self.width / 2

    def shoot(self) -> "Bullet":
        return Bullet(
            surface=self.surface,
            x=self.x + self.width // 2,
            y=self.y - self.height // 2,
            width=5,
            height=5,
            color=RED,
        )


class Bullet:
    def __init__(
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        color: pygame.Color,
    ):
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 5

    def draw(self):
        self.y -= self.speed

        pygame.draw.rect(
            self.surface,
            color=WHITE,
            rect=(self.x, self.y, self.width, self.height),
        )

    def did_exit_window_bounds(self) -> bool:
        return self.y <= 0

    def did_shot_enemy(self, enemy: "Enemy") -> bool:
        return (
            self.x >= enemy.x
            and self.x <= enemy.x + enemy.width
            and self.y <= enemy.y + enemy.height
        )


class Enemy:
    def __init__(
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        color: pygame.Color,
    ):
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 2
        self.life = randint(1, 3)

    def draw(self):
        self.y += self.speed
        rect = pygame.draw.rect(
            self.surface, self.color, (self.x, self.y, self.width, self.height)
        )

        fontTitle = pygame.font.SysFont(None, 22)
        textTitle = fontTitle.render(f"{self.life}", True, WHITE)
        rectTitle = textTitle.get_rect(center=rect.center)

        self.surface.blit(textTitle, rectTitle)

    def did_exit_window_bounds(self) -> bool:
        return self.y >= self.surface.get_height()

    def reappear(self):
        self.y = 0
        self.x = randint(0, self.surface.get_width() - self.width)

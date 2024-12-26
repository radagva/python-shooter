import pygame
from random import randint
from time import time

window_x = 480
window_y = 720

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

pygame.init()
pygame.display.set_caption("Space shooter by Radagv")

surface = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

paused = False
running = True


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
            color=red,
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
            color=white,
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

        fontTitle = pygame.font.SysFont("arial", 14)
        textTitle = fontTitle.render(f"{self.life}", True, white)
        rectTitle = textTitle.get_rect(center=rect.center)

        self.surface.blit(textTitle, rectTitle)

    def did_exit_window_bounds(self) -> bool:
        return self.y >= self.surface.get_height()

    def reappear(self):
        self.y = 0
        self.x = randint(0, self.surface.get_width() - self.width)


player = Ship(
    surface=surface,
    x=int((window_x / 2) - 20),
    y=(window_y - 20),
    width=20,
    height=20,
    color=white,
)

enemytime = time()

bullets: list[Bullet] = []
enemies: list[Enemy] = []


def create_enemy_if_possible():
    global enemytime
    time_has_ellapsed = time() >= enemytime
    did_reach_max_enemies = len(enemies) >= 10

    if time_has_ellapsed and not did_reach_max_enemies:
        position_x = randint(0, window_x - 30)
        enemy = Enemy(surface, y=0, x=position_x, width=30, height=30, color=red)
        enemies.append(enemy)

        # Reset the alarm to add a new enemy.
        enemytime = time() + randint(1, 2)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(player.shoot())

    create_enemy_if_possible()

    player.setup_movement()

    surface.fill(black)

    player.draw()

    for enemy in enemies:
        enemy.draw()

        if enemy.did_exit_window_bounds():
            enemy.reappear()

    for bullet in bullets:
        bullet.draw()

        for enemy in enemies:
            if bullet.did_shot_enemy(enemy):
                enemy.life -= 1
                bullets.remove(bullet)

                if enemy.life == 0:
                    enemies.remove(enemy)

        if bullet.did_exit_window_bounds():
            bullets.remove(bullet)

    pygame.display.update()

    fps.tick(60)

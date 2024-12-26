import pygame
from random import randint
from time import time
from game.constants import WINDOW_X, WINDOW_Y, BLACK, WHITE, RED
from game.entities import Ship, Bullet, Enemy


pygame.init()
pygame.display.set_caption("Space shooter by Radagv")

surface = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
fps = pygame.time.Clock()

paused = False
running = True


player = Ship(
    surface=surface,
    x=(WINDOW_X // 2) - 20,
    y=(WINDOW_Y - 20),
    width=20,
    height=20,
    color=WHITE,
)

enemytime = time()

bullets: list[Bullet] = []
enemies: list[Enemy] = []
score = 0


def create_enemy_if_possible():
    global enemytime
    time_has_ellapsed = time() >= enemytime
    did_reach_max_enemies = len(enemies) >= 10

    if time_has_ellapsed and not did_reach_max_enemies:
        position_x = randint(0, WINDOW_X - 30)
        enemy = Enemy(surface, y=0, x=position_x, width=30, height=30, color=RED)
        enemies.append(enemy)

        # Reset the alarm to add a new enemy.
        enemytime = time() + randint(1, 2)


def show_score(in_surface: pygame.Surface):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    in_surface.blit(text, (10, 10))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(player.shoot())

            if event.key == pygame.K_p:
                paused = not paused

    if not paused:
        surface.fill(BLACK)

        player.setup_movement()

        player.draw()

        create_enemy_if_possible()

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
                        score += 1
                        enemies.remove(enemy)

            if bullet.did_exit_window_bounds():
                bullets.remove(bullet)

        show_score(in_surface=surface)

    pygame.display.update()

    fps.tick(60)

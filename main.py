from windows import main_menu
import pygame


size = width, height = 448, 576

pygame.init()

old_screen = pygame.display.set_mode((800, 600))

nick = main_menu(old_screen)

pygame.display.set_caption(f"Pacman Classic ({nick})")

del old_screen
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit

    pygame.display.flip()
    clock.tick(60)

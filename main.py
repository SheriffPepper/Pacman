from windows import main_menu, black
from logic import LEFT, RIGHT, UP, DOWN
from load_data import field_background
from pacman import Pacman
import pygame


size = width, height = 448, 576

pygame.init()

old_screen = pygame.display.set_mode((800, 600))

nick = main_menu(old_screen)

pygame.display.set_caption(f"Pacman Classic ({nick})")

del old_screen
screen = pygame.display.set_mode(size)
fps = 60
speed = 1.5
counter = 0
animation_speed = fps // 8
clock = pygame.time.Clock()

pacman = Pacman((240, 440), LEFT)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            pacman.update(event.key)

    screen.fill(black)
    field_background.draw(screen)

    pacman.draw(screen)

    if counter % animation_speed == 0:
        pacman.next()

    pacman.forward(speed)

    pygame.display.flip()
    clock.tick(fps)

    counter = (counter + 1) % fps

from load_data import field_background, black
from logic import Field, LEFT
from windows import main_menu
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

field = Field(width, height)

pacman = Pacman((240, 424), LEFT)
pacman.set_field(field)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
                pacman.update(event.key)
                pacman.time = 0

    screen.fill(black)
    field_background.draw(screen)

    for y in range(field.height):
        for x in range(field.width):
            pygame.draw.rect(screen, 0xffffff,
                             (x * 16, y * 16,
                              16, 16), width=1)

    pacman.draw(screen)

    if counter % animation_speed == 0:
        pacman.next()

    pacman.forward(speed)
    pacman.pacman = pacman.pacman[pacman.direction]
    pacman.time += 1

    pygame.display.flip()
    clock.tick(fps)

    counter = (counter + 1) % fps

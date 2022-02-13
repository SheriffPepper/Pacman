from load_data import field_background, screen_print, black
from ghosts import Blinky, FRIGHTENED
from logic import Field, LEFT
from windows import main_menu
from pacman import Pacman
from time import sleep
import pygame


size = width, height = 448, 576

pygame.init()

old_screen = pygame.display.set_mode((800, 600))

nick = main_menu(old_screen)

del old_screen
screen = pygame.display.set_mode(size)
fps = 60
speed = 2
counter = 0
animation_speed = fps // 20
clock = pygame.time.Clock()
level = 1

field = Field(width, height)

pacman = Pacman((224, 424), LEFT)
blinky = Blinky((224, 232), LEFT)
pacman.set_field(field)
blinky.set_field(field)

while level < 256:
    pygame.display.set_caption(f"Pacman Classic ({nick}) {level} level")

    if pacman.lives < 1:
        del pacman
        del blinky

        del field

        field = Field(width, height)

        pacman = Pacman((224, 424), LEFT)
        blinky = Blinky((224, 232), LEFT)

        pacman.set_field(field)
        blinky.set_field(field)
    else:
        field.dead = False
        field.is_win = False

        pacman.position = 224, 424
        blinky.position = 224, 232

        pacman.set_field(field)
        blinky.set_field(field)

    screen.fill(black)
    field_background.draw(screen)
    field.draw(screen)

    pacman.draw(screen)
    blinky.draw(screen)

    screen_print(screen, "Ready!", (176, 320), (255, 255, 0, 255))
    screen_print(screen, "High Score", (144, 0), (255, 255, 255, 255))
    score = '00' if pacman.score == 0 else str(pacman.score)
    screen_print(screen, score,
                 ((7 - len(score)) * field.size[0], field.size[1]), (255, 255, 255, 255))

    width_, height_ = pacman.pacman.get_width(), pacman.pacman.get_height()

    for live in range(pacman.lives):
        pacman.pacman.move(live * field.size[0] * 2 + 3 * field.size[0] - width_ // 2,
                           35 * field.size[1] - height_ // 2)
        pacman.pacman.draw(screen)

    pygame.display.flip()
    counter = fps * 3  # 3 seconds

    while counter:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit

        counter -= 1
        clock.tick(fps)

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
        field.draw(screen)

        width_, height_ = pacman.pacman.get_width(), pacman.pacman.get_height()

        for live in range(pacman.lives):
            pacman.pacman.move(live * field.size[0] * 2 + 3 * field.size[0] - width_ // 2,
                               35 * field.size[1] - height_ // 2)
            pacman.pacman.draw(screen)

        # for y in range(field.height):
        #     for x in range(field.width):
        #         pygame.draw.rect(screen, 0xffffff,
        #                          (x * 16, y * 16,
        #                           16, 16), width=1)

        screen_print(screen, "High Score", (144, 0), (255, 255, 255, 255))
        score = '00' if pacman.score == 0 else str(pacman.score)
        screen_print(screen, score,
                     ((7 - len(score)) * field.size[0], field.size[1]), (255, 255, 255, 255))

        pacman.draw(screen)
        blinky.draw(screen)

        if counter % animation_speed == 0:
            pacman.next()
            blinky.next()

        pacman.forward(speed)

        pacman.pacman = pacman.pacman[pacman.direction]
        if blinky.mode != FRIGHTENED:
            blinky.ghost = blinky.ghost[blinky.direction]
        else:
            blinky.ghost = blinky.ghost[4 + ((counter % fps) // (fps // 4)) % 2]

        pacman.time += 1

        blinky.update(pacman)

        field.update(pacman, blinky, None, None, None)

        pygame.display.flip()
        clock.tick(fps)

        counter = (counter + 1) % (fps ** 2)

        if field.is_win:
            field.is_win = False
            break
        elif field.dead:
            break

    if field.dead:
        pacman.lives -= 1
        if pacman.lives > 0:
            continue
        raise SystemExit
    elif field.is_win:
        pacman.lives = 0

    sleep(3)

    level += 1

    del field
    field = Field(width, height)

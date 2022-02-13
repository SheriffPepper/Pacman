<<<<<<< HEAD
=======
from load_data import *
import sqlite3
import pygame
import sys

width, height = 800, 600


def start_game(screen: pygame.Surface) -> str:
    """Asks what's your nickname"""
    pygame.display.set_caption("Pacman Classic (start game)")

    screen.fill(black, (0, height // 2, width, height))
    nick = ''

    screen_print(screen, "Your nickname -", (100, height // 2 + 24))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                key = event.key
                # Esc - return (warning: no more, than 1000 times)
                if key == pygame.K_ESCAPE:
                    nick = ''
                    return main_menu(screen)
                # Print some text
                elif pygame.K_a <= key <= pygame.K_z or pygame.K_0 <= key <= pygame.K_9 or \
                        key == pygame.K_SPACE:
                    nick += chr(key)
                # Delete one symbol
                elif key == pygame.K_BACKSPACE:
                    nick = nick[:-1]
                # Enter the name
                elif key == pygame.K_RETURN:
                    if nick:
                        return nick
        nick = nick[:20]

        screen.fill(black, (356, height // 2 + 24, 320, 16))
        screen_print(screen, nick, (356, height // 2 + 24))
        pygame.display.flip()


def settings(screen: pygame.Surface) -> str:
    pygame.display.set_caption("Pacman Classic (settings)")

    screen.fill(black, (0, height // 2, width, height))

    screen_print(screen, "There are no settings here yet", (160, height // 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return main_menu(screen)

        pygame.display.flip()


def lider_board(screen: pygame.Surface) -> str:
    pygame.display.set_caption("Pacman Classic (lider board)")

    screen.fill(black, (0, height // 2, width, height))

    database = sqlite3.connect("./data/database.db")
    cursor = database.cursor()

    result = cursor.execute('''
    SELECT nickname,
           score
      FROM champions
     ORDER BY -score,
              nickname;
    ''').fetchall()[:3]

    for index, (nickname, score) in enumerate(result):
        screen_print(screen, f"{index + 1} {nickname}", (200, height // 2 + index * 24 + 50))
        screen_print(screen, str(score), (width // 2 + 200, height // 2 + index * 24 + 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return main_menu(screen)

        pygame.display.flip()


def secret(screen: pygame.Surface) -> str:
    screen.fill(black, (0, height // 2, width, height))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return main_menu(screen)

        pygame.display.flip()


def main_menu(screen: pygame.Surface) -> str:
    pygame.display.set_caption("Welcome to Pacman Classic!")

    screen.fill(black)

    # Welcome picture
    image = welcome_background.image

    # resize image
    image = pygame.transform.scale(image,
                                   (width, int(image.get_height() * (width / image.get_width()))))

    screen.blit(image, (0, 0))

    screen_print(screen, "Pacman v1/0", (0, height - 16))

    start_button_pos = width // 2 - 80, height // 2
    settings_button_pos = width // 2 - 64, height // 2 + 24
    lider_button_pos = width // 2 - 88, height // 2 + 48
    exit_button_pos = width // 2 - 32, height // 2 + 72

    # Button is hover
    start_button = False
    settings_button = False
    lider_button = False
    exit_button = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Button move
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                # Start Game button
                if start_button_pos[0] <= x <= start_button_pos[0] + 160 and \
                        start_button_pos[1] <= y <= start_button_pos[1] + 16:
                    start_button = True
                # Settings button
                elif settings_button_pos[0] <= x <= settings_button_pos[0] + 128 and \
                        settings_button_pos[1] <= y <= settings_button_pos[1] + 16:
                    settings_button = True
                # Lider button
                elif lider_button_pos[0] <= x <= lider_button_pos[0] + 192 and \
                        lider_button_pos[1] <= y <= lider_button_pos[1] + 16:
                    lider_button = True
                # Exit button
                elif exit_button_pos[0] <= x <= exit_button_pos[0] + 64 and \
                        exit_button_pos[1] <= y <= exit_button_pos[1] + 16:
                    exit_button = True
                else:
                    start_button = False
                    settings_button = False
                    lider_button = False
                    exit_button = False
            # Button click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Start Game button
                if start_button_pos[0] <= x <= start_button_pos[0] + 160 and \
                        start_button_pos[1] <= y <= start_button_pos[1] + 16:
                    return start_game(screen)
                # Settings button
                elif settings_button_pos[0] <= x <= settings_button_pos[0] + 128 and \
                        settings_button_pos[1] <= y <= settings_button_pos[1] + 16:
                    return settings(screen)
                    # Lider button
                elif lider_button_pos[0] <= x <= lider_button_pos[0] + 192 and \
                        lider_button_pos[1] <= y <= lider_button_pos[1] + 16:
                    return lider_board(screen)
                # Exit button
                elif exit_button_pos[0] <= x <= exit_button_pos[0] + 64 and \
                        exit_button_pos[1] <= y <= exit_button_pos[1] + 16:
                    raise SystemExit
                # Secret button
                elif 315 <= x <= 465 and 115 <= y <= 270:
                    return secret(screen)

        # Pseudo-buttons
        screen_print(screen, "Start Game", start_button_pos,
                     color=yellow if start_button else None)
        screen_print(screen, "Settings", settings_button_pos,
                     color=yellow if settings_button else None)
        screen_print(screen, "Lider Button", lider_button_pos,
                     color=yellow if lider_button else None)
        screen_print(screen, "Exit", exit_button_pos,
                     color=yellow if exit_button else None)

        pygame.display.flip()
>>>>>>> eae7e18 (Deadline release (buggy, crutchy and magic code).)

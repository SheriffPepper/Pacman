from load_data import *
import pygame
import sys


def main_menu(screen: pygame.Surface) -> None:
    pygame.display.set_caption("Welcome to Pacman Classic!")

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
                    print("Start Game")
                # Settings button
                elif settings_button_pos[0] <= x <= settings_button_pos[0] + 128 and \
                        settings_button_pos[1] <= y <= settings_button_pos[1] + 16:
                    print("Settings")
                    # Lider button
                elif lider_button_pos[0] <= x <= lider_button_pos[0] + 192 and \
                         lider_button_pos[1] <= y <= lider_button_pos[1] + 16:
                    print("Lider Board")
                # Exit button
                elif exit_button_pos[0] <= x <= exit_button_pos[0] + 64 and \
                     exit_button_pos[1] <= y <= exit_button_pos[1] + 16:
                    print("Exit")
                    raise SystemExit
                # Secret button
                elif 315 <= x <= 465 and 115 <= y <= 270:
                    print("Secret button!")
                else:
                    pass

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
        clock.tick(60)


if __name__ == "__main__":
    pygame.init()

    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    main_menu(screen)

    print("Main menu closed successfully!")
    pygame.quit()

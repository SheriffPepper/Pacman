from load_data import load_image
import pygame
import sys


def main_menu(screen: pygame.Surface) -> None:
    pygame.display.set_caption("Welcome to Pacman Classic!")

    image = load_image("./data/pictures/welcome.png")
    # resize image
    image = pygame.transform.scale(image,
                                   (width, int(image.get_height() * (width / image.get_width()))))

    screen.blit(image, (0, 0))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return


if __name__ == "__main__":
    pygame.init()

    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)

    main_menu(screen)

    print("Main menu closed successfully!")
    pygame.quit()

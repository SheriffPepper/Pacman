import pygame
import os


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image: str, *groups) -> None:
        super().__init__(*groups)

        self.image = load_image(image)
        self.rect = self.image.get_rect()

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)


def load_image(image: str) -> pygame.image:
    # Image was not found or is not a file
    if not (os.path.exists(image) and os.path.isfile(image)):
        exit(f"Image file \"{image}\" not found")

    return pygame.image.load(image)


# Automatic data-load
with open('./data/data.path', 'r', encoding='utf-8') as file:
    # Data-loader
    exec(file.read())


# Welcome window background
welcome_background = Sprite(welcome_background)

# Entities
pacman = Sprite(pacman)

blinky = Sprite(blinky)  # red ghost
pinky = Sprite(pinky)  # pink ghost
inky = Sprite(inky)  # blue ghost
clyde = Sprite(clyde)  # orange ghost

# Decoration textures
symbols = Sprite(symbols)
items = Sprite(items)

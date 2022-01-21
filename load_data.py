import pygame
import os


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
welcome_background = load_image(welcome_background)

# Entities
pacman = load_image(pacman)

blinky = load_image(blinky)  # red ghost
pinky = load_image(pinky)  # pink ghost
inky = load_image(inky)  # blue ghost
clyde = load_image(clyde)  # orange ghost

# Decoration textures
symbols = load_image(symbols)
items = load_image(items)

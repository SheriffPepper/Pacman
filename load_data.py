import pygame
import os


def load_image(image: str) -> pygame.image:
    # Image was not found or is not a file
    if not (os.path.exists(image) and os.path.isfile(image)):
        exit(f"Image file \"{image}\" not found")

    return pygame.image.load(image)

import pygame
import os


# Colors
empty = 0, 0, 0, 0
black = 0, 0, 0, 255
yellow = 255, 255, 0, 255
red = 255, 0, 0, 255
green = 0, 255, 0, 255
blue = 0, 0, 255, 255


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image: str, *groups) -> None:
        super().__init__(*groups)

        self.image = load_image(image)
        self.rect = self.image.get_rect()

    def get_height(self) -> int:
        return self.rect.height

    def get_width(self) -> int:
        return self.rect.width

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

    def move(self, x: int, y: int) -> None:
        self.rect.x = x
        self.rect.y = y


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, image: str, size: tuple, *groups) -> None:
        super().__init__(*groups)

        self.image_name = image
        image = load_image(image)

        # Set fixed size
        self.rect = pygame.Rect(0, 0, image.get_width() // size[0], image.get_height() // size[1])

        self.index = 0, 0  # x, y
        self.size = self.columns, self.rows = size
        self.frames = []

        # Cutting the sprite sheet
        for y in range(size[1]):
            row = []
            for x in range(size[0]):
                frame_location = self.rect.width * x, self.rect.height * y
                row.append(image.subsurface(frame_location, self.rect.size))
            self.frames.append(row)

        self.image = self[self.index]

    def __next__(self):
        self.index = (self.index[0] + 1) % self.columns, self.index[1]
        self.image = self[self.index]

        return self

    def __getitem__(self, index):
        if isinstance(index, tuple):
            x, y = index

            return self.frames[y][x]
        elif isinstance(index, int):
            self.index = self.index[0], (self.index[1] + 1) % self.rows
            self.image = self[self.index]

            return self

    def get_height(self) -> int:
        return self.rect.height

    def get_width(self) -> int:
        return self.rect.width

    def draw(self, screen: pygame.Surface) -> None:
        """Draws a sprite on the screen"""
        screen.blit(self.image, self.rect)

    def move(self, x: int, y: int) -> None:
        self.rect.x = x
        self.rect.y = y

    def update(self) -> None:
        self.image = self[self.index]


def load_image(image: str) -> pygame.image:
    # Image was not found or is not a file
    if not (os.path.exists(image) and os.path.isfile(image)):
        exit(f"Image file \"{image}\" not found")

    return pygame.image.load(image)


def screen_print(screen: pygame.Surface, string: str, position: tuple, color: tuple = None) -> None:
    letters = 'abcdefghijklmnopqrstuvwxyz!\"/-0123456789'
    string = string.lower()

    x, y = position  # position in pixels

    for letter in string:
        if letter in letters:
            if color is None:
                screen.blit(symbols[letters.find(letter), 0], (x, y))
            else:
                # Changing the color of the symbol
                image = symbols[letters.find(letter), 0].copy()
                array = pygame.PixelArray(image)
                array.replace((222, 222, 255, 255), color)
                del array
                screen.blit(image, (x, y))

        x += symbols.rect.width


# Automatic data-load
with open('./data/data.path', 'r', encoding='utf-8') as file:
    # Data-loader
    exec(file.read())


# Welcome window background
welcome_background = Sprite(welcome_background)

# Entities
pacman = AnimatedSprite(pacman, (4, 4))

blinky = AnimatedSprite(blinky, (2, 6))  # red ghost
pinky = AnimatedSprite(pinky, (2, 6))  # pink ghost
inky = AnimatedSprite(inky, (2, 6))  # blue ghost
clyde = AnimatedSprite(clyde, (2, 6))  # orange ghost

# Decoration textures
symbols = AnimatedSprite(symbols, (40, 1))
items = AnimatedSprite(items, (4, 1))

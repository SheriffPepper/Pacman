import pygame

from logic import Entity
from load_data import pacman
from logic import UP, DOWN, LEFT, RIGHT


class Pacman(Entity):
    def __init__(self, position: tuple, direction: int) -> None:
        super().__init__(position, direction)
        self.pacman = pacman[direction]

    def next(self) -> None:
        self.pacman = next(self.pacman)

    def update(self, key: int = -1) -> None:
        if key == pygame.K_w:
            self.change_direction(UP)
        elif key == pygame.K_a:
            self.change_direction(LEFT)
        elif key == pygame.K_s:
            self.change_direction(DOWN)
        elif key == pygame.K_d:
            self.change_direction(RIGHT)

        self.pacman = self.pacman[self.direction]

    def draw(self, screen: pygame.Surface) -> None:
        x, y = self.position
        width, height = self.pacman.get_width(), self.pacman.get_height()
        x, y = x - width, y - height

        if x < -(width // 2):
            x = screen.get_width() + width // 2
        elif x > (screen.get_width() + width // 2):
            x = -(width // 2)

        if y < -(height // 2):
            y = screen.get_height() + height // 2
        elif y > (screen.get_height() + height // 2):
            y = -(height // 2)

        self.pacman.move(int(x), int(y))
        self.position = x + width, y + height

        self.pacman.draw(screen)

import pygame

from logic import Entity
from load_data import pacman
from logic import UP, DOWN, LEFT, RIGHT


class Pacman(Entity):
    def __init__(self, position: tuple, direction: int) -> None:
        super().__init__(position, direction)
        self.pacman = pacman

    def update(self, key: int) -> None:
        if key == pygame.K_w:
            self.change_direction(UP)
        elif key == pygame.K_a:
            self.change_direction(LEFT)
        elif key == pygame.K_s:
            self.change_direction(DOWN)
        elif key == pygame.K_d:
            self.change_direction(RIGHT)

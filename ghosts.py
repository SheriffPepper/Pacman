from logic import Entity, UP, DOWN, LEFT, RIGHT
import pygame


HOUSE = 0
CHASE = 1
SCATTER = 2
FRIGHTENED = 3


class Ghost(Entity):
    def __init__(self, position: tuple, direction: int) -> None:
        super().__init__(position, direction)
        self.mode = HOUSE
        self.aim = position

    def set_aim(self, position: tuple) -> None:
        self.aim = position

    def move_to_aim(self) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pass

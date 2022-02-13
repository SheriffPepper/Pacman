from logic import Entity, UP, DOWN, LEFT, RIGHT
from load_data import blinky
from random import randint
import pygame


HOUSE = 0
CHASE = 1
SCATTER = 2
FRIGHTENED = 3


class Ghost(Entity):
    STEP = 2

    def __init__(self, position: tuple, direction: int) -> None:
        super().__init__(position, direction)
        self.mode = HOUSE
        self.aim = position
        self.cell = None
        self.ghost = blinky[self.direction]

    def set_aim(self, position: tuple) -> None:
        self.aim = position

    def move_to_aim(self) -> None:
        x, y = self.position
        cell = self.field.get_cell((int(x), int(y)))
        left, right, up, down = list(map(lambda num: num == '1', bin(cell)[2:].rjust(4, '0')[::-1]))
        count = sum((left, right, up, down))
        cell = (x // self.field.size[0]) % self.field.width, \
               (y // self.field.size[1]) % self.field.height

        # Two ways (usually forward and backward)
        if count == 2:
            left = False if self.direction == RIGHT else left
            right = False if self.direction == LEFT else right
            up = False if self.direction == DOWN else up
            down = False if self.direction == UP else down

            if self.cell != cell:
                self.change_direction([left, right, up, down].index(True))
                self.cell = cell
            return self.forward(self.STEP)
        # Breaking the deadlock
        elif count == 1:
            if self.cell != cell:
                self.cell = cell
            return self.change_direction([left, right, up, down].index(True))
        # Crossroad
        else:
            left = False if self.direction == RIGHT else left
            right = False if self.direction == LEFT else right
            up = False if self.direction == DOWN else up
            down = False if self.direction == UP else down

            aim = (self.aim[0] // self.field.size[0]) % self.field.width, \
                  (self.aim[1] // self.field.size[1]) % self.field.height
            answer = []

            # We can go left
            if left:
                answer.append((LEFT,
                               ((cell[0] - 1 - aim[0]) ** 2 + (cell[1] - aim[1]) ** 2) ** 0.5))
            # We can go right
            if right:
                answer.append((RIGHT,
                               ((cell[0] + 1 - aim[0]) ** 2 + (cell[1] - aim[1]) ** 2) ** 0.5))
            # We can go up
            if up and ((cell not in ((12, 14), (15, 14), (12, 26), (15, 26)) and
                       self.mode != FRIGHTENED) or self.mode == FRIGHTENED):
                answer.append((UP,
                               ((cell[0] - aim[0]) ** 2 + (cell[1] - 1 - aim[1]) ** 2) ** 0.5))
            # We can go down
            if down:
                answer.append((DOWN,
                               ((cell[0] - aim[0]) ** 2 + (cell[1] + 1 - aim[1]) ** 2) ** 0.5))

            if self.cell != cell:
                if self.mode != FRIGHTENED:
                    self.change_direction(min(answer, key=lambda element: element[::-1])[0])
                else:
                    self.change_direction(answer[randint(0, len(answer) - 1)][0])
                self.cell = cell

            return self.forward(self.STEP)

    def change_mode(self, mode: int) -> None:
        if mode == self.mode:
            return

        if mode == CHASE:
            pass
        elif mode == SCATTER:
            pass
        elif mode == FRIGHTENED:
            pass

    def draw(self, screen: pygame.Surface) -> None:
        x, y = self.position
        width, height = self.ghost.get_width(), self.ghost.get_height()

        if x < -(width // 2):
            x = screen.get_width() + width // 2
        elif x > (screen.get_width() + width // 2):
            x = -(width // 2)

        if y < -(height // 2):
            y = screen.get_height() + height // 2
        elif y > (screen.get_height() + height // 2):
            y = -(height // 2)

        self.ghost.move(int(x - width // 2), int(y - height // 2))
        self.position = x, y

        self.ghost.draw(screen)

    def next(self):
        self.ghost = next(self.ghost)


class Blinky(Ghost):
    def __init__(self, position: tuple, direction: int) -> None:
        super().__init__(position, direction)
        self.mode = CHASE  # CHASE FRIGHTENED

    def update(self, pacman) -> None:
        # >:)
        if self.mode == CHASE:
            self.set_aim(pacman.position)
            self.move_to_aim()
        # ))) >:)
        elif self.mode == SCATTER:
            self.set_aim((int(25.5 * self.field.size[0]), int(0.5 * self.field.size[1])))
            self.move_to_aim()
        # ~~~ XoX
        elif self.mode == FRIGHTENED:
            self.set_aim(self.position)
            self.move_to_aim()

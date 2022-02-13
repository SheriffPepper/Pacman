import pygame.draw
from load_data import items

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
WALL = -1
VERTICAL = UP, DOWN
HORIZONTAL = LEFT, RIGHT


class Matrix(object):
    def __init__(self, width: int, height: int, default: int = 0) -> None:
        if width < 1 or height < 1:
            raise TypeError("Can't make non-positive matrix.")

        self.size = self.width, self.height = width, height

        self.matrix = [[default for _ in range(width)] for _ in range(height)]

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.matrix[index // self.width][index % self.width]
        elif isinstance(index, tuple) and len(index) == 2:
            x, y = index
            return self.matrix[y][x]
        elif isinstance(index, slice):
            start = (0, 0) if index.start is None else index.start
            stop = (self.width, self.height) if index.stop is None else index.stop
            step = 1 if index.step is None else index.step

            if isinstance(start, tuple) and isinstance(stop, tuple) and isinstance(step, int):
                matrix = []
                width, height = 0, 0

                for y in range(start[1], stop[1], step):
                    row = []
                    for x in range(start[0], stop[0], step):
                        if x < self.width and y < self.height:
                            row.append(self.matrix[y][x])
                    matrix.append(row)
                    if len(row) > width:
                        width = len(row)

                height = len(matrix)

                matrix_ = Matrix(width, height)
                matrix_.matrix = matrix
                return matrix_
            else:
                raise TypeError("Wrong type for slice index")

        raise IndexError(f"Wrong index {repr(index)} for Matrix.")

    def __setitem__(self, index, value: int) -> None:
        # matrix[x + y * width] = int | float | Matrix(width=1, height=1)
        if isinstance(index, int):
            if isinstance(value, int) or isinstance(value, float):
                self.matrix[index // self.width][index % self.width] = value
            elif isinstance(value, self.__class__) and value.width == value.height == 1:
                self.matrix[index // self.width][index % self.width] = value[0, 0]
        # matrix[x, y] = int | float | Matrix(width=1, height=1)
        elif isinstance(index, tuple) and len(index) == 2:
            x, y = index
            if isinstance(value, int) or isinstance(value, float):
                self.matrix[y][x] = value
            elif isinstance(value, self.__class__) and value.width == value.height == 1:
                self.matrix[y][x] = value[0, 0]
        # matrix[(x1, y1):(x2, y2):step] = int | float | Matrix
        elif isinstance(index, slice):
            start = (0, 0) if index.start is None else index.start
            stop = (self.width, self.height) if index.stop is None else index.stop
            step = 1 if index.step is None else index.step

            if isinstance(value, int) or isinstance(value, float):
                if isinstance(step, int):
                    for y in range(start[1], stop[1], step):
                        for x in range(start[0], stop[0], step):
                            self.matrix[y][x] = value
                elif isinstance(step, tuple) and len(step) == 2:
                    for y in range(start[1], stop[1], step[1]):
                        for x in range(start[0], stop[0], step[0]):
                            self.matrix[y][x] = value
                else:
                    raise TypeError("Wrong type of slice step")
            elif isinstance(value, self.__class__):
                matrix_ = self.__getitem__(index)

                if value.width == value.height == 1:
                    if isinstance(step, int):
                        for y in range(start[1], stop[1], step):
                            for x in range(start[0], stop[0], step):
                                self.matrix[y][x] = value[0, 0]
                    elif isinstance(step, tuple) and len(step) == 2:
                        for y in range(start[1], stop[1], step[1]):
                            for x in range(start[0], stop[0], step[0]):
                                self.matrix[y][x] = value[0, 0]
                    else:
                        raise TypeError("Wrong type of slice step")
                elif value.width == matrix_.width and value.height == matrix_.height:
                    if isinstance(step, int):
                        y_ = 0
                        for y in range(start[1], stop[1], step):
                            x_ = 0
                            for x in range(start[0], stop[0], step):
                                self.matrix[y][x] = value[x_, y_]
                                x_ += 1
                            y_ += 1
                    elif isinstance(step, tuple) and len(step) == 2:
                        y_ = 0
                        for y in range(start[1], stop[1], step[1]):
                            x_ = 0
                            for x in range(start[0], stop[0], step[0]):
                                self.matrix[y][x] = value[x_, y_]
                                x_ += 1
                            y_ += 1
                    else:
                        raise TypeError("Wrong type of slice step")
                else:
                    raise TypeError("Wrong size of the matrix in value.")

    def max(self) -> float:
        return max([max(row) for row in self.matrix])

    def min(self) -> float:
        return min([min(row) for row in self.matrix])

    def __list__(self) -> list:
        return list(map(list.copy, self.matrix))

    def __tuple__(self) -> tuple:
        return tuple(map(tuple, self.matrix))

    def __str__(self) -> str:
        answer = ''
        separator = max(len(str(self.max())), len(str(self.min())))

        for y in range(self.height):
            answer += '[ '
            for x in range(self.width):
                answer += str(self.matrix[y][x]).rjust(separator, ' ') + '  '
            answer = answer.rstrip() + " ]\n"

        return answer


class Entity(object):
    def __init__(self, position: tuple, direction: int) -> None:
        self.position = position
        self.direction = direction
        self.time = 0
        self.queue = None
        self.field = None

    def change_direction(self, direction: int) -> None:
        self.queue = direction

    def set_field(self, field) -> None:
        self.field = field

    def move(self, x: int, y: int) -> None:
        self.position = x, y

    def forward(self, step: float) -> None:
        direction = None
        if self.queue is not None and self.time < 30:
            direction, self.direction = self.direction, self.queue
            self.queue = None
        elif self.queue is not None:
            self.queue = None

        x, y = x1, y1 = self.position

        # Left direction
        if self.direction == LEFT:
            x -= step
            x1 -= step * 2
        # Right direction
        elif self.direction == RIGHT:
            x += step
            x1 += step * 2
        # Up direction
        elif self.direction == UP:
            y -= step
            y1 -= step * 2
        # Down direction
        elif self.direction == DOWN:
            y += step
            y1 += step * 2
        # Zero direction
        else:
            return

        hitbox = [# Upper left
                  (x1 - self.field.size[0] // 2 + step,
                   y1 - self.field.size[1] // 2 + step),
                  # Upper right
                  (x1 + self.field.size[0] // 2 - step,
                   y1 - self.field.size[1] // 2 + step),
                  # Lower left
                  (x1 - self.field.size[0] // 2 + step,
                   y1 + self.field.size[1] // 2 - step),
                  # Lower right
                  (x1 + self.field.size[0] // 2 - step,
                   y1 + self.field.size[1] // 2 - step)]

        collide = False
        for point_x, point_y in hitbox:
            if self.field.get_cell((int(point_x), int(point_y))) is WALL:
                collide = True
                break

        # No wall intersection
        if not collide:
            self.move(x, y)
        # Return old direction
        elif direction is not None:
            queue = self.direction
            self.direction = direction
            self.forward(step)
            self.queue = queue

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, (255, 255, 255, 255),
                           self.position, 16)


class Field(Matrix):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width=28, height=36)
        self.matrix = [
            [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
            [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
            [ 7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 10,  3,  3,  3,  3, 11,  3,  3,  3,  3,  3,  9, -1, -1, 10,  3,  3,  3,  3,  3, 11,  3,  3,  3,  3,  9, -1],
            [-1, 12, -1, -1, -1, -1, 12, -1, -1, -1, -1, -1, 12, -1, -1, 12, -1, -1, -1, -1, -1, 12, -1, -1, -1, -1, 12, -1],
            [-1, 12, -1, -1, -1, -1, 12, -1, -1, -1, -1, -1, 12, -1, -1, 12, -1, -1, -1, -1, -1, 12, -1, -1, -1, -1, 12, -1],
            [-1, 12, -1, -1, -1, -1, 12, -1, -1, -1, -1, -1, 12, -1, -1, 12, -1, -1, -1, -1, -1, 12, -1, -1, -1, -1, 12, -1],
            [-1, 14,  3,  3,  3,  3, 15,  3,  3,  3,  3,  3,  7,  3,  3,  7,  3,  3, 11,  3,  3, 15,  3,  3,  3,  3, 13, -1],
            [-1, 12, -1, -1, -1, -1, 12, -1, -1, 12, -1, -1, -1, -1, -1, -1, -1, -1, 12, -1, -1, 12, -1, -1, -1, -1, 12, -1],
            [-1, 12, -1, -1, -1, -1, 12, -1, -1, 12, -1, -1, -1, -1, -1, -1, -1, -1, 12, -1, -1, 12, -1, -1, -1, -1, 12, -1],
            [-1,  6,  3,  3,  3,  3, 13, -1, -1,  6,  3,  3,  9, -1, -1, 10,  3,  3,  5, -1, -1, 14,  3,  3,  3,  3,  5, -1],
            [-1, -1, -1, -1, -1, -1, 12, -1, -1, -1, -1, -1, 12, -1, -1, 12, -1, -1, -1, -1, -1, 12, -1, -1, -1, -1, -1, -1],
            [11, 11, 11, 11,  9, -1, 12, -1, -1, -1, -1, -1, 12, -1, -1, 12, -1, -1, -1, -1, -1, 12, -1, 10, 11, 11, 11, 11],
            [15, 15, 15, 15, 13, -1, 12, -1, -1, 10,  3,  3,  7,  3,  3,  7,  3,  3,  9, -1, -1, 12, -1, 14, 15, 15, 15, 15],
            [ 7,  7,  7,  7,  5, -1, 12, -1, -1, 12, -1, -1, -1,  4,  4, -1, -1, -1, 12, -1, -1, 12, -1,  6,  7,  7,  7,  7],
            [-1, -1, -1, -1, -1, -1, 12, -1, -1, 12, -1, 10, 11, 15, 15, 11,  9, -1, 12, -1, -1, 12, -1, -1, -1, -1, -1, -1],
            [ 3,  3,  3,  3,  3,  3, 15,  3,  3, 13, -1, 14, 15, 15, 15, 15, 13, -1, 14,  3,  3, 15,  3,  3,  3,  3,  3,  3],
            [-1, -1, -1, -1, -1, -1, 12, -1, -1, 12, -1,  6,  7,  7,  7,  7,  5, -1, 12, -1, -1, 12, -1, -1, -1, -1, -1, -1],
            [11, 11, 11, 11,  9, -1, 12, -1, -1, 12, -1, -1, -1, -1, -1, -1, -1, -1, 12, -1, -1, 12, -1, 10, 11, 11, 11, 11],
            [15, 15, 15, 15, 13, -1, 12, -1, -1, 14,  3,  3,  3,  3,  3,  3,  3,  3, 13, -1, -1, 12, -1, 14, 15, 15, 15, 15],
            [ 7,  7,  7,  7,  5, -1, 12, -1, -1, 12, -1, -1, -1, -1, -1, -1, -1, -1, 12, -1, -1, 12, -1,  6,  7,  7,  7,  7],
            [-1, -1, -1, -1, -1, -1, 12, -1, -1, 12, -1, -1, -1, -1, -1, -1, -1, -1, 12, -1, -1, 12, -1, -1, -1, -1, -1, -1],
            [-1, 10,  3,  3,  3,  3, 15,  3,  3,  7,  3,  3,  9, -1, -1, 10,  3,  3,  7,  3,  3, 15,  3,  3,  3,  3,  9, -1],
            [-1, 12, -1, -1, -1, -1, 12, -1, -1, -1, -1, -1, 12, -1, -1, 12, -1, -1, -1, -1, -1, 12, -1, -1, -1, -1, 12, -1],
            [-1, 12, -1, -1, -1, -1, 12, -1, -1, -1, -1, -1, 12, -1, -1, 12, -1, -1, -1, -1, -1, 12, -1, -1, -1, -1, 12, -1],
            [-1,  6,  3,  9, -1, -1, 14,  3,  3, 11,  3,  3,  7,  3,  3,  7,  3,  3, 11,  3,  3, 13, -1, -1, 10,  3,  5, -1],
            [-1, -1, -1, 12, -1, -1, 12, -1, -1, 12, -1, -1, -1, -1, -1, -1, -1, -1, 12, -1, -1, 12, -1, -1, 12, -1, -1, -1],
            [-1, -1, -1, 12, -1, -1, 12, -1, -1, 12, -1, -1, -1, -1, -1, -1, -1, -1, 12, -1, -1, 12, -1, -1, 12, -1, -1, -1],
            [-1, 10,  3,  7,  3,  3,  5, -1, -1,  6,  3,  3,  9, -1, -1, 10,  3,  3,  5, -1, -1,  6,  3,  3,  7,  3,  9, -1],
            [-1, 12, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 12, -1, -1, 12, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 12, -1],
            [-1, 12, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 12, -1, -1, 12, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 12, -1],
            [-1,  6,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  7,  3,  3,  7,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  5, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11],
            [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]]
        self.energizers = {(1, 6), (26, 6), (1, 26), (26, 26)}
        self.dots = {(1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
                     (7, 4), (8, 4), (9, 4), (10, 4), (11, 4), (12, 4),
                     (15, 4), (16, 4), (17, 4), (18, 4), (19, 4), (20, 4),
                     (21, 4), (22, 4), (23, 4), (24, 4), (25, 4), (26, 4),
                     (1, 5), (6, 5), (12, 5), (15, 5), (21, 5), (26, 5),
                     (6, 6), (12, 6), (15, 6), (21, 6),
                     (1, 7), (6, 7), (12, 7), (15, 7), (21, 7), (26, 7),
                     (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8),
                     (7, 8), (8, 8), (9, 8), (10, 8), (11, 8), (12, 8),
                     (13, 8), (14, 8), (15, 8), (16, 8), (17, 8), (18, 8),
                     (19, 8), (20, 8), (21, 8), (22, 8), (23, 8), (24, 8), (25, 8), (26, 8),
                     (1, 9), (6, 9), (9, 9), (18, 9), (21, 9), (26, 9),
                     (1, 10), (6, 10), (9, 10), (18, 10), (21, 10), (26, 10),
                     (1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (6, 11),
                     (9, 11), (10, 11), (11, 11), (12, 11),
                     (15, 11), (16, 11), (17, 11), (18, 11),
                     (21, 11), (22, 11), (23, 11), (24, 11), (25, 11), (26, 11),
                     (6, 12), (21, 12), (6, 12), (21, 12), (6, 13), (21, 13),
                     (6, 14), (21, 14), (6, 15), (21, 15), (6, 16), (21, 16),
                     (6, 17), (21, 17), (6, 18), (21, 18), (6, 19), (21, 19),
                     (6, 20), (21, 20), (6, 21), (21, 21), (6, 22), (21, 22),
                     (1, 23), (2, 23), (3, 23), (4, 23), (5, 23), (6, 23),
                     (7, 23), (8, 23), (9, 23), (10, 23), (11, 23), (12, 23),
                     (15, 23), (16, 23), (17, 23), (18, 23), (19, 23), (20, 23),
                     (21, 23), (22, 23), (23, 23), (24, 23), (25, 23), (26, 23),
                     (1, 24), (6, 24), (12, 24), (15, 24), (21, 24), (26, 24),
                     (1, 25), (6, 25), (12, 25), (15, 25), (21, 25), (26, 25),
                     (2, 26), (3, 26), (6, 26), (7, 26), (8, 26),
                     (9, 26), (10, 26), (11, 26), (12, 26), (15, 26), (16, 26),
                     (17, 26), (18, 26), (19, 26), (20, 26), (21, 26), (24, 26), (25, 26),
                     (3, 27), (6, 27), (9, 27), (18, 27), (21, 27), (24, 27),
                     (3, 28), (6, 28), (9, 28), (18, 28), (21, 28), (24, 28),
                     (1, 29), (2, 29), (3, 29), (4, 29), (5, 29), (6, 29),
                     (9, 29), (10, 29), (11, 29), (12, 29), (15, 29), (16, 29), (17, 29), (18, 29),
                     (21, 29), (22, 29), (23, 29), (24, 29), (25, 29), (26, 29),
                     (1, 30), (12, 30), (15, 30), (26, 30),
                     (1, 31), (12, 31), (15, 31), (26, 31),
                     (1, 32), (2, 32), (3, 32), (4, 32), (5, 32), (6, 32),
                     (7, 32), (8, 32), (9, 32), (10, 32), (11, 32), (12, 32),
                     (13, 32), (14, 32), (15, 32), (16, 32), (17, 32), (18, 32),
                     (19, 32), (20, 32), (21, 32), (22, 32), (23, 32), (24, 32), (25, 32), (26, 32)}
        self.pixel_width = width
        self.pixel_height = height
        self.size = self.pixel_width // self.width, self.pixel_height // self.height
        self.is_win = False
        self.dead = False

    def get_cell(self, position: tuple) -> int:
        return self[(position[0] // self.size[0]) % self.width,
                    (position[1] // self.size[1]) % self.height]

    def is_wall(self, x: int, y: int) -> bool:
        return self[x, y] is WALL

    def draw(self, screen: pygame.Surface) -> None:
        energizer = items[2, 0]
        width, height = energizer.get_width(), energizer.get_height()

        for x, y in self.energizers:
            x, y = x * self.size[0] + self.size[0] // 2, y * self.size[1] + self.size[1] // 2
            screen.blit(energizer, (int(x - width // 2), int(y - height // 2)))

        dot = items[3, 0]

        for x, y in self.dots:
            x, y = x * self.size[0] + self.size[0] // 2, y * self.size[1] + self.size[1] // 2
            screen.blit(dot, (int(x - width // 2), int(y - height // 2)))

    def update(self, pacman, blinky, pinky, inky, clyde) -> None:
        x, y = pacman.position
        x, y = (x // self.size[0]) % self.width, (y // self.size[1]) % self.height

        if (x, y) in self.dots:
            pacman.score += 10
            self.dots.remove((x, y))
        elif (x, y) in self.energizers:
            pacman.score += 50

            blinky.change_mode(3)
            pinky.change_mode(3)
            inky.change_mode(3)
            clyde.change_mode(3)

            blinky.counter = 300
            pinky.counter = 300
            inky.counter = 300
            clyde.counter = 300

            self.energizers.remove((x, y))

        x1, y1 = blinky.position
        x1, y1 = (x1 // self.size[0]) % self.width, (y1 // self.size[1]) % self.height

        if (x, y) == (x1, y1):
            if blinky.mode == 3:
                blinky.move(228, 280)
                blinky.direction = UP
                blinky.change_mode(0)
            else:
                self.dead = True

        x1, y1 = pinky.position
        x1, y1 = (x1 // self.size[0]) % self.width, (y1 // self.size[1]) % self.height

        if (x, y) == (x1, y1):
            if pinky.mode == 3:
                pinky.move(224, 280)
                pinky.direction = UP
                pinky.change_mode(0)
            else:
                self.dead = True

        x1, y1 = inky.position
        x1, y1 = (x1 // self.size[0]) % self.width, (y1 // self.size[1]) % self.height

        if (x, y) == (x1, y1):
            if inky.mode == 3:
                inky.move(224, 280)
                inky.direction = UP
                inky.change_mode(0)
                inky.tmp = True
            else:
                self.dead = True

        x1, y1 = clyde.position
        x1, y1 = (x1 // self.size[0]) % self.width, (y1 // self.size[1]) % self.height

        if (x, y) == (x1, y1):
            if clyde.mode == 3:
                clyde.move(224, 280)
                clyde.direction = UP
                clyde.change_mode(0)
                clyde.tmp = True
            else:
                self.dead = True

        if pacman.score >= 30 and not inky.tmp:
            inky.tmp = True
            inky.move(224, 280)
            inky.mode = 0

        if pacman.score >= 860 and not clyde.tmp:
            clyde.tmp = True
            clyde.move(224, 280)
            clyde.mode = 0

        if not self.dots and not self.energizers:
            self.is_win = True

    def __del__(self) -> None:
        del self.matrix
        del self.energizers
        del self.dots
        del self.pixel_width
        del self.pixel_height
        del self.size
        del self.is_win


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    entity = Entity((100, 100), RIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    entity.change_direction(UP)
                elif event.key == pygame.K_a:
                    entity.change_direction(LEFT)
                elif event.key == pygame.K_s:
                    entity.change_direction(DOWN)
                elif event.key == pygame.K_d:
                    entity.change_direction(RIGHT)

        screen.fill(0)

        entity.forward(2)
        entity.draw(screen)

        pygame.display.flip()
        clock.tick(60)

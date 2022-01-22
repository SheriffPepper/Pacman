import pygame.draw

import load_data

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3


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

    def change_direction(self, direction: int) -> None:
        self.direction = direction

    def move(self, x: int, y: int) -> None:
        self.position = x, y

    def forward(self, step: int) -> None:
        if self.direction == LEFT:
            self.position = self.position[0] - step, self.position[1]
        elif self.direction == RIGHT:
            self.position = self.position[0] + step, self.position[1]
        elif self.direction == UP:
            self.position = self.position[0], self.position[1] - step
        else:
            self.position = self.position[0], self.position[1] + step

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, (255, 255, 255, 255),
                           self.position, 16)


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

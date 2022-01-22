from logic import Entity, UP, DOWN, LEFT, RIGHT


class Ghost(Entity):
    def __init__(self, position: tuple, direction: int) -> None:
        super().__init__(position, direction)
        self.aim = 0, 0

    def set_aim(self) -> None:
        pass

    def move_to(self, position: tuple) -> None:
        pass

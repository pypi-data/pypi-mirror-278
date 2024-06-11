from typing import List, Tuple

from snake_game.board import Board
from snake_game.direction import Direction


class Snake:

    COLOR_HEAD: str = 'green3'
    COLOR_BODY: str = 'green'

    def __init__(self, board: Board):
        self.board: Board = board
        self.segments: List[Tuple[int, int]] = [
            (self.board.cell_size * 3, self.board.cell_size),
            (self.board.cell_size * 2, self.board.cell_size),
            (self.board.cell_size, self.board.cell_size),
        ]
        self.direction: Direction = Direction.RIGHT
        self.growing: bool = False
    
    @property
    def head(self) -> Tuple[int, int]:
        return self.segments[0]

    def draw(self) -> None:
        for x, y in self.segments:
            self.board.canvas.create_rectangle(
                x,
                y,
                x + self.board.cell_size,
                y + self.board.cell_size,
                fill=self.COLOR_HEAD if (x, y) == self.head else self.COLOR_BODY,
                outline=self.board.COLOR,
                tags='snake',
            )

    def move(self) -> None:
        head_x, head_y = self.head
        if self.direction == Direction.UP:
            head_y -= self.board.cell_size
        elif self.direction == Direction.DOWN:
            head_y += self.board.cell_size
        elif self.direction == Direction.LEFT:
            head_x -= self.board.cell_size
        elif self.direction == Direction.RIGHT:
            head_x += self.board.cell_size

        new_head = (head_x, head_y)
        self.segments.insert(0, new_head)

        if not self.growing:
            self.segments.pop()
        else:
            self.growing = False

    def grow(self) -> None:
        self.growing = True

    def check_collision(self) -> bool:
        head_x, head_y = self.head
        return (
            head_x < 0 or head_x >= self.board.width or
            head_y < 0 or head_y >= self.board.height or
            len(self.segments) != len(set(self.segments))
        )
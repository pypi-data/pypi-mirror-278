import random
from typing import Tuple

from snake_game.board import Board
from snake_game.snake import Snake


class Food:

    COLOR: str = 'red'

    def __init__(self, board: Board) -> None:
        self.board: Board = board
        self.position: Tuple[int, int] = (0, 0)

    def draw(self) -> None:
        x, y = self.position
        self.board.canvas.create_rectangle(
            x,
            y,
            x + self.board.cell_size,
            y + self.board.cell_size,
            fill=self.COLOR,
            outline=self.board.COLOR,
            tags='food',
        )

    def create(self, snake: Snake) -> None:
        available_positions = [
            (x, y) for x in range(0, self.board.width, self.board.cell_size)
            for y in range(0, self.board.height, self.board.cell_size)
            if (x, y) not in snake.segments
        ]
        self.position = random.choice(available_positions)
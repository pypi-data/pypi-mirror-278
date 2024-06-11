from typing import Dict

import tkinter as tk

from snake_game.board import Board
from snake_game.snake import Snake
from snake_game.food import Food
from snake_game.direction import Direction 


class Game:
    WIDTH: int = 400
    HEIGHT: int = 400
    CELL_SIZE: int = 20
    VELOCITY: int = 200 # milliseconds between movements
    DIRECTION_MAPPING: Dict[str, Direction] = {direction.value: direction for direction in Direction}
    UNALLOWED_DIRECTIONS: Dict[Direction, Direction] = {
        Direction.UP: Direction.DOWN,
        Direction.DOWN: Direction.UP,
        Direction.LEFT: Direction.RIGHT,
        Direction.RIGHT: Direction.LEFT
    }

    def __init__(self, master: tk.Tk) -> None:
        self.master: tk.Tk = master
        self.master.resizable(False, False)
        self.master.bind("<KeyPress>", self.change_direction)

        self.board = Board(self.master, self.WIDTH, self.HEIGHT, self.CELL_SIZE)
        self.score = 0

        self.snake = Snake(self.board)
        self.food = Food(self.board)
        self.food.create(self.snake)

        self.running = True
        self.run()

    def draw_board(self) -> None:
        self.board.clear()
        self.snake.draw()
        self.food.draw()
        self.master.title(f"Snake Game - Score: {self.score}")

    def change_direction(self, event: tk.Event) -> None:
        new_direction_str: str = event.keysym
        if new_direction_str in self.DIRECTION_MAPPING and \
           new_direction_str != self.UNALLOWED_DIRECTIONS[self.snake.direction]:
            self.snake.direction = self.DIRECTION_MAPPING[new_direction_str]

    def run(self) -> None:
        if self.running:
            self.snake.move()
            if self.snake.check_collision():
                self.running = False
            elif self.snake.head == self.food.position:
                self.score += 1
                self.food.create(self.snake)
                self.snake.grow()
            self.draw_board()
            self.master.after(self.VELOCITY, self.run)
        else:
            self.board.canvas.create_text(
                self.board.width // 2,
                self.board.height // 2,
                text="GAME OVER",
                fill="white",
                font=("Courier", 30, "bold"),
                tags='gameover',
            )


def run():
    master = tk.Tk()
    game = Game(master)
    master.mainloop()


if __name__ == "__main__":
    run()
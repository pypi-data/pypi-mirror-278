import unittest
import tkinter as tk

from snake_game.board import Board
from snake_game.snake import Snake
from snake_game.direction import Direction


class TestSnake(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.board = Board(self.root, 400, 400, 20)
        self.snake = Snake(self.board)

    def test_initialization(self):
        self.assertEqual(len(self.snake.segments), 3)
        self.assertEqual(self.snake.direction, Direction.RIGHT)
        self.assertFalse(self.snake.growing)

    def test_draw_snake(self):
        self.snake.draw()
        snake_items = self.board.canvas.find_withtag('snake')
        self.assertEqual(len(snake_items), 3)

    def test_head_property(self):
        self.assertEqual(self.snake.head, (60, 20))

    def test_move(self):
        self.snake.move()
        self.assertEqual(self.snake.head, (80, 20))
        self.assertEqual(len(self.snake.segments), 3)

    def test_grow(self):
        self.snake.grow()
        self.assertTrue(self.snake.growing)
        self.snake.move()
        self.assertEqual(len(self.snake.segments), 4)
        self.assertFalse(self.snake.growing)

    def test_check_collision(self):
        self.snake.segments = [(20, 20), (20, 40), (20, 60)]
        self.assertFalse(self.snake.check_collision())
        self.snake.segments = [(20, 20), (20, 40), (20, 60), (20, 20)]
        self.assertTrue(self.snake.check_collision())

    def test_collision_with_wall(self):
        self.snake.segments = [(0, 0)]
        self.snake.direction = Direction.LEFT
        self.snake.move()
        self.assertTrue(self.snake.check_collision())


if __name__ == '__main__':
    unittest.main()

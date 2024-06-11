import unittest
import tkinter as tk

from snake_game.board import Board
from snake_game.food import Food
from snake_game.snake import Snake


class TestFood(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.board = Board(self.root, 400, 400, 20)
        self.food = Food(self.board)
        self.snake = Snake(self.board)

    def test_initialization(self):
        self.assertEqual(self.food.position, (0, 0))

    def test_create_food(self):
        self.food.create(self.snake)
        self.assertNotEqual(self.food.position, (0, 0))
        self.assertNotIn(self.food.position, self.snake.segments)

    def test_draw_food(self):
        self.food.create(self.snake)
        self.food.draw()
        food_items = self.board.canvas.find_withtag('food')
        self.assertEqual(len(food_items), 1)


if __name__ == '__main__':
    unittest.main()

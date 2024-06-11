import unittest
import tkinter as tk

from snake_game.main import Game


class TestGame(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.game = Game(self.root)

    def test_initialization(self):
        self.assertTrue(self.game.running)
        self.assertEqual(self.game.score, 0)
        self.assertIsNotNone(self.game.snake)
        self.assertIsNotNone(self.game.food)

    def test_change_direction(self):
        event = tk.Event()
        event.keysym = 'Left'
        self.game.change_direction(event)
        self.assertEqual(self.game.snake.direction, self.game.DIRECTION_MAPPING['Left'])


if __name__ == '__main__':
    unittest.main()

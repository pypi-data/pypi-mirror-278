import unittest
import tkinter as tk

from snake_game.board import Board


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.board = Board(self.root, 400, 400, 20)

    def test_initialization(self):
        self.assertEqual(self.board.width, 400)
        self.assertEqual(self.board.height, 400)
        self.assertEqual(self.board.cell_size, 20)
        self.assertEqual(self.board.canvas['bg'], 'black')

    def test_clear(self):
        self.board.canvas.create_rectangle(10, 10, 20, 20, fill="green")
        self.board.clear()
        self.assertEqual(len(self.board.canvas.find_all()), 0)


if __name__ == '__main__':
    unittest.main()

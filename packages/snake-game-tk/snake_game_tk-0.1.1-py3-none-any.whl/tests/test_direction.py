import unittest

from snake_game.direction import Direction


class TestDirection(unittest.TestCase):

    def test_enum_values(self):
        self.assertEqual(Direction.UP.value, "Up")
        self.assertEqual(Direction.DOWN.value, "Down")
        self.assertEqual(Direction.LEFT.value, "Left")
        self.assertEqual(Direction.RIGHT.value, "Right")


if __name__ == '__main__':
    unittest.main()

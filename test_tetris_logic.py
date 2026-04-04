import unittest
from tetris import Board, Tetromino

class TestTetrisLogic(unittest.TestCase):
    def test_tetromino_rotation(self):
        t = Tetromino('T')
        initial_shape = t.shape[t.rotation]

        t.rotate()
        self.assertNotEqual(t.shape[t.rotation], initial_shape)

        t.rotate()
        t.rotate()
        t.rotate()
        self.assertEqual(t.shape[t.rotation], initial_shape)

    def test_board_collision(self):
        board = Board(10, 20)
        # Use 'I' shape which has blocks at x=0 in rotation 0: [(0, 1), (1, 1), (2, 1), (3, 1)]
        t = Tetromino('I')
        t.x = 0
        t.y = 0

        # Initial position should be valid
        self.assertTrue(board.is_valid_position(t))

        # Move outside left boundary (x-1 = -1)
        self.assertFalse(board.is_valid_position(t, dx=-1))

        # Move outside right boundary (I shape width is 4, max x index is 3)
        # at x=6, occupies 6,7,8,9 (valid)
        t.x = 6
        self.assertTrue(board.is_valid_position(t))
        # at x=7, occupies 7,8,9,10 (invalid)
        t.x = 7
        self.assertFalse(board.is_valid_position(t))

        # Move below floor
        # I shape height is 2 (y indices 1), so y=18 occupies 19. valid.
        # Wait, 'I' shape rotation 0 is horizontal line at y=1.
        # [(0, 1), (1, 1), (2, 1), (3, 1)]
        # So at t.y=18, block y is 19. Valid.
        t.x = 0
        t.y = 18
        self.assertTrue(board.is_valid_position(t))

        t.y = 19 # Occupies 19, 20. 20 is invalid.
        self.assertFalse(board.is_valid_position(t))

    def test_line_clearing(self):
        board = Board(10, 20)

        # Fill bottom row except one cell
        for x in range(9):
            board.grid[19][x] = 1

        self.assertEqual(board.clear_lines(), 0)

        # Fill the last cell
        board.grid[19][9] = 1
        self.assertEqual(board.clear_lines(), 1)

        # Check if line is cleared (moved down and new empty line at top)
        self.assertEqual(sum(board.grid[0]), 0)
        self.assertEqual(sum(board.grid[19]), 0) # Should be empty as it was cleared and upper lines were empty

    def test_score_calculation(self):
        board = Board(10, 20)

        # Simulate clearing 4 lines (Tetris)
        board.grid[16] = [1] * 10
        board.grid[17] = [1] * 10
        board.grid[18] = [1] * 10
        board.grid[19] = [1] * 10

        lines = board.clear_lines()
        self.assertEqual(lines, 4)
        self.assertEqual(board.score, 800) # Level 1 * 800

if __name__ == '__main__':
    unittest.main()

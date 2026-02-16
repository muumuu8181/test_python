"""
Tetris - The Ultimate Python Curses Edition
Created by Jules (AI Assistant)

Features:
- Full color support
- Ghost piece for drop prediction
- Hold functionality (Press 'C')
- Next piece preview
- Level progression and Scoring system
- Visual effects for line clearing
- Smooth input handling

Controls:
- Arrow Keys: Move and Rotate
- Space: Hard Drop
- Down: Soft Drop
- C: Hold Piece
- P: Pause
- Q: Quit
"""
import random
import copy
import curses
import time

# Tetromino shapes
SHAPES = {
    'I': [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
        [(0, 2), (1, 2), (2, 2), (3, 2)],
        [(1, 0), (1, 1), (1, 2), (1, 3)]
    ],
    'J': [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)]
    ],
    'L': [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)]
    ],
    'O': [
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)]
    ],
    'S': [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
        [(1, 1), (2, 1), (0, 2), (1, 2)],
        [(0, 0), (0, 1), (1, 1), (1, 2)]
    ],
    'T': [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)]
    ],
    'Z': [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (1, 2), (2, 2)],
        [(0, 0), (0, 1), (1, 1), (0, 2)]
    ]
}

# Colors mapping (will be used with curses later)
COLORS = {
    'I': 1,  # Cyan
    'J': 2,  # Blue
    'L': 3,  # Orange
    'O': 4,  # Yellow
    'S': 5,  # Green
    'T': 6,  # Purple
    'Z': 7   # Red
}

class Tetromino:
    def __init__(self, shape_key=None):
        if shape_key is None:
            self.shape_key = random.choice(list(SHAPES.keys()))
        else:
            self.shape_key = shape_key

        self.shape = SHAPES[self.shape_key]
        self.color = COLORS[self.shape_key]
        self.rotation = 0
        self.x = 3  # Initial x position
        self.y = 0  # Initial y position

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

    def rotate_back(self):
        self.rotation = (self.rotation - 1) % len(self.shape)

    def get_blocks(self):
        return [(x + self.x, y + self.y) for x, y in self.shape[self.rotation]]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


class Board:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.score = 0
        self.lines_cleared = 0
        self.level = 1

    def is_valid_position(self, tetromino, dx=0, dy=0, rotation=None):
        if rotation is None:
            rotation = tetromino.rotation

        # Calculate potential block positions
        # shape is list of rotations, each rotation is list of (x,y)
        shape_coords = tetromino.shape[rotation]
        blocks = [(x + tetromino.x + dx, y + tetromino.y + dy)
                  for x, y in shape_coords]

        for x, y in blocks:
            # Check walls and floor
            if x < 0 or x >= self.width or y >= self.height:
                return False
            # Check collision with existing blocks
            # Only check if y is within the grid (y < 0 means above board, which is valid for movement but not for placement usually)
            if y >= 0:
                if self.grid[y][x] != 0:
                    return False
        return True

    def place_tetromino(self, tetromino):
        for x, y in tetromino.get_blocks():
            if 0 <= y < self.height and 0 <= x < self.width:
                self.grid[y][x] = tetromino.color

    def get_completed_lines(self):
        return [i for i, row in enumerate(self.grid) if all(cell != 0 for cell in row)]

    def clear_lines(self):
        lines_to_clear = self.get_completed_lines()
        num_lines = len(lines_to_clear)

        if num_lines > 0:
            # Remove lines
            # Must remove from bottom to top to keep indices valid, but here we just rebuild the grid logic
            # Actually, `del self.grid[i]` shifts indices, so we need to be careful if we iterate
            # But the previous implementation `for i in lines_to_clear` worked because `lines_to_clear` contains indices
            # However, if we delete row 19, then row 18 becomes 19. If we also need to delete 18, its index changed?
            # No, `del` shifts subsequent elements.
            # So if we have [18, 19] to delete. Delete 18 -> 19 becomes 18. Delete 19 (original) which is now at 18?
            # It's safer to delete from original grid logic or reconstruct.

            new_grid = [row for i, row in enumerate(self.grid) if i not in lines_to_clear]
            lines_added = [[0 for _ in range(self.width)] for _ in range(num_lines)]
            self.grid = lines_added + new_grid

            self.lines_cleared += num_lines
            # Basic scoring: 100, 300, 500, 800
            scores = [0, 100, 300, 500, 800]
            self.score += scores[num_lines] * self.level

            # Level up every 10 lines
            self.level = 1 + (self.lines_cleared // 10)

        return num_lines

class TetrisGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.board = Board()
        self.tetromino = Tetromino()
        self.next_tetromino = Tetromino()
        self.hold_tetromino = None
        self.can_hold = True
        self.game_over = False
        self.paused = False

        # Curses setup
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        self.stdscr.timeout(10) # 100 FPS roughly

        # Color initialization
        curses.start_color()
        curses.use_default_colors()
        for i in range(1, 8):
            curses.init_pair(i, i, -1) # Foreground color, default background

        # White for borders
        curses.init_pair(8, curses.COLOR_WHITE, -1)
        # Ghost piece color (dim white)
        curses.init_pair(9, curses.COLOR_WHITE, -1)

        self.last_fall_time = time.time()
        self.fall_speed = 1.0 # Seconds per drop

    def reset(self):
        self.board = Board()
        self.tetromino = Tetromino()
        self.next_tetromino = Tetromino()
        self.hold_tetromino = None
        self.can_hold = True
        self.game_over = False
        self.paused = False
        self.last_fall_time = time.time()
        self.update_speed()

    def update_speed(self):
        # Speed increases with level
        # Level 1: 1.0s, Level 10: 0.1s
        self.fall_speed = max(0.1, 1.0 - (self.board.level - 1) * 0.1)

    def flash_lines(self, lines):
        # Determine offset
        height, width = self.stdscr.getmaxyx()
        board_h, board_w = self.board.height, self.board.width
        offset_y = (height - board_h) // 2
        offset_x = (width - board_w * 2) // 2

        # Draw lines in white
        for y in lines:
            for x in range(self.board.width):
                self.draw_block(y, x, 8, offset_y, offset_x, char="[]", attr=curses.A_BOLD | curses.A_REVERSE)
        self.stdscr.refresh()
        time.sleep(0.1)

    def show_start_screen(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        title = [
            "T E T R I S",
            "",
            "Controls:",
            "Left/Right: Move",
            "Up: Rotate",
            "Down: Soft Drop",
            "Space: Hard Drop",
            "C: Hold",
            "P: Pause",
            "Q: Quit",
            "",
            "Press Any Key to Start"
        ]
        for i, line in enumerate(title):
            try:
                self.stdscr.addstr(h // 2 - len(title) // 2 + i, w // 2 - len(line) // 2, line, curses.A_BOLD)
            except curses.error:
                pass
        self.stdscr.refresh()
        self.stdscr.nodelay(False) # Wait for input
        self.stdscr.getch()
        self.stdscr.nodelay(True) # Back to non-blocking

    def show_game_over(self):
        self.stdscr.nodelay(False)
        h, w = self.stdscr.getmaxyx()
        msg = f"GAME OVER - Score: {self.board.score}"
        try:
            self.stdscr.addstr(h // 2, w // 2 - len(msg) // 2, msg, curses.A_BOLD | curses.color_pair(7))
            self.stdscr.addstr(h // 2 + 2, w // 2 - 14, "Press R to Restart, Q to Quit")
        except curses.error:
            pass
        self.stdscr.refresh()

        while True:
            key = self.stdscr.getch()
            if key == ord('q') or key == ord('Q'):
                return False # Quit
            if key == ord('r') or key == ord('R'):
                return True # Restart

    def get_ghost_position(self):
        ghost = copy.deepcopy(self.tetromino)
        while self.board.is_valid_position(ghost, dy=1):
            ghost.move(0, 1)
        return ghost

    def hold_piece(self):
        if not self.can_hold:
            return

        current_shape = self.tetromino.shape_key

        if self.hold_tetromino is None:
            self.hold_tetromino = Tetromino(current_shape)
            self.tetromino = self.next_tetromino
            self.next_tetromino = Tetromino()
        else:
            # Swap
            held_shape = self.hold_tetromino.shape_key
            self.hold_tetromino = Tetromino(current_shape)
            self.tetromino = Tetromino(held_shape)

        self.can_hold = False

    def handle_input(self):
        try:
            key = self.stdscr.getch()
        except curses.error:
            return

        if key == -1:
            return

        if key == ord('q'):
            self.game_over = True
            return

        if key == ord('p'):
            self.paused = not self.paused
            return

        if self.paused:
            return

        if key == ord('c') or key == ord('C'):
            self.hold_piece()
            return

        if key == curses.KEY_LEFT:
            if self.board.is_valid_position(self.tetromino, dx=-1):
                self.tetromino.move(-1, 0)
        elif key == curses.KEY_RIGHT:
            if self.board.is_valid_position(self.tetromino, dx=1):
                self.tetromino.move(1, 0)
        elif key == curses.KEY_DOWN:
            if self.board.is_valid_position(self.tetromino, dy=1):
                self.tetromino.move(0, 1)
        elif key == curses.KEY_UP:
            self.tetromino.rotate()
            if not self.board.is_valid_position(self.tetromino):
                # Simple wall kick: try moving left or right
                if self.board.is_valid_position(self.tetromino, dx=1):
                    self.tetromino.move(1, 0)
                elif self.board.is_valid_position(self.tetromino, dx=-1):
                    self.tetromino.move(-1, 0)
                else:
                    self.tetromino.rotate_back()
        elif key == ord(' '): # Hard drop
            while self.board.is_valid_position(self.tetromino, dy=1):
                self.tetromino.move(0, 1)
            # Force immediate lock
            self.last_fall_time = 0

    def update(self):
        if self.paused or self.game_over:
            return

        current_time = time.time()
        if current_time - self.last_fall_time > self.fall_speed:
            if self.board.is_valid_position(self.tetromino, dy=1):
                self.tetromino.move(0, 1)
            else:
                self.board.place_tetromino(self.tetromino)

                completed_lines = self.board.get_completed_lines()
                if completed_lines:
                    self.draw() # Draw current state first
                    self.flash_lines(completed_lines)
                    self.board.clear_lines()

                self.update_speed()
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino()
                self.can_hold = True # Reset hold capability

                if not self.board.is_valid_position(self.tetromino):
                    self.game_over = True

            self.last_fall_time = current_time

    def draw_block(self, y, x, color_idx, offset_y=0, offset_x=0, char="[]", attr=0):
        try:
            # Draw two characters for a square look
            # Ensure we are within screen bounds
            h, w = self.stdscr.getmaxyx()
            draw_y = offset_y + y
            draw_x = offset_x + x * 2
            if 0 <= draw_y < h and 0 <= draw_x < w - 1:
                self.stdscr.addstr(draw_y, draw_x, char, curses.color_pair(color_idx) | attr)
        except curses.error:
            pass

    def draw(self):
        self.stdscr.erase()

        # Calculate center position
        height, width = self.stdscr.getmaxyx()
        board_h, board_w = self.board.height, self.board.width

        offset_y = (height - board_h) // 2
        offset_x = (width - board_w * 2) // 2

        # Draw border
        try:
            for y in range(board_h + 2):
                self.stdscr.addstr(offset_y - 1 + y, offset_x - 2, "|", curses.color_pair(8))
                self.stdscr.addstr(offset_y - 1 + y, offset_x + board_w * 2, "|", curses.color_pair(8))

            self.stdscr.addstr(offset_y - 1, offset_x - 2, "+" + "-" * (board_w * 2) + "+", curses.color_pair(8))
            self.stdscr.addstr(offset_y + board_h, offset_x - 2, "+" + "-" * (board_w * 2) + "+", curses.color_pair(8))
        except curses.error:
            pass

        # Draw grid
        for y, row in enumerate(self.board.grid):
            for x, cell in enumerate(row):
                if cell != 0:
                    self.draw_block(y, x, cell, offset_y, offset_x)

        # Draw ghost tetromino
        ghost = self.get_ghost_position()
        for x, y in ghost.get_blocks():
            if y >= 0:
                self.draw_block(y, x, 9, offset_y, offset_x, char="..", attr=curses.A_DIM)

        # Draw current tetromino
        for x, y in self.tetromino.get_blocks():
            if y >= 0:
                self.draw_block(y, x, self.tetromino.color, offset_y, offset_x)

        # Draw Next Piece
        next_offset_x = offset_x + board_w * 2 + 4
        self.stdscr.addstr(offset_y, next_offset_x, "NEXT", curses.A_BOLD)
        for x, y in self.next_tetromino.get_blocks():
            rel_x = x - self.next_tetromino.x
            rel_y = y - self.next_tetromino.y
            self.draw_block(rel_y + 2, rel_x, self.next_tetromino.color, offset_y, next_offset_x)

        # Draw Hold Piece
        hold_offset_x = offset_x - 10
        self.stdscr.addstr(offset_y, hold_offset_x, "HOLD", curses.A_BOLD)
        if self.hold_tetromino:
            for x, y in self.hold_tetromino.get_blocks():
                # For hold piece, we also need to normalize position
                # Since hold piece retains its x,y, we need to shift it to 0,0 relative
                rel_x = x - self.hold_tetromino.x
                rel_y = y - self.hold_tetromino.y
                # Sometimes x,y might be far off if it was swapped from board position
                # So we should probably just use the shape definition directly
                # But get_blocks uses current x,y.
                # Actually, when we hold, we reset x,y to 3,0 in hold_piece logic.
                # But wait, hold_piece sets x=3, y=0.
                rel_x = x - 3
                rel_y = y
                self.draw_block(rel_y + 2, rel_x + 1, self.hold_tetromino.color, offset_y, hold_offset_x)

        # Draw Score and Level
        self.stdscr.addstr(offset_y + 8, next_offset_x, f"SCORE: {self.board.score}")
        self.stdscr.addstr(offset_y + 10, next_offset_x, f"LEVEL: {self.board.level}")
        self.stdscr.addstr(offset_y + 12, next_offset_x, f"LINES: {self.board.lines_cleared}")

        if self.paused:
            self.stdscr.addstr(height // 2, width // 2 - 3, "PAUSED", curses.A_BOLD | curses.A_BLINK)

        if self.game_over:
            self.stdscr.addstr(height // 2, width // 2 - 5, "GAME OVER", curses.A_BOLD | curses.color_pair(7))

        self.stdscr.refresh()

    def run(self):
        self.show_start_screen()
        while True:
            while not self.game_over:
                self.handle_input()
                self.update()
                self.draw()

            if not self.show_game_over():
                break

            self.reset()
            # Restore nodelay after game over screen
            self.stdscr.nodelay(True)

def main(stdscr):
    game = TetrisGame(stdscr)
    game.run()

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass

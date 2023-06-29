import random

class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_open = False
        self.is_marked = False
        self.adjacent_mines = 0

class Minesweeper:
    def __init__(self, size, num_mines):
        self.size = size
        self.num_mines = num_mines
        self.board = [[Cell() for _ in range(size)] for _ in range(size)]
        self.game_over = False

    def generate_mines(self, start_row, start_col):
        positions = random.sample(range(self.size * self.size), self.num_mines)
        for pos in positions:
            row = pos // self.size
            col = pos % self.size
            if row == start_row and col == start_col:
                continue
            self.board[row][col].is_mine = True

    def calculate_adjacent_mines(self):
        for row in range(self.size):
            for col in range(self.size):
                cell = self.board[row][col]
                if not cell.is_mine:
                    count = 0
                    for r in range(max(0, row - 1), min(row + 2, self.size)):
                        for c in range(max(0, col - 1), min(col + 2, self.size)):
                            if self.board[r][c].is_mine:
                                count += 1
                    cell.adjacent_mines = count

    def is_valid_position(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def is_game_won(self):
        for row in range(self.size):
            for col in range(self.size):
                cell = self.board[row][col]
                if not cell.is_mine and not cell.is_open:
                    return False
        return True

    def print_board(self, show_mines=False):
        for row in range(self.size):
            for col in range(self.size):
                cell = self.board[row][col]
                if show_mines and cell.is_mine:
                    print('M', end=' ')
                elif cell.is_open:
                    if cell.is_mine:
                        print('*', end=' ')
                    elif cell.adjacent_mines > 0:
                        print(cell.adjacent_mines, end=' ')
                    else:
                        print('.', end=' ')
                elif cell.is_marked:
                    print('P', end=' ')
                else:
                    print('#', end=' ')
            print()

    def open_cell(self, row, col):
        cell = self.board[row][col]
        if cell.is_open or cell.is_marked:
            return

        cell.is_open = True

        if cell.is_mine:
            self.game_over = True
            self.print_board(show_mines=True)
            print('Game Over! You hit a mine.')
            return

        if cell.adjacent_mines == 0:
            self.open_adjacent_cells(row, col)

        if self.is_game_won():
            self.game_over = True
            self.print_board(show_mines=True)
            print('Congratulations! You won the game.')

    def toggle_marked(self, row, col):
        cell = self.board[row][col]
        if cell.is_open:
            return

        if cell.is_marked:
            cell.is_marked = False
            self.num_mines += 1
        elif self.num_mines > 0:
            cell.is_marked = True
            self.num_mines -= 1

    def open_adjacent_cells(self, row, col):
        for r in range(max(0, row - 1), min(row + 2, self.size)):
            for c in range(max(0, col - 1), min(col + 2, self.size)):
                if not self.board[r][c].is_open:
                    self.open_cell(r, c)

def get_valid_integer_input(prompt, lower_bound, upper_bound):
    while True:
        try:
            value = int(input(prompt))
            if lower_bound <= value <= upper_bound:
                return value
            print('Invalid input. Please enter a valid integer within the specified range.')
        except ValueError:
            print('Invalid input. Please enter a valid integer.')

def play_minesweeper():
    size = get_valid_integer_input("Enter the number of lines on the board: ", 2, 100)
    max_mines = size * size // 2
    num_mines = get_valid_integer_input(f"Enter the number of mines (1 to {max_mines}): ", 1, max_mines)

    game = Minesweeper(size, num_mines)
    start_row = get_valid_integer_input(f"Enter the starting row (0 to {size-1}): ", 0, size-1)
    start_col = get_valid_integer_input(f"Enter the starting column (0 to {size-1}): ", 0, size-1)
    game.generate_mines(start_row, start_col)
    game.calculate_adjacent_mines()

    while not game.game_over:
        game.print_board()
        row = get_valid_integer_input("Enter the row (0 to {}): ".format(size-1), 0, size-1)
        col = get_valid_integer_input("Enter the column (0 to {}): ".format(size-1), 0, size-1)
        action = input("Enter 'open', 'mark', or 'unmark': ").lower()
        if action == 'open':
            game.open_cell(row, col)
        elif action == 'mark':
            game.toggle_marked(row, col)
        elif action == 'unmark':
            game.toggle_marked(row, col)
        else:
            print('Invalid action. Please enter a valid action.')

play_minesweeper()

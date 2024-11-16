class Game:
    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]  # 6 rows, 7 columns
        self.current_player = 'X'  # Player 1 starts. Player 1 = X, Player 2 = O.
        self.status = 'IN_PROGRESS' # In progress, player1 won, player2 won, or draw

    def is_valid_move(self, column):
        # Check if a move is valid (e.g., column is not full)
        # A move is valid if the top row of the column is empty
        return self.board[0][column] == ' '

    def make_move(self, column):
        # Place the current player's piece in the chosen column
        row = self.get_next_open_row(column)
        if row is None:
            return None
        else:
            self.board[row][column] = self.current_player
            # Check for a win before switching players
            self.check_win()
            if self.status == 'IN_PROGRESS':
                self.switch_player()
            return True

    # Find the bottom-most open row in the selected column
    # To drop the piece
    def get_next_open_row(self, column):
        # Loop over rows from bottom to top
        for row in range(5, -1, -1):  # 5 is the bottom-most row
            if self.board[row][column] == ' ':  # Check if the cell is empty
                return row
        return None  # Return None if the column is full

    def check_win(self):
        # Check if a player has won if there are 4 consecutive pieces
        # Loop through the board for each direction
        # Check every row (horizontal)
        for row in range(6):
            for col in range(4):  # Only need to check until column 3 for horizontal 4-in-a-row
                if self.board[row][col] == self.current_player and \
                        self.board[row][col] == self.board[row][col + 1] and \
                        self.board[row][col] == self.board[row][col + 2] and \
                        self.board[row][col] == self.board[row][col + 3]:
                    if self.current_player == 'X':
                        self.status = 'PLAYER1_WON'
                    else:
                        self.status = 'PLAYER2_WON'
                    return

        # Check every column (vertical)
        for col in range(7):
            for row in range(3):  # Only need to check until row 2 for vertical 4-in-a-row
                if self.board[row][col] == self.current_player and \
                        self.board[row][col] == self.board[row + 1][col] and \
                        self.board[row][col] == self.board[row + 2][col] and \
                        self.board[row][col] == self.board[row + 3][col]:
                    if self.current_player == 'X':
                        self.status = 'PLAYER1_WON'
                    else:
                        self.status = 'PLAYER2_WON'
                    return

        # Check diagonal bottom-left to top-right
        for row in range(3, 6):  # Only need to start from row 3 to row 5 for bottom-left to top-right
            for col in range(4):  # Only need to check until column 3 for diagonal 4-in-a-row
                if self.board[row][col] == self.current_player and \
                        self.board[row][col] == self.board[row - 1][col + 1] and \
                        self.board[row][col] == self.board[row - 2][col + 2] and \
                        self.board[row][col] == self.board[row - 3][col + 3]:
                    if self.current_player == 'X':
                        self.status = 'PLAYER1_WON'
                    else:
                        self.status = 'PLAYER2_WON'
                    return

        # Check diagonal top-left to bottom-right
        for row in range(3):  # Only need to check until row 2 for top-left to bottom-right
            for col in range(4):  # Only need to check until column 3 for diagonal 4-in-a-row
                if self.board[row][col] == self.current_player and \
                        self.board[row][col] == self.board[row + 1][col + 1] and \
                        self.board[row][col] == self.board[row + 2][col + 2] and \
                        self.board[row][col] == self.board[row + 3][col + 3]:
                    if self.current_player == 'X':
                        self.status = 'PLAYER1_WON'
                    else:
                        self.status = 'PLAYER2_WON'
                    return
        return

    def check_draw(self):
        # Loss if board is full and there was no winner
        if ' ' not in self.board and self.status == 'IN_PROGRESS':
            self.status = 'DRAW'

    def reset_game(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.current_player = 'X'  # Reset to Player 1's turn
        self.status = 'IN_PROGRESS'

    def switch_player(self):
        # Switch between players
        self.current_player = 'O' if self.current_player == 'X' else 'X'

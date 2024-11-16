class Game:
    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]  # 6 rows, 7 columns
        self.current_player = 'X'  # Player 1 starts. Player 1 = X, Player 2 = O.

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
            self.switch_player()

    # Find the bottom-most open row in the selected column
    # To drop the piece
    def get_next_open_row(self, column):
        # Loop over rows from bottom to top
        for row in range(5, -1, -1):  # 5 is the bottom-most row
            if self.board[row][column] == ' ':  # Check if the cell is empty
                return row
        return None  # Return None if the column is full

    def check_win(self):
        # Check if the current player has won
        pass

    def reset_game(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.current_player = 'X'  # Reset to Player 1's turn

    def switch_player(self):
        # Switch between players
        self.current_player = 'O' if self.current_player == 'X' else 'X'

class Game:
    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]  # 6 rows, 7 columns
        self.current_player = 'X'  # Player 1 starts

    def is_valid_move(self, column):
        # Check if a move is valid (e.g., column is not full)
        pass

    def make_move(self, column):
        # Place the current player's disc in the chosen column
        pass

    def check_win(self):
        # Check if the current player has won
        pass

    def switch_player(self):
        # Switch between players
        self.current_player = 'O' if self.current_player == 'X' else 'X'
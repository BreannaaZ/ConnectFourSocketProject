import socket
import threading
import pickle

# Game constants
ROWS = 6
COLS = 7
EMPTY = '.'
PLAYER1 = 'X'  # Player 1 = X = Red
PLAYER2 = 'O'  # Player 2 = O = Yellow


# The ConnectFourGame class holds the game instance and holds the game controller logic
class ConnectFourGame:
    def __init__(self):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = PLAYER1  # AKA PLAYER X / RED
        self.status = "WAITING"  # WAITING, IN_PROGRESS, X_WON, O_WON, DRAW

    def is_valid_move(self, column):
        # Check if the move is valid if the passed in column is within the range of cols
        # and the top of that column is empty
        return 0 <= column < COLS and self.board[0][column] == EMPTY

    def make_move(self, column):
        # Make the move by iterating through the chosen column
        # to find the bottom most row to place the piece
        # (Iterates from bottom up of board)
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][column] == EMPTY:
                self.board[row][column] = self.current_player
                break

        # Check if this move wins the game
        if self.check_win():
            self.status = f"{self.current_player}_WON"
        elif all(self.board[0][col] != EMPTY for col in range(COLS)):
            self.status = "DRAW"
        else:
            # Switch turns
            self.current_player = PLAYER1 if self.current_player == PLAYER2 else PLAYER2

    def check_win(self):
        # Check for a win condition for the four possible directions (vertical, horizontal, and 2 diagonal)
        # directions holds (row change, column change)
        # (0, 1) = horizontal, left to right
        # (1, 0) = vertical, top down
        # (1, 1) = diagonal, top left to bottom right
        # (1, -1) = diagonal, bottom left to top right
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        # Loop through every cell in the board
        for row in range(ROWS):
            for col in range(COLS):
                # Skip empty cells
                if self.board[row][col] == EMPTY:
                    continue
                # Check all four directions from a non-empty cell
                # To check if 4 pieces connect in that direction
                for dr, dc in directions:
                    if self.is_winning_line(row, col, dr, dc):
                        return True  # Winning connection found
        return False  # No winning connection

    def is_winning_line(self, row, col, dr, dc):
        # Check if there are 4 pieces in a line from the piece at (row, col)
        # in the given direction (row direction, column direction)
        piece = self.board[row][col]
        for i in range(1, 4):
            r, c = row + dr * i, col + dc * i
            # Check that index is within board range, if not quit
            # Check that pieces are same type, if not quit
            if not (0 <= r < ROWS and 0 <= c < COLS) or self.board[r][c] != piece:
                return False  # No winning connection
        return True  # Winning connection found


# The GameServer class handles setting up the server to receive and send data to the clients
class GameServer:
    def __init__(self, host="192.168.1.204", port=5555):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)
        print("Server started. Waiting for players...")
        self.clients = []
        self.game = ConnectFourGame()
        self.lock = threading.Lock()

    def handle_client(self, client_socket, player_id):
        client_socket.send(pickle.dumps({"player_id": player_id, "status": "WAITING"}))

        # Wait for game to start
        while self.game.status == "WAITING":
            pass

        while self.game.status == "IN_PROGRESS":
            try:
                # Receive the move from client
                move = pickle.loads(client_socket.recv(1024))
                column = move.get("column")
                print(f"Server received move at col: ${column}")

                # Process move if valid
                with self.lock:  # To avoid race conditions
                    if self.game.current_player == (PLAYER1 if player_id == 1 else PLAYER2) and self.game.is_valid_move(
                            column):
                        self.game.make_move(column)
                        self.broadcast_game_state()
                    else:
                        client_socket.send(pickle.dumps({"error": "Invalid move or not your turn"}))
            except Exception as e:
                print(f"Error handling player {player_id}: {e}")
                break

        # Close socket
        client_socket.close()

    def broadcast_game_state(self):
        # Send the current game state to both clients, with the board, current players turn, and status
        game_state = {
            "board": self.game.board,
            "current_player": self.game.current_player,
            "status": self.game.status
        }
        for client in self.clients:
            client.send(pickle.dumps(game_state))
        print(f"Sent board: ${self.game.board}, current player: ${self.game.current_player}, "
              f"status: ${self.game.status}")

    def start(self):
        # Accept two clients / players
        while len(self.clients) < 2:
            client_socket, _ = self.server_socket.accept()
            player_id = len(self.clients) + 1
            print(f"Player {player_id} connected.")
            self.clients.append(client_socket)
            # Start a thread for each client
            threading.Thread(target=self.handle_client, args=(client_socket, player_id)).start()

        # Start the game
        print("Start game")
        with self.lock: # To avoid race conditions
            self.game.status = "IN_PROGRESS"
        self.broadcast_game_state()


if __name__ == "__main__":
    server = GameServer()
    server.start()

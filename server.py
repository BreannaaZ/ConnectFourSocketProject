import socket
import threading
import pickle

# Game constants
ROWS = 6
COLS = 7
EMPTY = '.'
PLAYER1 = 'X'
PLAYER2 = 'O'

class ConnectFourGame:
    def __init__(self):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = PLAYER1
        self.status = "WAITING"  # Game states: WAITING, IN_PROGRESS, PLAYER1_WON, PLAYER2_WON, DRAW

    def is_valid_move(self, column):
        return 0 <= column < COLS and self.board[0][column] == EMPTY

    def make_move(self, column):
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
            self.current_player = PLAYER1 if self.current_player == PLAYER2 else PLAYER2

    def check_win(self):
        """Check for a win condition (horizontally, vertically, diagonally)."""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == EMPTY:
                    continue
                for dr, dc in directions:
                    if self.is_winning_line(row, col, dr, dc):
                        return True
        return False

    def is_winning_line(self, row, col, dr, dc):
        """Check if there are 4 in a line from (row, col) in direction (dr, dc)."""
        piece = self.board[row][col]
        for i in range(1, 4):
            r, c = row + dr * i, col + dc * i
            if not (0 <= r < ROWS and 0 <= c < COLS) or self.board[r][c] != piece:
                return False
        return True


class GameServer:
    def __init__(self, host="127.0.0.1", port=65432):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)
        print("Server started. Waiting for players...")
        self.clients = []
        self.game = ConnectFourGame()

    def handle_client(self, client_socket, player_id):
        client_socket.send(pickle.dumps({"player_id": player_id, "status": "WAITING"}))

        # Wait until both players are connected
        while self.game.status == "WAITING":
            pass

        while self.game.status == "IN_PROGRESS":
            try:
                # Receive move from client
                move = pickle.loads(client_socket.recv(1024))
                column = move.get("column")

                # Process move
                if self.game.current_player == (PLAYER1 if player_id == 1 else PLAYER2) and self.game.is_valid_move(column):
                    self.game.make_move(column)
                    self.broadcast_game_state()
                else:
                    client_socket.send(pickle.dumps({"error": "Invalid move or not your turn"}))
            except:
                break

        client_socket.close()

    def broadcast_game_state(self):
        """Send the current game state to all clients."""
        game_state = {
            "board": self.game.board,
            "current_player": self.game.current_player,
            "status": self.game.status
        }
        for client in self.clients:
            client.send(pickle.dumps(game_state))

    def start(self):
        while len(self.clients) < 2:
            client_socket, _ = self.server_socket.accept()
            player_id = len(self.clients) + 1
            print(f"Player {player_id} connected.")
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket, player_id)).start()

        self.game.status = "IN_PROGRESS"
        self.broadcast_game_state()


if __name__ == "__main__":
    server = GameServer()
    server.start()
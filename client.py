import socket
import pickle


class GameClient:
    def __init__(self, host="127.0.0.1", port=65432):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.player_id = None
        self.is_my_turn = False

    def receive_game_state(self):
        """Receive and print the current game state."""
        data = pickle.loads(self.client_socket.recv(4096))
        if "error" in data:
            print(data["error"])
        else:
            self.print_board(data["board"])
            self.is_my_turn = data["current_player"] == ('X' if self.player_id == 1 else 'O')
            print(f"Game Status: {data['status']}")
            if data["status"] != "IN_PROGRESS":
                print("Game over!")
                self.client_socket.close()
                exit()

    def print_board(self, board):
        print("\n".join(" ".join(row) for row in board))
        print("-" * 15)
        print("0 1 2 3 4 5 6")  # Column numbers

    def send_move(self):
        """Send the move to the server."""
        column = int(input("Enter column (0-6): "))
        self.client_socket.send(pickle.dumps({"column": column}))

    def play(self):
        """Main game loop."""
        data = pickle.loads(self.client_socket.recv(4096))
        self.player_id = data["player_id"]
        print(f"You are Player {self.player_id}. Waiting for another player...")

        while True:
            self.receive_game_state()
            if self.is_my_turn:
                print("It's your turn!")
                self.send_move()


if __name__ == "__main__":
    client = GameClient()
    client.play()

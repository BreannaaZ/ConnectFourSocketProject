import socket
from threading import Thread
from common.game_logic import Game


def handle_client(client_socket, address, game):
    # Handle client communication: receive moves, send game state, etc.
    pass


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 5555))
    server.listen(2)  # Allow only two players
    print("Server started, waiting for players...")

    game = Game()  # Initialize the game logic
    while True:
        client_socket, address = server.accept()
        print(f"Player connected: {address}")
        Thread(target=handle_client, args=(client_socket, address, game)).start()


if __name__ == "__main__":
    start_server()

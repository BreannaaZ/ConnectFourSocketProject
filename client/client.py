import socket
import tkinter as tk
from tkinter import messagebox


class ConnectFourClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect Four")
        self.board = self.create_board()

    def create_board(self):
        # Create a GUI for the board (e.g., 7 columns, 6 rows)
        pass

    def connect_to_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect(("localhost", 5555))  # Server IP and port
        # Start receiving game updates from the server
        self.receive_game_updates()

    def send_move(self, column):
        # Send the selected column to the server
        pass

    def receive_game_updates(self):
        # Listen for game state updates from the server
        pass


if __name__ == "__main__":
    root = tk.Tk()
    client = ConnectFourClient(root)
    client.connect_to_server()
    root.mainloop()

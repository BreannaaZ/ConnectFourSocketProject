import tkinter as tk


class ConnectFourGUI:
    def __init__(self, master, game):
        self.master = master
        self.game = game
        self.buttons = []
        self.create_widgets()

    def create_widgets(self):
        for r in range(6):
            row_buttons = []
            for c in range(7):
                btn = tk.Button(self.master, text=" ", width=10, height=3, command=lambda c=c: self.on_column_click(c))
                btn.grid(row=r, column=c)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def on_column_click(self, column):
        # Handle a click event for a column (send move to server)
        pass

    def update_board(self):
        # Update the board display based on the game state
        pass

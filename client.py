import socket
import pickle
import time
import pygame
import threading


class GameClient:
    def __init__(self, host="192.168.1.204", port=5555):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.player_id = None
        self.is_my_turn = False
        self.connected = False
        self.running = True
        self.board = [[" " for _ in range(7)] for _ in range(6)]  # Empty board
        self.status = "WAITING"  # Tracks game status

    def receive_game_state(self):
        # Receive the game state from the server (for current board, status, turn info)
        while self.running:
            try:
                data = pickle.loads(self.client_socket.recv(4096))
                if "error" in data:
                    print(data["error"])
                else:
                    self.board = data["board"]
                    self.status = data["status"]
                    self.is_my_turn = data["current_player"] == ('X' if self.player_id == 1 else 'O')
                    if data["status"] != "IN_PROGRESS":
                        time.sleep(3)  # Delay before ending game to show end game screen
                        self.running = False  # Stop running when the game is over
                        print("Game Over")
                    print(f"Client received: ${self.board}, status: ${self.status}, turn?: ${self.is_my_turn} ")
            except Exception as e:
                print(f"Connection error: {e}")
                self.running = False

    def send_move(self, column):
        # Send a move to the server (column for piece placement)
        try:
            self.client_socket.send(pickle.dumps({"column": column}))
            print(f"Client sent move in col: ${column}")
        except Exception as e:
            print(f"Failed to send move: {e}")

    def play(self):
        # Start the thread and receive the initial data
        data = pickle.loads(self.client_socket.recv(4096))
        self.player_id = data["player_id"]
        print(f"Play, player id: ${self.player_id}")
        print(f"Play, initial data: ${data}")
        self.connected = True  # Set connected to True once the player ID is received
        threading.Thread(target=self.receive_game_state, daemon=True).start()


# GUI Setup
def draw_waiting_screen(screen, font):
    # Draw the "waiting for players" screen
    screen.fill((0, 0, 0))  # Black background
    text = font.render("Waiting for Players...", True, (255, 255, 255))
    # Center the text
    text_width = text.get_width()
    text_height = text.get_height()
    x_position = (screen.get_width() - text_width) // 2
    y_position = (screen.get_height() - text_height) // 2
    # Add to display
    screen.blit(text, (x_position, y_position))
    pygame.display.update()


def draw_game_over_screen(screen, font, status, player_id):
    # Draw the "GAME OVER" screen when a player wins or game draws
    message = " "
    screen.fill((0, 0, 0))  # Black background
    # Player 1 = X (red), Player 2 = O (yellow).

    # WIN/LOST text
    if status == "X_WON":
        if player_id == 1:
            message = "YOU WON"
        else:
            message = "YOU LOST"
    elif status == "O_WON":
        if player_id == 2:
            message = "YOU WON"
        else:
            message = "YOU LOST"
    text = font.render(message, True, (255, 255, 255))
    # Center the text
    text_width = text.get_width()
    text_height = text.get_height()
    x_position = (screen.get_width() - text_width) // 2
    y_position = (screen.get_height() - text_height) // 2
    screen.blit(text, (x_position, y_position))

    # QUITTING text
    text = font.render("Quitting...", True, (255, 255, 255))
    # Center the text
    text_width = text.get_width()
    text_height = text.get_height()
    x_position = (screen.get_width() - text_width) // 2
    y_position = (screen.get_height() - text_height) // 2
    screen.blit(text, (x_position, y_position + 100))

    pygame.display.update()


def draw_game_screen(screen, font, board, is_my_turn, player_id):
    # Draw the main game screen (title, turn info, game board)
    screen.fill((0, 0, 0))  # Black background

    # Draw and center the title
    title_text = font.render("CONNECT FOUR", True, (255, 255, 255))
    # Center the title horizontally
    text_width = title_text.get_width()
    text_height = title_text.get_height()
    x_position = (screen.get_width() - text_width) // 2
    y_position = 25  # 25 pixels down from top of screen
    screen.blit(title_text, (x_position, y_position))

    # Draw and center the turn info (lower slightly below title text)
    # Set turn text color based on player (so text color matches their piece color)
    if player_id == 1:
        player_color = (255, 0, 0)  # Red
    else:
        player_color = (255, 255, 0)  # Yellow
    turn_text = font.render("Your Turn" if is_my_turn else "Waiting...", True, player_color)
    text_width = turn_text.get_width()
    text_height = turn_text.get_height()
    x_position = (screen.get_width() - text_width) // 2
    y_position = 100  # 100 pixels down from top of screen
    screen.blit(turn_text, (x_position, y_position))

    # Offset for the grid, to move it down further so title/turn info text has more room
    vertical_offset = 150
    # Draw grid
    for row in range(6):
        for col in range(7):
            pygame.draw.rect(screen, (0, 0, 255), (col * 100, row * 100 + vertical_offset, 100, 100))
            if board[row][col] == "X":
                pygame.draw.circle(screen, (255, 0, 0), (col * 100 + 50, row * 100 + vertical_offset + 50), 40)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, (255, 255, 0), (col * 100 + 50, row * 100 + vertical_offset + 50), 40)
            else:
                pygame.draw.circle(screen, (0, 0, 0), (col * 100 + 50, row * 100 + vertical_offset + 50), 40)

    pygame.display.update()


# Main Game Loop and pygame start
def main():
    pygame.init()
    screen = pygame.display.set_mode((700, 800))
    pygame.display.set_caption("Connect Four")
    font = pygame.font.Font(None, 74)

    # Connect as client
    client = GameClient()
    client.play()

    while client.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.running = False

            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN and client.is_my_turn:
                x, y = event.pos
                # Find the column the user clicked
                if 150 <= y <= 750:  # Click within the grid area
                    col = x // 100
                    if 0 <= col <= 6:
                        client.send_move(col)

        # Update screen
        if client.status == "WAITING":
            draw_waiting_screen(screen, font)
        elif client.status == "IN_PROGRESS":
            draw_game_screen(screen, font, client.board, client.is_my_turn, client.player_id)
        else:
            draw_game_over_screen(screen, font, client.status, client.player_id)

    print("Quitting...")
    pygame.quit()


if __name__ == "__main__":
    main()

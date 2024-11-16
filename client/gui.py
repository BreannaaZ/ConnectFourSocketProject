import pygame
import sys

from common import game_logic
from common.game_logic import Game

# import game_logic  # Import your game logic file

# Constants
ROWS = 6
COLS = 7
CELL_SIZE = 90
PADDING = 50
TOP_PADDING = 140
BOTTOM_PADDING = 220
RADIUS = int(CELL_SIZE / 2 - 10)
SCREEN_WIDTH = COLS * CELL_SIZE + 2 * PADDING
SCREEN_HEIGHT = (ROWS + 1) * CELL_SIZE + BOTTOM_PADDING
PLAYER_COLORS = [(255, 0, 0), (0, 0, 255)]  # Red and blue
BACKGROUND_COLOR = (255, 255, 255)  # White
BOARD_COLOR = (128, 128, 128)  # Gray
EMPTY_SLOT_COLOR = (255, 255, 255)  # White
BORDER_THICKNESS = 4  # Thickness of the border
PLAYER_COLOR = (128, 128, 128)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Connect 4")

# Initialize game instance
game_instance = Game()

# Fonts and sizes
title_font = pygame.font.Font(None, 72)  # Font for title, size 72
subtitle_font = pygame.font.Font(None, 48)  # Font for subtitle, size 48
small_font = pygame.font.Font(None, 24)  # Font for smaller text, size 24


def draw_board(hovered_column):
    """Draw the Connect 4 board."""
    screen.fill(BACKGROUND_COLOR)

    # Draw the title at the top
    title_text = title_font.render("CONNECT FOUR", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, TOP_PADDING // 3))
    screen.blit(title_text, title_rect)

    # Draw player turn labels
    pygame.draw.rect(screen, PLAYER_COLOR, ((SCREEN_WIDTH // 2 - 250), (TOP_PADDING // 2 + 10), 200, 50))
    pygame.draw.rect(screen, PLAYER_COLOR, ((SCREEN_WIDTH // 2 + 50), (TOP_PADDING // 2 + 10), 200, 50))

    player1_turn_text = subtitle_font.render("PLAYER 1", True, (255, 0, 0))
    player1_rect = player1_turn_text.get_rect(center=((SCREEN_WIDTH // 2 - 250) + 100, (TOP_PADDING // 2 + 10) + 25))
    screen.blit(player1_turn_text, player1_rect)

    # Get current player/turn to change colors
    if game_instance.current_player == 'X':
        PLAYER1_BORDER_COLOR = (255, 0, 0)
    else:
        PLAYER1_BORDER_COLOR = BACKGROUND_COLOR
    if game_instance.current_player == 'O':
        PLAYER2_BORDER_COLOR = (0, 0, 255)
    else:
        PLAYER2_BORDER_COLOR = BACKGROUND_COLOR

    # Player1 textbox border
    player1_border_rect = player1_rect.inflate(50, 20)
    pygame.draw.rect(screen, PLAYER1_BORDER_COLOR, player1_border_rect, BORDER_THICKNESS)

    player2_turn_text = subtitle_font.render("PLAYER 2", True, (0, 0, 255))
    player2_rect = player2_turn_text.get_rect(center=((SCREEN_WIDTH // 2 + 50) + 100, (TOP_PADDING // 2 + 10) + 25))
    screen.blit(player2_turn_text, player2_rect)

    # Player2 textbox border
    player2_border_rect = player2_rect.inflate(50, 20)
    pygame.draw.rect(screen, PLAYER2_BORDER_COLOR, player2_border_rect, BORDER_THICKNESS)

    # Draw the border around the board
    board_left = PADDING
    board_top = TOP_PADDING
    board_width = COLS * CELL_SIZE
    board_height = ROWS * CELL_SIZE
    pygame.draw.rect(screen, BOARD_COLOR, (board_left, board_top + CELL_SIZE, board_width, board_height))

    # Draw slots
    for r in range(ROWS + 1):
        for c in range(COLS):
            x = c * CELL_SIZE + PADDING
            y = (r + 1) * CELL_SIZE + PADDING

            # Adjust for the top row (different color)
            if r == 0:
                color = BACKGROUND_COLOR  # Set color for the new top row
            else:
                color = EMPTY_SLOT_COLOR  # Set color for the regular slots

            pygame.draw.circle(screen, color, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), RADIUS)

            # Draw pieces
            if r > 0 and game_instance.board[r - 1][c] is not None:
                if game_instance.board[r - 1][c] == 'X':
                    color = PLAYER_COLORS[0]
                elif game_instance.board[r - 1][c] == 'O':
                    color = PLAYER_COLORS[1]
                # color = PLAYER_COLORS[game_instance.board[r - 1][c]]
                pygame.draw.circle(screen, color, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), RADIUS)

        # Highlight the topmost circle of the hovered column
        if hovered_column is not None:
            x = hovered_column * CELL_SIZE + PADDING
            y = PADDING + CELL_SIZE  # Keep it at the top of the screen
            # Get current player/turn to change colors
            if game_instance.current_player == 'X':
                HOVER_COLOR = (255, 0, 0)
            elif game_instance.current_player == 'O':
                HOVER_COLOR = (0, 0, 255)
            else:
                HOVER_COLOR = BACKGROUND_COLOR
            pygame.draw.circle(screen, HOVER_COLOR, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), RADIUS)

    # Quit game button
    # Define button properties
    BUTTON_WIDTH = 225
    BUTTON_HEIGHT = 50
    BUTTON_COLOR = (255, 0, 0)  # Red
    BUTTON_HOVER_COLOR = (200, 0, 0)  # Darker red for hover effect
    BUTTON_TEXT_COLOR = (255, 255, 255)  # White text color

    # Create the button rectangle (position it below the board)
    button_rect = pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT - BUTTON_HEIGHT - 20),
                              (BUTTON_WIDTH, BUTTON_HEIGHT))
    # Render the "Reset Game" text
    reset_text = subtitle_font.render("Reset Game", True, BUTTON_TEXT_COLOR)
    # Get the rect for the text (centered within the button)
    reset_text_rect = reset_text.get_rect(center=button_rect.center)
    # Draw the button
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)  # Draw the button with the defined color
    # Draw the text inside the button
    screen.blit(reset_text, reset_text_rect)
    # Handle mouse hover effect over button (change color when hovered)
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)  # Change button color on hover
        screen.blit(reset_text, reset_text_rect)  # Redraw the text on top of the button

    # Return the button rectangle so it can be checked in the event loop
    return button_rect


def handle_click(x, y):
    """Handle the column selection and return the updated board."""
    col = (x - PADDING) // CELL_SIZE
    if col < 0 or col >= COLS or y < TOP_PADDING or y > (ROWS * CELL_SIZE + BOTTOM_PADDING):
        return None

    valid_move = game_instance.make_move(col)
    return valid_move


def display_winner(winner):
    """Display the winning message and quit."""
    message = f"Player {winner + 1} wins!"
    text = subtitle_font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, PADDING // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()


def main():
    hovered_column = None
    button_rect = draw_board(hovered_column) # Draw board and get reset button location

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle reset game button clicked
                if event.button == 1:  # Left mouse button clicked
                    if button_rect.collidepoint(event.pos):  # Check if click is inside the button
                        # Reset the game (clear board, etc.)
                        game_instance.reset_game()  # Call your function to reset the game state

                # Handle column click
                x = event.pos[0]
                y = event.pos[1]
                # board, move = handle_click(x, board, current_player)
                move = handle_click(x, y)
                if move is not None:
                    draw_board(hovered_column)
                    pygame.display.update()

                    # Check for a winner
                    if game_instance.check_win():
                        draw_board(hovered_column)
                        pygame.display.update()
                        display_winner(game_instance.current_player)

                    # Switch players
                    game_instance.switch_player()

        # Get the current mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Calculate which column the mouse is over
        hovered_column = (mouse_x - PADDING) // CELL_SIZE
        if hovered_column < 0 or hovered_column >= COLS \
                or mouse_y < TOP_PADDING or mouse_y > (ROWS * CELL_SIZE + BOTTOM_PADDING):
            hovered_column = None  # Mouse is not over any column

        # Draw and update the board
        draw_board(hovered_column)
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

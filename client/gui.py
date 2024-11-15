import pygame
import sys

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
PLAYER_COLORS = [(255, 0, 0), (255, 255, 0)]  # Red and Yellow
BACKGROUND_COLOR = (0, 0, 0)  # Black
BOARD_COLOR = (128, 128, 128)  # Gray
EMPTY_SLOT_COLOR = (255, 255, 255)  # White
PLAYER1_BORDER_COLOR = (255, 255, 255)  # White border
PLAYER2_BORDER_COLOR = (255, 255, 255)  # White border
BORDER_THICKNESS = 3  # Thickness of the border
PLAYER_COLOR = (128, 128, 128)
TOP_ROW_COLOR = (128, 128, 128)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Connect 4")

# Fonts and sizes
title_font = pygame.font.Font(None, 72)  # Font for title, size 72
subtitle_font = pygame.font.Font(None, 48)  # Font for subtitle, size 48
small_font = pygame.font.Font(None, 24)  # Font for smaller text, size 24


def draw_board(board):
    """Draw the Connect 4 board."""
    screen.fill(BACKGROUND_COLOR)

    # Draw the title at the top
    title_text = title_font.render("CONNECT FOUR", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, TOP_PADDING // 3))
    screen.blit(title_text, title_rect)

    # Draw player turn labels
    pygame.draw.rect(screen, PLAYER_COLOR, ((SCREEN_WIDTH // 2 - 250), (TOP_PADDING // 2 + 10), 200, 50))
    pygame.draw.rect(screen, PLAYER_COLOR, ((SCREEN_WIDTH // 2 + 50), (TOP_PADDING // 2 + 10), 200, 50))

    player1_turn_text = subtitle_font.render("PLAYER 1", True, (255, 0, 0))
    player1_rect = player1_turn_text.get_rect(center=((SCREEN_WIDTH // 2 - 250) + 100, (TOP_PADDING // 2 + 10) + 25))
    screen.blit(player1_turn_text, player1_rect)

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
                color = TOP_ROW_COLOR  # Set color for the new top row
            else:
                color = EMPTY_SLOT_COLOR  # Set color for the regular slots

            pygame.draw.circle(screen, color, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), RADIUS)

            # Draw pieces
            if r > 0 and board[r - 1][c] is not None:
                color = PLAYER_COLORS[board[r][c]]
                pygame.draw.circle(screen, color, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), RADIUS)

    # Quite game button
    # Define button properties
    BUTTON_WIDTH = 225
    BUTTON_HEIGHT = 50
    BUTTON_COLOR = (255, 0, 0)  # Green color for the button
    BUTTON_HOVER_COLOR = (200, 0, 0)  # Darker green for hover effect
    BUTTON_TEXT_COLOR = (255, 255, 255)  # White color for the button text

    # Create the button rectangle (position it below the board)
    button_rect = pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT - BUTTON_HEIGHT - 20),
                              (BUTTON_WIDTH, BUTTON_HEIGHT))
    # Render the "Reset Game" text
    reset_text = subtitle_font.render("Reset Game", True, BUTTON_TEXT_COLOR)
    # Get the rect for the text (centered within the button)
    reset_text_rect = reset_text.get_rect(center=button_rect.center)
    # Draw the button
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)  # Draw the button with the defined color
    pygame.draw.rect(screen, (0, 0, 0), button_rect, 3)  # Optionally add a black border around the button
    # Draw the text inside the button
    screen.blit(reset_text, reset_text_rect)
    # Handle mouse hover effect (change color when hovered)
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)  # Change button color on hover
        pygame.draw.rect(screen, (0, 0, 0), button_rect, 3)  # Border stays the same
        screen.blit(reset_text, reset_text_rect)  # Redraw the text on top of the button


def handle_click(x, board, current_player):
    """Handle the column selection and return the updated board."""
    col = (x - PADDING) // CELL_SIZE
    if col < 0 or col >= COLS:
        return board, None

    # Get the next open row for the selected column
    row = game_logic.get_next_open_row(board, col)
    if row is not None:
        board[row][col] = current_player
        return board, (row, col)
    return board, None


def display_winner(winner):
    """Display the winning message and quit."""
    message = f"Player {winner + 1} wins!"
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, PADDING // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()


def main():
    # Initialize the board
    board = [[None for _ in range(COLS)] for _ in range(ROWS)]
    current_player = 0  # 0 = Red, 1 = Yellow

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle column click
                x = event.pos[0]
                board, move = handle_click(x, board, current_player)
                if move:
                    draw_board(board)
                    pygame.display.update()

                    # Check for a winner
                    # if game_logic.check_winner(board, current_player):
                    #    draw_board(board)
                    #    pygame.display.update()
                    #    display_winner(current_player)

                    # Switch players
                    current_player = 1 - current_player

        # Draw the board
        draw_board(board)
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

import pygame
import random  # Import the random module

from game import Game
from boardgame import Boardgame
from const import *

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.boardgame = Boardgame()
        self.game = Game(self.boardgame)
        self.phase = "placement"
        self.current_player = "red"
        self.game_over = False
        self.win_message = None
        self.highlighted_square1 = None
        self.highlighted_square = None

    def mainloop(self):
        screen = self.screen
        game = self.game
        running = True

        while running:
            game.show_bg(screen)
            game.show_pieces(screen)
            game.render_number_of_row(screen)
            game.render_letter_of_col(screen)
            game.render_number_of_black_pieces(screen)
            game.render_name_of_black_pieces(screen)
            game.render_number_of_red_pieces(screen)
            game.render_name_of_red_pieces(screen)

            if self.game_over:
                self.game.display_win_message(screen)

            if self.highlighted_square1:
                row, col = self.highlighted_square1
                game.highlight_selected_square_placement_phase(screen, row, col)

            if self.highlighted_square:
                row, col = self.highlighted_square
                game.highlight_selected_square_game_phase(screen, row, col)

            if self.game.show_valid_moves_flag:
                game.display_valid_moves(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:  # Check for key presses
                    if event.key == pygame.K_2 and self.phase == "placement":  # If '2' is pressed during placement
                        self.auto_place_pieces()  # Call the auto-placement function
                        
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // RECT_WIDTH
                    row = pos[1] // RECT_HEIGHT

                    if self.phase == "placement":
                        if self.boardgame.check_all_pieces_placed():
                            self.flag = False
                            self.phase = "gameplay"
                            self.current_player = "red"
                            self.highlighted_square = (row, col)
                            self.game.show_valid_moves_flag = True
                            self.game.show_valid_moves(self.screen, row, col)
                            self.handle_gameplay(event.button, row, col)

                        else:
                            result = self.boardgame.handle_placement(event.button, row, col)
                            if result:
                                self.highlighted_square = result
                            else:
                                self.highlighted_square = None
                    else:
                        result = self.handle_gameplay(event.button, row, col)
                        if result:
                            self.highlighted_square = result
                        else:
                            self.highlighted_square = None

            pygame.display.update()

        pygame.quit()

    def handle_gameplay(self, button, row, col):
        if button == 1:
            if self.boardgame.selected_piece is None:
                if self.boardgame.select_piece(row, col, self.current_player):
                    self.game.show_valid_moves_flag = True
                    self.game.show_valid_moves(self.screen, row, col)
                    pygame.display.update()
                    return (row, col)
                else:
                    return None # No piece selected or invalid selection
            else:
                start_row, start_col = self.boardgame.selected_piece
                if self.boardgame.squares[row][col].has_piece() and self.boardgame.squares[row][col].piece.color == self.current_player:
                    self.boardgame.selected_piece = (row, col)
                    self.game.show_valid_moves(self.screen, row, col)
                    return (row, col)
                else:
                    move_result = self.boardgame.move_piece(start_col, start_row, col, row, self.current_player)
                    if move_result:
                        self.game.show_valid_moves_flag = False
                        win_condition = self.boardgame.check_win_condition()
                        if win_condition:
                            self.game_over = True
                            self.game.win_message = win_condition
                        else:
                            self.current_player = "black" if self.current_player == "red" else "red"
                            self.boardgame.selected_piece = None
                        return None  # Indicate successful move
                    else:
                        return (start_row, start_col) # Return to the originally selected piece
        return None # No action taken

    def auto_place_pieces(self):
        """
        Automatically places all remaining pieces for both red and black.
        """
        # Auto-place black pieces
        for row in range(4):
            for col in range(10):  # Adjusted range to cover the left side
                if not self.boardgame.squares[row][col].has_piece():
                    # Find a black piece that hasn't been placed yet
                    for r in range(4):  # Iterate over the black piece selection area
                        for c in range(10, 13):
                            if self.boardgame.squares[r][c].has_piece() and self.boardgame.squares[r][c].number > 0 and self.boardgame.squares[r][c].piece.color == "black":
                                self.boardgame.handle_black_piece_selection(r, c)  # Select the piece
                                self.boardgame.handle_black_piece_placement(row, col)  # Place the piece
                                break  # Break out of the inner loop after placing a piece
                        else:
                            continue  # Continue to the next column if a piece was placed
                        break  # Break out of the outer loop if a piece was placed

        # Auto-place red pieces
        for row in range(6, 10):
            for col in range(10):  # Adjusted range to cover the left side
                if not self.boardgame.squares[row][col].has_piece():
                    # Find a red piece that hasn't been placed yet
                    for r in range(6, 10):  # Iterate over the red piece selection area
                        for c in range(10, 13):
                            if self.boardgame.squares[r][c].has_piece() and self.boardgame.squares[r][c].number > 0 and self.boardgame.squares[r][c].piece.color == "red":
                                self.boardgame.handle_red_piece_selection(r, c)  # Select the piece
                                self.boardgame.handle_red_piece_placement(row, col)  # Place the piece
                                break  # Break out of the inner loop after placing a piece
                        else:
                            continue  # Continue to the next column if a piece was placed
                        break  # Break out of the outer loop if a piece was placed

        self.phase = "gameplay" #change phase after auto placement
        self.current_player = "red" #red turn after placement

main = Main()
main.mainloop()

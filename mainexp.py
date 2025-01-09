import pygame
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
            game.render_number_of_red_pieces(screen)

            if self.game_over:
                self.display_win_message(screen)
        
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
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // RECT_WIDTH
                    row = pos[1] // RECT_HEIGHT
                    if self.phase == "placement":
                        if self.phase == "placement" and self.boardgame.check_all_pieces_placed():
                            self.phase = "gameplay"
                            self.current_player = "red"
                        result = self.boardgame.handle_placement(event.button, row, col)
                        if result:
                            self.highlighted_square = result  # Set highlighted square to selected piece
                        else:
                            self.highlighted_square = None
                    else:
                        result = self.handle_gameplay(event.button, row, col)
                        if result:  # If a piece was selected, update highlighted_square
                            self.highlighted_square = result  # Set highlighted square to selected piece
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
                    return (row, col)
            else:
                start_row, start_col = self.boardgame.selected_piece
                if self.boardgame.squares[row][col].has_piece() and self.boardgame.squares[row][col].piece.color == self.current_player:
                    self.boardgame.selected_piece = (row, col)
                    self.game.show_valid_moves(self.screen, row, col)
                    return (row, col)
                else:
                    move_result = self.boardgame.move_piece(start_col, start_row, col, row, self.current_player)

                    if move_result:
                        print("Move successful; hiding valid moves.")
                        self.game.show_valid_moves_flag = False
                        win_condition = self.boardgame.check_win_condition()
                        if win_condition:
                            self.game_over = True
                            self.win_message = win_condition
                        else:
                            self.current_player = "black" if self.current_player == "red" else "red"
                        self.boardgame.selected_piece = None
                        return None
                    else:
                        return (start_row, start_col)
        
        pygame.display.update()

    def display_win_message(self, surface):
        font = pygame.font.Font(None, 36)
        text = font.render(self.win_message, True, (255, 0, 0))
        text_rect = text.get_rect(center = (WIDTH // 2, HEIGHT // 2))
        surface.blit(text, text_rect)

main = Main()
main.mainloop()

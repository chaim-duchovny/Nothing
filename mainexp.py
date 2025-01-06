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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // RECT_WIDTH
                    row = pos[1] // RECT_HEIGHT
                    if self.phase == "placement":
                        self.handle_placement(event.button, row, col)
                    else:
                        self.handle_gameplay(event.button, row, col)

            pygame.display.update()

        pygame.quit()

    def handle_placement(self, button, row, col):
        if button == 1:
            self.boardgame.handle_black_piece_selection(row, col)
            self.boardgame.handle_black_piece_placement(row, col)
            self.boardgame.handle_red_piece_selection(row, col)
            self.boardgame.handle_red_piece_placement(row, col)
            self.boardgame.reset_piece_placement()
        elif button == 3:
            self.boardgame.return_piece_black_selction(row, col)
            self.boardgame.return_piece_black_return(row, col)
            self.boardgame.return_piece_red_selction(row, col)
            self.boardgame.return_piece_red_return(row, col)

        if self.boardgame.check_all_pieces_placed():
            self.phase = "gameplay"
            self.current_player = "red"

    def handle_gameplay(self, button, row, col):
        if button == 1:
            if self.boardgame.selected_piece is None:
                self.boardgame.select_piece(row, col, self.current_player)
            else:
                start_row, start_col = self.boardgame.selected_piece
                move_result = self.boardgame.move_piece(start_col, start_row, col, row, self.current_player)
                if move_result:
                    win_condition = self.boardgame.check_win_condition()
                    if win_condition:
                        self.game_over = True
                        self.win_message = win_condition
                    else:
                        self.current_player = "black" if self.current_player == "red" else "red"
                    self.boardgame.selected_piece = None
                    self.game.show_pieces(self.screen)
                    pygame.display.update()

    def display_win_message(self, surface):
        font = pygame.font.Font(None, 36)
        text = font.render(self.win_message, True, (255, 0, 0))
        text_rect = text.get_rect(center = (WIDTH // 2, HEIGHT // 2))
        surface.blit(text, text_rect)

main = Main()
main.mainloop()

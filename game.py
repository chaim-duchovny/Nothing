
import pygame
from boardgame import Boardgame
from const import *


class Game:

    def __init__(self, boardgame):
        self.boardgame = boardgame
        self.selected_black_piece = None
        self.selected_red_piece = None
        self.piece_placed = False
        self.piece_to_return_black = None
        self.piece_to_return_red = None
        self.selected = False
        self.valid_moves = []
        self.show_valid_moves_flag = False

    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (10 <= col <= 12):
                    color = (211,211,211)
                elif(row, col) in SPECIAL_POSITION:
                    color = (173, 216, 230)
                elif(row + col) % 2 == 0 :
                    color = (234, 235, 200)
                elif(row + col) % 2 != 0 :
                    color = (119, 154, 88)

                rect = (col * RECT_WIDTH, row * RECT_HEIGHT, RECT_WIDTH, RECT_HEIGHT)

                pygame.draw.rect(surface, color, rect)
            
        for col in range(10, 13):
            start_pos = (col * RECT_WIDTH, 0)
            end_pos = (col * RECT_WIDTH, 4 * RECT_HEIGHT)
            pygame.draw.line(surface, (0, 0, 0), start_pos, end_pos, 1)

        for col in range(10, 13):
            start_pos = (col * RECT_WIDTH, 6 * RECT_HEIGHT)
            end_pos = (col * RECT_WIDTH, ROWS * RECT_HEIGHT)
            pygame.draw.line(surface, (0, 0, 0), start_pos, end_pos, 1)

        for row in range(0, 5):
            start_pos = (10 * RECT_WIDTH, row * RECT_HEIGHT)
            end_pos = (13 * RECT_WIDTH, row * RECT_HEIGHT)
            pygame.draw.line(surface, (0, 0, 0), start_pos, end_pos, 1)

        for row in range(6, 10):
            start_pos = (10 * RECT_WIDTH, row * RECT_HEIGHT)
            end_pos = (13 * RECT_WIDTH, row * RECT_HEIGHT)
            pygame.draw.line(surface, (0, 0, 0), start_pos, end_pos, 1)
    
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.boardgame.squares[row][col].has_piece():
                    piece = self.boardgame.squares[row][col].piece
                    
                    img = pygame.image.load(piece.texture)
                    img_center = col * RECT_WIDTH + RECT_WIDTH // 2, row * RECT_HEIGHT + RECT_HEIGHT // 2
                    piece.texture_rect = img.get_rect(center = img_center)
                    surface.blit(img, piece.texture_rect)
    
    def render_number_of_black_pieces(self, surface):
        for row in range(4):
            for col in range(10, 13):
                if self.boardgame.squares[row][col].number is not None:
                    font = pygame.font.Font(None, 24)  
                    text = font.render(str(self.boardgame.squares[row][col].number), True, (0, 0, 0)) 
                    text_rect = text.get_rect(topleft=(col * 90 + 5, row * 65 + 5))  
                    surface.blit(text, text_rect)
    
    def render_number_of_red_pieces(self, surface):
        for row in range(6, 10):
            for col in range(10, 13):
                if self.boardgame.squares[row][col].number is not None:
                    font = pygame.font.Font(None, 24)  
                    text = font.render(str(self.boardgame.squares[row][col].number), True, (255, 0, 0)) 
                    text_rect = text.get_rect(topleft=(col * 90 + 5, row * 65 + 5))  
                    surface.blit(text, text_rect)

    def render_number_of_row(self, surface):
        for row in range(ROWS):
            if self.boardgame.squares[row][0].number is None:
                font = pygame.font.Font(None, 24)  
                text = font.render(str(ROWS - row), True, (0, 0, 0)) 
                text_rect = text.get_rect(topleft=(0 * 90 + 5, row * 65 + 40))  
                surface.blit(text, text_rect)

    def render_letter_of_col(self, surface):
        for col in range(COLS):
            if self.boardgame.squares[0][col].number is None:
                font = pygame.font.Font(None, 24)  
                text = font.render(chr(col % 26 + ord('A')), True, (0, 0, 0)) 
                text_rect = text.get_rect(topleft=(col * 90 + 75, 0 * 65 + 5))  
                surface.blit(text, text_rect)
    
    def highlight_selected_square_placement_phase(self, surface, row, col):
        rect = (col * RECT_WIDTH, row * RECT_HEIGHT, RECT_WIDTH, RECT_HEIGHT)
        pygame.draw.rect(surface, "BLUE", rect, 3)

    def highlight_selected_square_game_phase(self, surface, row, col):
        rect = (col * RECT_WIDTH, row * RECT_HEIGHT, RECT_WIDTH, RECT_HEIGHT)
        pygame.draw.rect(surface, "BLUE", rect, 3)

    def show_valid_moves(self, surface, row, col):
        if self.show_valid_moves_flag:
            self.valid_moves = []
            piece = self.boardgame.squares[row][col].piece
            if piece:
                for end_row in range(ROWS):
                    for end_col in range(COLS):
                        if self.boardgame.valid_move(col, row, end_col, end_row, piece):
                            self.valid_moves.append((end_row, end_col))
                            rect = (end_col * RECT_WIDTH, end_row * RECT_HEIGHT, RECT_WIDTH, RECT_HEIGHT)
                            pygame.draw.rect(surface, (0, 255, 0, 128), rect, 3)
        else:                    
            return False
    
    def display_valid_moves(self, surface):
        for row, col in self.valid_moves:
            rect = (col * RECT_WIDTH, row * RECT_HEIGHT, RECT_WIDTH, RECT_HEIGHT)
            pygame.draw.rect(surface, (0, 255, 0, 128), rect, 3)
        

    
        
    





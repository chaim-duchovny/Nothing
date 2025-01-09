from square import Square
from piece import *
from const import *
import random

class Boardgame:

    def __init__(self):
        self.squares = [[Square(row, col) for col in range(COLS)] for row in range(ROWS)]
        self.create()
        self.add_pieces_black("black")
        self.add_pieces_red("red")
        self.selected_piece = None
        self.selected_black_piece = None
        self.selected_red_piece = None
        self.piece_placed = False
        self.black_piece_selected = False
        self.red_piece_selected = False
        self.piece_to_return_black = None
        self.piece_to_return_red = None
        self.move_history = {}

    def create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
    
    def add_pieces_black(self, color):
        pieces = [
            (6, Bomb), 
            (1, Marshal), 
            (1, General),
            (2, Colonel), 
            (3, Major), 
            (4, Captain),
            (4, Lieutenant), 
            (4, Sergeant), 
            (5, Miner),
            (8, Scout), 
            (1, Spy), 
            (1, Flag)
        ]
    
        available_squares = [(row, col) for row in range(4) for col in range(10, 13)]
        self.original_positions_black = {}
    
        for count, piece_class in pieces:
            if available_squares:
                row, col = random.choice(available_squares)
                piece_instance = piece_class(color)
                self.squares[row][col] = Square(row, col, count, piece_instance)
                self.original_positions_black[piece_instance] = (row, col)
                available_squares.remove((row, col))

    def add_pieces_red(self, color):
        pieces = [
            (6, Bomb), 
            (1, Marshal), 
            (1, General),
            (2, Colonel), 
            (3, Major), 
            (4, Captain),
            (4, Lieutenant), 
            (4, Sergeant), 
            (5, Miner),
            (8, Scout), 
            (1, Spy), 
            (1, Flag)
        ]
    
        available_squares = [(row, col) for row in range(6, 10) for col in range(10, 13)]
        self.original_positions_red = {}
    
        for count, piece_class in pieces:
            if available_squares:
                row, col = random.choice(available_squares)
                piece_instance = piece_class(color)
                self.squares[row][col] = Square(row, col, count, piece_instance)
                self.original_positions_red[piece_instance] = (row, col)
                available_squares.remove((row, col))
        
    def handle_black_piece_selection(self, row, col):
        if (0 <= row <= 3) and (10 <= col <= 12):  
            if self.selected_black_piece is None: 
                if self.squares[row][col].has_piece():
                    piece = self.squares[row][col].piece

                    if piece.color == "black" and self.squares[row][col].number > 0:
                        self.squares[row][col].number -= 1
                        self.selected_black_piece = piece
                        
                        if self.squares[row][col].number == 0:
                            self.squares[row][col].piece = None

            else:  
                original_row, original_col = self.get_original_position_black(self.selected_black_piece)
                if original_row is not None and original_col is not None:
                    self.squares[original_row][original_col].number += 1

                    if self.squares[original_row][original_col].piece is None:
                        self.squares[original_row][original_col].piece = self.selected_black_piece
                    self.selected_black_piece = None

    def handle_black_piece_placement(self, row, col):
        if self.selected_black_piece:
            if (0 <= row <= 3) and (0 <= col <= 9):
                if not self.squares[row][col].has_piece():
                    self.squares[row][col].piece = self.selected_black_piece
                    self.selected_black_piece = None
                    self.piece_placed = True

    def handle_red_piece_selection(self, row, col):
        if (6 <= row <= 9) and (10 <= col <= 12): 
            if self.selected_red_piece is None:  
                if self.squares[row][col].has_piece():
                    piece = self.squares[row][col].piece

                    if piece.color == "red" and self.squares[row][col].number > 0:
                        self.squares[row][col].number -= 1
                        self.selected_red_piece = piece
                        
                        if self.squares[row][col].number == 0:
                            self.squares[row][col].piece = None

            else:  
                original_row, original_col = self.get_original_position_red(self.selected_red_piece)
                if original_row is not None and original_col is not None:
                    self.squares[original_row][original_col].number += 1

                    if self.squares[original_row][original_col].piece is None:
                        self.squares[original_row][original_col].piece = self.selected_red_piece
                    self.selected_red_piece = None

    def handle_red_piece_placement(self, row, col):
        if self.selected_red_piece:
            if (6 <= row <= 9) and (0 <= col <= 9):
                if not self.squares[row][col].has_piece():
                    self.squares[row][col].piece = self.selected_red_piece
                    self.selected_red_piece = None
                    self.piece_placed = True
    
    def reset_piece_placement(self):
        if self.piece_placed:
            self.piece_placed = False

    def get_original_position_black(self, piece):
        return self.original_positions_black.get(piece, None)
    
    def get_original_position_red(self, piece):
        return self.original_positions_red.get(piece, None)

    def return_piece_black_selection(self, row, col):
        if 0 <= row <= 3 and 0 <= col <= 9:
            if self.squares[row][col].has_piece() and self.piece_to_return_black is None:
                self.piece_to_return_black = self.squares[row][col].piece
                self.squares[row][col].piece = None
        
    def return_piece_black_return(self, row, col):
        if self.piece_to_return_black is not None and self.piece_to_return_black.color == "black":
            original_position = self.get_original_position_black(self.piece_to_return_black)
            if (row, col) == original_position:
                self.squares[row][col].piece = self.piece_to_return_black
                self.squares[row][col].number += 1
                self.piece_placed = False
                self.piece_to_return_black = None  

    def return_piece_red_selection(self, row, col):
        if 6 <= row <= 9 and 0 <= col <= 9:
            if self.squares[row][col].has_piece() and self.piece_to_return_red is None:
                self.piece_to_return_red = self.squares[row][col].piece
                self.squares[row][col].piece = None

    def return_piece_red_return(self, row, col):         
        if self.piece_to_return_red is not None and self.piece_to_return_red.color == "red":
            original_position = self.get_original_position_red(self.piece_to_return_red)
            if (row, col) == original_position:
                self.squares[row][col].piece = self.piece_to_return_red
                self.squares[row][col].number += 1
                self.piece_placed = False
                self.piece_to_return_red = None 
    
    def update_move_history(self, piece, start, end):
        if piece not in self.move_history:
            self.move_history[piece] = []
        self.move_history[piece].append((start, end))

        if len(self.move_history[piece]) > 3:
            self.move_history[piece].pop(0)

        if len(self.move_history[piece]) == 3:
            if self.move_history[piece][0][0] == self.move_history[piece][2][1] and \
            self.move_history[piece][1][0] == self.move_history[piece][2][1] and \
            self.move_history[piece][0][1] == self.move_history[piece][1][1] == self.move_history[piece][2][0]:
                return False
        return True
    
    def valid_move(self, startx, starty, endx, endy, piece):
        startx, starty, endx, endy = map(int, (startx, starty, endx, endy))
    
        if 10 <= endx <= 12:
            return False
        
        if (endy, endx) in SPECIAL_POSITION:
            return False
        
        if piece.rank == 0 or piece.rank == 1:  # Flag or Bomb
            return False
    
        if piece.rank != 10:  # Not a Scout
            if abs(startx - endx) + abs(starty - endy) != 1:
                return False
    
        if self.squares[endy][endx].has_piece() and self.squares[endy][endx].piece.color == piece.color:
            return False
        
        if piece.rank == 10:  # Scout
            if startx != endx and starty != endy:
                return False  # Prevent diagonal movement

            dx = 1 if endx > startx else -1 if endx < startx else 0
            dy = 1 if endy > starty else -1 if endy < starty else 0
            
            # Only allow movement in one direction at a time (horizontal or vertical)
            if abs(dx) + abs(dy) != 1:
                return False

            x, y = startx + dx, starty + dy
            while (x, y) != (endx, endy):
                if self.squares[y][x].has_piece():
                    return False
                x += dx
                y += dy
        
        if piece in self.move_history:
            if self.move_history[piece].count(((startx, starty), (endx, endy))) >= 2:
                return False
            
        return True

    def move_piece(self, startx, starty, endx, endy, current_player):
        startx, starty, endx, endy = map(int, (startx, starty, endx, endy))

        start_square = self.squares[starty][startx]
        end_square = self.squares[endy][endx]
    
        if not start_square.has_piece():
            return False
        
        piece = start_square.piece
        if piece.color != current_player:
            return False
        
        if self.valid_move(startx, starty, endx, endy, piece):
            if end_square.has_piece():
                if end_square.piece.color != piece.color:
                    combat_result = self.combat(piece, end_square.piece, startx, starty, endx, endy)
                    if combat_result:
                        self.update_move_history(piece, (startx, starty), (endx, endy))
                        self.show_valid_moves_flag = False
                        return True, combat_result
                else:
                    return False
            else:
                end_square.piece = piece
                start_square.piece = None
                self.update_move_history(piece, (startx, starty), (endx, endy))
                self.show_valid_moves_flag = False

            win_result = self.check_win_condition()
            if win_result:
                return True, win_result
        
            return True

        return False

    def combat(self, attacker, defender, attackerx, attackery, defenderx, defendery):
        attackerx ,attackery, defenderx, defendery = map(int, (attackerx ,attackery, defenderx, defendery))

        attacker = self.squares[attackery][attackerx].piece
        defender = self.squares[defendery][defenderx].piece

        if attacker is not None and defender is not None:
            
            if defender.rank == 1:
                self.squares[defendery][defenderx].piece = attacker
                self.squares[attackery][attackerx].piece = None

            #Miner > Bomb
            if attacker.rank == 9 and defender.rank == 0:
                if attacker.color == "red" and defender.color == "black":
                    original_position = self.get_original_position_black(self.squares[defendery][defenderx].piece)
                    defendery_original, defenderx_original = original_position
                    self.squares[defendery_original][defenderx_original].piece = defender
                    self.squares[defendery_original][defenderx_original].number += 1
                    self.squares[defendery][defenderx].piece  = attacker
                    self.squares[attackery][attackerx].piece = None
                    
                if attacker.color == "black" and defender.color == "red":
                    original_position = self.get_original_position_red(self.squares[defendery][defenderx].piece)
                    defendery_original, defenderx_original = original_position
                    self.squares[defendery_original][defenderx_original].piece = defender
                    self.squares[defendery_original][defenderx_original].number += 1
                    self.squares[defendery][defenderx].piece  = attacker
                    self.squares[attackery][attackerx].piece = None

            #Spy > Marshal    
            elif attacker.rank == 11 and defender.rank == 2:
                if attacker.color == "red" and defender.color == "black":
                    original_position = self.get_original_position_black(self.squares[defendery][defenderx].piece)
                    defendery_original, defenderx_original = original_position
                    self.squares[defendery_original][defenderx_original].piece = defender
                    self.squares[defendery_original][defenderx_original].number += 1
                    self.squares[defendery][defenderx].piece  = attacker
                    self.squares[attackery][attackerx].piece = None
                    
                if attacker.color == "black" and defender.color == "red":
                    original_position = self.get_original_position_red(self.squares[defendery][defenderx].piece)
                    defendery_original, defenderx_original = original_position
                    self.squares[defendery_original][defenderx_original].piece = defender
                    self.squares[defendery_original][defenderx_original].number += 1
                    self.squares[defendery][defenderx].piece  = attacker
                    self.squares[attackery][attackerx].piece = None
            
            #Marshal < Spy
            elif attacker.rank == 2 and defender.rank == 11:
                if attacker.color == "red" and defender.color == "black":
                    original_position = self.get_original_position_black(self.squares[attackery][attackerx].piece)
                    attackery_original, attackerx_original = original_position
                    self.squares[attackery_original][attackerx_original].piece = attacker
                    self.squares[defendery_original][defenderx_original].number += 1
                    self.squares[attackery][attackerx].piece = None
                    
                if attacker.color == "black" and defender.color == "red":
                    original_position = self.get_original_position_red(self.squares[defendery][defenderx].piece)
                    attackery_original, attackerx_original = original_position
                    self.squares[attackery_original][attackerx_original].piece = attacker
                    self.squares[defendery_original][defenderx_original].number += 1
                    self.squares[attackery][attackerx].piece = None

            elif attacker.rank < defender.rank:
                if attacker.color == "red" and defender.color == "black":
                    original_position = self.get_original_position_black(self.squares[defendery][defenderx].piece)
                    defendery_original, defenderx_original = original_position
                    self.squares[defendery_original][defenderx_original].piece = defender
                    self.squares[defendery_original][defenderx_original].number += 1
                    self.squares[defendery][defenderx].piece  = attacker
                    self.squares[attackery][attackerx].piece = None
                    
                if attacker.color == "black" and defender.color == "red":
                    original_position = self.get_original_position_red(self.squares[defendery][defenderx].piece)
                    defendery_original, defenderx_original = original_position
                    self.squares[defendery_original][defenderx_original].piece = defender
                    self.squares[defendery_original][defenderx_original].number += 1
                    self.squares[defendery][defenderx].piece  = attacker
                    self.squares[attackery][attackerx].piece = None

            elif attacker.rank > defender.rank:
                if attacker.color == "red" and defender.color == "black":
                    original_position = self.get_original_position_red(self.squares[attackery][attackerx].piece)
                    attackery_original, attackerx_original = original_position
                    self.squares[attackery_original][attackerx_original].piece = attacker
                    self.squares[attackery_original][attackerx_original].number += 1
                    self.squares[attackery][attackerx].piece = None
                    
                if attacker.color == "black" and defender.color == "red":
                    original_position = self.get_original_position_black(self.squares[attackery][attackerx].piece)
                    attackery_original, attackerx_original = original_position
                    self.squares[attackery_original][attackerx_original].piece = attacker
                    self.squares[attackery_original][attackerx_original].number += 1
                    self.squares[attackery][attackerx].piece = None

            #Attacker.rank = Defender.rank
            else:
                if attacker.color == "red" and defender.color == "black":
                    original_position1 = self.get_original_position_red(self.squares[attackery][attackerx].piece)
                    attackery_original, attackerx_original = original_position1
                    original_position2 = self.get_original_position_black(self.squares[defendery][defenderx].piece)
                    defendery_original, defenderx_original = original_position2
                    self.squares[attackery_original][attackerx_original].piece = attacker
                    self.squares[attackery_original][attackerx_original].number += 1
                    self.squares[defendery_original][defenderx_original].piece = defender
                    self.squares[defendery_original][defenderx_original].number += 1
                    self.squares[attackery][attackerx].piece = None
                    self.squares[defendery][defenderx].piece = None
                    
                if attacker.color == "black" and defender.color == "red":
                    original_position1 = self.get_original_position_black(self.squares[attackery][attackerx].piece)
                    attackery_original, attackerx_original = original_position1
                    original_position2 = self.get_original_position_red(self.squares[defendery][defenderx].piece)
                    defendery_original, defenderx_original = original_position2
                    self.squares[attackery_original][attackerx_original].piece = attacker
                    self.squares[attackery_original][attackerx_original].number += 1
                    self.squares[defendery_original][defenderx_original].piece = defender
                    self.squares[defendery_original][defenderx_original].number += 1
                    self.squares[attackery][attackerx].piece = None
                    self.squares[defendery][defenderx].piece = None

        return None
    
    def select_piece(self, row, col, current_player):
        if self.squares[row][col].has_piece() and self.squares[row][col].piece.color == current_player:
            self.selected_piece = (row, col)

    def check_all_pieces_placed(self):
        return all(square.has_piece() for row in self.squares[:4] for square in row[:10]) and all(square.has_piece() for row in self.squares[6:] for square in row[:10])
    
    def check_win_condition(self):
        black_flag_found = False
        red_flag_found = False
        black_pieces_remaining = False
        red_pieces_remaining = False

        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece():
                    piece = self.squares[row][col].piece
                    if piece.rank == 1:  # Flag
                        if piece.color == "black":
                            black_flag_found = True
                        else:
                            red_flag_found = True
                    elif piece.rank not in [0, 1]:  # Not Bomb or Flag
                        if piece.color == "black":
                            black_pieces_remaining = True
                        else:
                            red_pieces_remaining = True

        if not black_flag_found:
            return "Red wins by capturing the black flag!"
        elif not red_flag_found:
            return "Black wins by capturing the red flag!"
        elif not black_pieces_remaining:
            return "Red wins! Black has no movable pieces left."
        elif not red_pieces_remaining:
            return "Black wins! Red has no movable pieces left."
        else:
            return None
        
    def select_piece(self, row, col, current_player):
        if self.squares[row][col].has_piece() and self.squares[row][col].piece.color == current_player:
            self.selected_piece = (row, col)
            return True
        return False
    
    def handle_placement(self, button, row, col):
        if button == 1:
            if (0 <= row <= 3) and (10 <= col <= 12):
                self.handle_black_piece_selection(row, col)
                return (row, col)
            
            if (0 <= row <= 3) and (0 <= col <= 9):
                self.handle_black_piece_placement(row, col)
                self.reset_piece_placement()
                return None
            
            if (6 <= row <= 9) and (10 <= col <= 12):
                self.handle_red_piece_selection(row, col)
                return (row, col)
            
            if (6 <= row <= 9) and (0 <= col <= 9):
                self.handle_red_piece_placement(row, col)
                self.reset_piece_placement()
                return None
                
        elif button == 3:
            if (0 <= row <= 3) and (0 <= col <= 9):
                self.return_piece_black_selection(row, col)
                return (row, col)
        
            if (0 <= row <= 3) and (10 <= col <= 12):
                original_position = self.get_original_position_black(self.piece_to_return_black)
                if original_position == (row, col):
                    self.return_piece_black_return(row, col)
                    return None
                
            if (6 <= row <= 9) and (0 <= col <= 9):
                self.return_piece_red_selection(row, col)
                return (row, col)
        
            if (6 <= row <= 9) and (10 <= col <= 12):
                original_position = self.get_original_position_red(self.piece_to_return_red)
                if original_position == (row, col):
                    self.return_piece_red_return(row, col)
                    return None

        return None

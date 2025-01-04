from square import Square
from piece import *
from const import *

class Boardgame:

    def __init__(self):
        self.squares = [[Square(row, col) for col in range(COLS)] for row in range(ROWS)]
        self._create()
        self._add_pieces_black("black")
        self._add_pieces_red("red")
        self.selected_piece = None
        self.selected_black_piece = None
        self.selected_red_piece = None
        self.piece_placed = False
        self.piece_to_return_black = None
        self.piece_to_return_red = None

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
    
    def _add_pieces_black(self, color):
        self.squares[0][10] = Square(0, 0, 6, Bomb(color))
        self.squares[1][10] = Square(1, 0, 1, Marshal(color))
        self.squares[2][10] = Square(2, 0, 1, General(color))
        self.squares[3][10] = Square(3, 0, 2, Colonel(color))
        self.squares[0][11] = Square(0, 1, 3, Major(color))
        self.squares[1][11] = Square(1, 1, 4, Captain(color))
        self.squares[2][11] = Square(2, 1, 4, Lieutenant(color))
        self.squares[3][11] = Square(3, 1, 4, Sergeant(color))
        self.squares[0][12] = Square(0, 2, 5, Miner(color))
        self.squares[1][12] = Square(1, 2, 8, Scout(color))
        self.squares[2][12] = Square(2, 2, 1, Spy(color))
        self.squares[3][12] = Square(3, 2, 1, Flag(color))

    def _add_pieces_red(self, color):
        self.squares[6][10] = Square(0, 0, 6, Bomb(color))
        self.squares[7][10] = Square(1, 0, 1, Marshal(color))
        self.squares[8][10] = Square(2, 0, 1, General(color))
        self.squares[9][10] = Square(3, 0, 2, Colonel(color))
        self.squares[6][11] = Square(0, 1, 3, Major(color))
        self.squares[7][11] = Square(1, 1, 4, Captain(color))
        self.squares[8][11] = Square(2, 1, 4, Lieutenant(color))
        self.squares[9][11] = Square(3, 1, 4, Sergeant(color))
        self.squares[6][12] = Square(0, 2, 5, Miner(color))
        self.squares[7][12] = Square(1, 2, 8, Scout(color))
        self.squares[8][12] = Square(2, 2, 1, Spy(color))
        self.squares[9][12] = Square(3, 2, 1, Flag(color))
        
    def handle_black_piece_selection(self, row, col):
        if not self.selected_black_piece and not self.piece_placed:
            if (0 <= row <= 3) and (10 <= col <= 12):
                if self.squares[row][col].has_piece():
                    piece = self.squares[row][col].piece

                    if piece.color == "black":
                        if self.squares[row][col].number > 0:
                            self.squares[row][col].number -= 1
                            self.selected_black_piece = piece

                        if self.squares[row][col].number == 0:
                            self.squares[row][col].piece = None

    def handle_black_piece_placement(self, row, col):
        if self.selected_black_piece:
            if (0 <= row <= 3) and (0 <= col <= 9):
                if not self.squares[row][col].has_piece():
                    self.squares[row][col].piece = self.selected_black_piece
                    self.selected_black_piece = None
                    self.piece_placed = True

    def handle_red_piece_selection(self, row, col):
        if not self.selected_red_piece and not self.piece_placed:
            if (6 <= row <= 9) and (10 <= col <= 12):
                if self.squares[row][col].has_piece():
                    piece = self.squares[row][col].piece
                    
                    if piece.color == "red":
                        if self.squares[row][col].number > 0:
                            self.squares[row][col].number -= 1
                            self.selected_red_piece = piece

                        if self.squares[row][col].number == 0:
                            self.squares[row][col].piece = None

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
        piece_positions = {
            Bomb: (0, 10),
            Marshal: (1, 10),
            General: (2, 10),
            Colonel: (3, 10),
            Major: (0, 11),
            Captain: (1, 11),
            Lieutenant: (2, 11),
            Sergeant: (3, 11),
            Miner: (0, 12),
            Scout: (1, 12),
            Spy: (2, 12),
            Flag: (3, 12)
        }
        return piece_positions.get(type(piece), None)

    def return_piece_black_selction(self, row, col):
        if 0 <= row <= 3 and 0 <= col <= 9:
            if self.squares[row][col].has_piece():
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

    def return_piece_red_selction(self, row, col):
        if 6 <= row <= 9 and 0 <= col <= 9:
            if self.squares[row][col].has_piece():
                self.piece_to_return_red = self.squares[row][col].piece
                self.squares[row][col].piece = None

    def return_piece_red_return(self, row, col):         
        if self.piece_to_return_red is not None and self.piece_to_return_red.color == "red" and (6 <= row <= 9 and 10 <= col <= 12):
            self.squares[row][col].piece = self.piece_to_return_red 
            self.squares[row][col].number += 1
            self.piece_placed = False
            self.piece_to_return_red = None
    
    def valid_move(self, startx, starty, endx, endy, piece):
        startx, starty, endx, endy = map(int, (startx, starty, endx, endy))
    
        if piece.rank == 0 or piece.rank == 1:  # Flag or Bomb
            return False
    
        if piece.rank != 10:  # Not a Scout
            if abs(startx - endx) + abs(starty - endy) != 1:
                return False
    
        if self.squares[endy][endx].has_piece() and self.squares[endy][endx].piece.color == piece.color:
            return False
        
        if piece.rank == 10:  # Scout
            dx = 1 if endx > startx else -1 if endx < startx else 0
            dy = 1 if endy > starty else -1 if endy < starty else 0
            x, y = startx + dx, starty + dy
            while (x, y) != (endx, endy):
                if self.squares[y][x].has_piece():
                    return False
                x += dx
                y += dy
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
                    self.combat(piece, end_square.piece, startx, starty, endx, endy)
                else:
                    return False
            else:
                end_square.piece = piece
                start_square.piece = None
            return True
        return False

    def combat(self, attacker, defender, attackerx, attackery, defenderx, defendery):
        attackerx ,attackery, defenderx, defendery = map(int, (attackerx ,attackery, defenderx, defendery))

        attacker = self.squares[attackery][attackerx].piece
        defender = self.squares[defendery][defenderx].piece

        if attacker is not None and defender is not None:
            if attacker.rank == 9 and defender.rank == 0:
                self.squares[defendery][defenderx].piece  = attacker
                self.squares[attackery][attackerx].piece = None

            #Marshal against Spy
            elif attacker.rank == 11 and defender.rank == 2: 
                self.squares[defendery][defenderx].piece = attacker
                self.squares[attackery][attackerx].piece = None
            
            elif attacker.rank == 2 and defender.rank == 11:
                self.squares[defendery][defenderx].piece = defender
                self.squares[attackery][attackerx].piece = None

            elif defender.rank == 1: 
                self.squares[defendery][defenderx].piece = attacker
                self.squares[attackery][attackerx].piece = None

            elif attacker.rank < defender.rank:
                self.squares[defendery][defenderx].piece = attacker
                self.squares[attackery][attackerx].piece = None

            elif attacker.rank > defender.rank:
                self.squares[attackery][attackerx].piece = None

            else:
                self.squares[defendery][defenderx].piece = None
                self.squares[attackery][attackerx].piece = None
    
    def select_piece(self, row, col, current_player):
        if self.squares[row][col].has_piece() and self.squares[row][col].piece.color == current_player:
            self.selected_piece = (row, col)

    def check_all_pieces_placed(self):
        return all(square.has_piece() for row in self.squares[:4] for square in row[:10]) and all(square.has_piece() for row in self.squares[6:] for square in row[:10])



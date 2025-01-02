class Square:

    def __init__(self, row, col, number = None, piece = None):
        self.row = row
        self.col = col
        self.piece = piece
        self.number = number

    def has_piece(self):
        return self.piece != None

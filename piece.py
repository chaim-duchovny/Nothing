import os

class Piece:

    def __init__(self, name, color, rank, player = None, texture = None, texture_rect = None):
        self.name = name
        self.color = color
        self.rank = rank
        self.player = player
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self):
        self.texture = os.path.join(f"assets/images/{self.color}/{self.color}-{self.name}.png")

class Bomb(Piece):
    
    def __init__(self, color):
        super().__init__("Bomb", color, 0)

class Marshal(Piece):

    def __init__(self, color):
        super().__init__("Marshal", color, 2)
        
class General(Piece):

    def __init__(self, color):
        super().__init__("General", color, 3)
        
class Colonel(Piece):

    def __init__(self, color):
        super().__init__("Colonel", color, 4)
        
class Major(Piece):

    def __init__(self, color):
        super().__init__("Major", color, 5)
        
class Captain(Piece):

    def __init__(self, color):
        super().__init__("Captain", color, 6)
        
class Lieutenant(Piece):

    def __init__(self, color):
        super().__init__("Lieutenant", color, 7)
        
class Sergeant(Piece):

    def __init__(self, color):
        super().__init__("Sergeant", color, 8)
        
class Miner(Piece):

    def __init__(self, color):
        super().__init__("Miner", color, 9)
        
class Scout(Piece):

    def __init__(self, color):
        super().__init__("Scout", color, 10)
        
class Spy(Piece):

    def __init__(self, color):
        super().__init__("Spy", color, 11)
        
class Flag(Piece):

    def __init__(self, color):
        super().__init__("Flag", color, 1)
        




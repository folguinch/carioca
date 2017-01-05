from .cards import Hand, Down

class Player:

    def __init__(self, name):
        self.name = name
        self.hand = None
        self.down = None

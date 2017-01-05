from utils import *

class Card:

    def __init__(self, value, suit):
        """
        Create a card.
        Input:
        ------
            value: int, str
                Card value ('W' for joker)
            suit: str or None
                Card suit ('spades', 'hearts', 'diamonds', 'stars',
                'black_joker', 'red_joker')
        """
        # Check card

        # Define card
        self.value = value
        self.suit = suit

    def __str__(self):
        if self.value != 'W':
            return (SUITS_UNICODE[self.suit] % self.value).encode('utf-8',
                    'replace')
        else:
            return SUITS_UNICODE[self.suit].encode('utf-8','replace')

class Cards(list):

    def __init__(self, *args):
        super(Cards, self).__init__([Card(*arg) for arg in args])

    def __str__(self):
        return '  '.join(map(str,self))

if __name__=='__main__':
    a = Card('A', 'hearts')
    print a

    b = Cards(('A','hearts'),(10,'hearts'),('W','red_joker'))
    print b

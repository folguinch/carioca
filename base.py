import json

from .utils import *

def decode_card(load):
    return Card(*json.loads(load))

class Card(tuple):

    def __new__(cls, value, suit):
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
        validate_card(value, suit)

        # Define card
        #super(Card, self).__init__((value, suit))
        return tuple.__new__(cls, (value, suit))

    def __str__(self):
        if self.value != 'W':
            return (SUITS_UNICODE[self.suit] % self.value).encode('utf-8',
                    'replace')
        else:
            return SUITS_UNICODE[self.suit].encode('utf-8','replace')

    @property
    def value(self):
        return self[0]

    @property
    def suit(self):
        return self[1]

    def encode(self):
        return json.dumps(self)

class Cards(list):

    def __init__(self, *args):
        super(Cards, self).__init__([Card(*arg) for arg in args])

    def __str__(self):
        return '  '.join(map(str,self))

    def sort(self, pattern=None):
        if pattern is None:
            super(Cards, self).sort(key=sort_cards_key)
        else:
            super(Cards, self).sort(key=lambda x: pattern.index(x))

    @property
    def values(self):
        return [card.value for card in self]

    def encode(self):
        return json.dumps(self)

    def decode(self, load):
        self.__init__(*json.loads(load))

    def values_as_str(self):
        return map(lambda x: str(x)[0], self.values)

if __name__=='__main__':
    a = Card('A', 'hearts')
    print a

    b = Cards(('A','hearts'),(10,'hearts'),('W','red_joker'), a)
    print b

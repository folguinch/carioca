import random

from .base import Cards
from .utils import get_deck

class Deck(Cards):

    def __init__(self, ndecks=2, game=''):
        if game != 'RS':
            cards = get_deck(ndecks)
        else:
            # Do not include the joker in real straight
            cards = get_deck(ndecks, False)
        super(Deck, self).__init__(*cards)

    def shuffle(self):
        random.shuffle(self)

class Discard(list):
    pass

class Hand(Cards):
    pass

    #def __init__(self, cards, nmax=12):
    #    self.nmax = nmax
    #    super(Hand, self).__init__(*cards)

class Down(Cards):
    pass

import random

from .base import Cards

class Deck(Cards):

    def __init__(self, ndecks=2):
        cards = get_deck(ndecks)
        super(Deck, self).__init__(*cards)

    def shuffle(self):
        random.shuffle(self)

class Discard(list):
    pass

class Hand(Cards):

    def __init__(self, cards, nmax=12):
        self.nmax = nmax
        super(Hand, self).__init__(*cards)

class Down(Cards):
    pass

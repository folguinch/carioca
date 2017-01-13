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
    def lower_three(self, cards):
        low = Down()
        value = None
        wildcards = 0

        # Validate and lower
        for i in cards:
            if self[i].value=='W':
                wildcards += 1
                if wildcards > 1:
                    break
                else:
                    low.append(self[i])
                    self[i] = None
                    continue
            elif value is None:
                value = self[i].value
                low.append(self[i])
                self[i] = None
            elif self[i].value == value:
                low.append(self[i])
                self[i] = None
            else:
                break

        if len(low)==3:
            self = filter(lambda x: x is not None, self)
            return low
        else:
            for i, card in zip(cards, low):
                self[i] = card
            return []


    #def __init__(self, cards, nmax=12):
    #    self.nmax = nmax
    #    super(Hand, self).__init__(*cards)

class Down(Cards):
    pass


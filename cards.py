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

    def compact(self):
        self = filter(lambda x: x is not None, self)

    def unlower(self, cards, low):
        for i, card in zip(cards, low):
            self[i] = card

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
            self.compact()
            return low
        else:
            self.unlower(cards, low)
            return []

    def lower_straight(self, cards):
        low = Down()
        suit = None
        wildcards = 0

        # Validate suit and wildcards:
        for i in cards:
            if self[i].value=='W':
                wildcards +=1
                if wildcards > 1:
                    break
                else:
                    low.append(self[i])
                    self.[i] = None
                    continue
            elif suit is None:
                suit = self[i].suit
                low.append(self[i])
                self[i] = None
            elif self[i].suit == suit:
                low.append(self[i])
                self[i] = None
            else:
                break

        if len(low)==4:
            # Sort and check the stright
            self.compact()
            return low
        else:
            self.unlower(cards, low)
            return []


    #def __init__(self, cards, nmax=12):
    #    self.nmax = nmax
    #    super(Hand, self).__init__(*cards)

class Down(Cards):
    pass

